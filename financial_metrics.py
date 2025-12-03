import numpy as np
import pandas as pd

def calculate_adjusted_close(prices, tickers):
    for ticker in tickers:
        close_col = f"{ticker}_Close"
        dividends_col = f"{ticker}_Dividends"
        splits_col = f"{ticker}_StockSplits"

        # Replace 0 splits with 1 (no split)
        prices[splits_col] = prices[splits_col].replace(0, 1)

        # Dividend factor (1 - dividend / close), avoid division by zero by replacing close 0 with NaN
        div_factor = 1 - (prices[dividends_col] / prices[close_col].replace(0, np.nan))
        div_factor.fillna(1, inplace=True)

        # Calculate cumulative product of dividend and split factors backward in time
        cum_div_factor = div_factor[::-1].cumprod()[::-1]
        cum_split_factor = prices[splits_col][::-1].cumprod()[::-1]

        # Calculate adjusted close price
        prices[f'{ticker}_AdjClose'] = prices[close_col] * cum_div_factor * cum_split_factor

    return prices

def compute_log_returns(prices):
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    log_returns = np.log(close_cols / close_cols.shift(1))
    return log_returns

def compute_rolling_volatility(prices, window=20):
    log_returns = compute_log_returns(prices)
    rolling_vol = log_returns.rolling(window=window).std() * np.sqrt(252)  
    return rolling_vol


## Feature Engineering

def compute_simple_moving_average(prices, window=20): 
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    moving_avg = close_cols.rolling(window=window).mean()
    return moving_avg

def compute_exponential_moving_average(prices, span=20):
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    exp_moving_avg = close_cols.ewm(span=span, adjust=False).mean()
    return exp_moving_avg

def compute_RSI(prices, window=14):
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    delta = close_cols.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

def compute_MACD(prices, span_short=12, span_long=26, signal_span=9):
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    ema_short = close_cols.ewm(span=span_short, adjust=False).mean()
    ema_long = close_cols.ewm(span=span_long, adjust=False).mean()
    MACD = ema_short - ema_long
    signal = MACD.ewm(span=signal_span, adjust=False).mean()

    return MACD, signal

def compute_Bollinger_Bands(prices, window=20, num_std=2):
    close_cols = prices[[col for col in prices.columns if "adjclose" in col.lower()]]
    rolling_mean = close_cols.rolling(window=window).mean()
    rolling_std = close_cols.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band

def compute_ATR(prices, window=14):
    # prices: DataFrame with multi-ticker OHLC columns named like 'AAPL_High', 'AAPL_Low', 'AAPL_Close', etc.
    
    tickers = set(col.split('_')[0] for col in prices.columns if '_' in col)
    ATR = pd.DataFrame(index=prices.index)
    
    for ticker in tickers:
        high_col = f"{ticker}_High"
        low_col = f"{ticker}_Low"
        close_col = f"{ticker}_Close"
        
        # Check if the columns exist in the dataframe
        if all(c in prices.columns for c in [high_col, low_col, close_col]):
            high = prices[high_col]
            low = prices[low_col]
            close = prices[close_col]
            
            # True Range calculation
            high_low = high - low
            high_close = (high - close.shift(1)).abs()
            low_close = (low - close.shift(1)).abs()
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            
            # ATR is rolling mean of True Range
            atr = true_range.rolling(window=window, min_periods=1).mean()
            ATR[f"{ticker}_ATR"] = atr
    
    return ATR