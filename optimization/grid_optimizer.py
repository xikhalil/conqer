# grid_optimizer.py
# ==================================================
# 🧠 AI GRID OPTIMIZER – LEARNS FROM PAST TRADES 🧠
# ==================================================

import numpy as np
from core.exchange_connector import ExchangeConnector
from ai_models.predictive_ai import PredictiveAI
from config import PAIR

class GridOptimizer:
    def __init__(self):
        """Initialize AI-powered grid trading optimizer."""
        self.exchange = ExchangeConnector()
        self.ai_model = PredictiveAI()
        self.cached_predictions = None  # Store last AI prediction

    def optimize_grid_parameters(self):
        """
        Uses AI to find the best grid trading settings.
        Returns:
            dict: Optimized grid settings.
        """
        market_data = self.exchange.fetch_market_data(PAIR)
        if market_data is None or market_data.empty:
            print("⚠️ No market data available for optimization.")
            return {"grid_size": 10, "grid_spacing": 0.5}

        # Cache AI predictions to prevent redundant calculations
        if self.cached_predictions is None:
            self.cached_predictions = self.ai_model.generate_trade_signal(market_data)

        volatility = np.std(market_data["close"].pct_change())
        optimized_grid_size = max(5, min(20, int(10 * (1 + volatility))))
        optimized_grid_spacing = max(0.2, min(1.5, 0.5 * (1 + volatility)))

        return {"grid_size": optimized_grid_size, "grid_spacing": optimized_grid_spacing}

    def execute_optimized_grid_trades(self):
        """
        Places optimized grid trades.
        """
        optimized_settings = self.optimize_grid_parameters()
        grid_size, grid_spacing = optimized_settings["grid_size"], optimized_settings["grid_spacing"]
        market_price = self.exchange.fetch_ticker(PAIR)['last']
        grid_levels = [market_price * (1 + (i - grid_size // 2) * grid_spacing / 100) for i in range(grid_size)]

        for price in grid_levels:
            if price < market_price:
                self.exchange.create_limit_buy_order(PAIR, 0.01, price)
            else:
                self.exchange.create_limit_sell_order(PAIR, 0.01, price)

        print(f"✅ AI-Optimized Grid Trading Activated: {grid_size} Levels, {grid_spacing}% Spacing")

# 🚀 START AI-OPTIMIZED GRID TRADING
if __name__ == "__main__":
    grid_bot = GridOptimizer()
    grid_bot.execute_optimized_grid_trades()
