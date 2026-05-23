"""Entry point: `python -m reservas_restaurante`.

Distribución de mesas (25 en total):
  Mesas  1– 5  →  capacidad 2
  Mesas  6–10  →  capacidad 4
  Mesas 11–15  →  capacidad 6
  Mesas 16–20  →  capacidad 8
  Mesas 21–25  →  capacidad 10
"""

from .models import Mesa
from .services import ReservaService
from .ui import ConsoleUI


def construir_mesas() -> list[Mesa]:
    layout = [
        (range(1, 6), 2),
        (range(6, 11), 4),
        (range(11, 16), 6),
        (range(16, 21), 8),
        (range(21, 26), 10),
    ]
    return [Mesa(numero=n, capacidad=cap) for rng, cap in layout for n in rng]


def main() -> None:
    mesas = construir_mesas()
    service = ReservaService(mesas)
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()
