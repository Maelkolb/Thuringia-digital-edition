"""Shared helpers for the A09 analysis scripts (pp. 208-241, chapter III 1-4).
Reads canonical page JSON; never types printed numbers by hand."""
import json, re
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[4]
PAGES = {}
for f in (ROOT / "data" / "pages").glob("*.json"):
    p = json.loads(f.read_text(encoding="utf-8"))
    PAGES[p["slug"]] = p

GENERATED_BY = "Claude Sonnet 5.5 (subagent A09)"
DATE = "2026-10-01"
MORGEN_HA = 0.255322  # Brückner p. 832: 1 preuß. Morgen = 0,255322 ha


def block(page, bid):
    p = PAGES[page]
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((page, bid))


def grid(page, bid):
    """Grid as list of rows; row N of the text view (rN) is grid[N-1]."""
    return block(page, bid)["grid"]


def row(page, bid, n):
    return grid(page, bid)[n - 1]


DASH = {"—", "–", "-", "", "—", "–"}


def num(s):
    """Parse a printed German number: '1234', '12,5', '5666 2/3', '—' -> None/0 handled by caller."""
    s = s.strip()
    s = re.sub(r"\s*\*+\)$", "", s)  # footnote markers like **)
    if s in DASH:
        return None
    s = s.replace(" ", " ")
    m = re.fullmatch(r"(\d+)\s+(\d+)/(\d+)", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    m = re.fullmatch(r"(\d+)/(\d+)", s)
    if m:
        return int(m.group(1)) / int(m.group(2))
    s = s.replace(" ", "")
    if re.fullmatch(r"\d+,\d+", s):
        return float(s.replace(",", "."))
    if re.fullmatch(r"\d+", s):
        return int(s)
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        return int(s.replace(".", ""))
    raise ValueError(f"cannot parse number {s!r}")


def n0(s):
    """num() with dash -> 0"""
    v = num(s)
    return 0 if v is None else v


def bi(de, en):
    return {"de": de, "en": en}


def write_analysis(ana):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)
    return out


def de_num(x, nd=1):
    """German decimal formatting for prose, e.g. 1234.5 -> '1234,5' (thousands with thin separator not used)."""
    s = f"{x:,.{nd}f}"
    s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s


def en_num(x, nd=1):
    return f"{x:,.{nd}f}"
