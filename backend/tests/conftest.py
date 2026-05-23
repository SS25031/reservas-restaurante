"""Fixtures compartidas para pytest."""

import pytest

from reservas_app.models import Mesa
from reservas_app.services import ReservaService
from tests._fixtures.mesas import construir_mesas


@pytest.fixture
def mesas() -> list[Mesa]:
    return construir_mesas()


@pytest.fixture
def service(mesas: list[Mesa]) -> ReservaService:
    return ReservaService(mesas)
