from ..BaseAlgorithm import BaseAlgorithm

class GridTradingAlgorithm(BaseAlgorithm):
    """
    Simple grid trading algorithm.

    Rules:
      - Start by investing `start_invest_frac` of your balance on the first price.
      - If price drops by `grid_pct` from last reference → BUY.
      - If price rises by `grid_pct` from last reference → SELL.
      - Each trade uses `trade_fraction` of current cash (for buys) or equivalent sizing (for sells).
      - After each trade, reset reference price to the latest traded price.
    """

    def __init__(self, balance: float,
                 start_invest_frac: float = 0.75,   # fraction of balance to invest initially
                 grid_pct: float = 0.05,            # threshold % move up/down to trigger trades
                 trade_fraction: float = 0.10,      # fraction of cash to use each trade
                 fee_rate_bps: float = 0.0,         # trading fee in basis points (1 bps = 0.01%)
                 slippage_rate_bps: float = 0.0):    # slippage in basis points on execution
        self.balance = float(balance)
        self.start_invest_frac = start_invest_frac
        self.grid_pct = grid_pct
        self.trade_fraction = trade_fraction
        self.fee = fee_rate_bps / 10_000.0
        self.slip = slippage_rate_bps / 10_000.0

    def run(self, prices) -> float:
        """
        Backtest on a sequence of prices.
        Returns final equity (cash + shares * last_price).
        """
        if not prices or len(prices) < 2:
            raise ValueError("Need at least 2 prices.")

        cash, shares = self.balance, 0.0
        ref = prices[0]

        # --- initial buy ---
        buy_px = ref * (1 + self.slip)
        qty = (cash * self.start_invest_frac) / buy_px
        cost, fee = qty * buy_px, (qty * buy_px) * self.fee
        if qty > 0 and cost + fee <= cash:
            cash -= cost + fee
            shares += qty

        # --- main loop ---
        for px in prices[1:]:
            # BUY trigger
            if px <= ref * (1 - self.grid_pct) and cash > 0:
                buy_px = px * (1 + self.slip)
                trade_cash = cash * self.trade_fraction
                qty = trade_cash / buy_px
                cost, fee = qty * buy_px, (qty * buy_px) * self.fee
                if qty > 0 and cost + fee <= cash:
                    cash -= cost + fee
                    shares += qty
                    ref = px
            # SELL trigger
            elif shares > 0 and px >= ref * (1 + self.grid_pct):
                sell_px = px * (1 - self.slip)
                qty = (cash * self.trade_fraction) / sell_px
                qty = min(qty, shares)
                proceeds, fee = qty * sell_px, (qty * sell_px) * self.fee
                if qty > 0:
                    cash += proceeds - fee
                    shares -= qty
                    ref = px

        return cash + shares * prices[-1]