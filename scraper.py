from datetime import datetime
from glob import glob
import os
from time import sleep
from logger import logger
from driver import driver
from definitions import CLASS_NAME, TAG_NAME
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def get_link(link):
    driver.get(link)
    sleep(5)

def scrape_videos(link, file, label):
    title = ""
    get_link(link)
    videos = driver.find_elements(by=TAG_NAME, value=f"ytd-video-renderer")
    
    logger.debug("number of videos found = " + str(len(videos)))

    videos = videos[:10]
    links = []
    titles = []
    channels = []
    video_links = []
    
    for video in videos:
        video_link = video.find_element(by=TAG_NAME, value='a').get_attribute('href')
        video_title = video.find_element(by=TAG_NAME, value='a').get_attribute('title')
        video_channel = video.find_element(by=CLASS_NAME, value="yt-simple-endpoint style-scope yt-formatted-string")
        yt = YouTube(video_link)
        links.append(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download())
        video_links.append(video_link)
        titles.append(video_title)
        channels.append(video_channel)
    
    links = links[::-1]
    titles = titles[::-1]
    channels = channels[::-1]
    video_links = video_links[::-1]

    if os.path.exists(file):
        os.remove(file)

    clips = []
    title = f"Top {len(links)} {label} shorts of the day {datetime.today()}"
    description = "Disclaimer : No copyright intention, I do not own the audio, video or the images in this video. All rights belong to the rightful owner. \n\nCredits: \n" 
    for i in range(10):
        description += f'{10-i}. {channels[i]} - {titles[i]} : {video_links[i]}\n'
    for i in range(0, len(links)):
        textclip = TextClip(str(10-i), fontsize=100, color='white', stroke_color='black', align='West')
        textclip = textclip.set_position((0, 0))
        videoclip = VideoFileClip(links[i])
        compositeclip = CompositeVideoClip([textclip, videoclip])
        clips.append(compositeclip.set_duration(videoclip.duration))

    final = concatenate_videoclips(clips, method="compose")
    logger.info("Final video duration: " + str(final.duration))
    final.write_videofile(file)

    for file in glob("*.mp4"):
        logger.info(file)
        if file != file:
            os.remove(file)