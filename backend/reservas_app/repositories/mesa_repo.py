"""Repositorio de mesas respaldado por SQLAlchemy."""

from typing import Protocol

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from reservas_app.models import Mesa
from reservas_app.models.mappers import mesa_dto_a_orm, mesa_orm_a_dto
from reservas_app.models.orm import MesaORM


class MesaRepository(Protocol):
    """Backend de persistencia para el layout de mesas."""

    def listar(self) -> list[Mesa]:
        """Devuelve las mesas del restaurante ordenadas por número."""
        ...

    def reemplazar_todas(self, mesas: list[Mesa]) -> None:
        """Reemplaza atómicamente el layout completo de mesas."""
        ...


class SqlAlchemyMesaRepository:
    """Persistencia de mesas vía SQLAlchemy."""

    def __init__(self, session: Session, restaurant_id: int = 1):
        self._session = session
        self._restaurant_id = restaurant_id

    def listar(self) -> list[Mesa]:
        stmt = (
            select(MesaORM)
            .where(MesaORM.restaurant_id == self._restaurant_id)
            .order_by(MesaORM.numero)
        )
        return [mesa_orm_a_dto(row) for row in self._session.scalars(stmt)]

    def reemplazar_todas(self, mesas: list[Mesa]) -> None:
        self._session.execute(delete(MesaORM).where(MesaORM.restaurant_id == self._restaurant_id))
        for mesa in mesas:
            self._session.add(mesa_dto_a_orm(mesa, self._restaurant_id))
        self._session.commit()

    def contar(self) -> int:
        stmt = select(MesaORM).where(MesaORM.restaurant_id == self._restaurant_id)
        return len(self._session.scalars(stmt).all())
