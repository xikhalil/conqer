import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv
from custom_logging.logger import Logger

# Load API keys securely from .env file
load_dotenv()

class ExchangeConnector:
    def __init__(self):
        """
        Initializes connection to the MEXC exchange.
        """
        try:
            self.api_key = os.getenv("MEXC_API_KEY")
            self.api_secret = os.getenv("MEXC_API_SECRET")
            self.base_url = "https://api.mexc.com/api/v3"  # ✅ FIXED BASE URL
            
            # Create a session for reusing the connection
            self.session = requests.Session()
            self.session.headers.update({'X-MEXC-APIKEY': self.api_key})

            Logger.info("✅ MEXC API Initialized Successfully.")
        except Exception as e:
            Logger.error(f"❌ MEXC API Initialization Failed: {e}")
            exit()

    def fetch_market_data(self, pair="PI/USDT"):
        """
        Fetch latest market data for the given pair.
        """
        try:
            url = f"{self.base_url}/klines"  # ✅ FIXED ENDPOINT
            params = {
                'symbol': pair.replace("/", ""),  # ✅ Convert "PI/USDT" -> "PIUSDT"
                'interval': '1m',
                'limit': 200
            }

            response = self.session.get(url, params=params)

            if response.status_code == 429:
                Logger.warning("⚠️ Rate limit hit. Retrying in 60 seconds...")
                time.sleep(60)
                return self.fetch_market_data(pair)  # Retry the request

            # ✅ Log raw response for debugging
            Logger.info(f"API Response: {response.text[:200]}")  # Log first 200 chars

            # ✅ Detect if response is HTML instead of JSON
            if "text/html" in response.headers.get("Content-Type", ""):
                Logger.error(f"❌ Received HTML instead of JSON: {response.text[:200]}")
                return None

            data = response.json()

            # ✅ Ensure the API response is a list (not a dict)
            if not isinstance(data, list):
                Logger.error(f"❌ Unexpected API response format: {type(data)}")
                return None

            # ✅ Convert list to DataFrame with correct columns
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.drop(columns=['close_time', 'quote_asset_volume'], inplace=True)  # Remove unnecessary columns
            df.dropna(inplace=True)

            if df.empty:
                Logger.warning(f"⚠️ No market data received for {pair}. Skipping cycle.")
                return None

            Logger.info(f"✅ Market Data Loaded: {len(df)} candles.")
            return df

        except requests.exceptions.RequestException as e:
            Logger.error(f"❌ Network error: {e}")
            return None
        except Exception as e:
            Logger.error(f"❌ Error fetching market data: {e}")
            return None

    def fetch_balance(self):
        """
        Fetch account balance from the MEXC API.
        """
        try:
            url = f"{self.base_url}/account/api/v3/account"  # ✅ FIXED ENDPOINT
            response = self.session.get(url)
            data = response.json()

            if not isinstance(data, dict):
                Logger.error("❌ Unexpected response format for balance.")
                return {"USDT": 0, "PI": 0}

            if data.get("code") != 200:
                Logger.error(f"❌ Error fetching balance: {data.get('msg')}")
                return {"USDT": 0, "PI": 0}

            balance = data.get('data', {})
            return {"USDT": balance.get('USDT', 0), "PI": balance.get('PI', 0)}

        except requests.exceptions.RequestException as e:
            Logger.error(f"❌ Network error: {e}")
            return {"USDT": 0, "PI": 0}
        except Exception as e:
            Logger.error(f"❌ Error fetching balance: {e}")
            return {"USDT": 0, "PI": 0}

    def place_order(self, pair, side, amount):
        """
        Places a market order (BUY or SELL).
        """
        if amount <= 0:
            Logger.error(f"❌ Invalid order amount: {amount}")
            return None

        try:
            url = f"{self.base_url}/order"
            params = {
                'symbol': pair.replace("/", ""),  # ✅ FIXED PAIR FORMAT
                'side': side.upper(),  # ✅ ENSURE UPPERCASE
                'orderType': 'MARKET',  # ✅ FIXED PARAMETER NAME
                'quantity': amount,
            }

            response = self.session.post(url, params=params)
            data = response.json()

            if not isinstance(data, dict):
                Logger.error("❌ Unexpected response format for order placement.")
                return None

            if data.get("code") != 200:
                Logger.error(f"❌ Error placing order: {data.get('msg')}")
                return None

            Logger.info(f"✅ Order Executed: {data}")
            return data

        except requests.exceptions.RequestException as e:
            Logger.error(f"❌ Network error: {e}")
            return None
        except Exception as e:
            Logger.error(f"❌ Error placing order: {e}")
            return None

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    exchange = ExchangeConnector()
    print("💰 Balance:", exchange.fetch_balance())
    market_data = exchange.fetch_market_data()
    if market_data is not None:
        print(market_data.head())
