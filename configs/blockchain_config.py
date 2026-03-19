import os
from dotenv import load_dotenv

load_dotenv()

class BlockchainConfig:
    WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
    WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY", "")

blockchain_settings = BlockchainConfig()
