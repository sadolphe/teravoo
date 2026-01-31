from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.producer import ProducerProfile
from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderResponse

router = APIRouter()

@router.get("/")
def list_producers(db: Session = Depends(deps.get_db)):
    """
    List all producers (Public for now).
    """
    return db.query(ProducerProfile).all()

@router.post("/")
def create_producer(
    data: dict, # Simplified for MVP
    db: Session = Depends(deps.get_db)
):
    """
    Onboard a new producer from Mobile.
    """
    # Check if exists
    existing = db.query(ProducerProfile).filter(ProducerProfile.name == data['name']).first()
    if existing:
        return existing
        
    new_producer = ProducerProfile(
        name=data['name'],
        location_region=data.get('location_region'),
        location_district=data.get('location_district'),
        bio=data.get('bio'),
        badges=data.get('badges', [])
    )
    db.add(new_producer)
    db.commit()
    db.refresh(new_producer)
    return new_producer

@router.get("/{producer_id}")
def get_producer(producer_id: int, db: Session = Depends(deps.get_db)):
    """
    Get a single producer profile by ID.
    Used by Mobile app to display profile in drawer.
    """
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

@router.put("/{producer_id}")
def update_producer(
    producer_id: int,
    data: dict,  # Simplified MVP: accept any fields
    db: Session = Depends(deps.get_db)
):
    """
    Update producer profile (name, phone, bio, location, etc.).
    Used by Mobile app's ProfileScreen.
    """
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    
    # Update fields if provided
    if 'name' in data and data['name']:
        producer.name = data['name']
    if 'phone' in data:
        producer.phone = data['phone']
    if 'bio' in data:
        producer.bio = data['bio']
    if 'contact_email' in data:
        producer.contact_email = data['contact_email']
    if 'location_region' in data:
        producer.location_region = data['location_region']
    if 'location_district' in data:
        producer.location_district = data['location_district']
    
    db.commit()
    db.refresh(producer)
    return producer

@router.post("/{producer_id}/photo")
def upload_producer_photo(
    producer_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Upload producer profile photo.
    For MVP: return a mock URL since we don't have file storage setup yet.
    TODO: Integrate with S3 or local static file serving.
    """
    producer = db.query(ProducerProfile).filter(ProducerProfile.id == producer_id).first()
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    
    # MVP Mock: Return a placeholder photo URL
    # In production, this would save the uploaded file and return the real URL
    photo_url = f"https://ui-avatars.com/api/?name={producer.name.replace(' ', '+')}&size=200&background=4CAF50&color=fff"
    
    return {"photo_url": photo_url, "message": "Photo uploaded successfully (mock for MVP)"}

@router.get("/me/sales")
def get_my_sales(db: Session = Depends(deps.get_db)):
    """
    Get sales for the authenticated producer.
    For MVP: We'll fetch orders linked to products owned by the *first* producer found
    (since we don't have real user auth linking yet, or we assume single user demo).
    """
    # DEMO GOD MODE: Return ALL orders in the system for everyone.
    # This ensures that no matter which producer you selected when creating the product,
    # the order appears in the dashboard.
    orders = db.query(Order).order_by(Order.id.desc()).all()
    
    return orders
