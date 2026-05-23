"""Reservation domain model."""

from dataclasses import dataclass
from datetime import date
from enum import Enum

from reservas_app.exceptions import ValorInvalidoError

_NOMBRES_DIA_SEMANA: dict[int, str] = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}


class Turno(Enum):
    """Tres turnos diarios del restaurante."""

    MANANA = "Mañana"
    TARDE = "Tarde"
    NOCHE = "Noche"

    @classmethod
    def desde_entero(cls, valor: int) -> "Turno":
        """Convierte 1/2/3 a Turno. Lanza ValorInvalidoError si está fuera de rango."""
        mapping = {1: cls.MANANA, 2: cls.TARDE, 3: cls.NOCHE}
        if valor not in mapping:
            raise ValorInvalidoError(
                f"Turno inválido: {valor}. Use 1 (Mañana), 2 (Tarde) o 3 (Noche)."
            )
        return mapping[valor]


@dataclass
class Reserva:
    """Una reserva concreta para una mesa en una fecha y turno dados."""

    id: int
    fecha: date
    turno: Turno
    numero_mesa: int
    cliente: str
    telefono: str
    personas: int

    @property
    def nombre_dia(self) -> str:
        return _NOMBRES_DIA_SEMANA[self.fecha.weekday()]

    @property
    def nombre_turno(self) -> str:
        return self.turno.value

    def __str__(self) -> str:
        sep = "-" * 50
        return (
            f"{sep}\n"
            f"ID de Reserva : {self.id}\n"
            f"Cliente       : {self.cliente}\n"
            f"Teléfono      : {self.telefono}\n"
            f"Fecha         : {self.fecha.isoformat()} ({self.nombre_dia})\n"
            f"Turno         : {self.nombre_turno}\n"
            f"Mesa          : {self.numero_mesa}\n"
            f"Personas      : {self.personas}\n"
            f"{sep}"
        )
