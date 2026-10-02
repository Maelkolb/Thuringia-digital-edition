// node browser_check.mjs <feature-id> [container-width] [de|en] [light|dark]
// compiles each chart like tools/compile_charts.mjs and renders it in headless Edge with the site fonts and vega runtime
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const T = 'C:/Users/totom/Projects/reuss-edition/tools';
const S = 'C:/Users/totom/Projects/reuss-edition/site';
const OUT = 'C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F8/out';
const vl = await import(pathToFileURL(`${T}/node_modules/vega-lite/build/index.js`).href);
const { theme, isComposite, applyTokens } = await import(pathToFileURL(`${T}/vega_theme.mjs`).href);
const require = createRequire(`${T}/package.json`);
const { chromium } = require('playwright-core');
const [fid, cw = '720', lang = 'de', mode = 'light'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(`C:/Users/totom/Projects/reuss-edition/data/analyses/${fid}.json`, 'utf8'));
const resolveLang = (n) => Array.isArray(n) ? n.map(resolveLang) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n[lang] : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, resolveLang(v)]))) : n;
const rowsAsObjects = (ds) => ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));
const specs = {};
for (const ch of a.charts) {
  const spec = applyTokens(resolveLang(structuredClone(ch.vegalite)), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
  if (!full.data) full.data = { name: ch.dataset };
  if (isComposite(full)) { full.autosize = { type: 'pad' }; if (full.width === 'container') delete full.width; } else full.width = 'container';
  const vg = vl.compile(full, { config: theme(mode), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error() {} } }).spec;
  const names = new Set([ch.dataset, ...(ch.extra_datasets || [])]);
  for (const d of vg.data || []) if (names.has(d.name) && !d.values && !d.source && !d.url) d.values = rowsAsObjects(a.datasets.find((x) => x.name === d.name));
  specs[ch.id] = vg;
}
const bg = mode === 'dark' ? '#1d1b18' : '#fbf8f1';
const html = `<!doctype html><meta charset="utf-8"><style>
@font-face { font-family: "Source Sans 3"; font-weight: 200 900; src: url("file:///${S}/assets/fonts/source-sans-3-latin-wght-normal.woff2") format("woff2"); }
body { margin: 0; background: ${bg}; font-family: "Source Sans 3"; } .c { width: ${cw}px; margin: 10px; background: ${bg}; }
</style><body>${a.charts.map((c) => `<div class="c" id="${c.id}"></div>`).join('')}
<script src="file:///${S}/assets/vendor/vega/vega.min.js"></script>
<script>
window.SPECS = ${JSON.stringify(specs)};
vega.formatLocale(${lang === 'de' ? "{ decimal: ',', thousands: '.', grouping: [3], currency: ['', ' Taler'] }" : "{ decimal: '.', thousands: ',', grouping: [3], currency: ['', ' thalers'] }"});
window.DONE = Promise.all(Object.keys(SPECS).map((id) => { const v = new vega.View(vega.parse(SPECS[id]), { renderer: 'svg', container: '#' + id }); return v.runAsync(); }));
</script>`;
fs.mkdirSync(OUT, { recursive: true });
const file = `${OUT}/browser_${fid}.html`;
fs.writeFileSync(file, html);
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: Number(cw) + 40, height: 900 }, colorScheme: mode, deviceScaleFactor: 1.5 });
const page = await ctx.newPage();
page.on('pageerror', (e) => console.log('pageerror', String(e).slice(0, 300)));
page.on('console', (m) => { if (m.type() === 'error') console.log('console', m.text().slice(0, 200)); });
await page.goto(pathToFileURL(file).href);
await page.evaluate(async () => { await window.DONE; return 1; });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);
for (const ch of a.charts) {
  const el = await page.$('#' + ch.id);
  const out = `${OUT}/br_${fid}__${ch.id}__${cw}_${lang}_${mode}.png`;
  await el.screenshot({ path: out });
  const box = await el.boundingBox();
  console.log(out, Math.round(box.width), Math.round(box.height));
}
await browser.close();
