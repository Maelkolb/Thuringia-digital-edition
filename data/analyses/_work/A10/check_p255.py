import sys, re
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *
def n(x): return num(x) or 0
g=grid("255","b1")
for i,r in enumerate(g, start=1):
    if len(r)==13 and any(x.strip() for x in r[1:]) and re.fullmatch(r"[\d—]+", r[1].strip() or "x"):
        v=[n(x) for x in r[1:]]
        for c in range(4):
            if v[c]+v[4+c]!=v[8+c]:
                print("St+Pl != Summe", f"r{i}", r[0], "SGDF"[c], v[c], v[4+c], v[8+c])
# group totals vs rows
groups={"Gera":(3,7,8),"Schleiz":(10,14,15),"Lob":(17,21,22),"Fst":(24,28,29)}
for k,(a,b,t) in groups.items():
    rows=[[n(x) for x in g[i-1][1:]] for i in range(a,b+1)]
    tot=[n(x) for x in g[t-1][1:]]
    s=[sum(r[c] for r in rows) for c in range(12)]
    print(k, [(c,s[c],tot[c]) for c in range(12) if s[c]!=tot[c]])
# Fuerstenthum rows = sum of 3 districts
for off in range(5):
    rows=[[n(x) for x in g[i-1][1:]] for i in (3+off,10+off,17+off)]
    f=[n(x) for x in g[24+off-1][1:]]
    s=[sum(r[c] for r in rows) for c in range(12)]
    print(g[24+off-1][0], [(c,s[c],f[c]) for c in range(12) if s[c]!=f[c]])
