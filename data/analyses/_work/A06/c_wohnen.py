"""A06 / analysis 3: dwellings, households and house density 1867 (pp. 94-95)."""
import re
from common import *

AREAS = {"Gera": 4.03, "Schleiz": 6.03, "Lobenstein-Ebersdorf": 5.00, "Fürstenthum": 15.06}
POP1867 = {"Gera": 38252, "Schleiz": 27368, "Lobenstein-Ebersdorf": 22354, "Fürstenthum": 87974}

g = grid("94", "b3")
SETTL = ["Städte", "Landorte", "Zusammen"]
houses = []
for r in g[3:]:
    name = "Fürstenthum" if r[0] == "Fürstenthum" else r[0]
    assert name in AREAS, name
    h = [integer(x) for x in r[1:4]]
    fam = [num(x) for x in r[4:7]]
    per = [num(x) for x in r[7:10]]
    assert h[0] + h[1] == h[2]
    for i, s in enumerate(SETTL):
        houses.append([name, s, h[i], fam[i], per[i]])
    # check: inhabitants per house (all) = population / houses
    print(name, "persons/house", round(POP1867[name] / h[2], 2), per[2])

# houses per square mile: districts (p. 95 b1) and other countries (p. 95 b2)
t1 = block("95", "b1")["text"]
t2 = block("95", "b2")["text"]
hps = []
vals = re.findall(r"(\d+,\d) ", t1)
print("p95 b1 values", vals)
dist_vals = {"Gera": num(vals[0]), "Lobenstein-Ebersdorf": num(vals[1]), "Schleiz": num(vals[2]), "Fürstenthum": num(vals[3])}
for k, v in dist_vals.items():
    hh = next(x[2] for x in houses if x[0] == k and x[1] == "Zusammen")
    print(k, v, round(hh / AREAS[k], 1))
other_text = t2.split("☐ Meile:")[1]
others = re.findall(r"([A-Za-zäöüÄÖÜß\-\. ]+?)[ \.]{2,}\s*(\d+(?:,\d)?)\s*(?:Häuser|\")", other_text.replace("\n", " "))
others = [(n.strip(" ."), num(v)) for n, v in others]
print(others)
assert len(others) == 8, others
OTH = {"Belgien": ("Belgien", "Belgium"), "Sachsen": ("Sachsen", "Saxony"), "Reuß j. L.": None,
       "Coburg-Gotha": ("Coburg-Gotha", "Coburg-Gotha"), "Baden": ("Baden", "Baden"), "Württemberg": ("Württemberg", "Württemberg"),
       "Beide Schwarzburg": ("Beide Schwarzburg", "Both Schwarzburgs"), "Bayern": ("Bayern", "Bavaria")}
place_rows = []
LAB = {"Gera": ("Bezirk Gera", "Gera district"), "Schleiz": ("Bezirk Schleiz", "Schleiz district"),
       "Lobenstein-Ebersdorf": ("Bezirk Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf district"),
       "Fürstenthum": ("Reuß j. L. (Fürstenthum)", "Reuss j. L. (principality)")}
mapping = {}
for k in ("Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstenthum"):
    place_rows.append([k, "Reuß j. L.", dist_vals[k], round(dist_vals[k] / SQM_KM2, 1)])
    mapping[k] = LAB[k]
for n, v in others:
    if n.startswith("Reuß"):
        assert abs(v - dist_vals["Fürstenthum"]) < 1e-9
        continue
    key = {"Württemberg": "Württemberg"}.get(n, n)
    place_rows.append([n, "übrige", v, round(v / SQM_KM2, 1)])
    mapping[n] = OTH[n]
PLACE_TRANSFORM = relabel("place", "place_label", mapping)

# persons per house in other states (p. 94 b4, running text)
t94 = block("94", "b4")["text"]
thur = num(re.search(r"im Durchschnitte (\d,\d\d)", t94).group(1))
bay = num(re.search(r"Bayern, wo (\d,\d\d)", t94).group(1))
sax = num(re.search(r"Sachsen, wo (\d,\d\d)", t94).group(1))
reuss_pph = next(x[4] for x in houses if x[0] == "Fürstenthum" and x[1] == "Zusammen")
compare = [["Thüringen (Durchschnitt)", "übrige", thur], ["Bayern", "übrige", bay], ["Fürstenthum Reuß j. L.", "Reuß j. L.", reuss_pph], ["Sachsen", "übrige", sax]]
CMP_TRANSFORM = relabel("region", "region_label", {
    "Thüringen (Durchschnitt)": ("Thüringen (Durchschnitt)", "Thuringia (average)"), "Bayern": ("Bayern", "Bavaria"),
    "Fürstenthum Reuß j. L.": ("Reuß j. L.", "Reuss j. L."), "Sachsen": ("Sachsen", "Saxony")})
print(compare)

H = {(r[0], r[1]): r for r in houses}
town_g, rural_g = H[("Gera", "Städte")][4], H[("Gera", "Landorte")][4]
town_f, rural_f = H[("Fürstenthum", "Städte")][4], H[("Fürstenthum", "Landorte")][4]
fam_g = H[("Gera", "Städte")][3]
hp = {r[0]: r[2] for r in place_rows}
hp_oth = {r[0]: r[2] for r in place_rows if r[1] == "übrige"}
ratio_town = [(k, H[(k, "Städte")][4]) for k in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")]
print(ratio_town)
assert hp["Gera"] > hp_oth["Sachsen"] > hp["Fürstenthum"] > hp_oth["Coburg-Gotha"]

ana = {
    "id": "wohnen-wohnhaeuser-wohndichte-1867",
    "title": {"de": "Wohnhäuser und Wohndichte 1867", "en": "Dwellings and housing density, 1867"},
    "category": "housing",
    "section": SECTION,
    "sources": refs(("94", "b3", "r4-r7"), ("94", "b4"), ("95", "b1"), ("95", "b2")),
    "summary": {
        "de": f"Für 1867 gibt Brückner die bewohnten Häuser der Landestheile, getrennt nach Städten und Landorten, die Zahl der Familien und Einwohner je Wohnhaus sowie die Häuser je Quadratmeile im Vergleich mit anderen Ländern an. Das städtische Haus beherbergt mit {de(town_f,1)} Personen deutlich mehr Menschen als das ländliche ({de(rural_f,1)}), am meisten in Gera ({de(town_g,1)}).",
        "en": f"For 1867 Brückner gives the inhabited houses of the districts, separated into towns and rural places, the number of families and inhabitants per dwelling house, and the houses per square mile in comparison with other countries. The urban house holds {en(town_f,1)} persons on average, markedly more than the rural one ({en(rural_f,1)}), most of all in Gera ({en(town_g,1)}).",
    },
    "method": {
        "de": f"Übernommen wurden die Tabelle »Bevölkerungsdichtigkeit in Bezug auf die Wohnungen« (S. 94), die Häuser je ☐Meile für die Landestheile (S. 95, Textblock) und die Vergleichszahlen anderer Länder (S. 95; Durchschnittswerte Thüringens, Bayerns und Sachsens aus dem Text auf S. 94). Die Häuser je ☐Meile wurden zusätzlich in Häuser je km² umgerechnet (1 ☐Meile = {de(SQM_KM2,2)} km², siehe die Analyse zur Bevölkerungsdichte). Kontrolle: Städtische und ländliche Häuser ergeben je Landestheil die Gesamtzahl; die Summe der drei Landestheile ergibt 10 962 Häuser; Einwohner : Häuser reproduziert die gedruckten Zahlen (z. B. Gera 38 252 : 4 022 = 9,51). Die Häuser je ☐Meile folgen aus Häusern : Fläche (Gera 4 022 : 4,03 = 998,0).",
        "en": f"Taken over are the table “population density with regard to dwellings” (p. 94), the houses per square mile for the districts (p. 95, text block) and the figures for other countries (p. 95; the Thuringian, Bavarian and Saxon averages come from the running text on p. 94). Houses per square mile were additionally converted to houses per km² (1 square mile = {en(SQM_KM2,2)} km², see the analysis of population density). Checks: urban and rural houses add up to the total of each district; the three districts add up to 10,962 houses; inhabitants ÷ houses reproduces the printed figures (e.g. Gera 38,252 ÷ 4,022 = 9.51). Houses per square mile follow from houses ÷ area (Gera 4,022 ÷ 4.03 = 998.0).",
    },
    "findings": [
        {"de": f"Auf ein Wohnhaus kommen im Fürstenthum {de(reuss_pph,2)} Einwohner und {de(H[('Fürstenthum','Zusammen')][3],2)} Familien; in den Städten sind es {de(town_f,2)} Einwohner und {de(H[('Fürstenthum','Städte')][3],2)} Familien, auf dem Land {de(rural_f,2)} und {de(H[('Fürstenthum','Landorte')][3],2)}.",
         "en": f"In the principality a dwelling house holds {en(reuss_pph,2)} inhabitants and {en(H[('Fürstenthum','Zusammen')][3],2)} families; in the towns the figures are {en(town_f,2)} inhabitants and {en(H[('Fürstenthum','Städte')][3],2)} families, in the countryside {en(rural_f,2)} and {en(H[('Fürstenthum','Landorte')][3],2)}."},
        {"de": f"Gera fällt heraus: In der Stadt wohnen im Mittel {de(town_g,2)} Personen in {de(fam_g,2)} Familien in einem Haus, in den Städten von Schleiz ({de(H[('Schleiz','Städte')][4],2)}) und Lobenstein-Ebersdorf ({de(H[('Lobenstein-Ebersdorf','Städte')][4],2)}) sind es knapp 9. Brückner erklärt dies mit der größeren Stockwerkzahl der Geraer Häuser.",
         "en": f"Gera stands out: in the town an average of {en(town_g,2)} persons in {en(fam_g,2)} families share a house, in the towns of Schleiz ({en(H[('Schleiz','Städte')][4],2)}) and Lobenstein-Ebersdorf ({en(H[('Lobenstein-Ebersdorf','Städte')][4],2)}) it is just under 9. Brückner explains this by the greater number of storeys of Gera's houses."},
        {"de": f"Je ☐Meile stehen im Fürstenthum {de(hp['Fürstenthum'],1)} Häuser, im Bezirk Gera {de(hp['Gera'],1)}, in Lobenstein-Ebersdorf {de(hp['Lobenstein-Ebersdorf'],1)} und in Schleiz {de(hp['Schleiz'],1)}. Mehr Häuser je ☐Meile als das Fürstenthum haben Belgien ({de(hp_oth['Belgien'],0)}) und Sachsen ({de(hp_oth['Sachsen'],0)}), weniger Coburg-Gotha ({de(hp_oth['Coburg-Gotha'],0)}), Baden ({de(hp_oth['Baden'],0)}), Württemberg ({de(hp_oth['Württemberg'],0)}), beide Schwarzburg ({de(hp_oth['Beide Schwarzburg'],0)}) und Bayern ({de(hp_oth['Bayern'],0)}); der Bezirk Gera allein übertrifft Sachsen.",
         "en": f"There are {en(hp['Fürstenthum'],1)} houses per square mile in the principality, {en(hp['Gera'],1)} in the district of Gera, {en(hp['Lobenstein-Ebersdorf'],1)} in Lobenstein-Ebersdorf and {en(hp['Schleiz'],1)} in Schleiz. Belgium ({en(hp_oth['Belgien'],0)}) and Saxony ({en(hp_oth['Sachsen'],0)}) have more houses per square mile than the principality, Coburg-Gotha ({en(hp_oth['Coburg-Gotha'],0)}), Baden ({en(hp_oth['Baden'],0)}), Württemberg ({en(hp_oth['Württemberg'],0)}), both Schwarzburgs ({en(hp_oth['Beide Schwarzburg'],0)}) and Bavaria ({en(hp_oth['Bayern'],0)}) fewer; the district of Gera alone exceeds Saxony."},
        {"de": f"Mit {de(reuss_pph,2)} Personen je Haus ist die Wohndichte höher als im thüringischen Durchschnitt ({de(thur,2)}) und in Bayern ({de(bay,2)}), aber etwas niedriger als in Sachsen ({de(sax,2)}).",
         "en": f"At {en(reuss_pph,2)} persons per house, housing density is higher than the Thuringian average ({en(thur,2)}) and Bavaria ({en(bay,2)}) but somewhat lower than in Saxony ({en(sax,2)})."},
    ],
    "caveats": [
        {"de": "Brückner nennt keine Quelle für die Vergleichszahlen anderer Länder und kein Jahr; »Wohnhaus« und »Familie« sind nach den jeweiligen Zählregeln definiert und nicht notwendig vergleichbar. Gemeint ist das Haus, nicht die Wohnung (trotz der Tabellenüberschrift »Wohnungen«).",
         "en": "Brückner names no source or year for the figures of other countries; “dwelling house” and “family” follow the respective census rules and are not necessarily comparable. The unit is the house, not the flat (despite the heading “Wohnungen”)."},
        {"de": "Die Städte-Spalte zählt nur die sechs Städte des Landes (Gera; Schleiz, Saalburg, Tanna; Lobenstein, Hirschberg); der Unterschied Stadt–Land ist deshalb stark von Gera geprägt.",
         "en": "The towns column covers only the six towns of the country (Gera; Schleiz, Saalburg, Tanna; Lobenstein, Hirschberg); the town–country contrast is therefore strongly shaped by Gera."},
    ],
    "conversions": [
        {"from": "☐Meile (geographische Quadratmeile)", "to": "km²", "factor_or_formula": f"1 ☐Meile = {SQM_KM2:.2f} km²",
         "reference": "Brückner S. 832: 1 geographische Meile = 0,9894 künftige Meile (zu 7500 m); Annahme: geographische Meile"},
    ],
    "datasets": [
        {"name": "houses", "title": {"de": "Bewohnte Häuser, Familien und Einwohner je Wohnhaus", "en": "Inhabited houses, families and inhabitants per dwelling house"},
         "columns": [
             col("district", "Landestheil", "District", "string"),
             col("settlement", "Siedlungsart", "Settlement type", "string", None, False, "Städte, Landorte, Zusammen"),
             col("houses", "Bewohnte Häuser", "Inhabited houses", "integer", "Häuser"),
             col("families_per_house", "Familien je Wohnhaus", "Families per house", "number", "Familien"),
             col("persons_per_house", "Einwohner je Wohnhaus", "Inhabitants per house", "number", "Personen"),
         ],
         "rows": houses, "source_refs": refs(("94", "b3", "r4-r7"))},
        {"name": "houses_per_sqm", "title": {"de": "Häuser je Quadratmeile", "en": "Houses per square mile"},
         "columns": [
             col("place", "Gebiet", "Area", "string"),
             col("group", "Gruppe", "Group", "string", None, True, "Reuß j. L. gegenüber den übrigen Ländern (editorisch)"),
             col("houses_per_sqm", "Häuser je ☐Meile", "Houses per square mile", "number", "Häuser/☐Meile"),
             col("houses_per_km2", "Häuser je km²", "Houses per km²", "number", "Häuser/km²", True),
         ],
         "rows": place_rows, "source_refs": refs(("95", "b1"), ("95", "b2"))},
        {"name": "persons_per_house_compare", "title": {"de": "Einwohner je Wohnhaus im Vergleich", "en": "Inhabitants per dwelling house, comparison"},
         "columns": [
             col("region", "Gebiet", "Region", "string"),
             col("group", "Gruppe", "Group", "string", None, True, "Reuß j. L. gegenüber den übrigen Gebieten (editorisch)"),
             col("persons_per_house", "Einwohner je Wohnhaus", "Inhabitants per house", "number", "Personen"),
         ],
         "rows": compare, "source_refs": refs(("94", "b4"), ("94", "b3", "r7"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "houses",
         "title": {"de": "Einwohner je Wohnhaus 1867", "en": "Inhabitants per dwelling house, 1867"},
         "caption": {"de": "Durchschnittliche Zahl der Einwohner eines Wohnhauses in den Städten, den Landorten und insgesamt.",
                     "en": "Average number of inhabitants of a dwelling house in the towns, the rural places and overall."},
         "vegalite": {
             "height": 300,
             "transform": [DIST_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DIST_KEYS}, "axis": {"labelAngle": 0, "labelExpr": DIST_LABEL_EXPR}},
                 "xOffset": {"field": "settlement", "type": "nominal", "scale": {"domain": SETTL}},
                 "y": {"field": "persons_per_house", "type": "quantitative", "title": {"de": "Einwohner je Haus", "en": "Inhabitants per house"}},
                 "color": {"field": "settlement", "type": "nominal", "scale": {"domain": SETTL},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'Towns' : datum.label == 'Landorte' ? 'Rural places' : 'Overall'"}}},
                 "tooltip": [tt("district_label", "Landestheil", "District"), tt("settlement", "Siedlungsart", "Settlement"),
                             tt_fmt("persons_per_house", "Einwohner je Haus", "Inhabitants per house", ".2f"),
                             tt_fmt("families_per_house", "Familien je Haus", "Families per house", ".2f"),
                             tt_fmt("houses", "Bewohnte Häuser", "Inhabited houses", ",")]}}},
        {"id": "c2", "dataset": "houses",
         "title": {"de": "Familien je Wohnhaus 1867", "en": "Families per dwelling house, 1867"},
         "caption": {"de": "Durchschnittliche Zahl der Familien (Haushalte) in einem Wohnhaus; in Gera wohnen in der Stadt im Mittel mehr als drei Familien in einem Haus.",
                     "en": "Average number of families (households) in a dwelling house; in the town of Gera more than three families share a house on average."},
         "vegalite": {
             "height": 280,
             "transform": [DIST_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DIST_KEYS}, "axis": {"labelAngle": 0, "labelExpr": DIST_LABEL_EXPR}},
                 "xOffset": {"field": "settlement", "type": "nominal", "scale": {"domain": SETTL}},
                 "y": {"field": "families_per_house", "type": "quantitative", "title": {"de": "Familien je Haus", "en": "Families per house"}},
                 "color": {"field": "settlement", "type": "nominal", "scale": {"domain": SETTL},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'Towns' : datum.label == 'Landorte' ? 'Rural places' : 'Overall'"}}},
                 "tooltip": [tt("district_label", "Landestheil", "District"), tt("settlement", "Siedlungsart", "Settlement"),
                             tt_fmt("families_per_house", "Familien je Haus", "Families per house", ".2f"),
                             tt_fmt("persons_per_house", "Einwohner je Haus", "Inhabitants per house", ".2f")]}}},
        {"id": "c3", "dataset": "houses_per_sqm",
         "title": {"de": "Häuser je Quadratmeile im Vergleich", "en": "Houses per square mile in comparison"},
         "caption": {"de": "Zahl der Häuser auf 1 ☐Meile in den Landestheilen und im Fürstenthum Reuß j. L. (hervorgehoben) sowie in anderen Ländern.",
                     "en": "Number of houses per square mile in the districts and in the Principality of Reuss j. L. (highlighted) and in other countries."},
         "vegalite": {
             "height": 340,
             "transform": [PLACE_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "place_label", "type": "nominal", "title": None, "sort": "-x", "axis": {"labelLimit": 300}},
                 "x": {"field": "houses_per_sqm", "type": "quantitative", "title": {"de": "Häuser je ☐Meile", "en": "Houses per square mile"}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige", "Reuß j. L."]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label == 'übrige' ? 'andere Länder' : 'Reuß j. L.'", "en": "datum.label == 'übrige' ? 'other countries' : 'Reuss j. L.'"}}},
                 "tooltip": [tt("place_label", "Gebiet", "Area"), tt_fmt("houses_per_sqm", "Häuser je ☐Meile", "Houses per sq. mile", ",.1f"),
                             tt_fmt("houses_per_km2", "Häuser je km²", "Houses per km²", ".1f")]}}},
        {"id": "c4", "dataset": "persons_per_house_compare",
         "title": {"de": "Einwohner je Wohnhaus im Vergleich", "en": "Inhabitants per dwelling house in comparison"},
         "caption": {"de": "Durchschnitt Thüringens, Bayern und Sachsen nach Brückners Text (S. 94) gegenüber dem Fürstenthum Reuß j. L. (1867).",
                     "en": "Thuringian average, Bavaria and Saxony according to Brückner's text (p. 94) compared with the Principality of Reuss j. L. (1867)."},
         "vegalite": {
             "height": 200,
             "transform": [CMP_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "region_label", "type": "nominal", "title": None, "sort": "-x", "axis": {"labelLimit": 300}},
                 "x": {"field": "persons_per_house", "type": "quantitative", "title": {"de": "Einwohner je Haus", "en": "Inhabitants per house"}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige", "Reuß j. L."]}, "legend": None},
                 "tooltip": [tt("region_label", "Gebiet", "Region"), tt_fmt("persons_per_house", "Einwohner je Haus", "Inhabitants per house", ".2f")]}}},
    ],
    "keywords": {"de": ["Wohnhäuser", "Häuser", "Wohndichte", "Haushalte", "Familien je Haus", "Gera", "Stadt und Land", "Wohnverhältnisse"],
                 "en": ["dwelling houses", "houses", "housing density", "households", "families per house", "Gera", "town and country", "living conditions"]},
    "related": ["bevoelkerung-dichte-1834-1867"],
}
write(ana)
