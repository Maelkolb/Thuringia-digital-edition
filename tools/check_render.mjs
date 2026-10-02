// Open every analysis page and the map in headless Edge and report what did not render.
//   node tools/check_render.mjs <site-dir> [http|file] [out.json]
import { chromium } from 'playwright-core';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [siteArg, mode = 'http', outFile] = process.argv.slice(2);
const SITE = path.resolve(siteArg);
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json',
  '.png': 'image/png', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.xml': 'application/xml', '.csv': 'text/csv' };

let server, base;
if (mode === 'http') {
  server = http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p.endsWith('/')) p += 'index.html';
    const f = path.join(SITE, p);
    if (!f.startsWith(SITE) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  await new Promise((r) => server.listen(8643, '127.0.0.1', r));
  base = 'http://127.0.0.1:8643/';
} else {
  base = pathToFileURL(SITE).href + '/';
}

const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const report = [];

async function check(rel, fn) {
  const page = await ctx.newPage();
  const errors = [], failed = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', (e) => errors.push('pageerror: ' + String(e).slice(0, 200)));
  page.on('response', (r) => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url().slice(0, 120)); });
  page.on('requestfailed', (r) => failed.push('FAIL ' + r.url().slice(0, 120) + ' ' + (r.failure()?.errorText || '')));
  await page.goto(base + rel, { waitUntil: 'load' }).catch((e) => errors.push('goto: ' + e.message));
  await page.waitForTimeout(2500);
  const res = await fn(page);
  report.push({ page: rel, ...res, errors: [...new Set(errors)].slice(0, 6), failed: [...new Set(failed)].slice(0, 6), nFailed: failed.length });
  await page.close();
}

const charts = (page) => page.evaluate(() => {
  const els = Array.from(document.querySelectorAll('[data-chart]'));
  const empty = els.filter((e) => { const s = e.querySelector('svg'); return !s || s.getBoundingClientRect().width < 20 || s.getBoundingClientRect().height < 20; })
    .map((e) => e.getAttribute('data-chart'));
  return { charts: els.length, empty };
});

const only = process.env.ONLY;
const pages = only ? only.split(',') : fs.readdirSync(path.join(SITE, 'auswertungen')).filter((f) => f.endsWith('.html') && f !== 'index.html').map((f) => 'auswertungen/' + f);
await check('karte.html', (page) => page.evaluate(() => {
  const tiles = Array.from(document.querySelectorAll('.leaflet-tile'));
  return { tiles: tiles.length, tilesLoaded: tiles.filter((t) => t.complete && t.naturalWidth > 0).length, tileSrc: tiles[0] && tiles[0].src.slice(0, 40),
    places: document.querySelectorAll('#map-list li').length, noTiles: document.getElementById('map').classList.contains('no-tiles') };
}));
await check('suche.html?q=Napoleon', (page) => page.evaluate(() => ({ status: document.querySelector('[data-search-status]').innerText, results: document.querySelectorAll('.result').length,
  snippets: Array.from(document.querySelectorAll('.result .snip')).filter((s) => s.innerText.trim()).length })));
await check('index.html', async (page) => {
  await page.fill('[data-quicksearch] input', 'Schleiz'); await page.waitForTimeout(1200);
  return page.evaluate(() => ({ quick: document.querySelectorAll('[data-quicksearch] .qs-results a').length, fontsLoaded: document.fonts.status, faces: Array.from(document.fonts).filter((f) => f.status === 'loaded').length }));
});
await check('register/orte.html#gera', async (page) => {
  const b = await page.$('[data-kwic]'); if (b) { await b.click(); await page.waitForTimeout(1500); }
  return page.evaluate(() => ({ kwic: document.querySelectorAll('.kwic a').length }));
});
await check('seite/44.html', async (page) => { await page.waitForTimeout(3000); return page.evaluate(() => ({ facsimile: document.querySelectorAll('.openseadragon-canvas canvas, .facs-viewer canvas').length, faces: Array.from(document.fonts).filter((f) => f.status === 'loaded').length })); });
for (const p of pages) await check(p, charts);
await browser.close();
if (server) server.close();

const bad = report.filter((r) => (r.empty && r.empty.length) || (r.charts === 0) || r.errors.length || r.nFailed);
const special = report.filter((r) => !r.page.startsWith('auswertungen/'));
for (const r of special.concat(bad.filter((r) => r.page.startsWith('auswertungen/')).slice(0, 5))) console.log(JSON.stringify(r));
console.log(`${mode}: ${report.length} pages checked, ${bad.length} with problems; charts total ${report.reduce((a, r) => a + (r.charts || 0), 0)}, empty ${report.reduce((a, r) => a + (r.empty ? r.empty.length : 0), 0)}`);
if (outFile) fs.writeFileSync(outFile, JSON.stringify(report, null, 1));
