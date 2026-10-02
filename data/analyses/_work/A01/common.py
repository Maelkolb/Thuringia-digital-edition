"""Shared helpers for package A01 (Brückner, Part I, chapter 'Die Natur des Landes', pp. 3-24)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] if False else Path(r"C:\Users\totom\Projects\reuss-edition")
PAGES = {}
for f in (ROOT / "data" / "pages").glob("*.json"):
    p = json.loads(f.read_text(encoding="utf-8"))
    PAGES[p["slug"]] = p


def block(page, bid):
    for b in PAGES[page]["blocks"] + PAGES[page]["footnotes"]:
        if b["id"] == bid:
            return b
    raise KeyError((page, bid))


def grid(page, bid):
    return block(page, bid)["grid"]


def text(page, bid):
    return block(page, bid)["text"]


def num(s):
    return float(str(s).replace(",", "."))


def bi(de, en):
    return {"de": de, "en": en}


# 1 preuss. Decimalfuss (Brückner p. 11 fn.) = 1/10 preuss. Ruthe; Ruthe = 3.766242 m (Brückner p. 831)
RUTE_M = 3.766242
DFUSS_M = RUTE_M / 10.0          # 0.3766242 m
PFUSS_M = 0.313853               # 1 preuss. Fuss (p. 831) = 12/10 Dezimalfuss -> check


def write_analysis(a):
    out = ROOT / "data" / "analyses" / f"{a['id']}.json"
    out.write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)


def fmt(x, nd=1, lang="de"):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "de" else s


def fmt_int(x, lang="de"):
    s = f"{int(round(x)):,}"
    return s.replace(",", ".") if lang == "de" else s


# ---- shared unit evidence for the height analyses (Brückner p. 11 fn., p. 12 fn., p. 21, p. 831) ---------------
PARIS_FUSS_M = 0.324839           # 1 Pariser Fuss (for the comparison only)
TOISE_M = 6 * PARIS_FUSS_M        # 1 Toise = 6 Pariser Fuss
RHEIN_FUSS_M = 0.313853           # rhein. Fuss = preuss. Fuss (Brückner p. 831: 0,313853 m)


def unit_checks():
    d = DFUSS_M
    k = 577 * RHEIN_FUSS_M / d        # Köstritz Bf
    g = 607.53 * RHEIN_FUSS_M / d     # Gera Bf
    t = 289.628 * TOISE_M / d         # Heinrichsruh Wetterfahne
    return dict(koe=k, koe_dev=k / 474 - 1, gera=g, gera_dev=g / 502 - 1, toise=t, toise_dev=t / 1496 - 1,
                toise_m=289.628 * TOISE_M, koe_m=577 * RHEIN_FUSS_M, gera_m=607.53 * RHEIN_FUSS_M)


def conversions_height(lang_both=True):
    u = unit_checks()
    return [{
        "from": "preußischer Dezimalfuß (Höhenangaben der Landeskunde)",
        "to": "Meter",
        "factor_or_formula": f"1 Dezimalfuß = 1/10 preuß. Ruthe = 3,766242 m / 10 = {DFUSS_M:.7f} m (= 1,2 preuß. Fuß)",
        "reference": (f"Brückner S. 11 Anm. (»preuß. Decimalfuß, auf den Pegel bei Swinemünde bezogen«), S. 831 (1 preuß. Ruthe = 3,766242 m). "
                      f"Gegenprobe mit Brückners eigenen Werten: Bahnhof Köstritz 577 rhein. Fuß = {u['koe']:.0f} Dezimalfuß (gedruckt 474′), Bahnhof Gera 607,53 rhein. Fuß = {u['gera']:.0f} (gedruckt 502′; S. 12 Anm.); "
                      f"Wetterfahne Heinrichsruh 289,628 Toisen = {u['toise']:.0f} Dezimalfuß (gedruckt 1496′; S. 21/23). Als Pariser Fuß (0,324839 m) gelesen, ergäben sich dagegen {289.628 * TOISE_M / PARIS_FUSS_M:.0f}′ bzw. {577 * RHEIN_FUSS_M / PARIS_FUSS_M:.0f}′ – unvereinbar mit den gedruckten Zahlen.")
    }]
