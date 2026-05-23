"""
Entry point for the restaurant reservation system.

Table layout (25 tables):
  Mesas  1– 5  →  capacity 2
  Mesas  6–10  →  capacity 4
  Mesas 11–15  →  capacity 6
  Mesas 16–20  →  capacity 8
  Mesas 21–25  →  capacity 10
"""

import sys
import os

# Allow imports from the restaurante/ package root
sys.path.insert(0, os.path.dirname(__file__))

from models import Mesa
from services import ReservaService
from ui import ConsoleUI


def build_mesas() -> list[Mesa]:
    layout = [
        (range(1, 6), 2),
        (range(6, 11), 4),
        (range(11, 16), 6),
        (range(16, 21), 8),
        (range(21, 26), 10),
    ]
    return [Mesa(numero=n, capacidad=cap) for rng, cap in layout for n in rng]


def main() -> None:
    mesas = build_mesas()
    service = ReservaService(mesas)
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()
