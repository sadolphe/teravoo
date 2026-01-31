"""
Reverse Engineering Script - Auto-generate migrations from model differences
Compares SQLAlchemy models with actual Render DB schema and creates missing columns
"""
import os
import sys

# Add backend to path
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

from sqlalchemy import text, inspect
from app.db.session import engine
from app.db.base import Base

def auto_migrate():
    """Automatically detect and add missing columns"""
    
    print("=" * 60)
    print("AUTO-MIGRATION: REVERSE ENGINEERING DB SCHEMA")
    print("=" * 60)
    
    inspector = inspect(engine)
    
    # Get all SQLAlchemy model tables
    model_tables = Base.metadata.tables
    
    print(f"\n📋 Found {len(model_tables)} models to check")
    
    with engine.connect() as conn:
        for table_name, table_obj in model_tables.items():
            
            # Check if table exists in DB
            if not inspector.has_table(table_name):
                print(f"\n⚠️  Table '{table_name}' doesn't exist in DB (will be created by Base.metadata.create_all)")
                continue
            
            print(f"\n🔍 Checking table: {table_name}")
            
            # Get existing columns in DB
            existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
            
            # Get model columns
            model_columns = {col.name: col for col in table_obj.columns}
            
            # Find missing columns
            missing_columns = set(model_columns.keys()) - existing_columns
            
            if not missing_columns:
                print(f"  ✓ All columns exist")
                continue
            
            # Add missing columns
            for col_name in missing_columns:
                col = model_columns[col_name]
                
                # Skip primary key and foreign keys (complex migration)
                if col.primary_key:
                    print(f"  ⊗ Skipping primary key: {col_name}")
                    continue
                
                # Determine column type
                col_type = str(col.type)
                
                # Map SQLAlchemy types to PostgreSQL types
                if 'VARCHAR' in col_type or 'String' in str(col.type.__class__):
                    pg_type = 'VARCHAR'
                elif 'INTEGER' in col_type:
                    pg_type = 'INTEGER'
                elif 'FLOAT' in col_type or 'DOUBLE' in col_type:
                    pg_type = 'DOUBLE PRECISION'
                elif 'BOOLEAN' in col_type:
                    pg_type = 'BOOLEAN'
                elif 'DATETIME' in col_type or 'DateTime' in str(col.type.__class__):
                    pg_type = 'TIMESTAMP'
                else:
                    pg_type = 'VARCHAR'  # Default fallback
                
                # Get default value
                default_clause = ""
                if col.default is not None:
                    default_val = col.default.arg if hasattr(col.default, 'arg') else col.default
                    if isinstance(default_val, str):
                        default_clause = f" DEFAULT '{default_val}'"
                    elif isinstance(default_val, (int, float)):
                        default_clause = f" DEFAULT {default_val}"
                    elif isinstance(default_val, bool):
                        default_clause = f" DEFAULT {str(default_val).upper()}"
                
                # Nullable
                nullable = "" if col.nullable else " NOT NULL"
                
                # Build ALTER TABLE statement
                alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {pg_type}{default_clause}{nullable};"
                
                print(f"  → Adding column: {col_name} ({pg_type})")
                
                try:
                    conn.execute(text(alter_sql))
                    conn.commit()
                    print(f"    ✓ Added {col_name}")
                except Exception as e:
                    print(f"    ✗ Error: {e}")
                    conn.rollback()
    
    print("\n" + "=" * 60)
    print("AUTO-MIGRATION COMPLETE")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        auto_migrate()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
