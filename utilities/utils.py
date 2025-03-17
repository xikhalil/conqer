# utils.py
# ==================================================
# ⚙️ UTILITY FUNCTIONS – GENERAL HELPER MODULE ⚙️
# ==================================================

import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class Utils:
    @staticmethod
    def format_timestamp(timestamp):
        """
        Converts a Unix timestamp to a human-readable format.
        Args:
            timestamp (float): Unix timestamp.
        Returns:
            str: Formatted date-time string.
        """
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def log_message(message, level="info"):
        """
        Logs messages to the system log file.
        Args:
            message (str): The message to log.
            level (str): Log level ("info", "warning", "error").
        """
        if level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        print(f"📜 {message}")  # Also print to console

    @staticmethod
    def retry_function(func, retries=3, delay=2):
        """
        Retries a function if it fails.
        Args:
            func (function): The function to retry.
            retries (int): Number of retry attempts.
            delay (int): Delay between retries (in seconds).
        Returns:
            Any: Function output or None if all retries fail.
        """
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                Utils.log_message(f"Attempt {attempt + 1}/{retries} failed: {e}", "warning")
                time.sleep(delay)
        return None

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    Utils.log_message("Bot has started.", "info")
    timestamp = Utils.format_timestamp(time.time())
    print(f"🕒 Current Time: {timestamp}")
