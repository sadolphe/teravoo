from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.producer import TraceabilityEvent
from app.schemas.producer import TraceabilityEventResponse, TraceabilityEventCreate

router = APIRouter()

@router.get("/request/{request_id}", response_model=List[TraceabilityEventResponse])
def read_request_traceability(
    request_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get traceability timeline for a specific sourcing request.
    """
    events = db.query(TraceabilityEvent).filter(TraceabilityEvent.request_id == request_id).order_by(TraceabilityEvent.timestamp.asc()).all()
    return events

@router.get("/order/{order_id}", response_model=List[TraceabilityEventResponse])
def read_order_traceability(
    order_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get traceability timeline for a specific order.
    Adhering to model: filtering by offer_id (as offer leads to order).
    """
    # For MVP, we'll assume the client passes the related ID directly or we filter by generic ID
    # Filter by offer_id for now as a proxy for "Order Traceability"
    events = db.query(TraceabilityEvent).filter(TraceabilityEvent.offer_id == order_id).order_by(TraceabilityEvent.timestamp.asc()).all()
    return events

@router.get("/product/{product_id}", response_model=List[TraceabilityEventResponse])
def read_product_traceability(
    product_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get traceability timeline for a specific product (Genesis to Sales).
    """
    events = db.query(TraceabilityEvent).filter(TraceabilityEvent.product_id == product_id).order_by(TraceabilityEvent.timestamp.asc()).all()
    return events

@router.post("/", response_model=TraceabilityEventResponse)
def create_traceability_event(
    event_in: TraceabilityEventCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create a new traceability event (System or Facilitator).
    """
    event = TraceabilityEvent(**event_in.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
