"""Build analysis relief-erhebungen-hoechste-punkte (A01): height points and mountains, pp. 13-15, 22-24."""
import re, statistics as st
from collections import Counter
import io, contextlib
from heights_data import *

T = lambda de, en: {"de": de, "en": en}
D = DFUSS_M
LB = T("Landesteil", "Part of the country")
COL = {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland"]}}
f0 = lambda x: fmt(x, 0)
f0e = lambda x: fmt(x, 0, "en")
m = lambda ft: ft * D

KIND_LABEL = {"berg": "Berg, Hügel (benannt)", "richtungshoehe": "Höhenpunkt (nach Himmelsrichtung)", "bauwerk": "Bauwerk, Straße, Quelle u. Ä."}


def short(n):
    n = re.sub(r"\s*\(Signal\)", "", n).strip()
    if len(n) > 34 and "," in n:
        n = n.split(",")[0]
    return n


S = [s for s in SUMMITS if s["kind"] != "detail"]
assert all(not s.get("error") for s in S)
rows = []
for i, s in enumerate(S, 1):
    rows.append([i, s["name"], short(s["name"]), s["landesteil"], KIND_LABEL[s["kind"]], s["h"], round(m(s["h"]), 3), s["bracket"], s["page"], s["cell"]])
print(len(rows))

# ---- statistics --------------------------------------------------------------------------------------------------
def sel(lt, kind=None, br=0):
    return [s for s in S if s["landesteil"] == lt and (kind is None or s["kind"] == kind) and s["bracket"] == br]

cnt = {lt: Counter(s["kind"] for s in S if s["landesteil"] == lt) for lt in ("Unterland", "Oberland")}
nU, nO = len(sel("Unterland")), len(sel("Oberland"))
topO = sorted(sel("Oberland", "berg"), key=lambda s: -s["h"])[:15]
topU = sorted(sel("Unterland", "berg"), key=lambda s: -s["h"])[:15]
# uniqueness of short names within the top lists
for top in (topO, topU):
    names = [short(s["name"]) for s in top]
    assert len(set(names)) == len(names), names
medU_h = st.median(s["h"] for s in sel("Unterland")); medO_h = st.median(s["h"] for s in sel("Oberland"))
placesU = [(p["lo"] + p["hi"]) / 2 for p in PLACES if p["landesteil"] == "Unterland" and not p["bracket"]]
placesO = [(p["lo"] + p["hi"]) / 2 for p in PLACES if p["landesteil"] == "Oberland" and not p["bracket"]]
medU_p, medO_p = st.median(placesU), st.median(placesO)
t17b1 = text("17", "b1").lower()
frank = []
for s in topO[:7]:
    key = {"Fichteberg, zwischen dem Rohrbache und dem großen Grunde an der Landesgrenze": "fichteberg", "Hohe Tanne": "hohe tanne", "Sieglitzberg": "sieglitz",
           "Fels bei Helmsgrün": "fels", "Kulm": "kulm", "Finkenberg": "finkenberg", "Oßlahügel": "oßlahügel"}.get(s["name"])
    frank.append((s["name"], key, key in t17b1 if key else False))
n_frank = sum(1 for _, k, ok in frank if ok and k != "fels")
print(frank)
print(cnt, nU, nO, medU_h * 1, medO_h, medU_p, medO_p)
extremeU = max(sel("Unterland"), key=lambda s: s["h"]); extremeO = max(sel("Oberland"), key=lambda s: s["h"])
ob_above_p = sum(1 for s in sel("Oberland") if s["h"] > max(p["hi"] for p in PLACES if p["landesteil"] == "Oberland" and not p["bracket"]))
un_above_p = sum(1 for s in sel("Unterland") if s["h"] > max(p["hi"] for p in PLACES if p["landesteil"] == "Unterland" and not p["bracket"]))
print("above highest place", ob_above_p, un_above_p)
n_named_O = len(sel("Oberland", "berg")); n_named_U = len(sel("Unterland", "berg"))

# compare dataset (places midpoints and listed points, in m) --------------------------------------------------------
cmp_rows = []
GR = [("Unterland", "Wohnorte"), ("Unterland", "Erhebungen"), ("Oberland", "Wohnorte"), ("Oberland", "Erhebungen")]
for gi, (lt, art) in enumerate(GR, 1):
    if art == "Wohnorte":
        for p in PLACES:
            if p["landesteil"] == lt and not p["bracket"]:
                cmp_rows.append([f"{lt}: Orte", gi, lt, art, p["name"], round((p["lo"] + p["hi"]) / 2 * D, 1)])
    else:
        for s in S:
            if s["landesteil"] == lt and not s["bracket"]:
                cmp_rows.append([f"{lt}: Höhen", gi, lt, art, s["name"], round(s["h"] * D, 1)])
print(len(cmp_rows))
q = lambda lst, p_: sorted(lst)[int(round(p_ * (len(lst) - 1)))]
