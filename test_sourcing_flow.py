import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from fastapi.testclient import TestClient
from backend.main import app
from backend.app.db.session import SessionLocal

# Create client
client = TestClient(app)

def test_sourcing_flow():
    print("🚀 Starting Sourcing Module Test Flow...\n")

    # 1. Create Request
    print("[1] Creating Sourcing Request...")
    req_payload = {
        "buyer_id": 1,
        "product_type": "Vanilla",
        "volume_target_kg": 1000,
        "price_target_usd": 215.0,
        "grade_target": "B",
        "accepts_partial": True,
        "specs_json": {"moisture": "25%"}
    }
    r = client.post("/api/v1/requests/", json=req_payload)
    if r.status_code != 200:
        print(f"❌ Failed: {r.text}")
        return
    req_data = r.json()
    req_id = req_data['id']
    print(f"✅ Request Created! ID={req_id}, Target={req_data['volume_target_kg']}kg\n")

    # 2. Facilitator A makes an offer
    print("[2] Facilitator A submits Offer (Partial)...")
    offer_payload = {
        "volume_offered_kg": 400.0,
        "price_offered_usd": 220.0, # Higher than target
        "photos_json": ["img1.jpg"],
        "request_id": req_id,
        "facilitator_id": 101,
        "status": "PENDING"
    }
    r = client.post(f"/api/v1/requests/{req_id}/offers", json=offer_payload)
    offer_data = r.json()
    offer_id = offer_data['id']
    print(f"✅ Offer Created! ID={offer_id}, Price=${offer_data['price_offered_usd']}\n")

    # 3. Get AI Insight
    print("[3] Asking AI for Negotiation Insight...")
    r = client.get(f"/api/v1/requests/offers/{offer_id}/ai-insight")
    insight = r.json()
    print(f"🤖 AI Advice: {insight['ai_advice']}")
    print(f"   Delta: ${insight['price_delta']}\n")

    # 4. Negotiate (Update Status)
    print("[4] Buyer decides to Negotiate...")
    r = client.put(f"/api/v1/requests/offers/{offer_id}", json={"status": "NEGOTIATING", "price_offered_usd": 218.0})
    updated_offer = r.json()
    print(f"✅ Offer Updated! Status={updated_offer['status']}, New Price=${updated_offer['price_offered_usd']}\n")

    # 5. Check Dashboard View (Aggregation)
    print("[5] Checking Dashboard Aggregation...")
    r = client.get(f"/api/v1/requests/{req_id}")
    dashboard = r.json()
    offers = dashboard['offers']
    print(f"✅ Dashboard Loaded. Total Offers: {len(offers)}")
    print(f"   Offer #1 Status: {offers[0]['status']}")
    
    print("\n🎉 TEST COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test_sourcing_flow()
