from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List
from datetime import datetime


# ═══════════════════════════════════════════════════════════
# TEMPLATE TIERS (Option B - Templates réutilisables)
# ═══════════════════════════════════════════════════════════

class TemplateTierBase(BaseModel):
    min_quantity_kg: float
    max_quantity_kg: Optional[float] = None
    discount_percent: float = 0.0

    @field_validator('discount_percent')
    @classmethod
    def validate_discount(cls, v):
        if v < 0 or v > 100:
            raise ValueError('discount_percent doit être entre 0 et 100')
        return v

    @field_validator('min_quantity_kg')
    @classmethod
    def validate_min_quantity(cls, v):
        if v < 0:
            raise ValueError('min_quantity_kg doit être positif')
        return v


class TemplateTierCreate(TemplateTierBase):
    pass


class TemplateTierResponse(TemplateTierBase):
    id: int
    position: int

    class Config:
        from_attributes = True


class PriceTierTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_default: bool = False
    tiers: List[TemplateTierCreate]

    @field_validator('tiers')
    @classmethod
    def validate_tiers(cls, v):
        if not v:
            raise ValueError('Au moins un palier est requis')
        if len(v) > 5:
            raise ValueError('Maximum 5 paliers autorisés')
        return v

    @model_validator(mode='after')
    def validate_tiers_contiguity(self):
        tiers = sorted(self.tiers, key=lambda t: t.min_quantity_kg)
        for i, tier in enumerate(tiers):
            if i == 0 and tier.min_quantity_kg != 1:
                # Le premier palier doit commencer à 1 kg
                pass  # On autorise d'autres valeurs pour flexibilité
            if i > 0:
                prev_tier = tiers[i - 1]
                # Vérifier que les discounts sont croissants
                if tier.discount_percent < prev_tier.discount_percent:
                    raise ValueError('Les réductions doivent être croissantes avec la quantité')
        return self


class PriceTierTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    tiers: Optional[List[TemplateTierCreate]] = None


class PriceTierTemplateResponse(BaseModel):
    id: int
    producer_id: int
    name: str
    description: Optional[str] = None
    is_default: bool
    tiers: List[TemplateTierResponse] = []
    products_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════
# PRICE TIERS (Option A - Paliers par produit)
# ═══════════════════════════════════════════════════════════

class PriceTierBase(BaseModel):
    min_quantity_kg: float
    max_quantity_kg: Optional[float] = None
    price_per_kg: float

    @field_validator('price_per_kg')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('price_per_kg doit être positif')
        return v

    @field_validator('min_quantity_kg')
    @classmethod
    def validate_min_quantity(cls, v):
        if v < 0:
            raise ValueError('min_quantity_kg doit être positif')
        return v


class PriceTierCreate(PriceTierBase):
    pass


class PriceTierResponse(PriceTierBase):
    id: int
    product_id: int
    position: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductPriceTiersCreate(BaseModel):
    """Création/Remplacement de tous les paliers d'un produit"""
    tiers: List[PriceTierCreate]

    @field_validator('tiers')
    @classmethod
    def validate_tiers(cls, v):
        if not v:
            raise ValueError('Au moins un palier est requis')
        if len(v) > 5:
            raise ValueError('Maximum 5 paliers autorisés')
        return v

    @model_validator(mode='after')
    def validate_tiers_decreasing_price(self):
        tiers = sorted(self.tiers, key=lambda t: t.min_quantity_kg)
        for i in range(1, len(tiers)):
            if tiers[i].price_per_kg > tiers[i - 1].price_per_kg:
                raise ValueError('Les prix doivent être décroissants avec la quantité')
        return self


# ═══════════════════════════════════════════════════════════
# PRICING MODE
# ═══════════════════════════════════════════════════════════

class PricingModeUpdate(BaseModel):
    """Changement du mode de tarification d'un produit"""
    mode: str  # SINGLE, TIERED, TEMPLATE
    template_id: Optional[int] = None  # Requis si mode = TEMPLATE

    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v):
        if v not in ['SINGLE', 'TIERED', 'TEMPLATE']:
            raise ValueError('mode doit être SINGLE, TIERED ou TEMPLATE')
        return v

    @model_validator(mode='after')
    def validate_template_required(self):
        if self.mode == 'TEMPLATE' and not self.template_id:
            raise ValueError('template_id est requis quand mode = TEMPLATE')
        return self


# ═══════════════════════════════════════════════════════════
# CALCUL DE PRIX
# ═══════════════════════════════════════════════════════════

class TierApplied(BaseModel):
    min_quantity_kg: float
    max_quantity_kg: Optional[float] = None
    position: int


class NextTierInfo(BaseModel):
    at_quantity_kg: float
    price_per_kg: float
    extra_savings_total: float


class PriceTrendInfo(BaseModel):
    direction: str  # "up", "down", "stable"
    percent: float
    since: Optional[datetime] = None


class CalculatedPrice(BaseModel):
    """Résultat du calcul de prix pour une quantité donnée"""
    product_id: int
    quantity_kg: float
    pricing_mode: str

    tier_applied: Optional[TierApplied] = None
    price_per_kg: float
    total: float

    savings_vs_base: Optional[dict] = None  # {percent: float, amount: float}
    next_tier: Optional[NextTierInfo] = None
    price_trend: Optional[PriceTrendInfo] = None


# ═══════════════════════════════════════════════════════════
# HISTORIQUE
# ═══════════════════════════════════════════════════════════

class PriceTierHistoryResponse(BaseModel):
    id: int
    product_id: int
    pricing_mode: str
    base_price_fob: float
    tiers_snapshot: Optional[List[dict]] = None
    change_reason: Optional[str] = None
    changed_at: datetime
    changed_by: Optional[str] = None

    class Config:
        from_attributes = True


class PriceComparisonResponse(BaseModel):
    """Comparaison des prix entre deux dates"""
    product_id: int
    current_base_price: float
    previous_base_price: float
    price_change_percent: float
    compared_to_date: datetime
