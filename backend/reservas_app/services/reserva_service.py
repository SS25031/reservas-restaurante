"""Business logic for restaurant reservations.

All methods that can fail raise a subclass of `ReservaError`. The UI layer
is responsible for catching these and presenting friendly messages.
"""

from collections.abc import Iterable
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from reservas_app.config import Configuracion
from reservas_app.exceptions import (
    CapacidadInsuficienteError,
    ConflictoHorarioError,
    LimiteDiarioExcedidoError,
    MesaNoDisponibleError,
    ReservaNoEncontradaError,
    ValorInvalidoError,
)
from reservas_app.models import Mesa, Reserva, Turno
from reservas_app.models.orm import RestaurantORM
from reservas_app.models.reserva import EstadoReserva
from reservas_app.repositories.mesa_repo import SqlAlchemyMesaRepository
from reservas_app.repositories.sqla_repo import SqlAlchemyReservaRepository

if TYPE_CHECKING:
    from reservas_app.repositories.base import ReservaRepository


class ReservaService:
    """Maintains an in-memory collection of reservations against a fixed table layout."""

    def __init__(
        self,
        mesas: Iterable[Mesa],
        config: Configuracion | None = None,
        reservas_iniciales: list[Reserva] | None = None,
        ultimo_id: int = 0,
    ):
        self.mesas: list[Mesa] = list(mesas)
        self.config: Configuracion = config or Configuracion()
        self._reservas: list[Reserva] = list(reservas_iniciales or [])
        self._contador_id: int = ultimo_id

    # ---------------- Read helpers ----------------

    @property
    def total_reservas(self) -> int:
        return len(self._reservas_activas())

    @property
    def ultimo_id(self) -> int:
        return self._contador_id

    def todas_las_reservas(self) -> list[Reserva]:
        """Returns active reservations sorted by fecha, turno, numero_mesa."""
        return sorted(
            self._reservas_activas(),
            key=lambda r: (r.fecha, r.turno.name, r.numero_mesa),
        )

    def buscar_por_id(self, reserva_id: int) -> Reserva:
        for r in self._reservas:
            if r.id == reserva_id:
                return r
        raise ReservaNoEncontradaError(f"No existe una reserva con id {reserva_id}.")

    def mesas_disponibles(self, fecha: date, turno: Turno) -> list[Mesa]:
        ocupadas = self._mesas_ocupadas(fecha, turno)
        return [m for m in self.mesas if m.numero not in ocupadas]

    # ---------------- Mutations ----------------

    def hacer_reserva(
        self,
        *,
        cliente: str,
        telefono: str,
        email: str,
        personas: int,
        fecha: date,
        turno: Turno,
    ) -> Reserva:
        self._validar_cliente(cliente)
        self._validar_email(email)
        self._validar_personas(personas)

        if not any(m.puede_acomodar(personas) for m in self.mesas):
            raise CapacidadInsuficienteError(f"Ninguna mesa puede acomodar a {personas} personas.")

        if self._reservas_en_dia(fecha) >= self.config.max_reservas_por_dia:
            raise LimiteDiarioExcedidoError(
                f"El día {fecha.isoformat()} ya alcanzó el límite de "
                f"{self.config.max_reservas_por_dia} reservas."
            )

        mesa = self._primera_mesa_libre(personas, fecha, turno)
        if mesa is None:
            raise MesaNoDisponibleError(
                "No hay mesas disponibles del tamaño requerido para esa fecha y turno."
            )

        self._contador_id += 1
        reserva = Reserva(
            id=self._contador_id,
            fecha=fecha,
            turno=turno,
            numero_mesa=mesa.numero,
            cliente=cliente,
            telefono=telefono,
            email=email,
            personas=personas,
        )
        self._reservas.append(reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> None:
        reserva = self.buscar_por_id(reserva_id)
        if not reserva.activa:
            raise ReservaNoEncontradaError(f"No existe una reserva activa con id {reserva_id}.")
        reserva.estado = EstadoReserva.CANCELADA

    def editar_reserva(
        self,
        reserva_id: int,
        *,
        nueva_fecha: date,
        nuevo_turno: Turno,
    ) -> Reserva:
        reserva = self.buscar_por_id(reserva_id)
        if not reserva.activa:
            raise ReservaNoEncontradaError(f"No existe una reserva activa con id {reserva_id}.")

        reservas_en_nuevo_dia = sum(
            1 for r in self._reservas_activas() if r.fecha == nueva_fecha and r.id != reserva_id
        )
        if reservas_en_nuevo_dia >= self.config.max_reservas_por_dia:
            raise LimiteDiarioExcedidoError(
                f"El día {nueva_fecha.isoformat()} ya alcanzó el límite de "
                f"{self.config.max_reservas_por_dia} reservas."
            )

        conflicto = any(
            r.fecha == nueva_fecha
            and r.turno == nuevo_turno
            and r.numero_mesa == reserva.numero_mesa
            and r.id != reserva_id
            for r in self._reservas_activas()
        )
        if conflicto:
            raise ConflictoHorarioError(
                f"La mesa {reserva.numero_mesa} ya está reservada el "
                f"{nueva_fecha.isoformat()} en turno {nuevo_turno.value}."
            )

        reserva.fecha = nueva_fecha
        reserva.turno = nuevo_turno
        return reserva

    # ---------------- Persistence ----------------

    @classmethod
    def cargar_desde(
        cls,
        mesas: Iterable[Mesa],
        repositorio: "ReservaRepository",
        config: Configuracion | None = None,
    ) -> "ReservaService":
        reservas, ultimo_id = repositorio.cargar()
        return cls(
            mesas=mesas,
            config=config,
            reservas_iniciales=reservas,
            ultimo_id=ultimo_id,
        )

    @classmethod
    def desde_db(cls, session: Session, restaurant_id: int = 1) -> "ReservaService":
        """Construye el servicio cargando mesas y reservas desde la base de datos."""
        mesa_repo = SqlAlchemyMesaRepository(session, restaurant_id)
        reserva_repo = SqlAlchemyReservaRepository(session, restaurant_id)
        restaurant = session.get(RestaurantORM, restaurant_id)
        config = (
            Configuracion(
                max_reservas_por_dia=restaurant.max_reservas_por_dia,
                capacidad_maxima_grupo=restaurant.capacidad_maxima_grupo,
            )
            if restaurant is not None
            else Configuracion()
        )
        return cls.cargar_desde(mesa_repo.listar(), reserva_repo, config)

    def persistir_en(self, repositorio: "ReservaRepository") -> None:
        repositorio.guardar(list(self._reservas), self._contador_id)

    # ---------------- Private helpers ----------------

    def _reservas_activas(self) -> list[Reserva]:
        return [r for r in self._reservas if r.activa]

    def _validar_personas(self, personas: int) -> None:
        if personas < 1:
            raise ValorInvalidoError("La cantidad de personas debe ser ≥ 1.")
        if personas > self.config.capacidad_maxima_grupo:
            raise CapacidadInsuficienteError(
                f"El grupo supera la capacidad máxima ({self.config.capacidad_maxima_grupo})."
            )

    def _validar_cliente(self, cliente: str) -> None:
        if not cliente.strip():
            raise ValorInvalidoError("El nombre del cliente no puede estar vacío.")

    def _validar_email(self, email: str) -> None:
        if not email.strip():
            raise ValorInvalidoError("El correo electrónico no puede estar vacío.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValorInvalidoError("El correo electrónico no es válido.")

    def _mesas_ocupadas(self, fecha: date, turno: Turno) -> set[int]:
        return {
            r.numero_mesa for r in self._reservas_activas() if r.fecha == fecha and r.turno == turno
        }

    def _reservas_en_dia(self, fecha: date) -> int:
        return sum(1 for r in self._reservas_activas() if r.fecha == fecha)

    def _primera_mesa_libre(self, personas: int, fecha: date, turno: Turno) -> Mesa | None:
        ocupadas = self._mesas_ocupadas(fecha, turno)
        for mesa in self.mesas:
            if mesa.puede_acomodar(personas) and mesa.numero not in ocupadas:
                return mesa
        return None
