// node browser_shot.mjs <analysis.json> [lang=de] [mode=light] [width=780]
// Renders every chart of an analysis in headless Edge with the site's Vega runtime and fonts (real text metrics).
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import * as vl from '../../../../tools/node_modules/vega-lite/build/index.js';
import { chromium } from '../../../../tools/node_modules/playwright-core/index.mjs';
import { theme, isComposite, applyTokens } from '../../../../tools/vega_theme.mjs';
const ROOT = path.resolve('C:/Users/totom/Projects/reuss-edition');
const [file, lang = 'de', mode = 'light', width = '780'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const res = (n) => (Array.isArray(n) ? n.map(res) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n[lang] : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, res(v)]))) : n);
const rows = (ds) => ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));
const specs = {};
for (const ch of a.charts) {
  const spec = applyTokens(res(structuredClone(ch.vegalite)), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, ...spec };
  if (isComposite(full)) { full.autosize = { type: 'pad' }; } else { full.width = 'container'; }
  const vg = vl.compile(full, { config: theme(mode), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error() {} } }).spec;
  const names = new Set([ch.dataset, ...(ch.extra_datasets || [])]);
  for (const d of vg.data || []) if (names.has(d.name) && !d.values && !d.source && !d.url) d.values = rows(a.datasets.find((x) => x.name === d.name));
  specs[ch.id] = vg;
}
const fonts = path.join(ROOT, 'site/assets/fonts');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"Source Sans 3";src:url("${pathToFileURL(path.join(fonts, 'source-sans-3-latin-wght-normal.woff2'))}");font-weight:200 900}
@font-face{font-family:"Source Sans 3";src:url("${pathToFileURL(path.join(fonts, 'source-sans-3-latin-ext-wght-normal.woff2'))}");font-weight:200 900;unicode-range:U+0100-02AF}
body{margin:0;padding:12px;background:${mode === 'dark' ? '#1d1b18' : '#fbf8f1'};font-family:"Source Sans 3",sans-serif}
.c{width:${width}px;margin:0 0 24px 0;overflow:visible}
</style></head><body>
${a.charts.map((c) => `<div class="c" id="${c.id}"></div>`).join('\n')}
<script src="${pathToFileURL(path.join(ROOT, 'site/assets/vendor/vega/vega.min.js'))}"></script>
<script>
const specs = ${JSON.stringify(specs)};
vega.formatLocale(${lang === 'de' ? "{ decimal: ',', thousands: '.', grouping: [3], currency: ['', ' Taler'] }" : "{ decimal: '.', thousands: ',', grouping: [3], currency: ['', ' thalers'] }"});
document.fonts.ready.then(async () => {
  for (const [id, spec] of Object.entries(specs)) { const v = new vega.View(vega.parse(spec), { renderer: 'svg', container: '#' + id }); await v.runAsync(); }
  document.title = 'done';
});
</script></body></html>`;
const outdir = path.join(path.dirname(file), '_work', 'F1', 'browser');
fs.mkdirSync(outdir, { recursive: true });
const htmlPath = path.join(outdir, `${a.id}__${lang}_${mode}.html`);
fs.writeFileSync(htmlPath, html);
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: +width + 40, height: 900 }, deviceScaleFactor: 1.4 });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(pathToFileURL(htmlPath).href);
await page.waitForFunction(() => document.title === 'done', null, { timeout: 30000 }).catch((e) => errors.push('timeout'));
for (const c of a.charts) {
  const el = await page.$('#' + c.id);
  await el.screenshot({ path: path.join(outdir, `${a.id}__${c.id}__${lang}_${mode}.png`) });
}
console.log(errors.length ? errors.join(' | ') : 'ok');
await browser.close();
