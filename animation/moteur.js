// Moteur commun : présentateur articulé + décors animés (feu de camp s1, chapelle s2, sommet s3, chambre s4).
// Utilisé par la démo (animation/anim.js) et par les vidéos verset (verset/scene.js).
// Tout est déterministe : la même valeur de t donne toujours la même image (rendu image par image).
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
function setupDecors() {
  E = {
    etoiles: data('.etoile'), flammes: data('.flamme'), braises: data('.braise'), lum1: data('.c1_lum'),
    rayons: data('.rayon'), poussieres: data('.poussiere'), bougies: data('.bougie_fl'), bougiesGl: [...document.querySelectorAll('.bougie_gl')],
    nuages: data('.nuage'), oiseaux: data('.oiseau'), brumes: data('.brume'), pluie: data('.pluie'), gouttes: data('.goutte'),
  };
  E.bougiesGl.forEach((el, i) => { el._b = +el.getAttribute('opacity'); el._p = rnd(i) * 6; });
}
// syllabes d'une prise de parole (durées et ouvertures tirées au sort, mais fixes) : [[début, durée, ouverture], ...]
function syllabes(paroles, graine = 0) {
  const syl = []; let k = 0;
  for (const [a, b] of paroles) {
    let t = a;
    while (t < b - 0.1) {
      const d = 0.12 + rnd(graine + k * 3.1) * 0.12, amp = 0.35 + rnd(graine + k * 7.7) * 0.65;
      syl.push([t, d, amp]); t += d + (rnd(graine + k * 1.3) < 0.18 ? 0.09 : 0); k++;
    }
  }
  return syl;
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
  const k = Math.floor(u * 100);
  if (sc.env && sc.env[k] >= 0) o = cl((sc.env[k] + Math.max(0, sc.env[k + 1] ?? 0)) / 2 * 1.25);   // vraie voix
  else for (const [t, d, a] of sc.syl) if (u >= t && u < t + d) { o = a * Math.pow(Math.sin(Math.PI * (u - t) / d), 0.7); break; }
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
      set(p.el, 'cx', (p.x + p.a * Math.sin(gt * p.sp + p.ph) + 30 * Math.sin(gt * 0.07 + p.ph)).toFixed(1));
      set(p.el, 'cy', (p.y + 0.6 * p.a * Math.sin(gt * p.sp * 0.7 + p.ph * 1.3) + 20 * Math.sin(gt * 0.05 + p.ph * 1.7)).toFixed(1));
      set(p.el, 'opacity', (0.25 + 0.55 * (0.5 + 0.5 * Math.sin(gt * 1.3 + p.ph))).toFixed(3));
    }
  },
  s3(u, gt, dur = 5) {
    etoiles(gt);
    set($('c3_astre'), 'transform', `translate(0 ${(30 - 46 * lisse(u / dur)).toFixed(1)})`);
    for (const n of E.nuages) set(n.el, 'transform', `translate(${((((n.v * u) % 2400) + 2400) % 2400).toFixed(1)} 0)`);
    for (const o of E.oiseaux) {
      const x = -100 + (((o.x + o.v * u + 100) % 2300) + 2300) % 2300, y = o.y + 8 * Math.sin(u * 1.1 + o.ph), ail = Math.cos(u * 11 + o.ph);
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
