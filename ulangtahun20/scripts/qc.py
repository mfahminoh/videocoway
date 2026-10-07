"""QC akhir -> out/qc.csv: tempoh 20.0s, 1080x1920, peraturan wajib 1-5 (dari pelan + fail mp4).

    python scripts/qc.py V01-V15
"""
import csv
import json
import subprocess
import sys

from common import BUILD, OUT, check_text_rules, has_7_bulan, has_price, load_segments, read_json
from render import pick


def probe(path):
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,nb_frames",
                                   "-of", "json", str(path)], capture_output=True, text=True).stdout)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = any(s["codec_type"] == "audio" for s in p["streams"])
    return float(p["format"]["duration"]), v["width"], v["height"], int(v.get("nb_frames", 0)), a


def overlaps(a0, a1, b0, b1):
    return a0 < b1 - 1e-6 and b0 < a1 - 1e-6


def check(v):
    p = read_json(BUILD / f"{v['id']}.json")
    mp4 = OUT / v["file"]
    notes = []
    dur, w, h, nf, has_a = probe(mp4) if mp4.exists() else (0, 0, 0, 0, False)
    ok_fmt = abs(dur - 20.0) < 0.02 and (w, h) == (1080, 1920) and nf == 600 and has_a
    if not ok_fmt:
        notes.append(f"format {dur:.3f}s {w}x{h} {nf}f audio={has_a}")

    # Peraturan 1: RM20 di skrin -> "7 bulan pertama" dalam babak sama (teks babak atau chip)
    r1 = True
    for sc in p["scenes"]:
        shown = [sc["text"]] + [s["text"] for s in p["subs"] if overlaps(sc["t0"], sc["t1"], s["t0"], s["t1"])]
        if p["style"] == "S6" and 3.0 <= sc["t0"] < 16.0:
            shown.append("RM20 7 bulan pertama")          # panel kanan S6 sentiasa ada kedua-duanya
        if any(has_price(x) for x in shown) and not (has_7_bulan(sc["text"]) or sc.get("chip7")
                                                     or (p["style"] == "S6" and 3.0 <= sc["t0"] < 16.0)):
            r1 = False; notes.append(f"P1 babak {sc['key']}")
    # Peraturan 2 & 4: tarikh/harga lain, Halal/JAKIM/WQA
    texts = [sc["text"] for sc in p["scenes"]] + [s["text"] for s in p["subs"]]
    bad = check_text_rules(texts)
    r2 = not any(b.startswith("peraturan 2") for b in bad)
    r4 = not any(b.startswith("peraturan 4") for b in bad)
    notes += bad
    # Peraturan 3: CTA hanya "WhatsApp sekarang"
    cta = next(sc for sc in p["scenes"] if sc["key"] == "cta")["text"].strip()
    r3 = cta == "WhatsApp sekarang"
    if not r3:
        notes.append(f"P3 CTA '{cta}'")
    # Peraturan 5: shot dengan RM20 di skrin mesti klip Neon; model_lain hanya babak tanpa harga
    segs = load_segments()
    r5 = True
    for s in p["shots"]:
        if s.get("endcard"):
            continue
        clips = [s["right"]] if s.get("split") else [s]
        if s["need_neon"] and not all(c["neon"] for c in clips):
            r5 = False; notes.append(f"P5 shot {s['t0']}s bukan Neon")
        if not s.get("split") and s.get("tag") == "model_lain" and s["need_neon"]:
            r5 = False; notes.append(f"P5 model_lain di shot harga {s['t0']}s")
    used = sorted({c["id"] for s in p["shots"] if not s.get("endcard") for c in ([s["left"], s["right"]] if s.get("split") else [s])})
    return {"id": v["id"], "file": v["file"], "style": v["style"], "durasi_s": f"{dur:.3f}", "resolusi": f"{w}x{h}", "frame": nf,
            "format_ok": ok_fmt, "p1_7bulan": r1, "p2_tarikh_harga": r2, "p3_cta": r3, "p4_halal_jakim_wqa": r4, "p5_neon": r5,
            "lulus": all([ok_fmt, r1, r2, r3, r4, r5]), "klip": " ".join(used), "nota": "; ".join(notes)}


if __name__ == "__main__":
    rows = [check(v) for v in pick(sys.argv[1] if len(sys.argv) > 1 else "V01-V30") if (BUILD / f"{v['id']}.json").exists()]
    path = OUT / "qc.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
    for r in rows:
        print(r["id"], "LULUS" if r["lulus"] else "GAGAL", r["durasi_s"], r["resolusi"], r["nota"])
    print("ditulis", path)
