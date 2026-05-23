"""Pruebas HTTP del router de onboarding."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from reservas_app.db import get_db
from reservas_app.main import app
from reservas_app.models.orm import Base
from tests.conftest import _seed_restaurant


@pytest.fixture
def client():
    """TestClient con DB en memoria inyectada vía override de dependencias."""
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

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    session.close()
    engine.dispose()


def test_estado_inicial(client):
    response = client.get("/api/v1/onboarding/estado")
    assert response.status_code == 200
    data = response.json()
    assert data["completado"] is False
    assert data["mesas_count"] == 0


def test_mesas_put_get_roundtrip(client):
    payload = {
        "mesas": [
            {"numero": 1, "capacidad": 2, "pos_x": 1.0, "pos_y": 2.0},
            {"numero": 2, "capacidad": 4},
        ]
    }
    put = client.put("/api/v1/onboarding/mesas", json=payload)
    assert put.status_code == 200
    assert len(put.json()) == 2

    get = client.get("/api/v1/onboarding/mesas")
    assert get.status_code == 200
    assert get.json()[0]["numero"] == 1


def test_completar_sin_mesas_devuelve_400(client):
    response = client.post("/api/v1/onboarding/completar")
    assert response.status_code == 400


def test_flujo_completar_onboarding(client):
    client.put(
        "/api/v1/onboarding/mesas",
        json={"mesas": [{"numero": 1, "capacidad": 2}]},
    )
    completar = client.post("/api/v1/onboarding/completar")
    assert completar.status_code == 200
    assert completar.json()["completado"] is True

    estado = client.get("/api/v1/onboarding/estado")
    assert estado.json()["completado"] is True


def test_completar_dos_veces_devuelve_409(client):
    client.put(
        "/api/v1/onboarding/mesas",
        json={"mesas": [{"numero": 1, "capacidad": 2}]},
    )
    client.post("/api/v1/onboarding/completar")
    segunda = client.post("/api/v1/onboarding/completar")
    assert segunda.status_code == 409


def test_restaurant_put_get(client):
    response = client.put(
        "/api/v1/onboarding/restaurant",
        json={"nombre": "La Buena Mesa"},
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "La Buena Mesa"

    get = client.get("/api/v1/onboarding/restaurant")
    assert get.json()["nombre"] == "La Buena Mesa"
