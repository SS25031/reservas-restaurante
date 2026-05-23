"""Modelos ORM (SQLAlchemy 2.0 declarativo).

Los DTOs `Mesa` y `Reserva` (dataclasses) en `models/mesa.py` y
`models/reserva.py` son la representación de dominio; estos modelos ORM
son la representación de persistencia. La capa repository hace el mapeo.
"""

from sqlalchemy import CheckConstraint, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM."""


class MesaORM(Base):
    """Mesa en la base de datos.

    El campo `tenant_id` es un placeholder para multi-tenant futuro
    (NULL en el modo single-restaurant actual).
    """

    __tablename__ = "mesa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    tenant_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, index=True
    )

    __table_args__ = (
        CheckConstraint("capacidad > 0", name="capacidad_positiva"),
    )
