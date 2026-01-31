"""
Simplified Seed Script - Matches Render Database Schema
Only uses columns that actually exist on Render
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.db.session import engine

def seed_data():
    print("=" * 60)
    print("🌱 SEEDING REALISTIC DATA (SIMPLIFIED)")
    print("=" * 60)
    
    with engine.connect() as conn:
        
        # Check producers
        result = conn.execute(text("SELECT COUNT(*) FROM producer_profiles"))
        producer_count = result.scalar()
        
        if producer_count == 0:
            print("\n⚠️  No producers found. Run initial_data.py first.")
            return
        
        print(f"\n✓ Found {producer_count} producers")
        
        # Get producer IDs
        result = conn.execute(text("SELECT id FROM producer_profiles LIMIT 3"))
        pids = [row[0] for row in result]
        
        #═══════════════════════════════════════════════════════════
        # 1. PRODUCTS (without grade column)
        #═══════════════════════════════════════════════════════════
        print("\n[1/3] Creating products...")
        
        products_sql = f"""
        INSERT INTO product (
            name, price_fob, quantity_available,
            moisture_content, vanillin_content, status,
            description, producer_id,
            image_url_raw, image_url_ai,
            origin, farmer_name, harvest_date
        ) VALUES 
        ('Premium Bourbon Vanilla A', 285.0, 0, 33.0, 2.1, 'PUBLISHED',
         'Premium bourbon vanilla beans. Rich, creamy aroma. Grade A quality.', {pids[0]},
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Organic Madagascar Vanilla A', 295.0, 150, 32.5, 2.0, 'PUBLISHED',
         'Certified organic. Sweet, intense flavor. Grade A quality.', {pids[0]},
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Gourmet Sambava Vanilla A', 310.0, 75, 34.0, 2.2, 'PUBLISHED',
         'Rare Sambava origin. Full-bodied. Grade A premium.', {pids[min(2, len(pids)-1)]},
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'Sambava, Madagascar', 'Cooperative C', 'July 2024'),
        
        ('Standard Extract Quality B', 180.0, 400, 28.0, 1.6, 'PUBLISHED',
         'Perfect for vanilla extract. Grade B quality.', {pids[min(1, len(pids)-1)]},
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'Antalaha, Madagascar', 'Cooperative B', 'July 2024'),
        
        ('Mananara Vanilla B', 175.0, 320, 27.5, 1.5, 'PUBLISHED',
         'Consistent Grade B quality. Ideal for manufacturers.', {pids[min(1, len(pids)-1)]},
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'Mananara, Madagascar', 'Cooperative B', 'July 2024'),
        
        ('Commercial Grade C', 120.0, 650, 25.0, 1.2, 'PUBLISHED',
         'Budget-friendly Grade C. Industrial use.', {pids[min(2, len(pids)-1)]},
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'https://images.unsplash.com/photo-1605631653535-b16a71b5a2c9?w=800',
         'North Madagascar', 'Cooperative C', 'July 2024'),
        
        ('Premium Splits', 90.0, 800, 30.0, 1.8, 'PUBLISHED',
         'Split beans from A harvest. Great flavor, reduced price.', {pids[0]},
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',
         'SAVA Region, Madagascar', 'Cooperative A', 'July 2024'),
        
        ('Mixed Cuts & Splits', 65.0, 1200, 28.0, 1.4, 'PUBLISHED',
         'Cuts and splits. Perfect for extraction.', {pids[min(1, len(pids)-1)]},
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800',
         'Antalaha, Madagascar', 'Cooperative B', 'July 2024'),
        
        ('New Harvest 2025 Grade A', 290.0, 500, 35.0, 2.0, 'PUBLISHED',
         '🆕 Fresh 2025 harvest! Limited availability.', {pids[min(2, len(pids)-1)]},
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'https://images.unsplash.com/photo-1589985270727-8532bb37384f?w=800',
         'Sambava, Madagascar', 'Cooperative C', 'January 2025')
        """
        
        try:
            conn.execute(text(products_sql))
            conn.commit()
            print("  ✓ Created 9 products")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            conn.rollback()
            return
        
        #═══════════════════════════════════════════════════════════
        # 2. ORDERS
        #═══════════════════════════════════════════════════════════
        print("\n[2/3] Creating orders...")
        
        # Check if orders table exists and has quantity_kg
        try:
            # Determine table name (order or orders)
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_name IN ('order', 'orders')
            """))
            order_table = result.scalar()
            
            if not order_table:
                print("  ⚠️  No orders table found, skipping orders")
            else:
                print(f"  → Using table: {order_table}")
                
                # CONFIRMED orders
                conn.execute(text(f"""
                INSERT INTO {order_table} (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
                SELECT 
                    id, name, 'Vanilla Co. France',
                    (10 + random() * 40)::numeric(10,2),
                    price_fob * (10 + random() * 40),
                    'CONFIRMED',
                    NOW() - (interval '1 day' * 45)
                FROM product
                ORDER BY random() LIMIT 3
                """))
                
                # SECURED orders
                conn.execute(text(f"""
                INSERT INTO {order_table} (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
                SELECT 
                    id, name, 'Sweet Extracts USA',
                    (20 + random() * 40)::numeric(10,2),
                    price_fob * (20 + random() * 40),
                    'SECURED',
                    NOW() - (interval '1 day' * 7)
                FROM product WHERE quantity_available > 100
                ORDER BY random() LIMIT 2
                """))
                
                # PENDING orders
                conn.execute(text(f"""
                INSERT INTO {order_table} (product_id, product_name, buyer_name, quantity_kg, amount, status, created_at)
                SELECT 
                    id, name, 'Gourmet Suppliers UK',
                    (15 + random() * 30)::numeric(10,2),
                    price_fob * (15 + random() * 30),
                    'PENDING',
                    NOW() - (interval '1 day' * 2)
                FROM product WHERE quantity_available > 50
                ORDER BY random() LIMIT 3
                """))
                
                conn.commit()
                print("  ✓ Created 8 orders (3 CONFIRMED, 2 SECURED, 3 PENDING)")
        except Exception as e:
            print(f"  ✗ Error creating orders: {e}")
            conn.rollback()
        
        #═══════════════════════════════════════════════════════════
        # SUMMARY
        #═══════════════════════════════════════════════════════════
        result = conn.execute(text("SELECT COUNT(*) FROM product"))
        product_count = result.scalar()
        
        try:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {order_table if order_table else 'orders'}"))
            order_count = result.scalar()
        except:
            order_count = 0
        
        print("\n" + "=" * 60)
        print("✅ SEEDING COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  • {producer_count} Producers")
        print(f"  • {product_count} Products")
        print(f"  • {order_count} Orders")
        print("\n✨ Your marketplace is now populated!\n")

if __name__ == "__main__":
    try:
        seed_data()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
