"""Persistence interface for reservations."""

from typing import Protocol

from models import Reserva


class ReservaRepository(Protocol):
    """A pluggable persistence backend for reservations."""

    def cargar(self) -> tuple[list[Reserva], int]:
        """Return (reservas, last_id_used). If no data exists, return ([], 0)."""
        ...

    def guardar(self, reservas: list[Reserva], ultimo_id: int) -> None:
        """Persist the full set of reservations and the highest ID assigned so far."""
        ...
