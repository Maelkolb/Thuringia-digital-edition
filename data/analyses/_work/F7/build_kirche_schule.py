"""Feature F7b: kirche-schule (Kirchen und Schulen)."""
import json
import os
import statistics
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F7")
from common import *
from school_data import build as build_school_data

FID = "kirche-schule"
n, e = de_num, en_num

# ---------------------------------------------------------------- school places and links
places, links, place_refs, link_refs = build_school_data()
N = len(places)
own = [p for p in places if p["own"]]
neighbour = [p for p in places if not p["own"]]
n_own, n_neighbour = len(own), len(neighbour)
assert n_own + n_neighbour == N == 173
region_stats = {}
for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
    xs = [p for p in places if p["landestheil"] == lt]
    region_stats[lt] = (len(xs), sum(p["own"] for p in xs))
share = lambda lt: region_stats[lt][1] / region_stats[lt][0] * 100
big = [p for p in places if p["inhabitants"] >= 300]
big_share = sum(p["own"] for p in big) / len(big) * 100
small = [p for p in places if p["inhabitants"] < 100]
small_own = sum(p["own"] for p in small)
pupils_median = statistics.median([p["pupils"] for p in own if p["pupils"] and p["name"] != "Gera"])
no_coord = [p["name"] for p in places if p["lon"] is None]
missing_pupils = [p["name"] for p in own if p["pupils"] is None]
missing_pupils_de = ", ".join(missing_pupils[:-1]) + " und " + missing_pupils[-1]
missing_pupils_en = ", ".join(missing_pupils[:-1]) + " and " + missing_pupils[-1]
links_drawn = [l for l in links if l["drawn"]]
links_outside = [l for l in links if not l["inside"]]

ds_places = dataset(
    "schulorte",
    bi("Schulort oder Schule im Nachbarort: 173 Gemeinden", "School place or school in a neighbouring place: 173 municipalities"),
    [col("name", "Ort", "Place", "string"),
     col("landestheil", "Landesteil", "District", "string"),
     col("kind", "Art des Ortes", "Type of place", "string", None, True, "Stadt, Marktflecken oder Dorf nach der Angabe im Ortsartikel"),
     col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
     col("school", "Schule", "School", "string", None, True, "eigene Schule oder Schule im Nachbarort, nach dem Ortsartikel; Kleinfalke korrigiert"),
     col("pupils", "Schulkinder", "Pupils", "integer", "Kinder", False, "Bei Schulorten einschließlich eingeschulter Kinder anderer Orte, bei Orten ohne Schule die Kinder im auswärtigen Schulort"),
     col("school_place", "Schulort (für Orte ohne eigene Schule)", "School place (for places without a school)", "string", None, True),
     col("lon", "Länge", "Longitude", "number", "°", True, "GeoNames"),
     col("lat", "Breite", "Latitude", "number", "°", True, "GeoNames")],
    [[p["name"], p["landestheil"], p["kind"], p["inhabitants"],
      "eigene Schule" if p["own"] else "Schule im Nachbarort", p["pupils"],
      None if p["own"] else (" oder ".join(l["school_place"] for l in links if l["place"] == p["name"]) or None),
      p["lon"], p["lat"]] for p in places],
    place_refs,
)

ds_links = dataset(
    "schulwege",
    bi("Orte ohne eigene Schule und ihr Schulort", "Places without a school of their own and their school place"),
    [col("place", "Ort ohne eigene Schule", "Place without a school", "string"),
     col("school_place", "Schulort", "School place", "string"),
     col("outside", "Schulort außerhalb des Fürstentums", "School place outside the principality", "string", None, True),
     col("place_lon", "Länge des Ortes", "Longitude of the place", "number", "°", True, "GeoNames"),
     col("place_lat", "Breite des Ortes", "Latitude of the place", "number", "°", True, "GeoNames"),
     col("school_lon", "Länge des Schulortes", "Longitude of the school place", "number", "°", True, "GeoNames"),
     col("school_lat", "Breite des Schulortes", "Latitude of the school place", "number", "°", True, "GeoNames")],
    [[l["place"], l["school_place"], "nein" if l["inside"] else "ja", l["place_lon"], l["place_lat"], l["school_lon"], l["school_lat"]] for l in links],
    link_refs,
)

base_places = shared_dataset("base_places.json")
base_rivers = shared_dataset("base_rivers.json")

# ---------------------------------------------------------------- pupils per teacher
V = {  # name -> (de, en, schools, teachers, pupils 1863, pupils 1868)
    "Gera Land": ("Volksschulen Gera, Land", "Elementary schools, Gera, country", 30, 34, 2860, 3163),
    "Schleiz Land": ("Volksschulen Schleiz, Land", "Elementary schools, Schleiz, country", 37, 39, 3115, 3356),
    "Schleiz Städte": ("Volksschulen Schleiz, Städte", "Elementary schools, Schleiz, towns", 4, 17, 1333, 1373),
    "Lobenstein-Ebersdorf Land": ("Volksschulen Lobenstein-Ebersdorf, Land", "Elementary schools, Lobenstein-Ebersdorf, country", 39, 44, 2899, 2980),
    "Lobenstein-Ebersdorf Städte": ("Volksschulen Lobenstein-Ebersdorf, Städte", "Elementary schools, Lobenstein-Ebersdorf, towns", 2, 13, 847, 838),
    "Gera Stadt": ("Volksschulen Gera, Stadt", "Elementary schools, Gera, town", 3, 59, 1865, 2529),
}
H = {  # name -> (de, en, teachers, pupils)
    "Realschule Gera": ("Realschule Gera", "Realschule, Gera", 19, 432),
    "Gymnasium Gera": ("Gymnasium Gera", "Gymnasium, Gera", 15, 190),
    "Gymnasium Schleiz": ("Gymnasium Schleiz", "Gymnasium, Schleiz", 11, 114),
}
sl_rows = []
for k, (de, en, sch, tea, p63, p68) in V.items():
    sl_rows.append([de, en, "Volksschule", sch, tea, p63, p68, round(p68 / tea, 1), round((p68 / p63 - 1) * 100, 1)])
for k, (de, en, tea, pu) in H.items():
    sl_rows.append([de, en, "Höhere Schule", None, tea, None, pu, round(pu / tea, 1), None])
ppt = {r[0]: r[7] for r in sl_rows}
vol_tot = {"schools": sum(v[2] for v in V.values()), "teachers": sum(v[3] for v in V.values()), "pupils": sum(v[5] for v in V.values()), "pupils63": sum(v[4] for v in V.values())}
assert vol_tot == {"schools": 115, "teachers": 206, "pupils": 14239, "pupils63": 12919}
land_pupils = sum(V[k][5] for k in ("Gera Land", "Schleiz Land", "Lobenstein-Ebersdorf Land"))
land_teachers = sum(V[k][3] for k in ("Gera Land", "Schleiz Land", "Lobenstein-Ebersdorf Land"))
land_ppt = land_pupils / land_teachers
assert land_pupils == 9499 and land_teachers == 117
avg_ppt = vol_tot["pupils"] / vol_tot["teachers"]

ds_sl = dataset(
    "schulen_lehrer",
    bi("Schüler und Lehrer an Volksschulen und höheren Schulen", "Pupils and teachers at elementary and secondary schools"),
    [col("name_de", "Schule", "School", "string"),
     col("name_en", "Schule (englisch)", "School (English)", "string"),
     col("kind", "Schulart", "Type of school", "string", None, True),
     col("schools", "Schulen", "Schools", "integer", "Schulen"),
     col("teachers", "Lehrer", "Teachers", "integer", "Lehrer", True, "Volksschulen wie gedruckt; Realschule 17 + 2 eigene Lehrer, Gymnasien Haupt- plus Hilfslehrer"),
     col("pupils_1863", "Schüler 1863", "Pupils 1863", "integer", "Schüler"),
     col("pupils", "Schüler", "Pupils", "integer", "Schüler", False, "Volksschulen Ende 1868, höhere Schulen 1868/69"),
     col("pupils_per_teacher", "Schüler je Lehrer", "Pupils per teacher", "number", None, True),
     col("growth_pct", "Zunahme der Schülerzahl 1863 bis 1868", "Growth in pupils 1863 to 1868", "number", "%", True)],
    sl_rows,
    [ref(299, "b3", "r2, r3, r6, r7, r10, r11"), ref(299, "b4"), ref(300, "b4"), ref(300, "b6")],
)

# ---------------------------------------------------------------- pay
pay_rows = [
    [1, "Volksschullehrer, Mindestgehalt", "Elementary teachers, minimum salary", "Lehrer", 180, 240, None, None, None],
    [2, "Rektoren, Oberlehrer, Mindestgehalt", "Rectors, senior teachers, minimum salary", "Lehrer", 300, 400, None, None, None],
    [3, "Pfarrstellen", "Pastorates", "Pfarrer", 400, 500, 8, 2, None],
    [4, "Pfarrstellen", "Pastorates", "Pfarrer", 500, 600, 12, 2, None],
    [5, "Pfarrstellen", "Pastorates", "Pfarrer", 600, 700, 11, 3, None],
    [6, "Pfarrstellen", "Pastorates", "Pfarrer", 700, 800, 6, 1, None],
    [7, "Pfarrstellen", "Pastorates", "Pfarrer", 800, 1000, 12, 2, 1],
    [8, "Pfarrstellen", "Pastorates", "Pfarrer", 1000, None, 10, None, 2],
]
posts_total = sum(r[6] for r in pay_rows if r[6])
posts_below_600 = sum(r[6] for r in pay_rows if r[6] and r[5] is not None and r[5] <= 600)
posts_from_800 = sum(r[6] for r in pay_rows if r[6] and r[4] >= 800)
min_pastor = min(r[4] for r in pay_rows if r[3] == "Pfarrer")
min_teacher = min(r[4] for r in pay_rows if r[3] == "Lehrer")
teacher_max = max(r[5] for r in pay_rows if r[3] == "Lehrer" and r[0] == 1)
deacons_total = sum(r[7] or 0 for r in pay_rows)
ephors_total = sum(r[8] or 0 for r in pay_rows)
NORM = 50
assert posts_total == 59

ds_pay = dataset(
    "gehaelter",
    bi("Gehalt der Pfarrstellen und gesetzliches Mindestgehalt der Lehrer", "Pay of the pastorates and legal minimum pay of teachers"),
    [col("order", "Reihenfolge", "Order", "integer", None, True),
     col("group_de", "Gruppe", "Group", "string"),
     col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
     col("kind", "Art", "Kind", "string", None, True),
     col("lo", "Von", "From", "integer", "Taler"),
     col("hi", "Bis (leer: nach oben offen)", "To (empty: open at the top)", "integer", "Taler"),
     col("posts", "Zahl der Stellen", "Number of posts", "integer", "Stellen"),
     col("deacons", "darunter Diakonen", "of which deacons", "integer", "Stellen"),
     col("ephors", "darunter Ephoren", "of which ephors", "integer", "Stellen")],
    pay_rows,
    [ref(294, "b2", "r2-r7"), ref(297, "b3")],
)

ds_eph = dataset(
    "ephorien",
    bi("Parochien, Kirchen und Geistliche nach Ephorien", "Parishes, churches and clergy by ephory"),
    [col("ephory", "Ephorie", "Ephory", "string"),
     col("parishes", "Parochien", "Parishes", "integer", "Parochien"),
     col("churches", "Kirchen", "Churches", "integer", "Kirchen"),
     col("clergy", "Geistliche", "Clergy", "integer", "Personen"),
     col("catechists", "Katecheten", "Catechists", "integer", "Personen")],
    [["Gera", 14, 44, 25, 2], ["Schleiz", 20, 36, 27, None], ["Lobenstein", 11, 22, 16, None]],
    [ref(294, "b6", "r2-t5")],
)
eph_tot = {"parishes": 45, "churches": 102, "clergy": 68}
assert eph_tot == {"parishes": 14 + 20 + 11, "churches": 44 + 36 + 22, "clergy": 25 + 27 + 16}

# ---------------------------------------------------------------- charts
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}
label_names = ["Gera", "Schleiz", "Lobenstein", "Hirschberg", "Hohenleuben", "Tanna", "Saalburg", "Frankenthal", "Dorna", "Großaga", "Groitschen"]
name_filter = "indexof(" + json.dumps(label_names, ensure_ascii=False).replace('"', "'") + ", datum.name) >= 0"
status_calc = {"calculate": {
    "de": "datum.school === 'eigene Schule' ? 'Eigene Schule' : 'Schule im Nachbarort'",
    "en": "datum.school === 'eigene Schule' ? 'School of its own' : 'School in a neighbouring place'"}, "as": "status"}
STATUS_LEGEND = {"title": None, "orient": "none", "legendX": 10, "legendY": 10, "direction": "vertical", "symbolSize": 90, "labelLimit": 320}
status_color = lambda legend: {
    "field": "status", "type": "nominal",
    "scale": {"domain": [bi("Eigene Schule", "School of its own"), bi("Schule im Nachbarort", "School in a neighbouring place")], "range": ["@accent", "@accent2"]},
    "legend": legend}
tip_place = [
    {"field": "name", "title": bi("Ort", "Place")},
    {"field": "landestheil", "title": bi("Landesteil", "District")},
    {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants"), "format": ",d"},
    {"field": "status", "title": bi("Schule", "School")},
    {"field": "pupils", "title": bi("Schulkinder", "Pupils"), "format": ",d"},
    {"field": "school_place", "title": bi("Schulort", "School place")},
]

def panel(title, center, scale, width, height, labels, with_legend, bar_at, bbox):
    """One map panel; the legends are drawn only in the panel that asks for them."""
    flt = "indexof(" + json.dumps(labels, ensure_ascii=False).replace('"', "'") + ", datum.name) >= 0 && isValid(datum.lon)"
    color_nb = status_color(STATUS_LEGEND) if with_legend else None
    size_legend = ({"title": bi("Schulkinder", "Pupils"), "values": [25, 100, 300, 1000], "format": ",d", "orient": "none", "legendX": width - 112, "legendY": height - 130,
                    "direction": "vertical", "symbolFillColor": "@muted", "symbolStrokeColor": "@paper"} if with_legend else None)
    nb_enc = {"longitude": LON, "latitude": LAT, "tooltip": tip_place}
    own_enc = {"longitude": LON, "latitude": LAT, "tooltip": tip_place,
               "size": {"field": "pupils", "type": "quantitative", "scale": {"type": "sqrt", "domain": [0, 2700], "range": [10, 800]}, "legend": size_legend}}
    nb_mark = {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 1, "size": 34}
    own_mark = {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85}
    if with_legend:
        nb_enc["color"] = status_color(STATUS_LEGEND)
        own_enc["color"] = status_color(STATUS_LEGEND)
    else:
        nb_mark["color"] = "@accent2"
        own_mark["color"] = "@accent"
    lon0, lat0 = bar_at
    dlon = 5 / (111.32 * 0.634)
    west, east, south, north = bbox
    inside = lambda lo, la: f"datum.{lo} > {west} && datum.{lo} < {east} && datum.{la} > {south} && datum.{la} < {north}"
    geo = inside("lon", "lat")
    return {
        "title": {"text": title, "anchor": "start", "fontSize": 12, "fontWeight": 600, "offset": 6},
        "width": width, "height": height,
        "view": {"stroke": "@context", "strokeWidth": 1},
        "projection": {"type": "mercator", "center": center, "scale": scale, "translate": [width / 2, height / 2]},
        "layer": [
            {"data": {"name": "fluesse_basis"}, "transform": [{"filter": geo}], "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2},
             "encoding": {"longitude": LON, "latitude": LAT, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
            {"data": {"name": "orte_basis"}, "transform": [{"filter": geo}], "mark": {"type": "circle", "size": 10, "color": "@land", "opacity": 1},
             "encoding": {"longitude": LON, "latitude": LAT}},
            {"data": {"name": "schulwege"},
             "transform": [{"filter": "isValid(datum.place_lon) && isValid(datum.school_lon) && " + inside("place_lon", "place_lat") + " && " + inside("school_lon", "school_lat")}],
             "mark": {"type": "rule", "color": "@accent2", "strokeWidth": 1.1, "opacity": 0.75},
             "encoding": {"longitude": {"field": "place_lon", "type": "quantitative"}, "latitude": {"field": "place_lat", "type": "quantitative"},
                          "longitude2": {"field": "school_lon"}, "latitude2": {"field": "school_lat"}}},
            {"transform": [{"filter": geo + " && datum.school !== 'eigene Schule'"}, status_calc],
             "mark": nb_mark, "encoding": nb_enc},
            {"transform": [{"filter": geo + " && datum.school === 'eigene Schule' && isValid(datum.pupils)"}, status_calc],
             "mark": own_mark, "encoding": own_enc},
            {"transform": [{"filter": geo + " && datum.school === 'eigene Schule' && !isValid(datum.pupils)"}, status_calc],
             "mark": {"type": "circle", "filled": False, "stroke": "@accent", "strokeWidth": 2, "size": 110, "opacity": 1},
             "encoding": {"longitude": LON, "latitude": LAT, "tooltip": tip_place}},
            {"transform": [{"filter": flt}], "mark": {"type": "text", "style": "place-halo", "dy": -11},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "name"}}},
            {"transform": [{"filter": flt}], "mark": {"type": "text", "style": "place-label", "dy": -11},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "name"}}},
            *([] if False else [{"transform": [{"filter": "datum.name === 'Gera'"}], "mark": {"type": "rule", "color": "@ink2", "strokeWidth": 2},
             "encoding": {"longitude": {"datum": lon0}, "latitude": {"datum": lat0}, "longitude2": {"datum": lon0 + dlon}, "latitude2": {"datum": lat0}}},
            {"transform": [{"filter": "datum.name === 'Gera'"}], "mark": {"type": "text", "style": "annotation", "dy": -7},
             "encoding": {"longitude": {"datum": lon0 + dlon / 2}, "latitude": {"datum": lat0}, "text": {"value": "5 km"}}}]),
        ],
    }


c1 = {
    "id": "c1",
    "dataset": "schulorte",
    "extra_datasets": ["schulwege", "orte_basis", "fluesse_basis"],
    "title": bi("Im Unterland schulten viele Orte nach auswärts, im Oberland hatten fast alle eine eigene Schule",
                "In the Unterland many places sent children elsewhere, in the Oberland nearly all had a school"),
    "caption": bi(
        f"Kreise: Orte mit eigener Schule, Größe nach Schulkindern (Ring: Zahl nicht genannt). Punkte: Orte ohne Schule, Linie zum Schulort, soweit dieser im Fürstentum liegt. {len(no_coord)} Orte ohne Koordinaten fehlen. Quelle: Ortskunde S. 418 bis 825.",
        f"Circles: places with a school of their own, sized by pupils (ring: number not given). Dots: places without a school, line to the school place where it lies in the principality. {len(no_coord)} places without coordinates are missing. Source: topography pp. 418 to 825."),
    "vegalite": {
        "hconcat": [
            panel(bi("Unterland (Landesteil Gera)", "Unterland (Gera district)"), [12.10, 50.885], 67000, 418, 420,
                  ["Gera", "Frankenthal", "Dorna", "Großaga", "Groitschen", "Roben", "Lusan"], False, (11.955, 50.795), (11.78, 12.45, 50.70, 51.07)),
            panel(bi("Oberland (Schleiz, Lobenstein-Ebersdorf)", "Oberland (Schleiz, Lobenstein-Ebersdorf)"), [11.815, 50.545], 39000, 418, 420,
                  ["Schleiz", "Lobenstein", "Hirschberg", "Hohenleuben", "Tanna", "Saalburg"], True, (11.985, 50.515), (11.30, 12.35, 50.28, 50.80)),
        ],
        "spacing": 8,
        "resolve": {"legend": {"color": "independent", "size": "independent"}},
    },
}

ratio_domain = ["Volksschule", "Höhere Schule"]
sorted_rows = sorted(sl_rows, key=lambda r: -r[7])
sort_list = [bi(r[0], r[1]) for r in sorted_rows]
land_keys = ("Volksschulen Gera, Land", "Volksschulen Schleiz, Land", "Volksschulen Lobenstein-Ebersdorf, Land")
land_lo, land_hi = min(ppt[k] for k in land_keys), max(ppt[k] for k in land_keys)
gym_lo, gym_hi = min(ppt["Gymnasium Gera"], ppt["Gymnasium Schleiz"]), max(ppt["Gymnasium Gera"], ppt["Gymnasium Schleiz"])
c2 = {
    "id": "c2",
    "dataset": "schulen_lehrer",
    "title": bi(f"Auf dem Land kamen {n(land_lo)} bis {n(land_hi)} Schüler auf einen Lehrer, an Gymnasien {n(gym_lo)} bis {n(gym_hi)}",
                f"In the country {e(land_lo)} to {e(land_hi)} pupils went to one teacher, at Gymnasien {e(gym_lo)} to {e(gym_hi)}"),
    "caption": bi(
        "Schüler je Lehrer an den Volksschulen (Ende 1868, nach Landesteil und Stadt oder Land) und an der Realschule und den Gymnasien in Gera und Schleiz (1868/69). Gestrichelt: Brückners Normalmaß von 50. Quelle: S. 299, 300.",
        "Pupils per teacher at the elementary schools (end of 1868, by district and town or country) and at the Realschule and the Gymnasien in Gera and Schleiz (1868/69). Dashed: Brückner’s norm of 50. Source: pp. 299, 300."),
    "vegalite": {
        "height": {"step": 30},
        "transform": [{"calculate": {"de": "datum.name_de", "en": "datum.name_en"}, "as": "label"}],
        "encoding": {"y": {"field": "label", "type": "nominal", "sort": sort_list,
                           "axis": {"title": None, "labelLimit": 560, "ticks": False, "domain": False}}},
        "layer": [
            {"mark": {"type": "bar", "height": 18},
             "encoding": {"x": {"field": "pupils_per_teacher", "type": "quantitative", "scale": {"domain": [0, 110]},
                                "axis": {"title": bi("Schüler je Lehrer", "Pupils per teacher"), "values": [0, 25, 50, 75, 100]}},
                          "color": {"field": "kind", "type": "nominal", "legend": None, "scale": {"domain": ratio_domain, "range": ["@accent", "@muted"]}},
                          "tooltip": [{"field": "label", "title": bi("Schule", "School")},
                                      {"field": "schools", "title": bi("Schulen", "Schools")},
                                      {"field": "teachers", "title": bi("Lehrer", "Teachers")},
                                      {"field": "pupils", "title": bi("Schüler", "Pupils"), "format": ",d"},
                                      {"field": "pupils_per_teacher", "title": bi("Schüler je Lehrer", "Pupils per teacher"), "format": ".1f"}]}},
            {"mark": {"type": "rule", "strokeDash": [4, 3], "color": "@ink2"},
             "encoding": {"x": {"datum": 50, "type": "quantitative"}, "y": None}},
            {"transform": [{"filter": "datum.name_de === 'Volksschulen Gera, Land'"}],
             "mark": {"type": "text", "align": "left", "baseline": "bottom", "dx": 4, "dy": -17, "style": "annotation"},
             "encoding": {"x": {"datum": 50, "type": "quantitative"}, "y": {"value": 0},
                          "text": {"value": bi("Normalmaß 50", "norm of 50")}}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "place-halo"},
             "encoding": {"x": {"field": "pupils_per_teacher", "type": "quantitative"}, "text": {"field": "pupils_per_teacher", "format": ".1f"}}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "place-label"},
             "encoding": {"x": {"field": "pupils_per_teacher", "type": "quantitative"}, "text": {"field": "pupils_per_teacher", "format": ".1f"}}},
        ],
    },
}

c3 = {
    "id": "c3",
    "dataset": "gehaelter",
    "title": bi("Schon die niedrigste Pfarrstelle zahlte mehr als das Doppelte des Mindestgehalts eines Landlehrers",
                "Even the lowest pastorate paid more than twice the minimum salary of a village teacher"),
    "caption": bi(
        f"Gehaltsklassen der {posts_total} Pfarrstellen (Zahl der Stellen) und gesetzliches Mindestgehalt der Lehrer, in Taler im Jahr. Lehrer: Spannweite je nach Ort, freie Wohnung zusätzlich. Heller Balken: nach oben offen. Quelle: S. 294, 297.",
        f"Salary classes of the {posts_total} pastorates (number of posts) and legal minimum pay of teachers, in thalers a year. Teachers: range by place, free housing in addition. Lighter bar: open at the top. Source: pp. 294, 297."),
    "vegalite": {
        "height": {"step": 34},
        "transform": [
            {"calculate": "isValid(datum.hi) ? datum.hi : 1100", "as": "hi_plot"},
            {"calculate": {"de": "isValid(datum.hi) ? format(datum.lo, ',d') + ' bis ' + format(datum.hi, ',d') + ' Taler' : 'über ' + format(datum.lo, ',d') + ' Taler'",
                           "en": "isValid(datum.hi) ? format(datum.lo, ',d') + ' to ' + format(datum.hi, ',d') + ' thalers' : 'over ' + format(datum.lo, ',d') + ' thalers'"}, "as": "range_label"},
            {"calculate": {"de": "datum.kind === 'Pfarrer' ? datum.group_de + ' ' + replace(datum.range_label, ' Taler', '') : datum.group_de",
                           "en": "datum.kind === 'Pfarrer' ? datum.group_en + ' ' + replace(datum.range_label, ' thalers', '') : datum.group_en"}, "as": "label"},
            {"calculate": {"de": "datum.kind === 'Pfarrer' ? datum.posts + ' Stellen' : datum.range_label",
                           "en": "datum.kind === 'Pfarrer' ? datum.posts + ' posts' : datum.range_label"}, "as": "value_label"},
        ],
        "encoding": {"y": {"field": "label", "type": "nominal", "sort": {"field": "order", "op": "min"},
                           "axis": {"title": None, "labelLimit": 420, "ticks": False, "domain": False}}},
        "layer": [
            {"mark": {"type": "bar", "height": 20, "cornerRadiusEnd": 0},
             "encoding": {"x": {"field": "lo", "type": "quantitative", "scale": {"domain": [0, 1350]},
                                "axis": {"title": bi("Taler im Jahr", "Thalers a year"), "values": [0, 200, 400, 600, 800, 1000], "format": ",d", "labelOverlap": False}},
                          "x2": {"field": "hi_plot"},
                          "color": {"field": "kind", "type": "nominal", "legend": None, "scale": {"domain": ["Pfarrer", "Lehrer"], "range": ["@accent3", "@accent"]}},
                          "opacity": {"condition": {"test": "!isValid(datum.hi)", "value": 0.5}, "value": 1},
                          "tooltip": [{"field": "label", "title": bi("Gruppe", "Group")},
                                      {"field": "range_label", "title": bi("Gehalt", "Pay")},
                                      {"field": "posts", "title": bi("Stellen", "Posts")}]}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"x": {"field": "hi_plot", "type": "quantitative"}, "text": {"field": "value_label"}}},
        ],
    },
}

# ---------------------------------------------------------------- texts
g, s, l = "Gera", "Schleiz", "Lobenstein-Ebersdorf"
pct = lambda lt: f"{region_stats[lt][1]} von {region_stats[lt][0]}"
summary = bi(
    f"Kirchlich gliederte sich das Fürstentum in {len(ds_eph['rows'])} Ephorien mit {eph_tot['parishes']} Parochien, {eph_tot['churches']} Kirchen und {eph_tot['clergy']} Geistlichen; hinzu kamen {vol_tot['schools']} Volksschulen mit {vol_tot['teachers']} Lehrern und {n(vol_tot['pupils'])} Schülern. {n_own} von {N} Orten hatten eine eigene Schule. Auf dem Land kamen {n(land_ppt)} Schüler auf einen Lehrer; die niedrigste Pfarrstelle zahlte {min_pastor}, der Landlehrer mindestens {min_teacher} Taler.",
    f"Ecclesiastically the principality was divided into {len(ds_eph['rows'])} ephories with {eph_tot['parishes']} parishes, {eph_tot['churches']} churches and {eph_tot['clergy']} clergy; in addition there were {vol_tot['schools']} elementary schools with {vol_tot['teachers']} teachers and {e(vol_tot['pupils'])} pupils. {n_own} of {N} places had a school of their own. In the country {e(land_ppt)} pupils went to one teacher; the lowest pastorate paid {min_pastor}, the village teacher at least {min_teacher} thalers.")

findings = [
    bi(f"Von den {region_stats[g][0]} Orten des Landesteils Gera hatten {region_stats[g][1]} eine eigene Schule ({n(share(g))} Prozent), von den {region_stats[s][0]} in Schleiz {region_stats[s][1]} ({n(share(s))} Prozent), von den {region_stats[l][0]} in Lobenstein-Ebersdorf {region_stats[l][1]} ({n(share(l))} Prozent).",
       f"Of the {region_stats[g][0]} places in the Gera district {region_stats[g][1]} had a school of their own ({e(share(g))} percent), of the {region_stats[s][0]} in Schleiz {region_stats[s][1]} ({e(share(s))} percent), of the {region_stats[l][0]} in Lobenstein-Ebersdorf {region_stats[l][1]} ({e(share(l))} percent)."),
    bi(f"Auf einen Lehrer kamen an den Landschulen im Durchschnitt {n(land_ppt)} Schüler, an der Stadtschule Gera {n(ppt['Volksschulen Gera, Stadt'])}, an den Gymnasien {n(ppt['Gymnasium Schleiz'])} bis {n(ppt['Gymnasium Gera'])}. Brückner nennt {n(NORM)} als Normalmaß.",
       f"At the village schools on average {e(land_ppt)} pupils went to one teacher, at the town school of Gera {e(ppt['Volksschulen Gera, Stadt'])}, at the Gymnasien {e(ppt['Gymnasium Schleiz'])} to {e(ppt['Gymnasium Gera'])}. Brückner gives {e(NORM)} as the norm."),
    bi(f"Das gesetzliche Mindestgehalt der Volksschullehrer lag zwischen {min_teacher} und {teacher_max} Talern, die niedrigste Pfarrstelle zahlte {min_pastor}. {posts_from_800} von {posts_total} Pfarrstellen zahlten {800} Taler und mehr.",
       f"The legal minimum pay of elementary teachers lay between {min_teacher} and {teacher_max} thalers, the lowest pastorate paid {min_pastor}. {posts_from_800} of {posts_total} pastorates paid {800} thalers or more."),
]

method = bi(
    f"Schulorte und Schulkinder stammen aus den {N} Ortsartikeln der Ortskunde (S. 418 bis 825). Ein Ort zählt als Schulort, wenn der Artikel eine eigene Schule nennt, sonst als Ort mit Schule im Nachbarort; der Artikel von Kleinfalke nennt eine eigene Schule seit 1810 und wurde gegenüber der früheren Einzelauswertung korrigiert. Der Schulort der {n_neighbour} Orte ohne Schule wurde aus dem Artikel gelesen; Koordinaten stammen von GeoNames. Linien zeichnen nur Schulorte im Fürstentum ({len(links_drawn)} von {len(links)} Verbindungen); {len(links_outside)} führen in Nachbarstaaten, {len(links) - len(links_drawn) - len(links_outside)} scheitern an fehlenden Koordinaten. Bieblach darf nach Tinz oder Gera zur Schule gehen und erscheint mit beiden Linien. Die Schüler und Lehrer der Volksschulen stehen in der Tabelle auf S. 299 (Ende 1868), die der höheren Schulen auf S. 299 und 300. Schüler je Lehrer ist berechnet; an den Gymnasien zählen Haupt- und Hilfslehrer, an der Realschule die 17 und 2 eigenen Lehrer. Gehaltsklassen der Pfarrstellen stehen auf S. 294, das gesetzliche Mindestgehalt der Lehrer auf S. 297. Die Zahl der Parochien, Kirchen und Geistlichen je Ephorie steht als weitere Tabelle zum Herunterladen bereit. Die Gemeindehaushalte aus den Ortsartikeln sind in dieser Auswertung nicht enthalten.",
    f"School places and pupils come from the {N} place articles of the topography (pp. 418 to 825). A place counts as a school place if the article names a school of its own, otherwise as a place with its school in a neighbouring place; the article on Kleinfalke names a school of its own since 1810 and was corrected against the earlier single analysis. The school place of the {n_neighbour} places without a school was read from the article; coordinates come from GeoNames. Lines are drawn only for school places in the principality ({len(links_drawn)} of {len(links)} connections); {len(links_outside)} lead into neighbouring states, {len(links) - len(links_drawn) - len(links_outside)} fail for lack of coordinates. Bieblach may go to school in Tinz or Gera and appears with both lines. Pupils and teachers of the elementary schools are in the table on p. 299 (end of 1868), those of the secondary schools on pp. 299 and 300. Pupils per teacher is calculated; at the Gymnasien main and assistant teachers are counted, at the Realschule the 17 and 2 own teachers. The salary classes of the pastorates are on p. 294, the legal minimum pay of teachers on p. 297. The number of parishes, churches and clergy per ephory is a further table for download. The municipal budgets from the place articles are not part of this analysis.")

caveats = [
    bi(f"Die Schulkinder gelten für verschiedene Jahre, bei Schulorten einschließlich der eingeschulten Kinder anderer Orte. Die Größe der Kreise ist deshalb nur ein Näherungswert. Für {missing_pupils_de} nennt der Artikel keine einzelne Zahl; sie sind als Ring gezeichnet. Die Einwohner sind die des Ortsartikels.",
       f"The pupils refer to different years and, for school places, include the children of other places. The size of the circles is therefore only approximate. For {missing_pupils_en} the article gives no single figure; they are drawn as a ring. Inhabitants are those of the place article."),
    bi("Die Lehrerzahl der Stadt Gera enthält die Lehrerinnen. An den Gymnasien zählen Haupt- und Hilfslehrer, die Hilfslehrer können Teilzeitkräfte sein; an der Realschule sind die vier hilfsweise herangezogenen Lehrer nicht gezählt. Volksschulen und höhere Schulen sind deshalb nur grob vergleichbar.",
       "The number of teachers in the town of Gera includes women teachers. At the Gymnasien main and assistant teachers are counted; assistants may be part-time. At the Realschule the four teachers drawn in from elsewhere are not counted. Elementary and secondary schools are therefore only roughly comparable."),
    bi(f"Die Gehaltsklassen nennt Brückner ohne Jahr und ohne Angabe, ob Naturalien eingerechnet sind. Die Pfarrstellen schließen {deacons_total} Diakonate und {ephors_total} Ephorenstellen ein. Bei den Lehrern handelt es sich um das gesetzliche Mindestgehalt ohne Alterszulagen, in dem Bezüge aus Stiftungskassen eingerechnet sind.",
       f"Brückner gives the salary classes without a year and without saying whether payments in kind are included. The pastorates include {deacons_total} deaconates and {ephors_total} ephor posts. For teachers it is the legal minimum without seniority supplements, in which payments from foundation funds are counted."),
]

transcription = [
    {"page": "299", "block": "b3", "cell": "r15c8", "transcribed": "1,10", "facsimile": "1,40", "checked_facsimile": True,
     "note": "Druckfehler im Original (117 : 106 = 1,10); die Transkription hat den Wert stillschweigend berichtigt. Die Zahl wird hier nicht verwendet."},
    {"page": "299", "block": "b3", "cell": "r16c6", "transcribed": "7426", "facsimile": "7426", "checked_facsimile": True,
     "note": "Druckfehler im Original: die Knaben der Landesteile ergeben 7526. Die Transkription entspricht dem Druck; der Wert wird nicht verwendet."},
    {"page": "299", "block": "b3", "cell": "r16c7", "transcribed": "7613", "facsimile": "7613", "checked_facsimile": True,
     "note": "Druckfehler im Original: die Mädchen der Landesteile ergeben 6713 (Summe 14239 stimmt). Die Transkription entspricht dem Druck; der Wert wird nicht verwendet."},
]

obj = {
    "id": FID,
    "title": bi("Kirchen und Schulen", "Churches and schools"),
    "category": "education",
    "section": "t1-4-6",
    "merges": ["kirche-ephorien-pfarreien-besoldung-1868", "schule-volksschulen-schueler-lehrer-1863-1868", "schule-hoehere-anstalten-schueler-lehrer-1868", "orte-schulen-gemeindehaushalt"],
    "sources": [ref(294, "b2"), ref(294, "b6"), ref(294, "b7"), ref(297, "b3"), ref(299, "b3"), ref(299, "b4"), ref(299, "b5"), ref(300, "b1"), ref(300, "b2"), ref(300, "b4"), ref(300, "b6"),
                ref(418, "b3")],
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "datasets": [ds_places, ds_links, base_places, base_rivers, ds_sl, ds_pay, ds_eph],
    "charts": [c1, c2, c3],
    "transcription_issues": transcription,
    "keywords": {
        "de": ["Schule", "Schulort", "Volksschule", "Gymnasium", "Realschule", "Schüler", "Lehrer", "Lehrergehalt", "Kirche", "Ephorie", "Parochie", "Pfarrer", "Pfarrbesoldung"],
        "en": ["school", "school place", "elementary school", "Gymnasium", "Realschule", "pupils", "teachers", "teachers’ pay", "church", "ephory", "parish", "pastor", "pastors’ pay"],
    },
    "related": ["armenwesen-stiftungen", "siedlung-wohnen", "verfassung-verwaltung", "staatsfinanzen"],
    "generated_by": "Claude Sonnet 5.5 (Agent F7), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    print("regions", region_stats, [round(share(x), 1) for x in region_stats])
    print("big share", big_share, len(big), "small own", small_own, len(small), "median pupils", pupils_median)
    print("no coord", no_coord)
    print("links", len(links), len(links_drawn), len(links_outside))
    print("ppt", ppt, land_ppt, avg_ppt)
    print("posts", posts_total, posts_below_600, posts_from_800)
    probs = check_limits(obj)
    print("limit problems:", probs)
    print(write_feature(obj))
    ok = validate(FID)
    print("OK" if ok else "FAIL")
