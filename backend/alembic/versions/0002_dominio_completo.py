"""Dominio completo: restaurant, mesa extendida, turnos, calendario, reserva, admin.

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "restaurant",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.Text(), nullable=False),
        sa.Column("max_reservas_por_dia", sa.Integer(), nullable=False, server_default="25"),
        sa.Column("capacidad_maxima_grupo", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("onboarding_completado", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.Text(),
            nullable=False,
            server_default=sa.text("(datetime('now'))"),
        ),
        sa.CheckConstraint("max_reservas_por_dia > 0", name="max_reservas_positivo"),
        sa.CheckConstraint("capacidad_maxima_grupo > 0", name="capacidad_grupo_positiva"),
    )
    op.create_index("ix_restaurant_tenant_id", "restaurant", ["tenant_id"])
    op.execute("INSERT INTO restaurant (id, nombre) VALUES (1, 'Mi Restaurante')")

    with op.batch_alter_table("mesa", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("restaurant_id", sa.Integer(), nullable=False, server_default="1")
        )
        batch_op.add_column(sa.Column("pos_x", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("pos_y", sa.Float(), nullable=True))
        batch_op.create_foreign_key(
            "fk_mesa_restaurant", "restaurant", ["restaurant_id"], ["id"]
        )
        batch_op.create_unique_constraint(
            "uq_mesa_restaurant_numero", ["restaurant_id", "numero"]
        )

    op.create_table(
        "turno_config",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurant.id"), nullable=False),
        sa.Column("turno", sa.String(length=10), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("hora_inicio", sa.String(length=5), nullable=True),
        sa.Column("hora_fin", sa.String(length=5), nullable=True),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "turno IN ('MANANA', 'TARDE', 'NOCHE')", name="turno_valido"
        ),
        sa.UniqueConstraint("restaurant_id", "turno", name="uq_turno_restaurant"),
    )
    op.create_index("ix_turno_config_restaurant_id", "turno_config", ["restaurant_id"])
    op.execute(
        """
        INSERT INTO turno_config (restaurant_id, turno, activo) VALUES
            (1, 'MANANA', 1),
            (1, 'TARDE', 1),
            (1, 'NOCHE', 1)
        """
    )

    op.create_table(
        "calendar_day",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurant.id"), nullable=False),
        sa.Column("fecha", sa.String(length=10), nullable=False),
        sa.Column("cerrado", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("nota", sa.Text(), nullable=True),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.UniqueConstraint("restaurant_id", "fecha", name="uq_calendar_restaurant_fecha"),
    )
    op.create_index(
        "ix_calendar_day_restaurant_fecha", "calendar_day", ["restaurant_id", "fecha"]
    )

    op.create_table(
        "reserva",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurant.id"), nullable=False),
        sa.Column("fecha", sa.String(length=10), nullable=False),
        sa.Column("turno", sa.String(length=10), nullable=False),
        sa.Column("mesa_id", sa.Integer(), sa.ForeignKey("mesa.id"), nullable=False),
        sa.Column("cliente", sa.Text(), nullable=False),
        sa.Column("telefono", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("personas", sa.Integer(), nullable=False),
        sa.Column("estado", sa.String(length=10), nullable=False, server_default="activa"),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.Text(),
            nullable=False,
            server_default=sa.text("(datetime('now'))"),
        ),
        sa.CheckConstraint(
            "turno IN ('MANANA', 'TARDE', 'NOCHE')", name="reserva_turno_valido"
        ),
        sa.CheckConstraint("personas > 0", name="personas_positivas"),
        sa.CheckConstraint(
            "estado IN ('activa', 'cancelada')", name="reserva_estado_valido"
        ),
    )
    op.create_index("ix_reserva_restaurant_fecha", "reserva", ["restaurant_id", "fecha"])
    op.create_index(
        "ix_reserva_mesa_fecha_turno", "reserva", ["mesa_id", "fecha", "turno"]
    )

    op.create_table(
        "admin_user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurant.id"), nullable=False),
        sa.Column("email", sa.Text(), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.Text(),
            nullable=False,
            server_default=sa.text("(datetime('now'))"),
        ),
    )
    op.create_index("ix_admin_user_restaurant_id", "admin_user", ["restaurant_id"])


def downgrade() -> None:
    op.drop_index("ix_admin_user_restaurant_id", table_name="admin_user")
    op.drop_table("admin_user")
    op.drop_index("ix_reserva_mesa_fecha_turno", table_name="reserva")
    op.drop_index("ix_reserva_restaurant_fecha", table_name="reserva")
    op.drop_table("reserva")
    op.drop_index("ix_calendar_day_restaurant_fecha", table_name="calendar_day")
    op.drop_table("calendar_day")
    op.drop_index("ix_turno_config_restaurant_id", table_name="turno_config")
    op.drop_table("turno_config")

    with op.batch_alter_table("mesa", schema=None) as batch_op:
        batch_op.drop_constraint("uq_mesa_restaurant_numero", type_="unique")
        batch_op.drop_constraint("fk_mesa_restaurant", type_="foreignkey")
        batch_op.drop_column("pos_y")
        batch_op.drop_column("pos_x")
        batch_op.drop_column("restaurant_id")

    op.drop_index("ix_restaurant_tenant_id", table_name="restaurant")
    op.drop_table("restaurant")
