from common import *
def rep(msg): print("  !!", msg)
def close(a,b,t): return abs(a-b)<=t
print("== p115 b1 Lobenstein")
g=grid("115","b1")
for r in g[1:12]:
    pop,d,p=inum(r[1]),inum(r[2]),num(r[3])
    if not close(d/pop*100,p,0.011): rep(f"{r[0]} {d}/{pop}={d/pop*100:.2f} vs {p}")
print(g[12], sum(num(r[3]) for r in g[1:12])/11, sum(inum(r[2]) for r in g[1:12])/11)
print("== p115 sex")
g=grid("115","b5"); print(g)
print("== p116 classes")
g=grid("116","b2")
L=grid("115","b1")
for i,r in enumerate(g[1:12]):
    v=[inum(x) for x in r[1:7]]
    tot=sum(v)
    d=inum(L[1+i][2])
    if tot!=d: rep(f"{r[0]} class sum {tot} vs deaths {d}")
    kin=v[0]+v[1]; led=v[2]+v[3]; ver=v[4]+v[5]
    for val,pc,nm in ((kin,r[7],'K'),(led,r[8],'L'),(ver,r[9],'V')):
        if not close(val/tot*100,num(pc),0.011): rep(f"{r[0]} {nm} {val/tot*100:.2f} vs {pc}")
print(g[12])
for j in range(1,10):
    vals=[num(r[j]) for r in g[1:12]]
    print(j, round(sum(vals)/11,2), g[12][j])
print("== p116 ages")
g2=grid("116","b4")
for i,r in enumerate(g2[1:12]):
    v=[inum(x) or 0 for x in r[1:11]]
    d=inum(L[1+i][2])
    if sum(v)!=d: rep(f"{r[0]} age sum {sum(v)} vs deaths {d}")
print(g2[12])
for j in range(1,11):
    vals=[inum(r[j]) or 0 for r in g2[1:12]]
    print(j, round(sum(vals)/11,2), g2[12][j])
print(g2[0])
