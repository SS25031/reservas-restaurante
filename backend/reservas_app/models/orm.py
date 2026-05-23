"""Modelos ORM (SQLAlchemy 2.0 declarativo).

Los DTOs `Mesa` y `Reserva` (dataclasses) en `models/mesa.py` y
`models/reserva.py` son la representación de dominio; estos modelos ORM
son la representación de persistencia. La capa repository hace el mapeo.
"""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM."""


class RestaurantORM(Base):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    max_reservas_por_dia: Mapped[int] = mapped_column(Integer, nullable=False, default=25)
    capacidad_maxima_grupo: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    onboarding_completado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="(datetime('now'))"
    )

    __table_args__ = (
        CheckConstraint("max_reservas_por_dia > 0", name="max_reservas_positivo"),
        CheckConstraint("capacidad_maxima_grupo > 0", name="capacidad_grupo_positiva"),
    )


class MesaORM(Base):
    """Mesa en la base de datos."""

    __tablename__ = "mesa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("restaurant.id"), nullable=False, index=True
    )
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float | None] = mapped_column(Float, nullable=True)
    pos_y: Mapped[float | None] = mapped_column(Float, nullable=True)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)

    __table_args__ = (
        CheckConstraint("capacidad > 0", name="capacidad_positiva"),
        UniqueConstraint("restaurant_id", "numero", name="uq_mesa_restaurant_numero"),
    )


class TurnoConfigORM(Base):
    __tablename__ = "turno_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("restaurant.id"), nullable=False, index=True
    )
    turno: Mapped[str] = mapped_column(String(10), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    hora_inicio: Mapped[str | None] = mapped_column(String(5), nullable=True)
    hora_fin: Mapped[str | None] = mapped_column(String(5), nullable=True)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("turno IN ('MANANA', 'TARDE', 'NOCHE')", name="turno_valido"),
        UniqueConstraint("restaurant_id", "turno", name="uq_turno_restaurant"),
    )


class CalendarDayORM(Base):
    __tablename__ = "calendar_day"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("restaurant.id"), nullable=False, index=True
    )
    fecha: Mapped[str] = mapped_column(String(10), nullable=False)
    cerrado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    nota: Mapped[str | None] = mapped_column(Text, nullable=True)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("restaurant_id", "fecha", name="uq_calendar_restaurant_fecha"),
    )


class ReservaORM(Base):
    __tablename__ = "reserva"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    restaurant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("restaurant.id"), nullable=False, index=True
    )
    fecha: Mapped[str] = mapped_column(String(10), nullable=False)
    turno: Mapped[str] = mapped_column(String(10), nullable=False)
    mesa_id: Mapped[int] = mapped_column(Integer, ForeignKey("mesa.id"), nullable=False)
    cliente: Mapped[str] = mapped_column(Text, nullable=False)
    telefono: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    personas: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False, default="activa")
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="(datetime('now'))"
    )

    __table_args__ = (
        CheckConstraint("turno IN ('MANANA', 'TARDE', 'NOCHE')", name="reserva_turno_valido"),
        CheckConstraint("personas > 0", name="personas_positivas"),
        CheckConstraint("estado IN ('activa', 'cancelada')", name="reserva_estado_valido"),
    )


class AdminUserORM(Base):
    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("restaurant.id"), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    tenant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[str] = mapped_column(
        Text, nullable=False, server_default="(datetime('now'))"
    )
