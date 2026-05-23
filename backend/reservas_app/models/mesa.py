class Mesa:
    """Representa una mesa del restaurante con capacidad fija."""

    def __init__(
        self,
        numero: int,
        capacidad: int,
        pos_x: float | None = None,
        pos_y: float | None = None,
    ):
        self.numero = numero
        self.capacidad = capacidad
        self.pos_x = pos_x
        self.pos_y = pos_y

    def puede_acomodar(self, personas: int) -> bool:
        return self.capacidad >= personas

    def __repr__(self) -> str:
        return f"Mesa(numero={self.numero}, capacidad={self.capacidad})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mesa):
            return NotImplemented
        return (
            self.numero == other.numero
            and self.capacidad == other.capacidad
            and self.pos_x == other.pos_x
            and self.pos_y == other.pos_y
        )
