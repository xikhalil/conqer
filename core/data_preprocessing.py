# ==================================================
# 📊 DATA PREPROCESSING – CLEANS & FORMATS MARKET DATA 📊
# ==================================================

import pandas as pd
import numpy as np
import ta  # ✅ Technical Analysis Library
from custom_logging.logger import Logger


class DataPreprocessing:
    def __init__(self, df):
        """
        Initializes the data preprocessing module.
        Args:
            df (pd.DataFrame): Raw market data.
        """
        self.df = df.copy()

    def apply_technical_indicators(self):
        """
        Applies RSI, MACD, Volatility, and other indicators to the dataset.
        Returns:
            pd.DataFrame: Market data with indicators.
        """
        try:
            # ✅ Ensure 'close' column exists
            if "close" not in self.df.columns:
                Logger.error("❌ Missing 'close' price data in DataFrame.")
                return self.df

            Logger.info("📊 Applying Technical Indicators...")

            # ✅ Relative Strength Index (RSI)
            self.df["rsi"] = ta.momentum.RSIIndicator(self.df["close"], window=14).rsi()

            # ✅ Moving Average Convergence Divergence (MACD)
            macd = ta.trend.MACD(self.df["close"])
            self.df["macd"], self.df["signal"] = macd.macd(), macd.macd_signal()

            # ✅ Volatility (Rolling Standard Deviation)
            self.df["volatility"] = self.df["close"].rolling(window=10).std()

            # ✅ Momentum (Percentage Change)
            self.df["momentum"] = self.df["close"].pct_change()

            # ✅ Fix missing values after calculations
            self.df.fillna(method="bfill", inplace=True)  # Backfill missing values
            self.df.dropna(inplace=True)  # Drop remaining NaNs

            Logger.info("✅ Technical Indicators Applied Successfully.")
            return self.df

        except Exception as e:
            Logger.error(f"❌ Error Applying Technical Indicators: {e}")
            return self.df

    def clean_data(self):
        """
        Handles missing values, removes infinite values, and ensures clean data.
        Returns:
            pd.DataFrame: Cleaned market data.
        """
        Logger.info("🧹 Cleaning Data...")

        # ✅ Replace infinite values with NaN
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # ✅ Fill missing values with the previous valid observation
        self.df.fillna(method="bfill", inplace=True)
        self.df.dropna(inplace=True)

        Logger.info("✅ Data Cleaning Complete.")
        return self.df

    def preprocess(self):
        """
        Runs all preprocessing steps and returns cleaned data.
        Returns:
            pd.DataFrame: Fully processed market data.
        """
        self.apply_technical_indicators()
        return self.clean_data()

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    # Sample raw data
    raw_data = {
        "close": [50000, 50200, 50500, 50700, 51000, 51500, 52000, 53000, 54000]
    }
    df = pd.DataFrame(raw_data)

    processor = DataPreprocessing(df)
    cleaned_df = processor.preprocess()

    print("✅ Processed Data:\n", cleaned_df)
