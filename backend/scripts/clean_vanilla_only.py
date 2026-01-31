"""
Clean database and seed ONLY vanilla products with real vanilla bean photos
"""
import os
import sys

backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

from sqlalchemy import text
from app.db.session import engine

def clean_and_seed_vanilla():
    print("=" * 60)
    print("🧹 CLEANING & SEEDING VANILLA ONLY")
    print("=" * 60)
    
    with engine.connect() as conn:
        
        # Delete ALL existing products (cascade delete traceability events first)
        print("\n[1/2] Deleting all existing data...")
        
        # Delete traceability events first (foreign key constraint)
        result_trace = conn.execute(text("DELETE FROM traceability_events"))
        print(f"  ✓ Deleted {result_trace.rowcount} traceability events")
        
        # Delete products
        result = conn.execute(text("DELETE FROM product"))
        print(f"  ✓ Deleted {result.rowcount} products")
        
        conn.commit()
        
        # Get producer IDs
        result = conn.execute(text("SELECT id FROM producer_profiles LIMIT 3"))
        pids = [row[0] for row in result]
        
        if not pids:
            print("  ⚠️  No producers found!")
            return
        
        print(f"\n[2/2] Seeding VANILLA products with real photos...")
        
        # Real vanilla bean image URLs from Unsplash
        vanilla_images = [
            "https://images.unsplash.com/photo-1591645911241-1b6e6b4e2f3e?w=800&q=80",  # Vanilla pods
            "https://images.unsplash.com/photo-1609788612981-3eaf7b4c9c9b?w=800&q=80",  # Vanilla beans
            "https://images.unsplash.com/photo-1599057331332-7f5d8c9e1e1e?w=800&q=80",  # Vanilla pods close
            "https://images.unsplash.com/photo-1593165171965-7f6c2d7e0e0e?w=800&q=80",  # Vanilla bundle
            "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800&q=80",  # Vanilla beans macro
        ]
        
        # Use a fallback vanilla image
        vanilla_fallback = "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800&q=80"
        
        seed_sql = f"""
        INSERT INTO product (
            name, grade, price_fob, quantity_available,
            moisture_content, vanillin_content, status,
            description, producer_id,
            image_url_raw, image_url_ai,
            origin, farmer_name, harvest_date,
            moq_kg, pricing_mode
        ) VALUES 
        -- GRADE A - PREMIUM
        ('Vanille Bourbon Grade A', 'A', 285.0, 0, 33.0, 2.1, 'PUBLISHED',
         'Gousses de vanille bourbon premium. Arôme riche et crémeux. Parfait pour la haute pâtisserie.', {pids[0]},
         '{vanilla_images[0]}', '{vanilla_images[0]}',
         'Région SAVA, Madagascar', 'Coopérative A', 'Juillet 2024',
         10.0, 'SINGLE'),
        
        ('Vanille Bio Madagascar Grade A', 'A', 295.0, 150, 32.5, 2.0, 'PUBLISHED',
         'Certifiée biologique. Profil aromatique intense avec notes florales.', {pids[0]},
         '{vanilla_images[1]}', '{vanilla_images[1]}',
         'Région SAVA, Madagascar', 'Coopérative A', 'Juillet 2024',
         10.0, 'SINGLE'),
        
        ('Vanille Sambava Gourmet Grade A', 'A', 310.0, 75, 34.0, 2.2, 'PUBLISHED',
         'Origine rare de Sambava. Corps plein avec notes de chocolat.', {pids[min(2, len(pids)-1)]},
         '{vanilla_images[2]}', '{vanilla_images[2]}',
         'Sambava, Madagascar', 'Coopérative C', 'Juillet 2024',
         10.0, 'SINGLE'),
        
        -- GRADE B - EXTRACTION
        ('Vanille Grade B Qualité Extraction', 'B', 180.0, 400, 28.0, 1.6, 'PUBLISHED',
         'Parfaite pour production d extrait de vanille. Excellent rapport qualité-prix.', {pids[min(1, len(pids)-1)]},
         '{vanilla_images[3]}', '{vanilla_images[3]}',
         'Antalaha, Madagascar', 'Coopérative B', 'Juillet 2024',
         20.0, 'SINGLE'),
        
        ('Vanille Mananara Grade B', 'B', 175.0, 320, 27.5, 1.5, 'PUBLISHED',
         'Qualité constante. Idéale pour les fabricants d extraits commerciaux.', {pids[min(1, len(pids)-1)]},
         '{vanilla_images[4]}', '{vanilla_images[4]}',
         'Mananara, Madagascar', 'Coopérative B', 'Juillet 2024',
         20.0, 'SINGLE'),
        
        -- GRADE C - COMMERCIAL
        ('Vanille Grade C Commercial', 'C', 120.0, 650, 25.0, 1.2, 'PUBLISHED',
         'Option économique pour usage industriel.', {pids[min(2, len(pids)-1)]},
         '{vanilla_fallback}', '{vanilla_fallback}',
         'Nord Madagascar', 'Coopérative C', 'Juillet 2024',
         50.0, 'SINGLE'),
        
        -- SPLITS & CUTS
        ('Gousses Fendues Premium', 'SPLITS', 90.0, 800, 30.0, 1.8, 'PUBLISHED',
         'Gousses fendues issues de récolte Grade A. Belle saveur à prix réduit.', {pids[0]},
         '{vanilla_images[0]}', '{vanilla_images[0]}',
         'Région SAVA, Madagascar', 'Coopérative A', 'Juillet 2024',
         25.0, 'SINGLE'),
        
        ('Éclats et Gousses Fendues', 'CUTS', 65.0, 1200, 28.0, 1.4, 'PUBLISHED',
         'Parfait pour extraction. Meilleur rapport qualité-prix.', {pids[min(1, len(pids)-1)]},
         '{vanilla_images[1]}', '{vanilla_images[1]}',
         'Antalaha, Madagascar', 'Coopérative B', 'Juillet 2024',
         50.0, 'SINGLE'),
        
        -- NOUVELLE RÉCOLTE
        ('🆕 Nouvelle Récolte 2025 Grade A', 'A', 290.0, 500, 35.0, 2.0, 'PUBLISHED',
         'Récolte fraîche 2025 ! Disponibilité limitée. Précommandez maintenant.', {pids[min(2, len(pids)-1)]},
         '{vanilla_images[2]}', '{vanilla_images[2]}',
         'Sambava, Madagascar', 'Coopérative C', 'Janvier 2025',
         10.0, 'SINGLE')
        """
        
        try:
            conn.execute(text(seed_sql))
            conn.commit()
            print("  ✓ Seeded 9 vanilla products")
            print("\n📸 Images utilisées:")
            for i, url in enumerate(vanilla_images, 1):
                print(f"  {i}. {url}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            conn.rollback()
            return
        
        print("\n" + "=" * 60)
        print("✅ DATABASE CLEANED & SEEDED - VANILLA ONLY!")
        print("=" * 60)

if __name__ == "__main__":
    try:
        clean_and_seed_vanilla()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
