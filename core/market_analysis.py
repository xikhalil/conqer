# market_analysis.py
# ==================================================
# 📊 MARKET ANALYSIS – ADVANCED TRADING INSIGHTS 📊
# ==================================================

import pandas as pd
import numpy as np

class MarketAnalysis:
    def __init__(self, df):
        """
        Initializes the market analysis module.
        Args:
            df (pd.DataFrame): Market data containing OHLCV values.
        """
        self.df = df.copy()

    def detect_trend(self):
        """
        Determines whether the market is in an uptrend, downtrend, or sideways.
        Returns:
            str: "UPTREND", "DOWNTREND", or "SIDEWAYS".
        """
        short_ma = self.df["close"].rolling(window=10).mean()
        long_ma = self.df["close"].rolling(window=50).mean()

        if short_ma.iloc[-1] > long_ma.iloc[-1]:
            return "UPTREND"
        elif short_ma.iloc[-1] < long_ma.iloc[-1]:
            return "DOWNTREND"
        return "SIDEWAYS"

    def calculate_volatility(self):
        """
        Calculates rolling volatility.
        Returns:
            float: Current market volatility.
        """
        returns = self.df["close"].pct_change()
        return returns.rolling(window=10).std().iloc[-1]

    def identify_support_resistance(self):
        """
        Identifies key support and resistance levels.
        Returns:
            dict: Support and resistance levels.
        """
        support = self.df["low"].rolling(window=20).min().iloc[-1]
        resistance = self.df["high"].rolling(window=20).max().iloc[-1]
        return {"support": support, "resistance": resistance}

    def get_market_summary(self):
        """
        Returns a complete market analysis summary.
        Returns:
            dict: Market insights including trend, volatility, and key levels.
        """
        return {
            "trend": self.detect_trend(),
            "volatility": round(self.calculate_volatility(), 5),
            "support_resistance": self.identify_support_resistance()
        }

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    sample_data = {
        "close": [50000, 50200, 50500, 50700, 51000, 51500, 52000, 53000, 54000],
        "high": [50100, 50300, 50600, 50800, 51100, 51600, 52100, 53100, 54100],
        "low": [49900, 50100, 50400, 50600, 50900, 51400, 51900, 52900, 53900]
    }
    df = pd.DataFrame(sample_data)

    analyzer = MarketAnalysis(df)
    summary = analyzer.get_market_summary()
    print("📊 Market Summary:\n", summary)
