"""Build analysis lage-vermessene-punkte-laenge-breite (A01)."""
import json, math, statistics, collections
from common import *

d = json.load(open("lage_points.json", encoding="utf-8"))
P = d["points"]
issues = d["issues"]
FERRO = 17 + 40 / 60

def dms(x):
    deg = int(x); m = (x - deg) * 60; mi = int(m); s = (m - mi) * 60
    return deg, mi, s

def fmt_dms(x, sec_nd=0):
    deg, mi, s = dms(x + 1e-9)
    return f"{deg}° {mi}′ {s:.{sec_nd}f}″".replace(".", ",")

# ---- extents (p. 6 b2) -----------------------------------------------------------------------
def dec(d, m, s): return d + m / 60 + s / 3600
EXT = {
    "Unterland": dict(lon=(dec(29, 33, 48), dec(29, 52, 42)), lat=(dec(50, 47, 48), dec(50, 58, 38.6)),
                      lon_txt="29° 33′ 48″ – 29° 52′ 42″ L.", lat_txt="50° 47′ 48″ – 50° 58′ 38,6″ Br."),
    "Oberland": dict(lon=(dec(29, 7, 20), dec(29, 47, 40)), lat=(dec(50, 22, 45), dec(50, 43, 50)),
                     lon_txt="29° 7′ 20″ – 29° 47′ 40″ L.", lat_txt="50° 22′ 45″ – 50° 43′ 50″ Br."),
}
ext_rows = []
for k in ("Oberland", "Unterland"):
    e = EXT[k]
    lat_mid = (e["lat"][0] + e["lat"][1]) / 2
    w_km = (e["lon"][1] - e["lon"][0]) * 111.32 * math.cos(math.radians(lat_mid))
    h_km = (e["lat"][1] - e["lat"][0]) * 111.2
    e["w_km"], e["h_km"] = w_km, h_km
    ext_rows.append([k, e["lon_txt"], e["lat_txt"],
                     round(e["lon"][0], 5), round(e["lon"][1], 5), round(e["lat"][0], 5), round(e["lat"][1], 5),
                     round(e["lon"][0] - FERRO, 5), round(e["lon"][1] - FERRO, 5),
                     round(w_km, 1), round(h_km, 1)])
gap_lat = EXT["Unterland"]["lat"][0] - EXT["Oberland"]["lat"][1]
gap_km = gap_lat * 111.2

# ---- point rows -----------------------------------------------------------------------------
pt_rows = []
for i, p in enumerate(P, 1):
    lon, lat = p["lon"], p["lat"]
    pt_rows.append([i, p["name"], p["landesteil"], p["obj"], p["cls"],
                    lon[0], lon[1], lon[2],
                    lat[0] if lat else None, lat[1] if lat else None, lat[2] if lat else None,
                    round(p["lon_dec"], 5), round(p["lon_gw"], 5),
                    round(p["lat_dec"], 5) if p["lat_dec"] is not None else None,
                    p["bracket"], p["lab"], p["page"]])

# ---- statistics ---------------------------------------------------------------------------------
Pm = [p for p in P if p["lat_dec"] is not None]
n_all = len(P); n_map = len(Pm)
by_lt = collections.Counter(p["landesteil"] for p in P)
unbr = [p for p in Pm if not p["bracket"]]
west = min(unbr, key=lambda p: p["lon_dec"]); east = max(unbr, key=lambda p: p["lon_dec"])
south = min(unbr, key=lambda p: p["lat_dec"]); north = max(unbr, key=lambda p: p["lat_dec"])
north_all = max(Pm, key=lambda p: p["lat_dec"])
cls_count = collections.Counter(p["cls"] for p in P)
n_tower = cls_count["Kirche"] + cls_count["Turmknopf"] + cls_count["Turm, Schloss, Ruine"]
gera = next(p for p in P if p["name"] == "Gera")
tanna = next(p for p in P if p["name"] == "Tanna")
schleiz = next(p for p in P if p["name"] == "Schleiz")
geissen = next(p for p in P if p["name"] == "Geissen")
n_bracket = sum(p["bracket"] for p in P)

def gw_txt(p, lang):
    return f"{fmt_dms(p['lon_gw'])} {'O' if lang == 'de' else 'E'}, {fmt_dms(p['lat_dec'])} {'N'}"

print(n_all, n_map, by_lt, west["name"], east["name"], south["name"], north["name"], north_all["name"], cls_count, n_tower)
print(ext_rows, gap_km)
print(gw_txt(gera, "de"), gw_txt(tanna, "de"), gw_txt(schleiz, "de"))
print("geissen", geissen["lat_dec"], fmt_dms(geissen["lat_dec"]))
# points outside printed extents (by landesteil)
out = []
for p in Pm:
    e = EXT[p["landesteil"]]
    if not (e["lon"][0] <= p["lon_dec"] <= e["lon"][1] and e["lat"][0] <= p["lat_dec"] <= e["lat"][1]):
        out.append(p["name"])
print("outside own printed box:", out)
# minimal consistency of p. 4/5: Oberland 29-7-20 + 40-20 = 29-47-40 ; 50-22-45 + 21-5 = 50-43-50 ; Unterland + 18-54 / + 10-50
print(fmt_dms(dec(29,7,20)+dec(0,40,20)), fmt_dms(dec(50,22,45)+dec(0,21,5)), fmt_dms(dec(29,33,48)+dec(0,18,54)), fmt_dms(dec(50,47,48)+dec(0,10,50)))
