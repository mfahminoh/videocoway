#!/usr/bin/env bash
# Bina semula E04 "3 sebab ramai pasang Coway Neon" (jalankan dari root repo).
set -euo pipefail
FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")

# 1. Suara: Gemini TTS (Orus). vo.wav dalam repo = take gemini-3.1-flash-tts-preview (tak baca arahan, tak dipotong)
# python3 voiceover/gemini_tts.py videos/E04/lines.json videos/E04/vo.wav --voice Orus --style "Say in Malaysian Malay, ..."

# 2. Bingkai klip Neon (assets/clips/neon/)
ex() { mkdir -p out/frames/e04_$1; "$FF" -v error -y -ss $3 -t $4 -i assets/clips/neon/$2.mp4 -vf fps=30 -q:v 3 out/frames/e04_$1/%04d.jpg; }
ex n1w presenter 0.0 2.6
ex n1c presenter 6.4 1.6
ex n4w press_pour 0.0 3.0
ex n2b bottles_busy 0.0 2.6
ex n4p press_pour 3.0 3.8
ex n3b bottle_to_baby 7.3 2.7

# 3. Animasi + audio
python3 render.py --src videos/E04/index.html --out out/E04_noaudio.mp4 --jobs 4
python3 videos/build_audio.py videos/E04 --mux out/E04_noaudio.mp4      # -> out/E04_final.mp4
