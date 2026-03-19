import pandas as pd
import hashlib
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import random

from app.graph_engine.graph_builder import build_graph
from app.pipelines.inference_pipeline import run_inference
from app.services.blockchain_service import blockchain_service
from app.db.session import SessionLocal
from app.models.database_models import Transaction, SuspiciousAccount, AccountMapping, ProcessingHistory

def _log_results(accounts):
    """Logs highly suspicious accounts to blockchain and database."""
    db = SessionLocal()
    try:
        for account in accounts:
            # score is a percentage 0-100
            score = account.get("suspicion_score", 0)
            if score > 0.1: 
                account_id = str(account.get("account_id", ""))
                account_hash = hashlib.sha256(account_id.encode()).hexdigest()
                
                # 1. Log to Blockchain
                blockchain_service.log_flagged_account(account_hash, score / 100.0)
                
                # 2. Log to Database (SuspiciousAccount)
                existing = db.query(SuspiciousAccount).filter_by(account_hash=account_hash).first()
                if not existing:
                    new_flag = SuspiciousAccount(
                        account_hash=account_hash,
                        suspicion_score=score,
                        status="flagged"
                    )
                    db.add(new_flag)
                
                # 3. Secure Mapping Vault (Seed PII if missing)
                mapping = db.query(AccountMapping).filter_by(account_hash=account_hash).first()
                if not mapping:
                    # Generate dummy PII for testing
                    first_names = ["Arjun", "Priya", "Rahul", "Ananya", "Vikram", "Sanya", "Amit", "Neha", "Rohan", "Kavya", "Suresh", "Ishani"]
                    last_names = ["Sharma", "Gupta", "Patel", "Reddy", "Khan", "Iyer", "Das", "Singh", "Malhotra", "Joshi", "Verma", "Nair"]
                    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    
                    new_mapping = AccountMapping(
                        account_hash=account_hash,
                        original_id=account_id,
                        full_name=full_name,
                        email=f"{full_name.lower().replace(' ', '.')}@example-bank.com"
                    )
                    db.add(new_mapping)
        
        db.commit()
    except Exception as e:
        print(f"Error in background logging: {e}")
        db.rollback()
    finally:
        db.close()


def get_graph_data():
    """Generates Nodes and Edges for React Flow visualization."""
    from app.db.session import SessionLocal
    from app.models.database_models import Transaction, SuspiciousAccount
    import hashlib
    import random
    
    db = SessionLocal()
    try:
        # Filter out transactions involving already 'audited' (investigated/dismissed) accounts
        audited_hashes = {s.account_hash for s in db.query(SuspiciousAccount).filter(SuspiciousAccount.status != 'flagged').all()}
        
        txs = db.query(Transaction).filter(
            ~Transaction.sender_id.in_(audited_hashes),
            ~Transaction.receiver_id.in_(audited_hashes)
        ).limit(100).all()
        
        flagged = {a.account_hash for a in db.query(SuspiciousAccount).all()}
        
        
        nodes = {}
        edges = []
        
        for tx in txs:
            # Add Source Node
            s_id_str = str(tx.sender_id)
            s_hash = hashlib.sha256(s_id_str.encode()).hexdigest()
            if s_hash not in nodes:
                nodes[s_hash] = {
                    "id": s_hash,
                    "data": {"label": f"{s_id_str[:6]}...", "isFlagged": s_hash in flagged, "fullId": s_id_str},
                    "type": "custom",
                    "position": {"x": random.randint(0, 800), "y": random.randint(0, 500)}
                }
            
            # Add Target Node
            r_id_str = str(tx.receiver_id)
            r_hash = hashlib.sha256(r_id_str.encode()).hexdigest()
            if r_hash not in nodes:
                nodes[r_hash] = {
                    "id": r_hash,
                    "data": {"label": f"{r_id_str[:6]}...", "isFlagged": r_hash in flagged, "fullId": r_id_str},
                    "type": "custom",
                    "position": {"x": random.randint(0, 800), "y": random.randint(0, 500)}
                }
            
            # Add Edge
            edges.append({
                "id": f"e-{tx.id}",
                "source": s_hash,
                "target": r_hash,
                "animated": True,
                "label": f"${tx.amount}",
                "style": {"stroke": "#FF0000" if s_hash in flagged or r_hash in flagged else "#FFD700", "strokeWidth": 2, "opacity": 0.6}
            })
            
        return {"nodes": list(nodes.values()), "edges": edges}
    finally:
        db.close()


def validate_and_normalize_schema(df):
    """Ensures the dataframe has the required columns and normalizes names (case-insensitive)."""
    mapping = {
        "sender_id": ["sender", "source", "from_account", "sender_id", "from", "source_account", "tx_from"],
        "receiver_id": ["receiver", "destination", "to_account", "receiver_id", "to", "destination_account", "tx_to"],
        "amount": ["value", "amount_usd", "transaction_amount", "amount", "amt", "val", "quantity"],
        "timestamp": ["time", "date", "txn_time", "timestamp", "ts", "datetime", "date_time"]
    }
    
    # Normalize current columns to lowercase for matching
    df.columns = [c.lower().strip() for c in df.columns]
    
    for target, alternates in mapping.items():
        if target not in df.columns:
            for alt in alternates:
                if alt.lower() in df.columns:
                    df = df.rename(columns={alt.lower(): target})
                    break
        
        if target not in df.columns:
            print(f"DEBUG: Mapping failed for {target}. Found columns: {list(df.columns)}")
            raise ValueError(f"Missing required column: {target}. Please ensure your CSV has a column for {target}.")
    
    return df


async def process_dataset(file, background_tasks: BackgroundTasks = None):
    db = SessionLocal()
    import io
    try:
        print(f"DEBUG: Processing file: {file.filename}")
        content = await file.read()
        if not content:
            raise ValueError("File is empty")
            
        print("Reading CSV...")
        df = pd.read_csv(io.BytesIO(content))
        print(f"DEBUG: CSV columns found: {list(df.columns)}")
        
        print("Normalizing schema...")
        df = validate_and_normalize_schema(df)

        print("Normalizing data types...")
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Drop rows with invalid critical data
        initial_count = len(df)
        df = df.dropna(subset=['sender_id', 'receiver_id', 'amount', 'timestamp'])
        if len(df) < initial_count:
            print(f"Warning: Dropped {initial_count - len(df)} rows due to invalid data format.")

        print("Persisting transactions to DB...")
        transactions = []
        for _, row in df.iterrows():
            transactions.append(Transaction(
                sender_id=str(row['sender_id']),
                receiver_id=str(row['receiver_id']),
                amount=float(row['amount']),
                timestamp=row['timestamp']
            ))
        db.bulk_save_objects(transactions)
        db.commit()

        print("Building graph...")
        G = build_graph(df)

        print("Running inference...")
        results = run_inference(df, G)

        print("Sorting results...")
        top_accounts = sorted(
            results,
            key=lambda x: x["suspicion_score"],
            reverse=True
        )[:20]

        # Fire off background task to log highly suspicious accounts
        if background_tasks:
            background_tasks.add_task(_log_results, top_accounts)

        # Log to History
        import json
        history_entry = ProcessingHistory(
            filename=file.filename,
            entries_count=len(results),
            column_mapping=json.dumps(list(df.columns)),
            status="completed"
        )
        db.add(history_entry)
        db.commit()

        return {
            "accounts_analyzed": len(results),
            "suspicious_accounts": top_accounts,
            "blockchain_logging": "initiated" if background_tasks else "skipped"
        }
    except Exception as e:
        import traceback
        print(f"Error processing dataset: {e}")
        traceback.print_exc()
        db.rollback()
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()