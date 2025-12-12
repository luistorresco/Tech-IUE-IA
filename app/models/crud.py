from sqlalchemy.orm import Session
from app.models import sql_models as models
from app.views import schemas
import json

def get_soil_type_by_name(db: Session, name: str):
    return db.query(models.SoilType).filter(models.SoilType.name == name).first()

def get_crop_recommendations_by_soil(db: Session, soil_id: int):
    return db.query(models.CropRecommendation).filter(models.CropRecommendation.soil_type_id == soil_id).all()

def get_all_crop_infos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CropInfo).offset(skip).limit(limit).all()

def create_soil_type(db: Session, name: str, description: str):
    db_soil = models.SoilType(name=name, description=description)
    db.add(db_soil)
    db.commit()
    db.refresh(db_soil)
    return db_soil

def create_crop_recommendation(db: Session, rec: schemas.CropRecommendationBase, soil_id: int):
    # Map schema fields to model fields
    db_rec = models.CropRecommendation(
        soil_type_id=soil_id,
        crop_name=rec.crop_name,
        suitability_score=rec.suitability_score,
        expected_yield=rec.expected_yield,
        growing_season=rec.growing_season,
        water_requirements=rec.water_requirements,
        notes=rec.notes,
        image_url=rec.image_url
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec

def create_crop_info(db: Session, crop: schemas.CropData):
    soil_json = json.dumps(crop.soil_types)
    db_crop = models.CropInfo(
        crop_name=crop.crop_name,
        min_altitude=crop.min_altitude,
        max_altitude=crop.max_altitude,
        soil_types_json=soil_json,
        water_needs=crop.water_needs,
        growing_season=crop.growing_season,
        expected_yield=crop.expected_yield,
        image_url=crop.image_url
    )
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop

def count_crop_infos(db: Session):
    return db.query(models.CropInfo).count()

def get_crop_info_by_name(db: Session, name: str):
    return db.query(models.CropInfo).filter(models.CropInfo.crop_name == name).first()
