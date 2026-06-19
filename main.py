from funcionalidades.crear_reserva import crear_reserva
from funcionalidades.ver_mesas import ver_mesas
from funcionalidades.editar_reserva import editar_reserva
from funcionalidades.cancelar_reserva import cancelar_reserva

def menu_principal():
    while True:
        print("=== SISTEMA DE RESERVAS ===")
        print("1. Crear una reserva")
        print("2. Ver reservas registradas")
        print("3. Editar una reserva")
        print("4. Eliminar una reserva")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        match opcion:
            case "1":
                crear_reserva()
            case "2":
                ver_mesas()
            case "3":
                editar_reserva()
            case "4":
                cancelar_reserva()
            case "0":
                print("Saliendo del sistema...")
                print("Hasta pronto!")
                break

if __name__ == "__main__":  
    menu_principal()
