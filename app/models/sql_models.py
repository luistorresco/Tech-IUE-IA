from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, ARRAY, JSON
from sqlalchemy.orm import relationship
from app.config.database import Base

class SoilType(Base):
    __tablename__ = "soil_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Simplified: One soil can have many crop recommendations specific to it
    recommendations = relationship("CropRecommendation", back_populates="soil_type")

class CropRecommendation(Base):
    """
    Stores specific recommendations for a soil type.
    """
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    soil_type_id = Column(Integer, ForeignKey("soil_types.id"))
    crop_name = Column(String, index=True)
    
    # Details for the recommendation
    suitability_score = Column(Float, default=0.0)
    expected_yield = Column(String, nullable=True)
    growing_season = Column(String, nullable=True)
    water_requirements = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

    soil_type = relationship("SoilType", back_populates="recommendations")

class CropInfo(Base):
    """
    General info about crops for the browsing catalog (Home Screen).
    """
    __tablename__ = "crop_info"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, unique=True, index=True)
    min_altitude = Column(Integer, default=0)
    max_altitude = Column(Integer, default=5000)
    # Storing list of compatible soil types as a JSON string or simple string for now to avoid complexity
    soil_types_json = Column(String, default="[]") 
    water_needs = Column(String, nullable=True)
    growing_season = Column(String, nullable=True)
    expected_yield = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
