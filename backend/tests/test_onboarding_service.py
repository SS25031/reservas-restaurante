"""Pruebas unitarias de OnboardingService."""

from datetime import date

import pytest

from reservas_app.exceptions import (
    OnboardingIncompletoError,
    OnboardingYaCompletadoError,
    ValorInvalidoError,
)
from reservas_app.models import Mesa
from reservas_app.services.onboarding_service import OnboardingService


@pytest.fixture
def onboarding(db_session):
    return OnboardingService(db_session)


def test_obtener_estado_inicial(onboarding):
    estado = onboarding.obtener_estado()
    assert estado["completado"] is False
    assert estado["mesas_count"] == 0
    assert estado["turnos_activos"] == 3


def test_guardar_mesas_y_completar(onboarding):
    onboarding.guardar_mesas([Mesa(numero=1, capacidad=2), Mesa(numero=2, capacidad=4)])
    result = onboarding.completar_onboarding()
    assert result["completado"] is True
    assert onboarding.obtener_estado()["completado"] is True


def test_completar_sin_mesas_falla(onboarding):
    with pytest.raises(OnboardingIncompletoError):
        onboarding.completar_onboarding()


def test_completar_dos_veces_falla(onboarding):
    onboarding.guardar_mesas([Mesa(numero=1, capacidad=2)])
    onboarding.completar_onboarding()
    with pytest.raises(OnboardingYaCompletadoError):
        onboarding.completar_onboarding()


def test_guardar_calendario_excepciones(onboarding):
    onboarding.guardar_calendario([{"fecha": "2026-12-25", "cerrado": True, "nota": "Navidad"}])
    dias = onboarding.listar_calendario(desde=date(2026, 12, 1), hasta=date(2026, 12, 31))
    assert len(dias) == 1
    assert dias[0]["cerrado"] is True


def test_mesas_duplicadas_rechazadas(onboarding):
    with pytest.raises(ValorInvalidoError):
        onboarding.guardar_mesas([Mesa(numero=1, capacidad=2), Mesa(numero=1, capacidad=4)])
