import sys
sys.path.insert(0, '.')
from common import *
print("== p66 b3 Gera phenomena")
g = grid("66","b3")
print(g[0])
for c in range(1, 12):
    vals = [num(g[r][c]) or 0 for r in range(1, 13)]
    s = sum(vals); print(g[0][c], "sum", s, "printed", g[13][c], "mittel printed", g[14][c], "calc/12", round(s/12,2))
print("== p66 b5 Hohenleuben")
g = grid("66","b5")
for c in range(1, 4):
    vals = [frac(g[r][c]) for r in range(1, 13)]
    print(g[0][c], "sum", round(sum(vals),3), "printed", g[13][c], "=", round(frac(g[13][c]),3))
print("== p67 b2")
g = grid("67","b2")
for c in range(1, 11):
    vals = [num(g[r][c]) or 0 for r in range(1, 13)]
    print(c, "sum", sum(vals), "printed", g[13][c], "mittel", g[14][c], "calc/2", sum(vals)/2)
print("== p67 b7")
g = grid("67","b7")
for r in (1,2):
    print(g[r][0], sum(num(x) or 0 for x in g[r][1:]))
for c in range(1,13):
    print(g[0][c], (num(g[1][c]) or 0)+(num(g[2][c]) or 0), g[3][c])
print("== p68 b2")
g = grid("68","b2")
print(g)
print(sum(num(x) for x in g[1][1:]), sum(num(x) for x in g[3][1:]))
print("== p69 b1")
g = grid("69","b1")
for r in range(1,9):
    print(g[r][0], num(g[r][1])+num(g[r][2]), g[r][3], "season sum", sum(num(g[r][c]) for c in range(4,8)), "/4", sum(num(g[r][c]) for c in range(4,8))/4, g[r][8])
for c in range(1,9):
    vals=[num(g[r][c].replace('*)','')) for r in range(1,9)]
    print(g[0][c], "mean", round(sum(vals)/8,3), "printed", g[9][c])
