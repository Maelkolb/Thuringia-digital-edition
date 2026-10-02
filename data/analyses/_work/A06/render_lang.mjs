// Renders the English (or German) version of an analysis' charts to PNG for visual checking.
//   node render_lang.mjs <analysis-id> [en|de]  -> data/analyses/_work/A06/_en/<id>__<chart>.png
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = 'C:/Users/totom/Projects/reuss-edition';
const T = ROOT + '/tools/node_modules/';
const vl = await import(pathToFileURL(T + 'vega-lite/build/index.js').href);
const vega = await import(pathToFileURL(T + 'vega/build/vega-node.js').href).catch(() => import(pathToFileURL(T + 'vega/build/vega.module.js').href));
const { Resvg } = await import(pathToFileURL(T + '@resvg/resvg-js/index.js').href);
const { theme } = await import(pathToFileURL(ROOT + '/tools/vega_theme.mjs').href);

function resolveLang(node, lang) {
  if (Array.isArray(node)) return node.map((n) => resolveLang(n, lang));
  if (node && typeof node === 'object') {
    const keys = Object.keys(node);
    if (keys.length === 2 && keys.includes('de') && keys.includes('en') && typeof node.de === 'string') return node[lang];
    const o = {};
    for (const [k, v] of Object.entries(node)) o[k] = resolveLang(v, lang);
    return o;
  }
  return node;
}

const id = process.argv[2];
const lang = process.argv[3] || 'en';
const a = JSON.parse(fs.readFileSync(`${ROOT}/data/analyses/${id}.json`, 'utf8'));
const out = `${ROOT}/data/analyses/_work/A06/_${lang}`;
fs.mkdirSync(out, { recursive: true });
for (const ch of a.charts) {
  const spec = resolveLang(structuredClone(ch.vegalite), lang);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec, data: { name: ch.dataset } };
  if (full.width === undefined) full.width = 640;
  const vg = vl.compile(full, { config: theme('light') }).spec;
  const view = new vega.View(vega.parse(vg), { renderer: 'none' });
  const ds = a.datasets.find((d) => d.name === ch.dataset);
  view.data(ch.dataset, ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]]))));
  await view.runAsync();
  const svg = await view.toSVG();
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  fs.writeFileSync(path.join(out, `${id}__${ch.id}.png`), png);
  console.log('wrote', `${id}__${ch.id}.png`);
}
