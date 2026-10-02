from common import *
def rep(msg): print("  !!", msg)
def close(a,b,t): return abs(a-b)<=t
g=grid("105","b3")
for r in g[1:]:
    a,b,c=inum(r[1]),inum(r[3]),inum(r[5]); tot=a+b+c
    pcts=[num(r[2]),num(r[4]),num(r[6])]
    calc=[x/tot*100 for x in (a,b,c)]
    for p,cv in zip(pcts,calc):
        if not close(p,cv,0.011): rep(f"{r[0]}: {p} vs {cv:.2f}")
    print(r[0], tot, round(sum(pcts),2))
# sums
rows={r[0]:r for r in g[1:]}
for lab,(x,y) in {"Gera Summe":("Gera Stadt","Gera Plattland"),"Schleiz Summe":("Schleiz Städte","Schleiz Plattland"),"Lobenstein-Ebersdorf Summe":("Lobenstein-Ebersdorf Städte","Lobenstein-Ebersdorf Plattland")}.items():
    for c in (1,3,5):
        if inum(rows[x][c])+inum(rows[y][c])!=inum(rows[lab][c]): rep(f"{lab} col{c}")
for c in (1,3,5):
    s=sum(inum(rows[k][c]) for k in ("Gera Stadt","Schleiz Städte","Lobenstein-Ebersdorf Städte"))
    if s!=inum(rows["Fürstenthum Städte"][c]): rep(f"Fü Städte col{c} {s} vs {rows['Fürstenthum Städte'][c]}")
    s=sum(inum(rows[k][c]) for k in ("Gera Plattland","Schleiz Plattland","Lobenstein-Ebersdorf Plattland"))
    if s!=inum(rows["Fürstenthum Plattland"][c]): rep(f"Fü Platt col{c} {s} vs {rows['Fürstenthum Plattland'][c]}")
    s=sum(inum(rows[k][c]) for k in ("Gera Summe","Schleiz Summe","Lobenstein-Ebersdorf Summe"))
    if s!=inum(rows["Fürstenthum Summe"][c]): rep(f"Fü Summe col{c} {s} vs {rows['Fürstenthum Summe'][c]}")
g=grid("105","b5"); print(g)
s=sum(num(r[0]) for r in g[1:10]); print("foreign sum", s)
print("== p106 religion")
g=grid("106","b2"); print(g)
for r in g[1:]:
    v=[inum(x) or 0 for x in r[1:]]; print(r[0], sum(v))
print("== p118 emigration")
g=grid("118","b5"); print(g)
for r in g[1:4]:
    v=[inum(x) for x in r[1:5]]
    if sum(v[:3])!=v[3]: rep(f"{r[0]} {v}")
for c in range(1,5):
    s=sum(inum(g[i][c]) for i in (1,2,3))
    if s!=inum(g[4][c]): rep(f"col{c} sum {s} vs {g[4][c]}")
g=grid("118","b6") if False else block("118","b6")
print(block("118","b6"))
