"""
Realistic Data Seed Script for TeraVoo Production
Creates a full marketplace scenario with products, orders, and various statuses
"""
import os
import sys
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.producer import ProducerProfile, TraceabilityEvent
from app.models.order import Order
from app.models.pricing import PriceTier, PriceTierTemplate

def seed_realistic_data():
    """Seed the database with realistic marketplace data"""
    db = SessionLocal()
    
    print("=" * 60)
    print("🌱 SEEDING REALISTIC DATA FOR TERAVOO")
    print("=" * 60)
    
    # ═══════════════════════════════════════════════════════════
    # 1. PRODUCERS (Already seeded by initial_data.py)
    # ═══════════════════════════════════════════════════════════
    producers = db.query(ProducerProfile).all()
    if not producers:
        print("⚠️  No producers found. Please run initial_data.py first.")
        return
    
    print(f"\n✓ Found {len(producers)} producers")
    
    # ═══════════════════════════════════════════════════════════
    # 2. VANILLA PRODUCTS - Diverse Quality & Availability
    # ═══════════════════════════════════════════════════════════
    print("\n[1/3] Creating vanilla products...")
    
    products_data = [
        # PREMIUM GRADE A - High demand, some sold out
        {
            "name": "Premium Bourbon Grade A",
            "grade": "A",
            "price_fob": 285.0,
            "quantity_available": 0,  # SOLD OUT
            "moisture_content": 33.0,
            "vanillin_content": 2.1,
            "status": "PUBLISHED",
            "description": "Premium bourbon vanilla beans. Rich, creamy aroma. Perfect for high-end pastries.",
            "producer_id": producers[0].id
        },
        {
            "name": "Organic Madagascar Grade A",
            "grade": "A",
            "price_fob": 295.0,
            "quantity_available": 150,
            "moisture_content": 32.5,
            "vanillin_content": 2.0,
            "status": "PUBLISHED",
            "description": "Certified organic. Sweet, intense flavor profile with floral notes.",
            "producer_id": producers[0].id
        },
        {
            "name": "Gourmet Sambava Grade A",
            "grade": "A",
            "price_fob": 310.0,
            "quantity_available": 75,
            "moisture_content": 34.0,
            "vanillin_content": 2.2,
            "status": "PUBLISHED",
            "description": "Rare Sambava origin. Full-bodied with chocolate undertones.",
            "producer_id": producers[2].id
        },
        
        # GRADE B - Mid-range, good availability
        {
            "name": "Standard Grade B Extract Quality",
            "grade": "B",
            "price_fob": 180.0,
            "quantity_available": 400,
            "moisture_content": 28.0,
            "vanillin_content": 1.6,
            "status": "PUBLISHED",
            "description": "Perfect for vanilla extract production. Excellent value.",
            "producer_id": producers[1].id
        },
        {
            "name": "Mananara Grade B",
            "grade": "B",
            "price_fob": 175.0,
            "quantity_available": 320,
            "moisture_content": 27.5,
            "vanillin_content": 1.5,
            "status": "PUBLISHED",
            "description": "Consistent quality. Ideal for commercial extract manufacturers.",
            "producer_id": producers[1].id
        },
        
        # GRADE C - Budget option, high availability
        {
            "name": "Commercial Grade C",
            "grade": "C",
            "price_fob": 120.0,
            "quantity_available": 650,
            "moisture_content": 25.0,
            "vanillin_content": 1.2,
            "status": "PUBLISHED",
            "description": "Budget-friendly option for industrial use.",
            "producer_id": producers[2].id
        },
        
        # SPLITS & CUTS - Discounted, very available
        {
            "name": "Premium Splits",
            "grade": "SPLITS",
            "price_fob": 90.0,
            "quantity_available": 800,
            "moisture_content": 30.0,
            "vanillin_content": 1.8,
            "status": "PUBLISHED",
            "description": "Split beans from Grade A harvest. Great flavor at reduced price.",
            "producer_id": producers[0].id
        },
        {
            "name": "Mixed Cuts & Splits",
            "grade": "CUTS",
            "price_fob": 65.0,
            "quantity_available": 1200,
            "moisture_content": 28.0,
            "vanillin_content": 1.4,
            "status": "PUBLISHED",
            "description": "Perfect for extraction. Maximum value.",
            "producer_id": producers[1].id
        },
        
        # NEW ARRIVAL - Just published, full stock
        {
            "name": "New Harvest 2025 Grade A",
            "grade": "A",
            "price_fob": 290.0,
            "quantity_available": 500,
            "moisture_content": 35.0,
            "vanillin_content": 2.0,
            "status": "PUBLISHED",
            "description": "🆕 Fresh harvest! Limited availability. Pre-order now.",
            "producer_id": producers[2].id
        }
    ]
    
    created_products = []
    for prod_data in products_data:
        product = Product(
            **prod_data,
            image_url_raw="https://placehold.co/600x400?text=Vanilla+Beans",
            image_url_ai="https://placehold.co/600x400?text=Vanilla+Beans",
            origin=f"{producers[prod_data['producer_id']-1].location_region}, Madagascar",
            farmer_name=producers[prod_data['producer_id']-1].name,
            harvest_date="July 2024" if "2025" not in prod_data["name"] else "January 2025"
        )
        db.add(product)
        created_products.append(product)
    
    db.commit()
    print(f"  ✓ Created {len(created_products)} products")
    
    # ═══════════════════════════════════════════════════════════
    # 3. ORDERS - Various States
    # ═══════════════════════════════════════════════════════════
    print("\n[2/3] Creating orders with various statuses...")
    
    buyer_names = [
        "Vanilla Co. France",
        "Sweet Extracts USA",
        "Gourmet Suppliers UK",
        "Premium Foods Japan",
        "Artisan Bakery Berlin"
    ]
    
    orders_data = []
    
    # COMPLETED/DELIVERED orders (past)
    for i in range(5):
        product = random.choice([p for p in created_products if p.grade in ["A", "B"]])
        qty = random.randint(10, 50)
        orders_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "buyer_name": random.choice(buyer_names),
            "quantity_kg": float(qty),
            "amount": product.price_fob * qty,
            "status": "CONFIRMED",
            "created_at": datetime.utcnow() - timedelta(days=random.randint(30, 90))
        })
    
    # IN TRANSIT orders (recent)
    for i in range(3):
        product = random.choice([p for p in created_products if p.quantity_available > 100])
        qty = random.randint(20, 80)
        orders_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "buyer_name": random.choice(buyer_names),
            "quantity_kg": float(qty),
            "amount": product.price_fob * qty,
            "status": "SECURED",  # Paid, ready to ship
            "created_at": datetime.utcnow() - timedelta(days=random.randint(5, 15))
        })
    
    # PENDING orders (need producer approval)
    for i in range(4):
        product = random.choice([p for p in created_products if p.quantity_available > 50])
        qty = random.randint(15, 60)
        orders_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "buyer_name": random.choice(buyer_names),
            "quantity_kg": float(qty),
            "amount": product.price_fob * qty,
            "status": "PENDING",
            "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 3))
        })
    
    created_orders = []
    for order_data in orders_data:
        order = Order(**order_data)
        db.add(order)
        created_orders.append(order)
    
    db.commit()
    print(f"  ✓ Created {len(created_orders)} orders")
    print(f"    - {len([o for o in orders_data if o['status'] == 'CONFIRMED'])} CONFIRMED (delivered)")
    print(f"    - {len([o for o in orders_data if o['status'] == 'SECURED'])} SECURED (in transit)")
    print(f"    - {len([o for o in orders_data if o['status'] == 'PENDING'])} PENDING (awaiting approval)")
    
    # ═══════════════════════════════════════════════════════════
    # 4. TRACEABILITY EVENTS
    # ═══════════════════════════════════════════════════════════
    print("\n[3/3] Creating traceability events...")
    
    events_created = 0
    for product in created_products[:5]:  # Add events for first 5 products
        # Origin event
        event1 = TraceabilityEvent(
            product_id=product.id,
            stage="ORIGIN",
            status="VALIDATED",
            description=f"Harvested by {product.farmer_name}",
            location_scan=product.origin,
            created_by="System",
            created_at=datetime.utcnow() - timedelta(days=120)
        )
        db.add(event1)
        
        # Processing event
        event2 = TraceabilityEvent(
            product_id=product.id,
            stage="PROCESSING",
            status="VALIDATED",
            description="Curing and preparation completed. Quality check passed.",
            location_scan="Processing Facility, Sambava",
            created_by="QC Team",
            created_at=datetime.utcnow() - timedelta(days=90)
        )
        db.add(event2)
        
        # If sold, add DEAL event
        if product.quantity_available < 200:
            event3 = TraceabilityEvent(
                product_id=product.id,
                stage="DEAL",
                status="VALIDATED",
                description=f"Offer accepted. Volume: {random.randint(50, 150)}kg",
                created_by="Smart Contract",
                created_at=datetime.utcnow() - timedelta(days=random.randint(10, 30))
            )
            db.add(event3)
            events_created += 1
        
        events_created += 2
    
    db.commit()
    print(f"  ✓ Created {events_created} traceability events")
    
    # ═══════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("✅ REALISTIC DATA SEEDING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • {len(producers)} Producers")
    print(f"  • {len(created_products)} Products (various grades & availability)")
    print(f"  • {len(created_orders)} Orders (various statuses)")
    print(f"  • {events_created} Traceability Events")
    print(f"\n🎯 Stock Status:")
    print(f"  • {len([p for p in created_products if p.quantity_available == 0])} Sold Out")
    print(f"  • {len([p for p in created_products if p.quantity_available < 200])} Low Stock")
    print(f"  • {len([p for p in created_products if p.quantity_available >= 200])} Well Stocked")
    print("\n✨ Your marketplace is now live with realistic data!\n")
    
    db.close()

if __name__ == "__main__":
    seed_realistic_data()
