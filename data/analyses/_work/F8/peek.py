import json,sys
sys.stdout.reconfigure(encoding='utf-8')
aid=sys.argv[1]; what=sys.argv[2:] 
d=json.load(open(f'../../_archive/{aid}.json',encoding='utf-8'))
if not what or 'meta' in what:
    for k in ('title','summary','findings','caveats','transcription_issues','conversions'):
        if k in d: print(k, json.dumps(d[k],ensure_ascii=False))
    for ds in d['datasets']:
        print('DS',ds['name'],len(ds['rows']),[c['name'] for c in ds['columns']], json.dumps(ds.get('source_refs'),ensure_ascii=False)[:300])
    for c in d['charts']:
        print('CH',c['id'],c['dataset'],json.dumps(c['title'],ensure_ascii=False))
for w in what:
    if w=='meta': continue
    ds=[x for x in d['datasets'] if x['name']==w][0]
    print('==',w,[c['name'] for c in ds['columns']])
    for r in ds['rows']: print(json.dumps(r,ensure_ascii=False))
