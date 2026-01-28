
import requests

BASE_URL = "http://localhost:8000/api/v1"
PHONE_NUMBER = "+261340512345"

def test_login_flow():
    # 1. Request OTP (Mock)
    print(f"1. Requesting OTP for {PHONE_NUMBER}...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={"phone_number": PHONE_NUMBER})
    assert resp.status_code == 200
    print("   OTP Requested.")

    # 2. Verify OTP (Expect Producer ID)
    print("2. Verifying OTP...")
    resp = requests.post(f"{BASE_URL}/auth/verify", json={"phone_number": PHONE_NUMBER, "otp": "1234"})
    
    if resp.status_code != 200:
        print(f"   FAILED: {resp.text}")
        return

    data = resp.json()
    print("   Response:", data)
    
    if "producer_id" in data and data["producer_id"] is not None:
        print(f"   SUCCESS: Received Producer ID: {data['producer_id']}")
    else:
        print("   FAILURE: producer_id missing or null")

if __name__ == "__main__":
    test_login_flow()
