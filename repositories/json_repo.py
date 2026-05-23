"""JSON-file-backed reservation repository."""

import json
from datetime import date
from pathlib import Path
from typing import Any

from models import Reserva, Turno


class JsonReservaRepository:
    """Persists reservations to a single JSON file.

    File schema::

        {
          "ultimo_id": 3,
          "reservas": [
            {"id": 1, "fecha": "2026-06-01", "turno": "NOCHE",
             "numero_mesa": 3, "cliente": "Ana Pérez",
             "telefono": "7000-1234", "personas": 2},
            ...
          ]
        }
    """

    def __init__(self, ruta: Path):
        self._ruta = Path(ruta)

    def cargar(self) -> tuple[list[Reserva], int]:
        if not self._ruta.exists():
            return [], 0
        with self._ruta.open("r", encoding="utf-8") as f:
            data = json.load(f)
        ultimo_id = int(data.get("ultimo_id", 0))
        reservas = [self._reserva_desde_dict(d) for d in data.get("reservas", [])]
        return reservas, ultimo_id

    def guardar(self, reservas: list[Reserva], ultimo_id: int) -> None:
        payload: dict[str, Any] = {
            "ultimo_id": ultimo_id,
            "reservas": [self._reserva_a_dict(r) for r in reservas],
        }
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        with self._ruta.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _reserva_a_dict(r: Reserva) -> dict[str, Any]:
        return {
            "id": r.id,
            "fecha": r.fecha.isoformat(),
            "turno": r.turno.name,
            "numero_mesa": r.numero_mesa,
            "cliente": r.cliente,
            "telefono": r.telefono,
            "personas": r.personas,
        }

    @staticmethod
    def _reserva_desde_dict(d: dict[str, Any]) -> Reserva:
        return Reserva(
            id=int(d["id"]),
            fecha=date.fromisoformat(d["fecha"]),
            turno=Turno[d["turno"]],
            numero_mesa=int(d["numero_mesa"]),
            cliente=str(d["cliente"]),
            telefono=str(d["telefono"]),
            personas=int(d["personas"]),
        )
