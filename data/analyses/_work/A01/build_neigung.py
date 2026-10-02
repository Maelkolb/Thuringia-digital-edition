"""Build analysis relief-hoehe-und-lage-neigung (A01): join of the coordinate table (pp. 6-7) and the
altitude lists of the inhabited places (pp. 11-22); planar fit of altitude over position."""
import json, math
import numpy as np
from heights_data import *

T = lambda de, en: {"de": de, "en": en}
D = DFUSS_M
LB = T("Landesteil", "Part of the country")
COL = {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland"]}}

pts = json.load(open("lage_points.json", encoding="utf-8"))["points"]
ALIAS = {"Rödersdorf": "Rüdersdorf", "Geissen": "Geißen", "Bergkirche": "Schleizer Bergkirche",
         "Oettersdorf": "Dettersdorf, Mitte", "Kirschkau": "Kirschkau, die nördlichen Häuser",
         "Grumbach": "Grumbach, Mitte", "Schleiz": "Schleiz, Wiesenthal"}
LAB = {"Gera", "Köstritz", "Hohenleuben", "Schleiz", "Lobenstein", "Tanna", "Hirschberg", "Wurzbach"}

matched, skipped, seen = [], [], set()
for pt in pts:
    if pt["lat_dec"] is None or pt["bracket"]:
        skipped.append((pt["name"], "keine Breite/Klammer"))
        continue
    nm = ALIAS.get(pt["name"], pt["name"])
    c = [p for p in PLACES if p["name"] == nm and p["landesteil"] == pt["landesteil"]]
    if len(c) != 1:
        skipped.append((pt["name"], "kein Ort in der Höhenliste"))
        continue
    if nm in seen:
        skipped.append((pt["name"], "zweiter Punkt desselben Ortes"))
        continue
    seen.add(nm)
    p = c[0]
    matched.append(dict(pt=pt, pl=p))
print(len(matched), "matched;", skipped)

LAT0, LON0 = 50.70, 11.85
KX = 111.32 * math.cos(math.radians(LAT0))
KY = 111.2
rows_src = []
for m in matched:
    pt, pl = m["pt"], m["pl"]
    x = (pt["lon_gw"] - LON0) * KX
    y = (pt["lat_dec"] - LAT0) * KY
    mid = (pl["lo"] + pl["hi"]) / 2 * D
    rows_src.append(dict(name=pt["name"], hname=pl["name"], lt=pt["landesteil"], lon=pt["lon_gw"], lat=pt["lat_dec"], x=x, y=y,
                         lo=pl["lo"] * D, hi=pl["hi"] * D, mid=mid, lab=1 if pt["name"] in LAB else 0, pg=pt["page"], hp=pl["page"]))

def fit(sub):
    X = np.array([[1.0, r["x"], r["y"]] for r in sub])
    y = np.array([r["mid"] for r in sub])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = float(((y - pred) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    b, c = beta[1], beta[2]
    slope = math.hypot(b, c)
    az_down = (math.degrees(math.atan2(-b, -c))) % 360      # azimuth (from north, clockwise) of steepest descent
    return dict(beta=beta, r2=1 - ss_res / ss_tot, slope=slope, az=az_down, rmse=math.sqrt(ss_res / len(sub)), pred=pred, n=len(sub))

F_all = fit(rows_src)
F_ob = fit([r for r in rows_src if r["lt"] == "Oberland"])
F_un = fit([r for r in rows_src if r["lt"] == "Unterland"])
for r, pr in zip(rows_src, F_all["pred"]):
    r["fit"] = float(pr); r["res"] = r["mid"] - float(pr)
print("all", F_all["beta"], F_all["r2"], F_all["slope"], F_all["az"], F_all["rmse"], F_all["n"])
print("Oberland", F_ob["slope"], F_ob["az"], F_ob["r2"], F_ob["n"], "Unterland", F_un["slope"], F_un["az"], F_un["r2"], F_un["n"])
# correlation with latitude only
lat = np.array([r["lat"] for r in rows_src]); h = np.array([r["mid"] for r in rows_src])
r_lat = float(np.corrcoef(lat, h)[0, 1])
b_lat = float(np.polyfit(lat, h, 1)[0])
print("r_lat", r_lat, "slope per 10 km north", b_lat / KY * 10)
big = sorted(rows_src, key=lambda r: -abs(r["res"]))[:4]
print([(r["name"], round(r["res"])) for r in big])
# the steepest part: Oberland vs Unterland mean
mO = np.mean([r["mid"] for r in rows_src if r["lt"] == "Oberland"]); mU = np.mean([r["mid"] for r in rows_src if r["lt"] == "Unterland"])
print(mO, mU)
