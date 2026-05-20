import unittest
from unittest.mock import patch
import pandas as pd
from models.finbert import FinBERT
from models.aggregator import aggregate_sentiment

class TestModelPipeline(unittest.TestCase):

    @patch('models.finbert.pipeline')
    def test_finbert_scoring(self, mock_pipeline):
        # Mock the pipeline return value
        mock_pipeline.return_value.return_value = [
            {'label': 'positive', 'score': 0.9},
            {'label': 'negative', 'score': 0.8}
        ]
        
        # We need to re-initialize or mock the singleton to use our mock pipeline
        # For simplicity in this test, we'll just test the logic if we can
        fb = FinBERT()
        fb._pipeline = mock_pipeline.return_value # Inject mock
        
        results = fb.score_headlines(["Good news", "Bad news"])
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['label'], 'positive')
        self.assertEqual(results[1]['label'], 'negative')

    def test_sentiment_aggregation(self):
        # Mock scored news DataFrame
        df = pd.DataFrame({
            'date': ['2026-05-01', '2026-05-01', '2026-05-02'],
            'ticker': ['AAPL', 'AAPL', 'AAPL'],
            'headline': ['H1', 'H2', 'H3'],
            'label': ['positive', 'negative', 'neutral'],
            'score': [0.8, 0.6, 0.9]
        })
        
        # Expected calculation:
        # 2026-05-01: (0.8 + -0.6) / 2 = 0.1
        # 2026-05-02: 0 / 1 = 0.0
        
        agg_df = aggregate_sentiment(df)
        
        self.assertEqual(len(agg_df), 2)
        self.assertAlmostEqual(agg_df[agg_df['date'] == '2026-05-01']['avg_sentiment'].iloc[0], 0.1)
        self.assertAlmostEqual(agg_df[agg_df['date'] == '2026-05-02']['avg_sentiment'].iloc[0], 0.0)

if __name__ == '__main__':
    unittest.main()
