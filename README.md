# ffmpeg-fragment-cutter

This tool allows you to extract a fragment from a video file, starting at a specified time and ending at another specified time. It also supports extracting audio and subtitles from the video.

## Requirements
- Python 3.x
- FFmpeg (for video processing)
- FFprobe (for analyzing video)

## Installation
Install FFmpeg following the instructions on the official site.

Ensure that FFmpeg and FFprobe are available in your system's PATH.

## Usage
1. Run the script:

```bash
python ffmpeg_fragment_cutter.py
```

2. Enter the path to the video file you want to split.

3. Specify the start time for the video split in the following format:

- 75 —> 75 seconds
- 12.100 —> 12 seconds and 100 milliseconds
- 1:12 —> 1 minute and 12 seconds
- 1:12.50 —> 1 minute, 12 seconds, and 50 milliseconds
- 1:01:12.500 —> 1 hour, 1 minute, 12 seconds, and 500 milliseconds

4. Specify the end time (if required), or leave it empty to split until the end of the video.

5. The program will list all available audio tracks and subtitles from the video. You can select which ones to save.

- For audio: Enter the indices of the audio tracks you want to save (Example: 0 1 2) or skip.
- For subtitles: Enter the indices of the audio tracks you want to save (Example: 0 1 2) or skip.

6. The program will create a new file with the selected time range and selected streams.

## Example
```bash
Enter the path to the video file: "path/to/video.mp4"
--------------------------------------------------------
Video duration: 00:05:30.000
--------------------------------------------------------
Enter the start time (leave empty for 0): 1:00
Enter the end time (leave empty for the end of the video): 1:30
--------------------------------------------------------
Audio streams:
Index: 0, Title: N/A, Language: ru
Index: 1, Title: N/A, Language: en
Select audio streams to save (Example: 0 1 2, leave empty to skip): 1
--------------------------------------------------------
Subtitles:
Index: 0, Title: N/A, Language: ru
Index: 1, Title: N/A, Language: en
Select subtitles to save (Example: 0 1 2, leave empty to skip): 0
--------------------------------------------------------
```
