from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.replicate_service import replicate_service
from app.api import deps
from app.models.product import Product

router = APIRouter()

@router.post("/upload", response_model=ProductResponse)
def upload_product(product_in: ProductCreate, db: Session = Depends(deps.get_db)):
    """
    MVP: Recieves product info + raw image URL.
    Triggers AI processing.
    Saves to DB.
    """
    
    # 1. AI Processing
    enhanced_url = replicate_service.enhance_image(product_in.image_url)

    # 2. Save to DB
    # Fetch producer details if provided
    producer_origin = None
    producer_name = None
    
    if product_in.producer_id:
        from app.models.producer import ProducerProfile
        producer = db.query(ProducerProfile).filter(ProducerProfile.id == product_in.producer_id).first()
        if producer:
            producer_origin = f"{producer.location_region}, {producer.location_district}"
            producer_name = producer.name

    db_product = Product(
        name=product_in.name,
        grade=product_in.grade,
        price_fob=product_in.price_fob,
        image_url_raw=product_in.image_url,
        image_url_ai=enhanced_url,
        
        producer_id=product_in.producer_id,
        origin=producer_origin or "Sava Region, Madagascar",
        farmer_name=producer_name or "Unknown Producer",

        status="PUBLISHED", # Auto-publish for MVP
        moisture_content=product_in.moisture_content,
        vanillin_content=product_in.vanillin_content,
        description=product_in.description or "Premium Madagascar Vanilla Beans. Hand-cured and sun-dried."
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # 3. Traceability: Auto-Generate "ORIGIN" Event
    try:
        from app.models.producer import TraceabilityEvent
        origin_event = TraceabilityEvent(
            product_id=db_product.id,
            stage="ORIGIN",
            status="VALIDATED",
            description=f"Initial harvest declaration by {db_product.farmer_name}",
            location_scan=db_product.origin, # Metadata
            created_by="System (On behalf of Facilitator)"
        )
        db.add(origin_event)
        db.commit()
    except Exception as e:
        print(f"Error creating origin event: {e}")
    
    return db_product

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(deps.get_db)):
    """
    MVP: List all products from DB.
    """
    products = db.query(Product).all()
    return products

@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(deps.get_db)):
    """
    Withdraw/Delete a product.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # In a real app we might just set status='WITHDRAWN'
    # For MVP we hard delete to keep list clean
    db.delete(product)
    db.commit()
    
    return product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(deps.get_db)):
    """
    Update product details (Name, Grade, Price, Specs).
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_in.name is not None:
        product.name = product_in.name
    if product_in.grade is not None:
        product.grade = product_in.grade
    if product_in.price_fob is not None:
        product.price_fob = product_in.price_fob
    if product_in.moisture_content is not None:
        product.moisture_content = product_in.moisture_content
    if product_in.vanillin_content is not None:
        product.vanillin_content = product_in.vanillin_content
    if product_in.description is not None:
        product.description = product_in.description
        
    db.commit()
    db.refresh(product)
    
    return product
