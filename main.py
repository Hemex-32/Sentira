from data.price_fetcher import fetch_prices
from data.news_fetcher import fetch_news
from models.finbert import finbert_model
from models.aggregator import aggregate_sentiment
from signals.generator import apply_signals
from signals.merger import merge_signals_with_prices
from backtest.evaluator import run_backtest, print_stats
from utils.config import DEFAULT_TICKERS, LOOKBACK_DAYS

def run_pipeline(ticker: str, days: int = 30):
    """
    Run the full end-to-end pipeline for a single ticker.
    """
    print(f"\n>>> Running pipeline for {ticker} ({days} days lookback) <<<")
    
    # 1. Fetch Data
    prices = fetch_prices(ticker, days=days)
    if prices.empty:
        print(f"Error: No price data found for {ticker}")
        return None
    
    news = fetch_news(ticker, days=days)
    if news.empty:
        print(f"Warning: No news headlines found for {ticker}")
        # We can still proceed, but sentiment will be 0 (HOLD)
    
    # 2. Score Sentiment
    if not news.empty:
        print(f"Scoring {len(news)} headlines...")
        results = finbert_model.score_headlines(news['headline'].tolist())
        news['label'] = [r['label'] for r in results]
        news['score'] = [r['score'] for r in results]
        
        # 3. Aggregate
        sentiment_agg = aggregate_sentiment(news)
    else:
        import pandas as pd
        sentiment_agg = pd.DataFrame(columns=['date', 'ticker', 'avg_sentiment'])
    
    # 4. Generate Signals
    signal_df = apply_signals(sentiment_agg)
    
    # 5. Merge
    merged_df = merge_signals_with_prices(prices, signal_df)
    
    # 6. Backtest
    print("Running backtest...")
    stats, plot_path = run_backtest(merged_df)
    
    if stats is not None:
        print_stats(stats)
        print(f"Backtest plot saved to: {plot_path}")
    
    return {
        'ticker': ticker,
        'prices': prices,
        'news': news,
        'sentiment': sentiment_agg,
        'signals': signal_df,
        'merged': merged_df,
        'stats': stats,
        'plot_path': plot_path
    }

if __name__ == "__main__":
    # Test with the first default ticker
    if DEFAULT_TICKERS:
        run_pipeline(DEFAULT_TICKERS[0], days=LOOKBACK_DAYS)
