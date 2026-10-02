"""A06 / analysis 5: size classes of the political municipalities 1867 (p. 98, block b1)."""
from common import *

g = grid("98", "b1")
CLASSES = ["1–500", "500–1000", "1000–2000", "2000–3000", "3000–4000", "4000–5000", "16000–17000"]
CLASS_EN = {"1–500": "1–500", "500–1000": "500–1,000", "1000–2000": "1,000–2,000", "2000–3000": "2,000–3,000",
            "3000–4000": "3,000–4,000", "4000–5000": "4,000–5,000", "16000–17000": "16,000–17,000"}
assert [x for x in g[0][2:9]] == ["1—500.", "500 bis 1000.", "1000 bis 2000.", "2000 bis 3000.", "3000 bis 4000.", "4000 bis 5000.", "16000 bis 17000."], g[0]


def pair(cell):
    a, b = cell.split("\n")
    return integer(a), integer(b)


size_rows = []
sums = {}
for r in g[1:4]:
    d = {"Gera . . .": "Gera", "Schleiz . .": "Schleiz", "Lobenstein-Ebersdorf": "Lobenstein-Ebersdorf"}[r[0]]
    tot_pl = tot_pop = 0
    for i, c in enumerate(CLASSES):
        n, pop = pair(r[2 + i])
        size_rows.append([d, c, i + 1, n, pop])
        tot_pl += n or 0
        tot_pop += pop or 0
    n, pop = pair(r[9])
    assert (tot_pl, tot_pop) == (n, pop), (d, tot_pl, tot_pop, n, pop)
    sums[d] = (n, pop)

# principality row + printed percentages and per-municipality averages
r5, r6, r7 = g[4], g[5], g[6]
prin_rows = []
tp = tpop = 0
for i, c in enumerate(CLASSES):
    n, pop = pair(r5[2 + i])
    share_pop = num(r6[2 + i])
    per = num(r7[2 + i])
    prin_rows.append([c, i + 1, n, pop, share_pop, per])
    tp += n or 0
    tpop += pop or 0
n_all, pop_all = pair(r5[9])
assert (tp, tpop) == (n_all, pop_all)
# principality = sum of districts
for i, c in enumerate(CLASSES):
    s_n = sum((x[3] or 0) for x in size_rows if x[1] == c)
    s_p = sum((x[4] or 0) for x in size_rows if x[1] == c)
    assert (s_n, s_p) == (prin_rows[i][2] or 0, prin_rows[i][3] or 0), c
# derived: share of municipalities per class (%), printed share of population recomputed
final_prin = []
for c, o, n, pop, sp, per in prin_rows:
    share_pl = round((n or 0) / n_all * 100, 2)
    final_prin.append([c, o, n, pop, share_pl, sp, per])
    if pop:
        chk = round(pop / pop_all * 100, 2)
        assert abs(chk - sp) < 0.011, (c, chk, sp)

# prose numbers
small = prin_rows[0]
under1000_n = sum(p[2] or 0 for p in prin_rows[:2])
under1000_pop = sum(p[3] or 0 for p in prin_rows[:2])
over1000_n = n_all - under1000_n
over1000_pop = pop_all - under1000_pop
print(under1000_n, under1000_pop, over1000_n, over1000_pop)
gera = {c: (n, p) for d, c, o, n, p in size_rows if d == "Gera"}
share_tiny = {d: sum((n or 0) for dd, c, o, n, p in size_rows if dd == d and c == "1–500") / sums[d][0] * 100 for d in sums}
print(share_tiny)
largest = prin_rows[-1]
print(largest, pop_all / n_all)

ana = {
    "id": "bevoelkerung-gemeindegroessen-1867",
    "title": {"de": "Größe der Gemeinden 1867", "en": "Size of the municipalities, 1867"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("98", "b1", "r2-r7"), ("98", "b2"), ("97", "b5"), ("94", "b1", "r3")),
    "summary": {
        "de": f"Brückner verteilt die {n_all} politischen Gemeinden des Fürstenthums nach ihrer Einwohnerzahl auf Größenklassen, getrennt nach Landrathsbezirken. {de(under1000_n,0)} Gemeinden haben weniger als 1000 Einwohner, nur {de(over1000_n,0)} mehr; dennoch leben knapp {de(over1000_pop/pop_all*100,0)} % der Bevölkerung in den größeren Orten, allein {de(largest[4],1)} % in der Stadt Gera.",
        "en": f"Brückner distributes the {n_all} political municipalities of the principality over size classes by population, separately for the districts. {en(under1000_n,0)} municipalities have fewer than 1,000 inhabitants and only {en(over1000_n,0)} have more; nevertheless almost {en(over1000_pop/pop_all*100,0)} % of the population live in the larger places, {en(largest[4],1)} % in the town of Gera alone.",
    },
    "method": {
        "de": "Aus der Tabelle auf S. 98 wurden je Bezirk und Größenklasse die Zahl der Gemeinden und ihre Volksmenge übernommen; die Zellen enthalten untereinander beide Zahlen. Leere Klassen (»—«) bleiben ohne Wert. Brückners Klassengrenzen überlappen in der Schreibung (»500 bis 1000«, »1000 bis 2000«); die Zuordnung der Grenzwerte ist nicht angegeben. Abgeleitet wurde der Anteil der Gemeinden je Klasse an allen 173 Gemeinden; die gedruckten Prozentzahlen der Volksmenge und die Seelenzahl je Gemeinde wurden übernommen und gegen Volksmenge : Gesamtbevölkerung geprüft (alle Werte stimmen). Die Zeilen- und Spaltensummen sowie die Summe der drei Bezirke gleich der Zeile »Fürstenthum« wurden mit Python kontrolliert und stimmen.",
        "en": "From the table on p. 98 the number of municipalities and their population were taken for each district and size class; the cells contain both numbers one below the other. Empty classes (“—”) are left without a value. Brückner's class limits overlap in print (“500 to 1000”, “1000 to 2000”); the assignment of boundary values is not stated. Derived is the share of municipalities per class in all 173 municipalities; the printed percentages of the population and the persons per municipality were taken over and checked against population ÷ total population (all values agree). Row and column sums and the equality of the three districts' sum with the “principality” row were checked in Python and agree.",
    },
    "findings": [
        {"de": f"{de(under1000_n,0)} der {n_all} Gemeinden ({de(under1000_n/n_all*100,1)} %) haben weniger als 1000 Einwohner und vereinen {de(under1000_pop,0)} Personen ({de(under1000_pop/pop_all*100,1)} %); {de(small[2],0)} Gemeinden zählen höchstens 500 Seelen (im Mittel {de(small[5],1)}).",
         "en": f"{en(under1000_n,0)} of the {n_all} municipalities ({en(under1000_n/n_all*100,1)} %) have fewer than 1,000 inhabitants and together hold {en(under1000_pop,0)} persons ({en(under1000_pop/pop_all*100,1)} %); {en(small[2],0)} municipalities have at most 500 souls (on average {en(small[5],1)})."},
        {"de": f"Die {over1000_n} Gemeinden über 1000 Einwohner ({de(over1000_n/n_all*100,1)} % der Gemeinden) umfassen {de(over1000_pop,0)} Einwohner ({de(over1000_pop/pop_all*100,1)} %); Brückner vergleicht diese Zahl mit dem Fürstenthum Reuß ä. L. (43 889 Einwohner).",
         "en": f"The {over1000_n} municipalities of over 1,000 inhabitants ({en(over1000_n/n_all*100,1)} % of the municipalities) comprise {en(over1000_pop,0)} inhabitants ({en(over1000_pop/pop_all*100,1)} %); Brückner compares this figure with the Principality of Reuss (elder line, 43,889 inhabitants)."},
        {"de": f"Zwischen 5000 und 16 000 Einwohnern gibt es keine Gemeinde: Auf die Stadt Gera ({de(largest[3],0)}) folgt Schleiz mit {de(prin_rows[5][3],0)}; im Bezirk Gera sind {de(share_tiny['Gera'],1)} % der Gemeinden kleiner als 500 Einwohner, in Schleiz {de(share_tiny['Schleiz'],1)} %, in Lobenstein-Ebersdorf {de(share_tiny['Lobenstein-Ebersdorf'],1)} %.",
         "en": f"There is no municipality between 5,000 and 16,000 inhabitants: the town of Gera ({en(largest[3],0)}) is followed by Schleiz with {en(prin_rows[5][3],0)}; in the Gera district {en(share_tiny['Gera'],1)} % of the municipalities have fewer than 500 inhabitants, in Schleiz {en(share_tiny['Schleiz'],1)} %, in Lobenstein-Ebersdorf {en(share_tiny['Lobenstein-Ebersdorf'],1)} %."},
    ],
    "caveats": [
        {"de": "Gezählt werden politische (staatsrechtliche) Gemeinden, nicht Ortschaften im Sinne von Siedlungen; mehrere Dörfer können eine Gemeinde bilden und umgekehrt. Die Einwohnerzahlen sind die der Volkszählung von 1867 (Gera 38 252, Schleiz 27 368, Lobenstein-Ebersdorf 22 354).",
         "en": "The unit is the political (constitutional) municipality, not the settlement; several villages may form one municipality. The population figures are those of the 1867 census (Gera 38,252, Schleiz 27,368, Lobenstein-Ebersdorf 22,354)."},
        {"de": "Brückners Text zählt 159 Gemeinden unter und 14 über 1000 Einwohner (45 044 bzw. 42 930 Einwohner); das stimmt mit den Zeilensummen überein.",
         "en": "Brückner's text counts 159 municipalities below and 14 above 1,000 inhabitants (45,044 and 42,930 inhabitants); this agrees with the row sums."},
    ],
    "datasets": [
        {"name": "size_classes", "title": {"de": "Gemeinden nach Größenklassen und Bezirken", "en": "Municipalities by size class and district"},
         "columns": [
             col("district", "Landrathsbezirk", "District", "string"),
             col("size_class", "Größenklasse (Einwohner)", "Size class (inhabitants)", "string"),
             col("class_order", "Klassennummer", "Class number", "integer", None, True, "editorische Ordnung 1–7"),
             col("places", "Zahl der Gemeinden", "Number of municipalities", "integer", "Gemeinden"),
             col("population", "Volksmenge", "Population", "integer", "Personen"),
         ],
         "rows": size_rows, "source_refs": refs(("98", "b1", "r2-r4"))},
        {"name": "size_total", "title": {"de": "Fürstenthum: Gemeinden und Volksmenge nach Größenklassen", "en": "Principality: municipalities and population by size class"},
         "columns": [
             col("size_class", "Größenklasse (Einwohner)", "Size class (inhabitants)", "string"),
             col("class_order", "Klassennummer", "Class number", "integer", None, True, "editorische Ordnung 1–7"),
             col("places", "Zahl der Gemeinden", "Number of municipalities", "integer", "Gemeinden"),
             col("population", "Volksmenge", "Population", "integer", "Personen"),
             col("share_places", "Anteil der Gemeinden", "Share of municipalities", "number", "%", True),
             col("share_population", "Anteil der Volksmenge (gedruckt)", "Share of population (printed)", "number", "%"),
             col("persons_per_place", "Seelen je Gemeinde (gedruckt)", "Persons per municipality (printed)", "number", "Personen"),
         ],
         "rows": final_prin, "source_refs": refs(("98", "b1", "r5-r7"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "size_total",
         "title": {"de": "Gemeinden und Bevölkerung nach Größenklassen", "en": "Municipalities and population by size class"},
         "caption": {"de": "Anteil der Gemeinden und Anteil der Volksmenge je Größenklasse (Fürstenthum, 1867). Die vielen kleinen Gemeinden haben einen kleineren Bevölkerungsanteil als die wenigen großen Orte; zwischen 2000 und 16 000 Einwohnern liegen nur vier Gemeinden.",
                     "en": "Share of the municipalities and share of the population by size class (principality, 1867). The many small municipalities have a smaller share of the population than the few large places; only four municipalities lie between 2,000 and 16,000 inhabitants."},
         "vegalite": {
             "height": 320,
             "transform": [{"fold": ["share_places", "share_population"], "as": ["measure", "pct"]},
                           {"calculate": "datum.pct == null ? 0 : datum.pct", "as": "pct0"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "size_class", "type": "ordinal", "sort": {"field": "class_order", "op": "min"}, "title": {"de": "Einwohner der Gemeinde", "en": "Inhabitants of the municipality"}, "axis": {"labelAngle": 0, "labelExpr": {"de": "datum.label", "en": "replace(datum.label, /(\\d+)(\\d{3})/g, '$1,$2')"}}},
                 "xOffset": {"field": "measure", "type": "nominal", "scale": {"domain": ["share_places", "share_population"]}},
                 "y": {"field": "pct0", "type": "quantitative", "title": {"de": "Anteil (%)", "en": "Share (%)"}},
                 "color": {"field": "measure", "type": "nominal", "scale": {"domain": ["share_places", "share_population"]},
                           "legend": {"title": None, "labelLimit": 320, "labelExpr": {"de": "datum.label == 'share_places' ? 'Anteil der Gemeinden' : 'Anteil der Bevölkerung'", "en": "datum.label == 'share_places' ? 'Share of municipalities' : 'Share of population'"}}},
                 "tooltip": [tt("size_class", "Größenklasse", "Size class"), tt_fmt("places", "Gemeinden", "Municipalities", ","), tt_fmt("population", "Volksmenge", "Population", ","),
                             tt_fmt("share_places", "Anteil Gemeinden (%)", "Share of municipalities (%)", ".2f"), tt_fmt("share_population", "Anteil Volksmenge (%)", "Share of population (%)", ".2f")]}}},
        {"id": "c2", "dataset": "size_classes",
         "title": {"de": "Volksmenge je Größenklasse und Bezirk", "en": "Population by size class and district"},
         "caption": {"de": "Einwohner der Gemeinden einer Größenklasse, nach Bezirken gestapelt. Die Klasse »16000–17000« ist die Stadt Gera; die Klasse »3000–4000« ist unbesetzt.",
                     "en": "Inhabitants of the municipalities of a size class, stacked by district. The class “16,000–17,000” is the town of Gera; the class “3,000–4,000” is empty."},
         "vegalite": {
             "height": 320,
             "transform": [{"filter": "datum.population != null"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "size_class", "type": "ordinal", "scale": {"domain": CLASSES}, "title": {"de": "Einwohner der Gemeinde", "en": "Inhabitants of the municipality"}, "axis": {"labelAngle": 0, "labelExpr": {"de": "datum.label", "en": "replace(datum.label, /(\\d+)(\\d{3})/g, '$1,$2')"}}},
                 "y": {"field": "population", "type": "quantitative", "title": {"de": "Einwohner", "en": "Inhabitants"}},
                 "color": color_dist(domain=["Gera", "Schleiz", "Lobenstein-Ebersdorf"]),
                 "tooltip": [tt("district", "Bezirk", "District"), tt("size_class", "Größenklasse", "Size class"), tt_fmt("places", "Gemeinden", "Municipalities", ","), tt_fmt("population", "Volksmenge", "Population", ",")]}}},
    ],
    "keywords": {"de": ["Gemeinden", "Gemeindegröße", "Größenklassen", "Einwohnerzahl", "Gera", "Schleiz", "Lobenstein", "Ebersdorf", "Dörfer", "Siedlungsstruktur"],
                 "en": ["municipalities", "municipality size", "size classes", "population", "Gera", "Schleiz", "Lobenstein", "villages", "settlement structure"]},
    "related": ["bevoelkerung-stadt-land-1833-1867"],
}
write(ana)
