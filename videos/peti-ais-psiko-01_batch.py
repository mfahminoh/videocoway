"""Peti ais Coway x psikografik thread (research/peti-ais-psikografik.md): PA38-PA42, isu -> Coway sebagai penyelesaian.
Hook = ayat sebenar komen (nama jenama/pengguna dibuang). Promo batch 3. Tiada dakwaan tahan lama / repair percuma.

    python3 videos/peti-ais-psiko-01_batch.py && python3 videos/build_video.py PA38 --tts --render --review out/peti-ais-psiko-01
"""
import importlib.util, json, pathlib
HERE = pathlib.Path(__file__).parent
_s = importlib.util.spec_from_file_location("b3", HERE / "peti-ais-p2-01_b3.py"); b3 = importlib.util.module_from_spec(_s); _s.loader.exec_module(b3)
b1 = b3.b1
L, R, banner, title, pill, photo, card, lakonan = b1.L, b1.R, b1.banner, b1.title, b1.pill, b1.photo, b1.card, b1.lakonan
price, hantar, cta, FINE_PW = b3.price, b3.hantar, b3.cta, b3.FINE_PW
RED, YEL, BRAND = b1.RED, b1.YEL, b1.BRAND
FEM_S = "Say in Malaysian Malay, as a tired, fed-up mother venting honestly to a friend, emotional but natural"
MALE_S = "Say in Malaysian Malay, as a frustrated father telling a real experience, sincere, natural pace"
INTRO = ("Peti ais Coway ada dua jenis. Multi-Door, lima ratus lima puluh satu liter, empat pintu. Dan Side-by-Side, tujuh ratus lima belas liter. Dua-dua, Cody datang servis berkala tujuh tahun.",
         "Coway: *551L 4 pintu* · *715L side-by-side*", "Rasmi 551_front + 715_kitchen1, kad Cody")
END = ("Dari lapan puluh empat ringgit sebulan. Sekarang promosi rebat, bayar dua puluh ringgit je, tujuh bulan pertama. Hantar dan pasang percuma. WhatsApp saya.",
       "Bayar *RM20*/bulan · 7 bulan* · *WhatsApp saya*", "Harga + CTA")


def tail(n):
    a = f"@{n:02d}"
    return [price(a, f"{a}%60", "RM84"), hantar(f"{a}%40", f"{a}%60"), cta(f"{a}%60", fine=FINE_PW, btn=f"{a}%80")]


def bridge(a, o, html):
    return title(a, o, html, top=640, size=110)


def intro(a, o):
    F = b1.F
    return [banner(a, o, "PETI AIS COWAY <em>ADA 2 JENIS</em>"),
            {"type": "photo", "in": a, "out": o, "top": 400, "left": 70, "w": 450, "h": 560, "src": F + "551_front.jpg"},
            {"type": "photo", "in": f"{a}%35", "out": o, "top": 400, "left": 560, "w": 450, "h": 560, "src": F + "715_kitchen1.jpg"},
            {"type": "chips", "in": a, "out": o, "top": 1000, "items": [{"text": "551L · 4 PINTU", "color": "#fff", "at": f"{a}%15"},
                                                                       {"text": "715L · SIDE-BY-SIDE", "color": YEL, "at": f"{a}%40"}]},
            card(f"{a}%70", o, "tech", "CODY SERVIS BERKALA", "Dua-dua model, 7 tahun", top=1150)]


SC = [("@04", "navy"), ("@05", "navy"), ("@06", "blue")]
V = {}
V["PA38"] = dict(tajuk="Penat buang lauk basah", slug="penat-buang-lauk-basah", voice="Sulafat", style=FEM_S, lines=L(
    ("Penat. Banyak kali dah terpaksa buang lauk basah kat freezer, sebab peti rosak.", "Penat. *Banyak kali dah* buang lauk basah", "pa13_a_tong"),
    ("Ayam, ikan, rendang. Semua masuk tong sampah.", "Ayam · ikan · *rendang*", "pa13_b_cium"),
    ("Sampai satu tahap, daripada buang lauk je selalu, biar peti ni yang saya buang.", "*Biar peti ni yang saya buang*", "pa07_a_nazak"),
    ("Kali ni, saya nak peti yang ada orang jaga.", "Kali ni, nak yang *ada orang jaga*", "Tajuk"),
    INTRO, END),
  scenes=[(0, R("pa13_a_tong", "night")), ("@02", R("pa13_b_cium", "night")), ("@03", R("pa07_a_nazak", "night")), SC[0], SC[1], SC[2]],
  els=[lakonan(), banner("@01", "@02", "PENAT. <em>BANYAK KALI DAH</em><br>BUANG LAUK BASAH"),
       pill("@02", "@03", "AYAM · IKAN · RENDANG → TONG SAMPAH", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "BIAR PETI NI<br>YANG SAYA BUANG", top=600, size=110, color="#ffffff"),
       bridge("@04", "@05", "KALI NI, NAK YANG<br>ADA ORANG JAGA"), *intro("@05", "@06"), *tail(6)])
V["PA39"] = dict(tajuk="Kejap elok, kejap rosak", slug="kejap-elok-kejap-rosak", voice="Kore", style=FEM_S, lines=L(
    ("Alamak. Peti ais saya pun, sekejap elok, sekejap tak.", "Sekejap elok, *sekejap tak* 😭", "pa12_b_separuh"),
    ("Pagi sejuk. Petang lauk dah berbau. Tak tahu nak percaya ke tak.", "Pagi sejuk. Petang *dah berbau*.", "pa13_b_cium"),
    ("Bosan hadap perangai peti ni. Tengah berkira-kira, nak baiki lagi, atau beli baru.", "Baiki lagi, atau *beli baru*?", "pa11_a_repair"),
    ("Kalau beli baru, pilih yang ada orang datang jaga.", "Pilih yang *ada orang jaga*", "Tajuk"),
    INTRO, END),
  scenes=[(0, R("pa12_b_separuh")), ("@02", R("pa13_b_cium", "night")), ("@03", R("pa11_a_repair")), SC[0], SC[1], SC[2]],
  els=[banner("@01", "@02", "SEKEJAP ELOK,<br><em>SEKEJAP TAK</em> 😭"),
       pill("@02", "@03", "PAGI SEJUK · PETANG DAH BERBAU", top=1180, bg=RED, color="#fff"),
       banner("@03", "@04", "BAIKI LAGI,<br><em>ATAU BELI BARU?</em>"),
       bridge("@04", "@05", "PILIH YANG<br>ADA ORANG JAGA"), *intro("@05", "@06"), *tail(6)])
V["PA40"] = dict(tajuk="Ada waranti, tetap kena bayar", slug="waranti-tetap-kena-bayar", voice="Algieba", style=MALE_S, lines=L(
    ("Ada waranti, tapi nak tukar kompressor, tetap kena bayar tujuh ratus ringgit lebih.", "Ada waranti… tetap bayar *RM700+*", "pa11_b_resit"),
    ("Technician datang rumah, tengok pun tak pasti rosak sebab apa.", "Tengok pun *tak pasti rosak sebab apa*", "pa11_a_repair"),
    ("Kos dia, sama macam beli baru.", "Kos *sama macam beli baru*", "pa15_a_kira"),
    ("Jadi bila nak tukar, tanya dulu: lepas beli, siapa yang jaga?", "Lepas beli, *siapa yang jaga?*", "Tajuk"),
    INTRO, END),
  scenes=[(0, R("pa11_b_resit")), ("@02", R("pa11_a_repair")), ("@03", R("pa15_a_kira")), SC[0], SC[1], SC[2]],
  els=[lakonan(), banner("@01", "@02", "ADA WARANTI…<br><em>TETAP BAYAR RM700+</em>"),
       pill("@02", "@03", "TENGOK PUN TAK PASTI ROSAK SEBAB APA", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "KOS SAMA MACAM<br>BELI BARU", top=600, size=110, color="#ffffff"),
       bridge("@04", "@05", "LEPAS BELI,<br>SIAPA YANG JAGA?"), *intro("@05", "@06"), *tail(6)])
V["PA41"] = dict(tajuk="Peti mak 20 tahun, peti kita 4 tahun", slug="peti-mak-20-tahun", voice="Aoede", style=FEM_S, lines=L(
    ("Peti ais mak saya bertahan dua puluh tahun. Peti saya? Empat tahun je.", "Peti mak *20 tahun*. Peti saya? *4 tahun je.*", "pa07_a_nazak"),
    ("Orang lain semua pakai atas sepuluh tahun. Kita baru masuk tahun keempat, dah rosak.", "Kita baru tahun ke-4, *dah rosak*", "pa13_a_tong"),
    ("Belum puas pakai, dah kena buang. Serupa harga pakai buang je.", "Belum puas pakai, *dah kena buang*", "pa13_c_bungkus"),
    ("Kali ni, saya nak tenang.", "Kali ni, saya nak *tenang*", "Tajuk"),
    INTRO, END),
  scenes=[(0, R("pa07_a_nazak", "night")), ("@02", R("pa13_a_tong")), ("@03", R("pa13_c_bungkus", "night")), SC[0], SC[1], SC[2]],
  els=[lakonan(), banner("@01", "@02", "PETI MAK <em>20 TAHUN</em>.<br>PETI SAYA? <em>4 TAHUN JE.</em>"),
       pill("@02", "@03", "BARU TAHUN KE-4, DAH ROSAK", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "BELUM PUAS PAKAI,<br>DAH KENA BUANG", top=600, size=100, color="#ffffff"),
       bridge("@04", "@05", "KALI NI,<br>SAYA NAK TENANG"), *intro("@05", "@06"), *tail(6)])
V["PA42"] = dict(tajuk="Murah, tapi jangan tertipu", slug="murah-jangan-tertipu", voice="Orus", style=b1.MALE, lines=L(
    ("Murah, tapi jangan tertipu.", "Murah, tapi *jangan tertipu*", "s15_kedai"),
    ("Ramai beli peti sebab harga. Tak sampai setahun, tiga kali claim.", "Tak sampai setahun, *3 kali claim*", "pa11_a_repair"),
    ("Mahal sikit tak apa, asal tak sakit kepala. Biar alah membeli, menang memakai.", "Biar alah membeli, *menang memakai*", "pa15_a_kira"),
    ("Kali ni, pilih yang ada orang jaga.", "Pilih yang *ada orang jaga*", "Tajuk"),
    INTRO, END),
  scenes=[(0, R("s15_kedai")), ("@02", R("pa11_a_repair")), ("@03", R("pa15_a_kira")), SC[0], SC[1], SC[2]],
  els=[banner("@01", "@02", "MURAH,<br><em>TAPI JANGAN TERTIPU</em>"),
       pill("@02", "@03", "TAK SAMPAI SETAHUN, 3 KALI CLAIM", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "BIAR ALAH MEMBELI,<br>MENANG MEMAKAI", top=600, size=100, color="#ffffff"),
       bridge("@04", "@05", "PILIH YANG<br>ADA ORANG JAGA"), *intro("@05", "@06"), *tail(6)])

if __name__ == "__main__":
    md = ["# Skrip: peti-ais-psiko-01 — 5 video isu → Coway (PA38–PA42)\n",
          "Status: DILULUSKAN 1 Nov 2026 (user). Sumber hook: research/peti-ais-psikografik.md (ayat komen asal, nama jenama dibuang). Promo batch 3.\n"]
    for vid, v in V.items():
        d = HERE / vid; d.mkdir(exist_ok=True)
        lines = [{k: x for k, x in l.items() if not k.startswith("_")} for l in v["lines"]]
        (d / "lines.json").write_text(json.dumps(lines, ensure_ascii=False, indent=1))
        spec = {"slug": v["slug"], "voice": v["voice"], "style": v["style"], "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"], "cap": False, **BRAND}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        md.append(f"\n## {vid} · {v['tajuk']}\n\n| # | VO | Kapsyen | Visual |\n|---|---|---|---|\n" + "\n".join(f"| {l['id']} | {l['text']} | {l['cap']} | {l['_vis']} |" for l in v["lines"]))
        print(vid, sum(len(l["text"].split()) for l in lines), "perkataan")
    (HERE.parent / "projek" / "peti-ais-psiko-01" / "skrip.md").write_text("\n".join(md) + "\n")
