"""Entrada principal del backend FastAPI.

Para correr el servidor en desarrollo:

    cd backend
    .venv/bin/uvicorn reservas_app.main:app --reload

Endpoints:
- GET /health
- /api/v1/auth/* — registro del primer admin, login, logout, me
- /api/v1/onboarding/* — configuración inicial (requiere sesión admin)
- /api/v1/admin/* — gestión de reservas (requiere sesión admin)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from reservas_app.api.deps import get_config
from reservas_app.api.routers import admin, auth, onboarding

_config = get_config()

app = FastAPI(title="Reservas Restaurante API", version="0.6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(_config.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    onboarding.router,
    prefix="/api/v1/onboarding",
    tags=["onboarding"],
)
app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["admin"],
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Endpoint de salud — confirma que el servidor está vivo."""
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Evita 404 en logs cuando el navegador pide el icono por defecto."""
    return Response(status_code=204)
