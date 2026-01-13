import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("GET /api/v1/traceability/product/101")
try:
    response = client.get("/api/v1/traceability/product/101")
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    import traceback
    traceback.print_exc()
