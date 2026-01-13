from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String) # Snapshot of product name
    amount = Column(Float)
    status = Column(String, default="PENDING")
    contract_url = Column(String, nullable=True)
    buyer_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # We could adding FK to Product, but for MVP strict loose coupling or direct ID is fine.
    # Let's keep it simple: just product_id stored if needed, but the PDF logic used snapshots.
    product_id = Column(Integer)
