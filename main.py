# Importaciones
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import logging
import time

#configuracion de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("api_productos")


# creacion de la API

app = FastAPI(
    title="API de Productos",
    description="API REST para gestionar productos",
    version="1.0.0"
)



# Modelo de datos y validaciones 

class Producto(BaseModel):
    nombre: str = Field(
        min_length=2,
        description="Nombre del producto"
    )

    categoria: str = Field(
        min_length=2,
        description="Categoría del producto"
    )

    precio: float = Field(
        gt=0,
        description="Precio mayor que 0"
    )

    stock: int = Field(
        ge=0,
        description="Stock mayor o igual a 0"
    )



# Estructura de datos


productos = [
    {
        "id": 1,
        "nombre": "Teclado",
        "categoria": "Perifericos",
        "precio": 80000,
        "stock": 10
    },
    {
        "id": 2,
        "nombre": "Mouse",
        "categoria": "Perifericos",
        "precio": 45000,
        "stock": 20
    }
]



# Metricas 


total_peticiones = 0
peticiones_exitosas = 0
peticiones_error = 0
tiempo_total_respuesta = 0

peticiones_get = 0
peticiones_post = 0
peticiones_put = 0
peticiones_delete = 0


# Middleware de observabilidad 

@app.middleware("http")
async def registrar_peticiones(request: Request, call_next):

    global total_peticiones
    global peticiones_exitosas
    global peticiones_error
    global tiempo_total_respuesta

    global peticiones_get
    global peticiones_post
    global peticiones_put
    global peticiones_delete

    inicio = time.perf_counter()

    total_peticiones += 1

    metodo = request.method
    ruta = request.url.path

    # Contar peticiones según el método HTTP
    if metodo == "GET":
        peticiones_get += 1
    elif metodo == "POST":
        peticiones_post += 1
    elif metodo == "PUT":
        peticiones_put += 1
    elif metodo == "DELETE":
        peticiones_delete += 1

    logger.info(
        f"INICIO PETICIÓN | {metodo} {ruta} | Petición recibida"
    )

    try:
        response = await call_next(request)

        if response.status_code < 400:
            peticiones_exitosas += 1

            logger.info(
                f"ÉXITO PETICIÓN | {metodo} {ruta} | "
                f"Operación exitosa | HTTP {response.status_code}"
            )

        else:
            peticiones_error += 1

            logger.error(
                f"ERROR HTTP | {metodo} {ruta} | "
                f"HTTP {response.status_code}"
            )

        return response

    except Exception as error:

        peticiones_error += 1

        logger.error(
            f"ERROR INTERNO | {metodo} {ruta} | {error}"
        )

        raise

    finally:

        fin = time.perf_counter()

        duracion = fin - inicio

        tiempo_total_respuesta += duracion

        logger.info(
            f"FIN PETICIÓN | {metodo} {ruta} | "
            f"Operación finalizada | "
            f"Tiempo: {duracion:.4f} segundos"
        )



# ENDPOINT inicial


@app.get("/")
def inicio():

    logger.info("INICIO | GET / | Inicio de la API")

    try:

        resultado = {
            "mensaje": "Mi API funciona"
        }

        logger.info(
            "ÉXITO | GET / | API funcionando correctamente"
        )

        return resultado

    except Exception as error:

        logger.error(
            f"ERROR | GET / | {error}"
        )

        raise

    finally:

        logger.info(
            "FIN | GET / | Operación finalizada"
        )



# GET - (obtener los productos)


@app.get("/productos")
def obtener_productos():

    logger.info(
        "INICIO | GET /productos | Consulta de productos"
    )

    try:

        logger.info(
            f"ÉXITO | GET /productos | "
            f"Consulta exitosa | Productos encontrados: {len(productos)}"
        )

        return productos

    except Exception as error:

        logger.error(
            f"ERROR | GET /productos | {error}"
        )

        raise

    finally:

        logger.info(
            "FIN | GET /productos | Operación finalizada"
        )



# POST - (crear un producto)

@app.post("/productos")
def crear_producto(producto: Producto):

    logger.info(
        "INICIO | POST /productos | Registro de producto"
    )

    try:

        # Generar un ID único
        if productos:
            nuevo_id = max(p["id"] for p in productos) + 1
        else:
            nuevo_id = 1

        # Crear producto
        nuevo_producto = {
            "id": nuevo_id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio": producto.precio,
            "stock": producto.stock
        }

        # Agregar producto a la lista
        productos.append(nuevo_producto)

        logger.info(
            f"ÉXITO | POST /productos | "
            f"Producto registrado | ID: {nuevo_id}"
        )

        return nuevo_producto

    except Exception as error:

        logger.error(
            f"ERROR | POST /productos | {error}"
        )

        raise

    finally:

        logger.info(
            "FIN | POST /productos | Operación finalizada"
        )


# GET - (obqtener un producto por ID)

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):

    logger.info(
        f"INICIO | GET /productos/{producto_id} | "
        f"Consulta de producto"
    )

    try:

        for producto in productos:

            if producto["id"] == producto_id:

                logger.info(
                    f"ÉXITO | GET /productos/{producto_id} | "
                    f"Producto encontrado"
                )

                return producto

        logger.error(
            f"ERROR | GET /productos/{producto_id} | "
            f"Producto no encontrado"
        )

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    except HTTPException:
        raise

    except Exception as error:

        logger.error(
            f"ERROR | GET /productos/{producto_id} | {error}"
        )

        raise

    finally:

        logger.info(
            f"FIN | GET /productos/{producto_id} | "
            f"Operación finalizada"
        )



# PUT - (actualizar un producto por ID)

@app.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: int,
    producto_actualizado: Producto
):

    logger.info(
        f"INICIO | PUT /productos/{producto_id} | "
        f"Actualización de producto"
    )

    try:

        for producto in productos:

            if producto["id"] == producto_id:

                producto["nombre"] = producto_actualizado.nombre
                producto["categoria"] = producto_actualizado.categoria
                producto["precio"] = producto_actualizado.precio
                producto["stock"] = producto_actualizado.stock

                logger.info(
                    f"ÉXITO | PUT /productos/{producto_id} | "
                    f"Producto actualizado"
                )

                return producto

        logger.error(
            f"ERROR | PUT /productos/{producto_id} | "
            f"Producto no encontrado"
        )

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    except HTTPException:
        raise

    except Exception as error:

        logger.error(
            f"ERROR | PUT /productos/{producto_id} | {error}"
        )

        raise

    finally:

        logger.info(
            f"FIN | PUT /productos/{producto_id} | "
            f"Operación finalizada"
        )


# ============================================================
# DELETE - (eliminar un producto por ID)
# ============================================================

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):

    logger.info(
        f"INICIO | DELETE /productos/{producto_id} | "
        f"Eliminación de producto"
    )

    try:

        for producto in productos:

            if producto["id"] == producto_id:

                productos.remove(producto)

                logger.info(
                    f"ÉXITO | DELETE /productos/{producto_id} | "
                    f"Producto eliminado"
                )

                return {
                    "mensaje": "Producto eliminado correctamente"
                }

        logger.error(
            f"ERROR | DELETE /productos/{producto_id} | "
            f"Producto no encontrado"
        )

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    except HTTPException:
        raise

    except Exception as error:

        logger.error(
            f"ERROR | DELETE /productos/{producto_id} | {error}"
        )

        raise

    finally:

        logger.info(
            f"FIN | DELETE /productos/{producto_id} | "
            f"Operación finalizada"
        )


# GET - (metricas de la API)


@app.get("/metricas")
def obtener_metricas():

    logger.info(
        "INICIO | GET /metricas | Consulta de métricas"
    )

    try:

        if total_peticiones > 0:
            tiempo_promedio = (
                tiempo_total_respuesta / total_peticiones
            )
        else:
            tiempo_promedio = 0

        resultado = {
            "total_peticiones": total_peticiones,
            "peticiones_exitosas": peticiones_exitosas,
            "peticiones_error": peticiones_error,
            "tiempo_promedio_respuesta_segundos": round(
                tiempo_promedio,
                4
            ),
            "productos_registrados": len(productos),
            "peticiones_get": peticiones_get,
            "peticiones_post": peticiones_post,
            "peticiones_put": peticiones_put,
            "peticiones_delete": peticiones_delete
        }

        logger.info(
            "ÉXITO | GET /metricas | "
            "Métricas consultadas correctamente"
        )

        return resultado

    except Exception as error:

        logger.error(
            f"ERROR | GET /metricas | {error}"
        )

        raise

    finally:

        logger.info(
            "FIN | GET /metricas | Operación finalizada"
        )