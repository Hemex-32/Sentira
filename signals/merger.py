import pandas as pd

def merge_signals_with_prices(price_df: pd.DataFrame, signal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join signal data onto price data on (ticker, date).
    Fills missing signal days with 'HOLD' and avg_sentiment with 0.
    """
    if price_df.empty:
        return pd.DataFrame()

    # Ensure date formats match for joining
    # yfinance uses datetime index, news/signals use string YYYY-MM-DD
    prices = price_df.copy()
    
    # Flatten MultiIndex columns just in case they slipped through
    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(-1)

    prices['date_str'] = prices.index.strftime('%Y-%m-%d')
    
    # Left join signals onto prices
    # We join on date_str from prices and date from signal_df
    merged = pd.merge(
        prices, 
        signal_df, 
        left_on='date_str', 
        right_on='date', 
        how='left'
    )
    
    # Fill missing values for days without news
    merged['signal'] = merged['signal'].fillna('HOLD')
    merged['avg_sentiment'] = merged['avg_sentiment'].fillna(0.0)
    
    # Restore the original index (datetime)
    merged.index = price_df.index
    
    # Clean up temporary and redundant columns
    cols_to_drop = ['date_str', 'date']
    if 'ticker_y' in merged.columns:
        cols_to_drop.append('ticker_y')
        if 'ticker_x' in merged.columns:
            merged.rename(columns={'ticker_x': 'ticker'}, inplace=True)
    
    merged.drop(columns=[c for c in cols_to_drop if c in merged.columns], inplace=True)
    
    return merged
