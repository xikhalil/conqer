# train_transformer.py
# ==================================================
# 🎯 TRAIN TRANSFORMER AI MODEL FOR TRADING 🎯
# ==================================================

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from config import MODEL_PATH, TRAIN_EPOCHS, TRAIN_BATCH_SIZE
from core.data_preprocessing import load_market_data

class TrainTransformer:
    def __init__(self):
        """Initialize AI training module."""
        self.df = load_market_data()
        self.model = self.load_or_create_model()

    def load_or_create_model(self):
        """
        Loads an existing model or creates a new one if unavailable.
        Returns:
            Trained or new AI model.
        """
        try:
            model = load_model(MODEL_PATH)
            print("✅ Existing Transformer Model Loaded.")
        except Exception:
            print("⚠️ No saved model found. Creating a new model...")
            model = self.build_model()
        return model

    def build_model(self):
        """
        Builds a Transformer-based AI model for price prediction.
        Returns:
            Sequential: Compiled AI model.
        """
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(30, 5)),
            Dropout(0.3),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1)  # Output: Predicted price movement
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def prepare_training_data(self):
        """
        Prepares historical market data for AI training.
        Returns:
            tuple: (X_train, y_train) for model training.
        """
        indicators = ['rsi', 'macd', 'signal', 'momentum', 'volatility']
        X, y = [], []
        for i in range(30, len(self.df) - 1):
            X.append(self.df[indicators].iloc[i-30:i].values)
            y.append(self.df['close'].iloc[i + 1])

        return np.array(X), np.array(y)

    def train_model(self):
        """
        Trains the AI model on historical market data.
        """
        X_train, y_train = self.prepare_training_data()
        self.model.fit(X_train, y_train, epochs=TRAIN_EPOCHS, batch_size=TRAIN_BATCH_SIZE, verbose=1)
        self.model.save(MODEL_PATH)
        print("✅ AI Model Training Complete & Saved.")

# 🚀 TRAIN THE MODEL
if __name__ == "__main__":
    trainer = TrainTransformer()
    trainer.train_model()
