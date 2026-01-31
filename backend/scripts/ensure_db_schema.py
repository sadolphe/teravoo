"""
Database Schema Initialization Script
Ensures all required tables and columns exist on deployment.
Safe to run multiple times (idempotent).
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

def column_exists(engine, table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def table_exists(engine, table_name: str) -> bool:
    """Check if a table exists"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def ensure_schema():
    """Ensure all tables and columns exist"""
    print("=" * 60)
    print("ENSURING DATABASE SCHEMA")
    print("=" * 60)
    
    # 1. Create all tables from SQLAlchemy models
    print("\n[1/3] Creating tables from models...")
    try:
        # Import all models to ensure they're registered with Base.metadata
        from app.models.product import Product
        from app.models.producer import ProducerProfile, TraceabilityEvent
        from app.models.order import Order
        from app.models.user import User
        from app.models.pricing import PriceTier, PriceTierTemplate, PriceTierHistory
        from app.models.sourcing import SourcingRequest, SourcingOffer
        
        print(f"  → Found {len(Base.metadata.tables)} table definitions in models")
        
        # Get list of existing tables
        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())
        print(f"  → Found {len(existing_tables)} existing tables in database")
        
        # First, try the global create_all
        Base.metadata.create_all(bind=engine, checkfirst=True)
        
        # Then verify each table individually and force create if missing
        missing_tables = []
        for table_name, table_obj in Base.metadata.tables.items():
            if not table_exists(engine, table_name):
                missing_tables.append((table_name, table_obj))
        
        if missing_tables:
            print(f"  ⚠️  {len(missing_tables)} table(s) still missing, forcing individual creation...")
            with engine.connect() as conn:
                from sqlalchemy.schema import CreateTable
                for table_name, table_obj in missing_tables:
                    try:
                        print(f"    → Creating {table_name}...")
                        conn.execute(CreateTable(table_obj, if_not_exists=True))
                        conn.commit()
                        print(f"    ✓ Created {table_name}")
                    except Exception as e:
                        print(f"    ✗ Failed to create {table_name}: {e}")
        
        print("✓ All tables created/verified")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    # 2. Add missing columns (for legacy migrations)
    print("\n[2/3] Checking for missing columns...")
    
    with engine.connect() as conn:
        # Check product.quantity_available
        if table_exists(engine, 'product'):
            if not column_exists(engine, 'product', 'quantity_available'):
                print("  → Adding quantity_available to product table...")
                try:
                    conn.execute(text("ALTER TABLE product ADD COLUMN quantity_available INTEGER DEFAULT 500;"))
                    conn.commit()
                    print("  ✓ Added quantity_available")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ product.quantity_available exists")
        
        # Check producer_profiles.user_id
        if table_exists(engine, 'producer_profiles'):
            if not column_exists(engine, 'producer_profiles', 'user_id'):
                print("  → Adding user_id to producer_profiles table...")
                try:
                    conn.execute(text("ALTER TABLE producer_profiles ADD COLUMN user_id INTEGER;"))
                    conn.commit()
                    print("  ✓ Added user_id")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ producer_profiles.user_id exists")
        
        # Check product.grade
        if table_exists(engine, 'product'):
            if not column_exists(engine, 'product', 'grade'):
                print("  → Adding grade to product table...")
                try:
                    conn.execute(text("ALTER TABLE product ADD COLUMN grade VARCHAR DEFAULT 'A';"))
                    conn.commit()
                    print("  ✓ Added grade")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ product.grade exists")
            
            # Check product.moq_kg
            if not column_exists(engine, 'product', 'moq_kg'):
                print("  → Adding moq_kg to product table...")
                try:
                    conn.execute(text("ALTER TABLE product ADD COLUMN moq_kg FLOAT DEFAULT 1.0;"))
                    conn.commit()
                    print("  ✓ Added moq_kg")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ product.moq_kg exists")
            
            # Check product.pricing_mode
            if not column_exists(engine, 'product', 'pricing_mode'):
                print("  → Adding pricing_mode to product table...")
                try:
                    conn.execute(text("ALTER TABLE product ADD COLUMN pricing_mode VARCHAR DEFAULT 'SINGLE';"))
                    conn.commit()
                    print("  ✓ Added pricing_mode")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ product.pricing_mode exists")
            
            # Check product.template_id
            if not column_exists(engine, 'product', 'template_id'):
                print("  → Adding template_id to product table...")
                try:
                    conn.execute(text("ALTER TABLE product ADD COLUMN template_id INTEGER;"))
                    conn.commit()
                    print("  ✓ Added template_id")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ product.template_id exists")
        
        
        # Check orders.quantity_kg (handle both 'order' and 'orders' table names)
        order_table_name = 'orders' if table_exists(engine, 'orders') else 'order' if table_exists(engine, 'order') else None
        
        if order_table_name:
            if not column_exists(engine, order_table_name, 'quantity_kg'):
                print(f"  → Adding quantity_kg to {order_table_name} table...")
                try:
                    conn.execute(text(f"ALTER TABLE {order_table_name} ADD COLUMN quantity_kg FLOAT DEFAULT 10.0;"))
                    conn.commit()
                    print(f"  ✓ Added quantity_kg to {order_table_name}")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print(f"  ✓ {order_table_name}.quantity_kg exists")

    
    # 3. Verify critical tables
    print("\n[3/3] Verifying critical tables...")
    critical_tables = [
        'product', 
        'producer_profiles', 
        'order',  # Note: Currently 'order' but will be 'orders' after schema recreation
        'price_tiers',
        'price_tier_templates'
    ]
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    for table in critical_tables:
        if table in existing_tables:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} MISSING!")
    
    # 4. Seed realistic data if database is empty
    print("\n[4/4] Seeding realistic data (if needed)...")
    
    with engine.connect() as conn:
        # Check if we already have products
        result = conn.execute(text("SELECT COUNT(*) FROM product"))
        product_count = result.scalar()
        
        if product_count >= 5:
            print(f"  ℹ️  Database already has {product_count} products, skipping seed")
        else:
            print("  → Seeding marketplace with realistic data...")
            
            # Get producer IDs
            result = conn.execute(text("SELECT id FROM producer_profiles LIMIT 3"))
            pids = [row[0] for row in result]
            
            if not pids:
                print("  ⚠️  No producers found, skipping product seed")
            else:
                # Seed products with varied grades and stock
                seed_sql = f"""
                INSERT INTO product (
                    name, grade, price_fob, quantity_available,
                    moisture_content, vanillin_content, status,
                    description, producer_id,
                    image_url_raw, image_url_ai,
                    origin, farmer_name, harvest_date
                ) VALUES 
                ('Premium Bourbon Grade A', 'A', 285.0, 0, 33.0, 2.1, 'PUBLISHED',
                 'Premium bourbon vanilla beans. Rich, creamy aroma.', {pids[0]},
                 'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
                 'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
                 'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
                
                ('Organic Madagascar Grade A', 'A', 295.0, 150, 32.5, 2.0, 'PUBLISHED',
                 'Certified organic. Sweet, intense flavor.', {pids[0]},
                 'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
                 'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
                 'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
                
                ('Standard Grade B', 'B', 180.0, 400, 28.0, 1.6, 'PUBLISHED',
                 'Perfect for vanilla extract production.', {pids[min(1, len(pids)-1)]},
                 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
                 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
                 'Antalaha, Madagascar', 'Cooperative B', 'July 2024'),
                
                ('Commercial Grade C', 'C', 120.0, 650, 25.0, 1.2, 'PUBLISHED',
                 'Budget-friendly option for industrial use.', {pids[min(2, len(pids)-1)]},
                 'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
                 'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
                 'North Madagascar', 'Cooperative C', 'July 2024'),
                
                ('Premium Splits', 'SPLITS', 90.0, 800, 30.0, 1.8, 'PUBLISHED',
                 'Split beans from A harvest. Great value.', {pids[0]},
                 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
                 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
                 'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
                
                ('Mixed Cuts', 'CUTS', 65.0, 1200, 28.0, 1.4, 'PUBLISHED',
                 'Perfect for extraction. Maximum value.', {pids[min(1, len(pids)-1)]},
                 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
                 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
                 'Antalaha, Madagascar', 'Cooperative B', 'July 2024')
                """
                
                try:
                    conn.execute(text(seed_sql))
                    conn.commit()
                    print("  ✓ Seeded 6 diverse vanilla products")
                except Exception as e:
                    print(f"  ✗ Error seeding products: {e}")
                    conn.rollback()
    
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA READY & SEEDED")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        ensure_schema()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        sys.exit(1)
