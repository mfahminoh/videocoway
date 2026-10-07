// 8 style. Setiap style boleh ganti komponen babak (hook/offer/gift/urgency/cta) dan tambah `extra` (elemen sepanjang video).
// Fungsi babak: (sc, opt, H) -> { update(t) }. H = helper dari overlay.js.
(function () {
  const S = window.STYLES;
  const C = () => window.COMP;

  // nota ringkas dalam kotak putih (dipakai S6/S7)
  function note(sc, H, top = 1060, size = 62, dark = false) {
    const box = H.$("div", "", H.rich(sc.text.replace(/ · /g, " · ")));
    Object.assign(box.style, { position: "absolute", left: "70px", right: "70px", top: top + "px", textAlign: "center",
      fontWeight: 700, padding: "20px 30px", borderRadius: "26px", lineHeight: 1.15,
      background: dark ? "rgba(35,31,32,.9)" : "rgba(255,255,255,.95)", color: dark ? "#fff" : "#231F20",
      boxShadow: "0 12px 34px rgba(0,0,0,.25)" });
    H.root.appendChild(box);
    H.fitLines(box, 940, 230, size, 40); box.style.width = "";
    return { update: t => H.enter(box, t, sc.t0, sc.t1, "rise") };
  }

  // ---------------- S1 Hentak Harga ----------------
  S.S1 = { flashes: [0.02, 3.0] };

  // ---------------- S2 Countdown ----------------
  S.S2 = {
    hook: (sc, o, H) => C().hook(sc, { kind: "drop", top: 640 }),
    offer: (sc, o, H) => C().offer(sc, { kind: "rise", kind2: "pop" }),
    extra: (D, root, H) => {
      const w = H.$("div", "", `<div class="cdl">TAMAT <b>25 OKT</b></div><div class="cdd"><span class="n">${D.days_left}</span><span class="u">HARI</span></div><div class="cdt">23:59:59</div>`);
      Object.assign(w.style, { position: "absolute", right: "46px", top: "64px", width: "300px", padding: "18px 10px 16px",
        background: "#231F20", borderRadius: "26px", textAlign: "center", boxShadow: "0 10px 30px rgba(0,0,0,.35)" });
      root.appendChild(w);
      const st = document.createElement("style");
      st.textContent = `.cdl{font-size:30px;font-weight:500;color:#fff;letter-spacing:1px}.cdl b{color:#00A0E0;font-weight:800}
        .cdd{margin-top:2px}.cdd .n{font-size:110px;font-weight:800;color:#fff;line-height:1}.cdd .u{font-size:40px;font-weight:800;color:#00A0E0;margin-left:8px}
        .cdt{font-size:44px;font-weight:700;color:#fff;font-variant-numeric:tabular-nums;background:#00A0E0;border-radius:14px;margin:8px 16px 0;padding:2px 0}`;
      document.head.appendChild(st);
      const clock = w.querySelector(".cdt");
      return [t => {
        const k = H.seg(t, .1, .45);
        H.put(w, t >= D.end_card ? 0 : k, 0, -60 * (1 - H.E.out(k)));
        const left = 86399 - Math.floor(t);                       // jam undur berdetik setiap saat
        const hh = String(Math.floor(left / 3600)).padStart(2, "0"), mm = String(Math.floor(left % 3600 / 60)).padStart(2, "0"), ss = String(left % 60).padStart(2, "0");
        clock.textContent = `${hh}:${mm}:${ss}`;
        const pulse = 1 + .05 * Math.max(0, 1 - ((t % 1) / .25));
        clock.style.transform = `scale(${pulse})`;
      }];
    },
  };

  // ---------------- S3 Kalkulator Harga ----------------
  S.S3 = {
    offer: (sc, o, H) => {
      const card = H.$("div", "calc");
      const txt = sc.text;
      let lhs, rhs;
      if (txt.includes("=")) [lhs, rhs] = txt.split("=").map(s => s.trim());
      else { const p = H.parts(txt); lhs = p[0]; rhs = p[1] || ""; }
      card.innerHTML = `<div class="lcd"><div class="lhs">${H.rich(lhs)}</div><div class="rhs">${rhs ? (txt.includes("=") ? "= " : "") + H.rich(rhs) : ""}</div></div>
        <div class="keys">${["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "="].map(k => `<span class="${"÷×=".includes(k) ? "op" : ""}">${k}</span>`).join("")}</div>`;
      H.root.appendChild(card);
      const st = document.createElement("style");
      st.textContent = `.calc{position:absolute;left:110px;right:110px;top:470px;background:#fff;border-radius:44px;padding:34px;box-shadow:0 24px 60px rgba(0,0,0,.35);color:#231F20}
        .calc .lcd{background:#F8F8F8;border-radius:24px;padding:26px 30px;text-align:right;min-height:250px}
        .calc .lhs{font-size:66px;font-weight:500;color:#35383B}.calc .rhs{font-size:96px;font-weight:800;line-height:1.05;margin-top:6px}
        .calc .price{box-shadow:none}.calc .keys{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
        .calc .keys span{display:block;text-align:center;font-size:48px;font-weight:700;padding:14px 0;border-radius:20px;background:#B2CDDB;color:#231F20}
        .calc .keys span.op{background:#00A0E0;color:#fff}`;
      document.head.appendChild(st);
      const lh = card.querySelector(".lhs"), rh = card.querySelector(".rhs");
      H.fitLines(lh, 740, 160, 66, 40); lh.style.width = ""; H.fitLines(rh, 740, 220, 96, 50); rh.style.width = "";
      const num = rhs && rhs.match(/RM(\d+)/);
      const target = num ? +num[1] : null, rhsHTML = rh.innerHTML;
      return { el: card, update: t => {
        H.enter(card, t, sc.t0, sc.t1, "pop");
        H.enter(lh, t, sc.t0, sc.t1, "fade", .25);
        if (t < sc.t0 + .9) { rh.style.opacity = 0; return; }
        rh.style.opacity = 1;
        if (target) {                                              // nombor berlari 0 -> sasaran
          const k = H.E.out(H.seg(t, sc.t0 + .9, sc.t0 + 1.8));
          rh.innerHTML = rhsHTML.replace(/RM\d+/, "RM" + Math.round(target * k));
        }
      } };
    },
    flashes: [3.95],
  };
  window.CHIP7_TOP = window.CHIP7_TOP || {};

  // ---------------- S4 3 Sebab ----------------
  const PASTEL = ["#B2CDDB", "#CBEED1", "#F99CD4"];
  function reasonCard(sc, H, i) {
    const m = sc.text.match(/^(\d)\s*·\s*(.*)$/);
    const n = m ? m[1] : String(i + 1), body = m ? m[2] : sc.text;
    const card = H.$("div", "", `<div class="rn">${n}</div><div class="rt">${H.rich(body)}</div>`);
    Object.assign(card.style, { position: "absolute", left: "60px", right: "60px", top: "520px", background: PASTEL[i % 3], color: "#231F20",
      borderRadius: "48px", padding: "40px 46px 50px", boxShadow: "0 24px 60px rgba(0,0,0,.3)" });
    H.root.appendChild(card);
    const rn = card.querySelector(".rn"), rt = card.querySelector(".rt");
    Object.assign(rn.style, { width: "200px", height: "200px", borderRadius: "50%", background: "#231F20", color: "#fff", fontSize: "150px",
      fontWeight: 800, lineHeight: "200px", textAlign: "center" });
    Object.assign(rt.style, { marginTop: "26px", fontSize: "84px", fontWeight: 800, lineHeight: 1.08 });
    H.fitLines(rt, 860, 300, 84, 50); rt.style.width = "";
    return { update: t => {
      if (t < sc.t0 || t > sc.t1) return H.put(card, 0);
      const k = H.seg(t, sc.t0, sc.t0 + .35), out = 1 - H.seg(t, sc.t1 - .15, sc.t1);
      H.put(card, out, 1080 * (1 - H.E.out(k)) - 600 * H.seg(t, sc.t1 - .15, sc.t1), 0, 1, -4 * (1 - H.E.out(k)));
      H.put(rn, 1, 0, 0, .3 + .7 * H.E.back(H.seg(t, sc.t0 + .2, sc.t0 + .5)));
    } };
  }
  S.S4 = { offer: (sc, o, H) => reasonCard(sc, H, 0), gift: (sc, o, H) => reasonCard(sc, H, 1), urgency: (sc, o, H) => reasonCard(sc, H, 2) };

  // ---------------- S5 Kad Soalan Lazim ----------------
  function faq(sc, H, i) {
    const t0 = sc.text, qi = t0.indexOf("?");
    const q = qi >= 0 ? t0.slice(0, qi + 1) : null, a = qi >= 0 ? t0.slice(qi + 1).trim() : t0;
    const wrap = H.$("div", ""); Object.assign(wrap.style, { position: "absolute", left: "70px", right: "70px", top: "540px" });
    const qc = H.$("div", "", q ? H.rich(q) : "Jawapan:"), ac = H.$("div", "", H.rich(a));
    Object.assign(qc.style, { background: PASTEL[i % 2], color: "#231F20", fontSize: "78px", fontWeight: 800, padding: "30px 40px", borderRadius: "40px 40px 40px 8px",
      boxShadow: "0 16px 40px rgba(0,0,0,.25)", display: "inline-block", maxWidth: "940px" });
    Object.assign(ac.style, { marginTop: "30px", marginLeft: "80px", background: "#fff", color: "#231F20", fontSize: "70px", fontWeight: 500, padding: "28px 40px",
      borderRadius: "40px 40px 8px 40px", boxShadow: "0 16px 40px rgba(0,0,0,.25)", display: "inline-block", maxWidth: "860px" });
    wrap.appendChild(qc); wrap.appendChild(H.$("div", "")); wrap.lastChild.appendChild(ac); H.root.appendChild(wrap);
    H.fitLines(qc, 940, 260, q ? 78 : 50, 44); qc.style.width = ""; H.fitLines(ac, 860, 260, 70, 44); ac.style.width = "";
    return { update: t => { H.enter(qc, t, sc.t0, sc.t1, "pop"); H.enter(ac, t, sc.t0, sc.t1, "rise", .7); } };
  }
  S.S5 = { offer: (sc, o, H) => faq(sc, H, 0), gift: (sc, o, H) => faq(sc, H, 1), urgency: (sc, o, H) => faq(sc, H, 0) };

  // ---------------- S6 Sekarang vs Tunggu ----------------
  S.S6 = {
    hook: (sc, o, H) => C().hook(sc, { kind: "slam", top: 700 }),
    offer: (sc, o, H) => note(sc, H, 1050), gift: (sc, o, H) => note(sc, H, 1050), urgency: (sc, o, H) => note(sc, H, 1050, 62, true),
    extra: (D, root, H) => {
      const L = H.$("div", "", `<div class="sx">TUNGGU</div><div class="sy">lepas <span class="date">25 Okt</span></div><div class="sz">tiada promo</div>`);
      const R = H.$("div", "", `<div class="sx">SEKARANG</div><div class="sy"><span class="price">RM20</span><span class="thin">/bulan</span></div><div class="sz">7 bulan pertama</div>`);
      const vs = H.$("div", "", "VS"), line = H.$("div", "");
      [L, R].forEach((e, i) => { Object.assign(e.style, { position: "absolute", top: "250px", width: "500px", left: i ? "560px" : "20px", textAlign: "center", textShadow: "0 3px 12px rgba(0,0,0,.6)" }); root.appendChild(e); });
      Object.assign(line.style, { position: "absolute", left: "536px", width: "8px", top: "0", height: "1920px", background: "#fff", boxShadow: "0 0 20px rgba(0,0,0,.4)" });
      Object.assign(vs.style, { position: "absolute", left: "455px", top: "560px", width: "170px", height: "170px", borderRadius: "50%", background: "#231F20",
        color: "#fff", fontSize: "76px", fontWeight: 800, lineHeight: "170px", textAlign: "center", boxShadow: "0 10px 30px rgba(0,0,0,.4)" });
      root.insertBefore(line, root.firstChild); root.appendChild(vs);
      const st = document.createElement("style");
      st.textContent = `.sx{font-size:74px;font-weight:800;color:#fff}.sy{font-size:70px;font-weight:800;color:#fff;margin-top:6px}.sz{display:inline-block;margin-top:14px;font-size:44px;font-weight:800;padding:6px 22px;border-radius:999px;background:#fff;color:#231F20;text-shadow:none}`;
      document.head.appendChild(st);
      L.querySelector(".sz").style.background = "#35383B"; L.querySelector(".sz").style.color = "#fff";
      return [t => {
        const on = t >= 3.0 && t < 16.0, k = H.seg(t, 3.0, 3.35), o = on ? 1 - H.seg(t, 15.85, 16.0) : 0;
        H.put(L, o * k, -200 * (1 - H.E.out(k))); H.put(R, o * k, 200 * (1 - H.E.out(k)));
        line.style.opacity = o; H.put(vs, o, 0, 0, .5 + .5 * H.E.back(H.seg(t, 3.1, 3.45)) * (1 + .04 * Math.sin(t * 6)));
      }];
    },
  };

  // ---------------- S7 Montaj ASMR ----------------
  S.S7 = {
    hook: (sc, o, H) => C().hook(sc, { kind: "fade", size: 120, top: 760 }),
    offer: (sc, o, H) => note(sc, H, 1080, 66, true), gift: (sc, o, H) => note(sc, H, 1080, 60, true), urgency: (sc, o, H) => note(sc, H, 1080, 60, true),
  };

  // ---------------- S8 Pengumuman Ulangtahun ----------------
  function confetti(root, H, bursts) {
    const cv = document.createElement("canvas"); cv.width = 1080; cv.height = 1920;
    Object.assign(cv.style, { position: "absolute", left: 0, top: 0 }); root.appendChild(cv);
    const ctx = cv.getContext("2d"), cols = ["#00A0E0", "#F99CD4", "#CBEED1", "#B2CDDB", "#FFFFFF", "#FFD34D"];
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const P = bursts.flatMap(b => Array.from({ length: 140 }, () => ({ b, x: 540 + (rnd() - .5) * 300, y: 900, vx: (rnd() - .5) * 1700, vy: -900 - rnd() * 1300,
      r: rnd() * 6, vr: (rnd() - .5) * 14, w: 14 + rnd() * 16, h: 8 + rnd() * 10, c: cols[Math.floor(rnd() * cols.length)] })));
    return t => {
      ctx.clearRect(0, 0, 1080, 1920);
      for (const p of P) {
        const dt = t - p.b; if (dt < 0 || dt > 2.6) continue;
        const x = p.x + p.vx * dt * Math.exp(-dt * .6), y = p.y + p.vy * dt + 1100 * dt * dt;
        ctx.save(); ctx.globalAlpha = Math.min(1, (2.6 - dt) * 2); ctx.translate(x, y); ctx.rotate(p.r + p.vr * dt);
        ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(dt * 9 + p.r))); ctx.restore();
      }
    };
  }
  S.S8 = {
    hook: (sc, o, H) => {
      const bg = H.$("div", ""); Object.assign(bg.style, { position: "absolute", inset: 0, background: "linear-gradient(170deg,#F99CD4 0%,#FBC6E6 55%,#CBEED1 100%)" });
      bg.innerHTML = `<div class="b20">20</div><div class="btah">TAHUN COWAY DI MALAYSIA</div>
        <img class="bprod" src="../assets/img/neon-lineup-5-warna.jpg">`;
      H.root.appendChild(bg);
      const st = document.createElement("style");
      st.textContent = `.b20{position:absolute;left:0;right:0;top:170px;text-align:center;font-size:520px;font-weight:800;color:#fff;line-height:1;letter-spacing:-20px;text-shadow:0 18px 50px rgba(0,160,224,.45)}
        .btah{position:absolute;left:0;right:0;top:700px;text-align:center;font-size:54px;font-weight:800;color:#231F20;letter-spacing:4px}
        .bprod{position:absolute;left:240px;top:1180px;width:600px;height:600px;object-fit:cover;border-radius:48px;box-shadow:0 20px 50px rgba(0,0,0,.25)}`;
      document.head.appendChild(st);
      const h = C().hook(sc, { kind: "pop", top: 820, size: 104, maxH: 330 }); h.el.style.color = "#231F20"; h.el.style.textShadow = "none";
      const b20 = bg.querySelector(".b20"), prod = bg.querySelector(".bprod");
      return { update: t => {
        if (t > sc.t1) { H.put(bg, 0); return h.update(t); }
        H.put(bg, 1 - H.seg(t, sc.t1 - .15, sc.t1));
        H.put(b20, 1, 0, 0, .3 + .7 * H.E.back(H.seg(t, 0, .45)));
        H.put(prod, H.seg(t, .5, .8), 0, 120 * (1 - H.E.out(H.seg(t, .5, .9))));
        h.update(t);
      } };
    },
    extra: (D, root, H) => [confetti(root, H, [0.15, 3.0, 7.0, 12.0])],
    hideLogo: t => t < 3.0,
  };
})();
