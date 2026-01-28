import requests

API_URL = "http://localhost:8000/api/v1"

def seed():
    # 1. Get or Create Producer
    print("Checking for existing producers...")
    res = requests.get(f"{API_URL}/producers/")
    producer_id = None
    if res.status_code == 200:
        producers = res.json()
        if producers:
            producer_id = producers[0]['id']
            print(f"Using existing producer ID: {producer_id}")
    
    if not producer_id:
        p_payload = {
            "name": "Test Producer For Pricing",
            "location_region": "Sava",
            "location_district": "Sambava",
            "bio": "Test Bio",
            "badges": []
        }
        print("Creating producer...")
        res = requests.post(f"{API_URL}/producers/", json=p_payload)
        if res.status_code not in [200, 201]:
            print("Failed to create producer", res.text)
            return
        producer_id = res.json()["id"]
        print(f"Producer created: {producer_id}")

    # 2. Create Product (using upload endpoint)
    prod_payload = {
        "name": "Premium Vanilla Beans",
        "price_fob": 250.0,
        "image_url": "https://example.com/item.jpg",
        "description": "High quality beans for testing pricing tiers.",
        "producer_id": producer_id,
        "moq_kg": 5.0,
        "pricing_mode": "SINGLE"
    }
    print("Creating product...")
    res = requests.post(f"{API_URL}/products/upload", json=prod_payload)
    if res.status_code not in [200, 201]:
        print("Failed to create product", res.text)
        return
    product_id = res.json()["id"]
    print(f"Product created: {product_id}")
    
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
