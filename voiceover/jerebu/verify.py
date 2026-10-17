"""Semak setiap klip babak dengan transkripsi Gemini: adakah klip NN.wav betul-betul baca babak NN?

    python voiceover/jerebu/verify.py [--only j3_pm25]

Cetak skor padanan (0–1) antara transkrip dan skrip; skor < 0.6 = potongan salah, betulkan
dengan --align atau edit cuts.json (masa mula babak 2..N) kemudian generate_vo.py --split-only.
"""
import argparse
import difflib
import json
import pathlib
import re
import time

from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
NUM = {"0": "kosong", "1": "satu", "2": "dua", "3": "tiga", "4": "empat", "5": "lima", "6": "enam", "7": "tujuh",
       "8": "lapan", "9": "sembilan"}


def norm(t):
    t = re.sub(r"[^\w\s]", " ", t.lower())
    t = re.sub(r"\d", lambda m: " " + NUM[m.group()] + " ", t)   # kasar: digit -> perkataan
    return t.split()


MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3-flash-preview"]


def transcribe_all(client, paths):
    """Satu permintaan untuk semua klip satu video (kuota kecil); tukar model bila kena had kadar."""
    parts = []
    for k, pth in enumerate(paths):
        parts += [f"KLIP {k + 1}:", types.Part.from_bytes(data=pth.read_bytes(), mime_type="audio/wav")]
    parts.append(f"Transkripsikan setiap klip audio di atas kata demi kata (Bahasa Melayu). "
                 f"Jawab dengan tatasusunan JSON {len(paths)} rentetan, satu bagi setiap klip ikut turutan.")
    for attempt in range(10):
        m = MODELS[attempt % len(MODELS)]
        try:
            r = client.models.generate_content(model=m, contents=parts,
                                               config=types.GenerateContentConfig(response_mime_type="application/json"))
            return json.loads(r.text)
        except Exception as e:
            print(f"  ({m}: {str(e)[:60]})", flush=True); time.sleep(5)
    raise RuntimeError("transkripsi gagal")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only")
    a = ap.parse_args()
    S = json.loads((HERE / "skrip.json").read_text())
    client = genai.Client()
    names = [a.only] if a.only else [k for k in S if not k.startswith("_")]
    bad = 0
    for n in names:
        heard = transcribe_all(client, [HERE / n / f"{i + 1:02d}.wav" for i in range(len(S[n]["scenes"]))])
        for i, (t, h) in enumerate(zip(S[n]["scenes"], heard)):
            a_, b_ = norm(t), norm(h)
            head = difflib.SequenceMatcher(None, a_[:4], b_[:4]).ratio()
            tail = difflib.SequenceMatcher(None, a_[-4:], b_[-4:]).ratio()
            score = min(head, tail); bad += score < .6
            print(f"{n} {i + 1:02d} {score:.2f} {'SALAH' if score < .6 else 'ok   '} | {h}", flush=True)
    print("klip bermasalah:", bad)


if __name__ == "__main__":
    main()
