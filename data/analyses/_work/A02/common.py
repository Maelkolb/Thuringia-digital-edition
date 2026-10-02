"""Shared helpers for the A02 analysis scripts (reads canonical page JSON)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent  # reuss-edition
PAGES = {}
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    PAGES[p["slug"]] = p


def block(page, bid):
    p = PAGES[page]
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((page, bid))


def text(page, bid):
    b = block(page, bid)
    if b.get("grid"):
        return "\n".join(" | ".join(r) for r in b["grid"])
    return b["text"]


def write_analysis(ana):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)


FT_M = 0.3766242  # 1 preuss. Decimalfuss = 1/10 preuss. Ruthe = 0.3766242 m (p. 11 fn.: all heights are Decimalfuss; p. 831: 1 Ruthe = 3.766242 m)

YEAR = {"de": "Jahr", "en": "Year"}


def de(x, nd=1):
    """German number format (decimal comma, no thousands separator for 4-digit numbers)."""
    s = f"{x:.{nd}f}"
    return s.replace(".", ",")


def en(x, nd=1):
    return f"{x:.{nd}f}"


def num_in_text(s, page, bid):
    """Assert that the printed number string (e.g. "1721,7") occurs in the block text."""
    t = text(page, bid)
    pat = r"(?<![\d,.])" + re.escape(s) + r"(?![\d])"
    if not re.search(pat, t):
        raise AssertionError(f"{s!r} not found in {page}/{bid}: {t[:120]}")
    return float(s.replace(",", "."))
