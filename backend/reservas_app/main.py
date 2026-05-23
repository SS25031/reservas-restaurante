"""Entrada principal del backend FastAPI.

Para correr el servidor en desarrollo:

    cd backend
    .venv/bin/uvicorn reservas_app.main:app --reload

Endpoints:
- GET /health
- /api/v1/onboarding/* — configuración inicial del restaurante (sin auth)
"""

from fastapi import FastAPI
from fastapi.responses import Response

from reservas_app.api.routers import onboarding

app = FastAPI(title="Reservas Restaurante API", version="0.4.0")

app.include_router(
    onboarding.router,
    prefix="/api/v1/onboarding",
    tags=["onboarding"],
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Endpoint de salud — confirma que el servidor está vivo."""
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Evita 404 en logs cuando el navegador pide el icono por defecto."""
    return Response(status_code=204)
