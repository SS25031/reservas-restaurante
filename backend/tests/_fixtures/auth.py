"""Helper de registro/login para pruebas HTTP."""

from fastapi.testclient import TestClient

DEFAULT_EMAIL = "admin@example.com"
DEFAULT_PASSWORD = "secreta123"


def registrar_primer_admin(
    client: TestClient,
    email: str = DEFAULT_EMAIL,
    password: str = DEFAULT_PASSWORD,
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text


def login(
    client: TestClient,
    email: str = DEFAULT_EMAIL,
    password: str = DEFAULT_PASSWORD,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
