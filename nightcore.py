#!/usr/bin/env python3
import os 
import sys
import subprocess

def yt_download(url: str) -> str:
    output_template = "%(title)s.%(ext)s"
    result = subprocess.run(
        [
            "yt-dlp",
            "-f",
            "bestaudio/best",
            "--no-playlist",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--embed-thumbnail",
            "--output",
            output_template,
            "--print",
            "after_move:filepath",
            url,
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    downloaded_file = result.stdout.strip().splitlines()[-1:]
    if not downloaded_file or not os.path.isfile(downloaded_file[0]):
        print("Error: yt-dlp did not report a downloaded audio file.")
        sys.exit(1)
    return downloaded_file[0]

def make_nightcore(input_file: str, speed_factor: float = 0, pitch_factor: float = 0) -> str:

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    if speed_factor <= 0 or pitch_factor <= 0:
        print("Error: Speed and pitch factors must be positive numbers.")
        sys.exit(1)

    print(f"Processing '{input_file}' with speed factor '{speed_factor}' and pitch factor '{pitch_factor}' ...")

    output_file = os.path.splitext(input_file)[0] + "_nightcore.mp3"
    overwrite_existing = False
    while os.path.isfile(output_file):
        choice = input(
            f"File '{output_file}' is existing. [O] Overwrite, [C] Change name, [A] Cancel: "
        ).strip().lower()

        if choice in ("o", "overwrite"):
            overwrite_existing = True
            break
        if choice in ("c", "change"):
            new_output_file = input("Enter the new output file name: ").strip()
            if not new_output_file:
                print("The name cannot be empty.")
                continue
            output_file = new_output_file
            overwrite_existing = False
            continue
        if choice in ("a", "cancel"):
            print("Canceled.")
            sys.exit(0)

        print("Enter O (overwrite), C (change name) or A (cancel).")

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostats",
            "-y" if overwrite_existing else "-n",
            "-i",
            input_file,
            "-map",
            "0:a:0",
            "-map",
            "0:v:disp:attached_pic?",
            "-map_metadata",
            "0",
            "-c:v",
            "copy",
            "-id3v2_version",
            "3",
            "-filter:a",
            f"rubberband=tempo={speed_factor}:pitch={pitch_factor}",
            "-q:a",
            "2",
            output_file,
        ],
        check=True,
    )

    print(f"Nightcore version saved as '{output_file}'")

    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python nightcore.py <input_file_or_url> [speed_factor] [pitch_factor]")
        sys.exit(1)

    input_file = sys.argv[1]
    if input_file.startswith(("http://", "https://")):
        input_file = yt_download(input_file)

    speed_factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.25
    pitch_factor = float(sys.argv[3]) if len(sys.argv) > 3 else 1.25

    make_nightcore(input_file, speed_factor, pitch_factor)

if __name__ == "__main__":
    main()

