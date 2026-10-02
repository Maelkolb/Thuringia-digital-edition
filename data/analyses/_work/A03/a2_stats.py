from common import *
import statistics as st
def tab(label,bid,ncol=12,off=1):
    d={}
    for r in grid(label,bid)[1:]:
        k=r[0].strip()
        d[k]=[num(x) for x in r[1:1+ncol]]
    return d
gera=tab("55","b7"); hoh=tab("56","b2"); sch=tab("56","b5"); rot=tab("57","b2"); zie=tab("57","b6")
gea=tab("55","b9",5); hoa=tab("56","b3",5); sca=tab("56","b6",5); zia=tab("57","b8",5)
print("gera ann",{k:v[4] for k,v in gea.items()})
print("hoh ann",{k:v[4] for k,v in hoa.items()})
# overlap Gera vs Hohenleuben annual 1856-1860
for lab,other in (("Hohenleuben",hoa),("Schleiz",sca)):
    ys=[y for y in other if y.isdigit() and y in gea and other[y][4] is not None]
    d=[gea[y][4]-other[y][4] for y in ys]
    print(lab, ys, [round(x,2) for x in d], "mean diff R",round(st.mean(d),2), "K",round(st.mean(d)*1.25,2))
    ds=[gea[y][0]-other[y][0] for y in ys]; dw=[gea[y][1]-other[y][1] for y in ys]
    print("  summer diff",round(st.mean(ds),2),"winter diff",round(st.mean(dw),2))
# monthly cycle amplitude
for name,d,keys in (("Gera",gera,None),("Hoh",hoh,None),("Sch",sch,None)):
    ys=[k for k in d if k.isdigit()]
    mm=[st.mean(d[y][j] for y in ys if d[y][j] is not None) for j in range(12)]
    print(name,[round(x,2) for x in mm],"amp",round(max(mm)-min(mm),2), round((max(mm)-min(mm))*1.25,2), "jan",round(mm[0],2),"jul",round(mm[6],2))
# rothenacker vs gera same years
for y in ("1865","1867"):
    r=rot[y]; g=gera[y]
    print(y,"Rot-Gera monthly diff R",[round(a-b,2) for a,b in zip(r,g)], "mean",round(st.mean(a-b for a,b in zip(r,g)),2))
    s=sch[y]; print(" Sch-Gera",round(st.mean(a-b for a,b in zip(s,g)),2))
print(zie)
