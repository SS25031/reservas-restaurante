# Sistema de Reservas de Restaurante

Backend FastAPI + frontend SvelteKit para gestionar reservas de un restaurante.

> **Nota:** La CLI original fue retirada. El archivo `~/.reservas-restaurante/reservas.json` ya no se usa.

## Requisitos

- Python ≥ 3.10
- Node.js ≥ 20 (frontend)

## Backend

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/alembic upgrade head
.venv/bin/uvicorn reservas_app.main:app --reload --port 8000
```

## Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:5173 — proxy /api → backend :8000
```

En desarrollo, arranca **backend y frontend** a la vez. El proxy de Vite reenvía `/api` y `/health` al backend para que las cookies de sesión funcionen.

### Flujo admin inicial

1. Abrir http://localhost:5173/register — crear primer administrador
2. Tras el registro, redirige a `/admin`
3. Configurar mesas en `/admin/onboarding` (wizard con editor Konva)
4. Gestionar reservas en `/admin/reservas` o `/admin/calendario`

### Panel admin

| Ruta | Función |
|------|---------|
| `/admin` | Resumen, estado onboarding, reabrir configuración |
| `/admin/reservas` | Listado, crear, editar fecha/turno, cancelar |
| `/admin/calendario` | Vista mensual con detalle por día |
| `/admin/onboarding` | Wizard: restaurante, mesas (Konva), turnos, calendario |

### API pública (sin auth)

| Método | Ruta | Función |
|--------|------|---------|
| `GET` | `/api/v1/public/restaurant` | Info del restaurante |
| `GET` | `/api/v1/public/disponibilidad` | Turnos disponibles (`fecha`, `personas`) |
| `POST` | `/api/v1/public/reservas` | Crear reserva |

Rate limit configurable: `PUBLIC_RATE_LIMIT_REQUESTS` (default 20/min por IP).

### Reserva pública (clientes)

| Ruta | Función |
|------|---------|
| `/` | Inicio con enlace a reservar |
| `/reservar` | Wizard: fecha → turno/datos → confirmación |

## Desarrollo backend

```bash
cd backend
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/mypy
```

## Desarrollo frontend

```bash
cd frontend
npm run check
npm run build
```

## Arquitectura

```
reservas-restaurante/
├── backend/          # FastAPI, SQLAlchemy, Alembic
├── frontend/         # SvelteKit
└── pseint/           # legado PSeInt (referencia)
```

Orden de construcción acordado: **1 → 2 → 3 → 6 → 5 → 9 → 4 → 8 → 7 → 10** (ver specs en `docs/superpowers/`).
