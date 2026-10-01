import sys,re
sys.path.insert(0,'C:/Users/totom/Projects/reuss-edition/data/entities/_work/E3')
from lib import *
a,b=int(sys.argv[1]),int(sys.argv[2])
nctx=int(sys.argv[3]) if len(sys.argv)>3 else 1
W=int(sys.argv[4]) if len(sys.argv)>4 else 85
def trim(t):
    m=re.search('⟦',t)
    if not m: return t[:2*W]
    i=m.start(); j=t.find('⟧',i)
    return t[max(0,i-W):min(len(t),j+W)].replace('\n',' ')
for i,k in enumerate(S[a:b],a):
    x=E[k]
    forms=x['forms']
    fs=' '.join(f'{f}:{n}' for f,n in forms.items()) if len(forms)>1 or k not in forms else ''
    print(f"#{i} {k!r} n={x['n']} pp={x['n_pages']} {fs}".rstrip())
    for r in x.get('brueckner_register',[]):
        print('   REG',r['name'],r['pages'],'par=',r.get('parents'),'W' if r.get('wuestung') else '','G' if r.get('gemeinde') else '')
    gs=[g for g in x.get('geonames_candidates',[]) if g['km']<=60 and g.get('class')!='P'][:4]
    for g in gs:
        print(f"   GN {g['geonames']} {g['name']} {g['code']} km={g['km']}")
    ps=[g for g in x.get('geonames_candidates',[]) if g['km']<=60 and g.get('class')=='P'][:2]
    for g in ps:
        print(f"   gnP {g['geonames']} {g['name']} {g['code']} km={g['km']}")
    for v in verify(k): print('   VER',v)
    for cx in x['contexts'][:nctx]:
        print(f"   [{cx['page']}] {trim(cx['text'])}")
