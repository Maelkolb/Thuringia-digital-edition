from common import *
def rep(msg): print("  !!", msg)
def close(a,b,t): return abs(a-b)<=t
dist=["Gera","Schleiz","Lob","Fü"]
gd=grid("117","b4"); gb=grid("118","b2")
def parse(kind):
    T={}
    for i in range(8):
        k=dist[i//2]; y=1864 if i%2==0 else 1867
        if kind=="deaf":
            v=gd[3+i][2:]
        else:
            v=gb[3+i][1:]
        T[(k,y)]=[num(x) or 0 if x in ("—",) else num(x) for x in v]
        # '—' -> None -> treat 0
        T[(k,y)]=[0.0 if x=="—" else num(x) for x in v]
    return T
deaf=parse("deaf"); blind=parse("blind")
groups=[("urban",0,3),("rural",6,9),("all",12,15)]
for name,T in (("deaf",deaf),("blind",blind)):
    print("=====",name)
    for (k,y),v in T.items():
        for g,c0,r0 in groups:
            m,w,z=v[c0:c0+3]; rm,rw,rz=v[c0+3:c0+6]
            if m+w!=z: rep(f"{k} {y} {g} m+w {m}+{w}!={z}")
        if v[0]+v[6]!=v[12] or v[1]+v[7]!=v[13] or v[2]+v[8]!=v[14]: rep(f"{k} {y} urban+rural != all {v[0:3]} {v[6:9]} {v[12:15]}")
        # implied pops
        for g,c0,_ in groups:
            pops=[]
            for j in range(3):
                n=v[c0+j]; r=v[c0+3+j]
                pops.append(n/r*10000 if r else None)
            print(name,k,y,g,[round(p) if p else None for p in pops])
    for y in (1864,1867):
        for c in range(0,18):
            if c in (3,4,5,9,10,11,15,16,17): continue
            s=sum(T[(k,y)][c] for k in dist[:3])
            if s!=T[("Fü",y)][c]: rep(f"{name} {y} col{c} sum {s} vs Fü {T[('Fü',y)][c]}")
