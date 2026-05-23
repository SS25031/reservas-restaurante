"""Operaciones admin sobre reservas y configuración."""

from datetime import date

from sqlalchemy.orm import Session

from reservas_app.models import Reserva, Turno
from reservas_app.repositories.sqla_repo import SqlAlchemyReservaRepository
from reservas_app.services.onboarding_service import OnboardingService
from reservas_app.services.reserva_service import ReservaService


class AdminService:
    """Orquesta ReservaService con persistencia SQL para el panel admin."""

    def __init__(self, session: Session, restaurant_id: int = 1):
        self._session = session
        self._restaurant_id = restaurant_id

    def _repo(self) -> SqlAlchemyReservaRepository:
        return SqlAlchemyReservaRepository(self._session, self._restaurant_id)

    def _cargar_servicio(self) -> ReservaService:
        return ReservaService.desde_db(self._session, self._restaurant_id)

    def _persistir(self, servicio: ReservaService) -> None:
        servicio.persistir_en(self._repo())

    def listar_reservas(self) -> list[Reserva]:
        return self._cargar_servicio().todas_las_reservas()

    def obtener_reserva(self, reserva_id: int) -> Reserva:
        return self._cargar_servicio().buscar_por_id(reserva_id)

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
        servicio = self._cargar_servicio()
        reserva = servicio.hacer_reserva(
            cliente=cliente,
            telefono=telefono,
            email=email,
            personas=personas,
            fecha=fecha,
            turno=turno,
        )
        self._persistir(servicio)
        return reserva

    def editar_reserva(
        self,
        reserva_id: int,
        *,
        fecha: date | None = None,
        turno: Turno | None = None,
    ) -> Reserva:
        servicio = self._cargar_servicio()
        actual = servicio.buscar_por_id(reserva_id)
        nueva_fecha = fecha if fecha is not None else actual.fecha
        nuevo_turno = turno if turno is not None else actual.turno
        reserva = servicio.editar_reserva(
            reserva_id,
            nueva_fecha=nueva_fecha,
            nuevo_turno=nuevo_turno,
        )
        self._persistir(servicio)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> None:
        servicio = self._cargar_servicio()
        servicio.cancelar_reserva(reserva_id)
        self._persistir(servicio)

    def reabrir_onboarding(self) -> dict[str, bool]:
        return OnboardingService(self._session, self._restaurant_id).reabrir_onboarding()
