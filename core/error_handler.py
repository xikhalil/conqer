# ==================================================
# ⚠️ ERROR HANDLER – MANAGES API FAILURES & RETRIES ⚠️
# ==================================================

import time
import ccxt
from custom_logging.logger import Logger


class ErrorHandler:
    MAX_RETRIES = 3  # ✅ Limits retries to prevent infinite loops

    @staticmethod
    def handle_error(error, context="Unknown"):
        """
        Handles errors gracefully, logs them, and decides whether to retry.
        Args:
            error (Exception): The exception that occurred.
            context (str): Context where the error happened.
        Returns:
            bool: True if the operation should be retried, False otherwise.
        """
        Logger.error(f"❌ ERROR in {context}: {str(error)}")

        # ✅ Handle CCXT-Specific Errors
        if isinstance(error, ccxt.NetworkError):
            Logger.warning("🌐 Network Error detected. Retrying...")
            return True  # Retry operation

        elif isinstance(error, ccxt.ExchangeError):
            Logger.critical("❌ Exchange API Error. Check API settings or rate limits.")
            return False  # Do NOT retry

        elif isinstance(error, ccxt.BadSymbol):
            Logger.critical("⚠️ Invalid trading pair. Check the symbol format.")
            return False  # Do NOT retry

        # ✅ Generic error handling (e.g., temporary failures)
        Logger.warning("🔁 Retrying operation after unexpected error...")
        return True  # Retry operation

    @staticmethod
    def safe_execute(func, *args, **kwargs):
        """
        Executes a function with built-in error handling and retry mechanism.
        Args:
            func (callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        Returns:
            Any: The function result if successful, or None if failed.
        """
        retries = 0
        while retries < ErrorHandler.MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not ErrorHandler.handle_error(e, func.__name__):
                    return None  # Do NOT retry if error is critical
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff before retrying

        Logger.critical(f"🚨 MAX RETRIES REACHED for {func.__name__}. Skipping operation.")
        return None  # Final failure case

# 🚀 TEST ERROR HANDLER (DEBUG ONLY)
if __name__ == "__main__":
    def test_function():
        raise ccxt.NetworkError("Simulated Network Failure")

    print("🛠️ Testing Safe Execution:")
    ErrorHandler.safe_execute(test_function)
