import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lib
for f in ('p1','p2','p3','p4'):
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),f+'.py'),encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wd_ids.py'),encoding='utf-8').read()) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wd_ids.py')) else None
cand=json.load(open('C:/Users/totom/Projects/reuss-edition/data/entities/candidates/organisations.json',encoding='utf-8'))['entries']
keys=[e['key'] for e in cand]
sl=json.load(open('C:/Users/totom/Projects/reuss-edition/data/entities/slices.json',encoding='utf-8'))['E6']['keys']
assert set(sl)==set(keys)
miss=[k for k in keys if k not in lib.D]
assert not miss, miss
WD=globals().get('WD',{})
for k,q in WD.items():
    assert k in lib.D and lib.D[k]['action']!='merge', k
    lib.D[k]['wikidata']=q
out={"package":"E6","group":"organisations","decisions":[lib.D[k] for k in keys]}
json.dump(out,open('C:/Users/totom/Projects/reuss-edition/data/entities/decisions/E6.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('written',len(out['decisions']))
