/* Pemain "mg": motion graphic bergaya (15 gaya mg-styles-15), satu halaman ditulis tangan bagi setiap video.
   Muat selepas timing.js dan engine.js; halaman videos/<ID>/index.html memanggil MG.run(draw).

   window.V (timing.js, dari build_video.py):  off, dur, lines (kapsyen), seg {"01": [a, b], ...}, cues {nama: saat}, sfx, bpm
   Semua masa dalam draw(t) ialah masa VO (saat), sama seperti spec "scenes":  t = masa video - V.off.

     const T = MG.at;                 // T('@03'), T('@03e'), T('@03%40'), T('@03+0.2')  -> saat VO
     const Q = MG.cue;                // Q('unit1') -> saat VO dari "cues" dalam spec.json (sama dengan masa SFX)
     MG.run(t => { ... }, { caption: true });

   Pembantu tambahan atas engine.js (clamp, mix, p, E, set, inout, caption):
     E.pop (cubic-bezier .34,1.56,.64,1), E.outQt, E.outX, E.ioQ;  MG.spring / MG.squash (pop + squash & stretch)
     MG.rng(seed), MG.svg(tag, attrs, parent), MG.tf(node, x, y, sx, sy, r), MG.inv(a, b, x), MG.hump(u)  */
(function () {
  const bezier = (x1, y1, x2, y2) => {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = t => ((ax * t + bx) * t + cx) * t, sy = t => ((ay * t + by) * t + cy) * t, dx = t => (3 * ax * t + 2 * bx) * t + cx;
    return u => { if (u <= 0) return 0; if (u >= 1) return 1; let t = u;
      for (let i = 0; i < 10; i++) { const d = dx(t); if (Math.abs(d) < 1e-6) break; t = clamp(t - (sx(t) - u) / d); } return sy(t); };
  };
  Object.assign(E, {
    pop: bezier(.34, 1.56, .64, 1),                 // lengkung overshoot klasik MG
    ioQ: u => u < .5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2,
    outQt: u => 1 - (1 - u) ** 4,
    outX: u => u >= 1 ? 1 : 1 - 2 ** (-10 * u),
    inB: (u, s = 1.70158) => (s + 1) * u ** 3 - s * u ** 2,
  });

  const inv = (a, b, x) => clamp((x - a) / (b - a));
  const hump = u => 4 * u * (1 - u);
  /* spring tertutup 0 -> 1 dan halajunya; f = Hz, z = redaman */
  const spring = (t, f = 2.4, z = .42) => { if (t <= 0) return 0; const w = 2 * Math.PI * f, a = z * w, b = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-a * t) * (Math.cos(b * t) + (a / b) * Math.sin(b * t)); };
  const springV = (t, f = 2.4, z = .42) => { if (t <= 0) return 0; const w = 2 * Math.PI * f, a = z * w, b = w * Math.sqrt(1 - z * z);
    return Math.exp(-a * t) * (w * w / b) * Math.sin(b * t); };
  /* pop spring bermula t0: [skala, squash]; squash +ve = regang menegak. Dipaku tepat 1 selepas `pin` s */
  const squash = (t, t0, { f = 2.4, z = .42, amt = .12, pin = .9 } = {}) => {
    const tt = t - t0; let s = spring(tt, f, z), k = clamp(springV(tt, f, z) / (2 * Math.PI * f) * amt * 2, -.3, .3);
    const w = E.ioQ(inv(pin * .7, pin, tt)); return [mix(s, 1, w), mix(k, 0, w)];
  };
  const rng = seed => { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };

  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const f3 = v => Math.round(v * 1000) / 1000;
  const tf = (e, x, y, sx = 1, sy = sx, r = 0) => {
    if (Math.abs(sx) < 1e-4 || Math.abs(sy) < 1e-4) { sx = 0; sy = 0; }
    e.setAttribute('transform', `translate(${f3(x)} ${f3(y)}) rotate(${f3(r)}) scale(${sx.toFixed(4)} ${sy.toFixed(4)})`);
  };

  /* "@07", "@07e", "@07%40", "@07+0.3" -> saat VO (sama seperti build_video.py) */
  const at = x => {
    if (typeof x === 'number') return x;
    const m = /^@(\w+?)(e|%(\d+))?([+-][\d.]+)?$/.exec(x);
    if (!m || !V.seg[m[1]]) throw new Error('masa tak sah: ' + x);
    const [a, b] = V.seg[m[1]];
    return (m[2] === 'e' ? b : m[3] ? a + (b - a) * m[3] / 100 : a) + (+m[4] || 0);
  };

  const cue = k => { if (!(k in V.cues)) throw new Error('cue tiada dalam spec.json: ' + k); return V.cues[k]; };

  /* draw(t) melukis bingkai pada masa VO t (boleh pulangkan Promise); kapsyen VO dalam #cap/#capText jika ada */
  const run = (draw, { caption: cap = true } = {}) => {
    window.DURATION = V.dur;
    const CH = buildChunks(V.lines);
    const hasCap = cap && document.getElementById('cap');
    window.seek = T => { const t = T - V.off; const r = draw(t); if (hasCap) caption(CH, t); return r; };
    window.seek(0);
  };

  window.MG = { at, cue, run, spring, springV, squash, rng, svg, tf, inv, hump, bezier };
})();
