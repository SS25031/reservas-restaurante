//FUNCIONES
//Funcion HacerReservacion

SubProceso HacerReservacion(capacidadMesas, reservacionMesa, totalReservas Por Referencia)
	
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
						
						//Recorre las 23 mesas ara buscar una que sirva y este libre
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
										
										reservacionMesa[totalReservas, 1] <- opc_dia
										reservacionMesa[totalReservas, 2] <- opc_turno
										reservacionMesa[totalReservas, 3] <- i // se guarda el numero de mesa
										
										reserva_hecha <- Verdadero
										
										Escribir "------------------------------------------"
										Escribir "La reserva se realizo con exito"
										Escribir "Se asigno la mesa numero: ", i
										Escribir "El numero de reserva es: ", totalReservas
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



Algoritmo reservas_restaurante
	Definir opc_menu Como Entero
	Definir totalReservas Como Entero
	Definir capacidadMesas Como Entero
	Definir reservacionMesa Como Entero
	Dimension capacidadMesas[25]
	Dimension reservacionMesa[100, 3]
	totalReservas <- 0

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
				HacerReservacion(capacidadMesas, reservacionMesa, totalReservas)
				
			2:	
				//Opcion 2: Ver reservas
				
			3: 
				//Opcion 3: Cancelar/Eliminar una reserva
				
			4: 
				//Opcion 4: Editar una reserva
				
			5: 
				//Opcion 5: Ver mesas disponibles
			De Otro Modo:
				Escribir "Opcion no valida, intente nuevamente"
		Fin Segun
	Hasta Que opc_menu == 0
	Escribir "La sesion ha finalizado"
	
	//Fin Menu principal
	
	
	
	
FinAlgoritmo
