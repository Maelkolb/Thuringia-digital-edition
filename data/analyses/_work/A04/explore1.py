import sys
sys.path.insert(0,'.')
from common import *
tabs={"Gera":("62","b3",10),"Hohenleuben":("63","b2",7),"Schleiz":("63","b4",2),"Rothenacker":("63","b6",1)}
data={}
for st,(p,b,y) in tabs.items():
    g=grid(p,b)
    data[st]=[[int(num(g[r][c]) or 0) for c in range(1,9)] for r in range(1,13)]
for st,m in data.items():
    tot=[sum(m[r][c] for r in range(12)) for c in range(8)]
    T=sum(tot)
    print(st,T,[round(100*t/T,1) for t in tot])
    # west share SW+W+NW by month
    ws=[round(100*(m[r][5]+m[r][6]+m[r][7])/sum(m[r]),1) for r in range(12)]
    ss=[round(100*(m[r][4])/sum(m[r]),1) for r in range(12)]
    print("  west(SW+W+NW)",ws)
    print("  S",ss)
    print("  month totals",[sum(m[r]) for r in range(12)])
# Gera seasons
m=data["Gera"]
import collections
for name,mons in [("Winter",[11,0,1]),("Frühling",[2,3,4]),("Sommer",[5,6,7]),("Herbst",[8,9,10])]:
    tot=[sum(m[r][c] for r in mons) for c in range(8)]
    T=sum(tot); print(name,T,[round(100*t/T,1) for t in tot])
