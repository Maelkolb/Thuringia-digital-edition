import sys, itertools
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
import estates_parse as ep
from a09common import *

K, KT = ep.kammer_rows()
R, RT = ep.ritter_estates()
keys = ["hof", "garten", "feld", "wiese", "nadel", "laub", "hut", "wasser", "steuer"]

def printed_sum(T, lt, key):
    # printed 'Summe' rows: first 'sum' row with lt
    rows = [t for t in T if t["name"] == "Summe" and t["lt"] == lt]
    return rows[0][key] if rows else None

def cands(vals, target, tol=0.011):
    """vals: list of (label, value, fmt string). find single digit substitutions that reach the target sum."""
    total = sum(v for _, v in vals)
    out = []
    for lab, v in vals:
        s = f"{v:.2f}"
        for pos, ch in enumerate(s):
            if ch == ".":
                continue
            for d in "0123456789":
                if d == ch: continue
                s2 = s[:pos] + d + s[pos+1:]
                v2 = float(s2)
                if abs(total - v + v2 - target) <= tol:
                    out.append((lab, s, s2))
    return total, out

for name, E, T in (("KAMMER", K, KT), ("RITTER", R, RT)):
    print("=====", name)
    for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
        for key in keys:
            ptr = printed_sum(T, lt, key)
            if ptr is None: continue
            vals = [(e["name"], e[key]) for e in E if e["lt"] == lt and e[key] is not None]
            tot = round(sum(v for _, v in vals), 2)
            if abs(tot - ptr) > 0.02:
                total, c = cands(vals, ptr)
                print(f"{lt:22s} {key:7s} sum={tot:10.2f} printed={ptr:10.2f} diff={tot-ptr:8.2f}  cands={c[:8]}")
