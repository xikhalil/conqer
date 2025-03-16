# risk_management.py
# ==================================================
# 🛡️ RISK MANAGEMENT – PROTECTS TRADING STRATEGY 🛡️
# ==================================================

from config import STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, RISK_PER_TRADE, ORDER_MINIMUM_VALUE
from utils.logger import Logger
import pandas as pd

def calculate_risk_levels(entry_price, trade_type):
    """
    Calculates stop-loss & take-profit levels dynamically.
    Args:
        entry_price (float): The price where trade is executed.
        trade_type (str): "BUY" or "SELL".
    Returns:
        dict: Stop-loss and take-profit prices.
    """
    if trade_type == "BUY":
        stop_loss = entry_price * (1 - STOP_LOSS_PERCENT)
        take_profit = entry_price * (1 + TAKE_PROFIT_PERCENT)
    else:  # SELL
        stop_loss = entry_price * (1 + STOP_LOSS_PERCENT)
        take_profit = entry_price * (1 - TAKE_PROFIT_PERCENT)

    Logger.info(f"📊 Risk Levels | {trade_type}: Stop-Loss: {stop_loss:.6f}, Take-Profit: {take_profit:.6f}")
    return {"stop_loss": stop_loss, "take_profit": take_profit}

def validate_trade(trade_signal, market_data, balance):
    """
    Validates a trade before execution, ensuring proper risk management.
    Args:
        trade_signal (str): "BUY" or "SELL".
        market_data (DataFrame): Market data for analysis.
        balance (dict): Available balance in USDT & assets.
    Returns:
        dict: Trade validation result.
    """
    if trade_signal not in ["BUY", "SELL"]:
        return {"valid": False, "reason": "Invalid trade signal"}

    latest_price = market_data["close"].iloc[-1]

    # ✅ Check if there is enough balance for the trade
    if trade_signal == "BUY" and balance["USDT"] < latest_price:
        Logger.warning("⚠️ Trade not valid: Not enough USDT to buy.")
        return {"valid": False, "reason": "Not enough USDT to buy"}

    if trade_signal == "SELL" and balance["PI"] <= 0:
        Logger.warning("⚠️ Trade not valid: Not enough PI to sell.")
        return {"valid": False, "reason": "Not enough PI to sell"}

    # ✅ Calculate Trade Size (based on risk per trade)
    position_size = (balance["USDT"] * RISK_PER_TRADE) / latest_price if trade_signal == "BUY" else balance["PI"] * RISK_PER_TRADE
    position_size = round(position_size, 6)

    # ✅ Ensure trade meets minimum exchange size
    min_trade_size = max(ORDER_MINIMUM_VALUE / latest_price, 0.01)
    if position_size < min_trade_size:
        Logger.warning(f"⚠️ Trade size too small: {position_size} PI. Adjusting to minimum: {min_trade_size} PI.")
        position_size = min_trade_size

    if position_size * latest_price < ORDER_MINIMUM_VALUE:
        Logger.warning("⚠️ Trade size below exchange minimum order value. Trade skipped.")
        return {"valid": False, "reason": "Trade size too small"}

    # ✅ Apply Risk Management
    risk_levels = calculate_risk_levels(latest_price, trade_signal)

    Logger.info(f"✅ Trade Validated | {trade_signal}: Size {position_size}, Entry {latest_price}")
    return {
        "valid": True,
        "position_size": position_size,
        "entry_price": latest_price,
        "stop_loss": risk_levels['stop_loss'],
        "take_profit": risk_levels['take_profit']
    }

# 🚀 EXAMPLE USAGE
if __name__ == "__main__":
    sample_data = pd.DataFrame({"close": [50000, 50200, 50500, 50700, 51000]})
    balance = {"USDT": 1000, "PI": 2}

    validation = validate_trade("BUY", sample_data, balance)
    print("📊 Trade Validation Result:", validation)
