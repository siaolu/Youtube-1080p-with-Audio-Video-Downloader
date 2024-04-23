# media_downloads.py
# Version 0.54
# Provides functions for downloading media, extracting audio, and retrieving metadata from videos. Enhanced for robust and scalable asynchronous operations.

import asyncio
from pytube import YouTube
import moviepy.editor as mpe
from config import statlogtimer

@statlogtimer
async def download_video(url, output_path):
    """Asynchronously download a video from YouTube.
    
    Args:
        url (str): URL of the YouTube video.
        output_path (str): Directory path where the video will be saved.
    
    Returns:
        str: Filename of the downloaded video or None if the download fails.
    """
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            return await asyncio.to_thread(video.download, output_path=output_path)
    except Exception as e:
        raise RuntimeError(f"Failed to download video from {url}: {e}")

@statlogtimer
def extract_audio(video_path):
    """Extract audio from the downloaded video file.
    
    Args:
        video_path (str): Path to the video file.
    
    Returns:
        str: The path to the MP3 file or None if extraction fails.
    """
    try:
        clip = mpe.VideoFileClip(video_path)
        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        clip.audio.write_audiofile(audio_path)
        clip.close()
        return audio_path
    except Exception as e:
        raise RuntimeError(f"Failed to extract audio from {video_path}: {e}")
