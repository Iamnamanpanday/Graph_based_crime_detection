from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.models.database_models import SuspiciousAccount, AccountMapping
from app.core.security import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_investigator(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role != "investigator":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@router.get("/flagged-accounts")
async def get_flagged_accounts(db: Session = Depends(get_db)):
    """Public list of flagged hashes (anonymous)."""
    return db.query(SuspiciousAccount).all()

@router.get("/reveal/{account_hash}")
async def reveal_account_info(
    account_hash: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_investigator)
):
    """
    Secure De-anonymization: Only authenticated investigators can see PII.
    """
    mapping = db.query(AccountMapping).filter_by(account_hash=account_hash).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found for this hash.")
    
    return {
        "account_hash": mapping.account_hash,
        "original_id": mapping.original_id,
        "full_name": mapping.full_name,
        "email": mapping.email,
        "revealed_by": current_user
    }

@router.get("/graph", tags=["Graph"])
async def get_exploration_graph(current_investigator: str = Depends(get_current_investigator)):
    from app.services.pipeline_service import get_graph_data
    return get_graph_data()
