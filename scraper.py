from datetime import datetime
import os
from time import sleep
from logger import logger
from driver import driver
from definitions import CSS_SELECTOR, TAG_NAME
from pytube import YouTube
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, vfx

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
        ele = video.find_element(by=TAG_NAME, value='a')
        video_link = ele.get_attribute('href')
        video_title = ele.get_attribute('title')
        video_channel = video.find_element(by=CSS_SELECTOR, value=".yt-simple-endpoint.style-scope.yt-formatted-string").text
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
        textclip = TextClip(str(10-i), fontsize=100, color='white', stroke_color='black', align='West', font='Lato-Black')
        textclip = textclip.set_position((10, 10))
        videoclip = VideoFileClip(links[i])
        compositeclip = CompositeVideoClip([videoclip, textclip])
        compositeclip = compositeclip.fx(vfx.speedx, 1.1)
        clips.append(compositeclip.set_duration(videoclip.duration))

    final = concatenate_videoclips(clips, method="compose")
    logger.info("Final video duration: " + str(final.duration))
    final.write_videofile(file, threads=4, logger=None)

    command = f'python3 upload_video.py --noauth_local_webserver --file "{file}" --title "{title}" --description "{description}" --privacyStatus public'

    # os.listdir()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    for file_name in links:
        logger.info(file_name)
        os.remove(file_name.split("/")[-1])
