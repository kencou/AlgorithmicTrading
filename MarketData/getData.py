# MarketData/getData.py
from __future__ import annotations

from typing import List, Optional
import pandas as pd
import yfinance as yf


class MarketData:
    """
    Minimal helper focused on HOURLY prices.
    - No local storage.
    - get_hourly_prices(): returns list of hourly Close prices, most-recent last.
    """

    _MAX_HOURLY_LOOKBACK_DAYS = 730  # Yahoo cap for 60m bars

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker.upper().strip()

    def get_hourly_prices(
        self,
        lookback_days: Optional[int] = None, # how many days back to fetch
        rth_only: bool = False, # regular trading hours only
        auto_adjust: bool = True, # adjust for splits/dividends
    ) -> List[float]:
        """
        Fetch hourly bars and return a list of Close prices (floats).

        Parameters
        ----------
        lookback_days : int | None
            Days to look back. Default uses Yahoo's practical max (~730).
        rth_only : bool
            If True, keep only Regular Trading Hours (09:30–16:00 America/New_York).
        auto_adjust : bool
            If True, adjust for splits/dividends (recommended).

        Returns
        -------
        List[float]  # most-recent price is last element
        """
        days = lookback_days or self._MAX_HOURLY_LOOKBACK_DAYS

        df = yf.download(
            self.ticker,
            period=f"{days}d",
            interval="60m",
            auto_adjust=auto_adjust,
            actions=False,
            progress=False,
        )

        if df is None or df.empty:
            return []

        # Ensure naive timestamps for consistent handling
        df.index = pd.to_datetime(df.index).tz_localize(None)

        if rth_only:
            # treat timestamps as NY-local, filter RTH, then drop tz again
            df = df.tz_localize("America/New_York", ambiguous="NaT", nonexistent="shift_forward")
            df = df.between_time("09:30", "16:00", include_start=True, include_end=True)
            df = df.tz_convert(None)

        # Return Close column as a plain Python list (Series -> list)
        return df["Close"].astype(float).squeeze().tolist()
