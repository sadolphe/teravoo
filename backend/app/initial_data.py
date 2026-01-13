import logging
import sys
from sqlalchemy.orm import Session

# Add the directory containing the app module to the python path
sys.path.append(".")

from app.db.session import SessionLocal
from app.db.base import Base  # To ensure models are loaded
from app.db.session import engine
from app.models.producer import ProducerProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producers_data = [
    {
        "name": "Sava Gold Collectors",
        "location_region": "Sava, Madagascar",
        "location_district": "Sambava",
        "bio": "Specialized in organic vanilla since 2010. We work with 450 smallholder farmers in the Sambava region.",
        "badges": ["ORGANIC", "FAIRTRADE", "RAINFOREST"],
        "years_experience": 14,
        "transactions_count": 32,
        "trust_score": 4.9
    },
    {
        "name": "Mananara Bio Cooperative",
        "location_region": "Mananara, Madagascar",
        "location_district": "Mananara",
        "bio": "A cooperative of 120 families producing high-quality clove and vanilla. Focused on sustainable agroforestry.",
        "badges": ["ORGANIC"],
        "years_experience": 8,
        "transactions_count": 15,
        "trust_score": 4.6
    },
    {
        "name": "Vohémar Spice Trad",
        "location_region": "Sava, Madagascar",
        "location_district": "Vohémar",
        "bio": "Premium vanilla preparation and export. We guarantee fully traceable lots from farm to FOB.",
        "badges": ["HACCP"],
        "years_experience": 5,
        "transactions_count": 7,
        "trust_score": 4.2
    }
]

def init_db(db: Session) -> None:
    # ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    for producer_in in producers_data:
        existing = db.query(ProducerProfile).filter(ProducerProfile.name == producer_in["name"]).first()
        if not existing:
            producer = ProducerProfile(**producer_in)
            db.add(producer)
            db.commit()
            db.refresh(producer)
            logger.info(f"Created producer: {producer.name}")
        else:
            logger.info(f"Producer already exists: {existing.name}")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    db.close()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
