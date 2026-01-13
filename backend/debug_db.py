from app.db.session import SessionLocal
# Import base to register all models
import app.db.base
from app.models.product import Product
from sqlalchemy import text

db = SessionLocal()
try:
    print("Querying Products...")
    products = db.query(Product).all()
    print(f"Found {len(products)} products.")
    for p in products:
        print(p.name)
except Exception as e:
    print(f"ERROR: {e}")

print("\n--- Inspecting Table Schema ---")
try:
    # Postgres/SQLite specific check
    result = db.execute(text("PRAGMA table_info(products);")).fetchall()
    for row in result:
        print(row)
except Exception as e:
    print(f"Schema Check Error: {e}")
