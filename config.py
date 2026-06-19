import json
import os

ARCHIVO_JSON = "reservas_db.json"

TOTAL_MESAS = 25
reservas = []

CAPACIDAD_MESAS = {
    1: 2, 2: 2, 3: 2, 4: 2, 5: 2,  # Mesas para 2
    6: 4, 7: 4, 8: 4, 9: 4, 10: 4,  # Mesas para 4
    11: 6, 12: 6, 13: 6, 14: 6, 15: 6,  # Mesas para 6
    16: 8, 17: 8, 18: 8, 19: 8, 20: 8,  # Mesas para 8
    21: 10, 22: 10, 23: 10, 24: 10, 25: 10  # Mesas para 10
}

def cargar_datos():
    #Leer el archivo .json al inciar el programa. Si no existe, devuelve una lista vacia
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r") as archivo:
            return json.load(archivo)
    return []

def guardar_datos(lista_actual):
    #Sobreescribir el archivo json con la lista mas reciente de reservas
    with open(ARCHIVO_JSON, "w") as archivo:
        json.dump(lista_actual, archivo, indent=4)


reservas = cargar_datos()


