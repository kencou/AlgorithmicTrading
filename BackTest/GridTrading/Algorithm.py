from ..BaseAlgorithm import BaseAlgorithm

class GridTradingAlgorithm(BaseAlgorithm):
    """
    Buy if price drops 5% from last ref (use 12% of remaining cash).
    Sell if price rises 10% from last ref (sell 8% of current shares).
    Ref price resets after each trade. Starts by investing start_invest_frac.
    """

    def __init__(self, balance: float,
                 start_invest_frac: float = 0.75,
                 buy_trigger_pct: float = 0.05,      # 5% down
                 sell_trigger_pct: float = 0.08,     # 8% up
                 buy_cash_fraction: float = 0.10,    # 10% of cash on buys
                 sell_position_fraction: float = 0.10,  # 8% of shares on sells
                 fee_rate_bps: float = 0.0,
                 slippage_rate_bps: float = 0.0):
        self.balance = float(balance)
        self.start_invest_frac = float(start_invest_frac)
        self.buy_trig = float(buy_trigger_pct)
        self.sell_trig = float(sell_trigger_pct)
        self.buy_frac = float(buy_cash_fraction)
        self.sell_frac = float(sell_position_fraction)
        self.fee = float(fee_rate_bps) / 10_000.0
        self.slip = float(slippage_rate_bps) / 10_000.0

    def run(self, prices) -> float:
        if not prices or len(prices) < 2:
            raise ValueError("Need at least 2 prices.")

        cash, shares = self.balance, 0.0
        ref = float(prices[0])

        # initial buy: invest start_invest_frac of cash at first price
        buy_px = ref * (1 + self.slip)
        qty = (cash * self.start_invest_frac) / buy_px
        cost = qty * buy_px
        fee = cost * self.fee
        if qty > 0 and cost + fee <= cash:
            cash -= cost + fee
            shares += qty

        for px in map(float, prices[1:]):
            # BUY: price dropped >= 5% from ref
            if px <= ref * (1 - self.buy_trig) and cash > 0:
                buy_px = px * (1 + self.slip)
                spend = cash * self.buy_frac
                qty = spend / buy_px
                cost = qty * buy_px
                fee = cost * self.fee
                if qty > 0 and cost + fee <= cash:
                    cash -= cost + fee
                    shares += qty
                    ref = px

            # SELL: price rose >= 10% from ref
            elif shares > 0 and px >= ref * (1 + self.sell_trig):
                sell_px = px * (1 - self.slip)
                qty = shares * self.sell_frac
                proceeds = qty * sell_px
                fee = proceeds * self.fee
                if qty > 0:
                    cash += proceeds - fee
                    shares -= qty
                    ref = px

        return cash + shares * float(prices[-1])
