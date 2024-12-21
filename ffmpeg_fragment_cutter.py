import os
import json
import subprocess


def time_to_milliseconds(time_str):
    hours, minutes, seconds, milliseconds = [int(el) for el in time_str]
    total_milliseconds = (((hours * 60 + minutes) * 60) + seconds) * 1000 + milliseconds

    return total_milliseconds


def milliseconds_to_ffmpeg_format(milliseconds):
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"


def get_stream_info(input_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-print_format', 'json',
        '-show_streams',
        '-show_entries', 'stream=index,codec_type,codec_name,codec_long_name,profile,width,height,channels,channel_layout,sample_rate,bit_rate,language,title',
        input_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        streams_info = json.loads(result.stdout)

        return streams_info
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")

        return {}


def get_duration(input_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        duration_seconds = float(result.stdout.strip())
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000

        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")

        return "00:00:00.000"


def split_video(input_path, start_time, end_time=None):
    folder, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)

    if end_time is not None:
        output_name = f"{name} from {start_time} to {end_time}{ext}"
    else:
        output_name = f"{name} from {start_time}{ext}"

    output_path = os.path.join(folder, output_name)

    start_ms = time_to_milliseconds(start_time)
    start_ffmpeg = milliseconds_to_ffmpeg_format(start_ms)

    cmd = f'ffmpeg -y -loglevel quiet -ss {start_ffmpeg} -i "{input_path}"'

    if end_time is not None:
        end_ms = time_to_milliseconds(end_time)
        duration_ms = end_ms - start_ms
        duration_ffmpeg = milliseconds_to_ffmpeg_format(duration_ms)
        cmd += f' -t {duration_ffmpeg}'

    streams = get_stream_info(input_path)

    audio_streams = [stream for stream in streams['streams'] if stream.get('codec_type') == 'audio']
    subtitle_streams = [stream for stream in streams['streams'] if stream.get('codec_type') == 'subtitle']

    cmd += ' -map 0:v:0'

    if audio_streams:
        print("--------------------------------------------------------")
        print("Audio streams:")

        for i, audio in enumerate(audio_streams):
            language = audio.get('tags', {}).get('language', 'N/A')
            title = audio.get('tags', {}).get('title', 'N/A')

            print(f"Index: {i}, Title: {title}, Language: {language}")

        audio_indices = input("Select audio streams to save (Example: 0 1 2, leave empty to skip): ").split()

        if audio_indices:
            audio_indices = ' '.join(f"-map 0:a:{idx}" for idx in audio_indices)
            cmd += f' {audio_indices}'

    if subtitle_streams:
        print("--------------------------------------------------------")
        print("Subtitles:")

        for i, subtitle in enumerate(subtitle_streams):
            language = subtitle.get('tags', {}).get('language', 'N/A')
            title = subtitle.get('tags', {}).get('title', 'N/A')

            print(f"Index: {i}, Title: {title}, Language: {language}")

        subtitle_indices = input("Select subtitles to save (Example: 0 1 2, leave empty to skip): ").split()
        print("--------------------------------------------------------")

        subtitle_indices = ' '.join(f"-map 0:s:{idx}" for idx in subtitle_indices)
        cmd += f' {subtitle_indices}'

    cmd += f' -c copy "{output_path}"'

    print(f"Executing command: {cmd}")
    os.system(cmd)


def get_time_input(prompt):
    while True:
        time_str = input(f"{prompt}: ").strip()

        if not time_str:
            return ['0', '0', '0', '000']

        try:
            if '.' in time_str and ':' not in time_str:
                seconds, milliseconds = time_str.split('.')
                milliseconds = milliseconds.ljust(3, '0')
                hours, minutes, seconds = 0, 0, int(seconds)
                time_parts = [0, 0, int(seconds)]
            elif '.' in time_str:
                main_time, milliseconds = time_str.split('.')
                milliseconds = milliseconds.ljust(3, '0')
                time_parts = [int(el) for el in main_time.split(':')]
            else:
                main_time, milliseconds = time_str, '000'
                time_parts = [int(el) for el in main_time.split(':')]

            if len(time_parts) == 1:
                hours, minutes, seconds = 0, 0, time_parts[0]
            elif len(time_parts) == 2:
                hours, minutes, seconds = 0, time_parts[0], time_parts[1]
            elif len(time_parts) == 3:
                hours, minutes, seconds = time_parts
            else:
                raise ValueError("Invalid time format.")

            return [hours, minutes, seconds, milliseconds]

        except ValueError:
            print("Invalid input. Ensure the time format is correct (hh:mm:ss.mmm).")


def main():
    print("Examples of valid time input:")
    print("75 —> 75 seconds")
    print("12.100 —> 12 seconds, 100 milliseconds")
    print("1:12 —> 1 minute, 12 seconds")
    print("1:12.50 —> 1 minute, 12 seconds, 50 milliseconds")
    print("1:01:12.500 —> 1 hour, 1 minute, 12 seconds, 500 milliseconds")
    print("--------------------------------------------------------")

    input_path = input("Enter the path to the video file: ").strip('"')
    print("--------------------------------------------------------")

    duration = get_duration(input_path)

    print(f"Video duration: {duration}")
    print("--------------------------------------------------------")

    start_time = get_time_input("Enter the start time (leave empty for 0)")
    end_time_input = get_time_input("Enter the end time (leave empty for the end of the video)")
    print("--------------------------------------------------------")
    end_time = None if all(el == '0' or el == '000' for el in end_time_input) else end_time_input

    split_video(input_path, start_time, end_time)


if __name__ == "__main__":
    main()
