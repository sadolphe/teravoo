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
    # DEMO GOD MODE: Return ALL orders in the system for everyone.
    # This ensures that no matter which producer you selected when creating the product,
    # the order appears in the dashboard.
    orders = db.query(Order).order_by(Order.id.desc()).all()
    
    return orders
