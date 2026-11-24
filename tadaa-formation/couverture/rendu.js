// node rendu.js → ../couverture_evenement_facebook_1920x1005.png
const { chromium } = require("playwright"), path = require("path");
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1005 }, deviceScaleFactor: 1 });
  await p.goto("file://" + path.join(__dirname, "couverture.html")); await p.evaluate(() => window.ready);
  await p.locator("#c").screenshot({ path: path.join(__dirname, "..", "couverture_evenement_facebook_1920x1005.png") });
  await b.close(); console.log("OK");
})();
