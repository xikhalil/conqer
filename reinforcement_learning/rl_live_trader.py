# rl_live_trader.py
# ==================================================
# ⚡ REINFORCEMENT LEARNING LIVE TRADER ⚡
# ==================================================

import numpy as np
import time
from core.exchange_connector import ExchangeConnector
from core.order_manager import OrderManager
from core.risk_management import validate_trade
from rl.rl_trading_agent import RLTradingAgent
from config import PAIR, RL_BATCH_SIZE

# 🔌 Initialize components
exchange = ExchangeConnector()
order_manager = OrderManager()
state_size = 5  # RSI, MACD, signal, momentum, volatility
action_size = 3  # BUY, SELL, HOLD
agent = RLTradingAgent(state_size, action_size)

# ✅ Load trained model if available
agent.load_model()

def get_state(market_data):
    """Extracts relevant state from market data."""
    return np.array([market_data.iloc[-1][["rsi", "macd", "signal", "momentum", "volatility"]]])

def rl_trade():
    """Main RL trading loop."""
    while True:
        try:
            # 📡 Fetch Market Data
            market_data = exchange.fetch_market_data(PAIR)
            if market_data is None or market_data.empty:
                print("⚠️ No valid market data. Skipping cycle.")
                time.sleep(60)
                continue

            if market_data.shape[0] < 30:
                print("⚠️ Not enough historical data for RL decision-making.")
                time.sleep(60)
                continue

            state = get_state(market_data).reshape(1, -1)  
            action = agent.act(state)

            trade_signal = {0: "BUY", 1: "SELL", 2: "HOLD"}[action]

            if trade_signal == "HOLD":
                print("⏳ RL decided to HOLD. No trade this cycle.")
                time.sleep(30)
                continue

            # 🏦 Fetch Account Balance
            balance = exchange.fetch_balance()

            # 🛡️ Validate Trade
            trade_decision = validate_trade(trade_signal, market_data, balance)
            if not trade_decision["valid"]:
                print(f"⚠️ Trade not valid: {trade_decision['reason']}. Skipping...")
                time.sleep(30)
                continue

            # 📈 Execute Trade
            order = order_manager.execute_order(trade_signal, trade_decision)
            if order:
                print(f"✅ RL Trade Executed: {trade_signal} {trade_decision['position_size']} {PAIR}")

                # 🧠 Reinforcement Learning: Store experience
                next_state = get_state(market_data).reshape(1, -1)
                reward = order["filled"] * (1 if trade_signal == "BUY" else -1)
                agent.remember(state, action, reward, next_state, False)

                # 🔄 Train RL Model
                agent.replay(batch_size=RL_BATCH_SIZE)

        except Exception as e:
            print(f"❌ RL Trading Error: {e}")

        time.sleep(60)

# 🚀 Start RL Live Trading
if __name__ == "__main__":
    print("⚡ RL TRADER ACTIVATED ⚡")
    rl_trade()
