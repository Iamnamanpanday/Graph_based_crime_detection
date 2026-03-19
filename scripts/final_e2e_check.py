import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_full_patent_flow():
    print("--- Phase 3 Final E2E Check ---")
    
    # 1. Health Check
    try:
        requests.get(f"{BASE_URL}/stats")
        print("✅ Backend reachable")
    except:
        print("❌ Backend NOT reachable")
        return

    # 2. Upload Dummy Data (200 entries simulated)
    # We'll use the existing /upload endpoint
    files = {'file': ('test_200.csv', 'sender_id,receiver_id,amount,timestamp\n' + '\n'.join([f"acc_{i},acc_{i+1},{100+i},2024-03-20 10:00:00" for i in range(199)]))}
    print("Uploading 200 entries...")
    resp = requests.post(f"{BASE_URL}/upload", files=files)
    if resp.status_code == 200:
        print(f"✅ Upload success: {resp.json().get('accounts_analyzed')} accounts analyzed")
    else:
        print(f"❌ Upload failed: {resp.text}")
        return

    # 3. Check Stats
    time.sleep(2) # Give background tasks a moment
    stats = requests.get(f"{BASE_URL}/stats").json()
    print(f"📊 Stats: {stats['analyzed']} analyzed, {stats['suspicious']} suspicious")

    # 4. Check Graph Data (requires auth)
    # Login
    login_form = {'username': 'investigator_admin', 'password': 'secure_pass_2024'}
    login_resp = requests.post(f"{BASE_URL}/auth/login", data=login_form)
    token = login_resp.json()['access_token']
    
    graph = requests.get(f"{BASE_URL}/graph", headers={"Authorization": f"Bearer {token}"}).json()
    print(f"🕸️ Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges detected")
    print("--- E2E Flow Successful ---")

if __name__ == "__main__":
    test_full_patent_flow()
