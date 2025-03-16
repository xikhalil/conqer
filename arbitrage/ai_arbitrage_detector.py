# ai_arbitrage_detector.py
# ==================================================
# 🧠 AI ARBITRAGE DETECTOR – FINDS PROFITABLE TRADES 🧠
# ==================================================

import numpy as np
from core.exchange_connector import ExchangeConnector
from config import MONITORED_EXCHANGES, ARBITRAGE_MIN_PROFIT

class AIArbitrageDetector:
    def __init__(self):
        """Initialize AI-powered arbitrage detector."""
        self.exchange = ExchangeConnector()

    def get_market_prices(self):
        """
        Fetches market prices from multiple exchanges.
        Returns:
            dict: {exchange: {asset: price}}
        """
        prices = {}
        for exchange in MONITORED_EXCHANGES:
            try:
                prices[exchange] = self.exchange.fetch_ticker(exchange)
            except Exception as e:
                print(f"❌ Failed to fetch prices from {exchange}: {e}")
        return prices

    def find_arbitrage_opportunity(self):
        """
        Scans for price differences across exchanges.
        Returns:
            tuple: (buy_exchange, sell_exchange, asset, buy_price, sell_price)
        """
        prices = self.get_market_prices()
        best_buy = None
        best_sell = None

        for exchange, assets in prices.items():
            for asset, price in assets.items():
                if best_buy is None or price < best_buy[1]:
                    best_buy = (exchange, asset, price)
                if best_sell is None or price > best_sell[1]:
                    best_sell = (exchange, asset, price)

        if best_buy and best_sell:
            buy_exchange, asset, buy_price = best_buy
            sell_exchange, _, sell_price = best_sell
            profit_percentage = ((sell_price - buy_price) / buy_price) * 100

            if profit_percentage >= ARBITRAGE_MIN_PROFIT:
                return buy_exchange, sell_exchange, asset, buy_price, sell_price

        return None
