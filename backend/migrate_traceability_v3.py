from sqlalchemy import text
from app.db.session import engine

def migrate():
    columns = [
        ("request_id", "INTEGER REFERENCES sourcing_requests(id)"),
        ("offer_id", "INTEGER REFERENCES sourcing_offers(id)"),
        ("product_id", "INTEGER REFERENCES product(id)"),
        ("location_scan", "VARCHAR"),
        ("documents_urls", "JSONB"),
        ("created_by", "VARCHAR")
    ]
    
    for col_name, col_type in columns:
        with engine.connect() as conn:
            print(f"Checking column {col_name}...")
            try:
                conn.execute(text(f"ALTER TABLE traceability_events ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added column {col_name}")
            except Exception as e:
                # Likely already exists
                print(f"Skipped {col_name}: {e}")

if __name__ == "__main__":
    migrate()
