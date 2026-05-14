# ==========================================
#                  CLASES
# ==========================================

class Mesa:
    def __init__(self, numero, capacidad):
        self.numero = numero
        self.capacidad = capacidad
        
    def __str__(self):
        # Imprimir informacion de la mesa
        return f"Mesa {self.numero} (Capacidad: {self.capacidad} personas)"

class Reserva:
    def __init__(self, id_reserva, dia, turno, mesa):
        self.id_reserva = id_reserva
        self.dia = dia
        self.turno = turno
        self.mesa = mesa # Guarda el obj 'Mesa' completo
        
    def __str__(self):
        # Resumen de ticket
        return f"Reserva #{self.id_reserva} | Día: {self.dia} | Turno: {self.turno} | {self.mesa}"


# ==========================================
#               CLASE PRINCIPAL
# ==========================================

class SistemaReservas:
    def __init__(self):
        self.mesas = []      # Lista vaci para guardar las 25 mesas
        self.reservas = []   # Lista vacia para los tickets de reserva
        self.contador_id = 0 # Contador para los IDs de las reservas
        
        
        self._inicializar_mesas() 

    def _inicializar_mesas(self):

        # Mesas 1 al 5 (Capacidad 2)
        for i in range(1, 6):
            self.mesas.append(Mesa(i, 2))
            
        # Mesas 6 al 10 (Capacidad 4)
        for i in range(6, 11):
            self.mesas.append(Mesa(i, 4))
            
        # Mesas 11 al 15 (Capacidad 6)
        for i in range(11, 16):
            self.mesas.append(Mesa(i, 6))
            
        # Mesas 16 al 20 (Capacidad 8)
        for i in range(16, 21):
            self.mesas.append(Mesa(i, 8))
            
        # Mesas 21 al 25 (Capacidad 10)
        for i in range(21, 26):
            self.mesas.append(Mesa(i, 10))

    # ---------------------------------------------------------
    #                       METODOS
    # ---------------------------------------------------------

    def hacer_reserva(self):
        #METODOD: hacer_reserva()
        print("\n*** Usted esta creando una nueva reserva ***")
        
        try:
            cantidad = int(input("Ingrese la cantidad de personas para la reserva: "))
        except ValueError:
            print("Error: Por favor ingrese un número válido.")
            return # Detiene la funcion y regresa al menu

        
        mesas_adecuadas = []
        for mesa in self.mesas:
            if mesa.capacidad >= cantidad:
                mesas_adecuadas.append(mesa)
                
        if not mesas_adecuadas: # Si la lista quedo vacia
            print("Lo sentimos, no hay mesas con capacidad suficiente para esa cantidad de personas.")
            return

        #PEDIR Dia DE LA RESERVA
        print("\nSeleccione el día para la reserva:")
        print("1. Lunes | 2. Martes | 3. Miércoles | 4. Jueves | 5. Viernes | 6. Sábado | 7. Domingo")
        dia = input("Día (1-7): ")
        
        if dia not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Día no válido. Operación cancelada.")
            return

        #PEDIR TURNO Y VALIDAR CAPACIDAD MAXIMA
        turno_valido = False
        
        while not turno_valido: # Repetir hasta que elija un turno con DISPO
            print("\nSeleccione el turno:")
            print("1. Mañana | 2. Tarde | 3. Noche | 0. Cancelar")
            turno = input("Turno (1-3) o 0 para salir: ")
            
            if turno == "0":
                print("Reserva cancelada por el usuario.")
                return
            elif turno not in ["1", "2", "3"]:
                print("Turno no válido. Intente de nuevo.")
                continue # Regresa al inicio del while
                
            # Contar reservas para este dia Y este turno especifico
            reservas_en_este_turno = 0
            for r in self.reservas:
                if r.dia == dia and r.turno == turno:
                    reservas_en_este_turno += 1
            
            # validar si el turno elegido ya alcazo las 25 reservas
            if reservas_en_este_turno >= 25:
                print(f"\nLo sentimos, el turno {turno} esta LLENO para este dia.")
                print("Por favor, seleccione un turno distinto.")
               
            else:
                turno_valido = True 

        #BUSCAR LA MESA Y ASIGNAR
        mesa_asignada = None 
        
        #Solo revisa las mesas con la capacidad correcta
        for mesa in mesas_adecuadas:
            mesa_ocupada = False
            
            # Revisar si hay choque
            for r in self.reservas:
                if r.dia == dia and r.turno == turno and r.mesa.numero == mesa.numero:
                    mesa_ocupada = True
                    break 
            
            if not mesa_ocupada:
                mesa_asignada = mesa 
                break 

        #GUARDAR LA RESERVA FINAL
        if mesa_asignada:
            self.contador_id += 1 # Aumentar el ID único
            # TICKET
            nueva_reserva = Reserva(self.contador_id, dia, turno, mesa_asignada)
            
            # Guardar reserva
            self.reservas.append(nueva_reserva) 
            
            print("\nReserva realizada con éxito!")
            print(nueva_reserva) # Imprimir el ticket
        else:
            print("\nLo sentimos, no hay mesas disponibles con esa capacidad para ese día y turno.")
        print("\n*** Usted está creando una nueva reserva ***")
        pass

    #--------------------------------------------------------------------------------------------------#

    def ver_reservas(self):
        #METODO ver_reservas()
        print("\n*** LISTADO DE RESERVAS ***")
        pass

    def cancelar_reserva(self):
        # METODO: cancelar_reserva()
        print("\n*** CANCELAR RESERVA ***")
        pass

    def editar_reserva(self):
        # METODO: editar_reserva()
        print("\n*** EDITAR RESERVA ***")
        pass

    def ver_mesas_disponibles(self):
        # METODO: ver_mesas_disponibles()
        print("\n*** VER MESAS DISPONIBLES ***")
        pass


# ==========================================
#               MENÚ PRINCIPAL
# ==========================================

def main():
    sistema = SistemaReservas() # Inicializacion para cargar las 25 mesas
    
    while True:
        print("\n" + "="*40)
        print("*** BIENVENIDO AL SISTEMA DE RESERVAS ***")
        print("="*40)
        print("1. Hacer una reserva")
        print("2. Ver reservas")
        print("3. Cancelar/Eliminar una reserva")
        print("4. Editar una reserva")
        print("5. Ver mesas disponibles")
        print("0. Salir")
        
        opc = input("\nSeleccione una opción: ")
        
        if opc == "1":
            sistema.hacer_reserva()
        elif opc == "2":
            sistema.ver_reservas()
        elif opc == "3":
            sistema.cancelar_reserva()
        elif opc == "4":
            sistema.editar_reserva()
        elif opc == "5":
            sistema.ver_mesas_disponibles()
        elif opc == "0":
            print("Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()