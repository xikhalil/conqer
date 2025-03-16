# hedge_trading.py
# ==================================================
# ⚖️ HEDGE TRADING ENGINE – RISK REDUCTION STRATEGY ⚖️
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from core.market_correlation import MarketCorrelation
from core.risk_management import validate_trade
from config import ENABLE_HEDGE_TRADING, PAIR

class HedgeTrading:
    def __init__(self):
        """Initialize hedge trading system."""
        self.exchange = ExchangeConnector()
        self.market_correlation = MarketCorrelation(self.exchange.fetch_multi_asset_data())

    def execute_hedge_trade(self):
        """Analyzes market conditions & executes a hedge trade if needed."""
        if not ENABLE_HEDGE_TRADING:
            print("⚠️ Hedge trading is disabled in config.")
            return

        market_data = self.exchange.fetch_market_data(PAIR)
        balance = self.exchange.fetch_balance()
        if market_data is None or balance is None:
            print("⚠️ No valid market data available, skipping hedge trade.")
            return

        hedge_asset = self.market_correlation.find_best_hedge_asset(PAIR)
        if not hedge_asset:
            print("⚠️ No strong hedge asset found, skipping.")
            return

        trade_signal = "SELL"
        trade_decision = validate_trade(trade_signal, market_data, balance)

        if not trade_decision["valid"]:
            print(f"⚠️ Hedge trade not valid: {trade_decision['reason']}. Skipping...")
            return

        order = self.exchange.create_market_order(hedge_asset, trade_signal.lower(), trade_decision["position_size"])
        if order:
            print(f"✅ Hedge Trade Executed: {trade_signal} {trade_decision['position_size']} {hedge_asset}")

    def start_hedge_loop(self, interval=5):
        """Continuously monitors market & executes hedge trades if needed."""
        while True:
            self.execute_hedge_trade()
            time.sleep(interval)

# 🚀 START HEDGE TRADING
if __name__ == "__main__":
    print("⚖️ HEDGE TRADING ACTIVATED ⚖️")
    HedgeTrading().start_hedge_loop()
