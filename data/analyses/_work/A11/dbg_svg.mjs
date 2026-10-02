// debug helper: prints svg root attributes for chart i of an analysis file (run with cwd=tools)
import fs from 'node:fs';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { theme } from './vega_theme.mjs';
const a = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ch = a.charts[+process.argv[3] || 0];
const res = (n) => Array.isArray(n) ? n.map(res) : (n && typeof n === 'object') ? ((Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string') ? n.de : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, res(v)]))) : n;
const spec = res(ch.vegalite); spec.width = spec.width ?? 640; spec.data = { name: ch.dataset };
const vg = vl.compile({ $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec }, { config: theme('light') }).spec;
const ds = a.datasets.find((d) => d.name === ch.dataset);
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
view.data(ch.dataset, ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]]))));
await view.runAsync();
const svg = await view.toSVG();
console.log(svg.slice(0, 300));
