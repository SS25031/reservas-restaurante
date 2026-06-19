from datetime import datetime
# Validar fecha


def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False
 # Validar hora


def validar_hora(hora_texto):
    try:
        datetime.strptime(hora_texto, "%H:%M")
        return True
    except ValueError:
        return False
