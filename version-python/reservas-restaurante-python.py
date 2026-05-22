# Creacion de las listas para almacenar las mesas y su capacidad

# Mesa #1 - Mesa #5
mesa_1_5 = [2, 2, 2, 2, 2]
# Mesa#6 - Mesa #10
mesa_6_10 = [4, 4, 4, 4, 4]
# Mesa #11 - Mesa #15
mesa_11_15 = [6, 6, 6, 6, 6]
# Mesa #16 - Mesa #20
mesa_16_20 = [8, 8, 8, 8, 8]
# Mesa #21 - #25
mesa_21_25 = [10, 10, 10, 10, 10]

# Unir las listas en una sola
mesas = mesa_1_5 + mesa_6_10 + mesa_11_15 + mesa_16_20 + mesa_21_25

# Disponibilidad de mesas
# 7 dias, cada uno con 3 turnos
# cada mesa inicia como False (libre) en todos los turnos(dia, tarde, noche)
calendario = [[[False] * 25 for turno in range(3)] for dia in range(7)]

# -----------------------------------------------#
# FUNCIONES
# -----------------------------------------------#

# 1. FUNCION PARA CREAR RESERVAS#


def crear_reserva(nombre_cliente, dia_reserva, turno_reserva, personas, calendario):

    # Listas para asociarlas a cada dia y turno que el usuario elija
    nombre_turno = ["Dia", "Tarde", "Noche"]
    nombre_dia = ["Lunes", "Martes", "Miercoles",
                  "Jueves", "Viernes", "Sabado", "Domingo"]

    # Obtener el dia y turno de la reserva
    mesas_del_turno = calendario[dia_reserva][turno_reserva]

    # Contar las mesas ocupadas
    mesas_ocupadas = mesas_del_turno.count(True)

    # Verificar si el turno esta full (25 reservas) o aun hay espacio
    # Si esta lleno, devuelve un mensaje indicando que no hay dispo
    if mesas_ocupadas == 25:
        return "Lo sentimos, el turno seleccionado ya se encuentra lleno."
    # recorre las 25 mesas en busca de la disponibilidad (False) y la capacidad adecuada
    else:
        for i in range(len(mesas)):
            if mesas_del_turno[i] == False and mesas[i] >= personas:
                mesas_del_turno[i] = True
                mesa_asignada = i + 1
                return f"{nombre_cliente}, su reserva fue realizada con exito!. Su numero de mesa es la # {mesa_asignada} para el dia {nombre_dia[dia_reserva]} en el turno de/la {nombre_turno[turno_reserva]}"
    return "No se encontraron mesas disponibles con la capacidad requerida"


# 2. FUNCION PARA CANCELAR UNA RESERVA#
def cancelar_reserva(dia, turno, numero_mesa, calendario):
    indice_mesa = numero_mesa - 1

    if calendario[dia][turno][indice_mesa] == True:
        calendario[dia][turno][indice_mesa] = False
        return f"La reserva en la mesa {numero_mesa} fue cancelada con exito."
    else:
        return f"Parece que la mesa {numero_mesa} ya estaba libre. No se produjeron cambios."


# MENU PRINCIPAL#
while True:
    print("#-------------------------------------#")
    print("	    SISTEMA DE RESERVAS         ")
    print("     RESTAURANTE 'El Corrientazo'    ")
    print("#-------------------------------------#")
    print("1. Realizar reserva")
    print("2. Cancelar reserva")
    print("3. Ver mesas disponibles")
    print("4. Salir del sistema")

    opcion = input("Selecciona una opcion(1-4): ")

    match opcion:
        case "1":
            # Funcion crear_reserva()
            print("#---NUEVA RESERVA---#")

            # Capturar el nombre del usuario
            nombre = input("Por favor, ingresa un nombre: ")

            # Capturar el dia para la reserva
            print("0. Lunes")
            print("1. Martes")
            print("2. Miercoles")
            print("3. Jueves")
            print("4. Viernes")
            print("5. Sabado")
            print("6. Domingo")
            while True:
                try:
                    dia = int(input("Seleccione el dia para su reserva (0-6):"))
                    # Condicion: la opcion del menu ingresada debe estar entre 0 y 6
                    if 0 <= dia <= 6:
                        break  # Si el valor esta entre el rango definido, rompe la exepcion y continua
                    else:
                        print("Por favor, ingrese un numero valido entre 0 y 6")
                except ValueError:
                    print("No se deben ingresar letras, solo numeros")

            # Capturar el turno
            print("0. Dia")
            print("1. Tarde")
            print("2. Noche")
            while True:
                try:
                    turno = int(input("Seleccione un turno (0-2):"))
                    if (0 <= turno <= 2):
                        break
                    else:
                        print("Por favor, ingrese un numero valido entre  0 y 2")
                except ValueError:
                    print("No se debn ingresar letras, solo numeros")

            # Capturar cantidad de personas
            personas = int(
                input("Ingrese la cantidad de personas para la reserva: "))
            # PENDIENTE: validar ingreso de numeros negativos, letras o espacios vacios

            # Llamada a la funcion crear_reserva()
            print("#---RESUMEN DE LA RESERVA---#")
            reserva_creada = crear_reserva(
                nombre, dia, turno, personas, calendario)
            print(reserva_creada)
        case "2":
            # Funcion cancelar_reserva()
            print("#---CANCELAR RESERVA---#")
            # Capturar el dia:
            print(
                "0.Lunes | 1. Martes | 2. Miercoles | 3. Jueves | 4. Viernes | 5. Sabado | 6. Domingo")
            while True:
                try:
                    dia = int(
                        input("Ingrese el dia agendado para su reserva(0-6):"))
                    # Condicion: la opcion del menu ingresada debe estar entre 0 y 6
                    if 0 <= dia <= 6:
                        break  # Si el valor esta entre el rango definido, rompe la exepcion y continua
                    else:
                        print("Por favor, ingrese un numero valido entre 0 y 6")
                except ValueError:
                    print("No se deben ingresar letras, solo numeros")

            # Capturar el turno
            print("0. Dia | 1. Tarde | 2. Noche")
            while True:
                try:
                    turno = int(input(
                        "Ingrese el turno agendado para la reserva (0-2):"))
                    if 0 <= turno <= 2:
                        break
                    else:
                        print("Por favor, ingrese un numero valido entre 0 y 2")
                except ValueError:
                    print("No se deben ingresar letras, solo numeros")

            # Capturar el # de mesa
            while True:
                try:
                    num_mesa = int(input("Ingrese su numero de mesa (1-25):"))
                    if 1 <= num_mesa <= 25:
                        break
                    else:
                        print(
                            f"El numero de mesa {num_mesa} no existe o no es valido. Intente de nuevo")
                except ValueError:
                    print("No se deben ingresar letras, solo numeros")
            print("#---ESTADO DE LA CANCELACION---#")
            reserva_cancelada = cancelar_reserva(
                dia, turno, num_mesa, calendario)
            print(reserva_cancelada)
        case "3":
            # Funcion ver_mesas()
            pass
        case "4":
            # Salida del sistema
            print("Saliendo del sistema...")
            print("Hasta pronto!")
            break
