from common import *
def close(a,b,tol): return abs(a-b)<=tol
def rep(msg): print("  !!", msg)
b107=grid("107","b3")
print("=== p111 stillbirths")
g=grid("111","b1")
blocks={"Gera":(3,13,13),"Schleiz":(15,25,25),"Lob":(27,37,37),"Fü":(39,49,49)}
D={}
for k,(a,b,t) in blocks.items():
    for r in g[a:b]: D[(k,r[0])]=r
    avg=g[t]
    for c in (1,2,3):
        s=sum(inum(D[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avg[c]),0.051): rep(f"{k} avg col{c} {s} vs {avg[c]}")
    for c in (4,5,6,7,8,9):
        s=sum(num(D[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avg[c]),0.0151): rep(f"{k} avg col{c} {s:.3f} vs {avg[c]}")
for y in range(1858,1868):
    for k in blocks:
        r=D[(k,str(y))]
        if inum(r[1])+inum(r[2])!=inum(r[3]): rep(f"{k} {y} urban+rural {r[1:4]}")
        for c in (4,5,6):
            if not close(num(r[c])+num(r[c+3]),100,0.011): rep(f"{k} {y} live+still col{c} {r[c]} {r[c+3]}")
    for k in ("Gera","Schleiz","Lob"):
        pass
    s=sum(inum(D[(k,str(y))][c]) for k in ("Gera","Schleiz","Lob") for c in (3,))
    if s!=inum(D[("Fü",str(y))][3]): rep(f"{y} Fü sum {s} vs {D[('Fü',str(y))][3]}")
    for c in (1,2):
        s=sum(inum(D[(k,str(y))][c]) for k in ("Gera","Schleiz","Lob"))
        if s!=inum(D[("Fü",str(y))][c]): rep(f"{y} Fü col{c} sum {s} vs {D[('Fü',str(y))][c]}")
# vs births
for i,y in enumerate(range(1858,1868)):
    for k,jb in (("Gera",1),("Schleiz",3),("Lob",5),("Fü",7)):
        n=inum(D[(k,str(y))][3]); tot=inum(b107[1+i][jb]); sh=num(D[(k,str(y))][9])
        if not close(n/tot*100,sh,0.011): rep(f"{k} {y} stillbirth {n}/{tot}={n/tot*100:.2f} vs printed {sh}")

print("=== p112 marriages")
g=grid("112","b5")
# first block rows 2..11 (Gera cols1-6, Schleiz cols7-12), avg row 12; then rows 14..23 (Lob, Fü), avg row 24
M={}
for r in g[2:12]:
    M[("Gera",r[0])]=r[1:7]; M[("Schleiz",r[0])]=r[7:13]
for r in g[14:24]:
    M[("Lob",r[0])]=r[1:7]; M[("Fü",r[0])]=r[7:13]
avgrows={"Gera":g[12][1:7],"Schleiz":g[12][7:13],"Lob":g[24][1:7],"Fü":g[24][7:13]}
for k in ("Gera","Schleiz","Lob","Fü"):
    for c in range(3):
        s=sum(num(M[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avgrows[k][c]),0.051): rep(f"{k} avg abs col{c} {s} vs {avgrows[k][c]}")
    for c in range(3,6):
        s=sum(num(M[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avgrows[k][c]),0.0151): rep(f"{k} avg pct col{c} {s:.3f} vs {avgrows[k][c]}")
    for y in range(1858,1868):
        r=M[(k,str(y))]
        if inum(r[0])+inum(r[1])!=inum(r[2]): rep(f"{k} {y} urban+rural {r[:3]}")
for y in range(1858,1868):
    for c in range(3):
        s=sum(inum(M[(k,str(y))][c]) for k in ("Gera","Schleiz","Lob"))
        if s!=inum(M[("Fü",str(y))][c]): rep(f"{y} Fü col{c} sum {s} vs {M[('Fü',str(y))][c]}")
print(g[12][0],g[24][0])
print("=== p114 deaths")
g=grid("114","b1")
Dd={}
for r in g[3:13]:
    Dd[("Gera",r[0])]=r[1:7]; Dd[("Schleiz",r[0])]=r[7:13]
for r in g[15:25]:
    Dd[("Lob",r[0])]=r[1:7]; Dd[("Fü",r[0])]=r[7:13]
avgrows={"Gera":g[13][1:7],"Schleiz":g[13][7:13],"Lob":g[25][1:7],"Fü":g[25][7:13]}
print(g[13][0],g[25][0], g[3][0],g[15][0],g[14][:3],g[2][:3])
for k in ("Gera","Schleiz","Lob","Fü"):
    for c in range(3):
        s=sum(num(Dd[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avgrows[k][c]),0.051): rep(f"{k} avg abs col{c} {s} vs {avgrows[k][c]}")
    for c in range(3,6):
        s=sum(num(Dd[(k,str(y))][c]) for y in range(1858,1868))/10
        if not close(s,num(avgrows[k][c]),0.0151): rep(f"{k} avg pct col{c} {s:.3f} vs {avgrows[k][c]}")
    for y in range(1858,1868):
        r=Dd[(k,str(y))]
        if inum(r[0])+inum(r[1])!=inum(r[2]): rep(f"{k} {y} urban+rural {r[:3]}")
for y in range(1858,1868):
    for c in range(3):
        s=sum(inum(Dd[(k,str(y))][c]) for k in ("Gera","Schleiz","Lob"))
        if s!=inum(Dd[("Fü",str(y))][c]): rep(f"{y} Fü col{c} sum {s} vs {Dd[('Fü',str(y))][c]}")
# implied population consistency across pages births/deaths
for i,y in enumerate(range(1858,1868)):
    for k,jb in (("Gera",1),("Schleiz",3),("Lob",5),("Fü",7)):
        pb=inum(b107[1+i][jb])/num(b107[1+i][jb+1])*100
        pd=inum(Dd[(k,str(y))][2])/num(Dd[(k,str(y))][5])*100
        if abs(pb-pd)/pb>0.006: rep(f"{k} {y} pop implied births {pb:.0f} deaths {pd:.0f}")
