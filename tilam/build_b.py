"""Siri video tilam B, C, D, L (Prime Lite) (spec dalam tilam/b/<vid>.json) -> out/tilam/<vid>_<slug>.mp4

    python tilam/build_b.py b1                 # VO (Gemini, sekali) + render + audio
    python tilam/build_b.py b1 --stills 2,6,12 # pratonton PNG -> out/stills/
    python tilam/build_b.py all
    python tilam/build_b.py l01 l02 l03 l04 --rotate          # 1 video 1 gaya, gaya digilir
    python tilam/build_b.py l05 --style berita                 # gaya tertentu
    python tilam/build_b.py l01 l02 --rotate --offset 3        # mula gilir dari gaya ke-4
Gaya: kinetic berita whiteboard sinematik majalah chat clean coway  -> out/tilam/gaya/<vid>_<gaya>.mp4
"""
import argparse, json, pathlib, subprocess, sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R)); sys.path.insert(0, str(R / "tilam"))
import render  # noqa: E402
import lib_audio, lib_vo  # noqa: E402

FF = lib_vo.FF
MAIN = "assets/tilam/prime2/video/coway_prime2_seriess_mattress_video.mp4"
ROTATION = ["kinetic", "berita", "whiteboard", "sinematik", "majalah", "chat", "clean", "coway"]
STYLE_MOOD = {"kinetic": "drive", "berita": "drive", "sinematik": "warm", "majalah": "warm"}
SPECS, VODIR, OUT, FR = R / "tilam/b", R / "tilam/b/vo", R / "out/tilam", R / "out/tilam/_frames"


def clips_needed(spec, style=None):
    need = set()
    if style and style != "coway":  # gaya lain boleh guna klip mana-mana sebagai bg atau kad
        for ln in spec["lines"]:
            sc = ln.get("scene", {})
            for k in ("bg", "media"):
                if sc.get(k, {}).get("clip"): need |= {(sc[k]["clip"], "bg"), (sc[k]["clip"], "card")}
        return need
    for ln in spec["lines"]:
        sc = ln.get("scene", {})
        if sc.get("bg", {}).get("clip"): need.add((sc["bg"]["clip"], "bg"))
        if sc.get("media", {}).get("clip"): need.add((sc["media"]["clip"], "card"))
    return need


def extract(vid, spec, style=None):
    out = {}
    for name, var in sorted(clips_needed(spec, style)):
        c = spec["clips"][name]; src = R / c.get("src", MAIN)
        d = FR / vid / f"{name}_{var}"
        if not d.exists() or not any(d.iterdir()):
            d.mkdir(parents=True, exist_ok=True)
            cx = c.get("cx", .5)
            vf = (f"crop=ih*9/16:ih:(iw-ih*9/16)*{cx}:0,scale=1080:1920,fps=30" if var == "bg"
                  else "scale=1080:-2,fps=30")
            subprocess.run([FF, "-v", "error", "-y", "-ss", str(c["from"]), "-t", str(c["to"] - c["from"]), "-i", str(src),
                            "-vf", vf, "-q:v", "3", str(d / "%04d.jpg")], check=True)
        out[f"{name}_{var}"] = {"dir": str(d.relative_to(R)), "n": len(list(d.glob("*.jpg")))}
    return out


def data_js(vid, spec, tm, clips):
    d = dict(spec, timing=tm, clips=clips)
    p = R / "src/tilam/b/data" / f"{vid}.js"; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("window.SPEC = " + json.dumps(d, ensure_ascii=False) + ";\n")


def page_info(src):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, page = render.open_page(p, src)
        info = page.evaluate("({d: window.DURATION, sfx: window.SFX})")
        b.close()
    return info


def run(vid, stills=None, jobs=4, style=None):
    spec = json.loads((SPECS / f"{vid}.json").read_text())
    print(f"== {vid}: {spec['title']}")
    tm = lib_vo.build_vo(vid, spec["lines"], VODIR)
    clips = extract(vid, spec, style)
    data_js(vid, spec, tm, clips)
    styled = style and style != "coway"
    src = f"tilam/b/styled.html?v={vid}&style={style}" if styled else f"tilam/b/player.html?v={vid}"
    tag = f"{vid}_{style}" if style else vid
    if stills:
        render.stills(src, [float(x) for x in stills.split(",")], prefix=f"{tag}_"); return
    out = OUT / "gaya" if style else OUT
    out.mkdir(parents=True, exist_ok=True)
    info = page_info(src)
    silent, wav = out / f"_{tag}_noaudio.mp4", out / f"_{tag}.wav"
    final = out / (f"{vid}_{style}.mp4" if style else f"{vid}_{spec['slug']}.mp4")
    render.video(src, silent, jobs)
    lib_audio.build(info["d"], info["sfx"], VODIR / f"{vid}_vo.wav", wav, STYLE_MOOD.get(style) or spec.get("mood", "calm"))
    subprocess.run([FF, "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    silent.unlink(); wav.unlink(); print("siap:", final)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("vid", nargs="+"); ap.add_argument("--stills"); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--style", choices=ROTATION); ap.add_argument("--rotate", action="store_true"); ap.add_argument("--offset", type=int, default=0)
    a = ap.parse_args()
    vids = sorted(p.stem for p in SPECS.glob("[bcdl][0-9]*.json")) if a.vid == ["all"] else a.vid
    for i, v in enumerate(vids):
        st = ROTATION[(i + a.offset) % len(ROTATION)] if a.rotate else a.style
        if a.rotate: print(f"[{i + 1}/{len(vids)}] {v} -> {st}")
        run(v, a.stills, a.jobs, st)
