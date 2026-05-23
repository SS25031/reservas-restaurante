"""Configuración de runtime del backend."""

import os
from dataclasses import dataclass, field


def _default_database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///./reservas.db")


def _default_cors_origins() -> tuple[str, ...]:
    raw = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    return tuple(origin.strip() for origin in raw.split(",") if origin.strip())


def _default_session_cookie_name() -> str:
    return os.environ.get("SESSION_COOKIE_NAME", "reservas_session")


def _default_session_ttl_hours() -> int:
    return int(os.environ.get("SESSION_TTL_HOURS", "168"))


def _default_cookie_secure() -> bool:
    return os.environ.get("SESSION_COOKIE_SECURE", "").lower() in {"1", "true", "yes"}


def _default_public_rate_limit_requests() -> int:
    return int(os.environ.get("PUBLIC_RATE_LIMIT_REQUESTS", "20"))


def _default_public_rate_limit_window_seconds() -> int:
    return int(os.environ.get("PUBLIC_RATE_LIMIT_WINDOW_SECONDS", "60"))


@dataclass(frozen=True)
class Configuracion:
    """Límites configurables del servicio y URL de la base de datos."""

    max_reservas_por_dia: int = 25
    capacidad_maxima_grupo: int = 10
    database_url: str = field(default_factory=_default_database_url)
    session_cookie_name: str = field(default_factory=_default_session_cookie_name)
    session_ttl_hours: int = field(default_factory=_default_session_ttl_hours)
    session_cookie_secure: bool = field(default_factory=_default_cookie_secure)
    cors_origins: tuple[str, ...] = field(default_factory=_default_cors_origins)
    public_rate_limit_requests: int = field(default_factory=_default_public_rate_limit_requests)
    public_rate_limit_window_seconds: int = field(
        default_factory=_default_public_rate_limit_window_seconds
    )

    def __post_init__(self) -> None:
        if self.max_reservas_por_dia < 1:
            raise ValueError("max_reservas_por_dia debe ser ≥ 1")
        if self.capacidad_maxima_grupo < 1:
            raise ValueError("capacidad_maxima_grupo debe ser ≥ 1")
        if not self.database_url.strip():
            raise ValueError("database_url no puede estar vacía")
        if self.session_ttl_hours < 1:
            raise ValueError("session_ttl_hours debe ser ≥ 1")
        if not self.session_cookie_name.strip():
            raise ValueError("session_cookie_name no puede estar vacío")
        if self.public_rate_limit_requests < 1:
            raise ValueError("public_rate_limit_requests debe ser ≥ 1")
        if self.public_rate_limit_window_seconds < 1:
            raise ValueError("public_rate_limit_window_seconds debe ser ≥ 1")

    @property
    def session_max_age_seconds(self) -> int:
        return self.session_ttl_hours * 3600
