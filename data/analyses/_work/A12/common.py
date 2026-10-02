"""Shared helpers for the A12 analyses (chapter V, history and princely house)."""
import json, re
from pathlib import Path

ROOT = Path(r"C:/Users/totom/Projects/reuss-edition")
PAGES = ROOT / "data" / "pages"
OUT = ROOT / "data" / "analyses"

_cache = {}


def page(label):
    """canonical page JSON by printed label (scan seq = label + 12 for this chapter)"""
    label = str(label)
    if label not in _cache:
        seq = int(label) + 12
        p = json.loads((PAGES / f"{seq:04d}.json").read_text(encoding="utf-8"))
        assert p["slug"] == label, (label, p["slug"])
        _cache[label] = p
    return _cache[label]


def block(label, bid):
    p = page(label)
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def block_text(label, bid):
    b = block(label, bid)
    if b.get("grid"):
        return "\n".join(" | ".join(r) for r in b["grid"])
    if b.get("items"):
        return "\n".join(i["text"] for i in b["items"])
    return b["text"]


def cell(label, bid, r, c):
    """1-based row/col of a table grid (as in the text export rN)"""
    return block(label, bid)["grid"][r - 1][c - 1]


YEAR_RE = re.compile(r"(?<!\d)(\d{3,4})(?!\d)")


def years_in(label, bid):
    t = block_text(label, bid)
    return {int(m.group(1)) for m in YEAR_RE.finditer(t)}


def bi(de, en):
    return {"de": de, "en": en}


def write_analysis(a):
    out = OUT / f"{a['id']}.json"
    out.write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)
    return out


def refs_from(rows_pb):
    """unique, ordered [{'page','block'}] from iterable of (page, block)"""
    seen, out = set(), []
    for pg, b in rows_pb:
        if (pg, b) not in seen:
            seen.add((pg, b))
            out.append({"page": str(pg), "block": b})
    out.sort(key=lambda r: (int(r["page"]), int(re.sub(r"\D", "", r["block"])) + (1000 if r["block"].startswith("fn") else 0)))
    return out
