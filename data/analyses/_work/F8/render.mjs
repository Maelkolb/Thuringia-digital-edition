// node render.mjs <feature-id> <chart-id> [width] [light|dark] [out.png]
// renders one chart like the validator, but with a chosen width and mode; writes into _work/F8/out/
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const T = 'C:/Users/totom/Projects/reuss-edition/tools';
const vl = await import(pathToFileURL(`${T}/node_modules/vega-lite/build/index.js`).href);
const vega = await import(pathToFileURL(`${T}/node_modules/vega/build/vega.module.js`).href);
const { theme, isComposite, applyTokens } = await import(pathToFileURL(`${T}/vega_theme.mjs`).href);
const require = createRequire(`${T}/package.json`);
const { Resvg } = require('@resvg/resvg-js');

const [fid, cid, widthArg, modeArg, outArg] = process.argv.slice(2);
const width = Number(widthArg || 640);
const mode = modeArg || 'light';
const lang = process.env.LANG_RENDER || 'de';
const a = JSON.parse(fs.readFileSync(`C:/Users/totom/Projects/reuss-edition/data/analyses/${fid}.json`, 'utf8'));
const ch = a.charts.find((c) => c.id === cid);

function resolveLang(node) {
  if (Array.isArray(node)) return node.map(resolveLang);
  if (node && typeof node === 'object') {
    const keys = Object.keys(node);
    if (keys.length === 2 && keys.includes('de') && keys.includes('en') && typeof node.de === 'string') return node[lang];
    const o = {};
    for (const [k, v] of Object.entries(node)) o[k] = resolveLang(v);
    return o;
  }
  return node;
}
const rowsAsObjects = (ds) => ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));

const spec = applyTokens(resolveLang(structuredClone(ch.vegalite)), mode);
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
if (!full.data) full.data = { name: ch.dataset };
if (isComposite(full)) {
  full.autosize = { type: 'pad' };
} else full.width = width;
const vg = vl.compile(full, { config: theme(mode) }).spec;
if (process.env.DUMP) { const f=(n,p='')=>{ if(Array.isArray(n)) n.forEach((x,i)=>f(x,p+'['+i+']')); else if(n&&typeof n==='object'){ if(n.labelLimit!==undefined||n.scale&&n.orient) console.log(p, JSON.stringify(n).slice(0,300)); for(const [k,v] of Object.entries(n)) f(v,p+'.'+k);} }; f(vg); }
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const n of new Set([ch.dataset, ...(ch.extra_datasets || [])])) {
  try { view.data(n, rowsAsObjects(a.datasets.find((d) => d.name === n))); } catch { /* unused */ }
}
await view.runAsync();
const svg = await view.toSVG();
const clean = svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
const png = new Resvg(clean, { fitTo: { mode: 'zoom', value: 1.5 }, background: mode === 'dark' ? '#1d1b18' : '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
fs.mkdirSync('C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F8/out', { recursive: true });
const out = outArg || `C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F8/out/${fid}__${cid}__${width}${mode === 'dark' ? '_dark' : ''}${lang === 'en' ? '_en' : ''}.png`;
fs.writeFileSync(out, png);
console.log(out);
