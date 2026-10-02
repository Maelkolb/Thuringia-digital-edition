// Exercise the page view: citation panel, line view, text <-> facsimile highlighting, search hits.
//   node tools/check_pageview.mjs [page-slug] [outdir]
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [slug = '203', out = 'audit/pageview'] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const base = pathToFileURL(path.resolve('site')).href + '/';
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'de-DE' });
await ctx.addInitScript(() => { try { localStorage.setItem('rj.ui', 'de'); } catch (e) {} });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto(base + `seite/${slug}.html?hl=Gera`);
await page.waitForTimeout(3500);

await page.click('[data-cite-toggle]');
const cite = await page.$eval('[data-cite-text]', (el) => el.innerText.trim());
await page.screenshot({ path: `${out}/1_cite.png` });
await page.click('[data-cite-toggle]');

const hits = await page.$$eval('.zone.hit', (z) => z.length);
await page.click('[data-toggle-lines]');
await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/2_lines.png` });

const target = await page.$('.transcription p:nth-of-type(2)');
await target.scrollIntoViewIfNeeded();
await page.waitForTimeout(200);
const box = await target.boundingBox();
const hy = Math.min(Math.max(box.y + 40, 200), 700);
for (let k = 0; k < 4; k++) { await page.mouse.move(box.x + box.width * 0.4 + k * 6, hy); await page.waitForTimeout(150); }
const zoneShown = await page.$$eval('.zone:not(.hit):not(.block)', (z) => z.filter((e) => e.offsetParent !== null).length);
const textHl = await page.evaluate(() => (window.CSS && CSS.highlights && CSS.highlights.has('line')) ? 'yes' : 'no');
await page.screenshot({ path: `${out}/3_hover_text.png` });

const facs = await page.$('#facs');
const fb = await facs.boundingBox();
for (let k = 0; k < 4; k++) { await page.mouse.move(fb.x + fb.width * 0.5 + k * 6, fb.y + fb.height * 0.35); await page.waitForTimeout(150); }
const textHl2 = await page.evaluate(() => (window.CSS && CSS.highlights && CSS.highlights.has('line')) ? 'yes' : 'no');
await page.screenshot({ path: `${out}/4_hover_facs.png` });

console.log(JSON.stringify({ cite, searchHitZones: hits, zoneOnTextHover: zoneShown, textHighlightOnTextHover: textHl, textHighlightOnFacsHover: textHl2, errors }, null, 1));
await browser.close();
