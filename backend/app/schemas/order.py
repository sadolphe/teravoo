from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: int
    quantity_kg: float
    offer_price_total: float # e.g. 2400.0 for 10kg
    buyer_name: str # Simplified for MVP, usually from Auth

class OrderResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    amount: float
    status: str # PENDING, CONTRACT_SIGNED, SECURED, SHIPPED
    contract_url: Optional[str] = None
    created_at: datetime
