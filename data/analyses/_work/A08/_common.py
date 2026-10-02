"""Shared helpers for the A08 analysis scripts (Brückner, Part I, chapter II. Das Volk, pp. 119-207).

Reads the canonical page JSON (data/pages/*.json); nothing is typed by hand that can be read from there.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "data" / "analyses"
GEN = "Claude Sonnet 5.5 (subagent A08)"
DATE = "2026-10-01"

_pages = {}
for f in sorted((ROOT / "data" / "pages").glob("*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    _pages[p["slug"]] = p


def page(label):
    return _pages[str(label)]


def block(label, bid):
    p = page(label)
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def text(label, bid):
    b = block(label, bid)
    if b.get("grid"):
        return "\n".join(" | ".join(r) for r in b["grid"])
    if b.get("items"):
        return "\n".join(i["text"] for i in b["items"])
    return b["text"]


def num(s):
    """'13,60' -> 13.6 ; '1 3/4' not handled (use explicit mapping)."""
    s = s.strip().replace(" ", "").replace(" ", "")
    return float(s.replace(",", "."))


def bi(de, en):
    return {"de": de, "en": en}


def write(ana):
    out = OUT / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)
    return out


def dz(x, n=1):
    """German decimal comma."""
    return f"{x:.{n}f}".replace(".", ",")


def ez(x, n=1):
    return f"{x:.{n}f}"
