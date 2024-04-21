# media_downloads.py
from pytube import YouTube
import moviepy.editor as mpe
import os

def download_video(url, output_path):
    """
    Downloads the highest quality video from a YouTube URL.

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
            return video.download(output_path=output_path)
    except Exception as e:
        print(f"Failed to download video: {e}")
        return None

def extract_audio(video_path, output_path):
    """
    Extracts audio from a video file and saves it as mp3.

    Args:
        video_path (str): Path to the video file.
        output_path (str): Path where the mp3 should be saved.

    Returns:
        str: The path to the mp3 file or None if extraction fails.
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

def combine_video_audio(video_path, audio_path, output_path):
    """
    Combines video and audio into a single video file.

    Args:
        video_path (str): Path to the video file.
        audio_path (str): Path to the audio file.
        output_path (str): Output path for the combined video file.

    Returns:
        str: Path to the combined video file or None if combination fails.
    """
    try:
        video_clip = mpe.VideoFileClip(video_path)
        audio_clip = mpe.AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_file = os.path.join(output_path, os.path.basename(video_path))
        final_clip.write_videofile(final_file)
        video_clip.close()
        audio_clip.close()
        return final_file
    except Exception as e:
        print(f"Failed to combine video and audio: {e}")
        return None
