from get_data import *
from financial_metrics import *
import pandas as pd
from plot import *
from portfolio_optimization_module import *
from systematic_trading_strategy import *

# AAPL, MSFT: Large-cap tech stocks
# VTI: Broad US stock market ETF
# VXUS: International equity ETF
# BND: US bond market ETF for fixed income
# TLT: Long-term treasury bond ETF for stability
# XLK: Tech sector ETF for targeted growth exposure

tickers = ["VTI", "VXUS", "BND"]
# tickers = ["AAPL", "MSFT", "VTI", "VXUS", "BND", "TLT", "XLK", "META"]

raw_data = get_data(tickers, period="1y")
cleaned_data = get_data_cleaning(raw_data)
master_data = calculate_adjusted_close(cleaned_data, tickers)
# print(master_data.columns)
# print(master_data.head(2))

log_returns = compute_log_returns(master_data)
# print(log_returns.head(2))
# plot_graph(log_returns)

rolling_volatility = compute_rolling_volatility(master_data)
# print(rolling_volatility.head(29))
# plot_graph(rolling_volatility)

simple_moving_average = compute_simple_moving_average(master_data)
# print(simple_moving_average.head(29))

exponential_moving_average = compute_exponential_moving_average(master_data)
# print(exponential_moving_average.head(29))
# plot_graph(exponential_moving_average)

RSI = compute_RSI(master_data)
# print(RSI.head(29))

MACD, signal = compute_MACD(master_data)
# print(MACD.head(29))
# print(signal.head(29))

upper_band, lower_band = compute_Bollinger_Bands(master_data)
# print(upper_band.head(25))
# print(lower_band.head(25))

ATR = compute_ATR(master_data)
# print(ATR.head(2))
# plot_graph(ATR)

# Compute RSI for momentum signals
rsi_data = compute_RSI(master_data)
thresholds = calculate_rsi_thresholds(rsi_data, tickers)
momentum_signals = generate_momentum_signals(rsi_data, tickers, thresholds)
print("Momentum Signals (RSI > 50 = Buy, <= 50 = Sell):")
print(momentum_signals.tail(10))
plot_multiple_tickers_with_signals(master_data, momentum_signals, tickers, use_subplots=False)

# Generate mean reversion signals using Bollinger Bands
mean_reversion_signals = generate_mean_reversion_signals(master_data, tickers, window=20, num_std=2)
print("\nMean Reversion Signals (Price < Lower Band = Buy, > Upper Band = Sell):")
print(mean_reversion_signals.tail(10))
plot_multiple_tickers_with_signals(master_data, mean_reversion_signals, tickers, use_subplots=False)

# Compute ATR and determine volatility thresholds empirically
ATR = compute_ATR(master_data)
atr_values = ATR.stack().dropna()
low_vol_threshold = atr_values.quantile(0.25)  # 25th percentile threshold
high_vol_threshold = atr_values.quantile(0.75) # 75th percentile threshold
print(f"\nLow volatility threshold (25th percentile): {low_vol_threshold:.4f}")
print(f"High volatility threshold (75th percentile): {high_vol_threshold:.4f}")

# Generate volatility-based signals based on ATR thresholds
volatility_signals = generate_volatility_based_signals(ATR, tickers, low_vol_threshold, high_vol_threshold)
print("\nVolatility Based Signals (ATR < Low = Buy, ATR > High = Sell):")
print(volatility_signals.tail(10))
plot_multiple_tickers_with_signals(master_data, volatility_signals, tickers, use_subplots=False)