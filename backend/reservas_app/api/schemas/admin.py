"""Esquemas Pydantic para la API admin."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class ReservaResponse(BaseModel):
    id: int
    fecha: date
    turno: str
    turno_label: str
    numero_mesa: int
    cliente: str
    telefono: str
    email: str
    personas: int
    estado: str


class ReservaCreateRequest(BaseModel):
    cliente: str = Field(min_length=1)
    telefono: str = Field(min_length=1)
    email: EmailStr
    personas: int = Field(ge=1)
    fecha: date
    turno: Literal["MANANA", "TARDE", "NOCHE"]


class ReservaUpdateRequest(BaseModel):
    fecha: date | None = None
    turno: Literal["MANANA", "TARDE", "NOCHE"] | None = None


class ReabrirOnboardingResponse(BaseModel):
    completado: bool
