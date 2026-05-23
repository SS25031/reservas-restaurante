"""Router HTTP público para consultar disponibilidad y crear reservas."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from reservas_app.api.deps import enforce_public_rate_limit, get_public_booking_service
from reservas_app.api.schemas.public import (
    DisponibilidadResponse,
    PublicReservaCreateRequest,
    PublicReservaResponse,
    PublicRestaurantResponse,
)
from reservas_app.api.schemas.reserva import reserva_a_dict, turno_desde_api
from reservas_app.exceptions import (
    CapacidadInsuficienteError,
    ConflictoHorarioError,
    DiaCerradoError,
    LimiteDiarioExcedidoError,
    MesaNoDisponibleError,
    ReservaError,
    ReservasPublicasCerradasError,
    TurnoInactivoError,
    ValorInvalidoError,
)
from reservas_app.services.public_booking_service import PublicBookingService

router = APIRouter()


def _map_public_error(exc: ReservaError) -> HTTPException:
    if isinstance(exc, ReservasPublicasCerradasError):
        return HTTPException(status_code=503, detail=str(exc))
    if isinstance(exc, DiaCerradoError):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, TurnoInactivoError):
        return HTTPException(status_code=409, detail=str(exc))
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


@router.get("/restaurant", response_model=PublicRestaurantResponse)
def obtener_restaurant(
    booking: PublicBookingService = Depends(get_public_booking_service),
) -> PublicRestaurantResponse:
    return PublicRestaurantResponse.model_validate(booking.obtener_restaurant())


@router.get("/disponibilidad", response_model=DisponibilidadResponse)
def consultar_disponibilidad(
    request: Request,
    fecha: date = Query(..., description="Fecha ISO (YYYY-MM-DD)"),
    personas: int = Query(..., ge=1, description="Tamaño del grupo"),
    _: None = Depends(enforce_public_rate_limit),
    booking: PublicBookingService = Depends(get_public_booking_service),
) -> DisponibilidadResponse:
    del request
    try:
        result = booking.consultar_disponibilidad(fecha, personas)
    except ReservaError as exc:
        raise _map_public_error(exc) from exc
    return DisponibilidadResponse.model_validate(result)


@router.post("/reservas", response_model=PublicReservaResponse, status_code=201)
def crear_reserva_publica(
    body: PublicReservaCreateRequest,
    _: None = Depends(enforce_public_rate_limit),
    booking: PublicBookingService = Depends(get_public_booking_service),
) -> PublicReservaResponse:
    try:
        reserva = booking.crear_reserva(
            cliente=body.cliente,
            telefono=body.telefono,
            email=str(body.email),
            personas=body.personas,
            fecha=body.fecha,
            turno=turno_desde_api(body.turno),
        )
    except ReservaError as exc:
        raise _map_public_error(exc) from exc
    return PublicReservaResponse.model_validate(reserva_a_dict(reserva))
