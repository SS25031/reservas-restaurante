# Sistema de Gestión de Reservas

Un sistema de línea de comandos (CLI) robusto y modular desarrollado en Python para gestionar las reservas de un restaurante. El proyecto aplica principios de desarrollo limpio, persistencia de datos en formato JSON y cobertura de pruebas automatizadas.

---

## Características Principales

* **CRUD Completo:** Creación, lectura, actualización y eliminación de reservas.
* **Asignación Inteligente:** Filtra y asigna mesas automáticamente basándose en la capacidad requerida y la disponibilidad de fecha y hora.
* **Persistencia de Datos:** Las reservas se guardan localmente en un archivo `reservas_db.json`, permitiendo que los datos sobrevivan al cierre de la aplicación.
* **Validación de Entradas:** Manejo estricto de formatos de fecha (AAA-MM-DD), hora (HH:MM) y capacidades para evitar caídas del sistema.
* **Pruebas Automatizadas:** Suite de testing construida con `unittest` y `mock` para asegurar la estabilidad de cada módulo.

---

## Arquitectura del Proyecto

El código está refactorizado en una estructura modular para facilitar su escalabilidad:

| Directorio/Archivo | Descripción |
| :--- | :--- |
| `main.py` | Punto de entrada y menú interactivo principal. |
| `config.py` | Variables globales, diccionario de mesas y gestión de archivos JSON. |
| `validaciones.py` | Funciones de validación para fechas y horas. |
| `funcionalidades/` | Carpeta con los scripts independientes para cada operación CRUD. |
| `tests/` | Pruebas unitarias para validar la lógica y simular el ingreso de datos. |

---

## Cómo ejecutar el proyecto (Modo Desarrollador)

Asegúrate de tener Python instalado en tu sistema.

1. Clona este repositorio o descarga los archivos.
2. Abre una terminal en la carpeta raíz del proyecto.
3. Ejecuta el script principal:

```bash
python main.py
```

## Ejemplos de uso: Creacion de Reserva

```bash
=== SISTEMA DE RESERVAS ===
1. Crear una reserva
2. Ver reservas registradas
3. Editar una reserva
4. Eliminar una reserva
0. Salir

Seleccione una opcion: 1

=== NUEVA RESERVA ===
Ingrese el nombre del cliente: Carlos
Ingrese la fecha (AAA-MM-DD): 2026-07-08
Ingrese la hora (HH:MM): 17:00
Ingrese la cantidad de personas: 4

[*] ¡Reserva creada con éxito! Mesa #6 asignada.

```
## Ejemplo de Uso: Edicion de Reserva
```bash
=== SISTEMA DE RESERVAS ===
1. Crear una reserva
2. Ver reservas registradas
3. Editar una reserva
4. Eliminar una reserva
0. Salir
Seleccione una opcion: 3

=== EDITAR RESERVAS ===
Ingrese el nombre del cliente a editar: Armando Mendoza

Se encontraron 1 reserva(s) para 'armando mendoza':
1. Fecha: 2026-07-16 | Hora: 17:00 | Personas: 2 | Mesa #1

Seleccione el numero de la reserva qe desea editar (0 para cancelar):1

Qué dato desea modificar?
1. Fecha
2. Hora
3. Cantidad de personas
0. Cancelar
Seleccione una opcion: 2
Ingrese la nueva hora (HH:MM): 14:00

Reserva modificada exitosamente!
Nueva mesa asignada: #1

```

## Ejemplo de Uso: Cancelacion de Reservas
```bash
=== SISTEMA DE RESERVAS ===
1. Crear una reserva
2. Ver reservas registradas
3. Editar una reserva
4. Eliminar una reserva
0. Salir
Seleccione una opcion: 4

=== CANCELAR RESERVAS ===
Ingrese el nombre del cliente cuya reserva quiere eliminar: Lazaron Pinzon

Se encontraron 1 reserva(s) para 'lazaron pinzon':
1. Fecha: 2026-06-21 | Hora: 8:00 | Personas: 10 | Mesa #21

Seleccione el numero de la reserva que desea eliminar (0 para cancelar): 1
Esta seguro que desea eliminar la reserva de LAZARON PINZON? (s/n): s
[*] La reserva se ha eliminado correctamente!
La Mesa #21 vuelve a estar libre.
```


## Ejecucion de Pruebas(Testing)

El proyecto incluye pruebas automatizadas para garantizar el correcto funcionamiento de las validaciones y los flujos interactivos (CRUD).

Para ejecutar toda la batería de pruebas de una sola vez, asegúrate de estar posicionado en la carpeta raíz del proyecto y usa el siguiente comando:

```bash
python -m unittest discover -s tests
```
### Ejemplo de Salida Esperado

Si todo el código funciona correctamente, verás una serie de puntos (uno por cada prueba aprobada) seguido de un OK.

```bash
.....
----------------------------------------------------------------------
Ran 12 tests in 0.042s

OK
```

