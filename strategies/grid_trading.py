# grid_trading.py
# ==================================================
# 📊 STATIC GRID TRADING STRATEGY 📊
# ==================================================

from core.exchange_connector import ExchangeConnector
from config import PAIR, GRID_SIZE, GRID_SPACING

class GridTrading:
    def __init__(self):
        """Initializes grid trading strategy."""
        self.exchange = ExchangeConnector()

    def generate_grid_levels(self, base_price):
        """
        Creates grid levels around the current market price.
        Returns:
            list: Grid price levels.
        """
        return [
            base_price * (1 + (i - GRID_SIZE // 2) * GRID_SPACING / 100)
            for i in range(GRID_SIZE)
        ]

    def execute_grid_trades(self):
        """Places buy & sell orders at predefined grid levels."""
        market_price = self.exchange.fetch_ticker(PAIR)['last']
        grid_levels = self.generate_grid_levels(market_price)

        for price in grid_levels:
            if price < market_price:
                self.exchange.create_limit_buy_order(PAIR, 0.01, price)
            else:
                self.exchange.create_limit_sell_order(PAIR, 0.01, price)

        print(f"✅ Grid Trading Activated with {GRID_SIZE} Levels")

# 🚀 START STATIC GRID TRADING
if __name__ == "__main__":
    bot = GridTrading()
    bot.execute_grid_trades()
