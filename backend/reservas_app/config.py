"""Configuración de runtime del backend."""

import os
from dataclasses import dataclass, field


def _default_database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///./reservas.db")


@dataclass(frozen=True)
class Configuracion:
    """Límites configurables del servicio y URL de la base de datos."""

    max_reservas_por_dia: int = 25
    capacidad_maxima_grupo: int = 10
    database_url: str = field(default_factory=_default_database_url)

    def __post_init__(self) -> None:
        if self.max_reservas_por_dia < 1:
            raise ValueError("max_reservas_por_dia debe ser ≥ 1")
        if self.capacidad_maxima_grupo < 1:
            raise ValueError("capacidad_maxima_grupo debe ser ≥ 1")
        if not self.database_url.strip():
            raise ValueError("database_url no puede estar vacía")
