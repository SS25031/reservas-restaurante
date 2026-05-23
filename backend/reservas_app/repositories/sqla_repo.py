"""Repositorio de reservas respaldado por SQLAlchemy."""

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from reservas_app.models import Reserva
from reservas_app.models.mappers import reserva_dto_a_orm, reserva_orm_a_dto
from reservas_app.models.orm import MesaORM, ReservaORM
from reservas_app.models.reserva import EstadoReserva


class SqlAlchemyReservaRepository:
    """Persistencia de reservas vía SQLAlchemy."""

    def __init__(self, session: Session, restaurant_id: int = 1):
        self._session = session
        self._restaurant_id = restaurant_id

    def cargar(self) -> tuple[list[Reserva], int]:
        stmt = (
            select(ReservaORM, MesaORM.numero)
            .join(MesaORM, ReservaORM.mesa_id == MesaORM.id)
            .where(
                ReservaORM.restaurant_id == self._restaurant_id,
                ReservaORM.estado == EstadoReserva.ACTIVA.value,
            )
            .order_by(ReservaORM.id)
        )
        rows = self._session.execute(stmt).all()
        reservas = [reserva_orm_a_dto(orm, numero) for orm, numero in rows]

        ultimo_id = self._session.scalar(
            select(func.max(ReservaORM.id)).where(ReservaORM.restaurant_id == self._restaurant_id)
        )
        return reservas, ultimo_id or 0

    def guardar(self, reservas: list[Reserva], ultimo_id: int) -> None:
        del ultimo_id  # el ID máximo se infiere de las filas; el Protocol lo exige.
        self._session.execute(
            delete(ReservaORM).where(ReservaORM.restaurant_id == self._restaurant_id)
        )
        for reserva in reservas:
            mesa_id = self._mesa_id_por_numero(reserva.numero_mesa)
            if mesa_id is None:
                msg = f"No existe mesa con número {reserva.numero_mesa}."
                raise ValueError(msg)
            self._session.add(reserva_dto_a_orm(reserva, mesa_id, self._restaurant_id))
        self._session.commit()

    def _mesa_id_por_numero(self, numero: int) -> int | None:
        stmt = select(MesaORM.id).where(
            MesaORM.restaurant_id == self._restaurant_id,
            MesaORM.numero == numero,
        )
        return self._session.scalar(stmt)
