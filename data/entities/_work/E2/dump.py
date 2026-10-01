import json,sys,math,re
from pathlib import Path
c=json.load(open('data/entities/candidates/places.json',encoding='utf-8'))
e={x['key']:x for x in c['entries']}
s=json.load(open('data/entities/slices.json',encoding='utf-8'))['E2']['keys']
a,b=int(sys.argv[1]),int(sys.argv[2])
nctx=int(sys.argv[3]) if len(sys.argv)>3 else 2
_pc={}
def page(p):
    if p not in _pc:
        f=Path('data/text/pages')/f'{p}.txt'
        _pc[p]=f.read_text(encoding='utf-8') if f.exists() else ''
    return _pc[p]
def art(name,pages):
    for p in pages[:3]:
        t=page(p)
        m=re.search(r'\] '+re.escape(name)+r'(?= |,|\()([^\n]{0,170})',t)
        if m: return p,(name+m.group(1)).replace('\n',' ')
    for p in pages[:3]:
        t=page(p)
        m=re.search(r'(?<![\wäöü])'+re.escape(name)+r'(?= \(|, )([^\n]{0,170})',t)
        if m: return p,(name+m.group(1))
    return None,None
import difflib
_reg=json.load(open('data/registers/ortsregister.json',encoding='utf-8'))['entries']
def norm(s):
    s=s.lower()
    for a,b in (('ß','ss'),('ſ','s'),('ä','a'),('ö','o'),('ü','u'),('tz','z'),('ck','k'),('c','k'),('th','t'),('y','i'),('ph','f'),('ie','i'),('-',''),(' ',''),('.',''),('=',''),('dt','t')):
        s=s.replace(a,b)
    import re as _re
    return _re.sub(r'(.)+',r'',s)
_rn=[(norm(e['name']),e) for e in _reg if e.get('pages')]
def fuzzy(k):
    nk=norm(k); out=[]
    for n,e in _rn:
        if n==nk or difflib.SequenceMatcher(None,n,nk).ratio()>=0.86:
            out.append(e)
    return out
def hav(la1,lo1,la2,lo2):
    R=6371;p=math.pi/180
    d=math.sin((la2-la1)*p/2)**2+math.cos(la1*p)*math.cos(la2*p)*math.sin((lo2-lo1)*p/2)**2
    return 2*R*math.asin(math.sqrt(d))
for i,k in enumerate(s[a:b],a):
    x=e[k]
    forms=x['forms']
    fs=' '.join(f'{f}:{n}' for f,n in forms.items()) if len(forms)>1 or k not in forms else ''
    t=','.join(f'{t}:{n}' for t,n in x['types'].items()) if list(x['types'])!=['Location'] else ''
    print(f"#{i} {k!r} n={x['n']} pp={x['n_pages']} {t} {fs}".rstrip())
    for r in x.get('brueckner_register',[]):
        print('   REG',r['name'],r['pages'],'parents=',r.get('parents'),'W' if r.get('wuestung') else '','G' if r.get('gemeinde') else '')
        if len(sys.argv)>4 or True:
            p,sn=art(r['name'],r['pages'])
            if sn: print('      ART',p,':',sn[:190])
    if not x.get('brueckner_register'):
        for r in fuzzy(k)[:3]:
            print('   REG~',r['name'],r['pages'],'parents=',r.get('parents'),'W' if r.get('wuestung') else '','G' if r.get('gemeinde') else '')
            p,sn=art(r['name'],r['pages'])
            if sn: print('      ART',p,':',sn[:190])
    for g in x.get('geonames_candidates',[])[:5]:
        dg=hav(g['lat'],g['lon'],50.8803,12.0819)
        print(f"   GN {g['geonames']} {g['name']} {g['code']} pop={g.get('population')} ({g['lat']:.4f},{g['lon']:.4f}) km={g['km']} dGera={dg:.0f}")
    for cx in x['contexts'][:nctx]:
        t=cx['text']
        print(f"   [{cx['page']} {cx['unit']}] {t[:200]}")
