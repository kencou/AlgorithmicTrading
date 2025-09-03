from ..BaseAlgorithm import BaseAlgorithm

class BuyHoldAlgorithm(BaseAlgorithm):
    def __init__(self, balance, allow_fractional_shares=True):
        self.balance = float(balance)
        self.allow_fractional = allow_fractional_shares

    def run(self, prices) -> float:
        if not prices:
            raise ValueError("Need at least 1 price.")
        buy_px = prices[0]
        qty = self.balance / buy_px
        if not self.allow_fractional:
            qty = int(qty)
        cash = self.balance - qty * buy_px  # leftover after initial buy
        return cash + qty * prices[-1]      # sell all at the end
