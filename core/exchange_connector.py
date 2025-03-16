# exchange_connector.py
# ==================================================
# 🔗 EXCHANGE CONNECTOR – HANDLES MEXC API CONNECTION 🔗
# ==================================================

import os
import ccxt
import pandas as pd
import time
from dotenv import load_dotenv
from utils.logger import Logger


# ✅ Load API keys securely from .env file
load_dotenv()

class ExchangeConnector:
    def __init__(self):
        """
        Initializes connection to the MEXC exchange.
        """
        try:
            self.exchange = ccxt.mexc({
                'apiKey': os.getenv("MEXC_API_KEY"),
                'secret': os.getenv("MEXC_API_SECRET"),
                'enableRateLimit': True
            })

            self.exchange.load_markets()
            Logger.info("✅ Connected to MEXC successfully.")

        except Exception as e:
            Logger.error(f"❌ Exchange Connection Failed: {e}")
            exit()  # Stop execution if connection fails

    def fetch_market_data(self, pair="PI/USDT"):
        """
        Fetch latest market data and add indicators.
        Args:
            pair (str): Trading pair (default: "PI/USDT").
        Returns:
            pd.DataFrame: Market data with indicators.
        """
        try:
            Logger.info(f"📡 Fetching market data for {pair}...")
            ohlcv = self.exchange.fetch_ohlcv(pair, timeframe='1m', limit=200)

            if not ohlcv or len(ohlcv) == 0:
                Logger.warning(f"⚠️ No OHLCV data received for {pair}. Retrying in 60 seconds...")
                return None

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            df.dropna(inplace=True)
            Logger.info(f"✅ Market Data Loaded: {len(df)} candles.")
            return df

        except ccxt.NetworkError as e:
            Logger.error(f"🌐 Network Error fetching market data: {e}")
        except ccxt.ExchangeError as e:
            Logger.error(f"❌ Exchange API Error: {e}")
        except ccxt.BadSymbol as e:
            Logger.error(f"⚠️ Invalid Trading Pair: {pair}. Check if it exists on MEXC.")
        except Exception as e:
            Logger.error(f"⚠️ Unexpected Error: {e}")

        return None  # Ensure None is returned if there's an error

    def fetch_balance(self):
        """
        Fetch account balance from the exchange.
        Returns:
            dict: Available USDT and PI balance.
        """
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance['free'].get('USDT', 0)
            pi_balance = balance['free'].get('PI', 0)
            return {"USDT": usdt_balance, "PI": pi_balance}

        except Exception as e:
            Logger.error(f"❌ Error fetching balance: {e}")
            return {"USDT": 0, "PI": 0}  # ✅ Prevents crashes by returning default balance

    def place_order(self, pair, side, amount):
        """
        Places a market order (BUY or SELL).
        Args:
            pair (str): Trading pair (e.g., "PI/USDT").
            side (str): "buy" or "sell".
            amount (float): Order size.
        Returns:
            dict or None: Order details if successful, None if failed.
        """
        try:
            Logger.info(f"📈 Placing {side.upper()} order: {amount} {pair}...")
            order = self.exchange.create_market_order(pair, side, amount)
            Logger.info(f"✅ Order Executed: {order}")
            return order

        except Exception as e:
            Logger.error(f"❌ Order Execution Failed: {e}")
            return None

    def fetch_open_orders(self, pair="PI/USDT"):
        """
        Fetches all open orders for a trading pair.
        Args:
            pair (str): Trading pair.
        Returns:
            list: Open orders.
        """
        try:
            open_orders = self.exchange.fetch_open_orders(pair)
            return open_orders if open_orders else []

        except Exception as e:
            Logger.error(f"❌ Error fetching open orders: {e}")
            return []

    def cancel_order(self, order_id):
        """
        Cancels an open order.
        Args:
            order_id (str): ID of the order to cancel.
        Returns:
            dict or None: Cancelled order details or None if failed.
        """
        try:
            Logger.info(f"🔄 Cancelling Order ID: {order_id}...")
            order = self.exchange.cancel_order(order_id)
            Logger.info(f"✅ Order Cancelled: {order}")
            return order

        except Exception as e:
            Logger.error(f"❌ Error Cancelling Order: {e}")
            return None

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    exchange = ExchangeConnector()
    print("💰 Balance:", exchange.fetch_balance())

    market_data = exchange.fetch_market_data()
    if market_data is not None:
        print(market_data.head())

    # Test placing an order (SIMULATION MODE ONLY)
    # exchange.place_order("PI/USDT", "buy", 1.0)
