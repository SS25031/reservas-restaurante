"""Router HTTP de administración (reservas + reabrir onboarding)."""

from fastapi import APIRouter, Depends, HTTPException, Response

from reservas_app.api.deps import get_admin_service, get_current_admin
from reservas_app.api.schemas.admin import (
    ReabrirOnboardingResponse,
    ReservaCreateRequest,
    ReservaResponse,
    ReservaUpdateRequest,
)
from reservas_app.api.schemas.reserva import reserva_a_dict, turno_desde_api
from reservas_app.exceptions import (
    CapacidadInsuficienteError,
    ConflictoHorarioError,
    LimiteDiarioExcedidoError,
    MesaNoDisponibleError,
    ReservaError,
    ReservaNoEncontradaError,
    ValorInvalidoError,
)
from reservas_app.services.admin_service import AdminService

router = APIRouter(dependencies=[Depends(get_current_admin)])


def _map_reserva_error(exc: ReservaError) -> HTTPException:
    if isinstance(exc, ReservaNoEncontradaError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(
        exc,
        (
            ConflictoHorarioError,
            LimiteDiarioExcedidoError,
            MesaNoDisponibleError,
            CapacidadInsuficienteError,
        ),
    ):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, ValorInvalidoError):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@router.get("/reservas", response_model=list[ReservaResponse])
def listar_reservas(
    admin: AdminService = Depends(get_admin_service),
) -> list[ReservaResponse]:
    reservas = admin.listar_reservas()
    return [ReservaResponse.model_validate(reserva_a_dict(r)) for r in reservas]


@router.get("/reservas/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(
    reserva_id: int,
    admin: AdminService = Depends(get_admin_service),
) -> ReservaResponse:
    try:
        reserva = admin.obtener_reserva(reserva_id)
    except ReservaError as exc:
        raise _map_reserva_error(exc) from exc
    return ReservaResponse.model_validate(reserva_a_dict(reserva))


@router.post("/reservas", response_model=ReservaResponse, status_code=201)
def crear_reserva(
    body: ReservaCreateRequest,
    admin: AdminService = Depends(get_admin_service),
) -> ReservaResponse:
    try:
        reserva = admin.crear_reserva(
            cliente=body.cliente,
            telefono=body.telefono,
            email=str(body.email),
            personas=body.personas,
            fecha=body.fecha,
            turno=turno_desde_api(body.turno),
        )
    except ReservaError as exc:
        raise _map_reserva_error(exc) from exc
    return ReservaResponse.model_validate(reserva_a_dict(reserva))


@router.patch("/reservas/{reserva_id}", response_model=ReservaResponse)
def editar_reserva(
    reserva_id: int,
    body: ReservaUpdateRequest,
    admin: AdminService = Depends(get_admin_service),
) -> ReservaResponse:
    if body.fecha is None and body.turno is None:
        raise HTTPException(status_code=400, detail="Indica fecha y/o turno a actualizar.")
    try:
        reserva = admin.editar_reserva(
            reserva_id,
            fecha=body.fecha,
            turno=turno_desde_api(body.turno) if body.turno is not None else None,
        )
    except ReservaError as exc:
        raise _map_reserva_error(exc) from exc
    return ReservaResponse.model_validate(reserva_a_dict(reserva))


@router.post("/reservas/{reserva_id}/cancelar", status_code=204)
def cancelar_reserva(
    reserva_id: int,
    admin: AdminService = Depends(get_admin_service),
) -> Response:
    try:
        admin.cancelar_reserva(reserva_id)
    except ReservaError as exc:
        raise _map_reserva_error(exc) from exc
    return Response(status_code=204)


@router.post("/onboarding/reabrir", response_model=ReabrirOnboardingResponse)
def reabrir_onboarding(
    admin: AdminService = Depends(get_admin_service),
) -> ReabrirOnboardingResponse:
    result = admin.reabrir_onboarding()
    return ReabrirOnboardingResponse.model_validate(result)
