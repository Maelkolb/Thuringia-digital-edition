"""Shared helpers for the A10 analyses (Brückner pp. 242-262)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] if False else Path(r"C:\Users\totom\Projects\reuss-edition")
_PAGES = {}
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    _PAGES[d["slug"]] = d


def page(label):
    return _PAGES[label]


def block(label, bid):
    p = _PAGES[label]
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def grid(label, bid):
    return block(label, bid)["grid"]


def num(s):
    """'1,5' -> 1.5 ; '—' / '' -> None ; '75,367,300' -> int"""
    s = s.strip()
    if s in ("", "—", "-", "–"):
        return None
    t = s.replace(" ", "")
    # thousands separators like 71,923
    if t.count(",") > 1:
        t = t.replace(",", "")
    t = t.replace(",", ".")
    return float(t) if "." in t else int(t)


def bi(de, en):
    return {"de": de, "en": en}


def write_analysis(ana):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)


def de(x, dec=0):
    """German number format: 27527 -> '27.527', 1.5 -> '1,5'"""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def en(x, dec=0):
    return f"{x:,.{dec}f}"


GENERATED_BY = "Claude Sonnet 5.5 (subagent A10)"
DATE = "2026-10-01"
