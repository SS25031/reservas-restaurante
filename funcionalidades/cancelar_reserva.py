from config import reservas

def cancelar_reserva():
    print("\n=== CANCELAR RESERVAS ===")

    if not reservas:
        print("[!] No hay reservas registradas en el sistema.\n")
        return
    # Buscar cliente
    nombre_busqueda = input("Ingrese el nombre del cliente cuya reserva quiere eliminar: ").strip().lower()

    # Encontrar coincidencias
    coincidencias = [res for res in reservas if res["cliente"].lower() == nombre_busqueda]

    if not coincidencias:
        print(f"[!] No se encontro ninguna reserva a nombre de '{nombre_busqueda}'.\n")
        return
    
    # Si encuentra coincidencias, elige cual eliminar
    print(f"\nSe encontraron {len(coincidencias)} reserva(s) para '{nombre_busqueda}':")
    for idx, res in enumerate(coincidencias, start=1):
        print(f"{idx}. Fecha: {res['fecha']} | Hora: {res['hora']} | Personas: {res['personas']} | Mesa #{res['mesa']}")

    # Seleccionar la reserva a eliminar
    while True:
        try:
            seleccion = int(input("\nSeleccione el numero de la reserva que desea eliminar (0 para cancelar): "))
            if seleccion == 0:
                print("Operacion cancelada.\n")
                return
            if 1 <= seleccion <= len(coincidencias):
                reserva_a_cancelar = coincidencias[seleccion - 1]
                break
            print("[!] Seleccion invalida.")
        except ValueError:
            print("[!] Por favor, ingrese un numero entero valido.")
    
    # Confirmacion de seguridad
    confirmacion = input(f"Esta seguro que desea eliminar la reserva de {reserva_a_cancelar['cliente'].upper()}? (s/n): ")

    if confirmacion == 's':
        # Se elimina el dict de la lista global
        reservas.remove(reserva_a_cancelar)
        print(f"[*] La reserva se ha eliminado correctamente!")
        print(f"La Mesa #{reserva_a_cancelar['mesa']} vuelve a estar libre.\n")
    else:
        print("[!] Proceso cancelado. La reserva sigue activa.\n")