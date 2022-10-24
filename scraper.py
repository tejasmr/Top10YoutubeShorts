from time import sleep
from logger import logger
from driver import driver
from definitions import TAG_NAME
from pytube import YouTube

def get_link(link):
    driver.get(link)
    sleep(5)

def collect_video_metadata(link):
    get_link(link)
    videos = driver.find_elements(by=TAG_NAME, value=f"ytd-video-renderer")
    # for i in range(2, 2 + 10 - 1):
    #     try:
    #         videos.append(driver.find_element(by=CLASS_NAME, value=f"style-scope ytd-item-section-renderer"))
    #     except:
    #         pass
    # .style-scope.ytd-item-section-renderer
    logger.debug("number of videos found = " + str(len(videos)))
    logger.debug("videos found = " + str(videos))
    for video in videos[:10]:
        video_link = video.find_element(by=TAG_NAME, value='a').get_attribute('href')
        yt = YouTube(video_link)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
