"""Spesifikasi video dari skrip rasmi BEREX Elite (tilam/elite/skrip_elite_9_video.md) -> tilam/b/sNN.json

    python tilam/elite/gen_specs_skrip.py && python tilam/build_b.py s01
Peraturan visual:
- babak masalah/penerangan guna gambar jana realistik (assets/tilam/jana/el_*)
- visual rasmi Coway hanya pada product reveal, dan setiap gambar laman tidak diulang dalam video yang sama
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "b"
EL, J = "assets/tilam/elite/", "assets/tilam/jana/"
EV = EL + "video/"
THEME = {"bg": "#1a1712", "bg2": "#4a3f2e", "accent": "#e8c98a", "accent2": "#f5e6c4", "ink": "#1a1712"}
PRODUCT = {"name": "COWAY <b>BEREX ELITE</b>", "sub": "Soft &amp; Firm · Queen &amp; King", "img": EL + "latest-gallery2.png", "ctaSize": 76}
CLIPS = {
    "orbs": {"src": EV + "16x9_CUTDOWN_02_HIRES.mp4", "from": 5.0, "to": 10.0},
    "hero": {"src": EV + "16x9_CUTDOWN_01_HIRES.mp4", "from": 12.0, "to": 16.0},
    "plush": {"src": EV + "16x9_CUTDOWN_03_HIRES.mp4", "from": 2.0, "to": 8.0},
    "uv": {"src": EV + "16x9_CUTDOWN_04_HIRES.mp4", "from": 8.2, "to": 10.6},
}
IMG = {
    "penat": J + "el_v1a_bangun_penat.png", "malam": J + "el_v1b_tidur_malam.png", "kedai": J + "el_v1d_kedai_tilam.png",
    "mendap": J + "hook_tilam_mendap.png",
    "layer": EL + "mattreslayer-img.png",
}


def L(i, text, **scene): return {"id": f"{i:02d}", "text": text, "scene": scene}
def H(t=None, k=None, s=None, y=170, **kw): return dict({k2: v for k2, v in [("t", t), ("k", k), ("s", s)] if v}, y=y, **kw)
def BG(img=None, clip=None, dim=1): return dict({"img": IMG[img]} if img else {"clip": clip}, dim=dim)
def W(t, at=0.05, size=120, y=640, **kw): return dict(t=t, at=at, size=size, y=y, **kw)
def chips(*xs, y=1260, gap=105): return [{"t": t, "at": at, "y": y + i * gap} for i, (t, at) in enumerate(xs)]


V = {}
# Video 1 (TOFU) — Tidur dah cukup, tapi kenapa masih penat?
V["s01"] = dict(title="Tidur dah cukup, tapi kenapa masih penat?", slug="tidur-cukup-masih-penat", mood="calm", lines=[
    L(1, "Pernah tak, tidur malam rasa macam dah cukup. Tapi bila bangun pagi, badan masih rasa penat?",
      bg=BG("penat"), head=H("Tidur dah cukup…<br>tapi <b>masih penat?</b>", k="PERNAH TAK?", y=200)),
    L(2, "Kadang-kadang kita ingat, asalkan tidur tujuh ke lapan jam, mesti bangun segar, kan?",
      bg=BG("malam"), words=[W("<b>7–8 JAM</b>", at="tujuh", size=170, y=600), W("= bangun segar?", at="segar", size=80, y=800, anim="up")]),
    L(3, "Tapi sebenarnya, banyak benda boleh pengaruhi keselesaan tidur. Salah satunya, tilam yang kita guna setiap malam.",
      bg=BG("mendap", dim=.85), words=[W("SALAH SATUNYA:", at="Salah", size=70, y=600, anim="up"), W("<b>TILAM</b> KITA.", at="tilam", size=140, y=720)]),
    L(4, "Kita tidur atas tilam yang sama setiap hari. Tapi pernah tak, kita betul-betul ambil tahu apa yang ada dalam tilam tu?",
      bg=BG("kedai"), head=H("Apa yang ada<br><b>dalam tilam</b> kita?", y=200, at="pernah")),
    L(5, "Sebab tu, kalau nak pilih tilam, jangan tengok harga dengan rupa luaran je.", cont=True,
      chips=chips(("Bukan harga je", "harga"), ("Bukan rupa luar je", "rupa"), y=1300)),
    L(6, "Ini yang menarik tentang Coway BEREX Elite. Model tilam premium baharu daripada Coway.",
      bg=BG(clip="hero", dim=.55), head=H("Coway <b>BEREX Elite</b>", k="BAHARU", s="Model tilam premium", y=200)),
    L(7, "Dia gabungkan foam, lateks asli dan pocket spring, dengan sistem sokongan sembilan zon.",
      head=H("Sokongan <b>9 zon</b>", k="DALAM ELITE"), media={"img": IMG["layer"], "box": [0, 560, 1080, 540], "fit": "contain", "kb": "none"},
      chips=chips(("Foam", "foam"), ("Lateks asli", "lateks"), ("Pocket spring", "pocket"), y=1180)),
    L(8, "Kalau tengah survey tilam baru, jom kenali dulu BEREX Elite. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan satu-satu."}),
])

if __name__ == "__main__":
    for vid, d in V.items():
        spec = dict(id=vid, slug=d["slug"], title=f"{vid.upper()} — {d['title']}", mood=d["mood"],
                    theme=THEME, product=PRODUCT, clips=CLIPS, lines=d["lines"])
        (OUT / f"{vid}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        print("tulis", OUT / f"{vid}.json")
