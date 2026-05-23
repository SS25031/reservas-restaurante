"""Router HTTP del onboarding (sin auth — subsistema 3)."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from reservas_app.api.deps import get_onboarding_service
from reservas_app.api.schemas.onboarding import (
    CalendarDaySchema,
    CalendarioUpdateRequest,
    CompletarResponse,
    MesasUpdateRequest,
    MesaSchema,
    OnboardingEstadoResponse,
    RestaurantResponse,
    RestaurantUpdateRequest,
    TurnoSchema,
    TurnosUpdateRequest,
)
from reservas_app.exceptions import (
    OnboardingIncompletoError,
    OnboardingYaCompletadoError,
    ReservaError,
    ValorInvalidoError,
)
from reservas_app.models import Mesa
from reservas_app.services.onboarding_service import OnboardingService

router = APIRouter()


def _map_domain_error(exc: ReservaError) -> HTTPException:
    if isinstance(exc, OnboardingYaCompletadoError):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, (OnboardingIncompletoError, ValorInvalidoError)):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@router.get("/estado", response_model=OnboardingEstadoResponse)
def obtener_estado(
    service: OnboardingService = Depends(get_onboarding_service),
) -> OnboardingEstadoResponse:
    data = service.obtener_estado()
    return OnboardingEstadoResponse.model_validate(data)


@router.get("/restaurant", response_model=RestaurantResponse)
def obtener_restaurant(
    service: OnboardingService = Depends(get_onboarding_service),
) -> RestaurantResponse:
    return RestaurantResponse.model_validate(service.obtener_restaurant())


@router.put("/restaurant", response_model=RestaurantResponse)
def actualizar_restaurant(
    body: RestaurantUpdateRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> RestaurantResponse:
    try:
        data = service.actualizar_restaurant(
            nombre=body.nombre,
            max_reservas_por_dia=body.max_reservas_por_dia,
            capacidad_maxima_grupo=body.capacidad_maxima_grupo,
        )
    except ReservaError as exc:
        raise _map_domain_error(exc) from exc
    return RestaurantResponse.model_validate(data)


@router.get("/mesas", response_model=list[MesaSchema])
def listar_mesas(
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[MesaSchema]:
    return [MesaSchema.model_validate(m) for m in service.listar_mesas()]


@router.put("/mesas", response_model=list[MesaSchema])
def guardar_mesas(
    body: MesasUpdateRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[MesaSchema]:
    mesas = [
        Mesa(
            numero=m.numero,
            capacidad=m.capacidad,
            pos_x=m.pos_x,
            pos_y=m.pos_y,
        )
        for m in body.mesas
    ]
    try:
        guardadas = service.guardar_mesas(mesas)
    except ReservaError as exc:
        raise _map_domain_error(exc) from exc
    return [MesaSchema.model_validate(m) for m in guardadas]


@router.get("/turnos", response_model=list[TurnoSchema])
def listar_turnos(
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[TurnoSchema]:
    return [TurnoSchema.model_validate(t) for t in service.listar_turnos()]


@router.put("/turnos", response_model=list[TurnoSchema])
def guardar_turnos(
    body: TurnosUpdateRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[TurnoSchema]:
    try:
        turnos = service.guardar_turnos([t.model_dump() for t in body.turnos])
    except ReservaError as exc:
        raise _map_domain_error(exc) from exc
    return [TurnoSchema.model_validate(t) for t in turnos]


@router.get("/calendario", response_model=list[CalendarDaySchema])
def listar_calendario(
    desde: date | None = None,
    hasta: date | None = None,
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[CalendarDaySchema]:
    dias = service.listar_calendario(desde=desde, hasta=hasta)
    return [CalendarDaySchema.model_validate(d) for d in dias]


@router.put("/calendario", response_model=list[CalendarDaySchema])
def guardar_calendario(
    body: CalendarioUpdateRequest,
    service: OnboardingService = Depends(get_onboarding_service),
) -> list[CalendarDaySchema]:
    try:
        dias = service.guardar_calendario([d.model_dump(mode="json") for d in body.dias])
    except ReservaError as exc:
        raise _map_domain_error(exc) from exc
    return [CalendarDaySchema.model_validate(d) for d in dias]


@router.post("/completar", response_model=CompletarResponse)
def completar_onboarding(
    service: OnboardingService = Depends(get_onboarding_service),
) -> CompletarResponse:
    try:
        result = service.completar_onboarding()
    except ReservaError as exc:
        raise _map_domain_error(exc) from exc
    return CompletarResponse.model_validate(result)
