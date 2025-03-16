# logger.py
# ==================================================
# 📝 LOGGER – HANDLES STRUCTURED LOGGING FOR SYSTEM EVENTS 📝
# ==================================================

import logging
import os
from config import LOG_FILE

class Logger:
    """Handles logging for trading bot operations."""

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()  # ✅ Logs to console
        ]
    )

    @staticmethod
    def info(message):
        """Logs an informational message."""
        logging.info(message)

    @staticmethod
    def warning(message):
        """Logs a warning message."""
        logging.warning(message)

    @staticmethod
    def error(message):
        """Logs an error message."""
        logging.error(message)

# 🚀 TEST LOGGER
if __name__ == "__main__":
    Logger.info("✅ Logger Initialized Successfully.")
    Logger.warning("⚠️ This is a warning message.")
    Logger.error("❌ This is an error message.")
