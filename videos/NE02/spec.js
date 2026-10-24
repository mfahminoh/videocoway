window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "pastel",
   "t1": 5.58
  },
  {
   "t0": 5.58,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 7.54
  },
  {
   "t0": 7.54,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 5.3
   },
   "t1": 10.55
  },
  {
   "t0": 10.55,
   "bg": "navy",
   "t1": 17.27
  },
  {
   "t0": 17.27,
   "bg": {
    "clip": "bottle_to_baby",
    "c0": 7.2,
    "c1": 10.0
   },
   "t1": 19.88
  },
  {
   "t0": 19.88,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 22.44
  },
  {
   "t0": 22.44,
   "bg": "pastel",
   "t1": 25.0
  },
  {
   "t0": 25.0,
   "bg": "blue",
   "t1": 33.21
  },
  {
   "t0": 33.21,
   "bg": "blue",
   "t1": 38.64
  }
 ],
 "els": [
  {
   "type": "icon",
   "top": 420,
   "icon": "home",
   "color": "#E86E5A",
   "size": 240,
   "t0": 0.23,
   "t1": 5.58
  },
  {
   "type": "title",
   "top": 720,
   "size": 118,
   "html": "BARU KAHWIN?",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 0.23,
   "t1": 5.58
  },
  {
   "type": "pill",
   "top": 900,
   "html": "RUMAH PERTAMA",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 1.385,
   "t1": 5.58
  },
  {
   "type": "title",
   "top": 240,
   "size": 120,
   "html": "COWAY <span style='color:#E86E5A'>NEON</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 5.58,
   "t1": 7.54
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@04",
     "t": 7.54
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@04%25",
     "t": 8.193
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@04%55",
     "t": 8.976
    }
   ],
   "t0": 7.54,
   "t1": 10.55
  },
  {
   "type": "title",
   "top": 250,
   "size": 90,
   "html": "KAPASITI",
   "t0": 10.55,
   "t1": 17.27
  },
  {
   "type": "grid",
   "top": 440,
   "items": [
    {
     "big": "1L",
     "small": "AIR PANAS",
     "color": "#ff7a6b",
     "at": "@05",
     "t": 10.55
    },
    {
     "big": "1.5L",
     "small": "AIR SEJUK",
     "color": "#6cc2ff",
     "at": "@05%50",
     "t": 12.385
    },
    {
     "big": "∞",
     "small": "SUHU BILIK · TERUS",
     "color": "#e9eef5",
     "at": "@06",
     "t": 14.58
    }
   ],
   "t0": 10.55,
   "t1": 17.27
  },
  {
   "type": "pill",
   "top": 270,
   "html": "BERDUA → BERTIGA 👶",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 17.27,
   "t1": 19.88
  },
  {
   "type": "reason",
   "top": 250,
   "num": "✓",
   "title": "KOMPAK",
   "sub": "cantik di dapur rumah sewa",
   "t0": 19.88,
   "t1": 22.44
  },
  {
   "type": "title",
   "top": 240,
   "size": 120,
   "html": "<span style='color:#E86E5A'>5</span> WARNA",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 22.44,
   "t1": 25.0
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "all",
     "zoom": 1,
     "t": 22.44
    },
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 23.21
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 23.98
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 24.64
    }
   ],
   "t0": 22.44,
   "t1": 25.0
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 25.0,
   "t1": 33.21
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM104",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "to": "RM54",
   "t0": 25.0,
   "t1": 33.21,
   "badgeT": 29.34,
   "strikeT": 26.809,
   "toT": 27.412
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 33.21,
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
   "t0": 33.21,
   "t1": null
  }
 ],
 "clips": {
  "press_pour": {
   "dir": "../../out/frames/NE02_press_pour/",
   "n": 73,
   "start": 3.0
  },
  "bottle_to_baby": {
   "dir": "../../out/frames/NE02_bottle_to_baby/",
   "n": 84,
   "start": 7.2
  },
  "presenter": {
   "dir": "../../out/frames/NE02_presenter/",
   "n": 101,
   "start": 6.4
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably."
};
