import json,sys,math,re,glob,difflib
from pathlib import Path
ROOT=Path(r'C:\Users\totom\Projects\reuss-edition')
c=json.load(open(ROOT/'data/entities/candidates/places.json',encoding='utf-8'))
e={x['key']:x for x in c['entries']}
s=json.load(open(ROOT/'data/entities/slices.json',encoding='utf-8'))['E2']['keys']
a,b=int(sys.argv[1]),int(sys.argv[2])
_pc={}
def page(p):
    if p not in _pc:
        f=ROOT/'data/text/pages'/f'{p}.txt'
        _pc[p]=f.read_text(encoding='utf-8') if f.exists() else ''
    return _pc[p]
def art(name,pages):
    for p in pages[:3]:
        t=page(p)
        m=re.search(r'\] '+re.escape(name)+r'(?= |,|\()([^\n]{0,170})',t)
        if m: return p,(name+m.group(1)).replace('\n',' ')
    return None,None
GZ={}
for f in glob.glob(str(ROOT/'data/gazetteer/G*.json')):
    for x in json.load(open(f,encoding='utf-8'))['entries']:
        GZ.setdefault(x['name'],[]).append(x)
_reg=json.load(open(ROOT/'data/registers/ortsregister.json',encoding='utf-8'))['entries']
def norm(s):
    s=s.lower()
    for a_,b_ in (('ß','ss'),('ſ','s'),('ä','a'),('ö','o'),('ü','u'),('tz','z'),('ck','k'),('c','k'),('th','t'),('y','i'),('ph','f'),('ie','i'),('-',''),(' ',''),('.',''),('=',''),('dt','t')):
        s=s.replace(a_,b_)
    return re.sub(r'(.)\1+',r'\1',s)
_rn=[(norm(x['name']),x) for x in _reg if x.get('pages')]
def fuzzy(k):
    nk=norm(k); out=[]
    for n,x in _rn:
        if n==nk or difflib.SequenceMatcher(None,n,nk).ratio()>=0.86:
            out.append(x)
    return out
import locfit
def arttext(name,pages):
    for p in pages[:3]:
        tx=page(p)
        m=re.search(r'\] '+re.escape(name)+r'[ ,(]',tx)
        if m: return tx[m.start():m.start()+900]
    return ''
def fitline(r,gl):
    if not r.get('pages'): return
    near=[g for g in gl if g['km']<=75]
    if len(near)<1: return
    f=locfit.fit(arttext(r['name'],r['pages']),near)
    if not f: return
    if f[0]=='noref': print('      FIT noref',f[1:]); return
    h,d,ref,exp,out=f
    sc=sorted(out,key=lambda o:abs(o[1]-exp)/max(exp,3)+o[3]/60)[:2]
    print(f'      FIT {h}h {d} v.{ref} exp~{exp}km ->',' ; '.join(f'{o[0]} d={o[1]} brgErr={o[3]}' for o in sc))
for i,k in enumerate(s[a:b],a):
    x=e[k]
    forms=x['forms']
    fs=' '.join(f'{f}:{n}' for f,n in forms.items()) if len(forms)>1 or k not in forms else ''
    t=','.join(f'{t}:{n}' for t,n in x['types'].items()) if list(x['types'])!=['Location'] else ''
    print(f"#{i} {k!r} n={x['n']} pp={x['n_pages']} {t} {fs}".rstrip())
    regs=x.get('brueckner_register',[])
    fz=False
    if not regs:
        regs=fuzzy(k)[:3]; fz=True
    for r in regs:
        g=GZ.get(r['name'])
        print('   REG'+('~' if fz else ''),r['name'],r['pages'],'par=',r.get('parents'),'W' if r.get('wuestung') else '','G' if r.get('gemeinde') else '')
        if g:
            for gg in g:
                if not r['pages'] or gg['start']['page'] in r['pages'] or True:
                    print('      GZ',gg['start']['page'],gg.get('landestheil'),gg.get('type'),'|',(gg.get('type_verbatim') or '')[:60],'|',(gg.get('location') or {}).get('verbatim'))
        else:
            p,sn=art(r['name'],r['pages'])
            if sn: print('      ART',p,':',sn[:140])
    gl=x.get('geonames_candidates',[])
    if not fz:
        for r in regs: fitline(r,gl)
    near=[g for g in gl if g['km']<=75][:4]
    far=[g for g in gl if g['km']>75]
    far=sorted(far,key=lambda g:-(g.get('population') or 0))[:2]
    for g in near+far:
        print(f"   GN {g['geonames']} {g['name']} {g['code']} pop={g.get('population')} ({g['lat']:.3f},{g['lon']:.3f}) km={g['km']:.0f}")
    nctx=1 if regs and not fz and x['n']>=5 else 2
    for cx in x['contexts'][:nctx]:
        t=cx['text']
        print(f"   [{cx['page']} {cx['unit']}] {t[:190]}")
