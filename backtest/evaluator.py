import os
from backtesting import Backtest
from backtest.strategy import SentimentStrategy
from utils.config import OUTPUT_DIR

def run_backtest(merged_df, cash=10000, commission=0.002):
    """
    Run the backtest and return stats and plot path.
    """
    if merged_df.empty:
        return None, None

    # backtesting.py expects Open, High, Low, Close, Volume
    # merged_df should already have these from yfinance
    bt = Backtest(merged_df, SentimentStrategy, cash=cash, commission=commission)
    stats = bt.run()
    
    # Save plot
    plot_path = os.path.join(OUTPUT_DIR, "backtest_plot.html")
    try:
        bt.plot(filename=plot_path, open_browser=False)
    except Exception as e:
        print(f"Warning: Backtest plotting failed (likely due to bokeh compatibility): {e}")
        plot_path = None
    
    return stats, plot_path

def print_stats(stats):
    """
    Pretty print key backtest statistics.
    """
    if stats is None:
        print("No backtest results to display.")
        return

    print("\n--- Backtest Results ---")
    print(f"Total Return: {stats['Return [%]']:.2f}%")
    print(f"Buy & Hold Return: {stats['Buy & Hold Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
    print(f"Number of Trades: {stats['# Trades']}")
    print("------------------------\n")
