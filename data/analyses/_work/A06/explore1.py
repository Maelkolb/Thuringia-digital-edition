from common import *
import math
g91=grid('91','b4'); g92=grid('92','b1')
def parse(g, start):
    out={}
    dist=None
    for r in g:
        if r[0].startswith('Landrathsbezirk') or r[0].startswith('Das F'):
            dist=r[0]; continue
        if r[1]=='' and r[2]=='' and r[0]=='' : continue
        if r[0] and r[0].isdigit():
            out.setdefault(dist,[]).append(r)
    return out
# manual district separation
rows={}
cur=None
for r in g91[1:]:
    if r[0].startswith('Landrath'): cur=r[0]; continue
    if r[0].isdigit(): rows.setdefault(cur,[]).append(r)
for r in g92[3:]:
    if r[0].startswith('Landrath') or r[0].startswith('Das F'): cur=r[0]; continue
    if r[0].isdigit(): rows.setdefault(cur,[]).append(r)
for k,v in rows.items(): print(k,len(v))
# row checks
for k,v in rows.items():
    prev=None
    for r in v:
        y=int(r[0]); fam=integer(r[1]); o=[integer(x) for x in r[2:11]]; tot=o[8]; gr=num(r[11])
        chk=[]
        if o[0] is not None:
            om,of,os_,um,uf,us,tm,tf,ts=o
            if om+of!=os_: chk.append(('over14 sum',om+of,os_))
            if um+uf!=us: chk.append(('under14 sum',um+uf,us))
            if om+um!=tm: chk.append(('male tot',om+um,tm))
            if of+uf!=tf: chk.append(('fem tot',of+uf,tf))
            if tm+tf!=ts: chk.append(('tot',tm+tf,ts))
            if os_+us!=ts: chk.append(('age tot',os_+us,ts))
        # growth: simple vs compound
        gs=gc=None
        if prev:
            py,pt=prev
            n=y-py
            gs=(tot/pt-1)/n*100; gc=((tot/pt)**(1/n)-1)*100
        print(k[:12],y,tot,gr,None if gs is None else (round(gs,2),round(gc,2)),chk)
        prev=(y,tot)
