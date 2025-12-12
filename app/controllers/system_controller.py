from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import crud
from app.views import schemas
from datetime import datetime

router = APIRouter()

# Global reference to classifier will be needed if we want to check model status
# We can import it from soil_controller or move instantiation to a shared location.
# For now, let's import it from soil_controller (circular dependency risk? No, system imports soil)
# OR move classifier to a singleton in services.
# Let's try importing from soil_controller after defining it, or better:
# Instantiate here for health check? No, double loading.
# Pragmantic: Check if it's loaded by importing the singleton.
# Let's create `app/services/ml_service.py` to hold the singleton?
# app/models/ml_engine.py ALREADY has the class.
# Let's instantiate a GLOBAL singleton in `app/models/ml_engine.py`?
# Or just instantiate in main and pass it? (FastAPI dependency injection preferred but complex for global state).
# We will assume soil_controller has it.

@router.get("/")
def read_root():
    return {"message": "Welcome to TerraWish API"}

@router.get("/health", response_model=schemas.HealthResponse)
def health_check(db: Session = Depends(get_db)):
    db_connected = True
    try:
        db.execute("SELECT 1")
    except:
        db_connected = False
        
    cols_count = crud.count_crop_infos(db) if db_connected else 0
    
    # Check model status - Hacky import or we need a service registry
    # For now, simplistic: 
    model_loaded = False
    try:
        from app.controllers.soil_controller import classifier
        if classifier.model:
            model_loaded = True
    except:
        pass

    return {
        "status": "healthy" if db_connected else "degraded",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model_loaded,
        "database_connected": db_connected,
        "crops_database_entries": cols_count,
        "version": "1.0.0"
    }
