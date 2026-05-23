# Sistema de Reservas de Restaurante

CLI para gestionar reservas en un restaurante con 25 mesas distribuidas por capacidad. Persistencia local en JSON.

## Distribución de mesas

| Mesas  | Capacidad   |
| ------ | ----------- |
|  1– 5  | 2 personas  |
|  6–10  | 4 personas  |
| 11–15  | 6 personas  |
| 16–20  | 8 personas  |
| 21–25  | 10 personas |

Cada día permite hasta **25 reservas** distribuidas entre los turnos *Mañana*, *Tarde* y *Noche*.

## Requisitos

- Python ≥ 3.10

## Instalación

```bash
git clone <repo-url>
cd reservas-restaurante
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Uso

```bash
.venv/bin/python main.py
```

Los datos se persisten en `~/.reservas-restaurante/reservas.json`.

## Desarrollo

```bash
.venv/bin/pytest                # tests
.venv/bin/ruff check .          # lint
.venv/bin/ruff format .         # autoformat
.venv/bin/mypy .                # type check (uses pyproject.toml's [tool.mypy] files)
```

## Arquitectura

```
reservas-restaurante/
├── main.py            # composition root + entry point
├── config.py          # Configuración (límites configurables)
├── exceptions.py      # ReservaError + jerarquía de excepciones del dominio
├── restaurante.py     # construir_mesas() — layout fijo de 25 mesas
├── models/            # Mesa, Reserva, Turno
├── services/          # ReservaService (lógica de negocio)
├── repositories/      # ReservaRepository (Protocol) + JsonReservaRepository
├── ui/                # ConsoleUI
├── tests/             # pytest suite
└── pseint/            # prototipo PSeInt previo (legado, no se usa)
```

Los errores de dominio (`ReservaError` y subclases) son lanzados por el servicio y capturados por la UI. La capa de persistencia es intercambiable vía el `Protocol` `ReservaRepository`.

## Carpeta `pseint/`

Contiene un prototipo previo en PSeInt. Se mantiene únicamente como referencia histórica y **no** forma parte del sistema actual.
