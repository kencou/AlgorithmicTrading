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

=== Strategy Comparison vs Buy&Hold ===
BH = Buy&Hold, TSL = Trailing Stop Loss, Grid = Grid Trading
Ticker      Buy&Hold           TSL   Δ TSL vs BH     Δ% TSL          Grid  Δ Grid vs BH    Δ% Grid
----------------------------------------------------------------------------------------------------
TSLA         $571.51       $575.93         $4.42     +0.77%       $848.89       $277.38    +48.53%
OVV        $3,538.99     $3,355.41      $-183.57     -5.19%     $2,228.40    $-1,310.58    -37.03%
OPEN         $954.30       $901.55       $-52.74     -5.53%     $1,004.34        $50.05     +5.24%
QS         $1,874.23     $1,168.23      $-706.01    -37.67%     $1,668.30      $-205.93    -10.99%
MP           $332.29       $532.96       $200.67    +60.39%       $571.45       $239.16    +71.97%
NIO        $1,284.36     $1,548.21       $263.85    +20.54%     $1,545.24       $260.88    +20.31%
HRI          $684.70       $902.95       $218.25    +31.87%       $852.24       $167.54    +24.47%
RUN       $15,612.20    $15,559.59       $-52.61     -0.34%     $4,245.11   $-11,367.10    -72.81%
COIN         $680.94       $702.38        $21.45     +3.15%       $989.05       $308.11    +45.25%
PLTR         $440.44       $595.55       $155.12    +35.22%       $845.90       $405.47    +92.06%
CLF        $3,841.73     $3,756.79       $-84.95     -2.21%     $2,318.13    $-1,523.60    -39.66%
SHOP       $1,084.24     $2,032.31       $948.07    +87.44%     $1,002.98       $-81.26     -7.49%
----------------------------------------------------------------------------------------------------
TOTAL     $30,899.93    $31,631.87       $731.94     +2.37%    $18,120.04   $-12,779.89    -41.36%
```
#### Backtest on Big Tech Stocks
```
Backtest with Big tech stocks "AMD", "NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"

=== Strategy Comparison vs Buy&Hold ===
BH = Buy&Hold, TSL = Trailing Stop Loss, Grid = Grid Trading
Ticker      Buy&Hold           TSL   Δ TSL vs BH     Δ% TSL          Grid  Δ Grid vs BH    Δ% Grid
----------------------------------------------------------------------------------------------------
AMD        $1,970.47     $1,887.41       $-83.07     -4.22%     $1,707.67      $-262.80    -13.34%
NVDA       $2,969.96     $2,954.51       $-15.45     -0.52%     $2,088.44      $-881.52    -29.68%
TSLA       $2,312.50     $2,775.26       $462.76    +20.01%     $1,718.81      $-593.69    -25.67%
AAPL       $2,608.63     $2,584.02       $-24.61     -0.94%     $1,902.67      $-705.96    -27.06%
MSFT       $6,585.79     $8,158.88     $1,573.09    +23.89%     $2,762.82    $-3,822.97    -58.05%
GOOGL      $2,532.69     $2,231.80      $-300.89    -11.88%     $1,864.24      $-668.46    -26.39%
AMZN      $16,389.27    $15,551.33      $-837.94     -5.11%     $4,630.99   $-11,758.29    -71.74%
META       $1,626.36     $3,048.47     $1,422.11    +87.44%     $1,504.47      $-121.89     -7.49%
----------------------------------------------------------------------------------------------------
TOTAL     $36,995.69    $39,191.68     $2,196.00     +5.94%    $18,180.10   $-18,815.59    -50.86%
```

### Analysis

The results indicate that the algorithm effectively maximizes profit and minimizes losses. For instance, when backtested with NVDA, the algorithm yielded a profit percent of **826.25%** compared to **551.89%** from a simple buy-and-hold strategy since the beginning at low price 2 years ago. This shows that the algorithm outperforms most of the stock market and manages risk through its dynamic low threshold bar.

Feel free to explore and contribute to the repository if you have any suggestions or improvements!