from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import crud, ml_engine
from app.views import schemas
from datetime import datetime

router = APIRouter()

# Initialize ML Engine
classifier = ml_engine.SoilClassifier()

@router.post("/analyze", response_model=schemas.AnalysisResponse)
async def analyze_soil(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not classifier.model:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model using train.py")
    
    # Read image
    contents = await image.read()
    
    # Predict
    try:
        predicted_english_class, confidence = classifier.predict(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Map English class to Spanish DB name
    ENGLISH_TO_SPANISH_SOIL_MAP = {
        "Alluvial_Soil": "Suelo_Aluvial",
        "Arid_Soil": "Suelo_Arido",
        "Black_Soil": "Suelo_Negro",
        "Laterite_Soil": "Suelo_Lateritico", 
        "Mountain_Soil": "Suelo_Montanoso", 
        "Red_Soil": "Suelo_Rojo",
        "Yellow_Soil": "Suelo_Amarillo"
    }
    
    soil_name = ENGLISH_TO_SPANISH_SOIL_MAP.get(predicted_english_class, predicted_english_class)

    # Get details from DB
    soil_type = crud.get_soil_type_by_name(db, soil_name)
    
    recommendations_list = []
    if soil_type:
        recs = crud.get_crop_recommendations_by_soil(db, soil_type.id)
        for r in recs:
            recommendations_list.append(schemas.CropRecommendation(
                crop_id=r.id,
                crop_name=r.crop_name,
                suitability_score=r.suitability_score if r.suitability_score is not None else 0.0,
                expected_yield=r.expected_yield or "N/A",
                growing_season=r.growing_season or "N/A",
                water_requirements=r.water_requirements or "N/A",
                notes=r.notes or "",
                image_url=r.image_url
            ))
    
    # General recommendations (hardcoded for now or fetch from DB)
    gen_recs = ["Asegurar un buen drenaje.", "Realizar análisis de pH del suelo anualmente."]

    return {
        "soil_type": soil_name,
        "soil_confidence": float(confidence),
        "altitude": 0.0, # Mocked/Removed
        "temperature": 25.0, # Mocked
        "climate_zone": "Tropical", # Mocked
        "recommended_crops": recommendations_list,
        "general_recommendations": gen_recs,
        "timestamp": datetime.now().isoformat()
    }
