// Rend chaque <section> de carrousel_saas.html en PNG 1080 x 1920 dans tiktok/carrousel_saas.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'carrousel_saas.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const n = await p.locator('section.s').count();
  for (let i = 1; i <= n; i++) await p.locator('#s' + i).screenshot({ path: path.join(root, 'carrousel_saas', `image_${String(i).padStart(2, '0')}.png`) });
  console.log(n, 'images'); await b.close();
})();
