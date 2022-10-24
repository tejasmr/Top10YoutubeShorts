from logger import logger
from driver import driver
from definitions import CSS_SELECTOR

def collect_video_metadata(link):
    driver.get(link)
    videos = []
    for i in range(2, 2 + 10 - 1):
        try:
            videos.append(driver.find_element(by=CSS_SELECTOR, value=f"#contents > ytd-video-renderer:nth-child({i})"))
        except:
            pass
    # .style-scope.ytd-item-section-renderer
    logger.debug("number of videos found = " + str(len(videos)))
    logger.debug("videos found = " + str(videos))