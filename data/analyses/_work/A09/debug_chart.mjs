// Debug helper: render one chart of an analysis and print the svg header + warnings.
//   node data/analyses/_work/A09/debug_chart.mjs data/analyses/<id>.json c2 [de|en]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const TOOLS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../../tools');
const req = createRequire(path.join(TOOLS, 'package.json'));
const vl = await import(pathToFileURL(req.resolve('vega-lite')).href);
const vega = await import(pathToFileURL(req.resolve('vega')).href);
const { theme } = await import(pathToFileURL(path.join(TOOLS, 'vega_theme.mjs')).href);

const [file, cid, lang = 'de'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const ch = a.charts.find((c) => c.id === cid);
function res(n) { if (Array.isArray(n)) return n.map(res); if (n && typeof n === 'object') { const k = Object.keys(n); if (k.length === 2 && k.includes('de') && k.includes('en') && typeof n.de === 'string') return n[lang]; return Object.fromEntries(Object.entries(n).map(([x, y]) => [x, res(y)])); } return n; }
const spec = res(structuredClone(ch.vegalite));
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, width: 640, ...spec };
const logs = [];
const logger = { level() { return this; }, warn: (...m) => logs.push('WARN ' + m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERROR ' + m.join(' ')) };
const vg = vl.compile(full, { config: theme('light'), logger }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
const names = new Set([ch.dataset, ...(ch.extra_datasets || [])]);
for (const n of names) {
  const d = a.datasets.find((x) => x.name === n);
  const rows = d.rows.map((r) => Object.fromEntries(d.columns.map((c, i) => [c.name, r[i]])));
  try { view.data(n, rows); } catch (e) { console.log('data err', n, e.message); }
}
await view.runAsync();
const svg = await view.toSVG();
console.log(svg.slice(0, 300));
console.log(logs.join('\n'));
