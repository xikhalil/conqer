# predictive_ai.py
# ==================================================
# 🤖 AI-POWERED TRADE SIGNAL GENERATOR 🤖
# ==================================================

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pandas as pd
import os
from config import MODEL_PATH, RETRAIN_MODEL_INTERVAL

class PredictiveAI:
    def __init__(self):
        """Load AI model for trade signal prediction."""
        self.model = self.load_or_create_model()
        self.prediction_count = 0  # Track AI prediction usage

    def load_or_create_model(self):
        """Loads AI model if available, otherwise creates a new model."""
        if os.path.exists(MODEL_PATH):
            try:
                print("✅ Loading existing AI model...")
                return load_model(MODEL_PATH)
            except Exception as e:
                print(f"❌ AI Model Load Failed: {e}")

        print("⚠️ No valid AI model found. Creating a new model...")
        return self.create_new_model()

    def create_new_model(self):
        """Creates and compiles a new AI model."""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(30, 5)),
            Dropout(0.2),
            LSTM(30, return_sequences=False),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mse")
        print("✅ New AI Model Created and Compiled.")
        return model

    def prepare_data(self, market_data):
        """
        Prepares market data for AI model prediction.
        Args:
            market_data (DataFrame): Market data with OHLCV & indicators.
        Returns:
            np.array: Processed input data for model
        """
        indicators = ['rsi', 'macd', 'signal', 'momentum', 'volatility']
        if not all(indicator in market_data.columns for indicator in indicators):
            print("⚠️ Missing required indicators in market data. Returning HOLD.")
            return np.zeros((1, 30, 5))  # Return dummy data to prevent errors

        data = market_data[indicators].tail(30).values  # Last 30 time steps
        return np.expand_dims(data, axis=0)  # Reshape for model input

    def generate_trade_signal(self, market_data):
        """
        Uses AI model to generate a trade signal.
        Args:
            market_data (DataFrame): Latest market data.
        Returns:
            str: "BUY", "SELL", or "HOLD"
        """
        if len(market_data) < 30:
            return "HOLD"  # Not enough data for AI model

        input_data = self.prepare_data(market_data)
        predicted_price = self.model.predict(input_data, verbose=0)[0][0]
        latest_price = market_data['close'].iloc[-1]

        # Track predictions
        self.prediction_count += 1

        # Trade signal logic
        if predicted_price > latest_price * 1.005:
            return "BUY"
        elif predicted_price < latest_price * 0.995:
            return "SELL"
        return "HOLD"

    def retrain_if_needed(self, training_data, labels):
        """
        Retrains the AI model after a certain number of predictions.
        Args:
            training_data (np.array): Training data for the model.
            labels (np.array): Target labels for training.
        """
        if self.prediction_count >= RETRAIN_MODEL_INTERVAL:
            print("🔄 Retraining AI model...")
            self.model.fit(training_data, labels, epochs=3, batch_size=16, verbose=1)
            self.model.save(MODEL_PATH)
            self.prediction_count = 0
            print("✅ AI Model Retrained and Saved.")

# 🚀 Example usage
if __name__ == "__main__":
    print("🔍 AI Model Testing...")
    ai = PredictiveAI()
    test_data = pd.DataFrame({
        "close": np.random.rand(50),
        "rsi": np.random.rand(50),
        "macd": np.random.rand(50),
        "signal": np.random.rand(50),
        "momentum": np.random.rand(50),
        "volatility": np.random.rand(50)
    })
    signal = ai.generate_trade_signal(test_data)
    print("📈 Generated Trade Signal:", signal)
