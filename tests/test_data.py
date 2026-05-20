import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from data.price_fetcher import fetch_prices
from data.news_fetcher import fetch_news

class TestDataIngestion(unittest.TestCase):

    @patch('yfinance.download')
    def test_fetch_prices_structure(self, mock_download):
        # Create a mock DataFrame
        dates = pd.date_range(start='2026-05-01', periods=3)
        mock_df = pd.DataFrame({
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [95.0, 96.0, 97.0],
            'Close': [102.0, 103.0, 104.0],
            'Volume': [1000, 1100, 1200]
        }, index=dates)
        
        mock_download.return_value = mock_df
        
        # Use a fixed end_date to match our mock data range
        end_date = datetime(2026, 5, 4)
        df = fetch_prices("AAPL", days=5, end_date=end_date)
        
        self.assertFalse(df.empty)
        self.assertIn('return_next_day', df.columns)
        self.assertEqual(len(df), 3)
        # Check return_next_day calculation: (103-102)/102 = 0.0098...
        self.assertAlmostEqual(df['return_next_day'].iloc[0], (103.0-102.0)/102.0)

    @patch('data.news_fetcher.NEWS_API_KEY', 'fake_key')
    @patch('newsapi.NewsApiClient.get_everything')
    def test_fetch_news_structure(self, mock_get_everything):
        # Mock NewsAPI response
        mock_get_everything.return_value = {
            'status': 'ok',
            'articles': [
                {
                    'publishedAt': '2026-05-15T10:00:00Z',
                    'title': 'Test Headline 1',
                    'source': {'name': 'Reuters'}
                },
                {
                    'publishedAt': '2026-05-15T12:00:00Z',
                    'title': 'Test Headline 2',
                    'source': {'name': 'CNBC'}
                }
            ]
        }
        
        df = fetch_news("AAPL", days=5)
        
        self.assertEqual(len(df), 2)
        self.assertListEqual(list(df.columns), ['date', 'ticker', 'headline', 'source'])
        self.assertEqual(df['date'].iloc[0], '2026-05-15')

if __name__ == '__main__':
    unittest.main()
