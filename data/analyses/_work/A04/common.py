"""Shared helpers for the A04 analyses (Brückner, ch. 7 Klima, pp. 62-70)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent  # reuss-edition
PAGES = {}
for f in (ROOT / "data/pages").glob("*.json"):
    p = json.loads(f.read_text(encoding="utf-8"))
    PAGES[p["slug"]] = p


def block(page, bid):
    return next(b for b in PAGES[page]["blocks"] if b["id"] == bid)


def grid(page, bid):
    return block(page, bid)["grid"]


def num(s):
    """Parse a printed number: '210,3' -> 210.3, '—' / '' -> None, '124 Max.' -> 124.
    Mixed fractions such as '1 14/15' are handled by frac()."""
    s = s.strip()
    if s in ("", "—", "-", "–"):
        return None
    s = re.sub(r"\s*(Max\.|Min\.)\s*$", "", s)
    s = s.replace("—", "-").replace(" ", "")
    return float(s.replace(",", "."))


def mark(s):
    m = re.search(r"(Max\.|Min\.)\s*$", s.strip())
    return m.group(1) if m else ""


def frac(s):
    """'1 14/15' -> 1+14/15, '4/5' -> 0.8, '10' -> 10, '—' -> 0."""
    s = re.sub(r"\s*(Max\.|Min\.)\s*$", "", s.strip())
    if s in ("—", "", "-"):
        return 0.0
    tot = 0.0
    for part in s.split():
        if "/" in part:
            a, b = part.split("/")
            tot += int(a) / int(b)
        else:
            tot += float(part.replace(",", "."))
    return tot


MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "October", "November", "December"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DIRS = ["N", "NO", "O", "SO", "S", "SW", "W", "NW"]


# ---- bilingual snippets for Vega-Lite specs ---------------------------------
def bi(de, en):
    return {"de": de, "en": en}


DIR_EN_MAP = "{'N':'N','NO':'NE','O':'E','SO':'SE','S':'S','SW':'SW','W':'W','NW':'NW'}"
DIR_LABEL_CALC = {"calculate": bi("datum.direction", f"{DIR_EN_MAP}[datum.direction]"), "as": "dir_label"}
MONTH_ABBR_CALC = {
    "calculate": bi("['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'][datum.month-1]",
                    "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][datum.month-1]"),
    "as": "mlabel",
}
MONTH_ABBR_DE = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
MONTH_ABBR_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
SEASON_DE = {12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Frühling', 4: 'Frühling', 5: 'Frühling',
             6: 'Sommer', 7: 'Sommer', 8: 'Sommer', 9: 'Herbst', 10: 'Herbst', 11: 'Herbst'}
SEASON_EN_CALC = {"calculate": bi("datum.season", "{'Winter':'Winter','Frühling':'Spring','Sommer':'Summer','Herbst':'Autumn'}[datum.season]"), "as": "season_label"}


# ---- number formatting --------------------------------------------------------
def fmt(x, lang, dec=0):
    """German: 12.796 / 24,9 ; English: 12,796 / 24.9"""
    s = f"{x:,.{dec}f}"
    if lang == "de":
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s


def pct(x, lang, dec=1):
    return fmt(x, lang, dec) + (" %" if lang == "de" else " %")


# ---- wind rose (polar small multiples) -------------------------------------------
THETA_SCALE = {"domain": [0.5, 8.5], "range": [-0.3927, 5.8905]}  # N centred at 12 o'clock, clockwise


def rose_spec(facet_field, facet_sort_field, *, columns=2, cell=200, rmax=78, rings=(10, 20, 30), dom_max=40,
              label_r=92, extra_transform=None, radius_field="share", radius_title="%", tooltip_extra=None):
    """Wind-rose small multiples. Dataset needs: direction (N,NO,O,SO,S,SW,W,NW), dir_index (1..8), <radius_field>,
    and the facet field (already a bilingual-capable label field produced by extra_transform)."""
    rscale = {"type": "sqrt", "domain": [0, dom_max], "rangeMax": rmax}
    tooltip = [{"field": "dir_label", "title": bi("Richtung", "Direction")},
               {"field": radius_field, "title": radius_title, "format": ".1f"}]
    tooltip += tooltip_extra or []
    transform = list(extra_transform or []) + [
        DIR_LABEL_CALC,
        {"calculate": "datum.dir_index-0.5", "as": "dir_lo"},
        {"calculate": "datum.dir_index+0.5", "as": "dir_hi"},
    ]
    return {
        "autosize": {"type": "pad"},
        "columns": columns,
        "facet": {"field": facet_field, "type": "nominal", "sort": {"field": facet_sort_field, "op": "min"}, "title": None},
        "spec": {
            "width": cell, "height": cell,
            "layer": [
                {   # thin reference rings (same radius scale as the wedges), about 1.2 px thick
                    "transform": [{"filter": "datum.dir_index == 1"}, {"calculate": json.dumps(list(rings)), "as": "ring"},
                                  {"flatten": ["ring"]}, {"calculate": f"pow(sqrt(datum.ring)-{1.2 / rmax * dom_max ** 0.5:.4f},2)", "as": "ring_in"}],
                    "mark": {"type": "arc", "opacity": 0.5, "strokeWidth": 0},
                    "encoding": {"theta": {"value": 0}, "theta2": {"value": 6.2832},
                                 "radius": {"field": "ring", "type": "quantitative", "scale": rscale},
                                 "radius2": {"field": "ring_in", "type": "quantitative"}}},
                {   # wedges
                    "mark": {"type": "arc"},
                    "encoding": {"theta": {"field": "dir_lo", "type": "quantitative", "scale": THETA_SCALE, "stack": False},
                                 "theta2": {"field": "dir_hi"},
                                 "radius": {"field": radius_field, "type": "quantitative", "scale": rscale},
                                 "tooltip": tooltip}},
                {   # value labels just outside the wedge tips
                    "mark": {"type": "text", "fontSize": 10, "radiusOffset": 9},
                    "encoding": {"theta": {"field": "dir_index", "type": "quantitative", "scale": THETA_SCALE, "stack": False},
                                 "radius": {"field": radius_field, "type": "quantitative", "scale": rscale},
                                 "text": {"field": radius_field, "type": "quantitative", "format": ".0f"}}},
                {   # compass letters
                    "mark": {"type": "text", "fontSize": 11, "fontWeight": 600},
                    "encoding": {"theta": {"field": "dir_index", "type": "quantitative", "scale": THETA_SCALE, "stack": False},
                                 "radius": {"value": label_r}, "text": {"field": "dir_label"}}},
            ]},
        "transform": transform,
    }


GENERATED_BY = "Claude Sonnet 5.5 (subagent A04)"
DATE = "2026-10-01"


def write_analysis(ana):
    out = ROOT / "data/analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)
    return out


def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


MONTH_FULL_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MONTH_FULL_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
