import sys,re
sys.path.insert(0,'C:/Users/totom/Projects/reuss-edition/data/entities/_work/E3')
from lib import *
pl=places()
for k in sys.argv[1:]:
    x=E[k]
    cands=[g for g in x.get('geonames_candidates',[]) if g['km']<=60 and g.get('class')!='P']
    ws=set()
    for m in mentions().get(k,[]):
        for w in re.findall(r'[A-ZÄÖÜ][\w\-äöüß]+',seg(m,90)):
            if w in pl and w!=k: ws.add(w)
    out=[]
    for g in cands:
        best=sorted((round(min(hav(g['lat'],g['lon'],la,lo) for la,lo in pl[w]),1),w) for w in ws)[:3]
        out.append((g['geonames'],g['code'],round(g['lat'],3),round(g['lon'],3),best))
    print(k,sorted(ws)[:6]); 
    for o in out: print('   ',o)
