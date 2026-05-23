"""Esquemas Pydantic para el onboarding."""

from datetime import date

from pydantic import BaseModel, Field


class OnboardingEstadoResponse(BaseModel):
    completado: bool
    mesas_count: int
    turnos_activos: int


class RestaurantResponse(BaseModel):
    id: int
    nombre: str
    max_reservas_por_dia: int
    capacidad_maxima_grupo: int
    onboarding_completado: bool


class RestaurantUpdateRequest(BaseModel):
    nombre: str | None = None
    max_reservas_por_dia: int | None = Field(default=None, ge=1)
    capacidad_maxima_grupo: int | None = Field(default=None, ge=1)


class MesaSchema(BaseModel):
    numero: int = Field(ge=1)
    capacidad: int = Field(ge=1)
    pos_x: float | None = None
    pos_y: float | None = None


class MesasUpdateRequest(BaseModel):
    mesas: list[MesaSchema]


class TurnoSchema(BaseModel):
    turno: str
    activo: bool = True
    hora_inicio: str | None = None
    hora_fin: str | None = None


class TurnosUpdateRequest(BaseModel):
    turnos: list[TurnoSchema]


class CalendarDaySchema(BaseModel):
    fecha: date
    cerrado: bool = False
    nota: str | None = None


class CalendarioUpdateRequest(BaseModel):
    dias: list[CalendarDaySchema]


class CompletarResponse(BaseModel):
    completado: bool
