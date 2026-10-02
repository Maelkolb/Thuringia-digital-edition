"""A09 / analysis 9: Waldfläche und Besitzverhältnisse (pp. 240-241)."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

g = grid("240", "b2")
AREAS = [  # grid index, de, en, landestheil_de, landestheil_en, nr, lt_nr
    (1, "Gera", "Gera", "Gera", "Gera", 1, 1),
    (2, "Pflege Reichenfels", "Reichenfels district (Pflege)", "Schleiz", "Schleiz", 2, 2),
    (3, "Herrschaft Schleiz", "Schleiz lordship (Herrschaft)", "Schleiz", "Schleiz", 3, 2),
    (4, "Pflege Saalburg", "Saalburg district (Pflege)", "Schleiz", "Schleiz", 4, 2),
    (6, "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", 5, 3),
]
OWN = [("Kammerforste", "Chamber forests (domain)", 1), ("Gemeindeforste", "Municipal forests", 2), ("Stiftungsforste", "Foundation forests", 3), ("Privatwald", "Private woodland", 4)]
TYPE = [("Laubwald", "Deciduous", 1), ("Nadelwald", "Coniferous", 2)]
wald = []
for gi, ade, aen, lde, len_, an, ln in AREAS:
    r = g[gi]
    for oi, (ode, oen, on) in enumerate(OWN):
        for ti, (tde, ten, tn) in enumerate(TYPE):
            v = num(r[1 + 3 * oi + ti])
            wald.append([lde, len_, ln, ade, aen, an, ode, oen, on, tde, ten, tn, v, round((v or 0) * MORGEN_HA, 0)])
# printed total rows for checks
tot = {"Gera": [num(x) for x in g[1][1:]], "Schleiz": [num(x) for x in g[5][1:]], "Lobenstein-Ebersdorf": [num(x) for x in g[6][1:]], "Fürstenthum": [num(x) for x in g[7][1:]]}
# area / owner sums from the dataset
def S(**kw):
    sel = wald
    for k, v in kw.items():
        idx = {"lt": 0, "area": 3, "own": 6, "typ": 9}[k]
        sel = [r for r in sel if r[idx] == v]
    return sum((r[12] or 0) for r in sel)


F_total = S()
print("sum of dataset", F_total, "printed", tot["Fürstenthum"][14])
for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
    print(lt, S(lt=lt), tot[lt][14])
own_tot = {o[0]: S(own=o[0]) for o in OWN}
own_typ = {(o[0], t[0]): S(own=o[0], typ=t[0]) for o in OWN for t in TYPE}
print(own_tot, own_typ)

# ---------------------------------------------------------------- forest cover
g217 = grid("217", "b1")
area217 = {"Gera": num(g217[10][1]), "Schleiz": num(g217[10][2]), "Lobenstein-Ebersdorf": num(g217[10][3].replace("***)", "")), "Fürstenthum": num(g217[10][4])}
g4 = grid("240", "b4")
rowmap = {"Gera": 1, "Schleiz": 5, "Lobenstein-Ebersdorf": 6, "Fürstenthum": 7}
anteil = []
for k, (lt, lten) in enumerate((("Gera", "Gera"), ("Schleiz", "Schleiz"), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"), ("Fürstenthum", "Principality"))):
    r = g4[rowmap[lt]]
    wald_m = tot[lt][14]
    qm = num(r[4])
    einw = num(r[5])
    # for Gera the printed Summa 21298 is consistent with Laub + Nadel
    anteil.append([lt, lten, k + 1, wald_m, area217[lt], round(100 * wald_m / area217[lt], 1), qm, einw, round(einw * MORGEN_HA, 2) if einw is not None else None,
                   round(wald_m * MORGEN_HA, 0)])
print(anteil)

# ---------------------------------------------------------------- Domänenwald 1647 / 1867
b2 = block("241", "b2")["text"]
assert "61,786 Morgen Wald und 2240 Morgen Geräumde, zusammen 64,026 Morgen, somit 259 Morgen mehr" in b2
dom = [["1647", "1647", 1, "Wald", "Woodland", 61786, round(61786 * MORGEN_HA, 0)],
       ["1647", "1647", 1, "Geräumde (gerodete Flächen)", "Cleared land (Geräumde)", 2240, round(2240 * MORGEN_HA, 0)],
       ["heute (um 1868)", "present (c. 1868)", 2, "Kammerforste (Wald)", "Chamber forests (woodland)", tot["Fürstenthum"][2], round(tot["Fürstenthum"][2] * MORGEN_HA, 0)]]
assert 61786 + 2240 == 64026 and 64026 - tot["Fürstenthum"][2] == 259, (64026 - tot["Fürstenthum"][2])

# ---------------------------------------------------------------- numbers for the text
share_own = {o: 100 * v / F_total for o, v in own_tot.items()}
laub_share = {o[0]: 100 * own_typ[(o[0], "Laubwald")] / own_tot[o[0]] for o in OWN}
laub_all = 100 * S(typ="Laubwald") / F_total
lt_shares = {lt: {o[0]: 100 * S(lt=lt, own=o[0]) / S(lt=lt) for o in OWN} for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
laub_lt = {lt: 100 * S(lt=lt, typ="Laubwald") / S(lt=lt) for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf")}
laub_gera_of_all = 100 * S(lt="Gera", typ="Laubwald") / S(typ="Laubwald")
cover = {r[0]: r[5] for r in anteil}
einw = {r[0]: r for r in anteil}
print(share_own, laub_share, laub_all, lt_shares, laub_lt, laub_gera_of_all, cover)
print("printed shares p240:", [(r[6], r[7]) for r in g4[1:5]])
ha_F = F_total * MORGEN_HA

R_W = {"page": "240", "block": "b2", "rows": "r2-r8"}
R_P = {"page": "240", "block": "b4", "rows": "r2-r8"}
R_F = {"page": "217", "block": "b1", "rows": "t11"}
R_D = [{"page": "240", "block": "b5"}, {"page": "241", "block": "b1", "rows": "r2-r3"}, {"page": "241", "block": "b2"}]


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


ana = {
    "id": "forstwirtschaft-waldflaeche-besitz",
    "title": bi("Umfang und Besitzverhältnisse der Wälder (um 1868)", "Extent and ownership of the forests (c. 1868)"),
    "category": "forestry",
    "section": "t1-3-4",
    "sources": [R_W, R_P, R_F] + R_D,
    "summary": bi(
        f"Brückner gibt den Wald des Fürstenthums in Morgen nach Besitzern (Kammerforste, Gemeinde-, Stiftungs- und Privatwald) und nach Holzart (Laub-, Nadelholz) für die Landestheile und ihre Teilgebiete an – insgesamt {de_num(F_total,0)} Morgen oder rund {de_num(ha_F,0)} ha. Die Diagramme zeigen die Verteilung auf Besitzer, den Laubholzanteil, den Waldanteil je Landestheil und den Vergleich des Domänenwaldes von 1647 mit dem heutigen.",
        f"Brückner gives the forest of the principality in Morgen by owner (chamber forests, municipal, foundation and private woodland) and by kind of wood (deciduous, coniferous) for the districts and their subdivisions – {en_num(F_total,0)} Morgen in total, about {en_num(ha_F,0)} ha. The charts show the distribution among owners, the share of deciduous wood, the forest share by district, and the comparison of the domain forest of 1647 with the present one."),
    "method": bi(
        "Die Flächen stammen aus Tabelle a) »Ueberhaupt in preußischen Morgen« (S. 240, Block b2), die Vergleichszahlen aus Tabelle b) (Block b4); Gesamtfläche der Landestheile aus der Vermessung 1854 (S. 217). Hektar wurden mit Brückners Faktor 0,255322 berechnet (S. 832). Der Waldanteil (Spalte anteil_pct) ist die Waldfläche geteilt durch die vermessene Gesamtfläche des Landestheils; er weicht deshalb von Brückners Gesamtangabe »41 1/5 Procent« etwas ab (hier 41,4 %), weil Waldfläche (heutiger Stand) und Gesamtfläche (Vermessung 1854, Lobenstein-Ebersdorf nur croquirt) aus verschiedenen Zeiten stammen. Der Landestheil Schleiz setzt sich aus Pflege Reichenfels, Herrschaft Schleiz und Pflege Saalburg zusammen (Klammer in der Vorlage). Die Besitzeranteile sind aus den Flächen berechnet, nicht aus Brückners Prozentzahlen.",
        "The areas come from table a) “Ueberhaupt in preußischen Morgen” (p. 240, block b2), the comparative figures from table b) (block b4); the total area of the districts from the survey of 1854 (p. 217). Hectares were computed with Brückner's factor 0.255322 (p. 832). The forest share (column anteil_pct) is the forest area divided by the surveyed total area of the district; it therefore deviates somewhat from Brückner's overall figure “41 1/5 per cent” (here 41.4 %), because forest area (present state) and total area (survey of 1854, Lobenstein-Ebersdorf only sketched) come from different times. The district of Schleiz consists of the Reichenfels district, the Schleiz lordship and the Saalburg district (bracket in the source). The owner shares are computed from the areas, not from Brückner's percentages."),
    "findings": [
        bi(f"Der Wald des Fürstenthums umfasst {de_num(F_total,0)} Morgen ({de_num(ha_F,0)} ha), das sind rund {de_num(cover['Fürstenthum'])} % der vermessenen Fläche; davon sind {de_num(100-laub_all)} % Nadelwald und nur {de_num(laub_all)} % Laubwald.",
           f"The forest of the principality covers {en_num(F_total,0)} Morgen ({en_num(ha_F,0)} ha), about {en_num(cover['Fürstenthum'])} % of the surveyed area; {en_num(100-laub_all)} % of it is coniferous and only {en_num(laub_all)} % deciduous."),
        bi(f"Fast die Hälfte des Waldes gehört dem Staat (Kammerforste {de_num(share_own['Kammerforste'])} %), fast die andere Hälfte Privatbesitzern ({de_num(share_own['Privatwald'])} %); Gemeinden ({de_num(share_own['Gemeindeforste'])} %) und Stiftungen ({de_num(share_own['Stiftungsforste'])} %) besitzen zusammen nur {de_num(share_own['Gemeindeforste']+share_own['Stiftungsforste'])} %.",
           f"Almost half of the forest belongs to the state (chamber forests {en_num(share_own['Kammerforste'])} %), almost the other half to private owners ({en_num(share_own['Privatwald'])} %); municipalities ({en_num(share_own['Gemeindeforste'])} %) and foundations ({en_num(share_own['Stiftungsforste'])} %) own only {en_num(share_own['Gemeindeforste']+share_own['Stiftungsforste'])} % together."),
        bi(f"Im Unterland (Gera) ist der Wald überwiegend privat ({de_num(lt_shares['Gera']['Privatwald'])} %), im Oberland dagegen zu gut der Hälfte staatlich (Schleiz: {de_num(lt_shares['Schleiz']['Kammerforste'])} % Kammerforste, Lobenstein-Ebersdorf: {de_num(lt_shares['Lobenstein-Ebersdorf']['Kammerforste'])} %).",
           f"In the Lower Land (Gera) the forest is predominantly private ({en_num(lt_shares['Gera']['Privatwald'])} %), in the Upper Land slightly more than half state-owned (Schleiz: {en_num(lt_shares['Schleiz']['Kammerforste'])} % chamber forests, Lobenstein-Ebersdorf: {en_num(lt_shares['Lobenstein-Ebersdorf']['Kammerforste'])} %)."),
        bi(f"Der Waldanteil steigt vom Unterland zum Oberland: Gera {de_num(cover['Gera'])} %, Schleiz {de_num(cover['Schleiz'])} %, Lobenstein-Ebersdorf {de_num(cover['Lobenstein-Ebersdorf'])} % der Fläche; auf einen Einwohner kommen {de_num(einw['Gera'][7],2)}, {de_num(einw['Schleiz'][7],2)} bzw. {de_num(einw['Lobenstein-Ebersdorf'][7],2)} Morgen.",
           f"The forest share rises from the Lower to the Upper Land: Gera {en_num(cover['Gera'])} %, Schleiz {en_num(cover['Schleiz'])} %, Lobenstein-Ebersdorf {en_num(cover['Lobenstein-Ebersdorf'])} % of the area; per inhabitant there are {en_num(einw['Gera'][7],2)}, {en_num(einw['Schleiz'][7],2)} and {en_num(einw['Lobenstein-Ebersdorf'][7],2)} Morgen respectively."),
        bi(f"Laubwald ist fast auf Gera beschränkt: Der Landestheil hat {de_num(laub_gera_of_all)} % des gesamten Laubwaldes; dort sind {de_num(laub_lt['Gera'])} % des Waldes Laubholz, in Schleiz {de_num(laub_lt['Schleiz'])} % und in Lobenstein-Ebersdorf {de_num(laub_lt['Lobenstein-Ebersdorf'])} %. Der Privatwald hat mit {de_num(laub_share['Privatwald'])} % den höchsten, die Kammerforste mit {de_num(laub_share['Kammerforste'])} % den niedrigsten Laubholzanteil.",
           f"Deciduous wood is almost confined to Gera: the district has {en_num(laub_gera_of_all)} % of all deciduous woodland; there {en_num(laub_lt['Gera'])} % of the forest is deciduous, in Schleiz {en_num(laub_lt['Schleiz'])} % and in Lobenstein-Ebersdorf {en_num(laub_lt['Lobenstein-Ebersdorf'])} %. Private woodland has the highest share of deciduous wood at {en_num(laub_share['Privatwald'])} %, the chamber forests the lowest at {en_num(laub_share['Kammerforste'])} %."),
        bi(f"Der Domänenwald von 1647 (61 786 Morgen Wald und 2240 Morgen Geräumde, zusammen 64 026 Morgen) ist nur 259 Morgen größer als die heutigen Kammerforste ({de_num(tot['Fürstenthum'][2],0)} Morgen). Brückner schließt daraus, dass in 222 Jahren mehr Domänenwaldboden anderen Zwecken zugeführt als durch den Erwerb von Rittergütern gewonnen wurde.",
           f"The domain forest of 1647 (61,786 Morgen of woodland and 2,240 Morgen of cleared land, 64,026 Morgen in total) is only 259 Morgen larger than today's chamber forests ({en_num(tot['Fürstenthum'][2],0)} Morgen). Brückner concludes that in 222 years more domain forest land was put to other uses than was gained by the acquisition of manors."),
    ],
    "caveats": [
        bi("Die Zahlen von Block b2 stimmen bis auf eine Stelle in sich: Für den Privatwald des Landestheils Gera ist Laub + Nadel = 4701 + 10480 = 15 181, gedruckt ist »Sa. 15 191«; die Gesamtfläche Gera (21 298) und die Summe des Fürstenthums (64 959) passen zu 15 181. Die Auswertung verwendet Laub- und Nadelwert getrennt.",
           "The figures of block b2 are internally consistent except for one place: for the private woodland of the district of Gera, deciduous + coniferous = 4,701 + 10,480 = 15,181, whereas “Sa. 15,191” is printed; the total area of Gera (21,298) and the sum for the principality (64,959) fit 15,181. The analysis uses the deciduous and coniferous values separately."),
        bi("Brückners Prozentangaben im Text zum Besitzstand (Privatwald 48,23 %, Domänenwald 48,12 %, Gemeindewald 2,15 %, Stiftungswald 1,50 %) weichen leicht von den aus den Flächen berechneten Anteilen ab; für die Landestheile nennt er die Anteile am Domänenwald (0,70 / 44,31 / 54,99 %), die sich mit der Flächentabelle (6,9 / 44,3 / 48,8 %) nicht ganz decken. Die Auswertung stützt sich auf die Flächen.",
           "Brückner's percentages in the text for ownership (private woodland 48.23 %, domain forest 48.12 %, municipal 2.15 %, foundation 1.50 %) deviate slightly from the shares computed from the areas; for the districts he gives the shares of the domain forest (0.70 / 44.31 / 54.99 %), which do not quite agree with the area table (6.9 / 44.3 / 48.8 %). The analysis relies on the areas."),
        bi("Die Waldflächen sind nach Angabe der Fußnote für Gera und Schleiz amtlichen Mitteilungen aus Schleiz, für Lobenstein-Ebersdorf Mitteilungen aus Ebersdorf entnommen und nicht unbedingt gleichzeitig mit der Vermessung von 1854; für Lobenstein-Ebersdorf liegt nur eine Croquirung vor.",
           "According to the footnote, the forest areas for Gera and Schleiz are taken from official communications from Schleiz, for Lobenstein-Ebersdorf from communications from Ebersdorf, and are not necessarily contemporaneous with the survey of 1854; for Lobenstein-Ebersdorf only a sketch survey exists."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hectaren"},
    ],
    "datasets": [
        {"name": "wald", "title": bi("Wald nach Gebiet, Besitzer und Holzart", "Forest by area, owner and kind of wood"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("gebiet_de", "Gebiet", "Area", "string"),
             col("gebiet_en", "Gebiet (englisch)", "Area (English)", "string"),
             col("gebiet_nr", "Reihenfolge Gebiet", "Area order", "integer", derived=True),
             col("besitzer_de", "Besitzer", "Owner", "string"),
             col("besitzer_en", "Besitzer (englisch)", "Owner (English)", "string"),
             col("besitzer_nr", "Reihenfolge Besitzer", "Owner order", "integer", derived=True),
             col("holzart_de", "Holzart", "Kind of wood", "string"),
             col("holzart_en", "Holzart (englisch)", "Kind of wood (English)", "string"),
             col("holzart_nr", "Reihenfolge Holzart", "Order of kind of wood", "integer", derived=True),
             col("morgen", "Waldfläche", "Forest area", "integer", "preuß. Morgen"),
             col("ha", "Waldfläche in Hektar", "Forest area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
         ],
         "rows": wald, "source_refs": [R_W]},
        {"name": "waldanteil", "title": bi("Waldanteil und Wald je Einwohner", "Forest share and forest per inhabitant"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("wald_morgen", "Waldfläche", "Forest area", "integer", "preuß. Morgen"),
             col("flaeche_morgen", "Gesamtfläche (Vermessung 1854)", "Total area (survey of 1854)", "number", "preuß. Morgen"),
             col("anteil_pct", "Waldanteil an der Fläche", "Forest share of the area", "number", "%", derived=True, note="Waldfläche / Gesamtfläche × 100"),
             col("wald_je_qm", "Wald in Quadratmeilen", "Forest in square miles", "number", "□Meilen"),
             col("morgen_je_einw", "Morgen Wald auf 1 Einwohner", "Morgen of forest per inhabitant", "number", "Morgen"),
             col("ha_je_einw", "Hektar Wald je Einwohner", "Hectares of forest per inhabitant", "number", "ha", derived=True, note="Morgen × 0,255322"),
             col("wald_ha", "Waldfläche in Hektar", "Forest area in hectares", "number", "ha", derived=True),
         ],
         "rows": anteil, "source_refs": [R_P, R_W, R_F]},
        {"name": "domaene", "title": bi("Domänenwald 1647 und heute", "Domain forest 1647 and today"),
         "columns": [
             col("zeit_de", "Zeitpunkt", "Time", "string"),
             col("zeit_en", "Zeitpunkt (englisch)", "Time (English)", "string"),
             col("zeit_nr", "Reihenfolge", "Order", "integer", derived=True),
             col("art_de", "Art der Fläche", "Kind of land", "string"),
             col("art_en", "Art der Fläche (englisch)", "Kind of land (English)", "string"),
             col("morgen", "Fläche", "Area", "integer", "preuß. Morgen"),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
         ],
         "rows": dom, "source_refs": [{"page": "241", "block": "b2"}, R_W]},
    ],
    "charts": [
        {"id": "c1", "dataset": "wald",
         "title": bi("Wald nach Gebieten und Besitzern (Hektar)", "Forest by area and owner (hectares)"),
         "caption": bi("Waldfläche in Hektar nach Besitzern für die fünf Gebiete der Vorlage; der Landestheil Schleiz besteht aus den Gebieten Reichenfels, Schleiz und Saalburg. Im Oberland überwiegt der Staatswald leicht, in Gera deutlich der Privatwald.",
                       "Forest area in hectares by owner for the five areas of the source; the district of Schleiz consists of the areas Reichenfels, Schleiz and Saalburg. In the Upper Land state forest slightly predominates, in Gera private forest clearly."),
         "vegalite": {
             "height": 300,
             "transform": [{"aggregate": [{"op": "sum", "field": "ha", "as": "ha_sum"}, {"op": "sum", "field": "morgen", "as": "morgen_sum"}],
                            "groupby": ["gebiet_de", "gebiet_en", "gebiet_nr", "besitzer_de", "besitzer_en", "besitzer_nr"]}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "type": "nominal", "sort": {"field": "gebiet_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 260}},
                 "x": {"field": "ha_sum", "type": "quantitative", "title": "ha", "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(o[0], o[1]) for o in OWN]}, "legend": {"columns": 2, "labelLimit": 220}},
                 "order": {"field": "besitzer_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "gebiet_de", "en": "gebiet_en"}, "title": bi("Gebiet", "Area")},
                             {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "title": bi("Besitzer", "Owner")},
                             {"field": "morgen_sum", "title": bi("Morgen", "Morgen"), "format": ",.0f"},
                             {"field": "ha_sum", "title": "ha", "format": ",.0f"}]}}},
        {"id": "c2", "dataset": "wald",
         "title": bi("Laub- und Nadelwald nach Besitzern", "Deciduous and coniferous wood by owner"),
         "caption": bi("Anteil von Laub- und Nadelholz an der Waldfläche jedes Besitzers (gesamtes Fürstenthum). Der Wald ist überall überwiegend Nadelwald; Privat- und Stiftungswald haben etwas mehr Laubholz als die Kammerforste.",
                       "Share of deciduous and coniferous wood in the forest area of each owner (whole principality). The forest is predominantly coniferous everywhere; private and foundation forests have somewhat more deciduous wood than the chamber forests."),
         "vegalite": {
             "height": 220,
             "transform": [{"aggregate": [{"op": "sum", "field": "morgen", "as": "morgen_sum"}], "groupby": ["besitzer_de", "besitzer_en", "besitzer_nr", "holzart_de", "holzart_en", "holzart_nr"]}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "type": "nominal", "sort": {"field": "besitzer_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 240}},
                 "x": {"field": "morgen_sum", "type": "quantitative", "stack": "normalize", "title": bi("Anteil an der Waldfläche", "Share of the forest area"), "axis": {"format": "%"}},
                 "color": {"field": {"de": "holzart_de", "en": "holzart_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi("Laubwald", "Deciduous"), bi("Nadelwald", "Coniferous")]}},
                 "order": {"field": "holzart_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "besitzer_de", "en": "besitzer_en"}, "title": bi("Besitzer", "Owner")},
                             {"field": {"de": "holzart_de", "en": "holzart_en"}, "title": bi("Holzart", "Kind of wood")},
                             {"field": "morgen_sum", "title": bi("Morgen", "Morgen"), "format": ",.0f"}]}}},
        {"id": "c3", "dataset": "waldanteil",
         "title": bi("Waldanteil an der Landesfläche", "Forest share of the land area"),
         "caption": bi("Waldfläche in Prozent der vermessenen Gesamtfläche (Vermessung 1854; Waldfläche nach den amtlichen Angaben der Vorlage). In Lobenstein-Ebersdorf ist der Waldanteil mehr als doppelt so hoch wie in Gera.",
                       "Forest area as a percentage of the surveyed total area (survey of 1854; forest area according to the official statements of the source). In Lobenstein-Ebersdorf the forest share is more than twice as high as in Gera."),
         "vegalite": {
             "height": 240,
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": {"field": "lt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "anteil_pct", "type": "quantitative", "title": bi("% der Fläche", "% of the area")},
                 "tooltip": [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
                             {"field": "wald_morgen", "title": bi("Wald, Morgen", "Forest, Morgen"), "format": ",.0f"},
                             {"field": "wald_ha", "title": bi("Wald, ha", "Forest, ha"), "format": ",.0f"},
                             {"field": "anteil_pct", "title": bi("% der Fläche", "% of the area"), "format": ".1f"},
                             {"field": "morgen_je_einw", "title": bi("Morgen je Einwohner", "Morgen per inhabitant"), "format": ".2f"},
                             {"field": "ha_je_einw", "title": bi("ha je Einwohner", "ha per inhabitant"), "format": ".2f"}]}}},
        {"id": "c4", "dataset": "domaene",
         "title": bi("Domänenwald 1647 und heute", "Domain forest 1647 and today"),
         "caption": bi("Fläche des Domänenwaldes (Hektar): 1647 Wald und Geräumde (gerodete Flächen), um 1868 Kammerforste. Die Gesamtfläche hat sich in 222 Jahren kaum verändert (259 Morgen).",
                       "Area of the domain forest (hectares): in 1647 woodland and cleared land (Geräumde), around 1868 chamber forests. The total area has hardly changed in 222 years (259 Morgen)."),
         "vegalite": {
             "height": 220,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "zeit_de", "en": "zeit_en"}, "type": "nominal", "sort": {"field": "zeit_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 220}},
                 "x": {"field": "ha", "type": "quantitative", "title": "ha", "axis": {"format": ",.0f"}},
                 "color": {"field": {"de": "art_de", "en": "art_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi("Wald", "Woodland"), bi("Geräumde (gerodete Flächen)", "Cleared land (Geräumde)"), bi("Kammerforste (Wald)", "Chamber forests (woodland)")]},
                           "legend": {"columns": 1, "labelLimit": 260}},
                 "tooltip": [{"field": {"de": "zeit_de", "en": "zeit_en"}, "title": bi("Zeitpunkt", "Time")}, {"field": {"de": "art_de", "en": "art_en"}, "title": bi("Art", "Kind")},
                             {"field": "morgen", "title": bi("Morgen", "Morgen"), "format": ","}, {"field": "ha", "title": "ha", "format": ",.0f"}]}}},
    ],
    "keywords": {
        "de": ["Wald", "Forstwirtschaft", "Kammerforste", "Domänenwald", "Privatwald", "Gemeindewald", "Stiftungswald", "Nadelwald", "Laubwald", "Waldfläche", "Waldbesitz"],
        "en": ["forest", "forestry", "chamber forests", "domain forest", "private woodland", "municipal forest", "coniferous", "deciduous", "forest area", "forest ownership"],
    },
    "related": ["forstwirtschaft-holzpreise-zuwachs", "landwirtschaft-bodennutzung-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
