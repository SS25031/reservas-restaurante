"""Fixtures compartidas para pytest."""

import os

# Aísla los tests del archivo reservas.db de desarrollo. Debe ejecutarse antes
# de que cualquier módulo importe reservas_app.db (pytest carga conftest primero).
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from reservas_app.models import Mesa
from reservas_app.models.orm import Base, RestaurantORM, TurnoConfigORM
from reservas_app.services import ReservaService
from tests._fixtures.mesas import construir_mesas


def _seed_restaurant(session: Session) -> None:
    if session.get(RestaurantORM, 1) is not None:
        return
    session.add(
        RestaurantORM(
            id=1,
            nombre="Test Restaurant",
            max_reservas_por_dia=25,
            capacidad_maxima_grupo=10,
            onboarding_completado=False,
        )
    )
    for turno in ("MANANA", "TARDE", "NOCHE"):
        session.add(TurnoConfigORM(restaurant_id=1, turno=turno, activo=True))
    session.commit()


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Session SQLAlchemy contra SQLite en memoria con schema creado."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        _seed_restaurant(session)
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
