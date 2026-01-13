import requests
import json

API_URL = "http://localhost:8000/api/v1"

producers_data = [
    {
        "name": "Sava Gold Collectors",
        "location_region": "Sava, Madagascar",
        "location_district": "Sambava",
        "bio": "Specialized in organic vanilla since 2010. We work with 450 smallholder farmers in the Sambava region.",
        "badges": ["ORGANIC", "FAIRTRADE", "RAINFOREST"],
        "years_experience": 14,
        "transactions_count": 32,
        "trust_score": 4.9
    },
    {
        "name": "Mananara Bio Cooperative",
        "location_region": "Mananara, Madagascar",
        "location_district": "Mananara",
        "bio": "A cooperative of 120 families producing high-quality clove and vanilla. Focused on sustainable agroforestry.",
        "badges": ["ORGANIC"],
        "years_experience": 8,
        "transactions_count": 15,
        "trust_score": 4.6
    },
    {
        "name": "Vohémar Spice Trad",
        "location_region": "Sava, Madagascar",
        "location_district": "Vohémar",
        "bio": "Premium vanilla preparation and export. We guarantee fully traceable lots from farm to FOB.",
        "badges": ["HACCP"],
        "years_experience": 5,
        "transactions_count": 7,
        "trust_score": 4.2
    }
]

def seed_producers():
    print("Seeding Producers...")
    for p in producers_data:
        # We need to map the flat structure to schema if needed, but schema matches close enough
        # Actually Schema is: name, location_region, location_district, bio, badges (defaults)
        # But response has trust_score etc. The CREATE endpoint only takes `ProducerBase` fields by default
        # Wait, my ProducerCreate inherits ProducerBase which has only name, loc, bio, badges.
        # kpi fields are not in ProducerCreate.
        # I need to update the ProducerCreate schema or the endpoint to allow setting KPIs for seeding/mocking.
        # Or I just create them via API (will have default scores) and then maybe I update them manually if I had an update endpoint?
        # For MVP, let's just accept defaults (5.0, 1 yr, 0 sales) OR update the schema to allow seeding stats.
        
        # Let's try sending everything. Pydantic might ignore extra fields if not in schema.
        # I'll update the schema in seed script? No, I can't.
        # I will just create them, they will have default 5.0 score. That's fine for verification.
        
        try:
            res = requests.post(f"{API_URL}/producers/", json=p)
            if res.status_code == 200:
                print(f"Created {p['name']} (ID: {res.json()['id']})")
                # Dirty hack for seeding: Update the trust score via SQL or just accept default. 
                # Since I'm verifying frontend display, getting 5.0 is fine.
            else:
                print(f"Failed to create {p['name']}: {res.text}")
        except Exception as e:
            print(f"Error connecting to API: {e}")

if __name__ == "__main__":
    seed_producers()
