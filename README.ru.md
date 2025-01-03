<p align="center">
  <a href="README.ru.md"><img src="https://img.shields.io/badge/Русский-Readme-blue" alt="Russian" /></a>&nbsp;&nbsp;
  <a href="README.md"><img src="https://img.shields.io/badge/English-Readme-blue" alt="English" /></a>&nbsp;&nbsp;
  <img src="https://visitor-badge.laobi.icu/badge?page_id=White-Tiger-PX.ffmpeg-fragment-cutter" alt="Посетители" />&nbsp;&nbsp;
  <img src="https://img.shields.io/github/stars/White-Tiger-PX/ffmpeg-fragment-cutter?style=social" alt="GitHub звёзды" />
</p>

# ffmpeg-fragment-cutter

Этот инструмент позволяет вырезать фрагменты из видеофайла, начиная с указанного времени и заканчивая другим указанным временем. Также поддерживается выбор аудио и субтитров из исходного видео.

## Требования

- Python 3.x
- FFmpeg (для обработки видео)
- FFprobe (для анализа видео)

## Установка

Установите FFmpeg, следуя инструкциям на официальном сайте.

Убедитесь, что FFmpeg и FFprobe доступны в вашем PATH.

## Использование

1. Запустите скрипт:

    ```bash
    python ffmpeg_fragment_cutter.py
    ```

2. Укажите путь к видеофайлу, который хотите разделить.

3. Укажите начальное время для разделения видео в следующем формате:

    - 75 —> 75 секунд
    - 1:12 —> 1 минута и 12 секунд
    - 12.100 —> 12 секунд и 100 миллисекунд
    - 1:12.50 —> 1 минута, 12 секунд и 50 миллисекунд
    - 6:25.075 —> 6 минут, 25 секунд и 75 миллисекунд
    - 1:01:12.5 —> 1 час, 1 минута, 12 секунд и 500 миллисекунд
    - 10:00:00 —> 10 часов

4. Укажите конечное время (если нужно), или оставьте пустым, чтобы сохранить видео до конца.

5. Программа выведет все доступные аудиотреки и субтитры в видео. Вы можете выбрать, какие из них будут включены в итоговый файл.

    - Для аудио: Введите индексы аудиотреков, которые хотите сохранить (например: 0 1 2) или пропустите.
    - Для субтитров: Введите индексы субтитров, которые хотите сохранить (например: 0 1 2) или пропустите.
    - Программа сохраняет исходный кодек видео, так что качество и формат остаются прежними.

6. Программа создаст новый файл с выбранным временным диапазоном и выбранными потоками.

## Пример

```bash
Enter the path to the video file: "путь/к/видео.mp4"
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
