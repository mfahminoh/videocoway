window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "pastel",
   "t1": 6.5
  },
  {
   "t0": 6.5,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 7.72
  },
  {
   "t0": 7.72,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 5.3
   },
   "t1": 9.55
  },
  {
   "t0": 9.55,
   "bg": "navy",
   "t1": 15.54
  },
  {
   "t0": 15.54,
   "bg": {
    "clip": "bottle_to_baby",
    "c0": 7.2,
    "c1": 10.0
   },
   "t1": 17.6
  },
  {
   "t0": 17.6,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 19.87
  },
  {
   "t0": 19.87,
   "bg": "pastel",
   "t1": 22.52
  },
  {
   "t0": 22.52,
   "bg": "blue",
   "t1": 30.45
  },
  {
   "t0": 30.45,
   "bg": "blue",
   "t1": 36.03
  }
 ],
 "els": [
  {
   "type": "icon",
   "top": 420,
   "icon": "home",
   "color": "#E86E5A",
   "size": 240,
   "t0": 0.26,
   "t1": 6.5
  },
  {
   "type": "title",
   "top": 720,
   "size": 130,
   "html": "BARU KAHWIN?",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 0.26,
   "t1": 6.5
  },
  {
   "type": "pill",
   "top": 900,
   "html": "RUMAH PERTAMA",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 1.6,
   "t1": 6.5
  },
  {
   "type": "title",
   "top": 240,
   "size": 120,
   "html": "COWAY <span style='color:#E86E5A'>NEON</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 6.5,
   "t1": 7.72
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@04",
     "t": 7.72
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@04%25",
     "t": 8.115
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@04%55",
     "t": 8.589
    }
   ],
   "t0": 7.72,
   "t1": 9.55
  },
  {
   "type": "title",
   "top": 250,
   "size": 90,
   "html": "KAPASITI",
   "t0": 9.55,
   "t1": 15.54
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
     "t": 9.55
    },
    {
     "big": "1.5L",
     "small": "AIR SEJUK",
     "color": "#6cc2ff",
     "at": "@05%50",
     "t": 10.91
    },
    {
     "big": "∞",
     "small": "SUHU BILIK · TERUS",
     "color": "#e9eef5",
     "at": "@06",
     "t": 12.4
    }
   ],
   "t0": 9.55,
   "t1": 15.54
  },
  {
   "type": "pill",
   "top": 270,
   "html": "BERDUA → BERTIGA 👶",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 15.54,
   "t1": 17.6
  },
  {
   "type": "reason",
   "top": 250,
   "num": "✓",
   "title": "KOMPAK",
   "sub": "cantik di dapur rumah sewa",
   "t0": 17.6,
   "t1": 19.87
  },
  {
   "type": "title",
   "top": 240,
   "size": 120,
   "html": "<span style='color:#E86E5A'>5</span> WARNA",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 19.87,
   "t1": 22.52
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "all",
     "zoom": 1,
     "t": 19.87
    },
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 20.738
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 21.606
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 22.35
    }
   ],
   "t0": 19.87,
   "t1": 22.52
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 22.52,
   "t1": 30.45
  },
  {
   "type": "price",
   "top": 560,
   "label": "DARI",
   "from": "RM54",
   "badge": "DISKAUN 50% · 6 BULAN PERTAMA",
   "to": "RM27",
   "t0": 22.52,
   "t1": 30.45,
   "badgeT": 25.1,
   "strikeT": 27.445,
   "toT": 28.486
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 30.45,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PENGHANTARAN PERCUMA",
    "PEMASANGAN PERCUMA",
    "5 PILIHAN WARNA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Diskaun 50% untuk 6 bulan pertama. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 30.45,
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
 }
};
