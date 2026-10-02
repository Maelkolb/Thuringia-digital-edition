// run from the tools directory:  cd tools && FILE=... CHART=c1 LANG=de MODE=light node --input-type=module < ../data/analyses/_work/F3/svg.mjs
import fs from 'node:fs';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { Resvg } from '@resvg/resvg-js';
import { theme, isComposite, applyTokens } from './vega_theme.mjs';

const file = process.env.FILE;
const chartId = process.env.CHART || 'c1';
const lang = process.env.LNG || 'de';
const mode = process.env.MODE || 'light';
const out = process.env.OUT || `../data/analyses/_work/F3/out_${chartId}_${lang}_${mode}.png`;
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const ch = a.charts.find((c) => c.id === chartId);

function resolveLang(node, l) {
  if (Array.isArray(node)) return node.map((n) => resolveLang(n, l));
  if (node && typeof node === 'object') {
    const keys = Object.keys(node);
    if (keys.length === 2 && keys.includes('de') && keys.includes('en') && typeof node.de === 'string') return node[l];
    const o = {};
    for (const [k, v] of Object.entries(node)) o[k] = resolveLang(v, l);
    return o;
  }
  return node;
}
const rowsAsObjects = (ds) => ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));
const cleanSvg = (svg) => svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');

const spec = applyTokens(resolveLang(structuredClone(ch.vegalite), lang), mode);
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
if (!full.data) full.data = { name: ch.dataset };
if (isComposite(full)) {
  full.autosize = { type: 'pad' };
  if (full.width === 'container') delete full.width;
} else if (full.width === undefined || full.width === 'container') full.width = 640;
const logs = [];
const logger = { level() { return this; }, warn: (...m) => logs.push(m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERROR ' + m.join(' ')) };
const vg = vl.compile(full, { config: theme(mode), logger }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of new Set([ch.dataset, ...(ch.extra_datasets || [])])) {
  const ds = a.datasets.find((d) => d.name === n);
  try { view.data(n, rowsAsObjects(ds)); } catch (e) { /* unused */ }
}
await view.runAsync();
const svg = await view.toSVG();
fs.writeFileSync(out.replace('.png', '.svg'), svg);
const m = svg.match(/width="([\d.]+)" height="([\d.]+)"/);
console.log('logs:', [...new Set(logs)].join(' | '));
console.log('svg size', m && m.slice(1, 3).join('x'));
if (m && +m[1] > 0 && +m[2] > 0) {
  const png = new Resvg(cleanSvg(svg), { fitTo: { mode: 'width', value: 1100 }, background: mode === 'dark' ? '#1d1b18' : '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  fs.writeFileSync(out, png);
  console.log('wrote', out);
}
