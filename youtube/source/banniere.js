// Bannière YouTube 2560 x 1440. Tout le contenu tient dans la bande visible partout (1546 x 423 au centre),
// et la bande visible sur ordinateur (2560 x 423) reste habillée. Usage : node banniere.js [nuit|creme]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const theme = process.argv[2] || 'nuit';
const T = theme === 'nuit'
  ? { fond: ['#2A170C', '#160C06', '#0E0804'], lueur: '#FFC98A', lueurOp: .3, braise: '#C0522B', braiseOp: .55, logo: '#F5EDE0', nom: '#FFF6E8', sur: '#E8A06A', slogan: '#D9C19C', trait: '#C0522B', braises: '#E8893C', sortie: 'banniere_youtube_2560x1440.png', svg: 'banniere_youtube.svg' }
  : { fond: ['#FAF4EA', '#F5EDE0', '#E2CFB2'], lueur: '#FFFBF3', lueurOp: .9, braise: '#C0522B', braiseOp: .18, logo: '#3B2412', nom: '#3B2412', sur: '#8A6E57', slogan: '#5A4130', trait: '#3B2412', braises: '#B8662A', sortie: 'banniere_youtube_creme_2560x1440.png', svg: 'banniere_youtube_creme.svg' };
const d = s => s.match(/ d="([^"]+)"/)[1];
const logo = fs.readFileSync(path.join(ROOT, 'youtube/logo.svg'), 'utf8');
const subs = d(logo).match(/M[^M]+/g); const torche = subs.slice(0, 12).join(''), flamme = subs.slice(12).join('');
const nom = d(fs.readFileSync(path.join(ROOT, 'marque/nom_feu_d_elevation.svg'), 'utf8'));
const inter = fs.readFileSync(path.join(ROOT, 'intro/fonts/inter-500.woff2')).toString('base64');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" id="ban" width="2560" height="1440" viewBox="0 0 2560 1440">
<style>@font-face{font-family:"InterB";src:url(data:font/woff2;base64,${inter}) format("woff2");font-weight:100 900} text{font-family:"InterB",Inter,Arial,sans-serif;font-weight:500}</style>
<defs>
 <radialGradient id="bg" cx="50%" cy="50%" r="75%"><stop offset="0" stop-color="${T.fond[0]}"/><stop offset=".55" stop-color="${T.fond[1]}"/><stop offset="1" stop-color="${T.fond[2]}"/></radialGradient>
 <radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1"><stop offset="0" stop-color="${T.lueur}" stop-opacity="${T.lueurOp}"/><stop offset=".5" stop-color="${T.lueur}" stop-opacity="${T.lueurOp * .35}"/><stop offset="1" stop-color="${T.lueur}" stop-opacity="0"/></radialGradient>
 <radialGradient id="br" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1"><stop offset="0" stop-color="${T.braise}" stop-opacity="${T.braiseOp}"/><stop offset="1" stop-color="${T.braise}" stop-opacity="0"/></radialGradient>
 <filter id="f6" filterUnits="userSpaceOnUse" x="0" y="0" width="2560" height="1440"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="2560" height="1440" fill="url(#bg)"/>
<ellipse cx="0" cy="0" rx="1" ry="1" fill="url(#br)" transform="translate(260 1000) scale(900 520)"/>
<ellipse cx="0" cy="0" rx="1" ry="1" fill="url(#br)" transform="translate(2330 420) scale(820 480)"/>
<ellipse id="g" cx="0" cy="0" rx="1" ry="1" fill="url(#glow)"/>
<g id="braises" fill="${T.braises}"></g>
<g id="logo" fill-rule="evenodd" fill="${T.logo}"><path d="${torche}"/><path d="${flamme}"/></g>
<text id="eyebrow" font-size="26" letter-spacing="11" fill="${T.sur}">MINISTÈRE CHRÉTIEN</text>
<path id="name" fill="${T.nom}" d="${nom}"/>
<rect id="rule" height="4" fill="${T.trait}"/>
<text id="tag" font-size="30" letter-spacing="5" fill="${T.slogan}">PRIÈRE • ADORATION • ENSEIGNEMENT • ÉVANGÉLISATION</text>
</svg>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
  await p.setContent('<body style="margin:0">' + svg + '</body>'); await p.evaluate(() => document.fonts.ready);
  const out = await p.evaluate(() => {
    const $ = id => document.getElementById(id);
    const LH = 370, LS = LH / 800, LW = 486 * LS, NW = 1060, NS = NW / 6376, GAP = 96;
    const tag = $('tag'), k = NW / tag.getComputedTextLength();
    tag.setAttribute('font-size', (30 * k).toFixed(2)); tag.setAttribute('letter-spacing', (5 * k).toFixed(2));
    const x0 = 1280 - (LW + GAP + NW) / 2, xt = x0 + LW + GAP, cy = 720, top = cy - LH / 2;
    $('logo').setAttribute('transform', `translate(${x0.toFixed(1)} ${top}) scale(${LS})`);
    const yb = cy - 150, base = yb + 54 + 942 * NS;
    $('eyebrow').setAttribute('x', xt + 4); $('eyebrow').setAttribute('y', yb + 22);
    $('name').setAttribute('transform', `translate(${xt.toFixed(1)} ${base.toFixed(1)}) scale(${NS.toFixed(5)})`);
    $('rule').setAttribute('x', xt + 4); $('rule').setAttribute('y', base + 32); $('rule').setAttribute('width', 96);
    tag.setAttribute('x', xt + 2); tag.setAttribute('y', base + 92);
    const fx = x0 + 250 * LS, fy = top + 200 * LS;
    $('g').setAttribute('transform', `translate(${fx} ${fy}) scale(${640 * 1.3} 560)`);
    [[-50, -150, 6], [40, -205, 4.5], [105, -130, 4], [-12, -250, 3.5], [78, -278, 3], [-78, -210, 3], [140, -190, 2.5]].forEach(([dx, dy, r]) => {
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', fx + dx); c.setAttribute('cy', fy + dy + 40); c.setAttribute('r', r); c.setAttribute('opacity', .7); $('braises').appendChild(c); });
    const bb = ['logo', 'name', 'tag', 'eyebrow'].map(id => { const r = $(id).getBoundingClientRect(); return [id, Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
    return { svg: $('ban').outerHTML, bb };
  });
  const zone = { x0: 507, y0: 508, x1: 2053, y1: 931 };
  const ok = out.bb.every(([, l, t, r, bt]) => l >= zone.x0 && r <= zone.x1 && t >= zone.y0 && bt <= zone.y1);
  console.log(theme, JSON.stringify(out.bb), ok ? 'OK : tout est dans la zone visible partout' : 'ATTENTION : hors zone');
  fs.writeFileSync(path.join(ROOT, 'youtube', T.svg), out.svg);
  await p.screenshot({ path: path.join(ROOT, 'youtube', T.sortie) });
  await b.close();
})();
