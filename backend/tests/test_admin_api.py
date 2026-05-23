"""Pruebas HTTP del router admin (reservas + reabrir onboarding)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from reservas_app.db import get_db
from reservas_app.main import app
from reservas_app.models.orm import Base
from tests._fixtures.auth import registrar_primer_admin
from tests.conftest import _seed_restaurant

RESERVA_PAYLOAD = {
    "cliente": "Ana García",
    "telefono": "600111222",
    "email": "ana@example.com",
    "personas": 2,
    "fecha": "2026-06-15",
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

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    session.close()
    engine.dispose()


@pytest.fixture
def authed_client(client: TestClient) -> TestClient:
    registrar_primer_admin(client)
    return client


@pytest.fixture
def authed_con_mesas(authed_client: TestClient) -> TestClient:
    response = authed_client.put(
        "/api/v1/onboarding/mesas",
        json={"mesas": [{"numero": 1, "capacidad": 4}, {"numero": 2, "capacidad": 2}]},
    )
    assert response.status_code == 200
    return authed_client


def _crear_reserva(client: TestClient, payload: dict | None = None) -> dict:
    body = payload or RESERVA_PAYLOAD
    response = client.post("/api/v1/admin/reservas", json=body)
    assert response.status_code == 201, response.text
    return response.json()


def test_admin_requiere_sesion(client: TestClient):
    response = client.get("/api/v1/admin/reservas")
    assert response.status_code == 401


def test_listar_reservas_vacio(authed_con_mesas: TestClient):
    response = authed_con_mesas.get("/api/v1/admin/reservas")
    assert response.status_code == 200
    assert response.json() == []


def test_crear_y_obtener_reserva(authed_con_mesas: TestClient):
    creada = _crear_reserva(authed_con_mesas)
    assert creada["cliente"] == "Ana García"
    assert creada["estado"] == "activa"
    assert creada["numero_mesa"] == 1

    lista = authed_con_mesas.get("/api/v1/admin/reservas")
    assert len(lista.json()) == 1

    detalle = authed_con_mesas.get(f"/api/v1/admin/reservas/{creada['id']}")
    assert detalle.status_code == 200
    assert detalle.json()["email"] == "ana@example.com"


def test_editar_reserva_fecha_y_turno(authed_con_mesas: TestClient):
    creada = _crear_reserva(authed_con_mesas)
    response = authed_con_mesas.patch(
        f"/api/v1/admin/reservas/{creada['id']}",
        json={"fecha": "2026-06-16", "turno": "TARDE"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fecha"] == "2026-06-16"
    assert data["turno"] == "TARDE"


def test_editar_sin_campos_devuelve_400(authed_con_mesas: TestClient):
    creada = _crear_reserva(authed_con_mesas)
    response = authed_con_mesas.patch(f"/api/v1/admin/reservas/{creada['id']}", json={})
    assert response.status_code == 400


def test_cancelar_reserva(authed_con_mesas: TestClient):
    creada = _crear_reserva(authed_con_mesas)
    cancelar = authed_con_mesas.post(f"/api/v1/admin/reservas/{creada['id']}/cancelar")
    assert cancelar.status_code == 204

    lista = authed_con_mesas.get("/api/v1/admin/reservas")
    assert lista.json() == []

    detalle = authed_con_mesas.get(f"/api/v1/admin/reservas/{creada['id']}")
    assert detalle.status_code == 200
    assert detalle.json()["estado"] == "cancelada"


def test_cancelar_dos_veces_devuelve_404(authed_con_mesas: TestClient):
    creada = _crear_reserva(authed_con_mesas)
    authed_con_mesas.post(f"/api/v1/admin/reservas/{creada['id']}/cancelar")
    segunda = authed_con_mesas.post(f"/api/v1/admin/reservas/{creada['id']}/cancelar")
    assert segunda.status_code == 404


def test_reserva_inexistente_devuelve_404(authed_con_mesas: TestClient):
    response = authed_con_mesas.get("/api/v1/admin/reservas/999")
    assert response.status_code == 404


def test_crear_sin_mesas_devuelve_409(authed_client: TestClient):
    response = authed_client.post("/api/v1/admin/reservas", json=RESERVA_PAYLOAD)
    assert response.status_code == 409


def test_reabrir_onboarding(authed_con_mesas: TestClient):
    authed_con_mesas.post("/api/v1/onboarding/completar")
    assert authed_con_mesas.get("/api/v1/onboarding/estado").json()["completado"] is True

    reabrir = authed_con_mesas.post("/api/v1/admin/onboarding/reabrir")
    assert reabrir.status_code == 200
    assert reabrir.json()["completado"] is False

    estado = authed_con_mesas.get("/api/v1/onboarding/estado")
    assert estado.json()["completado"] is False


def test_crear_reserva_email_invalido(authed_con_mesas: TestClient):
    payload = {**RESERVA_PAYLOAD, "email": "no-es-email"}
    response = authed_con_mesas.post("/api/v1/admin/reservas", json=payload)
    assert response.status_code == 422
