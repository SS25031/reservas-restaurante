"""Helper para preparar restaurante listo para reservas públicas."""

from fastapi.testclient import TestClient

from tests._fixtures.auth import registrar_primer_admin


def preparar_restaurant_publico(client: TestClient) -> None:
    """Registra admin, define mesas y completa onboarding."""
    registrar_primer_admin(client)
    client.put(
        "/api/v1/onboarding/mesas",
        json={"mesas": [{"numero": 1, "capacidad": 4}, {"numero": 2, "capacidad": 2}]},
    )
    client.post("/api/v1/onboarding/completar")
