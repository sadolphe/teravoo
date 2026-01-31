"""
Update products with REAL vanilla bean photos from verified sources
"""
import os
import sys

backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

from sqlalchemy import text
from app.db.session import engine

def update_vanilla_photos():
    print("=" * 60)
    print("📸 UPDATING WITH REAL VANILLA PHOTOS")
    print("=" * 60)
    
    # REAL vanilla bean photos from public sources
    # Using Pexels and Pixabay (free, no attribution required)
    vanilla_photos = {
        # Pexels vanilla photos
        1: "https://images.pexels.com/photos/4198018/pexels-photo-4198018.jpeg?auto=compress&cs=tinysrgb&w=800",
        2: "https://images.pexels.com/photos/5872362/pexels-photo-5872362.jpeg?auto=compress&cs=tinysrgb&w=800",
        3: "https://images.pexels.com/photos/6157395/pexels-photo-6157395.jpeg?auto=compress&cs=tinysrgb&w=800",
        # Pixabay vanilla photos
        4: "https://cdn.pixabay.com/photo/2017/01/20/15/06/vanilla-1995455_1280.jpg",
        5: "https://cdn.pixabay.com/photo/2016/07/11/19/54/vanilla-1510191_1280.jpg",
        6: "https://cdn.pixabay.com/photo/2018/02/25/07/56/vanilla-3179438_1280.jpg",
        # Additional fallback
        7: "https://images.pexels.com/photos/10626441/pexels-photo-10626441.jpeg?auto=compress&cs=tinysrgb&w=800",
        8: "https://images.pexels.com/photos/4226897/pexels-photo-4226897.jpeg?auto=compress&cs=tinysrgb&w=800",
    }
    
    with engine.connect() as conn:
        print("\n🔄 Updating product photos...")
        
        # Get all products
        result = conn.execute(text("SELECT id, name FROM product ORDER BY id"))
        products = list(result)
        
        for i, (product_id, name) in enumerate(products, 1):
            # Select photo based on product index
            photo_url = vanilla_photos.get(i, vanilla_photos[1])
            
            update_sql = text("""
                UPDATE product 
                SET image_url_raw = :url, image_url_ai = :url
                WHERE id = :id
            """)
            
            conn.execute(update_sql, {"url": photo_url, "id": product_id})
            print(f"  ✓ {name[:40]:40} → Photo {i}")
        
        conn.commit()
        
        print("\n📸 Photos utilisées:")
        for idx, url in vanilla_photos.items():
            print(f"  {idx}. {url}")
        
        print(f"\n✅ Updated {len(products)} products with real vanilla photos!")
    
    print("\n" + "=" * 60)
    print("PHOTOS UPDATED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        update_vanilla_photos()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
