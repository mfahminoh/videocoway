window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "dark",
   "t1": 17.38
  },
  {
   "t0": 17.38,
   "bg": {
    "clip": "clip4",
    "c0": 6.0,
    "c1": 10.0
   },
   "t1": 21.12
  },
  {
   "t0": 21.12,
   "bg": {
    "clip": "clip5",
    "c0": 6.3,
    "c1": 9.5
   },
   "t1": 25.39
  },
  {
   "t0": 25.39,
   "bg": {
    "clip": "clip5",
    "c0": 0.3,
    "c1": 4.2
   },
   "t1": 29.45
  },
  {
   "t0": 29.45,
   "bg": "blue",
   "t1": 36.96
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 240,
   "size": 110,
   "html": "<span style='color:var(--yellow)'>8 SUHU</span><br>UNTUK APA?",
   "t0": 0.09,
   "t1": 4.16
  },
  {
   "type": "led",
   "top": 560,
   "items": [
    {
     "num": "8",
     "unit": "",
     "label": "PILIHAN SUHU",
     "at": "@01%40",
     "t": 1.554
    },
    {
     "num": "95",
     "label": "MI SEGERA",
     "at": "@02",
     "t": 4.16
    },
    {
     "num": "80",
     "label": "KOPI",
     "at": "@03",
     "t": 7.34
    },
    {
     "num": "70",
     "label": "TEH",
     "at": "@04",
     "t": 8.94
    },
    {
     "num": "40",
     "label": "SUSU BABY",
     "at": "@05%20",
     "t": 11.902
    },
    {
     "num": "50",
     "label": "AIR MINUM",
     "at": "@05%52",
     "t": 13.921
    },
    {
     "num": "60",
     "label": "RENDAM BIHUN",
     "at": "@05%78",
     "t": 15.562
    }
   ],
   "t0": 1.554,
   "t1": 17.38
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@06",
     "t": 17.38
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@06%50",
     "t": 19.11
    }
   ],
   "t0": 17.38,
   "t1": 21.12
  },
  {
   "type": "pill",
   "top": 270,
   "html": "120ml → TANPA HAD",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 21.12,
   "t1": 25.39
  },
  {
   "type": "pill",
   "top": 1250,
   "html": "SATU MESIN · 11.4L",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 25.39,
   "t1": 29.45
  },
  {
   "type": "price",
   "top": 380,
   "label": "HARGA ASAL",
   "from": "RM120",
   "to": "RM74",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "t0": 29.45,
   "t1": null,
   "badgeT": 31.614,
   "strikeT": 29.931,
   "toT": 30.508
  },
  {
   "type": "cta",
   "top": 1300,
   "ticks": [],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM120/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 33.057,
   "t1": null
  }
 ],
 "clips": {
  "clip4": {
   "dir": "../../out/frames/V305_clip4/",
   "n": 120,
   "start": 6.0
  },
  "clip5": {
   "dir": "../../out/frames/V305_clip5/",
   "n": 281,
   "start": 0.3
  }
 }
};
