// Validate edition analyses and render preview PNGs.
//
//   node tools/validate_analysis.mjs data/analyses/<id>.json [...]
//   node tools/validate_analysis.mjs --all
//
// Checks: JSON schema, source references exist, dataset shape and types,
// printed numbers really occur in the cited source blocks (non-derived
// columns), Vega-Lite compiles in both languages without warnings, no dual
// y-axes, no hard-coded data/config. Writes previews to
// data/analyses/_preview/<id>__<chart>.png (open them with an image viewer).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Ajv from 'ajv';
import * as vl from 'vega-lite';
import * as vega from 'vega';
import { Resvg } from '@resvg/resvg-js';
import { theme, isComposite } from './vega_theme.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ANALYSES = path.join(ROOT, 'data', 'analyses');
const PREVIEW = path.join(ANALYSES, '_preview');
const schema = JSON.parse(fs.readFileSync(path.join(ROOT, 'schemas', 'analysis.schema.json'), 'utf8'));
const ajv = new Ajv({ allErrors: true, strict: false });
const validateSchema = ajv.compile(schema);

// page index: label -> page json
const pages = new Map();
for (const f of fs.readdirSync(path.join(ROOT, 'data', 'pages'))) {
  const p = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'pages', f), 'utf8'));
  pages.set(p.slug, p);
}
const sections = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'structure', 'structure.json'), 'utf8')).sections.map((s) => s.id));

function blockText(ref) {
  const p = pages.get(ref.page);
  if (!p) return null;
  const b = [...p.blocks, ...p.footnotes].find((x) => x.id === ref.block);
  if (!b) return null;
  if (b.grid) return b.grid.map((r) => r.join(' │ ')).join('\n') + (b.caption ? '\n' + b.caption : '');
  if (b.items) return b.items.map((i) => i.text).join('\n');
  return b.text;
}

const FRAC = { '½': 0.5, '¼': 0.25, '¾': 0.75, '⅓': 1 / 3, '⅔': 2 / 3, '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875 };
function numbersIn(text) {
  const out = new Set();
  const add = (v) => { if (Number.isFinite(v)) { out.add(+v.toFixed(6)); out.add(+(-v).toFixed(6)); } };
  // thousands separators: 75,367,300 or 75.367.300 ; decimals with comma or dot
  const re = /(\d{1,3}(?:[.,]\d{3}){1,4}(?![\d])|\d+(?:[.,]\d+)?)(\s?[½¼¾⅓⅔⅛⅜⅝⅞])?/g;
  let m;
  while ((m = re.exec(text))) {
    const raw = m[1];
    const frac = m[2] ? FRAC[m[2].trim()] : 0;
    const asDec = parseFloat(raw.replace(',', '.'));
    add(asDec + frac);
    if (/^\d{1,3}([.,]\d{3})+$/.test(raw)) add(parseFloat(raw.replace(/[.,]/g, '')) + frac);
    // "1112,9" -> also accept the integer part (tables sometimes split)
    add(Math.trunc(asDec));
  }
  // superscript-like split decimals "326 40" are not handled on purpose
  return out;
}

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

function walk(node, fn, p = []) {
  if (Array.isArray(node)) node.forEach((n, i) => walk(n, fn, [...p, i]));
  else if (node && typeof node === 'object') {
    fn(node, p);
    for (const [k, v] of Object.entries(node)) walk(v, fn, [...p, k]);
  }
}

export function rowsAsObjects(ds) {
  return ds.rows.map((r) => Object.fromEntries(ds.columns.map((c, i) => [c.name, r[i]])));
}

async function renderChart(a, chart, lang, mode, errors, warnings) {
  const spec = resolveLang(structuredClone(chart.vegalite), lang);
  const ds = a.datasets.find((d) => d.name === chart.dataset);
  if (!ds) { errors.push(`chart ${chart.id}: unknown dataset ${chart.dataset}`); return null; }
  if (spec.data && !spec.data.name) errors.push(`chart ${chart.id}: spec must not carry inline data/url - use the dataset`);
  if (spec.config) errors.push(`chart ${chart.id}: no "config" in specs - the edition theme is applied globally`);
  walk(spec, (n, p) => {
    if (n.resolve && n.resolve.scale && n.resolve.scale.y === 'independent') errors.push(`chart ${chart.id}: independent y scales (dual axis) are not allowed - use facets/small multiples`);
    if (n.data && n.data.url) errors.push(`chart ${chart.id}: external data url at ${p.join('.')}`);
  });
  const full = { $schema: 'https://vega.github.io/schema/vega-lite/v6.json', ...spec };
  if (!full.data) full.data = { name: chart.dataset };
  if (isComposite(full)) {
    full.autosize = { type: 'pad' };
    if (full.width === 'container') delete full.width;
  } else if (full.width === undefined || full.width === 'container') full.width = 640;
  const logs = [];
  const logger = { level() { return this; }, warn: (...m) => logs.push(m.join(' ')), info() {}, debug() {}, error: (...m) => logs.push('ERROR ' + m.join(' ')) };
  let vgSpec;
  try {
    vgSpec = vl.compile(full, { config: theme(mode), logger }).spec;
  } catch (e) {
    errors.push(`chart ${chart.id} [${lang}]: Vega-Lite compile error: ${e.message}`);
    return null;
  }
  for (const l of logs) warnings.push(`chart ${chart.id} [${lang}]: ${l}`);
  try {
    const view = new vega.View(vega.parse(vgSpec), { renderer: 'none' });
    const names = new Set([chart.dataset, ...(chart.extra_datasets || [])]);
    for (const n of names) {
      const d = a.datasets.find((x) => x.name === n);
      if (!d) { errors.push(`chart ${chart.id}: unknown extra dataset ${n}`); continue; }
      try { view.data(n, rowsAsObjects(d)); } catch { /* dataset not referenced */ }
    }
    await view.runAsync();
    const svg = await view.toSVG();
    return svg;
  } catch (e) {
    errors.push(`chart ${chart.id} [${lang}]: Vega runtime error: ${e.message}`);
    return null;
  }
}

export async function validate(file, { preview = true } = {}) {
  const errors = [];
  const warnings = [];
  let a;
  try { a = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return { file, errors: [`invalid JSON: ${e.message}`], warnings }; }
  if (!validateSchema(a)) for (const e of validateSchema.errors) errors.push(`schema: ${e.instancePath || '/'} ${e.message}${e.params && e.params.additionalProperty ? ' (' + e.params.additionalProperty + ')' : ''}${e.params && e.params.allowedValues ? ' ' + JSON.stringify(e.params.allowedValues) : ''}`);
  if (errors.length) return { file, id: a.id, errors, warnings };
  if (path.basename(file, '.json') !== a.id) errors.push(`file name must equal id (${a.id}.json)`);
  if (!sections.has(a.section)) errors.push(`unknown section ${a.section}`);
  const refs = [...a.sources, ...a.datasets.flatMap((d) => d.source_refs)];
  for (const r of refs) if (blockText(r) === null) errors.push(`source not found: page ${r.page} block ${r.block}`);
  // datasets ---------------------------------------------------------------
  const names = new Set();
  for (const ds of a.datasets) {
    if (names.has(ds.name)) errors.push(`duplicate dataset ${ds.name}`);
    names.add(ds.name);
    const cn = new Set();
    for (const c of ds.columns) { if (cn.has(c.name)) errors.push(`${ds.name}: duplicate column ${c.name}`); cn.add(c.name); }
    ds.rows.forEach((r, i) => {
      if (r.length !== ds.columns.length) errors.push(`${ds.name}: row ${i + 1} has ${r.length} values, ${ds.columns.length} columns`);
      ds.columns.forEach((c, j) => {
        const v = r[j];
        if (v === null || v === undefined) return;
        if ((c.type === 'integer' && !Number.isInteger(v)) || (c.type === 'number' && typeof v !== 'number')) errors.push(`${ds.name}: row ${i + 1} col ${c.name} expects ${c.type}, got ${JSON.stringify(v)}`);
        if ((c.type === 'string' || c.type === 'date') && typeof v !== 'string') errors.push(`${ds.name}: row ${i + 1} col ${c.name} expects ${c.type} string, got ${JSON.stringify(v)}`);
      });
    });
    // printed-number cross-check
    const text = ds.source_refs.map(blockText).filter(Boolean).join('\n');
    const avail = numbersIn(text);
    let checked = 0;
    const missing = [];
    ds.columns.forEach((c, j) => {
      if (c.derived || !(c.type === 'integer' || c.type === 'number')) return;
      for (const r of ds.rows) {
        const v = r[j];
        if (typeof v !== 'number') continue;
        checked++;
        if (!avail.has(+v.toFixed(6))) missing.push(`${c.name}=${v}`);
      }
    });
    if (checked) {
      const share = missing.length / checked;
      const msg = `${ds.name}: ${missing.length}/${checked} printed values not found in the cited source blocks${missing.length ? ' e.g. ' + missing.slice(0, 8).join(', ') : ''}`;
      if (share > 0.05) errors.push(msg + ' - fix the values, cite the right blocks, or mark computed columns "derived": true');
      else if (missing.length) warnings.push(msg);
    }
  }
  // charts -------------------------------------------------------------------
  if (preview) fs.mkdirSync(PREVIEW, { recursive: true });
  for (const ch of a.charts) {
    for (const lang of ['de', 'en']) {
      const svg = await renderChart(a, ch, lang, 'light', errors, warnings);
      if (svg && preview && lang === 'de') {
        const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1100 }, background: '#fbf8f1', font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' } }).render().asPng();
        fs.writeFileSync(path.join(PREVIEW, `${a.id}__${ch.id}.png`), png);
      }
    }
    // dark mode compiles too
    await renderChart(a, ch, 'en', 'dark', errors, warnings);
  }
  return { file, id: a.id, errors, warnings: [...new Set(warnings)] };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  let files = process.argv.slice(2);
  if (files.includes('--all')) files = fs.readdirSync(ANALYSES).filter((f) => f.endsWith('.json')).map((f) => path.join(ANALYSES, f));
  let bad = 0;
  for (const f of files) {
    const r = await validate(f);
    const ok = r.errors.length === 0;
    if (!ok) bad++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} ${path.basename(f)}${r.warnings.length ? `  (${r.warnings.length} warnings)` : ''}`);
    for (const e of r.errors) console.log('   ERROR  ' + e);
    for (const w of r.warnings) console.log('   warn   ' + w);
    if (ok) console.log(`   previews: data/analyses/_preview/${r.id}__c*.png`);
  }
  process.exitCode = bad ? 1 : 0;
}
