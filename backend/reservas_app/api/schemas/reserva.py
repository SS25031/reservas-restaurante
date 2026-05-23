"""Serialización de reservas para la API admin."""

from datetime import date

from reservas_app.exceptions import ValorInvalidoError
from reservas_app.models import Reserva, Turno


def turno_desde_api(valor: str) -> Turno:
    try:
        return Turno[valor]
    except KeyError as exc:
        msg = f"Turno inválido: {valor}. Use MANANA, TARDE o NOCHE."
        raise ValorInvalidoError(msg) from exc


def reserva_a_dict(reserva: Reserva) -> dict[str, object]:
    return {
        "id": reserva.id,
        "fecha": reserva.fecha.isoformat(),
        "turno": reserva.turno.name,
        "turno_label": reserva.turno.value,
        "numero_mesa": reserva.numero_mesa,
        "cliente": reserva.cliente,
        "telefono": reserva.telefono,
        "email": reserva.email,
        "personas": reserva.personas,
        "estado": reserva.estado.value,
    }


def parse_fecha(valor: date | str) -> date:
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(valor)
