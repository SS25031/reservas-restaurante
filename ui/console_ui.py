from models import Dia, Turno
from services import ReservaService


class ConsoleUI:
    """
    Handles all user interaction (input/output).
    Delegates every business decision to ReservaService.
    """

    SEP = "-" * 42

    def __init__(self, service: ReservaService):
        self.service = service

    # ------------------------------------------------------------------ #
    # Main loop                                                            #
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        print("*** BIENVENIDO AL SISTEMA DE RESERVAS ***")
        while True:
            self._mostrar_menu()
            opcion = self._leer_entero("Seleccione una opcion: ")
            if opcion == 0:
                break
            self._despachar(opcion)
        print("La sesion ha finalizado.")

    # ------------------------------------------------------------------ #
    # Menu                                                                 #
    # ------------------------------------------------------------------ #

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
        acciones = {
            1: self._hacer_reserva,
            2: self._ver_reservas,
            3: self._cancelar_reserva,
            4: self._editar_reserva,
            5: self._ver_mesas_disponibles,
        }
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opcion no valida, intente nuevamente.")

    # ------------------------------------------------------------------ #
    # Feature handlers                                                     #
    # ------------------------------------------------------------------ #

    def _hacer_reserva(self) -> None:
        print("\n*** NUEVA RESERVA ***")
        personas = self._leer_entero("Cantidad de personas: ")
        dia = self._leer_dia()
        turno = self._leer_turno()

        ok, mensaje, reserva = self.service.hacer_reserva(personas, dia, turno)
        if ok:
            print(f"\n{reserva}")
        else:
            print(f"\nError: {mensaje}")

    def _ver_reservas(self) -> None:
        print("\n*** VER RESERVAS ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        print("1. Ver todas las reservas")
        print("2. Buscar por ID")
        opcion = self._leer_entero("Opcion: ")

        if opcion == 1:
            print(f"\nTotal de reservas: {self.service.total_reservas}")
            for r in self.service.todas_las_reservas():
                print(r)

        elif opcion == 2:
            rid = self._leer_entero("ID de reserva: ")
            reserva = self.service.buscar_por_id(rid)
            if reserva:
                print(reserva)
            else:
                print("No se encontro ninguna reserva con ese ID.")
        else:
            print("Opcion no valida.")

    def _cancelar_reserva(self) -> None:
        print("\n*** CANCELAR RESERVA ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        rid = self._leer_entero("ID de la reserva a cancelar: ")
        reserva = self.service.buscar_por_id(rid)
        if not reserva:
            print("No se encontro ninguna reserva con ese ID.")
            return

        print(reserva)
        confirmacion = input("¿Confirma la cancelacion? (S/N): ").strip().upper()
        if confirmacion == "S":
            ok, mensaje = self.service.cancelar_reserva(rid)
            print(mensaje)
        else:
            print("Cancelacion abortada. La reserva sigue activa.")

    def _editar_reserva(self) -> None:
        print("\n*** EDITAR RESERVA ***")
        if self.service.total_reservas == 0:
            print("No hay reservas registradas.")
            return

        rid = self._leer_entero("ID de la reserva a editar: ")
        reserva = self.service.buscar_por_id(rid)
        if not reserva:
            print("No se encontro ninguna reserva con ese ID.")
            return

        print(f"\nReserva actual:\n{reserva}")
        nuevo_dia = self._leer_dia()
        nuevo_turno = self._leer_turno()

        ok, mensaje = self.service.editar_reserva(rid, nuevo_dia, nuevo_turno)
        print(mensaje)

    def _ver_mesas_disponibles(self) -> None:
        print("\n*** MESAS DISPONIBLES ***")
        dia = self._leer_dia()
        turno = self._leer_turno()
        mesas = self.service.mesas_disponibles(dia, turno)
        if not mesas:
            print("No hay mesas disponibles para ese dia y turno.")
        else:
            for m in mesas:
                print(f"Mesa {m.numero:>2}  (Capacidad: {m.capacidad} personas)")

    # ------------------------------------------------------------------ #
    # Input helpers                                                        #
    # ------------------------------------------------------------------ #

    def _leer_entero(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Ingrese un numero entero valido.")

    def _leer_dia(self) -> int:
        print("Dias: 1-Lunes  2-Martes  3-Miercoles  4-Jueves  5-Viernes  6-Sabado  7-Domingo")
        while True:
            dia = self._leer_entero("Dia (1-7): ")
            if 1 <= dia <= 7:
                return dia
            print("Dia invalido. Ingrese un valor entre 1 y 7.")

    def _leer_turno(self) -> int:
        print("Turnos: 1-Manana  2-Tarde  3-Noche")
        while True:
            turno = self._leer_entero("Turno (1-3): ")
            if 1 <= turno <= 3:
                return turno
            print("Turno invalido. Ingrese 1, 2 o 3.")
