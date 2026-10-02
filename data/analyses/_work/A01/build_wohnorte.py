"""Build analysis relief-wohnorte-hoehenlage (A01): heights of inhabited places, pp. 11-13, 20-22."""
import statistics as st
from collections import Counter
from heights_data import *

T = lambda de, en: {"de": de, "en": en}
D = DFUSS_M

# ---- rows -------------------------------------------------------------------------------------------------
valid = [p for p in PLACES if not p["bracket"]]
rank = {}
pct = {}
for lt in ("Unterland", "Oberland"):
    ps = sorted([p for p in valid if p["landesteil"] == lt], key=lambda p: ((p["lo"] + p["hi"]) / 2, p["lo"], p["name"]))
    for i, p in enumerate(ps, 1):
        rank[id(p)] = i
        pct[id(p)] = round(100 * (i - 0.5) / len(ps), 1)

rows = []
for i, p in enumerate(PLACES, 1):
    mid = (p["lo"] + p["hi"]) / 2
    rows.append([i, p["name"], p["landesteil"], p["gruppe"], "Ort" if p["kind"] == "ort" else "Einzelstelle",
                 p["lo"], p["hi"], round(mid, 2), round(p["lo"] * D, 1), round(p["hi"] * D, 1), round(mid * D, 1),
                 rank.get(id(p)), pct.get(id(p)), p["rng"], p["bracket"], p["page"], p["cell"]])

# ---- statistics ---------------------------------------------------------------------------------------------
def grp(lt, kind=None, rng=None):
    return [p for p in valid if p["landesteil"] == lt and (kind is None or p["kind"] == kind) and (rng is None or p["rng"] == rng)]

U, O = grp("Unterland"), grp("Oberland")
mid = lambda p: (p["lo"] + p["hi"]) / 2
nU, nO = len(U), len(O)
nR = {g: len([p for p in valid if p["gruppe"] == g]) for g in ("Unterland, rechtes Elsterufer", "Unterland, linkes Elsterufer")}
med_U, med_O = st.median(mid(p) for p in U), st.median(mid(p) for p in O)
mean_U, mean_O = st.mean(mid(p) for p in U), st.mean(mid(p) for p in O)
n_range = sum(p["rng"] for p in valid)
lowU = min(U, key=lambda p: (p["lo"], p["name"])); highU = max(U, key=lambda p: p["hi"])
lowO = min(O, key=lambda p: (p["lo"], p["name"])); highO = max(O, key=lambda p: p["hi"])
lowO_all = sorted([p["name"] for p in O if p["lo"] == lowO["lo"]])
spreadU = st.median(p["hi"] - p["lo"] for p in grp("Unterland", rng=1))
spreadO = st.median(p["hi"] - p["lo"] for p in grp("Oberland", rng=1))
maxspread = max(grp("Oberland", rng=1) + grp("Unterland", rng=1), key=lambda p: p["hi"] - p["lo"])
O_below_359 = sum(1 for p in O if mid(p) * D < highU["hi"] * D)
U_above_301 = sum(1 for p in U if mid(p) * D > lowO["lo"] * D)
einzel_O = Counter(p["kind"] for p in O)["einzelstelle"]
einzel_U = Counter(p["kind"] for p in U)["einzelstelle"]
