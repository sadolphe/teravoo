from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.producer import ProducerProfile
from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderResponse

router = APIRouter()

@router.get("/me/sales")
def get_my_sales(db: Session = Depends(deps.get_db)):
    """
    Get sales for the authenticated producer.
    For MVP: We'll fetch orders linked to products owned by the *first* producer found
    (since we don't have real user auth linking yet, or we assume single user demo).
    """
    # 1. Find the Producer Profile (Mocking 'Me')
    # In real app: producer = db.query(ProducerProfile).filter(ProducerProfile.user_id == current_user.id).first()
    producer = db.query(ProducerProfile).first()
    
    if not producer:
        return []

    # 2. Get Products owned by this Producer
    products = db.query(Product).filter(Product.producer_id == producer.id).all()
    product_ids = [p.id for p in products]
    
    if not product_ids:
        return []

    # 3. Get Orders for these products
    orders = db.query(Order).filter(Order.product_id.in_(product_ids)).order_by(Order.id.desc()).all()
    
    return orders
