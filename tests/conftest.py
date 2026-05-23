"""Shared pytest fixtures."""

import pytest

from models import Mesa
from restaurante import construir_mesas
from services import ReservaService


@pytest.fixture
def mesas() -> list[Mesa]:
    """A fresh copy of the 25-table production layout."""
    return construir_mesas()


@pytest.fixture
def service(mesas: list[Mesa]) -> ReservaService:
    """A ReservaService with the production layout and no reservations."""
    return ReservaService(mesas)
