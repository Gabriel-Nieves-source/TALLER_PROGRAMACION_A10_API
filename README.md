# SITRAL API — Sistema de Trazabilidad y Control por Lotes para Droguerías

Backend REST en **Python 3.12 + FastAPI + SQLAlchemy 2.0 + MySQL 8** que soporta la aplicación móvil
multiplataforma (Android / iOS) de SITRAL. Guía de Laboratorio 5 (UD5, Sesiones 9 y 10) — Taller de Programación,
Universidad Manuela Beltrán.

**Integrantes:** Cristian Camilo Girata Ravelo · Gabriel Leonardo Nieves Bello · Zharick Yojana Puentes Rodríguez
**Tutor:** Juan José Osorio Tabares

---

## 1. Ejecución local

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   ·   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # ajuste DATABASE_URL y JWT_SECRET_KEY
docker compose up -d                 # (opcional) MySQL 8 local
python -m scripts.crear_admin --usuario admin --nombre Ana --apellido Rojas
uvicorn app.main:app --reload
```

* Swagger UI: <http://127.0.0.1:8000/docs> · ReDoc: `/redoc` · OpenAPI 3: `/openapi.json`
* Pruebas: `pytest -v` (usan SQLite en memoria, no requieren MySQL; el pipeline de GitHub Actions las ejecuta).

## 2. Estructura

```
app/
├── main.py              # FastAPI, metadatos OpenAPI (inglés), CORS, tarea diaria de alertas
├── core/                # config (.env), database, security (Argon2id + JWT), deps (roles), errors
├── domain/              # reglas puras sin BD: enums, vencimiento (regla 10 días), escaneo (EAN/GS1/QR)
├── models/              # 10 tablas del esquema relacional Fase 1 (SQLAlchemy 2.0)
├── schemas/             # Pydantic v2 con descripciones y ejemplos en inglés
├── services/            # generación idempotente de alertas, conversión de lotes, datos base
└── routers/             # auth, medicamentos, proveedores, lotes, alertas, ai
tests/                   # 60+ casos: integración (TestClient) + unitarias de dominio
scripts/crear_admin.py   # primer Administrador
```

## 3. Regla de vencimiento (RQF008) — decisión de diseño

La propuesta Fase 1 fijó una **línea base de 30 días** (entrevista, Tabla 1 P4) y el brief del proyecto exige
alertar **como máximo 10 días antes** del vencimiento. SITRAL aplica ambas con dos umbrales:

| Nivel        | Condición                          | Editable                     | Efecto                                   |
|--------------|------------------------------------|------------------------------|------------------------------------------|
| `VENCIDO`    | días < 0                           | —                            | No apto para venta; se sugiere baja       |
| `CRITICA`    | 0 ≤ días ≤ **10**                  | **No** (constante de código) | Alerta inmediata; priorizar venta (FEFO) |
| `PREVENTIVA` | 10 < días ≤ `dias_anticipacion`    | Sí, Administrador (10–180)   | Alerta temprana; línea base 30 días      |
| —            | días > `dias_anticipacion`         | —                            | Lote `VIGENTE`                           |

Un Administrador no puede fijar el umbral por debajo de 10 (respuesta **422**), por lo que la ventana crítica
de 10 días siempre se cumple. Los días se calculan con la fecha de **America/Bogota**, no la del servidor.

## 4. Endpoints (prefijo `/api/v1`)

| Método | Ruta                               | Rol            | Descripción                                        |
|--------|------------------------------------|----------------|----------------------------------------------------|
| POST   | `/auth/login`                      | Público        | Login (OAuth2 password) → JWT                      |
| GET    | `/auth/me`                         | Autenticado    | Perfil del usuario del token                        |
| POST/GET | `/usuarios`                      | Admin          | Crear / listar usuarios                             |
| GET/POST | `/medicamentos`                  | Admin, Farm.   | Listar / crear medicamento                          |
| GET    | `/medicamentos/{id}`               | Admin, Farm.   | Consultar medicamento                               |
| PUT    | `/medicamentos/{id}`               | Admin          | Actualización parcial                               |
| DELETE | `/medicamentos/{id}`               | Admin          | Borrado lógico (INACTIVO)                           |
| *(ídem)* | `/proveedores[/{id}]`            | Admin, Farm.   | CRUD de proveedores (PUT/DELETE solo Admin)         |
| POST   | `/lotes/escanear`                  | Admin, Farm.   | Decodifica EAN/GTIN, GS1 (DataMatrix/QR) o QR SITRAL |
| POST   | `/lotes`                           | Admin, Farm.   | Registra lote + movimiento ENTRADA + alerta si aplica |
| GET    | `/lotes`                           | Admin, Farm.   | Inventario por lote en orden FEFO, filtros          |
| GET    | `/lotes/{id}`                      | Admin, Farm.   | Consultar lote                                      |
| GET    | `/lotes/{id}/validacion`           | Admin, Farm.   | **Validación a 10 días**                            |
| GET    | `/lotes/{id}/trazabilidad`         | Admin, Farm.   | Historial completo del lote (RQF012)                |
| PATCH  | `/lotes/{id}`                      | Admin          | Corrección auditada (movimiento AJUSTE)             |
| DELETE | `/lotes/{id}`                      | Admin          | Baja lógica (movimiento BAJA → KPI de pérdidas)     |
| POST   | `/alertas/generar`                 | Admin, Farm.   | Evaluación idempotente de vencimientos              |
| GET    | `/alertas`                         | Admin, Farm.   | Alertas por urgencia                                |
| PATCH  | `/alertas/{id}/atender`            | Admin, Farm.   | Marcar alerta como ATENDIDA                         |
| GET/PUT | `/alertas/configuracion`          | GET ambos / PUT Admin | Umbral preventivo (10–180)                   |

Códigos HTTP: 200, 201, 400 (regla de negocio), 401 (sin token / token inválido), 403 (rol), 404, 409 (duplicado),
422 (validación). Todos los errores comparten el cuerpo `ErrorResponse`.

## 5. Asistente IA (Gemini + RAG) — `/api/v1/ai`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/ai/consultas` | Pregunta en lenguaje natural; `tecnica`: `zero_shot`, `few_shot` o `cot` |
| POST | `/ai/comparar` | Misma pregunta con las 3 técnicas (3 llamadas) |
| GET | `/ai/contexto` | Muestra los documentos que recupera el RAG (no llama al LLM, costo 0) |

* **RAG básico:** cada lote con existencias se vuelve un documento; BM25 + refuerzo por urgencia recupera los
  `top_k` más relevantes y se insertan como CONTEXTO en el prompt (Retrieve → Augment → Generate).
* **Errores:** 429 (cuota de Gemini o límite propio de 10 consultas/min por usuario, con `Retry-After`),
  503 (sin API key, clave inválida o modelo no disponible), 504 (timeout de 30 s), 502 (respuesta vacía).
  Reintentos automáticos con espera exponencial para 429/5xx/timeout.
* **Bitácora:** cada llamada queda en `logs/llamadas_ia.jsonl` (tokens, latencia, costo, respuesta).
* **Costos:** Gemini 3.8 Flash, USD 0,75 / 1M tokens de entrada y USD 3,75 / 1M de salida (incluye *thinking*)
  hasta el 31-12-2026; el doble desde 2027. Plan gratuito de AI Studio: USD 0 dentro de la cuota.

### Experimento de prompting (≥ 10 llamadas reales)
```bash
python -m scripts.sembrar_datos_demo                 # ~100 medicamentos y ~175 lotes ficticios
uvicorn app.main:app                                 # terminal 1
python -m scripts.experimento_prompting --usuario admin   # terminal 2 (12 llamadas, ~2 min)
```
Genera `resultados/experimento_<fecha>.json` (evidencia) y `.md` (tablas comparativas y proyección de costos
en inglés para 4 usuarios × 20 consultas/día).

## 6. Cambios respecto a la Fase 1

* Credenciales movidas a `.env` (pendiente de la sección 10.12).
* Columna nueva `medicamento.registro_sanitario` (registro INVIMA) para la trazabilidad exigida por la Secretaría de Salud.
* Estado de lote `BAJA` y estado de alerta `ESCALADA`.
* Restricción única (`id_medicamento`, `numero_lote`) e índice por `fecha_vencimiento`.

## 7. Próximas iteraciones

1. Facturación de entrada/salida (RQF006/RQF007) con descuento FEFO y bloqueo de lotes vencidos.
2. Dashboard de KPIs (RQF010).
3. Migración CSV/Excel desde Navasoft (RQF011).
