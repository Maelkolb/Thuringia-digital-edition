// axe-core accessibility audit of edition pages (local server on :8642)
import { chromium } from 'playwright-core';
import fs from 'node:fs';
const axe = fs.readFileSync(new URL('./node_modules/axe-core/axe.min.js', import.meta.url), 'utf8');
const pages = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
for (const dark of [false, true]) {
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 }, colorScheme: dark ? 'dark' : 'light' });
  const page = await ctx.newPage();
  for (const p of pages) {
    await page.goto('http://127.0.0.1:8642/' + p, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);
    await page.addScriptTag({ content: axe });
    const res = await page.evaluate(async () => (await axe.run(document, { resultTypes: ['violations'] })).violations
      .map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, help: v.help, ex: v.nodes.slice(0, 2).map((n) => n.target.join(' ') + ' :: ' + (n.failureSummary || '').split('\n').slice(1, 2).join(' ')) })));
    console.log(`\n== ${p} ${dark ? '(dark)' : ''}: ${res.length} violation types`);
    for (const v of res) console.log(`  [${v.impact}] ${v.id} x${v.n}: ${v.help}\n      ${v.ex.join('\n      ')}`);
  }
  await ctx.close();
}
await browser.close();
