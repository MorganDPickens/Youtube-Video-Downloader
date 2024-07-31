# Youtube downloader created by BlackSmith Ether

import subprocess
import sys
import os
import zipfile
import platform
from urllib.request import urlretrieve
from tkinter import Tk
from tkinter.filedialog import askdirectory

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_ffmpeg():
    """Check if ffmpeg is installed and in the system path."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ffmpeg is installed and available.")
        return True
    except FileNotFoundError:
        print("ffmpeg is not installed or not in the system PATH.")
        return False

def download_ffmpeg():
    """Download and set up ffmpeg for the system."""
    print("Downloading ffmpeg...")
    if platform.system() == "Windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    elif platform.system() == "Darwin":
        url = "https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip"  # URL for macOS ffmpeg binaries
    else:
        print("Please manually install ffmpeg from https://ffmpeg.org/download.html for your OS.")
        sys.exit(1)
    
    output = "ffmpeg.zip"
    urlretrieve(url, output)
    print("Extracting ffmpeg...")
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall("ffmpeg")
    os.remove(output)
    
    extracted_dir = [name for name in os.listdir("ffmpeg") if os.path.isdir(os.path.join("ffmpeg", name))][0]
    ffmpeg_bin_path = os.path.join(os.getcwd(), "ffmpeg", extracted_dir, "bin")
    
    # Ensure the correct path is used
    add_to_path(ffmpeg_bin_path)
    print(f"ffmpeg extracted to: {ffmpeg_bin_path}")
    print("ffmpeg installation and PATH update complete.")

def add_to_path(new_path):
    """Add a new path to the system PATH environment variable."""
    try:
        if new_path not in os.environ['PATH']:
            os.environ['PATH'] = f"{new_path};{os.environ['PATH']}"
            subprocess.run(['setx', 'PATH', os.environ['PATH']], check=True)
            print(f"Added {new_path} to PATH.")
        else:
            print(f"{new_path} is already in PATH.")
    except Exception as e:
        print(f"Failed to add {new_path} to PATH: {e}")

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Installing now...")
    install("yt-dlp")
    import yt_dlp

def check_video_availability(url):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        print("The YouTube URL is valid and the video is available for download.")
        return info_dict
    except yt_dlp.utils.DownloadError as e:
        print(f"The video could not be processed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def download_video_and_audio(url, path, resolution):
    try:
        video_outtmpl = os.path.join(path, 'video.%(ext)s')
        audio_outtmpl = os.path.join(path, 'audio.%(ext)s')
        final_outfile = os.path.join(path, 'final_video.mp4')

        ydl_opts = {
            'outtmpl': video_outtmpl,
            'format': f'bestvideo[height<={resolution}]',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        ydl_opts = {
            'outtmpl': audio_outtmpl,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Manually merge video and audio using ffmpeg, ensuring compatibility with QuickTime
        video_file = [f for f in os.listdir(path) if f.startswith("video")][0]
        audio_file = [f for f in os.listdir(path) if f.startswith("audio")][0]

        merge_command = [
            'ffmpeg', '-i', os.path.join(path, video_file),
            '-i', os.path.join(path, audio_file),
            '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast',
            '-c:a', 'aac', '-b:a', '192k', '-strict', 'experimental',
            final_outfile
        ]
        subprocess.run(merge_command)
        print("Download and merge complete! The file is saved as 'final_video.mp4'.")
    except Exception as e:
        print(f"An error occurred during the download: {e}")

if __name__ == "__main__":
    # Detect OS
    os_type = platform.system()
    print(f"Detected operating system: {os_type}")

    # Check if ffmpeg is installed
    if not check_ffmpeg():
        download_ffmpeg()

    # Ask the user to input the YouTube video URL
    url = input("Enter the YouTube video URL: ")
    print("Checking if the YouTube URL is valid and the video is available for download...")
    
    info_dict = check_video_availability(url)
    if info_dict:
        # Ask the user to select the desired video quality
        print("Select the desired video quality:")
        print("1. 720p")
        print("2. 1080p")
        print("3. 1440p")
        print("4. 4K")
        quality_option = input("Enter the number corresponding to your choice: ")

        quality_map = {
            '1': 720,
            '2': 1080,
            '3': 1440,
            '4': 2160
        }

        if quality_option in quality_map:
            resolution = quality_map[quality_option]
        else:
            print("Invalid choice. Defaulting to 720p.")
            resolution = 720

        # Open a file dialog to select the download directory
        root = Tk()
        root.withdraw()  # Hide the main window
        download_path = askdirectory(title="Select Download Folder")
        
        if download_path:
            download_video_and_audio(url, download_path, resolution)
        else:
            print("No directory selected. Exiting.")
    else:
        print("Exiting due to invalid or unavailable video.")
