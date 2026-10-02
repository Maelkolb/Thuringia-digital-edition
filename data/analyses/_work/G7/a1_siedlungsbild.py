"""G7 analysis 1: settlement pattern 1867 (map, size classes, persons per house).

Reads the six gazetteer files, builds one row per political Gemeinde (173 places,
the number Brueckner gives on p. 98) and writes data/analyses/orte-siedlungsbild-1867.json.
"""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *

ents = load_entries()
C = load_coords()
by_id = {uid(e): e for e in ents}
U = gemeinden(ents)

# Goeritz / Neundorf: the entries store the figure of the Ort alone, the article also
# gives the figure of the whole Gemeinde (with Lehesten / Hornsgruen ...). Brueckner's
# statistical table (p. 98) counts the Gemeinde -> use it (both numbers occur in the text).
OVERRIDE = {"goeritz": {"inhabitants": 607, "houses": 89},
            "neundorf-lobenstein": {"inhabitants": 716}}

rows = []
for e in sorted(U, key=lambda e: (LT_ORDER.index(e["landestheil"]), int(e["start"]["page"]), int(e["start"]["block"][1:]))):
    inh, hou = e["inhabitants"], e["houses"]
    if e["id"] in OVERRIDE:
        inh = OVERRIDE[e["id"]].get("inhabitants", inh)
        hou = OVERRIDE[e["id"]].get("houses", hou)
    lon, lat, gn = coord(e, C)
    so, sc = size_class(inh)
    pc = place_class(e)
    rows.append([uid(e), e["name"], e["landestheil"], e["type"], pc, PLACE_CLASS_EN[pc],
                 "reußischer Anteil" if e["id"] in PARTIAL else "ganze Gemeinde",
                 inh, hou, round(inh / hou, 2), so, sc,
                 lon, lat, gn, e["start"]["page"], e["start"]["block"]])

cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("type", "Ortsart (Gazetteer)", "Place type (gazetteer)", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True, note="Stadt / Marktflecken / Dorf (Weiler und Kammergut mit eigener Gemeinde zu Dorf)"),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("scope", "Geltungsbereich der Zahlen", "Scope of the figures", "string", note="zweiherrische Orte: nur der reußische Anteil"),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("houses", "Häuser", "Houses", "integer", "Häuser", note="meist bewohnte Privathäuser ohne Kirche, Schule, Gemeindehaus"),
    col("persons_per_house", "Personen je Haus", "Persons per house", "number", "Personen/Haus", derived=True),
    col("size_order", "Größenklasse (Nr.)", "Size class (no.)", "integer", derived=True),
    col("size_class", "Größenklasse", "Size class", "string", "Einwohner", derived=True),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (data/gazetteer/coords.json), nicht im Druck"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (data/gazetteer/coords.json), nicht im Druck"),
    col("geonames", "GeoNames-ID", "GeoNames ID", "integer", derived=True),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
refs_places = uniq_refs(U)

# --- check against Brueckner's own size table (Part I, p. 98) ---------------------------------
BANDS = [("1–500", 1, 501), ("500–1000", 501, 1000), ("1000–2000", 1000, 2000),
         ("2000–3000", 2000, 3000), ("4000–5000", 4000, 5000), ("16000–17000", 16000, 17000)]
PRINTED = {  # transcribed from p. 98 b1 r2-r5 (Zahl der Orte / Volksmenge)
    "Gera": {"1–500": (71, 13684), "500–1000": (6, 3577), "1000–2000": (3, 4708), "16000–17000": (1, 16283)},
    "Schleiz": {"1–500": (36, 10059), "500–1000": (4, 2910), "1000–2000": (3, 4775), "2000–3000": (2, 4671), "4000–5000": (1, 4953)},
    "Lobenstein-Ebersdorf": {"1–500": (35, 10148), "500–1000": (7, 4666), "1000–2000": (3, 4697), "2000–3000": (1, 2843)},
}
check_rows = []
for lt in LT_ORDER:
    for band, lo, hi in BANDS:
        mine = [r for r in rows if r[2] == lt and lo <= r[7] < hi]
        pr = PRINTED[lt].get(band)
        if not pr and not mine:
            continue
        check_rows.append([lt, band, pr[0] if pr else 0, pr[1] if pr else 0, len(mine), sum(r[7] for r in mine),
                           len(mine) - (pr[0] if pr else 0), sum(r[7] for r in mine) - (pr[1] if pr else 0)])
check_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("band", "Größenband (Brückner)", "Size band (Brückner)", "string", "Einwohner"),
    col("places_printed", "Orte (Brückner S. 98)", "Places (Brückner p. 98)", "integer", "Orte"),
    col("population_printed", "Volksmenge (Brückner S. 98)", "Population (Brückner p. 98)", "integer", "Personen"),
    col("places_g7", "Orte (Ortsartikel)", "Places (place articles)", "integer", "Orte", derived=True),
    col("population_g7", "Volksmenge (Ortsartikel)", "Population (place articles)", "integer", "Personen", derived=True),
    col("diff_places", "Differenz Orte", "Difference, places", "integer", derived=True),
    col("diff_population", "Differenz Volksmenge", "Difference, population", "integer", derived=True),
]
# totals printed in the three Landestheil introductions
lt_entries = {e["id"]: e for e in ents if e["type"] == "Landestheil"}
cov_rows = []
for lt, key in zip(LT_ORDER, ["landestheil-gera", "landestheil-schleiz", "landestheil-lobenstein-ebersdorf"]):
    r = [x for x in rows if x[2] == lt]
    s = sum(x[7] for x in r)
    p = lt_entries[key]["inhabitants"]
    cov_rows.append([lt, p, len(r), s, s - p, round(100 * (s - p) / p, 2)])
cov_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("population_intro", "Einwohner laut Einleitung des Landestheils", "Inhabitants given in the district introduction", "integer", "Personen"),
    col("n_places", "Orte (Summe der Ortsartikel)", "Places (sum of place articles)", "integer", "Orte", derived=True),
    col("population_sum", "Summe der Einwohner der Orte", "Sum of the places' inhabitants", "integer", "Personen", derived=True),
    col("diff", "Differenz", "Difference", "integer", "Personen", derived=True),
    col("diff_pct", "Differenz", "Difference", "number", "%", derived=True),
]
refs_cov = uniq_refs([lt_entries[k] for k in lt_entries])

# --- statistics for the text ------------------------------------------------------------------
n = len(rows)
tot = sum(r[7] for r in rows)
cls_n = {c: sum(1 for r in rows if r[4] == c) for c in ["Stadt", "Marktflecken", "Dorf"]}
small = [r for r in rows if r[7] < 300]
big = [r for r in rows if r[7] >= 1000]
sm_pop = sum(r[7] for r in small)
bg_pop = sum(r[7] for r in big)
med_v = {lt: median([r[7] for r in rows if r[2] == lt and r[4] == "Dorf"]) for lt in LT_ORDER}
mean_v = {lt: mean([r[7] for r in rows if r[2] == lt and r[4] == "Dorf"]) for lt in LT_ORDER}
n_v = {lt: sum(1 for r in rows if r[2] == lt and r[4] == "Dorf") for lt in LT_ORDER}
n_all = {lt: sum(1 for r in rows if r[2] == lt) for lt in LT_ORDER}
pph_v = {lt: median([r[9] for r in rows if r[2] == lt and r[4] == "Dorf"]) for lt in LT_ORDER}
pph_t = {r[1]: r[9] for r in rows if r[4] == "Stadt"}
villages_big = sorted([r for r in rows if r[4] == "Dorf" and r[7] >= 1000], key=lambda r: -r[7])
top_pph = sorted([r for r in rows if r[4] == "Dorf"], key=lambda r: -r[9])[:3]
exact_cells = sum(1 for r in check_rows if r[6] == 0)
exact_pop = sum(1 for r in check_rows if r[7] == 0)
lt_diff = {r[0]: r[4] for r in cov_rows}


def sg(x):
    return '±0' if x == 0 else (f'+{x}' if x > 0 else f'−{abs(x)}')

# Brueckner's table totals (p. 98) per Landestheil: 38252, 27368, 22354
tab_tot = {"Gera": 38252, "Schleiz": 27368, "Lobenstein-Ebersdorf": 22354}
sum_lt = {lt: sum(r[7] for r in rows if r[2] == lt) for lt in LT_ORDER}
dt = {lt: sum_lt[lt] - tab_tot[lt] for lt in LT_ORDER}
n_geo = sum(1 for r in rows if r[12] is not None)
doubt = sorted({e["name"] + " (" + e["landestheil"] + ")" for e in ents
                if (e["id"], e["landestheil"]) in DOUBTFUL_COORDS and e["id"] in C})
pp_town_gera = pph_t["Gera"]

findings = [
    bi(f"Aus den Ortsartikeln lassen sich Brückners {n} Gemeinden vollständig nachbilden: {fnum(n)} Orte mit zusammen {fnum(tot)} Einwohnern ({cls_n['Stadt']} Städte, {cls_n['Marktflecken']} Marktflecken, {cls_n['Dorf']} Dörfer). In allen {len(check_rows)} Größenbändern von S. 98 stimmt die Zahl der Orte, die Volksmenge stimmt in {exact_pop} von {len(check_rows)} Bändern genau; die Summen der Landestheile weichen von Brückners Tabelle um {sg(dt['Gera'])} (Gera), {sg(dt['Schleiz'])} (Schleiz) und {sg(dt['Lobenstein-Ebersdorf'])} (Lobenstein-Ebersdorf) Personen ab.",
       f"Brückner's {n} municipalities can be rebuilt completely from the place articles: {fnum(n,0,'en')} places with {fnum(tot,0,'en')} inhabitants in total ({cls_n['Stadt']} towns, {cls_n['Marktflecken']} market towns, {cls_n['Dorf']} villages). The number of places agrees in all {len(check_rows)} size bands of p. 98, the population agrees exactly in {exact_pop} of {len(check_rows)} bands; the district totals differ from Brückner's table by {sg(dt['Gera'])} (Gera), {sg(dt['Schleiz'])} (Schleiz) and {sg(dt['Lobenstein-Ebersdorf'])} (Lobenstein-Ebersdorf) persons.")
    if exact_cells == len(check_rows) else
    bi(f"Aus den Ortsartikeln lassen sich Brückners {n} Gemeinden nachbilden: {fnum(n)} Orte mit zusammen {fnum(tot)} Einwohnern. Die Zahl der Orte stimmt in {exact_cells} von {len(check_rows)} Größenbändern von S. 98 überein.",
       f"Brückner's {n} municipalities can be rebuilt from the place articles: {fnum(n,0,'en')} places with {fnum(tot,0,'en')} inhabitants. The number of places agrees in {exact_cells} of {len(check_rows)} size bands of p. 98."),
    bi(f"Das Siedlungsbild ist kleinteilig: {len(small)} von {n} Orten ({pct(100*len(small)/n,0)}) haben weniger als 300 Einwohner und beherbergen zusammen {pct(100*sm_pop/tot,1)} der Bevölkerung; die {len(big)} Orte ab 1 000 Einwohnern ({pct(100*len(big)/n,1)} der Orte) vereinen dagegen {pct(100*bg_pop/tot,1)}.",
       f"The settlement pattern is fine-grained: {len(small)} of {n} places ({pct(100*len(small)/n,0,'en')}) have fewer than 300 inhabitants and together hold {pct(100*sm_pop/tot,1,'en')} of the population; the {len(big)} places with 1,000 or more inhabitants ({pct(100*len(big)/n,1,'en')} of the places) account for {pct(100*bg_pop/tot,1,'en')}."),
    bi(f"Im Landestheil Gera liegen {n_v['Gera']} Dörfer mit im Median {fnum(med_v['Gera'])} Einwohnern, in Schleiz {n_v['Schleiz']} mit {fnum(med_v['Schleiz'])} und in Lobenstein-Ebersdorf {n_v['Lobenstein-Ebersdorf']} mit {fnum(med_v['Lobenstein-Ebersdorf'])}: Das Unterland hat also mehr und kleinere Dörfer (Mittelwert {fnum(mean_v['Gera'])} gegen {fnum(mean_v['Schleiz'])} und {fnum(mean_v['Lobenstein-Ebersdorf'])}).",
       f"The district of Gera has {n_v['Gera']} villages with a median of {fnum(med_v['Gera'],0,'en')} inhabitants, Schleiz {n_v['Schleiz']} with {fnum(med_v['Schleiz'],0,'en')} and Lobenstein-Ebersdorf {n_v['Lobenstein-Ebersdorf']} with {fnum(med_v['Lobenstein-Ebersdorf'],0,'en')}: the lowland thus has more and smaller villages (mean {fnum(mean_v['Gera'],0,'en')} against {fnum(mean_v['Schleiz'],0,'en')} and {fnum(mean_v['Lobenstein-Ebersdorf'],0,'en')})."),
    bi(f"Im Dorf wohnen im Median {fnum(pph_v['Gera'],1)} (Gera), {fnum(pph_v['Schleiz'],1)} (Schleiz) und {fnum(pph_v['Lobenstein-Ebersdorf'],1)} (Lobenstein-Ebersdorf) Personen in einem Haus; die Stadt Gera erreicht {fnum(pp_town_gera,1)}, die übrigen Städte {fnum(min(v for k,v in pph_t.items() if k!='Gera'),1)}–{fnum(max(v for k,v in pph_t.items() if k!='Gera'),1)}. Das Dorf mit den meisten Personen je Haus ist {top_pph[0][1]} ({fnum(top_pph[0][9],1)}).",
       f"In villages the median is {fnum(pph_v['Gera'],1,'en')} (Gera), {fnum(pph_v['Schleiz'],1,'en')} (Schleiz) and {fnum(pph_v['Lobenstein-Ebersdorf'],1,'en')} (Lobenstein-Ebersdorf) persons per house; the town of Gera reaches {fnum(pp_town_gera,1,'en')}, the other towns {fnum(min(v for k,v in pph_t.items() if k!='Gera'),1,'en')}–{fnum(max(v for k,v in pph_t.items() if k!='Gera'),1,'en')}. The village with most persons per house is {top_pph[0][1]} ({fnum(top_pph[0][9],1,'en')})."),
]

charts = []
LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
charts.append({
    "id": "c1", "dataset": "places",
    "title": bi("Die Orte des Fürstenthums 1867", "The places of the principality, 1867"),
    "caption": bi(f"Je Kreis ein Ort ({n_geo} von {n} verortet), Fläche nach Einwohnerzahl (Wurzelskala), Farbe nach Landestheil. Beschriftet sind die Orte ab 1 800 Einwohnern; Norden ist oben. Die Koordinaten stammen aus GeoNames, nicht aus dem Buch.",
                  f"One circle per place ({n_geo} of {n} located), area by number of inhabitants (square-root scale), colour by district. Places with 1,800 or more inhabitants are labelled; north is up. Coordinates are taken from GeoNames, not from the book."),
    "vegalite": {
        "height": 460,
        "projection": {"type": "mercator"},
        "layer": [
            {"transform": [{"filter": "isValid(datum.lat)"}],
             "mark": {"type": "circle", "opacity": 0.72},
             "encoding": {
                 "longitude": {"field": "lon", "type": "quantitative"},
                 "latitude": {"field": "lat", "type": "quantitative"},
                 "size": {"field": "inhabitants", "type": "quantitative", "title": bi("Einwohner", "Inhabitants"),
                          "scale": {"type": "sqrt", "range": [14, 1500], "domain": [0, 16300]},
                          "legend": {"values": [100, 1000, 5000], "labelExpr": bi("replace(format(datum.value, ','), ',', ' ')", "format(datum.value, ',')")}},
                 "color": LT_COLOR,
                 "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                             {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Ortsklasse", "Class")},
                             {"field": "landestheil", "title": bi("Landestheil", "District")},
                             {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants")},
                             {"field": "houses", "title": bi("Häuser", "Houses")},
                             {"field": "page", "title": bi("Seite", "Page")}]}},
            {"transform": [{"filter": "isValid(datum.lat) && datum.inhabitants >= 10000"}],
             "mark": {"type": "text", "align": "left", "dx": 27, "dy": -4, "fontSize": 11},
             "encoding": {"longitude": {"field": "lon", "type": "quantitative"},
                          "latitude": {"field": "lat", "type": "quantitative"},
                          "text": {"field": "name"}}},
            {"transform": [{"filter": "isValid(datum.lat) && datum.inhabitants >= 1800 && datum.inhabitants < 10000"}],
             "mark": {"type": "text", "align": "left", "dx": 14, "dy": -4, "fontSize": 10},
             "encoding": {"longitude": {"field": "lon", "type": "quantitative"},
                          "latitude": {"field": "lat", "type": "quantitative"},
                          "text": {"field": "name"}}},
        ]},
})
charts.append({
    "id": "c2", "dataset": "places",
    "title": bi("Größenklassen der Orte nach Landestheil", "Size classes of the places by district"),
    "caption": bi("Anzahl der Orte je Größenklasse (Einwohner). Das Unterland (Gera) hat die meisten kleinen Orte, die Städte und größten Märkte liegen in der Klasse ab 1 000.",
                  "Number of places per size class (inhabitants). The lowland (Gera) has most of the small places; the towns and the largest market towns fall into the classes from 1,000."),
    "vegalite": {
        "height": 280,
        "mark": "bar",
        "encoding": {
            "x": {"field": "size_class", "type": "ordinal", "sort": {"field": "size_order", "op": "min"},
                  "title": bi("Einwohner", "Inhabitants"), "axis": {"labelAngle": 0}},
            "xOffset": {"field": "landestheil", "sort": LT_ORDER},
            "y": {"aggregate": "count", "type": "quantitative", "title": bi("Anzahl der Orte", "Number of places"),
                  "axis": {"tickMinStep": 1}},
            "color": LT_COLOR,
            "tooltip": [{"field": "size_class", "title": bi("Größenklasse", "Size class")},
                        {"field": "landestheil", "title": bi("Landestheil", "District")},
                        {"aggregate": "count", "title": bi("Orte", "Places")},
                        {"aggregate": "sum", "field": "inhabitants", "title": bi("Einwohner", "Inhabitants")}]}},
})
charts.append({
    "id": "c3", "dataset": "places",
    "title": bi("Personen je Haus: Dörfer und Städte", "Persons per house: villages and towns"),
    "caption": bi("Kasten: Dörfer und Marktflecken je Landestheil (Median, Quartile, 1,5-facher Quartilsabstand); Rauten: die sechs Städte; Kreise: auffällige Dörfer (Untermhaus, Cuba, Pforten, Tinz). Gera fällt mit dem mehrstöckigen Stadthaus aus dem Rahmen.",
                  "Box: villages and market towns per district (median, quartiles, 1.5 x interquartile range); diamonds: the six towns; circles: outlying villages (Untermhaus, Cuba, Pforten, Tinz). Gera stands out with its multi-storey town houses."),
    "vegalite": {
        "height": 300,
        "layer": [
            {"transform": [{"filter": "datum.class_de != 'Stadt'"}],
             "mark": {"type": "boxplot", "extent": 1.5, "size": 38, "opacity": 0.55},
             "encoding": {
                 "x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "persons_per_house", "type": "quantitative", "title": bi("Personen je Haus", "Persons per house"), "scale": {"zero": False}},
                 "color": LT_COLOR}},
            {"transform": [{"filter": "datum.class_de == 'Stadt'"}],
             "mark": {"type": "point", "filled": True, "size": 90, "shape": "diamond", "opacity": 1},
             "encoding": {
                 "x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER},
                 "y": {"field": "persons_per_house", "type": "quantitative"},
                 "color": LT_COLOR,
                 "tooltip": [{"field": "name", "title": bi("Stadt", "Town")},
                             {"field": "persons_per_house", "title": bi("Personen je Haus", "Persons per house"), "format": ".1f"},
                             {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants")},
                             {"field": "houses", "title": bi("Häuser", "Houses")}]}},
            {"transform": [{"filter": "datum.class_de != 'Stadt' && datum.persons_per_house >= 11"}],
             "mark": {"type": "text", "align": "left", "dx": 9, "fontSize": 10},
             "encoding": {"x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER},
                          "y": {"field": "persons_per_house", "type": "quantitative"},
                          "text": {"field": "name"}}},
            {"transform": [{"filter": "datum.class_de == 'Stadt'"}],
             "mark": {"type": "text", "align": "left", "dx": 9, "fontSize": 10},
             "encoding": {"x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER},
                          "y": {"field": "persons_per_house", "type": "quantitative"},
                          "text": {"field": "name"}}},
        ]},
})

a = {
    "id": "orte-siedlungsbild-1867",
    "title": bi("Siedlungsbild 1867: Größe der Orte und Personen je Haus", "Settlement pattern 1867: size of places and persons per house"),
    "category": "places",
    "section": "t2",
    "sources": refs_places + [r for r in refs_cov if r not in refs_places] + [{"page": "98", "block": "b1", "rows": "r2-r5"}],
    "summary": bi(
        f"Der Ortskundeteil beschreibt jede der {n} Gemeinden des Fürstenthums mit Häuser- und Einwohnerzahl. Zusammengeführt ergibt das ein Bild des Siedlungsnetzes 1867: Karte der Orte, Verteilung der Ortsgrößen je Landestheil und die Zahl der Personen je Haus in Dörfern und Städten.",
        f"The topography part describes each of the principality's {n} municipalities with its numbers of houses and inhabitants. Put together, they give a picture of the settlement network in 1867: a map of the places, the distribution of place sizes by district, and the number of persons per house in villages and towns."),
    "method": bi(
        f"Grundlage sind die Einträge der sechs Gazetteer-Pakete G1–G6 (data/gazetteer/G1–G6.json). Aufgenommen wurden alle Einträge der Ortsarten Stadt, Marktflecken, Dorf, Weiler und Kammergut, die Häuser- und Einwohnerzahl haben und keine Bestandteile anderer Gemeinden sind (ausgeschlossen: Pöppeln, das in Geras Zahlen enthalten ist; Dürrenbach, das 1867 zu Grumbach zählte; Dürrenberg, Eleonorenthal, Köstritzer Bahnhof, Heinrichshall und die Chemische Fabrik, die in Hartmannsdorf, Köstritz und Pohlitz mitgezählt sind), das sind {n} Orte. Die Zahlen sind, soweit nicht anders gesagt, die des Zählungsjahres 1867; bei zweiherrischen Orten (Roschitz, Hundhaupten, Kraftsdorf, Rüdersdorf, Seifartsdorf, Bethenhausen, Weitisberga, Blintendorf, Mödlareuth) nur der reußische Anteil. Als Häuser zählt Brückner meist die bewohnten Privathäuser ohne Kirche, Schule und Gemeindehaus. Bei Göritz (607 Einwohner, 89 Häuser mit Lehesten) und Neundorf (716 Einwohner mit Hornsgrün, Heinrichsgrün, Langwassermühle und Jägersruh) wurde die im Artikel genannte Zahl der ganzen Gemeinde statt der des Hauptorts verwendet, damit die Summen Brückners Tabelle auf S. 98 entsprechen. Personen je Haus = Einwohner : Häuser. Größenklassen: 100er-Schritte bis 300, dann 300–499, 500–999, 1 000–1 999 und ab 2 000. Koordinaten (Länge, Breite) stammen aus GeoNames (data/gazetteer/coords.json) und sind abgeleitete Spalten; {len(doubt)} Koordinatenpaare wurden nicht verwendet, weil sie auf ein gleichnamiges Dorf an anderer Stelle zeigen oder doppelt belegt sind ({', '.join(doubt)}). Die Karte zeigt {n_geo} der {n} Orte. Prüfung: Die Orte wurden den Größenbändern von Brückners Tabelle (Teil I, S. 98) zugeordnet und mit den dort gedruckten Zahlen verglichen (Datensatz size_check); die Summen je Landestheil stehen im Datensatz coverage den Gesamtzahlen der Landestheil-Einleitungen gegenüber.",
        f"The basis is the entries of the six gazetteer packages G1–G6 (data/gazetteer/G1–G6.json). All entries of the types town, market town, village, hamlet and Kammergut that have house and inhabitant figures and are not parts of other municipalities were included (excluded: Pöppeln, which is contained in the figures for Gera; Dürrenbach, which belonged to Grumbach in 1867; Dürrenberg, Eleonorenthal, Köstritzer Bahnhof, Heinrichshall and the Chemische Fabrik, which are counted within Hartmannsdorf, Köstritz and Pohlitz); this gives {n} places. Unless stated otherwise the figures are those of the 1867 census; for places shared with a neighbouring state (Roschitz, Hundhaupten, Kraftsdorf, Rüdersdorf, Seifartsdorf, Bethenhausen, Weitisberga, Blintendorf, Mödlareuth) only the Reuss share. By 'houses' Brückner mostly means inhabited private houses without church, school and municipal buildings. For Göritz (607 inhabitants, 89 houses including Lehesten) and Neundorf (716 inhabitants including Hornsgrün, Heinrichsgrün, Langwassermühle and Jägersruh) the figure for the whole municipality given in the article was used instead of that for the main settlement, so that the sums match Brückner's table on p. 98. Persons per house = inhabitants : houses. Size classes: steps of 100 up to 300, then 300–499, 500–999, 1,000–1,999 and 2,000 and over. Coordinates (longitude, latitude) come from GeoNames (data/gazetteer/coords.json) and are derived columns; {len(doubt)} coordinate pairs were not used because they point to a homonymous village elsewhere or are assigned twice ({', '.join(doubt)}). The map shows {n_geo} of the {n} places. Check: the places were assigned to the size bands of Brückner's table (Part I, p. 98) and compared with the printed figures (dataset size_check); the sums per district are set against the totals of the district introductions in the dataset coverage."),
    "findings": findings,
    "caveats": [
        bi("Die Zahlen sind die des Zählungsjahres 1867; bei den Dörfern steht das Jahr meist nicht dabei und wird angenommen (Vergleichszahlen von 1861 oder 1864 nennt Brückner mehrfach, sie wurden nicht verwendet).",
           "The figures are those of the 1867 census; for villages the year is mostly not stated and is assumed (Brückner often gives comparison figures for 1861 or 1864, which were not used)."),
        bi(f"Die Einwohnerzahlen der Landestheil-Einleitungen (Gera {fnum(cov_rows[0][1])}, Schleiz {fnum(cov_rows[1][1])}, Lobenstein-Ebersdorf {fnum(cov_rows[2][1])}) weichen von den Summen der Orte ab (Gera {sg(cov_rows[0][4])}, Schleiz {sg(cov_rows[1][4])}, Lobenstein-Ebersdorf {sg(cov_rows[2][4])}); Brückners Tabelle auf S. 98 führt für Gera {fnum(tab_tot['Gera'])} und für Lobenstein-Ebersdorf {fnum(tab_tot['Lobenstein-Ebersdorf'])}. Die Quellen sind also nicht ganz einheitlich.",
           f"The inhabitant figures in the district introductions (Gera {fnum(cov_rows[0][1],0,'en')}, Schleiz {fnum(cov_rows[1][1],0,'en')}, Lobenstein-Ebersdorf {fnum(cov_rows[2][1],0,'en')}) differ from the sums of the places (Gera {sg(cov_rows[0][4])}, Schleiz {sg(cov_rows[1][4])}, Lobenstein-Ebersdorf {sg(cov_rows[2][4])}); Brückner's table on p. 98 gives {fnum(tab_tot['Gera'],0,'en')} for Gera and {fnum(tab_tot['Lobenstein-Ebersdorf'],0,'en')} for Lobenstein-Ebersdorf. The sources are therefore not entirely uniform."),
        bi("Die Zahl der Häuser ist nicht überall gleich definiert (Privathäuser, bewohnte Gebäude, bei Gera 'Häuser' einschließlich Pöppeln, bei Schleiz einschließlich Mühlen); Personen je Haus ist daher nur ein grobes Maß der Haushaltsgröße. Die Stadt Gera (mit Pöppeln) und Untermhaus (Fabrikarbeiter in Mehrfamilienhäusern) heben sich auch deshalb ab.",
           "The number of houses is not defined uniformly everywhere (private houses, inhabited buildings; for Gera 'houses' include Pöppeln, for Schleiz mills); persons per house is therefore only a rough measure of household size. The town of Gera (with Pöppeln) and Untermhaus (factory workers in multi-family houses) stand out partly for this reason."),
        bi("Koordinaten sind GeoNames-Positionen der heutigen Orte (Ortsmitte), nicht Brückners Angaben; einige Orte sind unverortet oder wegen zweifelhafter Zuordnung ausgelassen. Die Karte ist eine einfache Punktkarte ohne Grenzen und Gewässer.",
           "Coordinates are GeoNames positions of today's places (settlement centres), not Brückner's data; some places are unlocated or omitted because of doubtful matches. The map is a plain point map without borders or rivers."),
    ],
    "datasets": [
        {"name": "places", "title": bi("Die Gemeinden mit Einwohnern, Häusern und Lage", "The municipalities with inhabitants, houses and position"),
         "columns": cols, "rows": rows, "source_refs": refs_places},
        {"name": "size_check", "title": bi("Vergleich mit Brückners Größentabelle (S. 98)", "Comparison with Brückner's size table (p. 98)"),
         "columns": check_cols, "rows": check_rows, "source_refs": [{"page": "98", "block": "b1", "rows": "r2-r5"}]},
        {"name": "coverage", "title": bi("Summe der Orte und Einwohnerzahl der Landestheile", "Sum of the places and inhabitants of the districts"),
         "columns": cov_cols, "rows": cov_rows, "source_refs": refs_cov},
    ],
    "charts": charts,
    "conversions": [],
    "keywords": {"de": ["Siedlungsbild", "Ortsgrößen", "Einwohner", "Häuser", "Personen je Haus", "Dörfer", "Städte", "Landestheile", "Karte"],
                 "en": ["settlement pattern", "place sizes", "inhabitants", "houses", "persons per house", "villages", "towns", "districts", "map"]},
    "related": ["bevoelkerung-gemeindegroessen-1867", "wohnen-wohnhaeuser-wohndichte-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
