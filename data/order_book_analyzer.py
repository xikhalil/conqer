# order_book_analyzer.py
# ==================================================
# 📊 ORDER BOOK ANALYZER – DETECTS LIQUIDITY & PRICE MOVEMENT 📊
# ==================================================

import numpy as np

class OrderBookAnalyzer:
    def __init__(self, order_book):
        """Initialize with the latest order book data."""
        self.order_book = order_book

    def detect_buy_sell_walls(self):
        """
        Detects large buy/sell walls in the order book.
        Returns:
            dict: Buy/Sell wall strength.
        """
        if not self.order_book:
            return {"buy_wall": 0, "sell_wall": 0}

        bids = np.array(self.order_book.get("bids", []))
        asks = np.array(self.order_book.get("asks", []))

        if bids.size == 0 or asks.size == 0:
            return {"buy_wall": 0, "sell_wall": 0}

        buy_wall = np.max(bids[:, 1])  # Highest volume on buy side
        sell_wall = np.max(asks[:, 1])  # Highest volume on sell side

        return {"buy_wall": buy_wall, "sell_wall": sell_wall}

    def detect_liquidity_gaps(self):
        """
        Detects gaps in liquidity that could cause price spikes.
        Returns:
            bool: True if liquidity gaps are detected, False otherwise.
        """
        if not self.order_book:
            return False

        asks = np.array(self.order_book.get("asks", []))
        bids = np.array(self.order_book.get("bids", []))

        if len(asks) < 2 or len(bids) < 2:
            return False

        top_ask_gap = (asks[1, 0] - asks[0, 0]) / asks[0, 0]  # % gap between first two asks
        top_bid_gap = (bids[0, 0] - bids[1, 0]) / bids[0, 0]  # % gap between first two bids

        return top_ask_gap > 0.005 or top_bid_gap > 0.005  # If gap > 0.5%, potential price spike
