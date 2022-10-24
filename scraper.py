from logger import logger
from driver import driver
from definitions import TAG_NAME

def collect_video_metadata(link):
    driver.get(link)
    logger.debug(driver.page_source)
    videos = driver.find_elements(by=TAG_NAME, value=f"ytd-video-renderer")
    # for i in range(2, 2 + 10 - 1):
    #     try:
    #         videos.append(driver.find_element(by=CLASS_NAME, value=f"style-scope ytd-item-section-renderer"))
    #     except:
    #         pass
    # .style-scope.ytd-item-section-renderer
    logger.debug("number of videos found = " + str(len(videos)))
    logger.debug("videos found = " + str(videos))