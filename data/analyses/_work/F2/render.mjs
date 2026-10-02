// node render.mjs <feature-id> <chart-id> [de|en] [light|dark] [width]
// Renders one chart to _work/F2/out/<id>__<chart>__<lang>__<mode>.png using the project theme.
import fs from 'node:fs';
import path from 'node:path';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { Resvg } from '@resvg/resvg-js';
import { theme, isComposite, applyTokens } from '../../../../tools/vega_theme.mjs';
import { rowsAsObjects } from '../../../../tools/validate_analysis.mjs';

const [id, chartId, lang = 'de', mode = 'light', widthArg = '640'] = process.argv.slice(2);
const root = path.resolve('../../../..');
const a = JSON.parse(fs.readFileSync(path.join(root, 'data', 'analyses', `${id}.json`), 'utf8'));
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

const spec = applyTokens(resolveLang(structuredClone(ch.vegalite), lang), mode);
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, ...spec };
if (isComposite(full)) full.autosize = { type: 'pad' };
else if (full.width === undefined || full.width === 'container') full.width = Number(widthArg);
const logs = [];
const logger = { level() { return this; }, warn: (...m) => logs.push(m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERROR ' + m.join(' ')) };
const vg = vl.compile(full, { config: theme(mode), logger }).spec;
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of [ch.dataset, ...(ch.extra_datasets || [])]) {
  const d = a.datasets.find((x) => x.name === n);
  try { view.data(n, rowsAsObjects(d)); } catch { /* unused */ }
}
await view.runAsync();
const svg = await view.toSVG();
const clean = svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
const bg = mode === 'dark' ? '#1d1b18' : '#fbf8f1';
const png = new Resvg(clean, { fitTo: { mode: 'width', value: 1100 }, background: bg, font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
fs.mkdirSync('out', { recursive: true });
const outFile = path.join('out', `${id}__${chartId}__${lang}__${mode}.png`);
fs.writeFileSync(outFile, png);
console.log(path.resolve(outFile), logs.join(' | '));
