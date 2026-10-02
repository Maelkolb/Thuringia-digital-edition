import sys, re
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

def rows_of(label, bid):
    g = grid(label, bid)
    out = []
    for i, r in enumerate(g, start=1):
        if len(r) == 17 and all(re.fullmatch(r"[\d—\-–\s]*", x) for x in r[1:]) and any(x.strip() for x in r[1:]) and r[1].strip() not in ("S.","S.*)"):
            out.append((i, r[0], [num(x) or 0 for x in r[1:]]))
    return out

allrows = []
for label, bid in [("252","b4"),("253","b1"),("254","b1")]:
    for i, name, v in rows_of(label, bid):
        allrows.append((label, bid, i, name, v))
print(len(allrows))
# per-row check: Fürstenthum = sum of 3 districts (columns S,G,D,F)
for label,bid,i,name,v in allrows:
    for c in range(4):
        tot = v[c]+v[4+c]+v[8+c]
        if tot != v[12+c]:
            print("ROWSUM MISMATCH", label, bid, f"r{i}", name, "col", "SGDF"[c], "districts", v[c], v[4+c], v[8+c], "sum", tot, "printed", v[12+c])
