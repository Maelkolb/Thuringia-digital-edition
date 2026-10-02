"""Shared helpers for the A11 analysis scripts (chapter IV, Der Staat, pp. 263-310)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent
assert (ROOT / "data" / "pages").exists(), ROOT
GENERATED_BY = "Claude Sonnet 5.5 (subagent A11)"
DATE = "2026-10-01"


def page(label):
    """Canonical page JSON by printed page label (scan = label + 12 in this part of the book)."""
    for f in (ROOT / "data" / "pages").glob("*.json"):
        pass
    p = json.loads((ROOT / "data" / "pages" / f"{int(label) + 12:04d}.json").read_text(encoding="utf-8"))
    assert p["slug"] == str(label), (label, p["slug"])
    return p


def block(label, bid):
    p = page(label)
    for b in p["blocks"] + p["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((label, bid))


def grid(label, bid):
    return block(label, bid)["grid"]


def num(s):
    """Parse a printed number: '1,5' -> 1.5 (decimal comma), '94308' -> 94308, '—' -> None."""
    s = str(s).strip().replace("*)", "").replace("*", "")
    if s in ("", "—", "-", "–", "\"", "null"):
        return None
    if "," in s and len(s.split(",")[-1]) == 3 and s.replace(",", "").isdigit():
        return int(s.replace(",", ""))  # thousands separator 459,126
    s = s.replace(",", ".")
    v = float(s)
    return int(v) if v == int(v) and "." not in s else v


def bi(de, en):
    return {"de": de, "en": en}


def write(ana):
    out = ROOT / "data" / "analyses" / f"{ana['id']}.json"
    ana.setdefault("generated_by", GENERATED_BY)
    ana.setdefault("date", DATE)
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)
    return out


YEAR = bi("Jahr", "Year")


def F(base):
    """Bilingual field reference: dataset carries <base>_de and <base>_en columns."""
    return {"de": f"{base}_de", "en": f"{base}_en"}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    c = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        c["derived"] = True
    if note:
        c["note"] = note
    return c


def tt(field, de, en=None, fmt=None):
    d = {"field": field, "title": bi(de, en) if en else de}
    if fmt:
        d["format"] = fmt
    return d


def ttf(base, de, en):
    """tooltip entry for a bilingual field"""
    return {"field": F(base), "title": bi(de, en)}


def fmt_de(x, nd=0):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".").replace("-", "−")


def fmt_en(x, nd=0):
    return f"{x:,.{nd}f}".replace("-", "−")
