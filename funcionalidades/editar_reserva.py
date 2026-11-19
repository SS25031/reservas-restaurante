from config import reservas, CAPACIDAD_MESAS, guardar_datos
from validaciones import validar_fecha, validar_hora


def editar_reserva():
    print("\n=== EDITAR RESERVAS ===")

    if not reservas:
        print("[!] No hay reservas registradas en el sistema.\n")
        return
    # Buscar cliente
    nombre_busqueda = input(
        "Ingrese el nombre del cliente a editar: ").strip().lower()

    # Hallar coincidencias
    coincidencias = [
        res for res in reservas if res["cliente"].lower() == nombre_busqueda]

    if not coincidencias:
        print(
            f"[!] No se encontro ninguna reserva a nombre de {nombre_busqueda}.\n")
        return

    # Si existen coincidencias, elegir cual editar
    print(
        f"\nSe encontraron {len(coincidencias)} reserva(s) para '{nombre_busqueda}':")
    for idx, res in enumerate(coincidencias, start=1):
        print(
            f"{idx}. Fecha: {res['fecha']} | Hora: {res['hora']} | Personas: {res['personas']} | Mesa #{res['mesa']}")

    # Seleccionar indice
    while True:
        try:
            seleccion = int(
                input("\nSeleccione el numero de la reserva qe desea editar (0 para cancelar):"))
            if seleccion == 0:
                print("Operacion cancelada.\n")
                return
            if 1 <= seleccion <= len(coincidencias):
                reserva_a_editar = coincidencias = coincidencias[seleccion - 1]
                break
            print("[!] Seleccion invalida")
        except ValueError:
            print("[!] Por favor, ingrese un numero entero valido.")

    # Submenu para edicion
    print("\nQué dato desea modificar?")
    print("1. Fecha")
    print("2. Hora")
    print("3. Cantidad de personas")
    print("0. Cancelar")

    opcion = input("Seleccione una opcion: ")

    # Copia temporal para verificar si el cambio es posible
    fecha_nueva = reserva_a_editar["fecha"]
    hora_nueva = reserva_a_editar["hora"]
    personas_nuevas = reserva_a_editar["personas"]

    match opcion:
        case "1":
            while True:
                fecha_nueva = input("Ingrese la nueva fecha (AAAA-MM-DD): ")
                if validar_fecha(fecha_nueva):
                    break
                print("[!] Formato de fecha incorrecto.")
        case "2":
            while True:
                hora_nueva = input("Ingrese la nueva hora (HH:MM): ")
                if validar_hora(hora_nueva):
                    break
                print("[!] Formato de hora incorrecto.")
        case "3":
            while True:
                try:
                    personas_nuevas = int(
                        input("Ingrese la nueva cantidad de personas para la reserva: "))
                    if personas_nuevas > 0:
                        break
                    print("[!] La cantidad debe ser mayor a cero.")
                except ValueError:
                    print("[!] Ingrese un numero entero valido.")

        case "0":
            print("Edicion cancelada.")
            return
        case _:
            print("[!] Opcion invalida.\n")
            return

    # Validar disponibilidad de la mesa con los datos temporales
    # Remover la reserva actual para que no choque consigo misma

    reservas.remove(reserva_a_editar)
    mesa_asignada = None
    encontrada = False

    for mesa, capacidad in CAPACIDAD_MESAS.items():
        if personas_nuevas <= capacidad:
            mesa_ocupada = False
            for res in reservas:
                if res["mesa"] == mesa and res["fecha"] == fecha_nueva and res["hora"] == hora_nueva:
                    mesa_ocupada = True
                    break

            if not mesa_ocupada:
                mesa_asignada = mesa
                encontrada = True
                break
    if not encontrada:
        print(
            "[!] Error: No hay mesas disponibles o con capacidad suficiente para esta reserva")
        # Si la validacion falla, se vuelve a guardar la reserva sin cambios
        reservas.append(reserva_a_editar)
        return

    # Si pasa el filtro, se aplican los cambios
    reserva_a_editar["fecha"] = fecha_nueva
    reserva_a_editar["hora"] = hora_nueva
    reserva_a_editar["personas"] = personas_nuevas
    reserva_a_editar["mesa"] = mesa_asignada

    # Actualizar la lista global
    reservas.append(reserva_a_editar)
    guardar_datos(reservas)  # Guardar datos en formato .json

    print("\nReserva modificada exitosamente!")
    print(f"Nueva mesa asignada: #{mesa_asignada}\n")
