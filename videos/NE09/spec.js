window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 3.45
  },
  {
   "t0": 3.45,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 7.42
  },
  {
   "t0": 7.42,
   "bg": {
    "clip": "bottles_busy",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 9.18
  },
  {
   "t0": 9.18,
   "bg": "navy",
   "t1": 12.96
  },
  {
   "t0": 12.96,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 17.57
  },
  {
   "t0": 17.57,
   "bg": "pastel",
   "t1": 21.03
  },
  {
   "t0": 21.03,
   "bg": "blue",
   "t1": 27.4
  },
  {
   "t0": 27.4,
   "bg": "blue",
   "t1": 34.33
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 520,
   "size": 180,
   "html": "<span style='color:var(--yellow)'>3 TANDA</span>",
   "t0": 0.1,
   "t1": 3.45
  },
  {
   "type": "banner",
   "top": 780,
   "html": "COWAY NEON SESUAI<br><em>UNTUK RUMAH ANDA</em>",
   "t0": 0.976,
   "t1": 3.45
  },
  {
   "type": "reason",
   "top": 250,
   "num": "1",
   "title": "DAPUR KECIL",
   "sub": "Neon kompak, tak makan ruang",
   "t0": 3.45,
   "t1": 7.42
  },
  {
   "type": "reason",
   "top": 250,
   "num": "2",
   "title": "SELALU SIBUK",
   "sub": "ambil pakej self-service",
   "t0": 7.42,
   "t1": 9.18
  },
  {
   "type": "title",
   "top": 250,
   "size": 84,
   "html": "FILTER BARU<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>",
   "t0": 9.18,
   "t1": 12.96
  },
  {
   "type": "delivery",
   "top": 620,
   "t0": 9.18,
   "t1": 12.96
  },
  {
   "type": "reason",
   "top": 220,
   "num": "3",
   "title": "<span style='color:#0B2F6B; text-shadow:none'>ADA BUDAK KECIL</span>",
   "t0": 12.96,
   "t1": 14.97
  },
  {
   "type": "photo",
   "top": 380,
   "left": 0,
   "w": 1080,
   "h": 1080,
   "radius": 0,
   "shadow": false,
   "float": false,
   "src": "../../assets/img/neon/pink.jpg",
   "zx": 57,
   "zy": 33,
   "zs": 2.8,
   "t0": 14.97,
   "t1": 17.57,
   "zt0": 14.97,
   "zt1": 15.852
  },
  {
   "type": "pill",
   "top": 250,
   "html": "🔒 HOT LOCK · TEKAN 3 SAAT",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 15.656,
   "t1": 17.57
  },
  {
   "type": "title",
   "top": 240,
   "size": 100,
   "html": "BONUS: <span style='color:#E86E5A'>5 WARNA</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 17.57,
   "t1": 21.03
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "all",
     "zoom": 1,
     "t": 17.57
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 18.634
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 19.546
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 20.61
    }
   ],
   "t0": 17.57,
   "t1": 21.03
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 21.03,
   "t1": 27.4
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM104",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "to": "RM54",
   "t0": 21.03,
   "t1": 27.4,
   "badgeT": 25.372,
   "strikeT": 22.839,
   "toT": 23.744
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 27.4,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PROMOSI RM54 SEBULAN*",
    "+ REBAT RM20 × 7 BULAN*",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM104/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 27.4,
   "t1": null
  }
 ],
 "clips": {
  "presenter": {
   "dir": "../../out/frames/NE09_presenter/",
   "n": 101,
   "start": 6.4
  },
  "bottles_busy": {
   "dir": "../../out/frames/NE09_bottles_busy/",
   "n": 94,
   "start": 0.0
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably."
};
