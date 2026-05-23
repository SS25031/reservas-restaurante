"""Reservas públicas: disponibilidad y creación sin autenticación."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas_app.exceptions import (
    DiaCerradoError,
    ReservasPublicasCerradasError,
    TurnoInactivoError,
    ValorInvalidoError,
)
from reservas_app.models import Reserva, Turno
from reservas_app.models.orm import CalendarDayORM, RestaurantORM, TurnoConfigORM
from reservas_app.repositories.sqla_repo import SqlAlchemyReservaRepository
from reservas_app.services.reserva_service import ReservaService


class PublicBookingService:
    """Consulta disponibilidad y crea reservas para clientes públicos."""

    def __init__(self, session: Session, restaurant_id: int = 1):
        self._session = session
        self._restaurant_id = restaurant_id

    def obtener_restaurant(self) -> dict[str, object]:
        restaurant = self._restaurant()
        return {
            "nombre": restaurant.nombre,
            "capacidad_maxima_grupo": restaurant.capacidad_maxima_grupo,
            "acepta_reservas": bool(restaurant.onboarding_completado),
        }

    def consultar_disponibilidad(self, fecha: date, personas: int) -> dict[str, object]:
        self._validar_personas(personas)
        self._validar_fecha_reservable(fecha)
        restaurant = self._restaurant()
        if not restaurant.onboarding_completado:
            raise ReservasPublicasCerradasError(
                "El restaurante aún no acepta reservas en línea."
            )

        calendario = self._dia_calendario(fecha)
        if calendario is not None and calendario.cerrado:
            return {
                "fecha": fecha.isoformat(),
                "personas": personas,
                "cerrado": True,
                "nota": calendario.nota,
                "acepta_reservas": False,
                "turnos": [],
            }

        servicio = self._cargar_servicio()
        cupo_diario = self._cupo_diario_disponible(servicio, fecha)
        turnos = []
        for turno in self._turnos_activos():
            mesas_libres = servicio.mesas_disponibles(fecha, turno)
            aptas = [mesa for mesa in mesas_libres if mesa.puede_acomodar(personas)]
            disponible = cupo_diario and len(aptas) > 0
            turnos.append(
                {
                    "turno": turno.name,
                    "turno_label": turno.value,
                    "disponible": disponible,
                    "mesas_libres": len(aptas),
                }
            )

        return {
            "fecha": fecha.isoformat(),
            "personas": personas,
            "cerrado": False,
            "nota": calendario.nota if calendario is not None else None,
            "acepta_reservas": any(item["disponible"] for item in turnos),
            "turnos": turnos,
        }

    def crear_reserva(
        self,
        *,
        cliente: str,
        telefono: str,
        email: str,
        personas: int,
        fecha: date,
        turno: Turno,
    ) -> Reserva:
        self._validar_fecha_reservable(fecha)
        restaurant = self._restaurant()
        if not restaurant.onboarding_completado:
            raise ReservasPublicasCerradasError(
                "El restaurante aún no acepta reservas en línea."
            )

        calendario = self._dia_calendario(fecha)
        if calendario is not None and calendario.cerrado:
            raise DiaCerradoError(f"El día {fecha.isoformat()} está cerrado para reservas.")

        if turno.name not in {t.name for t in self._turnos_activos()}:
            raise TurnoInactivoError(f"El turno {turno.value} no está disponible.")

        servicio = self._cargar_servicio()
        reserva = servicio.hacer_reserva(
            cliente=cliente,
            telefono=telefono,
            email=email,
            personas=personas,
            fecha=fecha,
            turno=turno,
        )
        servicio.persistir_en(SqlAlchemyReservaRepository(self._session, self._restaurant_id))
        return reserva

    def _restaurant(self) -> RestaurantORM:
        restaurant = self._session.get(RestaurantORM, self._restaurant_id)
        if restaurant is None:
            msg = f"No existe restaurant con id {self._restaurant_id}."
            raise ValorInvalidoError(msg)
        return restaurant

    def _cargar_servicio(self) -> ReservaService:
        return ReservaService.desde_db(self._session, self._restaurant_id)

    def _dia_calendario(self, fecha: date) -> CalendarDayORM | None:
        stmt = select(CalendarDayORM).where(
            CalendarDayORM.restaurant_id == self._restaurant_id,
            CalendarDayORM.fecha == fecha.isoformat(),
        )
        return self._session.scalar(stmt)

    def _turnos_activos(self) -> list[Turno]:
        stmt = (
            select(TurnoConfigORM.turno)
            .where(
                TurnoConfigORM.restaurant_id == self._restaurant_id,
                TurnoConfigORM.activo.is_(True),
            )
            .order_by(TurnoConfigORM.turno)
        )
        return [Turno[nombre] for nombre in self._session.scalars(stmt)]

    @staticmethod
    def _validar_personas(personas: int) -> None:
        if personas < 1:
            raise ValorInvalidoError("La cantidad de personas debe ser ≥ 1.")

    @staticmethod
    def _validar_fecha_reservable(fecha: date) -> None:
        if fecha < date.today():
            raise ValorInvalidoError("No se pueden reservar fechas pasadas.")

    @staticmethod
    def _cupo_diario_disponible(servicio: ReservaService, fecha: date) -> bool:
        reservas_en_dia = sum(
            1 for reserva in servicio.todas_las_reservas() if reserva.fecha == fecha
        )
        return reservas_en_dia < servicio.config.max_reservas_por_dia
