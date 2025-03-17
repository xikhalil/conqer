# profit_tracker.py
# ==================================================
# 📈 PROFIT TRACKER – MONITORS TRADE PROFITS & PERFORMANCE 📈
# ==================================================

import json
import os
from config import PROFIT_TRACKER_FILE
from logging import Logger

class ProfitTracker:
    """Tracks and logs trading performance, profit/loss metrics."""

    def __init__(self):
        """Initialize or load trading performance data."""
        self.file_path = PROFIT_TRACKER_FILE
        self.trading_data = {
            "total_trades": 0,
            "total_profit": 0.0,
            "total_loss": 0.0,
            "win_rate": 0.0,
            "loss_rate": 0.0
        }

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    self.trading_data = json.load(file)
            except Exception as e:
                Logger.error(f"⚠️ Error loading profit tracking data: {e}")

    def update_trade(self, trade_result, profit_loss):
        """
        Updates trade statistics based on latest trade.
        
        Args:
            trade_result (str): "WIN" or "LOSS"
            profit_loss (float): Profit or loss from the trade.
        """
        self.trading_data["total_trades"] += 1

        if trade_result == "WIN":
            self.trading_data["total_profit"] += profit_loss
        else:
            self.trading_data["total_loss"] += abs(profit_loss)

        wins = self.trading_data["total_profit"]
        losses = self.trading_data["total_loss"]
        total = wins + losses

        self.trading_data["win_rate"] = round((wins / total) * 100, 2) if total > 0 else 0
        self.trading_data["loss_rate"] = round((losses / total) * 100, 2) if total > 0 else 0

        self.save_data()

    def save_data(self):
        """Saves trading data to file."""
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.trading_data, file, indent=4)
        except Exception as e:
            Logger.error(f"❌ Error saving profit tracking data: {e}")

    def get_summary(self):
        """Returns a summary of trading performance."""
        return self.trading_data

# 🚀 TEST PROFIT TRACKER
if __name__ == "__main__":
    tracker = ProfitTracker()
    
    tracker.update_trade("WIN", 50.0)
    tracker.update_trade("LOSS", -20.0)

    print("📊 Updated Trading Summary:", tracker.get_summary())
