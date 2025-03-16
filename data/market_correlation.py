# market_correlation.py
# ==================================================
# 📈 MARKET CORRELATION ANALYZER 📈
# ==================================================

import numpy as np
import pandas as pd

class MarketCorrelation:
    def __init__(self, historical_data):
        """
        Initialize market correlation analysis.
        Args:
            historical_data (dict): Dictionary of historical price data per asset.
        """
        self.data = historical_data

    def calculate_correlation_matrix(self):
        """
        Computes the correlation matrix of multiple assets.
        Returns:
            DataFrame: Correlation matrix.
        """
        df = pd.DataFrame(self.data)
        return df.corr(method="pearson")  # ✅ More accurate correlation calculation

    def find_best_hedge_asset(self, asset):
        """
        Finds the best hedge asset for a given trading pair.
        Args:
            asset (str): The asset to hedge.
        Returns:
            str: Best hedge asset.
        """
        correlation_matrix = self.calculate_correlation_matrix()

        if asset not in correlation_matrix.columns:
            print(f"⚠️ Asset {asset} not found in correlation data.")
            return None

        correlated_assets = correlation_matrix[asset].sort_values(ascending=False)
        return correlated_assets.index[1]  # Most correlated asset (excluding itself)
