# Montaj "30 VIDEO WP COWAY" — 3 versi × 15 saat (Portrait 1080×1920)

Untuk mempromosi pakej 30 video Coway kepada ejen. Setiap montaj guna potongan daripada video sedia ada
(Menyampah Air Botol, Neo Plus 60s, Neo Plus versi penuh, Villaem 3) dengan teks bold **30 VIDEO / WP COWAY**
di tengah sepanjang video. Tiada shot berulang antara versi.

| Fail | Gaya |
|---|---|
| `out/pakej30_v1.mp4` | 15 potongan × 1 s, kilat putih setiap potongan, muzik ceria (C–Am–F–G) |
| `out/pakej30_v2.mp4` | 30 potongan × 0.5 s (30 shot = "30 video"), hi-hat laju, muzik bertenaga (Am–F–C–G) |
| `out/pakej30_v3.mp4` | 10 potongan × 1.5 s, lebih tenang, muzik hangat (F–C–Dm–Bb) |

## Bina semula
```
python pakej30/build.py        # semua versi (muzik dijana automatik)
python pakej30/build.py 2      # satu versi
```
Tukar shot dalam `shots.json` (`video` = fail sumber, `t` = saat tengah shot; `cut` × bilangan shot mesti = 15).
