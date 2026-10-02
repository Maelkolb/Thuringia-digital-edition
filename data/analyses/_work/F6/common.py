"""Shared helpers for agent F6 (bergbau, handel-verkehr, staatsfinanzen, rechtspflege)."""
import sys, json, copy, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
ANALYSES = ROOT / "data" / "analyses"
ARCHIVE = ANALYSES / "_archive"
SHARED = ANALYSES / "_shared"
GENERATED_BY = "Claude Sonnet 5.5 (Agent F6), aus {n} Einzelauswertungen zusammengeführt"
DATE = "2026-10-02"


def archive(i):
    return json.load(open(ARCHIVE / f"{i}.json", encoding="utf-8"))


def dataset(arch, name, new_name=None, drop_cols=(), add_cols=(), row_filter=None):
    """Copy one dataset of an archived analysis. add_cols: list of (column dict, function(row dict)->value)."""
    ds = copy.deepcopy(next(d for d in arch["datasets"] if d["name"] == name))
    if new_name:
        ds["name"] = new_name
    names = [c["name"] for c in ds["columns"]]
    rows = [dict(zip(names, r)) for r in ds["rows"]]
    if row_filter:
        rows = [r for r in rows if row_filter(r)]
    for col, fn in add_cols:
        ds["columns"].append(col)
        for r in rows:
            r[col["name"]] = fn(r)
    keep = [c for c in ds["columns"] if c["name"] not in drop_cols]
    ds["columns"] = keep
    ds["rows"] = [[r[c["name"]] for c in keep] for r in rows]
    return ds


def rows(ds):
    names = [c["name"] for c in ds["columns"]]
    return [dict(zip(names, r)) for r in ds["rows"]]


def col(name, de, en, typ="string", unit=None, derived=False, note=None):
    c = {"name": name, "label": {"de": de, "en": en}, "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def new_dataset(name, title_de, title_en, columns, row_dicts, source_refs):
    return {"name": name, "title": {"de": title_de, "en": title_en}, "columns": columns,
            "rows": [[r[c["name"]] for c in columns] for r in row_dicts], "source_refs": source_refs}


def uniq_sources(*lists):
    seen, out = set(), []
    for lst in lists:
        for s in lst:
            k = (s["page"], s["block"])
            if k not in seen:
                seen.add(k)
                out.append({"page": s["page"], "block": s["block"]})
    return out


def _sep(n, dec, thou, point):
    s = f"{abs(n):,.{dec}f}"
    s = s.replace(",", "\0").replace(".", point).replace("\0", thou)
    return ("-" if n < 0 else "") + s


def de(n, dec=0):
    """German number format: thousands '.', decimals ','; four-digit numbers also grouped (1.234)."""
    return _sep(n, dec, ".", ",")


def en(n, dec=0):
    return _sep(n, dec, ",", ".")


def words(s):
    return len(s.split())


def write_analysis(a):
    out = ANALYSES / f"{a['id']}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    print("written", out)


def check_limits(a):
    def lim(label, bi, mx):
        for l in ("de", "en"):
            w = words(bi[l])
            flag = "  <-- TOO LONG" if w > mx else ""
            print(f"  {label:<14}{l}: {w:3d}/{mx}{flag}")
    lim("title", a["title"], 12)
    lim("summary", a["summary"], 75)
    for i, f in enumerate(a.get("findings", [])):
        lim(f"finding {i+1}", f, 35)
    for i, f in enumerate(a.get("caveats", [])):
        lim(f"caveat {i+1}", f, 60)
    lim("method", a["method"], 260)
    for c in a["charts"]:
        lim(f"{c['id']} title", c["title"], 16)
        lim(f"{c['id']} caption", c["caption"], 45)


def base_layers():
    p = json.load(open(SHARED / "base_places.json", encoding="utf-8"))
    r = json.load(open(SHARED / "base_rivers.json", encoding="utf-8"))
    return p, r


def assert_in_page(page, text):
    """Printed numbers quoted in prose but not in a dataset must occur on the cited page."""
    t = (ROOT / "data" / "text" / "pages" / f"{page}.txt").read_text(encoding="utf-8")
    assert text in t, f"{text!r} not found on page {page}"
