# media_downloads.py
# Version 0.52
# Handles asynchronous downloading of media from YouTube, extracting audio, 
# and logging download status to a SQLite database managed by app_main.py.

import asyncio
from pytube import YouTube
import moviepy.editor as mpe
import os
from config import statlogtimer, get_db

@statlogtimer
async def download_video(url, output_path):
    """
    Asynchronously downloads the highest quality video from a YouTube URL.

    Args:
        url (str): URL of the YouTube video.
        output_path (str): Directory path where the video will be saved.

    Returns:
        str: Filename of the downloaded video or None if download fails.
    """
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            filename = await asyncio.to_thread(video.download, output_path=output_path)
            log_download_success(url, filename)
            return filename
    except Exception as e:
        log_download_failure(url, str(e))
        return None

@statlogtimer
def extract_audio(video_path):
    """
    Extracts audio from a video file and saves it as an MP3.

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
        print(f"Failed to extract audio: {e}")
        return None

def log_download_success(url, filename):
    db = get_db()
    db.execute('INSERT INTO downloads (url, status, filename) VALUES (?, ?, ?)', (url, 'success', filename))
    db.commit()

def log_download_failure(url, error_message):
    db = get_db()
    db.execute('INSERT INTO downloads (url, status, error) VALUES (?, ?, ?)', (url, 'failure', error_message))
    db.commit()

if __name__ == "__main__":
    # This block is only for testing purposes
    import sys
    url = sys.argv[1]  # Assume the URL is passed as the first command-line argument
    output_path = sys.argv[2]  # Assume the output path is passed as the second command-line argument
    asyncio.run(download_video(url, output_path))
