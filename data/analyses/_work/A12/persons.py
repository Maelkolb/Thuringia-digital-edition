"""Build the person table (life dates) from Tab. VI-XIV, pp. 394-402."""
import re, json
from common import *
from parse_tabs import BLOCKS, HEADS, norm
from parse_tabs2 import cells, BM
import parse_tabs3 as P

# entries that are spouses / not members of the house or unusable: (page, block, pos, birth)
EXCLUDE = {
 ("395","b4","r1c2",1835),   # Pauline Louise Agnes v. Wuerttemberg (spouse)
 ("397","b4","r1c1",1797),   # placeholder, replaced by manual
 ("398","b2","r3c2",1749),   # unnamed 'g. u. + 1749' after the husband of Friederike (ambiguous)
 ("398","b2","r6c3",1798),   # Heinrich LXXIV: Tab. X says + 1855, Tab. XI and p. 388 show him alive
 ("401","b2","r1c5",1777),   # Babette Benigne v. Wenz zum Lahnstein (spouse)
 ("401","b3","p",1628),      # Sibille Magd. v. Kirchberg (spouse of Heinrich I.)
 ("401","b7","p",1819),      # Carol. v. Hessen-Homburg (spouse)
 ("397","b4","r1c2",1800),   # Heinrich LXXII. name only; Sophie Adelheid (b. 1800) is entered by the manual rule
 ("401","b7","p",1806),      # Isabelle v. Wenz zum Lahnstein (spouse of H. XIX.? not a descendant)
}
# manual replacement of messy cells: (page, block, pos) -> list of (name, birth, death, same_year)
MANUAL = {
 ("398","b2","r7c1"): [("H. LXI.",1784,1813)],   # print: H. LXI. (transcribed LX.)
 ("396","b2","r2c4"): [("H. V.",1650,1672),("H. VI.",1651,1651)],
 ("396","b3","r2c4"): [("H. II.",1702,1782),("H. III.",1704,1731),("H. VII.",1708,1731)],
 ("396","b3","r2c5"): [("H. XIV.",1717,1718),("H. XVII.",1719,1719),("H. XVIII.",1720,1720),("H. XX.",1721,1721)],
 ("397","b4","r1c1"): [("Caroline",1792,None),("Heinrich LXXII.",1797,1853),("Sophie Adelheid",1800,None)],
}
NAMEFIX = {"Christ.":"Magdal. Christ.","Eleonore":"Christ. Eleonore","Elise":"Frieder. Elise","Friederike":"Ernest. Friederike",
           "Victorie":"Ernest. Victorie","Adelheid":"Maria Carol. Adelheid"}

def clean_name(n):
    n = re.sub(r"^Tab\. [IVXL]+\.\s*", "", n.strip(" ,;"))
    n = n.split(",")[0].strip()
    n = NAMEFIX.get(n, n)
    return n

def sex_of(n):
    n = n.strip()
    if re.match(r"(Heinrich|H\.)(\s|$|,)", n) or n.startswith("Todter Prinz") : return "m"
    if n.startswith("Todte"): return "f"
    return "f"

def all_entries():
    out = []
    srcs = []
    for pg,b,tab,pos,t in cells():
        srcs.append((pg,b,tab,pos,t))
    inblocks = {(pg,b) for pg,b,_ in BLOCKS}
    for pg,b in HEADS:
        if (pg,b) in inblocks: continue
        bl = block(pg,b)
        # headings/paragraphs of the table heads (first person only)
        tab = {"394":"VI","395":"VII","396":"VIII","397":"IX","398":"X","399":"XI","400":"XII","401":"XIII","402":"XIV"}[pg]
        srcs.append((pg,b,tab,"head",norm(bl["text"])))
    for pg,b,tab,pos,t in srcs:
        if (pg,b,pos) in MANUAL:
            for nm,bi_,de in MANUAL[(pg,b,pos)]:
                out.append(dict(page=pg,block=b,tab=tab,pos=pos,name=nm,birth=bi_,death=de,same_year=(bi_==de)))
            continue
        es = P.entries(t)
        if pos == "head":
            es = es[:1]
        for e in es:
            if e["birth"] is None: continue
            if (pg,b,pos,e["birth"]) in EXCLUDE: continue
            e = dict(e); e.update(page=pg,block=b,tab=tab,pos=pos)
            out.append(e)
    return out

if __name__ == "__main__":
    es = all_entries()
    print(len(es))
    seen = {}
    for e in es:
        e["name"] = clean_name(e["name"])
        e["sex"] = sex_of(e["name"])
        k = (e["name"], e["birth"])
        seen.setdefault(k, []).append(e)
    dups = {k:v for k,v in seen.items() if len(v)>1}
    for k,v in dups.items():
        print("DUP", k, [(x["tab"],x["pos"],x["death"]) for x in v])
    odd = [e for e in es if e["death"] is not None and (e["death"]<e["birth"] or e["death"]-e["birth"]>95)]
    for e in odd: print("ODD", e)
    short = [e for e in es if len(e["name"])<6 or not re.match(r"[A-ZÄÖÜ]", e["name"])]
    for e in short: print("SHORT", e["name"], e["tab"], e["pos"], e["birth"], e["death"])


def build():
    es = all_entries()
    rows = []
    byk = {}
    for e in es:
        e["name"] = clean_name(e["name"])
        e["sex"] = sex_of(e["name"])
        base = re.split(r"\s+(?:von|v\.)\s+", e["name"])[0]
        k = (base, e["birth"])
        byk.setdefault(k, []).append(e)
    out = []
    for k, v in byk.items():
        # merge identical / complete duplicates
        seen = []
        for e in v:
            dupe = False
            for o in seen:
                if o["death"] == e["death"] or e["death"] is None or o["death"] is None:
                    if o["death"] is None and e["death"] is not None:
                        o.update(death=e["death"], same_year=e["same_year"], tab=e["tab"], pos=e["pos"], page=e["page"], block=e["block"])
                    dupe = True
                    break
            if not dupe:
                seen.append(e)
        out.extend(seen)
    return out

if __name__ == "__main__" and False:
    pass
