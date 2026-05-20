import pandas as pd

def aggregate_sentiment(scored_news_df: pd.DataFrame) -> pd.DataFrame:
    """
    Map labels to numeric scores and aggregate by ticker and date.
    Input: DataFrame with ['date', 'ticker', 'headline', 'label', 'score']
    Output: DataFrame with ['date', 'ticker', 'avg_sentiment']
    """
    if scored_news_df.empty:
        return pd.DataFrame(columns=['date', 'ticker', 'avg_sentiment'])

    # Map labels to numeric scores
    # positive -> +confidence, negative -> -confidence, neutral -> 0
    def map_score(row):
        if row['label'] == 'positive':
            return row['score']
        elif row['label'] == 'negative':
            return -row['score']
        else:
            return 0.0

    df = scored_news_df.copy()
    df['sentiment_value'] = df.apply(map_score, axis=1)

    # Group by ticker and date, calculate mean sentiment
    aggregated = df.groupby(['ticker', 'date'])['sentiment_value'].mean().reset_index()
    aggregated.rename(columns={'sentiment_value': 'avg_sentiment'}, inplace=True)

    return aggregated
