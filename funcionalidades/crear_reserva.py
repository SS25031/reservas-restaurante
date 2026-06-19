from config import reservas, CAPACIDAD_MESAS


def crear_reserva():
    #Recolectar datos
    nombre_cliente = input("Ingrese nombre del cliente:")
    fecha_reserva = input("Fecha para la reserva:")
    hora_reserva = input("Hora para la reserva:")
    personas = int(input("Cantidad de personas para la reserva: "))

    #Empaquetar la informacion en un dict
    nueva_reserva = {
    "cliente": nombre_cliente,
    "fecha": fecha_reserva,
    "hora": hora_reserva,
    "personas": personas,
    "mesa": 5
    }

    #Asignar mesa en base a capacidad
    for mesa, capacidad in CAPACIDAD_MESAS.items():
        pass

    reservas.append(nueva_reserva)#Agg el dict al final de la lista reservas[]
    print("[*] Reserva creada con exito!")#Msj de confirmacion