from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price_fob = Column(Float)
    image_url_raw = Column(String)
    image_url_ai = Column(String)
    status = Column(String, default="DRAFT") # DRAFT, PUBLISHED
    
    # Showcase Fields
    description = Column(String, nullable=True) # Full text description
    origin = Column(String, nullable=True) # e.g. "Sava Region, Sambava"
    farmer_name = Column(String, nullable=True) # e.g. "Jean-Pierre R."
    
    # Specs
    harvest_date = Column(String, nullable=True) # e.g. "July 2025" - String for simplicity MVP
    moisture_content = Column(Float, nullable=True) # e.g. 35.0 (%)
    vanillin_content = Column(Float, nullable=True) # e.g. 1.8 (%)

    # Sourcing Link
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=True)
    producer = relationship("ProducerProfile")
