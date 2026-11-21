// Animation du présentateur dans les décors. window.seek(t) dessine l'image au temps t (secondes).
// Tout est déterministe : la même valeur de t donne toujours la même image (rendu image par image).
const C = window.CONFIG;
const $ = id => document.getElementById(id);
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, x) => a + (b - a) * x;
const lisse = x => { x = cl(x); return x * x * (3 - 2 * x); };
const rnd = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
// bruit doux (somme de sinus) entre -1 et 1, pour le vacillement des flammes
const nz = (t, p) => 0.5 * Math.sin(t * 9.3 + p) + 0.3 * Math.sin(t * 15.1 + p * 1.7) + 0.2 * Math.sin(t * 24.7 + p * 2.3);
const set = (el, k, v) => el.setAttribute(k, v);
const data = (sel) => [...document.querySelectorAll(sel)].map(el => ({ el, ...Object.fromEntries(Object.entries(el.dataset).map(([k, v]) => [k, +v])) }));

let E = {};
function setup() {
  E = {
    etoiles: data('.etoile'), flammes: data('.flamme'), braises: data('.braise'), lum1: data('.c1_lum'),
    rayons: data('.rayon'), poussieres: data('.poussiere'), bougies: data('.bougie_fl'), bougiesGl: [...document.querySelectorAll('.bougie_gl')],
    nuages: data('.nuage'), oiseaux: data('.oiseau'), brumes: data('.brume'), pluie: data('.pluie'), gouttes: data('.goutte'),
  };
  E.bougiesGl.forEach((el, i) => { el._b = +el.getAttribute('opacity'); el._p = rnd(i) * 6; });
  // syllabes de chaque prise de parole (durées et ouvertures tirées au sort, mais fixes)
  C.scenes.forEach((sc, si) => {
    sc.syl = []; let k = 0;
    for (const [a, b] of sc.paroles) {
      let t = a;
      while (t < b - 0.1) {
        const d = 0.12 + rnd(si * 100 + k * 3.1) * 0.12, amp = 0.35 + rnd(si * 100 + k * 7.7) * 0.65;
        sc.syl.push([t, d, amp]); t += d + (rnd(si * 100 + k * 1.3) < 0.18 ? 0.09 : 0); k++;
      }
    }
  });
}

// ---------------------------------------------------------------- personnage
function bouche(o) {
  const x0 = 314 + 3 * o, x1 = 376 - 3 * o, haut = 400 - 10 * o, bas = 400 + 34 * o;
  const d = `M${x0} 386 C330 ${haut} 356 ${haut} ${x1} 384 C356 ${bas} 330 ${bas} ${x0} 386 Z`;
  set($('bouche_int'), 'd', d); set($('bouche_cp'), 'd', d); set($('bouche_ln'), 'd', d);
  set($('dents'), 'd', `M${x0} 386 C330 ${haut} 356 ${haut} ${x1} 384 L${x1} 392 C356 ${haut + 8} 330 ${haut + 8} ${x0} 394 Z`);
  set($('langue'), 'cy', 388 + 24 * o); set($('langue'), 'ry', 3 + 9 * o);
}
function paupiere(n, b) {
  const g = $('paup_' + n);
  if (b <= 0.001) { set(g, 'display', 'none'); set($('cil_' + n), 'transform', ''); return; }
  set(g, 'display', 'inline');
  const h = 80 * b;
  set($('paupr_' + n), 'height', h);
  set($('paupl_' + n), 'transform', `translate(0 ${h})`);
  set($('cil_' + n), 'transform', `translate(0 ${60 * b})`);
}
function clin(u, temps) {   // 0 = ouvert, 1 = fermé
  let b = 0;
  for (const t0 of temps) {
    const x = u - t0;
    if (x < 0 || x > 0.2) continue;
    b = Math.max(b, x < 0.07 ? x / 0.07 : x < 0.1 ? 1 : 1 - (x - 0.1) / 0.1);
  }
  return b;
}
function personnage(sc, u, gt) {
  // parole : ouverture de la bouche par syllabe
  let o = 0;
  for (const [t, d, a] of sc.syl) if (u >= t && u < t + d) { o = a * Math.pow(Math.sin(Math.PI * (u - t) / d), 0.7); break; }
  bouche(o);
  let parle = 0;
  for (const [a, b] of sc.paroles) parle = Math.max(parle, lisse((u - a + 0.15) / 0.3) * (1 - lisse((u - b + 0.1) / 0.3)));
  // respiration (le buste monte, la tête suit)
  const br = Math.sin(2 * Math.PI * gt / 3.6);
  set($('buste'), 'transform', `translate(0 780) scale(1 ${1 + 0.008 * br}) translate(0 -780)`);
  const ang = 1.4 * Math.sin(2 * Math.PI * gt * 0.21 + 0.7) + parle * 1.6 * Math.sin(2 * Math.PI * u * 0.85 + 1);
  const dy = -2.5 * br + parle * 2.2 * Math.sin(2 * Math.PI * u * 1.7);
  set($('tete'), 'transform', `translate(0 ${dy.toFixed(2)}) rotate(${ang.toFixed(2)} 340 450)`);
  // sourcils : se lèvent au début de chaque phrase
  let s = 0;
  for (const [a] of sc.paroles) s = Math.max(s, Math.exp(-Math.pow((u - a - 0.25) / 0.3, 2)));
  set($('sourcils'), 'transform', `translate(0 ${(-7 * s).toFixed(2)})`);
  // clignements
  const b = clin(u, sc.clins); paupiere('g', b); paupiere('d', b);
  // le pied qui pend se balance doucement
  set($('pied'), 'transform', `rotate(${(2.2 * Math.sin(2 * Math.PI * gt * 0.45)).toFixed(2)} 480 805)`);
}

// ---------------------------------------------------------------- décors
function flammeT(f, t, sx = 1, sy = 1) {
  const n1 = nz(t, f.ph), n2 = nz(t * 0.8, f.ph + 2), n3 = nz(t * 1.1, f.ph + 4);
  return `translate(${f.x} ${f.y}) skewX(${(7 * n3).toFixed(2)}) scale(${(f.w * sx * (1 + 0.07 * n2)).toFixed(1)} ${(f.h * sy * (1 + 0.14 * n1)).toFixed(1)})`;
}
function bougies(gt) {
  for (const f of E.bougies) set(f.el, 'transform', `translate(${f.x} ${f.y}) skewX(${(6 * nz(gt * 1.3, f.ph + 3)).toFixed(2)}) scale(${(11 * f.s).toFixed(1)} ${(24 * f.s * (1 + 0.18 * nz(gt * 1.4, f.ph))).toFixed(1)})`);
  for (const el of E.bougiesGl) set(el, 'opacity', (el._b * (0.82 + 0.18 * nz(gt * 1.2, el._p))).toFixed(3));
}
function etoiles(gt) { for (const s of E.etoiles) set(s.el, 'opacity', (s.o * (0.6 + 0.4 * Math.sin(gt * s.sp + s.ph))).toFixed(3)); }

const ANIM = {
  s1(u, gt) {
    etoiles(gt);
    for (const f of E.flammes) set(f.el, 'transform', flammeT(f, gt));
    const v = nz(gt * 0.9, 0.5);
    for (const l of E.lum1) set(l.el, 'opacity', (l.b * (0.85 + 0.15 * v)).toFixed(3));
    set($('f_s1_r0'), 'flood-opacity', (0.72 + 0.2 * v).toFixed(3));
    for (const e of E.braises) {
      const age = (gt + e.off) % e.l, k = age / e.l;
      set(e.el, 'cx', (e.x + e.a * Math.sin(age * e.f + e.ph) + age * 14).toFixed(1));
      set(e.el, 'cy', (930 - age * e.v).toFixed(1));
      set(e.el, 'opacity', (cl(age / 0.15) * (1 - k) * (0.7 + 0.3 * Math.sin(gt * 20 + e.ph))).toFixed(3));
    }
  },
  s2(u, gt) {
    bougies(gt);
    for (const r of E.rayons) set(r.el, 'opacity', (r.b * (0.78 + 0.22 * Math.sin(gt * 0.9 + r.ph))).toFixed(3));
    for (const p of E.poussieres) {
      set(p.el, 'cx', (p.x + p.a * Math.sin(gt * p.sp + p.ph) - gt * 6).toFixed(1));
      set(p.el, 'cy', (p.y + 0.6 * p.a * Math.sin(gt * p.sp * 0.7 + p.ph * 1.3) + gt * 4).toFixed(1));
      set(p.el, 'opacity', (0.25 + 0.55 * (0.5 + 0.5 * Math.sin(gt * 1.3 + p.ph))).toFixed(3));
    }
  },
  s3(u, gt) {
    etoiles(gt);
    set($('c3_astre'), 'transform', `translate(0 ${(30 - 46 * lisse(u / C.scene)).toFixed(1)})`);
    for (const n of E.nuages) set(n.el, 'transform', `translate(${(n.v * u).toFixed(1)} 0)`);
    for (const o of E.oiseaux) {
      const x = o.x + o.v * u, y = o.y + 8 * Math.sin(u * 1.1 + o.ph), ail = Math.cos(u * 11 + o.ph);
      set(o.el, 'transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${o.s} ${(o.s * (0.25 + 0.75 * ail)).toFixed(2)})`);
    }
    for (const b of E.brumes) set(b.el, 'cx', (b.x - b.v * u).toFixed(1));
  },
  s4(u, gt) {
    bougies(gt);
    for (const p of E.pluie) { const y = 110 + ((p.y + p.v * gt) % 640); set(p.el, 'transform', `translate(${(p.x - (y - 110) * 0.12).toFixed(1)} ${y.toFixed(1)})`); }
    for (const g of E.gouttes) {
      const cyc = (g.y + g.v * gt) % 620, glisse = cyc + 18 * Math.max(0, Math.sin(gt * 1.7 + g.x));   // glisse par à-coups
      set(g.el, 'transform', `translate(${g.x} ${(110 + glisse).toFixed(1)})`);
    }
  },
};

// ---------------------------------------------------------------- montage
let courante = -1;
window.seek = function (t) {
  const n = C.scenes.length, i = Math.min(n - 1, Math.floor(t / C.scene)), u = t - i * C.scene, sc = C.scenes[i];
  if (i !== courante) {
    C.scenes.forEach((s, k) => { set($(s.id + '_fond'), 'display', k === i ? 'inline' : 'none'); set($(s.id + '_devant'), 'display', k === i ? 'inline' : 'none'); });
    set($('perso_pos'), 'transform', `translate(${sc.tx} ${sc.ty}) scale(${sc.s})`);
    set($('perso_lum'), 'filter', `url(#f_${sc.id})`);
    $('lab_n').textContent = `DÉCOR ${i + 1} / ${n}`; $('lab_t').textContent = sc.titre; $('lab_s').textContent = sc.sous;
    const w = Math.max($('lab_t').getComputedTextLength(), $('lab_s').getComputedTextLength(), $('lab_n').getComputedTextLength());
    set($('lab_fond'), 'width', (w + 56).toFixed(0));
    courante = i;
  }
  // caméra : lente avancée vers le personnage
  const [fx, fy] = sc.foyer, z = 1 + 0.045 * lisse(u / C.scene);
  set($('cam'), 'transform', `translate(${fx} ${fy}) scale(${z.toFixed(4)}) translate(${-fx} ${-fy})`);
  personnage(sc, u, t);
  ANIM[sc.id](u, t);
  // étiquette du décor
  const e = lisse((u - 0.35) / 0.4) * (1 - lisse((u - 4.25) / 0.35));
  set($('etiquette'), 'opacity', e.toFixed(3));
  set($('etiquette'), 'transform', `translate(${(56 - 24 * (1 - e)).toFixed(1)} 56)`);
  // passage au noir entre les décors
  const noir = Math.max(1 - lisse(u / 0.3), lisse((u - (C.scene - 0.3)) / 0.3));
  set($('noir'), 'opacity', noir.toFixed(3));
};
window.ready = document.fonts.ready.then(() => { setup(); window.seek(0.5); });

// ---------------------------------------------------------------- ambiance sonore (rendue hors ligne)
window.renderAudio = async function () {
  const D = C.dur, S = C.scene, sr = 48000, ac = new OfflineAudioContext(2, Math.ceil(D * sr), sr);
  const master = ac.createGain(); master.gain.value = 0.6; master.connect(ac.destination);
  const conv = ac.createConvolver(), ir = ac.createBuffer(2, sr * 2.5, sr);
  for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = (rnd(i * 7 + c) * 2 - 1) * Math.pow(1 - i / d.length, 2.5); }
  conv.buffer = ir; const wet = ac.createGain(); wet.gain.value = 0.3; conv.connect(wet); wet.connect(master);
  const blanc = (sec, g = 1) => { const b = ac.createBuffer(1, Math.ceil(sr * sec), sr), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(i * 3.1 + g) * 2 - 1; return b; };
  const brun = (sec) => { const b = ac.createBuffer(1, Math.ceil(sr * sec), sr), d = b.getChannelData(0); let l = 0; for (let i = 0; i < d.length; i++) { l = (l + 0.02 * (rnd(i * 1.7) * 2 - 1)) / 1.02; d[i] = l * 3.5; } return b; };
  // un bus par décor, avec fondu d'entrée et de sortie calé sur les passages au noir
  const bus = (k, rev = 0) => {
    const g = ac.createGain(), a = k * S, b = (k + 1) * S;
    g.gain.setValueAtTime(0, 0); g.gain.setValueAtTime(0, a + 0.001); g.gain.linearRampToValueAtTime(1, a + 0.35);
    g.gain.setValueAtTime(1, b - 0.35); g.gain.linearRampToValueAtTime(0, b);
    g.connect(master); if (rev) { const r = ac.createGain(); r.gain.value = rev; g.connect(r); r.connect(conv); }
    return g;
  };
  const source = (buf, t0, t1, ...chaine) => { const s = ac.createBufferSource(); s.buffer = buf; let n = s; for (const c of chaine) { n.connect(c); n = c; } s.start(t0); s.stop(t1); return n; };
  const filtre = (type, f, q = 0.7) => { const x = ac.createBiquadFilter(); x.type = type; x.frequency.value = f; x.Q.value = q; return x; };
  const gain = (v) => { const g = ac.createGain(); g.gain.value = v; return g; };
  const tic = (out, t, f, a, dec) => { const s = ac.createBufferSource(); s.buffer = blanc(0.08, t * 1000); const bp = filtre('bandpass', f, 1.2), g = ac.createGain();
    g.gain.setValueAtTime(a, t); g.gain.exponentialRampToValueAtTime(0.0005, t + dec); s.connect(bp); bp.connect(g); g.connect(out); s.start(t); s.stop(t + 0.08); };
  const nappe = (out, notes, t0, t1, a, type = 'triangle', fc = 1200) => notes.forEach((f, i) => [-4, 4].forEach(dt => {
    const o = ac.createOscillator(); o.type = type; o.frequency.value = f; o.detune.value = dt; const lp = filtre('lowpass', fc, 0.5), g = ac.createGain();
    g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(a, t0 + 1.2); o.connect(lp); lp.connect(g); g.connect(out); o.start(t0); o.stop(t1); }));
  // 1. feu de camp : grondement, souffle, crépitements
  { const o = bus(0, 0.1); source(brun(S), 0, S, filtre('lowpass', 380), gain(0.36)).connect(o); source(blanc(S, 1), 0, S, filtre('bandpass', 2600, 0.6), gain(0.025)).connect(o);
    for (let k = 0; k < 75; k++) tic(o, rnd(k + 0.3) * S, 1200 + rnd(k + 9) * 4800, 0.03 + Math.pow(rnd(k + 4), 3) * 0.2, 0.008 + rnd(k + 6) * 0.03); }
  // 2. chapelle : nappe douce et résonance
  { const o = bus(1, 0.8), a = S; nappe(o, [146.83, 220, 293.66, 369.99, 659.25], a, a + S, 0.022, 'sine', 1400);
    source(brun(S), a, a + S, filtre('lowpass', 180), gain(0.18)).connect(o);
    [[a + 0.5, 587.33], [a + 2.6, 880]].forEach(([t, f]) => [1, 2.01, 3.02].forEach((h, k) => { const os = ac.createOscillator(); os.frequency.value = f * h; const g = ac.createGain();
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.03 / (k + 1), t + 0.01); g.gain.exponentialRampToValueAtTime(0.0003, t + 2.5); os.connect(g); g.connect(o); os.start(t); os.stop(t + 2.6); })); }
  // 3. sommet : vent, nappe claire, oiseaux
  { const o = bus(2, 0.3), a = 2 * S, bp = filtre('bandpass', 500, 0.8), g = gain(0);
    source(blanc(S, 2), a, a + S, bp, g).connect(o);
    [[0, 380, 0.2], [1.2, 900, 0.36], [2.4, 520, 0.24], [3.5, 1100, 0.4], [5, 450, 0.2]].forEach(([t, f, v]) => { bp.frequency.linearRampToValueAtTime(f, a + t); g.gain.linearRampToValueAtTime(v, a + t); });
    nappe(o, [293.66, 440, 659.25, 739.99], a, a + S, 0.018, 'sine', 2400);
    [1.2, 1.38, 3.1, 3.3, 3.45].forEach((t, k) => { const os = ac.createOscillator(), gg = ac.createGain(), t0 = a + t; os.frequency.setValueAtTime(2900 + k * 150, t0); os.frequency.exponentialRampToValueAtTime(3900, t0 + 0.07);
      gg.gain.setValueAtTime(0, t0); gg.gain.linearRampToValueAtTime(0.03, t0 + 0.01); gg.gain.exponentialRampToValueAtTime(0.0005, t0 + 0.09); os.connect(gg); gg.connect(o); os.start(t0); os.stop(t0 + 0.1); }); }
  // 4. chambre : pluie sur la vitre, gouttes, nappe grave
  { const o = bus(3, 0.15), a = 3 * S; source(blanc(S, 3), a, a + S, filtre('highpass', 1300), filtre('lowpass', 7000), gain(0.11)).connect(o);
    source(brun(S), a, a + S, filtre('lowpass', 500), gain(0.16)).connect(o);
    for (let k = 0; k < 60; k++) tic(o, a + rnd(k + 50) * S, 3500 + rnd(k + 70) * 3500, 0.02 + rnd(k + 90) * 0.05, 0.006 + rnd(k + 40) * 0.01);
    nappe(o, [146.83, 185, 220], a, a + S, 0.014, 'sine', 700); }
  const buf = await ac.startRendering();
  let pk = 0; for (let c = 0; c < 2; c++) for (const v of buf.getChannelData(c)) pk = Math.max(pk, Math.abs(v));
  const k = 0.89 / pk, Lc = buf.getChannelData(0), Rc = buf.getChannelData(1), n = Lc.length, ab = new ArrayBuffer(44 + n * 4), dv = new DataView(ab);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
  ws(0, 'RIFF'); dv.setUint32(4, 36 + n * 4, true); ws(8, 'WAVE'); ws(12, 'fmt '); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 2, true);
  dv.setUint32(24, sr, true); dv.setUint32(28, sr * 4, true); dv.setUint16(32, 4, true); dv.setUint16(34, 16, true); ws(36, 'data'); dv.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { dv.setInt16(44 + i * 4, cl(Lc[i] * k, -1, 1) * 32767, true); dv.setInt16(46 + i * 4, cl(Rc[i] * k, -1, 1) * 32767, true); }
  let s = ''; const u8 = new Uint8Array(ab); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768)); return btoa(s);
};
