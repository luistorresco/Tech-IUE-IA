# TerraWish Backend

## Configuración
Estructura del proyecto:

back/app/<br>
├── config/                              <br>
│   └── database.py                      <br>
├── models/                              <br>
│   ├── sql_models.py                    <br>
│   ├── crud.py                          <br>
│   └── ml_engine.py                     <br>
├── views/                               <br>
│   └── schemas.py                       <br>
├── controllers/                         <br>
│   ├── system_controller.py             <br>
│   ├── soil_controller.py               <br>
│   └── crop_controller.py               <br>
└── main.py                              <br>



## 1. **Instalar Dependencias**:
   Para instalar las dependencias necesarias, ejecuta:
   ```bash
   pip install -r requirements.txt
2. Configuración de la Base de Datos:
Asegúrate de tener PostgreSQL instalado y en funcionamiento.

Crea una base de datos (por ejemplo, terrawish).

Copia el archivo .env.example a .env y actualiza el DATABASE_URL con tus credenciales.

bash
Copiar código
cp .env.example .env
# Edita el archivo .env con tus credenciales
Ejecuta el script de seed para crear las tablas y poblar los datos iniciales:

bash
Copiar código
python seed.py
3. Entrenar el Modelo:
Antes de ejecutar la API, debes entrenar el modelo utilizando tu conjunto de datos.

Ejecuta el script de entrenamiento:

bash
Copiar código
python train.py
Esto guardará el modelo entrenado en model_data/best_model.h5 y los nombres de las clases en model_data/classes.txt.

4. Ejecutar la API:
Para iniciar la API, ejecuta el siguiente comando:

bash
Copiar código
uvicorn app.main:app --reload
Endpoints de la API
POST /predict/: Subir una imagen para obtener la clasificación del suelo y recomendaciones de cultivos.

GET /docs: Documentación interactiva de la API (Swagger UI).

Configuración con Docker
1. Construir y Ejecutar el Contenedor:
Para construir y ejecutar el contenedor, usa:

bash
Copiar código
docker-compose up --build
2. Inicializar los Datos (Una vez que el contenedor esté en funcionamiento):
Abre una terminal separada:

bash
Copiar código
# Sembrar la base de datos
docker-compose exec backend python seed.py

# Entrenar el modelo (Requerido para las predicciones)
# Nota: Este proceso puede tardar un poco dentro del contenedor
docker-compose exec backend python train.py
