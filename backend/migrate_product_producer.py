import logging
from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating products table...")
        try:
            # Check if column exists first? 
            # Simple approach: Try add, catch duplicate
            conn.execute(text("ALTER TABLE product ADD COLUMN producer_id INTEGER REFERENCES producer_profiles(id)"))
            print("Added producer_id column to product table")
            conn.commit()
        except Exception as e:
            print(f"Error adding producer_id (might exist or table mismatch): {e}")

if __name__ == "__main__":
    migrate()
