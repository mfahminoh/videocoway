window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 4.45
  },
  {
   "t0": 4.45,
   "bg": "navy",
   "t1": 6.35
  },
  {
   "t0": 6.35,
   "bg": "pastel",
   "t1": 8.81
  },
  {
   "t0": 8.81,
   "bg": "navy",
   "t1": 12.9
  },
  {
   "t0": 12.9,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 16.7
  },
  {
   "t0": 16.7,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 19.68
  },
  {
   "t0": 19.68,
   "bg": "navy",
   "t1": 23.31
  },
  {
   "t0": 23.31,
   "bg": "blue",
   "t1": 29.13
  },
  {
   "t0": 29.13,
   "bg": "blue",
   "t1": 33.37
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 520,
   "size": 100,
   "html": "PROSES PASANG<br><span style='color:var(--yellow)'>COWAY NEON</span>",
   "t0": 0.25,
   "t1": 4.45
  },
  {
   "type": "pill",
   "top": 820,
   "html": "4 LANGKAH",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 2.225,
   "t1": 4.45
  },
  {
   "type": "reason",
   "top": 360,
   "num": "1",
   "title": "WHATSAPP SAYA",
   "t0": 4.45,
   "t1": 6.35
  },
  {
   "type": "icon",
   "top": 700,
   "icon": "phone",
   "size": 300,
   "color": "#25D366",
   "t0": 4.772,
   "t1": 6.35
  },
  {
   "type": "pill",
   "top": 250,
   "html": "2 · PILIH WARNA",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 6.35,
   "t1": 8.81
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "all",
     "zoom": 1,
     "t": 6.35
    },
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 7.29
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 8.112
    }
   ],
   "t0": 6.35,
   "t1": 8.81
  },
  {
   "type": "reason",
   "top": 250,
   "num": "3",
   "title": "PILIH PAKEJ",
   "t0": 8.81,
   "t1": 12.9
  },
  {
   "type": "card",
   "top": 640,
   "icon": "tech",
   "title": "BESERTA SERVIS",
   "sub": "Technician datang servis",
   "t0": 9.953,
   "t1": 12.9
  },
  {
   "type": "card",
   "top": 950,
   "icon": "box",
   "icbg": "#fff3cc",
   "iccolor": "#b07b00",
   "title": "SELF-SERVICE",
   "sub": "Tukar filter sendiri",
   "t0": 11.096,
   "t1": 12.9
  },
  {
   "type": "pill",
   "top": 270,
   "html": "4 · PEMASANGAN PERCUMA",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 12.9,
   "t1": 16.7
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@06%40",
     "t": 17.808
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@06%60",
     "t": 18.362
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@06%80",
     "t": 18.916
    }
   ],
   "t0": 16.7,
   "t1": 19.68
  },
  {
   "type": "title",
   "top": 250,
   "size": 80,
   "html": "SELF-SERVICE:<br>FILTER TIAP <span style='color:var(--yellow)'>8 BULAN</span>",
   "t0": 19.68,
   "t1": 23.31
  },
  {
   "type": "delivery",
   "top": 620,
   "t0": 19.68,
   "t1": 23.31
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 23.31,
   "t1": 29.13
  },
  {
   "type": "price",
   "top": 560,
   "label": "DARI",
   "from": "RM54",
   "badge": "DISKAUN 50% · 6 BULAN PERTAMA",
   "to": "RM27",
   "t0": 23.31,
   "t1": 29.13,
   "badgeT": 25.48,
   "strikeT": 27.028,
   "toT": 27.716
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 29.13,
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
   "t0": 29.13,
   "t1": null,
   "btnT": 29.592
  }
 ],
 "clips": {
  "presenter": {
   "dir": "../../out/frames/NE10_presenter/",
   "n": 101,
   "start": 6.4
  },
  "press_pour": {
   "dir": "../../out/frames/NE10_press_pour/",
   "n": 111,
   "start": 3.0
  }
 }
};
