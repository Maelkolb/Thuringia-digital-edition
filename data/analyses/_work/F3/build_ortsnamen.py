import sys, collections, statistics
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F3")
from common import *
from geo import Panel, place_labels

MERGES = [
    "ortsnamen-sorbische-wurzeln",
    "orte-erste-erwaehnungen-namensformen",
    "kultur-ortssiegel-motive",
    "orte-wuestungen-ortskunde",
]
coords = coordinate_lookup()
base_places, base_rivers = base_layers()

# ------------------------------------------------------------------ deserted villages
wuest = dataset("orte-wuestungen-ortskunde", "wuestungen")
wd = dicts(wuest)
near = collections.OrderedDict()
for r in wd:
    near.setdefault(r["near"], []).append(r)
arch_near = {r["near"]: r for r in dicts(dataset("orte-wuestungen-ortskunde", "wuest_near"))}

# two windows at the same scale
SCALE = 60000
PL = Panel((11.90, 12.20), (50.83, 50.985), SCALE)
PR = Panel((11.55, 11.93), (50.395, 50.665), SCALE)
print("panel sizes", PL.w, PL.h, PR.w, PR.h)


def panel_of(lon, lat):
    return "L" if lat > 50.75 else "R"


items = {"L": [], "R": []}
rows = []
for name, ws in near.items():
    lon, lat, lt = coords[name]
    assert abs(lon - arch_near[name]["lon"]) < 1e-6 and abs(lat - arch_near[name]["lat"]) < 1e-6
    p = panel_of(lon, lat)
    # long names wrap after two names
    names = [w["name"] for w in ws]
    lines = []
    cur = ""
    for nm in names:
        add = nm if not cur else cur + (" " if cur.endswith(":") else ", ") + nm
        if len(add) > 26 and cur and not cur.endswith(":"):
            lines.append(cur + ",")
            cur = nm
        else:
            cur = add
    lines.append(cur)
    items[p].append({"key": name, "lon": lon, "lat": lat, "lines": lines, "n": len(ws)})
    rows.append((name, ws[0]["landestheil"], len(ws), "; ".join(names), lon, lat, "\n".join(lines), p))


def radius(it):
    return {1: 6.5, 2: 8, 3: 9.5, 4: 11}[it["n"]]


lab = {}
lab.update(place_labels(PL, items["L"], radius_of=radius))
lab.update(place_labels(PR, items["R"], radius_of=radius))
bad = {k: v for k, v in lab.items() if v[3] > 0}
print("labels with overlaps or off-frame:", bad)

wp_rows = []
for name, lt, n, nm, lon, lat, text, p in rows:
    al, dx, dy, _ = lab[name]
    wp_rows.append([name, lt, n, nm, lon, lat, text, al, round(dx, 1), round(dy, 1), p])
wuest_places = make_dataset(
    "wuest_places",
    "Wüstungen je Bezugsort mit Lage",
    "Deserted villages per reference place with position",
    [
        col("near", "Bezugsort", "Reference place", "string", None, True, "das Dorf, bei dem Brückners Artikel die Wüstung verortet"),
        col("landestheil", "Landesteil", "District", "string", None, False),
        col("n_wuestungen", "Zahl der Wüstungen", "Number of deserted villages", "integer", "Wüstungen", True),
        col("names", "Wüstungen", "Deserted villages", "string", None, True),
        col("lon", "Länge", "Longitude", "number", "° O", True, "GeoNames, über den Namen des Bezugsorts"),
        col("lat", "Breite", "Latitude", "number", "° N", True, "GeoNames"),
        col("label", "Beschriftung", "Label", "string", None, True),
        col("label_align", "Ausrichtung der Beschriftung", "Label alignment", "string", None, True),
        col("label_dx", "Versatz x", "Offset x", "number", "px", True),
        col("label_dy", "Versatz y", "Offset y", "number", "px", True),
        col("panel", "Kartenausschnitt", "Map window", "string", None, True),
    ],
    wp_rows,
    wuest["source_refs"],
)
by_district = collections.Counter(r["landestheil"] for r in wd)
n_wuest = len(wd)
top_near = max(near.items(), key=lambda kv: len(kv[1]))
print("wuestungen", n_wuest, by_district, "top", top_near[0], len(top_near[1]))

# ------------------------------------------------------------------ first mentions
mentions = dataset("orte-erste-erwaehnungen-namensformen", "mentions")
md = dicts(mentions)
dated = [r for r in md if r["first_year"]]
n_communes = len(md)
districts = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
n_by_district = {d: sum(1 for r in md if r["landestheil"] == d) for d in districts}
median = {d: statistics.median(r["first_year"] for r in dated if r["landestheil"] == d) for d in districts}
print("communes", n_communes, n_by_district, "dated", len(dated), "median", median)
by_year = collections.Counter(r["first_year"] for r in dated)
spike_years = [1121, 1325, 1333, 1364, 1533]
spike_total = sum(by_year[y] for y in spike_years)
oldest = min(dated, key=lambda r: r["first_year"])
print("spikes", [(y, by_year[y]) for y in spike_years], spike_total, "oldest", oldest["name"], oldest["first_year"])
century14 = sum(1 for r in dated if 1300 <= r["first_year"] < 1400)
print("14th century", century14, century14 / len(dated))
y1364_districts = collections.Counter(r["landestheil"] for r in dated if r["first_year"] == 1364)
print("1364 by district", y1364_districts)
before1200 = {d: sum(1 for r in dated if r["landestheil"] == d and r["first_year"] < 1200) for d in districts}
print("before 1200", before1200)

# ------------------------------------------------------------------ Sorbian roots
groups = dataset("ortsnamen-sorbische-wurzeln", "groups")
gd = dicts(groups)
for r in gd:
    assert r["names"] == len(r["list"].split(", ")), r
add_columns(
    groups,
    [col("examples", "Beispiele (die ersten drei Namen)", "Examples (first three names)", "string", None, True)],
    lambda d: [", ".join(d["list"].split(", ")[:3])],
)
gd = dicts(groups)
total_names = sum(r["names"] for r in gd)
landscape = sum(r["names"] for r in gd if r["kind_de"] == "Landschaftsmerkmal")
roots_total = sum(r["roots"] for r in gd)
plants = next(r["names"] for r in gd if r["key"] == "pflanze")
print("sorbian", total_names, landscape, roots_total, plants)

# ------------------------------------------------------------------ seals
seals = dataset("kultur-ortssiegel-motive", "seals")
sd = dicts(seals)
n_seals = len(sd)
trees_seals = sum(1 for r in sd if r["class_key"] in ("baum", "baeume", "baumtier"))
print("seals", n_seals, trees_seals)

# ------------------------------------------------------------------ specs
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}
DISTRICT = {
    "field": "landestheil",
    "type": "nominal",
    "scale": {"domain": districts, "range": ["@accent", "@accent2", "@accent3"]},
    "legend": {"title": None, "orient": "top", "direction": "horizontal"},
}
SIZE = {
    "field": "n_wuestungen",
    "type": "quantitative",
    "scale": {"type": "sqrt", "domain": [0, 4], "range": [0, 300]},
    "legend": {
        "title": {"de": "Wüstungen am Bezugsort", "en": "Deserted villages at the reference place"},
        "titleLimit": 300,
        "values": [1, 2, 4],
        "orient": "top",
        "direction": "horizontal",
        "symbolFillColor": "@muted",
        "symbolStrokeColor": "@paper",
    },
}


def panel_spec(panel, key, title):
    inside = panel.inside_expr()
    inside_river = panel.inside_expr(8)
    layers = [
        {
            "data": {"name": "fluesse_basis"},
            "transform": [{"filter": inside_river}],
            "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2, "interpolate": "monotone"},
            "encoding": {"longitude": LON, "latitude": LAT, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}},
        },
        {
            "data": {"name": "orte_basis"},
            "transform": [{"filter": inside}],
            "mark": {"type": "circle", "size": 10, "color": "@land", "opacity": 1},
            "encoding": {"longitude": LON, "latitude": LAT},
        },
        {
            "transform": [{"filter": f"datum.panel == '{key}'"}],
            "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.9},
            "encoding": {
                "longitude": LON,
                "latitude": LAT,
                "size": SIZE,
                "color": DISTRICT,
                "tooltip": [
                    tip("names", "Wüstungen", "Deserted villages"),
                    tip("near", "Bezugsort", "Reference place"),
                    tip("landestheil", "Landesteil", "District"),
                ],
            },
        },
    ]
    combos = collections.OrderedDict()
    for r in wp_rows:
        if r[10] != key:
            continue
        combos.setdefault((r[7], r[8], r[9]), []).append(r[0])
    for (align, dx, dy), names in combos.items():
        flt = f"indexof({names!r}, datum.near) >= 0"
        for style in ("place-halo", "place-label"):
            layers.append(
                {
                    "transform": [{"filter": flt}],
                    "mark": {"type": "text", "style": style, "align": align, "dx": dx, "dy": dy, "lineBreak": "\n", "fontWeight": 400, "fontSize": 10.5},
                    "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "label"}},
                }
            )
    return {
        "width": panel.w,
        "height": panel.h,
        "title": {"text": title, "anchor": "start", "fontSize": 12, "fontWeight": 600, "offset": 6},
        "view": {"stroke": "@context", "strokeWidth": 1},
        "projection": panel.projection(),
        "layer": layers,
    }


c1 = {
    "spacing": 14,
    "hconcat": [
        panel_spec(PL, "L", bi("Landesteil Gera", "District of Gera")),
        panel_spec(PR, "R", bi("Landesteile Schleiz und Lobenstein-Ebersdorf", "Districts of Schleiz and Lobenstein-Ebersdorf")),
    ],
    "resolve": {"legend": {"color": "shared", "size": "shared"}},
}

X_SCALE = {"domain": [1060, 1660], "nice": False}


def mention_panel(district, last):
    n_dated = sum(1 for r in dated if r["landestheil"] == district)
    med = median[district]
    flt = f"datum.landestheil == '{district}' && isValid(datum.first_year)"
    return {
        "width": 640,
        "height": 112,
        "title": {
            "text": bi(f"Landesteil {district}: {n_dated} Orte mit Jahr, Median {int(med)}", f"District of {district}: {n_dated} places with a year, median {int(med)}"),
            "anchor": "start",
            "fontSize": 12,
            "fontWeight": 600,
            "offset": 6,
        },
        "layer": [
            {
                "transform": [{"filter": flt}, {"window": [{"op": "row_number", "as": "stack"}], "groupby": ["first_year"], "sort": [{"field": "name"}]}],
                "mark": {"type": "square", "size": 16, "opacity": 0.9},
                "encoding": {
                    "x": {
                        "field": "first_year",
                        "type": "quantitative",
                        "scale": X_SCALE,
                        "axis": {"title": None, "format": "d", "values": [1100, 1200, 1300, 1400, 1500, 1600], "grid": True, "labels": last, "ticks": last, "domain": last},
                    },
                    "y": {"field": "stack", "type": "quantitative", "scale": {"domain": [0, 17]}, "axis": None},
                    "color": {"value": "@accent"},
                    "tooltip": [
                        tip("name", "Ort", "Place"),
                        tip("first_year", "Erste Erwähnung", "First mention", "d"),
                        tip("landestheil", "Landesteil", "District"),
                        tip("forms", "Namensformen", "Name forms"),
                    ],
                },
            },
            {
                "transform": [{"filter": flt}, {"aggregate": [{"op": "median", "field": "first_year", "as": "med"}]}],
                "mark": {"type": "rule", "strokeDash": [4, 3], "strokeWidth": 1.5, "color": "@accent2"},
                "encoding": {"x": {"field": "med", "type": "quantitative", "scale": X_SCALE}},
            },
            {
                "transform": [{"filter": flt}, {"aggregate": [{"op": "median", "field": "first_year", "as": "med"}]}],
                "mark": {"type": "text", "style": "label", "align": "right", "dx": -6, "baseline": "top", "dy": 2},
                "encoding": {
                    "x": {"field": "med", "type": "quantitative", "scale": X_SCALE},
                    "y": {"value": 0},
                    "text": {"field": "med", "type": "quantitative", "format": "d"},
                    "color": {"value": "@accent2"},
                },
            },
            {
                "transform": [{"filter": flt}, {"aggregate": [{"op": "count", "as": "n"}], "groupby": ["first_year"]}, {"filter": "datum.n >= 6"}],
                "mark": {"type": "text", "style": "annotation", "align": "left", "dx": 6, "dy": 2},
                "encoding": {
                    "x": {"field": "first_year", "type": "quantitative", "scale": X_SCALE},
                    "y": {"field": "n", "type": "quantitative", "scale": {"domain": [0, 17]}, "axis": None},
                    "text": {"field": "n", "type": "quantitative"},
                },
            },
        ],
    }


c2 = {"spacing": 14, "vconcat": [mention_panel(d, d == districts[-1]) for d in districts]}

c3 = {
    "height": {"step": 25},
    "encoding": {
        "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": {"field": "names", "op": "max", "order": "descending"}, "axis": {"title": None, "labelLimit": 460, "labelFontSize": 12}},
        "x": {"field": "names", "type": "quantitative", "scale": {"domain": [0, 27], "nice": False}, "axis": None},
    },
    "layer": [
        {
            "mark": {"type": "bar", "height": {"band": 0.62}},
            "encoding": {
                "color": {"condition": {"test": "datum.kind_de == 'Landschaftsmerkmal'", "value": "@accent"}, "value": "@context"},
                "tooltip": [
                    tip({"de": "group_de", "en": "group_en"}, "Bedeutung der Wurzel", "Meaning of the root"),
                    tip("names", "Ortsnamen", "Place names"),
                    tip("roots", "Wurzeln", "Roots"),
                    tip("list", "Namen", "Names"),
                ],
            },
        },
        {
            "mark": {"type": "text", "style": "label", "align": "left", "dx": 6},
            "encoding": {"text": {"field": "names"}},
        },
        {
            "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 24},
            "encoding": {"text": {"field": "examples"}},
        },
    ],
}

# ------------------------------------------------------------------ texts
gera, schl, lob = by_district["Gera"], by_district["Schleiz"], by_district["Lobenstein-Ebersdorf"]
per10 = {d: by_district[d] / n_by_district[d] * 10 for d in districts}
summary_de = (
    f"Für {n_de(len(dated))} von {n_de(n_communes)} Gemeinden nennt Brückner die erste urkundliche Erwähnung; Orte im Landesteil Gera sind früher belegt. "
    f"Er beschreibt {n_wuest} Wüstungen, {gera} davon im Landesteil Gera, und nennt für {n_de(total_names)} Ortsnamen {roots_total} sorbische Wurzeln. "
    f"Die Siegel von {n_seals} Dörfern zeigen in {trees_seals} Fällen Bäume."
)
summary_en = (
    f"For {n_en(len(dated))} of {n_en(n_communes)} municipalities Brückner gives the first documentary mention; places in the district of Gera are attested earlier. "
    f"He describes {n_wuest} deserted villages, {gera} of them in the district of Gera, and names {roots_total} Sorbian roots for {n_en(total_names)} place names. "
    f"The seals of {n_seals} villages show trees in {trees_seals} cases."
)
print("summary", words(summary_de), words(summary_en))
no_year = sum(1 for r in wd if r["earliest_year"] is None)
f1_de = (
    f"Je 10 Gemeinden kommen im Landesteil Gera {n_de(per10['Gera'], 1)} Wüstungen vor, in Schleiz {n_de(per10['Schleiz'], 1)} und in Lobenstein-Ebersdorf {n_de(per10['Lobenstein-Ebersdorf'], 1)}. "
    f"Bei {top_near[0]} werden die meisten verortet ({len(top_near[1])}); {no_year} Wüstungen haben keine Jahresangabe."
)
f1_en = (
    f"Per 10 municipalities there are {n_en(per10['Gera'], 1)} deserted villages in the district of Gera, {n_en(per10['Schleiz'], 1)} in Schleiz and {n_en(per10['Lobenstein-Ebersdorf'], 1)} in Lobenstein-Ebersdorf. "
    f"Most are placed near {top_near[0]} ({len(top_near[1])}); {no_year} have no year."
)
f2_de = (
    f"Die älteste Erwähnung hat {oldest['name']} ({oldest['first_year']}). Fünf Jahre (1121, 1325, 1333, 1364, 1533) stehen für {spike_total} der {len(dated)} Orte; sie spiegeln eher einzelne Urkunden als Gründungszeiten. "
    f"Allein 1364 nennt {by_year[1364]} Orte, alle im Landesteil Gera."
)
f2_en = (
    f"{oldest['name']} has the oldest mention ({oldest['first_year']}). Five years (1121, 1325, 1333, 1364, 1533) account for {spike_total} of the {len(dated)} places, reflecting single documents rather than founding dates. "
    f"1364 names {by_year[1364]} places, all in Gera district."
)
assert set(y1364_districts) == {"Gera"}
f3_de = (
    f"Brückner referiert {roots_total} slawische Wurzeln für {n_de(total_names)} Namen. {n_de(landscape)} beschreiben Landschaftsmerkmale, {plants} Pflanzen, je einer ein Tier (Kattenstein) und die Kirche (Köstritz). "
    f"Gera leitet er von gora (Berg) ab."
)
f3_en = (
    f"Brückner reports {roots_total} Slavic roots for {n_en(total_names)} names. {n_en(landscape)} describe landscape features, {plants} plants, one an animal (Kattenstein), one the church (Köstritz). "
    f"Gera he derives from gora (mountain)."
)
title_c1 = bi(
    f"Von {n_wuest} Wüstungen liegen {gera} im Landesteil Gera, {schl} in Schleiz und nur {lob} in Lobenstein-Ebersdorf",
    f"The district of Gera has {gera} of {n_wuest} deserted villages, Schleiz {schl}, Lobenstein-Ebersdorf only {lob}",
)
title_c2 = bi(
    f"Orte im Landesteil Gera sind früher belegt (Median {median['Gera']}) als in Schleiz ({int(median['Schleiz'])}) und Lobenstein-Ebersdorf ({median['Lobenstein-Ebersdorf']})",
    f"Places in Gera district are attested earlier (median {median['Gera']}) than in Schleiz ({int(median['Schleiz'])}) or Lobenstein-Ebersdorf ({median['Lobenstein-Ebersdorf']})",
)
title_c3 = bi(
    f"{landscape} von {total_names} gedeuteten sorbischen Ortsnamen beschreiben Landschaftsmerkmale wie Bodenform, Wald und Wasser",
    f"{landscape} of {total_names} interpreted Sorbian place names describe landscape features such as landform, forest and water",
)
caption_c1 = bi(
    f"Wüstungen aus Brückners Ortsartikeln, eingezeichnet beim Dorf, bei dem er sie verortet (Lage nur ungefähr); Größe: Zahl der Wüstungen dort. Zwei Ausschnitte im gleichen Maßstab: links Landesteil Gera, rechts Schleiz und Lobenstein-Ebersdorf. S. 419–786.",
    f"Deserted villages from Brückner’s place articles, drawn at the village near which he locates them (position approximate); size: number of deserted villages there. Two windows at the same scale: left district of Gera, right Schleiz and Lobenstein-Ebersdorf. Pp. 419–786.",
)
caption_c2 = bi(
    f"Jedes Quadrat ist eine Gemeinde, gestapelt nach dem Jahr der ersten urkundlichen Erwähnung laut Ortsartikel ({len(dated)} von {n_communes} Gemeinden). Die Zahl neben einem Stapel nennt die Orte dieses Jahres; gestrichelt: Median je Landesteil. S. 418–825.",
    f"Each square is a municipality, stacked by the year of first documentary mention in its article ({len(dated)} of {n_communes} municipalities). The number beside a stack gives the places of that year; dashed: median per district. Pp. 418–825.",
)
caption_c3 = bi(
    f"Brückners Übersicht sorbischer Wortwurzeln und der davon abgeleiteten Ortsnamen, nach Bedeutung der Wurzel gruppiert (Gruppen redaktionell); blau: Landschaftsmerkmale. Die Zeile nennt die ersten Beispiele. S. 121.",
    f"Brückner’s overview of Sorbian word roots and the place names derived from them, grouped by the meaning of the root (groups editorial); blue: landscape features. The line gives the first examples. P. 121.",
)
method_de = (
    "Die Wüstungen sind alle Einträge des Typs Wüstung in Brückners Ortskunde (34). Jede ist beim Dorf eingezeichnet, bei dem der Artikel sie verortet (gedruckte Lageangabe); die Koordinaten sind die des Bezugsorts aus der Kartengrundlage (GeoNames). "
    "Das Jahr der ersten Erwähnung ist das früheste Jahr der urkundlichen Nennung im Ortsartikel; fehlt eine ausdrückliche Angabe, gilt die früheste datierte Namensform bis 1700. "
    "Die Tabelle der sorbischen Wurzeln (S. 121) wurde Zeile für Zeile übernommen, jeder Ortsname einzeln erfasst und die gedruckte Bedeutung acht Sachgruppen zugeordnet; gezählt werden verschiedene Ortsnamen. "
    "Die Siegelbilder der Dörfer (S. 124 f.) stehen als Tabelle bei, in acht Motivklassen geordnet; die sechs Stadtwappen sind nicht gezählt. Eine eigene Grafik gibt es dafür nicht."
)
method_en = (
    "The deserted villages are all entries of the type Wüstung in Brückner’s topography (34). Each is drawn at the village near which the article locates it (printed location statement); the coordinates are those of the reference place from the base map (GeoNames). "
    "The year of first mention is the earliest year of documentary mention in the place article; where none is stated, the earliest dated name form up to 1700 applies. "
    "The table of Sorbian roots (p. 121) was taken over row by row, each place name recorded separately and the printed meaning assigned to eight subject groups; distinct place names are counted. "
    "The seal images of the villages (pp. 124 f.) are attached as a table, ordered in eight classes of motif; the six town arms are not counted. There is no chart of their own."
)
print("method", words(method_de), words(method_en))
caveats = [
    bi(
        "Die Zahl der Wüstungen hängt davon ab, was Brückner in einem eigenen Absatz behandelt; sie ist ein Mindestwert. Nicht alle Einträge sind untergegangene Dörfer (Platte: Kupferhammer, Alte Klause: Kapelle, Wüstenhain: Wald, Wüstendittersdorf: bestehende Höfe). Die Karte zeigt die Bezugsorte, nicht die Lage der Wüstungen.",
        "The number of deserted villages depends on what Brückner treats in a paragraph of its own; it is a minimum. Not all entries are lost villages (Platte: copper hammer, Alte Klause: chapel, Wüstenhain: woodland, Wüstendittersdorf: farms that still exist). The map shows reference places, not the position of the deserted villages.",
    ),
    bi(
        "Das Jahr der ersten Erwähnung ist das früheste vom Verfasser genannte, nicht notwendig das früheste überlieferte. Die Häufung auf wenige Jahre (1364, 1533) deutet auf einzelne Urkunden und Verzeichnisse hin und nicht auf die Gründungszeit; für 21 Gemeinden nennt der Artikel kein Jahr.",
        "The year of first mention is the earliest one the author names, not necessarily the earliest transmitted. The clustering on a few years (1364, 1533) points to single documents and registers rather than the time of founding; for 21 municipalities the article gives no year.",
    ),
    bi(
        "Die sorbischen Deutungen referiert Brückner nur »in historischer Hinsicht«; er hält eine sichere Etymologie ohne die ältesten urkundlichen Formen für unmöglich. Vieles ist nach heutiger Kenntnis unsicher oder Volksetymologie. Die Tabelle ist eine Auswahl: Nach S. 119 hat etwa die Hälfte der Ortsnamen sorbischen Laut.",
        "Brückner reports the Sorbian interpretations only “from a historical point of view”; he holds a secure etymology impossible without the oldest documentary forms. Much is uncertain or folk etymology by present knowledge. The table is a selection: according to p. 119 about half of the place names have a Sorbian sound.",
    ),
    bi(
        "Die Siegelliste ist Brückners Auswahl und nennt keine Zahl der Orte ohne Bild; die Einteilung in Motivklassen stammt vom Bearbeiter. Brückner hält acht Bilder (Kränze, Anker, Sonne) für neuere Erfindungen ohne historischen Wert.",
        "The list of seals is Brückner’s selection and gives no number of places without an image; the classes of motif are the editor’s. Brückner regards eight images (wreaths, anchor, sun) as recent inventions without historical value.",
    ),
]
src = union_sources("ortsnamen-sorbische-wurzeln", "kultur-ortssiegel-motive") + [dict(r) for r in wuest["source_refs"]]
feature = {
    "id": "ortsnamen",
    "title": bi("Ortsnamen, erste Erwähnungen und Wüstungen", "Place names, first mentions and deserted villages"),
    "category": "places",
    "section": "t2",
    "merges": MERGES,
    "sources": src,
    "summary": bi(summary_de, summary_en),
    "findings": [bi(f1_de, f1_en), bi(f2_de, f2_en), bi(f3_de, f3_en)],
    "method": bi(method_de, method_en),
    "caveats": caveats,
    "datasets": [wuest_places, mentions, groups, wuest, seals, base_places, base_rivers],
    "charts": [
        {"id": "c1", "dataset": "wuest_places", "extra_datasets": ["orte_basis", "fluesse_basis"], "title": title_c1, "caption": caption_c1, "vegalite": c1},
        {"id": "c2", "dataset": "mentions", "title": title_c2, "caption": caption_c2, "vegalite": c2},
        {"id": "c3", "dataset": "groups", "title": title_c3, "caption": caption_c3, "vegalite": c3},
    ],
    "keywords": {
        "de": ["Ortsnamen", "Wüstungen", "erste Erwähnung", "Urkunden", "sorbisch", "slawisch", "Siegel", "Ortskunde", "Gera", "Tanna", "Namensformen"],
        "en": ["place names", "deserted villages", "first mention", "charters", "Sorbian", "Slavic", "seals", "topography", "Gera", "Tanna", "name forms"],
    },
    "related": ["siedlung-wohnen", "sagen-brauch", "landesgeschichte", "dorfleben"],
    "generated_by": GENERATED_BY.format(k=len(MERGES)),
    "date": DATE,
}
ti = union_issues(*MERGES)
if ti:
    feature["transcription_issues"] = ti
print(check_lengths(feature))
print(write_feature(feature))
