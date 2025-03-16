# triangular_arbitrage.py
# ==================================================
# 🔄 TRIANGULAR ARBITRAGE STRATEGY 🔄
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from config import ENABLE_TRIANGULAR_ARBITRAGE, PAIR

class TriangularArbitrage:
    def __init__(self):
        """Initialize triangular arbitrage system."""
        self.exchange = ExchangeConnector()

    def find_arbitrage_opportunity(self):
        """
        Scans for profitable triangular arbitrage cycles.
        Returns:
            tuple: (asset_1, asset_2, asset_3, profit_percentage) or None
        """
        if not ENABLE_TRIANGULAR_ARBITRAGE:
            print("⚠️ Triangular arbitrage is disabled in config.")
            return None

        market_prices = self.exchange.fetch_market_data()

        # Define possible triangular cycles (USDT → BTC → ETH → USDT)
        pairs = [
            ("BTC/USDT", "ETH/BTC", "ETH/USDT"),
            ("ETH/USDT", "LTC/ETH", "LTC/USDT"),
            ("BNB/USDT", "ETH/BNB", "ETH/USDT")
        ]

        best_opportunity = None
        best_profit = 0

        for pair in pairs:
            try:
                price1 = market_prices[pair[0]]['last']
                price2 = market_prices[pair[1]]['last']
                price3 = market_prices[pair[2]]['last']

                # Calculate final USDT value if 1 USDT starts cycle
                final_usdt = 1 / price1 * price2 * price3
                profit_percentage = (final_usdt - 1) * 100

                if profit_percentage > best_profit:
                    best_opportunity = pair
                    best_profit = profit_percentage

            except KeyError:
                continue

        if best_opportunity and best_profit > 0.2:  # Minimum profit threshold
            return best_opportunity + (best_profit,)

        return None

    def execute_arbitrage_trade(self):
        """
        Executes a triangular arbitrage trade if profitable.
        """
        opportunity = self.find_arbitrage_opportunity()

        if not opportunity:
            print("⏳ No triangular arbitrage opportunities found.")
            return

        asset_1, asset_2, asset_3, profit = opportunity
        print(f"🚀 Executing triangular arbitrage: {asset_1} → {asset_2} → {asset_3} | Profit: {profit:.2f}%")

        self.exchange.create_market_order(asset_1, "buy", 0.01)
        self.exchange.create_market_order(asset_2, "buy", 0.01)
        self.exchange.create_market_order(asset_3, "sell", 0.01)

    def start_triangular_arbitrage_loop(self, interval=10):
        """
        Continuously scans & executes triangular arbitrage trades.
        """
        while True:
            self.execute_arbitrage_trade()
            time.sleep(interval)

# 🚀 START TRIANGULAR ARBITRAGE
if __name__ == "__main__":
    print("🔄 TRIANGULAR ARBITRAGE ACTIVATED 🔄")
    TriangularArbitrage().start_triangular_arbitrage_loop()
