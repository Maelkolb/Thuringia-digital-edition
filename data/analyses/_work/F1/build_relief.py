"""Feature relief-hoehen (agent F1): merges relief-erhebungen-hoechste-punkte, relief-hoehe-und-lage-neigung,
relief-hoehenstufen-oberland-unterland, relief-wohnorte-hoehenlage, relief-bergnamen."""
import collections
import re
import statistics
import numpy as np
from common import *

a_wohn = load("relief-wohnorte-hoehenlage")
a_erh = load("relief-erhebungen-hoechste-punkte")
a_stufen = load("relief-hoehenstufen-oberland-unterland")
a_neig = load("relief-hoehe-und-lage-neigung")
a_berg = load("relief-bergnamen")

places_ds = json.loads(json.dumps(ds_of(a_wohn, "places")))
for row in places_ds["rows"]:
    if row[1] == "Karolinensfeld":      # print: "Karolinenfeld" (checked in the facsimile)
        row[1] = "Karolinenfeld"
heights_ds = ds_of(a_erh, "heights")
levels_ds = ds_of(a_stufen, "levels")
names_ds = ds_of(a_berg, "names")

# ------------------------------------------------------------------ join places to the GeoNames base layer
base_places = shared("base_places")
bcols = [c["name"] for c in base_places["columns"]]
base = collections.defaultdict(list)
for r in base_places["rows"]:
    base[r[0]].append(dict(zip(bcols, r)))
SPELLING = {"Seifarthsdorf": "Seifartsdorf", "Lauenhayn": "Lauenhain", "Carolinenfeld": "Karolinenfield", "Dettersdorf": "Oettersdorf", "Benzka": "Venzka", "Spilmes": "Spielmes"}


def norm(name):
    n = re.sub(r"\s*\(.*?\)", "", name).split(",")[0].strip()
    n = re.sub(r"\s+(oberstes|unterste|Nordgasse|Dorfmitte|Mitte)\b.*$", "", n).strip()
    return SPELLING.get(n, n)


def teil_of(b):
    d = b["landestheil"]
    if d in ("Gera",):
        return "Unterland"
    if d in ("Schleiz", "Lobenstein-Ebersdorf"):
        return "Oberland"
    return "Unterland" if b["lat"] > 50.78 else "Oberland"


pcols = [c["name"] for c in places_ds["columns"]]
plist = [dict(zip(pcols, r)) for r in places_ds["rows"]]
cand = collections.defaultdict(list)           # (base name, base index) -> place indexes
for i, p in enumerate(plist):
    if p["art"] != "Ort" or p["in_klammern"]:
        continue
    n = norm(p["name"])
    for j, b in enumerate(base.get(n, [])):
        if teil_of(b) == p["landesteil"]:
            cand[(n, j)].append(i)
match = {}
dropped_ambiguous = []
for (n, j), idx in cand.items():
    hs = [plist[i]["hoehe_mitte_m"] for i in idx]
    if max(hs) - min(hs) > 10:                     # homonyms with different heights: not mapped
        dropped_ambiguous.append((n, hs))
        continue
    for i in idx:
        match[i] = (n, j)
print("mapped places:", len(match), "ambiguous dropped:", dropped_ambiguous)

places_ds["columns"] += [
    col("lon", "Länge", "Longitude", "number", "°", True, "GeoNames; gleichnamiger Ort der Kartengrundlage (Name und Landesteil müssen passen)"),
    col("lat", "Breite", "Latitude", "number", "°", True, "GeoNames"),
]
for i, r in enumerate(places_ds["rows"]):
    if i in match:
        b = base[match[i][0]][match[i][1]]
        r += [round(b["lon"], 5), round(b["lat"], 5)]
    else:
        r += [None, None]
plist = [dict(zip([c["name"] for c in places_ds["columns"]], r)) for r in places_ds["rows"]]

# ------------------------------------------------------------------ numbers
inh = [p for p in plist if not p["in_klammern"]]
by = {lt: [p for p in inh if p["landesteil"] == lt] for lt in ("Oberland", "Unterland")}
n_ober, n_unter = len(by["Oberland"]), len(by["Unterland"])
med_o = statistics.median(p["hoehe_mitte_m"] for p in by["Oberland"])
med_u = statistics.median(p["hoehe_mitte_m"] for p in by["Unterland"])
top_o = max(by["Oberland"], key=lambda p: p["hoehe_mitte_m"])
top_u = max(by["Unterland"], key=lambda p: p["hoehe_mitte_m"])
low_u = min(by["Unterland"], key=lambda p: p["hoehe_mitte_m"])
low_o = min(by["Oberland"], key=lambda p: p["hoehe_mitte_m"])
print("places", len(inh), n_ober, n_unter, "median", med_o, med_u, "top", top_o["name"], top_o["hoehe_mitte_m"], top_u["name"], top_u["hoehe_mitte_m"],
      "low", low_u["name"], low_u["hoehe_mitte_m"], low_o["name"], low_o["hoehe_mitte_m"])
lv = {(r[0], r[1]): r[4] for r in levels_ds["rows"]}
lo_ober = lv[("Oberland", "tiefster Punkt")]
hi_unter = lv[("Unterland", "höchster Punkt")]
hi_ober = lv[("Oberland", "höchster Punkt")]
overlap = hi_unter - lo_ober
print("levels", lo_ober, hi_unter, hi_ober, "overlap m", overlap)
n_ober_below = sum(p["hoehe_mitte_m"] < hi_unter for p in by["Oberland"])
n_unter_above = sum(p["hoehe_mitte_m"] > lo_ober for p in by["Unterland"])
print("places in overlap: oberland below", hi_unter, n_ober_below, "unterland above", lo_ober, n_unter_above)

# plane through the places with coordinates (steepest descent)
pl = [p for p in plist if p["lon"] is not None]
lat0, lon0 = 50.70, 11.85
X = np.array([[1.0, (p["lon"] - lon0) * 111.32 * np.cos(np.radians(p["lat"])), (p["lat"] - lat0) * 111.2] for p in pl])
y = np.array([p["hoehe_mitte_m"] for p in pl])
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
pred = X @ beta
r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
grad = float(np.hypot(beta[1], beta[2]))
azim = float((np.degrees(np.arctan2(-beta[1], -beta[2]))) % 360)     # direction of steepest descent, clockwise from north
print("plane: n", len(pl), "gradient m/km", grad, "azimuth", azim, "R2", r2, "rmse", float(np.sqrt(((y - pred) ** 2).mean())))

# summits
hs = rows_as_dicts(heights_ds)
n_h_o = sum(h["landesteil"] == "Oberland" and not h["in_klammern"] for h in hs)
n_h_u = sum(h["landesteil"] == "Unterland" and not h["in_klammern"] for h in hs)
above_o = sum(h["landesteil"] == "Oberland" and not h["in_klammern"] and h["hoehe_m"] > top_o["hoehe_mitte_m"] for h in hs)
above_u = sum(h["landesteil"] == "Unterland" and not h["in_klammern"] and h["hoehe_m"] > top_u["hoehe_mitte_m"] for h in hs)
summit_o = max((h for h in hs if h["landesteil"] == "Oberland"), key=lambda h: h["hoehe_m"])
summit_u = max((h for h in hs if h["landesteil"] == "Unterland"), key=lambda h: h["hoehe_m"])
print("height points", n_h_o, n_h_u, "above highest village", above_o, above_u, summit_o["kurzname"], summit_o["hoehe_m"], summit_u["kurzname"], summit_u["hoehe_m"])
fichte_over = summit_o["hoehe_m"] - top_o["hoehe_mitte_m"]
print("Fichteberg above village m", fichte_over)

# names
nm = rows_as_dicts(names_ds)
cnt = collections.Counter((n["landesteil"], n["typ"]) for n in nm)
tot = collections.Counter(n["landesteil"] for n in nm)
share = lambda lt, typ: cnt[(lt, typ)] / tot[lt] * 100
print("names", tot, "berg", share("Unterland", "-berg"), share("Oberland", "-berg"), "buehl", cnt[("Oberland", "-bühl")], cnt[("Unterland", "-bühl")])

# ------------------------------------------------------------------ charts
OBER, UNTER = "@accent2", "@accent"
LAND_SCALE = {"domain": ["Oberland", "Unterland"], "range": [OBER, UNTER]}

label_names = ["Gera", "Schleiz, Wiesenthal", "Lobenstein", "Grumbach, Mitte", "Caaschwitz", "Hohenleuben"]
c1 = {
    "height": 540,
    "projection": {"type": "mercator"},
    "layer": [
        {"data": {"name": "fluesse_basis"}, "transform": [{"filter": "(datum.fluss != 'Weiße Elster' || datum.lat > 50.7) && datum.lat >= 50.36"}],
         "mark": {"type": "line", "color": "@river", "strokeWidth": 1.1},
         "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                      "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
        {"data": {"name": "orte_basis"}, "mark": {"type": "circle", "size": 8, "color": "@land", "opacity": 1},
         "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}},
        {"transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat) && datum.in_klammern == 0"}],
         "mark": {"type": "circle", "size": 78, "stroke": "@paper", "strokeWidth": 0.8, "opacity": 1},
         "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                      "color": {"field": "hoehe_mitte_m", "type": "quantitative",
                                "scale": {"range": "ramp", "domain": [150, 725]},
                                "legend": {"title": {"de": "Höhe in m", "en": "Altitude in m"}, "orient": "top-left", "direction": "vertical",
                                           "gradientLength": 120, "gradientThickness": 12, "format": "d", "values": [200, 300, 400, 500, 600, 700]}},
                      "tooltip": tooltip(("name", "Ort", "Place"), ("landesteil", "Landesteil", "Part"),
                                         ("hoehe_min_m", "tiefstes Haus (m)", "lowest house (m)", ".0f"),
                                         ("hoehe_max_m", "höchstes Haus (m)", "highest house (m)", ".0f"),
                                         ("hoehe_mitte_m", "Mitte der Spanne (m)", "midpoint of range (m)", ".0f"))}},
    ],
}
for style in ("place-halo", "place-label"):
    c1["layer"].append({
        "transform": [{"filter": "isValid(datum.lon) && indexof(" + json.dumps(label_names, ensure_ascii=False).replace('"', "'") + ", datum.name) >= 0"},
                      {"calculate": "split(datum.name, ',')[0] + ' ' + format(datum.hoehe_mitte_m, '.0f') + ' m'", "as": "label"}],
        "mark": {"type": "text", "style": style, "dy": {"expr": "datum.name == 'Caaschwitz' ? 0 : -12"}, "dx": {"expr": "datum.name == 'Caaschwitz' ? -10 : 0"},
                 "align": {"expr": "datum.name == 'Caaschwitz' ? 'right' : 'center'"}},
        "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}, "text": {"field": "label"}}})

# c2: histogram of place heights per part
c2 = {
    "height": 300,
    "layer": [
        {"transform": [{"filter": "datum.in_klammern == 0"}],
         "mark": {"type": "bar", "opacity": 0.78, "cornerRadiusEnd": 0},
         "encoding": {"x": {"field": "hoehe_mitte_m", "type": "quantitative", "bin": {"step": 25}, "scale": {"domain": [150, 750], "zero": False, "nice": False},
                            "axis": {"title": {"de": "Höhe über dem Meer in m (Mitte der Spanne des Ortes)", "en": "Altitude above sea level in m (midpoint of the place’s range)"},
                                     "values": [200, 300, 400, 500, 600, 700], "format": "d"}},
                      "y": {"aggregate": "count", "type": "quantitative", "stack": None,
                            "axis": {"title": {"de": "Anzahl Wohnpunkte", "en": "Number of inhabited points"}, "tickMinStep": 5}},
                      "color": {"field": "landesteil", "type": "nominal", "scale": LAND_SCALE, "legend": None},
                      "tooltip": [{"field": "landesteil", "title": {"de": "Landesteil", "en": "Part"}},
                                  {"field": "hoehe_mitte_m", "bin": {"step": 25}, "title": {"de": "Höhenklasse (m)", "en": "Altitude class (m)"}},
                                  {"aggregate": "count", "title": {"de": "Wohnpunkte", "en": "Inhabited points"}}]}},
        {"transform": [{"filter": "datum.in_klammern == 0"},
                       {"aggregate": [{"op": "median", "field": "hoehe_mitte_m", "as": "med"}], "groupby": ["landesteil"]},
                       {"calculate": {"de": "datum.landesteil + ': Median ' + format(datum.med, '.0f') + ' m'", "en": "datum.landesteil + ': median ' + format(datum.med, '.0f') + ' m'"}, "as": "label"}],
         "mark": {"type": "rule", "strokeWidth": 2},
         "encoding": {"x": {"field": "med", "type": "quantitative"},
                      "color": {"field": "landesteil", "type": "nominal", "scale": LAND_SCALE, "legend": None}}},
        {"transform": [{"filter": "datum.in_klammern == 0"},
                       {"aggregate": [{"op": "median", "field": "hoehe_mitte_m", "as": "med"}], "groupby": ["landesteil"]},
                       {"calculate": {"de": "datum.landesteil + ': Median ' + format(datum.med, '.0f') + ' m'", "en": "datum.landesteil + ': median ' + format(datum.med, '.0f') + ' m'"}, "as": "label"}],
         "mark": {"type": "text", "style": "label", "baseline": "bottom", "dy": -4, "align": {"expr": "datum.landesteil == 'Unterland' ? 'right' : 'left'"}, "dx": {"expr": "datum.landesteil == 'Unterland' ? -6 : 6"}},
         "encoding": {"x": {"field": "med", "type": "quantitative"}, "y": {"value": 0},
                      "text": {"field": "label"},
                      "color": {"field": "landesteil", "type": "nominal", "scale": LAND_SCALE, "legend": None}}},
    ],
}



def fit(sel):
    X = np.array([[1.0, (p["lon"] - lon0) * 111.32 * np.cos(np.radians(p["lat"])), (p["lat"] - lat0) * 111.2] for p in sel])
    yy = np.array([p["hoehe_mitte_m"] for p in sel])
    beta, *_ = np.linalg.lstsq(X, yy, rcond=None)
    pr = X @ beta
    return {"n": len(sel), "grad": float(np.hypot(beta[1], beta[2])), "azim": float(np.degrees(np.arctan2(-beta[1], -beta[2])) % 360),
            "r2": float(1 - ((yy - pr) ** 2).sum() / ((yy - yy.mean()) ** 2).sum())}


fit_o = fit([p for p in pl if p["landesteil"] == "Oberland"])
fit_u = fit([p for p in pl if p["landesteil"] == "Unterland"])
print("fit Oberland", fit_o, "fit Unterland", fit_u)
mapped = [p for p in plist if p["lon"] is not None and not p["in_klammern"]]
n_orte = sum(1 for p in plist if p["art"] == "Ort" and not p["in_klammern"])
hi_map = max(mapped, key=lambda p: p["hoehe_mitte_m"])
lo_map = min(mapped, key=lambda p: p["hoehe_mitte_m"])
print("mapped", len(mapped), "of", n_orte, "highest", hi_map["name"], hi_map["hoehe_mitte_m"], "lowest", lo_map["name"], lo_map["hoehe_mitte_m"])

# arrow of steepest descent in the Oberland (annotation of the map, placed in the empty north-west of the map)
L_KM = 11.0
az = np.radians(fit_o["azim"])
a_lat1, a_lon1 = 50.82, 11.58
a_lon2 = a_lon1 + np.sin(az) * L_KM / (111.32 * np.cos(np.radians(a_lat1)))
a_lat2 = a_lat1 + np.cos(az) * L_KM / 111.2
arrow_ds = {
    "name": "gefaelle_pfeil",
    "title": T("Richtung des steilsten Gefälles im Oberland (Pfeil der Karte)", "Direction of steepest descent in the Oberland (arrow on the map)"),
    "columns": [col("lon1", "Länge Anfang", "Longitude start", "number", "°", True), col("lat1", "Breite Anfang", "Latitude start", "number", "°", True),
                col("lon2", "Länge Ende", "Longitude end", "number", "°", True), col("lat2", "Breite Ende", "Latitude end", "number", "°", True),
                col("azimut", "Richtung des Gefälles (von Nord im Uhrzeigersinn)", "Direction of fall (clockwise from north)", "number", "°", True),
                col("gefaelle_m_je_km", "Gefälle der Ausgleichsebene", "Slope of the fitted plane", "number", "m/km", True)],
    "rows": [[round(a_lon1, 4), a_lat1, round(float(a_lon2), 4), round(float(a_lat2), 4), round(fit_o["azim"], 1), round(fit_o["grad"], 2)]],
    "source_refs": [{"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}],
}
c1["layer"] += [
    {"data": {"name": "gefaelle_pfeil"}, "mark": {"type": "rule", "strokeWidth": 2.2, "color": "@ink2"},
     "encoding": {"longitude": {"field": "lon1", "type": "quantitative"}, "latitude": {"field": "lat1", "type": "quantitative"},
                  "longitude2": {"field": "lon2"}, "latitude2": {"field": "lat2"}}},
    {"data": {"name": "gefaelle_pfeil"}, "mark": {"type": "point", "shape": "triangle", "filled": True, "size": 110, "color": "@ink2"},
     "encoding": {"longitude": {"field": "lon2", "type": "quantitative"}, "latitude": {"field": "lat2", "type": "quantitative"},
                  "angle": {"field": "azimut", "type": "quantitative", "scale": None}}},
    {"data": {"name": "gefaelle_pfeil"}, "mark": {"type": "text", "style": "annotation", "align": "left", "baseline": "top", "dx": 8, "dy": 6},
     "encoding": {"longitude": {"field": "lon1", "type": "quantitative"}, "latitude": {"field": "lat1", "type": "quantitative"},
                  "text": {"value": {"de": f"Oberland: {de(fit_o['grad'], 1)} m Gefälle je km", "en": f"Oberland: {en(fit_o['grad'], 1)} m fall per km"}}}},
]

# c2: overlap band between the lowest point of the Oberland and the highest point of the Unterland (Brückner's own figures)
c2["layer"].insert(0, {
    "data": {"name": "levels"},
    "transform": [{"filter": "(datum.landesteil == 'Oberland' && datum.merkmal == 'tiefster Punkt') || (datum.landesteil == 'Unterland' && datum.merkmal == 'höchster Punkt')"},
                  {"aggregate": [{"op": "min", "field": "hoehe_m", "as": "lo"}, {"op": "max", "field": "hoehe_m", "as": "hi"}]}],
    "mark": {"type": "rect", "color": "@muted", "opacity": 0.16},
    "encoding": {"x": {"field": "lo", "type": "quantitative"}, "x2": {"field": "hi"}, "y": {"value": 0}, "y2": {"value": 300}}})


c2["layer"].append({
    "data": {"name": "levels"},
    "transform": [{"filter": "datum.landesteil == 'Oberland' && datum.merkmal == 'tiefster Punkt'"}, {"calculate": "datum.hoehe_m + " + str(round(overlap / 2, 2)), "as": "mid"}],
    "mark": {"type": "text", "style": "annotation", "align": "center", "baseline": "top", "dy": 6},
    "encoding": {"x": {"field": "mid", "type": "quantitative"}, "y": {"value": 0},
                 "text": {"value": {"de": "Überschneidung", "en": "overlap"}}}})


# c3: highest named mountains versus highest inhabited point, per part
def summit_panel(part, color, title, last):
    top6 = [{"filter": f"datum.landesteil == '{part}' && datum.in_klammern == 0 && datum.art == 'Berg, Hügel (benannt)'"},
            {"window": [{"op": "row_number", "as": "rang"}], "sort": [{"field": "hoehe_m", "order": "descending"}]},
            {"filter": "datum.rang <= 6"},
            {"calculate": "replace(datum.kurzname, /\s*\([^)]*\)/g, '')", "as": "label"}]
    xs = {"type": "quantitative", "scale": {"domain": [150, 800]}}
    return {
        "width": 480,
        "height": {"step": 24},
        "title": {"text": title, "anchor": "start", "fontSize": 13, "offset": 6},
        "encoding": {"y": {"field": "label", "type": "nominal", "sort": {"field": "hoehe_m", "order": "descending"},
                           "axis": {"title": None, "labelLimit": 400, "labelAlign": "left", "labelPadding": 212, "minExtent": 215}}},
        "layer": [
            {"transform": top6, "mark": {"type": "rule", "strokeWidth": 1.6, "color": "@context"},
             "encoding": {"x": {"field": "hoehe_m", **xs}, "x2": {"datum": 150}}},
            {"transform": top6, "mark": {"type": "point", "filled": True, "size": 90, "color": color, "opacity": 1},
             "encoding": {"x": {"field": "hoehe_m", **xs,
                                "axis": {"title": ({"de": "Höhe über dem Meer in m", "en": "Altitude above sea level in m"} if last else None),
                                         "values": [200, 300, 400, 500, 600, 700], "format": "d"}},
                          "tooltip": tooltip(("name", "Berg", "Mountain"), ("hoehe_fuss", "preuß. Dezimalfuß", "Prussian decimal feet", ",.1~f"),
                                             ("hoehe_m", "Meter", "Meters", ".0f"), ("seite", "Seite", "Page"))}},
            {"transform": top6 + [{"calculate": "format(datum.hoehe_m, '.0f') + ' m'", "as": "wert"}], "mark": {"type": "text", "style": "label", "align": "right"},
             "encoding": {"x": {"datum": 800, "type": "quantitative"}, "text": {"field": "wert"}}},
            {"data": {"name": "places"},
             "transform": [{"filter": f"datum.landesteil == '{part}' && datum.in_klammern == 0"},
                           {"aggregate": [{"op": "max", "field": "hoehe_mitte_m", "as": "hoechster_ort"}]}],
             "mark": {"type": "rule", "strokeDash": [4, 3], "strokeWidth": 1.6, "color": "@ink2"},
             "encoding": {"x": {"field": "hoechster_ort", "type": "quantitative"}, "y": None}},
        ],
    }


c3 = {"vconcat": [
    summit_panel("Oberland", OBER, {"de": f"Oberland (gestrichelt: höchster bewohnter Punkt, {top_o['name']} {de(top_o['hoehe_mitte_m'], 0)} m)",
                                    "en": f"Oberland (dashed: highest inhabited point, {top_o['name']} {en(top_o['hoehe_mitte_m'], 0)} m)"}, False),
    summit_panel("Unterland", UNTER, {"de": f"Unterland (gestrichelt: höchster bewohnter Punkt, {top_u['name']} {de(top_u['hoehe_mitte_m'], 0)} m)",
                                      "en": f"Unterland (dashed: highest inhabited point, {top_u['name']} {en(top_u['hoehe_mitte_m'], 0)} m)"}, True),
], "spacing": 24}

# ------------------------------------------------------------------ texts
over_o = summit_o["hoehe_m"] - top_o["hoehe_mitte_m"]
over_u = summit_u["hoehe_m"] - top_u["hoehe_mitte_m"]
n_all_places = n_ober + n_unter
n_heights = n_h_o + n_h_u
elster_exit = lv[("Unterland", "tiefster Punkt")]

lead_de = (f"Brückner verzeichnet die Meereshöhe von {n_all_places} bewohnten Punkten und {n_heights} Höhenpunkten in preußischen Dezimalfuß. Umgerechnet liegen die "
           f"Wohnpunkte des Unterlandes im Median bei {de(med_u, 0)} m, die des Oberlandes bei {de(med_o, 0)} m. Höchster Punkt ist der Fichteberg im Frankenwald "
           f"mit {de(summit_o['hoehe_m'], 0)} m; die Elster verlässt das Land bei {de(elster_exit, 0)} m.")
lead_en = (f"Brückner lists the altitude of {n_all_places} inhabited points and {n_heights} height points in Prussian decimal feet. Converted, the inhabited points "
           f"of the Unterland lie at a median of {en(med_u, 0)} m, those of the Oberland at {en(med_o, 0)} m. The highest point is the Fichteberg in the Frankenwald "
           f"at {en(summit_o['hoehe_m'], 0)} m; the Elster leaves the country at {en(elster_exit, 0)} m.")
f1_de = (f"Eine Ausgleichsebene durch {fit_o['n']} Orte des Oberlandes fällt mit {de(fit_o['grad'], 1)} m je km nach Nordosten ({de(fit_o['azim'], 0)}°), wie Brückner schreibt. "
         f"Im Unterland erklärt die Lage kaum etwas (R² {de(fit_u['r2'], 2)}).")
f1_en = (f"A plane fitted through {fit_o['n']} places of the Oberland falls {en(fit_o['grad'], 1)} m per km toward the northeast ({en(fit_o['azim'], 0)}°), as Brückner writes. "
         f"In the Unterland position explains little (R² {en(fit_u['r2'], 2)}).")
f2_de = (f"Nur {above_o} der {n_h_o} Höhenpunkte des Oberlandes und {above_u} der {n_h_u} des Unterlandes liegen über dem höchsten bewohnten Punkt.")
f2_en = (f"Only {above_o} of the {n_h_o} height points of the Oberland and {above_u} of the {n_h_u} of the Unterland lie above the highest inhabited point.")
f3_de = (f"Im Unterland enden {de(share('Unterland', '-berg'), 0)} Prozent der {tot['Unterland']} genannten Bergnamen auf -berg, im Oberland {de(share('Oberland', '-berg'), 0)} Prozent "
         f"von {tot['Oberland']}; Namen auf -bühl gibt es nur im Oberland ({cnt[('Oberland', '-bühl')]}).")
f3_en = (f"In the Unterland {en(share('Unterland', '-berg'), 0)} percent of the {tot['Unterland']} mountain names end in -berg, in the Oberland {en(share('Oberland', '-berg'), 0)} percent "
         f"of {tot['Oberland']}; names in -bühl occur only in the Oberland ({cnt[('Oberland', '-bühl')]}).")

title1_de = f"Die Höhe der Orte sinkt von {de(hi_map['hoehe_mitte_m'], 0)} m im Südwesten auf {de(lo_map['hoehe_mitte_m'], 0)} m an der Elster"
title1_en = f"Altitude of places falls from {en(hi_map['hoehe_mitte_m'], 0)} m in the southwest to {en(lo_map['hoehe_mitte_m'], 0)} m on the Elster"
cap1_de = (f"{len(mapped)} von {n_orte} Orten mit Höhenangabe, an der heutigen Ortslage (GeoNames) gekartet. Farbe: Mitte der gedruckten Höhenspanne, aus preußischen Dezimalfuß in Meter "
           f"umgerechnet. Pfeil: Richtung des steilsten Gefälles im Oberland. Quelle: S. 11 bis 13, 20 bis 22.")
cap1_en = (f"{len(mapped)} of {n_orte} places with a stated altitude, mapped at their present-day location (GeoNames). Color: midpoint of the printed altitude range, converted from Prussian "
           f"decimal feet to meters. Arrow: direction of steepest descent in the Oberland. Source: pp. 11 to 13, 20 to 22.")
title2_de = f"Die Wohnpunkte des Unterlandes liegen im Median {de(med_u, 0)} m hoch, die des Oberlandes {de(med_o, 0)} m"
title2_en = f"Unterland inhabited points lie at a median of {en(med_u, 0)} m, Oberland ones at {en(med_o, 0)} m"
cap2_de = (f"Zahl der Wohnpunkte (Orte, Mühlen, Einzelhäuser) je Höhenklasse von 25 m; Linien: Median. Grau: Höhenbereich, den beide Landesteile teilen, "
           f"vom tiefsten Punkt des Oberlandes ({de(lo_ober, 0)} m) bis zum höchsten des Unterlandes ({de(hi_unter, 0)} m). Quelle: S. 4 bis 5, 11 bis 13, 20 bis 22.")
cap2_en = (f"Inhabited points (places, mills, single houses) per altitude class of 25 m; lines: median. Grey: range shared, "
           f"from the lowest point of the Oberland ({en(lo_ober, 0)} m) to the highest of the Unterland ({en(hi_unter, 0)} m). Source: pp. 4 to 5, 11 to 13, 20 to 22.")
title3_de = f"Die höchsten Berge überragen die höchsten Wohnplätze nur um {de(over_o, 0)} m (Oberland) und {de(over_u, 0)} m (Unterland)"
title3_en = f"The highest mountains rise only {en(over_o, 0)} m (Oberland) and {en(over_u, 0)} m (Unterland) above the highest villages"
cap3_de = ("Die sechs höchsten benannten Berge je Landesteil nach Brückners Höhenlisten, in Metern (Dezimalfuß × 0,3766). "
           "Quelle: S. 11 bis 15, 20 bis 24.")
cap3_en = ("The six highest named mountains per part according to Brückner’s height lists, in meters (decimal feet × 0.3766). "
           "Source: pp. 11 to 15, 20 to 24.")

for k, v in (("lead", lead_de), ("f1", f1_de), ("f2", f2_de), ("f3", f3_de), ("t1", title1_de), ("cap1", cap1_de), ("t2", title2_de), ("cap2", cap2_de),
             ("t3", title3_de), ("cap3", cap3_de)):
    print(f"[{words(v)}] {k}: {v}")

method_de = (
    "Quellen sind die Höhenlisten der bewohnten Punkte (S. 11 bis 13 für das Unterland, S. 20 bis 22 für das Oberland), die Listen der Höhenpunkte und Berghöhen "
    "(S. 13 bis 15, 22 bis 24), die Terrassenmittel im Text (S. 4 bis 5) und Brückners Aufzählung der Bergnamen (S. 10 bis 11, 15, 17 bis 20). Alle Höhen sind preußische "
    "Dezimalfuß, auf den Pegel bei Swinemünde bezogen (S. 11 Anm.), und wurden mit 0,3766242 m je Fuß in Meter umgerechnet. Bei Orten steht meist eine Spanne vom untersten "
    "bis zum obersten Haus; die Karte und die Mediane verwenden die Mitte. Für die Karte wurden die Orte über den Namen und den Landesteil mit der Kartengrundlage "
    "(GeoNames) verbunden; gleichnamige Orte mit verschiedenen Höhen blieben weg. Die Ausgleichsebene H = a + b × x + c × y wurde nach der Methode der kleinsten Quadrate "
    "durch die gekarteten Orte jedes Landesteils gelegt; die Fallrichtung ist der Azimut des steilsten Gefälles (von Nord im Uhrzeigersinn). Die Bergnamen wurden aus "
    "Brückners Aufzählungen nach dem Grundwort sortiert (editorisch). Die Einteilung der Höhenpunkte in benannte Berge, Himmelsrichtungshöhen und Bauwerke ist ebenfalls "
    "editorisch.")
method_en = (
    "Sources are the altitude lists of the inhabited points (pp. 11 to 13 for the Unterland, pp. 20 to 22 for the Oberland), the lists of height points and mountain "
    "heights (pp. 13 to 15, 22 to 24), the terrace means in the text (pp. 4 to 5) and Brückner’s enumeration of mountain names (pp. 10 to 11, 15, 17 to 20). All altitudes are "
    "Prussian decimal feet, referred to the Swinemünde gauge (p. 11 note), and were converted to meters at 0.3766242 m per foot. For places there is mostly a range from "
    "the lowest to the highest house; the map and the medians use the midpoint. For the map the places were joined to the base layer (GeoNames) by name and part of the "
    "country; homonyms with different altitudes were left out. The plane H = a + b × x + c × y was fitted by least squares through the mapped places of each part; the direction "
    "of fall is the azimuth of steepest descent (clockwise from north). The mountain names were sorted by generic element from Brückner’s enumerations (editorial). "
    "The division of the height points into named mountains, compass-direction heights and structures is also editorial.")
assert words(method_de) <= 260 and words(method_en) <= 260, (words(method_de), words(method_en))

caveats = [
    {"de": "Das Wort Fuß steht bei Brückner für den preußischen Dezimalfuß (0,3766 m), nicht für den Pariser Fuß (0,3248 m). Mit dem Pariser Fuß umgerechnet, lägen alle Höhen um rund 14 Prozent zu niedrig. Brückners eigene Gegenproben stützen die Umrechnung.",
     "en": "Brückner’s “Fuß” means the Prussian decimal foot (0.3766 m), not the Paris foot (0.3248 m). Converted with the Paris foot, all altitudes would be about 14 percent too low. Brückner’s own cross-checks support the conversion."},
    {"de": "Die Mitte der Spanne ist nur eine Kennzahl, keine Ortshöhe im heutigen Sinn. Die Unterscheidung von Orten und Einzelstellen (Mühlen, Bahnhöfe, Einzelhäuser) ist editorisch. Brückners Zählung für das Oberland (63 höher, 74 niedriger als 1340 Fuß, S. 22) lässt sich aus der Liste nicht nachvollziehen.",
     "en": "The midpoint of the range is only a summary figure, not a place altitude in the modern sense. The distinction between places and single sites (mills, stations, single houses) is editorial. Brückner’s count for the Oberland (63 higher, 74 lower than 1340 feet, p. 22) cannot be reproduced from the list."},
    {"de": "Die Karte stützt sich auf heutige Ortslagen. Der höchste bewohnte Punkt, Karolinenfeld bei Grumbach (706 m), ist nicht in der Kartengrundlage und fehlt deshalb. Ebersberg erscheint zweimal mit verschiedener Höhe und blieb ebenfalls weg.",
     "en": "The map rests on present-day locations. The highest inhabited point, Karolinenfeld near Grumbach (706 m), is not in the base layer and is therefore missing. Ebersberg appears twice with different altitudes and was also left out."},
    {"de": "Die Höhenlisten sind eine Auswahl, meist trigonometrisch für die Karte bestimmte Punkte, und keine systematische Erfassung; Höhere Gipfel können fehlen. Die Bergnamen sind Brückners Auswahl der wichtigen Berge. Die Anteile der Grundwörter sagen deshalb etwas über seine Auswahl, nicht über alle Flurnamen.",
     "en": "The height lists are a selection, mostly points determined trigonometrically for the map, and not a systematic survey; higher summits may be missing. The mountain names are Brückner’s selection of the important mountains. The shares of generic elements therefore say something about his selection, not about all field names."},
]
for c in caveats:
    assert words(c["de"]) <= 60 and words(c["en"]) <= 60, (words(c["de"]), words(c["en"]))
caveats[3]["de"] = caveats[3]["de"].replace("Höhere", "höhere")

issues = list(a_wohn.get("transcription_issues", [])) + list(a_erh.get("transcription_issues", []))
issues += [
    {"page": "22", "block": "b1", "cell": "r34c2", "transcribed": "Karolinensfeld 1874,6'", "facsimile": "Karolinenfeld 1874,6'", "checked_facsimile": True,
     "note": "Ortsname (höchster bewohnter Punkt des Oberlandes); die Zahl stimmt. Im Datensatz nach dem Faksimile korrigiert."},
    {"page": "22", "block": "b2", "transcribed": "Karolinensfeld", "facsimile": "Karolinenfeld (Karo-linenfeld)", "checked_facsimile": True,
     "note": "Ortsname im Text; derselbe Fehler steht auf S. 58 (Block b4, »Karolinensfeld bei Grumbach«), das hier nicht zitiert wird."},
]
union_sources = []
for a_ in (a_stufen, a_wohn, a_erh, a_neig, a_berg):
    for s_ in a_["sources"]:
        if s_ not in union_sources:
            union_sources.append(s_)
union_sources = [s_ for s_ in union_sources if not (s_["page"] in ("6", "7") )]   # coordinate tables belong to land-lage-grenzen
print("sources", len(union_sources))

orte = shared("base_places")
fluesse = shared("base_rivers")
feature = {
    "id": "relief-hoehen",
    "title": T("Berge und Höhenlage", "Mountains and altitude"),
    "category": "relief",
    "section": "t1-1-4",
    "merges": ["relief-erhebungen-hoechste-punkte", "relief-hoehe-und-lage-neigung", "relief-hoehenstufen-oberland-unterland",
               "relief-wohnorte-hoehenlage", "relief-bergnamen"],
    "sources": union_sources,
    "summary": T(lead_de, lead_en),
    "findings": [T(f1_de, f1_en), T(f2_de, f2_en), T(f3_de, f3_en)],
    "method": T(method_de, method_en),
    "conversions": [{**c_, "reference": c_["reference"].replace(" – unvereinbar", "; das ist unvereinbar")} for c_ in a_stufen["conversions"]],
    "caveats": caveats,
    "transcription_issues": issues,
    "datasets": [places_ds, heights_ds, levels_ds, arrow_ds, names_ds, orte, fluesse],
    "charts": [
        {"id": "c1", "dataset": "places", "extra_datasets": ["orte_basis", "fluesse_basis", "gefaelle_pfeil"],
         "title": T(title1_de, title1_en), "caption": T(cap1_de, cap1_en), "vegalite": c1},
        {"id": "c2", "dataset": "places", "extra_datasets": ["levels"],
         "title": T(title2_de, title2_en), "caption": T(cap2_de, cap2_en), "vegalite": c2},
        {"id": "c3", "dataset": "heights", "extra_datasets": ["places"],
         "title": T(title3_de, title3_en), "caption": T(cap3_de, cap3_en), "vegalite": c3},
    ],
    "keywords": {
        "de": ["Höhenlage", "Berge", "Gipfel", "Fichteberg", "Kulm", "Frankenwald", "Oberland", "Unterland", "Terrassen", "Bergnamen", "Meereshöhe"],
        "en": ["altitude", "mountains", "summits", "Fichteberg", "Kulm", "Frankenwald", "Oberland", "Unterland", "terraces", "mountain names", "elevation"],
    },
    "related": ["land-lage-grenzen", "gewaesser", "geologie-boden", "klima-stationen"],
    "generated_by": "Claude Sonnet 5.5 (Agent F1), aus 5 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}
dump(feature)
if "--no-validate" not in sys.argv:
    validate("relief-hoehen")
