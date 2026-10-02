// Render one analysis chart to SVG (no PNG) to debug rendering problems.
//   node tools/debug_svg.mjs <analysis.json> <chart-id> [layers-to-keep, e.g. 0,2]
import fs from 'node:fs';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { theme, applyTokens } from './vega_theme.mjs';
import { rowsAsObjects } from './validate_analysis.mjs';

const [file, chartId, keep] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const ch = a.charts.find((c) => c.id === chartId);
const de = (n) => (Array.isArray(n) ? n.map(de) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n ? n.de : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, de(v)]))) : n);
const spec = applyTokens(de(structuredClone(ch.vegalite)), 'light');
if (keep && spec.layer) spec.layer = keep.split(',').map(Number).map((i) => spec.layer[i]);
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, width: 640, ...spec };
const vg = vl.compile(full, { config: theme('light') }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of [ch.dataset, ...(ch.extra_datasets || [])]) { try { view.data(n, rowsAsObjects(a.datasets.find((d) => d.name === n))); } catch { /* unused */ } }
await view.runAsync();
const svg = await view.toSVG();
fs.writeFileSync('debug.svg', svg);
console.log('svg bytes', svg.length, 'NaN:', (svg.match(/NaN/g) || []).length, 'empty paths:', (svg.match(/d=""/g) || []).length, 'single-point paths:', (svg.match(/d="M[-\d.]+,[-\d.]+Z?"/g) || []).length);
