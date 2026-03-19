from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, index=True)
    receiver_id = Column(String, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=func.now())

class SuspiciousAccount(Base):
    __tablename__ = "suspicious_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_hash = Column(String, unique=True, index=True)
    suspicion_score = Column(Float)
    detected_at = Column(DateTime, default=func.now())
    status = Column(String, default="flagged") # flagged, investigated, dismissed

class AccountMapping(Base):
    """
    Secure Mapping Vault: Links hashes back to original IDs and PII.
    Access to this table should be strictly controlled via RBAC.
    """
    __tablename__ = "account_mappings"

    id = Column(Integer, primary_key=True, index=True)
    account_hash = Column(String, unique=True, index=True)
    original_id = Column(String) # e.g., real bank account number
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)

class ProcessingHistory(Base):
    __tablename__ = "processing_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    entries_count = Column(Integer)
    processed_at = Column(DateTime, default=func.now())
    status = Column(String, default="completed")
    column_mapping = Column(String) # JSON string of detected columns
