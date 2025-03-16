# multi_asset_trading.py
# ==================================================
# 🔄 MULTI-ASSET TRADING – TRADE MULTIPLE MARKETS 🔄
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from ai_models.predictive_ai import PredictiveAI
from core.risk_management import validate_trade
from core.order_manager import OrderManager
from core.portfolio_manager import PortfolioManager
from config import TRADING_PAIRS, SCAN_INTERVAL

class MultiAssetTrading:
    def __init__(self):
        """Initialize multi-asset trading system."""
        self.exchange = ExchangeConnector()
        self.order_manager = OrderManager(self.exchange)
        self.portfolio_manager = PortfolioManager(self.exchange)
        self.ai_model = PredictiveAI()

    def trade_assets(self):
        """
        Scans & trades multiple assets based on AI signals.
        """
        for pair in TRADING_PAIRS:
            market_data = self.exchange.fetch_market_data(pair)
            balance = self.exchange.fetch_balance()

            if market_data is None or balance is None:
                print(f"⚠️ No valid market data for {pair}. Skipping.")
                continue

            # 🤖 Generate AI Trading Signal
            trade_signal = self.ai_model.generate_trade_signal(market_data)

            if trade_signal == "HOLD":
                print(f"⏳ No strong signal for {pair}. Holding...")
                continue

            # 🛡️ Validate Trade
            trade_decision = validate_trade(trade_signal, market_data, balance)

            if not trade_decision["valid"]:
                print(f"⚠️ Trade not valid for {pair}: {trade_decision['reason']}. Skipping...")
                continue

            # 🚀 Execute Trade
            order = self.order_manager.execute_order(trade_signal, trade_decision)

            if order:
                print(f"✅ Trade Executed: {trade_signal} {trade_decision['position_size']} {pair}")

    def start_multi_asset_trading(self):
        """
        Continuously scans & trades multiple assets in a loop.
        """
        while True:
            self.trade_assets()
            time.sleep(SCAN_INTERVAL)

# 🚀 START MULTI-ASSET TRADING
if __name__ == "__main__":
    print("🔄 MULTI-ASSET TRADING ACTIVATED 🔄")
    MultiAssetTrading().start_multi_asset_trading()
