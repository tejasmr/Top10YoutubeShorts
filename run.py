from definitions import FINANCE_FILE, FINANCE_LINK
from logger import logger
from scraper import collect_video_metadata

if __name__ == "__main__":
    collect_video_metadata(FINANCE_LINK, FINANCE_FILE, "Finance")
    logger.info('Ran the program successfully')