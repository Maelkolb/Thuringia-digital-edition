"""A11-04: Zivilrechtspflege vor den Einzelgerichten (Justizämtern) 1864-1867 (pp. 283-284)."""
from common import *

g3 = grid("283", "b4")      # generalia
g4 = grid("284", "b2")      # civilia
COURTS = ["Gera I", "Gera II", "Hirschberg", "Hohenleuben", "Lobenstein I", "Lobenstein II", "Schleiz I", "Schleiz II"]
# --- generalia (p. 283): rows 2..9 courts, 10 = Summe 1867, 11..13 = 1866..1864
c3 = {r[0].rstrip("."): r for r in g3[2:10]}
y3 = {1867: g3[10], 1866: g3[11], 1865: g3[12], 1864: g3[13]}
assert g3[10][0] == "Summe 1867" and g3[13][0] == "1864"
# --- civilia (p. 284): rows 4..11 courts, 12 = Summe 1867, 13..15 = 1866..1864
c4 = {r[0].rstrip("."): r for r in g4[4:12]}
y4 = {1867: g4[12], 1866: g4[13], 1865: g4[14], 1864: g4[15]}
assert g4[12][0] == "Summe 1867" and g4[15][0] == "1864"
assert [k for k in c3] == COURTS and [k for k in c4] == COURTS, (list(c3), list(c4))

N = lambda x: num(x) or 0
yearly = []
for y in (1864, 1865, 1866, 1867):
    a, b = y3[y], y4[y]
    yearly.append([y, N(a[1]), N(a[2]), N(b[1]), N(b[2]), N(b[3]), N(b[4]), N(b[5]), N(b[6]), N(b[7]), N(b[8]), N(b[9]), N(b[10])])
print(yearly)
Y = {r[0]: r for r in yearly}
# column positions in `yearly`
cols_y = ["year", "registranden", "termine", "rs_alt", "rs_neu", "erk_alt", "erk_neu", "verg_alt", "verg_neu", "unerl_alt", "unerl_neu", "konk_alt", "konk_neu"]
ix = {c: i for i, c in enumerate(cols_y)}

# --- index 1864 = 100
MEAS = [
    ("a_reg", "Registrandennummern", "Register numbers"),
    ("b_ter", "Termine", "Hearings"),
    ("c_rs", "Neue Prozesse", "New formal lawsuits"),
    ("d_erk", "Erkenntnisse", "Judgments"),
    ("e_verg", "Vergleiche", "Settlements"),
]
index_rows = []
for k, de, en in MEAS:
    kk = {"a_reg": "registranden", "b_ter": "termine", "c_rs": "rs_neu", "d_erk": "erk_neu", "e_verg": "verg_neu"}[k]
    base = Y[1864][ix[kk]]
    for y in (1864, 1865, 1866, 1867):
        v = Y[y][ix[kk]]
        index_rows.append([k, de, en, y, v, round(100 * v / base, 1)])

# --- courts 1867
courts = []
outcomes = []
for c in COURTS:
    a, b = c3[c], c4[c]
    reg, ter = int(num(a[1])), int(num(a[2]))
    rs, erk, ver, une = int(num(b[2])), int(num(b[4])), int(num(b[6])), int(num(b[8]))
    assert rs == erk + ver + une, (c, rs, erk, ver, une)
    share = round(100 * ver / (erk + ver), 1)
    courts.append([c, reg, ter, rs, erk, ver, une, share])
    outcomes += [[c, "a", "Durch Erkenntnis", "By judgment", erk], [c, "b", "Durch Vergleich", "By settlement", ver], [c, "c", "Unerledigt", "Unresolved", une]]
tot_reg = sum(r[1] for r in courts)
assert tot_reg == 94308
print(courts)

# --- numbers for the text
def pct(a, b):
    return 100 * a / b


chg = lambda k: pct(Y[1867][ix[k]] - Y[1864][ix[k]], Y[1864][ix[k]])
sh = lambda y: pct(Y[y][ix["verg_neu"]], Y[y][ix["verg_neu"]] + Y[y][ix["erk_neu"]])
unr = lambda y: pct(Y[y][ix["unerl_neu"]], Y[y][ix["rs_neu"]])
gera_reg = courts[0][1] + courts[1][1]
top_share = max(courts, key=lambda r: r[7])
low_share = min(courts, key=lambda r: r[7])
print(chg("registranden"), chg("termine"), chg("rs_neu"), sh(1864), sh(1867), unr(1864), unr(1867), top_share, low_share)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


R = Y
ana = {
    "id": "justiz-zivilrechtspflege-einzelgerichte-1864-1867",
    "title": bi("Zivilrechtspflege der Justizämter 1864–1867", "Civil justice in the first-instance courts (Justizämter), 1864–1867"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "283", "block": "b4", "rows": "r3-r14"}, {"page": "284", "block": "b2", "rows": "r5-r16"}],
    "summary": bi(
        f"Die Justizämter (Einzelgerichte) in Gera, Hohenleuben, Schleiz, Lobenstein und Hirschberg meldeten für 1867 insgesamt {D(R[1867][1])} Registrandennummern und {D(R[1867][4])} neue förmliche Rechtsstreitigkeiten; Brückner stellt die Jahre 1864–1867 und die acht Gerichtsabteilungen nebeneinander. Die Auswertung zeigt das Wachstum der Geschäfte, den steigenden Anteil der Vergleiche und die Unterschiede zwischen den Gerichten.",
        f"The Justizämter (single-judge courts) at Gera, Hohenleuben, Schleiz, Lobenstein and Hirschberg reported {E(R[1867][1])} register numbers and {E(R[1867][4])} new formal lawsuits for 1867; Brückner sets the years 1864–1867 and the eight court divisions side by side. The analysis shows the growth of business, the rising share of settlements and the differences between the courts.",
    ),
    "method": bi(
        "Die Zahlen stammen aus den Tabellen »Generalia« (S. 283) und »Civilia« (S. 284) der Statistik der Rechtspflege. Für jedes Jahr wurden Registrandennummern, Termine und die Spalten der förmlichen Rechtsstreitigkeiten (alte = aus Vorjahren übernommene, neue = im Jahr eingegangene; erledigt durch Erkenntnis oder Vergleich; unerledigt) und der Konkurse übernommen. Für die Entwicklung wurde jede Reihe auf 1864 = 100 indexiert (abgeleitet). Der Vergleichsanteil = Vergleiche : (Erkenntnisse + Vergleiche) unter den neuen Fällen. Nicht ausgewertet sind die Appellationsspalten (S. 284) und die Sühnetermine, die laut Überschrift nur 1866 betreffen.",
        "The figures come from the tables “Generalia” (p. 283) and “Civilia” (p. 284) of the justice statistics. For each year register numbers, hearings and the columns for formal lawsuits (old = carried over from earlier years, new = received in the year; decided by judgment or settled; unresolved) and bankruptcies were taken over. For the trend each series was indexed to 1864 = 100 (derived). The settlement share = settlements : (judgments + settlements) among the new cases. Not analysed are the appeal columns (p. 284) and the conciliation hearings, which according to the heading refer to 1866 only.",
    ),
    "findings": [
        bi(f"Von 1864 bis 1867 wuchsen die Registrandennummern um {D(chg('registranden'),1)} % ({D(R[1864][1])} auf {D(R[1867][1])}), die Termine um {D(chg('termine'),1)} % und die neuen förmlichen Rechtsstreitigkeiten um {D(chg('rs_neu'),1)} %; die Registratur wuchs also deutlich schneller als die Zahl der förmlichen Prozesse.",
           f"From 1864 to 1867 register numbers grew by {E(chg('registranden'),1)} % ({E(R[1864][1])} to {E(R[1867][1])}), hearings by {E(chg('termine'),1)} % and new formal lawsuits by {E(chg('rs_neu'),1)} %; the registry thus grew considerably faster than the number of formal lawsuits."),
        bi(f"Der Anteil der Vergleiche an den entschiedenen neuen Fällen stieg von {D(sh(1864),1)} % (1864) auf {D(sh(1867),1)} % (1867); die Zahl der Vergleiche wuchs um {D(chg('verg_neu'),1)} %, die der Erkenntnisse sank um {D(-chg('erk_neu'),1)} %.",
           f"The share of settlements among the decided new cases rose from {E(sh(1864),1)} % (1864) to {E(sh(1867),1)} % (1867); settlements grew by {E(chg('verg_neu'),1)} %, judgments fell by {E(-chg('erk_neu'),1)} %."),
        bi(f"Die beiden geraer Justizämter vereinen {D(pct(gera_reg, tot_reg),1)} % aller Registrandennummern; Gera I allein hat {D(courts[0][1])} Nummern und {D(courts[0][3])} neue Rechtsstreitigkeiten ({D(pct(courts[0][3], R[1867][4]),1)} % aller).",
           f"The two Gera Justizämter account for {E(pct(gera_reg, tot_reg),1)} % of all register numbers; Gera I alone has {E(courts[0][1])} numbers and {E(courts[0][3])} new lawsuits ({E(pct(courts[0][3], R[1867][4]),1)} % of all)."),
        bi(f"Der Vergleichsanteil reicht 1867 von {D(low_share[7],1)} % ({low_share[0]}) bis {D(top_share[7],1)} % ({top_share[0]}). Am Jahresende 1867 waren {D(unr(1867),1)} % der neuen Fälle unerledigt (1864: {D(unr(1864),1)} %).",
           f"In 1867 the settlement share ranges from {E(low_share[7],1)} % ({low_share[0]}) to {E(top_share[7],1)} % ({top_share[0]}). At the end of 1867 {E(unr(1867),1)} % of the new cases were unresolved (1864: {E(unr(1864),1)} %)."),
    ],
    "caveats": [
        bi("Zwei Zeilen sind im Druck nicht in sich stimmig: In der Summe 1867 stehen 392 alte Rechtsstreitigkeiten, die Einzelwerte ergeben 357; die Zeile Schleiz I nennt 15 (die Teilspalten 14 + 34 + 2 ergeben 50, und mit 50 stimmt die Summe 392). Für 1864 ergeben die Teilspalten der neuen Fälle 2.015 statt der gedruckten 2.021. Beides steht so im Original (Faksimile geprüft).",
           "Two rows are not internally consistent in the print: the 1867 total shows 392 old lawsuits while the individual values add up to 357; the Schleiz I row gives 15 (its sub-columns 14 + 34 + 2 make 50, and with 50 the total 392 is correct). For 1864 the sub-columns of new cases add up to 2,015 instead of the printed 2,021. Both are in the original (facsimile checked)."),
        bi("»Registrandennummern« sind laufende Registraturnummern des Geschäftsverkehrs; Brückner erklärt den Begriff nicht. Sie messen den Umfang der Geschäfte, nicht die Zahl der Fälle. Einwohnerzahlen je Gerichtsbezirk fehlen, daher sind keine Pro-Kopf-Raten möglich.",
           "“Registrandennummern” are running register numbers of the court's business; Brückner does not define the term. They measure the volume of business, not the number of cases. Population figures per court district are missing, so no per-capita rates can be given."),
        bi("Dass die Vergleiche zunahmen, fällt in die Zeit nach dem Gesetz vom 28. April 1863 über Friedensgerichte und freie Gerichtstage (S. 282); ein ursächlicher Zusammenhang ist eine Vermutung, Brückner äußert sich dazu nicht.",
           "The rise in settlements falls in the period after the law of 28 April 1863 on conciliation courts and free court days (p. 282); a causal link is conjecture, Brückner does not comment on it."),
        bi("In der Appellationsspalte der Tabelle S. 284 (Hohenleuben, Appellationsgericht) war die Transkription an zwei Zellen vertauscht (siehe transcription_issues); die Spalten werden hier nicht ausgewertet.",
           "In the appeal column of the table on p. 284 (Hohenleuben, Appellate Court) two cells were transposed in the transcription (see transcription_issues); these columns are not analysed here."),
    ],
    "datasets": [
        {"name": "yearly", "title": bi("Justizämter insgesamt, 1864–1867", "All Justizämter, 1864–1867"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("registranden", "Registrandennummern", "Register numbers", "integer", "Nummern"),
             col("termine", "Zahl der Termine", "Number of hearings", "integer", "Termine"),
             col("rs_alt", "Förmliche Rechtsstreitigkeiten, alte", "Formal lawsuits, old", "integer", "Fälle"),
             col("rs_neu", "Förmliche Rechtsstreitigkeiten, neue", "Formal lawsuits, new", "integer", "Fälle"),
             col("erk_alt", "alte, erledigt durch Erkenntnis", "old, decided by judgment", "integer", "Fälle"),
             col("erk_neu", "neue, erledigt durch Erkenntnis", "new, decided by judgment", "integer", "Fälle"),
             col("verg_alt", "alte, erledigt durch Vergleich", "old, settled", "integer", "Fälle"),
             col("verg_neu", "neue, erledigt durch Vergleich", "new, settled", "integer", "Fälle"),
             col("unerl_alt", "alte, unerledigt", "old, unresolved", "integer", "Fälle"),
             col("unerl_neu", "neue, unerledigt", "new, unresolved", "integer", "Fälle"),
             col("konk_alt", "Konkurse, alte", "Bankruptcies, old", "integer", "Verfahren"),
             col("konk_neu", "Konkurse, neue", "Bankruptcies, new", "integer", "Verfahren"),
         ],
         "rows": yearly, "source_refs": [{"page": "283", "block": "b4", "rows": "r11-r14"}, {"page": "284", "block": "b2", "rows": "r13-r16"}]},
        {"name": "index", "title": bi("Entwicklung 1864 = 100", "Development, 1864 = 100"),
         "columns": [
             col("measure_key", "Kürzel", "Key", "string"),
             col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("value", "Wert", "Value", "integer", "Anzahl"),
             col("index", "Index (1864 = 100)", "Index (1864 = 100)", "number", None, derived=True),
         ],
         "rows": index_rows, "source_refs": [{"page": "283", "block": "b4", "rows": "r11-r14"}, {"page": "284", "block": "b2", "rows": "r13-r16"}]},
        {"name": "courts", "title": bi("Die acht Gerichtsabteilungen 1867", "The eight court divisions, 1867"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("registranden", "Registrandennummern", "Register numbers", "integer", "Nummern"),
             col("termine", "Zahl der Termine", "Number of hearings", "integer", "Termine"),
             col("rs_neu", "Neue förmliche Rechtsstreitigkeiten", "New formal lawsuits", "integer", "Fälle"),
             col("erk_neu", "durch Erkenntnis erledigt", "decided by judgment", "integer", "Fälle"),
             col("verg_neu", "durch Vergleich erledigt", "settled", "integer", "Fälle"),
             col("unerl_neu", "unerledigt", "unresolved", "integer", "Fälle"),
             col("verg_share", "Vergleichsanteil", "Settlement share", "number", "%", derived=True, note="Vergleiche : (Erkenntnisse + Vergleiche)"),
         ],
         "rows": courts, "source_refs": [{"page": "283", "block": "b4", "rows": "r3-r10"}, {"page": "284", "block": "b2", "rows": "r5-r12"}]},
        {"name": "outcomes", "title": bi("Ausgang der neuen Rechtsstreitigkeiten 1867 (lang)", "Outcome of the new lawsuits in 1867 (long format)"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("outcome_key", "Kürzel", "Key", "string"),
             col("outcome_de", "Ausgang", "Outcome", "string"), col("outcome_en", "Ausgang (englisch)", "Outcome (English)", "string"),
             col("cases", "Fälle", "Cases", "integer", "Fälle"),
         ],
         "rows": outcomes, "source_refs": [{"page": "284", "block": "b2", "rows": "r5-r12"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "index",
         "title": bi("Geschäftsentwicklung der Justizämter (1864 = 100)", "Business trend of the Justizämter (1864 = 100)"),
         "caption": bi("Summe aller Justizämter. »Erkenntnisse« und »Vergleiche« beziehen sich auf die neuen förmlichen Prozesse des Jahres; die Vergleiche wuchsen stark, die Erkenntnisse gingen zurück.",
                       "Totals for all Justizämter. “Judgments” and “settlements” refer to the new formal lawsuits of the year; settlements grew strongly while judgments declined."),
         "vegalite": {
             "height": 300,
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                      "y": {"field": "index", "type": "quantitative", "title": bi("Index (1864 = 100)", "Index (1864 = 100)"), "scale": {"zero": False}},
                      "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}, "legend": {"columns": 3, "labelLimit": 200}},
                      "tooltip": [ttf("measure", "Messgröße", "Measure"), tt("year", "Jahr", "Year"), {"field": "value", "title": bi("Anzahl", "Count"), "format": ","}, {"field": "index", "title": bi("Index", "Index"), "format": ".1f"}]}},
                 {"mark": {"type": "rule", "strokeDash": [3, 3]}, "encoding": {"y": {"datum": 100}}},
             ]}},
        {"id": "c2", "dataset": "outcomes",
         "title": bi("Neue förmliche Rechtsstreitigkeiten 1867 nach Gericht und Ausgang", "New formal lawsuits in 1867 by court and outcome"),
         "caption": bi("Anzahl der Fälle. Gera I hat mit Abstand die meisten Verfahren; überall überwiegen die Vergleiche.",
                       "Number of cases. Gera I has by far the most proceedings; settlements predominate everywhere."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": {"field": "cases", "op": "sum", "order": "descending"}},
                 "x": {"field": "cases", "type": "quantitative", "title": bi("Fälle", "Cases"), "stack": "zero"},
                 "color": {"field": F("outcome"), "type": "nominal", "title": None, "sort": {"field": "outcome_key", "op": "min"}},
                 "order": {"field": "outcome_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("court", "Gericht", "Court"), ttf("outcome", "Ausgang", "Outcome"), tt("cases", "Fälle", "Cases")]}}},
        {"id": "c3", "dataset": "courts",
         "title": bi("Vergleichsanteil nach Gericht, 1867", "Settlement share by court, 1867"),
         "caption": bi("Vergleiche in Prozent der durch Erkenntnis oder Vergleich entschiedenen neuen Fälle.",
                       "Settlements as a percentage of the new cases decided by judgment or settlement."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": "-x"},
                 "x": {"field": "verg_share", "type": "quantitative", "title": bi("Vergleichsanteil (%)", "Settlement share (%)"), "scale": {"domain": [0, 100]}},
                 "tooltip": [tt("court", "Gericht", "Court"), {"field": "verg_share", "title": bi("Vergleichsanteil (%)", "Settlement share (%)"), "format": ".1f"}, tt("verg_neu", "Vergleiche", "Settlements"), tt("erk_neu", "Erkenntnisse", "Judgments")]}}},
    ],
    "keywords": {"de": ["Rechtspflege", "Justizamt", "Zivilprozess", "Rechtsstreitigkeiten", "Vergleich", "Konkurs", "Gerichtsstatistik", "Gera", "Schleiz", "Lobenstein"],
                 "en": ["justice", "courts", "civil procedure", "lawsuits", "settlement", "bankruptcy", "judicial statistics", "Gera", "Schleiz", "Lobenstein"]},
    "transcription_issues": [
        {"page": "284", "block": "b2", "cell": "r8c19", "transcribed": "1", "facsimile": "3", "checked_facsimile": True, "note": "Hohenleuben, Appellationen beim Appellationsgerichte, »bestätigt«; Summe der Spalte (11) bestätigt den Wert 3. Die Spalte wird in dieser Auswertung nicht verwendet."},
        {"page": "284", "block": "b2", "cell": "r8c21", "transcribed": "3", "facsimile": "1", "checked_facsimile": True, "note": "Hohenleuben, Appellationen beim Appellationsgerichte, »zurückgenommen«; Summe der Spalte (2) bestätigt den Wert 1."},
    ],
}
write(ana)
