"""Parse Brückner's height lists (pp. 10-15, 20-24) into entry lists (reading order)."""
import re
from common import *

DASH = r"\s*[—–\-]\s*"
NUM = r"\d+(?:,\d+)?"
END = re.compile(rf"^(?P<name>.*?)\s+(?P<a>{NUM})(?:{DASH}(?P<b>{NUM}))?\s*'?\.?\s*\*?\)?\.?\)?$")
TOISE = re.compile(rf"^(?P<name>.*?)\s+(?P<a>{NUM})\s*Toisen\.?$")


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\n", " ")).strip()


def join_cont(prev, cur):
    prev = prev.rstrip()
    if prev.endswith("="):
        return prev[:-1] + cur.lstrip()
    return prev + " " + cur.lstrip()


def column_stream(cells):
    """Merge continuation lines: a cell with no trailing number is prefixed to the next cell."""
    out, pending = [], None
    for ref, c in cells:
        c = clean(c)
        if not c:
            continue
        if re.match(r"^Toisen\.?$", c) and out:
            out[-1] = (out[-1][0] + "+" + ref, out[-1][1] + " Toisen.")
            continue
        if pending is not None:
            c = join_cont(pending[1], c)
            ref = pending[0] + "+" + ref
            pending = None
        if END.match(c) or TOISE.match(c):
            out.append((ref, c))
        elif re.search(r"\bbis$", c):
            pending = (ref, c)
        else:
            pending = (ref, c)
    if pending:
        out.append((pending[0], pending[1]))   # unparsed leftover
    return out


def parse_entry(ref, c):
    m = TOISE.match(c)
    if m:
        return dict(ref=ref, raw=c, name=m.group("name").rstrip(",").strip(), lo=None, hi=None, toisen=num(m.group("a")))
    m = END.match(c)
    if not m:
        return dict(ref=ref, raw=c, name=c, lo=None, hi=None, error=True)
    name = m.group("name").strip().rstrip(",").strip()
    a = num(m.group("a"))
    b = num(m.group("b")) if m.group("b") else None
    # "1250 bis" continuation case: name ends with 'bis'
    mm = re.match(rf"^(.*?)\s+({NUM})\s+bis\s+({NUM})'?\.?$", c)
    if mm:
        name, a, b = mm.group(1).strip(), num(mm.group(2)), num(mm.group(3))
    return dict(ref=ref, raw=c, name=name, lo=a, hi=b if b is not None else a, range=b is not None)


def table_entries(page, bid, cols=(0, 1)):
    g = grid(page, bid)
    res = []
    for ci in cols:
        cells = [(f"{page}/{bid}/r{ri+1}c{ci+1}", row[ci] if ci < len(row) else "") for ri, row in enumerate(g)]
        for ref, c in column_stream(cells):
            res.append(parse_entry(ref, c))
    return res


if __name__ == "__main__":
    for page, bid in [("11", "b13"), ("12", "b1"), ("12", "b3"), ("13", "b1"), ("20", "b3"), ("21", "b1"), ("22", "b1")]:
        es = table_entries(page, bid)
        print(page, bid, len(es), "errors:", [e["raw"] for e in es if e.get("error")])
