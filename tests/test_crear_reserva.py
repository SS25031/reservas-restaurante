import unittest
from unittest.mock import patch
from config import reservas
from funcionalidades.crear_reserva import crear_reserva

class TestCrearReserva(unittest.TestCase):

    def setUp(self):
        reservas.clear() # La lista de reservas empieza vacia

    # @patch para simular datos de usuario
    @patch('builtins.input')
    def test_creacion_exitosa(self, mock_input):
        # Testing con datos correctos
        mock_input.side_effect = [
            "Carlos",      # Nombre
            "2026-07-08",  # Fecha
            "17:00",       # Hora
            "2"            # Cantidad de personas
        ]

        # Llamada a la funcion
        crear_reserva()

        # confirmar que los cambios ocurrieron de forma correcta
        self.assertEqual(len(reservas), 1)  # Debe haber exactamente 1 reserva guardada
        self.assertEqual(reservas[0]["cliente"], "Carlos")  # El nombre debe coincidir
        self.assertEqual(reservas[0]["mesa"], 1)  # Se ;e debe asignar la mesa #1 por ser el primero

    @patch('builtins.input')
    def test_creacion_con_reintentos_por_error(self, mock_input):
        
        # Testing con datos incorrectos o invalidos (fecha mala)
        mock_input.side_effect = [
            "María",       # Nombre
            "fecha_mala",  #Fecha incorrecta 
            "2026-07-08",  #Fecha correcta
            "18:30",       # Hora
            "4"            # Personas
        ]

        crear_reserva()

        self.assertEqual(len(reservas), 1)
        self.assertEqual(reservas[0]["cliente"], "María")
        self.assertEqual(reservas[0]["fecha"], "2026-07-08") # Guarda la fecha corregida

if __name__ == '__main__':
    unittest.main()