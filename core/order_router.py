# order_router.py
# ==================================================
# 📡 ORDER ROUTER – EXECUTES & MANAGES TRADES 📡
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from core.risk_management import validate_trade
from utils.logger import Logger
from config import MAX_SLIPPAGE, RETRY_ATTEMPTS, RETRY_DELAY

class OrderRouter:
    def __init__(self, exchange: ExchangeConnector):
        """
        Initializes the order router.
        Args:
            exchange (ExchangeConnector): The exchange connection instance.
        """
        self.exchange = exchange

    def place_order(self, trade_signal, market_data, balance):
        """
        Places a trade order with risk management & slippage handling.
        Args:
            trade_signal (str): "BUY" or "SELL".
            market_data (DataFrame): Latest market data.
            balance (dict): Available balance.
        Returns:
            dict or None: Order details if successful, None if failed.
        """
        try:
            # ✅ Validate trade
            trade_decision = validate_trade(trade_signal, market_data, balance)
            if not trade_decision["valid"]:
                Logger.warning(f"⚠️ Trade Rejected: {trade_decision['reason']}")
                return None

            symbol = "PI/USDT"
            position_size = trade_decision["position_size"]
            entry_price = trade_decision["entry_price"]

            # ✅ Check slippage before placing the order
            latest_price = self.exchange.fetch_ticker(symbol)["last"]
            allowed_slippage = entry_price * MAX_SLIPPAGE
            slippage_limit = entry_price + allowed_slippage if trade_signal == "BUY" else entry_price - allowed_slippage

            if (trade_signal == "BUY" and latest_price > slippage_limit) or (trade_signal == "SELL" and latest_price < slippage_limit):
                Logger.warning(f"⚠️ Trade rejected due to high slippage: {latest_price} (Limit: {slippage_limit})")
                return None

            # ✅ Execute order
            return self._execute_trade_with_retry(symbol, trade_signal, position_size)

        except Exception as e:
            Logger.error(f"❌ OrderRouter.place_order failed: {e}")
            return None

    def _execute_trade_with_retry(self, symbol, trade_signal, position_size):
        """
        Tries to execute a trade multiple times if it fails.
        Args:
            symbol (str): Trading pair.
            trade_signal (str): "BUY" or "SELL".
            position_size (float): Amount to trade.
        Returns:
            dict or None: Order details if successful, None if failed.
        """
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                Logger.info(f"📡 Attempting {trade_signal} order for {symbol} (Size: {position_size}) - Try {attempt}/{RETRY_ATTEMPTS}")
                
                if trade_signal == "BUY":
                    order = self.exchange.create_market_buy_order(symbol, position_size)
                else:
                    order = self.exchange.create_market_sell_order(symbol, position_size)

                if order:
                    Logger.info(f"✅ Order Successful: {order}")
                    return order

            except Exception as e:
                Logger.warning(f"⚠️ Trade attempt {attempt} failed: {e}")
                time.sleep(RETRY_DELAY)  # Wait before retrying

        Logger.error(f"❌ Order execution failed after {RETRY_ATTEMPTS} attempts.")
        return None

# 🚀 TEST ORDER ROUTER (DEBUG ONLY)
if __name__ == "__main__":
    from core.exchange_connector import ExchangeConnector
    import pandas as pd

    # Initialize components
    exchange = ExchangeConnector()
    router = OrderRouter(exchange)

    # Simulated trade decision
    sample_data = pd.DataFrame({"close": [50000, 50200, 50500, 50700, 51000]})
    balance = {"USDT": 1000, "PI": 2}

    order_result = router.place_order("BUY", sample_data, balance)
    print("📊 Order Result:", order_result)
