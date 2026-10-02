// Scratch renderer: node proto.mjs <analysis.json> <chartId> [lang]   -> proto_<chart>.png (does not touch _preview)
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const TOOLS = 'C:/Users/totom/Projects/reuss-edition/tools';
const req = createRequire(TOOLS + '/x.js');
const imp = async (n) => import(pathToFileURL(req.resolve(n)).href);
const vl = await imp('vega-lite'); const vega = await imp('vega'); const { Resvg } = req('@resvg/resvg-js');
const { theme } = await import(pathToFileURL(TOOLS + '/vega_theme.mjs').href);
const [file, cid, lang = 'de'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
function res(n) { if (Array.isArray(n)) return n.map(res); if (n && typeof n === 'object') { const k = Object.keys(n); if (k.length === 2 && k.includes('de') && k.includes('en') && typeof n.de === 'string') return n[lang]; return Object.fromEntries(Object.entries(n).map(([a, b]) => [a, res(b)])); } return n; }
const ch = a.charts.find(c => c.id === cid);
const spec = res(structuredClone(ch.vegalite));
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec, data: { name: ch.dataset } };
if (full.width === undefined) full.width = 640;
const logs = [];
const logger = { level() { return this; }, warn: (...m) => logs.push(m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERROR ' + m.join(' ')) };
const vg = vl.compile(full, { config: theme('light'), logger }).spec;
console.log(logs);
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
const ds = a.datasets.find(d => d.name === ch.dataset);
view.data(ch.dataset, ds.rows.map(r => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]]))));
for (const n of (ch.extra_datasets||[])) { const d2 = a.datasets.find(d => d.name === n); view.data(n, d2.rows.map(r => Object.fromEntries(d2.columns.map((c, i) => [c.name, r[i]])))); }
await view.runAsync();
const svg = await view.toSVG();
fs.writeFileSync('proto_'+cid+'.svg', svg); console.log(svg.slice(0,300)); const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
fs.writeFileSync(`proto_${cid}.png`, png);
console.log('wrote proto_' + cid + '.png');
