"""Q01: brief dump: title, summary.de, finding heads, datasets (name, rows, cols), charts (title) for overlap analysis."""
import json, sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
for a in sys.argv[1:]:
    for f in sorted(glob.glob(str(ROOT/'data'/'analyses'/f'{a}.json'))):
        d = json.load(open(f, encoding='utf-8'))
        print('='*90); print(d['id'], '|', d['category'], d['section'], '| src', ' '.join(sorted({s['page'] for s in d['sources']})))
        print('T:', d['title']['de']); print('S:', d['summary']['de'])
        for k, x in enumerate(d['findings']): print(f' F{k}:', x['de'][:260])
        for ds in d['datasets']:
            print(f"  DS {ds['name']} n={len(ds['rows'])} cols={[c['name'] for c in ds['columns']][:14]}")
        for ch in d['charts']: print('  CH', ch['id'], ch['dataset'], ch['title']['de'])
        print(' REL', d.get('related'))
