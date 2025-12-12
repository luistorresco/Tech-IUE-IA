# TerraWish Backend

## Setup
back/app/
├── config/             # Configuración y Conexión a Base de Datos
│   └── database.py     # postgresql
├── models/             # Lógica de Negocio y Datos
│   ├── sql_models.py   # Modelos SQLAlchemy (Tablas BD)
│   ├── crud.py         # Operaciones de Datos (Service Layer)
│   └── ml_engine.py    # Motor de Inteligencia Artificial
├── views/              # Representación de Datos
│   └── schemas.py      # Esquemas Pydantic (DTOs / View Models)
├── controllers/        # Controladores (Endpoints/Rutas)
│   ├── system_controller.py # /health, /
│   ├── soil_controller.py   # /analyze
│   └── crop_controller.py   # /crops, /crops/details
└── main.py             # Punto de entrada y configuración de rutas
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   - Ensure you have PostgreSQL installed and running.
   - Create a database (e.g., `terrawish`).
   - Copy `.env.example` to `.env` and update the `DATABASE_URL` with your credentials.
   ```bash
   cp .env.example .env
   # Edit .env
   ```
   - Run the seed script to create tables and populate initial data:
   ```bash
   python seed.py
   ```

3. **Train the Model**:
   - Before running the API, you must train the model using your dataset.
   - Run the training script:
   ```bash
   python train.py
   ```
   - This will save the model to `model_data/best_model.h5` and class names to `model_data/classes.txt`.

4. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **POST /predict/**: Upload an image to get soil classification and crop recommendations.
- **GET /docs**: Interactive API documentation (Swagger UI).

## Docker Setup

1. **Build and Run**:
   ```bash
   docker-compose up --build
   ```

2. **Initialize Data** (Once container is running):
   - Open a separate terminal:
   ```bash
   # Seed Database
   docker-compose exec backend python seed.py
   
   # Train Model (Required for prediction)
   # Note: This might take time inside the container
   docker-compose exec backend python train.py
   ```
