import pandas as pd
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from utils.config import NEWS_API_KEY

def fetch_news(ticker: str, days: int = 30) -> pd.DataFrame:
    """
    Fetch news headlines for a given ticker from NewsAPI.
    """
    if not NEWS_API_KEY or NEWS_API_KEY == "your_newsapi_key_here":
        print("Warning: NEWS_API_KEY not set correctly.")
        return pd.DataFrame()

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    all_articles = newsapi.get_everything(
        q=ticker,
        from_param=from_date,
        to=datetime.now().strftime('%Y-%m-%d'),
        language='en',
        sort_by='publishedAt',
        page_size=100
    )
    
    if all_articles['status'] != 'ok' or not all_articles['articles']:
        return pd.DataFrame(columns=['date', 'ticker', 'headline', 'source'])
    
    data = []
    for article in all_articles['articles']:
        data.append({
            'date': article['publishedAt'][:10], # Extract YYYY-MM-DD
            'ticker': ticker,
            'headline': article['title'],
            'source': article['source']['name']
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Quick manual test (will likely fail without key)
    news = fetch_news("AAPL", days=7)
    print(news.head())
