import pandas as pd

def calculate_rsi_thresholds(RSI, tickers, quantile=0.5):
    '''
    Calculate RSI threshold per ticker based on historical RSI distribution quantile (default median).
    RSI: DataFrame with RSI values, e.g., columns like 'VTI_AdjClose'
    tickers: list of tickers
    
    Returns:
    dict {ticker: threshold_value}
    '''
    thresholds = {}
    for ticker in tickers:
        col = f"{ticker}_AdjClose"
        thresholds[ticker] = RSI[col].quantile(quantile)
    return thresholds


def generate_momentum_signals(RSI, tickers, thresholds=None):
    '''
    Momentum strategy using RSI with adaptive thresholds:
    - Buy (1) when RSI > threshold
    - Sell (-1) when RSI <= threshold
    - Hold (0) otherwise
    
    RSI: DataFrame with RSI values
    tickers: list of ticker symbols
    thresholds: dict {ticker: threshold}, if None, defaults to 0.5 quantile (median)
    
    Returns:
    DataFrame of signals
    '''
    if thresholds is None:
        thresholds = calculate_rsi_thresholds(RSI, tickers)
    
    signals = pd.DataFrame(index=RSI.index)
    for ticker in tickers:
        col = f"{ticker}_AdjClose"
        thresh = thresholds.get(ticker, 50)  # fallback to 50 if missing
        signals[ticker] = 0
        signals.loc[RSI[col] > thresh, ticker] = 1
        signals.loc[RSI[col] <= thresh, ticker] = -1
    
    return signals



def generate_mean_reversion_signals(prices, tickers, window=20, num_std=2):
    '''
    Mean Reversion strategy using Bollinger Bands:
    - Buy (1) when price closes below lower band (oversold)
    - Sell (-1) when price closes above upper band (overbought)
    - Hold (0) when price is inside bands

    prices: DataFrame with AdjClose columns e.g. 'VTI_AdjClose'
    tickers: list of tickers to consider
    window: rolling window for Bollinger bands (default 20)
    num_std: number of standard deviations for bands (default 2)
    '''
    signals = pd.DataFrame(index=prices.index)
    rolling_mean = prices[[f"{ticker}_AdjClose" for ticker in tickers]].rolling(window).mean()
    rolling_std = prices[[f"{ticker}_AdjClose" for ticker in tickers]].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    for ticker in tickers:
        price_col = f"{ticker}_AdjClose"
        signals[ticker] = 0
        signals.loc[prices[price_col] < lower_band[price_col], ticker] = 1
        signals.loc[prices[price_col] > upper_band[price_col], ticker] = -1
    
    return signals


def generate_volatility_based_signals(ATR, tickers, low_vol_threshold, high_vol_threshold):
    '''
    Volatility based strategy using ATR:
    - Buy (1) when ATR < low_vol_threshold (volatility contraction)
    - Sell (-1) when ATR > high_vol_threshold (volatility expansion)
    - Hold (0) otherwise
    
    ATR: DataFrame with ATR indicators, columns like 'VTI_ATR'
    tickers: list of tickers
    low_vol_threshold: float lower ATR threshold for entry
    high_vol_threshold: float upper ATR threshold for exit
    '''
    signals = pd.DataFrame(index=ATR.index)
    for ticker in tickers:
        atr_col = f"{ticker}_ATR"
        signals[ticker] = 0
        signals.loc[ATR[atr_col] < low_vol_threshold, ticker] = 1
        signals.loc[ATR[atr_col] > high_vol_threshold, ticker] = -1
    return signals
