"""Sanity tests for model classes."""

from models import Mesa


def test_mesa_puede_acomodar_grupo_igual_a_capacidad():
    mesa = Mesa(numero=1, capacidad=4)
    assert mesa.puede_acomodar(4) is True


def test_mesa_puede_acomodar_grupo_pequeno():
    mesa = Mesa(numero=1, capacidad=4)
    assert mesa.puede_acomodar(2) is True


def test_mesa_no_acomoda_grupo_mayor_que_capacidad():
    mesa = Mesa(numero=1, capacidad=4)
    assert mesa.puede_acomodar(5) is False
