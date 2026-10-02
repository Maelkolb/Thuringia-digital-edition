from common import *
def rep(msg): print("  !!", msg)
def rowcheck(name, D, tol=0.006):
    for (k,y),r in D.items():
        try:
            ns,nl,nz=[num(x) for x in r[0:3]]; ps,pl,pz=[num(x) for x in r[3:6]]
        except Exception: continue
        if None in (ns,nl,nz,ps,pl,pz): continue
        S=ns/ps*100; L=nl/pl*100; Z=nz/pz*100
        if abs(S+L-Z)/Z>tol: rep(f"{name} {k} {y}: S+L={S+L:.0f} Z={Z:.0f} ({(S+L)/Z-1:+.2%}) row={r}")
g=grid("112","b5")
M={}
for r in g[2:12]:
    M[("Gera",r[0])]=r[1:7]; M[("Schleiz",r[0])]=r[7:13]
for r in g[14:24]:
    M[("Lob",r[0])]=r[1:7]; M[("Fü",r[0])]=r[7:13]
rowcheck("marr",M)
g=grid("114","b1")
Dd={}
for r in g[3:13]:
    Dd[("Gera",r[0])]=r[1:7]; Dd[("Schleiz",r[0])]=r[7:13]
for r in g[15:25]:
    Dd[("Lob",r[0])]=r[1:7]; Dd[("Fü",r[0])]=r[7:13]
rowcheck("death",Dd)
# births urban/rural? p111 ok
# p117 suicide
print("== p117 suicide")
g=grid("117","b2")
for r in g[3:13]:
    y=r[0]; n=[inum(x) for x in r[1:5]]
    if sum(n[:3])!=n[3]: rep(f"{y} sum {n}")
    dn={"Gera":0,"Schleiz":1,"Lob":2,"Fü":3}
    # pct of deaths and per 1000
    for k,j in dn.items():
        pct=num(r[5+j]); per=num(r[9+j])
        death=inum(Dd[(k,y)][2]); pz=num(Dd[(k,y)][5])
        pop=death/pz*100
        if abs(n[j]/death*100-pct)>0.011: rep(f"{y} {k} pct deaths {n[j]}/{death}={n[j]/death*100:.2f} vs {pct}")
        if abs(n[j]/pop*1000-per)>0.011: rep(f"{y} {k} per1000 {n[j]/pop*1000:.2f} vs {per} (pop {pop:.0f})")
print(g[13])
for j in range(1,5):
    print(j, round(sum(inum(r[j]) for r in g[3:13])/10,2))
for j in range(5,13):
    print(j, round(sum(num(r[j]) for r in g[3:13])/10,3), g[13][j])
