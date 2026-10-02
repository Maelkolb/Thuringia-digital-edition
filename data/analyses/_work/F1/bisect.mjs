import fs from 'node:fs';
import * as vl from '../../../../tools/node_modules/vega-lite/build/index.js';
const [file, chartId] = process.argv.slice(2);
const a = JSON.parse(fs.readFileSync(file, 'utf8'));
const ch = a.charts.find((c) => c.id === chartId);
const de = (n) => (Array.isArray(n) ? n.map(de) : n && typeof n === 'object' ? (Object.keys(n).length === 2 && 'de' in n && 'en' in n ? n.de : Object.fromEntries(Object.entries(n).map(([k, v]) => [k, de(v)]))) : n);
const spec = de(structuredClone(ch.vegalite));
const panel = spec.vconcat ? spec.vconcat[0] : spec;
for (let i = 0; i < panel.layer.length; i++) {
  const p = structuredClone(panel);
  p.layer = [p.layer[i]];
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', data: { name: ch.dataset }, ...p };
  try { vl.compile(full); console.log('layer', i, 'ok'); } catch (e) { console.log('layer', i, 'FAIL', e.message); }
}
