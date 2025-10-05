import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# exchange API keys
BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET")
BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET")

# exchange testnet API keys
BINANCE_TESTNET_SPOT_API_KEY: str = os.getenv("BINANCE_TESTNET_SPOT_API_KEY")
BINANCE_TESTNET_SPOT_API_SECRET: str = os.getenv("BINANCE_TESTNET_SPOT_API_SECRET")
BINANCE_TESTNET_FUTURE_API_KEY: str = os.getenv("BINANCE_TESTNET_FUTURE_API_KEY")
BINANCE_TESTNET_FUTURE_API_SECRET: str = os.getenv("BINANCE_TESTNET_FUTURE_API_SECRET")
