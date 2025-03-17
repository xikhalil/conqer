# dynamic_grid.py
# ==================================================
# 🔄 DYNAMIC GRID TRADING – ADAPTIVE STRATEGY 🔄
# ==================================================

import numpy as np
from core.exchange_connector import ExchangeConnector
from data.volatility_scaling import VolatilityScaling
from config import PAIR, BASE_GRID_SIZE

class DynamicGridTrading:
    def __init__(self):
        """Initializes dynamic grid trading strategy."""
        self.exchange = ExchangeConnector()
        self.base_grid_size = BASE_GRID_SIZE

    def adjust_grid_parameters(self):
        """
        Dynamically adjusts grid spacing based on volatility.
        Returns:
            dict: Adjusted grid parameters.
        """
        try:
            market_data = self.exchange.fetch_market_data(PAIR)
            if market_data is None:
                print("⚠️ Error fetching market data.")
                return {"grid_size": self.base_grid_size, "grid_spacing": 0.5}

            # Calculate volatility using VolatilityScaling
            volatility_scaler = VolatilityScaling()
            volatility = volatility_scaler.calculate_volatility(market_data)

            # Adjust grid size and spacing based on volatility
            grid_size = max(5, min(20, int(self.base_grid_size * (1 + volatility))))
            grid_spacing = max(0.2, min(1.5, 0.5 * (1 + volatility)))

            return {"grid_size": grid_size, "grid_spacing": grid_spacing}
        except Exception as e:
            print(f"⚠️ Error adjusting grid parameters: {e}")
            return {"grid_size": self.base_grid_size, "grid_spacing": 0.5}

    def execute_dynamic_grid_trades(self):
        """Places dynamically adjusted grid trades."""
        try:
            market_price = self.exchange.fetch_ticker(PAIR)['last']
            grid_params = self.adjust_grid_parameters()

            grid_levels = [
                market_price * (1 + (i - grid_params["grid_size"] // 2) * grid_params["grid_spacing"] / 100)
                for i in range(grid_params["grid_size"])
            ]

            for price in grid_levels:
                if price < market_price:
                    self.exchange.create_limit_buy_order(PAIR, 0.01, price)
                else:
                    self.exchange.create_limit_sell_order(PAIR, 0.01, price)

            print(f"✅ Dynamic Grid Trading Activated: {grid_params['grid_size']} Levels, {grid_params['grid_spacing']}% Spacing")
        except Exception as e:
            print(f"⚠️ Error executing dynamic grid trades: {e}")

# 🚀 START DYNAMIC GRID TRADING
if __name__ == "__main__":
    bot = DynamicGridTrading()
    bot.execute_dynamic_grid_trades()
