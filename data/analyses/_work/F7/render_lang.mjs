// Renders every chart of an analysis in one language and mode to data/analyses/_work/F7/*.png.
// Copy into tools/ to run (it imports ./vega_theme.mjs and ./validate_analysis.mjs):  node tools/render_lang.mjs data/analyses/<id>.json en dark
import fs from 'node:fs';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { Resvg } from '@resvg/resvg-js';
import { theme, isComposite, applyTokens } from './vega_theme.mjs';
import { rowsAsObjects } from './validate_analysis.mjs';
const [file, lang = 'en', mode = 'light'] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const resolveLang = (n) => (Array.isArray(n) ? n.map(resolveLang) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n && typeof n.de === 'string' ? n[lang] : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, resolveLang(v)]))) : n);
const cleanSvg = (svg) => svg.replace(/<path\b[^>]*\sd=""[^>]*?(\/>|><\/path>)/g, '');
for (const ch of a.charts) {
  const spec = applyTokens(resolveLang(structuredClone(ch.vegalite)), mode);
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, ...spec };
  if (isComposite(full)) full.autosize = { type: 'pad' }; else full.width = 640;
  const vg = vl.compile(full, { config: theme(mode) }).spec;
  const view = new vega.View(vega.parse(vg), { renderer: 'none' });
  for (const n of [ch.dataset, ...(ch.extra_datasets || [])]) { try { view.data(n, rowsAsObjects(a.datasets.find((d) => d.name === n))); } catch { } }
  await view.runAsync();
  const svg = await view.toSVG();
  const bg = mode === 'dark' ? '#1d1b18' : '#fbf8f1';
  const png = new Resvg(cleanSvg(svg), { fitTo: { mode: 'width', value: 1100 }, background: bg, font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
  fs.writeFileSync(`data/analyses/_work/F7/${a.id}__${ch.id}__${lang}_${mode}.png`, png);
  console.log('wrote', a.id, ch.id, lang, mode);
}
