// Compile every analysis chart to self-contained Vega specs (de/en x light/dark)
// and render a thumbnail per analysis.
//   node tools/compile_charts.mjs <out-dir>
// writes <out-dir>/specs/<id>.json and <out-dir>/thumbs/<id>.png
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { Resvg } from '@resvg/resvg-js';
import { theme, isComposite, applyTokens } from './vega_theme.mjs';

// resvg cannot handle empty paths (e.g. line segments that collapse when projected)
const cleanSvg = (svg) => svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
import { rowsAsObjects, validate } from './validate_analysis.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.resolve(process.argv[2] || path.join(ROOT, 'site', 'auswertungen'));
fs.mkdirSync(path.join(OUT, 'specs'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'thumbs'), { recursive: true });

function resolveLang(node, lang) {
  if (Array.isArray(node)) return node.map((n) => resolveLang(n, lang));
  if (node && typeof node === 'object') {
    const k = Object.keys(node);
    if (k.length === 2 && k.includes('de') && k.includes('en') && typeof node.de === 'string') return node[lang];
    const o = {};
    for (const [kk, v] of Object.entries(node)) o[kk] = resolveLang(v, lang);
    return o;
  }
  return node;
}

function compile(a, ch, lang, mode, width) {
  const spec = applyTokens(resolveLang(structuredClone(ch.vegalite), lang), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
  if (!full.data) full.data = { name: ch.dataset };
  if (isComposite(full)) {
    full.autosize = { type: 'pad' };
    if (full.width === 'container') delete full.width;
  } else {
    full.width = width || 'container';
    if (width) full.autosize = { type: 'fit-x', contains: 'padding' };
  }
  const vgSpec = vl.compile(full, { config: theme(mode), logger: { level() { return this; }, warn() {}, info() {}, debug() {}, error() {} } }).spec;
  // inline the datasets so the spec is self-contained
  const names = new Set([ch.dataset, ...(ch.extra_datasets || [])]);
  for (const d of vgSpec.data || []) {
    if (names.has(d.name) && !d.values && !d.source && !d.url) {
      const ds = a.datasets.find((x) => x.name === d.name);
      d.values = rowsAsObjects(ds);
    }
  }
  return vgSpec;
}

const files = fs.readdirSync(path.join(ROOT, 'data', 'analyses')).filter((f) => f.endsWith('.json'));
let ok = 0, bad = 0;
const index = [];
for (const f of files) {
  const file = path.join(ROOT, 'data', 'analyses', f);
  const v = await validate(file, { preview: false });
  if (v.errors.length) { bad++; console.log('SKIP (invalid)', f, v.errors[0]); continue; }
  const a = JSON.parse(fs.readFileSync(file, 'utf8'));
  const out = {};
  try {
    for (const ch of a.charts) {
      out[ch.id] = {};
      for (const lang of ['de', 'en']) for (const mode of ['light', 'dark']) out[ch.id][`${lang}_${mode}`] = compile(a, ch, lang, mode);
    }
    fs.writeFileSync(path.join(OUT, 'specs', `${a.id}.json`), JSON.stringify(out));
    // thumbnail: first chart, German, light, fixed width
    const th = compile(a, a.charts[0], 'de', 'light', 560);
    const view = new vega.View(vega.parse(th), { renderer: 'none' });
    await view.runAsync();
    const svg = await view.toSVG();
    const png = new Resvg(cleanSvg(svg), { fitTo: { mode: 'width', value: 640 }, background: '#fffdf8', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
    fs.writeFileSync(path.join(OUT, 'thumbs', `${a.id}.png`), png);
    index.push(a.id);
    ok++;
  } catch (e) {
    bad++;
    console.log('FAIL', f, e.message);
  }
}
console.log(`compiled ${ok} analyses, skipped ${bad}`);
