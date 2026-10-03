# Nightcore Maker

Python script to make a nightcore version of an audio file or YouTube link.

## Usage

```bash
python3 nightcore.py <input_file_or_url> [speed_factor] [pitch_factor]
```

Example:

```bash
python3 nightcore.py song.mp3
python3 nightcore.py song.mp3 1.25 1.25
python3 nightcore.py "https://youtube.com/watch?v=..."
```

## Requirements

- Python 3
- ffmpeg
- yt-dlp

It downloads audio, changes tempo/pitch, and saves the result as `_nightcore.mp3`.
