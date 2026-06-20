import unittest
from validaciones import validar_fecha, validar_hora

class TestValidaciones(unittest.TestCase):

    # === PRUEBAS PARA validar_fecha ===
    
    def test_fecha_correcta(self):
        """Prueba que el formato AAA-MM-DD sea aceptado"""
        self.assertTrue(validar_fecha("2026-07-08"))
        self.assertTrue(validar_fecha("2026-12-31"))

    def test_fecha_incorrecta(self):
        """Prueba que formatos invalidos sean rechazados"""
        self.assertFalse(validar_fecha("08-07-2026"))  # Formato europeo
        self.assertFalse(validar_fecha("2026/07/08"))  # Uso de barras
        self.assertFalse(validar_fecha("2026-13-01"))  # Mes invalido
        self.assertFalse(validar_fecha("texto_random")) # Sin formato de fecha

    # === PRUEBAS PARA validar_hora ===

    def test_hora_correcta(self):
        """Prueba que el formato HH:MM sea aceptado"""
        self.assertTrue(validar_hora("17:00"))
        self.assertTrue(validar_hora("09:30"))

    def test_hora_incorrecta(self):
        """Prueba que formatos de hora invlidos sean rechazados"""
        self.assertFalse(validar_hora("1700"))         # Sin dos puntos
        self.assertFalse(validar_hora("5:00 PM"))      # Formato 12h
        self.assertFalse(validar_hora("25:00"))        # Hora irreal
        self.assertFalse(validar_hora("hola"))         # Texto invalido

if __name__ == '__main__':
    unittest.main()