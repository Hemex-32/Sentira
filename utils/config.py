import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Trading Thresholds
BUY_THRESHOLD = float(os.getenv("BUY_THRESHOLD", 0.1))
SELL_THRESHOLD = float(os.getenv("SELL_THRESHOLD", -0.1))

# Default Settings
DEFAULT_TICKERS = os.getenv("DEFAULT_TICKERS", "AAPL,MSFT,TSLA").split(",")
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", 30))

# Path for outputs
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
