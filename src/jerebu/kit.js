/* Kit dikongsi pakej Jerebu (src/jerebu/*.html). Bergantung pada ../v5/engine.js.
   - Masa babak datang dari timing/<nama>.js (dijana build_jerebu.py ikut panjang VO):
       window.TIMING = { scenes: [[s, e, voStart, voDur], ...], duration }
     Babak .scene diberi data-s/data-e ikut turutan. data-in boleh guna "%" = peratus tempoh VO babak
     (cth. data-in="45%" muncul lebih kurang bila VO sampai 45% ayat) — jadi animasi ikut suara.
   - K.haze(ctx, t, opt)    : zarah jerebu (drift | suck | leak | clean), deterministik ikut t
   - K.ring(level)           : warna penunjuk kualiti udara 0 merah · 1 kuning · 2 hijau · 3 biru
   - K.cta(opts)             : babak CTA WhatsApp (guna sebagai babak terakhir)                     */
(function () {
  const { p, mix, clamp, E } = Engine;
  const K = {};
  const T = window.TIMING || { scenes: [], duration: 30 };
  K.T = T;

  K.applyTiming = function () {
    const scenes = [...document.querySelectorAll('.scene')];
    scenes.forEach((el, i) => {
      const s = T.scenes[i] || [i * 5, i * 5 + 5, 0, 4];
      el.dataset.s = s[0]; el.dataset.e = i === scenes.length - 1 ? 9999 : s[1];
      el.querySelectorAll('[data-in]').forEach(n => {
        const v = n.dataset.in;
        if (v.endsWith('%')) n.dataset.in = (s[2] - s[0] + s[3] * parseFloat(v) / 100).toFixed(3);
      });
      el.querySelectorAll('[data-at]').forEach(n => {   // data-at="a%,b%" -> masa mutlak untuk hooks
        n._at = n.dataset.at.split(',').map(v => s[0] + (v.endsWith('%') ? s[2] - s[0] + s[3] * parseFloat(v) / 100 : +v));
      });
    });
  };
  K.scene = i => { const s = T.scenes[i]; return { s: s[0], e: s[1], vo: s[2], d: s[3] }; };
  K.at = (i, frac) => { const s = T.scenes[i]; return s[2] + s[3] * frac; };   // masa mutlak pada % VO babak i

  /* ---------- zarah ---------- */
  function rnd(i, k) { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  K.haze = function (ctx, t, o) {
    const n = Math.round((o.n || 300) * clamp(o.density == null ? 1 : o.density));
    const [W, H] = [ctx.canvas.width, ctx.canvas.height];
    const col = o.color || '120,100,80';
    for (let i = 0; i < n; i++) {
      const sz = (o.size || 4) * (.4 + 1.2 * rnd(i, 3));
      let x, y, a = (o.alpha || .55) * (.35 + .65 * rnd(i, 4));
      if (o.mode === 'suck' || o.mode === 'leak' || o.mode === 'clean') {
        const per = o.period || 2.4, ph = rnd(i, 5);
        const k = ((t / per + ph) % 1 + 1) % 1;
        const src = o.mode === 'suck'
          ? { x: (o.box ? o.box[0] + rnd(i, 1) * o.box[2] : rnd(i, 1) * W), y: (o.box ? o.box[1] + rnd(i, 2) * o.box[3] : rnd(i, 2) * H) }
          : { x: o.x, y: o.y };
        let dst;
        if (o.mode === 'suck') dst = { x: o.x + (rnd(i, 6) - .5) * (o.spread || 60), y: o.y + (rnd(i, 7) - .5) * (o.spread || 60) };
        else { const ang = (o.angle || 0) + (rnd(i, 6) - .5) * (o.cone || 1.2); const L = (o.reach || 600) * (.4 + .6 * rnd(i, 7));
               dst = { x: o.x + Math.cos(ang) * L, y: o.y + Math.sin(ang) * L }; }
        const e = o.mode === 'suck' ? E.in(k) : E.out(k);
        x = mix(src.x, dst.x, e) + Math.sin(t * 2 + i) * 6 * (1 - k);
        y = mix(src.y, dst.y, e) + Math.cos(t * 1.7 + i) * 6 * (1 - k);
        a *= o.mode === 'suck' ? Math.min(1, k * 4) * (1 - Math.pow(k, 6)) : Math.min(1, k * 6) * (1 - k);
      } else {
        const vx = (rnd(i, 6) - .3) * (o.speed || 18), vy = (rnd(i, 7) - .5) * (o.speed || 18) * .6;
        x = ((rnd(i, 1) * W + vx * t + Math.sin(t * .7 + i) * 14) % W + W) % W;
        y = ((rnd(i, 2) * H + vy * t + Math.cos(t * .5 + i) * 14) % H + H) % H;
      }
      ctx.fillStyle = `rgba(${o.mode === 'clean' ? (o.color || '150,220,255') : col},${a})`;
      ctx.beginPath(); ctx.arc(x, y, sz, 0, 6.283); ctx.fill();
    }
  };
  K.clear = ctx => ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  /* ---------- penunjuk kualiti udara ---------- */
  const RING = [[229, 50, 45], [245, 190, 30], [60, 190, 90], [40, 150, 255]];
  K.ring = function (level) {      // level 0..3 boleh pecahan (peralihan lembut)
    const l = clamp(level, 0, 3), i = Math.min(2, Math.floor(l)), f = l - i;
    const c = RING[i].map((v, k) => Math.round(mix(v, RING[i + 1][k], f)));
    return `rgb(${c.join(',')})`;
  };
  K.ringName = l => ['MERAH · KOTOR', 'KUNING · SEDERHANA', 'HIJAU · BAIK', 'BIRU · BERSIH'][Math.round(clamp(l, 0, 3))];

  /* Storm II dengan cincin penunjuk yang boleh diwarnakan. size = lebar px. */
  K.storm = function (id, x, y, size, attrs = '') {
    const s = size / 450;
    return `<div class="el" id="${id}" style="top:${y}px; left:${x}px; width:${size}px; height:${740 * s}px" ${attrs}>
      <img src="../../assets/img/air/storm2-neutral.png" style="position:absolute; inset:0; width:100%; height:100%">
      <div class="glow" style="position:absolute; inset:0; background:#2896ff; -webkit-mask-image:url(../../assets/img/air/storm2-glow.png); -webkit-mask-size:100% 100%"></div>
      <div class="halo" style="position:absolute; left:${(230 - 110) * s}px; top:${(157 - 110) * s}px; width:${220 * s}px; height:${220 * s}px; border-radius:50%; background:radial-gradient(circle, transparent 36%, rgba(40,150,255,.6) 47%, transparent 66%)"></div>
    </div>`;
  };
  K.setStorm = function (id, level) {
    const el = document.getElementById(id); if (!el) return;
    const c = K.ring(level);
    el.querySelector('.glow').style.background = c;
    el.querySelector('.halo').style.background = `radial-gradient(circle, transparent 36%, ${c.replace('rgb', 'rgba').replace(')', ',.7)')} 47%, transparent 66%)`;
  };

  /* ---------- CTA ---------- */
  const WA = '<svg width="60" height="60" viewBox="0 0 24 24" style="flex:none"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2s.2-1.1.1-1.2-.2-.2-.5-.3z"/></svg>';
  K.WA = WA;
  /* Kad CTA + promosi semua penapis udara: RM20/bulan untuk 7 bulan pertama. Masa elemen ikut VO babak (%). */
  K.cta = function (o = {}) {
    const imgs = o.imgs || ['storm2.png'];
    const w = imgs.length === 1 ? 360 : 260, gap = imgs.length === 1 ? 0 : 20;
    const x0 = (1080 - (imgs.length * w + (imgs.length - 1) * gap)) / 2;
    const prods = imgs.map((f, i) => `<img class="el" src="../../assets/img/air/${f}" style="top:${o.imgTop || 150}px; left:${x0 + i * (w + gap)}px; width:${w}px; height:${w * 740 / 450}px; filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))" data-in="${.1 + i * .12}" data-a="zoom">`).join('');
    const y = (imgs.length === 1 ? 150 + 360 * 740 / 450 : 150 + 260 * 740 / 450) + 40;
    return `<div class="scene cta" style="color:var(--cta-text, #fff)">
      ${prods}
      ${o.extra || ''}
      <div class="el c" style="top:${y}px" data-in="0%" data-a="pop"><span style="display:inline-block; background:#E5322D; color:#fff; font-weight:800; letter-spacing:3px; font-size:36px; padding:12px 36px; border-radius:50px">PROMOSI SEMUA AIR PURIFIER</span></div>
      <div class="el c" style="top:${y + 80}px; white-space:nowrap; line-height:1" data-in="12%" data-a="slam"><span style="font-family:Anton; font-size:230px; color:var(--accent)">RM20</span><span style="font-size:64px; font-weight:800">/bulan</span></div>
      <div class="el c" style="top:${y + 320}px; font-size:50px; font-weight:700" data-in="22%" data-a="up">untuk <span style="color:var(--accent)">7 bulan pertama</span></div>
      <div class="el c" style="top:${y + 410}px" data-in="${o.stampAt || '45%'}" data-a="stamp"><span style="display:inline-block; background:#FFD23F; color:#111; font-weight:800; font-size:54px; padding:12px 40px; border-radius:18px; transform:rotate(-3deg)">RM20 dah boleh pasang!</span></div>
      <div class="el c fit" style="top:${y + 540}px; font-size:52px; font-weight:800; white-space:nowrap" data-in="62%" data-a="up">${o.h1 || 'Udara bersih untuk keluarga.'}</div>
      <div class="el" id="ctaBtn" style="top:${y + 630}px; left:110px; width:860px; height:130px; border-radius:80px; background:#25D366; display:flex !important; align-items:center; justify-content:center; gap:22px; font-size:46px; font-weight:800; color:#fff; white-space:nowrap; box-shadow:0 20px 50px rgba(37,211,102,.45)" data-in="${o.btnAt || '75%'}" data-a="pop">${WA} ${o.btn || 'WHATSAPP SAYA SEKARANG'}</div>
      <div class="el c" style="top:${y + 790}px; font-size:24px; opacity:.65; line-height:1.4; padding:0 70px" data-in="30%" data-a="fade">${o.fine || '*Promosi semua penapis udara Coway: RM20/bulan untuk 7 bulan pertama, kemudian harga sewa biasa (dari RM49/bulan, pelan 7 tahun; penapis ganti termasuk). Tertakluk terma &amp; syarat.'}</div>
    </div>`;
  };

  /* Foto realistik penuh skrin (Seedream) dengan zum perlahan (Ken Burns) dan bayang untuk teks. */
  const SHADE = 'linear-gradient(180deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,.18) 32%, rgba(0,0,0,.22) 58%, rgba(0,0,0,.78) 100%)';
  K.photo = function (file, o = {}) {
    return `<div class="el photo" style="left:0; top:0; width:1080px; height:1920px; overflow:hidden; z-index:-1" data-in="${o.in || 0}" data-a="${o.a || 'fade'}" ${o.id ? `id="${o.id}"` : ''}>
      <img class="kb" src="../../assets/generated/${file}" style="width:100%; height:100%; object-fit:cover; object-position:${o.pos || '50% 50%'}" data-kb="${o.kb || 'in'}">
      <div style="position:absolute; inset:0; background:${o.shade || SHADE}"></div></div>`;
  };
  /* Foto dalam kad bersudut bulat (untuk tema cerah) */
  K.card = function (file, x, y, w, h, o = {}) {
    return `<div class="el" style="left:${x}px; top:${y}px; width:${w}px; height:${h}px; border-radius:36px; overflow:hidden; box-shadow:0 24px 50px rgba(0,0,0,.18)" data-in="${o.in || 0}" data-a="${o.a || 'zoom'}">
      <img class="kb" src="../../assets/generated/${file}" style="width:100%; height:100%; object-fit:cover; object-position:${o.pos || '50% 50%'}" data-kb="in"></div>`;
  };
  K.kenBurns = function (t) {
    document.querySelectorAll('img.kb').forEach(im => {
      const sc = im.closest('.scene'); if (!sc || sc.style.display === 'none') return;
      const k = Engine.clamp((t - +sc.dataset.s) / Math.max(1, Math.min(9999, +sc.dataset.e) - +sc.dataset.s));
      const z = im.dataset.kb === 'out' ? 1.12 - .08 * k : 1.04 + .08 * k;
      im.style.transform = `scale(${z})`;
    });
  };
  K.ctaPulse = function (t) {
    const b = document.getElementById('ctaBtn'); if (!b) return;
    const s = T.scenes[T.scenes.length - 1][0];
    const t0 = +b.dataset.in + s + .6; if (t > t0) b.style.transform += ` scale(${1 + .045 * Math.max(0, Math.sin((t - t0) * 5))})`;
  };

  /* Panggil selepas HTML siap: susun masa + mula enjin */
  K.start = function (hooks, extra = {}) {
    K.applyTiming();
    Engine.init(Object.assign({ duration: T.duration, hooks: t => { hooks && hooks(t); K.kenBurns(t); K.ctaPulse(t); } }, extra));
  };
  window.K = K;
})();
