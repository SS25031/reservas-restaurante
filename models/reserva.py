from dataclasses import dataclass
from enum import Enum


class Dia(Enum):
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7

    @classmethod
    def nombre(cls, valor: int) -> str:
        return cls(valor).name.capitalize()


class Turno(Enum):
    MANANA = 1
    TARDE = 2
    NOCHE = 3

    @classmethod
    def nombre(cls, valor: int) -> str:
        return cls(valor).name.capitalize()


@dataclass
class Reserva:
    """Represents a single reservation."""

    id: int
    dia: int          # 1–7  (Dia enum value)
    turno: int        # 1–3  (Turno enum value)
    numero_mesa: int
    capacidad_mesa: int

    @property
    def nombre_dia(self) -> str:
        return Dia.nombre(self.dia)

    @property
    def nombre_turno(self) -> str:
        return Turno.nombre(self.turno)

    def __str__(self) -> str:
        sep = "-" * 42
        return (
            f"{sep}\n"
            f"ID de Reserva : {self.id}\n"
            f"Dia           : {self.nombre_dia}\n"
            f"Turno         : {self.nombre_turno}\n"
            f"Mesa          : {self.numero_mesa}  "
            f"(Capacidad: {self.capacidad_mesa} personas)\n"
            f"{sep}"
        )
