"""A06 / analysis 2: population and family density 1834-1867, comparison with other German states (pp. 93-94)."""
from common import *

print("km per Meile", MEILE_KM, "km2 per SqMeile", SQM_KM2)

keys = DIST_KEYS
g = grid("93", "b4")
density = []
for r in g[1:]:
    y = int(r[0])
    for i, k in enumerate(keys):
        fam, inh = num(r[1 + 2 * i]), num(r[2 + 2 * i])
        density.append([k, y, fam, inh, round(inh / SQM_KM2, 1)])

g = grid("93", "b2")
famsize = []
for r in g[1:]:
    y = int(r[0])
    for k, c in zip(keys, (1, 2, 3, 6)):
        v = num(r[c])
        if v is not None:
            famsize.append([k, y, v])

STATES_EN = {
    "Königreich Sachsen": ("Sachsen (Kgr.)", "Kingdom of Saxony"),
    "Fürstenthum Reuß ä. L.": ("Reuß ä. L.", "Reuss (elder line)"),
    "Herzogthum S.-Altenburg": ("S.-Altenburg", "Saxe-Altenburg"),
    "Fürstenthum Reuß j. L.": ("Reuß j. L.", "Reuss (younger line)"),
    "Fürstenthum Lippe-Detmold": ("Lippe-Detmold", "Lippe-Detmold"),
    "Großherzogthum Baden": ("Baden", "Baden"),
    "Königreich Würtemberg": ("Württemberg", "Württemberg"),
    "Herzogthum Braunschweig": ("Braunschweig", "Brunswick"),
    "Fürstenthum Schwarzburg-Sondershausen": ("Schwarzburg-Sondershausen", "Schwarzburg-Sondershausen"),
    "Großherzogthum S.-Weimar": ("S.-Weimar", "Saxe-Weimar"),
    "Fürstenthum Schwarzburg-Rudolstadt": ("Schwarzburg-Rudolstadt", "Schwarzburg-Rudolstadt"),
    "Herzogthum Anhalt": ("Anhalt", "Anhalt"),
    "Herzogthum Meiningen": ("S.-Meiningen", "Saxe-Meiningen"),
    "Fürstenthum Schaumburg-Lippe": ("Schaumburg-Lippe", "Schaumburg-Lippe"),
    "Königreich Preußen incl. Lauenburg": ("Preußen (incl. Lauenburg)", "Prussia (incl. Lauenburg)"),
    "Königreich Bayern": ("Bayern", "Bavaria"),
    "Großherzogthum Oldenburg": ("Oldenburg", "Oldenburg"),
    "Großherzogthum Mecklenburg-Schwerin": ("Mecklenburg-Schwerin", "Mecklenburg-Schwerin"),
    "Großherzogthum Mecklenburg-Strelitz": ("Mecklenburg-Strelitz", "Mecklenburg-Strelitz"),
}
g = grid("94", "b1")
states = []
devs = []
for r in g[1:]:
    name = r[0]
    area = num(r[1])
    inh = int(r[2].replace(",", ""))   # "2,423586" = 2 423 586
    dens = num(r[3])
    comp = inh / area
    devs.append((name, dens, comp, (dens / comp - 1) * 100))
    states.append([name, "Reuß j. L." if "Reuß j. L." in name else "übrige", area, inh, dens, round(dens / SQM_KM2, 1)])
assert all(s[0] in STATES_EN for s in states)
STATE_TRANSFORM = relabel("state", "state_label", STATES_EN)

# ---- numbers for prose
D = {(r[0], r[1]): r for r in density}
inh1867 = {k: D[(k, 1867)][3] for k in keys}
km1867 = {k: D[(k, 1867)][4] for k in keys}
inc = {k: (D[(k, 1867)][3] / D[(k, 1834)][3] - 1) * 100 for k in keys}
rank = sorted(states, key=lambda s: -s[4])
pos = [s[0] for s in rank].index("Fürstenthum Reuß j. L.") + 1
assert inh1867["Gera"] > 2 * inh1867["Schleiz"] and inh1867["Gera"] > 2 * inh1867["Lobenstein-Ebersdorf"]
print("rank", pos, [(s[0], s[4]) for s in rank[:5]])
fs = {(r[0], r[1]): r[2] for r in famsize}
fs_prin = [(r[1], r[2]) for r in famsize if r[0] == "Fürstenthum"]
fmin = min(fs_prin, key=lambda t: t[1])
fmax = max(fs_prin, key=lambda t: t[1])
lobmax = max([(r[1], r[2]) for r in famsize if r[0] == "Lobenstein-Ebersdorf"], key=lambda t: t[1])
bad_states = sorted([d for d in devs if abs(d[3]) > 0.45], key=lambda d: -abs(d[3]))
print("state deviations", [(d[0], round(d[3], 2)) for d in bad_states])
sax = next(s for s in states if s[0] == "Königreich Sachsen")
meck = next(s for s in states if s[0] == "Großherzogthum Mecklenburg-Strelitz")
print(sax[4], meck[4])

ana = {
    "id": "bevoelkerung-dichte-1834-1867",
    "title": {"de": "Bevölkerungs- und Familiendichte 1834–1867", "en": "Population and family density, 1834–1867"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("93", "b2", "r2-r14"), ("93", "b4", "r2-r6"), ("93", "b5"), ("94", "b1", "r2-r20")),
    "summary": {
        "de": f"Brückner gibt die Zahl der Einwohner und Familien je Quadratmeile für die drei Landrathsbezirke und das Fürstenthum für fünf Zählungen von 1834 bis 1867 an, dazu die durchschnittliche Familiengröße und einen Vergleich mit 18 anderen deutschen Staaten. Die Dichte stieg im ganzen Land, am stärksten im Bezirk Gera; im Vergleich der Staaten liegt das Fürstenthum Reuß j. L. an {pos}. Stelle von {len(states)}.",
        "en": f"Brückner gives the number of inhabitants and families per square mile for the three districts and the principality in five censuses from 1834 to 1867, together with the average family size and a comparison with 18 other German states. Density rose throughout the country, most strongly in the district of Gera; in the comparison of states the Principality of Reuss (younger line) ranks {pos}{'th' if pos > 3 else ''} of {len(states)}.",
    },
    "method": {
        "de": f"Übernommen wurden die Tabellen »Familiendichtigkeit« (Seelen je Familie) und »Bevölkerungsdichtigkeit« (Familien und Einwohner auf 1 ☐Meile) auf S. 93 sowie die Staatentabelle auf S. 94. Die Einwohnerzahlen dieser Tabelle druckt Brückner mit Komma als Tausendertrenner (2,423586 = 2 423 586); sie wurden als ganze Zahlen übernommen. Umgerechnet wurde die Dichte in Einwohner je km²: Brückners Tabelle auf S. 832 gibt 1 geographische Meile = 0,9894 künftige Meile (zu 7 500 m), also {de(MEILE_KM,4)} km und 1 ☐Meile = {de(SQM_KM2,2)} km². Brückner nennt die Meile nicht näher; angenommen wird die in der deutschen Statistik der Zeit übliche geographische Quadratmeile. Aus den Tabellen folgen die Flächen der Bezirke (Einwohner : Dichte): Gera 4,03, Schleiz 6,03, Lobenstein-Ebersdorf 5,00, zusammen 15,06 ☐Meilen (S. 8: 4,03 für Gera, 15,06 für das Land nach der preußischen Berechnung von Nowack), das wären rund {de(15.06*SQM_KM2,0)} km².",
        "en": f"Taken over are the tables “family density” (persons per family) and “population density” (families and inhabitants per square mile) on p. 93 and the table of states on p. 94. Brückner prints the inhabitants of that table with a comma as thousands separator (2,423586 = 2,423,586); they were entered as integers. Density was converted to inhabitants per km²: Brückner's table on p. 832 gives 1 geographical mile = 0.9894 future mile (of 7,500 m), i.e. {en(MEILE_KM,4)} km, so 1 square mile = {en(SQM_KM2,2)} km². Brückner does not specify the mile; the geographical square mile, customary in German statistics of the time, is assumed. The tables imply the areas of the districts (inhabitants ÷ density): Gera 4.03, Schleiz 6.03, Lobenstein-Ebersdorf 5.00, together 15.06 square miles (p. 8: 4.03 for Gera and 15.06 for the country according to Nowack's Prussian calculation), i.e. about {en(15.06*SQM_KM2,0)} km².",
    },
    "findings": [
        {"de": f"1867 lebten im Bezirk Gera {de(km1867['Gera'],0)} Einwohner auf dem km² ({de(inh1867['Gera'],0)} je ☐Meile), in Schleiz {de(km1867['Schleiz'],0)} und in Lobenstein-Ebersdorf {de(km1867['Lobenstein-Ebersdorf'],0)}; das Fürstenthum insgesamt {de(km1867['Fürstenthum'],0)}.",
         "en": f"In 1867 the district of Gera had {en(km1867['Gera'],0)} inhabitants per km² ({en(inh1867['Gera'],0)} per square mile), Schleiz {en(km1867['Schleiz'],0)} and Lobenstein-Ebersdorf {en(km1867['Lobenstein-Ebersdorf'],0)}; the principality as a whole {en(km1867['Fürstenthum'],0)}."},
        {"de": f"Seit 1834 stieg die Dichte in Gera um {de(inc['Gera'],0)} %, in Schleiz um {de(inc['Schleiz'],0)} %, in Lobenstein-Ebersdorf um {de(inc['Lobenstein-Ebersdorf'],0)} % (Fürstenthum {de(inc['Fürstenthum'],0)} %); Lobenstein-Ebersdorf bleibt seit 1852 bei etwa 4 470 Einwohnern je ☐Meile.",
         "en": f"Since 1834 density has risen by {en(inc['Gera'],0)} % in Gera, {en(inc['Schleiz'],0)} % in Schleiz and {en(inc['Lobenstein-Ebersdorf'],0)} % in Lobenstein-Ebersdorf (principality {en(inc['Fürstenthum'],0)} %); Lobenstein-Ebersdorf has stayed at about 4,470 inhabitants per square mile since 1852."},
        {"de": f"Unter den 19 verglichenen Staaten steht das Fürstenthum Reuß j. L. mit {de(next(s for s in states if s[0]=='Fürstenthum Reuß j. L.')[4],0)} Einwohnern je ☐Meile an {pos}. Stelle, hinter dem Königreich Sachsen ({de(sax[4],0)}), Reuß ä. L. und S.-Altenburg; am dünnsten besiedelt ist Mecklenburg-Strelitz ({de(meck[4],0)}).",
         "en": f"Among the 19 states compared, the Principality of Reuss (younger line) ranks {pos}th with {en(next(s for s in states if s[0]=='Fürstenthum Reuß j. L.')[4],0)} inhabitants per square mile, behind the Kingdom of Saxony ({en(sax[4],0)}), Reuss (elder line) and Saxe-Altenburg; Mecklenburg-Strelitz is the least densely settled ({en(meck[4],0)})."},
        {"de": f"Die Familie hat im Fürstenthum durchgehend 4,4 bis 4,9 Köpfe: 1647 gab Brückner 4,50 an, 1846 war mit {de(fmax[1],2)} der höchste und 1864 mit {de(fmin[1],2)} der niedrigste Wert; in Lobenstein-Ebersdorf erreichte sie 1846 {de(lobmax[1],2)}.",
         "en": f"Throughout the principality the family has 4.4 to 4.9 members: Brückner gives 4.50 for 1647, the highest value was {en(fmax[1],2)} in {fmax[0]}, the lowest {en(fmin[1],2)} in {fmin[0]}; in Lobenstein-Ebersdorf it reached {en(lobmax[1],2)} in {lobmax[0]}."},
    ],
    "caveats": [
        {"de": "Unstimmigkeiten im gedruckten Original (Transkription und Faksimile stimmen überein): Die Dichte für Schleiz 1852 (4 324,07) passt nicht zu den 25 074 Einwohnern von S. 91 (ergäbe 4 158); die Familiendichte für Gera 1867 (1 984,11) ergibt mit 8 094 Familien 2 008; die 1867er Dichte des Fürstenthums (5 853,22) entspricht einer Fläche von 15,03 statt der gedruckten 15,06 ☐Meilen. Auch die Dichte einzelner Staaten weicht von Einwohner : Fläche ab (am stärksten Schaumburg-Lippe: gedruckt 3 952, errechnet 3 874); gerechnet wurde mit den gedruckten Werten.",
         "en": "Inconsistencies in the printed original (transcription and facsimile agree): the density for Schleiz in 1852 (4,324.07) does not fit the 25,074 inhabitants of p. 91 (which would give 4,158); the family density of Gera in 1867 (1,984.11) corresponds to 2,008 with 8,094 families; the 1867 density of the principality (5,853.22) corresponds to an area of 15.03 instead of the printed 15.06 square miles. The density of individual states also deviates from inhabitants ÷ area (most for Schaumburg-Lippe: printed 3,952, computed 3,874); the printed values were used."},
        {"de": "Die Umrechnung in km² beruht auf der Annahme, dass Brückner die geographische Quadratmeile (55,06 km²) meint; wäre die preußische Meile (7,532 km) gemeint, lägen alle km²-Werte um etwa 3 % niedriger. Die Vergleiche zwischen den Staaten und Bezirken sind davon nicht berührt.",
         "en": "The conversion to km² assumes that Brückner means the geographical square mile (55.06 km²); if the Prussian mile (7.532 km) were meant, all km² values would be about 3 % lower. Comparisons between states and districts are not affected."},
        {"de": "Die gedruckte Familiengröße weicht gelegentlich von Einwohner : Familien nach S. 91 ab (z. B. Schleiz 1840: 4,67 gedruckt, 4,88 errechnet).",
         "en": "The printed family size occasionally differs from inhabitants ÷ families on p. 91 (e.g. Schleiz 1840: 4.67 printed, 4.88 computed)."},
        {"de": "Brückner vergleicht Zahlen unterschiedlicher Jahre (die Staatentabelle trägt kein Jahr; für Reuß j. L. ist es die Zählung 1867); »Familie« bezeichnet die Haushaltsfamilie der Zählung, nicht notwendig Verwandte.",
         "en": "Brückner compares figures of different years (the table of states carries no year; for Reuss j. L. it is the 1867 count); “family” means the household family of the census, not necessarily kin."},
    ],
    "conversions": [
        {"from": "☐Meile (geographische Quadratmeile)", "to": "km²",
         "factor_or_formula": f"1 ☐Meile = (0,9894 × 7,5 km)² = {SQM_KM2:.2f} km²",
         "reference": "Brückner S. 832: 1 geographische Meile = 0,9894 künftige Meile (zu 7500 m)"},
    ],
    "datasets": [
        {"name": "density", "title": {"de": "Dichte der Bevölkerung und der Familien", "en": "Density of inhabitants and families"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("families_per_sqm", "Familien je ☐Meile", "Families per square mile", "number", "Familien/☐Meile"),
             col("inhabitants_per_sqm", "Einwohner je ☐Meile", "Inhabitants per square mile", "number", "Einw./☐Meile"),
             col("inhabitants_per_km2", "Einwohner je km²", "Inhabitants per km²", "number", "Einw./km²", True),
         ],
         "rows": density, "source_refs": refs(("93", "b4", "r2-r6"))},
        {"name": "family_size", "title": {"de": "Seelen auf 1 Familie", "en": "Persons per family"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("persons_per_family", "Seelen auf 1 Familie", "Persons per family", "number", "Personen"),
         ],
         "rows": famsize, "source_refs": refs(("93", "b2", "r2-r14"))},
        {"name": "states", "title": {"de": "Bevölkerungsdichte deutscher Staaten", "en": "Population density of German states"},
         "columns": [
             col("state", "Staat (Original)", "State (original)", "string"),
             col("group", "Gruppe", "Group", "string", None, True, "Reuß j. L. gegenüber den übrigen Staaten (editorisch)"),
             col("area_sqm", "Fläche", "Area", "number", "☐Meilen"),
             col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen", True, "Brückner druckt z. B. 2,423586 für 2 423 586; als ganze Zahl übernommen"),
             col("density_sqm", "Einwohner auf 1 ☐Meile", "Inhabitants per square mile", "number", "Einw./☐Meile"),
             col("density_km2", "Einwohner je km²", "Inhabitants per km²", "number", "Einw./km²", True),
         ],
         "rows": states, "source_refs": refs(("94", "b1", "r2-r20"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "density",
         "title": {"de": "Einwohner je km² nach Landrathsbezirken", "en": "Inhabitants per km² by district"},
         "caption": {"de": f"Aus Brückners Angaben je ☐Meile umgerechnet (1 ☐Meile = {de(SQM_KM2,2)} km²). Gera ist 1867 mehr als doppelt so dicht besiedelt wie Schleiz und Lobenstein-Ebersdorf.",
                     "en": f"Converted from Brückner's figures per square mile (1 square mile = {en(SQM_KM2,2)} km²). In 1867 Gera is more than twice as densely settled as Schleiz and Lobenstein-Ebersdorf."},
         "vegalite": {
             "height": 320,
             "transform": [DIST_TRANSFORM],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                 "y": {"field": "inhabitants_per_km2", "type": "quantitative", "title": {"de": "Einwohner je km²", "en": "Inhabitants per km²"}, "scale": {"zero": False}},
                 "color": color_dist(),
                 "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"),
                             tt_fmt("inhabitants_per_km2", "Einwohner je km²", "Inhabitants per km²", ".1f"),
                             tt_fmt("inhabitants_per_sqm", "Einwohner je ☐Meile (gedruckt)", "Inhabitants per sq. mile (printed)", ",.2f")]}}},
        {"id": "c2", "dataset": "states",
         "title": {"de": "Bevölkerungsdichte deutscher Staaten (Brückner)", "en": "Population density of German states (Brückner)"},
         "caption": {"de": "Einwohner je km², sortiert nach der Dichte. Das Fürstenthum Reuß j. L. ist hervorgehoben.",
                     "en": "Inhabitants per km², sorted by density. The Principality of Reuss (younger line) is highlighted."},
         "vegalite": {
             "height": 420,
             "transform": [STATE_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "state_label", "type": "nominal", "title": None, "sort": "-x", "axis": {"labelLimit": 300}},
                 "x": {"field": "density_km2", "type": "quantitative", "title": {"de": "Einwohner je km²", "en": "Inhabitants per km²"}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige", "Reuß j. L."]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label == 'übrige' ? 'übrige Staaten' : 'Reuß j. L.'", "en": "datum.label == 'übrige' ? 'other states' : 'Reuss (younger line)'"}}},
                 "tooltip": [tt("state_label", "Staat", "State"),
                             tt_fmt("density_km2", "Einwohner je km²", "Inhabitants per km²", ".0f"),
                             tt_fmt("density_sqm", "Einw. je ☐Meile (gedruckt)", "Inh. per sq. mile (printed)", ","),
                             tt_fmt("area_sqm", "Fläche (☐Meilen)", "Area (sq. miles)", ",.2f"),
                             tt_fmt("inhabitants", "Einwohner", "Inhabitants", ",")]}}},
        {"id": "c3", "dataset": "family_size",
         "title": {"de": "Seelen auf 1 Familie 1834–1867", "en": "Persons per family, 1834–1867"},
         "caption": {"de": "Durchschnittliche Zahl der Personen je Familie nach Brückners Tabelle (Lobenstein-Ebersdorf ab 1837). Die gestrichelte Linie markiert den Wert für das Fürstenthum im Jahr 1647 (4,50).",
                     "en": "Average number of persons per family according to Brückner's table (Lobenstein-Ebersdorf from 1837). The dashed rule marks the value for the principality in 1647 (4.50)."},
         "vegalite": {
             "height": 320,
             "transform": [DIST_TRANSFORM],
             "layer": [
                 {"transform": [{"filter": "datum.year >= 1834"}],
                  "mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                      "y": {"field": "persons_per_family", "type": "quantitative", "title": {"de": "Personen je Familie", "en": "Persons per family"}, "scale": {"zero": False}},
                      "color": color_dist(),
                      "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"),
                                  tt_fmt("persons_per_family", "Personen je Familie", "Persons per family", ".2f")]}},
                 {"transform": [{"filter": "datum.year == 1647"}],
                  "mark": {"type": "rule", "strokeDash": [4, 3]},
                  "encoding": {"y": {"field": "persons_per_family", "type": "quantitative"}}},
             ]}},
    ],
    "keywords": {"de": ["Bevölkerungsdichte", "Einwohner je Quadratmeile", "Familiengröße", "Familiendichte", "Dichte", "Quadratmeile", "Sachsen", "Staatenvergleich"],
                 "en": ["population density", "inhabitants per square mile", "family size", "density", "square mile", "comparison of states"]},
    "related": ["bevoelkerung-entwicklung-1647-1867"],
}
write(ana)
