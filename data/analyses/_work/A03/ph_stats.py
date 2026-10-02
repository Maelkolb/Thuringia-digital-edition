import re, datetime, statistics as st
from common import *
def pd_(s):
    s=s.strip()
    if s in ("—",""): return None
    m=re.match(r'^(\d+)\.(?:-(\d+)\.)?/(\d+)\.?$', s)
    assert m, s
    return int(m.group(1)), (int(m.group(2)) if m.group(2) else None), int(m.group(3))
for name,bid in (("Gera","b5"),("Hoh","b7")):
    g=grid("60",bid)
    yrs=[int(x.rstrip('.')) for x in g[0][1:-1]]
    print(name, yrs)
    for r in g[1:]:
        ds=[]
        for y,c in zip(yrs,r[1:-1]):
            p=pd_(c)
            if p: ds.append((y,doy(p[2],p[0]),c))
        d=[x[1] for x in ds]
        # also variant: 30-day months
        d30=[ (int(re.match(r'(\d+)',c).group(1)) + 30*(int(re.search(r'/(\d+)',c).group(1))-1)) for y,_,c in ds]
        print(f"{r[0]:25s} printed {r[-1]:>3s}  calc {max(d)-min(d):3d}  calc30 {max(d30)-min(d30)}  n={len(d)}", "" if int(r[-1])==max(d)-min(d) else "<<<")

print("=== spring index")
def table(bid):
    g=grid("60",bid); yrs=[int(x.rstrip('.')) for x in g[0][1:-1]]
    out={}
    for r in g[1:]:
        for y,c in zip(yrs,r[1:-1]):
            p=pd_(c)
            if p: out.setdefault(r[0],{})[y]=doy(p[2],p[0])
    return out
G=table("b5"); H=table("b7")
def index(T, skip=("Vitis vinifera",)):
    sp={k:v for k,v in T.items() if k not in skip}
    mean={k:st.mean(v.values()) for k,v in sp.items()}
    yrs=sorted({y for v in sp.values() for y in v})
    return {y: st.mean(v[y]-mean[k] for k,v in sp.items() if y in v) for y in yrs}
ig=index(G); ih=index(H)
print({y:round(v,1) for y,v in ig.items()}); print({y:round(v,1) for y,v in ih.items()})
common=[y for y in ig if y in ih]
print("common", common, [round(ig[y],1) for y in common],[round(ih[y],1) for y in common])
import math
def corr(x,y): return st.correlation(x,y)
print("corr Gera/Hoh index common years", corr([ig[y] for y in common],[ih[y] for y in common]))
# temperature Hohenleuben
hm={}
for r in grid("56","b2")[1:9]:
    hm[int(r[0])]=[num(x) for x in r[1:13]]
for lab,months in (("Mar-Apr",(3,4)),("Mar-May",(3,4,5)),("Apr",(4,)),("Feb-Apr",(2,3,4))):
    ys=[y for y in ih if y in hm]
    t=[st.mean(hm[y][m-1] for m in months)*1.25 for y in ys]
    print(lab, ys, [round(x,2) for x in t], "r=",round(corr(t,[ih[y] for y in ys]),3), "slope", st.linear_regression(t,[ih[y] for y in ys]).slope)

print("=== Hohenleuben vs Gera same species / years")
common_sp={"Viola odorata":"Viola odorata","Anemone nemorosa":"Anemone nem.","Ranunculus Ficaria":"Ficaria verna","Primula officinalis":"Prim. officinal.","Ribes Grossularia":"Ribes grossul.","Saxifraga granulata":"Saxifraga gran.","Pyrus communis":"Pyrus comm.","Prunus domestica":"Prun. domest.","Prunus Cerasus":"Cerasus acida","Pyrus Malus":"Pyrus Malus","Crataegus Oxyacantha":"Crataeg. Oxyat.","Sambucus nigra":"Sambuc. nigra"}
diffs=[]
for kg,kh in common_sp.items():
    for y in (1853,1854,1855,1856):
        if y in G[kg] and y in H[kh]: diffs.append(H[kh][y]-G[kg][y])
print(len(diffs), st.mean(diffs), min(diffs), max(diffs), st.median(diffs))
# by species
for kg,kh in common_sp.items():
    d=[H[kh][y]-G[kg][y] for y in (1853,1854,1855,1856) if y in G[kg] and y in H[kh]]
    print(kg, d)
