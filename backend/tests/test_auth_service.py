"""Pruebas unitarias de AuthService."""

import pytest

from reservas_app.exceptions import (
    CredencialesInvalidasError,
    RegistroCerradoError,
    SesionInvalidaError,
    ValorInvalidoError,
)
from reservas_app.services.auth_service import AuthService


@pytest.fixture
def auth(db_session):
    return AuthService(db_session)


def test_registro_primer_admin(auth: AuthService):
    admin, token = auth.registrar_primer_admin("admin@example.com", "secreta123")
    assert admin.email == "admin@example.com"
    assert token
    assert auth.hay_admin_registrado()


def test_registro_cerrado_si_ya_hay_admin(auth: AuthService):
    auth.registrar_primer_admin("admin@example.com", "secreta123")
    with pytest.raises(RegistroCerradoError):
        auth.registrar_primer_admin("otro@example.com", "secreta123")


def test_login_exitoso(auth: AuthService):
    auth.registrar_primer_admin("admin@example.com", "secreta123")
    admin, token = auth.iniciar_sesion("admin@example.com", "secreta123")
    assert admin.email == "admin@example.com"
    assert auth.admin_desde_token(token).id == admin.id


def test_login_credenciales_invalidas(auth: AuthService):
    auth.registrar_primer_admin("admin@example.com", "secreta123")
    with pytest.raises(CredencialesInvalidasError):
        auth.iniciar_sesion("admin@example.com", "mala-clave")


def test_logout_invalida_sesion(auth: AuthService):
    _, token = auth.registrar_primer_admin("admin@example.com", "secreta123")
    auth.cerrar_sesion(token)
    with pytest.raises(SesionInvalidaError):
        auth.admin_desde_token(token)


def test_password_corta_rechazada(auth: AuthService):
    with pytest.raises(ValorInvalidoError):
        auth.registrar_primer_admin("admin@example.com", "corta")
