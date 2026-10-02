// F6 helper: render a chart in English and/or dark mode to PNG in _work/F6/alt/ (the official validator only writes the German light preview).
//   node render_alt.mjs <analysis-id> <chart-id> <lang> <mode>
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const TOOLS = 'C:/Users/totom/Projects/reuss-edition/tools';
const require = createRequire(TOOLS + '/package.json');
const vl = await import('file:///' + TOOLS + '/node_modules/vega-lite/build/index.js');
const vega = await import('file:///' + TOOLS + '/node_modules/vega/build/vega.module.js');
const { Resvg } = require('@resvg/resvg-js');
const { theme, isComposite, applyTokens } = await import('file:///' + TOOLS + '/vega_theme.mjs');

const [id, chartId, lang = 'en', mode = 'light'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(`C:/Users/totom/Projects/reuss-edition/data/analyses/${id}.json`, 'utf8'));
const ch = a.charts.find((c) => c.id === chartId);
vega.formatLocale(lang === 'de' ? { decimal: ',', thousands: '.', grouping: [3], currency: ['', ' Taler'] } : { decimal: '.', thousands: ',', grouping: [3], currency: ['', ' thalers'] });
function resolveLang(node) {
  if (Array.isArray(node)) return node.map(resolveLang);
  if (node && typeof node === 'object') {
    const keys = Object.keys(node);
    if (keys.length === 2 && keys.includes('de') && keys.includes('en') && typeof node.de === 'string') return node[lang];
    return Object.fromEntries(Object.entries(node).map(([k, v]) => [k, resolveLang(v)]));
  }
  return node;
}
const spec = applyTokens(resolveLang(structuredClone(ch.vegalite)), mode);
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
if (!full.data) full.data = { name: ch.dataset };
if (isComposite(full)) { full.autosize = { type: 'pad' }; } else if (full.width === undefined) full.width = 640;
const vg = vl.compile(full, { config: theme(mode), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error: console.error } }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of new Set([ch.dataset, ...(ch.extra_datasets || [])])) {
  const d = a.datasets.find((x) => x.name === n);
  try { view.data(n, d.rows.map((r) => Object.fromEntries(d.columns.map((c, i) => [c.name, r[i]])))); } catch { /* unused */ }
}
await view.runAsync();
const svg = (await view.toSVG()).replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
const bg = mode === 'dark' ? '#1d1b18' : '#fbf8f1';
const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: bg, font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
const outDir = 'C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F6/alt';
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, `${id}__${chartId}__${lang}_${mode}.png`);
fs.writeFileSync(out, png);
console.log(out);
