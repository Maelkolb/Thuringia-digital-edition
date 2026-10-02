import re, statistics as st
from common import *
def pdate(s):
    s=s.strip()
    if s in ("—",""): return None
    m=re.match(r'^(\d+)\.(?:-(\d+)\.)?\s*/(\d+)\.?$', s)
    assert m, repr(s)
    d1=int(m.group(1)); d2=int(m.group(2)) if m.group(2) else d1; mo=int(m.group(3))
    return mo,d1,d2
g=grid("61","b5")
years=[1859,1860,1861,1862,1863,1864]
obs=[]
for r in g[2:]:
    sp=r[0]
    for i,y in enumerate(years):
        a=pdate(r[1+2*i]); d=pdate(r[2+2*i])
        if a or d:
            ad=None if not a else (doy(a[0],a[1])+doy(a[0],a[2]))/2
            dd=None if not d else (doy(d[0],d[1])+doy(d[0],d[2]))/2
            obs.append((sp,y,ad,dd))
print(len(obs))
pairs=[o for o in obs if o[2] is not None and o[3] is not None]
print("pairs",len(pairs))
allarr=[o[2] for o in obs if o[2] is not None]; alldep=[o[3] for o in obs if o[3] is not None]
print("arrival range",min(allarr),max(allarr),"dep range",min(alldep),max(alldep), len(allarr), len(alldep))
sp={}
for o in obs: sp.setdefault(o[0],[]).append(o)
rows=[]
for k,v in sp.items():
    a=[x[2] for x in v if x[2] is not None]; d=[x[3] for x in v if x[3] is not None]
    pr=[x for x in v if x[2] is not None and x[3] is not None]
    rows.append((k,len(a),len(d),len(pr), st.mean(a) if a else None, st.mean(d) if d else None))
for r in rows: print(r)
both=[r for r in rows if r[4] is not None and r[5] is not None]
print("species-level r (means, n=%d)"%len(both), st.correlation([r[4] for r in both],[r[5] for r in both]))
print("pooled pairs r", st.correlation([p[2] for p in pairs],[p[3] for p in pairs]))
# within-species
for k,v in sp.items():
    pr=[x for x in v if x[2] is not None and x[3] is not None]
    if len(pr)>=3:
        print(k, len(pr), round(st.correlation([x[2] for x in pr],[x[3] for x in pr]),2), [ (x[1],x[2],x[3]) for x in pr])
# stay days
stay=[(o[0],o[1],o[3]-o[2]) for o in pairs]
print(sorted(stay,key=lambda t:t[2])[:3], sorted(stay,key=lambda t:t[2])[-3:])
