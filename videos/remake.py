"""Remake video TikTok: satu storyboard -> beberapa video, satu suara, gaya berbeza (skill coway-remake).

    python3 videos/remake.py projek/<kod>/storyboard.json            # tulis videos/<ID>/{lines.json, spec.json}
    python3 videos/build_video.py <ID1> --tts                       # suara sekali, pada video pertama
    python3 videos/remake.py projek/<kod>/storyboard.json            # jalankan semula: salin vo.wav ke video lain
    python3 videos/build_video.py <ID> --render --review out/<kod>   # setiap video

storyboard.json (contoh penuh: projek/neon-p1-01/storyboard.json):
  kod, slug, voice, style_tts, fine, ticks[3], button, produk ("neon" -> elemen lineup), produk_img (assets/img/...),
  produk_cut (gambar potong untuk hype, assets/img/...), video: [{"id": "NE14", "gaya": "kinetic"}, ...],
  baris: [{"id": "01", "text", "cap", "jenis", ...medan ikut jenis}]

Jenis baris dan medannya ("|" dalam tajuk = pecah baris):
  hook    tajuk, sorot            produk  tajuk, sorot           suhu  tajuk?
  warna   tajuk, sorot            poin    tajuk, sorot           harga label?, harga, sub, per?, ikon?
  promo   tajuk, pre, harga, sub, atas?   (separuh pertama atas gambar, separuh kedua harga besar)
  desak   tajuk, sorot            cta     tajuk
Semua jenis boleh ada "gambar" (assets/img/..., latar penuh realistik).

Gaya templat: coway (pemain scenes), kinetic, comic, glow, paper, ugc (pemain hype).
Gaya "mg:<nama>" (mg-styles-15, .claude/skills/coway-video/formats/mg-gaya.md) ditulis tangan: skrip ini sediakan
lines.json, salin VO, dan spec.json minimum (hanya jika belum ada; cue sheet ditambah sendiri).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
HERE = ROOT / "videos"
NAVY, CORAL = "#0B2F6B", "#E86E5A"
BLUE, PINK, INK, YEL, GPINK = "#04A4E4", "#ff8fb1", "#2f3337", "#ffd23f", "#ff4f8f"
TEMPLAT = ["coway", "kinetic", "comic", "glow", "paper", "ugc"]
BGS = {"kinetic": ["k-blue", "k-ink", "k-white", "k-sky", "k-pink"], "comic": ["comic-pink", "comic-sky", "comic-blue", "comic-white"],
       "glow": ["glow-wall", "glow-dark"], "paper": ["paper-cream", "paper-blue", "paper-sky", "paper-pink"], "ugc": ["ugc-blue", "ugc-white"]}
LIGHT = {"k-white", "k-sky", "k-pink", "comic-white", "comic-sky", "paper-cream", "paper-sky", "paper-pink", "ugc-white"}
CHAR = {"kinetic": .5, "comic": .55, "glow": .62, "paper": .72, "ugc": .66}     # lebar purata aksara / saiz fon


def pieces(s):
    return [x.strip() for x in (s or "").split("|") if x.strip()]


def fit(txt, base, style):
    return max(56, min(base, int(940 / (CHAR[style] * max(1, len(txt))))))


class Line:
    """Masa satu baris: at (mula), mid(p) (p % ke dalam), out (mula baris seterusnya / None untuk terakhir)."""
    def __init__(self, b, nxt):
        self.b, self.id = b, b["id"]
        self.at, self.out = f"@{self.id}", (f"@{nxt}" if nxt else None)

    def mid(self, p):
        return f"@{self.id}%{p}"

    def __getitem__(self, k):
        return self.b.get(k)


# ------------------------------------------------------------------ gaya hype
def word(style, txt, at, size, accent=False, hit=False, light=False, photo=False):
    w = {"txt": txt, "at": at, "size": fit(txt, size, style)}
    if style == "kinetic":
        if photo:
            w.update(box=True, bg=BLUE if accent else "#111", color="#fff")
        else:
            w["color"] = (BLUE if accent else INK) if light else "#fff"
            if accent and not light:
                w.update(box=True, bg="#111")
    elif style == "comic":
        w["color"] = (BLUE if light else YEL) if accent else "#fff"
    elif style == "glow":
        w.update(g=GPINK if accent else BLUE)
    elif style == "paper":
        if accent:
            w.update(bg=BLUE, color="#fff")
    elif style == "ugc":
        w["color"] = (BLUE if light and not photo else YEL) if accent else ("#fff" if photo or not light else INK)
    if hit:
        w["hit"] = True
    return w


def W(at, out, top, items):
    return {"type": "words", "in": at, "out": out, "top": top, "items": items}


def hype_line(st, L, bg, sb, photo):
    """Elemen satu baris untuk gaya hype. bg = nama latar grafik (untuk warna teks) bila tiada gambar."""
    light = (not photo) and bg in LIGHT
    w = lambda txt, at, size, **k: word(st, txt, at, size, light=light, photo=photo, **k)
    j, els = L["jenis"], []
    tj = pieces(L["tajuk"])
    burst = st in ("comic", "ugc")

    def heading(top, size):
        items = [w(t, L.at if k == 0 else L.mid(30 * k), size) for k, t in enumerate(tj)]
        return W(L.at, L.out, top, items) if items else None

    if j == "hook":
        els.append(heading(top=220, size=130))
        if L["sorot"]:
            if burst:
                els.append({"type": "burst", "in": L.mid(50), "out": L.out, "html": L["sorot"].replace(" ", "<br>"), "top": 1000, "size": 500,
                            "x": 540, "color": "#fff", "textColor": PINK, "fs": 100, "rot": -6, "hit": True})
            else:
                els.append(W(L.mid(55), L.out, 1180, [w(L["sorot"], L.mid(60), 150, accent=True, hit=True)]))
    elif j == "produk":
        els.append(heading(top=170, size=150))
        if not photo:
            els.append({"type": "img", "in": L.mid(10), "out": L.out, "src": sb["_cut"], "w": 430, "top": 380,
                        "anim": "spin" if st == "comic" else "rise", **({"float": True} if st == "comic" else {})})
        if L["sorot"]:
            if burst:
                els.append({"type": "burst", "in": L.mid(55), "out": L.out, "html": L["sorot"].replace(" ", "<br>"), "top": 1000, "size": 400,
                            "x": 800, "color": YEL, "textColor": "#fff", "fs": 96, "rot": 12, "hit": True})
            else:
                els.append(W(L.mid(50), L.out, 1180, [w(L["sorot"], L.mid(60), 170, accent=True, hit=True)]))
    elif j == "suhu":
        if tj:
            els.append(heading(top=200, size=150))
        els.append({"type": "temps", "in": L.at, "out": L.out, "top": 780 if photo else 560,
                    "items": [{"k": "hot", "at": L.at}, {"k": "cold", "at": L.mid(30)}, {"k": "room", "at": L.mid(60)}]})
    elif j in ("warna", "poin"):
        items = [w(t, L.at if k == 0 else L.mid(25 * k), 120) for k, t in enumerate(tj)]
        if L["sorot"] and not (burst and j == "poin"):
            items.append(w(L["sorot"], L.mid(45), 170, accent=True, hit=True))
        els.append(W(L.at, L.out, 200, items))
        if burst and j == "poin" and L["sorot"]:
            els.append({"type": "burst", "in": L.mid(35), "out": L.out, "html": L["sorot"].replace(" ", "<br>"), "top": 1020 if photo else 460,
                        "size": 560, "x": 540, "color": "#fff", "textColor": BLUE, "fs": 84, "rot": -6, "hit": True})
        if j == "warna" and not photo:
            els.append({"type": "img", "in": L.mid(20), "out": L.out, "src": sb["_lineup"], "w": 1000, "top": 760, "anim": "rise"})
    elif j == "harga":
        if L["label"]:
            els.append(W(L.at, L.out, 200, [w(L["label"], L.at, 120)]))
        els.append({"type": "tag", "in": L.mid(30) if L["label"] else L.at, "out": L.out, "top": 1080 if photo else 600,
                    "big": L["harga"], "sub": L["sub"] or "", "hit": True})
    elif j == "promo":
        if photo:     # separuh pertama atas gambar
            items = [w(t, L.at if k == 0 else L.mid(20), 120, accent=k == len(tj) - 1, hit=k == len(tj) - 1) for k, t in enumerate(tj)]
            els.append(W(L.at, L.mid(50), 220, items))
        lightB = sb["_promo_bg"][st] in LIGHT
        wb = lambda txt, at, size, **k: word(st, txt, at, size, light=lightB, **k)
        s0 = 50 if photo else 0
        if st == "comic":
            els.append({"type": "gift", "in": L.mid(s0), "out": L.out, "openAt": L.mid(s0 + 12), "top": 440, "size": 560, "rays": "rgba(4,164,228,.35)"})
            els.append(W(L.mid(s0 + 12), L.out, 1060, [wb(f"{L['pre'] or ''} {L['harga']}".strip(), L.mid(s0 + 15), 140, accent=True, hit=True),
                                                       wb(L["sub"] or "", L.mid(s0 + 28), 80)]))
        else:
            items = ([wb(L["pre"], L.mid(s0), 160)] if L["pre"] else []) + [wb(L["harga"], L.mid(s0 + 8), 400, accent=True, hit=True)]
            if L["sub"]:
                items.append({**wb(L["sub"], L.mid(s0 + 25), 72, accent=True), **({"box": True, "bg": BLUE, "color": "#fff"} if st in ("kinetic", "ugc") else {})})
            els.append(W(L.mid(s0), L.out, 380, items))
        if st == "kinetic":
            els.append({"type": "ticker", "in": L.at, "out": sb["_after_promo"], "top": 1300, "text": f"{L['pre'] or ''} {L['harga']} {L['sub'] or ''}".strip(),
                        "rot": -5, "bg": "#111", "color": "#fff"})
    elif j == "desak":
        if burst:
            els.append({"type": "burst", "in": L.at, "out": L.out, "html": "<br>".join(tj), "top": 300, "size": 660, "x": 540, "color": YEL,
                        "textColor": "#fff", "fs": 150 if len(" ".join(tj)) > 8 else 190, "rot": -6, "hit": True})
            if L["sorot"]:
                els.append(W(L.mid(50), L.out, 1050, [w(L["sorot"], L.mid(55), 130)]))
        else:
            items = [w(t, L.at if k == 0 else L.mid(20), 170 if k == 0 else 300, accent=k == len(tj) - 1, hit=k == len(tj) - 1) for k, t in enumerate(tj)]
            if L["sorot"]:
                items.append({**w(L["sorot"], L.mid(55), 120), **({"box": True, "bg": "#111", "color": "#fff"} if st == "kinetic" else {})})
            els.append(W(L.at, L.out, 380, items))
    elif j == "cta":
        els.append(W(L.at, None, 330, [w(t, L.at if k == 0 else L.mid(30), 170) for k, t in enumerate(tj)]))
        els.append({"type": "cta", "in": L.at, "top": 900, "button": sb.get("button", "WhatsApp saya"), "btnAt": L.mid(40), "fine": sb["fine"],
                    **({"fineColor": "#333"} if light else {})})
    return [e for e in els if e]


def hype_video(st, sb, lines):
    scenes, els, cyc = [], [], BGS[st]
    for i, L in enumerate(lines):
        g, bg = L["gambar"], cyc[i % len(cyc)]
        at = 0 if i == 0 else L.at
        if L["jenis"] == "promo":
            bg = sb["_promo_bg"][st]
            if g:
                scenes += [(at, {"image": g, "color": cyc[0], "shade": True}), (L.mid(50), bg)]
            else:
                scenes.append((at, bg))
        elif L["jenis"] == "cta":
            bg = {"kinetic": "k-blue", "comic": "comic-blue", "glow": "glow-dark", "paper": "paper-blue", "ugc": "ugc-blue"}[st]
            scenes.append((at, bg))
        else:
            scenes.append((at, {"image": g, "color": cyc[0], "shade": True} if g else bg))
        els += hype_line(st, L, bg, sb, bool(g) and L["jenis"] not in ("cta",))
    head = {"voice": sb["voice"], "style_tts": sb["style_tts"], "style": st, "player": "hype", "bpm": 128, "brand": "coway", "cap": True}
    return head, scenes, els


# ------------------------------------------------------------------ gaya coway (pemain scenes)
def em_last(s):
    w = s.split()
    return " ".join(w[:-1] + [f"<em>{w[-1]}</em>"]) if len(w) > 1 else f"<em>{s}</em>"


def coway_video(sb, lines):
    scenes, els = [], []
    title = lambda at, out, html, top=240, size=110, dark=False, **kw: {"type": "title", "in": at, "out": out, "top": top, "size": size, "html": html,
                                                                       **({"color": NAVY, "shadow": False} if dark else {}), **kw}
    pill = lambda at, out, html, top: {"type": "pill", "in": at, "out": out, "top": top, "html": html, "bg": "var(--yellow)", "color": "var(--navy)"}
    photo = lambda at, out, top=380, size=500: {"type": "photo", "in": at, "out": out, "top": top, "left": (1080 - size) // 2, "w": size, "h": size,
                                                "src": "../../assets/img/" + sb["produk_img"]}
    nh = 0
    for i, L in enumerate(lines):
        g, j, tj = L["gambar"], L["jenis"], pieces(L["tajuk"])
        at = 0 if i == 0 else L.at
        img = {"image": g, "color": "navy", "shade": True} if g else None
        if j == "promo":
            scenes += ([(at, img), (L.mid(55), "navy")] if g else [(at, "navy")])
        elif j == "cta":
            scenes.append((at, "blue"))
        elif j == "desak":
            scenes.append((at, img or "navy"))
        elif j == "harga":
            scenes.append((at, img or "blue"))
        else:
            scenes.append((at, img or "pastel"))
        head = " ".join(tj)
        if j in ("hook", "poin"):
            if g:
                els.append({"type": "banner", "in": L.at, "out": L.out, "top": 200, "html": f"{head}<br><em>{L['sorot']}</em>" if L["sorot"] else em_last(head)})
            else:
                els.append(title(L.at, L.out, "<br>".join(tj), top=200, size=96, dark=True))
                if L["sorot"]:
                    els.append(pill(L.mid(45), L.out, L["sorot"], 440))
        elif j in ("produk", "warna"):
            if g:
                els.append({"type": "banner", "in": L.at, "out": L.out, "top": 200, "html": em_last(head)})
            else:
                els.append(title(L.at, L.out, head, top=200, size=110, dark=True))
                if j == "produk":
                    els.append(photo(L.at, L.out))
                elif sb.get("produk") == "neon":
                    els.append({"type": "lineup", "in": L.at, "out": L.out, "keys": [{"at": L.at, "unit": "all", "zoom": 1}] +
                                [{"at": L.mid(25 + 15 * k), "unit": u, "zoom": 2.1} for k, u in enumerate(["pink", "mint", "ciel", "gray", "white"])] +
                                [{"at": f"{L.at}e", "unit": "all", "zoom": 1}]})
            if j == "produk" and L["sorot"]:
                els.append(pill(L.mid(55), L.out, "✓ " + L["sorot"], 330 if g else 950))
        elif j == "suhu":
            if not g:
                els.append(photo(L.at, L.out))
            els.append({"type": "chips", "in": L.at, "out": L.out, "top": 220 if g else 950, "items": [
                {"text": "PANAS", "color": "#ff7a6b", "at": L.at}, {"text": "SEJUK", "color": "#6cc2ff", "at": L.mid(30)},
                {"text": "SUHU BILIK", "color": NAVY, "at": L.mid(60)}]})
        elif j == "harga":
            if L["label"]:
                els.append({"type": "banner", "in": L.at, "out": L.out, "top": 200, "html": em_last(L["label"])} if g else title(L.at, L.out, L["label"], top=230, size=90))
            nh += 1
            ic = L["ikon"] or ("tech" if nh % 2 else "box")
            els.append({"type": "card", "in": L.mid(30) if L["label"] else L.at, "out": L.out, "top": 1260 if g else 840, "icon": ic,
                        **({"icbg": "#fff3cc", "iccolor": "#b07b00"} if ic == "box" else {}),
                        "title": f"{L['harga']} {L['per'] or 'SEBULAN'}", "sub": (L["sub"] or "").capitalize()})
        elif j == "promo":
            if g:
                els.append(pill(L.at, L.mid(55), head, 260))
            s0 = 55 if g else 0
            if L["atas"]:
                els.append({"type": "text", "in": L.mid(s0), "out": L.out, "top": 300, "size": 60, "weight": 800, "html": L["atas"]})
            els.append(title(L.mid(s0), L.out, f"{L['pre'] or ''}<br><span style='color:var(--yellow)'>{L['harga']}</span>", top=420, size=170, hit=True))
            if L["sub"]:
                els.append(pill(L.mid(s0 + 20), L.out, L["sub"], 900))
        elif j == "desak":
            els.append({"type": "icon", "in": L.at, "out": L.out, "top": 300, "icon": "clock", "size": 260, "color": "#fff"})
            els.append(title(L.at, L.out, em_last(head).replace("<em>", "<span style='color:var(--yellow)'>").replace("</em>", "</span>"), top=640, size=130))
            if L["sorot"]:
                els.append({"type": "stamp", "in": L.mid(55), "out": L.out, "top": 960, "html": L["sorot"], "rot": -6})
        elif j == "cta":
            els.append(photo(L.at, None, top=200, size=420))
            els.append({"type": "cta", "in": L.at, "top": 720, "button": sb.get("button", "WhatsApp saya"), "btnAt": L.mid(35),
                        "ticks": sb["ticks"], "fine": sb["fine"]})
    head = {"voice": sb["voice"], "style": sb["style_tts"], "theme": "coway", "brand": "COWAY", "tagline": sb.get("tagline", "")}
    return head, scenes, els


# ------------------------------------------------------------------ utama
def main(path):
    sb = json.loads(pathlib.Path(path).read_text())
    rows = sb["baris"]
    lines = [Line(b, rows[i + 1]["id"] if i + 1 < len(rows) else None) for i, b in enumerate(rows)]
    for L in lines:
        if L["gambar"]:
            assert (ROOT / "assets/img" / L["gambar"]).exists(), f"gambar tiada: {L['gambar']}"
    pi = next((i for i, L in enumerate(lines) if L["jenis"] == "promo"), None)
    sb["_after_promo"] = lines[pi + 2].at if pi is not None and pi + 2 < len(lines) else None
    sb["_promo_bg"] = {"kinetic": "k-white", "comic": "comic-white", "glow": "glow-dark", "paper": "paper-cream", "ugc": "ugc-white"}
    sb["_cut"] = "../../assets/img/" + sb.get("produk_cut", "hype/neon_pink.png")
    sb["_lineup"] = "../../assets/img/" + sb.get("produk_lineup", "hype/lineup_cut.png")
    lj = [{"id": b["id"], "text": b["text"], "cap": b["cap"]} for b in rows]
    master = sb["video"][0]["id"]
    for k, v in enumerate(sb["video"]):
        vid, st = v["id"], v["gaya"]
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(lj, ensure_ascii=False, indent=1))
        if st.startswith("mg:"):
            assert (ROOT / "reference/mg-styles-15/prompts" / f"{st[3:]}.md").exists(), f"{vid}: gaya mg tiada: {st}"
            if not (d / "spec.json").exists():
                (d / "spec.json").write_text(json.dumps({"slug": f"{sb['slug']}-{st[3:].split('-', 1)[1]}", "voice": sb["voice"], "style": sb["style_tts"],
                                                         "player": "mg", "mg": st[3:], "bpm": 120, "cues": {}, "sfx": []}, ensure_ascii=False, indent=1))
            note = "mg: tulis index.html + cues ikut coway-video/formats/mg-gaya.md"
        else:
            assert st in TEMPLAT, f"{vid}: gaya tak dikenali '{st}' (templat: {', '.join(TEMPLAT)}, atau mg:<nama>)"
            head, scenes, els = coway_video(sb, lines) if st == "coway" else hype_video(st, sb, lines)
            spec = {"slug": f"{sb['slug']}-{st}", **head, "scenes": [{"at": a, "bg": b} for a, b in scenes], "els": els}
            (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
            note = f"{len(scenes)} babak, {len(els)} elemen"
        copied = ""
        if k and (HERE / master / "vo.wav").exists():          # satu suara untuk semua gaya
            for f in ("vo.wav", "segments.json", "chunks.txt"):
                if (HERE / master / f).exists():
                    (d / f).write_bytes((HERE / master / f).read_bytes())
            copied = f", VO disalin dari {master}"
        print(f"{vid}  {st:24s} {note}{copied}")


if __name__ == "__main__":
    main(sys.argv[1])
