"""Semak video Coway sebelum TTS / render, dan selepas render.

    python3 .claude/skills/coway-video/scripts/semak.py NE01 NE02      # semak lines.json + spec.json (+ VO / MP4 jika ada)
    python3 .claude/skills/coway-video/scripts/semak.py --max 60 PA01  # had saat lain (lalai 45; pemain story 90)

RALAT = mesti dibaiki sebelum teruskan. AMARAN = semak dengan mata, mungkin sengaja.
Keluar dengan kod 1 jika ada RALAT.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
VIDEOS = ROOT / "videos"
OFF, TAIL = 0.3, 2.4                     # sama seperti videos/build_video.py
TTS_MAX_CHARS = 1150                     # skrip lebih panjang kerap gagal (502) dalam satu permintaan
PLAYERS = {"scenes", "hype", "mg"}      # videos/build_video.py; "story" = spec dengan "shots" (videos/peti_ais.py)
MG_STYLES = ROOT / "reference" / "mg-styles-15" / "prompts"   # gaya sah untuk player "mg"
PRICE = re.compile(r"\bRM\s?\d|ringgit|harga|promo|diskaun|rebat|potongan|sebulan", re.I)


def walk(o):
    """Semua rentetan dalam struktur JSON."""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def times(o):
    """Semua ungkapan masa "@07", "@07e", "@07%40+0.3" dalam spec."""
    for s in walk(o):
        m = re.fullmatch(r"@(\w+?)(e|%\d+)?([+-][\d.]+)?", s)
        if m:
            yield m.group(1)


def duration(path):
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = "ffmpeg"
    err = subprocess.run([ff, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None


def check(vid, max_s=None):
    d = VIDEOS / vid
    err, warn = [], []
    if not (d / "lines.json").exists() or not (d / "spec.json").exists():
        return [f"tiada videos/{vid}/lines.json atau spec.json"], []
    lines = json.loads((d / "lines.json").read_text())
    spec = json.loads((d / "spec.json").read_text())
    story = "shots" in spec
    player = "story" if story else spec.get("player", "scenes")
    max_s = max_s or (90 if story else 45)

    # ---- lines.json ----
    ids = [l.get("id") for l in lines]
    if len(set(ids)) != len(ids):
        err.append("id baris berulang dalam lines.json")
    text = " ".join(l.get("text", "") for l in lines)
    coway = [l.get("id") for l in lines if re.search(r"\bcoway\b", l.get("text", ""), re.I)]
    for l in lines:
        t, i = l.get("text", ""), l.get("id")
        if not t.strip():
            err.append(f"baris {i}: text kosong")
        if re.search(r"\d", t):
            warn.append(f"baris {i}: ada angka dalam text TTS ({t[:50]!r}) — tulis dalam perkataan")
        if ("%" in t + l.get("cap", "") or "peratus" in t.lower()) and PRICE.search(t + " " + l.get("cap", "")):
            warn.append(f"baris {i}: peratus dalam baris harga/promo — sebut harga dalam RM sahaja")
        if "cap" not in l:
            warn.append(f"baris {i}: tiada cap (kapsyen akan guna text TTS, termasuk 'Kowei')")
    if coway:
        warn.append(f"'Coway' dalam text TTS baris {', '.join(coway)} — dengar sebutan selepas TTS; jika jadi 'Kawi'/'Cuckoo', tukar text kepada 'Kowei'")
    words = len(text.split())
    if len(text) > TTS_MAX_CHARS:
        warn.append(f"skrip {len(text)} aksara > {TTS_MAX_CHARS} — TTS satu permintaan mungkin gagal; pendekkan")
    if not 60 <= words <= 115:
        warn.append(f"skrip {words} perkataan (sasaran 70–100 untuk 30–45 s)")

    # ---- spec.json ----
    mg = player == "mg"
    page = (d / "index.html").read_text() if mg and (d / "index.html").exists() else ""
    for k in ("slug", "voice", *(("mg", "cues") if mg else ("shots" if story else "scenes", "els"))):
        if k not in spec:
            err.append(f"spec.json tiada kunci '{k}'")
    if "style" not in spec and "style_tts" not in spec:
        err.append("spec.json tiada 'style' atau 'style_tts' (arahan gaya suara TTS)")
    if spec.get("slug") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", spec["slug"]):
        err.append(f"slug '{spec['slug']}' mesti huruf kecil-dan-sengkang")
    if not story and player not in PLAYERS:
        err.append(f"player '{spec.get('player')}' tak dikenali ({', '.join(sorted(PLAYERS))})")
    for ref in sorted(set(times(spec)) - set(ids)):
        err.append(f"spec merujuk @{ref} tapi tiada baris id '{ref}'")
    els = spec.get("els", [])
    if mg:   # halaman ditulis tangan: semak gaya, cue dan CTA dalam index.html
        if not page:
            err.append(f"player mg perlukan videos/{vid}/index.html")
        if spec.get("mg") and not (MG_STYLES / f"{spec['mg']}.md").exists():
            err.append(f"gaya mg '{spec['mg']}' tiada dalam reference/mg-styles-15/prompts/")
        cues = spec.get("cues", {})
        used = {s[1].split("+")[0].split("-")[0] for s in spec.get("sfx", []) if isinstance(s[1], str) and not s[1].startswith("@")}
        used |= set(re.findall(r"\bQ\('(\w+)'\)", page))   # Q('unit' + i) dinamik tak disemak
        for c in sorted(used - set(cues)):
            err.append(f"cue '{c}' digunakan (sfx / Q() dalam index.html) tapi tiada dalam spec.cues")
        if page and "WhatsApp" not in page:
            err.append("tiada butang WhatsApp dalam index.html — setiap video mesti tutup dengan CTA")
    elif not any(e.get("type") == "cta" for e in els):
        err.append("tiada elemen cta (butang WhatsApp) — setiap video mesti tutup dengan CTA")
    if player == "scenes" and spec.get("theme") != "coway":
        warn.append("theme bukan 'coway' — warna rasmi Coway disyorkan (brand-guide.md)")

    allstr = " ".join(walk(spec)) + " " + " ".join(l.get("cap", "") for l in lines) + " " + page
    if re.search(r"RM\s?\d", allstr) and not re.search(r"tertakluk", allstr, re.I):
        err.append("ada harga RM tapi tiada nota 'Tertakluk ...' (letak dalam cta.fine)")
    if "99.9" in allstr and "TÜV" not in allstr and "TUV" not in allstr.upper():
        err.append("dakwaan 99.9% tanpa penafian TÜV SÜD (brand-guide.md §6)")
    if "1800-888-111" in allstr or "Coway Malaysia" in allstr:
        err.append("guna Careline / nama 'Coway Malaysia' — kita ejen, bukan Coway HQ")

    # aset wujud
    for sc in spec.get("scenes", []):
        bg = sc.get("bg")
        if isinstance(bg, dict) and bg.get("image") and not (ROOT / "assets" / "img" / bg["image"]).exists():
            err.append(f"gambar latar tiada: assets/img/{bg['image']}")
        if isinstance(bg, dict) and bg.get("clip"):
            c = bg["clip"]
            if not ((ROOT / "assets/clips/neon" / f"{c}.mp4").exists() or (ROOT / "assets/clips" / f"{c}.mp4").exists()):
                err.append(f"klip tiada: assets/clips[/neon]/{c}.mp4")
    if not story and not mg and spec.get("cap", True) is not False:   # bar kapsyen VO: top 1520–1690 px
        low = [f"{e['type']}@{e.get('in')}" for e in els if isinstance(e.get("top"), (int, float)) and e["top"] > 1380]
        if low:
            warn.append(f"elemen top > 1380 px bertindih dengan kapsyen: {', '.join(low)}")
    for sh in spec.get("shots", []):          # pemain story: img di bawah assets/img/, klip di assets/clips/fridge/
        if sh.get("img") and not (ROOT / "assets" / "img" / sh["img"]).exists():
            err.append(f"gambar shot tiada: assets/img/{sh['img']}")
        if sh.get("clip") and not (ROOT / "assets/clips/fridge" / f"{sh['clip']}.mp4").exists():
            err.append(f"klip shot tiada: assets/clips/fridge/{sh['clip']}.mp4")
    for e in els:
        src = e.get("src")
        if isinstance(src, str) and not src.startswith(("http", "data:")):
            p = ROOT / "assets" / "img" / src if story else (d / src).resolve()
            if not p.exists():
                err.append(f"{e['type']}.src tiada: {src}")

    # ---- selepas VO ----
    seg = d / "segments.json"
    if (d / "vo.wav").exists() and seg.exists():
        segs = json.loads(seg.read_text())
        dur = OFF + segs[-1]["b"] + TAIL
        if [s["id"] for s in segs] != ids:
            err.append("segments.json tak sepadan dengan lines.json — jalankan build_video.py semula (tanpa --no-align)")
        short = [s["id"] for s in segs if s["b"] - s["a"] < 0.35]
        if short:
            warn.append(f"segmen sangat pendek {short} — penjajaran mungkin lari; semak kapsyen vs suara")
        if dur > max_s:
            warn.append(f"panjang dijangka {dur:.1f} s > {max_s} s — pendekkan skrip")
        info = f"VO {dur:.1f} s"
    else:
        info = "belum ada VO"

    # ---- selepas render ----
    if spec.get("slug"):
        outs = sorted(ROOT.glob(f"out/**/{vid}_{spec['slug']}.mp4"))
        for o in outs:
            t = duration(o)
            info += f" · {o.relative_to(ROOT)} {t:.1f} s" if t else f" · {o.relative_to(ROOT)} (tak boleh baca)"
            if t and t > max_s + 1:
                warn.append(f"{o.name} {t:.1f} s > {max_s} s")
    return err, warn, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vids", nargs="+")
    ap.add_argument("--max", type=float, help="had panjang video dalam saat (lalai 45; pemain story 90)")
    a = ap.parse_args()
    bad = 0
    for vid in a.vids:
        r = check(vid, a.max)
        err, warn = r[0], r[1]
        info = r[2] if len(r) > 2 else ""
        print(f"{vid}: {'OK' if not err else 'RALAT'}  {info}")
        for x in err:
            print("   RALAT  ", x)
        for x in warn:
            print("   amaran ", x)
        bad += bool(err)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
