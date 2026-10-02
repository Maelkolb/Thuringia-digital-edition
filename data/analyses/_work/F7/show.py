import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open(sys.argv[1],encoding='utf-8'))
for k in d:
    if k in('datasets','charts'): continue
    print(k,':',json.dumps(d[k],ensure_ascii=False))
for ds in d['datasets']:
    print('\n== DATASET',ds['name'],json.dumps(ds['title'],ensure_ascii=False))
    print([ (c['name'],c.get('unit'),c.get('derived',False)) for c in ds['columns']])
    for r in ds['rows']: print(r)
    print('refs',ds.get('source_refs'))
    for k in ds:
        if k not in('name','title','columns','rows','source_refs'): print(k,json.dumps(ds[k],ensure_ascii=False))
for c in d['charts']:
    print('\n== CHART',c['id'],c['dataset'],json.dumps(c['title'],ensure_ascii=False))
