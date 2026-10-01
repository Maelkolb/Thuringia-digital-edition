import { chromium } from 'playwright-core';
const pages = process.argv.slice(2).map(Number);
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
const page = await ctx.newPage();
page.on('pageerror', e => console.log('PAGEERROR', e.message));
await page.goto('file:///C:/Users/totom/Projects/reuss-edition/source/final_edition_allpages.html', { waitUntil: 'load', timeout: 120000 });
await page.screenshot({ path: '../audit/shots/landing.png' });
await page.evaluate(() => { try { startEdition(0); } catch(e) { console.log(e) } });
await page.waitForTimeout(800);
for (const p of pages) {
  await page.evaluate((p) => { try { goToPage(p) } catch(e) {} }, p);
  await page.waitForTimeout(2500);
  const el = await page.$(`#page-${p}`);
  await el.screenshot({ path: `../audit/shots/legacy_p${p}.png` });
  console.log('shot', p);
}
await browser.close();
