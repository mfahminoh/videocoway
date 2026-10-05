"""Build one data-driven video: videos/<ID>/{lines.json, spec.json} -> review folder MP4.

    python videos/build_video.py NE01 --tts --render     # everything
    python videos/build_video.py NE01                    # re-resolve spec only (after editing spec.json)
    python videos/build_video.py NE01 --stills 2,8,15    # preview frames -> out/stills/

lines.json : [{"id": "01", "text": "<what TTS says, numbers spelled out>", "cap": "<caption, *highlight*>"}]
spec.json  : {"voice", "style", "slug", "scenes": [{"at", "bg"}], "els": [{"type", "in", "out", ...}]}
Time expressions: "@07" start of line 07, "@07e" its end, "@07%40" 40 % through it, optional "+0.3"/"-0.2";
plain numbers are voiceover seconds. Output: videos/<ID>/index.html + timing.js + spec.js, out/<ID>_final.mp4,
and a copy named <ID>_<slug>.mp4 in out/ (--review to change).
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent.parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
OFF, TAIL = 0.3, 2.4
CLIPDIR = ROOT / "assets" / "clips" / "neon"
CLIPS = ROOT / "assets" / "clips"          # klip Villaem (clip1..clip5) terus di sini

PAGE = """<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8"><title>{id}</title><link rel="stylesheet" href="../lib/scenes.css"></head>
<body><div id="stage"></div>
<script src="timing.js"></script><script src="spec.js"></script>
<script src="../lib/engine.js"></script><script src="../lib/scenes.js"></script>
</body></html>
"""


def run(*cmd):
    print("$", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT)


class Resolver:
    def __init__(self, segs):
        self.s = {g["id"]: (g["a"], g["b"]) for g in segs}
        self.end = segs[-1]["b"]

    def __call__(self, x):
        if x is None or isinstance(x, (int, float)):
            return x
        m = re.fullmatch(r"@(\w+?)(e|%(\d+))?([+-][\d.]+)?", x)
        if not m:
            raise ValueError(f"masa tak sah: {x}")
        a, b = self.s[m.group(1)]
        t = b if m.group(2) == "e" else a + (b - a) * int(m.group(3)) / 100 if m.group(3) else a
        return round(t + float(m.group(4) or 0), 3)


def prep(vid, align=True):
    d = ROOT / "videos" / vid
    lines = json.loads((d / "lines.json").read_text())
    spec = json.loads((d / "spec.json").read_text())
    if align:   # --no-align: guna segments.json sedia ada (dibetulkan manual)
        run(sys.executable, "voiceover/align.py", d / "vo.wav", d / "lines.json", d / "segments.json", 2, 0.1, 0.05)
    segs = json.loads((d / "segments.json").read_text())
    R = Resolver(segs)
    vo_end = segs[-1]["b"]
    dur = round(OFF + vo_end + TAIL, 2)

    # babak
    scenes = []
    for i, s in enumerate(spec["scenes"]):
        t0 = R(s["at"]) if i else 0.0
        scenes.append({"t0": t0, "bg": s["bg"]})
    for i, s in enumerate(scenes):
        s["t1"] = scenes[i + 1]["t0"] if i + 1 < len(scenes) else dur
    # klip: satu jujukan bingkai bagi setiap fail klip (julat gabungan)
    use = {}
    for s in scenes:
        bg = s["bg"]
        if isinstance(bg, dict) and bg.get("clip"):
            lo, hi = use.get(bg["clip"], (99, 0))
            use[bg["clip"]] = (min(lo, bg["c0"], bg["c1"]), max(hi, bg["c0"], bg["c1"]))
            speed = abs(bg["c1"] - bg["c0"]) / max(.01, s["t1"] - s["t0"])
            if not .55 <= speed <= 1.9:
                print(f"  ! {vid}: klip {bg['clip']} kelajuan {speed:.2f}x pada {s['t0']:.1f}s")
        if isinstance(bg, dict) and bg.get("image"):
            bg["image"] = "../../assets/img/" + bg["image"]
    clips = {}
    for name, (lo, hi) in use.items():
        fd = ROOT / "out" / "frames" / f"{vid}_{name}"
        if fd.exists():
            shutil.rmtree(fd)
        fd.mkdir(parents=True)
        subprocess.run([FF, "-v", "error", "-y", "-ss", str(lo), "-t", str(hi - lo + .1), "-i", str(CLIPDIR / f"{name}.mp4" if (CLIPDIR / f"{name}.mp4").exists() else CLIPS / f"{name}.mp4"),
                        "-vf", "fps=30", "-q:v", "3", str(fd / "%04d.jpg")], check=True)
        clips[name] = {"dir": f"../../out/frames/{vid}_{name}/", "n": len(list(fd.glob("*.jpg"))), "start": lo}

    # elemen + SFX
    sfx, freq = [], [700, 820, 940, 1060, 1180, 1300]
    for i, s in enumerate(scenes[1:]):
        sfx.append(["whoosh", round(s["t0"] - .12, 2), .2])
    els = []
    for n, e in enumerate(spec["els"]):
        e = dict(e)
        e["t0"], e["t1"] = R(e.pop("in")), R(e.pop("out", None))
        t_ = e["type"]
        f = freq[n % len(freq)]
        for key in ("items", "options"):
            for k, it in enumerate(e.get(key, [])):
                it["t"] = R(it.get("at", e["t0"] + .15 * k))
                sfx.append(["pop", it["t"], .24, 800 + 90 * k])
        for side in ("left", "right"):
            if t_ == "vs" and side in e:
                e[side]["t"] = R(e[side].get("at", e["t0"]))
                sfx.append(["pop", e[side]["t"], .25, 900])
        for src, dst in (("answerAt", "answerT"), ("badgeAt", "badgeT"), ("strikeAt", "strikeT"), ("toAt", "toT"), ("btnAt", "btnT"), ("zin", "zt0"), ("zout", "zt1")):
            if src in e:
                e[dst] = R(e.pop(src))
        if "keys" in e:
            for k in e["keys"]:
                k["t"] = R(k.pop("at"))
                sfx.append(["shimmer", k["t"], .1] if k["unit"] == "all" else ["pop", k["t"], .25, 1000])
        t = e["type"]
        if t == "stamp":
            sfx.append(["impact", e["t0"], .35])
        elif t == "price":
            sfx += [["impact", e["t0"], .4]]
            if "badgeT" in e: sfx.append(["pop", e["badgeT"], .3, 1100])
            if "strikeT" in e: sfx.append(["whoosh", e["strikeT"], .15])
            if "toT" in e: sfx += [["impact", e["toT"], .45], ["chaching", e["toT"] + .05, .07]]
        elif t == "counter":
            sfx.append(["tick", e["t0"] + e.get("delay", 0) + e.get("dur", 1), .3])
        elif t == "quiz":
            sfx += [["shimmer", e["answerT"], .12], ["pop", e["answerT"], .3, 1300]]
        elif t == "cta":
            bt = e.get("btnT", e["t0"] + .8)
            sfx += [["pop", bt, .32, 800], ["shimmer", bt + .1, .1]]
        elif t == "delivery":
            sfx += [["whoosh", e["t0"] + .4, .15], ["tick", e["t0"] + 2.0, .3]]
        elif t in ("title", "banner", "reason", "pill", "icon", "counter", "card", "photo"):
            sfx.append(["pop", e["t0"], .26 if t != "photo" else .15, f])
        els.append(e)
    sfx.sort(key=lambda x: x[1])
    if not any(s[0] == "impact" for s in sfx):
        sfx.insert(0, ["impact", segs[0]["b"], .3])

    caps = [[g["a"], g["b"], l.get("cap", l["text"])] for g, l in zip(segs, lines)]
    V = {"off": OFF, "dur": dur, "lines": caps, "sfx": sfx}
    (d / "timing.js").write_text("window.V = " + json.dumps(V, ensure_ascii=False, indent=1) + ";\n")
    (d / "spec.js").write_text("window.SPEC = " + json.dumps({"scenes": scenes, "els": els, "clips": clips, **{k: spec[k] for k in ("theme", "brand", "tagline") if k in spec}}, ensure_ascii=False, indent=1) + ";\n")
    (d / "index.html").write_text(PAGE.format(id=vid))
    print(f"{vid}: {dur:.1f}s, {len(scenes)} babak, {len(els)} elemen, klip {list(clips)}")
    return spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vid")
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--stills")
    ap.add_argument("--review", default="out")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-align", action="store_true")
    a = ap.parse_args()
    d = ROOT / "videos" / a.vid
    spec = json.loads((d / "spec.json").read_text())
    if a.tts:
        run(sys.executable, "voiceover/gemini_tts.py", d / "lines.json", d / "vo.wav", "--voice", spec["voice"], "--style", spec["style"])
    prep(a.vid, align=not a.no_align)
    if a.stills:
        run(sys.executable, "render.py", "--src", f"videos/{a.vid}/index.html", "--stills", a.stills)
    if a.render:
        run(sys.executable, "render.py", "--src", f"videos/{a.vid}/index.html", "--out", f"out/{a.vid}_noaudio.mp4", "--jobs", a.jobs)
        run(sys.executable, "videos/build_audio.py", f"videos/{a.vid}", "--mux", f"out/{a.vid}_noaudio.mp4")
        rv = ROOT / a.review
        rv.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "out" / f"{a.vid}_final.mp4", rv / f"{a.vid}_{spec['slug']}.mp4")
        print("siap:", rv / f"{a.vid}_{spec['slug']}.mp4")


if __name__ == "__main__":
    main()
