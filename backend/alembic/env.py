"""Configuración de Alembic.

Conecta el engine y target_metadata de la aplicación para que las
migraciones puedan generar y aplicar cambios contra el schema real.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from reservas_app.config import Configuracion
from reservas_app.models.orm import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override de la URL desde la configuración de la aplicación (que respeta DATABASE_URL).
config.set_main_option("sqlalchemy.url", Configuracion().database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Migraciones en modo offline (genera SQL sin conexión)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migraciones en modo online (conecta y aplica)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
