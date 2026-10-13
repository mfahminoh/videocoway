#!/usr/bin/env python3
"""Build a review page (grid + Lulus/Perlu ubah + feedback) for a batch of videos.

    python3 .claude/skills/video-review/scripts/build_review.py out/tilam/s0[2-9]_*.mp4 \
        --title "Review Video BEREX Elite" --eyebrow "Coway BEREX Elite" --out <scratchpad>/review-elite

Writes <out>/index.html and <out>/v/<id>.mp4 (720p, small enough to publish with the page),
then prints the `files` map to pass to the Artifact tool. Video titles come from the spec
JSON (tilam/b/<id>.json "title") when one exists, else from the file name.
"""
import argparse, glob, html, json, pathlib, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
FF = shutil.which("ffmpeg") or sys.exit("ffmpeg tidak dijumpai")
FP = shutil.which("ffprobe") or sys.exit("ffprobe tidak dijumpai")


def duration(p):
    out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout.strip()
    return round(float(out or 0))


def title_for(p, spec_dirs):
    vid = p.stem.split("_")[0]
    for d in spec_dirs:
        s = REPO / d / f"{vid}.json"
        if s.exists():
            t = json.loads(s.read_text()).get("title", "")
            return re.sub(r"^\S+\s+[—-]\s+", "", t) or t   # "S02 — Tajuk" -> "Tajuk"
    rest = p.stem.split("_", 1)[1] if "_" in p.stem else p.stem
    return rest.replace("-", " ").capitalize()


def compress(src, dst):
    subprocess.run([FF, "-v", "error", "-y", "-i", str(src), "-vf", "scale='min(720,iw)':-2", "-c:v", "libx264",
                    "-crf", "27", "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
                    str(dst)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+", help="fail atau glob .mp4")
    ap.add_argument("--out", required=True, help="folder output (guna scratchpad)")
    ap.add_argument("--title", default="Review Video", help="<title> halaman: nama 2–4 perkataan")
    ap.add_argument("--h1", help="tajuk besar (lalai = --title)")
    ap.add_argument("--eyebrow", default="Review video")
    ap.add_argument("--footer", default="Video dipaparkan 720p untuk review. Fail penuh ada dalam repo.")
    ap.add_argument("--spec-dir", action="append", default=["tilam/b"], help="folder spec JSON untuk tajuk video")
    a = ap.parse_args()

    files = sorted({pathlib.Path(f) for g in a.videos for f in (glob.glob(g) or [g])})
    files = [f for f in files if f.suffix.lower() == ".mp4" and f.exists()]
    if not files:
        sys.exit("tiada fail .mp4 dijumpai")
    out = pathlib.Path(a.out); (out / "v").mkdir(parents=True, exist_ok=True)

    vids = []
    for f in files:
        vid = re.sub(r"[^A-Za-z0-9_-]", "-", f.stem.split("_")[0])
        vids.append(dict(id=vid, file=f"{vid}.mp4", title=title_for(f, a.spec_dir), src=f))
    if len({v["id"] for v in vids}) != len(vids):   # prefix bertindih: guna nama penuh
        for v in vids:
            v["id"] = re.sub(r"[^A-Za-z0-9_-]", "-", v["src"].stem)[:120]; v["file"] = v["id"] + ".mp4"

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda v: compress(v["src"], out / "v" / v["file"]), vids))
    for v in vids:
        d = duration(v["src"])
        v["tag"] = f"{v['id'].upper()} · {d}s"
        v["path"] = str(v.pop("src"))

    page = (HERE.parent / "assets/template.html").read_text()
    js = json.dumps([{k: v[k] for k in ("id", "file", "title", "tag")} for v in vids], ensure_ascii=False)
    for k, val in {"{{TITLE}}": html.escape(a.title), "{{H1}}": html.escape(a.h1 or a.title),
                   "{{EYEBROW}}": html.escape(a.eyebrow), "{{FOOTER}}": html.escape(a.footer),
                   "{{COUNT}}": str(len(vids)), "{{VIDEOS_JSON}}": js.replace("</", "<\\/")}.items():
        page = page.replace(k, val)
    (out / "index.html").write_text(page)
    (out / "manifest.json").write_text(json.dumps(vids, ensure_ascii=False, indent=1))

    size = sum(p.stat().st_size for p in (out / "v").iterdir()) / 1e6
    print(f"halaman: {out / 'index.html'}  ({len(vids)} video, {size:.1f} MB)")
    print("files =", json.dumps({f"v/{v['file']}": f"v/{v['file']}" for v in vids}))
    if size > 60:
        print("AMARAN: lebih 60 MB, pecahkan kepada beberapa halaman (had 64 MB satu publish)")


if __name__ == "__main__":
    main()
