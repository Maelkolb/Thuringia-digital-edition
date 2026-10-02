"""Shared helpers for the G7 place analyses (Part II, Ortskunde)."""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent  # project root
ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")
PAGES = ROOT / "data" / "text" / "pages"


def load_entries():
    ents = []
    for f in sorted(glob.glob(str(ROOT / "data/gazetteer/G*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for e in d["entries"]:
            e["_pkg"] = d["package"]
            ents.append(e)
    return ents


def load_coords():
    c = json.load(open(ROOT / "data/gazetteer/coords.json", encoding="utf-8"))
    return c["coords"]


_page_cache = {}


def page_blocks(label):
    """-> ordered list of (block_id, text) for a printed page label."""
    if label in _page_cache:
        return _page_cache[label]
    p = PAGES / f"{label}.txt"
    out = []
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\[((?:b|fn)\d+)[^\]]*\]\s?(.*)", line)
            if m:
                out.append((m.group(1), m.group(2)))
            elif out:
                out[-1] = (out[-1][0], out[-1][1] + "\n" + line)
    _page_cache[label] = out
    return out


def bnum(b):
    return int(re.sub(r"\D", "", b))


def article_text(e):
    """Concatenate blocks b<n> (not footnotes) from start to end of an entry."""
    s, t = e["start"], e["end"]
    pages = [s["page"]]
    # walk page labels numerically
    try:
        a, b = int(s["page"]), int(t["page"])
        pages = [str(i) for i in range(a, b + 1)]
    except ValueError:
        pass
    txt = []
    for pg in pages:
        for bid, tx in page_blocks(pg):
            if not bid.startswith("b"):
                continue
            n = bnum(bid)
            if pg == s["page"] and n < bnum(s["block"]):
                continue
            if pg == t["page"] and n > bnum(t["block"]):
                continue
            txt.append(tx)
    return "\n".join(txt)


def refs_for(e):
    """Source refs (page, block) covering the article range of an entry."""
    s, t = e["start"], e["end"]
    try:
        pages = [str(i) for i in range(int(s["page"]), int(t["page"]) + 1)]
    except ValueError:
        pages = [s["page"]]
    out = []
    for pg in pages:
        for bid, _ in page_blocks(pg):
            if not bid.startswith("b"):
                continue
            n = bnum(bid)
            if pg == s["page"] and n < bnum(s["block"]):
                continue
            if pg == t["page"] and n > bnum(t["block"]):
                continue
            out.append({"page": pg, "block": bid})
    return out


# ---------------------------------------------------------------------------
# shared definitions for the G7 analyses
# ---------------------------------------------------------------------------
import math
import statistics as st

ANALYSES = ROOT / "data" / "analyses"
LT_ORDER = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
GENERATED_BY = "Claude Sonnet 5.5 (subagent G7)"
DATE = "2026-10-01"

# Bestandtheile / sub-entries whose numbers are already contained in another entry,
# plus Duerrenbach (belonged to Grumbach until 1869; Grumbach's figures include it)
NOT_OWN_GEMEINDE = {"poeppeln", "duerrenberg", "eleonorenthal", "koestritzer-bahnhof",
                    "heinrichshall", "chemische-fabrik", "duerrenbach"}
GEMEINDE_TYPES = ("Dorf", "Stadt", "Marktflecken", "Weiler", "Kammergut")
# zweiherrische places: the figures cover only the reussische Anteil (see per-entry notes)
PARTIAL = {"roschitz", "hundhaupten", "kraftsdorf", "seifartsdorf", "ruedersdorf",
           "bethenhausen", "weitisberga", "blintendorf", "moedlareuth"}
# coordinates in coords.json that fail the plausibility checks (wrong homonym etc.)
DOUBTFUL_COORDS = {("culm", "Gera"), ("reichenbach", "Gera"), ("wernsdorf", "Schleiz"),
                   ("lichtenau", "Gera"), ("platte", "Lobenstein-Ebersdorf"),
                   ("dittersdorf-tanna", "Schleiz")}

SIZE_CLASSES = [(1, "< 100", 0, 100), (2, "100–199", 100, 200), (3, "200–299", 200, 300),
                (4, "300–499", 300, 500), (5, "500–999", 500, 1000),
                (6, "1 000–1 999", 1000, 2000), (7, "≥ 2 000", 2000, 10**9)]


def size_class(n):
    for o, lab, lo, hi in SIZE_CLASSES:
        if lo <= n < hi:
            return o, lab
    raise ValueError(n)


def place_class(e):
    return {"Stadt": "Stadt", "Marktflecken": "Marktflecken"}.get(e["type"], "Dorf")


PLACE_CLASS_EN = {"Stadt": "Town", "Marktflecken": "Market town", "Dorf": "Village"}


def uid(e):
    """unique id (the gazetteer has two homonym id pairs)."""
    if e["id"] in ("wernsdorf", "hermannsdorf"):
        return e["id"] + "-" + e["landestheil"].split("-")[0].lower()
    return e["id"]


def coord(e, C):
    """(lon, lat, geonames) or (None, None, None) when missing/doubtful."""
    if (e["id"], e["landestheil"]) in DOUBTFUL_COORDS:
        return None, None, None
    c = C.get(e["id"])
    if not c:
        return None, None, None
    return c["lon"], c["lat"], c["geonames"]


def gemeinden(ents):
    return [e for e in ents if e["type"] in GEMEINDE_TYPES and e.get("inhabitants")
            and e.get("houses") and e["id"] not in NOT_OWN_GEMEINDE]


def lt_short(lt):
    return lt


def bi(de, en):
    return {"de": de, "en": en}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def fnum(x, nd=0, lang="de"):
    """format a number for prose."""
    if x is None:
        return "–"
    s = f"{x:,.{nd}f}".replace("-", "−")
    if lang == "de":
        s = s.replace(",", " ").replace(".", ",") if nd == 0 else s.replace(",", "X").replace(".", ",").replace("X", " ")
    return s


def pct(x, nd=1, lang="de"):
    s = fnum(x, nd, lang)
    return s + (" %" if lang == "de" else "%")


def uniq_refs(entries_or_refs):
    """unique, ordered [{'page','block'}] for a list of entries (article ranges)."""
    seen = {}
    for e in entries_or_refs:
        for r in (refs_for(e) if "start" in e else [e]):
            seen[(int(r["page"]), bnum(r["block"]))] = {"page": r["page"], "block": r["block"]}
    return [seen[k] for k in sorted(seen)]


def write_analysis(a):
    out = ANALYSES / f"{a['id']}.json"
    out.write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written", out, f"{out.stat().st_size/1024:.0f} kB")
    return out


def median(v):
    return st.median(v) if v else None


def mean(v):
    return st.mean(v) if v else None


# Goeritz / Neundorf: the entries hold the figure of the Ort alone; the article also gives the
# figure of the whole Gemeinde, which Brueckner's statistics (p. 98) use.
OVERRIDE_INH = {"goeritz": {"inhabitants": 607, "houses": 89},
                "neundorf-lobenstein": {"inhabitants": 716}}


def eff(e):
    """(inhabitants, houses) of the political Gemeinde."""
    o = OVERRIDE_INH.get(e["id"], {})
    return o.get("inhabitants", e["inhabitants"]), o.get("houses", e["houses"])


def sort_key(e):
    return (LT_ORDER.index(e["landestheil"]), int(e["start"]["page"]), int(e["start"]["block"][1:]))
