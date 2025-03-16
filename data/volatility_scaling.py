# volatility_scaling.py
# ==================================================
# 📊 VOLATILITY SCALING – ADAPTIVE POSITION SIZING 📊
# ==================================================

import numpy as np
from config import RISK_PER_TRADE, ORDER_MINIMUM_VALUE

class VolatilityScaling:
    @staticmethod
    def calculate_trade_size(balance, trade_type, price, market_volatility):
        """
        Dynamically calculates trade size based on balance, trade type, and market volatility.

        Args:
            balance (dict): Account balances { "USDT": float, "PI": float }.
            trade_type (str): "BUY" or "SELL".
            price (float): Current market price.
            market_volatility (float): Volatility factor affecting position size.

        Returns:
            float: Adjusted trade size.
        """
        if balance["USDT"] <= 0 and trade_type == "BUY":
            return 0.0

        if balance["PI"] <= 0 and trade_type == "SELL":
            return 0.0

        # ✅ Adjust trade size based on market volatility (Lower volatility → Higher position)
        volatility_factor = max(0.5, min(2, 1 / (market_volatility + 1e-6)))  # Keep between 0.5 and 2
        adjusted_risk_amount = balance["USDT"] * RISK_PER_TRADE * volatility_factor
        trade_size = adjusted_risk_amount / price if trade_type == "BUY" else balance["PI"] * RISK_PER_TRADE

        return round(trade_size, 6)

