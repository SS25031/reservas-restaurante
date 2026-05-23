"""Runtime configuration for the reservation service."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracion:
    """Configurable limits for reservations."""

    max_reservas_por_dia: int = 25
    capacidad_maxima_grupo: int = 10
