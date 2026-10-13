"""Build the 5 emotional peti ais Coway ads (videos/PA01..PA05) with the "story" player.

    python3 videos/peti_ais.py PA01 --tts --render     # voiceover + align + render + audio
    python3 videos/peti_ais.py PA01                    # re-resolve spec only (after editing spec.json)
    python3 videos/peti_ais.py PA01 --stills 3,20,60   # preview frames -> out/stills/
    python3 videos/peti_ais.py all --render            # every video

videos/<ID>/lines.json : [{"id", "text" (TTS, numbers spelled out), "cap" (caption, *highlight*, "" = none)}]
videos/<ID>/spec.json  : {"slug", "voice", "style_tts", "lift", "shots": [{"at", "img"|"clip"|"color", ...}], "els": [{"type", "in", "out", ...}]}
Times: "@07" start of line 07, "@07e" its end, "@07%40" 40 % through it, optional "+0.3"; numbers = voiceover seconds.
Images: "peti_ais/pa01_a.jpg" or "coway_fridge/551_drawers.jpg" (under assets/img/). Clips: assets/clips/fridge/<name>.mp4.
Output: out/peti_ais/<ID>_<slug>.mp4 (must stay under 90 s).
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "videos"))
from build_video import Resolver  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
OFF, TAIL, MAXDUR = 0.4, 2.6, 90.0
CLIPS = ROOT / "assets" / "clips" / "fridge"
REVIEW = ROOT / "out" / "peti_ais"
IDS = ["PA01", "PA02", "PA03", "PA04", "PA05"]
PAGE = """<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8"><title>{id}</title><link rel="stylesheet" href="../lib/story.css"></head>
<body><div id="stage"></div>
<script src="timing.js"></script><script src="spec.js"></script>
<script src="../lib/engine.js"></script><script src="../lib/story.js"></script>
</body></html>
"""
TIMEKEYS = (("strikeAt", "strikeT"), ("btnAt", "btnT"), ("noteAt", "noteT"), ("note2At", "note2T"))


def run(*cmd):
    print("$", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT)


def prep(vid, align=True):
    d = ROOT / "videos" / vid
    lines = json.loads((d / "lines.json").read_text())
    spec = json.loads((d / "spec.json").read_text())
    if align:
        run(sys.executable, "voiceover/align.py", d / "vo.wav", d / "lines.json", d / "segments.json", 2, 0.1, 0.05)
    segs = json.loads((d / "segments.json").read_text())
    R = Resolver(segs)
    dur = round(OFF + segs[-1]["b"] + TAIL, 2)

    shots = []
    for i, s in enumerate(spec["shots"]):
        s = dict(s)
        s["t0"] = R(s.pop("at")) if i else -OFF
        if s.get("img"):
            s["img"] = "../../assets/img/" + s["img"]
        shots.append(s)
    for i, s in enumerate(shots):
        s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else dur

    # klip -> jujukan JPG (out/frames/<ID>_<klip>/)
    use = {}
    for s in shots:
        if s.get("clip"):
            s.setdefault("c0", 0.0)
            if "c1" not in s:
                s["c1"] = s["c0"] + (s["t1"] - s["t0"])
            lo, hi = use.get(s["clip"], (99, 0))
            use[s["clip"]] = (min(lo, s["c0"], s["c1"]), max(hi, s["c0"], s["c1"]))
            speed = abs(s["c1"] - s["c0"]) / max(.01, s["t1"] - s["t0"])
            if not .3 <= speed <= 1.9:
                print(f"  ! {vid}: klip {s['clip']} kelajuan {speed:.2f}x pada {s['t0']:.1f}s")
    clips = {}
    for name, (lo, hi) in use.items():
        fd = ROOT / "out" / "frames" / f"{vid}_{name}"
        if fd.exists():
            shutil.rmtree(fd)
        fd.mkdir(parents=True)
        subprocess.run([FF, "-v", "error", "-y", "-ss", str(lo), "-t", str(hi - lo + .1), "-i", str(CLIPS / f"{name}.mp4"),
                        "-vf", "fps=30", "-q:v", "3", str(fd / "%04d.jpg")], check=True)
        clips[name] = {"dir": f"../../out/frames/{vid}_{name}/", "n": len(list(fd.glob("*.jpg"))), "start": lo}

    # elemen + SFX (masa voiceover)
    sfx = [["whoosh", round(s["t0"] - .25, 2), .07] for s in shots[1:] if not s.get("cut")]
    els = []
    for e in spec["els"]:
        e = dict(e)
        e["t0"], e["t1"] = R(e.pop("in")), R(e.pop("out", None))
        for a, b in TIMEKEYS:
            if a in e:
                e[b] = R(e.pop(a))
        if "lineAt" in e:
            e["lineAt"] = [R(x) for x in e["lineAt"]]
        for it in e.get("items", []):
            it["t"] = R(it.pop("at", e["t0"]))
        if e.get("src"):
            e["src"] = "../../assets/img/" + e["src"]
        t = e["type"]
        if t == "quote":
            sfx.append(["boom", e["t0"], .22])
        elif t in ("prod", "logo"):
            sfx.append(["shimmer", e["t0"], .07])
        elif t == "feats":
            sfx += [["chime", it["t"], .1, 1568 + 196 * k] for k, it in enumerate(e["items"])]
        elif t == "cal":
            sfx += [["tick", it["t"], .25] for it in e["items"]]
        elif t == "stamp":
            sfx.append(["thud", e["t0"], .35])
        elif t == "big":
            sfx.append(["thud", e["t0"], .22])
            if "strikeT" in e:
                sfx.append(["whoosh", e["strikeT"], .1])
        elif t == "year":
            sfx.append(["tick", e["t0"] + e.get("delay", .3) + e.get("dur", 2.2), .25])
        elif t == "price":
            sfx += [["shimmer", e["t0"], .08], ["chime", e["t0"] + .15, .12, 2093]]
        elif t == "cta":
            sfx += [["chime", e.get("btnT", e["t0"] + .5), .12, 1760], ["chime", e.get("btnT", e["t0"] + .5) + .12, .1, 2349]]
        elif t in ("bubble", "photo"):
            sfx.append(["pop", e["t0"], .12, 900])
        els.append(e)
    sfx.sort(key=lambda x: x[1])

    caps = [[g["a"], g["b"], l.get("cap", l["text"])] for g, l in zip(segs, lines)]
    lift = R(spec["lift"])
    V = {"off": OFF, "dur": dur, "lines": caps, "sfx": sfx, "mood": "emotional", "lift": lift, "bpm": spec.get("bpm", 70)}
    (d / "timing.js").write_text("window.V = " + json.dumps(V, ensure_ascii=False, indent=1) + ";\n")
    SP = {"shots": shots, "els": els, "clips": clips, "flashes": [R(x) for x in spec.get("flashes", [])]}
    (d / "spec.js").write_text("window.SPEC = " + json.dumps(SP, ensure_ascii=False, indent=1) + ";\n")
    (d / "index.html").write_text(PAGE.format(id=vid))
    print(f"{vid}: {dur:.1f}s, {len(shots)} syot, {len(els)} elemen, klip {list(clips)}")
    if dur > MAXDUR:
        raise SystemExit(f"{vid}: {dur:.1f}s melebihi {MAXDUR:.0f}s")
    return spec, dur


def build(vid, a):
    d = ROOT / "videos" / vid
    spec = json.loads((d / "spec.json").read_text())
    if a.tts:
        run(sys.executable, "voiceover/gemini_tts.py", d / "lines.json", d / "vo.wav", "--voice", spec["voice"], "--style", spec["style_tts"])
    prep(vid, align=not a.no_align)
    if a.stills:
        run(sys.executable, "render.py", "--src", f"videos/{vid}/index.html", "--stills", a.stills)
    if a.render:
        run(sys.executable, "render.py", "--src", f"videos/{vid}/index.html", "--out", f"out/{vid}_noaudio.mp4", "--jobs", a.jobs)
        run(sys.executable, "videos/build_audio.py", f"videos/{vid}", "--mux", f"out/{vid}_noaudio.mp4")
        REVIEW.mkdir(parents=True, exist_ok=True)
        dst = REVIEW / f"{vid}_{spec['slug']}.mp4"
        # encode akhir: saiz munasabah untuk Meta/WhatsApp (grain filem mahal untuk encoder)
        subprocess.run([FF, "-y", "-v", "error", "-i", str(ROOT / "out" / f"{vid}_final.mp4"), "-c:v", "libx264", "-preset", "slow", "-crf", "22",
                        "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(dst)], check=True)
        (ROOT / "out" / f"{vid}_noaudio.mp4").unlink()
        print("siap:", dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vid", help="PA01..PA05 atau 'all'")
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--stills")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-align", action="store_true")
    a = ap.parse_args()
    for vid in IDS if a.vid == "all" else [a.vid]:
        build(vid, a)


if __name__ == "__main__":
    main()
