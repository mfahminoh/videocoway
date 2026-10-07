"""Rancang satu video: babak, sarikata, shot (klip + masa) -> out/_build/V01.json

    python scripts/plan.py V01        # atau all

Peraturan yang dikuatkuasa di sini:
  1  babak yang ada "RM20" di skrin tapi tiada "7 bulan pertama" -> chip "7 bulan pertama" ditambah
  5  shot yang bertindih dengan teks RM20 (babak atau sarikata) hanya guna tetingkap neon=1
  6  hanya klip dalam data/clip_segments.csv (jangan_guna, semak_dulu bukan-Neon, teks tertanam tiada di situ)
"""
import random
import re
import sys

from common import AUDIO, BUILD, DUR, SCENES, days_left, has_7_bulan, has_price, load_segments, load_videos, read_json, write_json

END_CARD = 17.5                      # kad akhir putih 17.5s -> 20s
FALLBACK = ["produk_guna", "susu_bayi", "talking_head", "komersial"]


def shot_grid(style):
    if style == "S7":                # Montaj ASMR: potongan 1 saat
        return [(float(i), float(i + 1)) for i in range(17)] + [(17.0, END_CARD)]
    return [(0.0, 1.5), (1.5, 3.0), (3.0, 5.0), (5.0, 7.0), (7.0, 9.5), (9.5, 12.0),
            (12.0, 14.0), (14.0, 16.0), (16.0, END_CARD)]


def chunk_subs(cues):
    """Ayat -> potongan sarikata pendek (<= 5 perkataan / 28 aksara), masa ikut nisbah aksara."""
    subs = []
    keep = ["7 bulan pertama", "25 Oktober", "Freegift Premium Coway", "Coway Neon", "bulan ni", "WhatsApp sekarang"]
    for c in cues:
        txt = c["text"]
        for k in keep:                         # frasa dikunci: ruang biasa -> NBSP supaya tak dipotong
            txt = txt.replace(k, k.replace(" ", "\u00a0"))
        words = txt.split(" ")
        chunks, cur = [], []
        for w in words:
            glued = cur and re.fullmatch(r"(RM)?\d+[,.]?", cur[-1]) is not None      # jangan pisah "7 | bulan"
            if cur and not glued and (len(cur) >= 5 or len(" ".join(cur + [w])) > 28):
                chunks.append(" ".join(cur)); cur = []
            cur.append(w)
            if re.search(r"[.?!:,]$", w) and len(cur) >= 3:
                chunks.append(" ".join(cur)); cur = []
        if cur:
            if len(cur) == 1 and chunks and len(chunks[-1]) + len(cur[0]) <= 40:
                chunks[-1] += " " + cur[0]            # jangan tinggal satu perkataan seorang
            else:
                chunks.append(" ".join(cur))
        chunks = [x.replace("\u00a0", " ") for x in chunks]
        total = sum(len(x) for x in chunks)
        t = c["start"]
        for x in chunks:
            d = (c["end"] - c["start"]) * len(x) / total
            subs.append({"t0": round(t, 3), "t1": round(t + d, 3), "text": x})
            t += d
    for a, b in zip(subs, subs[1:]):          # isi jeda kecil supaya sarikata tak berkelip
        if 0 < b["t0"] - a["t1"] < 0.35:
            a["t1"] = b["t0"]
    return subs


def overlaps(a0, a1, b0, b1):
    return a0 < b1 - 1e-6 and b0 < a1 - 1e-6


def price_on_screen(t0, t1, scenes, subs, style):
    for s in scenes:
        if overlaps(t0, t1, s["t0"], s["t1"]) and has_price(s["text"]):
            return True
    for s in subs:
        if overlaps(t0, t1, s["t0"], s["t1"]) and has_price(s["text"]):
            return True
    return style == "S6" and overlaps(t0, t1, 3.0, 16.0)      # panel kanan S6 "sekarang / RM20" sepanjang badan


def pick(segs, tag, need_neon, dur, used, rng):
    """Pilih tetingkap klip: tag pilihan dahulu, kemudian tag lain; elak klip yang sudah diguna dalam video ini."""
    order = [tag] + [t for t in FALLBACK if t != tag]
    if not need_neon:
        order += ["model_lain"]
    for pass_ in (0, 1):                       # pass 1 benarkan klip berulang (tetingkap lain)
        for t in order:
            pool = [s for s in segs if s["tag"] == t and s["end"] - s["start"] >= dur - 1e-6
                    and (s["neon"] or not need_neon) and (pass_ or s["id"] not in used)]
            if not need_neon and t == tag:
                # babak tanpa harga: utamakan b-roll bukan-Neon untuk variasi jika ada, jika tidak apa-apa
                pool = sorted(pool, key=lambda s: s["neon"])
            if pool:
                s = rng.choice(pool[:max(1, len(pool))])
                off = rng.uniform(s["start"], s["end"] - dur)
                return s, round(off, 2)
    raise SystemExit(f"tiada klip untuk tag={tag} neon={need_neon} dur={dur}")


def plan(v):
    vo = read_json(AUDIO / f"{v['id']}.json")
    scenes = [{"key": k, "t0": a, "t1": b, "text": v[col]} for k, a, b, col in SCENES]
    subs = chunk_subs(vo["cues"])
    for s in scenes:                           # peraturan 1
        shown = [s["text"]] + [x["text"] for x in subs if overlaps(s["t0"], s["t1"], x["t0"], x["t1"])]
        s["chip7"] = any(has_price(x) for x in shown) and not has_7_bulan(s["text"])
    segs = load_segments()
    rng = random.Random(v["id"])
    used, shots = set(), []
    for t0, t1 in shot_grid(v["style"]):
        tag = v["clip_hook_tag"] if t0 < 3.0 else v["clip_body_tag"]
        need = price_on_screen(t0, t1, scenes, subs, v["style"])
        if v["style"] == "S6" and 3.0 <= t0 < 16.0:
            # skrin dibelah: kiri = "tunggu" (b-roll kelabu), kanan = "sekarang" (mesti Neon)
            left, lo = pick(segs, v["clip_body_tag"], False, t1 - t0, used, rng); used.add(left["id"])
            right, ro = pick(segs, "produk_guna", True, t1 - t0, used, rng); used.add(right["id"])
            shots.append({"t0": t0, "t1": t1, "split": True, "need_neon": True,
                          "left": {"id": left["id"], "file": left["file"], "ss": lo, "neon": left["neon"]},
                          "right": {"id": right["id"], "file": right["file"], "ss": ro, "neon": right["neon"]}})
            continue
        s, off = pick(segs, tag, need, t1 - t0, used, rng)
        used.add(s["id"])
        shots.append({"t0": t0, "t1": t1, "id": s["id"], "file": s["file"], "ss": off, "tag": s["tag"],
                      "neon": s["neon"], "need_neon": need})
    shots.append({"t0": END_CARD, "t1": DUR, "endcard": True, "need_neon": False})
    out = {"id": v["id"], "file": v["file"], "style": v["style"], "style_name": v["style_name"],
           "days_left": days_left(), "scenes": scenes, "subs": subs, "shots": shots, "end_card": END_CARD,
           "vo": vo["cues"]}
    write_json(BUILD / f"{v['id']}.json", out)
    return out


if __name__ == "__main__":
    want = sys.argv[1] if len(sys.argv) > 1 else "V01"
    for v in load_videos():
        if want == "all" or v["id"] in want.split(","):
            p = plan(v)
            print(v["id"], v["style"], " ".join(
                f"{s['t0']:g}:{'END' if s.get('endcard') else ('SPLIT' if s.get('split') else s['id'] + ('*' if s['need_neon'] else ''))}"
                for s in p["shots"]))
