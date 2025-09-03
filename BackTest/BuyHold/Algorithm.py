from ..BaseAlgorithm import BaseAlgorithm

class BuyHoldAlgorithm(BaseAlgorithm):
    def __init__(self, balance, fee_rate_bps: float = 0.0, tax_rate: float = 0.0):
        """
        :param balance: starting cash
        :param fee_rate_bps: trading fee in basis points (1 bps = 0.01%), applied on buy and sell
        :param tax_rate: tax on profits (e.g. 0.15 = 15% tax)
        """
        self.balance = float(balance)
        self.fee = fee_rate_bps / 10_000.0
        self.tax = float(tax_rate)

    def run(self, prices) -> float:
        if not prices:
            raise ValueError("Need at least 1 price.")

        cash = self.balance
        buy_px = prices[0]

        # initial buy
        qty = cash / buy_px
        cost = qty * buy_px
        fee = cost * self.fee
        cash -= cost + fee

        # final sell
        sell_px = prices[-1]
        proceeds = qty * sell_px
        fee = proceeds * self.fee
        cash += proceeds - fee

        # tax on profits
        profit = cash - self.balance
        if profit > 0 and self.tax > 0:
            cash -= profit * self.tax

        return cash
