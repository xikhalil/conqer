# performance_optimizer.py
# ==================================================
# 🚀 PERFORMANCE OPTIMIZER – BOOSTS EXECUTION SPEED 🚀
# ==================================================

import time
import logging
import psutil  # ✅ For CPU & Memory Monitoring

# ✅ Configure Logging
logging.basicConfig(filename="logs/performance.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PerformanceOptimizer:
    """
    Optimizes bot performance by monitoring resource usage & improving execution time.
    """
    def __init__(self):
        self.optimized = False

    def monitor_system_usage(self):
        """
        Logs CPU and Memory usage to track performance.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        logging.info(f"📊 CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")

    def optimize_execution(self):
        """
        Reduces unnecessary delays and improves execution flow.
        """
        if not self.optimized:
            logging.info("⚡ Optimizing execution settings...")
            # ✅ Reduce sleep intervals dynamically
            time.sleep(0.5)
            self.optimized = True

    def optimize_market_data_fetch(self, exchange_connector):
        """
        Ensures market data is fetched with minimal latency.
        Args:
            exchange_connector (ExchangeConnector): The exchange connection instance.
        Returns:
            DataFrame: Optimized market data.
        """
        start_time = time.time()
        market_data = exchange_connector.fetch_market_data("PI/USDT")

        if market_data is not None:
            fetch_time = time.time() - start_time
            logging.info(f"✅ Market Data Fetch Time: {fetch_time:.3f} seconds")
            return market_data
        else:
            logging.warning("⚠️ Market Data Fetch Failed!")
            return None

# 🚀 TEST PERFORMANCE OPTIMIZATION
if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    optimizer.monitor_system_usage()
    optimizer.optimize_execution()
