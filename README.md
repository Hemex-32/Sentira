# SENTIRA PRO // Institutional Sentiment Terminal

An automated, paper-trading intelligence platform that decodes financial news headlines using FinBERT, generates actionable signals (BUY/HOLD/SELL), and backtests vectors against real-time market OHLCV data. 

Featuring the **Terminal Obsidian V2** design system—a production-grade, industrial-utilitarian interface.

---

## Architecture Overview

```text
[ DATA INGESTION ] ───────► [ NLP ENGINE ] ────────► [ STRATEGY VECTORS ]
NewsAPI + yfinance          FinBERT Core             Vectorized Backtesting
        │                         │                           │
        └─────────────────────────┴─────────► [ TERMINAL OBSIDIAN DASHBOARD ]
```

## Features

- **Terminal Obsidian UI**: A high-craft, precision-focused interface featuring a responsive blueprint grid, fluid typography (`Space Grotesk` x `JetBrains Mono`), and mechanical haptic motion.
- **FinBERT NLP Core**: Deep learning architecture specialized for extracting semantic sentiment from high-frequency financial headlines.
- **Vectorized Backtesting**: High-speed evaluation of signal performance (Sharpe, Drawdown, Alpha) against historical volatility.
- **Live Synergy Stream**: Real-time ticker and intelligence feed merging Yahoo Finance data with global news streams.
- **Automated Scheduler**: Built-in APScheduler (`scheduler.py`) for midnight data synchronization and analysis execution.

---

## Project Structure

```text
sentira/
├── main.py                   # Pipeline execution entry point
├── scheduler.py              # Automated daily data synchronization
├── requirements.txt          # Dependencies
├── .env.example              # Environment variable template
├── data/                     # Ingestion layer (NewsAPI, yfinance)
├── models/                   # NLP & Sentiment aggregation
├── signals/                  # Signal generation & price merging
├── backtest/                 # Strategy evaluation & stats
└── dashboard/
    └── app.py                # Streamlit Terminal UI
```

## Quick Start

### 1. Environment Setup
```bash
git clone https://github.com/Hemex-32/Sentira.git
cd Sentira
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Copy the environment template and add your API keys:
```bash
cp .env.example .env
```
Ensure your `.env` contains:
```env
NEWS_API_KEY=your_key_here
DEFAULT_TICKERS=AAPL,MSFT,NVDA,TSLA,BTC-USD
LOOKBACK_DAYS=30
```

### 3. Launch the Terminal
```bash
streamlit run dashboard/app.py
```

### 4. Enable Automation (Optional)
To run the automated midnight synchronization job:
```bash
python scheduler.py
```

---

## Limitations & Disclaimers

- **Not Financial Advice**: This project demonstrates a complete ML pipeline. It does not claim live trading alpha. Sentiment-price correlation is inherently noisy.
- **API Limits**: The NewsAPI free tier is limited to a 1-month lookback and 100 articles per request.
- **Hardware**: The NLP model runs on CPU by default.

## License
MIT License
