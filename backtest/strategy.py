from backtesting import Strategy

class SentimentStrategy(Strategy):
    """
    Simple backtesting strategy based on sentiment signals.
    BUY when signal is 'BUY' and no position.
    SELL when signal is 'SELL' and position exists.
    """
    def init(self):
        super().init()
        # signal and avg_sentiment are columns in the self.data DataFrame

    def next(self):
        # Current signal for this bar
        current_signal = self.data.signal[-1]
        
        if current_signal == 'BUY' and not self.position:
            self.buy()
        elif current_signal == 'SELL' and self.position:
            self.position.close()
