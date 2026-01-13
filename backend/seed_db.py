from app.db.session import SessionLocal, engine
# Import Base to ensure all models are registered if they are imported there
import app.db.base
from app.db.base_class import Base
from app.models.product import Product
from app.models.producer import ProducerProfile
# Ensure TraceabilityEvent is also registered
from app.models.producer import TraceabilityEvent

def init_db():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if empty
    if db.query(Product).count() > 0:
        print("DB already seeded. Clearing old data to update showcase...")
        # Optional: Delete existing products to refresh with new fields
        db.query(Product).delete()
        db.commit()

    products = [
        Product(
            id=101,
            name="Vanille Bourbon Grade A (Noire)",
            price_fob=250.0,
            image_url_raw="https://placehold.co/400x300?text=Raw+Vanilla",
            image_url_ai="https://placehold.co/600x400/1a1a1a/e5e5e5?text=Vanille+Bourbon+Premium",
            status="PUBLISHED",
            description="Une vanille d'exception, cultivée selon les méthodes traditionnelles dans la région de la Sava. Gousses noires, souples et grasses, non fendues. Parfum intense aux notes boisées et cacaotées.",
            origin="Sambava, Région SAVA",
            farmer_name="Coopérative familiale 'Soa Vanilla'",
            harvest_date="Juillet 2024",
            moisture_content=35.0,
            vanillin_content=1.8
        ),
        Product(
            id=102,
            name="Girofle High Grade (CG3)",
            price_fob=120.0,
            image_url_raw="https://placehold.co/400x300?text=Raw+Clove",
            image_url_ai="https://placehold.co/600x400/1a1a1a/e5e5e5?text=Girofle+Excellence",
            status="PUBLISHED",
            description="Clous de girofle triés à la main, séchage naturel au soleil sur nattes. Taux de corps étrangers < 0.5%. Idéal pour l'extraction d'huile essentielle ou l'épice entière.",
            origin="Fénérive-Est, Côte Est",
            farmer_name="Association des Producteurs de l'Est",
            harvest_date="Octobre 2024",
            moisture_content=11.0,
            vanillin_content=0.0 # N/A
        )
    ]
    
    for p in products:
        db.add(p)
    
    # --- PRODUCERS SEED ---
    if db.query(ProducerProfile).count() > 0:
        db.query(ProducerProfile).delete()
    
    producers = [
        ProducerProfile(
            id=1,
            name="Sava Gold Collectors",
            location_region="Sava, Madagascar",
            location_district="Sambava",
            bio="Leading collector in Sambava region since 2010. We work with over 500 smallholder farmers to bring you the finest vanilla.",
            trust_score=4.8,
            years_experience=14,
            transactions_count=124,
            badges=["ORGANIC", "FAIRTRADE", "WOMEN_OWNED"]
        ),
        ProducerProfile(
            id=2,
            name="Coopérative Taroka",
            location_region="Sava, Madagascar",
            location_district="Antalaha",
            bio="A cooperative of 50 families dedicated to sustainable agroforestry showing the world that quality and ecology go hand in hand.",
            trust_score=4.9,
            years_experience=8,
            transactions_count=56,
            badges=["RAINFOREST", "BIO"]
        )
    ]
    
    for producer in producers:
        db.add(producer)

    db.commit()
    print("DB Seeded/Refreshed successfully via Showcase Data.")
    db.close()

if __name__ == "__main__":
    init_db()
