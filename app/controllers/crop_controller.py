from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import crud
from app.views import schemas
import json

router = APIRouter()

@router.get("/crops", response_model=schemas.CropsListResponse) 
def list_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
     crops = crud.get_all_crop_infos(db, skip, limit)
     
     mapped_crops = []
     for c in crops:
         mapped_crops.append(schemas.CropData(
             id=c.id,
             crop_name=c.crop_name,
             min_altitude=c.min_altitude,
             max_altitude=c.max_altitude,
             soil_types=json.loads(c.soil_types_json),
             water_needs=c.water_needs or "N/A",
             growing_season=c.growing_season or "N/A",
             expected_yield=c.expected_yield or "N/A",
             image_url=c.image_url
         ))
         
     return {
         "total": len(mapped_crops), # Should ideally be count from DB
         "crops": mapped_crops
     }

@router.get("/crops/details/{crop_name}", response_model=schemas.CropData)
def get_crop_details(crop_name: str, db: Session = Depends(get_db)):
    crop = crud.get_crop_info_by_name(db, crop_name)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    return schemas.CropData(
        id=crop.id,
        crop_name=crop.crop_name,
        min_altitude=crop.min_altitude,
        max_altitude=crop.max_altitude,
        soil_types=json.loads(crop.soil_types_json),
        water_needs=crop.water_needs or "N/A",
        growing_season=crop.growing_season or "N/A",
        expected_yield=crop.expected_yield or "N/A",
        image_url=crop.image_url
    )
