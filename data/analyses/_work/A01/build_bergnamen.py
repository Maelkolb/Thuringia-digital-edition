"""Build analysis relief-bergnamen (A01): lists of mountain names (pp. 10-11, 17-20)."""
import re
import collections
import io, contextlib
from common import *
with contextlib.redirect_stdout(io.StringIO()):
    from parse_names import all_names

T = lambda de, en: {"de": de, "en": en}
LB = T("Landesteil", "Part of the country")
f1 = lambda x: fmt(x, 1)
f1e = lambda x: fmt(x, 1, "en")
f0 = lambda x: fmt(x, 0)
f0e = lambda x: fmt(x, 0, "en")

PLACE_ADJ = set("robener pfortener saarscher langengrobsdorfer ernseer gerische frössner blintendorfer venzkaer gefeller dittersdorfer tegauer pahrener förthener lössauer göschitzer lobensteiner ebersdorfer hohendorfer langenbacher".split())
TYPES = ["-berg", "-bühl", "-hügel, -hübel", "-leite", "Wald (Hart, Brand)", "-stein/-fels/-kopf", "andere"]
FOREST = {"hart", "brand", "tännig", "busch", "holz", "wald", "bruch", "erlich", "fichtig", "birkicht", "eibicht", "delschig", "kaulicht", "pfaffentännig", "hartebruch"}


def norm(n):
    w = n.split(" ")
    while len(w) > 1 and w[0] in PLACE_ADJ:
        w = w[1:]
    return " ".join(w)


def typ(n):
    w = n.split(" ")[-1].lower()
    if w.endswith("berg") or w.endswith("berge") or w.endswith("bergs"):
        return "-berg"
    if w.endswith("bühl"):
        return "-bühl"
    if w.endswith("hügel") or w.endswith("hübel") or w.endswith("hubel"):
        return "-hügel, -hübel"
    if w.endswith("leite"):
        return "-leite"
    if w in FOREST or w.endswith("busch") or w.endswith("holz") or w.endswith("tännig") or w.endswith("wald") or w.endswith("bruch"):
        return "Wald (Hart, Brand)"
    if w.endswith("stein") or w.endswith("fels") or w.endswith("kopf") or w.endswith("koppe") or w.endswith("knock") or w.endswith("höhe"):
        return "-stein/-fels/-kopf"
    return "andere"


R = all_names()
for r in R:
    r["grund"] = norm(r["name"])
    r["typ"] = typ(r["grund"])
    r["seite"] = {"17+18": "17–18"}.get(r["page"], r["page"])
rows = [[i, r["name"], r["grund"], r["landesteil"], r["grossraum"], r["gebiet"], r["typ"], r["seite"], r["block"]] for i, r in enumerate(R, 1)]

# ---- shares by region ----------------------------------------------------------------------------------------------------
n_lt = collections.Counter(r["landesteil"] for r in R)
cnt_lt = {lt: collections.Counter(r["typ"] for r in R if r["landesteil"] == lt) for lt in n_lt}
n_gr = collections.Counter(r["grossraum"] for r in R)
cnt_gr = {g: collections.Counter(r["typ"] for r in R if r["grossraum"] == g) for g in n_gr}
berg_share = lambda c, n: c["-berg"] / n
OB_ORDER = sorted([g for g in n_gr if any(r["grossraum"] == g and r["landesteil"] == "Oberland" for r in R)], key=lambda g: -berg_share(cnt_gr[g], n_gr[g]))
UN_ORDER = ["Elster rechts", "Elster links"]
LINES = [("Unterland insgesamt", "Unterland", cnt_lt["Unterland"], n_lt["Unterland"])]
LINES += [(f"  Elsterufer {g.split()[1]}", "Unterland", cnt_gr[g], n_gr[g]) for g in UN_ORDER]
LINES += [("Oberland insgesamt", "Oberland", cnt_lt["Oberland"], n_lt["Oberland"])]
LINES += [(f"  {g}", "Oberland", cnt_gr[g], n_gr[g]) for g in OB_ORDER]
share_rows = []
for li, (lab, lt, c, n) in enumerate(LINES, 1):
    for ti, t in enumerate(TYPES, 1):
        share_rows.append([lab, li, lt, t, ti, c[t], round(100 * c[t] / n, 1), n])

# ---- frequent names ----------------------------------------------------------------------------------------------------------
EXCL = {"Berg", "Höhe"}
cn = collections.Counter(r["grund"] for r in R if r["grund"] not in EXCL)
cu = collections.Counter(r["grund"] for r in R if r["landesteil"] == "Unterland")
co = collections.Counter(r["grund"] for r in R if r["landesteil"] == "Oberland")
top = sorted(cn.items(), key=lambda kv: (-kv[1], kv[0]))[:14]
freq_rows = []
for name, k in top:
    t = typ(name)
    freq_rows.append([name, t, TYPES.index(t) + 1, k, cu[name], co[name], f"{k} (U {cu[name]} · O {co[name]})"])
print(top)
print(n_lt, {lt: {t: cnt_lt[lt][t] for t in TYPES} for lt in n_lt})
print([(g, n_gr[g], round(100 * cnt_gr[g]["-berg"] / n_gr[g])) for g in n_gr])

# Brückner's own list of generic terms for summits (p. 15): Bühl, Hügel (Hübel, Haug), Höhe, Kopf, Stein, Fels, Berg, Kulm, Delsch, Lohmen
t15 = text("15", "b3")
assert "Bühl, Hügel (Hübel, Haug), Höhe, Kopf, Stein, Fels, Berg, Kulm, Delsch, Lohmen" in t15
GEN = re.compile(r"(bühl|hügel|hübel|hubel|haug|höhe|kopf|stein|fels|berg|kulm|culm|delsch|oelsch|lohmen)$", re.I)
ob_names = [r for r in R if r["landesteil"] == "Oberland"]
cov_o = sum(1 for r in ob_names if GEN.search(r["grund"].split(" ")[-1]))
un_names = [r for r in R if r["landesteil"] == "Unterland"]
cov_u = sum(1 for r in un_names if GEN.search(r["grund"].split(" ")[-1]))
print("coverage", cov_o, len(ob_names), cov_u, len(un_names))
bue_u = cnt_lt["Unterland"]["-bühl"]; bue_o = cnt_lt["Oberland"]["-bühl"]
wein = (cu["Weinberg"], co["Weinberg"]); galg = (cu["Galgenberg"], co["Galgenberg"]); kirch = (cu["Kirchberg"], co["Kirchberg"]); muehl = (cu["Mühlberg"], co["Mühlberg"]); steinb = (cu["Steinberg"], co["Steinberg"])
print(wein, galg, kirch, muehl, steinb, "buehl", bue_u, bue_o)
per_u = n_lt["Unterland"] / 4.03; per_o = n_lt["Oberland"] / 11.03
share = lambda lt, t: 100 * cnt_lt[lt][t] / n_lt[lt]
