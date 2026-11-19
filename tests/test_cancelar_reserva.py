import unittest
from unittest.mock import patch
from config import reservas
from funcionalidades.cancelar_reserva import cancelar_reserva

class TestCancelarReserva(unittest.TestCase):

    def setUp(self):
        # Limpiar lista y cargar una reserva de prueba
        reservas.clear()
        reservas.append({
            "cliente": "Sandra",
            "fecha": "2026-07-24",
            "hora": "17:00",
            "personas": 2,
            "mesa": 1
        })

    @patch('builtins.input')
    def test_eliminar_reserva_exitosa(self, mock_input):
    
        # Prueba que la confirmacion 's' funcione
        mock_input.side_effect = ["Sandra", "1", "s"]
        
        cancelar_reserva()
        
        # Confirma que la lista ahora debe estar vacia
        self.assertEqual(len(reservas), 0)

    @patch('builtins.input')
    def test_eliminar_reserva_arrepentida(self, mock_input):
        # Prueba que la confirmacion 'n' funcione
        mock_input.side_effect = ["Sandra", "1", "n"]
        
        cancelar_reserva()
        
        # Confirma que la lista sigue teniendo 1 elemento
        self.assertEqual(len(reservas), 1)

    @patch('builtins.input')
    def test_cliente_no_encontrado(self, mock_input):
        # Busca "Usuario", como no existe el programa se detiene ahi
        mock_input.side_effect = ["Usuario"]
        
        cancelar_reserva()
        
        # Si se cancela el proceso de eliminacion, la reserva se mantiene
        self.assertEqual(len(reservas), 1)

if __name__ == '__main__':
    unittest.main()