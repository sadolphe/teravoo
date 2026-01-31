"""
Direct Database Seed Script for TeraVoo Production
Connects directly to PostgreSQL and inserts realistic data
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.config import settings
from app.db.session import engine

def seed_realistic_data():
    """Seed the database with realistic marketplace data"""
    
    print("=" * 60)
    print("🌱 SEEDING REALISTIC DATA FOR TERAVOO")
    print("=" * 60)
    print(f"\n🎯 Database: {settings.DATABASE_URL[:50]}...")
    
    with engine.connect() as conn:
        
        # ═══════════════════════════════════════════════════════════
        # 1. CHECK PRODUCERS
        # ═══════════════════════════════════════════════════════════
        result = conn.execute(text("SELECT COUNT(*) FROM producer_profiles"))
        producer_count = result.scalar()
        
        if producer_count == 0:
            print("\n⚠️  No producers found. Please run initial_data.py first.")
            return
        
        print(f"\n✓ Found {producer_count} producers")
        
        # Get producer IDs
        result = conn.execute(text("SELECT id FROM producer_profiles LIMIT 3"))
        producer_ids = [row[0] for row in result]
        
        # ═══════════════════════════════════════════════════════════
        # 2. VANILLA PRODUCTS
        # ═══════════════════════════════════════════════════════════
        print("\n[1/3] Creating vanilla products...")
        
        products_sql = """
        INSERT INTO product (
            name, grade, price_fob, quantity_available,
            moisture_content, vanillin_content, status,
            description, producer_id,
            image_url_raw, image_url_ai,
            origin, farmer_name, harvest_date
        ) VALUES 
        -- PREMIUM GRADE A
        ('Premium Bourbon Grade A', 'A', 285.0, 0, 33.0, 2.1, 'PUBLISHED',
         'Premium bourbon vanilla beans. Rich, creamy aroma. Perfect for high-end pastries.', :pid1,
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Organic Madagascar Grade A', 'A', 295.0, 150, 32.5, 2.0, 'PUBLISHED',
         'Certified organic. Sweet, intense flavor profile with floral notes.', :pid1,
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Gourmet Sambava Grade A', 'A', 310.0, 75, 34.0, 2.2, 'PUBLISHED',
         'Rare Sambava origin. Full-bodied with chocolate undertones.', :pid3,
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'Sambava, Madagascar', 'Cooperative C', 'July 2024'),
        
        -- GRADE B
        ('Standard Grade B Extract Quality', 'B', 180.0, 400, 28.0, 1.6, 'PUBLISHED',
         'Perfect for vanilla extract production. Excellent value.', :pid2,
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'Antalaha, Madagascar', 'Cooperative B', 'July 2024'),
        
        ('Mananara Grade B', 'B', 175.0, 320, 27.5, 1.5, 'PUBLISHED',
         'Consistent quality. Ideal for commercial extract manufacturers.', :pid2,
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'Mananara, Madagascar', 'Cooperative B', 'July 2024'),
        
        -- GRADE C
        ('Commercial Grade C', 'C', 120.0, 650, 25.0, 1.2, 'PUBLISHED',
         'Budget-friendly option for industrial use.', :pid3,
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'North Madagascar', 'Cooperative C', 'July 2024'),
        
        -- SPLITS & CUTS
        ('Premium Splits', 'SPLITS', 90.0, 800, 30.0, 1.8, 'PUBLISHED',
         'Split beans from Grade A harvest. Great flavor at reduced price.', :pid1,
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Mixed Cuts & Splits', 'CUTS', 65.0, 1200, 28.0, 1.4, 'PUBLISHED',
         'Perfect for extraction. Maximum value.', :pid2,
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'Antalaha, Madagascar', 'Cooperative B', 'July 2024'),
        
        -- NEW ARRIVAL
        ('New Harvest 2025 Grade A', 'A', 290.0, 500, 35.0, 2.0, 'PUBLISHED',
         '🆕 Fresh harvest! Limited availability. Pre-order now.', :pid3,
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'Sambava, Madagascar', 'Cooperative C', 'January 2025')
        """
        
        try:
            conn.execute(text(products_sql), {
                'pid1': producer_ids[0],
                'pid2': producer_ids[min(1, len(producer_ids)-1)],
                'pid3': producer_ids[min(2, len(producer_ids)-1)]
            })
            conn.commit()
            print("  ✓ Created 9 products")
        except Exception as e:
            print(f"  ✗ Error creating products: {e}")
            conn.rollback()
            return
        
        # ═══════════════════════════════════════════════════════════
        # 3. ORDERS - Various States
        # ═══════════════════════════════════════════════════════════
        print("\n[2/3] Creating orders...")
        
        # COMPLETED/DELIVERED orders
        orders_confirmed_sql = """
        INSERT INTO orders (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
        SELECT 
            id,
            name,
            CASE (random() * 4)::int
                WHEN 0 THEN 'Vanilla Co. France'
                WHEN 1 THEN 'Sweet Extracts USA'
                WHEN 2 THEN 'Gourmet Suppliers UK'
                WHEN 3 THEN 'Premium Foods Japan'
                ELSE 'Artisan Bakery Berlin'
            END,
            (10 + random() * 40)::numeric(10,2),
            price_fob * (10 + random() * 40),
            'CONFIRMED',
            NOW() - (interval '1 day' * (30 + random() * 60)::int)
        FROM product
        WHERE grade IN ('A', 'B')
        ORDER BY random()
        LIMIT 5
        """
        
        # IN TRANSIT orders
        orders_secured_sql = """
        INSERT INTO orders (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
        SELECT 
            id,
            name,
            CASE (random() * 4)::int
                WHEN 0 THEN 'Vanilla Co. France'
                WHEN 1 THEN 'Sweet Extracts USA'
                WHEN 2 THEN 'Gourmet Suppliers UK'
                WHEN 3 THEN 'Premium Foods Japan'
                ELSE 'Artisan Bakery Berlin'
            END,
            (20 + random() * 60)::numeric(10,2),
            price_fob * (20 + random() * 60),
            'SECURED',
            NOW() - (interval '1 day' * (5 + random() * 10)::int)
        FROM product
        WHERE quantity_available > 100
        ORDER BY random()
        LIMIT 3
        """
        
        # PENDING orders
        orders_pending_sql = """
        INSERT INTO orders (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
        SELECT 
            id,
            name,
            CASE (random() * 4)::int
                WHEN 0 THEN 'Vanilla Co. France'
                WHEN 1 THEN 'Sweet Extracts USA'
                WHEN 2 THEN 'Gourmet Suppliers UK'
                WHEN 3 THEN 'Premium Foods Japan'
                ELSE 'Artisan Bakery Berlin'
            END,
            (15 + random() * 45)::numeric(10,2),
            price_fob * (15 + random() * 45),
            'PENDING',
            NOW() - (interval '1 day' * (1 + random() * 2)::int)
        FROM product
        WHERE quantity_available > 50
        ORDER BY random()
        LIMIT 4
        """
        
        try:
            conn.execute(text(orders_confirmed_sql))
            conn.execute(text(orders_secured_sql))
            conn.execute(text(orders_pending_sql))
            conn.commit()
            print("  ✓ Created 12 orders")
            print("    - 5 CONFIRMED (delivered)")
            print("    - 3 SECURED (in transit)")
            print("    - 4 PENDING (awaiting approval)")
        except Exception as e:
            print(f"  ✗ Error creating orders: {e}")
            conn.rollback()
        
        # ═══════════════════════════════════════════════════════════
        # 4. TRACEABILITY EVENTS
        # ═══════════════════════════════════════════════════════════
        print("\n[3/3] Creating traceability events...")
        
        traceability_origin_sql = """
        INSERT INTO traceability_events (product_id, stage, status, description, location_scan, created_by, created_at)
        SELECT 
            id,
            'ORIGIN',
            'VALIDATED',
            'Harvested by ' || farmer_name,
            origin,
            'System',
            NOW() - interval '120 days'
        FROM product
        LIMIT 5
        """
        
        traceability_processing_sql = """
        INSERT INTO traceability_events (product_id, stage, status, description, location_scan, created_by, created_at)
        SELECT 
            id,
            'PROCESSING',
            'VALIDATED',
            'Curing and preparation completed. Quality check passed.',
            'Processing Facility, Sambava',
            'QC Team',
            NOW() - interval '90 days'
        FROM product
        LIMIT 5
        """
        
        traceability_deal_sql = """
        INSERT INTO traceability_events (product_id, stage, status, description, created_by, created_at)
        SELECT 
            id,
            'DEAL',
            'VALIDATED',
            'Offer accepted. Volume: ' || (50 + random() * 100)::int || 'kg',
            'Smart Contract',
            NOW() - (interval '1 day' * (10 + random() * 20)::int)
        FROM product
        WHERE quantity_available < 200
        LIMIT 3
        """
        
        try:
            conn.execute(text(traceability_origin_sql))
            conn.execute(text(traceability_processing_sql))
            conn.execute(text(traceability_deal_sql))
            conn.commit()
            print("  ✓ Created 13+ traceability events")
        except Exception as e:
            print(f"  ✗ Error creating traceability events: {e}")
            conn.rollback()
        
        # ═══════════════════════════════════════════════════════════
        # SUMMARY
        # ═══════════════════════════════════════════════════════════
        
        # Get actual counts
        result = conn.execute(text("SELECT COUNT(*) FROM product"))
        product_count = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM orders"))
        order_count = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM product WHERE quantity_available = 0"))
        sold_out_count = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM product WHERE quantity_available < 200 AND quantity_available > 0"))
        low_stock_count = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM product WHERE quantity_available >= 200"))
        well_stocked_count = result.scalar()
        
        print("\n" + "=" * 60)
        print("✅ REALISTIC DATA SEEDING COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  • {producer_count} Producers")
        print(f"  • {product_count} Products (various grades & availability)")
        print(f"  • {order_count} Orders (various statuses)")
        print(f"\n🎯 Stock Status:")
        print(f"  • {sold_out_count} Sold Out")
        print(f"  • {low_stock_count} Low Stock")
        print(f"  • {well_stocked_count} Well Stocked")
        print("\n✨ Your marketplace is now live with realistic data!\n")

if __name__ == "__main__":
    try:
        seed_realistic_data()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
