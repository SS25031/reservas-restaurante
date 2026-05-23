"""Migración inicial: tabla mesa.

Revision ID: 0001
Revises:
Create Date: 2026-05-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "mesa",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("numero", sa.Integer(), nullable=False, unique=True),
        sa.Column("capacidad", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("capacidad > 0", name="capacidad_positiva"),
    )
    op.create_index("ix_mesa_tenant_id", "mesa", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_mesa_tenant_id", table_name="mesa")
    op.drop_table("mesa")
