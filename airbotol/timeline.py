"""Skrip VO "Menyampah tengok air botol" (Coway Neo Plus) + garis masa.

    python airbotol/timeline.py                              # anggaran daripada panjang teks
    python airbotol/timeline.py --clips airbotol/clips   # guna tempoh klip suara sebenar

Menulis:
  airbotol/lines.json   slot setiap baris (untuk generate_vo.py & mix.py)
  airbotol/lines.js     salinan yang sama untuk index.html (window.LINES)
  airbotol/airbotol.srt

Tempoh setiap baris dianggar daripada panjang teks (CPS aksara/saat + jeda tanda baca).
index.html dan audio.py guna fungsi anggaran yang sama (at(i, 'perkataan')) untuk
meletakkan animasi & SFX tepat pada perkataan yang disebut.
"""
import argparse
import json
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

CPS = 14.5          # aksara sesaat (anggaran awal; tempoh sebenar diambil daripada klip)
P_STOP = 0.35       # jeda selepas . ? ! …
P_COMMA = 0.12      # jeda selepas ,
GAP = 0.35          # senyap antara baris
START = 0.3
HOLD = 2.2          # tahan penutup selepas baris terakhir

# (teks VO, teks sarikata jika berbeza, jeda tambahan sebelum baris)
SCRIPT = [
    # ---------- HOOK ----------
    ("Saya dah sampai menyampah tengok air botol.", None, 0),
    ("Ni ayat customer saya minggu lepas.", None, .2),
    # ---------- BODY ----------
    ("Dia dah kahwin dekat tiga tahun. Awal kahwin, dia rasa beli air botol paling senang.", None, .3),
    ("Tapi lama-lama, hidup dia macam berkisar dekat air botol je.", None, 0),
    ("Tiap-tiap minggu, kerja dia angkut air kotak.", None, 0),
    ("Berdua je pun, seminggu habis dua kotak. Empat puluh lapan botol!",
     "Berdua je pun, seminggu habis dua kotak. 48 botol!", 0),
    ("Bila dah ada anak, naik jadi tiga kotak.", None, 0),
    ("Stok habis, kena pergi stock hunting. Cari kedai yang murah. Kadang-kadang, harga naik.", None, 0),
    ("Nak tukar brand pun tak boleh. Sebab brand lain tak sedap.", None, 0),
    ("Kotak pula bersusun tepi dapur. Makan space, tak cantik, nak sorok pun tak boleh.", None, 0),
    ("Nak air panas? Masih kena jerang air, atau guna boiler.", None, 0),
    # ---------- TURNING POINT ----------
    ("Sampailah dia balik kampung. Tengok mak dia dah pasang Coway.", None, .4),
    # "Kowei" = ejaan sebutan untuk suara AI (tanpa ni, "Coway" terbaca "CCTV"/"Coenzyme"); sarikata tetap "Coway"
    ("Eh, mak pasang Kowei? Mak dia jawab, sonang kojo!", "\"Eh, mak pasang Coway?\" Mak dia jawab, \"Sonang kojo!\" (senang kerja)", 0),
    ("Dia rasa air tu sedap, kena dengan tekak. Air sejuk pun ada, tak payah simpan dalam peti ais.", None, 0),
    ("Balik rumah sendiri, tengok balik kotak air tepi dapur… makin tak best.", None, 0),
    ("Dua tiga bulan lepas tu, dia tak tahan dah. Aku nak pasang penapis air jugak!", None, 0),
    # ---------- SOLUTION ----------
    ("Minggu lepas, saya pasangkan Kowei Neo Plus untuk dia.", "Minggu lepas, saya pasangkan Coway Neo Plus untuk dia.", .4),
    ("Air panas, air sejuk, suhu bilik. Semua dah ada. Sesuai untuk keluarga kecil, bawah lima orang.", None, 0),
    ("Sebulan lima puluh sembilan ringgit je. Tapi tujuh bulan pertama, cuma dua puluh ringgit!",
     "Sebulan RM59 je. Tapi 7 bulan pertama, cuma RM20!", 0),
    ("Kata dia, berbaloi-baloi.", None, 0),
    # ---------- CTA ----------
    ("Kalau awak pun dah menyampah angkut air kotak… WhatsApp saya sekarang.", None, .3),
]


def est(text):
    """Anggaran tempoh bercakap (saat) untuk teks."""
    stops = len(re.findall(r"[.?!…](?=\s)", text))
    commas = text.count(",")
    return len(text) / CPS + stops * P_STOP + commas * P_COMMA


def clip_duration(clips, i):
    """Tempoh klip suara <clips>/<id>.wav|.mp3, atau None jika tiada."""
    for ext in (".mp3", ".wav"):
        f = clips / f"{i + 1:02d}{ext}"
        if f.exists():
            import imageio_ffmpeg
            err = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(f)], capture_output=True, text=True).stderr
            h, m, s = err.split("Duration: ")[1].split(",")[0].split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return None


def build(clips=None):
    """Slot setiap baris. Jika `clips` diberi, slot = tempoh klip suara sebenar (video ikut suara)."""
    t = START
    rows = []
    for i, (vo, sub, extra) in enumerate(SCRIPT):
        if i:
            t += GAP + extra
        real = clip_duration(clips, i) if clips else None
        d = round((real if real else est(vo)) / 0.05) * 0.05
        rows.append({"id": f"{i + 1:02d}", "start": round(t, 2), "end": round(t + d, 2), "text": vo, **({"sub": sub} if sub else {})})
        t += d
    return rows, round(t + HOLD, 2)


def at(rows, i, word=None, occurrence=1):
    """Masa (saat) perkataan `word` disebut dalam baris i (0-based). Tanpa word -> mula baris."""
    r = rows[i]
    if word is None:
        return r["start"]
    idx = -1
    for _ in range(occurrence):
        idx = r["text"].index(word, idx + 1)
    k = (r["end"] - r["start"]) / est(r["text"])
    return round(r["start"] + est(r["text"][:idx]) * k, 3)


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", help="folder klip suara; slot diambil daripada tempoh sebenar klip")
    a = ap.parse_args()
    rows, dur = build(pathlib.Path(a.clips).resolve() if a.clips else None)
    body = "[\n" + ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n"
    (HERE / "lines.json").write_text(body)
    (HERE / "lines.js").write_text(
        "// Dijana oleh timeline.py — jangan edit terus.\n"
        f"window.LINES = {body.strip()};\nwindow.DURATION = {dur};\n"
        f"window.TIMING = {{CPS: {CPS}, P_STOP: {P_STOP}, P_COMMA: {P_COMMA}}};\n")
    with open(HERE / "airbotol.srt", "w") as f:
        for n, r in enumerate(rows, 1):
            f.write(f"{n}\n{ts(r['start'])} --> {ts(r['end'])}\n{r.get('sub', r['text'])}\n\n")
    for r in rows:
        print(r["id"], f"{r['start']:6.2f}-{r['end']:6.2f}", r["text"][:60])
    print("DURATION", dur)
