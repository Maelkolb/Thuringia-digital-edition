// Render the charts of an analysis in English (the validator only writes the German previews).
import fs from 'node:fs';
const T = 'file:///C:/Users/totom/Projects/reuss-edition/tools/node_modules/';
const vl = await import(T + 'vega-lite/build/index.js');
const vega = await import(T + 'vega/build/vega.module.js');
const { Resvg } = await import(T + '@resvg/resvg-js/index.js');
const { theme } = await import('file:///C:/Users/totom/Projects/reuss-edition/tools/vega_theme.mjs');
const [file, lang, outdir, ...only] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
function res(n, l) { if (Array.isArray(n)) return n.map(x => res(x, l)); if (n && typeof n === 'object') { const k = Object.keys(n); if (k.length === 2 && k.includes('de') && k.includes('en') && typeof n.de === 'string') return n[l]; const o = {}; for (const [kk, v] of Object.entries(n)) o[kk] = res(v, l); return o; } return n; }
fs.mkdirSync(outdir, { recursive: true });
for (const ch of a.charts) {
  if (only.length && !only.includes(ch.id)) continue;
  const spec = res(structuredClone(ch.vegalite), lang);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec, data: { name: ch.dataset } };
  if (full.width === undefined) full.width = 640;
  const vg = vl.compile(full, { config: theme('light') }).spec;
  const ds = a.datasets.find(d => d.name === ch.dataset);
  const view = new vega.View(vega.parse(vg), { renderer: 'none' });
  view.data(ch.dataset, ds.rows.map(r => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]]))));
  await view.runAsync();
  const svg = await view.toSVG();
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  fs.writeFileSync(`${outdir}/${a.id}__${ch.id}_${lang}.png`, png);
}
console.log('done', a.id);
