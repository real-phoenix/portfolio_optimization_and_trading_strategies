# Systematic Trading Toolkit

This project is a Python toolkit for end-to-end equity analysis,
technical indicators, systematic trading signal generation, and
portfolio optimization using real market data from Yahoo Finance. It
supports both factor-based and mean-variance portfolio construction,
along with rich visualization utilities.

## Features

-   Automated data ingestion and cleaning from Yahoo Finance via
    yfinance.
-   Computation of adjusted close prices with dividends and stock
    splits.
-   **Core risk/return analytics:**
    -   Log returns and rolling volatility.
    -   Simple and exponential moving averages.
-   **Technical indicators:**
    -   RSI, MACD, Bollinger Bands, ATR.
-   **Systematic trading strategies:**
    -   Momentum (RSI-based).
    -   Mean reversion (Bollinger Bands).
    -   Volatility-based (ATR thresholds).
-   **Portfolio optimization with PyPortfolioOpt:**
    -   Mean-variance (max Sharpe portfolio).
    -   Simple factor-based (momentum) portfolio selection.
-   **Visualization:**
    -   Price charts.
    -   Trading signals overlays.
    -   Efficient frontier and optimal portfolio.
    -   Portfolio weights bar charts.

## Project Structure

    ├── get_data.py              # Yahoo Finance data fetching & cleaning
    ├── financial_metrics.py     # Technical indicators & risk metrics
    ├── systematic_trading_strategy.py  # Trading signal generators
    ├── portfolio_optimization_module.py # Portfolio optimization
    ├── plot.py                  # Visualization utilities
    └── main.py                  # Example usage & full pipeline

## Installation

``` bash
git clone https://github.com/real-phoenix/systematic-trading-toolkit.git
cd systematic-trading-toolkit

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### requirements.txt

    pandas
    numpy
    matplotlib
    yfinance
    PyPortfolioOpt

## Quick Start

``` python
# Edit tickers in main.py
tickers = ["VTI", "VXUS", "BND"]  # ETFs
# tickers = ["AAPL", "MSFT", "META"]  # Stocks

# Run full pipeline
python main.py
```

Outputs include: - Technical indicators (RSI, MACD, Bollinger Bands,
ATR) - Trading signals (Momentum, Mean Reversion, Volatility) -
Portfolio optimization results - Interactive price charts with buy/sell
signals - Efficient frontier & optimal weights

## Trading Strategies Implemented

### 1. Momentum (RSI-based)

    RSI > Median Threshold → Buy (1)
    RSI ≤ Median Threshold → Sell (-1)

### 2. Mean Reversion (Bollinger Bands)

    Price < Lower Band → Buy (1)  # Oversold
    Price > Upper Band → Sell (-1) # Overbought

### 3. Volatility (ATR-based)

    ATR < 25th percentile → Buy (1)  # Low vol contraction
    ATR > 75th percentile → Sell (-1) # High vol expansion

## Portfolio Optimization

### Mean-Variance Optimization

``` python
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()  # Maximum Sharpe ratio
```

### Factor Investing (Momentum)

-   Select top 5 tickers by 6-month momentum
-   Optimize portfolio weights among winners

## Example Output

    Momentum Signals (RSI > 50 = Buy, <= 50 = Sell):
                VTI  VXUS  BND
    2025-12-01   1     1    0
    2025-12-02  -1     1   -1

    Low volatility threshold (25th percentile): 0.0123
    High volatility threshold (75th percentile): 0.0456

## Usage Examples

``` python
# Custom tickers
tickers = ["AAPL", "MSFT", "GOOGL"]
raw_data = get_data(tickers, period="1y")

# Generate signals only
rsi_data = compute_RSI(master_data)
signals = generate_momentum_signals(rsi_data, tickers)

# Optimize portfolio
weights, mu, S, ret, vol, sharpe = mean_variance_optimization_portfolio(
    master_data, tickers
)
print(f"Max Sharpe Portfolio: Return={ret:.2%}, Vol={vol:.2%}, Sharpe={sharpe:.2f}")
```

## Tech Stack

    Core: Python 3.9+, Pandas, NumPy
    Data: yfinance (Yahoo Finance)
    Optimization: PyPortfolioOpt
    Visualization: Matplotlib

## Contributing

1.  Fork the repo\
2.  Create feature branch (`git checkout -b feature/add-new-strategy`)\
3.  Commit changes (`git commit -m "Add new strategy"`)\
4.  Push (`git push origin feature/add-new-strategy`)\
5.  Open Pull Request

## License

MIT License - see LICENSE file.

## Disclaimer

⚠️ For educational purposes only. Not financial advice.\
Past performance does not guarantee future results. Always conduct your
own research.

------------------------------------------------------------------------

Built with ❤️ by Shreya Singh\
IIT Roorkee '24 \| GitHub \| LinkedIn
