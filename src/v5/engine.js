/* Enjin animasi dikongsi untuk 5 video gaya (src/v5/*.html).
   - .scene[data-s][data-e]      : babak dengan masa mula/tamat (saat)
   - [data-in][data-a]           : elemen masuk pada masa relatif babak (up|pop|slam|stamp|left|right|fade|zoom)
   - .strike[data-in]            : garis potong;  [data-grow="t0,t1"] : bar memanjang
   - [data-count="a,b,t0,t1"]    : nombor berubah
   - addEndcard(start)           : kad promo + CTA dikongsi (17.8s), warna ikut pemboleh ubah CSS tema
   Setiap halaman memanggil Engine.init({ duration, hooks(t) }).                                       */
(function () {
  const $ = id => document.getElementById(id);
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const E = {
    lin: x => x, out: x => 1 - Math.pow(1 - x, 3), in: x => x * x * x,
    inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    back: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  };
  const p = (t, t0, t1, e = E.out) => e(clamp((t - t0) / (t1 - t0)));
  const mix = (a, b, k) => a + (b - a) * k;
  function tf(el, { o = 1, x = 0, y = 0, s = 1, r = 0, blur = 0 }) {
    el.style.opacity = o;
    el.style.visibility = o <= .001 ? 'hidden' : 'visible';
    el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
    el.style.filter = blur > .05 ? `blur(${blur}px)` : '';
  }
  function animItem(n, a, k) {
    if (k < 0) return tf(n, { o: 0 });
    const fi = clamp(k / .22);
    const q = p(k, 0, .5, a === 'pop' || a === 'stamp' ? E.back : E.out);
    switch (a) {
      case 'pop': return tf(n, { o: fi, s: mix(.5, 1, q) });
      case 'slam': return tf(n, { o: fi, s: mix(1.7, 1, p(k, 0, .4)), blur: (1 - clamp(k / .28)) * 10 });
      case 'stamp': return tf(n, { o: fi, s: mix(2.2, 1, q), r: mix(-14, 0, q) });
      case 'left': return tf(n, { o: fi, x: mix(140, 0, q), blur: (1 - clamp(k / .35)) * 8 });
      case 'right': return tf(n, { o: fi, x: mix(-140, 0, q), blur: (1 - clamp(k / .35)) * 8 });
      case 'fade': return tf(n, { o: p(k, 0, .6, E.inOut) });
      case 'zoom': return tf(n, { o: fi, s: mix(.85, 1, p(k, 0, .8)) });
      case 'cut': return tf(n, { o: 1 });
      default: return tf(n, { o: fi, y: mix(60, 0, q), blur: (1 - clamp(k / .35)) * 8 });
    }
  }

  const WA = '<svg width="60" height="60" viewBox="0 0 24 24" style="flex:none"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2s.2-1.1.1-1.2-.2-.2-.5-.3z"/></svg>';

  /* Kad promo + CTA. Masa dalam babak selari dengan petikan VO Gemini (lihat build_v5.py ENDCARD_VO). */
  function addEndcard(S, opts = {}) {
    const stage = $('stage');
    const tag = opts.tag || 'PROMO';
    const line = opts.line || ['Beli sekali. Pakai lama.', 'Puas hati.'];
    stage.insertAdjacentHTML('beforeend', `
    <div class="layer" id="ecBg" style="background:var(--ec-bg)"></div>
    <div class="scene" id="ecPromo" data-s="${S}" data-e="${S + 11.1}" style="color:var(--ec-text)">
      <div class="el c" style="top:250px"><span id="ecPill" data-in=".15" data-a="pop" style="display:inline-block; background:var(--ec-accent); color:var(--ec-on-accent); font-weight:800; letter-spacing:4px; font-size:40px; padding:16px 44px; border-radius:60px">${tag}</span></div>
      <div class="el c" style="top:370px; font-size:48px; font-weight:500; opacity:.8" data-in=".35" data-a="up">Harga asal</div>
      <div class="el c" style="top:425px; font-size:96px; font-weight:700; opacity:.7" data-in=".45" data-a="up">
        <span style="position:relative">RM120<span style="font-size:48px">/bulan</span><i class="strike" data-in="1.1" style="background:var(--ec-red)"></i></span></div>
      <div class="el c" style="top:580px; font-size:50px; font-weight:600" data-in="1.2" data-a="up">Promosi diskaun · <span style="color:var(--ec-accent-text)">serendah</span></div>
      <div class="el c" style="top:630px; white-space:nowrap; line-height:1.1" data-in="2.3" data-a="slam">
        <span style="font-size:220px; font-weight:800; color:var(--ec-price)">RM<span data-count="120,74,2.4,3.9">120</span></span><span style="font-size:64px; font-weight:600; opacity:.9">/bulan</span></div>
      <div class="el" style="top:915px; left:170px" data-in="5.0" data-a="stamp">
        <span style="display:inline-block; background:var(--ec-red); color:#fff; font-weight:800; font-size:44px; letter-spacing:3px; padding:14px 36px; border-radius:60px; transform:rotate(-4deg)">GANDA LAGI!</span></div>
      <div class="el" style="top:990px; left:110px; width:860px; height:220px; border-radius:36px; background:var(--ec-card); border:3px solid var(--ec-accent); text-align:center; padding-top:26px" data-in="5.6" data-a="pop">
        <div style="font-size:40px; font-weight:600">Rebat Ulang Tahun Coway</div>
        <div style="font-size:104px; font-weight:800; color:var(--ec-accent-text); line-height:1.1">RM20 × 7 BULAN</div></div>
      <div class="el c" style="top:1225px; font-size:32px; font-weight:500; opacity:.75" data-in="8.4" data-a="up">Selepas 7 bulan: RM74/bulan</div>
      <div class="el ecchk" style="top:1285px; left:190px" data-in="8.9" data-a="left"><span class="ectick">✓</span>Pemasangan <b style="color:var(--ec-accent-text)">&nbsp;PERCUMA</b></div>
      <div class="el ecchk" style="top:1370px; left:190px" data-in="9.4" data-a="left"><span class="ectick">✓</span>Servis setiap 2 / 4 bulan</div>
      <div class="el c" style="top:1465px" data-in="10.1" data-a="slam" id="ecLast">
        <span style="display:inline-block; background:var(--ec-red); color:#fff; font-size:50px; font-weight:800; padding:14px 50px; border-radius:16px">LAST CALL untuk promo ini!</span></div>
      <div class="el c" style="top:1575px; font-size:26px; opacity:.55" data-in="10.3" data-a="fade">*Tertakluk kepada terma &amp; syarat</div>
    </div>
    <div class="scene" id="ecCta" data-s="${S + 11.2}" data-e="9999" style="color:var(--ec-text)">
      <div class="el" id="ecImg" style="top:170px; left:0; width:1080px; height:925px; -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 12%, #000 80%, transparent 100%);" data-in=".1" data-a="fade">
        <img src="../../assets/img/two-colors.jpg" style="width:1080px; height:925px; display:block; ${opts.imgStyle || ''}"></div>
      <div class="el c fit" style="top:1060px; font-size:84px; font-weight:800; line-height:1.15; white-space:nowrap" data-in=".5" data-a="slam">${line[0]}</div>
      <div class="el c fit" style="top:1160px; font-size:100px; font-weight:800; color:var(--ec-accent-text); white-space:nowrap" data-in="1.0" data-a="slam">${line[1]}</div>
      <div class="el c" style="top:1310px; font-size:44px; font-weight:500; opacity:.9" data-in="1.6" data-a="up">${opts.ask || 'Cari penapis air <b>high spec</b>?'}</div>
      <div class="el" id="ecBtn" style="top:1390px; left:110px; width:860px; height:140px; border-radius:80px; background:#25D366; display:flex !important; align-items:center; justify-content:center; gap:22px; font-size:44px; font-weight:800; color:#fff; white-space:nowrap; box-shadow:0 20px 50px rgba(37,211,102,.45)" data-in="2.0" data-a="pop">${WA} WHATSAPP SAYA SEKARANG</div>
      <div class="el c" style="top:1570px; font-size:32px; font-weight:500; opacity:.7; letter-spacing:2px" data-in="2.6" data-a="fade">COWAY VILLAEM 3 · Pebble Grey | Porcelain White</div>
    </div>`);
    return S;
  }

  /* kecilkan saiz font sehingga kandungan muat dalam maxW piksel */
  function fit(sel, maxW = 980) {
    document.querySelectorAll(sel).forEach(el => {
      const r = document.createRange();
      let fs = parseFloat(getComputedStyle(el).fontSize);
      for (let i = 0; i < 40; i++) {
        r.selectNodeContents(el);
        if (r.getBoundingClientRect().width <= maxW) break;
        fs *= 0.95; el.style.fontSize = fs + 'px';
      }
    });
  }

  let scenes = [], cfg = {};
  function init(c) {
    cfg = c;
    fit('.fit', c.fitW || 980);
    window.DURATION = c.duration;
    scenes = [...document.querySelectorAll('.scene')].map(el => ({
      el, s: +el.dataset.s, e: +el.dataset.e,
      items: [...el.querySelectorAll('[data-in]')].map(n => ({ n, t: +n.dataset.in, a: n.dataset.a || 'up' })),
      strikes: [...el.querySelectorAll('.strike')],
      grows: [...el.querySelectorAll('[data-grow]')].map(n => ({ n, r: n.dataset.grow.split(',').map(Number) })),
      counts: [...el.querySelectorAll('[data-count]')].map(n => ({ n, r: n.dataset.count.split(',').map(Number) })),
    }));
    window.seek = seek;
    seek(0);
  }
  function seek(t) {
    const ecS = cfg.endcard;
    if (ecS != null) {
      const bg = $('ecBg');
      if (cfg.endWipe === 'up') { const w = p(t, ecS - .3, ecS + .15, E.inOut); bg.style.clipPath = `inset(${(1 - w) * 100}% 0 0 0)`; tf(bg, { o: t >= ecS - .3 ? 1 : 0 }); }
      else tf(bg, { o: p(t, ecS - .3, ecS + .1, E.inOut) });
    }
    scenes.forEach(sc => {
      const vis = t >= sc.s - .01 && t < sc.e + .45;
      sc.el.style.display = vis ? '' : 'none';
      if (!vis) return;
      const k = t - sc.s, out = sc.el.dataset.cut ? (t >= sc.e ? 1 : 0) : p(t, sc.e - .05, sc.e + .35, E.in);
      tf(sc.el, { o: 1 - out, y: sc.el.dataset.cut ? 0 : -out * 70, blur: sc.el.dataset.cut ? 0 : out * 8 });
      sc.items.forEach(it => animItem(it.n, it.a, k - it.t));
      sc.strikes.forEach(st => { st.style.transform = `scaleX(${p(k, +st.dataset.in, +st.dataset.in + .35, E.inOut)})`; st.style.opacity = 1; st.style.filter = ''; st.style.visibility = 'visible'; });
      sc.grows.forEach(g => { g.n.style.transform = `scaleX(${p(k, g.r[0], g.r[1], E.inOut)})`; g.n.style.opacity = 1; g.n.style.visibility = 'visible'; g.n.style.filter = ''; });
      sc.counts.forEach(c => { c.n.textContent = Math.round(mix(c.r[0], c.r[1], p(k, c.r[2], c.r[3], E.inOut))); c.n.style.opacity = 1; c.n.style.transform = ''; c.n.style.filter = ''; c.n.style.visibility = 'visible'; });
    });
    if (ecS != null) {
      if (t > ecS + .7 && t < ecS + 11.2) $('ecPill').style.transform += ` rotate(${Math.sin(t * 9) * 2.5}deg)`;
      if (t > ecS + 10.6 && t < ecS + 11.2) $('ecLast').style.transform += ` scale(${1 + .05 * Math.max(0, Math.sin((t - ecS - 10.6) * 8))})`;
      if (t > ecS + 13.8) $('ecBtn').style.transform += ` scale(${1 + .04 * Math.max(0, Math.sin((t - ecS - 13.8) * 6))})`;
      if (t > ecS + 11.2) $('ecImg').style.transform += ` scale(${mix(1.1, 1, p(t, ecS + 11.2, cfg.duration, E.out))})`;
    }
    if (cfg.hooks) cfg.hooks(t);
  }
  window.Engine = { init, addEndcard, fit, tf, p, mix, clamp, E, $ };
})();
