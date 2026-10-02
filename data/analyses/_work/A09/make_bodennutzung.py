"""A09 / analysis 2: Bodennutzung nach Landestheilen (Vermessung 1854), p. 217."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

g = grid("217", "b1")
LT = [("Gera", "Gera"), ("Schleiz", "Schleiz"), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"), ("Fürstenthum", "Principality")]
CATS = [  # row index (1-based grid row), de, en, group nr
    (2, "Gehöfte", "Farmsteads", 7),
    (3, "Gärten und Obstanlagen", "Gardens and orchards", 2),
    (4, "Feld", "Arable land", 1),
    (5, "Wiese", "Meadow", 3),
    (6, "Hutung", "Rough pasture", 4),
    (7, "Teiche", "Ponds", 7),
    (8, "Laubholz", "Deciduous woodland", 5),
    (9, "Nadelholz", "Coniferous woodland", 6),
    (10, "Steuerfreier Boden", "Tax-exempt land", 7),
]
GROUPS = {1: ("Feld", "Arable land"), 2: ("Gärten und Obstanlagen", "Gardens and orchards"), 3: ("Wiese", "Meadow"), 4: ("Hutung", "Rough pasture"),
          5: ("Laubholz", "Deciduous woodland"), 6: ("Nadelholz", "Coniferous woodland"), 7: ("Gehöfte, Teiche u. a.", "Farmsteads, ponds etc.")}
rows = []
for r_i, de, en, gn in CATS:
    r = g[r_i - 1]
    for k, (ltd, lte) in enumerate(LT):
        morgen = num(r[1 + k])
        pct = num(r[5 + k])
        rows.append([de, en, GROUPS[gn][0], GROUPS[gn][1], gn, ltd, lte, k + 1, morgen, pct, round(morgen * MORGEN_HA, 1)])
tot_row = g[10]
totals = {k: num(tot_row[1 + k]) for k in range(4)}  # printed Summe des Flächeninhalts

# landwirtschaftlicher Boden (b3)
g3 = grid("217", "b3")
lw_rows = []
by = {}
for r in rows:
    by[(r[0], r[5])] = r[8]
for k, (ltd, lte) in enumerate(LT):
    r = g3[1 + k]
    allg = num(r[1])
    pct = num(r[2])
    qm = num(r[3])
    fam = num(r[4])
    calc = round(by[("Gärten und Obstanlagen", ltd)] + by[("Feld", ltd)] + by[("Wiese", ltd)] + by[("Hutung", ltd)], 2)
    lw_rows.append([ltd, lte, k + 1, allg, pct, qm, fam, round(fam * MORGEN_HA, 2), round(allg * MORGEN_HA, 0), calc])
print(lw_rows)
print("totals", totals)

# ------------------------------------------------------------ numbers for the text
share = {(r[0], r[5]): r[9] for r in rows}
morgen = {(r[0], r[5]): r[8] for r in rows}
ha_F = totals[3] * MORGEN_HA
ha_by_lt = {lt: totals[i] * MORGEN_HA for i, (lt, _) in enumerate(LT)}
fam_ha = {r[0]: r[7] for r in lw_rows}
fam_m = {r[0]: r[6] for r in lw_rows}
wald = {lt: share[("Laubholz", lt)] + share[("Nadelholz", lt)] for lt, _ in LT}
agr_share = {}
for i, (lt, _) in enumerate(LT):
    a = by[("Gärten und Obstanlagen", lt)] + by[("Feld", lt)] + by[("Wiese", lt)] + by[("Hutung", lt)]
    agr_share[lt] = 100 * a / totals[i]
print(wald, agr_share, ha_F, ha_by_lt)
# sums of the printed columns against printed totals
for i, (lt, _) in enumerate(LT[:3]):
    s = sum(by[(c[1], lt)] for c in CATS)
    print(lt, round(s, 2), totals[i])
fsum = {c[1]: round(sum(by[(c[1], l)] for l, _ in LT[:3]), 2) for c in CATS}
print({c[1]: (fsum[c[1]], by[(c[1], 'Fürstenthum')]) for c in CATS})

REFB1 = {"page": "217", "block": "b1", "rows": "r2-t11"}
REFB3 = {"page": "217", "block": "b3", "rows": "r2-r5"}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


feld_G, feld_S, feld_L = share[("Feld", "Gera")], share[("Feld", "Schleiz")], share[("Feld", "Lobenstein-Ebersdorf")]
nad_G, nad_S, nad_L = share[("Nadelholz", "Gera")], share[("Nadelholz", "Schleiz")], share[("Nadelholz", "Lobenstein-Ebersdorf")]
wi_G, wi_S, wi_L = share[("Wiese", "Gera")], share[("Wiese", "Schleiz")], share[("Wiese", "Lobenstein-Ebersdorf")]
lau_G = share[("Laubholz", "Gera")]
lau_S = share[("Laubholz", "Schleiz")]

ana = {
    "id": "landwirtschaft-bodennutzung-1854",
    "title": bi("Bodennutzung in den drei Landestheilen (Vermessung 1854)", "Land use in the three districts (survey of 1854)"),
    "category": "agriculture",
    "section": "t1-3-2",
    "sources": [
        {"page": "216", "block": "b4"},
        REFB1, REFB3,
        {"page": "217", "block": "fn1"}, {"page": "217", "block": "fn2"}, {"page": "217", "block": "fn3"},
    ],
    "summary": bi(
        f"Nach der Landesvermessung von 1854 verteilt Brückner die Fläche des Fürstenthums ({de_num(totals[3],0)} Morgen, rund {de_num(ha_F,0)} ha) auf neun Nutzungsarten. Die Diagramme zeigen, wie sich Feld, Wiese, Hutung, Garten und Wald auf Gera, Schleiz und Lobenstein-Ebersdorf verteilen und wie viel landwirthschaftlicher Boden auf eine Familie kommt.",
        f"After the land survey of 1854 Brückner distributes the area of the principality ({en_num(totals[3],0)} Morgen, about {en_num(ha_F,0)} ha) over nine kinds of use. The charts show how arable land, meadow, pasture, garden and woodland are distributed over Gera, Schleiz and Lobenstein-Ebersdorf and how much agricultural land there is per family."),
    "method": bi(
        "Die Morgenzahlen und Prozentwerte stammen aus der Tabelle auf S. 217 (Block b1, Zeilen »Arten der Benutzung«) und aus der Tabelle zum landwirthschaftlichen Boden (Block b3). Umrechnung in Hektar mit Brückners eigener Tabelle (S. 832): 1 preuß. Morgen (180 Quadratruthen) = 0,255322 ha. Für die Diagramme sind Gehöfte, Teiche und steuerfreier Boden zur Gruppe »Gehöfte, Teiche u. a.« zusammengefasst. Der »landwirthschaftliche Boden« ist bei Brückner die Summe aus Gärten, Feld, Wiese und Hutung; zur Kontrolle wurde sie aus Block b1 nachgerechnet (Spalte morgen_berechnet).",
        "The Morgen figures and percentages come from the table on p. 217 (block b1, rows “Arten der Benutzung”) and from the table on agricultural land (block b3). Conversion to hectares uses Brückner's own table (p. 832): 1 Prussian Morgen (180 square rods) = 0.255322 ha. For the charts, farmsteads, ponds and tax-exempt land are combined into the group “Farmsteads, ponds etc.”. Brückner's “agricultural land” is the sum of gardens, arable land, meadow and pasture; as a check it was recomputed from block b1 (column morgen_berechnet)."),
    "findings": [
        bi(f"Gera ist ausgesprochenes Ackerland: {de_num(feld_G)} % der Fläche sind Feld, nur {de_num(nad_G)} % Nadelholz. In Schleiz ({de_num(feld_S)} % Feld) und Lobenstein-Ebersdorf ({de_num(feld_L)} %) ist dagegen der Nadelwald die größte Nutzung ({de_num(nad_S)} % bzw. {de_num(nad_L)} %).",
           f"Gera is distinctly arable country: {en_num(feld_G)} % of its area is field and only {en_num(nad_G)} % coniferous wood. In Schleiz ({en_num(feld_S)} % field) and Lobenstein-Ebersdorf ({en_num(feld_L)} %) coniferous woodland is the largest use ({en_num(nad_S)} % and {en_num(nad_L)} %)."),
        bi(f"Das Oberland hat im Verhältnis weit mehr Wiese als das Unterland: {de_num(wi_S)} % in Schleiz und {de_num(wi_L)} % in Lobenstein-Ebersdorf gegenüber {de_num(wi_G)} % in Gera.",
           f"The Upper Land has far more meadow in proportion than the Lower Land: {en_num(wi_S)} % in Schleiz and {en_num(wi_L)} % in Lobenstein-Ebersdorf against {en_num(wi_G)} % in Gera."),
        bi(f"Laubwald gibt es fast nur im Landestheil Gera ({de_num(lau_G)} % der Fläche); in Schleiz sind es {de_num(lau_S)} %.",
           f"Deciduous woodland is found almost only in the district of Gera ({en_num(lau_G)} % of the area); in Schleiz it is {en_num(lau_S)} %."),
        bi(f"Der Anteil des landwirthschaftlich genutzten Bodens (Garten, Feld, Wiese, Hutung) an der Gesamtfläche sinkt von {de_num(agr_share['Gera'])} % in Gera über {de_num(agr_share['Schleiz'])} % in Schleiz auf {de_num(agr_share['Lobenstein-Ebersdorf'])} % in Lobenstein-Ebersdorf (Fürstenthum: {de_num(agr_share['Fürstenthum'])} %).",
           f"The share of agriculturally used land (garden, field, meadow, pasture) in the total area falls from {en_num(agr_share['Gera'])} % in Gera through {en_num(agr_share['Schleiz'])} % in Schleiz to {en_num(agr_share['Lobenstein-Ebersdorf'])} % in Lobenstein-Ebersdorf (principality: {en_num(agr_share['Fürstenthum'])} %)."),
        bi(f"Auf eine Familie kommen in Gera {de_num(fam_m['Gera'],2)} Morgen ({de_num(fam_ha['Gera'],2)} ha) landwirthschaftlicher Boden, in Schleiz {de_num(fam_m['Schleiz'],2)} Morgen ({de_num(fam_ha['Schleiz'],2)} ha) und in Lobenstein-Ebersdorf {de_num(fam_m['Lobenstein-Ebersdorf'],2)} Morgen ({de_num(fam_ha['Lobenstein-Ebersdorf'],2)} ha).",
           f"Per family there are {en_num(fam_m['Gera'],2)} Morgen ({en_num(fam_ha['Gera'],2)} ha) of agricultural land in Gera, {en_num(fam_m['Schleiz'],2)} Morgen ({en_num(fam_ha['Schleiz'],2)} ha) in Schleiz and {en_num(fam_m['Lobenstein-Ebersdorf'],2)} Morgen ({en_num(fam_ha['Lobenstein-Ebersdorf'],2)} ha) in Lobenstein-Ebersdorf."),
    ],
    "caveats": [
        bi("Die Zahlen beruhen auf der Vermessung von 1854. Seither hat die Feldfläche vor allem im Landestheil Gera um etwa 1000 Morgen zugenommen (Fußnote S. 217 und S. 226); Brückner behält 1854 als Grundlage bei. Lobenstein-Ebersdorf war nur »croquirt«, seine Fläche ist wahrscheinlich größer als angegeben.",
           "The figures rest on the survey of 1854. Since then the arable area has grown, above all in the district of Gera by about 1,000 Morgen (footnote p. 217 and p. 226); Brückner keeps 1854 as the basis. Lobenstein-Ebersdorf was only sketched (“croquirt”), so its area is probably larger than stated."),
        bi("Die gedruckten Summen stimmen nicht ganz: Für Schleiz steht in Block b3 71 574 Morgen landwirthschaftlicher Boden, die Teilposten aus Block b1 ergeben 71 374; die Summe des Fürstenthums (188 542) passt zu 71 374. Auch einzelne Spalten des Fürstenthums weichen um bis zu etwa einen Morgen von der Summe der Landestheile ab. Die gedruckten Werte wurden unverändert übernommen (am Faksimile geprüft).",
           "The printed totals do not quite agree: for Schleiz block b3 gives 71,574 Morgen of agricultural land whereas the items in block b1 add up to 71,374; the principality total (188,542) fits 71,374. Individual columns of the principality also deviate by up to about one Morgen from the sum of the districts. The printed values were taken over unchanged (checked against the facsimile)."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hectaren"},
    ],
    "datasets": [
        {"name": "nutzung", "title": bi("Bodennutzung nach Landestheilen", "Land use by district"),
         "columns": [
             col("nutzung_de", "Art der Benutzung", "Kind of use", "string"),
             col("nutzung_en", "Art der Benutzung (englisch)", "Kind of use (English)", "string"),
             col("gruppe_de", "Gruppe (für die Diagramme)", "Group (for the charts)", "string", derived=True, note="editorische Zusammenfassung"),
             col("gruppe_en", "Gruppe (englisch)", "Group (English)", "string", derived=True),
             col("gruppe_nr", "Reihenfolge der Gruppe", "Group order", "integer", derived=True),
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge des Landestheils", "District order", "integer", derived=True),
             col("morgen", "Fläche", "Area", "number", "preuß. Morgen"),
             col("pct", "Anteil an der Fläche", "Share of area", "number", "%"),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
         ],
         "rows": rows, "source_refs": [REFB1]},
        {"name": "landw_boden", "title": bi("Landwirthschaftlicher Boden nach Landestheilen", "Agricultural land by district"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("morgen", "Landwirthschaftlicher Boden", "Agricultural land", "integer", "preuß. Morgen"),
             col("pct", "Anteil am landw. Boden des Fürstenthums", "Share of the principality's agricultural land", "number", "%"),
             col("morgen_je_qm", "Morgen auf 1 Quadratmeile", "Morgen per square mile", "number", "Morgen/□Meile"),
             col("morgen_je_familie", "Morgen auf 1 Familie", "Morgen per family", "number", "Morgen"),
             col("ha_je_familie", "Hektar auf 1 Familie", "Hectares per family", "number", "ha", derived=True, note="Morgen × 0,255322"),
             col("ha", "Landwirthschaftlicher Boden in Hektar", "Agricultural land in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
             col("morgen_berechnet", "Summe Garten + Feld + Wiese + Hutung (nachgerechnet)", "Sum of garden + field + meadow + pasture (recomputed)", "number", "preuß. Morgen", derived=True, note="aus Block b1 nachgerechnet"),
         ],
         "rows": lw_rows, "source_refs": [REFB3]},
    ],
    "charts": [
        {"id": "c1", "dataset": "nutzung",
         "title": bi("Zusammensetzung der Bodenfläche", "Composition of the land area"),
         "caption": bi("Anteile der Nutzungsarten an der Gesamtfläche des Landestheils bzw. des Fürstenthums (Vermessung 1854). Gera ist von Feld geprägt, Schleiz und Lobenstein-Ebersdorf von Nadelwald und Wiese.",
                       "Shares of the kinds of use in the total area of the district and of the principality (survey of 1854). Gera is dominated by arable land, Schleiz and Lobenstein-Ebersdorf by coniferous woodland and meadow."),
         "vegalite": {
             "height": 260,
             "transform": [{"aggregate": [{"op": "sum", "field": "pct", "as": "anteil"}, {"op": "sum", "field": "morgen", "as": "morgen_sum"}, {"op": "sum", "field": "ha", "as": "ha_sum"}],
                            "groupby": ["gruppe_de", "gruppe_en", "gruppe_nr", "landestheil_de", "landestheil_en", "lt_nr"]}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 220}},
                 "x": {"field": "anteil", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": bi("% der Fläche", "% of area")},
                 "color": {"field": {"de": "gruppe_de", "en": "gruppe_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(GROUPS[i][0], GROUPS[i][1]) for i in range(1, 8)]},
                           "legend": {"columns": 2, "labelLimit": 260}},
                 "order": {"field": "gruppe_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": {"de": "gruppe_de", "en": "gruppe_en"}, "title": bi("Nutzung", "Use")},
                             {"field": "morgen_sum", "title": bi("Morgen", "Morgen"), "format": ",.0f"},
                             {"field": "ha_sum", "title": "ha", "format": ",.0f"},
                             {"field": "anteil", "title": bi("% der Fläche", "% of area"), "format": ".1f"}]}}},
        {"id": "c2", "dataset": "nutzung",
         "title": bi("Fläche der Landestheile nach Nutzung (Hektar)", "Area of the districts by use (hectares)"),
         "caption": bi("Absolute Flächen, umgerechnet in Hektar (1 preuß. Morgen = 0,255322 ha). Schleiz ist der größte, Gera der kleinste Landestheil.",
                       "Absolute areas converted to hectares (1 Prussian Morgen = 0.255322 ha). Schleiz is the largest district, Gera the smallest."),
         "vegalite": {
             "height": 200,
             "transform": [{"filter": "datum.landestheil_de != 'Fürstenthum'"},
                           {"aggregate": [{"op": "sum", "field": "ha", "as": "ha_sum"}, {"op": "sum", "field": "morgen", "as": "morgen_sum"}],
                            "groupby": ["gruppe_de", "gruppe_en", "gruppe_nr", "landestheil_de", "landestheil_en", "lt_nr"]}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 220}},
                 "x": {"field": "ha_sum", "type": "quantitative", "title": "ha", "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "gruppe_de", "en": "gruppe_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(GROUPS[i][0], GROUPS[i][1]) for i in range(1, 8)]},
                           "legend": {"columns": 2, "labelLimit": 260}},
                 "order": {"field": "gruppe_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": {"de": "gruppe_de", "en": "gruppe_en"}, "title": bi("Nutzung", "Use")},
                             {"field": "morgen_sum", "title": bi("Morgen", "Morgen"), "format": ",.0f"},
                             {"field": "ha_sum", "title": "ha", "format": ",.0f"}]}}},
        {"id": "c3", "dataset": "landw_boden",
         "title": bi("Landwirthschaftlicher Boden je Familie", "Agricultural land per family"),
         "caption": bi("Garten, Feld, Wiese und Hutung zusammen, in Hektar je Familie (Brückner: Morgen auf 1 Familie, umgerechnet). Im Unterland (Gera) ist der Besitz je Familie am kleinsten.",
                       "Garden, field, meadow and pasture together, in hectares per family (Brückner: Morgen per family, converted). In the Lower Land (Gera) the holding per family is smallest."),
         "vegalite": {
             "height": 220,
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "ha_je_familie", "type": "quantitative", "title": bi("ha je Familie", "ha per family")},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "morgen_je_familie", "title": bi("Morgen je Familie", "Morgen per family"), "format": ".2f"},
                             {"field": "ha_je_familie", "title": bi("ha je Familie", "ha per family"), "format": ".2f"},
                             {"field": "morgen", "title": bi("Morgen insgesamt", "Morgen in total"), "format": ",.0f"}]}}},
    ],
    "keywords": {
        "de": ["Bodennutzung", "Flächennutzung", "Landesvermessung 1854", "Feld", "Wiese", "Hutung", "Nadelwald", "Laubwald", "Garten", "Morgen", "Landwirtschaft", "Oberland", "Unterland"],
        "en": ["land use", "survey 1854", "arable land", "meadow", "pasture", "coniferous forest", "deciduous forest", "garden", "Morgen", "agriculture", "Upper Land", "Lower Land"],
    },
    "related": ["landwirtschaft-grundbesitz-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
