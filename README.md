# Algorithmic Trading Strategies

After interning at a quant trading company, I became interested the US stock market and how to profit from it. This curiosity led me to learn personal finance and investing. I recently wrote an article on why you should invest early. You can read it [here](https://khznote.notion.site/Invest-early-the-power-of-compound-interest-3b5a087607c2416fadf653e370ad3223).

With a background in computer science, I created this repository to develop and backtest algorithmic trading strategies using the market data from the past 2 years (720 days to be exact).

You can easily understand what I am doinng in the BackTest folder.

## Requirements

To run this project, you will need:
- **Python 3**: Ensure you have Python 3 installed on your system.
- **yahoo_fin**: A library to fetch stock market data. You can install it using pip.

Install the required packages using:

```bash
pip install yahoo_fin
```

## Trailing Stop-Loss Algorithm

One of the strategies I developed is based on the [Trailing Stop-Loss](https://www.investopedia.com/articles/trading/08/trailing-stop-loss.asp) technique. The details of the algorithm can be found in `Strategy/trailingStop.py`. I backtested this strategy using data from the past 720 days.

### Backtest Results

I tested the algorithm with a variety of US stocks, including diversified stocks, highly volatile stocks, and big tech stocks. The strategy has outperformed a simple buy-and-hold approach over the 2-year period. Below are some backtest results:

#### Backtest on Most Volatile Stocks
```
Backtest on most volatile stocks including 'TSLA', 'OVV', 'OPEN', 'QS', 'MP', 'NIO', 'HRI', 'RUN', 'COIN', 'PLTR', 'CLF', 'SHOP'
----------Summary----------
Original balance $100000.00
Total TS amount $128809.16 - Total TS profit percent 28.81%
Total HOLD amount $106521.39 - Total HOLD profit percent 6.52%
```
#### Backtest on Big Tech Stocks
```
Backtest with Big tech stocks 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'NFLX', 'QQQ', 'SPY', 'TSLA'
----------Summary----------
Original balance $100000.00
Total TS amount $269225.14 - Total TS profit percent 169.23%
Total HOLD amount $217763.78 - Total HOLD profit percent 117.76%
```

### Analysis

The results indicate that the algorithm effectively maximizes profit and minimizes losses. For instance, when backtested with NVDA, the algorithm yielded a profit percent of **826.25%** compared to **551.89%** from a simple buy-and-hold strategy since the beginning at low price 2 years ago. This shows that the algorithm outperforms most of the stock market and manages risk through its dynamic low threshold bar.

Feel free to explore and contribute to the repository if you have any suggestions or improvements!