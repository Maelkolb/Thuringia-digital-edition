import re, sys, json
from common import *
from parse_tabs import BLOCKS, HEADS, norm
from parse_tabs2 import cells, BM

ABBR = {'Ernest','Magdal','Christ','Frieder','Friedr','Elis','Henr','Charl','Alex','Wilh','Ludw','Carol','Heinr','Soph','Magd','Marg','Kath','Joh','Dor','Jul','Gem','Wittwer','Wittwe'}
DATE = r"(?:\d{1,2}\.\s*(?:[A-Za-zäöü]+\.?)\s*)?"
YEARX = re.compile(r"\s*(?:\d{1,2}\.\s*[A-Za-zäöü]+\.?\s*)?(\d{4})")
DEATH = re.compile(r"\s*(?:\([^)]*\)\s*)?,?\s*†\s*(?:\d{1,2}\.\s*[A-Za-zäöü]+\.?\s*)?(\d{4})")

def entries(t):
    t = t.replace("§", "H.")
    marks = list(BM.finditer(t))
    out = []
    prev_end = 0
    for k, m in enumerate(marks):
        # name: back from m.start()
        seg = t[prev_end:m.start()]
        # boundaries
        cut = re.match(r"[\s.,;]*", seg).end() if k > 0 else 0
        if k > 0:
            for bm in re.finditer(r"\.\s+(?=[A-ZÄÖÜ])", seg):
                pre = seg[:bm.start()]
                lasttok = re.split(r"[\s,;]", pre.rstrip())[-1] if pre.strip() else ""
                ok = bool(re.search(r"\d$", lasttok)) or (len(lasttok) >= 4 and lasttok not in ABBR and not re.fullmatch(r"[IVXL]+", lasttok))
                if not ok:
                    continue
                tail = seg[bm.end():]
                if "†" in tail or re.search(r"\d", tail):
                    continue
                if tail.startswith("Gem"):
                    continue
                cut = bm.end()
        name = seg[cut:].strip(" ,;")
        same = bool(m.group(1))
        ym = YEARX.match(t, m.end())
        if not ym:
            out.append(dict(name=name, birth=None, death=None, raw=t[m.start():m.start()+40])); prev_end = m.end(); continue
        birth = int(ym.group(1)); end = ym.end()
        death = None
        if same:
            death = birth
        else:
            dm = DEATH.match(t, end)
            if dm:
                death = int(dm.group(1)); end = dm.end()
        out.append(dict(name=name, birth=birth, death=death, same_year=same))
        prev_end = end
    return out

if __name__ == "__main__":
    for pg,b,tab,pos,t in cells():
        es = entries(t)
        if len(es) > 1 or "-v" in sys.argv:
            print("==", pg, b, pos, "|", t[:2000])
            for e in es: print("    ", e)
