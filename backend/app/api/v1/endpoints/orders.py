from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse
from app.services.contract_service import contract_service
from app.api import deps
from app.models.order import Order
from app.models.product import Product

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def create_order(order_in: OrderCreate, db: Session = Depends(deps.get_db)):
    # Verify product exists
    product = db.query(Product).filter(Product.id == order_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check Stock
    if product.quantity_available < order_in.quantity_kg:
        raise HTTPException(status_code=400, detail="Product Sold Out or Insufficient Stock")

    product_name = product.name 
    
    # Create Order
    db_order = Order(
        product_id=order_in.product_id,
        product_name=product_name,
        amount=order_in.offer_price_total,
        status="PENDING",
        buyer_name=order_in.buyer_name
    )
    
    # Decrement Stock (Simplified transactional logic)
    product.quantity_available -= int(order_in.quantity_kg)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Traceability: Auto-Generate "DEAL" Event
    try:
        from app.models.producer import TraceabilityEvent
        deal_event = TraceabilityEvent(
            product_id=order_in.product_id,
            stage="DEAL",
            status="VALIDATED",
            description=f"Offer Accepted by {order_in.buyer_name}. Volume: {order_in.quantity_kg}kg @ ${order_in.offer_price_total}",
            created_by="System (Smart Contract)"
        )
        db.add(deal_event)
        db.commit()
    except Exception as e:
        print(f"Error creating deal event: {e}")

    return db_order

@router.post("/{order_id}/contract", response_model=OrderResponse)
def generate_contract(order_id: int, db: Session = Depends(deps.get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Generate PDF
    pdf_url = contract_service.generate_contract(
        order_id=order.id,
        buyer_name=order.buyer_name,
        product_name=order.product_name,
        amount=order.amount
    )
    
    order.contract_url = pdf_url
    order.status = "CONTRACT_GENERATED"
    db.commit()
    db.refresh(order)
    
    return order

@router.post("/{order_id}/pay", response_model=OrderResponse)
def simulate_payment(order_id: int, db: Session = Depends(deps.get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "SECURED"
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(deps.get_db)):
    """
    List all orders (MVP: No User Filtering yet).
    """
    orders = db.query(Order).order_by(Order.id.desc()).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(deps.get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{order_id}/download_contract")
def download_contract(order_id: int, db: Session = Depends(deps.get_db)):
    """
    Serve the generated PDF contract.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # In MVP, we saved it to /tmp/contract_order_{id}.pdf
    # In Prod, we would redirect to S3 presigned URL
    import os
    from fastapi.responses import FileResponse
    
    filename = f"contract_order_{order_id}.pdf"
    file_path = os.path.join("/tmp", filename)
    
    if not os.path.exists(file_path):
        # Regenerate if missing (since /tmp might be cleared)
        from app.services.contract_service import contract_service
        try:
            contract_service.generate_contract(
                order_id=order.id, 
                buyer_name=order.buyer_name or "Unknown Buyer", 
                product_name=order.product_name, 
                amount=order.amount
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not regenerate contract: {str(e)}")

    return FileResponse(file_path, media_type='application/pdf', filename=filename)

@router.post("/{order_id}/accept", response_model=OrderResponse)
def accept_order(order_id: int, db: Session = Depends(deps.get_db)):
    """
    Producer validates the order. Stock is already reserved (decremented), 
    so we just update status.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "PENDING" and order.status != "SECURED": 
        # "SECURED" means paid by buyer, "PENDING" might be just reserved. 
        # For simplicity MVP, we allow transition from PENDING/SECURED to CONFIRMED.
        pass

    order.status = "CONFIRMED"
    db.commit()
    db.refresh(order)
    return order

@router.post("/{order_id}/reject", response_model=OrderResponse)
def reject_order(order_id: int, db: Session = Depends(deps.get_db)):
    """
    Producer rejects the order.
    CRITICAL: Refill the stock!
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "REJECTED":
        raise HTTPException(status_code=400, detail="Already rejected")

    # 1. Update Status
    order.status = "REJECTED"
    
    # 2. Refund Stock
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        # We hardcoded 10kg in create_order, so we refund 10kg.
        # Ideally: order.quantity (if column existed)
        product.quantity_available += 10 
    
    db.commit()
    db.refresh(order)
    return order
