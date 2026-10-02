import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def dump(id, rows=True, maxrows=60):
    d=json.load(open(f'data/analyses/_archive/{id}.json',encoding='utf-8'))
    print('='*100); print(id, d.get('section'), d.get('category'))
    print('TITLE', d['title']['de']); print('SUMMARY', d['summary']['de'])
    for f in d.get('findings',[]): print('FIND', f['de'])
    print('METHOD', d['method']['de'])
    for c in d.get('caveats',[]): print('CAVEAT', c['de'])
    print('CONV', d.get('conversions'))
    print('TI', json.dumps(d.get('transcription_issues'),ensure_ascii=False))
    for ds in d['datasets']:
        print('--DS', ds['name'], ds['title']['de'], len(ds['rows']), ds['source_refs'] if len(json.dumps(ds['source_refs']))<600 else '[many refs]')
        print('  cols', [(c['name'],c['type'],c.get('unit'),'D' if c.get('derived') else '') for c in ds['columns']])
        if rows:
            for r in ds['rows'][:maxrows]: print('   ', r)
    for ch in d['charts']:
        print('--CHART', ch['id'], ch['dataset'], ch['title']['de'])
if __name__=='__main__':
    for a in sys.argv[1:]: dump(a)
