# portfolio_manager.py
# ==================================================
# 📊 PORTFOLIO MANAGER – TRACKS BALANCE & POSITIONS 📊
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from custom_logging.logger import Logger

from config import PAIR, ORDER_MINIMUM_VALUE

class PortfolioManager:
    def __init__(self):
        """Initialize portfolio management system."""
        self.exchange = ExchangeConnector()
        self.balance = {"USDT": 0, "PI": 0}
        self.positions = []  # ✅ Stores active positions

    def update_balance(self):
        """
        Fetch and update the latest account balance.
        """
        self.balance = self.exchange.fetch_balance()
        Logger.info(f"💰 Updated Balance: {self.balance}")

    def track_unrealized_pnl(self):
        """
        Calculate unrealized profit/loss on open positions.
        """
        if not self.positions:
            Logger.info("📊 No open positions to track.")
            return

        market_price = self.exchange.fetch_ticker_price(PAIR)
        for pos in self.positions:
            entry_price = pos["entry_price"]
            position_size = pos["size"]
            trade_type = pos["trade_type"]

            # ✅ Calculate Unrealized P/L
            if trade_type == "BUY":
                pnl = (market_price - entry_price) * position_size
            else:
                pnl = (entry_price - market_price) * position_size

            Logger.info(f"📊 Unrealized P/L for {pos['trade_type']} Position: {pnl:.2f} USDT")

    def add_position(self, trade_signal, position_size, entry_price):
        """
        Add a new position to the portfolio.
        Args:
            trade_signal (str): "BUY" or "SELL".
            position_size (float): Amount of asset.
            entry_price (float): Trade entry price.
        """
        if position_size * entry_price < ORDER_MINIMUM_VALUE:
            Logger.warning(f"⚠️ Position size too small: {position_size:.6f} PI. Skipping...")
            return

        position = {
            "trade_type": trade_signal,
            "size": position_size,
            "entry_price": entry_price,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.positions.append(position)
        Logger.info(f"✅ Position Added: {position}")

    def close_position(self, trade_id):
        """
        Close an active position.
        Args:
            trade_id (str): The ID of the trade to close.
        """
        self.positions = [pos for pos in self.positions if pos.get("trade_id") != trade_id]
        Logger.info(f"📉 Closed Trade ID: {trade_id}")

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    portfolio = PortfolioManager()
    portfolio.update_balance()
    portfolio.track_unrealized_pnl()
