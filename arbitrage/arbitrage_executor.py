# arbitrage_executor.py
# ==================================================
# 💰 ARBITRAGE EXECUTOR – AUTOMATED ARBITRAGE TRADING 💰
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from core.ai_arbitrage_detector import AIArbitrageDetector
from config import ENABLE_ARBITRAGE, ARBITRAGE_MIN_PROFIT

class ArbitrageExecutor:
    def __init__(self):
        """Initialize arbitrage trading system."""
        self.exchange = ExchangeConnector()
        self.arbitrage_detector = AIArbitrageDetector()

    def execute_arbitrage_trade(self):
        """
        Detects arbitrage opportunities & executes trades if profitable.
        """
        if not ENABLE_ARBITRAGE:
            print("⚠️ Arbitrage trading is disabled in config.")
            return

        arbitrage_opportunity = self.arbitrage_detector.find_arbitrage_opportunity()

        if not arbitrage_opportunity:
            print("⏳ No arbitrage opportunities found.")
            return

        exchange_1, exchange_2, asset, buy_price, sell_price = arbitrage_opportunity

        profit_percentage = ((sell_price - buy_price) / buy_price) * 100
        if profit_percentage < ARBITRAGE_MIN_PROFIT:
            print(f"⚠️ Profit too low ({profit_percentage:.2f}%). Skipping trade.")
            return

        print(f"🚀 Arbitrage Detected! Buying {asset} on {exchange_1} at {buy_price}, selling on {exchange_2} at {sell_price}")

        self.exchange.execute_arbitrage_order(exchange_1, exchange_2, asset, buy_price, sell_price)

    def start_arbitrage_loop(self, interval=10):
        """
        Continuously monitors markets & executes arbitrage trades.
        """
        while True:
            self.execute_arbitrage_trade()
            time.sleep(interval)

# 🚀 START ARBITRAGE TRADING
if __name__ == "__main__":
    print("💰 ARBITRAGE ENGINE ACTIVATED 💰")
    ArbitrageExecutor().start_arbitrage_loop()
