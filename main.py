'''
Author - Ken Cou
Algorithmic Trade Algorithm
'''

from BackTest.BuyHold.BuyHold import BuyHold
from BackTest.TrailingStopLoss.TrailingStopLoss import TrailingStopLoss
from BackTest.GridTrading.GridTrading import GridTrading

def _pp(a, b):
    # percent gain from a -> b
    return (b - a) / a * 100.0 if a else 0.0

def _fmt(v):  # money
    return f"${v:,.2f}"

def _fmtp(p):  # percent
    sign = "+" if p >= 0 else ""
    return f"{sign}{p:.2f}%"

if __name__ == "__main__":
    tickers = [ "AMD", "NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    balance = 10_000

    buyHold = BuyHold(tickers, balance)
    tsl = TrailingStopLoss(tickers, balance)
    gt = GridTrading(tickers, balance)

    bh_vals = buyHold.get_profits()
    tsl_vals = tsl.get_profits()
    gt_vals  = gt.get_profits()

    # header
    print("\n=== Strategy Comparison vs Buy&Hold ===")
    print("BH = Buy&Hold, TSL = Trailing Stop Loss, Grid = Grid Trading")
    print(f"{'Ticker':6}  {'Buy&Hold':>12}  {'TSL':>12}  {'Δ TSL vs BH':>12}  {'Δ% TSL':>9}  {'Grid':>12}  {'Δ Grid vs BH':>12}  {'Δ% Grid':>9}")
    print("-" * 100)

    # rows
    tot_bh = tot_tsl = tot_gt = 0.0
    for tk, bh, tslv, gtv in zip(tickers, bh_vals, tsl_vals, gt_vals):
        d_tsl = tslv - bh
        d_gt  = gtv  - bh
        print(f"{tk:6}  {_fmt(bh):>12}  {_fmt(tslv):>12}  {_fmt(d_tsl):>12}  {_fmtp(_pp(bh, tslv)):>9}  "
              f"{_fmt(gtv):>12}  {_fmt(d_gt):>12}  {_fmtp(_pp(bh, gtv)):>9}")
        tot_bh  += bh
        tot_tsl += tslv
        tot_gt  += gtv

    # totals
    print("-" * 100)
    d_tsl_tot = tot_tsl - tot_bh
    d_gt_tot  = tot_gt  - tot_bh
    print(f"{'TOTAL':6}  {_fmt(tot_bh):>12}  {_fmt(tot_tsl):>12}  {_fmt(d_tsl_tot):>12}  {_fmtp(_pp(tot_bh, tot_tsl)):>9}  "
          f"{_fmt(tot_gt):>12}  {_fmt(d_gt_tot):>12}  {_fmtp(_pp(tot_bh, tot_gt)):>9}\n")