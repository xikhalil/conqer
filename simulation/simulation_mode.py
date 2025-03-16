# simulation_mode.py
# ==================================================
# 🎮 SIMULATION MODE – PAPER TRADING & BACKTESTING 🎮
# ==================================================

import pandas as pd
import logging
from core.exchange_connector import ExchangeConnector
from ai_models.predictive_ai import PredictiveAI
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, PAIR

# ✅ Configure Logging
logging.basicConfig(
    filename="logs/simulation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class SimulationMode:
    def __init__(self):
        """Initialize simulation mode."""
        self.exchange = ExchangeConnector()
        self.ai_model = PredictiveAI()
        self.balance = {"USDT": 10000, "PI": 0}  # Simulated balance
        self.trade_history = []

    def load_historical_data(self):
        """
        Fetches historical market data for backtesting.
        Returns:
            DataFrame: Market data.
        """
        try:
            df = self.exchange.fetch_historical_data(PAIR, BACKTEST_START_DATE, BACKTEST_END_DATE)
            if df is None or df.empty:
                logging.error("⚠️ No historical data available.")
                return None
            return df
        except Exception as e:
            logging.error(f"❌ Error loading historical data: {e}")
            return None

    def execute_trade(self, trade_type, amount, price):
        """
        Simulates a trade execution.
        Args:
            trade_type (str): "BUY" or "SELL".
            amount (float): Trade size.
            price (float): Trade execution price.
        """
        if trade_type == "BUY":
            cost = amount * price
            if self.balance["USDT"] >= cost:
                self.balance["USDT"] -= cost
                self.balance["PI"] += amount
                self.trade_history.append((trade_type, amount, price))
                print(f"✅ Simulated BUY: {amount:.6f} PI at {price:.2f} USDT")
            else:
                print("⚠️ Not enough USDT for BUY trade.")
        elif trade_type == "SELL":
            if self.balance["PI"] >= amount:
                self.balance["PI"] -= amount
                self.balance["USDT"] += amount * price
                self.trade_history.append((trade_type, amount, price))
                print(f"✅ Simulated SELL: {amount:.6f} PI at {price:.2f} USDT")
            else:
                print("⚠️ Not enough PI for SELL trade.")

    def run_simulation(self):
        """
        Runs a backtest using historical market data.
        """
        df = self.load_historical_data()
        if df is None:
            print("⚠️ No market data available. Simulation aborted.")
            return

        print("🚀 Running Simulation...")
        for _, row in df.iterrows():
            signal = self.ai_model.generate_trade_signal(df)
            if signal == "BUY":
                self.execute_trade("BUY", 0.01, row["close"])
            elif signal == "SELL":
                self.execute_trade("SELL", 0.01, row["close"])

        final_balance = self.balance["USDT"] + (self.balance["PI"] * df.iloc[-1]["close"])
        profit_loss = final_balance - 10000  # Initial balance

        print(f"✅ Simulation Complete! Final Balance: {final_balance:.2f} USDT (PnL: {profit_loss:.2f} USDT)")
        logging.info(f"🏆 Simulation Results: Final Balance = {final_balance:.2f} USDT, PnL = {profit_loss:.2f} USDT")

# 🚀 RUN SIMULATION
if __name__ == "__main__":
    sim = SimulationMode()
    sim.run_simulation()
