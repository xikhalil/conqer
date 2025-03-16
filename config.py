# config.py
# ==================================================
# ⚙️ CONFIGURATION SETTINGS ⚙️
# ==================================================

import os
from dotenv import load_dotenv

# Load API keys securely
load_dotenv()

# ✅ Exchange Configuration
EXCHANGE_NAME = "mexc"
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# ✅ Trading Pair
PAIR = "PI/USDT"

# ✅ Trading Features
ENABLE_ARBITRAGE = True
ENABLE_GRID_TRADING = True
ENABLE_HEDGE_TRADING = True
ENABLE_SELF_LEARNING = True
ENABLE_MARKET_ADAPTATION = True

# ✅ Backtesting Parameters
BACKTEST_START_DATE = "2023-01-01"
BACKTEST_END_DATE = "2024-01-01"

# ✅ Risk Management
STOP_LOSS = 0.02  # 2% stop loss
TAKE_PROFIT = 0.05  # 5% take profit
RISK_PER_TRADE = 0.02  # 2% of balance per trade

# ✅ Performance Optimization
MAX_SLIPPAGE = 0.001  # 0.1% max slippage
LATENCY_OPTIMIZATION = True
HFT_TRADE_INTERVAL = 1  # High-frequency trading interval (1 sec)

# ✅ AI & RL Model Training
MODEL_PATH = "ai_models/trade_model.h5"
RETRAIN_MODEL_INTERVAL = 500  # Retrain after 500 predictions
RL_BATCH_SIZE = 32

# ✅ Logging & Monitoring
LOG_FILE = "logs/trading.log"
PROFIT_TRACKER_FILE = "logs/profit.json"

# ✅ Order Limits
ORDER_MINIMUM_VALUE = 5  # Minimum order value in USDT
MAX_QUANTUM_TRADES = 10  # Limit quantum trades to avoid overtrading
