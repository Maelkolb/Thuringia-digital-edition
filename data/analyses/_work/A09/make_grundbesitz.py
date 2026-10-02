"""A09 / analysis 3: Grundbesitz (pp. 224-225): Verteilung des landw. Bodens auf Hauptgrundbesitzer, Bauerngüter, Zersplitterung."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

# ---------------------------------------------------------------- p. 225 b3: owners
g = grid("225", "b3")
OWN = [(2, "Kammergüter", "Chamber estates (Kammergüter)"), (3, "Rittergüter", "Manorial estates (Rittergüter)"),
       (4, "Bäuerlicher Grundbesitz", "Peasant land")]
USE = [("Gärten", "Gardens"), ("Feld", "Arable land"), ("Wiesen", "Meadows"), ("Hutung", "Pasture"), ("Summe", "Total")]
besitzer = []
for oi, (ri, ode, oen) in enumerate(OWN):
    r = g[ri]
    for ui, (ude, uen) in enumerate(USE):
        morgen = num(r[1 + ui])
        pct = num(r[6 + ui])
        besitzer.append([ode, oen, oi + 1, ude, uen, ui + 1, morgen, pct, round(morgen * MORGEN_HA, 0)])
tot = [num(x) for x in g[5][1:6]]
print("p225 totals", tot)
for ui in range(5):
    print(USE[ui][0], round(sum(r[6] for r in besitzer if r[5] == ui + 1), 2), tot[ui], round(sum(r[7] for r in besitzer if r[5] == ui + 1), 2))

# ---------------------------------------------------------------- p. 224 b2: Bauerngüter by size class
g2 = grid("224", "b2")
SIZE = [("1–20 Morgen", "1–20 Morgen"), ("20–40 Morgen", "20–40 Morgen"), ("40–60 Morgen", "40–60 Morgen"),
        ("60–80 Morgen", "60–80 Morgen"), ("80–100 Morgen", "80–100 Morgen"), ("über 100 Morgen", "over 100 Morgen")]
LT = [(1, "Gera", "Gera"), (2, "Schleiz", "Schleiz"), (3, "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"), (4, "Fürstenthum", "Principality")]
bauern = []
for k, (ri, lde, len_) in enumerate(((1, "Gera", "Gera"), (2, "Schleiz", "Schleiz"), (3, "Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"), (4, "Fürstenthum", "Principality"))):
    r = g2[ri]
    for si, (sde, sen) in enumerate(SIZE):
        pct = None
        if ri == 4:
            pct = num(g2[5][1 + si])
        bauern.append([lde, len_, k + 1, sde, sen, si + 1, num(r[1 + si]), pct])
gera = [r[6] for r in bauern if r[0] == "Gera"]
schl = [r[6] for r in bauern if r[0] == "Schleiz"]
lobe = [r[6] for r in bauern if r[0] == "Lobenstein-Ebersdorf"]
fue = [r[6] for r in bauern if r[0] == "Fürstenthum"]
print("sizes", gera, sum(gera), schl, sum(schl), lobe, sum(lobe), fue, sum(fue))
sa = {"Gera": num(g2[1][7]), "Schleiz": num(g2[2][7]), "Lobenstein-Ebersdorf": num(g2[3][7]), "Fürstenthum": num(g2[4][7])}
print(sa)
ledige = {n: num(g2[i][9]) for n, i in (("Gera", 1), ("Schleiz", 2), ("Lobenstein-Ebersdorf", 3), ("Fürstenthum", 4))}
verb = {n: num(g2[i][8]) for n, i in (("Gera", 1), ("Schleiz", 2), ("Lobenstein-Ebersdorf", 3), ("Fürstenthum", 4))}
print("ledige", ledige, "verb", verb)

# ---------------------------------------------------------------- p. 224 b4: towns
g4 = grid("224", "b4")
CATS = [("gebundene Güter unter 60 Morgen", "closed farms under 60 Morgen"), ("gebundene Güter über 60 Morgen", "closed farms over 60 Morgen"),
        ("Grundstücksverbände", "plot associations (Grundstücksverbände)"), ("ledige Grundstücke", "free-standing plots (ledige Grundstücke)"),
        ("Hofraithen der Kleinhäusler", "cottagers' house plots (Hofraithen)")]
stadt = []
TOWNS = {}
for ti in range(6):
    r = g4[1 + ti]
    name = r[0].replace(" .", "").strip(" .")
    name = name.replace(". ", "").strip()
    TOWNS[ti] = name
    for ci, (cde, cen) in enumerate(CATS):
        stadt.append([name, ti + 1, cde, cen, ci + 1, num(r[1 + ci])])
print(TOWNS)
# ---------------------------------------------------------------- p. 224 b5: towns vs Flachland
g5 = grid("224", "b5")
sf = []
for ci, (cde, cen) in enumerate(CATS):
    for gi, (rowi, gde, gen) in enumerate(((1, "Städte", "Towns"), (2, "Flachland", "Lowland countryside"), (3, "Summe", "Total"))):
        r = g5[rowi]
        sf.append([cde, cen, ci + 1, gde, gen, gi + 1, num(r[1 + 2 * ci]), num(r[2 + 2 * ci])])
print(sf[:6])

# ---------------------------------------------------------------- numbers for the text
bz = {(r[0], r[3]): r for r in besitzer}
pct_b = {(r[0], r[3]): r[7] for r in besitzer}
morgen_b = {(r[0], r[3]): r[6] for r in besitzer}
big_share = pct_b[("Kammergüter", "Summe")] + pct_b[("Rittergüter", "Summe")]
bau_sum = morgen_b[("Bäuerlicher Grundbesitz", "Summe")]
bau_ha = bau_sum * MORGEN_HA
total_sum = tot[4]
n_farms = fue_total = sa["Fürstenthum"]
ledige_per_farm = ledige["Fürstenthum"] / sa["Fürstenthum"]
small_pct = 100 * (fue[0] + fue[1] + fue[2]) / sum(fue)
large_pct = 100 - small_pct


def over60(l):
    return 100 * (l[3] + l[4] + l[5]) / sum(l)


def under20(l):
    return 100 * l[0] / sum(l)


print(big_share, bau_sum, bau_ha, ledige_per_farm, small_pct, large_pct, over60(gera), over60(schl), over60(lobe), under20(gera), under20(schl), under20(lobe))
stadt_ledig_pct = [r for r in sf if r[0] == "ledige Grundstücke" and r[3] == "Städte"][0][7]
stadt_hof_pct = [r for r in sf if r[0] == "Hofraithen der Kleinhäusler" and r[3] == "Städte"][0][7]
stadt_klein_n = [r for r in sf if r[0] == "gebundene Güter unter 60 Morgen" and r[3] == "Städte"][0][6]
stadt_klein_pct = [r for r in sf if r[0] == "gebundene Güter unter 60 Morgen" and r[3] == "Städte"][0][7]
town_led = {r[0]: r[5] for r in stadt if r[2] == "ledige Grundstücke"}
town_hof = {r[0]: r[5] for r in stadt if r[2] == "Hofraithen der Kleinhäusler"}
top_led = max(town_led, key=town_led.get)
top_hof = max(town_hof, key=town_hof.get)
print(top_led, town_led[top_led], top_hof, town_hof[top_hof])
hut_k = pct_b[("Kammergüter", "Hutung")]
hut_b = pct_b[("Bäuerlicher Grundbesitz", "Hutung")]
wiese_b = pct_b[("Bäuerlicher Grundbesitz", "Wiesen")]
feld_b = pct_b[("Bäuerlicher Grundbesitz", "Feld")]

R_B3 = {"page": "225", "block": "b3", "rows": "r3-t6"}
R_BG = {"page": "224", "block": "b2", "rows": "r2-r6"}
R_ST = {"page": "224", "block": "b4", "rows": "r2-t8"}
R_SF = {"page": "224", "block": "b5", "rows": "r2-t4"}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


ana = {
    "id": "landwirtschaft-grundbesitz-1854",
    "title": bi("Grundbesitz: Güterklassen und Zersplitterung (um 1854)", "Landholding: kinds of owners and fragmentation (c. 1854)"),
    "category": "agriculture",
    "section": "t1-3-2",
    "sources": [R_BG, R_ST, R_SF, {"page": "224", "block": "b3"}, {"page": "225", "block": "b1"}, R_B3, {"page": "225", "block": "fn1"}],
    "summary": bi(
        f"Brückner vergleicht den landwirthschaftlichen Boden der drei Hauptgrundbesitzer – Kammergüter, Rittergüter und bäuerlicher Grundbesitz – und beschreibt den Bauernbesitz nach Größenklassen, Landestheilen und Städten. Die Diagramme zeigen, wie der Boden verteilt ist, wie viele Bauerngüter es in jeder Größenklasse gibt und wie stark Besitz in Städten und auf dem Land zersplittert ist.",
        f"Brückner compares the agricultural land of the three main landholders – chamber estates, manorial estates and peasant holdings – and describes peasant property by size class, district and town. The charts show how the land is distributed, how many peasant farms there are in each size class and how fragmented holdings are in towns and in the countryside."),
    "method": bi(
        "Die Zahlen stammen aus der Tabelle »Vergleichung des landwirthschaftlichen Bodens der drei Hauptgrundbesitzer« (S. 225, Block b3) und den Tabellen zum bäuerlichen Grundbesitz (S. 224, Blöcke b2, b4, b5). Die Prozentwerte sind Brückners (Anteil der Besitzergruppe an der jeweiligen Nutzungsart bzw. Anteil von Städten und Flachland); Hektarwerte sind mit Brückners Umrechnung 1 preuß. Morgen = 0,255322 ha (S. 832) berechnet. Die gedruckten Zeilen der Landestheile für Grundstücksverbände und ledige Grundstücke (S. 224) werden nicht in den Diagrammen verwendet, da sie nicht zu den gedruckten Summen passen (siehe Hinweise); die Diagramme stützen sich auf die Spalten der Größenklassen, die Zeilen »Städte/Flachland« und die Summen.",
        "The figures come from the table “Vergleichung des landwirthschaftlichen Bodens der drei Hauptgrundbesitzer” (p. 225, block b3) and from the tables on peasant landholding (p. 224, blocks b2, b4, b5). The percentages are Brückner's (share of the owner group in each kind of use, or share of towns and lowland countryside); hectare values are computed with Brückner's conversion 1 Prussian Morgen = 0.255322 ha (p. 832). The printed district rows for plot associations and free-standing plots (p. 224) are not used in the charts because they do not agree with the printed totals (see notes); the charts rely on the size-class columns, the “towns/countryside” rows and the totals."),
    "findings": [
        bi(f"Der bäuerliche Grundbesitz (einschließlich des städtischen Grundbesitzes) umfasst {de_num(pct_b[('Bäuerlicher Grundbesitz','Summe')],2)} % des landwirthschaftlichen Bodens ({de_num(bau_sum,0)} Morgen, rund {de_num(bau_ha,0)} ha); Kammer- und Rittergüter zusammen nur {de_num(big_share,2)} %.",
           f"Peasant landholding (including urban holdings) comprises {en_num(pct_b[('Bäuerlicher Grundbesitz','Summe')],2)} % of the agricultural land ({en_num(bau_sum,0)} Morgen, about {en_num(bau_ha,0)} ha); chamber and manorial estates together only {en_num(big_share,2)} %."),
        bi(f"Bei der Hutung ist der Anteil der Kammergüter mit {de_num(hut_k,2)} % am höchsten (Bauern {de_num(hut_b,2)} %), beim Feld {de_num(feld_b,2)} % und bei den Wiesen {de_num(wiese_b,2)} % in bäuerlicher Hand.",
           f"For pasture the share of the chamber estates is highest at {en_num(hut_k,2)} % (peasants {en_num(hut_b,2)} %); {en_num(feld_b,2)} % of the arable land and {en_num(wiese_b,2)} % of the meadows are in peasant hands."),
        bi(f"Von {de_num(sa['Fürstenthum'],0)} geschlossenen Bauerngütern haben {de_num(small_pct,2)} % weniger als 60 Morgen; Brückner rechnet die Güter über 60 Morgen mit {de_num(large_pct,2)} % als »große«. Am kleinteiligsten ist Gera ({de_num(under20(gera))} % der Güter mit 1–20 Morgen), am größten sind die Güter im Landestheil Schleiz ({de_num(over60(schl))} % über 60 Morgen, Gera {de_num(over60(gera))} %, Lobenstein-Ebersdorf {de_num(over60(lobe))} %).",
           f"Of {en_num(sa['Fürstenthum'],0)} closed peasant farms, {en_num(small_pct,2)} % have less than 60 Morgen; Brückner counts the farms over 60 Morgen, {en_num(large_pct,2)} %, as “large”. Gera has the smallest farms ({en_num(under20(gera))} % of its farms with 1–20 Morgen), farms are largest in the district of Schleiz ({en_num(over60(schl))} % over 60 Morgen, Gera {en_num(over60(gera))} %, Lobenstein-Ebersdorf {en_num(over60(lobe))} %)."),
        bi(f"Auf ein geschlossenes Bauerngut kommen {de_num(ledige_per_farm,1)} ledige Grundstücke (17 284 gegenüber {de_num(sa['Fürstenthum'],0)} Gütern) – nach Brückner Folge der Teilung der ursprünglichen Höfe durch Vererbung an mehrere Kinder und der Abfindung weichender Erben mit einzelnen Grundstücken.",
           f"There are {en_num(ledige_per_farm,1)} free-standing plots per closed peasant farm (17,284 against {en_num(sa['Fürstenthum'],0)} farms) – according to Brückner a consequence of the division of the original farms by inheritance among several children and of compensating the other heirs with single plots."),
        bi(f"Die Städte besitzen nur {de_num(stadt_klein_pct,2)} % der kleinen Höfe ({de_num(stadt_klein_n,0)} Höfe), aber {de_num(stadt_ledig_pct,2)} % der ledigen Grundstücke und {de_num(stadt_hof_pct,2)} % der Hofraithen der Kleinhäusler. Die meisten ledigen Grundstücke liegen in {top_led} ({de_num(town_led[top_led],0)}), die meisten Kleinhäusler-Hofraithen in {top_hof} ({de_num(town_hof[top_hof],0)}).",
           f"The towns hold only {en_num(stadt_klein_pct,2)} % of the small farms ({en_num(stadt_klein_n,0)} farms) but {en_num(stadt_ledig_pct,2)} % of the free-standing plots and {en_num(stadt_hof_pct,2)} % of the cottagers' house plots. Most free-standing plots lie in {top_led} ({en_num(town_led[top_led],0)}), most cottagers' house plots in {top_hof} ({en_num(town_hof[top_hof],0)})."),
    ],
    "caveats": [
        bi("Die Landestheil-Zeilen für Grundstücksverbände und ledige Grundstücke ergeben 900 bzw. 18 076, die gedruckte Summe lautet 890 bzw. 17 284 (und passt zur Summe aus Städten und Flachland). Am Faksimile ist die Vorlage so gedruckt; die Landestheil-Werte dieser Spalten wurden deshalb nicht ausgewertet.",
           "The district rows for plot associations and free-standing plots add up to 900 and 18,076, whereas the printed totals are 890 and 17,284 (which agree with the sum of towns and countryside). The source is printed like this in the facsimile; the district values of these columns were therefore not used."),
        bi("Der »bäuerliche Grundbesitz« schließt nach Brückners Fußnote den städtischen Grundbesitz ein; er ist also nicht gleichbedeutend mit dem Landbesitz von Bauern. Die Tabelle gibt Flächen nur für Garten, Feld, Wiese und Hutung an, nicht für Wald (vgl. die Analyse zur Waldfläche).",
           "According to Brückner's footnote, “peasant landholding” includes urban landholding; it is therefore not the same as land owned by farmers. The table gives areas only for garden, arable, meadow and pasture, not for woodland (see the analysis of forest area)."),
        bi("Die Güterklassen zählen Einheiten (geschlossene Bauerngüter), nicht Flächen; Brückners Einteilung »große Güter über 60 Morgen« ist eine Setzung des Autors.",
           "The size classes count units (closed peasant farms), not areas; Brückner's division into “large farms over 60 Morgen” is the author's convention."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "ha = Morgen × 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hectaren"},
    ],
    "datasets": [
        {"name": "besitzer", "title": bi("Landwirthschaftlicher Boden nach Hauptgrundbesitzern", "Agricultural land by main landholder"),
         "columns": [
             col("besitzer_de", "Grundbesitzer", "Landholder", "string"),
             col("besitzer_en", "Grundbesitzer (englisch)", "Landholder (English)", "string"),
             col("besitzer_nr", "Reihenfolge Besitzer", "Owner order", "integer", derived=True),
             col("nutzung_de", "Nutzungsart", "Kind of use", "string"),
             col("nutzung_en", "Nutzungsart (englisch)", "Kind of use (English)", "string"),
             col("nutzung_nr", "Reihenfolge Nutzung", "Use order", "integer", derived=True),
             col("morgen", "Fläche", "Area", "number", "preuß. Morgen"),
             col("pct", "Anteil an der Nutzungsart", "Share of the kind of use", "number", "%"),
             col("ha", "Fläche in Hektar", "Area in hectares", "number", "ha", derived=True, note="Morgen × 0,255322"),
         ],
         "rows": besitzer, "source_refs": [R_B3]},
        {"name": "bauerngueter", "title": bi("Geschlossene Bauerngüter nach Größenklassen", "Closed peasant farms by size class"),
         "columns": [
             col("landestheil_de", "Landestheil", "District", "string"),
             col("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             col("lt_nr", "Reihenfolge Landestheil", "District order", "integer", derived=True),
             col("klasse_de", "Größenklasse", "Size class", "string"),
             col("klasse_en", "Größenklasse (englisch)", "Size class (English)", "string"),
             col("klasse_nr", "Reihenfolge Klasse", "Class order", "integer", derived=True),
             col("anzahl", "Zahl der Güter", "Number of farms", "integer", "Güter"),
             col("pct", "Anteil (nur Fürstenthum gedruckt)", "Share (printed for the principality only)", "number", "%"),
         ],
         "rows": bauern, "source_refs": [R_BG]},
        {"name": "stadtgrundbesitz", "title": bi("Grundbesitz in den Städten", "Landholding in the towns"),
         "columns": [
             col("stadt", "Stadt", "Town", "string"),
             col("stadt_nr", "Reihenfolge Stadt", "Town order", "integer", derived=True),
             col("form_de", "Besitzform", "Kind of holding", "string"),
             col("form_en", "Besitzform (englisch)", "Kind of holding (English)", "string"),
             col("form_nr", "Reihenfolge Besitzform", "Order of holding", "integer", derived=True),
             col("anzahl", "Zahl", "Number", "integer"),
         ],
         "rows": stadt, "source_refs": [R_ST]},
        {"name": "staedte_flachland", "title": bi("Städte und Flachland im Vergleich", "Towns compared with the lowland countryside"),
         "columns": [
             col("form_de", "Besitzform", "Kind of holding", "string"),
             col("form_en", "Besitzform (englisch)", "Kind of holding (English)", "string"),
             col("form_nr", "Reihenfolge Besitzform", "Order of holding", "integer", derived=True),
             col("gebiet_de", "Gebiet", "Area", "string"),
             col("gebiet_en", "Gebiet (englisch)", "Area (English)", "string"),
             col("gebiet_nr", "Reihenfolge Gebiet", "Area order", "integer", derived=True),
             col("anzahl", "Zahl", "Number", "integer"),
             col("pct", "Anteil an der Summe", "Share of the total", "number", "%"),
         ],
         "rows": sf, "source_refs": [R_SF]},
    ],
    "charts": [
        {"id": "c1", "dataset": "besitzer",
         "title": bi("Wem gehört der landwirthschaftliche Boden?", "Who owns the agricultural land?"),
         "caption": bi("Anteil der drei Hauptgrundbesitzer an Gärten, Feld, Wiesen und Hutung des Fürstenthums (Brückners Prozentwerte). Die Hutung ist am stärksten in der Hand der Kammergüter und Rittergüter.",
                       "Share of the three main landholders in gardens, arable land, meadows and pasture of the principality (Brückner's percentages). Pasture is most strongly in the hands of the chamber and manorial estates."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "type": "nominal", "sort": {"field": "nutzung_nr", "op": "min"}, "title": None},
                 "x": {"field": "pct", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": bi("% der Fläche der jeweiligen Nutzung", "% of the area in the respective use")},
                 "color": {"field": {"de": "besitzer_de", "en": "besitzer_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi(o[1], o[2]) for o in OWN]}, "legend": {"columns": 1, "labelLimit": 300}},
                 "order": {"field": "besitzer_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "besitzer_de", "en": "besitzer_en"}, "title": bi("Grundbesitzer", "Landholder")},
                             {"field": {"de": "nutzung_de", "en": "nutzung_en"}, "title": bi("Nutzung", "Use")},
                             {"field": "morgen", "title": bi("Morgen", "Morgen"), "format": ",.2f"},
                             {"field": "ha", "title": "ha", "format": ",.0f"},
                             {"field": "pct", "title": bi("% der Nutzungsart", "% of the use"), "format": ".2f"}]}}},
        {"id": "c2", "dataset": "bauerngueter",
         "title": bi("Geschlossene Bauerngüter nach Größe", "Closed peasant farms by size"),
         "caption": bi("Zahl der geschlossenen Bauerngüter je Größenklasse und Landestheil. Gera hat viele kleine Güter, Schleiz viele mittlere und große.",
                       "Number of closed peasant farms per size class and district. Gera has many small farms, Schleiz many medium and large ones."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.landestheil_de != 'Fürstenthum'"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": {"de": "klasse_de", "en": "klasse_en"}, "type": "nominal", "sort": {"field": "klasse_nr", "op": "min"}, "title": bi("Größe des Guts", "Size of the farm"), "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "landestheil_de", "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]},
                 "y": {"field": "anzahl", "type": "quantitative", "title": bi("Zahl der Güter", "Number of farms")},
                 "color": {"field": "landestheil_de", "type": "nominal", "title": None, "scale": {"domain": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]}, "legend": {"labelLimit": 260}},
                 "tooltip": [{"field": "landestheil_de", "title": bi("Landestheil", "District")},
                             {"field": {"de": "klasse_de", "en": "klasse_en"}, "title": bi("Größenklasse", "Size class")},
                             {"field": "anzahl", "title": bi("Güter", "Farms")}]}}},
        {"id": "c3", "dataset": "staedte_flachland",
         "title": bi("Städte und Flachland: Zersplitterung des Besitzes", "Towns and lowland countryside: fragmentation of holdings"),
         "caption": bi("Anteil der Städte und des Flachlands an den Besitzformen (Brückners Prozentwerte). Städte haben fast keine Bauernhöfe, aber rund ein Drittel der ledigen Grundstücke und der Kleinhäusler-Hofraithen.",
                       "Share of the towns and of the lowland countryside in each kind of holding (Brückner's percentages). Towns have hardly any peasant farms but about a third of the free-standing plots and cottagers' house plots."),
         "vegalite": {
             "height": 240,
             "transform": [{"filter": "datum.gebiet_nr < 3"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": {"de": "form_de", "en": "form_en"}, "type": "nominal", "sort": {"field": "form_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
                 "x": {"field": "pct", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": bi("% der Summe", "% of the total")},
                 "color": {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi("Städte", "Towns"), bi("Flachland", "Lowland countryside")]}},
                 "order": {"field": "gebiet_nr", "type": "quantitative"},
                 "tooltip": [{"field": {"de": "form_de", "en": "form_en"}, "title": bi("Besitzform", "Kind of holding")},
                             {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "title": bi("Gebiet", "Area")},
                             {"field": "anzahl", "title": bi("Zahl", "Number"), "format": ","},
                             {"field": "pct", "title": "%", "format": ".2f"}]}}},
        {"id": "c4", "dataset": "stadtgrundbesitz",
         "title": bi("Ledige Grundstücke und Kleinhäusler in den Städten", "Free-standing plots and cottagers in the towns"),
         "caption": bi("Zahl der ledigen Grundstücke und der Hofraithen der Kleinhäusler in den sechs Städten. Tanna hat die meisten ledigen Grundstücke, Gera die meisten Kleinhäusler-Hofraithen.",
                       "Number of free-standing plots and of cottagers' house plots in the six towns. Tanna has the most free-standing plots, Gera the most cottagers' house plots."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.form_nr >= 4"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "stadt", "type": "nominal", "sort": {"field": "stadt_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": {"de": "form_de", "en": "form_en"}, "type": "nominal", "sort": [bi("ledige Grundstücke", "free-standing plots (ledige Grundstücke)"), bi("Hofraithen der Kleinhäusler", "cottagers' house plots (Hofraithen)")]},
                 "y": {"field": "anzahl", "type": "quantitative", "title": bi("Zahl", "Number")},
                 "color": {"field": {"de": "form_de", "en": "form_en"}, "type": "nominal", "title": None,
                           "scale": {"domain": [bi("ledige Grundstücke", "free-standing plots (ledige Grundstücke)"), bi("Hofraithen der Kleinhäusler", "cottagers' house plots (Hofraithen)")]},
                           "legend": {"columns": 1, "labelLimit": 300}},
                 "tooltip": [{"field": "stadt", "title": bi("Stadt", "Town")},
                             {"field": {"de": "form_de", "en": "form_en"}, "title": bi("Besitzform", "Kind of holding")},
                             {"field": "anzahl", "title": bi("Zahl", "Number"), "format": ","}]}}},
    ],
    "keywords": {
        "de": ["Grundbesitz", "Bauerngüter", "Kammergüter", "Rittergüter", "Zersplitterung", "Vererbung", "ledige Grundstücke", "Kleinhäusler", "Güterklassen", "Landwirtschaft"],
        "en": ["landholding", "peasant farms", "chamber estates", "manorial estates", "fragmentation", "inheritance", "cottagers", "farm size", "agriculture"],
    },
    "related": ["landwirtschaft-bodennutzung-1854", "landwirtschaft-kammer-rittergueter-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
