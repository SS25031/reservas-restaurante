class Mesa:
    """Represents a restaurant table with a fixed capacity."""

    def __init__(self, numero: int, capacidad: int):
        self.numero = numero
        self.capacidad = capacidad

    def puede_acomodar(self, personas: int) -> bool:
        return self.capacidad >= personas

    def __repr__(self) -> str:
        return f"Mesa(numero={self.numero}, capacidad={self.capacidad})"
