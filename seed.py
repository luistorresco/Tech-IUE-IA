
from app.config.database import SessionLocal, engine
from app.models import crud, sql_models as models
from app.views import schemas
import json

# ============================================================
#  IMÁGENES PERSONALIZADAS
# ============================================================
CUSTOM_IMAGES = {
    "Arroz": "https://saludsabor.com/wp-content/uploads/2025/12/arroz.png",
    "Maíz": "https://saludsabor.com/wp-content/uploads/2025/12/maiz.jpg",
    "Algodón": "https://saludsabor.com/wp-content/uploads/2025/12/algodon.jpg",
    "Trigo": "https://saludsabor.com/wp-content/uploads/2025/12/trigo.jpg",
    "Maní": "https://saludsabor.com/wp-content/uploads/2025/12/mani.jpeg",
    "Café": "https://saludsabor.com/wp-content/uploads/2025/12/cafe.jpg",
    "Papa": "https://saludsabor.com/wp-content/uploads/2025/12/papa.jpg",
    "Caña de azúcar": "https://saludsabor.com/wp-content/uploads/2025/12/azucar.jpeg",
    "Yuca": "https://saludsabor.com/wp-content/uploads/2025/12/yuca.jpg",
    "Plátano": "https://saludsabor.com/wp-content/uploads/2025/12/platano.jpg",
    "Dividivi": "https://saludsabor.com/wp-content/uploads/2025/12/dividivi.jpg",
    "Cacao": "https://saludsabor.com/wp-content/uploads/2025/12/cacao.jpg"
}

def seed_data():
    print("Creating tables if they don't exist...")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    # ============================================================
    # 1. TIPOS DE SUELO Y RECOMENDACIONES — COLOMBIA
    # ============================================================
    soil_data = {
        "Suelo_Aluvial": [
            {
                "name": "Arroz",
                "score": 0.95,
                "yield": "5200 kg/ha",
                "season": "Época de lluvias (Siembra de Primera)",
                "water": "Alta",
                "notes": (
                    "El arroz es uno de los principales cultivos de Colombia, especialmente en los Llanos Orientales "
                    "y zonas cálidas del Tolima, Huila y Meta. Requiere abundante disponibilidad de agua y suelos que "
                    "permitan un adecuado control del encharcamiento. El manejo adecuado del riego y la lámina de agua "
                    "es fundamental para maximizar los rendimientos."
                )
            },
            {
                "name": "Trigo",
                "score": 0.80,
                "yield": "3000 kg/ha",
                "season": "Época de lluvias",
                "water": "Moderada",
                "notes": (
                    "Aunque su cultivo no es tan extendido en Colombia, el trigo se desarrolla mejor en suelos profundos "
                    "y bien drenados de regiones frías como Boyacá y Nariño. Requiere temperaturas frescas y baja humedad "
                    "excesiva para lograr una buena formación del grano."
                )
            }
        ],

        "Suelo_Negro": [
            {
                "name": "Algodón",
                "score": 0.90,
                "yield": "2000 kg/ha",
                "season": "Época seca",
                "water": "Moderada",
                "notes": (
                    "El algodón fue un cultivo industrial clave en varias zonas del Caribe colombiano como Córdoba y "
                    "Sucre. Los suelos negros permiten una buena retención de humedad y favorecen el crecimiento de "
                    "raíces profundas esenciales para este cultivo."
                )
            },
            {
                "name": "Yuca",
                "score": 0.93,
                "yield": "2500 kg/ha",
                "season": "Todo el año",
                "water": "Baja",
                "notes": (
                    "La yuca es un cultivo fundamental en Colombia, tolerante a sequía y adaptable a suelos negros y pesados. "
                    "Es clave en la dieta de zonas rurales y en la industria de almidones."
                )
            }
        ],

        "Suelo_Rojo": [
            {
                "name": "Maní",
                "score": 0.82,
                "yield": "2000 kg/ha",
                "season": "Siembra de Mitaca",
                "water": "Baja",
                "notes": (
                    "El maní requiere suelos sueltos, de buen drenaje y zonas cálidas como el Caribe. Es sensible "
                    "al exceso de humedad, especialmente durante la etapa de floración y formación de vainas."
                )
            },
            {
                "name": "Plátano",
                "score": 0.90,
                "yield": "18000 kg/ha",
                "season": "Todo el año",
                "water": "Alta",
                "notes": (
                    "El plátano es uno de los cultivos más importantes de Colombia, especialmente en Antioquia, Chocó y el Eje Cafetero. "
                    "Los suelos rojos y húmedos favorecen su desarrollo continuo durante todo el año."
                )
            }
        ],

        "Suelo_Arido": [
            {
                "name": "Dividivi",
                "score": 0.91,
                "yield": "1500 kg/ha",
                "season": "Todo el año",
                "water": "Muy baja",
                "notes": (
                    "El dividivi es nativo de La Guajira y extremadamente resistente a la sequía. "
                    "Se utiliza en curtientes, tintes naturales y reforestación en zonas áridas."
                )
            }
        ],

        "Suelo_Lateritico": [
            {
                "name": "Café",
                "score": 0.97,
                "yield": "1000 kg/ha",
                "season": "Todo el año",
                "water": "Alta",
                "notes": (
                    "Colombia es líder mundial en café. Los suelos lateríticos y montañosos con altitudes entre 1200 y 2000 msnm, "
                    "lluvias frecuentes y sombra parcial crean las condiciones ideales para su producción."
                )
            },
            {
                "name": "Cacao",
                "score": 0.94,
                "yield": "900 kg/ha",
                "season": "Todo el año",
                "water": "Alta",
                "notes": (
                    "Colombia produce cacao de excelente calidad. Se desarrolla muy bien en suelos lateríticos con alta humedad, "
                    "especialmente en Santander, Arauca y Antioquia."
                )
            }
        ],

        "Suelo_Montanoso": [
            {
                "name": "Papa",
                "score": 0.95,
                "yield": "3000 kg/ha",
                "season": "Época de lluvias",
                "water": "Moderada",
                "notes": (
                    "La papa es fundamental en la economía de zonas frías como Cundinamarca, Boyacá y Nariño. "
                    "Se adapta muy bien a suelos volcánicos y montañosos bien drenados."
                )
            }
        ],

        "Suelo_Amarillo": [
            {
                "name": "Maíz",
                "score": 0.90,
                "yield": "3800 kg/ha",
                "season": "Época seca",
                "water": "Moderada",
                "notes": (
                    "El maíz es uno de los cultivos más sembrados en Colombia. Prefiere suelos amarillos, franco-limosos "
                    "y con buena fertilización nitrogenada. Se adapta a la mayoría de climas."
                )
            }
        ]
    }


    # ============================================================
    # ISO 1. SOIL TYPES & IMAGES
    # ============================================================
    SOIL_IMAGES = {
        "Suelo_Aluvial": "https://saludsabor.com/wp-content/uploads/2025/12/aluvial.jpg",
        "Suelo_Negro": "https://saludsabor.com/wp-content/uploads/2025/12/negro.jpg",
        "Suelo_Rojo": "https://saludsabor.com/wp-content/uploads/2025/12/rojo.jpg",
        "Suelo_Arido": "https://saludsabor.com/wp-content/uploads/2025/12/arido.jpg",
        "Suelo_Lateritico": "https://saludsabor.com/wp-content/uploads/2025/12/lateritico.jpg",
        "Suelo_Montanoso": "https://saludsabor.com/wp-content/uploads/2025/12/montanoso.jpg",
        "Suelo_Amarillo": "https://saludsabor.com/wp-content/uploads/2025/12/amarillo.jpg"
    }

    print("Seeding Soil Types and Recommendations...")

    for soil_name, crops in soil_data.items():
        db_soil = crud.get_soil_type_by_name(db, soil_name)
        if not db_soil:
            db_soil = crud.create_soil_type(db, soil_name, f"Tipo de suelo colombiano: {soil_name}")

        for c in crops:
            exists = any(r.crop_name == c["name"] for r in db_soil.recommendations)

            if not exists:
                img = CUSTOM_IMAGES.get(c["name"], f"https://source.unsplash.com/featured/?{c['name']}")

                rec_in = schemas.CropRecommendationBase(
                    crop_name=c["name"],
                    suitability_score=c["score"],
                    expected_yield=c["yield"],
                    growing_season=c["season"],
                    water_requirements=c["water"],
                    notes=c["notes"],
                    image_url=img
                )

                crud.create_crop_recommendation(db, rec_in, db_soil.id)

    # ============================================================
    # 2. CROP CATALOG (HOME SCREEN) — COLOMBIA
    # ============================================================

    print("Seeding Crop Catalog...")

    catalog_crops = [
        {"name": "Arroz", "min_alt": 0, "max_alt": 1200, "soils": ["Suelo_Aluvial"], "water": "Alta", "season": "Época de lluvias", "yield": "4500 kg/ha"},
        {"name": "Maíz", "min_alt": 0, "max_alt": 1800, "soils": ["Suelo_Amarillo", "Suelo_Franco"], "water": "Moderada", "season": "Época seca", "yield": "3800 kg/ha"},
        {"name": "Papa", "min_alt": 600, "max_alt": 3500, "soils": ["Suelo_Montanoso"], "water": "Moderada", "season": "Época de lluvias", "yield": "3000 kg/ha"},
        {"name": "Café", "min_alt": 800, "max_alt": 2100, "soils": ["Suelo_Lateritico"], "water": "Alta", "season": "Todo el año", "yield": "1000 kg/ha"},
        {"name": "Trigo", "min_alt": 200, "max_alt": 1600, "soils": ["Suelo_Aluvial"], "water": "Moderada", "season": "Época de lluvias", "yield": "3000 kg/ha"},
        {"name": "Algodón", "min_alt": 0, "max_alt": 800, "soils": ["Suelo_Negro"], "water": "Moderada", "season": "Época seca", "yield": "2000 kg/ha"},
        {"name": "Maní", "min_alt": 0, "max_alt": 1000, "soils": ["Suelo_Rojo"], "water": "Baja", "season": "Siembra de Mitaca", "yield": "2000 kg/ha"},
        {"name": "Caña de azúcar", "min_alt": 0, "max_alt": 1500, "soils": ["Suelo_Aluvial"], "water": "Alta", "season": "Todo el año", "yield": "6000 kg/ha"},
        {"name": "Yuca", "min_alt": 0, "max_alt": 1000, "soils": ["Suelo_Negro"], "water": "Baja", "season": "Todo el año", "yield": "2500 kg/ha"},
        {"name": "Plátano", "min_alt": 0, "max_alt": 1200, "soils": ["Suelo_Rojo"], "water": "Alta", "season": "Todo el año", "yield": "18000 kg/ha"},
        {"name": "Dividivi", "min_alt": 0, "max_alt": 500, "soils": ["Suelo_Arido"], "water": "Muy baja", "season": "Todo el año", "yield": "1500 kg/ha"},
        {"name": "Cacao", "min_alt": 200, "max_alt": 800, "soils": ["Suelo_Lateritico"], "water": "Alta", "season": "Todo el año", "yield": "900 kg/ha"}
    ]

    for c in catalog_crops:
        try:
            img = CUSTOM_IMAGES.get(c["name"], f"https://source.unsplash.com/featured/?{c['name']}")

            crop_in = schemas.CropData(
                id=0,
                crop_name=c["name"],
                min_altitude=c["min_alt"],
                max_altitude=c["max_alt"],
                soil_types=c["soils"],
                water_needs=c["water"],
                growing_season=c["season"],
                expected_yield=c["yield"],
                image_url=img
            )

            crud.create_crop_info(db, crop_in)

        except Exception:
            db.rollback()

    db.close()
    print("Seeding Complete.")


if __name__ == "__main__":
    seed_data()