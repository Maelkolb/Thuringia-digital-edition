import sys,json,time
sys.path.insert(0,'data/entities/_work/E6')
from wd2 import get
def info(qs):
    d=get({"action":"wbgetentities","ids":"|".join(qs),"props":"labels|descriptions|claims","languages":"de|en","format":"json"})
    if not d: print('FAILED'); return
    ids=set()
    for q,e in d['entities'].items():
        for p in ('P31','P131','P17','P361','P279','P159'):
            for c in e.get('claims',{}).get(p,[]):
                v=c['mainsnak'].get('datavalue',{}).get('value')
                if isinstance(v,dict) and 'id' in v: ids.add(v['id'])
    lab={}
    if ids:
        dd=get({"action":"wbgetentities","ids":"|".join(sorted(ids)[:50]),"props":"labels","languages":"de|en","format":"json"})
        for q,e in (dd or {}).get('entities',{}).items():
            lab[q]=(e['labels'].get('de') or e['labels'].get('en') or {}).get('value',q)
    for q,e in d['entities'].items():
        L=(e.get('labels',{}).get('de') or e.get('labels',{}).get('en') or {}).get('value')
        D=(e.get('descriptions',{}).get('de') or e.get('descriptions',{}).get('en') or {}).get('value')
        out=[]
        for p in ('P31','P279','P131','P17','P361','P159'):
            vs=[lab.get(c['mainsnak']['datavalue']['value']['id'],'?') for c in e.get('claims',{}).get(p,[]) if c['mainsnak'].get('datavalue')]
            if vs: out.append(p+'='+','.join(vs[:3]))
        inc=[c['mainsnak']['datavalue']['value']['time'][:6] for c in e.get('claims',{}).get('P571',[]) if c['mainsnak'].get('datavalue')]
        co=[ (round(c['mainsnak']['datavalue']['value']['latitude'],3),round(c['mainsnak']['datavalue']['value']['longitude'],3)) for c in e.get('claims',{}).get('P625',[]) if c['mainsnak'].get('datavalue')]
        print(q,'|',L,'|',D,'|',' '.join(out),'| inc',inc[:1],'| xy',co[:1])
if __name__=='__main__':
    info(sys.argv[1:])
