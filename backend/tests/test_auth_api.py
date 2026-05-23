"""Pruebas HTTP del router de autenticación."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from reservas_app.db import get_db
from reservas_app.main import app
from reservas_app.models.orm import Base
from tests._fixtures.auth import DEFAULT_EMAIL, DEFAULT_PASSWORD, registrar_primer_admin
from tests.conftest import _seed_restaurant


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


def test_registro_disponible_inicialmente(client: TestClient):
    response = client.get("/api/v1/auth/registro-disponible")
    assert response.status_code == 200
    assert response.json()["disponible"] is True


def test_registro_primer_admin_y_cookie(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD},
    )
    assert response.status_code == 200
    assert response.json()["email"] == DEFAULT_EMAIL
    assert client.cookies

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == DEFAULT_EMAIL


def test_segundo_registro_devuelve_409(client: TestClient):
    registrar_primer_admin(client)
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "otro@example.com", "password": DEFAULT_PASSWORD},
    )
    assert response.status_code == 409


def test_login_y_logout(client: TestClient):
    registrar_primer_admin(client)
    client.cookies.clear()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD},
    )
    assert login.status_code == 200

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200

    logout = client.post("/api/v1/auth/logout")
    assert logout.status_code == 204

    me_despues = client.get("/api/v1/auth/me")
    assert me_despues.status_code == 401


def test_me_sin_sesion_devuelve_401(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
