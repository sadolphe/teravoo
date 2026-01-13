from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# --- Producer Schemas ---

class ProducerBase(BaseModel):
    name: str
    location_region: str
    location_district: str
    bio: Optional[str] = None
    badges: Optional[List[str]] = []

class ProducerCreate(ProducerBase):
    pass

class ProducerUpdate(ProducerBase):
    pass

class ProducerResponse(ProducerBase):
    id: int
    trust_score: float
    years_experience: int
    transactions_count: int
    created_at: datetime

    class Config:
        orm_mode = True

# --- Traceability Schemas ---

class TraceabilityEventBase(BaseModel):
    stage: str # ORIGIN, QUALITY, TRANSIT, FOB, DELIVERED
    status: str # VALIDATED, PENDING, ALERT
    description: str
    location_scan: Optional[str] = None
    documents_urls: Optional[List[str]] = []
    
    # Links
    request_id: Optional[int] = None
    offer_id: Optional[int] = None

class TraceabilityEventCreate(TraceabilityEventBase):
    created_by: str = "System"

class TraceabilityEventResponse(TraceabilityEventBase):
    id: int
    timestamp: datetime
    created_by: str

    class Config:
        orm_mode = True

# Aggregated Timeline View
class TraceabilityTimeline(BaseModel):
    request_id: int
    events: List[TraceabilityEventResponse]
