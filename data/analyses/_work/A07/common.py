"""Shared helpers for the A07 analysis scripts (chapter II.1 Statistik, pp. 105-118)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent  # reuss-edition
PAGES = {}
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    PAGES[p["slug"]] = p


def block(page, bid):
    p = PAGES[page]
    return next(b for b in p["blocks"] + p["footnotes"] if b["id"] == bid)


def grid(page, bid):
    return block(page, bid)["grid"]


def num(s):
    """'3,94' -> 3.94 ; '—' -> None ; '1 234' -> 1234"""
    s = str(s).strip()
    if s in ("—", "–", "-", ""):
        return None
    return float(s.replace(" ", "").replace(",", "."))


def inum(s):
    v = num(s)
    return None if v is None else int(round(v))


def write(ana, name=None):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)
    return out


GEN = "Claude Sonnet 5.5 (subagent A07)"
DATE = "2026-10-01"
YEAR = {"de": "Jahr", "en": "Year"}
DISTRICT = {"de": "Landestheil", "en": "District"}


# ---------------------------------------------------------------- formatting
def fde(x, nd=2):
    """German number format: 3.94 -> '3,94'; thousands separator none (as in the source)."""
    s = f"{x:.{nd}f}"
    return s.replace(".", ",")


def fen(x, nd=2):
    return f"{x:.{nd}f}"


def fint_de(x):
    return f"{int(round(x)):,}".replace(",", ".") if abs(x) >= 10000 else str(int(round(x)))


def fint_en(x):
    return f"{int(round(x)):,}"


# ---------------------------------------------------------------- dataset / spec helpers
def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": {"de": de, "en": en}, "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def bi(de, en):
    return {"de": de, "en": en}


def ref(page, block, rows=None, note=None):
    r = {"page": page, "block": block}
    if rows:
        r["rows"] = rows
    if note:
        r["note"] = note
    return r


def tip(field, de, en=None, fmt=None):
    t = {"field": field, "title": bi(de, en) if en else de}
    if fmt:
        t["format"] = fmt
    return t


def lab_expr(mapping_en):
    """Legend/axis labelExpr: German = the stored value; English = lookup in mapping."""
    chain = "datum.label"
    for k, v in reversed(list(mapping_en.items())):
        chain = f"datum.label == '{k}' ? '{v}' : ({chain})"
    return {"de": "datum.label", "en": chain}


DISTRICTS = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Reuß j. L."]
AREAS = ["Städte", "Landorte"]
AREA_EN = {"Städte": "Towns", "Landorte": "Rural places", "Zusammen": "Total"}
DIST_TITLE = bi("Landestheil", "District")
YEAR_AX = {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}}


def lab_expr2(map_de, map_en):
    """labelExpr with explicit German and English lookup (keys = stored values)."""
    def chain(m):
        c = "datum.label"
        for k, v in reversed(list(m.items())):
            c = f"datum.label == '{k}' ? '{v}' : ({c})"
        return c
    return {"de": chain(map_de), "en": chain(map_en)}


def ordk(field, domain, as_="ordk"):
    """calculate transform: position of `field` in the fixed domain (for a stable stacking order)."""
    arr = "[" + ", ".join("'" + d + "'" for d in domain) + "]"
    return {"calculate": f"indexof({arr}, datum.{field})", "as": as_}
