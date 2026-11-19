from config import reservas
from validaciones import validar_fecha

def _imprimir_tabla(lista_a_mostrar, titulo_reporte):
    print(f"=== {titulo_reporte} ===")

    if not lista_a_mostrar:
        print("[!] No hay ninguna reserva registrada para este criterio. \n")
        return
    #CABECERA DE LA TABLA
    print(f"{'CLIENTE':<20} | {'FECHA':<12} | {'HORA':<8} | {'PERSONAS':<8} | {'MESA':}")
    print("-" * 65)

    for res in lista_a_mostrar:
       print(f"{res['cliente']:<20} | {res['fecha']:<12} | {res['hora']:<8} | {res['personas']:^8} | Mesa #{res['mesa']}")
       print("-----------------------------------------------------------------") 

    print(f"TOTAL DE RESERVAS MOSTRADAS: ", {len(lista_a_mostrar)})


def ver_mesas():
    while True:
       print("=== VER RESERVAS ===")
       print("1. Ver todas las reservas")
       print("2. Filtrar busqueda por fecha")
       print("0. Volver al menu principal")

       opcion = input("Seleccione una opcion: ")

       match opcion:
            case "1":
               _imprimir_tabla(reservas, "LISTA GENERAL DE RESERVAS")

            case "2":
                while True:
                   fecha_busqueda = input("Ingrese la fecha a consultar (AAA-MM-DD)")
                   if validar_fecha(fecha_busqueda):
                       break
                   print("[!] Formato incorrecto. Intente de nuevo (Ej: 2026-07-08)")

                reservas_filtradas = [res for res in reservas if res["fecha"] == fecha_busqueda]
                _imprimir_tabla(reservas_filtradas, f"RESERVAS DEL DIA{fecha_busqueda}")
            
            case "0":
                print("Regresando al menu principal...\n")
                break
            case _:
                print("[!] Opcion no valida. Intente de nuevo. \n")
   
