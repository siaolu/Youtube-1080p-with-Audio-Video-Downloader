# media_downloads.py
# This module handles downloading media from YouTube using the pytube library and processing it with moviepy.

from pytube import YouTube
import moviepy.editor as mpe
import os

from utils import slugify, FileMetadata, timelogger

@timelogger
def download_video(youtube, folder_name):
    """
    Download the highest resolution video from YouTube.
    
    Args:
        youtube (YouTube): An instance of pytube's YouTube class.
        folder_name (str): The directory where the video will be saved.
        
    Returns:
        tuple: A message indicating the result of the download and the status color.
    """
    video_stream = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if video_stream:
        file_path = video_stream.download(output_path=folder_name)
        return ("Video downloaded successfully.", "green")
    else:
        return ("No suitable video stream found.", "red")

@timelogger
def download_audio(youtube, folder_name):
    """
    Download the best quality audio from YouTube and convert it to mp3 format.
    
    Args:
        youtube (YouTube): An instance of pytube's YouTube class.
        folder_name (str): The directory where the audio will be saved.
        
    Returns:
        tuple: A message indicating the result of the download and the status color.
    """
    audio_stream = youtube.streams.get_audio_only()
    if audio_stream:
        output_file = audio_stream.download(output_path=folder_name)
        mp3_filename = os.path.splitext(output_file)[0] + '.mp3'
        convert_to_mp3(output_file, mp3_filename)
        return ("Audio downloaded and converted to MP3.", "green")
    else:
        return ("No audio stream available.", "red")

@timelogger
def convert_to_mp3(input_file, output_file):
    """
    Convert an audio file to MP3 format using moviepy.
    
    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output MP3 file.
    """
    audio_clip = mpe.AudioFileClip(input_file)
    audio_clip.write_audiofile(output_file)
    audio_clip.close()
    os.remove(input_file)

@timelogger
def download_and_combine(youtube, folder_name):
    """
    Download both video and audio, combine them into one file with high quality.
    
    Args:
        youtube (YouTube): An instance of pytube's YouTube class.
        folder_name (str): The directory where the combined file will be saved.
        
    Returns:
        tuple: A message indicating the result of the download and combination, and the status color.
    """
    video_file = download_video(youtube, folder_name)[0]
    audio_file = download_audio(youtube, folder_name)[0]
    combined_file = folder_name + "/combined.mp4"
    combine_video_audio(video_file, audio_file, combined_file)
    return ("Video and audio combined successfully.", "green")

def combine_video_audio(video_file, audio_file, output_file):
    """
    Combine video and audio files into a single video file.
    
    Args:
        video_file (str): The path to the video file.
        audio_file (str): The path to the audio file.
        output_file (str): The path for the output combined video file.
    """
    video_clip = mpe.VideoFileClip(video_file)
    audio_clip = mpe.AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec='libx264')
    video_clip.close()
    audio_clip.close()
    os.remove(video_file)
    os.remove(audio_file)
