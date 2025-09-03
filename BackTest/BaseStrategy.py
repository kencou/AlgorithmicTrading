from abc import ABC, abstractmethod
from typing import List
from MarketData.getData import MarketData

class BaseStrategy(ABC):
    """Abstract base for all trading strategies."""
    def __init__(self, tickers: List[str], balance, Algorithm):
        self.tickers = sorted(tickers)
        self.balance = balance
        if (Algorithm is None):
            raise ValueError("Algorithm class must be provided")
        self.Algorithm = Algorithm

    @abstractmethod
    def get_profits(self) -> List[float]:
        result = []
        splitted_balance = self.balance / len(self.tickers)
        for ticker in self.tickers:
            md = MarketData(ticker)
            cur_ticker_prices = md.get_hourly_prices()
            myStrategy = self.Algorithm(balance=splitted_balance)
            trailingstop_amount = myStrategy.run(cur_ticker_prices)
            result.append(trailingstop_amount)
        return self._validate_output(result)

    def _validate_output(self, values: List[float]) -> List[float]:
        if len(values) != len(self.tickers):
            raise ValueError(
                f"Output length {len(values)} does not match tickers {len(self.tickers)}"
            )
        return values