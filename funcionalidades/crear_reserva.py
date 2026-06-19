from config import reservas, CAPACIDAD_MESAS
from  validaciones import validar_fecha, validar_hora


def crear_reserva():
    print("=== CREANDO RESERVA NUEVA ===")

    # Recolectar datos
    nombre_cliente = input("Ingrese nombre del cliente:")

    # Validacion: FECHA
    while True:
        fecha_reserva = input("Ingrese la fecha para la reserva (AAA-MM-DD): ")
        if validar_fecha(fecha_reserva):
            break  # Formato correcto
        print("[!] Formato de fecha incorrecto o fecha invalida. Por favor usar formato AAA-MM-DD (Ej: 2026-06-19)")
    # Validacion: HORA
    while True:
        hora_reserva = input("Ingrese la hora para la reserva (HH:MM)")
        if validar_hora(hora_reserva):
            break  # Formato correcto
        print("[!] Formato de fecha incorrecto o invalido. Por favor usar formato de 24 horas (Ej: 19:30)")

    # Validacion: CANTIDAD DE PERSONAS (NUMERO)
    while True:
        try:
            personas = int(input("Cantidad de personas para la reserva: "))
            if personas > 0:
                break  # Numero valido
            print("[!] La cantidad de personas debe ser mayor a 0")
        except ValueError:
            print("Por favor, ingrese un numero entero valido")

    # Empaquetar la informacion en un dict
    nueva_reserva = {
        "cliente": nombre_cliente,
        "fecha": fecha_reserva,
        "hora": hora_reserva,
        "personas": personas,
        "mesa": mesa_asignada
    }

    mesa_asignada = None
    encontrada = False

    # Asignar mesa en base a capacidad
    for mesa, capacidad in CAPACIDAD_MESAS.items():
        if personas <= capacidad:
            # Filtro de fecha/hora
            mesa_ocupada = False
            for res in reservas:
                if res["mesa"] == mesa and res["fecha"] == fecha_reserva and res["hora"] == hora_reserva:
                    mesa_ocupada = True
                    break
            if not mesa_ocupada:
                mesa_asignada = mesa
                encontrada = True
                break
            # Si pasa el filtro, se asigna
            mesa_asignada = mesa
            encontrada = True
            break  # se detiene al encontrar una mesa
    # Si no encontro mesa:
    if not encontrada:
        print("[!] No hay mesas disponibles en este momento")
        return
    # Si se encuentra mesa, se guarda la informacion en el dict con la mesa asignada
    nueva_reserva = {
        "cliente": nombre_cliente,
        "fecha": fecha_reserva,
        "hora": hora_reserva,
        "personas": personas,
        "mesa": mesa_asignada
    }

    # Agg el dict al final de la lista reservas[]
    reservas.append(nueva_reserva)
    print("[*] Reserva creada con exito!")  # Msj de confirmacion
