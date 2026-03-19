import requests
import time
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

def test_integration():
    print("Step 1: Checking health...")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {resp.status_code}")
        try:
            print(f"Response JSON: {resp.json()}")
        except:
            print(f"Response Text (non-JSON): {resp.text}")
    except Exception as e:
        print(f"Error: Could not connect to API. Is it running? {e}")
        return

    print("\nStep 2: Uploading test dataset...")
    # Use a real file if possible, or create a dummy one
    test_file_path = "valid_test_data.csv"
    if not os.path.exists(test_file_path):
        with open(test_file_path, "w") as f:
            f.write("sender_id,receiver_id,amount,timestamp\n")
            f.write("ACC1,ACC2,500,1620000000\n")
            f.write("ACC2,ACC3,400,1620000010\n")
            f.write("SUSPECT_BOB,ACC1,1000000,1620000020\n")

    with open(test_file_path, "rb") as f:
        files = {"file": (test_file_path, f, "text/csv")}
        resp = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Upload Result: {resp.status_code}")
    try:
        upload_result = resp.json()
    except Exception as e:
        print(f"FAILED: Response is not JSON. Text: {resp.text}")
        return

    print(f"Blockchain Logging Status: {upload_result.get('blockchain_logging')}")
    print("Top Accounts Identified:")
    for acc in upload_result.get("suspicious_accounts", []):
        print(f" - {acc['account_id']}: {acc['suspicion_score']}")

    if upload_result.get('blockchain_logging') == "initiated":
        print("\nStep 3: Waiting for background task...")
        time.sleep(5) # Give it a few seconds to process background tasks
        
        # In our pipeline_service.py, we flag scores > 80.0
        # Let's assume SUSPECT_BOB got flagged (it will because of the volume)
        account_id = "SUSPECT_BOB"
        print(f"Verifying account {account_id} on blockchain...")
        
        resp = requests.get(f"{BASE_URL}/blockchain/verify/{account_id}")
        if resp.status_code == 200:
            print("SUCCESS: Account verify found on-chain!")
            print(resp.json())
        else:
            print(f"FAILED: Could not find account on-chain. Status: {resp.status_code}")
            print(resp.text)
    else:
        print("FAILED: Blockchain logging was not initiated.")

if __name__ == "__main__":
    test_integration()
