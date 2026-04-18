# reservas-restaurante

Sistema de reservas para restaurante desarrollado en PSeInt.

## Funcionalidades

| Opcion | Estado | Descripcion |
|--------|--------|-------------|
| 1. Hacer una reserva | Completo | Valida capacidad, dia, turno y disponibilidad de mesa. Asigna un ID permanente a cada reserva |
| 2. Ver reservas | Completo | Lista todas las reservas activas con su ID, dia, turno, mesa y capacidad |
| 3. Cancelar una reserva | Completo | Busca por ID permanente, muestra los datos para confirmar y elimina la reserva |
| 4. Editar una reserva | Completo | Busca por ID y pide ingresar nuevo dia y turno para esa reservacion y la actualiza|
| 5. Ver mesas disponibles | Completo | Muestra las mesas disponibles por dia|

## Estructura de datos

- `capacidadMesas[25]`: arreglo con la capacidad de cada mesa (2, 4, 6, 8 o 10 personas)
- `reservacionMesa[100, 4]`: matriz de reservas con columnas `[dia, turno, mesa, ID]`
- `contadorID`: contador global que genera IDs permanentes; solo crece, nunca se reinicia

## Mesas

| Mesas | Capacidad |
|-------|-----------|
| 1 – 5 | 2 personas |
| 6 – 10 | 4 personas |
| 11 – 15 | 6 personas |
| 16 – 20 | 8 personas |
| 21 – 25 | 10 personas |