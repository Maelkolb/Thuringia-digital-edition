// Check that norm.js (client) and norm.py (index) agree on the whole corpus vocabulary.
//   node tools/norm_parity.mjs
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const N = require('../site_src/static/js/norm.js');
const text = fs.readFileSync(new URL('../data/text/plain.txt', import.meta.url), 'utf8');
const words = [...new Set(N.tokens(text))];
fs.writeFileSync('norm_words.tmp', words.join('\n'), 'utf8');
const py = execFileSync('python', ['-c',
  "import sys,json;sys.path.insert(0,'pipeline/site');from norm import norm;w=open('norm_words.tmp',encoding='utf-8').read().split('\\n');print(json.dumps([norm(x) for x in w]))"],
  { encoding: 'utf8', maxBuffer: 1 << 28, env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
fs.unlinkSync('norm_words.tmp');
const P = JSON.parse(py);
let bad = 0;
words.forEach((w, i) => { const j = N.norm(w); if (j !== P[i]) { if (bad < 10) console.log('MISMATCH', w, j, P[i]); bad++; } });
console.log(`parity: ${words.length - bad}/${words.length} words identical`);
for (const w of ['Frost', 'Fronen', 'Kloster', 'clothes', 'Thal', 'Thale', 'Thaler', 'Teile', 'Theil', 'Wälder', 'Mühlen', 'Gera', 'Geras']) process.stdout.write(`${w}:${N.norm(w)} `);
console.log();
process.exitCode = bad ? 1 : 0;
