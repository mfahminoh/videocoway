#!/usr/bin/env bash
# Bina semula V05 dari awal (jalankan dari root repo).
#   pip install playwright imageio-ffmpeg numpy
set -euo pipefail
FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")

# 1. Suara (Gemini TTS) -> videos/V05/vo.wav, kemudian masa setiap baris
#    (vo.wav dalam repo sudah dipotong: take asal membaca arahan gaya dalam 7.4s pertama)
# python3 voiceover/gemini_tts.py videos/V05/lines.json videos/V05/vo.wav --voice Puck --style "..."
python3 voiceover/align.py videos/V05/vo.wav videos/V05/lines.json videos/V05/segments.json

# 2. Bingkai klip sendiri yang dipotong (clip2: panel 40->50->60, clip5: kapasiti 11.4L)
mkdir -p out/frames/v05_clip2 out/frames/v05_clip5
"$FF" -v error -y -ss 0 -t 3.0 -i assets/clips/clip2.mp4 -vf fps=30 -q:v 3 out/frames/v05_clip2/%04d.jpg
"$FF" -v error -y -ss 0.3 -t 4.0 -i assets/clips/clip5.mp4 -vf fps=30 -q:v 3 out/frames/v05_clip5/%04d.jpg

# 3. Animasi -> video senyap, kemudian muzik + SFX + suara
python3 render.py --src videos/V05/index.html --out out/V05_noaudio.mp4 --jobs 4
python3 videos/build_audio.py videos/V05 --mux out/V05_noaudio.mp4      # -> out/V05_final.mp4
