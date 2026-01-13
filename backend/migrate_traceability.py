from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating traceability_events table...")
        # Create products table if not exists (hack for MVP script)
        # Ideally we use ensure_tables.py first
        try:
            conn.execute(text("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY)"))
            print("Ensured products table shell exists")
        except:
             pass

        try:
            conn.execute(text("ALTER TABLE traceability_events ADD COLUMN product_id INTEGER REFERENCES products(id)"))
            print("Added product_id column")
        except Exception as e:
            print(f"Skipped product_id: {e}")
            
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
