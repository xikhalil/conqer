# cross_exchange_arbitrage.py
# ==================================================
# 🔄 CROSS-EXCHANGE ARBITRAGE – TRADES BETWEEN EXCHANGES 🔄
# ==================================================

from core.exchange_connector import ExchangeConnector
from config import ENABLE_CROSS_EXCHANGE_ARBITRAGE

class CrossExchangeArbitrage:
    def __init__(self):
        """Initialize cross-exchange arbitrage system."""
        self.exchange = ExchangeConnector()

    def transfer_asset(self, from_exchange, to_exchange, asset, amount):
        """
        Transfers an asset between exchanges.
        Args:
            from_exchange (str): Exchange to withdraw from.
            to_exchange (str): Exchange to deposit into.
            asset (str): Asset to transfer.
            amount (float): Amount of asset to transfer.
        """
        print(f"🔄 Transferring {amount} {asset} from {from_exchange} to {to_exchange}...")
        self.exchange.withdraw_asset(from_exchange, asset, amount, to_exchange)

    def execute_cross_exchange_arbitrage(self, buy_exchange, sell_exchange, asset, buy_price, sell_price):
        """
        Executes an arbitrage trade between two exchanges.
        """
        print(f"💰 Executing cross-exchange arbitrage: Buying {asset} on {buy_exchange} and selling on {sell_exchange}")

        self.exchange.create_market_order(buy_exchange, asset, "buy", 0.1)
        self.transfer_asset(buy_exchange, sell_exchange, asset, 0.1)
        self.exchange.create_market_order(sell_exchange, asset, "sell", 0.1)
