// node thumb.mjs <feature-id>  -> out/thumb_<id>.png (as compile_charts renders it) and out/thumb_<id>_crop.png (top 360 px)
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const T = 'C:/Users/totom/Projects/reuss-edition/tools';
const vl = await import(pathToFileURL(`${T}/node_modules/vega-lite/build/index.js`).href);
const vega = await import(pathToFileURL(`${T}/node_modules/vega/build/vega.module.js`).href);
const { theme, isComposite, applyTokens } = await import(pathToFileURL(`${T}/vega_theme.mjs`).href);
const require = createRequire(`${T}/package.json`);
const { Resvg } = require('@resvg/resvg-js');
const fid = process.argv[2];
const a = JSON.parse(fs.readFileSync(`C:/Users/totom/Projects/reuss-edition/data/analyses/${fid}.json`, 'utf8'));
const ch = a.charts[0];
const resolveLang = (n) => Array.isArray(n) ? n.map(resolveLang) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n.de : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, resolveLang(v)]))) : n;
const spec = applyTokens(resolveLang(structuredClone(ch.vegalite)), 'light');
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
if (!full.data) full.data = { name: ch.dataset };
if (isComposite(full)) { full.autosize = { type: 'pad' }; } else { full.width = 560; full.autosize = { type: 'fit-x', contains: 'padding' }; }
const vg = vl.compile(full, { config: theme('light'), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error() {} } }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of new Set([ch.dataset, ...(ch.extra_datasets || [])])) { try { const d = a.datasets.find((x) => x.name === n); view.data(n, d.rows.map((r) => Object.fromEntries(d.columns.map((c, i) => [c.name, r[i]])))); } catch {} }
await view.runAsync();
const svg = (await view.toSVG()).replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
const png = new Resvg(svg, { fitTo: { mode: 'width', value: 640 }, background: '#fffdf8', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
fs.mkdirSync('C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F8/out', { recursive: true });
fs.writeFileSync(`C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F8/out/thumb_${fid}.png`, png);
console.log(fid);
