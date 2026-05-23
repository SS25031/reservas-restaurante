"""Entry point: `python main.py`.

Los datos se persisten en ~/.reservas-restaurante/reservas.json.
"""

from pathlib import Path

from repositories import JsonReservaRepository
from restaurante import construir_mesas
from services import ReservaService
from ui import ConsoleUI

ARCHIVO_DATOS = Path.home() / ".reservas-restaurante" / "reservas.json"


def main() -> None:
    mesas = construir_mesas()
    repo = JsonReservaRepository(ARCHIVO_DATOS)
    service = ReservaService.cargar_desde(mesas, repo)
    ui = ConsoleUI(service, on_mutation=lambda: service.persistir_en(repo))
    ui.run()


if __name__ == "__main__":
    main()
