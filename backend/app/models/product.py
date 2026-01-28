from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price_fob = Column(Float)  # Prix de base FOB/kg
    image_url_raw = Column(String)
    image_url_ai = Column(String)
    status = Column(String, default="DRAFT")  # DRAFT, PUBLISHED
    grade = Column(String, default="A")  # A, B, C, D, SPLITS, CUTS

    # Showcase Fields
    description = Column(String, nullable=True)  # Full text description
    origin = Column(String, nullable=True)  # e.g. "Sava Region, Sambava"
    farmer_name = Column(String, nullable=True)  # e.g. "Jean-Pierre R."

    # Specs
    harvest_date = Column(String, nullable=True)  # e.g. "July 2025" - String for simplicity MVP
    moisture_content = Column(Float, nullable=True)  # e.g. 35.0 (%)
    vanillin_content = Column(Float, nullable=True)  # e.g. 1.8 (%)
    quantity_available = Column(Integer, default=500)  # Stock tracking

    # Sourcing Link
    producer_id = Column(Integer, ForeignKey("producer_profiles.id"), nullable=True)
    producer = relationship("ProducerProfile", back_populates="products")

    # Pricing Configuration
    moq_kg = Column(Float, default=1.0)  # Minimum Order Quantity en kg
    pricing_mode = Column(String, default="SINGLE")  # SINGLE, TIERED, TEMPLATE
    template_id = Column(Integer, ForeignKey("price_tier_templates.id"), nullable=True)

    # Relationships for pricing
    price_template = relationship("PriceTierTemplate", back_populates="products")
    price_tiers = relationship("PriceTier", back_populates="product", cascade="all, delete-orphan", order_by="PriceTier.position")
    price_history = relationship("PriceTierHistory", back_populates="product", cascade="all, delete-orphan", order_by="PriceTierHistory.changed_at.desc()")
