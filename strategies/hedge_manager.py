# hedge_manager.py
# ==================================================
# 🔄 HEDGE MANAGER – OPTIMIZES HEDGE POSITIONS 🔄
# ==================================================

import numpy as np
from core.exchange_connector import ExchangeConnector
from config import ENABLE_HEDGE_TRADING

class HedgeManager:
    def __init__(self):
        """Initialize hedge manager."""
        self.exchange = ExchangeConnector()

    def monitor_hedge_positions(self):
        """Monitors hedge trades & ensures risk-balanced positions."""
        if not ENABLE_HEDGE_TRADING:
            return "⚠️ Hedge trading is disabled."

        positions = self.exchange.fetch_open_positions()
        hedge_positions = [pos for pos in positions if pos.get("is_hedge")]

        if not hedge_positions:
            return "⚠️ No hedge positions open."

        for position in hedge_positions:
            optimal_size = self.recalculate_hedge_size(position)
            if optimal_size != position["size"]:
                self.adjust_hedge_trade(position, optimal_size)

        return "✅ Hedge positions optimized."

    def recalculate_hedge_size(self, position):
        """
        Recalculates ideal hedge size based on market conditions.
        """
        volatility = self.exchange.fetch_volatility(position["asset"])
        return np.round(position["size"] * (1 + volatility), 4)

    def adjust_hedge_trade(self, position, new_size):
        """
        Adjusts hedge trade position size dynamically.
        """
        print(f"🔄 Adjusting hedge position for {position['asset']} from {position['size']} to {new_size}.")
        self.exchange.modify_order(position["id"], new_size)
