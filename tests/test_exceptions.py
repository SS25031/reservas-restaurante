"""Tests for the domain exception hierarchy."""

import pytest

from reservas_restaurante.exceptions import (
    CapacidadInsuficienteError,
    ConflictoHorarioError,
    LimiteDiarioExcedidoError,
    MesaNoDisponibleError,
    ReservaError,
    ReservaNoEncontradaError,
    ValorInvalidoError,
)


@pytest.mark.parametrize(
    "exc_class",
    [
        CapacidadInsuficienteError,
        LimiteDiarioExcedidoError,
        MesaNoDisponibleError,
        ReservaNoEncontradaError,
        ConflictoHorarioError,
        ValorInvalidoError,
    ],
)
def test_todos_los_errores_de_dominio_heredan_de_reserva_error(exc_class):
    assert issubclass(exc_class, ReservaError)


def test_reserva_error_hereda_de_exception():
    assert issubclass(ReservaError, Exception)


def test_se_puede_capturar_via_clase_base():
    with pytest.raises(ReservaError):
        raise CapacidadInsuficienteError("no hay mesa")
