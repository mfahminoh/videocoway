window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": {
    "clip": "presenter",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 3.15
  },
  {
   "t0": 3.15,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 4.47
  },
  {
   "t0": 4.47,
   "bg": "pastel",
   "t1": 8.8
  },
  {
   "t0": 8.8,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.4
   },
   "t1": 12.86
  },
  {
   "t0": 12.86,
   "bg": "navy",
   "t1": 14.92
  },
  {
   "t0": 14.92,
   "bg": "blue",
   "t1": 21.38
  },
  {
   "t0": 21.38,
   "bg": "blue",
   "t1": 26.06
  }
 ],
 "els": [
  {
   "type": "banner",
   "top": 230,
   "html": "3 SEBAB RAMAI PILIH<br><em>COWAY NEON</em>",
   "t0": 0.1,
   "t1": 3.15
  },
  {
   "type": "reason",
   "top": 250,
   "num": "1",
   "title": "5 WARNA",
   "sub": "ikut tema dapur",
   "t0": 3.15,
   "t1": 4.47
  },
  {
   "type": "title",
   "top": 240,
   "size": 120,
   "html": "<span style='color:#E86E5A'>5</span> WARNA",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 4.47,
   "t1": 8.8
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 4.47
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 5.006
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 5.542
    },
    {
     "unit": "gray",
     "zoom": 2.1,
     "t": 6.079
    },
    {
     "unit": "white",
     "zoom": 2.1,
     "t": 6.615
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 7.228
    }
   ],
   "t0": 4.47,
   "t1": 8.8
  },
  {
   "type": "reason",
   "top": 250,
   "num": "2",
   "title": "3 SUHU",
   "sub": "satu tekan je",
   "t0": 8.8,
   "t1": 12.86
  },
  {
   "type": "chips",
   "top": 1180,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@04%30",
     "t": 9.856
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@04%45",
     "t": 10.384
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@04%60",
     "t": 10.912
    }
   ],
   "t0": 9.856,
   "t1": 12.86
  },
  {
   "type": "reason",
   "top": 760,
   "num": "3",
   "title": "YANG RAMAI<br>TAK JANGKA",
   "t0": 12.86,
   "t1": 14.92
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 14.92,
   "t1": 21.38
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM104",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "to": "RM54",
   "t0": 14.92,
   "t1": 21.38,
   "badgeT": 18.47,
   "strikeT": 16.128,
   "toT": 17.059
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 21.38,
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
   "t0": 21.38,
   "t1": null,
   "btnT": 22.172
  }
 ],
 "clips": {
  "presenter": {
   "dir": "../../out/frames/NL01_presenter/",
   "n": 94,
   "start": 0.0
  },
  "press_pour": {
   "dir": "../../out/frames/NL01_press_pour/",
   "n": 105,
   "start": 3.0
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably.",
 "style": "Say in Malaysian Malay, as a friendly and confident young man on TikTok, relaxed and fairly quick, smiling"
};
