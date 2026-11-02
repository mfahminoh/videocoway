"""Explainer fungsi peti ais Coway (projek/peti-ais-explainer-01): PA36 Multi-Door 551L, PA37 Side-by-Side 715L.
-> videos/PA36, PA37/{lines.json, spec.json} dan projek/peti-ais-explainer-01/skrip.md.

    python3 videos/peti-ais-explainer-01_batch.py
    python3 videos/build_video.py PA36 --tts
    python3 videos/peti-ais-explainer-01_batch.py          # jalan semula selepas VO: masa klip ikut segments.json
    python3 videos/build_video.py PA36 --render --review out/peti-ais-explainer-01

Sumber: pelan user (projek/peti-ais-explainer-01/pelan-user.md, bahagian 3-4). Setiap fakta "WAJIB SAHKAN" disemak dengan
coway.com.my (research/peti-ais-produk.md, 25 Okt 2026). VO tiada harga (pelan: "jangan rakam harga kekal");
end card guna promo batch 3 (bayar RM20 x 7 bulan, kemudian RM84 / RM99, hantar & pasang percuma) dengan nota kaki.
Klip rasmi Coway assets/clips/fridge/*.mp4 (segi empat) ditukar ke potret: assets/clips/peti-ais-explainer-01_*.mp4.
"""
import importlib.util
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("b1", HERE / "peti-ais-p2-01_batch.py")
b1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b1)
globals().update({k: getattr(b1, k) for k in (
    "F", "NAVY", "YEL", "BLUE", "RED", "INK", "BRAND", "FEM", "MALE", "L", "banner", "title", "pill", "photo", "card")})
KOD = "peti-ais-explainer-01"

FINE = ("*Promosi rebat: bayar RM20 sebulan untuk 7 bulan pertama, kemudian RM84 (715L) / RM99 (551L), pelan HEART Service "
        "7 tahun, termasuk SST. Hantar &amp; pasang percuma seluruh Malaysia. Promosi terhad, tertakluk terma &amp; syarat Coway. "
        "¹Ujian makmal dalam persekitaran terkawal.")
TICKS = {"551": ["BAYAR RM20 × 7 BULAN PERTAMA*", "KEMUDIAN 551L RM99 SEBULAN", "HANTAR & PASANG PERCUMA"],
         "715": ["BAYAR RM20 × 7 BULAN PERTAMA*", "KEMUDIAN 715L RM84 SEBULAN", "HANTAR & PASANG PERCUMA"]}


def C(name):
    """Klip rasmi potret (assets/clips/peti-ais-explainer-01_<name>.mp4); c1 diisi selepas VO."""
    return {"_clip": f"{KOD}_{name}"}


def cta(at, model):
    return {"type": "cta", "in": at, "top": 700, "ticks": TICKS[model], "button": "WhatsApp saya", "btnAt": f"{at}%40", "fine": FINE}


def chips(at, out, top, *items):
    return {"type": "chips", "in": at, "out": out, "top": top,
            "items": [{"text": t, "color": c, "at": a} for t, a, c in items]}


def grid(at, out, top, *items):
    return {"type": "grid", "in": at, "out": out, "top": top, "items": [{"big": b, "small": s, "at": a} for b, s, a in items]}


V = {}

# ---------------------------------------------------------------- PA36 · Explainer Multi-Door 551L
V["PA36"] = dict(model="551", tajuk="551L, 4 pintu: Convertible Zone, satu laci empat fungsi",
  slug="explainer-multi-door-551l", voice="Orus", style=MALE, lines=L(
    ("Peti ais besar, bukan bermaksud semua barang dicampak dalam satu ruang.", "Besar ≠ *campak dalam satu ruang*", "Klip rasmi 551_bigspace"),
    ("Ini peti ais Coway Multi-Door, lima ratus lima puluh satu liter, empat pintu, warna Black Inox.", "Coway *Multi-Door 551L* · 4 pintu", "Rasmi 551_front"),
    ("Tapi bintang dia, Convertible Zone. Laci bawah ni, satu ruang, empat fungsi. Tukar ikut keperluan, bila-bila masa.",
     "*Convertible Zone*: 1 laci, 4 fungsi", "Klip rasmi 551_convert"),
    ("Lima hingga tiga darjah: buah dan sayur, bila borong banyak.", "5→3°C · *buah & sayur*", "LED 3°C + 551_drawers"),
    ("Dua hingga kosong darjah: minuman sejuk. Tetamu datang, air dah sedia.", "2→0°C · *minuman sejuk*", "LED 0°C"),
    ("Negatif satu hingga negatif tujuh: simpanan singkat. Ayam dan ikan untuk masak esok atau lusa.", "−1→−7°C · *simpanan singkat*", "LED −7°C"),
    ("Negatif lapan hingga negatif dua puluh: simpanan lama. Stok daging korban, stok raya.", "−8→−20°C · *simpanan lama*", "LED −20°C"),
    ("Musim raya, jadikan freezer tambahan. Lepas raya, tukar balik jadi peti sejuk. Satu laci, ikut musim keluarga awak.",
     "Raya: *freezer* · Lepas raya: *peti sejuk*", "Rasmi 551_drawers + cip"),
    ("Triple inverter dan dinding penyejuk logam, untuk sejuk yang konsisten. Silver ion dan penapis penyahbau, bantu kurangkan bau ikan.",
     "Triple Inverter · Dual Hygiene¹", "Klip rasmi 551_airflow"),
    ("Lebar sembilan puluh, dalam enam puluh sentimeter. Ukur dulu, atau cuba dalam dapur guna app Coway AR.",
     "*90.5 × 59.7 cm* · app Coway AR", "Rasmi 551_builtin + grid"),
    ("Nak satu laci yang ikut musim keluarga? WhatsApp saya untuk semak ruang dan model.", "*WhatsApp saya*", "CTA")),
  scenes=[(0, C("551_bigspace")), ("@02", "navy"), ("@03", C("551_convert")), ("@04", "navy"), ("@09", C("551_airflow")), ("@10", "navy"), ("@11", "blue")],
  els=[banner("@01", "@02", "PETI BESAR ≠<br><em>CAMPAK SATU RUANG</em>"),
       banner("@02", "@03", "COWAY <em>MULTI-DOOR 551L</em>"),
       photo("@02", "@03", "551_front.jpg", top=380),
       chips("@02%40", "@03", 1180, ("4 PINTU", "@02%40", "#fff"), ("551L KASAR", "@02%60", "#fff"), ("BLACK INOX", "@02%80", YEL)),
       banner("@03", "@04", "<em>CONVERTIBLE</em> ZONE"),
       pill("@03%40", "@04", "1 LACI · 4 FUNGSI · TUKAR BILA-BILA MASA", top=1350),
       banner("@04", "@08", "<em>CONVERTIBLE</em> ZONE"),
       photo("@04", "@08", "551_drawers.jpg", top=360, w=560, h=560),
       {"type": "led", "in": "@04", "out": "@05", "top": 960, "items": [{"num": "3", "unit": "°C", "label": "BUAH & SAYUR · 5→3°C", "at": "@04"}]},
       {"type": "led", "in": "@05", "out": "@06", "top": 960, "items": [{"num": "0", "unit": "°C", "label": "MINUMAN SEJUK · 2→0°C", "at": "@05"}]},
       {"type": "led", "in": "@06", "out": "@07", "top": 960, "items": [{"num": "-7", "unit": "°C", "label": "SIMPANAN SINGKAT · −1→−7°C", "at": "@06"}]},
       {"type": "led", "in": "@07", "out": "@08", "top": 960, "items": [{"num": "-20", "unit": "°C", "label": "SIMPANAN LAMA · −8→−20°C", "at": "@07"}]},
       banner("@08", "@09", "<em>IKUT MUSIM</em> KELUARGA"),
       photo("@08", "@09", "551_drawers.jpg", top=360, w=560, h=560),
       {"type": "vs", "in": "@08%20", "out": "@09", "top": 960,
        "left": {"title": "MUSIM RAYA", "color": NAVY, "items": ["Freezer tambahan", "Stok rendang & daging"], "at": "@08%20"},
        "right": {"title": "LEPAS RAYA", "color": BLUE, "items": ["Tukar balik", "Jadi peti sejuk"], "at": "@08%55"}},
       banner("@09", "@10", "TRIPLE <em>INVERTER</em>"),
       chips("@09%30", "@10", 1340, ("METAL COOLING", "@09%30", "#fff"), ("DUAL HYGIENE¹", "@09%60", YEL)),
       banner("@10", "@11", "UKUR <em>DULU</em>"),
       photo("@10", "@11", "551_builtin.jpg", top=330, w=400, h=400),
       grid("@10%10", "@11", 760, ("90.5", "LEBAR (CM)", "@10%12"), ("59.7", "DALAM (CM)", "@10%30")),
       pill("@10%60", "@11", "CUBA DALAM DAPUR · APP COWAY AR", top=1000),
       cta("@11", "551")])

# ---------------------------------------------------------------- PA37 · Explainer Side-by-Side 715L
V["PA37"] = dict(model="715", tajuk="715L side-by-side: ruang besar untuk stok keluarga",
  slug="explainer-side-by-side-715l", voice="Kore",
  style="Speak in Bahasa Melayu with a natural Malaysian (Kuala Lumpur) accent, like a friendly Malaysian TV presenter. Use Malaysian Malay pronunciation and intonation, not Indonesian. Warm, clear, moderately paced", lines=L(
    ("Kalau setiap minggu beli stok untuk satu keluarga, ruang tujuh ratus lima belas liter memang nampak bezanya.", "*715L* untuk stok keluarga", "Rasmi 715_spaces"),
    ("Ini peti ais Coway Side-by-Side. Freezer di kiri, peti sejuk di kanan, dua-dua tinggi penuh.", "Freezer *kiri* · peti sejuk *kanan*", "Rasmi 715_open_dark"),
    ("Rak pintu untuk barang kecil, ruang utama untuk bekas besar, dan freezer untuk stok yang dilabel.", "Rak pintu · ruang utama · *freezer berlabel*", "Rasmi 715_kitchen_open"),
    ("Laci sayur ada kawalan kelembapan, bantu sayur dan buah kekal segar lebih lama.", "Laci *Humidity Control*", "Rasmi 715_humidity"),
    ("Double inverter, dengan suhu peti dan freezer dikawal berasingan. Ada empat mod: Smart, Eco, Power Cool, dan Super Freezing sampai negatif dua puluh lima.",
     "Double Inverter · *4 mod* · −25°C", "Rasmi 715_panel_touch + cip mod"),
    ("Silver ion bantu kurangkan bau di peti sejuk, dan penapis penyahbau di freezer neutralkan sehingga sembilan puluh lapan perpuluhan empat peratus bau ikan, dalam ujian makmal.",
     "Dual Hygiene · *98.4%* bau ikan¹", "Rasmi deodoriser 551_deo_cubes"),
    ("Tapi ingat, model ni dalam tujuh puluh empat sentimeter, lebar sembilan puluh satu. Ukur laluan, kedalaman dan ruang buka pintu dulu.",
     "Dalam *74 cm* · lebar *91 cm*", "Rasmi 715_kitchen1 + grid"),
    ("Kalau keutamaan awak kapasiti maksimum dan akses kiri kanan yang mudah, Side-by-Side patut dibandingkan. WhatsApp saya untuk semak ukuran.",
     "Kapasiti maksimum? *Side-by-Side* · *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@08", "blue")],
  els=[banner("@01", "@02", "<em>715L</em> UNTUK STOK KELUARGA"),
       photo(0, "@02", "715_spaces.jpg", top=380),
       banner("@02", "@03", "COWAY <em>SIDE-BY-SIDE</em>"),
       photo("@02", "@03", "715_open_dark.jpg", top=330, w=900, h=706),
       chips("@02%30", "@03", 1120, ("FREEZER KIRI", "@02%35", "#fff"), ("PETI SEJUK KANAN", "@02%55", YEL)),
       banner("@03", "@04", "SETIAP BARANG <em>ADA TEMPAT</em>"),
       photo("@03", "@04", "715_kitchen_open.jpg", top=380),
       chips("@03%15", "@04", 1180, ("RAK PINTU", "@03%15", "#fff"), ("RUANG UTAMA", "@03%40", "#fff"), ("FREEZER BERLABEL", "@03%65", YEL)),
       banner("@04", "@05", "<em>HUMIDITY</em> CONTROL"),
       photo("@04", "@05", "715_humidity.jpg", top=420, w=900, h=675),
       banner("@05", "@06", "DOUBLE <em>INVERTER</em>"),
       photo("@05", "@06", "715_panel_touch.jpg", top=360, w=560, h=560),
       chips("@05%30", "@06", 980, ("SMART", "@05%40", "#fff"), ("ECO", "@05%52", "#fff"), ("POWER COOL", "@05%64", "#fff"), ("SUPER FREEZING −25°C", "@05%76", YEL)),
       banner("@06", "@07", "DUAL <em>HYGIENE</em>"),
       photo("@06", "@07", "551_deo_cubes.jpg", top=380),
       pill("@06%55", "@07", "98.4% BAU IKAN (TRIMETHYLAMINE)¹", top=1180),
       banner("@07", "@08", "UKUR <em>DULU</em>"),
       photo("@07", "@08", "715_kitchen1.jpg", top=360, w=520, h=520),
       grid("@07%10", "@08", 920, ("91", "LEBAR (CM)", "@07%30"), ("74", "DALAM (CM)", "@07%12"), ("190.5", "TINGGI (CM)", "@07%45")),
       cta("@08", "715")])


def resolve(bg, a, b):
    if not (isinstance(bg, dict) and "_clip" in bg):
        return bg
    path = ROOT / "assets" / "clips" / f"{bg['_clip']}.mp4"
    cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                              capture_output=True, text=True).stdout or 0)
    dur = max((b - a) if a is not None and b is not None else cd, 0.5)
    c1 = round(min(max(dur * 0.55, min(cd, dur * 1.9)), cd) - 0.05, 2)
    return {"clip": bg["_clip"], "c0": 0, "c1": c1, "color": "navy", "shade": False}


def skrip_md():
    out = ["# Skrip: peti-ais-explainer-01 — explainer fungsi 551L & 715L\n",
           "Status: **DILULUSKAN 30 Okt 2026** (user: pelan explainer, \"pergi ke next task\") · Sumber: `pelan-user.md` bahagian 3–4",
           "Fakta disemak dengan coway.com.my (`research/peti-ais-produk.md`, 25 Okt 2026). Dijana daripada `videos/peti-ais-explainer-01_batch.py`.",
           f"\nNota kaki CTA: {FINE.replace('&amp;', '&')}\n"]
    for vid, v in V.items():
        out.append(f"\n## {vid} · {v['tajuk']}\nSuara: {v['voice']} · Format: scenes + klip/gambar rasmi Coway\n\n"
                   "| # | VO | Kapsyen | Visual |\n|---|---|---|---|\n" +
                   "\n".join(f"| {l['id']} | {l['text']} | {l['cap']} | {l['_vis']} |" for l in v["lines"]))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        lines = [{k: x for k, x in l.items() if not k.startswith("_")} for l in v["lines"]]
        (d / "lines.json").write_text(json.dumps(lines, ensure_ascii=False, indent=1))
        sp = d / "segments.json"
        seg = {s["id"]: (s["a"], s["b"]) for s in json.loads(sp.read_text())} if sp.exists() else None
        starts = [(0.0 if a == 0 else seg[a[1:3]][0]) if seg else None for a, _ in v["scenes"]]
        end = max(b for _, b in seg.values()) + 2.5 if seg else None
        scenes = [{"at": a, "bg": resolve(bg, starts[i], starts[i + 1] if i + 1 < len(starts) else end)}
                  for i, (a, bg) in enumerate(v["scenes"])]
        spec = {"slug": v["slug"], "voice": v["voice"], "style": v["style"], "scenes": scenes, "els": v["els"], **BRAND}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in lines)
        print(f"{vid} {v['slug']:30s} {v['voice']:6s} {len(lines):2d} baris, {words} perkataan (~{words / 2.4:.0f}s)")
    (ROOT / "projek" / KOD / "skrip.md").write_text(skrip_md())
