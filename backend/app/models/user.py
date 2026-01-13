from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=True) # Nullable for email-only buyers
    email = Column(String, unique=True, index=True, nullable=True) # Nullable for phone-only facilitators
    
    role = Column(String, default="FACILITATOR") # FACILITATOR, PRODUCER_REPRESENTATIVE, ADMIN, BUYER
    full_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    kyb_status = Column(String, default="PENDING") # PENDING, VALIDATED, REJECTED
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
