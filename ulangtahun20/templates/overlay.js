// Overlay deterministik: window.setup(data) sekali, kemudian window.__render(t) untuk setiap frame (t dalam saat).
// Tiada animasi CSS/rAF — semua keadaan dikira terus dari t supaya setiap frame boleh diulang tepat.
(function () {
  const $ = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const E = {
    out: x => 1 - Math.pow(1 - x, 3),
    inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    back: x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
  };
  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  // "Promo RM20" -> perkataan biasa + lencana harga; tarikh dalam Coway Blue
  const rich = s => esc(s)
    .replace(/RM\s?\d+/g, m => `<span class="price">${m}</span>`)
    .replace(/(\/bulan)/g, `<span class="thin">$1</span>`)
    .replace(/(25 Oktober|25 OKTOBER|25 Okt|25 OKT)/g, `<span class="date">$1</span>`)
    .replace(/(7 bulan pertama|7 BULAN PERTAMA)/g, `<b class="bold">$1</b>`)
    .replace(/((?:ke|KE)-\d+)/g, `<span style="white-space:nowrap">$1</span>`);
  const parts = s => s.split(" · ").map(x => x.trim()).filter(Boolean);
  const WA = `<svg viewBox="0 0 64 64"><path fill="#fff" d="M32 5C17.1 5 5 16.6 5 31c0 5 1.5 9.7 4.1 13.7L6 59l14.8-3.9c3.4 1.6 7.2 2.6 11.2 2.6 14.9 0 27-11.6 27-26S46.9 5 32 5z"/><path fill="#25D366" d="M45.6 38.6c-.7-.4-4.3-2.1-4.9-2.3-.7-.3-1.1-.4-1.6.4-.5.7-1.9 2.3-2.3 2.7-.4.5-.8.5-1.6.2-.7-.4-3-1.1-5.8-3.5-2.1-1.9-3.6-4.2-4-4.9-.4-.7 0-1.1.3-1.5.3-.3.7-.8 1.1-1.3.4-.4.5-.7.7-1.2.3-.5.1-.9 0-1.3-.2-.4-1.6-3.8-2.2-5.2-.6-1.4-1.2-1.2-1.6-1.2h-1.4c-.5 0-1.3.2-1.9.9-.7.7-2.5 2.4-2.5 5.9s2.6 6.8 2.9 7.3c.4.5 5 7.7 12.2 10.8 1.7.7 3 1.2 4.1 1.5 1.7.5 3.3.5 4.5.3 1.4-.2 4.3-1.7 4.9-3.4.6-1.7.6-3.1.4-3.4-.2-.3-.7-.5-1.4-.8z"/></svg>`;

  // ---------- keadaan kongsi ----------
  let D, root, logo, subsBox, subEls = [], flash, endcard, sceneEls = {}, chip7s = [], extra = [];
  const S = window.STYLES = {};

  // transform helper: el.style dari {o, x, y, s, r}
  function put(el, o = 1, x = 0, y = 0, s = 1, r = 0, origin) {
    el.style.opacity = o; el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
    if (origin) el.style.transformOrigin = origin;
    el.style.visibility = o <= 0.001 ? "hidden" : "visible";
  }
  // gegaran kecil deterministik
  const shake = (t, t0, amp = 14, dur = .28) => {
    const k = seg(t, t0, t0 + dur); if (k <= 0 || k >= 1) return [0, 0];
    const a = amp * (1 - k); return [Math.sin(t * 97) * a, Math.cos(t * 83) * a];
  };
  // masuk/keluar standard untuk satu elemen babak
  function enter(el, t, t0, t1, kind = "rise", delay = 0) {
    const a = t0 + delay, k = seg(t, a, a + (kind === "slam" ? .18 : .32)), out = 1 - seg(t, t1 - .14, t1);
    if (t < a || t > t1) return put(el, 0);
    if (kind === "slam") { const [sx, sy] = shake(t, a + .14); return put(el, Math.min(1, k * 3) * out, sx, sy, 2.4 - 1.4 * E.out(k)); }
    if (kind === "pop") return put(el, Math.min(1, k * 2) * out, 0, 0, .55 + .45 * E.back(k));
    if (kind === "left") return put(el, out * k, -260 * (1 - E.out(k)), 0);
    if (kind === "right") return put(el, out * k, 260 * (1 - E.out(k)), 0);
    if (kind === "drop") return put(el, out * k, 0, -180 * (1 - E.back(k)));
    if (kind === "fade") return put(el, out * E.inOut(k));
    return put(el, out * k, 0, 90 * (1 - E.out(k)));               // rise
  }
  // muat saiz font supaya teks muat dalam lebar w (sekali semasa setup)
  function fit(el, w, max, min = 40) {
    let f = max; el.style.fontSize = f + "px";
    while (f > min && (el.scrollWidth > w + 1 || el.getBoundingClientRect().width > w + 1)) { f -= 2; el.style.fontSize = f + "px"; }
    return f;
  }
  function fitLines(el, w, maxH, max, min = 40) {          // teks berbilang baris: kecilkan hingga tinggi <= maxH
    let f = max; el.style.fontSize = f + "px"; el.style.width = w + "px";
    while (f > min && el.scrollHeight > maxH) { f -= 2; el.style.fontSize = f + "px"; }
    return f;
  }
  const scene = k => D.scenes.find(s => s.key === k);

  // ---------- komponen lalai (dipakai/diubah oleh style) ----------
  const C = window.COMP = {
    hook(sc, opt = {}) {
      const el = $("div", "hookText", rich(sc.text)); root.appendChild(el);
      el.style.top = (opt.top || 600) + "px";
      fitLines(el, 940, opt.maxH || 520, opt.size || 150, 64);
      el.style.width = ""; el.style.left = "70px"; el.style.right = "70px";
      return { el, update: t => enter(el, t, sc.t0, sc.t1, opt.kind || "slam") };
    },
    offer(sc, opt = {}) {
      const p = parts(sc.text), box = $("div", "offer"); root.appendChild(box);
      const m = p[0].match(/^(.*?)(RM\s?\d+)(\/bulan)?(.*)$/);
      let big, l2;
      if (m && !m[1].trim() && !m[4].trim()) {
        big = $("div", "big", `<span class="price">${m[2]}</span>${m[3] ? `<span class="per">${m[3]}</span>` : ""}`);
      } else big = $("div", "plain", rich(p[0]));
      box.appendChild(big);
      if (p[1]) { l2 = $("div", "line2", rich(p[1])); box.appendChild($("div", "", "")).appendChild(l2); }
      if (big.className === "plain") fitLines(big, 940, 360, 100, 56);
      else fit(big, 960, 300, 120);
      return { el: box, update: t => {
        enter(big, t, sc.t0, sc.t1, opt.kind || "slam");
        if (l2) enter(l2, t, sc.t0, sc.t1, opt.kind2 || "pop", .35);
      } };
    },
    gift(sc, opt = {}) {
      const box = $("div", "chips"); root.appendChild(box);
      const chips = parts(sc.text).map(x => {
        const plus = x.startsWith("+"); const txt = plus ? x.slice(1).trim() : x;
        const c = $("div", "chip", (plus ? `<span class="plus">+</span>` : "") + rich(txt).replace(/(Freegift|Pasang free|Premium Coway)/g, "<b>$1</b>"));
        box.appendChild(c); fit(c, 960, 70, 40); return c;
      });
      return { el: box, update: t => chips.forEach((c, i) => enter(c, t, sc.t0, sc.t1, opt.kind || "pop", .1 + i * .45)) };
    },
    urgency(sc, opt = {}) {
      const p = parts(sc.text), band = $("div", "band"); root.appendChild(band);
      const l1 = p.length > 1 ? $("div", "l1", rich(p[0])) : null, l2 = $("div", "l2", rich(p[p.length - 1]));
      if (l1) band.appendChild(l1); band.appendChild(l2);
      fit(l2, 960, 104, 50);
      return { el: band, update: t => {
        const k = seg(t, sc.t0, sc.t0 + .35), out = 1 - seg(t, sc.t1 - .14, sc.t1);
        if (t < sc.t0 || t > sc.t1) return put(band, 0);
        put(band, out, 1080 * (1 - E.out(k)), 0);
        enter(l2, t, sc.t0, sc.t1, "pop", .3);
      } };
    },
    cta(sc) {
      const box = $("div", "ctaClip"); const b = $("div", "wa", WA + "<span>" + esc(sc.text) + "</span>"); box.appendChild(b); root.appendChild(box);
      return { el: box, update: t => {
        if (t < sc.t0 || t >= D.end_card) return put(box, 0);
        const k = seg(t, sc.t0, sc.t0 + .3), pulse = 1 + .06 * Math.sin((t - sc.t0) * Math.PI * 2 * 1.6);
        put(box, 1, 0, 0, 1); put(b, Math.min(1, k * 2), 0, 0, (.6 + .4 * E.back(k)) * pulse);
      } };
    },
  };

  function buildEndcard() {
    endcard = $("div", "endcard");
    endcard.innerHTML = `<img class="elogo" src="../assets/logo/coway-logo-4x.png">
      <img class="prod" src="../assets/img/neon-lineup-5-warna.jpg">
      <div class="name">Coway <b>Neon</b></div>
      <div class="btn"><div class="wa">${WA}<span>${esc(scene("cta").text)}</span></div></div>`;
    root.appendChild(endcard);
    const prod = endcard.querySelector(".prod"), btn = endcard.querySelector(".wa"), lg = endcard.querySelector(".elogo"), nm = endcard.querySelector(".name");
    return t => {
      if (t < D.end_card) return put(endcard, 0);
      const k = seg(t, D.end_card, D.end_card + .3);
      put(endcard, E.out(k), 0, 0, 1);
      put(lg, seg(t, D.end_card + .1, D.end_card + .4), -0, 40 * (1 - E.out(seg(t, D.end_card + .1, D.end_card + .45))));
      lg.style.transform += " translateX(-50%)"; lg.style.left = "50%";
      put(prod, seg(t, D.end_card + .2, D.end_card + .5), 0, 0, .9 + .1 * E.out(seg(t, D.end_card + .2, D.end_card + .7)));
      put(nm, seg(t, D.end_card + .35, D.end_card + .6));
      const kb = seg(t, D.end_card + .25, D.end_card + .55);
      put(btn, Math.min(1, kb * 2), 0, 0, (.6 + .4 * E.back(kb)) * (1 + .06 * Math.sin((t - D.end_card) * Math.PI * 2 * 1.6)));
    };
  }

  function buildSubs() {
    subsBox = $("div", "subs"); root.appendChild(subsBox);
    subEls = D.subs.map(s => { const e = $("div", "sub", rich(s.text)); subsBox.appendChild(e); e.style.position = "absolute"; return e; });
    return t => {
      subsBox.style.top = (t >= D.end_card ? 1500 : (window.SUB_TOP || 1300)) + "px";
      D.subs.forEach((s, i) => {
        const e = subEls[i];
        if (t < s.t0 || t >= s.t1) return put(e, 0);
        const k = seg(t, s.t0, s.t0 + .12); put(e, k, 0, 14 * (1 - k), .96 + .04 * k);
      });
    };
  }

  function buildChip7(sceneEls) {
    return D.scenes.filter(s => s.chip7 && s.key !== "cta").map(s => {
      const e = $("div", "chip7", "7 bulan pertama"); root.appendChild(e);
      const se = sceneEls[s.key];
      if (window.CHIP7_TOP && window.CHIP7_TOP[s.key]) e.style.top = window.CHIP7_TOP[s.key] + "px";
      else if (se) e.style.top = Math.min(1190, Math.round(se.getBoundingClientRect().bottom + 26)) + "px";
      return t => {
        if (t < s.t0 || t > s.t1) return put(e, 0);
        const k = seg(t, s.t0 + .25, s.t0 + .5), out = 1 - seg(t, s.t1 - .12, s.t1);
        e.style.opacity = Math.min(k, out); e.style.visibility = k * out > 0 ? "visible" : "hidden";
        e.style.transform = `translateX(-50%) scale(${.7 + .3 * E.back(k)})`;
      };
    });
  }

  window.setup = function (data) {
    D = data; root = document.getElementById("root");
    const style = S[D.style] || {};
    if (style.pre) style.pre(D, root, { $, rich, parts, put, seg, E, enter, fit, fitLines, shake, scene, WA, esc });
    const scrim = $("div", "scrim"); root.appendChild(scrim);
    logo = $("img", "logo"); logo.src = "../assets/logo/coway-logo-4x.png"; root.appendChild(logo);
    const updaters = [], sceneEls = {};
    for (const sc of D.scenes) {
      const make = (style[sc.key] || C[sc.key]);
      const r = make(sc, {}, { $, rich, parts, put, seg, E, enter, fit, fitLines, shake, scene, WA, esc, C, root, D });
      if (r) { updaters.push(r.update); if (r.el) sceneEls[sc.key] = r.el; }
    }
    if (style.extra) extra = style.extra(D, root, { $, rich, parts, put, seg, E, enter, fit, fitLines, shake, scene, WA, esc, C });
    updaters.push(...buildChip7(sceneEls));
    updaters.push(buildSubs());
    updaters.push(buildEndcard());
    flash = $("div", "flash"); root.appendChild(flash);
    const flashes = style.flashes || [];
    updaters.push(t => {
      let o = 0; for (const f of flashes) { const k = seg(t, f, f + .12); if (k > 0 && k < 1) o = Math.max(o, .45 * (1 - k)); }
      flash.style.opacity = o;
      logo.style.visibility = (t >= D.end_card || (style.hideLogo && style.hideLogo(t))) ? "hidden" : "visible";
    });
    if (extra) updaters.push(...[].concat(extra));
    window.__render = t => { for (const u of updaters) u(t); };
    return true;
  };
  window.seek = t => window.__render(t);
})();
