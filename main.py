"""Entry point: `python main.py`."""

from restaurante import construir_mesas
from services import ReservaService
from ui import ConsoleUI


def main() -> None:
    mesas = construir_mesas()
    service = ReservaService(mesas)
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()
