import json,sys
sys.stdout.reconfigure(encoding='utf-8')
aid=sys.argv[1]
d=json.load(open(f'data/analyses/_archive/{aid}.json',encoding='utf-8'))
print('ID',d['id'],'| section',d.get('section'))
print('TITLE',d['title']['de'])
print('SUMMARY',d['summary']['de'])
for f in d.get('findings',[]): print('FIND',f['de'])
print('SOURCES',d.get('sources'))
print('METHOD',d['method']['de'])
for c in d.get('caveats',[]): print('CAVEAT',c['de'])
print('TI',json.dumps(d.get('transcription_issues'),ensure_ascii=False))
print('CONV',json.dumps(d.get('conversions'),ensure_ascii=False))
for ds in d['datasets']:
    print('--- DATASET',ds['name'],ds['title']['de'],len(ds['rows']),'rows')
    print('  cols',[ (c['name'],c['type'],c.get('unit'),'D' if c.get('derived') else '') for c in ds['columns']])
    print('  refs',json.dumps(ds.get('source_refs'),ensure_ascii=False))
    n=int(sys.argv[2]) if len(sys.argv)>2 else 400
    for r in ds['rows'][:n]: print('  ',json.dumps(r,ensure_ascii=False))
for c in d['charts']:
    print('CHART',c['id'],c['title']['de'],'|',c['dataset'])
