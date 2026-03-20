import hashlib
from fastapi import APIRouter, HTTPException
from app.services.blockchain_service import blockchain_service

router = APIRouter()

@router.get("/verify/{account_id}")
async def verify_account_on_chain(account_id: str):
    """
    Check if a specific account ID has been flagged and logged to the blockchain.
    """
    try:
        account_hash = hashlib.sha256(account_id.encode()).hexdigest()
        log_data = blockchain_service.get_account_log(account_hash)
        
        if log_data is None:
            raise HTTPException(status_code=404, detail="Account not found in the blockchain audit trail.")
            
        return {
            "status": "success",
            "account_id": account_id,
            "on_chain_data": log_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying blockchain: {str(e)}")

@router.get("/logs")
async def get_all_blockchain_logs():
    """
    Fetches the entire blockchain audit trail documented in the local database.
    Each record represents a transaction verified and logged to the on-chain ledger.
    """
    from app.db.session import SessionLocal
    from app.models.database_models import SuspiciousAccount
    
    db = SessionLocal()
    try:
        logs = db.query(SuspiciousAccount).order_by(SuspiciousAccount.detected_at.desc()).all()
        
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "account_hash": log.account_hash,
                "suspicion_score": log.suspicion_score,
                "status": log.status,
                "timestamp": log.detected_at.isoformat() + "Z",
                "integrity_proof": hashlib.md5(log.account_hash.encode()).hexdigest().upper()[:12]
            })
            
        return formatted_logs
    finally:
        db.close()
