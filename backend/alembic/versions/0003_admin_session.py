"""Sesiones de admin para autenticación con cookies.

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "admin_session",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token", sa.Text(), nullable=False, unique=True),
        sa.Column("admin_user_id", sa.Integer(), sa.ForeignKey("admin_user.id"), nullable=False),
        sa.Column("expires_at", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.Text(),
            nullable=False,
            server_default=sa.text("(datetime('now'))"),
        ),
    )
    op.create_index("ix_admin_session_token", "admin_session", ["token"], unique=True)
    op.create_index("ix_admin_session_admin_user_id", "admin_session", ["admin_user_id"])


def downgrade() -> None:
    op.drop_index("ix_admin_session_admin_user_id", table_name="admin_session")
    op.drop_index("ix_admin_session_token", table_name="admin_session")
    op.drop_table("admin_session")
