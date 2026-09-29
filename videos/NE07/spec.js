window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "pastel",
   "t1": 15.05
  },
  {
   "t0": 15.05,
   "bg": "pastel",
   "t1": 20.35
  },
  {
   "t0": 20.35,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 24.8
  },
  {
   "t0": 24.8,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 26.59
  },
  {
   "t0": 26.59,
   "bg": "blue",
   "t1": 32.93
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 200,
   "size": 110,
   "html": "KUIZ <span style='color:#E86E5A'>10 SAAT</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 0.29,
   "t1": 15.05
  },
  {
   "type": "pill",
   "top": 350,
   "html": "DAPUR ANDA WARNA APA?",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 1.52,
   "t1": 15.05
  },
  {
   "type": "quiz",
   "top": 500,
   "answer": [
    0,
    1,
    2,
    3,
    4
   ],
   "options": [
    {
     "text": "Pink lembut",
     "color": "#F3C9BD",
     "at": "@02",
     "t": 3.14
    },
    {
     "text": "Hijau mint",
     "color": "#C5DCCB",
     "at": "@03",
     "t": 4.65
    },
    {
     "text": "Biru langit",
     "color": "#BFD5E8",
     "at": "@04",
     "t": 6.21
    },
    {
     "text": "Kelabu gelap",
     "color": "#3a3d42",
     "at": "@05",
     "t": 7.87
    },
    {
     "text": "Putih bersih",
     "color": "#F4F3EF",
     "at": "@06",
     "t": 9.5
    }
   ],
   "t0": 1.766,
   "t1": 15.05,
   "answerT": 11.2
  },
  {
   "type": "stamp",
   "top": 1250,
   "html": "SEMUA BETUL!",
   "color": "#1faa59",
   "t0": 11.2,
   "t1": 15.05
  },
  {
   "type": "title",
   "top": 240,
   "size": 110,
   "html": "<span style='color:#E86E5A'>5</span> WARNA NEON",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 15.05,
   "t1": 20.35
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 15.05
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 16.012
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 16.974
    },
    {
     "unit": "gray",
     "zoom": 2.1,
     "t": 17.936
    },
    {
     "unit": "white",
     "zoom": 2.1,
     "t": 18.898
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 19.86
    }
   ],
   "t0": 15.05,
   "t1": 20.35
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "KOMPAK",
     "color": "#fff",
     "at": "@09",
     "t": 20.35
    },
    {
     "text": "3 SUHU",
     "color": "#fff",
     "at": "@09%40",
     "t": 21.95
    }
   ],
   "t0": 20.35,
   "t1": 24.8
  },
  {
   "type": "title",
   "top": 180,
   "size": 100,
   "html": "KOMEN<br><span style='color:#E86E5A'>A · B · C · D · E</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 24.8,
   "t1": 26.59
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 26.59,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "5 PILIHAN WARNA",
    "PEMASANGAN PERCUMA",
    "DARI RM27 SEBULAN*"
   ],
   "button": "WhatsApp saya",
   "fine": "*Diskaun 50% untuk 6 bulan pertama. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 26.59,
   "t1": null
  }
 ],
 "clips": {
  "presenter": {
   "dir": "../../out/frames/NE07_presenter/",
   "n": 101,
   "start": 6.4
  }
 }
};
