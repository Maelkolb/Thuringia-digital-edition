// Run queries against the built edition's search page (needs the local server on :8642).
//   node tools/search_probe.mjs queries.txt [out.json]
// queries.txt: one query per line. Prints status + top 8 hits per query.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
const [file, out] = process.argv.slice(2);
const queries = fs.readFileSync(file, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter((s) => s && !s.startsWith('#'));
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'de-DE' });
const page = await ctx.newPage();
const results = [];
for (const q of queries) {
  await page.goto('http://127.0.0.1:8642/suche.html?q=' + encodeURIComponent(q), { waitUntil: 'networkidle' });
  await page.waitForTimeout(700);
  const r = await page.evaluate(() => {
    const st = document.querySelector('[data-search-status]').innerText;
    const dym = document.querySelector('[data-dym]').innerText;
    const ents = Array.from(document.querySelectorAll('[data-entity-hits] a')).map((a) => a.innerText.replace(/\s+/g, ' '));
    const hits = Array.from(document.querySelectorAll('.result')).slice(0, 8).map((d) => ({
      title: d.querySelector('.rt a').innerText, kind: d.querySelector('.pill').innerText,
      where: d.querySelector('.where').innerText, snippet: (d.querySelector('.snip').innerText || '').slice(0, 220),
    }));
    return { status: st, didyoumean: dym, entities: ents, hits };
  });
  results.push({ q, ...r });
  console.log(`\n### ${q}  ->  ${r.status}${r.didyoumean ? '  [' + r.didyoumean + ']' : ''}`);
  if (r.entities.length) console.log('   entities: ' + r.entities.slice(0, 5).join(' | '));
  for (const h of r.hits) console.log(`   - ${h.title} [${h.kind}] ${h.where} :: ${h.snippet.replace(/\n/g, ' ').slice(0, 140)}`);
}
if (out) fs.writeFileSync(out, JSON.stringify(results, null, 1));
await browser.close();
