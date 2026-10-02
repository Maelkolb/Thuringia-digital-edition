import sys
sys.path.insert(0,'data/analyses/_work/A09')
from a09common import *

# Collect the 14 classes: (page, block, first_row (1-based), column offset)
# p209 b3: classes 1,2 rows 3-14 ; classes 3,4 rows 17-28
# p210 b1: 5,6: rows 3-14; 7,8: rows 16-27; 9,10: rows 29-40
# p211 b1: 11,12: rows 3-14; b2: 13,14: rows 3-14
blocks = [
 ("209","b3",3,[(1,"Land- u. Forstwirthschaft"),(6,"Bergbau")]),
 ("209","b3",17,[(1,"Industrie"),(6,"Handel")]),
 ("210","b1",3,[(1,"Transportgewerbe"),(6,"Handarbeiter u. Taglöhner")]),
 ("210","b1",16,[(1,"Geistliche und Lehrer"),(6,"Beamte und Angestellte")]),
 ("210","b1",29,[(1,"Militär"),(6,"Wissenschaft und Kunst")]),
 ("211","b1",3,[(1,"Pensionärs und Rentiers"),(6,"Personen ohne Berufsausübung")]),
 ("211","b2",3,[(1,"Personen ohne angegebenen Beruf"),(6,"Alle Berufsklassen")]),
]
AREAS = ["Gera-Städte","Gera-Platt","Gera","Schleiz-Städte","Schleiz-Platt","Schleiz","LE-Städte","LE-Platt","LE","F-Städte","F-Platt","F"]
data = {}
for page, bid, r0, cls in blocks:
    g = grid(page, bid)
    for off, name in cls:
        for i, a in enumerate(AREAS):
            r = g[r0-1+i]
            vals = [num(x) or 0 for x in r[off:off+5]]
            data[(name,a)] = vals
# checks
bad = 0
for (name,a),v in data.items():
    if sum(v[:4]) != v[4]:
        print("ROLE SUM MISMATCH", name, a, v); bad+=1
for name in set(k[0] for k in data):
    for g_, parts in [("Gera",("Gera-Städte","Gera-Platt")),("Schleiz",("Schleiz-Städte","Schleiz-Platt")),("LE",("LE-Städte","LE-Platt")),("F",("F-Städte","F-Platt"))]:
        s = [data[(name,p)][k] for p in parts for k in range(5)]
        t = [x+y for x,y in zip(data[(name,parts[0])], data[(name,parts[1])])]
        if t != data[(name,g_)]:
            print("AREA SUM MISMATCH", name, g_, t, data[(name,g_)]); bad+=1
    s = [sum(data[(name,d)][k] for d in ("Gera","Schleiz","LE")) for k in range(5)]
    if s != data[(name,"F")]:
        print("FSUM MISMATCH", name, s, data[(name,"F")]); bad+=1
# sum over classes = class 14
classes = [n for _,_,_,c in blocks for _,n in c if n!="Alle Berufsklassen"]
for a in AREAS:
    s = [sum(data[(n,a)][k] for n in classes) for k in range(5)]
    if s != data[("Alle Berufsklassen",a)]:
        print("CLASS SUM MISMATCH", a, s, data[("Alle Berufsklassen",a)]); bad+=1
print("bad", bad)
# percentages p212
g = grid("212","b2")
print(g[0])
heads = ["Land- u. Forstwirthschaft","Bergbau","Industrie","Handel","Transportgewerbe","Handarbeiter u. Taglöhner","Geistliche und Lehrer","Beamte und Angestellte","Militär","Wissenschaft und Kunst","Pensionärs und Rentiers"]
for i,a in enumerate(AREAS):
    r = g[1+i]
    pct = [num(x) for x in r[1:12]]
    # col 13 is merged 'x y'
    comp = [100*data[(h,a)][4]/data[("Alle Berufsklassen",a)][4] for h in heads]
    diff = [ (h, p, round(c,2)) for h,p,c in zip(heads,pct,comp) if p is not None and abs(p-c)>0.011]
    print(r[0], len(r), r[-1], diff)
