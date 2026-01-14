from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class ProducerProfile(Base):
    __tablename__ = "producer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    # Link to Auth User
    user_id = Column(Integer, nullable=True) # Linked to users.id manually for MVP
    
    name = Column(String, index=True) # "Sava Gold Collectors"
    location_region = Column(String) # "Sava, Madagascar"
    location_district = Column(String) # "Sambava"
    bio = Column(String) # "Specialized in organic vanilla since 2010..."
    
    # KPIs (Denormalized for MVP speed)
    trust_score = Column(Float, default=5.0)
    years_experience = Column(Integer, default=1)
    transactions_count = Column(Integer, default=0)
    
    # Certifications badges (cached list of strings)
    badges = Column(JSON, default=list) # ["BIO", "FAIRTRADE"]
    
    # Contact info (Hidden publically)
    contact_email = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    offers = relationship("SourcingOffer", back_populates="producer")

class TraceabilityEvent(Base):
    __tablename__ = "traceability_events"

    id = Column(Integer, primary_key=True, index=True)
    
    # Polymorphic-like association (simpler for MVP)
    # Usually linked to a Request (if global) or an Offer (if specific) or a Shipment
    request_id = Column(Integer, ForeignKey("sourcing_requests.id"), nullable=True)
    offer_id = Column(Integer, ForeignKey("sourcing_offers.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    

    stage = Column(String) # "ORIGIN", "QUALITY_CHECK", "TRANSIT", "FOB", "DELIVERED"
    status = Column(String) # "VALIDATED", "PENDING", "ALERT", "CORRECTION"
    
    description = Column(String) # "Harvest declaration", "Phyto certificate uploaded"
    location_scan = Column(String, nullable=True) # "Lat,Long"
    
    # Evidence (Documents/Photos)
    documents_urls = Column(JSON, default=list) 
    
    # Immutable timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String) # "System (AI)", "Facilitator", "Admin"
