# ai_feedback_loop.py
# ==================================================
# 🔁 AI FEEDBACK LOOP – SELF-LEARNING TRADING STRATEGY 🔁
# ==================================================

import numpy as np
import pandas as pd
from ai_models.predictive_ai import PredictiveAI
from core.risk_management import apply_risk_management
from config import ENABLE_SELF_LEARNING, RETRAIN_MODEL_THRESHOLD, RETRAIN_MODEL_INTERVAL

class AIFeedbackLoop:
    def __init__(self):
        """
        Initializes the AI feedback system for adaptive learning.
        """
        self.ai_model = PredictiveAI()
        self.trade_history = []
        self.prediction_count = 0  # Track how many times AI makes predictions

    def update_trade_feedback(self, trade_signal, market_data, actual_outcome):
        """
        Collects data on AI's trade predictions vs. actual market movements.
        Args:
            trade_signal (str): "BUY", "SELL", or "HOLD".
            market_data (DataFrame): Market data at time of trade.
            actual_outcome (float): Actual price movement after trade.
        """
        if trade_signal in ["BUY", "SELL"]:
            entry_price = market_data["close"].iloc[-1]
            self.trade_history.append({
                "trade_signal": trade_signal,
                "entry_price": entry_price,
                "actual_outcome": actual_outcome
            })
            self.prediction_count += 1

    def calculate_trade_accuracy(self):
        """
        Evaluates the AI model's accuracy over recent trades.
        Returns:
            float: AI prediction accuracy percentage.
        """
        if len(self.trade_history) < 10:
            return None  # Not enough data to assess performance

        correct_predictions = sum(
            1 for trade in self.trade_history
            if (trade["trade_signal"] == "BUY" and trade["actual_outcome"] > trade["entry_price"]) or
               (trade["trade_signal"] == "SELL" and trade["actual_outcome"] < trade["entry_price"])
        )

        accuracy = (correct_predictions / len(self.trade_history)) * 100
        return accuracy

    def retrain_ai_model(self):
        """
        Retrains the AI model if performance is below the threshold.
        """
        if not ENABLE_SELF_LEARNING or len(self.trade_history) < 20:
            return

        accuracy = self.calculate_trade_accuracy()
        if accuracy and accuracy < RETRAIN_MODEL_THRESHOLD:
            print(f"⚠️ AI accuracy low ({accuracy:.2f}%). Retraining model...")
            self.ai_model.train_new_model()  # Calls AI retraining function
            self.trade_history.clear()  # Reset history after retraining
            self.prediction_count = 0  # Reset prediction count

    def adaptive_trade_sizing(self, trade_signal, balance, market_data):
        """
        Adjusts trade size dynamically based on market volatility.
        Args:
            trade_signal (str): "BUY" or "SELL".
            balance (dict): Current available balance.
            market_data (DataFrame): Latest market data.
        Returns:
            float: Adjusted trade size.
        """
        latest_volatility = market_data["volatility"].iloc[-1]

        base_trade_size = balance["USDT"] * 0.02 / market_data["close"].iloc[-1]  # Base risk level
        if latest_volatility > 2.0:  # High volatility → Reduce position
            trade_size = base_trade_size * 0.7
        elif latest_volatility < 0.5:  # Low volatility → Increase position
            trade_size = base_trade_size * 1.3
        else:
            trade_size = base_trade_size  # Normal condition

        trade_size = round(trade_size, 6)
        print(f"📊 Adjusted Trade Size Based on Volatility: {trade_size} {trade_signal}")
        return trade_size

    def check_and_retrain(self):
        """
        Checks AI performance & triggers retraining if needed.
        """
        if self.prediction_count >= RETRAIN_MODEL_INTERVAL:
            self.retrain_ai_model()

# 🚀 TEST AI FEEDBACK LOOP
if __name__ == "__main__":
    feedback = AIFeedbackLoop()

    # Simulated trade results
    trade_data = [
        {"trade_signal": "BUY", "market_data": {"close": [100, 102]}, "actual_outcome": 105},
        {"trade_signal": "SELL", "market_data": {"close": [105, 103]}, "actual_outcome": 101},
        {"trade_signal": "BUY", "market_data": {"close": [101, 103]}, "actual_outcome": 100},  # Incorrect
    ]

    # Convert market data to DataFrame
    for trade in trade_data:
        trade["market_data"] = pd.DataFrame({'close': trade["market_data"]["close"]})

    for trade in trade_data:
        feedback.update_trade_feedback(trade["trade_signal"], trade["market_data"], trade["actual_outcome"])

    print("✅ AI Trade Accuracy:", feedback.calculate_trade_accuracy(), "%")
    feedback.check_and_retrain()
