PI REST de Productos

Descripción

API REST desarrollada con Python y FastAPI para administrar productos
mediante los métodos HTTP GET, POST, PUT y DELETE.

El proyecto incluye validación de datos con Pydantic, manejo de errores,
documentación automática con Swagger UI y un mecanismo básico de
observabilidad mediante logs y métricas.

Tecnologías

Python 3.11

FastAPI

Uvicorn

Pydantic

Swagger UI

Git y GitHub

Estructura del proyecto

API_guia/
├── .venv/
├── main.py
└── requirements.txt

main.py contiene la implementación de la API y requirements.txt
contiene sus dependencias.

Recurso Producto

Campo       Tipo      Validación

id          Entero    Identificador único
nombre      Texto     Mínimo 2 caracteres
categoria   Texto     Mínimo 2 caracteres
precio      Decimal   Mayor que 0
stock       Entero    Mayor o igual que 0

Los productos se almacenan temporalmente en una lista de diccionarios en
memoria. No se utiliza una base de datos en esta versión.

Endpoints

Método   Endpoint                     Función

GET      /productos                 Obtener todos los productos
POST     /productos                 Registrar un producto
GET      /productos/{producto_id}   Obtener un producto por ID
PUT      /productos/{producto_id}   Actualizar un producto
DELETE   /productos/{producto_id}   Eliminar un producto
GET      /metricas                  Consultar métricas
GET      /                          Verificar que la API funciona

Validaciones

nombre: mínimo 2 caracteres.

categoria: mínimo 2 caracteres.

precio: mayor que 0.

stock: mayor o igual que 0.

Los productos inexistentes generan HTTP 404.

Los datos inválidos generan HTTP 422.

Los nuevos IDs se generan tomando como referencia el ID más alto
existente para evitar duplicados.

Observabilidad

La API utiliza el módulo logging de Python para registrar:

Fecha y hora.

Tipo de evento.

Peticiones recibidas.

Inicio de operaciones.

Operaciones exitosas.

Errores.

Finalización de operaciones.

Tiempo de respuesta.

El endpoint GET /metricas muestra:

Total de peticiones.

Peticiones exitosas.

Peticiones con error.

Tiempo promedio de respuesta.

Productos registrados.

Cantidad de peticiones GET, POST, PUT y DELETE.

Instalación

Crear el entorno virtual:

python -m venv .venv

Activarlo en Windows PowerShell:

.venv\Scripts\Activate.ps1

Instalar las dependencias:

pip install -r requirements.txt

Ejecución

Iniciar la API con:

uvicorn main:app --reload

La API estará disponible en:

http://127.0.0.1:8000

Swagger UI

La documentación interactiva de FastAPI está disponible en:

http://127.0.0.1:8000/docs

Desde Swagger UI se realizaron las pruebas de consulta, creación,
actualización, eliminación y validación de errores.

Códigos HTTP

200 OK: operación realizada correctamente.

404 Not Found: producto no encontrado.

422 Unprocessable Entity: datos que no cumplen las validaciones.

Evidencias

Las evidencias del proyecto incluyen capturas de:

GET /productos exitoso.

POST /productos exitoso.

GET /productos/{id} exitoso.

PUT /productos/{id} exitoso.

DELETE /productos/{id} exitoso.

Producto inexistente con respuesta 404.

Datos inválidos con respuesta 422.

GET /metricas.

Logs de la aplicación.

Uso de Inteligencia Artificial

La Inteligencia Artificial fue utilizada como herramienta de apoyo y
orientación durante el desarrollo. Se utilizó para comprender la
estructura del código, resolver dudas, proponer mejoras y explicar
errores.

Las sugerencias fueron revisadas y adaptadas al proyecto. También se
realizaron pruebas en Swagger para comprobar el funcionamiento de los
endpoints, las validaciones, los errores, los logs y las métricas.

La IA no sustituyó las pruebas ni las decisiones realizadas durante el
desarrollo.

Conclusión

El proyecto permitió desarrollar una API REST funcional utilizando
Python y FastAPI. Se aplicaron métodos HTTP, estructuras de datos,
validaciones, manejo de errores, documentación automática y
observabilidad básica. Las pruebas realizadas permitieron comprobar el
funcionamiento de las operaciones principales y sus diferentes
escenarios.
