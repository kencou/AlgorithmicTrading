
from ..BaseStrategy import BaseStrategy
from .Algorithm import GridTradingAlgorithm

class GridTrading(BaseStrategy):
    def __init__(self, tickers, balance=10000):
        super().__init__(tickers=tickers, balance=balance, Algorithm=GridTradingAlgorithm)

    def get_profits(self):
        return super().get_profits()