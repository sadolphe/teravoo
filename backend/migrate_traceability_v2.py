from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating traceability_events table...")
        columns = [
            ("request_id", "INTEGER REFERENCES sourcing_requests(id)"),
            ("offer_id", "INTEGER REFERENCES sourcing_offers(id)"),
            ("product_id", "INTEGER REFERENCES product(id)"), # Wait, product NOT products
            ("location_scan", "VARCHAR"),
            ("documents_urls", "JSONB"),
            ("created_by", "VARCHAR")
        ]
        
        for col_name, col_type in columns:
            try:
                conn.execute(text(f"ALTER TABLE traceability_events ADD COLUMN {col_name} {col_type}"))
                print(f"Added column {col_name}")
            except Exception as e:
                print(f"Skipped {col_name}: {e}")
        conn.commit()

if __name__ == "__main__":
    migrate()
