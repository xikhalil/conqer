# backtester.py
# ==================================================
# ⏳ BACKTESTER – SIMULATES TRADING STRATEGIES ON HISTORICAL DATA ⏳
# ==================================================

import pandas as pd
import numpy as np
import logging
from strategies.grid_trading import GridTrading
from strategies.hedge_trading import HedgeTrading
from ai_models.predictive_ai import PredictiveAI
from config import BACKTEST_START_DATE, BACKTEST_END_DATE, PAIR

# ✅ Configure Logging
logging.basicConfig(
    filename="logs/backtester.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class Backtester:
    def __init__(self, strategy="grid"):
        """
        Initializes the backtesting module.
        Args:
            strategy (str): "grid", "hedge", or "ai".
        """
        self.strategy = strategy
        self.initial_balance = 10000  # Start with 10,000 USDT
        self.balance = self.initial_balance
        self.position = 0
        self.trade_history = []

        # Select strategy
        if strategy == "grid":
            self.strategy_instance = GridTrading()
        elif strategy == "hedge":
            self.strategy_instance = HedgeTrading()
        elif strategy == "ai":
            self.strategy_instance = PredictiveAI()
        else:
            raise ValueError("Invalid strategy. Choose 'grid', 'hedge', or 'ai'.")

    def load_historical_data(self):
        """
        Loads historical market data for backtesting.
        Returns:
            pd.DataFrame: Market data.
        """
        try:
            data = pd.read_csv(f"data/{PAIR}_historical.csv")
            data["timestamp"] = pd.to_datetime(data["timestamp"])
            filtered_data = data[
                (data["timestamp"] >= pd.to_datetime(BACKTEST_START_DATE))
                & (data["timestamp"] <= pd.to_datetime(BACKTEST_END_DATE))
            ]
            
            if filtered_data.empty:
                logging.error("⚠️ No historical data available for backtesting.")
                return None

            return filtered_data
        except Exception as e:
            logging.error(f"❌ Error loading historical data: {e}")
            return None

    def execute_trade(self, trade_type, price):
        """
        Simulates trade execution during backtesting.
        Args:
            trade_type (str): "BUY" or "SELL".
            price (float): Trade execution price.
        """
        trade_size = self.balance * 0.02 / price  # Risk 2% of balance per trade

        if trade_type == "BUY":
            self.position += trade_size
            self.balance -= trade_size * price
        elif trade_type == "SELL" and self.position > 0:
            self.balance += self.position * price
            self.position = 0

        self.trade_history.append((trade_type, price, self.balance))

    def run_backtest(self):
        """
        Runs a backtest using historical market data.
        """
        df = self.load_historical_data()
        if df is None:
            print("⚠️ No historical data available. Backtest aborted.")
            return

        print("🚀 Running Backtest...")
        for i in range(len(df) - 1):
            market_data = df.iloc[: i + 1]
            signal = self.strategy_instance.generate_trade_signal(market_data)

            if signal == "BUY":
                self.execute_trade("BUY", df.iloc[i]["close"])
            elif signal == "SELL":
                self.execute_trade("SELL", df.iloc[i]["close"])

        final_balance = self.balance + (self.position * df.iloc[-1]["close"])
        roi = (final_balance - self.initial_balance) / self.initial_balance * 100

        print(f"✅ Backtest Complete: ROI = {roi:.2f}%")
        logging.info(f"📈 Final ROI: {roi:.2f}%")
        return roi

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    backtester = Backtester(strategy="grid")  # Choose "grid", "hedge", or "ai"
    roi = backtester.run_backtest()
    print(f"📊 Final ROI: {roi:.2f}%")
