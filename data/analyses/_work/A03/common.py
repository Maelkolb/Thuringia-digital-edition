"""Shared helpers for the A03 analyses (Brückner ch. 7 Klima, pp. 53-61)."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
# printed page label -> scan sequence (pp. 53..70 = scan 65..82)
SCAN = {str(p): p + 12 for p in range(1, 841)}


def page(label):
    n = SCAN[str(label)]
    return json.loads((ROOT / "data/pages" / f"{n:04d}.json").read_text(encoding="utf-8"))


def block(label, bid):
    p = page(label)
    return next(b for b in p["blocks"] + p["footnotes"] if b["id"] == bid)


def grid(label, bid):
    return block(label, bid)["grid"]


def num(s):
    """'— 6,8' -> -6.8 ; '—' -> None ; '25,0' -> 25.0 ; '-1,00' -> -1.0"""
    if s is None:
        return None
    s = s.strip().replace("*", "")
    if s in ("", "—", "-", "–"):
        return None
    neg = s[0] in "—–-"
    s = s.lstrip("—–- ").replace(",", ".")
    v = float(s)
    return -v if neg else v


MONTHS_PRINT = ["Jan.", "Febr.", "März", "April", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
MONTH_DE = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
R2C = 1.25  # Réaumur -> Celsius


def r2c(v):
    return None if v is None else round(v * R2C, 2)


def write(ana, root=ROOT):
    out = root / "data/analyses" / f"{ana['id']}.json"
    out.write_text(json.dumps(ana, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)


def bi(de, en):
    return {"de": de, "en": en}


# ---- shared chart helpers -------------------------------------------------
MONTH_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_LABEL_EXPR = bi("[" + ",".join(f"'{m}'" for m in MONTH_DE) + "][datum.value-1]",
                      "[" + ",".join(f"'{m}'" for m in MONTH_EN) + "][datum.value-1]")
YEAR = bi("Jahr", "Year")
MONTH = bi("Monat", "Month")
CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]  # days before month start, non-leap year


def doy(month, day):
    """Day of year in a normalised (non-leap) year, 1 = 1 January."""
    return CUM[month - 1] + day


def doy_axis(first=1, last=12, step=1):
    """x axis for a day-of-year scale labelled with the first of the month (months first..last)."""
    ms = list(range(first, last + 1, step))
    vals = [CUM[m - 1] + 1 for m in ms]
    idx = f"indexof([{','.join(map(str, vals))}], datum.value)"
    de = "[" + ",".join(f"'1. {MONTH_DE[m - 1]}'" for m in ms) + f"][{idx}]"
    en = "[" + ",".join(f"'{MONTH_EN[m - 1]} 1'" for m in ms) + f"][{idx}]"
    return {"values": vals, "labelExpr": bi(de, en), "labelAngle": 0}


def tip(field, de, en=None, fmt=None):
    t = {"field": field, "title": bi(de, en) if en else de}
    if fmt:
        t["format"] = fmt
    return t


def fde(x, nd=1):
    """German decimal comma."""
    return f"{x:.{nd}f}".replace(".", ",").replace("-", "−")


def fen(x, nd=1):
    return f"{x:.{nd}f}".replace("-", "−")
