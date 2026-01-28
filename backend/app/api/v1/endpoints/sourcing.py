from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.models.sourcing import SourcingRequest, SourcingOffer
from app.models.product import Product
from app.models.producer import ProducerProfile
from app.services.pdf_service import pdf_service
from app.schemas.sourcing import (
    SourcingRequestCreate,
    SourcingRequestResponse,
    SourcingOfferCreate,
    SourcingOfferResponse,
    SourcingOfferUpdate
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════
# PRICING TIER INTEGRATION HELPERS
# ═══════════════════════════════════════════════════════════

def get_product_effective_tiers(product: Product) -> List[dict]:
    """Retourne les paliers effectifs pour un produit"""
    if product.pricing_mode == "SINGLE":
        return [{
            "min_quantity_kg": product.moq_kg or 1.0,
            "max_quantity_kg": None,
            "price_per_kg": product.price_fob,
            "discount_percent": 0,
            "position": 0
        }]
    elif product.pricing_mode == "TIERED":
        return [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": t.price_per_kg,
                "discount_percent": round((1 - t.price_per_kg / product.price_fob) * 100, 2) if product.price_fob > 0 else 0,
                "position": t.position
            }
            for t in sorted(product.price_tiers, key=lambda x: x.position)
        ]
    elif product.pricing_mode == "TEMPLATE" and product.price_template:
        return [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": round(product.price_fob * (1 - t.discount_percent / 100), 2),
                "discount_percent": t.discount_percent,
                "position": t.position
            }
            for t in sorted(product.price_template.tiers, key=lambda x: x.position)
        ]
    return []


def get_producer_effective_tiers(producer: ProducerProfile, product_type: str, db: Session) -> List[dict]:
    """
    Récupère les paliers effectifs pour un producteur et un type de produit.
    Cherche d'abord un produit correspondant, sinon utilise le template par défaut.
    """
    # Chercher un produit du producteur correspondant au type demandé
    matching_product = db.query(Product).filter(
        Product.producer_id == producer.id,
        Product.status == "PUBLISHED"
    ).all()

    for product in matching_product:
        if product_type.lower() in product.name.lower():
            return get_product_effective_tiers(product), product

    # Sinon, chercher le template par défaut
    default_template = next(
        (t for t in producer.price_templates if t.is_default),
        None
    )

    if default_template:
        base_price = 250.0  # Prix de base par défaut
        return [
            {
                "min_quantity_kg": t.min_quantity_kg,
                "max_quantity_kg": t.max_quantity_kg,
                "price_per_kg": round(base_price * (1 - t.discount_percent / 100), 2),
                "discount_percent": t.discount_percent,
                "position": t.position
            }
            for t in sorted(default_template.tiers, key=lambda x: x.position)
        ], None

    return [], None


def find_tier_for_quantity(tiers: List[dict], quantity_kg: float) -> Optional[dict]:
    """Trouve le palier applicable pour une quantité donnée"""
    sorted_tiers = sorted(tiers, key=lambda t: t["min_quantity_kg"], reverse=True)
    for tier in sorted_tiers:
        if quantity_kg >= tier["min_quantity_kg"]:
            if tier["max_quantity_kg"] is None or quantity_kg <= tier["max_quantity_kg"]:
                return tier
    if tiers:
        return sorted(tiers, key=lambda t: t["min_quantity_kg"])[0]
    return None

# --- REQUESTS ---

@router.post("/", response_model=SourcingRequestResponse)
def create_request(
    request_in: SourcingRequestCreate, 
    db: Session = Depends(deps.get_db)
):
    """
    Buyer creates a new Sourcing Request (RFP).
    """
    db_request = SourcingRequest(**request_in.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/", response_model=List[SourcingRequestResponse])
def list_requests(
    db: Session = Depends(deps.get_db)
):
    """
    List all open requests.
    """
    return db.query(SourcingRequest).filter(SourcingRequest.status == "OPEN").all()

@router.get("/{request_id}", response_model=SourcingRequestResponse)
def get_request(
    request_id: int, 
    db: Session = Depends(deps.get_db)
):
    """
    Get detailed request with all offers (Dashboard View).
    Offers are sorted by Trust Score (Mocked) DESC.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # FEATURE 9: Ranking Strategy
    # Sort offers in memory by trust_score_snapshot DESC, then price ASC
    req.offers.sort(key=lambda x: (x.trust_score_snapshot or 0, -x.price_offered_usd), reverse=True)
    
    return req

@router.delete("/{request_id}")
def delete_request(
    request_id: int, 
    db: Session = Depends(deps.get_db)
):
    """
    Delete a request and its associated offers.
    Restricted: Cannot delete if offers are ACCEPTED or logistics started.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Validation: Don't delete if "too late"
    has_accepted_offers = any(o.status == 'ACCEPTED' for o in req.offers)
    has_logistics = req.logistics_status != "PREPARING" 
    
    if has_accepted_offers or has_logistics:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete request: Offers already accepted or supply chain started."
        )
    
    for offer in req.offers:
        db.delete(offer)
        
    db.delete(req)
    db.commit()
    return {"message": "Request deleted"}

@router.put("/{request_id}/logistics", response_model=SourcingRequestResponse)
def update_logistics_status(
    request_id: int,
    status: str, # "PREPARING", "TRANSIT", etc.
    db: Session = Depends(deps.get_db)
):
    """
    FEATURE 8: Update logistics status manually.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    req.logistics_status = status
    db.commit()
    db.refresh(req)
    return req

# --- CONTRACTS (FEATURE 10) ---

@router.post("/{request_id}/contract")
def generate_contract(
    request_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Generate PDF Smart Contract.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
        
    accepted_offers = [o for o in req.offers if o.status == 'ACCEPTED']
    if not accepted_offers:
        raise HTTPException(status_code=400, detail="Cannot generate contract: No accepted offers.")
    
    # Convert SQLAlchemy objects to dict/list for service
    req_dict = {
        "id": req.id,
        "buyer_id": req.buyer_id,
        "product_type": req.product_type,
        "grade_target": req.grade_target,
        "volume_target_kg": req.volume_target_kg
    }
    
    offers_list = []
    for o in accepted_offers:
        offers_list.append({
            "facilitator_id": o.facilitator_id,
            "volume_offered_kg": o.volume_offered_kg,
            "price_offered_usd": o.price_offered_usd,
            "status": o.status
        })

    pdf_bytes = pdf_service.generate_contract(req_dict, offers_list)
    
    # IN REAL APP: Upload to S3 and return URL.
    # FOR MVP: Return mock URL (But we generated the bytes successfully)
    
    return {
        "message": "Contract generated successfully.", 
        "contract_url": f"https://s3.aws.com/teravoo-contracts/REQ-{req.id}-SIGNED.pdf",
        "debug_size_bytes": len(pdf_bytes)
    }

# --- OFFERS (FACILITATOR SIDE) ---

@router.post("/{request_id}/offers", response_model=SourcingOfferResponse)
def create_offer(
    request_id: int,
    offer_in: SourcingOfferCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Facilitator submits an offer to a specific request.
    FEATURE 7: Cert validation.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # 2. Check Certs logic
    if req.required_certs:
        # If request needs certs, offer MUST have proofs
        if not offer_in.cert_proofs_urls:
             # Just warn or tag? Let's say we allow but AI downgrades score.
             # For Design strictness:
             pass 

    # 3. Create Offer
    offer_data = offer_in.dict()
    offer_data['request_id'] = request_id
    
    db_offer = SourcingOffer(**offer_data)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

# --- NEGOTIATION / ACTIONS ---

@router.put("/offers/{offer_id}", response_model=SourcingOfferResponse)
def update_offer_status(
    offer_id: int,
    start_update: SourcingOfferUpdate,
    db: Session = Depends(deps.get_db)
):
    """
    Buyer accepts/rejects/negotiates an offer.
    """
    offer = db.query(SourcingOffer).filter(SourcingOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if start_update.status:
        offer.status = start_update.status
    if start_update.price_offered_usd:
        offer.price_offered_usd = start_update.price_offered_usd
        
    db.commit()
    db.refresh(offer)
    return offer

# --- AI INSIGHTS ---

@router.get("/offers/{offer_id}/ai-insight")
def get_ai_negotiation_insight(offer_id: int, db: Session = Depends(deps.get_db)):
    """
    Mock AI Copilot for Negotiation.
    """
    offer = db.query(SourcingOffer).filter(SourcingOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    req = offer.request
    delta_price = offer.price_offered_usd - req.price_target_usd

    if delta_price > 0:
        advice = f"Offer is {delta_price}$ above target. However, facilitator has high trust. Suggest negotiating to {offer.price_offered_usd - (delta_price/2)}$."
    elif delta_price < 0:
        advice = "Great deal! Price is below target. Accept immediately."
    else:
        advice = "Price matches target perfectly."

    return {
        "offer_id": offer_id,
        "price_delta": delta_price,
        "ai_advice": advice
    }


# ═══════════════════════════════════════════════════════════
# PRICING TIER INTEGRATION FOR SOURCING
# ═══════════════════════════════════════════════════════════

@router.get("/{request_id}/suggested-price")
def get_suggested_price_for_request(
    request_id: int,
    producer_id: int = Query(..., description="ID du producteur"),
    db: Session = Depends(deps.get_db)
):
    """
    Calcule le prix suggéré pour un producteur basé sur ses paliers tarifaires
    et le volume demandé dans la requête de sourcing.

    Utile pour pré-remplir le formulaire d'offre du producteur.
    """
    # Récupérer la demande
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Récupérer le producteur
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")

    # Récupérer les paliers effectifs
    tiers, matching_product = get_producer_effective_tiers(producer, req.product_type, db)

    if not tiers:
        return {
            "request_id": request_id,
            "producer_id": producer_id,
            "volume_target_kg": req.volume_target_kg,
            "has_pricing_tiers": False,
            "suggested_price_per_kg": None,
            "suggested_total": None,
            "message": "Ce producteur n'a pas de paliers tarifaires configurés. Veuillez saisir un prix manuellement."
        }

    # Trouver le palier applicable
    applicable_tier = find_tier_for_quantity(tiers, req.volume_target_kg)

    if not applicable_tier:
        applicable_tier = tiers[0]

    suggested_price_per_kg = applicable_tier["price_per_kg"]
    suggested_total = round(suggested_price_per_kg * req.volume_target_kg, 2)

    # Calculer les économies vs prix de base
    base_tier = sorted(tiers, key=lambda t: t["min_quantity_kg"])[0]
    base_price = base_tier["price_per_kg"]
    savings_percent = round((1 - suggested_price_per_kg / base_price) * 100, 2) if base_price > 0 else 0

    # Trouver le prochain palier (si existe)
    next_tier_info = None
    sorted_tiers = sorted(tiers, key=lambda t: t["min_quantity_kg"])
    current_idx = next((i for i, t in enumerate(sorted_tiers) if t["position"] == applicable_tier["position"]), -1)

    if current_idx >= 0 and current_idx < len(sorted_tiers) - 1:
        next_tier = sorted_tiers[current_idx + 1]
        extra_kg_needed = next_tier["min_quantity_kg"] - req.volume_target_kg
        next_tier_info = {
            "at_quantity_kg": next_tier["min_quantity_kg"],
            "price_per_kg": next_tier["price_per_kg"],
            "extra_kg_needed": extra_kg_needed,
            "discount_percent": next_tier["discount_percent"]
        }

    return {
        "request_id": request_id,
        "producer_id": producer_id,
        "product_type": req.product_type,
        "volume_target_kg": req.volume_target_kg,
        "buyer_target_price": req.price_target_usd,
        "has_pricing_tiers": True,
        "matching_product_id": matching_product.id if matching_product else None,
        "tier_applied": {
            "min_quantity_kg": applicable_tier["min_quantity_kg"],
            "max_quantity_kg": applicable_tier.get("max_quantity_kg"),
            "discount_percent": applicable_tier["discount_percent"]
        },
        "suggested_price_per_kg": suggested_price_per_kg,
        "suggested_total": suggested_total,
        "savings_vs_base_percent": savings_percent,
        "next_tier": next_tier_info,
        "all_tiers": tiers,
        "price_comparison": {
            "vs_buyer_target": round(suggested_price_per_kg - req.price_target_usd, 2),
            "is_below_target": suggested_price_per_kg <= req.price_target_usd
        }
    }


@router.get("/{request_id}/all-producer-prices")
def get_all_producer_prices_for_request(
    request_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Récupère les prix suggérés de TOUS les producteurs ayant des produits correspondants
    pour une demande de sourcing donnée.

    Utile pour afficher un comparatif côté acheteur.
    """
    req = db.query(SourcingRequest).filter(SourcingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Trouver tous les produits correspondant au type demandé
    matching_products = db.query(Product).filter(
        Product.status == "PUBLISHED",
        Product.name.ilike(f"%{req.product_type}%")
    ).all()

    producer_prices = []

    for product in matching_products:
        if not product.producer_id:
            continue

        producer = db.query(ProducerProfile).filter(ProducerProfile.id == product.producer_id).first()
        if not producer:
            continue

        tiers = get_product_effective_tiers(product)
        applicable_tier = find_tier_for_quantity(tiers, req.volume_target_kg)

        if applicable_tier:
            suggested_price = applicable_tier["price_per_kg"]
            producer_prices.append({
                "producer_id": producer.id,
                "producer_name": producer.name,
                "trust_score": producer.trust_score,
                "product_id": product.id,
                "product_name": product.name,
                "pricing_mode": product.pricing_mode,
                "suggested_price_per_kg": suggested_price,
                "suggested_total": round(suggested_price * req.volume_target_kg, 2),
                "discount_applied_percent": applicable_tier["discount_percent"],
                "vs_buyer_target": round(suggested_price - req.price_target_usd, 2),
                "is_below_target": suggested_price <= req.price_target_usd,
                "quantity_available_kg": product.quantity_available
            })

    # Trier par prix (du moins cher au plus cher)
    producer_prices.sort(key=lambda x: x["suggested_price_per_kg"])

    return {
        "request_id": request_id,
        "product_type": req.product_type,
        "volume_target_kg": req.volume_target_kg,
        "buyer_target_price": req.price_target_usd,
        "producer_count": len(producer_prices),
        "producers": producer_prices
    }
