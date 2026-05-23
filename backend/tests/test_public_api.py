"""Pruebas HTTP del router público de reservas."""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from reservas_app.api.deps import get_public_rate_limiter
from reservas_app.api.rate_limit import InMemoryRateLimiter
from reservas_app.db import get_db
from reservas_app.main import app
from reservas_app.models.orm import Base
from tests._fixtures.public import preparar_restaurant_publico
from tests.conftest import _seed_restaurant

RESERVA_PAYLOAD = {
    "cliente": "Carlos López",
    "telefono": "600333444",
    "email": "carlos@example.com",
    "personas": 2,
    "fecha": "2026-08-10",
    "turno": "NOCHE",
}


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    _seed_restaurant(session)

    def override_get_db():
        try:
            yield session
        finally:
            pass

    test_limiter = InMemoryRateLimiter(max_requests=100, window_seconds=60)

    def override_rate_limiter():
        return test_limiter

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_public_rate_limiter] = override_rate_limiter
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    session.close()
    engine.dispose()


@pytest.fixture
def client_listo(client: TestClient) -> TestClient:
    preparar_restaurant_publico(client)
    return client


def test_restaurant_sin_onboarding_no_acepta_reservas(client: TestClient):
    response = client.get("/api/v1/public/restaurant")
    assert response.status_code == 200
    data = response.json()
    assert data["acepta_reservas"] is False


def test_restaurant_listo_acepta_reservas(client_listo: TestClient):
    response = client_listo.get("/api/v1/public/restaurant")
    assert response.status_code == 200
    assert response.json()["acepta_reservas"] is True


def test_disponibilidad_sin_onboarding_devuelve_503(client: TestClient):
    futura = (date.today() + timedelta(days=7)).isoformat()
    response = client.get(f"/api/v1/public/disponibilidad?fecha={futura}&personas=2")
    assert response.status_code == 503


def test_disponibilidad_muestra_turnos(client_listo: TestClient):
    futura = (date.today() + timedelta(days=7)).isoformat()
    response = client_listo.get(f"/api/v1/public/disponibilidad?fecha={futura}&personas=2")
    assert response.status_code == 200
    data = response.json()
    assert data["cerrado"] is False
    assert data["acepta_reservas"] is True
    assert len(data["turnos"]) == 3
    assert all(turno["disponible"] for turno in data["turnos"])


def test_disponibilidad_dia_cerrado(client_listo: TestClient):
    futura = (date.today() + timedelta(days=10)).isoformat()
    client_listo.put(
        "/api/v1/onboarding/calendario",
        json={"dias": [{"fecha": futura, "cerrado": True, "nota": "Evento privado"}]},
    )
    response = client_listo.get(f"/api/v1/public/disponibilidad?fecha={futura}&personas=2")
    assert response.status_code == 200
    data = response.json()
    assert data["cerrado"] is True
    assert data["acepta_reservas"] is False
    assert data["turnos"] == []


def test_crear_reserva_publica(client_listo: TestClient):
    payload = {
        **RESERVA_PAYLOAD,
        "fecha": (date.today() + timedelta(days=7)).isoformat(),
    }
    response = client_listo.post("/api/v1/public/reservas", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["cliente"] == "Carlos López"
    assert data["estado"] == "activa"
    assert data["numero_mesa"] == 1


def test_crear_reserva_dia_cerrado_devuelve_409(client_listo: TestClient):
    futura = (date.today() + timedelta(days=12)).isoformat()
    client_listo.put(
        "/api/v1/onboarding/calendario",
        json={"dias": [{"fecha": futura, "cerrado": True}]},
    )
    payload = {**RESERVA_PAYLOAD, "fecha": futura}
    response = client_listo.post("/api/v1/public/reservas", json=payload)
    assert response.status_code == 409


def test_crear_reserva_fecha_pasada_devuelve_400(client_listo: TestClient):
    payload = {**RESERVA_PAYLOAD, "fecha": "2020-01-01"}
    response = client_listo.post("/api/v1/public/reservas", json=payload)
    assert response.status_code == 400


def test_crear_reserva_turno_inactivo_devuelve_409(client_listo: TestClient):
    client_listo.put(
        "/api/v1/onboarding/turnos",
        json={
            "turnos": [
                {"turno": "MANANA", "activo": True},
                {"turno": "TARDE", "activo": True},
                {"turno": "NOCHE", "activo": False},
            ]
        },
    )
    payload = {
        **RESERVA_PAYLOAD,
        "fecha": (date.today() + timedelta(days=7)).isoformat(),
        "turno": "NOCHE",
    }
    response = client_listo.post("/api/v1/public/reservas", json=payload)
    assert response.status_code == 409


def test_rate_limit_devuelve_429(client: TestClient):
    strict_limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)

    def override_rate_limiter():
        return strict_limiter

    app.dependency_overrides[get_public_rate_limiter] = override_rate_limiter
    try:
        futura = (date.today() + timedelta(days=3)).isoformat()
        for _ in range(2):
            ok = client.get(f"/api/v1/public/disponibilidad?fecha={futura}&personas=2")
            assert ok.status_code in {200, 503}
        bloqueado = client.get(f"/api/v1/public/disponibilidad?fecha={futura}&personas=2")
        assert bloqueado.status_code == 429
    finally:
        app.dependency_overrides.pop(get_public_rate_limiter, None)
