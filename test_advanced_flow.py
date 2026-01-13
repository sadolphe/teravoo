import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from fastapi.testclient import TestClient
from backend.main import app
from backend.app.db.session import SessionLocal

# Create client
client = TestClient(app)

def test_full_sourcing_flow():
    print("🚀 Starting ADVANCED Sourcing Module Test Flow...\n")

    # 1. Create Request with Certs (Feature 7)
    print("[1] Creating Request with Cert Requirements...")
    req_payload = {
        "buyer_id": 1,
        "product_type": "Vanilla",
        "volume_target_kg": 1000,
        "price_target_usd": 215.0,
        "grade_target": "B",
        "accepts_partial": True,
        "required_certs": ["Organic"], 
        "specs_json": {"moisture": "25%"}
    }
    r = client.post("/api/v1/requests/", json=req_payload)
    if r.status_code != 200:
        print(f"❌ Failed: {r.text}")
        return
    req_data = r.json()
    req_id = req_data['id']
    print(f"✅ Request Created! ID={req_id}, Certs={req_data['required_certs']}\n")

    # 2. Facilitator A makes an offer (Accepted)
    print("[2] Facilitator A submits Offer (Partial)...")
    offer_payload = {
        "volume_offered_kg": 500.0,
        "price_offered_usd": 215.0,
        "cert_proofs_urls": ["http://proof_bio.pdf"],
        "request_id": req_id,
        "facilitator_id": 101,
        "status": "PENDING"
    }
    r = client.post(f"/api/v1/requests/{req_id}/offers", json=offer_payload)
    offer_id = r.json()['id']
    
    # Buyer Accepts
    client.put(f"/api/v1/requests/offers/{offer_id}", json={"status": "ACCEPTED"})
    print(f"✅ Offer #1 Accepted (500kg).\n")

    # 3. Contract Generation (Feature 10)
    print("[3] Generating Contract PDF...")
    r = client.post(f"/api/v1/requests/{req_id}/contract")
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Contract Generated!")
        print(f"   URL: {data['contract_url']}")
        print(f"   Size: {data['debug_size_bytes']} bytes\n")
    else:
        print(f"❌ Failed to generate contract: {r.text}")

    # 4. Logistics Update (Feature 8)
    print("[4] Updating Logistics Status...")
    r = client.put(f"/api/v1/requests/{req_id}/logistics?status=TRANSIT_TO_PORT")
    if r.status_code == 200:
        print(f"✅ Logistics Status Updated to: {r.json()['logistics_status']}\n")
    else:
        print(f"❌ Failed update logistics: {r.text}")

    print("\n🎉 ADVANCED TEST COMPLETED!")

if __name__ == "__main__":
    test_full_sourcing_flow()
