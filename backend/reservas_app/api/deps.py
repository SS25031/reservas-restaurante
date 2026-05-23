"""Dependencias compartidas de la capa API."""

from fastapi import Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import Response

from reservas_app.config import Configuracion
from reservas_app.db import get_db
from reservas_app.exceptions import SesionInvalidaError
from reservas_app.models.orm import AdminUserORM
from reservas_app.services.auth_service import AuthService
from reservas_app.services.onboarding_service import OnboardingService

_config = Configuracion()


def get_config() -> Configuracion:
    return _config


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db, config=_config)


def get_onboarding_service(db: Session = Depends(get_db)) -> OnboardingService:
    return OnboardingService(db)


def _token_desde_request(request: Request) -> str | None:
    return request.cookies.get(_config.session_cookie_name)


def get_current_admin(
    request: Request,
    auth: AuthService = Depends(get_auth_service),
) -> AdminUserORM:
    """Dependencia que exige una sesión admin válida (cookie HTTPOnly)."""
    try:
        return auth.admin_desde_token(_token_desde_request(request))
    except SesionInvalidaError as exc:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail=str(exc)) from exc


def set_session_cookie(response: Response, token: str) -> None:
    """Establece la cookie de sesión HTTPOnly en la respuesta."""
    response.set_cookie(
        key=_config.session_cookie_name,
        value=token,
        httponly=True,
        samesite="lax",
        secure=_config.session_cookie_secure,
        max_age=_config.session_max_age_seconds,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    """Elimina la cookie de sesión."""
    response.delete_cookie(
        key=_config.session_cookie_name,
        path="/",
        httponly=True,
        samesite="lax",
        secure=_config.session_cookie_secure,
    )
