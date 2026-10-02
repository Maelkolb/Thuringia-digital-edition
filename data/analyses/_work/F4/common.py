import copy
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = "C:/Users/totom/Projects/reuss-edition/"
ARCHIVE = ROOT + "data/analyses/_archive/"
OUT = ROOT + "data/analyses/"
SHARED = ROOT + "data/analyses/_shared/"


def archive(aid):
    with open(ARCHIVE + aid + ".json", encoding="utf-8") as f:
        return json.load(f)


def dataset(aid, name, new_name=None, drop_columns=(), keep_rows=None):
    d = archive(aid)
    ds = copy.deepcopy(next(x for x in d["datasets"] if x["name"] == name))
    if drop_columns:
        idx = [i for i, c in enumerate(ds["columns"]) if c["name"] not in drop_columns]
        ds["columns"] = [ds["columns"][i] for i in idx]
        ds["rows"] = [[r[i] for i in idx] for r in ds["rows"]]
    if keep_rows is not None:
        ds["rows"] = [r for r in ds["rows"] if keep_rows(dict(zip([c["name"] for c in ds["columns"]], r)))]
    if new_name:
        ds["name"] = new_name
    return ds


def shared(fname):
    with open(SHARED + fname, encoding="utf-8") as f:
        return json.load(f)


def rows_of(ds):
    names = [c["name"] for c in ds["columns"]]
    return [dict(zip(names, r)) for r in ds["rows"]]


def bi(de, en):
    return {"de": de, "en": en}


def num(x, dec=0, lang="de"):
    """Format a number for running text: German 1.234,5 or English 1,234.5."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP)
    s = f"{q:,.{dec}f}"
    if lang == "de":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def pair(x, dec=0):
    return num(x, dec, "de"), num(x, dec, "en")


def write_feature(obj):
    path = OUT + obj["id"] + ".json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print("written", path)


def words(s):
    return len(s.split())


def check_limits(obj):
    problems = []
    def lim(label, b, mx):
        for l in ("de", "en"):
            if words(b[l]) > mx:
                problems.append(f"{label} [{l}] {words(b[l])} > {mx}")
    lim("title", obj["title"], 12)
    lim("summary", obj["summary"], 75)
    for i, f in enumerate(obj.get("findings", [])):
        lim(f"finding{i+1}", f, 35)
    for i, c in enumerate(obj.get("caveats", [])):
        lim(f"caveat{i+1}", c, 60)
    lim("method", obj["method"], 260)
    for c in obj["charts"]:
        lim(c["id"] + " title", c["title"], 16)
        lim(c["id"] + " caption", c["caption"], 45)
    for p in problems:
        print("LIMIT", p)
    return not problems


def tooltip(field, de, en=None, fmt=None, **kw):
    t = {"field": field, "title": {"de": de, "en": en or de}}
    if fmt:
        t["format"] = fmt
    t.update(kw)
    return t
