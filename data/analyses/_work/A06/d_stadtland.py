"""A06 / analysis 4: urban and rural population 1833-1867, towns and larger villages 1647-1867 (pp. 95-97)."""
import re
from common import *

# ---------------------------------------------------------------- urban / rural (p. 95 b4)
g95 = grid("95", "b4")
urban_rural = []
cur = None
NAMES = {"Landrathsbezirk Gera.": "Gera", "Landrathsbezirk Schleiz.": "Schleiz",
         "Landrathsbezirk Lobenstein-Ebersdorf.": "Lobenstein-Ebersdorf", "Das Fürstenthum.": "Fürstenthum"}
for r in g95[1:]:
    if not r[0].isdigit():
        cur = NAMES[r[2]]
        continue
    y = int(r[0])
    urban, rural, total = integer(r[1]), integer(r[2]), integer(r[3])
    pu, pr = num(r[4]), num(r[5])
    if cur == "Fürstenthum" and y == 1867:
        assert rural == 58052  # misprint, see caveat: p. 97 and p. 99 print 59052
        rural = 59052
    assert urban + rural == total, (cur, y)
    urban_rural.append([cur, y, urban, rural, total, pu, pr])

# ---------------------------------------------------------------- towns and villages (p. 96)
def clean(n):
    return re.sub(r"[ .]+$", "", n).strip()

towns = []
for r in grid("96", "b3")[2:8]:
    towns.append((clean(r[0]), "Stadt", [integer(r[1]), integer(r[2]), integer(r[3])], num(re.match(r"[\d,]+", r[4]).group(0))))
vill = []
for r in grid("96", "b5")[1:9]:
    vill.append((clean(r[0]), "Landort", [integer(x) for x in r[1:6]], num(re.match(r"[\d,]+", r[6]).group(0))))
places_long, place_growth = [], []
for name, kind, vals, fprinted in towns:
    for y, v in zip((1647, 1833, 1867), vals):
        places_long.append([name, kind, y, v])
    place_growth.append([name, kind, vals[0], vals[-1], round(vals[-1] / vals[0], 2), fprinted])
for name, kind, vals, fprinted in vill:
    for y, v in zip((1647, 1833, 1861, 1864, 1867), vals):
        places_long.append([name, kind, y, v])
    place_growth.append([name, kind, vals[0], vals[-1], round(vals[-1] / vals[0], 2), fprinted])
print([p[0] for p in place_growth])

PLACE_EN = {"Gera": "Gera", "Schleiz": "Schleiz", "Lobenstein": "Lobenstein", "Tanna": "Tanna", "Saalburg": "Saalburg", "Hirschberg": "Hirschberg"}
TOWN_KEYS = [p[0] for p in towns]

# ---------------------------------------------------------------- settlement classes (p. 97 b3)
g97 = grid("97", "b3")
CLASSES = ["Städte", "8 Landorte über 1000 E.", "Landorte unter 1000 E."]
CLASS_EN = {"Städte": "Towns", "8 Landorte über 1000 E.": "8 rural places over 1,000", "Landorte unter 1000 E.": "Rural places under 1,000"}
order = [("Gera", 1833), ("Gera", 1867), ("Schleiz", 1833), ("Schleiz", 1867), ("Lobenstein-Ebersdorf", 1833),
         ("Lobenstein-Ebersdorf", 1867), ("Fürstenthum", 1833), ("Fürstenthum", 1867)]
pops = g97[2:10]
dens = g97[11:19]
classes = []
for (d, y), rp, rd in zip(order, pops, dens):
    assert rp[0].endswith(str(y)) and rd[0].endswith(str(y)), (rp[0], y)
    for i, c in enumerate(CLASSES):
        p = integer(rp[1 + i])
        dd = num(rd[1 + i])
        classes.append([d, y, c, p, dd, round(dd / SQM_KM2, 1)])
# stacked parts add to the printed rural total
for (d, y), rp in zip(order, pops):
    s = sum(integer(rp[i]) for i in (2, 3))
    t = integer(rp[4])
    if s != t:
        print("rural parts mismatch", d, y, s, t)

# ---------------------------------------------------------------- numbers for prose
UR = {(r[0], r[1]): r for r in urban_rural}
sh = {d: (UR[(d, 1833)][5], UR[(d, 1867)][5]) for d in DIST_KEYS}
dsh = {d: sh[d][1] - sh[d][0] for d in DIST_KEYS}
print(sh, dsh)
PG = {p[0]: p for p in place_growth}
ABS = {}
for n in TOWN_KEYS:
    a1833 = next(r[3] for r in places_long if r[0] == n and r[2] == 1833)
    a1867 = next(r[3] for r in places_long if r[0] == n and r[2] == 1867)
    ABS[n] = (a1833, a1867, a1867 - a1833)
print(ABS)
top = sorted(place_growth, key=lambda p: -p[4])
print([(p[0], p[4]) for p in top])
ebers = {r[2]: r[3] for r in places_long if r[0] == "Ebersdorf"}
print(ebers)
vill_sum_1647 = sum(p[2] for p in place_growth if p[1] == "Landort")
vill_sum_1867 = sum(p[3] for p in place_growth if p[1] == "Landort")
town_sum_1647 = sum(p[2] for p in place_growth if p[1] == "Stadt")
town_sum_1867 = sum(p[3] for p in place_growth if p[1] == "Stadt")
fac_t = town_sum_1867 / town_sum_1647
fac_v = vill_sum_1867 / vill_sum_1647
print(fac_t, fac_v)
Gd = {(r[0], r[1], r[2]): r for r in classes}
gera_big = Gd[("Gera", 1867, "Städte")][5], Gd[("Gera", 1833, "Städte")][5]
print(gera_big)

ana = {
    "id": "bevoelkerung-stadt-land-1833-1867",
    "title": {"de": "Stadt und Land: Städte, Landorte und Siedlungsgrößen 1647–1867",
              "en": "Town and country: towns, villages and settlement size, 1647–1867"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("95", "b4", "r3-r25"), ("96", "b3", "r3-r9"), ("96", "b5", "r2-r10"), ("97", "b3", "r3-r19"), ("95", "b5"), ("96", "b1")),
    "summary": {
        "de": f"Brückner teilt die Bevölkerung für 1833, 1843, 1852, 1864 und 1867 in städtische und ländliche und verfolgt die sechs Städte und die acht Landorte über 1000 Einwohner seit 1647. Im Fürstenthum blieb der Anteil der Stadtbevölkerung bei etwa einem Drittel ({de(sh['Fürstenthum'][0],1)} → {de(sh['Fürstenthum'][1],1)} %), doch in den Bezirken lief die Entwicklung auseinander: Gera verstädterte, Schleiz und Lobenstein-Ebersdorf wurden ländlicher.",
        "en": f"Brückner divides the population for 1833, 1843, 1852, 1864 and 1867 into urban and rural and follows the six towns and the eight villages of more than 1,000 inhabitants since 1647. In the principality the urban share stayed at about one third ({en(sh['Fürstenthum'][0],1)} → {en(sh['Fürstenthum'][1],1)} %), but the districts diverged: Gera became more urban, Schleiz and Lobenstein-Ebersdorf more rural.",
    },
    "method": {
        "de": f"Übernommen wurden die Tabelle »Vergleichung der städtischen und ländlichen Bevölkerung« (S. 95), die Einwohnerzahlen der sechs Städte und der acht größeren Landorte (S. 96) und die Gliederung der Bevölkerung nach Städten, den acht Landorten über 1000 Einwohnern und den kleineren Landorten samt der Dichte auf 1 ☐Meile (S. 97). Die Dichten wurden zusätzlich in Einwohner je km² umgerechnet (1 ☐Meile = {de(SQM_KM2,2)} km²). Berechnet wurden die Vermehrungsfaktoren 1647–1867 aus den gedruckten Einwohnerzahlen; Brückners gedruckte Faktoren weichen in einigen Fällen um 0,01–0,06 ab (z. B. Hirschberg 10,10 gedruckt, 10,16 errechnet) und stehen im Tooltip. Die Summen der Städte und Landorte ergeben in allen Zeilen die gedruckte Gesamtzahl; für das Fürstenthum 1867 wurde die ländliche Bevölkerung mit 59 052 (S. 97, S. 99) statt der auf S. 95 gedruckten 58 052 eingesetzt.",
        "en": f"Taken over are the table “comparison of the urban and rural population” (p. 95), the inhabitants of the six towns and the eight larger villages (p. 96) and the breakdown of the population into towns, the eight villages of over 1,000 inhabitants and the smaller villages together with the density per square mile (p. 97). The densities were additionally converted to inhabitants per km² (1 square mile = {en(SQM_KM2,2)} km²). The growth factors 1647–1867 were computed from the printed populations; Brückner's printed factors deviate by 0.01–0.06 in some cases (e.g. Hirschberg 10.10 printed, 10.16 computed) and appear in the tooltip. In every row the towns and rural places add up to the printed total; for the principality in 1867 the rural population was entered as 59,052 (pp. 97, 99) instead of the 58,052 printed on p. 95.",
    },
    "findings": [
        {"de": f"Der Stadtanteil im Fürstenthum blieb zwischen 1833 und 1867 nahezu gleich ({de(sh['Fürstenthum'][0],2)} → {de(sh['Fürstenthum'][1],2)} %); dahinter steht ein Anstieg in Gera um {de(dsh['Gera'],2)} Prozentpunkte und ein Rückgang in Schleiz um {de(-dsh['Schleiz'],2)} und in Lobenstein-Ebersdorf um {de(-dsh['Lobenstein-Ebersdorf'],2)} Punkte (Brückner nennt 4,02, 2,69 und 3,31).",
         "en": f"The urban share in the principality stayed almost the same between 1833 and 1867 ({en(sh['Fürstenthum'][0],2)} → {en(sh['Fürstenthum'][1],2)} %); behind this lie a rise of {en(dsh['Gera'],2)} percentage points in Gera and falls of {en(-dsh['Schleiz'],2)} in Schleiz and {en(-dsh['Lobenstein-Ebersdorf'],2)} in Lobenstein-Ebersdorf (Brückner gives 4.02, 2.69 and 3.31)."},
        {"de": f"Die Stadt Gera wuchs 1833–1867 um {de(ABS['Gera'][2],0)} Einwohner, alle übrigen fünf Städte zusammen um {de(sum(v[2] for k,v in ABS.items() if k!='Gera'),0)}; Lobenstein verlor {de(-ABS['Lobenstein'][2],0)} Einwohner ({de(ABS['Lobenstein'][2]/ABS['Lobenstein'][0]*100,1)} %).",
         "en": f"The town of Gera grew by {en(ABS['Gera'][2],0)} inhabitants in 1833–1867, all five other towns together by {en(sum(v[2] for k,v in ABS.items() if k!='Gera'),0)}; Lobenstein lost {en(-ABS['Lobenstein'][2],0)} inhabitants ({en(ABS['Lobenstein'][2]/ABS['Lobenstein'][0]*100,1)} %)."},
        {"de": f"Seit 1647 haben sich die sechs Städte zusammen auf das {de(fac_t,2)}fache, die acht größeren Landorte auf das {de(fac_v,2)}fache vermehrt; am stärksten wuchsen Ebersdorf (×{de(PG['Ebersdorf'][4],2)}), Hohenleuben (×{de(PG['Hohenleuben'][4],2)}), Untermhaus (×{de(PG['Untermhaus'][4],2)}) und Hirschberg (×{de(PG['Hirschberg'][4],2)}), Gera nur auf das {de(PG['Gera'][4],2)}fache.",
         "en": f"Since 1647 the six towns together have grown by a factor of {en(fac_t,2)} and the eight larger villages by {en(fac_v,2)}; the strongest growth was that of Ebersdorf (×{en(PG['Ebersdorf'][4],2)}), Hohenleuben (×{en(PG['Hohenleuben'][4],2)}), Untermhaus (×{en(PG['Untermhaus'][4],2)}) and Hirschberg (×{en(PG['Hirschberg'][4],2)}), while Gera grew only by {en(PG['Gera'][4],2)}."},
        {"de": f"Ebersdorf zählte 1861 noch {de(ebers[1861],0)}, 1867 nur noch {de(ebers[1867],0)} Einwohner ({de((ebers[1867]/ebers[1861]-1)*100,1)} %); Brückner bringt den Rückgang mit dem Verlust der Residenz 1848 in Verbindung.",
         "en": f"Ebersdorf had {en(ebers[1861],0)} inhabitants in 1861 and only {en(ebers[1867],0)} in 1867 ({en((ebers[1867]/ebers[1861]-1)*100,1)} %); Brückner links the decline to the loss of the residence in 1848."},
        {"de": f"Auf die Fläche des Bezirks bezogen trägt die Stadt Gera 1867 {de(gera_big[0],0)} Einwohner je km² zur Gesamtdichte von {de(sum(Gd[('Gera',1867,c)][5] for c in CLASSES),0)} bei (1833: {de(gera_big[1],0)} von {de(sum(Gd[('Gera',1833,c)][5] for c in CLASSES),0)}); in Lobenstein-Ebersdorf sank der Beitrag der Städte von {de(Gd[('Lobenstein-Ebersdorf',1833,'Städte')][5],0)} auf {de(Gd[('Lobenstein-Ebersdorf',1867,'Städte')][5],0)}, der der kleinen Landorte stieg von {de(Gd[('Lobenstein-Ebersdorf',1833,'Landorte unter 1000 E.')][5],0)} auf {de(Gd[('Lobenstein-Ebersdorf',1867,'Landorte unter 1000 E.')][5],0)}.",
         "en": f"Related to the area of the district, the town of Gera contributes {en(gera_big[0],0)} inhabitants per km² to the overall density of {en(sum(Gd[('Gera',1867,c)][5] for c in CLASSES),0)} in 1867 (1833: {en(gera_big[1],0)} of {en(sum(Gd[('Gera',1833,c)][5] for c in CLASSES),0)}); in Lobenstein-Ebersdorf the contribution of the towns fell from {en(Gd[('Lobenstein-Ebersdorf',1833,'Städte')][5],0)} to {en(Gd[('Lobenstein-Ebersdorf',1867,'Städte')][5],0)}, that of the small villages rose from {en(Gd[('Lobenstein-Ebersdorf',1833,'Landorte unter 1000 E.')][5],0)} to {en(Gd[('Lobenstein-Ebersdorf',1867,'Landorte unter 1000 E.')][5],0)}."},
    ],
    "caveats": [
        {"de": "Druckfehler im Original (die Transkription entspricht dem Faksimile): S. 95 nennt für die ländliche Bevölkerung des Fürstenthums 1867 »58052«, richtig sind 59 052 (Summe mit 28 922 = 87 974; S. 97 und S. 99 drucken 59 052; die Prozentzahl 67,13 passt dazu). S. 97 gibt für 1833 »46603« statt 46 605 (S. 95; 9 945 + 36 660). Bei Schleiz 1864 steht auf S. 95 die Summe 27 175, auf S. 91 27 174.",
         "en": "Misprints in the original (the transcription matches the facsimile): p. 95 gives “58052” for the rural population of the principality in 1867; the correct figure is 59,052 (with 28,922 it makes 87,974; pp. 97 and 99 print 59,052; the percentage 67.13 fits). p. 97 gives “46603” for 1833 instead of 46,605 (p. 95; 9,945 + 36,660). For Schleiz in 1864 p. 95 gives the total 27,175, p. 91 gives 27,174."},
        {"de": "»Stadt« ist rechtlich bestimmt: Die sechs Städte (Gera; Schleiz, Saalburg, Tanna; Lobenstein, Hirschberg) gelten als städtisch, auch wenn Landwirtschaft betrieben wird; Landorte mit Gewerbe oder Verwaltungssitz (Ebersdorf, Hohenleuben, Untermhaus) zählen als ländlich. Brückner weist selbst darauf hin, dass der Gegensatz nicht Industrie und Bauernwirtschaft trennt (S. 97).",
         "en": "“Town” is a legal category: the six towns (Gera; Schleiz, Saalburg, Tanna; Lobenstein, Hirschberg) count as urban even if they practise agriculture; villages with trades or an administrative seat (Ebersdorf, Hohenleuben, Untermhaus) count as rural. Brückner himself points out that the contrast does not separate industry from peasant farming (p. 97)."},
        {"de": "Die Orte werden nach dem Gebietsstand der Zählung aufgeführt; Untermhaus (bei Gera) und Köstritz erscheinen als eigene Landorte, nicht als Teile der Stadt Gera.",
         "en": "Places are listed as constituted at the time of each count; Untermhaus (near Gera) and Köstritz appear as separate rural places, not as parts of the town of Gera."},
    ],
    "conversions": [
        {"from": "☐Meile (geographische Quadratmeile)", "to": "km²", "factor_or_formula": f"1 ☐Meile = {SQM_KM2:.2f} km²",
         "reference": "Brückner S. 832: 1 geographische Meile = 0,9894 künftige Meile (zu 7500 m); Annahme: geographische Meile"},
    ],
    "datasets": [
        {"name": "urban_rural", "title": {"de": "Städtische und ländliche Bevölkerung", "en": "Urban and rural population"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("urban", "Städte", "Towns", "integer", "Personen"),
             col("rural", "Landorte", "Rural places", "integer", "Personen", False, "Fürstenthum 1867: 59052 nach S. 97/99 (S. 95 druckt 58052)"),
             col("total", "Summe der Bevölkerung", "Total population", "integer", "Personen"),
             col("urban_pct", "Städtische Bevölkerung", "Urban population", "number", "%"),
             col("rural_pct", "Ländliche Bevölkerung", "Rural population", "number", "%"),
         ],
         "rows": urban_rural, "source_refs": refs(("95", "b4", "r3-r25"), ("97", "b3", "r10"))},
        {"name": "places_long", "title": {"de": "Einwohner der Städte und größeren Landorte", "en": "Inhabitants of the towns and larger villages"},
         "columns": [
             col("place", "Ort", "Place", "string"),
             col("kind", "Art", "Type", "string", None, False, "Stadt oder Landort"),
             col("year", "Jahr", "Year", "integer"),
             col("population", "Einwohner", "Inhabitants", "integer", "Personen"),
         ],
         "rows": places_long, "source_refs": refs(("96", "b3", "r3-r8"), ("96", "b5", "r2-r9"))},
        {"name": "place_growth", "title": {"de": "Vermehrung der Orte seit 1647", "en": "Growth of the places since 1647"},
         "columns": [
             col("place", "Ort", "Place", "string"),
             col("kind", "Art", "Type", "string"),
             col("pop_1647", "Einwohner 1647", "Inhabitants 1647", "integer", "Personen"),
             col("pop_1867", "Einwohner 1867", "Inhabitants 1867", "integer", "Personen"),
             col("factor_computed", "Vermehrung um das …fache (berechnet)", "Growth factor (computed)", "number", "×", True),
             col("factor_printed", "Vermehrung um das …fache (gedruckt)", "Growth factor (printed)", "number", "×"),
         ],
         "rows": place_growth, "source_refs": refs(("96", "b3", "r3-r8"), ("96", "b5", "r2-r9"))},
        {"name": "settlement_classes", "title": {"de": "Bevölkerung und Dichte nach Siedlungsgröße", "en": "Population and density by settlement size"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("class", "Siedlungsklasse", "Settlement class", "string"),
             col("population", "Bevölkerung", "Population", "integer", "Personen"),
             col("density_sqm", "Dichte auf 1 ☐Meile", "Density per square mile", "number", "Einw./☐Meile"),
             col("density_km2", "Dichte je km²", "Density per km²", "number", "Einw./km²", True),
         ],
         "rows": classes, "source_refs": refs(("97", "b3", "r3-r19"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "urban_rural",
         "title": {"de": "Anteil der Stadtbevölkerung 1833–1867", "en": "Urban share of the population, 1833–1867"},
         "caption": {"de": "Anteil der Einwohner der Städte an der Gesamtbevölkerung in Prozent (gedruckte Werte). Im Fürstenthum bleibt er bei rund einem Drittel; Gera wird städtischer, Schleiz und Lobenstein-Ebersdorf werden ländlicher.",
                     "en": "Share of the inhabitants of the towns in the total population, per cent (printed values). In the principality it stays at about one third; Gera becomes more urban, Schleiz and Lobenstein-Ebersdorf more rural."},
         "vegalite": {
             "height": 320,
             "transform": [DIST_TRANSFORM],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                 "y": {"field": "urban_pct", "type": "quantitative", "title": {"de": "Städtische Bevölkerung (%)", "en": "Urban population (%)"}, "scale": {"zero": False}},
                 "color": color_dist(),
                 "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"),
                             tt_fmt("urban_pct", "Stadtanteil (%)", "Urban share (%)", ".2f"),
                             tt_fmt("urban", "Stadtbevölkerung", "Urban population", ","), tt_fmt("total", "Gesamtbevölkerung", "Total population", ",")]}}},
        {"id": "c2", "dataset": "places_long",
         "title": {"de": "Die sechs Städte 1647, 1833 und 1867", "en": "The six towns in 1647, 1833 and 1867"},
         "caption": {"de": "Einwohner je Stadt (logarithmische Achse). Gera, Schleiz und Lobenstein behalten ihre Rangfolge; Hirschberg überholt Tanna und Saalburg. Lobenstein schrumpft nach 1833.",
                     "en": "Inhabitants per town (logarithmic axis). Gera, Schleiz and Lobenstein keep their order; Hirschberg overtakes Tanna and Saalburg. Lobenstein shrinks after 1833."},
         "vegalite": {
             "height": 340,
             "transform": [{"filter": "datum.kind == 'Stadt'"}],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "quantitative", "title": YEAR, "scale": {"domain": [1640, 1875]}, "axis": {"format": "d", "labelAngle": 0, "values": [1647, 1700, 1750, 1800, 1833, 1867]}},
                 "y": {"field": "population", "type": "quantitative", "title": {"de": "Einwohner (log.)", "en": "Inhabitants (log)"}, "scale": {"type": "log", "domain": [100, 20000]}, "axis": {"values": [100, 200, 500, 1000, 2000, 5000, 10000, 20000], "format": ","}},
                 "color": {"field": "place", "type": "nominal", "scale": {"domain": TOWN_KEYS}, "legend": {"title": None}},
                 "tooltip": [tt("place", "Stadt", "Town"), tt("year", "Jahr", "Year"), tt_fmt("population", "Einwohner", "Inhabitants", ",")]}}},
        {"id": "c3", "dataset": "place_growth",
         "title": {"de": "Vermehrung der Städte und größeren Landorte seit 1647", "en": "Growth of the towns and larger villages since 1647"},
         "caption": {"de": "Faktor, um den die Einwohnerzahl 1867 größer war als 1647 (aus den gedruckten Zahlen berechnet). Die kleinen Ausgangszahlen von 1647 (Ebersdorf 81, Hirschberg 180, Triebes 180) erzeugen die höchsten Faktoren.",
                     "en": "Factor by which the number of inhabitants in 1867 exceeded that of 1647 (computed from the printed figures). The small starting populations of 1647 (Ebersdorf 81, Hirschberg 180, Triebes 180) produce the highest factors."},
         "vegalite": {
             "height": 380,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "place", "type": "nominal", "title": None, "sort": "-x"},
                 "x": {"field": "factor_computed", "type": "quantitative", "title": {"de": "Vermehrung um das …fache", "en": "Growth factor (×)"}},
                 "color": {"field": "kind", "type": "nominal", "scale": {"domain": ["Stadt", "Landort"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label == 'Stadt' ? 'Stadt' : 'Landort'", "en": "datum.label == 'Stadt' ? 'Town' : 'Village'"}}},
                 "tooltip": [tt("place", "Ort", "Place"), tt_fmt("pop_1647", "Einwohner 1647", "Inhabitants 1647", ","), tt_fmt("pop_1867", "Einwohner 1867", "Inhabitants 1867", ","),
                             tt_fmt("factor_computed", "Faktor (berechnet)", "Factor (computed)", ".2f"), tt_fmt("factor_printed", "Faktor (gedruckt)", "Factor (printed)", ".2f")]}}},
        {"id": "c4", "dataset": "settlement_classes",
         "title": {"de": "Einwohner je km² nach Siedlungsklasse 1833 und 1867", "en": "Inhabitants per km² by settlement class, 1833 and 1867"},
         "caption": {"de": "Auf die Gesamtfläche des Bezirks bezogen; die drei Klassen ergeben gestapelt die Gesamtdichte (rechts das ganze Fürstenthum); die Jahreszahl steht über dem Balken. Im Bezirk Gera wächst vor allem die Stadt.",
                     "en": "Related to the total area of the district; the three classes stacked give the overall density (on the right the whole principality); the year is printed above each bar. In the Gera district it is above all the town that grows."},
         "vegalite": {
             "height": 300,
             "layer": [
                 {"transform": [DIST_TRANSFORM, {"calculate": "datum.class == 'Städte' ? 0 : datum.class == '8 Landorte über 1000 E.' ? 1 : 2", "as": "class_order"}],
                  "mark": "bar",
                  "encoding": {
                      "x": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DIST_KEYS},
                            "axis": {"labelAngle": 0, "labelExpr": DIST_LABEL_EXPR}},
                      "xOffset": {"field": "year", "type": "ordinal", "scale": {"domain": [1833, 1867]}},
                      "y": {"field": "density_km2", "type": "quantitative", "title": {"de": "Einwohner je km²", "en": "Inhabitants per km²"}},
                      "color": {"field": "class", "type": "nominal", "scale": {"domain": CLASSES},
                                "legend": {"title": None, "labelLimit": 320, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'Towns' : datum.label == '8 Landorte über 1000 E.' ? '8 rural places over 1,000' : 'Rural places under 1,000'"}}},
                      "order": {"field": "class_order", "type": "quantitative"},
                      "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"), tt("class", "Klasse", "Class"),
                                  tt_fmt("density_km2", "Einw. je km²", "Inh. per km²", ".0f"), tt_fmt("density_sqm", "Einw. je ☐Meile (gedruckt)", "Inh. per sq. mile (printed)", ",.2f"),
                                  tt_fmt("population", "Einwohner", "Inhabitants", ",")]}},
                 {"transform": [{"aggregate": [{"op": "sum", "field": "density_km2", "as": "tot"}], "groupby": ["district", "year"]}],
                  "mark": {"type": "text", "dy": -6, "fontSize": 11},
                  "encoding": {
                      "x": {"field": "district", "type": "nominal", "scale": {"domain": DIST_KEYS}},
                      "xOffset": {"field": "year", "type": "ordinal", "scale": {"domain": [1833, 1867]}},
                      "y": {"field": "tot", "type": "quantitative"},
                      "text": {"field": "year", "type": "ordinal"}}},
             ]}},
    ],
    "transcription_issues": [
        {"page": "95", "block": "b4", "cell": "r25c3", "transcribed": "58052", "facsimile": "58052", "checked_facsimile": True,
         "note": "Druckfehler im Original; richtig 59052 (S. 97, S. 99; 28922 + 59052 = 87974). Transkription entspricht dem Druck."},
        {"page": "97", "block": "b3", "cell": "r9c5", "transcribed": "46603", "facsimile": "46603", "checked_facsimile": True,
         "note": "Druckfehler im Original; 9945 + 36660 = 46605 (S. 95). Transkription entspricht dem Druck."},
    ],
    "keywords": {"de": ["Stadt und Land", "Stadtbevölkerung", "Landbevölkerung", "Städte", "Gera", "Schleiz", "Lobenstein", "Hirschberg", "Tanna", "Saalburg", "Ebersdorf", "Hohenleuben", "Untermhaus", "Verstädterung"],
                 "en": ["town and country", "urban population", "rural population", "towns", "villages", "Gera", "Schleiz", "Lobenstein", "urbanisation"]},
    "related": ["bevoelkerung-entwicklung-1647-1867", "bevoelkerung-gemeindegroessen-1867"],
}
write(ana)
