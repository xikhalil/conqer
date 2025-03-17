# config.py
# ==================================================
# ⚙️ CONFIGURATION SETTINGS ⚙️
# ==================================================

import os
from dotenv import load_dotenv

# Load environment variables securely from the .env file
load_dotenv()

# ✅ Exchange Configuration
EXCHANGE_NAME = "mexc"
API_KEY = os.getenv("mx0vglBLV0QEL0P8ZN")  # Ensure these environment variables exist in your .env file
API_SECRET = os.getenv("e0f23c28c7274bafb4ce46e92b0e7bb9")

# ✅ Trading Pair
PAIR = "PI/USDT"  # Change this as per your trading pair

# ✅ Grid Trading Parameters (Add the BASE_GRID_SIZE here)
BASE_GRID_SIZE = 10  # You can adjust this value based on your desired grid size

# ✅ Trading Features
ENABLE_ARBITRAGE = True
ENABLE_GRID_TRADING = True
ENABLE_HEDGE_TRADING = True
ENABLE_SELF_LEARNING = True
ENABLE_MARKET_ADAPTATION = True
ENABLE_DYNAMIC_GRID = True  # Added ENABLE_DYNAMIC_GRID to match with main.py

# ✅ Backtesting Parameters
BACKTEST_START_DATE = "2023-01-01"
BACKTEST_END_DATE = "2024-01-01"

# ✅ Risk Management
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05  # 5% take profit
RISK_PER_TRADE = 0.02  # 2% of balance per trade
MAX_DRAWDOWN = 0.1  # Maximum acceptable drawdown (10%)

# ✅ Performance Optimization
MAX_SLIPPAGE = 0.001  # 0.1% max slippage
LATENCY_OPTIMIZATION = True
HFT_TRADE_INTERVAL = 1  # High-frequency trading interval (1 sec)

# ✅ AI & RL Model Training
MODEL_PATH = "ai_models/trade_model.h5"
RETRAIN_MODEL_INTERVAL = 500  # Retrain after 500 predictions
RETRAIN_MODEL_THRESHOLD = 75.0  # Retrain model if accuracy is below this threshold (percentage)
RL_BATCH_SIZE = 32

# ✅ Logging & Monitoring
LOG_FILE = "logs/trading.log"
PROFIT_TRACKER_FILE = "logs/profit.json"

# ✅ Order Limits
ORDER_MINIMUM_VALUE = 5  # Minimum order value in USDT
MAX_CONCURRENT_POSITIONS = 5  # Limit concurrent open positions
MAX_QUANTUM_TRADES = 10  # Limit quantum trades to avoid overtrading

# ✅ Simulation Mode (Add if required by your project)
ENABLE_SIMULATION_MODE = False  # Add this if simulation mode is needed

# ✅ Trading Interval Configuration (Added TRADE_INTERVAL here)
TRADE_INTERVAL = 60  # 60 seconds between trades (adjust as needed)
