import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_prices(ticker: str, days: int = 30, end_date: datetime = None) -> pd.DataFrame:
    """
    Fetch OHLCV data for a given ticker and calculate next day returns.
    """
    if end_date is None:
        end_date = datetime.now()
    start_date = end_date - timedelta(days=days + 5)  # Fetch extra days for returns calculation
    
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if df.empty:
        return pd.DataFrame()

    # Flatten MultiIndex columns if present (common in yfinance >= 0.2.0)
    if isinstance(df.columns, pd.MultiIndex):
        # Find the level that contains 'Close'
        for i in range(df.columns.nlevels):
            if 'Close' in df.columns.get_level_values(i):
                df.columns = df.columns.get_level_values(i)
                break
    
    # Calculate daily returns shifted by -1 (label for backtesting)
    df['return_next_day'] = df['Close'].pct_change().shift(-1)
    
    # Filter back to the requested lookback period
    limit_date = end_date - timedelta(days=days)
    df = df[df.index >= limit_date]
    
    return df

if __name__ == "__main__":
    # Quick manual test
    data = fetch_prices("AAPL", days=10)
    print(data.head())
    print(data.columns)
