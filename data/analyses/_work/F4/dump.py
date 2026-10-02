import json,sys
sys.stdout.reconfigure(encoding='utf-8')
ARCH='C:/Users/totom/Projects/reuss-edition/data/analyses/_archive/'
for aid in sys.argv[1:]:
    d=json.load(open(ARCH+aid+'.json',encoding='utf-8'))
    print('='*100); print(aid, '|', d['title']['de'], '| section', d['section'], '| cat', d['category'])
    print('SOURCES', [(s['page'],s['block']) for s in d['sources']])
    print('SUMMARY', d['summary']['de'])
    for f in d.get('findings',[]): print(' FIND', f['de'])
    print('METHOD', d['method']['de'])
    for c in d.get('caveats',[]): print(' CAV', c['de'])
    for t in d.get('transcription_issues',[]): print(' TI', t)
    for c in d.get('conversions',[]): print(' CONV', c)
    for ds in d['datasets']:
        print('-- DATASET', ds['name'], ds['title']['de'], 'refs', ds['source_refs'])
        print('   cols', [(c['name'],c.get('unit'),'D' if c.get('derived') else '') for c in ds['columns']])
        for r in ds['rows'][:int(40)]: print('  ', r)
        if len(ds['rows'])>40: print('   ...',len(ds['rows']),'rows')
    for ch in d['charts']:
        print('-- CHART', ch['id'], ch['dataset'], ch['title']['de'])
