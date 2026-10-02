import fs from 'node:fs';
const T = 'file:///C:/Users/totom/Projects/reuss-edition/tools/';
const vl = await import(T + 'node_modules/vega-lite/build/index.js');
const vega = await import(T + 'node_modules/vega/build/vega-node.js').catch(async () => await import(T + 'node_modules/vega/index.js'));
const { theme } = await import(T + 'vega_theme.mjs');
const a = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ch = a.charts[0];
function res(n, lang) { if (Array.isArray(n)) return n.map(x => res(x, lang)); if (n && typeof n === 'object') { const k = Object.keys(n); if (k.length === 2 && k.includes('de') && k.includes('en') && typeof n.de === 'string') return n[lang]; const o = {}; for (const [kk, v] of Object.entries(n)) o[kk] = res(v, lang); return o; } return n; }
const spec = res(structuredClone(ch.vegalite), 'de');
const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec, data: { name: ch.dataset }, width: 640 };
const logs = [];
const logger = { level() { return this; }, warn: (...m) => logs.push(m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERR ' + m.join(' ')) };
const vg = vl.compile(full, { config: theme('light'), logger }).spec;
console.log(JSON.stringify(vg.projections, null, 1));
console.log(logs);
const view = new vega.View(vega.parse(vg), { renderer: 'none' });
for (const d of a.datasets) { const rows = d.rows.map(r => Object.fromEntries(d.columns.map((c, i) => [c.name, r[i]]))); try { view.data(d.name, rows); } catch {} }
await view.runAsync();
const svg = await view.toSVG();
console.log(svg.slice(0, 300));
fs.writeFileSync(process.argv[3] || 'dump.svg', svg);
