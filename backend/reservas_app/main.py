"""Entrada principal del backend FastAPI.

Para correr el servidor en desarrollo:

    cd backend
    .venv/bin/uvicorn reservas_app.main:app --reload

Endpoints del subsistema 1:
- GET /health  -> {"status": "ok"}

Endpoints de dominio (reservas, onboarding, auth) llegan en subsistemas
posteriores.
"""

from fastapi import FastAPI

app = FastAPI(title="Reservas Restaurante API", version="0.3.0")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Endpoint de salud — confirma que el servidor está vivo."""
    return {"status": "ok"}
