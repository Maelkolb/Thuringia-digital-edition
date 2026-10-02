"""A10: Geburtsort/Zuzug 1864 (p. 105) and Auswanderung 1867 (p. 118)."""
import re
from common import *

# ---------------------------------------------------------------- birthplace (p.105 b3)
g = grid("105", "b3")
LABEL = {"Gera Stadt": ("Gera", "Städte"), "Gera Plattland": ("Gera", "Landorte"), "Gera Summe": ("Gera", "Zusammen"),
         "Schleiz Städte": ("Schleiz", "Städte"), "Schleiz Plattland": ("Schleiz", "Landorte"), "Schleiz Summe": ("Schleiz", "Zusammen"),
         "Lobenstein-Ebersdorf Städte": ("Lobenstein-Ebersdorf", "Städte"), "Lobenstein-Ebersdorf Plattland": ("Lobenstein-Ebersdorf", "Landorte"),
         "Lobenstein-Ebersdorf Summe": ("Lobenstein-Ebersdorf", "Zusammen"),
         "Fürstenthum Städte": ("Reuß j. L.", "Städte"), "Fürstenthum Plattland": ("Reuß j. L.", "Landorte"), "Fürstenthum Summe": ("Reuß j. L.", "Zusammen")}
ORIG = ["Geburtsgemeinde", "andere Gemeinde", "auswärts"]
birth = []
pop = {}
for r in g[1:13]:
    k, area = LABEL[r[0]]
    tot = 0
    for i, o in enumerate(ORIG):
        n, p = inum(r[1 + 2 * i]), num(r[2 + 2 * i])
        birth.append([k, area, o, n, p])
        tot += n
    if area == "Zusammen":
        pop[k] = tot
print(pop)
B = {(r[0], r[1], r[2]): r for r in birth}

# ---------------------------------------------------------------- origin of the foreign-born (p.105 b5)
gf = grid("105", "b5")
NAMES = {"S.-Weimar,": "S.-Weimar", "S.-Altenburg,": "S.-Altenburg", "Reuß ä. L.,": "Reuß ä. L.", "S.-Meiningen,": "S.-Meiningen",
         "S.-Coburg-Gotha,": "S.-Coburg-Gotha", "Schwarzburg-Rudolstadt,": "Schwarzburg-Rudolstadt", "\" Sondershausen,": "Schwarzburg-Sondershausen",
         "das übrige Deutschland,": "übriges Deutschland", "Europa,": "Europa", "die außereuropäischen Länder.": "außereuropäische Länder"}
origin = []
for r in gf[:10]:
    origin.append([NAMES[r[1]], float(re.match(r"(\d+,\d+)", r[0]).group(1).replace(",", "."))])
printed_sum = float(re.search(r"(\d+,\d+)", gf[10][0]).group(1).replace(",", "."))
parts_sum = round(sum(v for _, v in origin), 2)
print(origin, parts_sum, printed_sum)
thu = round(sum(v for n, v in origin[:7]), 2)

# ---------------------------------------------------------------- emigration 1867 (p.118 b5, b6)
ge = grid("118", "b5")
DIST_COLS = {"Gera": 1, "Schleiz": 2, "Lobenstein-Ebersdorf": 3, "Reuß j. L.": 4}
emig = []
for r in ge[1:5]:
    grp = r[0]
    for k, j in DIST_COLS.items():
        pct = num(r[5]) if k == "Reuß j. L." else None
        emig.append([k, grp, inum(r[j]), pct])
E = {(r[0], r[1]): r[2] for r in emig}
for k in DIST_COLS:
    assert E[(k, "Männer")] + E[(k, "Frauen")] + E[(k, "Kinder")] == E[(k, "Summe")]
items = block("118", "b6")["items"]
DEST_KEYS = ["andere Staaten des norddeutschen Bundes", "Bayern", "Baden", "Oesterreich", "Rußland", "Nordamerika", "Brasilien"]
dest = []
for key, it in zip(DEST_KEYS, items[1:8]):
    dest.append([key, int(re.match(r"(\d+)", it["text"]).group(1))])
assert sum(v for _, v in dest) == E[("Reuß j. L.", "Summe")] == int(re.search(r"(\d+)", items[8]["text"]).group(1))
print(dest)
emig_rate = []
for k in DIST_COLS:
    n = E[(k, "Summe")]
    emig_rate.append([k, n, pop[k], round(n / pop[k] * 1000, 2)])
print(emig_rate)

# ---- numbers for the texts
bf = lambda k, a, o: B[(k, a, o)][4]
F = "Reuß j. L."
mobile = min(DISTRICTS[:3], key=lambda k: bf(k, "Zusammen", ORIG[0]))
settled = max(DISTRICTS[:3], key=lambda k: bf(k, "Zusammen", ORIG[0]))
assert mobile == "Gera" and settled == "Lobenstein-Ebersdorf"
assert all(bf(k, "Städte", ORIG[0]) > bf(k, "Landorte", ORIG[0]) for k in DISTRICTS[:3])
R = {r[0]: r for r in emig_rate}
d_sorted = sorted(dest, key=lambda r: -r[1])
tot_e = E[(F, "Summe")]
men, women, kids = E[(F, "Männer")], E[(F, "Frauen")], E[(F, "Kinder")]
assert max(DISTRICTS[:3], key=lambda k: R[k][3]) == "Lobenstein-Ebersdorf"
assert max(DISTRICTS[:3], key=lambda k: R[k][1]) == "Lobenstein-Ebersdorf"
north = dict(dest)["andere Staaten des norddeutschen Bundes"]
na = dict(dest)["Nordamerika"]
print(thu, thu / parts_sum * 100)

import json
_A06 = json.loads((ROOT / "data" / "analyses" / "bevoelkerung-geburtensaldo-wanderung-1859-1867.json").read_text(encoding="utf-8"))
_per = next(d for d in _A06["datasets"] if d["name"] == "periods")
_cols = [c["name"] for c in _per["columns"]]
_row = next(r for r in _per["rows"] if r[0] == "Fürstenthum" and r[1] == "1865–1867")
NET_EM = _row[_cols.index("net_emigration")]
print("net emigration 1865-67 (A06):", NET_EM, NET_EM / 3)

ORIG_EN = {"Geburtsgemeinde": "Same municipality", "andere Gemeinde": "Other municipality", "auswärts": "Born elsewhere"}
ORIG_DE = {"Geburtsgemeinde": "Geburtsgemeinde", "andere Gemeinde": "Andere Gemeinde", "auswärts": "Auswärts geboren"}
OR_EN = {"S.-Weimar": "Saxe-Weimar", "S.-Altenburg": "Saxe-Altenburg", "Reuß ä. L.": "Reuss (elder line)", "S.-Meiningen": "Saxe-Meiningen",
         "S.-Coburg-Gotha": "Saxe-Coburg-Gotha", "Schwarzburg-Rudolstadt": "Schwarzburg-Rudolstadt", "Schwarzburg-Sondershausen": "Schwarzburg-Sondershausen",
         "übriges Deutschland": "Rest of Germany", "Europa": "Europe", "außereuropäische Länder": "Non-European countries"}
OR_DE = {"übriges Deutschland": "Übriges Deutschland", "Europa": "Europa", "außereuropäische Länder": "Außereuropäische Länder"}
GRP_EN = {"Männer": "Men", "Frauen": "Women", "Kinder": "Children"}
DEST_EN = {"andere Staaten des norddeutschen Bundes": "Other states of the North German Confederation", "Bayern": "Bavaria", "Baden": "Baden",
           "Oesterreich": "Austria", "Rußland": "Russia", "Nordamerika": "North America", "Brasilien": "Brazil"}
DEST_DE = {"andere Staaten des norddeutschen Bundes": "Andere Staaten des Norddeutschen Bundes", "Oesterreich": "Österreich", "Rußland": "Russland"}

ana = {
    "id": "bevoelkerung-wanderung-1864-1867",
    "title": bi("Geburtsort, Zuzug und Auswanderung 1864 und 1867", "Place of birth, immigration and emigration, 1864 and 1867"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [ref("105", "b2"), ref("105", "b3", "r2-r13"), ref("105", "b4"), ref("105", "b5", "h1-t11"), ref("118", "b4"), ref("118", "b5", "h1-t5"), ref("118", "b6", "i1-i9")],
    "summary": bi(
        f"Brückner gliedert die Bevölkerung von 1864 nach dem Geburtsort (Geburtsgemeinde, andere Gemeinde im Fürstenthum, auswärts) und nennt die Herkunftsländer der außerhalb Geborenen; für 1867 gibt er erstmals die Auswanderung nach Bezirk, Personengruppe und Ziel an. {fde(bf(F, 'Zusammen', ORIG[0]))} Procent der Bevölkerung lebten 1864 in ihrer Geburtsgemeinde, {fde(bf(F, 'Zusammen', ORIG[2]))} Procent waren auswärts geboren; 1867 wanderten {tot_e} Menschen aus ({fde(num('0,34'))} Procent der Bevölkerung), die meisten in andere Staaten des Norddeutschen Bundes oder nach Nordamerika.",
        f"Brückner divides the population of 1864 by place of birth (municipality of residence, other municipality in the principality, elsewhere) and gives the countries of origin of those born outside; for 1867 he gives for the first time emigration by district, group of persons and destination. In 1864 {fen(bf(F, 'Zusammen', ORIG[0]))} per cent of the population lived in the municipality where they were born and {fen(bf(F, 'Zusammen', ORIG[2]))} per cent were born elsewhere; in 1867 {tot_e} people emigrated ({fen(0.34)} per cent of the population), mostly to other states of the North German Confederation or to North America."),
    "method": bi(
        "Übernommen wurden die Tabelle S. 105 (Bevölkerung 1864 nach Geburtsort je Landestheil, getrennt nach Städten und Plattland, absolut und in Procent), die Liste der Herkunftsländer der auswärts Geborenen (S. 105, in Procent der gesamten Bevölkerung) sowie die Auswanderungstabelle und die Zielliste von S. 118. Die Bevölkerungszahl 1864 je Landestheil ergibt sich als Summe der drei gedruckten Spalten der Tabelle S. 105; sie dient (derived) dazu, die Auswanderer von 1867 auf 1000 Einwohner zu beziehen (Annäherung, da die Bevölkerung 1867 etwas höher lag). Alle übrigen Werte sind gedruckte Zahlen.",
        "The table on p. 105 (population of 1864 by place of birth per district, split into towns and rural area, in absolute numbers and per cent), the list of countries of origin of those born elsewhere (p. 105, in per cent of the total population), and the emigration table and destination list from p. 118 were used. The population of 1864 per district is the sum of the three printed columns of the table on p. 105; it is used (derived) to relate the emigrants of 1867 to 1,000 inhabitants (an approximation, since the population in 1867 was somewhat higher). All other values are printed figures."),
    "findings": [
        bi(f"{fde(bf(F, 'Zusammen', ORIG[0]))} Procent der Bevölkerung des Fürstenthums wohnten 1864 in ihrer Geburtsgemeinde, {fde(bf(F, 'Zusammen', ORIG[1]))} Procent waren in einer anderen Gemeinde des Landes und {fde(bf(F, 'Zusammen', ORIG[2]))} Procent auswärts geboren. Am sesshaftesten ist Lobenstein-Ebersdorf ({fde(bf(settled, 'Zusammen', ORIG[0]))} Procent in der Geburtsgemeinde), am beweglichsten Gera ({fde(bf(mobile, 'Zusammen', ORIG[0]))}).",
           f"{fen(bf(F, 'Zusammen', ORIG[0]))} per cent of the principality's population lived in 1864 in the municipality where they were born, {fen(bf(F, 'Zusammen', ORIG[1]))} per cent were born in another municipality of the country and {fen(bf(F, 'Zusammen', ORIG[2]))} per cent elsewhere. Lobenstein-Ebersdorf is the most settled ({fen(bf(settled, 'Zusammen', ORIG[0]))} per cent in the birth municipality), Gera the most mobile ({fen(bf(mobile, 'Zusammen', ORIG[0]))})."),
        bi(f"In jedem Landestheil liegt der Anteil der in der Wohngemeinde Geborenen in den Städten über dem des Plattlandes (Gera {fde(bf('Gera', 'Städte', ORIG[0]))} gegenüber {fde(bf('Gera', 'Landorte', ORIG[0]))}, Schleiz {fde(bf('Schleiz', 'Städte', ORIG[0]))} gegenüber {fde(bf('Schleiz', 'Landorte', ORIG[0]))}, Lobenstein-Ebersdorf {fde(bf('Lobenstein-Ebersdorf', 'Städte', ORIG[0]))} gegenüber {fde(bf('Lobenstein-Ebersdorf', 'Landorte', ORIG[0]))}); im Fürstenthum insgesamt sind die Werte fast gleich ({fde(bf(F, 'Städte', ORIG[0]))} und {fde(bf(F, 'Landorte', ORIG[0]))}).",
           f"In every district the share of those born in the municipality of residence is higher in the towns than in the rural area (Gera {fen(bf('Gera', 'Städte', ORIG[0]))} against {fen(bf('Gera', 'Landorte', ORIG[0]))}, Schleiz {fen(bf('Schleiz', 'Städte', ORIG[0]))} against {fen(bf('Schleiz', 'Landorte', ORIG[0]))}, Lobenstein-Ebersdorf {fen(bf('Lobenstein-Ebersdorf', 'Städte', ORIG[0]))} against {fen(bf('Lobenstein-Ebersdorf', 'Landorte', ORIG[0]))}); for the principality as a whole the values are almost equal ({fen(bf(F, 'Städte', ORIG[0]))} and {fen(bf(F, 'Landorte', ORIG[0]))})."),
        bi(f"Von den auswärts Geborenen stammen die meisten aus Thüringen und dem übrigen Deutschland: Sachsen-Weimar {fde(dict(origin)['S.-Weimar'])}, Sachsen-Altenburg {fde(dict(origin)['S.-Altenburg'])} und Reuß ä. L. {fde(dict(origin)['Reuß ä. L.'])} Procent der Bevölkerung; die thüringischen Staaten zusammen {fde(thu)} Procent, das übrige Deutschland {fde(dict(origin)['übriges Deutschland'])}. Aus „Europa“ (vermutlich außerhalb Deutschlands) und den außereuropäischen Ländern stammen zusammen nur {fde(dict(origin)['Europa'] + dict(origin)['außereuropäische Länder'])} Procent.",
           f"Most of those born elsewhere come from Thuringia and the rest of Germany: Saxe-Weimar {fen(dict(origin)['S.-Weimar'])}, Saxe-Altenburg {fen(dict(origin)['S.-Altenburg'])} and Reuss elder line {fen(dict(origin)['Reuß ä. L.'])} per cent of the population; the Thuringian states together {fen(thu)} per cent, the rest of Germany {fen(dict(origin)['übriges Deutschland'])}. “Europe” (presumably outside Germany) and the non-European countries together account for only {fen(dict(origin)['Europa'] + dict(origin)['außereuropäische Länder'])} per cent."),
        bi(f"1867 wanderten {tot_e} Menschen aus ({men} Männer, {women} Frauen, {kids} Kinder; {fde(0.34)} Procent der Bevölkerung). Lobenstein-Ebersdorf hat mit {fde(R['Lobenstein-Ebersdorf'][3])} Auswanderern auf 1000 Einwohner die höchste Rate, vor Gera ({fde(R['Gera'][3])}) und Schleiz ({fde(R['Schleiz'][3])}).",
           f"In 1867 {tot_e} people emigrated ({men} men, {women} women, {kids} children; {fen(0.34)} per cent of the population). Lobenstein-Ebersdorf has the highest rate with {fen(R['Lobenstein-Ebersdorf'][3])} emigrants per 1,000 inhabitants, ahead of Gera ({fen(R['Gera'][3])}) and Schleiz ({fen(R['Schleiz'][3])})."),
        bi(f"{north} der {tot_e} Auswanderer ({fde(north / tot_e * 100, 1)} Procent) zogen in andere Staaten des Norddeutschen Bundes, {na} ({fde(na / tot_e * 100, 1)} Procent) nach Nordamerika, 9 nach Brasilien und 8 nach Russland.",
           f"{north} of the {tot_e} emigrants ({fen(north / tot_e * 100, 1)} per cent) moved to other states of the North German Confederation, {na} ({fen(na / tot_e * 100, 1)} per cent) to North America, 9 to Brazil and 8 to Russia."),
    ],
    "caveats": [
        bi(f"Die Angaben zum Geburtsort sind Bestandsgrößen (Bevölkerung 1864), keine Zuwanderung eines bestimmten Jahres; Rückkehrer und im Ausland geborene Kinder Einheimischer sind darin enthalten. Die Auswanderung ist ein einzelnes Jahr (1867, erste Erhebung); die gemeldeten {tot_e} Auswanderer erklären nur einen Teil des aus den Zählungen abgeleiteten Wanderungsverlusts (S. 98 f.: {fint_de(NET_EM)} Personen 1865–1867, also etwa {fde(NET_EM / 3, 0)} im Jahr; vgl. die Auswertung zu Geburtenüberschuss und Wanderung).",
           f"The figures on place of birth are stocks (population 1864), not the immigration of a particular year; returning migrants and children of local parents born abroad are included. Emigration is a single year (1867, first survey); the {tot_e} registered emigrants explain only part of the migration loss derived from the censuses (p. 98 f.: {fint_en(NET_EM)} people in 1865–1867, i.e. about {fen(NET_EM / 3, 0)} a year; cf. the analysis of natural increase and migration)."),
        bi("Einzelne gedruckte Werte sind uneinheitlich: Für Lobenstein-Ebersdorf, Plattland, ergeben die drei Prozentzahlen 101 (75,26 + 14,51 + 11,23; aus den Zahlen folgen 10,24 für „auswärts“). Die Herkunftsliste addiert sich zu " + fde(parts_sum) + ", gedruckt ist als Summe " + fde(printed_sum) + ". Alle Werte stehen wie gedruckt im Datensatz.",
           "Some printed values are inconsistent: for Lobenstein-Ebersdorf, rural area, the three percentages add up to 101 (75.26 + 14.51 + 11.23; the counts give 10.24 for “elsewhere”). The list of origins adds up to " + fen(parts_sum) + ", the printed total is " + fen(printed_sum) + ". All values are in the dataset as printed."),
        bi("„Europa“ in der Herkunftsliste ist nicht näher erläutert (vermutlich Europa außerhalb Deutschlands). Das Bezugsjahr der Herkunftsliste ist 1864.",
           "“Europa” in the list of origins is not explained further (presumably Europe outside Germany). The reference year of the list of origins is 1864."),
    ],
    "datasets": [
        {"name": "birthplace", "title": bi("Bevölkerung 1864 nach Geburtsort", "Population in 1864 by place of birth"),
         "columns": [col("district", "Landestheil", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte (Plattland) / Zusammen (Summe)"),
                     col("origin", "Geburtsort", "Place of birth", "string"),
                     col("persons", "Personen", "Persons", "integer", "Personen"),
                     col("pct", "Procent der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": birth, "source_refs": [ref("105", "b3", "r2-r13")]},
        {"name": "origin_foreign", "title": bi("Herkunft der auswärts Geborenen", "Origin of those born elsewhere"),
         "columns": [col("origin", "Herkunft", "Origin", "string"),
                     col("pct_pop", "Procent der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": origin, "source_refs": [ref("105", "b5", "h1-t11")]},
        {"name": "emigration", "title": bi("Auswanderer 1867 nach Landestheil und Personengruppe", "Emigrants in 1867 by district and group"),
         "columns": [col("district", "Landestheil", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("group", "Gruppe", "Group", "string", note="Männer / Frauen / Kinder / Summe"),
                     col("persons", "Auswanderer", "Emigrants", "integer", "Personen"),
                     col("pct_pop", "Procent der betreffenden Bevölkerung", "Per cent of the respective population", "number", "%", note="nur für das Fürstenthum gedruckt")],
         "rows": emig, "source_refs": [ref("118", "b5", "h1-t5")]},
        {"name": "emigration_dest", "title": bi("Ziele der Auswanderer 1867", "Destinations of the emigrants in 1867"),
         "columns": [col("destination", "Ziel", "Destination", "string"),
                     col("persons", "Auswanderer", "Emigrants", "integer", "Personen")],
         "rows": dest, "source_refs": [ref("118", "b6", "i2-i8")]},
        {"name": "emigration_rate", "title": bi("Auswanderer 1867 auf 1000 Einwohner", "Emigrants in 1867 per 1,000 inhabitants"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("emigrants", "Auswanderer 1867", "Emigrants 1867", "integer", "Personen"),
                     col("population_1864", "Bevölkerung 1864", "Population 1864", "integer", "Personen", derived=True, note="Summe der drei gedruckten Spalten der Geburtsorttabelle"),
                     col("per_1000", "Auswanderer auf 1000 Einwohner", "Emigrants per 1,000 inhabitants", "number", "‰", derived=True)],
         "rows": emig_rate, "source_refs": [ref("118", "b5", "t5"), ref("105", "b3", "r2-r13")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "birthplace",
         "title": bi("Bevölkerung 1864 nach Geburtsort", "Population in 1864 by place of birth"),
         "caption": bi("Anteil der in der Wohngemeinde, in einer anderen Gemeinde des Fürstenthums und auswärts (außerhalb des Fürstenthums) Geborenen, je Landestheil, getrennt nach Städten und Plattland (gedruckte Procentzahlen).",
                       "Share of those born in the municipality of residence, in another municipality of the principality and elsewhere (outside the principality), per district, split into towns and rural area (printed percentages)."),
         "vegalite": {"height": 380,
                      "transform": [{"calculate": {"de": "datum.district + ' · ' + datum.area",
                                                   "en": "datum.district + ' · ' + (datum.area == 'Städte' ? 'towns' : (datum.area == 'Landorte' ? 'rural' : 'total'))"}, "as": "place"},
                                    {"calculate": "indexof(['Gera', 'Schleiz', 'Lobenstein-Ebersdorf', 'Reuß j. L.'], datum.district) * 10 + indexof(['Städte', 'Landorte', 'Zusammen'], datum.area)", "as": "ord"},
                                    ordk("origin", ORIG)],
                      "mark": "bar",
                      "encoding": {
                          "y": {"field": "place", "type": "nominal", "sort": {"field": "ord", "op": "min"}, "title": None, "axis": {"labelLimit": 300}},
                          "x": {"field": "pct", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population"), "stack": "zero", "scale": {"domain": [0, 101], "nice": False}, "axis": {"values": [0, 20, 40, 60, 80, 100]}},
                          "color": {"field": "origin", "type": "nominal", "title": None, "scale": {"domain": ORIG},
                                    "legend": {"orient": "right", "direction": "vertical", "labelLimit": 190, "labelExpr": lab_expr2(ORIG_DE, ORIG_EN)}},
                          "order": {"field": "ordk", "type": "quantitative", "sort": "ascending"},
                          "tooltip": [tip("place", "Landestheil und Gebiet", "District and area"), tip("origin", "Geburtsort", "Place of birth"),
                                      tip("persons", "Personen", "Persons"), tip("pct", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c2", "dataset": "origin_foreign",
         "title": bi("Herkunft der auswärts Geborenen", "Origin of those born elsewhere"),
         "caption": bi("In Procent der gesamten Bevölkerung von 1864 (Summe nach Brückner 14,48; die Einzelwerte addieren sich zu 14,43).",
                       "In per cent of the total population of 1864 (total according to Brückner 14.48; the individual values add up to 14.43)."),
         "vegalite": {"height": 340, "mark": "bar",
                      "encoding": {
                          "y": {"field": "origin", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelExpr": lab_expr2(OR_DE, OR_EN), "labelLimit": 300}},
                          "x": {"field": "pct_pop", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population")},
                          "tooltip": [tip("origin", "Herkunft", "Origin"), tip("pct_pop", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c3", "dataset": "emigration",
         "title": bi("Auswanderer 1867 nach Landestheil", "Emigrants in 1867 by district"),
         "caption": bi("Männer, Frauen und Kinder übereinander gestapelt; die Gesamthöhe ist die Zahl der Auswanderer des Landestheils.",
                       "Men, women and children stacked; the total height is the number of emigrants from the district."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.district != 'Reuß j. L.' && datum.group != 'Summe'"}, ordk("group", ["Männer", "Frauen", "Kinder"])], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS[:3], "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "y": {"field": "persons", "type": "quantitative", "title": bi("Auswanderer", "emigrants"), "stack": "zero"},
                          "color": {"field": "group", "type": "nominal", "title": None, "scale": {"domain": ["Männer", "Frauen", "Kinder"]},
                                    "legend": {"labelExpr": lab_expr2({"Männer": "Männer", "Frauen": "Frauen", "Kinder": "Kinder"}, GRP_EN)}},
                          "order": {"field": "ordk", "type": "quantitative", "sort": "ascending"},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("group", "Gruppe", "Group"), tip("persons", "Auswanderer", "Emigrants")]}}},
        {"id": "c4", "dataset": "emigration_dest",
         "title": bi("Ziele der Auswanderer 1867", "Destinations of the emigrants in 1867"),
         "caption": bi("Zahl der Auswanderer des Fürstenthums nach Zielland (Summe 296).",
                       "Number of emigrants from the principality by destination (total 296)."),
         "vegalite": {"height": 300, "mark": "bar",
                      "encoding": {
                          "y": {"field": "destination", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelExpr": lab_expr2(DEST_DE, DEST_EN), "labelLimit": 520}},
                          "x": {"field": "persons", "type": "quantitative", "title": bi("Auswanderer", "emigrants")},
                          "tooltip": [tip("destination", "Ziel", "Destination"), tip("persons", "Auswanderer", "Emigrants")]}}},
    ],
    "transcription_issues": [
        {"page": "105", "block": "b3", "cell": "r9c7", "transcribed": "11,23", "facsimile": "11,23", "checked_facsimile": True,
         "note": "Lobenstein-Ebersdorf, Plattland, auswärts: 1831 of 17887 = 10,24 %; the three printed percentages add to 101. Printer's error in the original."},
        {"page": "105", "block": "b5", "transcribed": "Summe 14,48", "facsimile": "Summe 14,48", "checked_facsimile": True,
         "note": "The ten printed shares add up to 14,43, not 14,48."},
    ],
    "keywords": {"de": ["Geburtsort", "Zuzug", "Einwanderung", "Auswanderung", "Wanderung", "Nordamerika", "Norddeutscher Bund", "Bevölkerungsstatistik"],
                 "en": ["place of birth", "immigration", "emigration", "migration", "North America", "North German Confederation", "population statistics"]},
    "related": ["bevoelkerung-geburtensaldo-wanderung-1859-1867", "bevoelkerung-natuerlicher-zuwachs-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
