from unicodedata import category
from definitions import categories
from logger import logger
from scraper import cleanup_all_intermediate_videos, dump_data, load_data, scrape_videos, upload_video_to_youtube

if __name__ == "__main__":

    for cat in categories:
        logger.info(f"Running script for category {cat.label}")
        file, title, description = scrape_videos(cat.link, cat.file, cat.label)
        dump_data(file, title, description)
        file, title, description = load_data()
        upload_video_to_youtube(file, title, description)
        cleanup_all_intermediate_videos()

    logger.info('Ran the program successfully')