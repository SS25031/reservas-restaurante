from funcionalidades.crear_reserva import crear_reserva

def menu_principal():
    while True:
        print("=== SISTEMA DE RESERVAS ===")
        print("1. Crear una reserva")
        print("2. Ver todas las reservas")
        print("3. Editar una reserva")
        print("4. Eliminar una reserva")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        match opcion:
            case "1":
                crear_reserva()
            case "2":
                pass
            case "0":
                print("Saliendo del sistema...")
                print("Hasta pronto!")
                break

if __name__ == "__main__":  
    menu_principal()
