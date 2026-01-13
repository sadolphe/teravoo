from typing import List, Optional, Any
from pydantic import BaseModel

# --- OFFER SCHEMAS ---

class SourcingOfferBase(BaseModel):
    volume_offered_kg: float
    price_offered_usd: float
    photos_json: Optional[List[str]] = []
    # FEATURE 7
    cert_proofs_urls: Optional[List[str]] = []

class SourcingOfferCreate(SourcingOfferBase):
    request_id: int
    facilitator_id: int

class SourcingOfferUpdate(BaseModel):
    status: Optional[str] = None # ACCEPTED, REJECTED, NEGOTIATING
    price_offered_usd: Optional[float] = None

class SourcingOfferResponse(SourcingOfferBase):
    id: int
    request_id: int
    facilitator_id: int
    status: str
    # FEATURE 9
    trust_score_snapshot: Optional[float] = 4.5

    class Config:
        orm_mode = True

# --- REQUEST SCHEMAS ---

class SourcingRequestBase(BaseModel):
    product_type: str
    volume_target_kg: float
    price_target_usd: float
    grade_target: str
    accepts_partial: bool = True
    specs_json: Optional[dict] = {}
    
    # FEATURE 7
    required_certs: Optional[List[str]] = [] # ["Organic"]

class SourcingRequestCreate(SourcingRequestBase):
    buyer_id: int # In real app, this comes from token

class SourcingRequestResponse(SourcingRequestBase):
    id: int
    buyer_id: int
    status: str
    offers: List[SourcingOfferResponse] = []
    
    # FEATURE 8
    logistics_status: Optional[str] = "PREPARING"
    
    # Computed fields for Dashboard
    @property
    def total_covered_kg(self) -> float:
        # This will be computed in validation or service layer if needed,
        # but for simple response, we might just assume the backend passes it pre-calculated
        # or lets frontend calculate it from 'offers'.
        # We'll rely on the 'offers' list for now.
        return 0.0

    class Config:
        orm_mode = True
