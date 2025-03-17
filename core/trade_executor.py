# trade_executor.py
# ==================================================
# 📈 TRADE EXECUTOR – HANDLES ORDER PLACEMENT 📈
# ==================================================

import time
from core.exchange_connector import ExchangeConnector
from core.order_router import OrderRouter
from core.risk_management import validate_trade
from custom_logging.logger import Logger

from config import RETRY_ATTEMPTS, RETRY_DELAY

class TradeExecutor:
    def __init__(self):
        """Initialize TradeExecutor with an exchange connection."""
        self.exchange = ExchangeConnector()
        self.order_router = OrderRouter(self.exchange)

    def execute_trade(self, trade_signal, market_data, balance):
        """
        Executes a trade based on AI trade signal & validation.
        Args:
            trade_signal (str): "BUY" or "SELL".
            market_data (DataFrame): Latest market data.
            balance (dict): Available USDT & PI balance.
        Returns:
            dict: Order details or None if failed.
        """
        try:
            # ✅ Validate trade before execution
            trade_decision = validate_trade(trade_signal, market_data, balance)
            if not trade_decision["valid"]:
                Logger.warning(f"⚠️ Trade Rejected: {trade_decision['reason']}")
                return None

            # ✅ Execute order through the order router
            return self._execute_with_retry(trade_signal, market_data, balance)

        except Exception as e:
            Logger.error(f"❌ Trade Execution Failed: {e}")
            return None

    def _execute_with_retry(self, trade_signal, market_data, balance):
        """
        Tries to execute a trade multiple times if it fails.
        Args:
            trade_signal (str): "BUY" or "SELL".
            market_data (DataFrame): Latest market data.
            balance (dict): Available balance.
        Returns:
            dict or None: Order details if successful, None if failed.
        """
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                Logger.info(f"📡 Attempting {trade_signal} trade - Try {attempt}/{RETRY_ATTEMPTS}")

                # ✅ Place order using OrderRouter
                order = self.order_router.place_order(trade_signal, market_data, balance)

                if order:
                    Logger.info(f"✅ Trade Successful: {order}")
                    return order

            except Exception as e:
                Logger.warning(f"⚠️ Trade attempt {attempt} failed: {e}")
                time.sleep(RETRY_DELAY)  # Wait before retrying

        Logger.error(f"❌ Trade execution failed after {RETRY_ATTEMPTS} attempts.")
        return None

# 🚀 TEST TRADE EXECUTOR (DEBUG ONLY)
if __name__ == "__main__":
    import pandas as pd

    # Initialize components
    exchange = ExchangeConnector()
    executor = TradeExecutor()

    # Simulated trade decision
    sample_data = pd.DataFrame({"close": [50000, 50200, 50500, 50700, 51000]})
    balance = {"USDT": 1000, "PI": 2}

    trade_result = executor.execute_trade("BUY", sample_data, balance)
    print("📊 Trade Execution Result:", trade_result)
