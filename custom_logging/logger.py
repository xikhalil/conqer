import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

class Logger:
    """Handles logging for trading bot operations."""

    # Create directory for log file if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Set up rotating log handler with max size of 10 MB and backup count of 5
    log_handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')

    # Get log level from environment variable (default to INFO if not set)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        handlers=[
            log_handler,
            logging.StreamHandler()
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
    def error(message, exc_info=False):
        """Logs an error message with optional stack trace."""
        logging.error(message, exc_info=exc_info)

# 🚀 TEST LOGGER
if __name__ == "__main__":
    Logger.info("✅ Logger Initialized Successfully.")
    Logger.warning("⚠️ This is a warning message.")
    try:
        raise ValueError("This is a test error")
    except Exception as e:
        Logger.error("❌ This is an error message.", exc_info=True)
