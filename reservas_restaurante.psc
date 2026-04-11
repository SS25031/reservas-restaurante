//FUNCIONES
//Funcion HacerReservacion

SubProceso HacerReservacion(capacidadMesas, reservacionMesa, totalReservas Por Referencia, contadorID Por Referencia)
	
	Definir cantidad_personas, opc_dia, opc_turno, i, contador_dia  Como Entero
	Definir mesa_encontrada Como Logico
	
	
	Escribir "*** Usted esta creando una nueva reserva ***"
	
	Escribir "Ingrese la cantidad de personas para la reserva: "
	Leer cantidad_personas
	//VALIDAR CAPACIDAD
	//verificar que haya mesa disponible con la capacidad de mesa adecuada (capacidadMesas)
	mesa_encontrada <- Falso
	
	Para i <- 1 Hasta 25 Hacer
		Si capacidadMesas[i] >= cantidad_personas Entonces
			mesa_encontrada <- Verdadero
		FinSi
	FinPara
	Si mesa_encontrada == Falso Entonces
		Escribir "Lo sentimos, no hay mesas disponibles para la cantidad de personas especificada"
		//FIN VALIDAR CAPACIDAD
	SiNo
		//VALIDAR DIA DE LA RESERVA
		Escribir "Seleccione el dia para la reserva: "
		Escribir "1. Lunes"
		Escribir "2. Martes"
		Escribir "3. Miercoles"
		Escribir "4. Jueves"
		Escribir "5. Viernes"
		Escribir "6. Sabado"
		Escribir "7. Domingo"
		Leer  opc_dia
		
		Si opc_dia >= 1 y opc_dia <= 7 Entonces
			//Validar que ese dia no este excedido de reservas (maximo 25 reservas por dia-- )
			contador_dia <- 0
			
			Si totalReservas > 0 Entonces
				//Revisar cuantas reservas hay en dia seleccionado
				Para i <- 1 Hasta totalReservas Hacer
					Si reservacionMesa[i, 1] == opc_dia Entonces
						contador_dia <- contador_dia + 1
					FinSi
				FinPara
			FinSi
			
			
			Si contador_dia >= 25 Entonces
				Escribir "Lo sentimos, este dia ya alcanzo el limite maximo de 25 reservas"
			SiNo
				//VALIDAR TURNO
				Escribir "Ingrese el turno para la reserva"
				Escribir "1. Manana"
				Escribir "2. Tarde"
				Escribir "3. Noche"
				Leer opc_turno
				
				Segun opc_turno Hacer
					1,2,3:
						//VALIDART TURNO
						//Una reserva no choque con otra (misma dia y mismo turno)
						
						Definir reserva_hecha, mesa_ocupada como Logico
						Definir j Como Entero
						reserva_hecha <- Falso // no se ha guardado nada
						
						//Recorre las 25 mesas ara buscar una que sirva y este libre
						Para i <- 1 Hasta 25 Hacer
							//Solo busca si no se se ha hecho la reservacion todavia
							Si reserva_hecha == Falso Entonces
								//1. verifica la capacidad de la mesa
								Si capacidadMesas[i] >= cantidad_personas Entonces
									mesa_ocupada <- Falso // esta libre
									//2. verifica que no choque con otra reserva
									Si totalReservas > 0 Entonces
										Para j <- 1 Hasta totalReservas Hacer
											Si reservacionMesa[j, 1] == opc_dia y reservacionMesa[j, 2] == opc_turno y reservacionMesa[j, 3] == i Entonces
												mesa_ocupada <- Verdadero //hay choque de reservas
											FinSi
										FinPara
									FinSi
									
									//3. Si no hay choque:
									Si mesa_ocupada == Falso Entonces
										totalReservas <- totalReservas + 1
										contadorID <- contadorID + 1
										
										reservacionMesa[totalReservas, 1] <- opc_dia
										reservacionMesa[totalReservas, 2] <- opc_turno
										reservacionMesa[totalReservas, 3] <- i // se guarda el numero de mesa
										reservacionMesa[totalReservas, 4] <- contadorID // ID unico y permanente
										
										reserva_hecha <- Verdadero
										
										Escribir "------------------------------------------"
										Escribir "La reserva se realizo con exito"
										Escribir "Se asigno la mesa numero: ", i
										Escribir "El ID de su reserva es: ", contadorID
										Escribir "------------------------------------------"
									FinSi
								FinSi
							FinSi
						FinPara
						Si reserva_hecha == Falso Entonces
							Escribir "Lo sentimos, no hay mesas disponibles para el turno seleccionado"
						FinSi
					De Otro Modo:
						Escribir "El turno ingresado no es valido"
				FinSegun
				//FIN VALIDAR TURNO
			FinSi
		SiNo
			Escribir "El dia ingresado no es valido, intente nuevamente"
		FinSi
		//FIN VALIDAR DIA DE LA RESERVA
	FinSi
FinSubProceso



//Funcion VerReservas
SubProceso VerReservas(reservacionMesa, capacidadMesas, totalReservas)
	Definir i, opc_ver, id_buscar, pos_encontrada Como Entero
	Definir nombre_dia, nombre_turno Como Cadena
	
	Escribir "*** VER RESERVAS ***"
	
	Si totalReservas == 0 Entonces
		Escribir "No hay reservas registradas"
	SiNo
		Escribir "1. Ver todas las reservas"
		Escribir "2. Buscar reserva por ID"
		Leer opc_ver
		
		Segun opc_ver Hacer
			1:
				//Mostrar todas las reservas
				Escribir "Total de reservas: ", totalReservas
				Escribir "------------------------------------------"
				
				Para i <- 1 Hasta totalReservas Hacer
					Segun reservacionMesa[i, 1] Hacer
						1: nombre_dia <- "Lunes"
						2: nombre_dia <- "Martes"
						3: nombre_dia <- "Miercoles"
						4: nombre_dia <- "Jueves"
						5: nombre_dia <- "Viernes"
						6: nombre_dia <- "Sabado"
						7: nombre_dia <- "Domingo"
					FinSegun
					
					Segun reservacionMesa[i, 2] Hacer
						1: nombre_turno <- "Manana"
						2: nombre_turno <- "Tarde"
						3: nombre_turno <- "Noche"
					FinSegun
					
					Escribir "ID de Reserva: ", reservacionMesa[i, 4]
					Escribir "Dia: ", nombre_dia
					Escribir "Turno: ", nombre_turno
					Escribir "Mesa: ", reservacionMesa[i, 3], " (Capacidad: ", capacidadMesas[reservacionMesa[i, 3]], " personas)"
					Escribir "------------------------------------------"
				FinPara
				
			2:
				//Buscar por ID
				Escribir "Ingrese el ID de la reserva a buscar: "
				Leer id_buscar
				
				pos_encontrada <- 0
				Para i <- 1 Hasta totalReservas Hacer
					Si reservacionMesa[i, 4] == id_buscar Entonces
						pos_encontrada <- i
					FinSi
				FinPara
				
				Si pos_encontrada == 0 Entonces
					Escribir "No se encontro ninguna reserva con el ID ingresado"
				SiNo
					Segun reservacionMesa[pos_encontrada, 1] Hacer
						1: nombre_dia <- "Lunes"
						2: nombre_dia <- "Martes"
						3: nombre_dia <- "Miercoles"
						4: nombre_dia <- "Jueves"
						5: nombre_dia <- "Viernes"
						6: nombre_dia <- "Sabado"
						7: nombre_dia <- "Domingo"
					FinSegun
					
					Segun reservacionMesa[pos_encontrada, 2] Hacer
						1: nombre_turno <- "Manana"
						2: nombre_turno <- "Tarde"
						3: nombre_turno <- "Noche"
					FinSegun
					
					Escribir "------------------------------------------"
					Escribir "ID de Reserva: ", reservacionMesa[pos_encontrada, 4]
					Escribir "Dia: ", nombre_dia
					Escribir "Turno: ", nombre_turno
					Escribir "Mesa: ", reservacionMesa[pos_encontrada, 3], " (Capacidad: ", capacidadMesas[reservacionMesa[pos_encontrada, 3]], " personas)"
					Escribir "------------------------------------------"
				FinSi
				
			De Otro Modo:
				Escribir "Opcion no valida"
		FinSegun
	FinSi
FinSubProceso



//Funcion CancelarReserva
SubProceso CancelarReserva(reservacionMesa Por Referencia, capacidadMesas, totalReservas Por Referencia)
	Definir id_reserva, pos_reserva, i Como Entero
	Definir nombre_dia, nombre_turno Como Cadena
	Definir confirmacion Como Caracter
	
	Escribir "*** CANCELAR RESERVA ***"
	
	Si totalReservas == 0 Entonces
		Escribir "No hay reservas registradas"
	SiNo
		Escribir "Ingrese el ID de la reserva a cancelar: "
		Leer id_reserva
		
		//Buscar la posicion de la reserva con ese ID
		pos_reserva <- 0
		Para i <- 1 Hasta totalReservas Hacer
			Si reservacionMesa[i, 4] == id_reserva Entonces
				pos_reserva <- i
			FinSi
		FinPara
		
		Si pos_reserva == 0 Entonces
			Escribir "No se encontro ninguna reserva con el ID ingresado"
		SiNo
			//Mostrar datos de la reserva antes de confirmar
			Segun reservacionMesa[pos_reserva, 1] Hacer
				1: nombre_dia <- "Lunes"
				2: nombre_dia <- "Martes"
				3: nombre_dia <- "Miercoles"
				4: nombre_dia <- "Jueves"
				5: nombre_dia <- "Viernes"
				6: nombre_dia <- "Sabado"
				7: nombre_dia <- "Domingo"
			FinSegun
			
			Segun reservacionMesa[pos_reserva, 2] Hacer
				1: nombre_turno <- "Manana"
				2: nombre_turno <- "Tarde"
				3: nombre_turno <- "Noche"
			FinSegun
			
			Escribir "------------------------------------------"
			Escribir "ID de Reserva: ", reservacionMesa[pos_reserva, 4]
			Escribir "Dia: ", nombre_dia
			Escribir "Turno: ", nombre_turno
			Escribir "Mesa: ", reservacionMesa[pos_reserva, 3], " (Capacidad: ", capacidadMesas[reservacionMesa[pos_reserva, 3]], " personas)"
			Escribir "------------------------------------------"
			Escribir "Esta seguro que desea cancelar esta reserva? (S/N): "
			Leer confirmacion
			
			Si confirmacion == "S" o confirmacion == "s" Entonces
				//Desplazar las reservas siguientes solo si hay elementos despues de la cancelada
				Si pos_reserva <= totalReservas - 1 Entonces
					Para i <- pos_reserva Hasta totalReservas - 1 Hacer
						reservacionMesa[i, 1] <- reservacionMesa[i + 1, 1]
						reservacionMesa[i, 2] <- reservacionMesa[i + 1, 2]
						reservacionMesa[i, 3] <- reservacionMesa[i + 1, 3]
						reservacionMesa[i, 4] <- reservacionMesa[i + 1, 4]
					FinPara
				FinSi
				
				//Limpiar la ultima posicion
				reservacionMesa[totalReservas, 1] <- 0
				reservacionMesa[totalReservas, 2] <- 0
				reservacionMesa[totalReservas, 3] <- 0
				reservacionMesa[totalReservas, 4] <- 0
				
				totalReservas <- totalReservas - 1
				
				Escribir "------------------------------------------"
				Escribir "La reserva ha sido cancelada exitosamente"
				Escribir "------------------------------------------"
			SiNo
				Escribir "Cancelacion abortada, la reserva sigue activa"
			FinSi
		FinSi
	FinSi
FinSubProceso

// Marcos Alas: Funcion Ver mesas disponibles
SubProceso VerMesasDisponibles(reservacionMesa, capacidadMesas, totalReservas)
	Definir dia, turno, i, j Como Entero
	Definir ocupada Como Logico
	
	Escribir "*** MESAS DISPONIBLES ***"
	
	Escribir "Ingrese dia (1-7):"
	Leer dia
	
	Escribir "Ingrese turno (1-3):"
	Leer turno
	
	Para i <- 1 Hasta 25 Hacer
		ocupada <- Falso
		
		Para j <- 1 Hasta totalReservas Hacer
			Si reservacionMesa[j,1] == dia y reservacionMesa[j,2] == turno y reservacionMesa[j,3] == i Entonces
				ocupada <- Verdadero
			FinSi
		FinPara
		
		Si ocupada == Falso Entonces
			Escribir "Mesa ", i, " disponible (Capacidad: ", capacidadMesas[i], ")"
		FinSi
	FinPara
FinSubProceso


// Marcos Alas: Funcion Editar Reserva
SubProceso EditarReserva(reservacionMesa Por Referencia, totalReservas)
	Definir id_buscar, pos, i, nuevo_dia, nuevo_turno Como Entero
	Definir conflicto Como Logico
	
	Escribir "*** EDITAR RESERVA ***"
	
	Si totalReservas == 0 Entonces
		Escribir "No hay reservas"
	SiNo
		
		Escribir "ID:"
		Leer id_buscar
		
		pos <- 0
		
		Para i <- 1 Hasta totalReservas Hacer
			Si reservacionMesa[i,4] == id_buscar Entonces
				pos <- i
			FinSi
		FinPara
		
		Si pos == 0 Entonces
			Escribir "No encontrada"
		SiNo
			
			Escribir "Nuevo dia:"
			Leer nuevo_dia
			
			Escribir "Nuevo turno:"
			Leer nuevo_turno
			
			conflicto <- Falso
			
			Para i <- 1 Hasta totalReservas Hacer
				Si i <> pos Entonces
					Si reservacionMesa[i,1]==nuevo_dia y reservacionMesa[i,2]==nuevo_turno y reservacionMesa[i,3]==reservacionMesa[pos,3] Entonces
						conflicto <- Verdadero
					FinSi
				FinSi
			FinPara
			
			Si conflicto Entonces
				Escribir "Conflicto de horario"
			SiNo
				reservacionMesa[pos,1] <- nuevo_dia
				reservacionMesa[pos,2] <- nuevo_turno
				Escribir "Actualizada"
			FinSi
			
		FinSi
	FinSi
FinSubProceso


Algoritmo reservas_restaurante
	Definir opc_menu Como Entero
	Definir totalReservas Como Entero //guarda la cantidad de reservas hechas
	Definir contadorID Como Entero //ID unico y permanente por reserva
	Definir capacidadMesas Como Entero
	Definir reservacionMesa Como Entero
	Dimension capacidadMesas[25] //Total de mesas disponibles en el restaurante
	Dimension reservacionMesa[100, 4] //Se pueden guardar hasta 100 reservaciones: dia, turno, numero de mesa, ID permanente
	totalReservas <- 0
	contadorID <- 0

	//Capacidad para cada mesa (asignacion)
	
	Para i <- 1 Hasta 5 Con Paso 1 Hacer
		capacidadMesas[i] <- 2
	Fin Para
	Para i <- 6 Hasta 10 con Paso 1 Hacer
		capacidadMesas[i] <- 4
	FinPara
	Para i <- 11 Hasta 15 Con Paso  1 Hacer
		capacidadMesas[i] <- 6
	FinPara
	Para i <- 16 Hasta 20 Con Paso 1 Hacer
		capacidadMesas[i] <- 8
	FinPara
	Para i <- 21 Hasta 25 Con Paso 1 Hacer
		capacidadMesas[i] <- 10
	FinPara
	
	//Fin Capacidad para cada mesa
	
	//Menu principal
	Repetir
		Escribir "*** BIENVENIDO AL SISTEMA DE RESERVAS ***"
		Escribir "Por favor, seleccione una opcion del menu:"
		Escribir "1. Hacer una reserva"
		Escribir "2. Ver reservas"
		Escribir "3. Cancelar/Eliminar una reserva"
		Escribir "4. Editar una reserva"
		Escribir "5. Ver mesas disponibles"
		Escribir "0. Salir"
		Leer opc_menu
		
		Segun opc_menu Hacer
			Opcion 1:
				//Opcion 1: Hacer una reservacion
				HacerReservacion(capacidadMesas, reservacionMesa, totalReservas, contadorID)
				
			2:	
				//Opcion 2: Ver reservas
				VerReservas(reservacionMesa, capacidadMesas, totalReservas)
				
			3: 
				//Opcion 3: Cancelar/Eliminar una reserva
				CancelarReserva(reservacionMesa, capacidadMesas, totalReservas)
				
		    4:
                //Opcion4 Editar la reserva Marcos Alas 
				EditarReserva(reservacionMesa, totalReservas)

			5: 
                //Opcion 5 Ver las mesas disponibles Marcos Alas 
				VerMesasDisponibles(reservacionMesa, capacidadMesas, totalReservas) 

			De Otro Modo:
				Escribir "Opcion no valida, intente nuevamente"

		Fin Segun
	Hasta Que opc_menu == 0
	Escribir "La sesion ha finalizado"
	
	//Fin Menu principal
	
FinAlgoritmo
