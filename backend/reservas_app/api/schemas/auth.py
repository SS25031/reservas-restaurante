"""Esquemas Pydantic para autenticación admin."""

from pydantic import BaseModel, EmailStr, Field


class AuthCredentialsRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class AdminUserResponse(BaseModel):
    id: int
    email: str
    restaurant_id: int


class RegistroDisponibleResponse(BaseModel):
    disponible: bool
