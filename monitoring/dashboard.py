# dashboard.py
# ==================================================
# 📊 TRADING DASHBOARD – MONITORS LIVE PERFORMANCE 📊
# ==================================================

from flask import Flask, render_template, jsonify
from core.exchange_connector import ExchangeConnector
from utilities.profit_tracker import ProfitTracker
import logging

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Initialize Trading Components
exchange = ExchangeConnector()
profit_tracker = ProfitTracker()

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    """Displays the real-time trading dashboard."""
    return render_template("dashboard.html")

@app.route("/status")
def get_status():
    """
    Returns real-time trading data as JSON.
    """
    try:
        balance = exchange.fetch_balance()
        open_trades = exchange.fetch_open_orders()
        profit_loss = profit_tracker.get_summary()

        return jsonify({
            "balance": balance,
            "open_trades": open_trades,
            "profit_loss": profit_loss
        })
    except Exception as e:
        logging.error(f"❌ Error Fetching Dashboard Data: {e}")
        return jsonify({"error": "Unable to fetch trading data"}), 500

# 🚀 START DASHBOARD
if __name__ == "__main__":
    import os
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    print("🚀 Dashboard Running at http://127.0.0.1:5000")
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
