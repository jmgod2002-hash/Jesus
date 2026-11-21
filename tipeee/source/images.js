// Images de la page Tipeee, tirées des visuels YouTube (aucun nouveau dessin).
// - photo_profil_800.png : la photo de profil YouTube, telle quelle.
// - couverture_1800x600.png : la bannière YouTube de nuit, recadrée en 3:1 autour du logo et du nom.
// Usage : node tipeee/source/images.js
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const svg = f => fs.readFileSync(path.join(ROOT, 'youtube', f), 'utf8');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
  await p.setContent('<body style="margin:0">' + svg('photo_profil_youtube.svg') + '</body>');
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(ROOT, 'tipeee', 'photo_profil_800.png'), clip: { x: 0, y: 0, width: 800, height: 800 } });
  await p.setContent('<body style="margin:0">' + svg('banniere_youtube.svg') + '</body>');
  await p.evaluate(() => document.fonts.ready);
  // Le contenu tient dans 507..2053 x 508..931 : le cadre 380..2180 x 420..1020 le garde entier avec de la marge.
  await p.screenshot({ path: path.join(ROOT, 'tipeee', 'couverture_1800x600.png'), clip: { x: 380, y: 420, width: 1800, height: 600 } });
  await b.close();
})();
