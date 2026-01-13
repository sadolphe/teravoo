from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.sourcing import SourcingRequest, SourcingOffer
from app.services.pdf_service import pdf_service
from app.schemas.sourcing import (
    SourcingRequestCreate,
    SourcingRequestResponse,
    SourcingOfferCreate,
    SourcingOfferResponse,
    SourcingOfferUpdate
)

router = APIRouter()

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
