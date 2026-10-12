"""Jana spesifikasi video siri E (Coway Elite + perbandingan Prime II) -> tilam/b/eNN.json

    python tilam/elite/gen_specs.py && python tilam/build_b.py e02 e05 e06 --style kinetic
Plan & fakta: tilam/elite/plan_elite_10_video.md
Peraturan babak hook: sebelum produk diperkenalkan, guna gambar jana (assets/tilam/jana/), bukan gambar produk.
Hanya video yang faktanya sudah disahkan dijana di sini (E02, E05, E06).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "b"
EL, P2, J = "assets/tilam/elite/", "assets/tilam/prime2/", "assets/tilam/jana/"
EV = EL + "video/"
THEME_ELITE = {"bg": "#1a1712", "bg2": "#4a3f2e", "accent": "#e8c98a", "accent2": "#f5e6c4", "ink": "#1a1712"}
ELITE = {"name": "COWAY <b>ELITE</b>", "sub": "Soft &amp; Firm · Queen &amp; King", "img": EL + "latest-gallery1.png", "ctaSize": 92}
CLIPS_ELITE = {
    "orbs": {"src": EV + "16x9_CUTDOWN_02_HIRES.mp4", "from": 5.0, "to": 10.0},
    "hero": {"src": EV + "16x9_CUTDOWN_01_HIRES.mp4", "from": 12.0, "to": 16.0},
    "plush": {"src": EV + "16x9_CUTDOWN_03_HIRES.mp4", "from": 2.0, "to": 8.0},
    "uv": {"src": EV + "16x9_CUTDOWN_04_HIRES.mp4", "from": 8.2, "to": 10.6},
}
CLIPS_P2 = {
    "layers5": {"src": P2 + "video/prime2-panel5.mp4", "from": 0.5, "to": 8.5},
    "spring7": {"src": P2 + "coway-prime2-series-mattress-7-zone-pocket-spring.mp4", "from": 0, "to": 5.0},
    "topper": {"from": 34.0, "to": 40.5},
    "topview": {"from": 11.2, "to": 14.0},
}
IMG = {
    "penat": J + "hook_bangun_penat.png", "pasangan": J + "hook_pasangan_terganggu.png", "mendap": J + "hook_tilam_mendap.png",
    "uv2": P2 + "step-7-mattress-cleaning-services-uv-sterilisation-coway-prime2.jpg",
    "p2bed": P2 + "prime2-panel3-desktop.jpg",
}
MB = [0, 600, 1080, 608]
TOPNOTE = "*Untuk pelanggan sewa. Tertakluk kepada terma &amp; syarat."
SVCNOTE = "*Untuk pakej termasuk servis."


def L(i, text, **scene): return {"id": f"{i:02d}", "text": text.replace("Prime II", "Prime 2"), "scene": scene}  # TTS sebut "Prime 2"; paparan tukar ke "Prime II"
def H(t=None, k=None, s=None, y=170, **kw): return dict({k2: v for k2, v in [("t", t), ("k", k), ("s", s)] if v}, y=y, **kw)
def M(img=None, clip=None, box=MB, **kw): return dict({"img": IMG[img]} if img else {"clip": clip}, box=box, **kw)
def BG(img=None, clip=None, dim=1): return dict({"img": IMG[img]} if img else {"clip": clip}, dim=dim)
def W(t, at=0.05, size=120, y=640, **kw): return dict(t=t, at=at, size=size, y=y, **kw)
def item(t, at, y, x=False): return dict({"t": t, "at": at, "y": y}, **({"x": True} if x else {}))
def chips(*xs, y=1260, gap=105): return [{"t": t, "at": at, "y": y + i * gap} for i, (t, at) in enumerate(xs)]
def cta(t): return {"cta": {"at": 0.1, "t": t}}


V = {}
V["e02"] = dict(title="Tidur 8 jam, bangun masih penat?", slug="tidur-8-jam-bangun-penat-elite", mood="calm",
                theme=THEME_ELITE, product=ELITE, clips=CLIPS_ELITE, lines=[
    L(1, "Tidur lapan jam, tapi bangun masih rasa penat?",
      bg=BG("penat"), head=H("Tidur 8 jam…<br>bangun <b>masih penat?</b>", k="POV", y=200)),
    L(2, "Kajian kata, satu daripada tiga rakyat Malaysia bangun pagi rasa penat.",
      bg=BG("penat", dim=.6), words=[W("<b>32%</b>", at="satu", size=220, y=560),
                                     W("rakyat Malaysia bangun penat", at="rakyat", size=64, y=820, anim="up")],
      note={"t": "Sumber: The Edge Malaysia", "y": 1480, "at": "rakyat"}),
    L(3, "Kadang bukan sebab kurang tidur, tapi tilam tak sokong badan dengan betul.",
      bg=BG("mendap"), words=[W("KURANG TIDUR?", at=0.05, size=100, y=560, strike="tapi"),
                              W("TILAM TAK <b>SOKONG</b>.", at="tilam", size=110, y=740)]),
    L(4, "Coway Elite ada sistem sokongan sembilan zon. Bahu, pinggang, pinggul, setiap bahagian dapat sokongan yang seimbang.",
      head=H("Sokongan <b>9 zon</b>", k="COWAY ELITE"), media=M(clip="orbs"),
      chips=chips(("Bahu", "Bahu"), ("Pinggang", "pinggang"), ("Pinggul", "pinggul"))),
    L(5, "Bukan kira berapa jam tidur. Tapi jadikan setiap jam tu berkualiti.",
      bg=BG(clip="hero", dim=.8), words=[W("BUKAN KIRA JAM.", at=0.05, size=100, y=600),
                                         W("JADIKAN SETIAP JAM <b>BERKUALITI</b>.", at="jadikan", size=84, y=780)]),
    L(6, "Nak rasa sendiri? WhatsApp saya, saya terangkan.", **cta("Tilam paling premium siri BEREX.")),
])

V["e05"] = dict(title="Tilam biasa vs Coway Prime II: 5 beza", slug="tilam-biasa-vs-prime2-5-beza", mood="drive",
                clips=CLIPS_P2, lines=[
    L(1, "Tilam biasa dengan Coway Prime II. Apa sebenarnya beza?",
      bg=BG("mendap"), head=H("Apa <b>beza</b><br>sebenarnya?", k="TILAM BIASA vs PRIME II", y=200)),
    L(2, "Satu, lapisan. Banyak tilam biasa cuma ada satu dua lapisan. Prime II ada enam, dari fabrik sejuk sampai sabut kelapa.",
      head=H("Lapisan", k="1"), media=M(clip="layers5"),
      items=[item("Tilam biasa: 1–2 lapisan", "Banyak", 1260, x=True), item("Prime II: <b>6 lapisan</b>", "enam", 1400)]),
    L(3, "Dua, spring. Tilam biasa, pasangan pusing, kita pun terjaga.",
      bg=BG("pasangan"), head=H("Pasangan pusing,<br><b>kita terjaga</b>", k="2 · SPRING", y=200)),
    L(4, "Prime II guna pocket spring tujuh zon. Pasangan pusing, kurang terasa.",
      head=H("Pocket spring <b>7 zon</b>", k="PRIME II"), media=M(clip="spring7"),
      chips=chips(("Kurang gangguan pasangan", "kurang"))),
    L(5, "Tiga, topper. Tilam biasa, kalau lapisan atas dah mendap, kena tukar satu tilam. Prime II, topper ditukar baru tiga tahun sekali.",
      head=H("Topper", k="3"), media=M(clip="topper"),
      items=[item("Tilam biasa: tukar satu tilam", "Tilam biasa", 1260, x=True), item("Prime II: <b>topper baru 3 tahun*</b>", "ditukar", 1400)],
      note={"t": TOPNOTE, "y": 1560, "at": "ditukar"}),
    L(6, "Empat, servis. Teknisyen datang setiap empat bulan, servis tujuh langkah.",
      head=H("Servis <b>4 bulan</b> sekali*", k="4"), media=M(img="uv2"),
      chips=chips(("7 langkah, sampai UV", "tujuh")), note={"t": SVCNOTE, "y": 1420, "at": "tujuh"}),
    L(7, "Lima, hantar dan pasang percuma, termasuk Sabah dan Sarawak.",
      head=H("Hantar &amp; pasang <b>percuma</b>", k="5"), media=M(clip="topview"),
      chips=chips(("Termasuk Sabah &amp; Sarawak", "Sabah"))),
    L(8, "Nak tengok Prime II depan mata? WhatsApp saya.", **cta("Saya tunjukkan beza dia.")),
])

V["e06"] = dict(title="Tilam 3 tahun kemudian", slug="tilam-3-tahun-kemudian-prime2", mood="warm",
                clips=CLIPS_P2, lines=[
    L(1, "Beli tilam hari ni. Tiga tahun lagi, macam mana rupanya?",
      bg=BG("mendap"), head=H("3 tahun lagi,<br><b>macam mana rupanya?</b>", k="TILAM ANDA", y=200)),
    L(2, "Lepas beberapa tahun, banyak tilam biasa mula mendap di tengah, tempat kita selalu baring.",
      bg=BG("penat", dim=.55), diagram="sag", sag={"at": 0.2, "sagAt": "mendap", "topper": False},
      head=H("Mula <b>mendap</b> di tengah", k="TILAM BIASA", y=200)),
    L(3, "Lapisan atas tak boleh ditukar. Nak cuci pun susah.",
      bg=BG("mendap", dim=.6), items=[item("Lapisan atas <b>tak boleh tukar</b>", "Lapisan", 700, x=True),
                                      item("Nak cuci <b>susah</b>", "cuci", 860, x=True)]),
    L(4, "Coway Prime II lain. Topper dia boleh dibuka, mudah diangkat untuk dicuci di rumah.",
      head=H("Topper <b>boleh dibuka</b>", k="COWAY PRIME II"), media=M(clip="topper"),
      chips=chips(("Mudah diangkat", "mudah"), ("Cuci di rumah", "rumah"))),
    L(5, "Masuk tahun ketiga, topper ditukar baru untuk pelanggan sewa. Servis pula setiap empat bulan.",
      head=H("Tahun ke-3: <b>topper baru*</b>", k="PRIME II"), media=M(img="p2bed"),
      chips=chips(("Topper ditukar 3 tahun sekali*", "topper"), ("Servis setiap 4 bulan", "Servis")),
      note={"t": TOPNOTE, "y": 1480, "at": "pelanggan"}),
    L(6, "Jadi tilam rasa macam baru, lebih lama. WhatsApp saya.", **cta("Tilam yang dijaga, bukan dibiar.")),
])

if __name__ == "__main__":
    for vid, d in V.items():
        spec = dict(id=vid, slug=d["slug"], title=f"{vid.upper()} — {d['title']}", mood=d["mood"],
                    **{k: d[k] for k in ("theme", "product") if k in d}, clips=d["clips"], lines=d["lines"])
        (OUT / f"{vid}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        print("tulis", OUT / f"{vid}.json")
