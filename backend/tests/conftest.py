"""Fixtures compartidas para pytest."""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from reservas_app.models import Mesa
from reservas_app.models.orm import Base
from reservas_app.services import ReservaService
from tests._fixtures.mesas import construir_mesas


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Session SQLAlchemy contra SQLite en memoria con schema creado."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def mesas() -> list[Mesa]:
    return construir_mesas()


@pytest.fixture
def service(mesas: list[Mesa]) -> ReservaService:
    return ReservaService(mesas)
