import os
import json
import logging
from web3 import Web3, EthereumTesterProvider
from web3.middleware import ExtraDataToPOAMiddleware
from configs.blockchain_config import blockchain_settings

logger = logging.getLogger(__name__)

# Load ABI generated from local compilation
try:
    with open("configs/contract_abi.json", "r") as f:
        CONTRACT_ABI = json.load(f)
except FileNotFoundError:
    logger.warning("configs/contract_abi.json not found. Blockchain logs will fail unless deployed.")
    CONTRACT_ABI = []

class BlockchainService:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        self._initialize_web3()

    def _initialize_web3(self):
        try:
            if not blockchain_settings.WEB3_PROVIDER_URI:
                logger.warning("WEB3_PROVIDER_URI not set. Blockchain logging disabled.")
                return

            if blockchain_settings.WEB3_PROVIDER_URI == "eth-tester":
                logger.info("Connecting to local in-memory blockchain (eth-tester)")
                self.w3 = Web3(EthereumTesterProvider())
                # Auto-deploy contract for eth-tester
                self._compile_and_deploy()
            else:
                self.w3 = Web3(Web3.HTTPProvider(blockchain_settings.WEB3_PROVIDER_URI))
                # Inject middleware for PoA networks (like Polygon or some testnets)
                self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

            if not self.w3.is_connected():
                logger.error("Failed to connect to the Web3 provider.")
                self.w3 = None
                return

            if blockchain_settings.WALLET_PRIVATE_KEY:
                self.account = self.w3.eth.account.from_key(blockchain_settings.WALLET_PRIVATE_KEY)
            
            # If contract is not already set by deploy, try loading from config
            if not self.contract and blockchain_settings.CONTRACT_ADDRESS and blockchain_settings.CONTRACT_ADDRESS != "YOUR_DEPLOYED_CONTRACT_ADDRESS":
                checksum_address = self.w3.to_checksum_address(blockchain_settings.CONTRACT_ADDRESS)
                self.contract = self.w3.eth.contract(address=checksum_address, abi=CONTRACT_ABI)
                logger.info(f"Connected to smart contract at {checksum_address}")

        except Exception as e:
            logger.error(f"Error initializing Web3: {e}")
            self.w3 = None

    def _compile_and_deploy(self):
        """Compiles and deploys the AuditTrail contract locally."""
        try:
            import solcx
            solc_version = "0.8.0"
            solcx.install_solc(solc_version)
            
            contract_path = "AuditTrail.sol"
            if not os.path.exists(contract_path):
                logger.error(f"Contract file {contract_path} not found.")
                return

            compiled_sol = solcx.compile_files(
                [contract_path],
                output_values=["abi", "bin"],
                solc_version=solc_version
            )
            
            contract_id, contract_interface = compiled_sol.popitem()
            bytecode = contract_interface['bin']
            abi = contract_interface['abi']
            
            # Use the first tester account
            self.w3.eth.default_account = self.w3.eth.accounts[0]
            
            AuditTrail = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            tx_hash = AuditTrail.constructor().transact()
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
            logger.info(f"Contract auto-deployed for testing at: {tx_receipt.contractAddress}")
            
            # Update global ABI for retrieval methods
            global CONTRACT_ABI
            CONTRACT_ABI = abi
            
        except Exception as e:
            logger.error(f"Failed to auto-deploy contract: {e}")

    def log_flagged_account(self, account_hash: str, score: float):
        """
        Logs a highly suspicious account to the blockchain.
        """
        if not self.w3 or not self.contract or not self.account:
            logger.warning("Blockchain service not fully initialized. Skipping log_flagged_account.")
            return None

        try:
            # Multiply score by 1000 to store as integer on-chain (e.g., 0.954 -> 954)
            int_score = int(score * 1000)

            # eth-tester allows direct transactions without manual signing/nonce-management
            if blockchain_settings.WEB3_PROVIDER_URI == "eth-tester":
                tx_hash = self.contract.functions.logAccount(account_hash, int_score).transact()
            else:
                # Build manual transaction for live testnets (Alchemy/Infura)
                nonce = self.w3.eth.get_transaction_count(self.account.address)
                tx_params = {
                    'chainId': self.w3.eth.chain_id,
                    'nonce': nonce,
                    'gas': 2000000, 
                    'maxFeePerGas': self.w3.to_wei('100', 'gwei'),
                    'maxPriorityFeePerGas': self.w3.to_wei('2', 'gwei'),
                }

                tx = self.contract.functions.logAccount(account_hash, int_score).build_transaction(tx_params)
                signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=blockchain_settings.WALLET_PRIVATE_KEY)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            logger.info(f"Blockchain log submitted: {self.w3.to_hex(tx_hash)}")
            
            return self.w3.to_hex(tx_hash)

        except Exception as e:
            logger.error(f"Error logging account to blockchain: {e}")
            return None

    def get_account_log(self, account_hash: str):
        """
        Retrieves the audit trail for a specific account hash from the blockchain.
        """
        if not self.w3 or not self.contract:
            logger.warning("Blockchain service not properly initialized.")
            return None

        try:
            result = self.contract.functions.getLog(account_hash).call()
            # result is a tuple: (accountHash, suspicionScore, timestamp)
            if result[1] == 0:
                return None # Not found or score 0
                
            return {
                "accountHash": result[0],
                "suspicionScore": result[1] / 1000.0, # Convert back to float
                "timestamp": result[2]
            }
        except Exception as e:
            logger.error(f"Error fetching account log from blockchain: {e}")
            return None

blockchain_service = BlockchainService()
