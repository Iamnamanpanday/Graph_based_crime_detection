import sqlite3
import os

db_path = 'mule_detetion.db'
if not os.path.exists(db_path):
    print(f'Database file {db_path} not found.')
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check suspicious_accounts
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suspicious_accounts';")
        if cursor.fetchone():
            cursor.execute("SELECT count(*) FROM suspicious_accounts")
            print(f"Suspicious accounts: {cursor.fetchone()[0]}")
        else:
            print("Table 'suspicious_accounts' does not exist.")
            
        # Check account_mappings
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='account_mappings';")
        if cursor.fetchone():
            cursor.execute("SELECT count(*) FROM account_mappings")
            print(f"Account mappings: {cursor.fetchone()[0]}")
        else:
            print("Table 'account_mappings' does not exist.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
