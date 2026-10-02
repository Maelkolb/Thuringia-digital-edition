"""Consistency checks of the printed temperature tables (means vs printed values)."""
from common import *
import statistics as st

def monthly(label, bid, i0=1, n=None):
    g = grid(label, bid)
    rows = []
    for r in g[1:]:
        rows.append((r[0], [num(x) for x in r[1:13]]))
    return rows

def seasons(vals):
    """Apr-Sep summer, Oct-Dec + Jan-Mar winter"""
    if any(v is None for v in vals): return None, None, None
    summer = st.mean(vals[3:9]); winter = st.mean(vals[9:12] + vals[0:3]); year = st.mean(vals)
    return summer, winter, year

def check(name, lab_m, bid_m, lab_s, bid_s):
    print("=====", name)
    m = [(y, v) for y, v in monthly(lab_m, bid_m) if y.strip().isdigit()]
    s = {r[0]: [num(x) for x in r[1:6]] for r in grid(lab_s, bid_s)[1:]}
    for y, v in m:
        su, wi, ye = seasons(v)
        pr = s.get(y)
        if su is None or pr is None: print(y, "incomplete"); continue
        d = [round(su - pr[0], 2), round(wi - pr[1], 2), round(ye - pr[4], 2)]
        flag = "  <<<" if any(abs(x) > 0.02 for x in d) else ""
        print(y, "calc", round(su, 2), round(wi, 2), round(ye, 2), "printed", pr[0], pr[1], pr[4], "diff", d, flag)
    # column means
    mm = []
    for j in range(12):
        col = [v[j] for y, v in m if v[j] is not None]
        mm.append(round(st.mean(col), 2))
    print("calc monthly means", mm)
    print("printed Mittel     ", [num(x) for x in grid(lab_m, bid_m)[-1][1:13]])

check("Gera", "55", "b7", "55", "b9")
check("Hohenleuben", "56", "b2", "56", "b3")
check("Schleiz", "56", "b5", "56", "b6")
check("Rothenacker", "57", "b2", "57", "b2")
