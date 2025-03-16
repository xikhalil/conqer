# ai_market_adaptation.py
# ==================================================
# 📊 AI MARKET ADAPTATION – DYNAMIC STRATEGY SWITCHING 📊
# ==================================================

import numpy as np
import pandas as pd
from ai_models.predictive_ai import PredictiveAI
from config import ENABLE_MARKET_ADAPTATION, TREND_WINDOW, VOLATILITY_WINDOW

class AIMarketAdaptation:
    def __init__(self):
        """
        Initializes AI strategy adaptation module.
        """
        self.ai_model = PredictiveAI()
        self.current_strategy = "scalping"  # Default strategy

    def detect_market_phase(self, market_data):
        """
        Detects market conditions and determines the optimal strategy.
        Args:
            market_data (DataFrame): Latest market data.
        Returns:
            str: Suggested trading strategy ("scalping", "swing", "grid", "momentum").
        """
        latest_volatility = self.calculate_volatility(market_data)
        latest_trend = self.detect_trend(market_data)

        # 🔹 Scalping: Best in low volatility & sideways markets
        if latest_volatility < 0.5 and latest_trend == "sideways":
            return "scalping"

        # 🔹 Swing Trading: Best in trending markets with moderate volatility
        elif latest_volatility < 1.5 and latest_trend in ["bullish", "bearish"]:
            return "swing"

        # 🔹 Grid Trading: Best in high volatility & ranging markets
        elif latest_volatility >= 1.5 and latest_trend == "sideways":
            return "grid"

        # 🔹 Momentum Trading: Best in strong breakout trends
        elif latest_volatility >= 2.0 and latest_trend in ["bullish", "bearish"]:
            return "momentum"

        return "scalping"  # Default fallback

    def detect_trend(self, market_data):
        """
        Analyzes market trend based on moving averages.
        Args:
            market_data (DataFrame): Latest market data.
        Returns:
            str: "bullish", "bearish", or "sideways".
        """
        if len(market_data) < TREND_WINDOW:
            return "sideways"  # Not enough data

        short_ma = market_data["close"].rolling(window=10).mean()
        long_ma = market_data["close"].rolling(window=30).mean()

        if short_ma.iloc[-1] > long_ma.iloc[-1]:
            return "bullish"
        elif short_ma.iloc[-1] < long_ma.iloc[-1]:
            return "bearish"
        return "sideways"

    def calculate_volatility(self, market_data):
        """
        Calculates rolling volatility based on price fluctuations.
        Args:
            market_data (DataFrame): Market data.
        Returns:
            float: Volatility percentage.
        """
        if len(market_data) < VOLATILITY_WINDOW:
            return 1.0  # Default value if not enough data

        returns = market_data["close"].pct_change()
        return returns.rolling(window=VOLATILITY_WINDOW).std().iloc[-1] * 100

    def adjust_trading_strategy(self, market_data):
        """
        Switches trading strategy based on market conditions.
        Args:
            market_data (DataFrame): Latest market data.
        """
        if not ENABLE_MARKET_ADAPTATION:
            return self.current_strategy  # Keep existing strategy if adaptation is disabled

        new_strategy = self.detect_market_phase(market_data)
        if new_strategy != self.current_strategy:
            print(f"🔄 Switching strategy: {self.current_strategy} → {new_strategy}")
            self.current_strategy = new_strategy

        return self.current_strategy

# 🚀 TEST AI MARKET ADAPTATION
if __name__ == "__main__":
    import random

    # Simulated market data
    sample_data = {
        "close": [random.uniform(50000, 55000) for _ in range(50)]
    }
    df = pd.DataFrame(sample_data)

    ai_adaptation = AIMarketAdaptation()
    strategy = ai_adaptation.adjust_trading_strategy(df)
    print(f"📊 Selected Strategy: {strategy}")
