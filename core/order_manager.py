# order_manager.py
# ==================================================
# 🛒 ORDER MANAGER – EXECUTES & HANDLES TRADES 🛒
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from config import ENABLE_SIMULATION_MODE, ORDER_MINIMUM_VALUE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
from utils.logger import Logger

class OrderManager:
    def __init__(self, exchange: ExchangeConnector):
        """
        Initializes the order manager with exchange connection.
        Args:
            exchange (ExchangeConnector): The exchange API connection.
        """
        self.exchange = exchange

    def execute_order(self, trade_type, trade_decision):
        """
        Executes a market order (BUY/SELL) with risk management.
        Args:
            trade_type (str): "BUY" or "SELL".
            trade_decision (dict): Contains trade size & risk parameters.
        Returns:
            dict or None: Order details if successful, otherwise None.
        """
        try:
            symbol = trade_decision.get("symbol", "PI/USDT")
            position_size = trade_decision["position_size"]
            entry_price = trade_decision["entry_price"]

            # ✅ Ensure trade size meets minimum exchange requirement
            if position_size * entry_price < ORDER_MINIMUM_VALUE:
                Logger.warning(f"⚠️ Trade size too small! Must be at least {ORDER_MINIMUM_VALUE} USDT.")
                return None

            # ✅ SIMULATION MODE – Prevent real execution if enabled
            if ENABLE_SIMULATION_MODE:
                Logger.info(f"🛠️ [SIMULATION] {trade_type} {position_size} {symbol} @ {entry_price}")
                return {"id": "SIM_ORDER", "status": "simulated", "symbol": symbol, "side": trade_type}

            # ✅ LIVE TRADING – Execute the order on the exchange
            Logger.info(f"📈 Executing {trade_type} Order: {position_size} {symbol}...")
            order = self.exchange.place_order(symbol, trade_type.lower(), position_size)

            if order:
                Logger.info(f"✅ Order Executed: {order}")
                return order

        except Exception as e:
            Logger.error(f"❌ Order Execution Failed: {e}")
            return None

    def set_stop_loss_and_take_profit(self, trade_type, entry_price):
        """
        Calculates stop-loss & take-profit levels based on trade type.
        Args:
            trade_type (str): "BUY" or "SELL".
            entry_price (float): Trade entry price.
        Returns:
            dict: Stop-loss and take-profit prices.
        """
        if trade_type == "BUY":
            stop_loss = entry_price * (1 - STOP_LOSS_PERCENT)
            take_profit = entry_price * (1 + TAKE_PROFIT_PERCENT)
        else:  # SELL
            stop_loss = entry_price * (1 + STOP_LOSS_PERCENT)
            take_profit = entry_price * (1 - TAKE_PROFIT_PERCENT)

        Logger.info(f"📊 Stop-Loss: {stop_loss:.6f}, Take-Profit: {take_profit:.6f}")
        return {"stop_loss": stop_loss, "take_profit": take_profit}

    def close_trade(self, trade_id):
        """
        Closes an open trade using the trade ID.
        Args:
            trade_id (str): The ID of the open trade.
        Returns:
            dict or None: Close order details if successful, otherwise None.
        """
        try:
            Logger.info(f"🔄 Closing Trade ID: {trade_id}...")
            order = self.exchange.cancel_order(trade_id)
            Logger.info(f"✅ Trade Closed: {order}")
            return order

        except Exception as e:
            Logger.error(f"❌ Error Closing Trade: {e}")
            return None

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    exchange = ExchangeConnector()
    order_manager = OrderManager(exchange)

    # Example trade execution
    trade_decision = {"position_size": 1.0, "entry_price": 1.50, "symbol": "PI/USDT"}
    order_manager.execute_order("BUY", trade_decision)
