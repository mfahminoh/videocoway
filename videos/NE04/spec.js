window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 8.98
  },
  {
   "t0": 8.98,
   "bg": "blue",
   "t1": 14.91
  },
  {
   "t0": 14.91,
   "bg": "navy",
   "t1": 20.56
  },
  {
   "t0": 20.56,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 24.64
  },
  {
   "t0": 24.64,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 28.18
  },
  {
   "t0": 28.18,
   "bg": "blue",
   "t1": 33.4
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 300,
   "size": 130,
   "html": "BERAPA<br><span style='color:var(--yellow)'>SEHARI?</span>",
   "t0": 0.25,
   "t1": 3.57
  },
  {
   "type": "photo",
   "top": 760,
   "left": 310,
   "w": 460,
   "h": 460,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 1.398,
   "t1": 3.57
  },
  {
   "type": "title",
   "top": 380,
   "size": 70,
   "html": "BULANAN",
   "t0": 3.57,
   "t1": 8.98
  },
  {
   "type": "counter",
   "top": 470,
   "from": 0,
   "to": 54,
   "prefix": "RM",
   "dur": 0.7,
   "t0": 3.57,
   "t1": 5.76
  },
  {
   "type": "text",
   "top": 760,
   "size": 60,
   "weight": 800,
   "html": "÷ 30 hari",
   "t0": 5.76,
   "t1": 8.98
  },
  {
   "type": "counter",
   "top": 860,
   "from": 54,
   "to": 1.8,
   "prefix": "RM",
   "decimals": 2,
   "dur": 0.8,
   "color": "#fff",
   "t0": 6.66,
   "t1": 8.98
  },
  {
   "type": "price",
   "top": 420,
   "label": "DARI",
   "from": "RM54",
   "badge": "DISKAUN 50% · 6 BULAN PERTAMA",
   "to": "RM27",
   "t0": 8.98,
   "t1": 14.91,
   "badgeT": 9.964,
   "strikeT": 12.52,
   "toT": 13.129
  },
  {
   "type": "title",
   "top": 380,
   "size": 80,
   "html": "SEHARI",
   "t0": 14.91,
   "t1": 18.56
  },
  {
   "type": "counter",
   "top": 480,
   "from": 1.8,
   "to": 0.9,
   "prefix": "RM",
   "decimals": 2,
   "dur": 0.8,
   "t0": 14.91,
   "t1": 18.56
  },
  {
   "type": "stamp",
   "top": 820,
   "html": "BAWAH RM1!",
   "t0": 17.01,
   "t1": 18.56
  },
  {
   "type": "icon",
   "top": 420,
   "icon": "cup",
   "size": 300,
   "color": "#fff",
   "t0": 18.56,
   "t1": 20.56
  },
  {
   "type": "title",
   "top": 800,
   "size": 76,
   "html": "LEBIH MURAH DARI<br><span style='color:var(--yellow)'>SECAWAN TEH TARIK</span>",
   "t0": 18.56,
   "t1": 20.56
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@08%30",
     "t": 21.712
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@08%55",
     "t": 22.672
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@08%75",
     "t": 23.44
    }
   ],
   "t0": 20.56,
   "t1": 24.64
  },
  {
   "type": "pill",
   "top": 270,
   "html": "NANOTRAP · PEMASANGAN PERCUMA",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 24.64,
   "t1": 28.18
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 28.18,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "RM27/BULAN* = RM0.90 SEHARI",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Diskaun 50% untuk 6 bulan pertama. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 28.18,
   "t1": null,
   "btnT": 29.692
  }
 ],
 "clips": {
  "press_pour": {
   "dir": "../../out/frames/NE04_press_pour/",
   "n": 111,
   "start": 3.0
  },
  "presenter": {
   "dir": "../../out/frames/NE04_presenter/",
   "n": 101,
   "start": 6.4
  }
 }
};
