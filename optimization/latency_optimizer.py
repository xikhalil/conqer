# latency_optimizer.py
# ==================================================
# 🚀 LATENCY OPTIMIZER – REDUCES EXECUTION DELAY 🚀
# ==================================================

import requests
import time
import threading
from core.exchange_connector import ExchangeConnector
from config import LATENCY_OPTIMIZATION

class LatencyOptimizer:
    def __init__(self):
        """Initialize latency optimizer."""
        self.exchange = ExchangeConnector()
        self.api_url = self.exchange.exchange.urls['api']

    def measure_latency(self):
        """
        Measures API response time to detect delays.
        Returns:
            float: Latency in milliseconds.
        """
        start_time = time.time()
        try:
            requests.get(self.api_url, timeout=2)  # Send test request to exchange
        except requests.exceptions.RequestException:
            return float("inf")  # High latency (request failed)
        return (time.time() - start_time) * 1000  # Convert to ms

    def optimize_trade_execution(self):
        """
        Optimizes trade execution speed by preloading API connections.
        """
        if not LATENCY_OPTIMIZATION:
            print("⚠️ Latency optimization is disabled.")
            return

        latency = self.measure_latency()
        print(f"⏳ Current API Latency: {latency:.2f}ms")

        if latency > 200:  # If latency > 200ms, attempt optimizations
            print("⚠️ High latency detected! Adjusting network settings...")
            self.exchange.exchange.enableRateLimit = False  # Disable rate limit for faster requests
            self.exchange.exchange.verbose = False  # Reduce API logging output
        else:
            print("✅ Low-latency conditions. No optimization needed.")

    def start_latency_monitor(self):
        """
        Continuously monitors & optimizes API latency.
        """
        while True:
            self.optimize_trade_execution()
            time.sleep(10)  # Check every 10 seconds

# 🚀 START LATENCY MONITORING
if __name__ == "__main__":
    print("🚀 LATENCY OPTIMIZER ACTIVATED 🚀")
    optimizer = LatencyOptimizer()
    latency_thread = threading.Thread(target=optimizer.start_latency_monitor)
    latency_thread.start()
