
from ..BaseStrategy import BaseStrategy
from .Algorithm import BuyHoldAlgorithm

class BuyHold(BaseStrategy):
    def __init__(self, tickers, balance=10000):
        super().__init__(tickers=tickers, balance=balance, Algorithm=BuyHoldAlgorithm)

    def get_profits(self):
        return super().get_profits()