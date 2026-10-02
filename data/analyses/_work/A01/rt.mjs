// render-test harness: node rt.mjs <file.json>   (file name = id; previews go to data/analyses/_preview)
import { validate } from '../../../../tools/validate_analysis.mjs';
for (const f of process.argv.slice(2)) {
  const r = await validate(f);
  console.log(r.errors.length ? 'FAIL' : 'OK', f);
  r.errors.forEach(e => console.log('  ERROR', e));
  r.warnings.forEach(e => console.log('  warn', e));
}
