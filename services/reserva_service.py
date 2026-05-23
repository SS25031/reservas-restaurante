from typing import Optional
from models import Mesa, Reserva

MAX_RESERVAS_POR_DIA = 25


class ReservaService:
    """
    Handles all reservation business logic.
    Keeps mesas and reservas collections entirely in memory.
    """

    def __init__(self, mesas: list[Mesa]):
        self.mesas: list[Mesa] = mesas
        self._reservas: list[Reserva] = []
        self._contador_id: int = 0

    # ------------------------------------------------------------------ #
    # Public read helpers                                                  #
    # ------------------------------------------------------------------ #

    @property
    def total_reservas(self) -> int:
        return len(self._reservas)

    def todas_las_reservas(self) -> list[Reserva]:
        return list(self._reservas)

    def buscar_por_id(self, reserva_id: int) -> Optional[Reserva]:
        for r in self._reservas:
            if r.id == reserva_id:
                return r
        return None

    def mesas_disponibles(self, dia: int, turno: int) -> list[Mesa]:
        ocupadas = {
            r.numero_mesa
            for r in self._reservas
            if r.dia == dia and r.turno == turno
        }
        return [m for m in self.mesas if m.numero not in ocupadas]

    # ------------------------------------------------------------------ #
    # Mutation operations                                                  #
    # ------------------------------------------------------------------ #

    def hacer_reserva(
        self, personas: int, dia: int, turno: int
    ) -> tuple[bool, str, Optional[Reserva]]:
        """
        Attempt to create a reservation.
        Returns (success, message, reserva_or_None).
        """
        # 1. At least one table can hold the group
        if not any(m.puede_acomodar(personas) for m in self.mesas):
            return False, "No hay mesas con capacidad suficiente.", None

        # 2. Day not over its daily cap
        reservas_dia = sum(1 for r in self._reservas if r.dia == dia)
        if reservas_dia >= MAX_RESERVAS_POR_DIA:
            return False, "Este dia ya alcanzo el limite de 25 reservas.", None

        # 3. Find a free table that fits the group
        mesa = self._primera_mesa_libre(personas, dia, turno)
        if mesa is None:
            return False, "No hay mesas disponibles para el turno seleccionado.", None

        # 4. Persist
        self._contador_id += 1
        reserva = Reserva(
            id=self._contador_id,
            dia=dia,
            turno=turno,
            numero_mesa=mesa.numero,
            capacidad_mesa=mesa.capacidad,
        )
        self._reservas.append(reserva)
        return True, "Reserva realizada con exito.", reserva

    def cancelar_reserva(self, reserva_id: int) -> tuple[bool, str]:
        reserva = self.buscar_por_id(reserva_id)
        if reserva is None:
            return False, "No se encontro ninguna reserva con ese ID."
        self._reservas.remove(reserva)
        return True, "Reserva cancelada exitosamente."

    def editar_reserva(
        self, reserva_id: int, nuevo_dia: int, nuevo_turno: int
    ) -> tuple[bool, str]:
        reserva = self.buscar_por_id(reserva_id)
        if reserva is None:
            return False, "No se encontro ninguna reserva con ese ID."

        # Check conflict: same mesa, same new day/turn, different reservation
        conflicto = any(
            r.dia == nuevo_dia
            and r.turno == nuevo_turno
            and r.numero_mesa == reserva.numero_mesa
            and r.id != reserva_id
            for r in self._reservas
        )
        if conflicto:
            return False, "Conflicto de horario con otra reserva existente."

        reserva.dia = nuevo_dia
        reserva.turno = nuevo_turno
        return True, "Reserva actualizada exitosamente."

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _primera_mesa_libre(
        self, personas: int, dia: int, turno: int
    ) -> Optional[Mesa]:
        ocupadas = {
            r.numero_mesa
            for r in self._reservas
            if r.dia == dia and r.turno == turno
        }
        for mesa in self.mesas:
            if mesa.puede_acomodar(personas) and mesa.numero not in ocupadas:
                return mesa
        return None
