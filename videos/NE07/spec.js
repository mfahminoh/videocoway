window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "pastel",
   "t1": 14.36
  },
  {
   "t0": 14.36,
   "bg": "pastel",
   "t1": 18.34
  },
  {
   "t0": 18.34,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 21.65
  },
  {
   "t0": 21.65,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 23.82
  },
  {
   "t0": 23.82,
   "bg": "blue",
   "t1": 33.61
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
   "t0": 0.21,
   "t1": 14.36
  },
  {
   "type": "pill",
   "top": 350,
   "html": "DAPUR ANDA WARNA APA?",
   "bg": "#0B2F6B",
   "color": "#fff",
   "t0": 1.5,
   "t1": 14.36
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
     "t": 3.19
    },
    {
     "text": "Hijau mint",
     "color": "#C5DCCB",
     "at": "@03",
     "t": 4.6
    },
    {
     "text": "Biru langit",
     "color": "#BFD5E8",
     "at": "@04",
     "t": 6.1
    },
    {
     "text": "Kelabu gelap",
     "color": "#3a3d42",
     "at": "@05",
     "t": 7.61
    },
    {
     "text": "Putih bersih",
     "color": "#F4F3EF",
     "at": "@06",
     "t": 9.13
    }
   ],
   "t0": 1.758,
   "t1": 14.36,
   "answerT": 10.69
  },
  {
   "type": "stamp",
   "top": 1250,
   "html": "SEMUA BETUL!",
   "color": "#1faa59",
   "t0": 10.69,
   "t1": 14.36
  },
  {
   "type": "title",
   "top": 240,
   "size": 110,
   "html": "<span style='color:#E86E5A'>5</span> WARNA NEON",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 14.36,
   "t1": 18.34
  },
  {
   "type": "lineup",
   "keys": [
    {
     "unit": "pink",
     "zoom": 2.1,
     "t": 14.36
    },
    {
     "unit": "mint",
     "zoom": 2.1,
     "t": 15.102
    },
    {
     "unit": "ciel",
     "zoom": 2.1,
     "t": 15.844
    },
    {
     "unit": "gray",
     "zoom": 2.1,
     "t": 16.586
    },
    {
     "unit": "white",
     "zoom": 2.1,
     "t": 17.328
    },
    {
     "unit": "all",
     "zoom": 1,
     "t": 18.07
    }
   ],
   "t0": 14.36,
   "t1": 18.34
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "KOMPAK",
     "color": "#fff",
     "at": "@09",
     "t": 18.34
    },
    {
     "text": "3 SUHU",
     "color": "#fff",
     "at": "@09%40",
     "t": 19.524
    }
   ],
   "t0": 18.34,
   "t1": 21.65
  },
  {
   "type": "title",
   "top": 180,
   "size": 100,
   "html": "KOMEN<br><span style='color:#E86E5A'>A · B · C · D · E</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 21.65,
   "t1": 23.82
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 23.82,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PROMOSI RM54 SEBULAN*",
    "+ REBAT RM20 × 7 BULAN*",
    "5 PILIHAN WARNA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM104/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 23.82,
   "t1": null
  }
 ],
 "clips": {
  "presenter": {
   "dir": "../../out/frames/NE07_presenter/",
   "n": 101,
   "start": 6.4
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably."
};
