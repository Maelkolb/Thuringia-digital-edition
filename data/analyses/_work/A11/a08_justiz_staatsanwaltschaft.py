"""A11-08: Strafsachen vor den Kreisgerichten: Staatsanwaltschaften 1864-1867 und Verurteilte nach Alter und Beruf (pp. 288-289)."""
from common import *

g2 = grid("288", "b2")
g4 = grid("288", "b4")
g6 = grid("288", "b6")
N = lambda x: num(x) or 0

# --- offices by year (b2): rows 1..4 Gera 1864..1867, 5..8 Schleiz 1864..1867
MEAS = [  # (key, de, en, column in the grid)
    ("a", "Vortragsnummern", "Vortragsnummern (reports)", 1),
    ("b", "Neu eingegangene Sachen", "New cases received", 2),
    ("c", "Voruntersuchungen veranlasst", "Preliminary investigations ordered", 5),
    ("d", "Anklageschriften", "Indictments", 7),
    ("e", "Hauptverhandlungen 1. Instanz", "Trials, first instance", 11),
]
offices = []
by = {}
for off, rng in (("Gera", range(1, 5)), ("Schleiz", range(5, 9))):
    for i, ri in enumerate(rng):
        year = 1864 + i
        r = g2[ri]
        vals = {m[0]: N(r[m[3]]) for m in MEAS}
        by[(off, year)] = vals
        offices.append([off, year] + [vals[m[0]] for m in MEAS])
assert g2[1][0].startswith("Gera") and g2[5][0].startswith("Schleiz") and g2[8][0] == "1867"
print(offices)

index_rows = []
for k, de, en, _ in MEAS:
    base = by[("Gera", 1864)][k] + by[("Schleiz", 1864)][k]
    for y in (1864, 1865, 1866, 1867):
        v = by[("Gera", y)][k] + by[("Schleiz", y)][k]
        index_rows.append([k, de, en, y, v, round(100 * v / base, 1)])

# --- handling of the investigations 1867 (b4) --------------------------------------------
# cols: 1 Rest Vorjahr 2 eingestellt 3 Zurücknahme 4 Endurteil 5 schwebend | 6 neue 7 eingestellt 8 Zurücknahme 9 Endurteil 10 schwebend
OUT = [("a", "Eingestellt", "Discontinued", 7), ("b", "Antrag zurückgenommen", "Complaint withdrawn", 8),
       ("c", "Endurteil oder Zurückweisung", "Final judgment or dismissal", 9), ("d", "Am Jahresschluss schwebend", "Pending at year end", 10)]
handling = []
for ri, off in ((1, "Gera"), (2, "Schleiz")):
    r = g4[ri]
    assert r[0] == off
    new = N(r[6])
    assert sum(N(r[c]) for c in (7, 8, 9, 10)) == new, (off, new)
    for k, de, en, c in OUT:
        handling.append([off, k, de, en, N(r[c]), round(100 * N(r[c]) / new, 1)])
print(handling)

# --- convicted by age class and occupation (b6): rows idx 4 = Summe 1866, idx 8 = Summe 1867 ----
AGE = [("a", "unter 18", "under 18", 2), ("b", "18–24", "18–24", 3), ("c", "24–40", "24–40", 4), ("d", "40–60", "40–60", 5), ("e", "60 und älter", "60 and over", 6)]
OCC = [("a", "Arbeitsleute", "Labourers", 9), ("b", "Dienstboten", "Servants", 10), ("c", "Gesellen und Gehilfen", "Journeymen and assistants", 11),
       ("d", "Selbständige Handwerker", "Independent craftsmen", 12), ("e", "Handelsleute", "Traders", 13),
       ("f", "Gutsbesitzer, Rentiers, Kaufleute", "Estate owners, rentiers, merchants", 14), ("g", "Amt und Wissenschaft", "Officials and scholars", 15),
       ("h", "Landwirte", "Farmers", 16), ("i", "Sonstige", "Others", 17)]
sums = {1866: g6[4], 1867: g6[8]}
assert sums[1866][0] == "Summe" and sums[1867][0] == "Summe" and g6[1][0] == "1866" and g6[5][0] == "1867"
age = []
occ = []
for y, r in sums.items():
    assert sum(N(r[c]) for _, _, _, c in AGE) == N(r[1])
    for k, de, en, c in AGE:
        age.append([y, k, de, en, N(r[c])])
    for k, de, en, c in OCC:
        occ.append([y, k, de, en, N(r[c])])
tot66, tot67 = N(sums[1866][1]), N(sums[1867][1])
print(tot66, tot67)

# --- numbers for the text
ix = {(k, y): v for k, _, _, y, _, v in index_rows}
val = {(k, y): v for k, _, _, y, v, _ in index_rows}
pct = lambda a, b: 100 * a / b
A = {(y, k): v for y, k, _, _, v in age}
O = {(y, k): v for y, k, _, _, v in occ}
under24 = {y: A[(y, "a")] + A[(y, "b")] for y in (1866, 1867)}
over40 = {y: A[(y, "d")] + A[(y, "e")] for y in (1866, 1867)}
H = {(o, k): (n, p) for o, k, _, _, n, p in handling}
print(ix, under24, over40, H)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "justiz-strafsachen-kreisgerichte-staatsanwaltschaft-1864-1867",
    "title": bi("Strafsachen vor den Kreisgerichten: Staatsanwaltschaften 1864–1867 und Verurteilte nach Alter und Beruf", "Criminal cases before the Kreisgerichte: public prosecutors 1864–1867 and convicts by age and occupation"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "288", "block": "b2", "rows": "r2-r9"}, {"page": "288", "block": "b4", "rows": "r2-t4"}, {"page": "288", "block": "b6", "rows": "r2-t9"}, {"page": "289", "block": "b2"}],
    "summary": bi(
        f"Die Staatsanwaltschaften bei den Kreisgerichten Gera und Schleiz bearbeiteten 1867 zusammen {D(val[('a', 1867)])} Vortragsnummern und {D(val[('c', 1867)])} Voruntersuchungen; die Zahl der Voruntersuchungen hat sich seit 1864 mehr als verdoppelt. Brückner gibt außerdem für 1866 und 1867 die Zahl der vor den Kreisgerichten und dem Schwurgericht Verurteilten nach Altersklasse, Konfession und Beruf an. Die Auswertung zeigt die Entwicklung und die Unterschiede der beiden Staatsanwaltschaften.",
        f"The public prosecutors at the Kreisgerichte of Gera and Schleiz dealt with {E(val[('a', 1867)])} briefing numbers and {E(val[('c', 1867)])} preliminary investigations in 1867 together; the number of preliminary investigations has more than doubled since 1864. Brückner also gives, for 1866 and 1867, the number of persons convicted before the Kreisgerichte and the jury court by age class, denomination and occupation. The analysis shows the development and the differences between the two prosecutors' offices.",
    ),
    "method": bi(
        "Die Zeitreihen stammen aus der Tabelle »Der formelle Umfang der Geschäfte der Staatsanwälte« (S. 288, b2), die Erledigung der Untersuchungen 1867 aus S. 288 b4, die Verurteilten aus S. 288 b6 (Summenzeilen 1866 und 1867). Für die Entwicklung wurden die Werte beider Staatsanwaltschaften addiert und auf 1864 = 100 indexiert (abgeleitet); »Vortragsnummern« sind die laufenden Nummern der Vorträge beim Staatsanwalt (Brückner erklärt den Begriff nicht). Der Anteil an den neuen Untersuchungen 1867 ergibt sich aus der Spalte »Neue, im Laufe des Jahres bewirkte Untersuchung«.",
        "The time series come from the table “The formal scope of the business of the public prosecutors” (p. 288, b2), the disposal of the investigations in 1867 from p. 288 b4, the convicted from p. 288 b6 (total rows 1866 and 1867). For the trend the values of both prosecutors' offices were added and indexed to 1864 = 100 (derived); “Vortragsnummern” are the running numbers of reports to the prosecutor (Brückner does not explain the term). The shares of the new investigations in 1867 come from the column “new investigations effected in the course of the year”.",
    ),
    "findings": [
        bi(f"Von 1864 bis 1867 stieg die Zahl der Voruntersuchungen beider Staatsanwaltschaften von {D(val[('c', 1864)])} auf {D(val[('c', 1867)])} (+{D(ix[('c', 1867)]-100,0)} %); die Anklageschriften nahmen nur von {D(val[('d', 1864)])} auf {D(val[('d', 1867)])} zu (+{D(ix[('d', 1867)]-100,0)} %), die neu eingegangenen Sachen von {D(val[('b', 1864)])} auf {D(val[('b', 1867)])} (+{D(ix[('b', 1867)]-100,0)} %).",
           f"From 1864 to 1867 the preliminary investigations of both prosecutors' offices rose from {E(val[('c', 1864)])} to {E(val[('c', 1867)])} (+{E(ix[('c', 1867)]-100,0)} %); indictments increased only from {E(val[('d', 1864)])} to {E(val[('d', 1867)])} (+{E(ix[('d', 1867)]-100,0)} %), newly received cases from {E(val[('b', 1864)])} to {E(val[('b', 1867)])} (+{E(ix[('b', 1867)]-100,0)} %)."),
        bi(f"Der größte Sprung liegt zwischen 1865 und 1866 (Voruntersuchungen {D(val[('c', 1865)])} auf {D(val[('c', 1866)])}); Brückner führt die Mehrarbeit 1867 auf die Not der Arbeiterbevölkerung im reichenfelser Gebiet zurück (S. 289).",
           f"The largest jump falls between 1865 and 1866 (preliminary investigations {E(val[('c', 1865)])} to {E(val[('c', 1866)])}); Brückner attributes the extra work in 1867 to the distress of the working population in the Reichenfels area (p. 289)."),
        bi(f"Der Umgang mit den neuen Untersuchungen 1867 unterscheidet sich: Gera stellte {D(H[('Gera','a')][1],1)} % ein, Schleiz {D(H[('Schleiz','a')][1],1)} %; am Jahresende schwebten in Schleiz {D(H[('Schleiz','d')][1],1)} % der neuen Untersuchungen, in Gera {D(H[('Gera','d')][1],1)} %.",
           f"The handling of the new investigations in 1867 differs: Gera discontinued {E(H[('Gera','a')][1],1)} %, Schleiz {E(H[('Schleiz','a')][1],1)} %; at year end {E(H[('Schleiz','d')][1],1)} % of the new investigations were pending in Schleiz, {E(H[('Gera','d')][1],1)} % in Gera."),
        bi(f"Die Zahl der Verurteilten stieg von 139 (1865) über {D(tot66)} (1866) auf {D(tot67)} (1867). Der Anteil der unter 24-Jährigen sank von {D(pct(under24[1866], tot66),1)} % auf {D(pct(under24[1867], tot67),1)} %, der der über 40-Jährigen stieg von {D(pct(over40[1866], tot66),1)} % auf {D(pct(over40[1867], tot67),1)} %; selbständige Handwerker unter den Verurteilten nahmen von {D(O[(1866,'d')])} auf {D(O[(1867,'d')])} zu.",
           f"The number of convicts rose from 139 (1865) through {E(tot66)} (1866) to {E(tot67)} (1867). The share of those under 24 fell from {E(pct(under24[1866], tot66),1)} % to {E(pct(under24[1867], tot67),1)} %, that of those over 40 rose from {E(pct(over40[1866], tot66),1)} % to {E(pct(over40[1867], tot67),1)} %; independent craftsmen among the convicts rose from {E(O[(1866,'d')])} to {E(O[(1867,'d')])}."),
    ],
    "caveats": [
        bi("In der Tabelle der Verurteilten steht für 1866 in der Spalte »Protestanten« die Summe 176, obwohl nur 167 Personen verurteilt wurden (76 + 91 = 167); die Fußnote spricht von »blos Protestanten«. Es handelt sich um einen Druckfehler des Originals (Faksimile geprüft); die Konfession wird hier nicht ausgewertet. Für 1867 nennen die Berufsklassen 150 Männer, die Spalte »männlichen Geschlechts« 148.",
           "In the table of convicts the “Protestants” column gives 176 for 1866 although only 167 persons were convicted (76 + 91 = 167); the footnote speaks of “only Protestants”. This is a misprint in the original (facsimile checked); denomination is not analysed here. For 1867 the occupation classes name 150 men, the column “male sex” 148."),
        bi("Die Zahlen der Voruntersuchungen und Einstellungen eines Jahres umfassen auch Fälle aus Vorjahren und lassen sich daher nicht als Aufteilung der neu eingegangenen Sachen lesen. Die Altersklassen- und Berufstabelle gilt für Kreisgerichte und Schwurgericht zusammen und enthält nur zwei Jahre.",
           "The numbers of preliminary investigations and discontinuations of a year also include cases from earlier years and therefore cannot be read as a breakdown of the newly received cases. The age and occupation table covers the Kreisgerichte and the jury court together and has only two years."),
    ],
    "datasets": [
        {"name": "offices", "title": bi("Geschäftsumfang der Staatsanwaltschaften je Amt und Jahr", "Business of the public prosecutors by office and year"),
         "columns": [col("office", "Staatsanwaltschaft", "Prosecutor's office", "string"), col("year", "Jahr", "Year", "integer")] + [col(f"m_{m[0]}", m[1], m[2], "integer", "Anzahl") for m in MEAS],
         "rows": offices, "source_refs": [{"page": "288", "block": "b2", "rows": "r2-r9"}]},
        {"name": "index", "title": bi("Entwicklung beider Staatsanwaltschaften, 1864 = 100", "Development of both prosecutors' offices, 1864 = 100"),
         "columns": [col("measure_key", "Kürzel", "Key", "string"), col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
                     col("year", "Jahr", "Year", "integer"), col("value", "Summe Gera + Schleiz", "Sum Gera + Schleiz", "integer", "Anzahl", derived=True),
                     col("index", "Index (1864 = 100)", "Index (1864 = 100)", "number", None, derived=True)],
         "rows": index_rows, "source_refs": [{"page": "288", "block": "b2", "rows": "r2-r9"}]},
        {"name": "handling", "title": bi("Erledigung der neuen Untersuchungen 1867", "Disposal of the new investigations in 1867"),
         "columns": [col("office", "Staatsanwaltschaft", "Prosecutor's office", "string"), col("outcome_key", "Kürzel", "Key", "string"),
                     col("outcome_de", "Erledigung", "Disposal", "string"), col("outcome_en", "Erledigung (englisch)", "Disposal (English)", "string"),
                     col("cases", "Untersuchungen", "Investigations", "integer", "Anzahl"),
                     col("share", "Anteil an den neuen Untersuchungen", "Share of the new investigations", "number", "%", derived=True)],
         "rows": handling, "source_refs": [{"page": "288", "block": "b4", "rows": "r2-r4"}]},
        {"name": "age", "title": bi("Verurteilte nach Altersklasse", "Convicts by age class"),
         "columns": [col("year", "Jahr", "Year", "integer"), col("age_key", "Kürzel", "Key", "string"), col("age_de", "Altersklasse", "Age class", "string"), col("age_en", "Altersklasse (englisch)", "Age class (English)", "string"),
                     col("persons", "Verurteilte", "Convicts", "integer", "Personen")],
         "rows": age, "source_refs": [{"page": "288", "block": "b6", "rows": "t5"}, {"page": "288", "block": "b6", "rows": "t9"}]},
        {"name": "occupation", "title": bi("Verurteilte nach Berufsklasse", "Convicts by occupation class"),
         "columns": [col("year", "Jahr", "Year", "integer"), col("occ_key", "Kürzel", "Key", "string"), col("occ_de", "Berufsklasse", "Occupation class", "string"), col("occ_en", "Berufsklasse (englisch)", "Occupation class (English)", "string"),
                     col("persons", "Verurteilte", "Convicts", "integer", "Personen")],
         "rows": occ, "source_refs": [{"page": "288", "block": "b6", "rows": "t5"}, {"page": "288", "block": "b6", "rows": "t9"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "index",
         "title": bi("Geschäfte der Staatsanwaltschaften, 1864 = 100", "Business of the public prosecutors, 1864 = 100"),
         "caption": bi("Gera und Schleiz zusammen. Die Voruntersuchungen wachsen weit stärker als Anklageschriften und Hauptverhandlungen.", "Gera and Schleiz together. Preliminary investigations grow far more than indictments and trials."),
         "vegalite": {
             "height": 300,
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                      "y": {"field": "index", "type": "quantitative", "title": bi("Index (1864 = 100)", "Index (1864 = 100)"), "scale": {"zero": False}},
                      "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                      "tooltip": [ttf("measure", "Messgröße", "Measure"), tt("year", "Jahr", "Year"), {"field": "value", "title": bi("Summe", "Sum"), "format": ","}, {"field": "index", "title": "Index", "format": ".1f"}]}},
                 {"mark": {"type": "rule", "strokeDash": [3, 3]}, "encoding": {"y": {"datum": 100}}},
             ]}},
        {"id": "c2", "dataset": "handling",
         "title": bi("Erledigung der neuen Untersuchungen 1867", "Disposal of the new investigations in 1867"),
         "caption": bi("Anteil an den im Jahr neu bewirkten Untersuchungen (Gera 319, Schleiz 333), Prozent.", "Share of the investigations newly effected in the year (Gera 319, Schleiz 333), per cent."),
         "vegalite": {
             "height": 170,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "office", "type": "nominal", "title": None},
                 "x": {"field": "share", "type": "quantitative", "title": bi("Anteil (%)", "Share (%)"), "stack": "zero", "scale": {"domain": [0, 100]}},
                 "color": {"field": F("outcome"), "type": "nominal", "title": None, "sort": {"field": "outcome_key", "op": "min"}, "legend": {"labelLimit": 400}},
                 "order": {"field": "outcome_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("office", "Staatsanwaltschaft", "Prosecutor's office"), ttf("outcome", "Erledigung", "Disposal"), tt("cases", "Untersuchungen", "Investigations"), {"field": "share", "title": bi("Anteil (%)", "Share (%)"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "age",
         "title": bi("Verurteilte nach Altersklasse, 1866 und 1867", "Convicts by age class, 1866 and 1867"),
         "caption": bi("Vor Kreisgerichten und Schwurgericht verurteilte Personen (Gera und Schleiz zusammen).", "Persons convicted before the Kreisgerichte and the jury court (Gera and Schleiz together)."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("age"), "type": "nominal", "title": bi("Alter (Jahre)", "Age (years)"), "sort": {"field": "age_key", "op": "min"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "year", "type": "ordinal"},
                 "y": {"field": "persons", "type": "quantitative", "title": bi("Verurteilte", "Convicts")},
                 "color": {"field": "year", "type": "nominal", "title": bi("Jahr", "Year")},
                 "tooltip": [ttf("age", "Altersklasse", "Age class"), tt("year", "Jahr", "Year"), tt("persons", "Verurteilte", "Convicts")]}}},
        {"id": "c4", "dataset": "occupation",
         "title": bi("Verurteilte nach Berufsklasse, 1866 und 1867", "Convicts by occupation class, 1866 and 1867"),
         "caption": bi("Männliche Verurteilte nach den neun Berufsklassen der Tabelle.", "Male convicts by the nine occupation classes of the table."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("occ"), "type": "nominal", "title": None, "sort": {"field": "occ_key", "op": "min"}, "axis": {"labelLimit": 300}},
                 "yOffset": {"field": "year", "type": "ordinal"},
                 "x": {"field": "persons", "type": "quantitative", "title": bi("Verurteilte", "Convicts")},
                 "color": {"field": "year", "type": "nominal", "title": bi("Jahr", "Year")},
                 "tooltip": [ttf("occ", "Berufsklasse", "Occupation class"), tt("year", "Jahr", "Year"), tt("persons", "Verurteilte", "Convicts")]}}},
    ],
    "keywords": {"de": ["Staatsanwaltschaft", "Kreisgericht", "Voruntersuchung", "Anklageschrift", "Verurteilte", "Altersklassen", "Berufsklassen", "Kriminalität", "Schwurgericht"],
                 "en": ["public prosecutor", "Kreisgericht", "preliminary investigation", "indictment", "convicts", "age classes", "occupations", "crime", "jury court"]},
}
write(ana)
