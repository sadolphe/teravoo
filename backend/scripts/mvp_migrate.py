import os
import sys
from sqlalchemy import create_engine, text

# Add parent directory to path to import app modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def migrate():
    print(f"Connecting to database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else '...'}")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        print("Running MVP Migrations...")
        
        # 1. Add quantity_available to product
        try:
            print("Adding quantity_available to product table...")
            conn.execute(text("ALTER TABLE product ADD COLUMN quantity_available INTEGER DEFAULT 500;"))
            print("Done.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        # 2. Add user_id to producer_profiles
        try:
            print("Adding user_id to producer_profiles table...")
            conn.execute(text("ALTER TABLE producer_profiles ADD COLUMN user_id INTEGER;"))
            print("Done.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        conn.commit()
        print("Migration Complete.")

if __name__ == "__main__":
    migrate()
