# Multi-Layer EMA and RSI Trading Strategy

## Overview
This repository contains a QuantConnect-based algorithmic trading strategy that leverages multiple 
Exponential Moving Averages (EMAs) and the Relative Strength Index (RSI) to trade stocks from the S&P 500 index. The strategy aims to capture trends and manage risk through systematic entry and exit signals.

## Strategy Description
The strategy uses five different EMAs (9, 15, 35, 65, and 200 periods) and an RSI indicator (14 periods) to make buy and sell decisions. It works on daily resolution data and applies to a diversified portfolio of S&P 500 stocks, including well-known companies like Apple, Microsoft, Google, and Amazon.

### Buy Condition
- The short-term EMA (9-period) is above the 15-period EMA, which is above the 65-period EMA, which is above the 200-period EMA.
- The 35-period EMA is greater than 60.

### Sell Condition
- The short-term EMA (9-period) is below the 15-period EMA, which is below the 65-period EMA, which is below the 200-period EMA.
- The 35-period EMA is less than 40.

### Exit Conditions
- If a buy condition is met, but the EMAs cross in a bearish manner or the RSI falls below 40, the position is liquidated.
- If a sell condition is met, but the EMAs cross in a bullish manner or the RSI rises above 60, the position is liquidated.

## Performance
The strategy has been backtested over several years and has demonstrated strong performance metrics:
- **CAGR**: 104.0%
- **Sharpe Ratio**: 2.1
- **Sortino Ratio**: 2.2
- **Max Drawdown**: 29.0%
- **Average Trades Per Day**: 11

> The full performance details and backtest results can be viewed [here](https://www.quantconnect.com/reports/9b2195ecbf4f473353656f7545dc1f22).

## Installation and Usage
To run this strategy, you will need to have a QuantConnect account and access to the QuantConnect platform.

### Steps:
1. Clone this repository.
   ```bash
   git clone https://github.com/yourusername/multilayer-ema-rsi-strategy.git
