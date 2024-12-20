import os
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog


# Select a directory using Tkinter
def select_filepath():
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()
    return Path(directory_path)


# Find all MP4 files in the specified directory
def collect_videos(directory: Path):
    return list(directory.rglob("*.mp4"))  # Recursively find all MP4 files


# Convert a single MP4 file to MP3
def convert_to_mp3(mp4_file: Path, output_directory: Path):
    output_file = output_directory / f"{mp4_file.stem}.mp3"
    command = f'ffmpeg -i "{mp4_file}" "{output_file}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Converted: {mp4_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {mp4_file}: {e}")


"""https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor"""
# Convert all videos in the selected directory
def convert_all_videos(mp4_directory: Path, output_directory: Path):
    output_directory.mkdir(exist_ok=True)  # Create output directory if it doesn't exist
    mp4_files = collect_videos(mp4_directory)

    
    with ThreadPoolExecutor() as executor:
        # Process each file in parallel
        for mp4_file in mp4_files:
            executor.submit(convert_to_mp3, mp4_file, output_directory)


if __name__ == "__main__":
    input_dir = select_filepath()
    output_dir = Path("output")

    if input_dir.is_dir():
        start_time = time.time()
        convert_all_videos(input_dir, output_dir)
        print(f"Conversion completed in {time.time() - start_time:.2f} seconds.")
    else:
        print("Invalid directory. Please check the path.")
