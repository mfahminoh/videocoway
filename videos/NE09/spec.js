window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 3.83
  },
  {
   "t0": 3.83,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 8.2
  },
  {
   "t0": 8.2,
   "bg": {
    "clip": "bottles_busy",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 10.38
  },
  {
   "t0": 10.38,
   "bg": "navy",
   "t1": 14.5
  },
  {
   "t0": 14.5,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 19.82
  },
  {
   "t0": 19.82,
   "bg": "pastel",
   "t1": 23.75
  },
  {
   "t0": 23.75,
   "bg": "blue",
   "t1": 26.86
  },
  {
   "t0": 26.86,
   "bg": "blue",
   "t1": 34.37
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 520,
   "size": 180,
   "html": "<span style='color:var(--yellow)'>3 TANDA</span>",
   "t0": 0.29,
   "t1": 3.83
  },
  {
   "type": "banner",
   "top": 780,
   "html": "COWAY NEON SESUAI<br><em>UNTUK RUMAH ANDA</em>",
   "t0": 1.256,
   "t1": 3.83
  },
  {
   "type": "reason",
   "top": 250,
   "num": "1",
   "title": "DAPUR KECIL",
   "sub": "Neon kompak, tak makan ruang",
   "t0": 3.83,
   "t1": 8.2
  },
  {
   "type": "reason",
   "top": 250,
   "num": "2",
   "title": "SELALU SIBUK",
   "sub": "ambil pakej self-service",
   "t0": 8.2,
   "t1": 10.38
  },
  {
   "type": "title",
   "top": 250,
   "size": 84,
   "html": "FILTER BARU<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>",
   "t0": 10.38,
   "t1": 14.5
  },
  {
   "type": "delivery",
   "top": 620,
   "t0": 10.38,
   "t1": 14.5
  },
  {
   "type": "reason",
   "top": 220,
   "num": "3",
   "title": "<span style='color:#0B2F6B; text-shadow:none'>ADA BUDAK KECIL</span>",
   "t0": 14.5,
   "t1": 16.92
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
   "t0": 16.92,
   "t1": 19.82,
   "zt0": 16.92,
   "zt1": 18.095
  },
  {
   "type": "pill",
   "top": 250,
   "html": "🔒 HOT LOCK · TEKAN 3 SAAT",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 17.834,
   "t1": 19.82
  },
  {
   "type": "title",
   "top": 240,
   "size": 100,
   "html": "BONUS: <span style='color:#E86E5A'>5 WARNA</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 19.82,
   "t1": 23.75
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "all",
     "zoom": 1,
     "t": 19.82
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 21.017
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 22.043
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 23.24
    }
   ],
   "t0": 19.82,
   "t1": 23.75
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 23.75,
   "t1": 26.86
  },
  {
   "type": "price",
   "top": 560,
   "label": "DARI",
   "from": "RM54",
   "badge": "DISKAUN 50% · 6 BULAN PERTAMA",
   "to": "RM27",
   "t0": 23.75,
   "t1": 26.86,
   "badgeT": 24.021,
   "strikeT": 24.698,
   "toT": 25.105
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 26.86,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PENGHANTARAN PERCUMA",
    "PEMASANGAN PERCUMA",
    "DARI RM27 SEBULAN*"
   ],
   "button": "WhatsApp saya",
   "fine": "*Diskaun 50% untuk 6 bulan pertama. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 26.86,
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
 }
};
