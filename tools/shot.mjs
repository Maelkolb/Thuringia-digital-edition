// Screenshot pages of the local edition for visual QA.
//   node tools/shot.mjs <outdir> path[@WIDTH][#dark|#en] ...
import { chromium } from 'playwright-core';
import fs from 'node:fs';
const [out, ...paths] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
for (const spec of paths) {
  let [p, opts = ''] = spec.split('|');
  let width = 1440, height = 900, dark = opts.includes('dark'), en = opts.includes('en'), full = opts.includes('full');
  const m = opts.match(/w(\d+)/); if (m) width = +m[1];
  if (width < 700) height = 860;
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme: dark ? 'dark' : 'light', deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push('PAGEERROR ' + e.message));
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push('CONSOLE ' + msg.text()); });
  if (en) await page.addInitScript(() => { try { localStorage.setItem('rj.ui', 'en'); } catch (e) {} });
  await page.goto('http://127.0.0.1:8642/' + p, { waitUntil: 'networkidle', timeout: 60000 }).catch((e) => errors.push('GOTO ' + e.message));
  await page.waitForTimeout(opts.includes('slow') ? 4000 : 1500);
  const name = (p.replace(/[\/?#=&:%]+/g, '_') || 'index') + (opts ? '_' + opts.replace(/[^a-z0-9]/gi, '') : '') + '.png';
  await page.screenshot({ path: `${out}/${name}`, fullPage: full });
  console.log(name, errors.length ? errors.slice(0, 4).join(' | ') : 'ok');
  await ctx.close();
}
await browser.close();
