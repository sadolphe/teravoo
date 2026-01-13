from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str 
    price_fob: float
    image_url: str 
    
    # Optional fields at creation (can be updated later or inferred)
    description: Optional[str] = None
    origin: Optional[str] = "Sava Region, Madagascar"
    moisture_content: Optional[float] = None
    vanillin_content: Optional[float] = None
    producer_id: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price_fob: float
    image_url_raw: str
    image_url_ai: str
    status: str
    
    description: Optional[str] = None
    origin: Optional[str] = None
    farmer_name: Optional[str] = None
    harvest_date: Optional[str] = None
    moisture_content: Optional[float] = None
    vanillin_content: Optional[float] = None
    producer_id: Optional[int] = None
