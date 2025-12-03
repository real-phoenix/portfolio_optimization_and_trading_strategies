import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns

def mean_variance_optimization_portfolio(prices, tickers):
    prices_adj = prices[[f"{ticker}_AdjClose" for ticker in tickers]].dropna()
    mu = expected_returns.mean_historical_return(prices_adj)
    S = risk_models.sample_cov(prices_adj)

    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    weights = ef.clean_weights()
    ret, vol, sharpe = ef.portfolio_performance(verbose=False)
    return weights, mu, S, ret, vol, sharpe

def factor_investing_portfolio_optimization(data, tickers, top_n=5):
    # 1. Extract adjusted close prices only for tickers specified
    price_cols = [f"{ticker}_AdjClose" for ticker in tickers]
    prices = data[price_cols].dropna()

    # 2. Calculate simplistic momentum factor: % return over last 6 months (~126 trading days)
    momentum = prices.pct_change(126).iloc[-1]

    # 3. For this example, use momentum alone as factor scores - normalize ranks
    factor_scores = momentum.rank(pct=True)

    # 4. Pick top N tickers based on factor scores
    top_tickers_cols = factor_scores.nlargest(top_n).index.tolist()

    # Map back to ticker names by removing "_AdjClose"
    selected_tickers = [col.split("_")[0] for col in top_tickers_cols]

    # 5. Prepare returns data for selected tickers
    selected_price_cols = [f"{ticker}_AdjClose" for ticker in selected_tickers]
    prices_selected = prices[selected_price_cols]

    # 6. Calculate expected returns (annualized) and sample covariance
    mu = prices_selected.pct_change().mean() * 252
    S = risk_models.sample_cov(prices_selected)

    # 7. Optimize portfolio for max Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    # 8. Portfolio performance metrics
    ret, vol, sharpe = ef.portfolio_performance(verbose=False)

    return cleaned_weights, selected_tickers, ret, vol, sharpe