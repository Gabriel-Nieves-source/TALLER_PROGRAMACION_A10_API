API de Gestión de Productos

API REST desarrollada con FastAPI para la administración de productos, implementada como parte del taller de Programación (Guía 4 – Observabilidad y DevOps inteligente con IA). 
Incluye operaciones CRUD completas, validaciones con Pydantic, y un sistema de observabilidad basado en logs y métricas.

Tecnologías utilizadas
Python 3.13
FastAPI – framework para la construcción de la API.
Uvicorn – servidor ASGI que ejecuta la aplicación.
Pydantic – validación de datos y definición de esquemas.
Swagger UI / OpenAPI – documentación interactiva generada automáticamente por FastAPI.
logging (Python) – registro de eventos, errores y operaciones.
Estructura del proyecto
.
├── main.py              # Código principal de la API
├── requirements.txt     # Dependencias del proyecto
├── app.log              # Archivo de logs generado en tiempo de ejecución
└── README.md
Funcionalidades principales
Método	Endpoint	Descripción
GET	/	Verifica que la API esté funcionando
GET	/productos	Consulta todos los productos
GET	/productos/{id}	Consulta un producto por ID
POST	/productos	Registra un nuevo producto
PUT	/productos/{id}	Actualiza un producto existente
DELETE	/productos/{id}	Elimina un producto
GET	/metricas	Consulta las métricas de la API
Modelo de datos: Producto
Campo	Tipo	Validación
nombre	string	mínimo 2 caracteres
categoria	string	mínimo 2 caracteres
precio	float	mayor que 0
stock	int	mayor o igual a 0
Observabilidad

La API implementa un middleware que registra automáticamente el inicio, fin, éxito y error de cada petición HTTP, junto con el tiempo de respuesta. 
Los eventos se guardan tanto en consola como en el archivo app.log, con el siguiente formato:

2026-09-13 10:15:32 | INFO | INICIO PETICIÓN | GET /productos | Petición recibida
2026-09-13 10:15:32 | INFO | ÉXITO PETICIÓN | GET /productos | Operación exitosa | HTTP 200

El endpoint /metricas expone en tiempo real:

Total de peticiones recibidas
Peticiones exitosas y fallidas
Tiempo promedio de respuesta
Número de productos registrados   
Peticiones por método HTTP (GET, POST, PUT, DELETE)
Instalación y ejecución
Clonar el repositorio:
bash
   git clone https://github.com/Gabriel-Nieves-source/TALLER_PROGRAMACION_A10.git
   cd TALLER_PROGRAMACION_A10
Crear y activar el entorno virtual:
bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1      # Windows (PowerShell)
   source .venv/bin/activate       # Linux / macOS
Instalar las dependencias:
bash
   pip install -r requirements.txt
Ejecutar la API:
bash
   uvicorn main:app --reload
Acceder a la documentación interactiva (Swagger UI):
   http://127.0.0.1:8000/docs 

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
