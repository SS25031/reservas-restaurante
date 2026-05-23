"""Router HTTP de autenticación admin."""

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from reservas_app.api.deps import (
    clear_session_cookie,
    get_auth_service,
    get_config,
    get_current_admin,
    set_session_cookie,
)
from reservas_app.api.schemas.auth import (
    AdminUserResponse,
    AuthCredentialsRequest,
    RegistroDisponibleResponse,
)
from reservas_app.config import Configuracion
from reservas_app.exceptions import (
    CredencialesInvalidasError,
    RegistroCerradoError,
    ReservaError,
    ValorInvalidoError,
)
from reservas_app.models.orm import AdminUserORM
from reservas_app.services.auth_service import AuthService

router = APIRouter()


def _map_auth_error(exc: ReservaError) -> JSONResponse:
    if isinstance(exc, RegistroCerradoError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    if isinstance(exc, CredencialesInvalidasError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    if isinstance(exc, ValorInvalidoError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@router.get("/registro-disponible", response_model=RegistroDisponibleResponse)
def registro_disponible(
    auth: AuthService = Depends(get_auth_service),
) -> RegistroDisponibleResponse:
    return RegistroDisponibleResponse(disponible=not auth.hay_admin_registrado())


@router.post("/register", response_model=AdminUserResponse)
def registrar_primer_admin(
    body: AuthCredentialsRequest,
    auth: AuthService = Depends(get_auth_service),
) -> Response:
    try:
        admin, token = auth.registrar_primer_admin(body.email, body.password)
    except ReservaError as exc:
        return _map_auth_error(exc)
    payload = AdminUserResponse.model_validate(AuthService.admin_a_dict(admin))
    response = JSONResponse(content=payload.model_dump())
    set_session_cookie(response, token)
    return response


@router.post("/login", response_model=AdminUserResponse)
def login(
    body: AuthCredentialsRequest,
    auth: AuthService = Depends(get_auth_service),
) -> Response:
    try:
        admin, token = auth.iniciar_sesion(body.email, body.password)
    except ReservaError as exc:
        return _map_auth_error(exc)
    payload = AdminUserResponse.model_validate(AuthService.admin_a_dict(admin))
    response = JSONResponse(content=payload.model_dump())
    set_session_cookie(response, token)
    return response


@router.post("/logout", status_code=204)
def logout(
    request: Request,
    auth: AuthService = Depends(get_auth_service),
    config: Configuracion = Depends(get_config),
) -> Response:
    token = request.cookies.get(config.session_cookie_name)
    auth.cerrar_sesion(token)
    response = Response(status_code=204)
    clear_session_cookie(response)
    return response


@router.get("/me", response_model=AdminUserResponse)
def me(admin: AdminUserORM = Depends(get_current_admin)) -> AdminUserResponse:
    return AdminUserResponse.model_validate(AuthService.admin_a_dict(admin))
