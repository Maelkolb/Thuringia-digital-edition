import fs from 'node:fs';
import * as vl from '../../../../tools/node_modules/vega-lite/build/index.js';
import { theme, applyTokens } from '../../../../tools/vega_theme.mjs';
const [file, id] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const ch = a.charts.find((c) => c.id === id);
const res = (n) => (Array.isArray(n) ? n.map(res) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n.de : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, res(v)]))) : n);
const spec = applyTokens(res(structuredClone(ch.vegalite)), 'light');
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, width: 640, ...spec };
const vg = vl.compile(full, { config: theme('light') }).spec;
console.log(JSON.stringify(vg.scales, null, 1));
import * as vega from '../../../../tools/node_modules/vega/build/vega.module.js';
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of [ch.dataset, ...(ch.extra_datasets || [])]) { try { view.data(n, a.datasets.find((d) => d.name === n).rows.map((r) => Object.fromEntries(a.datasets.find((d) => d.name === n).columns.map((c, i) => [c.name, r[i]])))); } catch {} }
await view.runAsync();
console.log('x domain', view.scale('x').domain(), 'range', view.scale('x').range());
