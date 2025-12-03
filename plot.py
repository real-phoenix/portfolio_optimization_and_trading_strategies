import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier
import numpy as np

def plot_graph(df):
    plt.figure(figsize=(14,7))
    for col in df.columns:
        plt.plot(df.index, df[col], label=col)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('Stock Closing Prices Over 1 Year')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_efficient_frontier(mu, S, ret_opt, vol_opt):
    ef = EfficientFrontier(mu, S)

    n_points = 100
    max_target = mu.max() * 0.99  # 99% of max return to ensure feasibility
    target_returns = np.linspace(mu.min(), max_target, n_points)
    risks = []
    for r in target_returns:
        ef.efficient_return(target_return=r)
        risks.append(ef.portfolio_performance(verbose=False)[1])

    plt.figure(figsize=(10, 6))
    plt.plot(risks, target_returns, label='Efficient Frontier')
    plt.scatter(vol_opt, ret_opt, c='red', marker='*', s=200, label='Max Sharpe Portfolio')
    plt.title('Efficient Frontier and Optimal Portfolio')
    plt.xlabel('Volatility (Std Deviation)')
    plt.ylabel('Expected Return')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_portfolio_weights_bar(weights, save_path=None):
    labels = list(weights.keys())
    sizes = list(weights.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, sizes, color='skyblue', edgecolor='black')

    plt.xlabel('Assets')
    plt.ylabel('Weights')
    plt.title('Portfolio Weights Bar Chart')
    plt.xticks(rotation=45, ha='right')

    # Add data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.2%}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # offset label slightly above bar
                     textcoords='offset points',
                     ha='center', va='bottom')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Bar chart saved to {save_path}")

    plt.show()


def plot_multiple_tickers_with_signals(prices, signals, tickers, use_subplots=False):
    colors = plt.cm.get_cmap('tab10', len(tickers))
    
    if use_subplots:
        fig, axes = plt.subplots(len(tickers), 1, figsize=(14, 4*len(tickers)), sharex=True)
        if len(tickers) == 1:
            axes = [axes]
    else:
        plt.figure(figsize=(14, 8))
    
    for i, ticker in enumerate(tickers):
        price_col = f"{ticker}_AdjClose"
        buy_markersize = 30
        sell_markersize = 30
        
        if use_subplots:
            ax = axes[i]
            ax.plot(prices.index, prices[price_col], label=f'{ticker} Price', color=colors(i))
            
            buy_signal_dates = signals.index[signals[ticker] == 1]
            sell_signal_dates = signals.index[signals[ticker] == -1]
            
            ax.scatter(buy_signal_dates, prices.loc[buy_signal_dates, price_col],
                       marker='o', color='g', s=buy_markersize, alpha=0.7, label='Buy Signal')
            ax.scatter(sell_signal_dates, prices.loc[sell_signal_dates, price_col],
                       marker='x', color='r', s=sell_markersize, alpha=0.7, label='Sell Signal')
            
            ax.set_title(f'Trading Signals for {ticker}')
            ax.set_ylabel('Price')
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='best', fontsize='small')
        else:
            plt.plot(prices.index, prices[price_col], label=f'{ticker} Price', color=colors(i))
            
            buy_signal_dates = signals.index[signals[ticker] == 1]
            sell_signal_dates = signals.index[signals[ticker] == -1]
            
            plt.scatter(buy_signal_dates, prices.loc[buy_signal_dates, price_col],
                        marker='o', color='g', s=buy_markersize, alpha=0.7, label=f'{ticker} Buy')
            plt.scatter(sell_signal_dates, prices.loc[sell_signal_dates, price_col],
                        marker='x', color='r', s=sell_markersize, alpha=0.7, label=f'{ticker} Sell')
    
    if not use_subplots:
        plt.title('Multiple Tickers Price with Trading Signals')
        plt.xlabel('Date')
        plt.ylabel('Price')
        # Avoid duplicate labels in legend
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize='small', ncol=2)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    else:
        plt.xlabel('Date')
        plt.tight_layout()
        plt.show()