"""Shared pytest fixtures."""

import pytest

from models import Mesa
from services import ReservaService


def construir_mesas() -> list[Mesa]:
    """Layout fijo de 25 mesas (helper temporal, se moverá a tests/_fixtures en Task 2)."""
    layout = [
        (range(1, 6), 2),
        (range(6, 11), 4),
        (range(11, 16), 6),
        (range(16, 21), 8),
        (range(21, 26), 10),
    ]
    return [Mesa(numero=n, capacidad=cap) for rng, cap in layout for n in rng]


@pytest.fixture
def mesas() -> list[Mesa]:
    """A fresh copy of the 25-table production layout."""
    return construir_mesas()


@pytest.fixture
def service(mesas: list[Mesa]) -> ReservaService:
    """A ReservaService with the production layout and no reservations."""
    return ReservaService(mesas)
