from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CropRecommendationBase(BaseModel):
    crop_name: str
    suitability_score: float
    expected_yield: str = "N/A"
    growing_season: str = "N/A"
    water_requirements: str = "N/A"
    notes: str = ""
    image_url: Optional[str] = None

class CropRecommendation(CropRecommendationBase):
    crop_id: int

class CropData(BaseModel):
    id: int
    crop_name: str
    min_altitude: int = 0
    max_altitude: int = 5000
    soil_types: List[str] = []
    water_needs: str = "N/A"
    growing_season: str = "N/A"
    expected_yield: str = "N/A"
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    soil_type: str
    soil_confidence: float
    altitude: float
    temperature: Optional[float] = None
    climate_zone: str = "Unknown"
    recommended_crops: List[CropRecommendation]
    general_recommendations: List[str]
    timestamp: str

class CropsListResponse(BaseModel):
    total: int
    crops: List[CropData]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model_loaded: bool = False
    database_connected: bool = False
    crops_database_entries: int = 0
    version: str = "1.0.0"
