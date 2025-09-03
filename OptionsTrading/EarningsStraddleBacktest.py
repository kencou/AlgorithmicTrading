# OptionsTrading/EarningsStraddleBacktest.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm


# ---------- Black–Scholes helpers ----------
def _d1(S, K, T, r, sigma):
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def _d2(S, K, T, r, sigma):
    d1 = _d1(S, K, T, r, sigma)
    if np.isnan(d1):
        return np.nan
    return d1 - sigma * np.sqrt(T)

def bs_call(S, K, T, r, sigma):
    if T <= 0:
        return max(S - K, 0.0)
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bs_put(S, K, T, r, sigma):
    if T <= 0:
        return max(K - S, 0.0)
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def bs_straddle(S, K, T, r, sigma):
    return bs_call(S, K, T, r, sigma) + bs_put(S, K, T, r, sigma)


# ---------- Config & result ----------
@dataclass
class StraddleBTConfig:
    r_annual: float = 0.03
    hv_lookback_days: int = 21
    crush_ratio: float = 0.55
    max_events: int = 24
    exit_when: str = "next_close"  # or "earnings_close"

@dataclass
class TradeResult:
    ticker: str
    earnings_dt: pd.Timestamp
    entry_date: pd.Timestamp
    exit_date: pd.Timestamp
    S0: float
    S1: float
    K: float
    T_entry: float
    T_exit: float
    sigma_entry: float
    sigma_exit: float
    cost_entry: float
    value_exit: float
    pnl: float
    pnl_pct_of_cost: float
    abs_move_pct: float


# ---------- Helpers ----------
def _nearest_friday_on_or_after(d: pd.Timestamp) -> pd.Timestamp:
    offset = (4 - d.weekday()) % 7
    return (d + pd.Timedelta(days=offset)).normalize()

def _prev_trading_day(price_index: pd.DatetimeIndex, ref: pd.Timestamp) -> Optional[pd.Timestamp]:
    candidates = price_index[price_index < ref]
    return candidates.max() if len(candidates) else None

def _next_trading_day(price_index: pd.DatetimeIndex, ref: pd.Timestamp) -> Optional[pd.Timestamp]:
    candidates = price_index[price_index > ref]
    return candidates.min() if len(candidates) else None

def _annualized_hv(returns: pd.Series, trading_days: int = 252) -> float:
    if returns.dropna().empty:
        return np.nan
    return (returns.std(ddof=1) * np.sqrt(trading_days)).item()


# ---------- Backtest ----------
def backtest_earnings_straddles(ticker: str, cfg: StraddleBTConfig = StraddleBTConfig()) -> pd.DataFrame:
    tkr = yf.Ticker(ticker)

    edf = tkr.get_earnings_dates(limit=cfg.max_events)
    if edf is None or edf.empty:
        raise ValueError(f"No earnings dates for {ticker}")

    if "Earnings Date" in edf.columns:
        earnings_dates = pd.to_datetime(edf["Earnings Date"]).dt.tz_localize(None).sort_values()
    else:
        earnings_dates = pd.to_datetime(edf.index).tz_localize(None).sort_values()

    start = (earnings_dates.min() - pd.Timedelta(days=120)).strftime("%Y-%m-%d")
    end   = (earnings_dates.max() + pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    px = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True, progress=False)
    if px.empty:
        raise ValueError(f"No price history for {ticker}")
    px.index = pd.to_datetime(px.index).tz_localize(None)

    results: List[TradeResult] = []

    for dt in earnings_dates:
        dt = pd.Timestamp(dt).normalize()
        entry_date = _prev_trading_day(px.index, dt)
        exit_date = _next_trading_day(px.index, dt) if cfg.exit_when == "next_close" else dt
        if entry_date is None or exit_date is None:
            continue

        S0 = px.loc[entry_date, "Close"].item()
        S1 = px.loc[exit_date, "Close"].item()
        K = round(S0)

        expiry = _nearest_friday_on_or_after(dt)
        if expiry <= exit_date:
            expiry = _nearest_friday_on_or_after(exit_date)

        T_entry = max((expiry - entry_date).days, 0) / 365.0
        T_exit  = max((expiry - exit_date).days, 0) / 365.0

        lookback_start = _prev_trading_day(px.index, entry_date - pd.Timedelta(days=cfg.hv_lookback_days - 1))
        if lookback_start is None:
            continue
        hist = px.loc[lookback_start:entry_date, "Close"].pct_change().dropna()
        sigma_entry = _annualized_hv(np.log1p(hist))
        if not np.isfinite(sigma_entry) or sigma_entry <= 0:
            continue

        sigma_exit = max(1e-6, cfg.crush_ratio * sigma_entry)

        cost_entry = bs_straddle(S0, K, T_entry, cfg.r_annual, sigma_entry)
        value_exit = bs_straddle(S1, K, T_exit, cfg.r_annual, sigma_exit)
        if not (np.isfinite(cost_entry) and np.isfinite(value_exit)):
            continue

        pnl = value_exit - cost_entry
        pnl_pct = pnl / cost_entry if cost_entry > 0 else np.nan
        abs_move_pct = abs(S1 / S0 - 1.0)

        results.append(TradeResult(
            ticker=ticker.upper(),
            earnings_dt=dt,
            entry_date=entry_date,
            exit_date=exit_date,
            S0=S0, S1=S1, K=K,
            T_entry=T_entry, T_exit=T_exit,
            sigma_entry=sigma_entry, sigma_exit=sigma_exit,
            cost_entry=cost_entry, value_exit=value_exit,
            pnl=pnl, pnl_pct_of_cost=pnl_pct,
            abs_move_pct=abs_move_pct
        ))

    df = pd.DataFrame([r.__dict__ for r in results])
    if not df.empty:
        df.sort_values("earnings_dt", inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df


# ---------- CLI ----------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Model-based earnings straddle backtest.")
    parser.add_argument("ticker", type=str)
    parser.add_argument("--events", type=int, default=24)
    parser.add_argument("--crush", type=float, default=0.55)
    parser.add_argument("--hv", type=int, default=21)
    parser.add_argument("--r", type=float, default=0.03)
    parser.add_argument("--exit", type=str, default="next_close", choices=["next_close", "earnings_close"])
    args = parser.parse_args()

    cfg = StraddleBTConfig(
        r_annual=args.r,
        hv_lookback_days=args.hv,
        crush_ratio=args.crush,
        max_events=args.events,
        exit_when=args.exit,
    )
    out = backtest_earnings_straddles(args.ticker, cfg)
    print(out.tail(10))
    if not out.empty:
        print("\nSummary:")
        print(out[["pnl", "pnl_pct_of_cost"]].describe())
