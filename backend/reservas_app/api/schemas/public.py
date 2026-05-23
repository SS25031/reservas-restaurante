"""Esquemas Pydantic para la API pública de reservas."""

from datetime import date

from pydantic import BaseModel

from reservas_app.api.schemas.admin import ReservaCreateRequest, ReservaResponse


class PublicRestaurantResponse(BaseModel):
    nombre: str
    capacidad_maxima_grupo: int
    acepta_reservas: bool


class TurnoDisponibilidadResponse(BaseModel):
    turno: str
    turno_label: str
    disponible: bool
    mesas_libres: int


class DisponibilidadResponse(BaseModel):
    fecha: date
    personas: int
    cerrado: bool
    nota: str | None = None
    acepta_reservas: bool
    turnos: list[TurnoDisponibilidadResponse]


PublicReservaCreateRequest = ReservaCreateRequest
PublicReservaResponse = ReservaResponse
