// Rendert alle SVG in ../ als PNG nach ../png (deviceScaleFactor 1)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1680, height: 1188 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    await p.goto('file://' + path.join(dir, f));
    await p.screenshot({ path: path.join(dir, 'png', f.replace('.svg', '.png')) });
    console.log('png', f);
  }
  await b.close();
})();
