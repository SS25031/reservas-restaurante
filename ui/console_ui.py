"""Console-based user interface for the reservation system.

All business logic is delegated to `ReservaService`. Domain exceptions
raised by the service are caught here and rendered as friendly messages.
"""

from collections.abc import Callable
from datetime import date

from exceptions import ReservaError
from models import Turno
from services import ReservaService

OnMutation = Callable[[], None] | None


class ConsoleUI:
    """Handles all user interaction (input/output)."""

    SEP = "-" * 50

    def __init__(self, service: ReservaService, on_mutation: OnMutation = None):
        self.service = service
        self._on_mutation: Callable[[], None] = on_mutation or (lambda: None)

    # ---------------- main loop ----------------

    def run(self) -> None:
        print("*** BIENVENIDO AL SISTEMA DE RESERVAS ***")
        while True:
            self._mostrar_menu()
            opcion = self._leer_entero("Seleccione una opción: ", minimo=0, maximo=5)
            if opcion == 0:
                break
            self._despachar(opcion)
        print("La sesión ha finalizado.")

    # ---------------- menu ----------------

    def _mostrar_menu(self) -> None:
        print(f"\n{self.SEP}")
        print("1. Hacer una reserva")
        print("2. Ver reservas")
        print("3. Cancelar una reserva")
        print("4. Editar una reserva")
        print("5. Ver mesas disponibles")
        print("0. Salir")
        print(self.SEP)

    def _despachar(self, opcion: int) -> None:
        acciones: dict[int, Callable[[], None]] = {
            1: self._hacer_reserva,
            2: self._ver_reservas,
            3: self._cancelar_reserva,
            4: self._editar_reserva,
            5: self._ver_mesas_disponibles,
        }
        accion = acciones[opcion]
        try:
            accion()
        except ReservaError as e:
            print(f"\nError: {e}")

    # ---------------- feature handlers ----------------

    def _hacer_reserva(self) -> None:
        print("\n*** NUEVA RESERVA ***")
        cliente = self._leer_texto("Nombre del cliente: ")
        telefono = self._leer_texto("Teléfono: ")
        personas = self._leer_entero("Cantidad de personas: ", minimo=1)
        fecha = self._leer_fecha()
        turno = self._leer_turno()

        reserva = self.service.hacer_reserva(
            cliente=cliente,
            telefono=telefono,
            personas=personas,
            fecha=fecha,
            turno=turno,
        )
        print(f"\nReserva realizada con éxito:\n{reserva}")
        self._on_mutation()

    def _ver_reservas(self) -> None:
        print("\n*** VER RESERVAS ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        print("1. Ver todas las reservas")
        print("2. Buscar por ID")
        opcion = self._leer_entero("Opción: ", minimo=1, maximo=2)

        if opcion == 1:
            print(f"\nTotal de reservas: {self.service.total_reservas}")
            for r in self.service.todas_las_reservas():
                print(r)
        else:
            rid = self._leer_entero("ID de reserva: ", minimo=1)
            print(self.service.buscar_por_id(rid))

    def _cancelar_reserva(self) -> None:
        print("\n*** CANCELAR RESERVA ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        rid = self._leer_entero("ID de la reserva a cancelar: ", minimo=1)
        reserva = self.service.buscar_por_id(rid)
        print(reserva)
        if self._confirmar("¿Confirma la cancelación? (S/N): "):
            self.service.cancelar_reserva(rid)
            print("Reserva cancelada exitosamente.")
            self._on_mutation()
        else:
            print("Cancelación abortada. La reserva sigue activa.")

    def _editar_reserva(self) -> None:
        print("\n*** EDITAR RESERVA ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        rid = self._leer_entero("ID de la reserva a editar: ", minimo=1)
        reserva = self.service.buscar_por_id(rid)
        print(f"\nReserva actual:\n{reserva}")

        nueva_fecha = self._leer_fecha()
        nuevo_turno = self._leer_turno()

        actualizada = self.service.editar_reserva(
            rid, nueva_fecha=nueva_fecha, nuevo_turno=nuevo_turno
        )
        print(f"\nReserva actualizada:\n{actualizada}")
        self._on_mutation()

    def _ver_mesas_disponibles(self) -> None:
        print("\n*** MESAS DISPONIBLES ***")
        fecha = self._leer_fecha()
        turno = self._leer_turno()
        mesas = self.service.mesas_disponibles(fecha, turno)
        if not mesas:
            print("No hay mesas disponibles para esa fecha y turno.")
        else:
            for m in mesas:
                print(f"Mesa {m.numero:>2}  (Capacidad: {m.capacidad} personas)")

    # ---------------- input helpers ----------------

    def _leer_texto(self, prompt: str) -> str:
        while True:
            valor = input(prompt).strip()
            if valor:
                return valor
            print("El valor no puede estar vacío.")

    def _leer_entero(
        self,
        prompt: str,
        *,
        minimo: int | None = None,
        maximo: int | None = None,
    ) -> int:
        while True:
            try:
                valor = int(input(prompt))
            except ValueError:
                print("Ingrese un número entero válido.")
                continue
            if minimo is not None and valor < minimo:
                print(f"Debe ser ≥ {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Debe ser ≤ {maximo}.")
                continue
            return valor

    def _leer_fecha(self) -> date:
        print("Fecha en formato AAAA-MM-DD (ej. 2026-06-15)")
        while True:
            texto = input("Fecha: ").strip()
            try:
                return date.fromisoformat(texto)
            except ValueError:
                print("Formato inválido. Use AAAA-MM-DD.")

    def _leer_turno(self) -> Turno:
        print("Turnos: 1-Mañana  2-Tarde  3-Noche")
        valor = self._leer_entero("Turno (1-3): ", minimo=1, maximo=3)
        return Turno.desde_entero(valor)

    def _confirmar(self, prompt: str) -> bool:
        respuesta = input(prompt).strip().lower()
        return respuesta in {"s", "si", "sí", "y", "yes"}
