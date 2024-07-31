
![github-header-image(4)](https://github.com/user-attachments/assets/8b971df7-1a18-4468-98c5-2a3744d99785)



Short explanation-(IMPORTANT -To use this downloader the best way is to download python and run it on the python launcher. This code will auto install anything you need to get it to work also gives 3 videos. no sound, mp3 audio, and final_video audio and video, you can also choose quality. This file downloader i created has 2 version.

VERSION 1. wiNDOWS ONLY
VERSION 2. MAC/WINDOWS

Long explination.-----YouTube Downloader is a Python-based tool created by BlackSmith Ether to download videos from YouTube. It uses the yt_dlp library to handle video extraction and download, while ffmpeg is employed to merge video and audio tracks, ensuring compatibility with various media players. This tool allows users to choose the quality of the video and select the download directory.
Features

    Automatic Dependency Management: Installs required packages like yt_dlp if not already present.
    FFmpeg Integration: Checks for the presence of ffmpeg and downloads it if not found, ensuring it's available in the system path.
    Customizable Video Quality: Users can choose between 720p, 1080p, 1440p, and 4K resolutions.
    Cross-Platform Compatibility: Supports Windows, macOS, and other operating systems.

How It Works

    OS Detection: The script first detects the user's operating system.
    FFmpeg Check & Installation: It checks if ffmpeg is installed. If not, it downloads and sets up the appropriate version for the detected OS.
    YouTube URL Validation: The script prompts the user for a YouTube video URL and verifies if the video is available for download.
    Quality Selection: Users are prompted to select the desired video quality.
    Download Directory Selection: A file dialog allows users to choose the directory where the video will be saved.
    Video & Audio Download: The video and audio are downloaded separately using yt_dlp.
    Merging Video & Audio: The downloaded video and audio files are merged into a single MP4 file using ffmpeg.

Requirements

    Python 3.x
    Internet connection
    Permissions to install software on the system

Installation & Setup

    Install Python: Ensure you have Python 3.x installed on your system.
    Run the Script: Execute the script using Python.

    bash

    python youtube_downloader.py

    Follow Prompts: Enter the YouTube video URL, select the desired quality, and choose the download directory.

Usage

Simply run the script and follow the on-screen instructions. The downloaded and merged video file will be saved in the chosen directory as final_video.mp4.
