const { chromium } = require('C:\\Users\\徐健\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const path = require('path');

const root = __dirname;
const out = path.join(root, 'assets');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    args: ['--no-first-run', '--no-default-browser-check'],
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 1 });
  const fixture = path.join(root, 'capture_ui_states.html').replace(/\\/g, '/');
  for (const state of ['proposal', 'confirmed', 'stale']) {
    await page.goto(`file:///${fixture}?state=${state}`, { waitUntil: 'load' });
    await page.screenshot({ path: path.join(out, `ui_${state}.png`), fullPage: true });
  }

  console.log('captured ui_proposal.png, ui_confirmed.png, ui_stale.png');
  await browser.close();
})().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
