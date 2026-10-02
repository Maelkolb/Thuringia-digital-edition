import sys
sys.path.insert(0, '.')
from common import *

def colsum(g, r0, r1, c):
    return sum(num(g[r][c]) or 0 for r in range(r0, r1))

print("== wind tables (sum row index 13, mean row 14)")
for page, bid, years in [("62","b3",10),("63","b2",7),("63","b4",2),("63","b6",1)]:
    g = grid(page, bid)
    for c in range(1, 9):
        s = colsum(g, 1, 13, c); ps = num(g[13][c]); pm = num(g[14][c])
        flag = "" if s == ps else "  <-- SUM MISMATCH"
        flag2 = "" if abs(s/years - pm) < 0.06 else f"  <-- MEAN: computed {s/years:.2f}"
        print(page, bid, g[0][c], "sum", s, "printed", ps, "mean", pm, flag, flag2)
print("total obs per table")
for page, bid in [("62","b3"),("63","b2"),("63","b4"),("63","b6")]:
    g = grid(page, bid)
    print(page, bid, sum(num(g[13][c]) for c in range(1,9)))

print("== cloud Gera p64 b6")
g = grid("64","b6")
for c in range(1, 7):
    s = colsum(g, 2, 14, c); print(g[1][c], "sum", round(s,2), "printed", g[14][c])
for r in range(2, 14):
    print(g[r][0], [num(g[r][c]) for c in range(1,7)], "tot", sum(num(g[r][c]) for c in range(1,4)), round(sum(num(g[r][c]) for c in range(4,7)),2),
      "per-year check", [round(num(g[r][c])/10,2) for c in range(1,4)])
print("== p65 b1")
g = grid("65","b1")
for c in range(1, 13):
    s = colsum(g, 3, 15, c); print(g[2][c], "sum", round(s,2), "printed", g[15][c])
for r in range(3, 15):
    print(g[r][0], sum(num(g[r][c]) for c in (1,2,3)), "per yr hohenl", round(sum(num(g[r][c]) for c in (4,5,6)),1), "schleiz tot", sum(num(g[r][c]) for c in (7,8,9)), round(sum(num(g[r][c]) for c in (10,11,12)),1))
