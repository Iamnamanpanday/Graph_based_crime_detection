
import asyncio
import os
import sys
from fastapi import UploadFile
import io

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())

from app.services.pipeline_service import process_dataset, _log_results
from app.db.session import SessionLocal, Base, engine

async def seed():
    print("Initializing Forensic Seed...")
    
    # Optional: Clear existing data first
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    csv_path = "data/test_sets/mule_data_100_entries.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    with open(csv_path, "rb") as f:
        content = f.read()
        
    # Create a mock FastAPI UploadFile
    mock_file = UploadFile(
        file=io.BytesIO(content),
        filename="mule_data_100_entries.csv"
    )
    
    print(f"Ingesting {csv_path} into Neural Engine...")
    result = await process_dataset(mock_file)
    
    print("Forcing Anomaly Logging to Forensic Vault...")
    _log_results(result['suspicious_accounts'])
    
    print(f"Seed Complete: {result['accounts_analyzed']} accounts analyzed and Indian identities logged.")

if __name__ == "__main__":
    asyncio.run(seed())
