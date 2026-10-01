// Fast probe: loads the search page once, then submits each query through the form (index and shards stay cached).
//   node data/search/qa/probe_fast.mjs queries.txt out.json [lang]
import { chromium } from 'file:///C:/Users/totom/Projects/reuss-edition/tools/node_modules/playwright-core/index.mjs';
import fs from 'node:fs';
const [file, out] = process.argv.slice(2);
const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/).map((s) => s.trim());
const queries = []; let cat = '';
for (const l of lines) { if (!l) continue; if (l.startsWith('#')) { cat = l.replace(/^#\s*-*\s*/, ''); continue; } queries.push({ q: l, cat }); }
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'de-DE' });
const page = await ctx.newPage();
// serve the SOURCE search.js (snapshot) instead of the possibly stale built copy
const jsOverride = process.env.SEARCH_JS;
if (jsOverride) await page.route((u) => /assets\/js\/search\.js/.test(u.toString()), (route) => route.fulfill({ path: jsOverride, contentType: 'application/javascript' }));
await page.goto('http://127.0.0.1:8642/suche.html', { waitUntil: 'networkidle' });
const results = [];
for (const { q, cat } of queries) {
  await page.evaluate((q) => {
    document.querySelector('[data-search-status]').textContent = '';
    const f = document.querySelector('[data-search-form]'); f.querySelector('input').value = q; f.requestSubmit();
  }, q);
  await page.waitForFunction(() => document.querySelector('[data-search-status]').textContent.trim() !== '', null, { timeout: 15000 }).catch(() => {});
  await page.waitForFunction(() => {
    const rs = Array.from(document.querySelectorAll('.result')).slice(0, 8);
    return rs.every((d) => { const k = d.querySelector('.pill').innerText; return !['Fließtext','Überschrift','Tabelle','Liste','Fußnote','Seitenübersicht'].includes(k) || d.querySelector('.snip').innerText.trim() !== ''; });
  }, null, { timeout: 4000 }).catch(() => {});
  await page.waitForTimeout(60);
  const r = await page.evaluate(() => {
    const st = document.querySelector('[data-search-status]').innerText;
    const dym = document.querySelector('[data-dym]').innerText;
    const ents = Array.from(document.querySelectorAll('[data-entity-hits] a')).map((a) => a.innerText.replace(/\s+/g, ' '));
    const all = Array.from(document.querySelectorAll('.result'));
    const hits = all.slice(0, 8).map((d) => ({
      title: d.querySelector('.rt a').innerText, kind: d.querySelector('.pill').innerText,
      where: d.querySelector('.where').innerText, href: d.querySelector('.rt a').getAttribute('href'), snippet: (d.querySelector('.snip').innerText || '').slice(0, 260),
    }));
    return { status: st, didyoumean: dym, entities: ents, shown: all.length, hits };
  });
  results.push({ q, cat, ...r });
  console.log(`### ${q}  ->  ${r.status.split('\n')[0]}${r.didyoumean ? '  [' + r.didyoumean + ']' : ''}`);
}
if (out) fs.writeFileSync(out, JSON.stringify(results, null, 1));
await browser.close();
