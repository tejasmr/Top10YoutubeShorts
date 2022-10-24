from unicodedata import category
from definitions import FINANCE_FILE, FINANCE_LINK,  categories
from logger import logger
from scraper import scrape_videos

if __name__ == "__main__":
    for cat in categories:
        scrape_videos(cat.link, cat.file, cat.label)
    logger.info('Ran the program successfully')