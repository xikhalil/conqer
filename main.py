import time
import threading
import traceback
from core.exchange_connector import ExchangeConnector
from core.order_manager import OrderManager
from core.risk_management import validate_trade
from ai_models.predictive_ai import PredictiveAI
from ai_models.ai_feedback_loop import AIFeedbackLoop
from strategies.dynamic_grid import DynamicGridTrading
from strategies.hedge_trading import HedgeTrading
from utilities.profit_tracker import ProfitTracker
from utilities.utils import Utils
from config import PAIR, TRADE_INTERVAL, ENABLE_HEDGE_TRADING, ENABLE_DYNAMIC_GRID

# 🔌 Initialize Components
exchange = ExchangeConnector()
order_manager = OrderManager(exchange)
ai_model = PredictiveAI()
feedback_loop = AIFeedbackLoop()
profit_tracker = ProfitTracker()

# ✅ Select Trading Strategy
if ENABLE_DYNAMIC_GRID:
    strategy = DynamicGridTrading()
elif ENABLE_HEDGE_TRADING:
    strategy = HedgeTrading()
else:
    strategy = None

# Lock for thread safety
from threading import Lock
trade_lock = Lock()

# 🚀 Trading Loop
def trading_loop():
    trade_count = 0
    while True:
        with trade_lock:  # Ensure thread safety
            try:
                # 📊 Fetch Market Data
                market_data = exchange.fetch_market_data(PAIR)
                if market_data is None or market_data.empty:
                    Utils.log_message(f"⚠️ Market data for {PAIR} is empty or None. Skipping cycle.", "warning")
                    time.sleep(TRADE_INTERVAL)
                    continue

                # 🤖 AI Prediction
                trade_signal = ai_model.generate_trade_signal(market_data)

                if trade_signal == "HOLD":
                    Utils.log_message("⏳ AI decided to HOLD. No trade this cycle.", "info")
                    time.sleep(TRADE_INTERVAL)
                    continue

                # 🏦 Fetch Account Balance
                balance = exchange.fetch_balance()

                # 🛡️ Validate Trade
                trade_decision = validate_trade(trade_signal, market_data, balance)

                if not trade_decision["valid"]:
                    Utils.log_message(f"⚠️ Trade not valid: {trade_decision['reason']}. Skipping...", "warning")
                    time.sleep(TRADE_INTERVAL)
                    continue

                # 📈 Execute Trade
                order = order_manager.execute_order(trade_signal, trade_decision)

                if order:
                    profit_tracker.update_trade("WIN" if order["profit"] > 0 else "LOSS", order["profit"])
                    feedback_loop.update_trade_feedback(trade_signal, market_data, order["profit"])
                    Utils.log_message(f"✅ Trade Executed: {trade_signal} {trade_decision['position_size']} {PAIR}", "info")

                # 🔄 Train AI if Needed
                if trade_count >= 100:
                    feedback_loop.retrain_ai_model()
                    trade_count = 0  # Reset trade count after retraining
                else:
                    trade_count += 1

            except Exception as e:
                Utils.log_message(f"❌ Trading Error: {str(e)}\n{traceback.format_exc()}", "error")

        time.sleep(TRADE_INTERVAL)

# Graceful shutdown
import signal
def graceful_shutdown(signal, frame):
    Utils.log_message("🚨 Bot shutting down...", "info")
    exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)

# 🚀 Start Trading
if __name__ == "__main__":
    Utils.log_message("🚀 Trading Bot Started!", "info")
    
    trade_thread = threading.Thread(target=trading_loop)
    trade_thread.start()
