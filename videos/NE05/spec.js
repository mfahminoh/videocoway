window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "night",
   "t1": 2.68
  },
  {
   "t0": 2.68,
   "bg": {
    "clip": "bottles_busy",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 7.52
  },
  {
   "t0": 7.52,
   "bg": {
    "clip": "press_pour",
    "c0": 0.0,
    "c1": 3.0
   },
   "t1": 11.01
  },
  {
   "t0": 11.01,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 14.27
  },
  {
   "t0": 14.27,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 18.56
  },
  {
   "t0": 18.56,
   "bg": {
    "image": "../../assets/img/neon/pink.jpg",
    "color": "pink",
    "top": 380,
    "h": 1080
   },
   "t1": 22.76
  },
  {
   "t0": 22.76,
   "bg": "navy",
   "t1": 25.12
  },
  {
   "t0": 25.12,
   "bg": "pastel",
   "t1": 27.88
  },
  {
   "t0": 27.88,
   "bg": {
    "clip": "bottle_to_baby",
    "c0": 7.2,
    "c1": 10.0
   },
   "t1": 31.13
  },
  {
   "t0": 31.13,
   "bg": "blue",
   "t1": 36.27
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 560,
   "size": 260,
   "html": "03:00",
   "t0": 0.21,
   "t1": 2.68
  },
  {
   "type": "text",
   "top": 880,
   "size": 56,
   "weight": 700,
   "html": "Baby menangis... 😢",
   "t0": 1.126,
   "t1": 2.68
  },
  {
   "type": "pill",
   "top": 270,
   "html": "DEKAT & CEPAT",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 7.52,
   "t1": 11.01
  },
  {
   "type": "title",
   "top": 190,
   "size": 110,
   "html": "COWAY <span style='color:#E86E5A'>NEON</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 11.01,
   "t1": 14.27
  },
  {
   "type": "pill",
   "top": 270,
   "html": "TEKAN JE",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 14.27,
   "t1": 16.23
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@07",
     "t": 16.23
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@07%30",
     "t": 16.833
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@07%60",
     "t": 17.436
    }
   ],
   "t0": 16.23,
   "t1": 18.56
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
   "t0": 18.56,
   "t1": 22.76,
   "zt0": 18.56,
   "zt1": 20.319
  },
  {
   "type": "pill",
   "top": 250,
   "html": "250ml · BERHENTI SENDIRI",
   "bg": "#fff",
   "color": "var(--navy)",
   "t0": 20.124,
   "t1": 22.76
  },
  {
   "type": "card",
   "top": 760,
   "icon": "filter",
   "title": "PENAPIS NANOTRAP",
   "sub": "Teknologi penapisan Coway",
   "t0": 22.76,
   "t1": 25.12
  },
  {
   "type": "card",
   "top": 760,
   "icon": "baby",
   "icbg": "#fde8e4",
   "iccolor": "#E86E5A",
   "title": "SUHU AIR SUSU?",
   "sub": "Ikut nasihat doktor / pakar kanak-kanak",
   "t0": 25.12,
   "t1": 27.88
  },
  {
   "type": "pill",
   "top": 270,
   "html": "DARI RM27/BULAN*",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 27.88,
   "t1": 31.13
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 31.13,
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
   "t0": 31.13,
   "t1": null
  }
 ],
 "clips": {
  "bottles_busy": {
   "dir": "../../out/frames/NE05_bottles_busy/",
   "n": 94,
   "start": 0.0
  },
  "press_pour": {
   "dir": "../../out/frames/NE05_press_pour/",
   "n": 201,
   "start": 0.0
  },
  "bottle_to_baby": {
   "dir": "../../out/frames/NE05_bottle_to_baby/",
   "n": 84,
   "start": 7.2
  }
 }
};
