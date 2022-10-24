from logger import logger
from driver import driver
from definitions import CSS_SELECTOR

def collect_video_metadata(link):
    driver.get(link)
    videos = driver.find_elements(by=CSS_SELECTOR, value="ytd-video-renderer.style-scope.ytd-item-section-renderer")
    logger.debug("number of videos found = ", len(videos))