"""Versi pendek ±30s untuk iklan, dipotong dari render penuh (tanpa render semula).

    python build_short.py            # semua -> out/pendek/<nama>_30s.mp4
    python build_short.py --only j1_masuk_rumah

Setiap versi = babak terpilih (indeks babak dalam src/jerebu/timing/<nama>.js), disambung terus pada
sempadan babak dengan fade audio 40ms. Bingkai pertama babak sambungan ditahan HOLD saat
(sisa pudar babak lain dibuang). Babak terakhir (CTA promosi) sentiasa sampai hujung video.
"""
import argparse
import json
import pathlib
import subprocess

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = ROOT / "out" / "pendek"
HOLD = 0.45

# babak dipilih: hook -> isi utama -> CTA
PICK = {
    "j1_masuk_rumah":  [0, 5, 6],        # "tutup tingkap dah selamat?" -> HEPA tapis apa tingkap tak halang -> promo
    "j2_kenapa_merah": [0, 1, 2, 7],     # semua share -> semua merah -> maksud warna -> promo
    "j3_pm25":         [0, 3, 7],        # musuh tak nampak -> masuk saluran darah (KKM) -> promo
    "j4_tips":         [0, 1, 2, 7],     # lampu masih merah? -> tip 1 & 2 -> Heart Service + promo
    "j5_pilih_model":  [0, 1, 5, 7],     # pening pilih -> Storm II -> Noble 2 -> promo semua model
    "j6_lepas_jerebu": [0, 5, 6, 7],     # "buat apa bayar bulan-bulan?" -> RM20 x 7 bulan -> jerebu datang balik -> CTA
    "m1_storm2":  [0, 1, 3, 6],          # cerita -> Storm II -> mod Haze -> promo
    "m2_lombok3": [0, 1, 5, 6],          # anak bersin -> Lombok III -> sesuai untuk -> promo
    "m3_studio":  [0, 1, 4, 6],          # bilik anak -> Studio -> mesra tidur -> promo
    "m4_suite":   [0, 1, 3, 6],          # ruang tamu -> Suite -> paparan PM2.5 -> promo
    "m5_noble2":  [0, 1, 3, 6],          # bela kucing -> Noble 2 -> HEPA + UVC -> promo
    "m6_atrium":  [0, 1, 2, 6],          # rumah besar -> Atrium -> 2 motor 2 sisi -> promo
}


def source(name):
    if name.startswith("j"):
        return ROOT / "out" / "jerebu" / f"coway_jerebu_{name}.mp4"
    return ROOT / "out" / "model" / f"coway_model_{name}.mp4"


def build(name):
    T = json.loads((ROOT / "src" / "jerebu" / "timing" / f"{name}.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
    sc, dur = T["scenes"], T["duration"]
    segs = [(sc[i][0], dur if i == len(sc) - 1 else sc[i][1]) for i in PICK[name]]
    parts, labels = [], []
    for k, (a, b) in enumerate(segs):
        d = b - a
        if k == 0:
            parts.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{k}]")
        else:   # babak sebelum dalam render penuh masih pudar ±0.4s: tahan bingkai bersih pertama, audio tak berubah
            parts.append(f"[0:v]trim={a + HOLD:.3f}:{b:.3f},setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration={HOLD}[v{k}]")
        parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={d - 0.04:.3f}:d=0.04[a{k}]")
        labels.append(f"[v{k}][a{k}]")
    parts.append("".join(labels) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"coway_{name}_30s.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(source(name)), "-filter_complex", ";".join(parts),
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print(f"{out.name}: {sum(b - a for a, b in segs):.1f}s  babak {PICK[name]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--only")
    a = ap.parse_args()
    for n in ([a.only] if a.only else PICK):
        build(n)
