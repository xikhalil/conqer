# transformer_model.py
# ==================================================
# 🤖 TRANSFORMER MODEL – AI-POWERED TRADE PREDICTION 🤖
# ==================================================

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from config import MODEL_PATH

class TransformerModel:
    def __init__(self):
        """
        Initializes the Transformer AI model for trade prediction.
        """
        self.model = self.load_model()

    def load_model(self):
        """
        Loads the trained Transformer model.
        Returns:
            Trained AI model.
        """
        try:
            model = load_model(MODEL_PATH)
            print("✅ Transformer Model Loaded Successfully.")
            return model
        except Exception as e:
            print(f"❌ Error loading Transformer Model: {e}")
            return None

    def preprocess_input(self, market_data):
        """
        Prepares real-time market data for AI model prediction.
        Args:
            market_data (np.array): Last 30 time steps of market indicators.
        Returns:
            np.array: Reshaped data for model input.
        """
        if market_data.shape != (30, 5):  # Ensure correct input shape
            print("⚠️ Market data format incorrect. Returning default values.")
            return np.zeros((1, 30, 5))  # Prevent errors with dummy input
        return np.expand_dims(market_data, axis=0)  # Reshape for model

    def predict_price(self, market_data):
        """
        Uses the Transformer AI model to predict the next price.
        Args:
            market_data (np.array): Market indicators for prediction.
        Returns:
            float: Predicted price movement.
        """
        processed_data = self.preprocess_input(market_data)
        prediction = self.model.predict(processed_data, verbose=0)[0][0]
        return prediction

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    model = TransformerModel()

    # 🔹 Simulated real-time market data (30 time steps, 5 indicators)
    dummy_data = np.random.rand(30, 5)  
    predicted_price = model.predict_price(dummy_data)

    print(f"📈 Predicted Price Movement: {predicted_price}")
