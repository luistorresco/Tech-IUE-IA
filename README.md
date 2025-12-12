# TerraWish — Backend

Descripción
-----------
Sistema backend de la aplicación TerraWish: API para clasificación de suelos
y recomendación de cultivos a partir de imágenes. Proyecto construido con
FastAPI, SQLAlchemy y un motor de ML que genera un modelo en `model_data/`.

Estructura del proyecto
-----------------------
back/
├── app/
│   ├── config/         # Configuración y conexión a la base de datos
│   │   └── database.py  # Conexión PostgreSQL
│   ├── controllers/    # Endpoints / controladores
│   ├── models/         # Lógica de negocio y ML
│   ├── views/          # Esquemas Pydantic (DTOs / respuestas)
│   └── main.py         # Punto de entrada de la API
├── model_data/         # Modelos y clases generadas por `train.py`
├── seed.py             # Script para crear tablas y datos iniciales
├── train.py            # Script de entrenamiento del modelo
├── requirements.txt    # Dependencias Python
└── Dockerfile / docker-compose.yml

Requisitos
----------
- Python 3.10+ (recomendado)
- PostgreSQL (base de datos)
- `pip` para instalar dependencias

Instalación rápida
------------------
1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Copiar el archivo de entorno y configurar la BD:

```bash
cp .env.example .env
# Edita `.env` y ajusta `DATABASE_URL` con tus credenciales
```

Base de datos (inicialización)
------------------------------
- Asegúrate de tener PostgreSQL instalado y en ejecución.
- Crea una base de datos (por ejemplo `terrawish`).
- Ejecuta el script de seed para crear tablas y datos iniciales:

```bash
python seed.py
```

Entrenar el modelo de ML
------------------------
Antes de usar la ruta de predicción debes entrenar el modelo con tu dataset.

```bash
python train.py
```

Al finalizar, el modelo se guardará en `model_data/best_model.h5` y las clases
en `model_data/classes.txt`.

Ejecutar la API
--------------
Usa Uvicorn para arrancar la aplicación en modo desarrollo:

```bash
uvicorn app.main:app --reload
```

Endpoints principales
--------------------
- `POST /predict/` — Subir una imagen para clasificar el tipo de suelo y
  recibir recomendaciones de cultivo.
- `GET /docs` — Documentación interactiva (Swagger UI).

Uso con Docker
--------------
1. Construir y levantar contenedores:

```bash
docker-compose up --build
```

2. (Dentro de otro terminal) Inicializar datos y entrenar el modelo en el
   contenedor (si lo prefieres dentro del contenedor):

```bash
# Ejecutar seed
docker-compose exec backend python seed.py

# Entrenar el modelo (puede tardar)
docker-compose exec backend python train.py
```

Notas y consejos
----------------
- Si ya tienes un modelo entrenado copia `model_data/best_model.h5` y
  `model_data/classes.txt` al directorio `model_data/` antes de arrancar la API.
- Revisa `app/config/database.py` para confirmar la cadena de conexión.
- Para entornos de producción desactiva `--reload` y usa un servidor ASGI
  (por ejemplo con `gunicorn` + `uvicorn.workers.UvicornWorker`).

Contribuciones
--------------
Si quieres colaborar, abre un issue o un PR. Describe el cambio y añade
tests si aplica.


