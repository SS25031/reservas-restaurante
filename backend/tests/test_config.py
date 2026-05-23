"""Pruebas de Configuracion."""

import pytest

from reservas_app.config import Configuracion


def test_configuracion_defaults_son_validos():
    config = Configuracion()
    assert config.max_reservas_por_dia == 25
    assert config.capacidad_maxima_grupo == 10
    assert config.database_url == "sqlite:///./reservas.db"


def test_max_reservas_por_dia_debe_ser_positivo():
    with pytest.raises(ValueError):
        Configuracion(max_reservas_por_dia=0)
    with pytest.raises(ValueError):
        Configuracion(max_reservas_por_dia=-1)


def test_capacidad_maxima_grupo_debe_ser_positiva():
    with pytest.raises(ValueError):
        Configuracion(capacidad_maxima_grupo=0)


def test_database_url_no_puede_estar_vacia():
    with pytest.raises(ValueError):
        Configuracion(database_url="")
    with pytest.raises(ValueError):
        Configuracion(database_url="   ")


def test_database_url_lee_env_var(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./otra.db")
    config = Configuracion()
    assert config.database_url == "sqlite:///./otra.db"
