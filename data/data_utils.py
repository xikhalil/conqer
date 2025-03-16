# data_utils.py
# ==================================================
# 📂 DATA UTILITIES – HELPER FUNCTIONS FOR DATA PROCESSING 📂
# ==================================================

import numpy as np
from config import ORDER_MINIMUM_VALUE, RISK_PER_TRADE

class DataUtils:
    @staticmethod
    def calculate_trade_size(balance, trade_type, price):
        """
        Calculates trade size while enforcing exchange minimum requirements.
        Args:
            balance (dict): {"USDT": float, "PI": float}.
            trade_type (str): "BUY" or "SELL".
            price (float): Current market price.

        Returns:
            float: Adjusted trade size.
        """
        if trade_type == "BUY":
            trade_size = (balance["USDT"] * RISK_PER_TRADE) / price
        else:
            trade_size = balance["PI"] * RISK_PER_TRADE  

        trade_size = round(trade_size, 6)  # Ensure precision

        # ✅ Ensure trade meets exchange minimum size
        min_trade_size = max(ORDER_MINIMUM_VALUE / price, 1.0)
        if trade_size < min_trade_size:
            print(f"⚠️ Adjusting trade size ({trade_size} PI) to minimum: {min_trade_size} PI.")
            trade_size = min_trade_size

        if trade_size * price < ORDER_MINIMUM_VALUE:
            print(f"❌ Trade size {trade_size} PI is still below exchange minimum order value. Trade skipped.")
            return 0

        print(f"🛠️ Final Trade Size Calculation: {trade_type}, Size = {trade_size:.6f}")
        return trade_size
