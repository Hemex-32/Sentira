from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_pipeline
from utils.config import DEFAULT_TICKERS, LOOKBACK_DAYS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SentiraScheduler")

def scheduled_job():
    logger.info("Starting daily sentiment analysis job...")
    if not DEFAULT_TICKERS:
        logger.warning("No tickers configured in DEFAULT_TICKERS.")
        return

    for ticker in DEFAULT_TICKERS:
        try:
            logger.info(f"Executing pipeline for {ticker}...")
            run_pipeline(ticker, days=LOOKBACK_DAYS)
        except Exception as e:
            logger.error(f"Failed to run pipeline for {ticker}: {e}")
    logger.info("Daily job completed.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Schedule job to run every day at 00:00 (midnight)
    scheduler.add_job(scheduled_job, 'cron', hour=0, minute=0)
    
    logger.info("Scheduler initialized. Daily job set for 00:00.")
    logger.info("Press Ctrl+C to exit.")
    
    # Run once at startup for immediate data synchronization
    logger.info("Running initial data synchronization...")
    scheduled_job()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
