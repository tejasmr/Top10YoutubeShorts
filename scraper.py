from datetime import datetime
from distutils.command.upload import upload
import os
from time import sleep
from logger import logger
from driver import driver
from definitions import CSS_SELECTOR, TAG_NAME, ID
from pytube import YouTube
from glob import glob
import subprocess
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, vfx

def get_link(link):
    driver.get(link)
    sleep(5)

def get_videos(link):
    logger.info("Created a driver...")
    
    logger.info(f"Hitting {link}...")
    get_link(link)

    logger.info("Trying to find video elements...")
    return driver.find_elements(by=TAG_NAME, value=f"ytd-video-renderer")[:10]


def collect_video_metadata(video, index, links, titles, channels, video_links):
    logger.info(f"Trying to find video metadata for video no. {index+1}...")

    ele = video.find_element(by=ID, value='video-title')

    video_link = ele.get_attribute('href')
    video_title = ele.get_attribute('title')
    video_channel = video.find_element(by=CSS_SELECTOR, value=".yt-simple-endpoint.style-scope.yt-formatted-string").get_attribute('text')
    
    yt = YouTube(video_link)
    
    links.append(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download())
    video_links.append(video_link)
    titles.append(video_title)
    channels.append(video_channel)


def collect_metadata_videos(link):
    logger.info("Capturing metadata for videos")

    links = []
    titles = []
    channels = []
    video_links = []
    videos = get_videos(link)

    for index, video in enumerate(videos):
        collect_video_metadata(video, index, links, titles, channels, video_links)
    
    return links[::-1], titles[::-1], channels[::-1], video_links[::-1]

def cleanup_previous_video(file):
    logger.info(f"Deleting the previous video file {file}...")

    if os.path.exists(file):
        os.remove(file)

def create_title(links, label):
    logger.info("Creating video title...")
    
    return f"Top {len(links)} {label} shorts of the day {datetime.today()}"

def create_description(n, titles, channels, video_links):
    logger.info("Creating video description...")

    description = "Disclaimer : No copyright intention, I do not own the audio, video or the images in this video. All rights belong to the rightful owner. \n\nCredits: \n" 

    for i in range(n):
        description += f'{n-i}. {channels[i]} - {titles[i]} : {video_links[i]}\n'
    
    return description

def create_composite_clips(links):
    logger.info("Creating a composite clips...")
    clips = []

    for i in range(0, len(links)):
        textclip = TextClip(str(10-i), fontsize=100, color='white', stroke_color='black', align='West', font='Lato-Black')
        textclip = textclip.set_position((10, 10))
        videoclip = VideoFileClip(links[i])
        compositeclip = CompositeVideoClip([videoclip, textclip])
        compositeclip = compositeclip.fx(vfx.speedx, 1.1)
        clips.append(compositeclip.set_duration(videoclip.duration))

    return clips

def cleanup_all_intermediate_videos():
    logger.info("Cleaning up all intermediate videos...")
    for file_name in glob('*.mp4'):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            logger.warning(f"{file_name} not found")

def upload_video_to_youtube(file, title, description):

    logger.info("Uploading to youtube...")
    command = ' '.join(['python', 'upload_video.py', f'--file="{file}"', f'--title="{title}"', f'--description="{description}"', '--privacyStatus="public"'])

    # os.listdir()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    logger.debug(str(stdout, 'UTF-8'))
    logger.debug(str(stderr, 'UTF-8'))

def scrape_videos(link, file, label):

    links, titles, channels, video_links = collect_metadata_videos(link)
    cleanup_previous_video(file)

    clips = create_composite_clips(links)
    
    logger.info("Concatenating the composite clips...")
    final_video = concatenate_videoclips(clips, method="compose")

    logger.info("Writing to file...")
    # final.write_videofile(file, threads=4, logger=None)
    final_video.write_videofile(file, threads=4)

    title = create_title(links, label)
    description = create_description(len(links), titles, channels, video_links)

    return file, title, description

def dump_data(file, title, description):
    with open('metadata.json', 'w') as json_file:
        json.dump({'file': file, 'title': title, 'description': description}, json_file)

def load_data():
    with open('metadata.json', 'r') as json_file:
        data = json.load(json_file)
        return data['file'], data['title'], data['description']