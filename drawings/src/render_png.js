// Rendert die SVG-Zeichnungen mit Chromium (Playwright) als PNG, deviceScaleFactor 1.
// Aufruf: node drawings/src/render_png.js [crop]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dir = path.resolve(__dirname, '..');
const out = path.join(dir, 'png');
const files = ['TZ-01_Gesamtansicht.svg', 'TZ-02_Details.svg'];

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const f of files) {
    const p = path.join(dir, f);
    if (!fs.existsSync(p)) continue;
    const svg = fs.readFileSync(p, 'utf8');
    const m = svg.match(/width="([\d.]+)mm" height="([\d.]+)mm"/);
    const w = Math.round(parseFloat(m[1]) * 96 / 25.4);
    const h = Math.round(parseFloat(m[2]) * 96 / 25.4);
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + p);
    const png = path.join(out, f.replace('.svg', '.png'));
    await page.screenshot({ path: png, fullPage: false });
    // Ausschnitte (Quadranten) zur Sichtpruefung
    if (process.argv[2] === 'crop') {
      const cw = Math.ceil(w / 2), ch = Math.ceil(h / 2);
      let k = 0;
      for (let j = 0; j < 2; j++) for (let i = 0; i < 2; i++) {
        k++;
        await page.screenshot({ path: path.join(out, f.replace('.svg', `_q${k}.png`)),
          clip: { x: i * cw, y: j * ch, width: Math.min(cw, w - i * cw), height: Math.min(ch, h - j * ch) } });
      }
    }
    await page.close();
    console.log(png, w, h);
  }
  await browser.close();
})();
