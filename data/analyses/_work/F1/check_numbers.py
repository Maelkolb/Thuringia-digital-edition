"""Independent check of the numbers quoted in titles, leads, findings and captions of the four F1 features.
Reads only the published JSON files (datasets inside them) and recomputes every figure; prints OK or the failing assertion."""
import json
import re
import statistics
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition\data\analyses")


def load(fid):
    a = json.loads((ROOT / f"{fid}.json").read_text(encoding="utf-8"))
    ds = {d["name"]: [dict(zip([c["name"] for c in d["columns"]], r)) for r in d["rows"]] for d in a["datasets"]}
    return a, ds


def text(a):
    parts = [a["summary"]["de"]] + [f["de"] for f in a["findings"]]
    for c in a["charts"]:
        parts += [c["title"]["de"], c["caption"]["de"]]
    return " ".join(parts)


def has(t, *needles):
    for n in needles:
        assert n in t, f"missing in text: {n}"


# ------------------------------------------------------------------ land-lage-grenzen
a, d = load("land-lage-grenzen")
t = text(a)
pts = d["points"]
assert len(pts) == 57 and sum(p["lat"] is not None for p in pts) == 56
g = d["grenzen"]
assert sum(x["laenge_stunden"] for x in g if x["landesteil"] == "Oberland") == 48
assert sum(x["laenge_stunden"] for x in g if x["landesteil"] == "Unterland") == 18
assert max(x["laenge_stunden"] for x in g if x["landesteil"] == "Oberland") == 22
tot = {x["quelle"]: x for x in d["totals"]}
drop = (1 - tot["Nowack"]["flaeche_qm"] / tot["Hassel/Stein"]["flaeche_qm"]) * 100
assert round(drop) == 29
assert sum(x["morgen"] for x in d["landestheile"]) == 316738
assert round(316738 * 0.255322 / 100, 1) == 808.7
assert round(tot["Nowack"]["flaeche_km2"]) == 829 and round(tot["Nowack"]["flaeche_qm"] * 55.06) == 829
off = [p["abstand_geonames_km"] for p in pts if p["abstand_geonames_km"] is not None and p["name"] != "Geissen"]
assert len(off) == 44 and round(statistics.median(off), 1) == 0.2
assert round(next(p["abstand_geonames_km"] for p in pts if p["name"] == "Geissen")) == 11
koburg = next(x for x in d["neighbours"] if "Koburg" in x["staat"])
assert round((koburg["flaeche_qm"] and 15.06 / koburg["flaeche_qm"] - 1) * 100) == 48
has(t, "57 trigonometrisch", "22 von 48", "9 von 18", "316.738", "808,7", "15,06", "21,1")
print("land-lage-grenzen OK")

# ------------------------------------------------------------------ relief-hoehen
a, d = load("relief-hoehen")
t = text(a)
pl = [p for p in d["places"] if not p["in_klammern"]]
assert len(pl) == 264 and sum(not h["in_klammern"] for h in d["heights"]) == 263
med = {lt: statistics.median(p["hoehe_mitte_m"] for p in pl if p["landesteil"] == lt) for lt in ("Oberland", "Unterland")}
assert round(med["Oberland"]) == 509 and round(med["Unterland"]) == 248
hi = {lt: max(p["hoehe_mitte_m"] for p in pl if p["landesteil"] == lt) for lt in ("Oberland", "Unterland")}
top = {lt: max(h["hoehe_m"] for h in d["heights"] if h["landesteil"] == lt) for lt in ("Oberland", "Unterland")}
assert round(top["Oberland"] - hi["Oberland"]) == 19 and round(top["Unterland"] - hi["Unterland"]) == 14
assert round(top["Oberland"]) == 725
above = {lt: sum(h["hoehe_m"] > hi[lt] for h in d["heights"] if h["landesteil"] == lt and not h["in_klammern"]) for lt in hi}
assert above == {"Oberland": 6, "Unterland": 6}
mp = [p for p in pl if p["lon"] is not None]
assert round(max(p["hoehe_mitte_m"] for p in mp)) == 677 and round(min(p["hoehe_mitte_m"] for p in mp)) == 174
sel = [p for p in mp if p["landesteil"] == "Oberland"]
X = np.array([[1, (p["lon"] - 11.85) * 111.32 * np.cos(np.radians(p["lat"])), (p["lat"] - 50.70) * 111.2] for p in sel])
yv = np.array([p["hoehe_mitte_m"] for p in sel])
b, *_ = np.linalg.lstsq(X, yv, rcond=None)
assert len(sel) == 97 and round(float(np.hypot(b[1], b[2])), 1) == 4.5 and round(float(np.degrees(np.arctan2(-b[1], -b[2])) % 360)) == 40
nm = d["names"]
c_ = Counter((n["landesteil"], n["typ"]) for n in nm)
n_u, n_o = sum(n["landesteil"] == "Unterland" for n in nm), sum(n["landesteil"] == "Oberland" for n in nm)
assert (n_u, n_o) == (175, 301) and round(c_[("Unterland", "-berg")] / n_u * 100) == 82 and round(c_[("Oberland", "-berg")] / n_o * 100) == 31
assert c_[("Oberland", "-bühl")] == 37 and c_[("Unterland", "-bühl")] == 0
has(t, "264 bewohnten", "263 Höhenpunkten", "248 m", "509 m", "725 m", "173 m", "97 Orte", "4,5 m", "677 m", "174 m", "19 m", "14 m")
print("relief-hoehen OK")

# ------------------------------------------------------------------ geologie-boden
a, d = load("geologie-boden")
t = text(a)
so = d["soils"]
assert len(so) == 25
gr = [s for s in so if s["rock_group"] == "greenstone"]
assert len(gr) == 6 and round(statistics.mean(s["soil_grade"] for s in gr), 1) == 4.8 and sum(s["soil_grade"] == 5 for s in gr) == 5
assert statistics.mean(s["soil_grade"] for s in so if s["rock_group"] == "slate") == 3.0
assert round(statistics.mean(s["soil_grade"] for s in so if s["region"] == "Oberland"), 1) == 3.8
assert statistics.mean(s["soil_grade"] for s in so if s["region"] == "Unterland") == 3.0
rs = d["resources"]
iron = {(r["formation_no"], r["region"]) for r in rs if r["resource"] == "iron"}
assert len(iron) == 7 and sum(r[1] == "Oberland" for r in iron) == 6
assert {r["resource"] for r in rs if r["region"] == "Unterland"} >= {"gypsum"} and "gypsum" not in {r["resource"] for r in rs if r["region"] == "Oberland"}
assert sum(r["status"] == "formerly" for r in rs) == 4 and len(rs) == 29
z, cl = d["zechstein"], d["clymenien"]
assert sum(x["species"] for x in z) == 95 and sum(x["species"] for x in cl) == 42
assert sum(x["species"] for x in z if x["klasse"] in ("bivalve", "brachiopod")) == 45
assert sum(x["species"] for x in cl if x["klasse"] == "cephalopod") == 21
has(t, "13 Gesteinsformationen", "95 Arten", "Mittel 4,8", "45 der 95", "21 der 42")
print("geologie-boden OK")

# ------------------------------------------------------------------ gewaesser
a, d = load("gewaesser")
t = text(a)
rv = {r["river"]: r for r in d["rivers"]}
assert [round(rv[k]["fall_m"]) for k in ("Saale", "Weida", "Elster")] == [101, 81, 25]
assert [rv[k]["sinuosity"] for k in ("Saale", "Weida", "Elster")] == [1.83, 1.75, 1.33]
rc = {r["stream"]: r for r in d["reaches"]}
assert rc["Wettera"]["fall_m"] > 200 and rc["Sieglitzbach"]["fall_m"] > 200 and round(rc["Elster"]["fall_m"]) == 25
assert len({p["stream"] for p in d["points"]}) == 28
tr = d["tributaries"]
assert len(tr) == 83
bank = Counter((x["river"], x["bank"]) for x in tr)
assert [bank[(r_, "rechts")] > bank[(r_, "links")] for r_ in ("Saale", "Elster", "Weida", "Rodach")] == [True, True, True, False]
ob = [x for x in tr if x["region"] == "Oberland"]
un = [x for x in tr if x["region"] == "Unterland"]
assert (len(ob), len(un)) == (50, 28) and round(sum(x["name_type"] == "bach" for x in ob) / 50 * 100) == 68 and round(sum(x["name_type"] == "bach" for x in un) / 28 * 100) == 29
assert sum(x["name_type"] in ("graben", "grund") for x in un) == 8 and sum(x["name_type"] in ("graben", "grund") for x in ob) == 0
comp = d["composition"]
tt = {k: sum(c["parts_per_10000"] for c in comp if c["spring"] == k) for k in ("Neue Quelle", "Agnesquelle")}
assert round(tt["Neue Quelle"], 4) == 2.5232 and round(tt["Agnesquelle"], 4) == 1.0082 and round(tt["Neue Quelle"] / tt["Agnesquelle"], 1) == 2.5
fe = {k: sum(c["parts_per_10000"] for c in comp if c["spring"] == k and c["group"] == "iron") for k in tt}
assert round(fe["Neue Quelle"] / fe["Agnesquelle"], 1) == 1.4
assert round(max(c["parts_per_10000"] for c in comp if c["spring"] == "Agnesquelle") / tt["Agnesquelle"] * 100) == 41
has(t, "83 Zuflüsse", "28 Bäche", "101 m", "1,83fache", "68 Prozent", "2,52", "41 Prozent", "2,5-mal", "1,4-mal")
print("gewaesser OK")
