from pydantic import BaseModel
from typing import Optional, List
from app.schemas.pricing import PriceTierResponse, TemplateTierResponse


class ProductCreate(BaseModel):
    name: str
    price_fob: float
    image_url: str
    grade: Optional[str] = "A"

    # Optional fields at creation (can be updated later or inferred)
    description: Optional[str] = None
    origin: Optional[str] = "Sava Region, Madagascar"
    moisture_content: Optional[float] = None
    vanillin_content: Optional[float] = None
    producer_id: Optional[int] = None

    # Pricing configuration (optional at creation)
    moq_kg: Optional[float] = 1.0
    pricing_mode: Optional[str] = "SINGLE"

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    price_fob: Optional[float] = None
    moisture_content: Optional[float] = None
    vanillin_content: Optional[float] = None
    description: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price_fob: float
    image_url_raw: str
    image_url_ai: str
    status: str
    grade: Optional[str] = "A"

    description: Optional[str] = None
    origin: Optional[str] = None
    farmer_name: Optional[str] = None
    harvest_date: Optional[str] = None
    moisture_content: Optional[float] = None
    vanillin_content: Optional[float] = None
    producer_id: Optional[int] = None
    quantity_available: Optional[int] = None

    # Pricing fields
    moq_kg: float = 1.0
    pricing_mode: str = "SINGLE"
    template_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProductWithPricingResponse(ProductResponse):
    """Product response with full pricing tiers details"""
    price_tiers: List[PriceTierResponse] = []
    # Computed tiers from template (if pricing_mode = TEMPLATE)
    computed_tiers: Optional[List[dict]] = None
