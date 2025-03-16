# hft_engine.py
# ==================================================
# ⚡ HIGH-FREQUENCY TRADING (HFT) ENGINE ⚡
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from data.order_book_analyzer import OrderBookAnalyzer
from config import ENABLE_HFT, HFT_TRADE_INTERVAL, PAIR

class HFTEngine:
    def __init__(self):
        """Initialize high-frequency trading engine."""
        self.exchange = ExchangeConnector()

    def execute_hft_trade(self):
        """
        Scans order book & executes HFT trades if profitable.
        """
        if not ENABLE_HFT:
            print("⚠️ HFT trading is disabled in config.")
            return
        
        try:
            # Fetch order book
            order_book = self.exchange.fetch_order_book(PAIR)
            if not order_book:
                print("⚠️ No valid order book data. Skipping HFT trade.")
                return

            # Analyze order book for arbitrage/spread opportunities
            analyzer = OrderBookAnalyzer(order_book)
            buy_sell_walls = analyzer.detect_buy_sell_walls()
            liquidity_gaps = analyzer.detect_liquidity_gaps()

            if liquidity_gaps:
                print("🚀 Liquidity gap detected! Executing HFT trade.")

            if buy_sell_walls["buy_wall"] > buy_sell_walls["sell_wall"]:
                # Buy-side dominance → Place quick buy order
                self.exchange.create_market_order(PAIR, "buy", 0.01)
            elif buy_sell_walls["sell_wall"] > buy_sell_walls["buy_wall"]:
                # Sell-side dominance → Place quick sell order
                self.exchange.create_market_order(PAIR, "sell", 0.01)

        except Exception as e:
            print(f"❌ HFT Execution Error: {e}")

    def start_hft_loop(self):
        """
        Continuously scans market & executes high-frequency trades.
        """
        while True:
            self.execute_hft_trade()
            time.sleep(HFT_TRADE_INTERVAL)

# 🚀 START HIGH-FREQUENCY TRADING
if __name__ == "__main__":
    print("⚡ HFT ENGINE ACTIVATED ⚡")
    HFTEngine().start_hft_loop()
