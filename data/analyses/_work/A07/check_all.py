from common import *
import math
def close(a,b,tol): return abs(a-b)<=tol
def rep(msg): print("  !!", msg)

print("=== p108 b1 urban/rural births pct + abs")
g=grid("108","b1"); b107=grid("107","b3")
for i,r in enumerate(g[2:12]):
    y=r[0]; st,la=inum(r[9]),inum(r[10]); tot=inum(b107[1+i][7])
    if st+la!=tot: rep(f"{y}: {st}+{la}!={tot}")
for j in range(1,11):
    vals=[num(r[j]) for r in g[2:12]]
    avg=sum(vals)/10 if j<9 else sum(vals)/10
    print(j, g[12][j], round(avg,2))
print("=== p108 b3 sex")
g=grid("108","b3")
for r in g[2:12]:
    y=r[0]
    for a,b,c,d in [(1,2,3,None),(4,5,6,None),(7,8,9,None)]:
        m,w,rat=inum(r[a]),inum(r[b]),num(r[c])
        if not close(m/w*100,rat,0.011): rep(f"{y} col{a}: ratio {m/w*100:.2f} vs {rat}")
    if inum(r[1])+inum(r[4])!=inum(r[7]): rep(f"{y} m sum")
    if inum(r[2])+inum(r[5])!=inum(r[8]): rep(f"{y} w sum")
    tot=inum(r[7])+inum(r[8])
    b=[x for x in b107[1:11] if x[0]==y][0]
    if tot!=inum(b[7]): rep(f"{y} total births {tot} vs p107 {b[7]}")
print([ (c) for c in g[12]])
for j in (1,2,4,5,7,8):
    print(j,g[12][j], round(sum(inum(r[j]) for r in g[2:12])/10,1))
print("=== p109 illegit")
g=grid("109","b1")
blocks={"Gera":(4,14),"Schleiz":(16,26),"Lob":(28,38),"Fü":(40,50)}
data={}
for k,(a,b) in blocks.items():
    for r in g[a:b]:
        data[(k,r[0])]=r
for y in [str(x) for x in range(1858,1868)]:
    for col in (1,4,7):
        s=sum(inum(data[(k,y)][col]) for k in ("Gera","Schleiz","Lob"))
        if s!=inum(data[("Fü",y)][col]): rep(f"{y} col{col} sum {s} vs {data[('Fü',y)][col]}")
    for k in blocks:
        r=data[(k,y)]
        for c in (2,5,8):
            if not close(num(r[c])+num(r[c+1]),100,0.011): rep(f"{k} {y} col{c} legit+illeg {num(r[c])+num(r[c+1])}")
# illegit share vs births
for i,y in enumerate(range(1858,1868)):
    b=b107[1+i]
    for k,jb in (("Gera",1),("Schleiz",3),("Lob",5),("Fü",7)):
        n=inum(data[(k,str(y))][7]); tot=inum(b[jb])
        sh=num(data[(k,str(y))][9])
        if not close(n/tot*100,sh,0.011): rep(f"{k} {y} illeg {n}/{tot}={n/tot*100:.2f} vs printed {sh}")
for k,(a,b) in blocks.items():
    r=g[b]
    print(k, r)
    for c in (1,4,7):
        print('   avg col',c, round(sum(inum(data[(k,str(y))][c]) for y in range(1858,1868))/10,1), r[c])
    for c in (3,6,9):
        print('   avg pct col',c, round(sum(num(data[(k,str(y))][c]) for y in range(1858,1868))/10,2), r[c])
# 5y averages Fü
f=[num(data[("Fü",str(y))][9]) for y in range(1858,1868)]
print("5y",sum(f[:5])/5,sum(f[5:])/5)
