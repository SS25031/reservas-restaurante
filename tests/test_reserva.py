"""Tests for Reserva model (post-refactor)."""

from datetime import date

import pytest

from reservas_restaurante.exceptions import ValorInvalidoError
from reservas_restaurante.models import Reserva, Turno


def make_reserva(**overrides) -> Reserva:
    base = dict(
        id=1,
        fecha=date(2026, 6, 5),  # viernes
        turno=Turno.NOCHE,
        numero_mesa=10,
        cliente="Ana Pérez",
        telefono="7000-1234",
        personas=4,
    )
    base.update(overrides)
    return Reserva(**base)


def test_reserva_nombre_dia_corresponde_al_dia_de_la_semana():
    r = make_reserva(fecha=date(2026, 6, 5))  # viernes
    assert r.nombre_dia == "Viernes"


def test_reserva_nombre_turno_legible():
    r = make_reserva(turno=Turno.MANANA)
    assert r.nombre_turno == "Mañana"


def test_turno_desde_entero_valido():
    assert Turno.desde_entero(1) is Turno.MANANA
    assert Turno.desde_entero(2) is Turno.TARDE
    assert Turno.desde_entero(3) is Turno.NOCHE


def test_turno_desde_entero_invalido_lanza_error():
    with pytest.raises(ValorInvalidoError):
        Turno.desde_entero(0)
    with pytest.raises(ValorInvalidoError):
        Turno.desde_entero(99)


def test_reserva_str_contiene_campos_clave():
    r = make_reserva()
    texto = str(r)
    assert "Ana Pérez" in texto
    assert "7000-1234" in texto
    assert "Viernes" in texto
    assert "Noche" in texto
    assert "10" in texto  # numero_mesa
    assert "4" in texto   # personas
