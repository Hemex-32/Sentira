import unittest
import pandas as pd
from signals.generator import generate_signal
from signals.merger import merge_signals_with_prices

class TestSignalLayer(unittest.TestCase):

    def test_signal_logic(self):
        # Default thresholds: BUY >= 0.1, SELL <= -0.1
        self.assertEqual(generate_signal(0.15), "BUY")
        self.assertEqual(generate_signal(0.1), "BUY")
        self.assertEqual(generate_signal(0.05), "HOLD")
        self.assertEqual(generate_signal(-0.1), "SELL")
        self.assertEqual(generate_signal(-0.2), "SELL")

    def test_merge_logic(self):
        # Mock price DataFrame (index is datetime)
        dates = pd.date_range(start='2026-05-01', periods=3)
        price_df = pd.DataFrame({
            'Close': [100.0, 101.0, 102.0],
            'ticker': ['AAPL', 'AAPL', 'AAPL']
        }, index=dates)
        
        # Mock signal DataFrame (date is string)
        signal_df = pd.DataFrame({
            'date': ['2026-05-01', '2026-05-03'],
            'ticker': ['AAPL', 'AAPL'],
            'avg_sentiment': [0.2, -0.2],
            'signal': ['BUY', 'SELL']
        })
        
        merged = merge_signals_with_prices(price_df, signal_df)
        
        self.assertEqual(len(merged), 3)
        self.assertEqual(merged['signal'].iloc[0], 'BUY')
        self.assertEqual(merged['signal'].iloc[1], 'HOLD') # Missing in signal_df
        self.assertEqual(merged['signal'].iloc[2], 'SELL')
        self.assertEqual(merged['avg_sentiment'].iloc[1], 0.0)

if __name__ == '__main__':
    unittest.main()
