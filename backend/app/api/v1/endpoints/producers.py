from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.producer import ProducerProfile
from app.schemas.producer import ProducerResponse, ProducerCreate

router = APIRouter()

@router.get("/", response_model=List[ProducerResponse])
def read_producers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve producers (facilitators/cooperatives).
    """
    producers = db.query(ProducerProfile).offset(skip).limit(limit).all()
    return producers

@router.get("/{producer_id}", response_model=ProducerResponse)
def read_producer(
    producer_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get generic producer profile by ID.
    """
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

@router.post("/", response_model=ProducerResponse)
def create_producer(
    *,
    db: Session = Depends(deps.get_db),
    producer_in: ProducerCreate,
) -> Any:
    """
    Create new producer profile (On-the-fly onboarding).
    """
    # Check if producer with same name exists in same village to avoid dups
    # MVP: Loose check
    existing = db.query(ProducerProfile).filter(
        ProducerProfile.name == producer_in.name,
        ProducerProfile.location_district == producer_in.location_district
    ).first()
    
    if existing:
        return existing # Idempotency for MVP
        
    producer = ProducerProfile(
        name=producer_in.name,
        location_region=producer_in.location_region,
        location_district=producer_in.location_district,
        bio=producer_in.bio,
        badges=producer_in.badges
    )
    db.add(producer)
    db.commit()
    db.refresh(producer)
    return producer
