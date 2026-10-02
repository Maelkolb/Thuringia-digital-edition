"""Q01 helper: print a readable text dump of one or more analyses (no rows)."""
import json, sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
def dump(i, rows=0):
    d = json.load(open(ROOT/'data'/'analyses'/f'{i}.json', encoding='utf-8'))
    print('='*100)
    print(d['id'], '|', d['category'], '|', d['section'], '|', d.get('generated_by'))
    print('TITLE', d['title']['de'], '||', d['title']['en'])
    print('SRC', ' '.join(f"{s['page']}/{s['block']}" for s in d['sources']))
    print('SUMMARY.de', d['summary']['de']); print('SUMMARY.en', d['summary']['en'])
    print('METHOD.de', d['method']['de']); print('METHOD.en', d['method']['en'])
    for k, f in enumerate(d['findings']): print(f'F{k}.de', f['de']); print(f'F{k}.en', f['en'])
    for k, f in enumerate(d.get('caveats', [])): print(f'C{k}.de', f['de']); print(f'C{k}.en', f['en'])
    for c in d.get('conversions', []): print('CONV', c)
    for t in d.get('transcription_issues', []): print('TI', t)
    print('KW.de', d['keywords']['de']); print('KW.en', d['keywords']['en'])
    print('RELATED', d.get('related'))
    for ds in d['datasets']:
        print(f"DS {ds['name']} ({len(ds['rows'])} rows):", ds['title']['de'], '||', ds['title']['en'])
        print('   cols:', ', '.join(f"{c['name']}[{c['type']}|{c.get('unit')}{'|D' if c.get('derived') else ''}]" for c in ds['columns']))
        for r in ds['rows'][:rows]: print('   ', r)
    for ch in d['charts']:
        vl = ch['vegalite']
        mk = vl.get('mark') or [l.get('mark') for l in vl.get('layer', [])] or ('facet' if 'facet' in vl else None)
        print(f"CH {ch['id']} ds={ch['dataset']} extra={ch.get('extra_datasets')} mark={json.dumps(mk, ensure_ascii=False)[:100]}")
        print('   T', ch['title']['de'], '||', ch['title']['en'])
        print('   CAP', ch['caption']['de']); print('   CAP', ch['caption']['en'])
if __name__ == '__main__':
    args = sys.argv[1:]
    rows = 0
    if args and args[0].startswith('--rows='):
        rows = int(args[0][7:]); args = args[1:]
    for a in args:
        for f in sorted(glob.glob(str(ROOT/'data'/'analyses'/f'{a}.json'))):
            dump(Path(f).stem, rows)
