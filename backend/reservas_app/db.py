"""Capa de acceso a la base de datos.

Expone:
- `engine`: el motor SQLAlchemy global.
- `SessionLocal`: factory de sessions.
- `get_db()`: dependencia FastAPI que cede una session por request.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from reservas_app.config import Configuracion

_config = Configuracion()
engine = create_engine(_config.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Iterator[Session]:
    """Dependencia FastAPI: provee una Session por request y la cierra al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
