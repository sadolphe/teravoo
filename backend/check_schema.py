"""
Check Product Table Schema on Render
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, inspect
from app.db.session import engine

print("=" * 60)
print("CHECKING PRODUCT TABLE SCHEMA")
print("=" * 60)

with engine.connect() as conn:
    inspector = inspect(engine)
    
    # Get columns
    columns = inspector.get_columns('product')
    
    print("\n📋 Columns in 'product' table:")
    for col in columns:
        print(f"  • {col['name']:30} {str(col['type']):20} {'NULL' if col['nullable'] else 'NOT NULL'}")
    
    print(f"\n✓ Total: {len(columns)} columns")
