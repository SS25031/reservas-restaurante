import unittest
from unittest.mock import patch
from config import reservas
from funcionalidades.editar_reserva import editar_reserva

class TestEditarReserva(unittest.TestCase):

    def setUp(self):
        # Limpiar lista y cargar datos de prueba
        reservas.clear()
        reservas.append({
            "cliente": "Sandra",
            "fecha": "2026-07-24",
            "hora": "17:00",
            "personas": 2,
            "mesa": 1
        })

    @patch('builtins.input')
    def test_editar_cantidad_personas(self, mock_input):
        # Prueba que se pueda cambiar la cantidad de personas correctamente:
        # Secuencia de inputs simulados:
        # 1. Nombre: "Sandra"
        # 2. Elegir reserva coincidente: "1"
        # 3. Elegir que editar: "3" (Cantidad de personas)
        # 4. Nuevo valor: "4"
        mock_input.side_effect = ["Sandra", "1", "3", "4"]
        
        editar_reserva()
        
        # Validar que en la lista global, el numero haya cambiado
        self.assertEqual(reservas[0]["personas"], 4)

    @patch('builtins.input')
    def test_editar_fecha(self, mock_input):
       # Prueba que se pueda cambiar la fecha de la reserva
        # Secuencia: 
        # - Busca 'Sandra'
        # - Elige 1 (coincidencia)
        # - Elige 1 (Cambiar fecha)
        # - Nueva feca '2026-10-31'
        mock_input.side_effect = ["Sandra", "1", "1", "2026-10-31"]
        
        editar_reserva()
        
        # Validar que la fecha cambio existosamente
        self.assertEqual(reservas[0]["fecha"], "2026-10-31")

    @patch('builtins.input')
    def test_cancelar_edicion_en_submenu(self, mock_input):
        # Prueba que los datos NO cambien si el usuario decide cancelar en el sub-menu
        # Secuencia: Busca "Sandra" -> Elige "1" -> Elige "0" (Cancelar)
        # Secuencia:
        # - Busca 'Sandra'
        # - Elige '0' (cancelar)
        mock_input.side_effect = ["Sandra", "1", "0"]
        
        editar_reserva()
        
        # Validar que la reserva continue activa
        self.assertEqual(reservas[0]["personas"], 2)
        self.assertEqual(reservas[0]["fecha"], "2026-07-24")

if __name__ == '__main__':
    unittest.main()