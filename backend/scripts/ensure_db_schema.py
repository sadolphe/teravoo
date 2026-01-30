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
        from app.models.sourcing import (
            ConnexionRequest, RfqRound, RfqOffer, 
            LogisticService, ShippingQuote, PartnershipInquiry
        )
        
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
        
        # Check orders.quantity_kg
        if table_exists(engine, 'orders'):
            if not column_exists(engine, 'orders', 'quantity_kg'):
                print("  → Adding quantity_kg to orders table...")
                try:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN quantity_kg FLOAT DEFAULT 10.0;"))
                    conn.commit()
                    print("  ✓ Added quantity_kg")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            else:
                print("  ✓ orders.quantity_kg exists")

    
    # 3. Verify critical tables
    print("\n[3/3] Verifying critical tables...")
    critical_tables = [
        'product', 
        'producer_profiles', 
        'orders', 
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
    
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA READY")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        ensure_schema()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        sys.exit(1)
