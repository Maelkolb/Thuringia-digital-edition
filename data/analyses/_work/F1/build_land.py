"""Feature land-lage-grenzen (agent F1): merges grenzen-umfang-nachbarlaender, lage-vermessene-punkte-laenge-breite,
flaeche-fuerstenthum-vermessung-nachbarn. Every number in the texts is computed here from the datasets."""
import statistics
from common import *

# ---------------------------------------------------------------- source data
a_lage = load("lage-vermessene-punkte-laenge-breite")
a_gren = load("grenzen-umfang-nachbarlaender")
a_flae = load("flaeche-fuerstenthum-vermessung-nachbarn")

points_ds = json.loads(json.dumps(ds_of(a_lage, "points")))
extent_ds = ds_of(a_lage, "extent")
gren_ds = ds_of(a_gren, "grenzen")
totals_ds = ds_of(a_flae, "totals")
estim_ds = ds_of(a_flae, "estimates")
neigh_ds = ds_of(a_flae, "neighbours")
lt_ds = ds_of(a_flae, "landestheile")

# -- correction after the facsimile: p. 7 prints "Rüdersdorf", the digitised text has "Rödersdorf"
cols = [c["name"] for c in points_ds["columns"]]
iname = cols.index("name")
for r in points_ds["rows"]:
    if r[iname] == "Rödersdorf":
        r[iname] = "Rüdersdorf"

# -- derived columns: extreme points (p. 7) and distance to the GeoNames location of the same place
base_places = shared("base_places")
bcols = [c["name"] for c in base_places["columns"]]
base = {r[0]: dict(zip(bcols, r)) for r in base_places["rows"]}
geonames_name = {"Geissen": "Geißen"}           # spelling only
EXTREME = {"Röttersdorf": "W", "Bethenhausen": "E", "Titschendorf": "S", "Großaga": "N"}
ilon, ilat, iobj = cols.index("lon_gw"), cols.index("lat"), cols.index("objektart")
pts = [dict(zip(cols, r)) for r in points_ds["rows"]]
# check the printed statement (p. 7): westernmost, easternmost, southernmost, northernmost point (bracketed points excluded)
inside = [p for p in pts if p["lat"] is not None and not p["in_klammern"]]
assert min(inside, key=lambda p: p["lon_gw"])["name"] == "Röttersdorf"
assert max(inside, key=lambda p: p["lon_gw"])["name"] == "Bethenhausen"
assert min(inside, key=lambda p: p["lat"])["name"] == "Titschendorf"
assert max(inside, key=lambda p: p["lat"])["name"] == "Großaga"

points_ds["columns"] += [
    col("extrem", "Äußerster Punkt (S. 7)", "Extreme point (p. 7)", "string", None, True,
        "W, O, S, N nach Brückners Satz auf S. 7"),
    col("abstand_geonames_km", "Abstand zur Ortslage in GeoNames", "Distance to the GeoNames location", "number", "km", True,
        "Luftlinie zum gleichnamigen Ort der Kartengrundlage (GeoNames); nur wo der Name eindeutig ist"),
]
offsets = {}
offset_rows = []
for r, p in zip(points_ds["rows"], pts):
    n = geonames_name.get(p["name"], p["name"])
    ext = {"W": "W", "E": "O", "S": "S", "N": "N"}[EXTREME[p["name"]]] if p["name"] in EXTREME else None
    d = None
    if n in base and p["lat"] is not None:
        d = round(km(p["lon_gw"], p["lat"], base[n]["lon"], base[n]["lat"]), 2)
        offsets[p["name"]] = d
        offset_rows.append((p["name"], d))
    r += [ext, d]
EXTREME_DE = {"Röttersdorf": "westlichster Punkt", "Bethenhausen": "östlichster Punkt",
              "Titschendorf": "südlichster Punkt", "Großaga": "nördlichster Punkt"}

# ---------------------------------------------------------------- numbers for the texts
n_points = len(pts)
n_with_lat = sum(p["lat"] is not None for p in pts)
n_ober = sum(p["landesteil"] == "Oberland" for p in pts)
n_unter = n_points - n_ober
geissen_off = offsets["Geissen"]
others = [v for k, v in offset_rows if k != "Geissen"]       # one value per surveyed point (Eliasbrunn has two points)
med_off = statistics.median(others)
n_off = len(others)
print("points", n_points, n_with_lat, n_ober, n_unter, "| offsets", n_off, "median", med_off, "Geissen", geissen_off)

ex = {r[0]: dict(zip([c["name"] for c in extent_ds["columns"]], r)) for r in extent_ds["rows"]}
gap_km = (ex["Unterland"]["lat_min"] - ex["Oberland"]["lat_max"]) * 111.2
print("gap km", gap_km, ex)

g = [dict(zip([c["name"] for c in gren_ds["columns"]], r)) for r in gren_ds["rows"]]
ober_tot = round(sum(x["laenge_stunden"] for x in g if x["landesteil"] == "Oberland"))
unter_tot = round(sum(x["laenge_stunden"] for x in g if x["landesteil"] == "Unterland"))
assert (ober_tot, unter_tot) == (48, 18)
top_o = max((x for x in g if x["landesteil"] == "Oberland"), key=lambda x: x["laenge_stunden"])
top_u = max((x for x in g if x["landesteil"] == "Unterland"), key=lambda x: x["laenge_stunden"])
print(top_o["nachbar"], top_o["laenge_stunden"], top_o["anteil"], top_u["nachbar"], top_u["laenge_stunden"], top_u["anteil"])
n_nb_o = sum(x["landesteil"] == "Oberland" for x in g)
n_nb_u = sum(x["landesteil"] == "Unterland" for x in g)
nb_names = {x["nachbar"] for x in g}

t = {r[0]: dict(zip([c["name"] for c in totals_ds["columns"]], r)) for r in totals_ds["rows"]}
old, eng, now, lv = t["Hassel/Stein"], t["Engelhardt"], t["Nowack"], t["Landesvermessung"]
drop_pct = (1 - now["flaeche_qm"] / old["flaeche_qm"]) * 100
drop_pct_lv = (1 - lv["flaeche_qm"] / old["flaeche_qm"]) * 100
print("drop to Nowack %", drop_pct, "to LV", drop_pct_lv, "km2", old["flaeche_km2"], now["flaeche_km2"], lv["flaeche_km2"])
lt = [dict(zip([c["name"] for c in lt_ds["columns"]], r)) for r in lt_ds["rows"]]
morgen_total = sum(x["morgen"] for x in lt)
km2_survey = morgen_total * 0.255322 / 100
print("Morgen", morgen_total, "km2", km2_survey)
assert morgen_total == 316738
# Lobenstein-Ebersdorf: the only identically delimited part in the old and the new tables
est = [dict(zip([c["name"] for c in estim_ds["columns"]], r)) for r in estim_ds["rows"]]
lob = {x["quelle"]: x["flaeche_qm"] for x in est if x["gruppe"] == "Lobenstein-Ebersdorf"}
lob_drop_eng = (1 - lob["Engelhardt"] / lob["Hassel/Stein"]) * 100
lob_drop_lv = (1 - lob["Landesvermessung"] / lob["Hassel/Stein"]) * 100
print("Lobenstein", lob, lob_drop_eng, lob_drop_lv)
nb = [dict(zip([c["name"] for c in neigh_ds["columns"]], r)) for r in neigh_ds["rows"]]
wrong = [x for x in nb if x["faktor_aussage"] is not None and abs(x["faktor_rechnung"] / x["faktor_aussage"] - 1) > 0.1]
print("comparison fractions off:", [(x["staat"], x["aussage"], x["faktor_rechnung"]) for x in wrong])
koburg = next(x for x in nb if "Koburg" in x["staat"])
koburg_pct = (koburg["faktor_rechnung"] - 1) * 100
nowack = {x["gruppe"]: x["flaeche_qm"] for x in est if x["quelle"] == "Nowack"}
unter_qm = nowack["Gera"]
ober_qm = nowack["Saalburg + Reichenfels + Schleiz + Lobenstein-Ebersdorf"]
assert (ober_qm, unter_qm) == (11.03, 4.03)   # = Brückner p. 4

# ---------------------------------------------------------------- charts
OBER, UNTER = "@accent2", "@accent"
LAND_COLOR = {"field": "landesteil", "type": "nominal", "legend": None,
              "scale": {"domain": ["Oberland", "Unterland"], "range": [OBER, UNTER]}}
LL = {"longitude": {"field": "lon_gw", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}

named = ["Gera", "Schleiz", "Lobenstein", "Tanna"]
label_expr = {
    "de": "datum.name == 'Röttersdorf' ? 'Röttersdorf (W)' : datum.name == 'Bethenhausen' ? 'Bethenhausen (O)' : datum.name == 'Titschendorf' ? 'Titschendorf (S)' : datum.name == 'Großaga' ? 'Großaga (N)' : datum.name",
    "en": "datum.name == 'Röttersdorf' ? 'Röttersdorf (W)' : datum.name == 'Bethenhausen' ? 'Bethenhausen (E)' : datum.name == 'Titschendorf' ? 'Titschendorf (S)' : datum.name == 'Großaga' ? 'Großaga (N)' : datum.name",
}
label_filter_main = "indexof(['Gera','Schleiz','Lobenstein','Tanna','Röttersdorf','Bethenhausen','Titschendorf','Großaga'], datum.name) >= 0"


def text_layer(style, dx=0, dy=0, align="center", baseline="middle", flt=None):
    return {
        "transform": [{"filter": flt}, {"filter": "isValid(datum.lat)"}, {"calculate": label_expr, "as": "label"}],
        "mark": {"type": "text", "style": style, "dx": dx, "dy": dy, "align": align, "baseline": baseline},
        "encoding": {**LL, "text": {"field": "label"}},
    }


c1 = {
    "height": 540,
    "projection": {"type": "mercator"},
    "layer": [
        {"data": {"name": "fluesse_basis"}, "transform": [{"filter": "(datum.fluss != 'Weiße Elster' || datum.lat > 50.7) && datum.lat >= 50.36"}],
         "mark": {"type": "line", "color": "@river", "strokeWidth": 1.1},
         "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                      "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
        {"data": {"name": "extent"},
         "mark": {"type": "rect", "filled": False, "strokeDash": [5, 4], "strokeWidth": 1.2, "stroke": "@muted"},
         "encoding": {"longitude": {"field": "lon_min_gw", "type": "quantitative"}, "latitude": {"field": "lat_min", "type": "quantitative"},
                      "longitude2": {"field": "lon_max_gw"}, "latitude2": {"field": "lat_max"}}},
        {"data": {"name": "orte_basis"}, "mark": {"type": "circle", "size": 14, "color": "@land", "opacity": 1},
         "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}},
        {"transform": [{"filter": "isValid(datum.lat) && datum.in_klammern == 0"}],
         "mark": {"type": "circle", "size": 70, "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.95},
         "encoding": {**LL, "color": LAND_COLOR,
                      "tooltip": tooltip(("name", "Ort", "Place"), ("objekt", "Gemessener Gegenstand", "Object measured"),
                                         ("landesteil", "Landesteil", "Part"),
                                         ("lon_gw", "Länge östlich von Greenwich (°)", "Longitude east of Greenwich (°)", ".4f"),
                                         ("lat", "Breite (°)", "Latitude (°)", ".4f"),
                                         ("abstand_geonames_km", "Abstand zur heutigen Ortslage (km)", "Distance to present-day location (km)", ".2f"))}},
        {"transform": [{"filter": "isValid(datum.lat) && datum.in_klammern == 1"}],
         "mark": {"type": "circle", "size": 60, "filled": False, "strokeWidth": 1.8},
         "encoding": {**LL, "color": LAND_COLOR,
                      "tooltip": tooltip(("name", "Ort (in Klammern gedruckt)", "Place (printed in brackets)"), ("objekt", "Gemessener Gegenstand", "Object measured"),
                                         ("lon_gw", "Länge östlich von Greenwich (°)", "Longitude east of Greenwich (°)", ".4f"),
                                         ("lat", "Breite (°)", "Latitude (°)", ".4f"))}},
        text_layer("place-halo", dy=-12, flt=label_filter_main), text_layer("place-label", dy=-12, flt=label_filter_main),
        text_layer("place-halo", dx=9, align="left", flt="datum.name == 'Geissen'"), text_layer("place-label", dx=9, align="left", flt="datum.name == 'Geissen'"),
        # part names at the lower left corner of each printed rectangle
        {"data": {"name": "extent"}, "transform": [{"filter": "datum.landesteil == 'Oberland'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "baseline": "top", "dx": 6, "dy": 6, "color": OBER},
         "encoding": {"longitude": {"field": "lon_min_gw", "type": "quantitative"}, "latitude": {"field": "lat_max", "type": "quantitative"},
                      "text": {"value": {"de": "Oberland", "en": "Oberland"}}}},
        {"data": {"name": "extent"}, "transform": [{"filter": "datum.landesteil == 'Unterland'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "baseline": "top", "dx": 6, "dy": 6, "color": UNTER},
         "encoding": {"longitude": {"field": "lon_min_gw", "type": "quantitative"}, "latitude": {"field": "lat_max", "type": "quantitative"},
                      "text": {"value": {"de": "Unterland", "en": "Unterland"}}}},
        {"data": {"name": "extent"}, "transform": [{"filter": "datum.landesteil == 'Unterland'"}, {"calculate": "(datum.lon_min_gw + datum.lon_max_gw) / 2", "as": "lon_mid"}],
         "mark": {"type": "text", "style": "annotation", "align": "right", "baseline": "top", "dy": 14, "dx": -4},
         "encoding": {"longitude": {"field": "lon_min_gw", "type": "quantitative"}, "latitude": {"field": "lat_min", "type": "quantitative"},
                      "text": {"value": {"de": f"{de(gap_km, 0)} km Abstand, Weimarer Gebiet", "en": f"{en(gap_km, 0)} km apart, Weimar territory"}}}},
    ],
}

# --- c2: boundary length by neighbouring state, one panel per part
def border_panel(part, color, title):
    return {
        "width": 520,
        "height": {"step": 24},
        "title": {"text": title, "anchor": "start", "fontSize": 13, "offset": 6},
        "transform": [{"filter": f"datum.landesteil == '{part}'"}],
        "encoding": {"y": {"field": "nachbar", "type": "nominal", "sort": {"field": "laenge_stunden", "op": "max", "order": "descending"}, "axis": {"title": None, "labelLimit": 300, "labelAlign": "left", "labelPadding": 104, "minExtent": 108}}},
        "layer": [
            {"mark": {"type": "bar", "cornerRadiusEnd": 3},
             "encoding": {"x": {"field": "laenge_stunden", "type": "quantitative",
                                "scale": {"domain": [0, 24]},
                                "axis": {"title": ({"de": "Stunden", "en": "Stunden"} if part == "Unterland" else None), "values": [0, 6, 12, 18, 24]}},
                          "color": {"condition": {"test": "datum.laenge_stunden == " + str(max(x["laenge_stunden"] for x in g if x["landesteil"] == part)), "value": color},
                                    "value": "@context"},
                          "tooltip": tooltip(("nachbar", "Angrenzender Staat", "Neighboring state"),
                                             ("landesteil", "Landesteil", "Part"),
                                             ("laenge_text", "Länge (Stunden, wie gedruckt)", "Length (Stunden, as printed)"),
                                             ("anteil", "Anteil am Umfang (%)", "Share of perimeter (%)", ".1f"))}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"x": {"field": "laenge_stunden", "type": "quantitative"},
                          "text": {"field": "laenge_stunden", "type": "quantitative", "format": ".1~f"}}},
        ],
    }


c2 = {
    "vconcat": [
        border_panel("Oberland", OBER, {"de": f"Oberland: Umfang {ober_tot} Stunden, sechs Nachbarn", "en": f"Oberland: perimeter {ober_tot} Stunden, six neighbors"}),
        border_panel("Unterland", UNTER, {"de": f"Unterland: Umfang {unter_tot} Stunden, vier Nachbarn", "en": f"Unterland: perimeter {unter_tot} Stunden, four neighbors"}),
    ],
    "spacing": 22,
}
assert n_nb_o == 6 and n_nb_u == 4

# --- c3: area estimates
src_label = {
    "de": "datum.quelle == 'Hassel/Stein' ? 'Hassel und Stein, bis 1840' : datum.quelle == 'Engelhardt' ? 'Engelhardt, 1853' : datum.quelle == 'Nowack' ? 'Nowack, mittlere Zahl' : 'Landesvermessung ab 1840'",
    "en": "datum.quelle == 'Hassel/Stein' ? 'Hassel and Stein, until 1840' : datum.quelle == 'Engelhardt' ? 'Engelhardt, 1853' : datum.quelle == 'Nowack' ? 'Nowack, mean figure' : 'Land survey from 1840'",
}
val_label = {
    "de": "format(datum.flaeche_qm, '.3~f') + ' □M. = ' + format(datum.flaeche_km2, ',.0f') + ' km²'",
    "en": "format(datum.flaeche_qm, '.3~f') + ' sq. mi. = ' + format(datum.flaeche_km2, ',.0f') + ' km²'",
}
c3 = {
    "height": {"step": 44},
    "transform": [{"calculate": src_label, "as": "label"}, {"calculate": val_label, "as": "wert"}],
    "encoding": {"y": {"field": "label", "type": "ordinal", "sort": {"field": "reihenfolge", "op": "min"}, "axis": {"title": None, "labelLimit": 320}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadiusEnd": 3, "height": {"band": 0.62}},
         "encoding": {"x": {"field": "flaeche_qm", "type": "quantitative", "scale": {"domain": [0, 30]},
                            "axis": {"title": {"de": "Fläche in geographischen Quadratmeilen", "en": "Area in geographical square miles"}, "values": [0, 5, 10, 15, 20, 25]}},
                      "color": {"condition": {"test": "datum.quelle == 'Nowack'", "value": "@accent"}, "value": "@context"},
                      "tooltip": tooltip(("quelle", "Quelle", "Source"), ("flaeche_qm", "Quadratmeilen", "Square miles", ".3~f"),
                                         ("flaeche_km2", "km²", "km²", ",.0f"))}},
        {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
         "encoding": {"x": {"field": "flaeche_qm", "type": "quantitative"}, "text": {"field": "wert"}}},
        {"transform": [{"filter": "datum.quelle == 'Nowack'"}],
         "mark": {"type": "text", "align": "left", "dx": 6, "dy": 15, "style": "annotation"},
         "encoding": {"x": {"field": "flaeche_qm", "type": "quantitative"},
                      "text": {"value": {"de": f"von Brückner angesetzt, {de(drop_pct, 0)} Prozent weniger", "en": f"adopted by Brückner, {en(drop_pct, 0)} percent less"}}}},
    ],
}

# ---------------------------------------------------------------- texts
lead_de = (f"Brückner druckt Länge und Breite von {n_points} trigonometrisch bestimmten Punkten, den Umfang beider Landesteile nach "
           f"Nachbarstaaten und mehrere Flächenangaben. Das Fürstentum besteht aus dem Oberland ({de(ober_qm, 2)} Quadratmeilen) und dem "
           f"Unterland ({de(unter_qm, 2)}), zwischen denen Weimarer Gebiet liegt. Die Fläche wurde von {de(old['flaeche_qm'], 1)} auf "
           f"{de(now['flaeche_qm'], 2)} Quadratmeilen herabgesetzt, umgerechnet rund {de(now['flaeche_km2'], 0)} km².")
lead_en = (f"Brückner prints longitude and latitude of {n_points} points fixed by triangulation, the perimeter of both parts by neighboring state, "
           f"and several area figures. The principality consists of the Oberland ({en(ober_qm, 2)} square miles) and the Unterland "
           f"({en(unter_qm, 2)}), with Weimar territory between them. The area was revised from {en(old['flaeche_qm'], 1)} to "
           f"{en(now['flaeche_qm'], 2)} square miles, about {en(now['flaeche_km2'], 0)} km² converted.")

f1_de = (f"Rechnet man Brückners Längen von Ferro auf Greenwich um, liegen {n_off} Punkte im Median {de(med_off, 1)} km neben der heutigen Ortslage; "
         f"nur Geissen weicht um {de(geissen_off, 0)} km ab.")
f1_en = (f"Converting Brückner’s longitudes from Ferro to Greenwich puts {n_off} points a median of {en(med_off, 1)} km from the present-day location; "
         f"only Geissen is off, by {en(geissen_off, 0)} km.")
f2_de = (f"Das Oberland grenzt mit {de(top_o['laenge_stunden'], 0)} von {ober_tot} Stunden Umfang an Reuß älterer Linie; "
         f"die Hälfte des Unterlandes ({de(top_u['laenge_stunden'], 0)} von {unter_tot} Stunden) grenzt an Altenburg.")
f2_en = (f"The Oberland borders Reuss (Elder Line) for {en(top_o['laenge_stunden'], 0)} of {ober_tot} Stunden of its perimeter; "
         f"half of the Unterland ({en(top_u['laenge_stunden'], 0)} of {unter_tot} Stunden) borders Altenburg.")
f3_de = (f"Auch das einzige gleich abgegrenzte Gebiet, Lobenstein-Ebersdorf, schrumpfte von {de(lob['Hassel/Stein'], 2)} auf {de(lob['Engelhardt'], 2)} Quadratmeilen "
         f"(minus {de(lob_drop_eng, 0)} Prozent); die Landesvermessung ergibt {de(morgen_total, 0)} preußische Morgen oder {de(km2_survey, 1)} km².")
f3_en = (f"Even the one identically delimited area, Lobenstein-Ebersdorf, shrank from {en(lob['Hassel/Stein'], 2)} to {en(lob['Engelhardt'], 2)} square miles "
         f"(minus {en(lob_drop_eng, 0)} percent); the land survey gives {en(morgen_total, 0)} Prussian Morgen, or {en(km2_survey, 1)} km².")

caption1_de = ("Gedruckte Koordinaten der 56 Punkte mit Länge und Breite, von Ferro auf Greenwich umgerechnet. Gestrichelt: Grenzwerte der beiden Landesteile (S. 6); "
               "hohl: Punkte in Klammern; W, O, S, N: äußerste Punkte (S. 7). Geissen fällt wegen einer vermutlich falsch gedruckten Breite in die Lücke.")
caption1_en = ("Printed coordinates of the 56 points with longitude and latitude, converted from Ferro to Greenwich. Dashed: limits of the two parts (p. 6); "
               "hollow: bracketed points; W, E, S, N: extreme points (p. 7). Geissen falls into the gap because of a probably misprinted latitude.")
title1_de = "Brückners Messpunkte zeichnen zwei getrennte Landesteile nach"
title1_en = "Brückner’s survey points trace two separate parts of the country"
title2_de = f"Das Oberland grenzt am längsten an Reuß ä. L., das Unterland an Altenburg"
title2_en = f"The Oberland borders Reuss (Elder Line) longest, the Unterland borders Altenburg"
caption2_de = ("Länge der Grenze in Stunden (vermutlich Wegstunden, von Brückner nicht erklärt) je Nachbarstaat, getrennt für beide Landesteile; "
               "gemessen in den Krümmungen einschließlich Ex- und Enklaven. Quelle: S. 5.")
caption2_en = ("Length of the boundary in Stunden (presumably walking hours, not explained by Brückner) by neighboring state, for each part separately; measured "
               "along its windings, including exclaves and enclaves. Source: p. 5.")
title3_de = f"Die Flächenschätzung sank von {de(old['flaeche_qm'], 1)} auf {de(now['flaeche_qm'], 2)} Quadratmeilen"
title3_en = f"The area estimate fell from {en(old['flaeche_qm'], 1)} to {en(now['flaeche_qm'], 2)} square miles"
caption3_de = (f"Gesamtfläche des Fürstentums nach vier Angaben, in Quadratmeilen und in km² (1 Quadratmeile = {de(QM_KM2, 2)} km²). "
               f"Das Ergebnis der Landesvermessung ({de(lv['flaeche_qm'], 3)}) und Engelhardts Zahl liegen eng bei Nowacks Mittel. Quelle: S. 7 bis 8.")
caption3_en = (f"Total area of the principality according to four statements, in square miles and km² (1 square mile = {en(QM_KM2, 2)} km²). "
               f"The result of the land survey ({en(lv['flaeche_qm'], 3)}) and Engelhardt’s figure lie close to Nowack’s mean. Source: pp. 7 to 8.")

method_de = (
    "Die Koordinaten der Punkte stehen in den Tabellen auf S. 6 und 7, die Grenzwerte der Landesteile über der Tabelle auf S. 6. Länge ist bei Brückner östlich "
    "von Ferro gezählt; für die Karte wurden 17° 40′ abgezogen (Ferro liegt genauer 17° 39′ 46″ westlich von Greenwich). Der Abstand zur Ortslage in GeoNames "
    "dient als Gegenprobe der Umrechnung. Die Zuordnung zum Oberland oder Unterland folgt der gedruckten Südgrenze des Unterlandes. Die Grenzlängen "
    "(S. 5) stehen im Fließtext; gemischte Brüche wurden in Dezimalzahlen umgesetzt, die Teilwerte ergeben genau 48 und 18 Stunden. "
    "Die Flächenangaben stammen von S. 7 und 8; Morgen wurden mit Brückners Faktor (S. 832) in Hektar, Quadratmeilen mit der geographischen "
    "Quadratmeile in km² umgerechnet. Dass Brückner diese Meile meint, ist eine Annahme, die die Gesamtzahlen stützen. Kilometerangaben "
    "zu den Grenzwerten sind Näherungen (1° Breite = 111,2 km).")
method_en = (
    "The coordinates of the points are in the tables on pp. 6 and 7, the limits of the two parts above the table on p. 6. Brückner counts longitude east "
    "of Ferro; for the map 17° 40′ were subtracted (more precisely Ferro lies 17° 39′ 46″ west of Greenwich). The distance to the location in GeoNames "
    "serves as a check of the conversion. Assignment to the Oberland or Unterland follows the printed southern limit of the Unterland. The boundary lengths "
    "(p. 5) are in the running text; mixed fractions were converted to decimals, and the partial values add up exactly to 48 and 18 Stunden. "
    "The area figures come from pp. 7 and 8; Morgen were converted to hectares with Brückner’s factor (p. 832), square miles to km² with the geographical "
    "square mile. That Brückner means this mile is an assumption supported by the totals. Kilometer figures for the limits "
    "are approximations (1° latitude = 111.2 km).")

geissen_lat_dms = "50° 45′ 44″"
geissen = next(p for p in pts if p["name"] == "Geissen")
geissen_fixed_off = km(geissen["lon_gw"], 50 + 51 / 60 + 44 / 3600, base["Geißen"]["lon"], base["Geißen"]["lat"])
print("Geissen with 51' instead of 45':", geissen_fixed_off)
caveats = [
    {"de": (f"Geissen liegt nach der gedruckten Breite ({geissen_lat_dms}) südlich der Südgrenze des Unterlandes und {de(geissen_off, 0)} km von der heutigen Ortslage entfernt. "
            f"Das Faksimile zeigt den Wert wie transkribiert; vermutlich ist 51′ statt 45′ gemeint, dann läge der Punkt {de(geissen_fixed_off, 1)} km neben der Ortslage. Er ist wie gedruckt eingetragen."),
     "en": (f"By its printed latitude ({geissen_lat_dms}) Geissen lies south of the southern limit of the Unterland and {en(geissen_off, 0)} km from the present-day location. "
            f"The facsimile shows the value as transcribed; probably 51′ instead of 45′ is meant, which would put the point {en(geissen_fixed_off, 1)} km from the location. It is plotted as printed.")},
    {"de": "Gemessen wurde nicht überall derselbe Gegenstand (Kirche, Turmknopf, Signal, Mühle, Schornstein, einzelner Baum). Hundertstelsekunden täuschen eine Genauigkeit vor, die die Methode nicht hatte. St. Gangloff und Heukenwalde stehen in Klammern, was Brückner nicht erklärt; sie liegen vermutlich außerhalb des Fürstentums.",
     "en": "Not the same kind of object was measured everywhere (church, tower finial, signal, mill, chimney, single tree). Hundredths of seconds imply a precision the method did not have. St. Gangloff and Heukenwalde are bracketed, which Brückner does not explain; they probably lie outside the principality."},
    {"de": "Die Stunde ist vermutlich ein Wegmaß, das Brückner nicht erklärt; seine Maßtabelle (S. 831 bis 832) enthält keine Wegstunde. Die Grenzlängen sind daher nur untereinander vergleichbar und lassen sich nicht in Kilometer umrechnen.",
     "en": "The Stunde is presumably a measure of walking distance that Brückner does not explain; his table of units (pp. 831 to 832) contains no walking hour. The boundary lengths are therefore comparable only with each other and cannot be converted to kilometers."},
    None,
]
# Koburg: Brueckner says "um 1/3 groesser als S.-Koburg"; from his numbers the principality is 48 % larger
caveats[3] = {
    "de": (f"Die Teilsummen der Quellen sind nicht gleich gruppiert, und die Morgen der Landesvermessung verhalten sich nicht proportional zu ihren Quadratmeilen. "
           f"Von Brückners Größenvergleichen mit sechs Nachbarstaaten stimmt nur einer nicht: Das Fürstentum ist nach seinen Zahlen um {de(koburg_pct, 0)} Prozent größer als Sachsen-Koburg, nicht um ein Drittel."),
    "en": (f"The partial sums of the sources are not grouped identically, and the Morgen of the land survey are not proportional to their square miles. "
           f"Of Brückner’s size comparisons with six neighboring states only one does not hold: by his figures the principality is {en(koburg_pct, 0)} percent larger than Saxe-Coburg, not a third."),
}
assert len(wrong) == 1 and "Koburg" in wrong[0]["staat"]

# ---------------------------------------------------------------- assemble
orte = shared("base_places")
fluesse = shared("base_rivers")

issues = [i for i in a_lage["transcription_issues"]]
issues.append({"page": "7", "block": "b1", "cell": "r3c1", "transcribed": "Rödersdorf", "facsimile": "Rüdersdorf",
               "checked_facsimile": True, "note": "Ortsname (Mühle bei Gera); im Datensatz nach dem Faksimile korrigiert. Die Zahlen stimmen."})

feature = {
    "id": "land-lage-grenzen",
    "title": T("Lage, Fläche und Grenzen", "Position, area and boundaries"),
    "category": "geography",
    "section": "t1-1-2",
    "merges": ["grenzen-umfang-nachbarlaender", "lage-vermessene-punkte-laenge-breite", "flaeche-fuerstenthum-vermessung-nachbarn"],
    "sources": [{"page": "3", "block": "b3"}, {"page": "4", "block": "b2"}, {"page": "4", "block": "b3"}, {"page": "5", "block": "b1"},
                {"page": "5", "block": "b2"}, {"page": "6", "block": "b2"}, {"page": "6", "block": "b3", "rows": "r1-r37"},
                {"page": "7", "block": "b1", "rows": "r1-r20"}, {"page": "7", "block": "b2"}, {"page": "7", "block": "b7", "rows": "r1-r3"},
                {"page": "8", "block": "b2", "rows": "r5-r10"}, {"page": "8", "block": "b3"}, {"page": "832", "block": "b2"}],
    "summary": T(lead_de, lead_en),
    "findings": [T(f1_de, f1_en), T(f2_de, f2_en), T(f3_de, f3_en)],
    "method": T(method_de, method_en),
    "conversions": a_lage["conversions"] + a_flae["conversions"][:2],
    "caveats": caveats,
    "transcription_issues": issues,
    "datasets": [
        points_ds,
        {**extent_ds},
        {**gren_ds},
        {**totals_ds},
        {**lt_ds},
        {**neigh_ds},
        orte,
        fluesse,
    ],
    "charts": [
        {"id": "c1", "dataset": "points", "extra_datasets": ["extent", "orte_basis", "fluesse_basis"],
         "title": T(title1_de, title1_en), "caption": T(caption1_de, caption1_en), "vegalite": c1},
        {"id": "c2", "dataset": "grenzen", "title": T(title2_de, title2_en), "caption": T(caption2_de, caption2_en), "vegalite": c2},
        {"id": "c3", "dataset": "totals", "title": T(title3_de, title3_en), "caption": T(caption3_de, caption3_en), "vegalite": c3},
    ],
    "keywords": {
        "de": ["Lage", "Größe", "Grenzen", "Nachbarstaaten", "Koordinaten", "Triangulation", "Landesvermessung", "Fläche", "Oberland", "Unterland"],
        "en": ["position", "area", "boundaries", "neighboring states", "coordinates", "triangulation", "land survey", "Oberland", "Unterland"],
    },
    "related": ["relief-hoehen", "gewaesser", "landesgeschichte", "bevoelkerung-1647-1867"],
    "generated_by": "Claude Sonnet 5.5 (Agent F1), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

for k, v in (("title", title1_de), ("lead", lead_de), ("f1", f1_de), ("f2", f2_de), ("f3", f3_de), ("c1cap", caption1_de), ("t2", title2_de),
             ("c2cap", caption2_de), ("t3", title3_de), ("c3cap", caption3_de)):
    print(f"[{words(v)} words] {k}: {v}")
dump(feature)
if "--no-validate" not in sys.argv:
    validate("land-lage-grenzen")
