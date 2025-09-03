from ..BaseAlgorithm import BaseAlgorithm

class TrailingStopLossAlgorithm(BaseAlgorithm):
    def __init__ (self, balance, buy_percent=0.2):
        '''
        Initialize the trailingStop instance.

        Parameters:
        balance (float): Initial balance for trading.
        buy_percent (float): Percentage increase from the minimum price to trigger a buy.
        '''
        self.balance = balance
        self.stockOwned = 0
        self.buy_percent = buy_percent
        self.low_threshold = 0
        self.high_threshold = 0


    '''
    Trailing Stop based algorithm to outperform the market.
        Algorithm summary
        -----------------
    keep track of the minimum price
    if the current price hits 120% of the minimum price, the stock keeps likely going up --> BUY
    For BUY, set the initial low and high bar to sell (managing the risk)

    After BUY, we either HOLD them or SELL them
    if the price keeps going up, we keep updating the low and high bar
    if the price hits either low or high bar, we sell them

    @prices: list of stock prices from MarketData
    @returns:
    float: Final balance after performing the backtest.
    '''
    def run(self, prices) -> float:
        min_price = float('inf')
        last_price = float('inf')
        bought = False
        for idx, price in enumerate(prices):
            if not bought:
                min_price = min(min_price, price)
                buy_threshold = min_price * (1 + self.buy_percent)
                # Buy
                if price >= buy_threshold:
                    self._buy(price)
                    self.low_threshold = price * 0.9
                    self.high_threshold = price * 1.3
                    bought = True
                    min_price = float('inf')
            else:
                # Sell
                if price <= self.low_threshold or price >= self.high_threshold:
                    self._sell(price)
                    bought = False
                    last_price = float('inf')
                # Hold
                else:
                    if price > last_price:
                        self.low_threshold = self.low_threshold * 0.95 # to maximize profit
                        self.high_threshold = price + (self.high_threshold * 0.3)
                    last_price = price
        if bought:
            self.balance += (price * self.stockOwned)
            self.stockOwned = 0
        return self.balance

    def _max_buy(self, price_per_stock):
        return self.balance // price_per_stock

    def _reset_threshold(self):
        self.low_threshold = 0
        self.high_threshold = 0

    def _buy(self, price):
        self.stockOwned = self._max_buy(price)
        self.balance -= (price * self.stockOwned)

    def _sell(self, price):
        self.balance += (price * self.stockOwned * 0.92)
        self.stockOwned = 0
        self._reset_threshold()
