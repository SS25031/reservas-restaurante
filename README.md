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

## Cómo ejecutar el proyecto (Modo Usuario)

Si no eres programador o simplemente quieres usar el sistema sin instalar Python, puedes usar la versión ejecutable:

1. Descarga el archivo `main.exe` y el archivo `reservas_db.json`.
2. Asegúrate de colocar **ambos archivos en la misma carpeta** (por ejemplo, en una carpeta llamada "Sistema Reservas" en tu Escritorio).
3. Haz doble clic sobre `main.exe` para iniciar el programa.

> **Nota sobre Antivirus:** Al ser un ejecutable creado de forma independiente, Windows Defender podría mostrar una pantalla azul indicando "Windows protegió su PC". Esto es normal. Simplemente haz clic en **"Más información"** y luego en **"Ejecutar de todas formas"**.

---

## Cómo ejecutar el proyecto (Modo Desarrollador)

Asegúrate de tener Python instalado en tu sistema.

1. Clona este repositorio o descarga los archivos.
2. Abre una terminal en la carpeta raíz del proyecto.
3. Ejecuta el script principal:

```bash
python main.py
