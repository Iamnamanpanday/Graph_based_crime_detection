import os
import json
import logging
from web3 import Web3, EthereumTesterProvider
import solcx

# Setup logging to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_deploy():
    try:
        print("Connecting to local in-memory blockchain (eth-tester)...")
        w3 = Web3(EthereumTesterProvider())
        
        solc_version = "0.8.0"
        print(f"Installing/verifying solc compiler {solc_version}...")
        solcx.install_solc(solc_version)
        
        contract_path = "AuditTrail.sol"
        if not os.path.exists(contract_path):
            print(f"Contract file {contract_path} not found.")
            return

        print("Compiling contract...")
        compiled_sol = solcx.compile_files(
            [contract_path],
            output_values=["abi", "bin"],
            solc_version=solc_version
        )
        
        contract_id, contract_interface = compiled_sol.popitem()
        bytecode = contract_interface['bin']
        abi = contract_interface['abi']
        
        # Use the first tester account
        w3.eth.default_account = w3.eth.accounts[0]
        
        print("Deploying contract...")
        AuditTrail = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = AuditTrail.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"Contract auto-deployed for testing at: {tx_receipt.contractAddress}")
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deploy()
