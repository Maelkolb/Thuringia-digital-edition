// node preview.mjs <analysis.json> [lang=en] [mode=light] -> writes data/analyses/_work/F1/prev/<id>__<chart>__<lang>_<mode>.png
import fs from 'node:fs';
import path from 'node:path';
import * as vl from '../../../../tools/node_modules/vega-lite/build/index.js';
import * as vega from '../../../../tools/node_modules/vega/build/vega.module.js';
import { Resvg } from '../../../../tools/node_modules/@resvg/resvg-js/index.js';
import { theme, isComposite, applyTokens } from '../../../../tools/vega_theme.mjs';
const [file, lang = 'en', mode = 'light'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const res = (n) => (Array.isArray(n) ? n.map(res) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n[lang] : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, res(v)]))) : n);
const out = path.join(path.dirname(file), '_work', 'F1', 'prev');
fs.mkdirSync(out, { recursive: true });
const rows = (ds) => ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));
for (const ch of a.charts) {
  const spec = applyTokens(res(structuredClone(ch.vegalite)), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, ...spec };
  if (isComposite(full)) full.autosize = { type: 'pad' }; else full.width = 640;
  const vg = vl.compile(full, { config: theme(mode), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error() {} } }).spec;
  const view = new vega.View(vega.parse(vg), { renderer: 'none' });
  for (const n of [ch.dataset, ...(ch.extra_datasets || [])]) { try { view.data(n, rows(a.datasets.find((d) => d.name === n))); } catch {} }
  await view.runAsync();
  let svg = await view.toSVG();
  svg = svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
  const bg = mode === 'dark' ? '#1d1b18' : '#fbf8f1';
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: bg, font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  fs.writeFileSync(path.join(out, `${a.id}__${ch.id}__${lang}_${mode}.png`), png);
}
console.log('ok');
