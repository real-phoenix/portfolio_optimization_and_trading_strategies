import pandas as pd
import yfinance as yf

def get_data_for_ticker(ticker, period="max"):  # period can be '1mo', '1y', 'max' etc.
    ticker_obj = yf.Ticker(ticker)
    # Load historical market data as a pandas DataFrame
    df = ticker_obj.history(period=period, interval="1d", auto_adjust=True)
    return df

def get_data(tickers, period="1d"): 
    all_df = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        df = get_data_for_ticker(ticker, period)
        all_df[ticker] = df
    # Concatenate multi ticker data with multi-level column indices (ticker, field)
    combined_df = pd.concat(all_df, axis=1)
    combined_df.columns = ['_'.join(col).strip().replace(" ", "") for col in combined_df.columns.values]    
    return combined_df

def get_data_cleaning(df):
    # Example cleaning: Fill missing values with forward fill method
    df_cleaned = df.ffill().bfill()
    return df_cleaned