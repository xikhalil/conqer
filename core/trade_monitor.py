# trade_monitor.py
# ==================================================
# 👀 TRADE MONITOR – LIVE TRADE TRACKING 👀
# ==================================================

import time
import logging
from core.exchange_connector import ExchangeConnector
from core.risk_management import apply_risk_management
from config import TRADE_MONITOR_INTERVAL, ENABLE_SIMULATION_MODE

class TradeMonitor:
    def __init__(self):
        """Initializes trade monitoring system."""
        self.exchange = ExchangeConnector()
        logging.basicConfig(level=logging.INFO)

    def get_open_trades(self):
        """
        Fetches all open trades from the exchange.
        Returns:
            list: List of open trades.
        """
        try:
            open_orders = self.exchange.fetch_open_orders()
            if open_orders:
                logging.info(f"📊 Found {len(open_orders)} open trades.")
            else:
                logging.info("⏳ No open trades currently.")
            return open_orders
        except Exception as e:
            logging.error(f"❌ Error fetching open trades: {e}")
            return []

    def check_trade_health(self):
        """
        Monitors open trades and applies stop-loss & take-profit dynamically.
        """
        open_trades = self.get_open_trades()
        if not open_trades:
            return

        for trade in open_trades:
            trade_id = trade["id"]
            symbol = trade["symbol"]
            entry_price = float(trade["price"])
            trade_type = trade["side"]

            # Apply risk management to get stop-loss & take-profit
            risk_data = apply_risk_management(entry_price, trade_type)
            stop_loss = risk_data["stop_loss"]
            take_profit = risk_data["take_profit"]

            # Get current market price
            try:
                ticker = self.exchange.fetch_ticker(symbol)
                current_price = float(ticker["last"])
            except Exception as e:
                logging.error(f"❌ Error fetching current price for {symbol}: {e}")
                continue

            # 🚨 Stop-Loss Trigger
            if trade_type == "BUY" and current_price <= stop_loss:
                logging.warning(f"🚨 Stop-loss hit for {trade_id} ({symbol}). Closing trade...")
                self.close_trade(trade_id)

            elif trade_type == "SELL" and current_price >= take_profit:
                logging.info(f"💰 Take-profit reached for {trade_id} ({symbol}). Closing trade...")
                self.close_trade(trade_id)

    def close_trade(self, trade_id):
        """
        Closes an open trade using the trade ID.
        Args:
            trade_id (str): The ID of the open trade.
        """
        if ENABLE_SIMULATION_MODE:
            logging.info(f"🛠️ [SIMULATION] Closing trade {trade_id}.")
            return

        try:
            logging.info(f"🔄 Closing Trade ID: {trade_id}...")
            order = self.exchange.cancel_order(trade_id)
            logging.info(f"✅ Trade Closed: {order}")
        except Exception as e:
            logging.error(f"❌ Error Closing Trade: {e}")

    def start_trade_monitoring(self):
        """
        Continuously monitors trades and ensures risk management.
        """
        while True:
            self.check_trade_health()
            time.sleep(TRADE_MONITOR_INTERVAL)

# 🚀 START TRADE MONITORING
if __name__ == "__main__":
    print("👀 TRADE MONITOR ACTIVATED 👀")
    monitor = TradeMonitor()
    monitor.start_trade_monitoring()
