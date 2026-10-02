"""A10: Saline Heinrichshall - Absatz 1857/1863 (pp. 250-251, corrigendum p. 831)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

g = grid("251", "b2")          # r1 = header, r2..r8 = body, three place blocks side by side
CLEAN = {"Greiz . . . .": "Greiz", "Möschlitz . .": "Möschlitz", "Zeulenroda .": "Zeulenroda", "Gefell . . . .": "Gefell",
         "Ranis . . . .": "Ranis", "Ziegenrück .": "Ziegenrück", "Auma . . . .": "Auma", "Berga . . . .": "Berga",
         "Münchenbernsd.": "Münchenbernsdorf", "Neustadt a. d. O.": "Neustadt a. d. Orla", "Weida . . . .": "Weida",
         "Liebschwitz .": "Liebschwitz", "Hof . . . . .": "Hof", "Gera . . . .": "Gera", "Schleiz . . .": "Schleiz",
         "Hohenleuben": "Hohenleuben", "Saalburg . .": "Saalburg", "Lobenstein .": "Lobenstein",
         "Hirschberg .": "Hirschberg", "Heinrichshall": "Heinrichshall"}
places = []   # (clean, printed, v1857, v1863, source row)
for ri, r in enumerate(g[1:], start=2):
    for k in (0, 3, 6):
        if r[k].strip():
            places.append((CLEAN[r[k]], r[k], num(r[k + 1]), num(r[k + 2]), f"r{ri}"))
assert len(places) == 20, len(places)

debit_rows = []
for clean, printed, a, b, row in places:
    debit_rows.append([clean, 1857, a, row])
    debit_rows.append([clean, 1863, b, row])

# derived: change 1857 -> 1863 (a dash in 1863 = no deliveries -> 0)
change_rows = []
for clean, printed, a, b, row in places:
    b0 = b or 0
    change_rows.append([clean, a, b, b0 - a, row])

sum57 = sum(a for _, _, a, _, _ in places)
sum63 = sum(b or 0 for _, _, _, b, _ in places)
PRINTED57, PRINTED63 = 27527, 23898
lost = [(c, a) for c, _, a, b, _ in places if b is None]
lost_sum = sum(a for _, a in lost)
hof57, hof63 = [(a, b) for c, _, a, b, _ in places if c == "Hof"][0]
delta = {c: (b or 0) - a for c, _, a, b, _ in places}
top_gain = sorted(delta.items(), key=lambda kv: -kv[1])[:3]
others_gain = sum(v for c, v in delta.items() if c not in {x for x, _ in lost})
rank57 = [c for c, _, a, b, _ in sorted(places, key=lambda x: -x[2])][:5]
rank63 = [c for c, _, a, b, _ in sorted(places, key=lambda x: -(x[3] or 0))][:5]
lostset = {x for x, _ in lost}
n_up = sum(1 for c, v in delta.items() if v > 0 and c not in lostset)
n_down = sum(1 for c, v in delta.items() if v < 0 and c not in lostset)
n_same = 17 - n_up - n_down

# products ---------------------------------------------------------------
g4 = grid("251", "b4")
viehsalz = {1857: num(g4[1][1]), 1863: num(g4[2][1])}
gewerbe = {1857: num(g4[1][2]), 1863: num(g4[2][2])}
dung = {1857: num(g4[1][3]), 1863: num(g4[2][3])}
soole_fabrik = {1857: num(g4[1][4]), 1863: num(g4[2][4])}
soole_bad = {1857: num(g4[1][5]), 1863: num(g4[2][5])}
KOCH = {"1857": 27527, "1858": 29000, "1863": 23898, "Ø 1865–67": 29727}
VIEH_AVG = 2281
prod_rows = [
    ["Kochsalz", "Kochsalz", "1857", 27527, "Centner", "b1"],
    ["Kochsalz", "Kochsalz", "1858", 29000, "Centner", "b1"],
    ["Kochsalz", "Kochsalz", "1863", 23898, "Centner", "b1"],
    ["Kochsalz", "Kochsalz", "Ø 1865–67", 29727, "Centner", "b5"],
    ["Viehsalz", "Viehsalz", "1857", viehsalz[1857], "Centner", "b4"],
    ["Viehsalz", "Viehsalz", "1863", viehsalz[1863], "Centner", "b4"],
    ["Viehsalz", "Viehsalz", "Ø 1865–67", VIEH_AVG, "Centner", "b5"],
    ["Gewerbesalz", "Gewerbesalz", "1857", gewerbe[1857], "Centner", "b4"],
    ["Gewerbesalz", "Gewerbesalz", "1863", gewerbe[1863], "Centner", "b4"],
    ["Dungsalz", "Dungsalz", "1857", dung[1857], "Centner", "b4"],
    ["Dungsalz", "Dungsalz", "1863", dung[1863], "Centner", "b4"],
]
prod_rows = [[r[0], r[2], r[3], r[5]] for r in prod_rows]
EN_PROD = {"Kochsalz": "Table salt (Kochsalz)", "Viehsalz": "Cattle salt", "Gewerbesalz": "Industrial salt", "Dungsalz": "Manure salt"}

# stats for findings -------------------------------------------------------
drop = PRINTED57 - PRINTED63
drop_pct = drop / PRINTED57 * 100
hof_share57 = hof57 / PRINTED57 * 100
hof_share63 = hof63 / PRINTED63 * 100
soole_change = (soole_fabrik[1863] - soole_fabrik[1857]) / soole_fabrik[1857] * 100
vieh_drop = (VIEH_AVG - viehsalz[1863]) / viehsalz[1863] * 100
print("rank57", rank57, "rank63", rank63, "others_gain", others_gain)
print("sum57", sum57, "sum63", sum63, "lost", lost, lost_sum, "top gain", top_gain, "up/down", n_up, n_down)
print("hof", hof_share57, hof_share63, "soole", soole_change, "vieh", vieh_drop, "drop", drop, drop_pct)

PLACE = {"de": "Ort", "en": "Place"}
YEAR = {"de": "Jahr", "en": "Year"}
CTR = {"de": "Centner (Ctr.)", "en": "Hundredweight (Ctr.)"}

ana = {
    "id": "bergbau-saline-heinrichshall-absatz-1857-1863",
    "title": {"de": "Saline Heinrichshall: Absatz von Salz 1857 und 1863", "en": "Heinrichshall saltworks: salt sales in 1857 and 1863"},
    "category": "mining",
    "section": "t1-3-5",
    "sources": [
        {"page": "250", "block": "b3"},
        {"page": "251", "block": "b1"},
        {"page": "251", "block": "b2", "rows": "r1-r8"},
        {"page": "251", "block": "b4", "rows": "h1-r3"},
        {"page": "251", "block": "b5"},
        {"page": "251", "block": "b6"},
        {"page": "831", "block": "b5", "note": "Berichtigung zu S. 251: Wegfall der Debitstellen 1868"},
    ],
    "summary": {
        "de": "Die fürstliche Saline Heinrichshall bei Köstritz wurde nach Bohrversuchen seit 1822 gegründet; Brückner nennt die abgegebenen Mengen an Kochsalz für 1857, 1858 und 1863 und verteilt die Abgabe von 1857 und 1863 auf 20 Debitstellen. Die Diagramme zeigen die Abgabe je Verkaufsstelle, deren Veränderung zwischen beiden Jahren und die Mengen der übrigen Salzsorten.",
        "en": "The princely saltworks at Heinrichshall near Köstritz were founded after drilling trials that began in 1822. Brückner gives the quantities of table salt delivered in 1857, 1858 and 1863 and breaks down the deliveries of 1857 and 1863 by 20 sales points (Debitstellen). The charts show deliveries by sales point, the change between the two years and the quantities of the other salt grades.",
    },
    "method": {
        "de": "Die Tabelle auf S. 251 (3 × 7 Orte, 1857 und 1863) wurde Ort für Ort in das Langformat übertragen; ein Strich (»—«) bedeutet keine Lieferung und ist als fehlender Wert kodiert. Die Veränderung 1857–1863 ist die Differenz der beiden Jahre (Strich = 0). Die Mengen der übrigen Sorten stammen aus der zweiten Tabelle und dem Text auf S. 251. Maßeinheit Centner (Ctr.) wie gedruckt; 1 Zollcentner = 100 Zollpfund = 50 kg (Zollpfund = 0,5 kg, S. 832). Ortsnamen wurden aufgelöst (»Münchenbernsd.« zu Münchenbernsdorf, »Neustadt a. d. O.« zu Neustadt a. d. Orla).",
        "en": "The table on p. 251 (3 × 7 places, 1857 and 1863) was transferred place by place into long format; a dash (“—”) means no delivery and is coded as a missing value. The change 1857–1863 is the difference between the two years (dash = 0). The quantities of the other grades come from the second table and the text on p. 251. The unit is the hundredweight (Centner, Ctr.) as printed; 1 Zollcentner = 100 Zollpfund = 50 kg (Zollpfund = 0.5 kg, p. 832). Place names were expanded (“Münchenbernsd.” to Münchenbernsdorf, “Neustadt a. d. O.” to Neustadt a. d. Orla).",
    },
    "findings": [
        {"de": f"Die gedruckten Gesamtmengen an Kochsalz sinken von {de(PRINTED57)} Ctr. (1857) auf {de(PRINTED63)} Ctr. (1863), also um {de(drop)} Ctr. oder {de(drop_pct, 1)} %; 1865–1867 liegt der Durchschnitt mit {de(29727)} Ctr. wieder über dem Stand von 1857.",
         "en": f"The printed totals of table salt fall from {en(PRINTED57)} Ctr. (1857) to {en(PRINTED63)} Ctr. (1863), a decline of {en(drop)} Ctr. or {en(drop_pct, 1)} %; the 1865–1867 average of {en(29727)} Ctr. is above the 1857 level again."},
        {"de": f"Der Rückgang geht auf drei Abnehmer zurück, die 1863 nicht mehr beliefert wurden: Greiz, Möschlitz und Zeulenroda (zusammen {de(lost_sum)} Ctr. im Jahr 1857). Die übrigen 17 Orte zusammen legten laut Tabelle um {de(others_gain)} Ctr. zu; {n_up} Orte bezogen 1863 mehr, {n_down} weniger als 1857.",
         "en": f"The decline is due to three customers that were no longer supplied in 1863: Greiz, Möschlitz and Zeulenroda ({en(lost_sum)} Ctr. together in 1857). According to the table, the remaining 17 places together gained {en(others_gain)} Ctr.; {n_up} places took more in 1863 than in 1857, {n_down} took less."},
        {"de": f"Hof in Bayern ist mit {de(hof57)} Ctr. (1857) und {de(hof63)} Ctr. (1863) die mit Abstand größte Debitstelle ({de(hof_share57, 1)} % bzw. {de(hof_share63, 1)} % der gedruckten Gesamtmenge); 1857 folgen Greiz ({de(2932)} Ctr.), Gera, Lobenstein und Schleiz, 1863 Gera ({de(2868)} Ctr.), Schleiz und Lobenstein.",
         "en": f"Hof in Bavaria is by far the largest sales point with {en(hof57)} Ctr. (1857) and {en(hof63)} Ctr. (1863), {en(hof_share57, 1)} % and {en(hof_share63, 1)} % of the printed total; in 1857 it is followed by Greiz ({en(2932)} Ctr.), Gera, Lobenstein and Schleiz, in 1863 by Gera ({en(2868)} Ctr.), Schleiz and Lobenstein."},
        {"de": f"Die an die chemische Fabrik gelieferte Soole stieg von {de(soole_fabrik[1857])} auf {de(soole_fabrik[1863])} Eimer ({de(soole_change, 1)} %), die an das Bad Köstritz gelieferte sank von {de(soole_bad[1857])} auf {de(soole_bad[1863])} Eimer. Viehsalz fiel von {de(viehsalz[1863])} Ctr. (1863) auf durchschnittlich {de(VIEH_AVG)} Ctr. in den Jahren 1865–1867.",
         "en": f"The brine delivered to the chemical factory rose from {en(soole_fabrik[1857])} to {en(soole_fabrik[1863])} Eimer ({en(soole_change, 1)} %), while the brine supplied to the Köstritz spa fell from {en(soole_bad[1857])} to {en(soole_bad[1863])} Eimer. Cattle salt dropped from {en(viehsalz[1863])} Ctr. (1863) to an average of {en(VIEH_AVG)} Ctr. in 1865–1867."},
    ],
    "caveats": [
        {"de": f"Die Debitstellen-Tabelle ergibt addiert {de(sum57)} (1857) und {de(sum63)} Ctr. (1863); das sind {de(PRINTED57 - sum57)} bzw. {de(PRINTED63 - sum63)} Ctr. weniger als die im Text genannten Gesamtmengen ({de(PRINTED57)} und {de(PRINTED63)}). Die Transkription stimmt mit dem Druck überein (Faksimile geprüft); die Differenz steckt im Original.",
         "en": f"The sales-point table sums to {en(sum57)} (1857) and {en(sum63)} Ctr. (1863), which is {en(PRINTED57 - sum57)} and {en(PRINTED63 - sum63)} Ctr. less than the totals given in the text ({en(PRINTED57)} and {en(PRINTED63)}). The transcription agrees with the print (facsimile checked); the discrepancy lies in the original."},
        {"de": "Die Abgabe 1863 an Greiz, Möschlitz und Zeulenroda ist im Druck mit einem Strich bezeichnet; ob es sich um fehlende Lieferungen oder fehlende Angaben handelt, sagt der Text nicht. Brückner nennt als Einflussgröße die Verträge der Nachbarstaaten.",
         "en": "The 1863 entries for Greiz, Möschlitz and Zeulenroda are printed as a dash; the text does not say whether this means no deliveries or no data. Brückner names the treaties with neighboring states as an influence on sales."},
        {"de": "Nach Brückners Berichtigung zu S. 251 (S. 831) sind die Debitstellen mit dem freien Salzhandel im Zollverein ab 1868 weggefallen; die Zahlen betreffen also ein abgeschlossenes Absatzsystem.",
         "en": "According to Brückner's correction to p. 251 (p. 831) the sales points ceased to exist when the salt trade was freed throughout the Zollverein from 1868; the figures therefore describe a system that had come to an end."},
    ],
    "conversions": [
        {"from": "Centner (Zollcentner)", "to": "kg", "factor_or_formula": "1 Ctr. = 100 Zollpfund = 50 kg", "reference": "1 Zollpfund = 0,5 kg (S. 832)"},
    ],
    "datasets": [
        {"name": "debitstellen", "title": {"de": "Abgabe von Kochsalz an die Debitstellen", "en": "Table salt delivered to the sales points"},
         "columns": [
             {"name": "place", "label": PLACE, "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "ctr", "label": {"de": "Kochsalz", "en": "Table salt"}, "type": "integer", "unit": "Ctr.", "note": "Strich im Druck = leer"},
             {"name": "row", "label": {"de": "Zeile der Tabelle", "en": "Table row"}, "type": "string", "unit": None},
         ],
         "rows": debit_rows, "source_refs": [{"page": "251", "block": "b2", "rows": "r1-r8"}]},
        {"name": "veraenderung", "title": {"de": "Veränderung der Abgabe 1857 → 1863", "en": "Change in deliveries 1857 → 1863"},
         "columns": [
             {"name": "place", "label": PLACE, "type": "string", "unit": None},
             {"name": "ctr_1857", "label": {"de": "1857", "en": "1857"}, "type": "integer", "unit": "Ctr."},
             {"name": "ctr_1863", "label": {"de": "1863", "en": "1863"}, "type": "integer", "unit": "Ctr.", "note": "Strich im Druck = leer"},
             {"name": "change", "label": {"de": "Veränderung", "en": "Change"}, "type": "integer", "unit": "Ctr.", "derived": True},
             {"name": "row", "label": {"de": "Zeile der Tabelle", "en": "Table row"}, "type": "string", "unit": None},
         ],
         "rows": change_rows, "source_refs": [{"page": "251", "block": "b2", "rows": "r1-r8"}]},
        {"name": "produkte", "title": {"de": "Salzsorten der Saline", "en": "Salt grades of the saltworks"},
         "columns": [
             {"name": "product", "label": {"de": "Sorte", "en": "Grade"}, "type": "string", "unit": None},
             {"name": "period", "label": {"de": "Jahr bzw. Zeitraum", "en": "Year or period"}, "type": "string", "unit": None},
             {"name": "ctr", "label": {"de": "Menge", "en": "Quantity"}, "type": "integer", "unit": "Ctr."},
             {"name": "block", "label": {"de": "Quellblock S. 251", "en": "Source block p. 251"}, "type": "string", "unit": None},
         ],
         "rows": prod_rows, "source_refs": [{"page": "251", "block": "b1"}, {"page": "251", "block": "b4", "rows": "h1-r3"}, {"page": "251", "block": "b5"}]},
        {"name": "soole", "title": {"de": "Soole an die chemische Fabrik und das Bad Köstritz", "en": "Brine supplied to the chemical factory and the Köstritz spa"},
         "columns": [
             {"name": "recipient", "label": {"de": "Abnehmer", "en": "Recipient"}, "type": "string", "unit": None},
             {"name": "year", "label": YEAR, "type": "integer", "unit": None},
             {"name": "eimer", "label": {"de": "Soole", "en": "Brine"}, "type": "integer", "unit": "Eimer"},
         ],
         "rows": [["Chemische Fabrik", 1857, soole_fabrik[1857]], ["Chemische Fabrik", 1863, soole_fabrik[1863]],
                  ["Bad Köstritz", 1857, soole_bad[1857]], ["Bad Köstritz", 1863, soole_bad[1863]]],
         "source_refs": [{"page": "251", "block": "b4", "rows": "h1-r3"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "debitstellen",
         "title": {"de": "Kochsalz-Abgabe je Debitstelle", "en": "Table salt delivered per sales point"},
         "caption": {"de": "Centner Kochsalz 1857 und 1863, Orte nach der Summe beider Jahre geordnet. Greiz, Möschlitz und Zeulenroda haben 1863 keinen Eintrag (Strich im Druck).",
                     "en": "Hundredweights of table salt in 1857 and 1863, places ordered by the sum of both years. Greiz, Möschlitz and Zeulenroda have no entry in 1863 (dash in the print)."},
         "vegalite": {
             "height": 520,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "place", "type": "nominal", "sort": {"field": "ctr", "op": "sum", "order": "descending"}, "title": None},
                 "yOffset": {"field": "year", "type": "nominal"},
                 "x": {"field": "ctr", "type": "quantitative", "title": CTR},
                 "color": {"field": "year", "type": "nominal", "title": YEAR},
                 "tooltip": [{"field": "place", "title": PLACE}, {"field": "year", "title": YEAR}, {"field": "ctr", "title": CTR}]}}},
        {"id": "c2", "dataset": "veraenderung",
         "title": {"de": "Veränderung der Abgabe 1857 → 1863", "en": "Change in deliveries 1857 → 1863"},
         "caption": {"de": "Differenz in Centnern; negative Werte (links) sind Rückgänge. Die drei größten Verluste sind die 1863 nicht mehr belieferten Orte Greiz, Möschlitz und Zeulenroda.",
                     "en": "Difference in hundredweights; negative values (left) are declines. The three largest losses are the places no longer supplied in 1863: Greiz, Möschlitz and Zeulenroda."},
         "vegalite": {
             "height": 460,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "place", "type": "nominal", "sort": {"field": "change", "order": "descending"}, "title": None},
                 "x": {"field": "change", "type": "quantitative", "title": {"de": "Veränderung (Ctr.)", "en": "Change (Ctr.)"}},
                 "color": {"field": "change", "type": "quantitative", "scale": {"range": "diverging", "domainMid": 0}, "legend": None},
                 "tooltip": [{"field": "place", "title": PLACE}, {"field": "ctr_1857", "title": {"de": "1857 (Ctr.)", "en": "1857 (Ctr.)"}},
                             {"field": "ctr_1863", "title": {"de": "1863 (Ctr.)", "en": "1863 (Ctr.)"}}, {"field": "change", "title": {"de": "Veränderung (Ctr.)", "en": "Change (Ctr.)"}}]}}},
        {"id": "c3", "dataset": "produkte",
         "title": {"de": "Salzsorten der Saline", "en": "Salt grades produced"},
         "caption": {"de": "Centner je Sorte und Jahr bzw. Dreijahresdurchschnitt 1865–67 (Kochsalz und Viehsalz). Kochsalz ist das wichtigste Fabrikat; Gewerbe- und Dungsalz machen zusammen weniger als 1000 Ctr. aus.",
                     "en": "Hundredweights by grade and year, or three-year average 1865–67 (table salt and cattle salt only). Table salt is the main product; industrial and manure salt together amount to less than 1,000 Ctr."},
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "product", "type": "nominal", "sort": ["Kochsalz", "Viehsalz", "Gewerbesalz", "Dungsalz"], "title": {"de": "Sorte", "en": "Grade"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "period", "type": "nominal", "sort": ["1857", "1858", "1863", "Ø 1865–67"]},
                 "y": {"field": "ctr", "type": "quantitative", "title": CTR},
                 "color": {"field": "period", "type": "nominal", "sort": ["1857", "1858", "1863", "Ø 1865–67"], "title": {"de": "Jahr", "en": "Year"}},
                 "tooltip": [{"field": "product", "title": {"de": "Sorte", "en": "Grade"}}, {"field": "period", "title": {"de": "Jahr/Zeitraum", "en": "Year/period"}}, {"field": "ctr", "title": CTR}]}}},
    ],
    "keywords": {"de": ["Saline", "Heinrichshall", "Köstritz", "Kochsalz", "Soole", "Salzhandel", "Debitstellen", "Hof", "Bergbau"],
                 "en": ["saltworks", "Heinrichshall", "Köstritz", "table salt", "brine", "salt trade", "sales points", "mining"]},
    "related": ["bergbau-erzbergbau-zeitleiste-ober-unterland"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
