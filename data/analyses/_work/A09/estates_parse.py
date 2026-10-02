"""Parse the Kammergüter (pp. 218-221) and Rittergüter (pp. 220-223) tables into estate rows.
Importable: kammer_rows(), ritter_rows(). Printed total rows are returned separately for checks."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

LT = {"Gera": "Gera", "Schleiz": "Schleiz", "Lobenstein-Ebersdorf": "Lobenstein-Ebersdorf"}


def clean_name(s):
    s = s.strip()
    s = re.sub(r"(\s*\.\s*)+$", "", s)
    s = re.sub(r"\s*\.(\s+\.)+\s*", " ", s)
    return s.strip()


def _val(s):
    return num(s)


# Confirmed misreadings of the transcription (checked against the facsimile, tenths digit 7 read as 1 etc.)
# (estate name, field) -> (new value, page, block, cell, transcribed text, facsimile text)
CORR_K = {
    ("Niederndorf", "garten"): (7.74, "218", "b2", "r11c3", "7,14", "7,74"),
    ("Niederndorf", "feld"): (291.75, "218", "b2", "r11c4", "291,15", "291,75"),
    ("Großsaara", "feld"): (158.73, "218", "b2", "r6c4", "158,13", "158,73"),
    ("Laasen mit Steinertsberg", "wiese"): (35.72, "218", "b2", "r9c5", "35,12", "35,72"),
    ("Oschitz", "garten"): (9.77, "218", "b2", "r27c3", "9,17", "9,77"),
    ("Dettersdorf", "wiese"): (134.74, "218", "b2", "r26c5", "134,14", "134,74"),
    ("Seubtendorf", "nadel"): (213.70, "218", "b2", "r31c6", "213,10", "213,70"),
    ("Weckersdorf (Forsthaus)", "feld"): (8.74, "218", "b2", "r32c4", "8,14", "8,74"),
}
CORR_R = {
    ("Schilbach", "wasser"): (4.74, "223", "b1", "r24c2", "4,14", "4,74"),
    ("b) Hohenpreis", "steuer"): (1375.87, "223", "b1", "r33c3", "1375,81", "1375,87"),
}
APPLIED = []


def _apply(estates, corr, lts=None):
    for e in estates:
        for (nm, fld), (new, pg, bl, cell, tr, fa) in corr.items():
            if e["name"] == nm and (lts is None or e["lt"] in lts):
                assert e[fld] is not None and abs(e[fld] - float(tr.replace(",", "."))) < 1e-9, (nm, fld, e[fld], tr)
                e[fld] = new
                APPLIED.append(dict(page=pg, block=bl, cell=cell, transcribed=tr, facsimile=fa, estate=nm, field=fld))


def kammer_rows():
    """Returns (estates, totals). estate: dict; totals: list of (landestheil_or_label, dict of areas, refs)."""
    left = []
    lt = "Gera"
    for page, bid, first in (("218", "b2", 3), ("220", "b1", 2)):
        g = grid(page, bid)
        for i in range(first - 1, len(g)):
            r = g[i]
            rn = i + 1
            label = r[0].strip()
            vals = r[1:6]
            if all(v.strip() == "" for v in vals):
                if label.startswith("Karolinenf"):
                    left.append(dict(kind="group", name=label.rstrip(":"), lt=lt))
                else:
                    lt = clean_name(label)
                continue
            if label.startswith(("Summe", "Hauptsumme", "Hierzu", '"')):
                kind = "sum"
            elif label in ("Latus", "Transport"):
                kind = "latus"
            else:
                kind = "estate"
            left.append(dict(kind=kind, name=clean_name(label), lt=lt, hof=_val(vals[0]), garten=_val(vals[1]), feld=_val(vals[2]),
                             wiese=_val(vals[3]), nadel=_val(vals[4]), page=page, bid=bid, rn=rn))
    right = []
    for page, bid, first in (("219", "b1", 2), ("221", "b1", 2)):
        g = grid(page, bid)
        for i in range(first - 1, len(g)):
            r = g[i]
            right.append(dict(laub=_val(r[0]), hut=_val(r[1]), wasser=_val(r[2]), steuer=_val(r[3]), gewinn=r[4].strip(), page=page, bid=bid, rn=i + 1))
    items = [x for x in left if x["kind"] != "group"]
    assert len(items) == len(right), (len(items), len(right))
    # name for Karolinenfeld sub-entries
    estates, totals = [], []
    for it, rt in zip(items, right):
        d = {**it, **{k: rt[k] for k in ("laub", "hut", "wasser", "steuer", "gewinn")}}
        d["refs"] = [(it["page"], it["bid"], it["rn"]), (rt["page"], rt["bid"], rt["rn"])]
        if d["name"].startswith(("a) Kammergut", "b) Forsthaus")):
            d["name"] = "Karolinenfeld, " + d["name"][3:]
        (estates if it["kind"] == "estate" else totals).append(d)
    if not any(a['page'] == '218' for a in APPLIED):
        _apply(estates, CORR_K)
    return estates, totals


def ritter_rows():
    left = []
    lt = "Gera"
    # p220 b3: rows 3..11 ; p222 b1: rows 2..43
    for page, bid, first in (("220", "b3", 3), ("222", "b1", 2)):
        g = grid(page, bid)
        for i in range(first - 1, len(g)):
            r = g[i]
            rn = i + 1
            label = r[0].strip()
            vals = r[1:7]
            if all(v.strip() == "" for v in vals):
                if label.startswith(("Mödlareuth", "Köstritz")):
                    left.append(dict(kind="group", name=label.rstrip(":"), lt=lt))
                else:
                    lt = {"Schleiz.": "Schleiz", "Lobenst.-Ebersd.": "Lobenstein-Ebersdorf"}.get(label, label)
                continue
            if label.startswith(("Summe", "Hauptsumme", "Hierzu", '"')):
                kind = "sum"
            elif label in ("Latus", "Transport"):
                kind = "latus"
            else:
                kind = "estate"
            left.append(dict(kind=kind, name=clean_name(label), lt=lt, vals=vals, page=page, bid=bid, rn=rn))
    return left


if __name__ == "__main__":
    E, T = kammer_rows()
    for e in E[:3]: print(e)
    print(len(E), len(T))
    for t in T: print(t["lt"], t["name"], t["hof"], t["garten"], t["feld"], t["wiese"], t["nadel"], t["laub"], t["hut"], t["wasser"], t["steuer"])
    # sums
    import collections
    keys = ["hof", "garten", "feld", "wiese", "nadel", "laub", "hut", "wasser", "steuer"]
    for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
        s = {k: round(sum((e[k] or 0) for e in E if e["lt"] == lt), 2) for k in keys}
        print(lt, len([e for e in E if e["lt"] == lt]), s)
    s = {k: round(sum((e[k] or 0) for e in E), 2) for k in keys}
    print("ALL", s)


def ritter_estates():
    """Returns (estates, totals). Aligns the left half (pp. 220/222) with the right half (pp. 221/223).
    Alignment for Gera/Schleiz is by order; Lobenstein-Ebersdorf (p. 223 r29-r38) mapped by hand after
    inspecting the facsimile (two owners for Frössen a), two for Töpen)."""
    left = ritter_rows()
    # split the merged Hartmannsdorf / Dürrenberg row
    out_left = []
    for it in left:
        if it["kind"] == "estate" and it["name"].startswith("Hartmannsdorf"):
            cols = [v.split() for v in it["vals"]]
            assert all(len(c) == 2 for c in cols), cols
            for k, nm in enumerate(("Hartmannsdorf", "Dürrenberg")):
                d = dict(it)
                d["name"] = nm
                d["vals"] = [c[k] for c in cols]
                out_left.append(d)
        else:
            out_left.append(it)
    # right halves
    rights = {}
    g = grid("221", "b2")  # header 1 row; r2..r11 : Hut, Wasser, Steuerwerth, Besitzer
    for i in range(1, len(g)):
        rights[("221", i + 1)] = g[i]
    g = grid("223", "b1")
    for i in range(2, len(g)):
        rights[("223", i + 1)] = g[i]
    # ordered list of right row keys per left estate/latus/sum
    def R(page, rn):
        r = rights[(page, rn)]
        return dict(hut=num(r[0]), wasser=num(r[1]), steuer=num(r[2]), besitzer=r[3].strip(), rref=(page, "b2" if page == "221" else "b1", rn))

    # build ordered keys
    keys = [("221", n) for n in range(2, 9)]            # Caaschwitz..Frankenthal
    keys += [("221", 9), ("221", 10)]                   # Hartmannsdorf, Dürrenberg
    keys += [("221", 11)]                               # Latus
    keys += [("223", 3)]                                # Transport
    keys += [("223", n) for n in range(4, 21)]          # Köstritz .. Zwötzen (17)
    keys += [("223", 21)]                               # Summe Gera
    keys += [("223", n) for n in range(22, 28)]         # Schleiz estates (6)
    keys += [("223", 28)]                               # Summe Schleiz
    # LE: mapped by hand
    le = [("223", 29), ("223", 30), ("223", 32), ("223", 33), ("223", 34), ("223", 35), ("223", 36), ("223", 38)]
    keys += le
    keys += [("223", 39), ("223", 40), ("223", 41), ("223", 42)]  # Summe LE, Gera, Schleiz, Hauptsumme
    estates, totals = [], []
    items = [x for x in out_left if x["kind"] != "group"]
    assert len(items) == len(keys), (len(items), len(keys))
    for it, k in zip(items, keys):
        d = dict(it)
        d.update(R(*k))
        d["hof"], d["garten"], d["feld"], d["wiese"], d["nadel"], d["laub"] = [num(v) for v in it["vals"]]
        d["lrefs"] = (it["page"], it["bid"], it["rn"])
        (estates if it["kind"] == "estate" else totals).append(d)
    if not any(a['page'] == '223' for a in APPLIED):
        _apply(estates, CORR_R)
    return estates, totals


def _check_ritter():
    E, T = ritter_estates()
    keys = ["hof", "garten", "feld", "wiese", "nadel", "laub", "hut", "wasser", "steuer"]
    print(len(E), "estates;", len(T), "totals")
    for t in T:
        print(t["lt"], t["name"], [t[k] for k in keys])
    for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
        s = {k: round(sum((e[k] or 0) for e in E if e["lt"] == lt), 2) for k in keys}
        print(lt, len([e for e in E if e["lt"] == lt]), s)
    s = {k: round(sum((e[k] or 0) for e in E), 2) for k in keys}
    print("ALL", s)
    for e in E:
        if e["lt"] == "Lobenstein-Ebersdorf":
            print(e["name"], [e[k] for k in keys], e["besitzer"])
