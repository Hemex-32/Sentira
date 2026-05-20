# Stock Sentiment AI Agent

A paper-trading agent that scores financial news headlines using FinBERT, generates BUY/HOLD/SELL signals, and backtests those signals against real price data.

> **Portfolio note:** This project demonstrates a complete ML pipeline — data ingestion → NLP scoring → signal logic → backtested evaluation. It does not claim live trading alpha; sentiment-price correlation at a 1-day lag is intentionally noisy and the backtest is included to show evaluation methodology, not profitability.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Entry point                         │
│                  main.py / scheduler                    │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │     Phase 1: Data layer     │
          │  data/news_fetcher.py       │  ← NewsAPI headlines
          │  data/price_fetcher.py      │  ← yfinance OHLCV
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │  Phase 2: Sentiment model   │
          │  models/finbert.py          │  ← ProsusAI/finbert
          │  models/aggregator.py       │  ← daily avg score
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │  Phase 3: Signal engine     │
          │  signals/generator.py       │  ← BUY / HOLD / SELL
          │  signals/merger.py          │  ← join with price data
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │  Phase 4: Backtesting       │
          │  backtest/strategy.py       │  ← backtesting.py Strategy
          │  backtest/evaluator.py      │  ← Sharpe, drawdown, win rate
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │       Dashboard             │
          │  dashboard/app.py           │  ← Streamlit UI
          └─────────────────────────────┘
```

---

## Project structure

```
sentiment-agent/
│
├── main.py                   # CLI entry point — run full pipeline
├── scheduler.py              # APScheduler daily job
├── requirements.txt
├── .env.example
│
├── data/
│   ├── __init__.py
│   ├── news_fetcher.py       # Fetch headlines from NewsAPI
│   └── price_fetcher.py      # Fetch OHLCV from yfinance
│
├── models/
│   ├── __init__.py
│   ├── finbert.py            # Load FinBERT, score headline list
│   └── aggregator.py         # Group scores by ticker + date
│
├── signals/
│   ├── __init__.py
│   ├── generator.py          # Threshold logic → BUY/HOLD/SELL
│   └── merger.py             # Merge signals with price DataFrame
│
├── backtest/
│   ├── __init__.py
│   ├── strategy.py           # backtesting.py Strategy subclass
│   └── evaluator.py          # Compute + print performance stats
│
├── dashboard/
│   ├── __init__.py
│   └── app.py                # Streamlit dashboard
│
└── utils/
    ├── __init__.py
    └── config.py             # Load .env, shared constants
```

---

## Module responsibilities

### `data/news_fetcher.py`
- Accepts: ticker symbol, `from_date`, `to_date`
- Calls NewsAPI `get_everything` endpoint
- Returns: `pd.DataFrame` with columns `[date, ticker, headline, source]`
- Handles pagination and rate limiting

### `data/price_fetcher.py`
- Accepts: ticker, date range
- Uses `yfinance.download()`
- Returns: `pd.DataFrame` with `[date, open, high, low, close, volume, return_next_day]`
- `return_next_day` is `close.pct_change().shift(-1)` — the label you backtest against

### `models/finbert.py`
- Loads `ProsusAI/finbert` once at startup via HuggingFace `pipeline`
- Accepts: list of headline strings
- Returns: list of `{label, score}` dicts
- Truncates at 512 tokens; batches in groups of 32 for memory efficiency

### `models/aggregator.py`
- Accepts: scored headlines DataFrame
- Converts label → numeric: `positive → +confidence`, `negative → −confidence`, `neutral → 0`
- Groups by `(ticker, date)`, returns mean `avg_sentiment` per day

### `signals/generator.py`
- Accepts: `avg_sentiment` float, `buy_threshold=0.1`, `sell_threshold=-0.1`
- Returns: `"BUY"`, `"SELL"`, or `"HOLD"`
- Thresholds are configurable via `utils/config.py`

### `signals/merger.py`
- Left-joins sentiment scores onto price DataFrame on `(ticker, date)`
- Fills missing sentiment days with `0` (HOLD)
- Returns merged DataFrame ready for backtesting

### `backtest/strategy.py`
- Subclasses `backtesting.Strategy`
- `init()`: wraps sentiment column as indicator
- `next()`: BUY when sentiment > threshold and no position; close when sentiment < threshold

### `backtest/evaluator.py`
- Runs `Backtest(...).run()`
- Prints: total return, Sharpe ratio, max drawdown, win rate
- Compares against buy-and-hold baseline
- Saves `bt.plot()` to `outputs/backtest_plot.html`

### `dashboard/app.py`
- Streamlit app with sidebar ticker + date range selectors
- Tab 1: live news feed with per-headline sentiment bars
- Tab 2: dual-axis chart — price line + sentiment score overlay
- Tab 3: signal log table (date, headlines, avg score, signal, next-day return)
- Tab 4: backtest stats panel

---

## Data flow (per ticker, per run)

```
NewsAPI headlines (raw)
  → finbert.score()           → [(headline, label, confidence), ...]
  → aggregator.aggregate()    → [(date, avg_sentiment), ...]
  → generator.generate()      → [(date, signal), ...]
  → merger.merge(prices)      → [(date, close, signal, return_next_day), ...]
  → strategy.run()            → backtest stats
```

---

## Configuration

Copy `.env.example` to `.env` and fill in:

```
NEWS_API_KEY=your_newsapi_key
BUY_THRESHOLD=0.1
SELL_THRESHOLD=-0.1
DEFAULT_TICKERS=AAPL,MSFT,TSLA
LOOKBACK_DAYS=30
```

---

## Limitations and known issues

- NewsAPI free tier: 1 month lookback, 100 articles/request
- FinBERT accuracy degrades on very short headlines (< 5 words)
- 1-day lag assumption is noisy; results vary significantly by ticker and period
- No slippage or market-impact modelling in the backtest
- Model runs on CPU by default; add `device=0` to the pipeline call for GPU
