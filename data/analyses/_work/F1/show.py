import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def show(aid, rows=True, charts=False):
    d=json.load(open(f'C:/Users/totom/Projects/reuss-edition/data/analyses/_archive/{aid}.json',encoding='utf-8'))
    print('=====',aid)
    for k in ('title','section','sources','summary','findings','method','conversions','caveats','transcription_issues','related'):
        if k in d: print(k,':',json.dumps(d[k],ensure_ascii=False))
    for ds in d['datasets']:
        print('--- dataset',ds['name'],ds['title']['de'])
        print(' cols:',[(c['name'],c['type'],c.get('unit'),'D' if c.get('derived') else '') for c in ds['columns']])
        print(' refs:',json.dumps(ds['source_refs'],ensure_ascii=False))
        if rows:
            for r in ds['rows']: print('  ',json.dumps(r,ensure_ascii=False))
    for c in d['charts']:
        print('--- chart',c['id'],c['dataset'],c['title']['de'])
        if charts: print(json.dumps(c['vegalite'],ensure_ascii=False)[:3000])
if __name__=='__main__':
    for a in sys.argv[1:]: show(a)
