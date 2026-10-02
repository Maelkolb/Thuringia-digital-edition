"""Shared helpers for the A06 analysis scripts (pp. 91-104, section t1-2-1).
Numbers are always read from the canonical page JSON (data/pages/*.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
assert (ROOT / "data" / "pages").exists(), ROOT
GENERATED_BY = "Claude Sonnet 5.5 (subagent A06)"
DATE = "2026-10-01"
SECTION = "t1-2-1"
THIN = " "  # narrow no-break space as thousands separator in German prose


def page(label):
    n = int(label) + 12
    return json.loads((ROOT / "data" / "pages" / f"{n:04d}.json").read_text(encoding="utf-8"))


def block(label, bid):
    p = page(label)
    return next(b for b in p["blocks"] if b["id"] == bid)


def grid(label, bid):
    return block(label, bid)["grid"]


DASHES = {"—", "–", "-", ""}


def num(s):
    """Parse a printed number: '1,07' -> 1.07, '-0,11' -> -0.11, dash -> None."""
    s = s.strip()
    if s in DASHES:
        return None
    s = s.replace("−", "-").replace(" ", "")
    return float(s.replace(",", "."))


def integer(s):
    s = s.strip()
    if s in DASHES:
        return None
    return int(s.replace(" ", ""))


def write(ana):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    ana.setdefault("generated_by", GENERATED_BY)
    ana.setdefault("date", DATE)
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)


# ---------------------------------------------------------------- formatting for prose
def de(x, nd=1, sign=False):
    """German number: decimal comma, narrow no-break space as thousands separator."""
    s = f"{abs(x):,.{nd}f}".replace(",", THIN).replace(".", ",")
    if x < 0:
        s = "−" + s
    elif sign:
        s = "+" + s
    return s


def en(x, nd=1, sign=False):
    s = f"{abs(x):,.{nd}f}"
    if x < 0:
        s = "−" + s
    elif sign:
        s = "+" + s
    return s


YEAR = {"de": "Jahr", "en": "Year"}


def tt(field, de_, en_=None):
    return {"field": field, "title": {"de": de_, "en": en_ if en_ else de_}}


def tt_fmt(field, de_, en_, fmt):
    return {"field": field, "title": {"de": de_, "en": en_}, "format": fmt}


def relabel(field, as_, mapping):
    """Vega-Lite calculate transform mapping German data values to bilingual labels.
    mapping = {value: (de, en)}"""
    def expr(i):
        items = ",".join("'%s':'%s'" % (k, v[i]) for k, v in mapping.items())
        return "({%s})[datum.%s]" % (items, field)
    return {"calculate": {"de": expr(0), "en": expr(1)}, "as": as_}


DISTRICTS = {
    "Gera": ("Gera", "Gera"),
    "Schleiz": ("Schleiz", "Schleiz"),
    "Lobenstein-Ebersdorf": ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"),
    "Fürstenthum": ("Fürstenthum", "Principality"),
}
DIST_KEYS = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstenthum"]
DIST_LABEL_EXPR = {"de": "datum.label", "en": "datum.label == 'Fürstenthum' ? 'Principality' : datum.label"}
DIST_TRANSFORM = relabel("district", "district_label", DISTRICTS)


def color_dist(field="district", legend=True, domain=None):
    c = {"field": field, "type": "nominal", "scale": {"domain": domain or DIST_KEYS}}
    c["legend"] = {"title": None, "labelExpr": DIST_LABEL_EXPR, "labelLimit": 260} if legend else None
    return c


def refs(*items):
    """refs(('91','b4','r3-r32'), ('92','b1')) -> list of ref dicts"""
    out = []
    for it in items:
        d = {"page": it[0], "block": it[1]}
        if len(it) > 2 and it[2]:
            d["rows"] = it[2]
        out.append(d)
    return out


def col(name, de_, en_, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": {"de": de_, "en": en_}, "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


# Brückner p. 832: 1 geographische Meile = 0,9894 künftige Meile (zu 7500 m)
MEILE_KM = 0.9894 * 7.5
SQM_KM2 = MEILE_KM ** 2  # km2 per square geographical mile (55.06)
