"""Pruebas del endpoint principal."""

from fastapi.testclient import TestClient

from reservas_app.main import app


def test_healthcheck_responde_ok():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
