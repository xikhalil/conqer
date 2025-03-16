# backtest_engine.py
# ==================================================
# 📊 BACKTESTING ENGINE – SIMULATES HISTORICAL TRADES 📊
# ==================================================

import pandas as pd
import logging
from core.exchange_connector import ExchangeConnector
from ai_models.predictive_ai import PredictiveAI
from core.risk_management import validate_trade
from config import PAIR, BACKTEST_START_DATE, BACKTEST_END_DATE

# ✅ Configure Logging
logging.basicConfig(
    filename="logs/backtest_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class BacktestEngine:
    def __init__(self):
        """
        Initializes the backtesting system.
        """
        self.exchange = ExchangeConnector()
        self.ai_model = PredictiveAI()
        self.initial_balance = {"USDT": 1000, "PI": 0}  # Simulated balance
        self.trade_history = []

    def fetch_historical_data(self):
        """
        Fetches historical market data for backtesting.
        Returns:
            DataFrame: Market data from the specified date range.
        """
        try:
            df = self.exchange.fetch_market_data(PAIR)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # ✅ Filter Data by Backtest Date Range
            df = df[
                (df["timestamp"] >= pd.to_datetime(BACKTEST_START_DATE))
                & (df["timestamp"] <= pd.to_datetime(BACKTEST_END_DATE))
            ]

            if df.empty:
                logging.error("⚠️ No historical data found for backtesting!")
                return None

            logging.info(f"✅ Historical Data Loaded: {len(df)} candles.")
            return df

        except Exception as e:
            logging.error(f"❌ Error Fetching Historical Data: {e}")
            return None

    def execute_trade(self, trade_signal, market_data):
        """
        Simulates trade execution during backtesting.
        Args:
            trade_signal (str): "BUY" or "SELL".
            market_data (DataFrame): Market data at time of trade.
        """
        trade_decision = validate_trade(trade_signal, market_data, self.initial_balance)
        if not trade_decision["valid"]:
            return None  # Skip invalid trades

        entry_price = trade_decision["entry_price"]
        trade_size = trade_decision["position_size"]

        if trade_signal == "BUY":
            self.initial_balance["PI"] += trade_size
            self.initial_balance["USDT"] -= trade_size * entry_price
        elif trade_signal == "SELL":
            self.initial_balance["PI"] -= trade_size
            self.initial_balance["USDT"] += trade_size * entry_price

        # ✅ Store Trade History
        self.trade_history.append(
            {
                "timestamp": market_data["timestamp"].iloc[-1],
                "signal": trade_signal,
                "entry_price": entry_price,
                "position_size": trade_size,
                "usdt_balance": self.initial_balance["USDT"],
                "pi_balance": self.initial_balance["PI"],
            }
        )

    def run_backtest(self):
        """
        Executes the backtest simulation.
        """
        df = self.fetch_historical_data()
        if df is None:
            print("⚠️ Backtest aborted due to missing data.")
            return

        print("🚀 Running Backtest...")
        for i in range(30, len(df)):
            market_data = df.iloc[:i]  # Use past data up to the current point

            # ✅ AI Prediction
            signal = self.ai_model.generate_trade_signal(market_data)

            if signal != "HOLD":
                self.execute_trade(signal, market_data)

        # ✅ Backtest Summary
        final_balance = self.initial_balance["USDT"] + (
            self.initial_balance["PI"] * df.iloc[-1]["close"]
        )
        profit_loss = final_balance - 1000
        print(f"✅ Backtest Complete! Final Balance: {final_balance:.2f} USDT (PnL: {profit_loss:.2f} USDT)")
        logging.info(
            f"🏆 Backtest Results: Final Balance = {final_balance:.2f} USDT, PnL = {profit_loss:.2f} USDT"
        )

# 🚀 Run Backtest
if __name__ == "__main__":
    backtest = BacktestEngine()
    backtest.run_backtest()
