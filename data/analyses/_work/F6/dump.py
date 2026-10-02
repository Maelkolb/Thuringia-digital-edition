import json, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
def dump(i, rows=0):
    d = json.load(open(ROOT/'data'/'analyses'/'_archive'/f'{i}.json', encoding='utf-8'))
    print('='*100)
    print(d['id'], '|', d['category'], '|', d['section'], '|', d.get('generated_by'))
    print('TITLE', d['title']['de'])
    print('SRC', ' '.join(f"{s['page']}/{s['block']}" for s in d['sources']))
    print('SUMMARY.de', d['summary']['de'])
    print('METHOD.de', d['method']['de'])
    for k, f in enumerate(d['findings']): print(f'F{k}.de', f['de'])
    for k, f in enumerate(d.get('caveats', [])): print(f'C{k}.de', f['de'])
    for c in d.get('conversions', []): print('CONV', c)
    for t in d.get('transcription_issues', []): print('TI', t)
    for ds in d['datasets']:
        print(f"DS {ds['name']} ({len(ds['rows'])} rows):", ds['title']['de'], '| refs', ds.get('source_refs'))
        print('   cols:', ', '.join(f"{c['name']}[{c['type']}|{c.get('unit')}{'|D' if c.get('derived') else ''}]" for c in ds['columns']))
        for r in ds['rows'][:rows]: print('   ', r)
    for ch in d['charts']:
        print(f"CH {ch['id']} ds={ch['dataset']}")
        print('   T', ch['title']['de'])
if __name__ == '__main__':
    args = sys.argv[1:]
    rows = 0
    if args and args[0].startswith('--rows='):
        rows = int(args[0][7:]); args = args[1:]
    for a in args:
        dump(a, rows)
