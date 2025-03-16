# stress_tester.py
# ==================================================
# 🏋️ SYSTEM STRESS TEST – SIMULATES EXTREME CONDITIONS 🏋️
# ==================================================

import time
import random
import logging
from core.exchange_connector import ExchangeConnector
from config import PAIR, STRESS_TEST_TRADES

# ✅ Configure Logging
logging.basicConfig(
    filename="logs/stress_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class StressTester:
    def __init__(self, num_trades=STRESS_TEST_TRADES):
        """
        Initializes the stress test.
        Args:
            num_trades (int): Number of simulated trades.
        """
        self.exchange = ExchangeConnector()
        self.num_trades = num_trades

    def simulate_trades(self):
        """
        Simulates a large number of trades rapidly to test system performance.
        """
        print(f"🚀 Starting Stress Test: {self.num_trades} trades")
        logging.info(f"🏋️ Running stress test with {self.num_trades} trades...")

        for i in range(self.num_trades):
            trade_type = random.choice(["BUY", "SELL"])
            trade_size = round(random.uniform(0.01, 0.1), 4)

            print(f"🔄 Simulating {trade_type} trade {i+1}/{self.num_trades} for {trade_size} {PAIR}")
            logging.info(f"🔄 Trade {i+1}/{self.num_trades}: {trade_type} {trade_size} {PAIR}")

            try:
                if trade_type == "BUY":
                    self.exchange.create_market_buy_order(PAIR, trade_size)
                else:
                    self.exchange.create_market_sell_order(PAIR, trade_size)
            except Exception as e:
                print(f"❌ Trade execution failed: {e}")
                logging.error(f"❌ Error executing trade {i+1}: {e}")

            time.sleep(0.1)  # Simulate trade delay

        print("✅ Stress test completed successfully.")
        logging.info("🏁 Stress test completed.")

# 🚀 RUN STRESS TEST
if __name__ == "__main__":
    tester = StressTester()
    tester.simulate_trades()
