import os
import random
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="The folder to pick video from")
parser.add_argument('-r', '--recursive', action='store_true',
                    help='recursively search subdirectories')
parser.add_argument('-o', '--open', action='store_true',
                    help='open the folder containing video')
parser.add_argument('-p', '--playlist', default=None, type=str,
                    help='make a playlist of videos in random order')

args = parser.parse_args()

folder = args.folder

video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv"]

if args.recursive:
    video_files = [os.path.join(root, f) for root, dirs, files in os.walk(folder) for f in files if f.endswith(tuple(video_extensions))]
else:
    video_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(tuple(video_extensions))]


if len(video_files) == 0:
    print("No video files found in folder.")
    exit()

playlist_file = args.playlist
if playlist_file:
    random.shuffle(video_files)
    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write("\n".join(video_files))
else:
    random_video_file = random.choice(video_files)
    print(random_video_file)

    if sys.platform.startswith("win"):
        command = f'start "" "{random_video_file}"'
        if args.open:
            explorer_path = os.path.dirname(random_video_file)
            #everything = r"C:\Program Files\Everything\Everything.exe"
            subprocess.Popen(f'explorer /select,"{random_video_file}"')
            #subprocess.Popen(fr'"{everything}" -parent "{explorer_path}" -select "{random_video_file}"')

    else:
        command = f'xdg-open "{random_video_file}"'

    subprocess.call(command, shell=True)
