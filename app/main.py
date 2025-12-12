from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import sql_models as models
from app.config import database
from app.controllers import system_controller, soil_controller, crop_controller
import time
from sqlalchemy.exc import OperationalError

app = FastAPI(title="TerraWish API", 
    version="5.7.2",
    description="Analisis de tierra Inteligente",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)



# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    retries = 5
    while retries > 0:
        try:
            models.Base.metadata.create_all(bind=database.engine)
            print("Database connected and tables created.")
            break
        except OperationalError:
            retries -= 1
            print(f"Database not ready yet. Retrying in 2 seconds... ({retries} retries left)")
            time.sleep(2)
    else:
        print("Could not connect to database.")

# Include Controllers
app.include_router(system_controller.router)
app.include_router(soil_controller.router)
app.include_router(crop_controller.router)
