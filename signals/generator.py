import pandas as pd
from utils.config import BUY_THRESHOLD, SELL_THRESHOLD

def generate_signal(avg_sentiment: float) -> str:
    """
    Generate a BUY, SELL, or HOLD signal based on the average sentiment score.
    """
    if avg_sentiment >= BUY_THRESHOLD:
        return "BUY"
    elif avg_sentiment <= SELL_THRESHOLD:
        return "SELL"
    else:
        return "HOLD"

def apply_signals(aggregated_sentiment_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply generate_signal to an aggregated sentiment DataFrame.
    """
    df = aggregated_sentiment_df.copy()
    df['signal'] = df['avg_sentiment'].apply(generate_signal)
    return df
