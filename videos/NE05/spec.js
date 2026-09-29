window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "night",
   "t1": 3.28
  },
  {
   "t0": 3.28,
   "bg": {
    "clip": "bottles_busy",
    "c0": 0.0,
    "c1": 3.9
   },
   "t1": 8.91
  },
  {
   "t0": 8.91,
   "bg": {
    "clip": "press_pour",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 12.82
  },
  {
   "t0": 12.82,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 16.2
  },
  {
   "t0": 16.2,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 20.58
  },
  {
   "t0": 20.58,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 24.97
  },
  {
   "t0": 24.97,
   "bg": "navy",
   "t1": 27.3
  },
  {
   "t0": 27.3,
   "bg": "pastel",
   "t1": 30.09
  },
  {
   "t0": 30.09,
   "bg": {
    "clip": "bottle_to_baby",
    "c0": 4.5,
    "c1": 10.0
   },
   "t1": 35.55
  },
  {
   "t0": 35.55,
   "bg": "blue",
   "t1": 40.03
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 560,
   "size": 260,
   "html": "03:00",
   "t0": 0.18,
   "t1": 3.28
  },
  {
   "type": "text",
   "top": 880,
   "size": 56,
   "weight": 700,
   "html": "Baby menangis... 😢",
   "t0": 1.32,
   "t1": 3.28
  },
  {
   "type": "pill",
   "top": 270,
   "html": "DEKAT & CEPAT",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 8.91,
   "t1": 12.82
  },
  {
   "type": "title",
   "top": 190,
   "size": 110,
   "html": "COWAY <span style='color:#E86E5A'>NEON</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 12.82,
   "t1": 16.2
  },
  {
   "type": "pill",
   "top": 270,
   "html": "TEKAN JE",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 16.2,
   "t1": 18.44
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@07",
     "t": 18.44
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@07%30",
     "t": 19.028
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@07%60",
     "t": 19.616
    }
   ],
   "t0": 18.44,
   "t1": 20.58
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
   "zx": 74,
   "zy": 29,
   "zs": 2.6,
   "t0": 20.58,
   "t1": 24.97,
   "zt0": 20.58,
   "zt1": 22.362
  },
  {
   "type": "pill",
   "top": 250,
   "html": "250ml · BERHENTI SENDIRI",
   "bg": "#fff",
   "color": "var(--navy)",
   "t0": 22.164,
   "t1": 24.97
  },
  {
   "type": "card",
   "top": 760,
   "icon": "filter",
   "title": "PENAPIS NANOTRAP",
   "sub": "Teknologi penapisan Coway",
   "t0": 24.97,
   "t1": 27.3
  },
  {
   "type": "card",
   "top": 760,
   "icon": "baby",
   "icbg": "#fde8e4",
   "iccolor": "#E86E5A",
   "title": "SUHU AIR SUSU?",
   "sub": "Ikut nasihat doktor / pakar kanak-kanak",
   "t0": 27.3,
   "t1": 30.09
  },
  {
   "type": "pill",
   "top": 270,
   "html": "PROMOSI RM54 + REBAT RM20 × 7 BULAN*",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 30.09,
   "t1": 35.55
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 35.55,
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
   "t0": 35.55,
   "t1": null
  }
 ],
 "clips": {
  "bottles_busy": {
   "dir": "../../out/frames/NE05_bottles_busy/",
   "n": 120,
   "start": 0.0
  },
  "press_pour": {
   "dir": "../../out/frames/NE05_press_pour/",
   "n": 201,
   "start": 0.0
  },
  "bottle_to_baby": {
   "dir": "../../out/frames/NE05_bottle_to_baby/",
   "n": 165,
   "start": 4.5
  }
 }
};
