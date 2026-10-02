"""Shared helpers for the A05 analysis scripts (pp. 70-90, Vegetation / Fauna)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3].parent  # .../reuss-edition
assert (ROOT / "data" / "pages").exists(), ROOT
OUT = ROOT / "data" / "analyses"

_PAGES = {}
for f in (ROOT / "data" / "pages").glob("*.json"):
    p = json.loads(f.read_text(encoding="utf-8"))
    _PAGES[p["slug"]] = p

GEN = "Claude Sonnet 5.5 (subagent A05)"
DATE = "2026-10-01"


def page(label):
    return _PAGES[label]


def block(label, bid):
    p = _PAGES[label]
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def text(label, bid):
    b = block(label, bid)
    if b.get("grid"):
        return "\n".join(" | ".join(r) for r in b["grid"])
    return b["text"]


def grid(label, bid):
    return block(label, bid)["grid"]


def num(s):
    return float(str(s).replace(",", ".").strip())


def bi(de, en):
    return {"de": de, "en": en}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def write(ana):
    out = OUT / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)


def need(sub, label, bid):
    """Assert that a string occurs in the cited block (guards typed-in names)."""
    t = text(label, bid)
    norm = lambda s: re.sub(r"\s+", " ", s.replace("-\n", "").replace("\n", " "))
    if norm(sub) not in norm(t):
        raise AssertionError(f"{sub!r} not in {label}/{bid}")
    return True


# bilingual tooltip titles reused everywhere
T_PAGE = bi("Seite", "Page")


def de(x, nd=1):
    """German number format (decimal comma)."""
    return f"{x:.{nd}f}".replace(".", ",")


def en(x, nd=1):
    return f"{x:.{nd}f}"


def tt(field, de_, en_=None):
    """tooltip entry with bilingual title"""
    return {"field": field, "title": bi(de_, en_ if en_ else de_) if isinstance(de_, str) else de_}
