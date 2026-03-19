import json
import os
import solcx
from web3 import Web3, EthereumTesterProvider
from dotenv import load_dotenv

load_dotenv()

def deploy():
    # 1. Compile the Solidity Contract
    solc_version = "0.8.0"
    print(f"Installing solc compiler {solc_version}...")
    solcx.install_solc(solc_version)

    print("Compiling AuditTrail.sol...")
    compiled_sol = solcx.compile_files(
        ["AuditTrail.sol"],
        output_values=["abi", "bin"],
        solc_version=solc_version
    )

    # Extract ABI and bytecode
    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    # 2. Connect to Provider
    provider_uri = os.getenv("WEB3_PROVIDER_URI", "eth-tester")
    
    if provider_uri == "eth-tester":
        print("Connecting to local in-memory blockchain (eth-tester)...")
        w3 = Web3(EthereumTesterProvider())
    else:
        print(f"Connecting to provider: {provider_uri}")
        w3 = Web3(Web3.HTTPProvider(provider_uri))

    # Wait for connection
    if not w3.is_connected():
        print(f"Error: Could not connect to {provider_uri}")
        return

    # Use the first account
    w3.eth.default_account = w3.eth.accounts[0]
    print(f"Using account: {w3.eth.default_account}")

    # 3. Deploy the Contract
    print("Deploying contract...")
    AuditTrail = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = AuditTrail.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed successfully at address: {contract_address}")

    # 4. Update the .env file
    env_path = ".env"
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    updates = {
        "CONTRACT_ADDRESS": contract_address,
        "WEB3_PROVIDER_URI": provider_uri
    }
    
    new_lines = []
    seen = set()
    for line in lines:
        if "=" in line:
            key = line.split("=")[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                seen.add(key)
                continue
        new_lines.append(line)
    
    for key, value in updates.items():
        if key not in seen:
            new_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)

    print(f".env file updated.")

    # Save the ABI for the app to use
    os.makedirs("configs", exist_ok=True)
    with open("configs/contract_abi.json", "w") as f:
        json.dump(abi, f)
    print("Saved ABI to configs/contract_abi.json")

if __name__ == "__main__":
    deploy()
