from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SourcingRequest(Base):
    __tablename__ = "sourcing_requests"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, index=True) # Logic Link to User table (when created)
    
    # Core Request Info
    product_type = Column(String, index=True) # e.g. "Vanilla", "Clove"
    volume_target_kg = Column(Float)
    price_target_usd = Column(Float) # Desired FOB Price
    grade_target = Column(String) # "A", "B", "C"
    
    # Logic
    accepts_partial = Column(Boolean, default=True)
    status = Column(String, default="OPEN") # OPEN, FULFILLED, CLOSED
    
    # Advanced Specs (JSON for flexibility)
    # e.g. {"vanillin_content_min": 1.4, "moisture_max": 30}
    specs_json = Column(JSON, nullable=True)

    # [NEW] Certifications (Feature 7)
    # e.g. ["Organic", "Fairtrade"]
    required_certs = Column(JSON, nullable=True)

    # [NEW] Supply Chain (Feature 8)
    # e.g. "PREPARING", "TRANSIT_TO_PORT", "AT_PORT", "FOB_COMPLETE"
    logistics_status = Column(String, default="PREPARING") 
    
    # Relationship
    offers = relationship("SourcingOffer", back_populates="request")


class SourcingOffer(Base):
    __tablename__ = "sourcing_offers"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("sourcing_requests.id"))
    facilitator_id = Column(Integer, ForeignKey("producer_profiles.id"), index=True)
    
    # Offer Details
    volume_offered_kg = Column(Float)
    price_offered_usd = Column(Float)
    
    status = Column(String, default="PENDING") # PENDING, NEGOTIATING, ACCEPTED, REJECTED
    
    # Evidence
    # e.g. ["url_photo_1", "url_photo_2"]
    photos_json = Column(JSON, nullable=True) 

    # [NEW] Cert Proofs (Feature 7)
    # e.g. ["http://s3.../cert_bio.pdf"]
    cert_proofs_urls = Column(JSON, nullable=True)

    # [NEW] Mock Ranking (Feature 9)
    # In a real app, this is computed. For MVP we store it to simulate sorting.
    trust_score_snapshot = Column(Float, default=4.5)
    
    # Relationship
    request = relationship("SourcingRequest", back_populates="offers")
    producer = relationship("ProducerProfile", back_populates="offers")
