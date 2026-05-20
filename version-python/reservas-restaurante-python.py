#Creacion de las listas para almacenar las mesas y su capacidad

#Mesa #1 - Mesa #5
mesa_1_5 = [2, 2, 2, 2, 2]
#Mesa#6 - Mesa #10
mesa_6_10 = [4, 4, 4, 4, 4]
#Mesa #11 - Mesa #15
mesa_11_15 = [6, 6, 6, 6, 6]
#Mesa #16 - Mesa #20
mesa_16_20 = [8, 8, 8, 8, 8]
#Mesa #21 - #25
mesa_21_25 = [10, 10, 10, 10, 10]

#Unir las listas en una sola
mesas = mesa_1_5 + mesa_6_10 + mesa_11_15 + mesa_16_20 + mesa_21_25

#Disponibilidad de mesas
#7 dias, cada uno con 3 turnos
#cada mesa inicia como False (libre) en todos los turnos(dia, tarde, noche)
calendario = [[[False] * 25 for turno in range(3)] for dia in range(7)]

#-----------------------------------------------#
#		FUNCIONES
#-----------------------------------------------#


def crear_reserva(nombre_cliente, dia_reserva, turno_reserva, personas, calendario):
	#Obtener el dia y turno de la reserva
	mesas_del_turno = calendario[dia_reserva][turno_reserva]
	
	#Contar las mesas ocupadas
	mesas_ocupadas = mesas_del_turno.count(True)
	
	#Verificar si el turno esta full (25 reservas) o aun hay espacio
	#Si esta lleno, devuelve un mensaje indicando que no hay dispo
	if mesas_ocupadas == 25:
		return "Lo sentimos, el turno seleccionado ya se encuentra lleno."
	else:	#recorre las 25 mesas en busca de la disponibilidad (False) y la capacidad adecuada
		for i in range (len(mesas)):
			if mesas_del_turno[i] == False and mesas[i] >= personas:
				mesas_del_turno[i] = True
				mesa_asignada = i + 1
				return f"Reserva realizada con exito!. Mesa asignada: {mesa_asignada}"
	return "No se encontraron mesas disponibles con la capacidad requerida"
	

				
	








