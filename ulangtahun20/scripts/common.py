"""Fungsi kongsi: laluan, data video/klip, placeholder, nombor -> perkataan (untuk TTS), semakan peraturan."""
import csv
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, SRC, OUT, AUDIO = ROOT / "data", ROOT / "sources", ROOT / "out", ROOT / "audio"
BUILD = OUT / "_build"
W, H, FPS, DUR = 1080, 1920, 30, 20.0
PROMO_END = dt.date(2026, 10, 25)
CHROMIUM = next((str(p) for p in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if p.exists()), None)

# Babak tetap (CLAUDE.md): hook, tawaran, hadiah, urgency, CTA
SCENES = [("hook", 0.0, 3.0, "text_0_3s"), ("offer", 3.0, 7.0, "text_3_7s"), ("gift", 7.0, 12.0, "text_7_12s"),
          ("urgency", 12.0, 16.0, "text_12_16s"), ("cta", 16.0, 20.0, "text_16_20s")]


def render_date():
    return dt.date.today()


def days_left(today=None):
    return (PROMO_END - (today or render_date())).days


def placeholders(today=None):
    """Nilai placeholder yang diluluskan pengguna: [x] = 25 Okt tolak tarikh render, [5] = 5."""
    return {"[x]": str(days_left(today)), "[5]": "5"}


def fill(text, today=None):
    for k, v in placeholders(today).items():
        text = text.replace(k, v)
    return text


def load_videos(today=None):
    rows = list(csv.DictReader(open(DATA / "videos.csv", encoding="utf-8")))
    for r in rows:
        for k in [s[3] for s in SCENES] + ["voiceover"]:
            r[k] = fill(r[k], today)
    return rows


def load_segments():
    """Tetingkap klip yang dibenarkan (portrait sahaja, tiada teks tertanam). neon=1 boleh guna di shot RM20."""
    probe = {r["id"]: r for r in csv.DictReader(open(OUT / "scan" / "probe.csv", encoding="utf-8"))}
    segs = []
    for r in csv.DictReader(open(DATA / "clip_segments.csv", encoding="utf-8")):
        p = probe[r["id"]]
        segs.append(dict(id=r["id"], tag=r["tag"], start=float(r["start"]), end=float(r["end"]),
                         neon=r["neon"] == "1", file=p["file"], w=int(p["w"]), h=int(p["h"])))
    return segs


# ---------- nombor -> perkataan Bahasa Melayu (untuk TTS sahaja; sarikata kekal angka) ----------
_ONES = ["kosong", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "lapan", "sembilan"]


def num_ms(n):
    n = int(n)
    if n < 10:
        return _ONES[n]
    if n == 10:
        return "sepuluh"
    if n == 11:
        return "sebelas"
    if n < 20:
        return _ONES[n - 10] + " belas"
    if n < 100:
        t, o = divmod(n, 10)
        return _ONES[t] + " puluh" + ("" if o == 0 else " " + _ONES[o])
    if n < 1000:
        h, r = divmod(n, 100)
        head = "seratus" if h == 1 else _ONES[h] + " ratus"
        return head + ("" if r == 0 else " " + num_ms(r))
    th, r = divmod(n, 1000)
    head = "seribu" if th == 1 else num_ms(th) + " ribu"
    return head + ("" if r == 0 else " " + num_ms(r))


def speakable(text):
    """Teks VO -> teks untuk TTS: RM20 -> dua puluh ringgit, ke-20 -> ke-dua puluh, 70 sen, dsb."""
    t = text
    t = re.sub(r"RM\s?(\d+)", lambda m: num_ms(m.group(1)) + " ringgit", t)
    t = re.sub(r"ke-(\d+)", lambda m: "ke-" + num_ms(m.group(1)), t)
    t = re.sub(r"(\d+)\s*×", lambda m: num_ms(m.group(1)) + " kali", t)
    t = re.sub(r"\d+", lambda m: num_ms(m.group(0)), t)
    t = t.replace("Freegift", "free gift").replace("÷", "bahagi")
    return t


# ---------- semakan peraturan wajib (teks yang muncul di skrin) ----------
BANNED = re.compile(r"\b(halal|jakim|wqa)\b", re.I)
REGULAR_PRICE = re.compile(r"harga (biasa|asal|normal)|lepas promo.*RM\d+|RM(?!20\b|140\b)\d+", re.I)


def has_price(text):
    return bool(re.search(r"RM\s?20\b", text))


def has_7_bulan(text):
    return "7 bulan pertama" in text.lower() or "7 bulan" in text.lower()


def check_text_rules(texts):
    """texts: senarai teks di skrin. Pulangkan senarai pelanggaran (kosong = lulus) untuk peraturan 2 dan 4."""
    bad = []
    for t in texts:
        if BANNED.search(t):
            bad.append(f"peraturan 4: '{t}'")
        if REGULAR_PRICE.search(t):
            bad.append(f"peraturan 2 (harga lain): '{t}'")
        if "25 oktober" not in t.lower() and re.search(r"\b\d{1,2} (okt|oktober|nov|november)\b", t, re.I):
            bad.append(f"peraturan 2 (tarikh lain): '{t}'")
    return bad


def read_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def write_json(p, obj):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
