from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating users table...")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
            print("Added email column")
        except Exception as e:
            print(f"Skipped email: {e}")
            
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN company_name VARCHAR"))
            print("Added company_name column")
        except Exception as e:
            print(f"Skipped company_name: {e}")

        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN kyb_status VARCHAR DEFAULT 'PENDING'"))
            print("Added kyb_status column")
        except Exception as e:
            print(f"Skipped kyb_status: {e}")
            
        # Make phone_number nullable (SQLite syntax might vary, but for MVP/Postgres ok)
        # SQLAlchemy create_all won't change existing columns easily in script without Alembic
        # For now, we assume we can just leave phone_number as is but we changed model to nullable=True
        # In SQL, making it nullable:
        try:
            conn.execute(text("ALTER TABLE users ALTER COLUMN phone_number DROP NOT NULL"))
            print("Altered phone_number to be nullable")
        except Exception as e:
            print(f"Skipped phone_number alter: {e}")

        print("Migration complete.")

if __name__ == "__main__":
    migrate()
