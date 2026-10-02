import sys, re
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *
def n(x): return num(x) or 0
# group sums p252/253/254
def numrows(label, bid):
    g = grid(label, bid)
    res=[]
    for i,r in enumerate(g, start=1):
        if len(r)==17 and all(re.fullmatch(r"[\d—\-–\s]*", x) for x in r[1:]) and any(x.strip() for x in r[1:]) and r[1].strip() not in ("S.",):
            res.append((i,r[0],[n(x) for x in r[1:]]))
    return res
def colsum(rows):
    return [sum(v[c] for _,_,v in rows) for c in range(16)]
# p252: group 1 rows r4-r9 sum t10 ; group 2 r12-r26 sum t27
g=numrows("252","b4")
d={i:(nm,v) for i,nm,v in g}
def chk(label, rowidx, totidx, rows):
    s=[sum(rows[i][1][c] for i in rowidx) for c in range(16)]
    t=rows[totidx][1]
    diff=[(c, s[c], t[c]) for c in range(16) if s[c]!=t[c]]
    print(label, "tot r%d"%totidx, "diffs (col, computed, printed):", diff)
chk("p252 Nahrung", range(4,10), 10, d)
chk("p252 Kleidung", range(12,27), 27, d)
g3=numrows("253","b1"); d3={i:(nm,v) for i,nm,v in g3}
chk("p253 Bau", range(4,11), 11, d3)
g4=numrows("254","b1"); d4={i:(nm,v) for i,nm,v in g4}
# Haus: p253 r13-r42 + p254 r4-r16 ; compare to p254 r17 total; Latus r43 and Transport r3
chk("p253 Latus", range(13,43), 43, d3)
rows=[d3[i] for i in range(13,43)]+[d4[i] for i in range(4,17)]
s=[sum(v[c] for _,v in rows) for c in range(16)]
print("Haus total computed", s)
print("Haus printed t17", d4[17][1])
print("sonst r19+r20 ->", [d4[19][1][c]+d4[20][1][c] for c in range(16)], "printed", d4[21][1])
