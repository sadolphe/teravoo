from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.models.product import Product
from app.models.producer import ProducerProfile
from app.models.pricing import PriceTierTemplate, TemplateTier, PriceTier, PriceTierHistory
from app.schemas.pricing import (
    PriceTierTemplateCreate,
    PriceTierTemplateUpdate,
    PriceTierTemplateResponse,
    ProductPriceTiersCreate,
    PriceTierResponse,
    PricingModeUpdate,
    CalculatedPrice,
    TierApplied,
    NextTierInfo,
    PriceTrendInfo,
    PriceTierHistoryResponse,
    PriceComparisonResponse,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def create_price_history_snapshot(db: Session, product: Product, change_reason: str = None, changed_by: str = None):
    """Crée un snapshot de l'état actuel des prix avant modification"""
    tiers_snapshot = None

    if product.pricing_mode == "TIERED":
        tiers_snapshot = [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": t.price_per_kg,
                "position": t.position
            }
            for t in product.price_tiers
        ]
    elif product.pricing_mode == "TEMPLATE" and product.price_template:
        tiers_snapshot = [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "discount_percent": t.discount_percent,
                "computed_price": product.price_fob * (1 - t.discount_percent / 100),
                "position": t.position
            }
            for t in product.price_template.tiers
        ]

    history = PriceTierHistory(
        product_id=product.id,
        pricing_mode=product.pricing_mode,
        base_price_fob=product.price_fob,
        tiers_snapshot=tiers_snapshot,
        template_id_snapshot=product.template_id,
        change_reason=change_reason,
        changed_by=changed_by
    )
    db.add(history)
    return history


def get_effective_tiers(product: Product) -> List[dict]:
    """Retourne les paliers effectifs (calculés) pour un produit"""
    if product.pricing_mode == "SINGLE":
        return [{
            "min_quantity_kg": product.moq_kg,
            "max_quantity_kg": None,
            "price_per_kg": product.price_fob,
            "position": 0,
            "discount_percent": 0
        }]
    elif product.pricing_mode == "TIERED":
        return [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": t.price_per_kg,
                "position": t.position,
                "discount_percent": round((1 - t.price_per_kg / product.price_fob) * 100, 2) if product.price_fob > 0 else 0
            }
            for t in sorted(product.price_tiers, key=lambda x: x.position)
        ]
    elif product.pricing_mode == "TEMPLATE" and product.price_template:
        return [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": round(product.price_fob * (1 - t.discount_percent / 100), 2),
                "position": t.position,
                "discount_percent": t.discount_percent
            }
            for t in sorted(product.price_template.tiers, key=lambda x: x.position)
        ]
    return []


def find_applicable_tier(tiers: List[dict], quantity_kg: float) -> Optional[dict]:
    """Trouve le palier applicable pour une quantité donnée"""
    sorted_tiers = sorted(tiers, key=lambda t: t["min_quantity_kg"], reverse=True)
    for tier in sorted_tiers:
        if quantity_kg >= tier["min_quantity_kg"]:
            if tier["max_quantity_kg"] is None or quantity_kg <= tier["max_quantity_kg"]:
                return tier
    # Fallback au premier palier si quantité trop petite
    if tiers:
        return sorted(tiers, key=lambda t: t["min_quantity_kg"])[0]
    return None


# ═══════════════════════════════════════════════════════════
# TEMPLATES ENDPOINTS (Option B)
# ═══════════════════════════════════════════════════════════

@router.post("/producers/{producer_id}/price-templates", response_model=PriceTierTemplateResponse)
def create_price_template(
    producer_id: int,
    template_in: PriceTierTemplateCreate,
    db: Session = Depends(deps.get_db)
):
    """Créer un nouveau template de paliers tarifaires pour un producteur"""
    # Vérifier que le producteur existe
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producteur non trouvé")

    # Si is_default, retirer le flag des autres templates
    if template_in.is_default:
        db.query(PriceTierTemplate).filter(
            PriceTierTemplate.producer_id == producer_id,
            PriceTierTemplate.is_default == True
        ).update({"is_default": False})

    # Créer le template
    db_template = PriceTierTemplate(
        producer_id=producer_id,
        name=template_in.name,
        description=template_in.description,
        is_default=template_in.is_default
    )
    db.add(db_template)
    db.flush()  # Pour avoir l'ID

    # Créer les paliers du template
    sorted_tiers = sorted(template_in.tiers, key=lambda t: t.min_quantity_kg)
    for position, tier_data in enumerate(sorted_tiers):
        db_tier = TemplateTier(
            template_id=db_template.id,
            min_quantity_kg=tier_data.min_quantity_kg,
            max_quantity_kg=tier_data.max_quantity_kg,
            discount_percent=tier_data.discount_percent,
            position=position
        )
        db.add(db_tier)

    db.commit()
    db.refresh(db_template)

    return PriceTierTemplateResponse(
        id=db_template.id,
        producer_id=db_template.producer_id,
        name=db_template.name,
        description=db_template.description,
        is_default=db_template.is_default,
        tiers=[
            {
                "id": t.id,
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "discount_percent": t.discount_percent,
                "position": t.position
            }
            for t in db_template.tiers
        ],
        products_count=len(db_template.products),
        created_at=db_template.created_at,
        updated_at=db_template.updated_at
    )


@router.get("/producers/{producer_id}/price-templates", response_model=List[PriceTierTemplateResponse])
def list_producer_templates(
    producer_id: int,
    db: Session = Depends(deps.get_db)
):
    """Lister tous les templates de paliers d'un producteur"""
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producteur non trouvé")

    templates = db.query(PriceTierTemplate).filter(
        PriceTierTemplate.producer_id == producer_id
    ).all()

    return [
        PriceTierTemplateResponse(
            id=t.id,
            producer_id=t.producer_id,
            name=t.name,
            description=t.description,
            is_default=t.is_default,
            tiers=[
                {
                    "id": tier.id,
                    "min_quantity_kg": tier.min_quantity_kg,
                    "max_quantity_kg": tier.max_quantity_kg,
                    "discount_percent": tier.discount_percent,
                    "position": tier.position
                }
                for tier in t.tiers
            ],
            products_count=len(t.products),
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in templates
    ]


@router.put("/price-templates/{template_id}", response_model=PriceTierTemplateResponse)
def update_price_template(
    template_id: int,
    template_in: PriceTierTemplateUpdate,
    db: Session = Depends(deps.get_db)
):
    """Modifier un template (met à jour les prix de tous les produits liés)"""
    db_template = db.query(PriceTierTemplate).filter(PriceTierTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template non trouvé")

    # Créer un snapshot historique pour tous les produits liés
    for product in db_template.products:
        create_price_history_snapshot(db, product, "Modification du template", "System")

    # Mettre à jour les champs simples
    if template_in.name is not None:
        db_template.name = template_in.name
    if template_in.description is not None:
        db_template.description = template_in.description
    if template_in.is_default is not None:
        if template_in.is_default:
            db.query(PriceTierTemplate).filter(
                PriceTierTemplate.producer_id == db_template.producer_id,
                PriceTierTemplate.is_default == True,
                PriceTierTemplate.id != template_id
            ).update({"is_default": False})
        db_template.is_default = template_in.is_default

    # Remplacer les paliers si fournis
    if template_in.tiers is not None:
        # Supprimer les anciens paliers
        db.query(TemplateTier).filter(TemplateTier.template_id == template_id).delete()

        # Créer les nouveaux
        sorted_tiers = sorted(template_in.tiers, key=lambda t: t.min_quantity_kg)
        for position, tier_data in enumerate(sorted_tiers):
            db_tier = TemplateTier(
                template_id=template_id,
                min_quantity_kg=tier_data.min_quantity_kg,
                max_quantity_kg=tier_data.max_quantity_kg,
                discount_percent=tier_data.discount_percent,
                position=position
            )
            db.add(db_tier)

    db.commit()
    db.refresh(db_template)

    return PriceTierTemplateResponse(
        id=db_template.id,
        producer_id=db_template.producer_id,
        name=db_template.name,
        description=db_template.description,
        is_default=db_template.is_default,
        tiers=[
            {
                "id": t.id,
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "discount_percent": t.discount_percent,
                "position": t.position
            }
            for t in db_template.tiers
        ],
        products_count=len(db_template.products),
        created_at=db_template.created_at,
        updated_at=db_template.updated_at
    )


@router.delete("/price-templates/{template_id}")
def delete_price_template(
    template_id: int,
    db: Session = Depends(deps.get_db)
):
    """Supprimer un template (seulement si aucun produit lié)"""
    db_template = db.query(PriceTierTemplate).filter(PriceTierTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template non trouvé")

    if db_template.products:
        raise HTTPException(
            status_code=400,
            detail=f"Impossible de supprimer: {len(db_template.products)} produit(s) utilisent ce template"
        )

    db.delete(db_template)
    db.commit()

    return {"status": "deleted", "template_id": template_id}


# ═══════════════════════════════════════════════════════════
# PRODUCT PRICE TIERS ENDPOINTS (Option A)
# ═══════════════════════════════════════════════════════════

@router.post("/products/{product_id}/price-tiers", response_model=List[PriceTierResponse])
def set_product_price_tiers(
    product_id: int,
    tiers_in: ProductPriceTiersCreate,
    db: Session = Depends(deps.get_db)
):
    """Définir les paliers personnalisés pour un produit (remplace les existants)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Créer un snapshot historique avant modification
    create_price_history_snapshot(db, product, "Définition des paliers personnalisés", "System")

    # Supprimer les anciens paliers
    db.query(PriceTier).filter(PriceTier.product_id == product_id).delete()

    # Passer en mode TIERED
    product.pricing_mode = "TIERED"
    product.template_id = None

    # Créer les nouveaux paliers
    sorted_tiers = sorted(tiers_in.tiers, key=lambda t: t.min_quantity_kg)
    created_tiers = []

    for position, tier_data in enumerate(sorted_tiers):
        db_tier = PriceTier(
            product_id=product_id,
            min_quantity_kg=tier_data.min_quantity_kg,
            max_quantity_kg=tier_data.max_quantity_kg,
            price_per_kg=tier_data.price_per_kg,
            position=position
        )
        db.add(db_tier)
        created_tiers.append(db_tier)

    db.commit()

    # Refresh pour avoir les IDs
    for tier in created_tiers:
        db.refresh(tier)

    return created_tiers


@router.get("/products/{product_id}/price-tiers")
def get_product_price_tiers(
    product_id: int,
    db: Session = Depends(deps.get_db)
):
    """Récupérer les paliers d'un produit (calculés si template)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    tiers = get_effective_tiers(product)

    return {
        "product_id": product_id,
        "pricing_mode": product.pricing_mode,
        "base_price_fob": product.price_fob,
        "moq_kg": product.moq_kg,
        "template_id": product.template_id,
        "tiers": tiers
    }


@router.delete("/products/{product_id}/price-tiers")
def delete_product_price_tiers(
    product_id: int,
    db: Session = Depends(deps.get_db)
):
    """Supprimer tous les paliers personnalisés et repasser en mode SINGLE"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Snapshot avant modification
    create_price_history_snapshot(db, product, "Suppression des paliers", "System")

    # Supprimer les paliers
    db.query(PriceTier).filter(PriceTier.product_id == product_id).delete()

    # Repasser en mode SINGLE
    product.pricing_mode = "SINGLE"
    product.template_id = None

    db.commit()

    return {"status": "deleted", "product_id": product_id, "pricing_mode": "SINGLE"}


@router.put("/products/{product_id}/pricing-mode")
def update_product_pricing_mode(
    product_id: int,
    mode_in: PricingModeUpdate,
    db: Session = Depends(deps.get_db)
):
    """Changer le mode de tarification d'un produit"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Si mode TEMPLATE, vérifier que le template existe et appartient au même producteur
    if mode_in.mode == "TEMPLATE":
        template = db.query(PriceTierTemplate).filter(PriceTierTemplate.id == mode_in.template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template non trouvé")
        if product.producer_id and template.producer_id != product.producer_id:
            raise HTTPException(status_code=400, detail="Le template doit appartenir au même producteur")

    # Snapshot avant modification
    create_price_history_snapshot(db, product, f"Changement de mode: {product.pricing_mode} → {mode_in.mode}", "System")

    # Mettre à jour
    product.pricing_mode = mode_in.mode
    product.template_id = mode_in.template_id if mode_in.mode == "TEMPLATE" else None

    db.commit()
    db.refresh(product)

    return {
        "product_id": product_id,
        "pricing_mode": product.pricing_mode,
        "template_id": product.template_id,
        "effective_tiers": get_effective_tiers(product)
    }


# ═══════════════════════════════════════════════════════════
# PRICE CALCULATION ENDPOINT
# ═══════════════════════════════════════════════════════════

@router.get("/products/{product_id}/calculate-price", response_model=CalculatedPrice)
def calculate_price(
    product_id: int,
    quantity_kg: float = Query(..., gt=0, description="Quantité en kg"),
    db: Session = Depends(deps.get_db)
):
    """Calculer le prix pour une quantité donnée"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Vérifier le MOQ
    if quantity_kg < product.moq_kg:
        raise HTTPException(
            status_code=400,
            detail=f"Quantité minimum: {product.moq_kg} kg"
        )

    # Obtenir les paliers effectifs
    tiers = get_effective_tiers(product)
    if not tiers:
        # Fallback au prix de base
        return CalculatedPrice(
            product_id=product_id,
            quantity_kg=quantity_kg,
            pricing_mode=product.pricing_mode,
            price_per_kg=product.price_fob,
            total=round(product.price_fob * quantity_kg, 2)
        )

    # Trouver le palier applicable
    applicable_tier = find_applicable_tier(tiers, quantity_kg)
    if not applicable_tier:
        applicable_tier = tiers[0]

    price_per_kg = applicable_tier["price_per_kg"]
    total = round(price_per_kg * quantity_kg, 2)

    # Calculer les économies vs prix de base
    base_price = product.price_fob
    savings_vs_base = None
    if base_price > 0 and price_per_kg < base_price:
        savings_amount = round((base_price - price_per_kg) * quantity_kg, 2)
        savings_percent = round((1 - price_per_kg / base_price) * 100, 2)
        savings_vs_base = {"percent": savings_percent, "amount": savings_amount}

    # Trouver le prochain palier
    next_tier = None
    sorted_tiers = sorted(tiers, key=lambda t: t["min_quantity_kg"])
    current_idx = next((i for i, t in enumerate(sorted_tiers) if t["position"] == applicable_tier["position"]), -1)
    if current_idx >= 0 and current_idx < len(sorted_tiers) - 1:
        next_tier_data = sorted_tiers[current_idx + 1]
        extra_quantity = next_tier_data["min_quantity_kg"] - quantity_kg
        extra_savings = round((price_per_kg - next_tier_data["price_per_kg"]) * next_tier_data["min_quantity_kg"], 2)
        next_tier = NextTierInfo(
            at_quantity_kg=next_tier_data["min_quantity_kg"],
            price_per_kg=next_tier_data["price_per_kg"],
            extra_savings_total=extra_savings
        )

    # Tendance des prix (historique)
    price_trend = None
    last_history = db.query(PriceTierHistory).filter(
        PriceTierHistory.product_id == product_id
    ).order_by(desc(PriceTierHistory.changed_at)).first()

    if last_history and last_history.base_price_fob != product.price_fob:
        change_percent = round((product.price_fob - last_history.base_price_fob) / last_history.base_price_fob * 100, 2)
        price_trend = PriceTrendInfo(
            direction="down" if change_percent < 0 else "up" if change_percent > 0 else "stable",
            percent=abs(change_percent),
            since=last_history.changed_at
        )

    return CalculatedPrice(
        product_id=product_id,
        quantity_kg=quantity_kg,
        pricing_mode=product.pricing_mode,
        tier_applied=TierApplied(
            min_quantity_kg=applicable_tier["min_quantity_kg"],
            max_quantity_kg=applicable_tier.get("max_quantity_kg"),
            position=applicable_tier["position"]
        ),
        price_per_kg=price_per_kg,
        total=total,
        savings_vs_base=savings_vs_base,
        next_tier=next_tier,
        price_trend=price_trend
    )


# ═══════════════════════════════════════════════════════════
# PRICE HISTORY ENDPOINTS
# ═══════════════════════════════════════════════════════════

@router.get("/products/{product_id}/price-history", response_model=List[PriceTierHistoryResponse])
def get_product_price_history(
    product_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db)
):
    """Récupérer l'historique des changements de prix d'un produit"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    history = db.query(PriceTierHistory).filter(
        PriceTierHistory.product_id == product_id
    ).order_by(desc(PriceTierHistory.changed_at)).limit(limit).all()

    return history


@router.get("/products/{product_id}/price-history/compare", response_model=PriceComparisonResponse)
def compare_product_price(
    product_id: int,
    from_date: datetime = Query(..., description="Date de comparaison"),
    db: Session = Depends(deps.get_db)
):
    """Comparer le prix actuel avec une date passée"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Trouver le snapshot le plus proche de la date demandée
    history = db.query(PriceTierHistory).filter(
        PriceTierHistory.product_id == product_id,
        PriceTierHistory.changed_at <= from_date
    ).order_by(desc(PriceTierHistory.changed_at)).first()

    if not history:
        raise HTTPException(status_code=404, detail="Pas d'historique disponible pour cette date")

    change_percent = round((product.price_fob - history.base_price_fob) / history.base_price_fob * 100, 2)

    return PriceComparisonResponse(
        product_id=product_id,
        current_base_price=product.price_fob,
        previous_base_price=history.base_price_fob,
        price_change_percent=change_percent,
        compared_to_date=history.changed_at
    )
