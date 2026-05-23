# Sistema de Reservas de Restaurante

Backend FastAPI con persistencia SQLite (vía SQLAlchemy + Alembic) para gestionar reservas de un restaurante. Frontend SvelteKit en construcción.

> **Nota:** La CLI original (`python main.py`) fue retirada. El estado anterior persistía en `~/.reservas-restaurante/reservas.json` — ese archivo ya no se usa y puede borrarse manualmente.

## Distribución de mesas (default — configurable vía onboarding en subsistemas posteriores)

| Mesas  | Capacidad   |
| ------ | ----------- |
|  1– 5  | 2 personas  |
|  6–10  | 4 personas  |
| 11–15  | 6 personas  |
| 16–20  | 8 personas  |
| 21–25  | 10 personas |

Hasta **25 reservas/día** entre los turnos *Mañana*, *Tarde* y *Noche*.

## Requisitos

- Python ≥ 3.10

## Instalación

```bash
git clone <repo-url>
cd reservas-restaurante/backend
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/alembic upgrade head    # crea ./reservas.db
```

## Correr el servidor

```bash
cd backend
.venv/bin/uvicorn reservas_app.main:app --reload
# Probar: curl http://localhost:8000/health
```

## Desarrollo

```bash
cd backend
.venv/bin/pytest                # tests
.venv/bin/ruff check .          # lint
.venv/bin/ruff format .         # autoformat
.venv/bin/mypy                  # type check
.venv/bin/alembic upgrade head  # aplicar migraciones
```

## Arquitectura

```
reservas-restaurante/
├── backend/
│   ├── alembic/           # migraciones de base de datos
│   ├── reservas_app/
│   │   ├── main.py        # FastAPI app + endpoints
│   │   ├── config.py      # Configuración (incluye DATABASE_URL)
│   │   ├── db.py          # engine, SessionLocal, get_db()
│   │   ├── exceptions.py  # ReservaError + jerarquía
│   │   ├── models/        # DTOs (dataclasses) + ORM (SQLAlchemy)
│   │   ├── services/      # ReservaService (lógica de negocio)
│   │   └── repositories/  # ReservaRepository (Protocol) + SqlAlchemyReservaRepository
│   └── tests/             # pytest suite
└── pseint/                # prototipo PSeInt previo (legado, no se usa)
```

## Carpeta `pseint/`

Contiene un prototipo previo en PSeInt. Se mantiene únicamente como referencia histórica y **no** forma parte del sistema actual.
