from definitions import FINANCE_FILE, FINANCE_LINK
from logger import logger
from scraper import scrape_videos

if __name__ == "__main__":
    scrape_videos(FINANCE_LINK, FINANCE_FILE, "Finance")
    logger.info('Ran the program successfully')