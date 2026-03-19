import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
import pandas as pd
import io
import time

from app.main import app
from app.db.session import engine, Base

client = TestClient(app)

def test_full_flow():
    # 0. Ensure DB is clean/ready
    Base.metadata.create_all(bind=engine)
    
    # 1. Health Check
    print("Checking API health...")
    resp = client.get("/health")
    print(f"Health: {resp.json()}")

    # 2. Upload Dataset
    print("\nUploading dataset to trigger persistence and flagging...")
    # Create a small valid CSV in memory
    csv_content = "sender_id,receiver_id,amount,timestamp\nacc_1,acc_2,1000.0,2023-01-01 10:00:00\nacc_2,acc_3,950.0,2023-01-01 11:00:00\nacc_3,acc_1,900.0,2023-01-01 12:00:00"
    file = io.BytesIO(csv_content.encode())
    
    # Note: process_dataset uses background tasks. 
    # TestClient runs background tasks synchronously by default.
    resp = client.post("/upload", files={"file": ("test.csv", file, "text/csv")})
    upload_res = resp.json()
    print(f"Upload Result: {upload_res.get('blockchain_logging', 'error')}")

    # 3. Get Flagged Accounts (Anonymous)
    print("\nFetching flagged accounts (anonymous hash view)...")
    resp = client.get("/investigation/flagged-accounts")
    flagged = resp.json()
    if not flagged:
        print("No accounts flagged yet. (This is expected if scores < 80)")
        # Let's check the DB directly or trust the logic if it ran
        return
    
    target_hash = flagged[0]["account_hash"]
    print(f"Found flagged hash: {target_hash}")

    # 4. Try to Reveal without Login (Should fail)
    print("\nAttempting unauthorized reveal...")
    resp = client.get(f"/investigation/reveal/{target_hash}")
    print(f"Status: {resp.status_code} (Expected 401)")

    # 5. Login as Investigator
    print("\nLogging in as investigator...")
    resp = client.post(
        "/auth/login", 
        data={"username": "investigator_01", "password": "password123"}
    )
    token = resp.json()["access_token"]
    print("Login successful.")

    # 6. Reveal with JWT
    print("\nAttempting authorized reveal...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get(f"/investigation/reveal/{target_hash}", headers=headers)
    print(f"Revealed Data: {resp.json()}")

if __name__ == "__main__":
    test_full_flow()
