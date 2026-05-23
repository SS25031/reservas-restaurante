"""Shared pytest fixtures."""

import pytest

from reservas_restaurante.__main__ import construir_mesas
from reservas_restaurante.models import Mesa
from reservas_restaurante.services import ReservaService


@pytest.fixture
def mesas() -> list[Mesa]:
    """A fresh copy of the 25-table production layout."""
    return construir_mesas()


@pytest.fixture
def service(mesas: list[Mesa]) -> ReservaService:
    """A ReservaService with the production layout and no reservations."""
    return ReservaService(mesas)
