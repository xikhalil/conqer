# async_trading.py
# ==================================================
# ⚡ ASYNCHRONOUS TRADING – MULTITHREADED TRADE EXECUTION ⚡
# ==================================================

import asyncio
import ccxt.async_support as ccxt
from config import PAIR, EXCHANGE_PLATFORM

class AsyncTrading:
    def __init__(self):
        """Initialize async trading system."""
        self.exchange = getattr(ccxt, EXCHANGE_PLATFORM)({
            "rateLimit": 100,
            "enableRateLimit": True,
        })

    async def fetch_market_data(self):
        """
        Fetches market data asynchronously.
        Returns:
            dict: Latest market data.
        """
        try:
            return await self.exchange.fetch_ticker(PAIR)
        except Exception as e:
            print(f"❌ Error fetching market data: {e}")
            return None

    async def execute_trade(self, trade_type, amount):
        """
        Executes a trade asynchronously.
        Args:
            trade_type (str): "BUY" or "SELL".
            amount (float): Trade size.
        """
        try:
            print(f"🚀 Executing {trade_type} trade for {amount} {PAIR}...")
            if trade_type == "BUY":
                await self.exchange.create_market_buy_order(PAIR, amount)
            else:
                await self.exchange.create_market_sell_order(PAIR, amount)
            print(f"✅ {trade_type} trade executed.")
        except Exception as e:
            print(f"❌ Trade execution failed: {e}")

    async def monitor_trades(self):
        """
        Continuously monitors and executes trades asynchronously.
        """
        while True:
            market_data = await self.fetch_market_data()
            if market_data:
                price = market_data["last"]
                print(f"📊 Current Market Price: {price}")
            await asyncio.sleep(2)  # Avoid excessive API calls

# 🚀 START ASYNC TRADING
if __name__ == "__main__":
    trading_bot = AsyncTrading()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(trading_bot.monitor_trades())
