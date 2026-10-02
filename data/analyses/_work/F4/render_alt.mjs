// Render English and/or dark previews of a feature chart into _work/F4/prev/
// usage: node render_alt.mjs <feature-id> <lang: de|en> <mode: light|dark> [chart ids...]
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const TOOLS = 'C:/Users/totom/Projects/reuss-edition/tools/';
const require = createRequire(TOOLS + 'package.json');
const vl = await import(pathToFileURL(TOOLS + 'node_modules/vega-lite/build/index.js').href);
const vega = await import(pathToFileURL(TOOLS + 'node_modules/vega/build/vega.module.js').href);
const { Resvg } = require('@resvg/resvg-js');
const { theme, isComposite, applyTokens } = await import(pathToFileURL(TOOLS + 'vega_theme.mjs').href);

const [id, lang = 'en', mode = 'light', ...only] = process.argv.slice(2);
const root = 'C:/Users/totom/Projects/reuss-edition/data/analyses/';
const a = JSON.parse(fs.readFileSync(root + id + '.json', 'utf8'));

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
const cleanSvg = (svg) => svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
const outDir = 'C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F4/prev/';
fs.mkdirSync(outDir, { recursive: true });

for (const ch of a.charts) {
  if (only.length && !only.includes(ch.id)) continue;
  const spec = applyTokens(resolveLang(structuredClone(ch.vegalite), lang), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
  if (!full.data) full.data = { name: ch.dataset };
  if (isComposite(full)) { full.autosize = { type: 'pad' }; if (full.width === 'container') delete full.width; }
  else if (full.width === undefined || full.width === 'container') full.width = 640;
  const vg = vl.compile(full, { config: theme(mode) }).spec;
  const view = new vega.View(vega.parse(vg), { renderer: 'none' });
  for (const n of new Set([ch.dataset, ...(ch.extra_datasets || [])])) {
    const d = a.datasets.find((x) => x.name === n);
    try { view.data(n, d.rows.map((r) => Object.fromEntries(d.columns.map((c, i) => [c.name, r[i]])))); } catch {}
  }
  await view.runAsync();
  const svg = await view.toSVG();
  const png = new Resvg(cleanSvg(svg), { fitTo: { mode: 'width', value: 1100 }, background: mode === 'dark' ? '#1d1b18' : '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  const f = path.join(outDir, `${id}__${ch.id}__${lang}_${mode}.png`);
  fs.writeFileSync(f, png);
  console.log(f);
}
