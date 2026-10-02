"""A08: Selbstmord und Ungluecksfaelle 1858-1867 (p. 117)."""
from common import *

YEARS = list(range(1858, 1868))
g = grid("117", "b2")
D4 = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Reuß j. L."]
cases, mean = [], []
for r in g[3:13]:
    y = int(r[0])
    for i, k in enumerate(D4):
        cases.append([y, k, inum(r[1 + i]), num(r[5 + i]), num(r[9 + i])])
avg = g[13]
assert avg[0].startswith("Durchschn")
for i, k in enumerate(D4):
    mean.append([k, num(avg[1 + i]), num(avg[5 + i]), num(avg[9 + i])])

# ---- numbers
C = {(r[0], r[1]): r for r in cases}
fue_n = {y: C[(y, "Reuß j. L.")][2] for y in YEARS}
fue_p = {y: C[(y, "Reuß j. L.")][4] for y in YEARS}
tot = sum(fue_n.values())
assert abs(tot / 10 - mean[3][1]) < 0.05
M = {r[0]: r for r in mean}
lo = min(fue_n, key=fue_n.get)
hi = max(fue_n, key=fue_n.get)
dist_hi = max(D4[:3], key=lambda k: M[k][3])
dist_lo = min(D4[:3], key=lambda k: M[k][3])
assert dist_hi == "Lobenstein-Ebersdorf" and dist_lo == "Schleiz"
lob = {y: C[(y, "Lobenstein-Ebersdorf")][2] for y in YEARS}
lob_other = [v for y, v in lob.items() if y != 1865]
print(tot, fue_n, fue_p, M, lob, lo, hi)
assert lob[1865] == min(lob.values()) and lo == 1865
gera_hi = [y for y in YEARS if C[(y, "Gera")][2] == max(C[(k, "Gera")][2] for k in YEARS)]
print(gera_hi)

SRC = ref("117", "b2", "r4-r13")
ana = {
    "id": "gesundheit-selbstmord-unglueck-1858-1867",
    "title": bi("Todesfälle durch Selbstmord oder Unglück 1858–1867", "Deaths by suicide or accident, 1858–1867"),
    "category": "health",
    "section": "t1-2-1",
    "sources": [ref("117", "b1"), SRC, ref("117", "b2", "t14")],
    "summary": bi(
        f"Von den Todesursachen wurden seit 1858 nur die Selbstmorde und Verunglückten, und zwar summarisch, aufgezeichnet. Brückner gibt ihre Zahl für 1858–1867 je Landestheil an, dazu den Anteil an allen Gestorbenen und die Zahl auf 1000 Einwohner. Im Fürstenthum waren es zwischen {fue_n[lo]} ({lo}) und {fue_n[hi]} ({hi}) Fälle im Jahr, im Mittel {fde(M['Reuß j. L.'][1], 1)} oder {fde(M['Reuß j. L.'][3])} auf 1000 Einwohner; Lobenstein-Ebersdorf hatte die höchste, Schleiz die niedrigste Ziffer.",
        f"Of the causes of death, only suicides and accidents were recorded from 1858, and only as a combined total. Brückner gives their number for 1858–1867 per district, together with the share of all deaths and the number per 1,000 inhabitants. In the principality there were between {fue_n[lo]} ({lo}) and {fue_n[hi]} ({hi}) cases a year, {fen(M['Reuß j. L.'][1], 1)} on average or {fen(M['Reuß j. L.'][3])} per 1,000 inhabitants; Lobenstein-Ebersdorf had the highest rate, Schleiz the lowest."),
    "method": bi(
        "Die Tabelle S. 117 nennt je Jahr und Landestheil die Todesfälle durch Selbstmord oder Unglück absolut, in Procenten der Gestorbenen und auf 1000 Einwohner, mit gedruckter Mittelzeile. Alle Werte stehen wie gedruckt im Datensatz (keine Umrechnung). Selbstmorde und Unglücksfälle sind in der Quelle nicht getrennt.",
        "The table on p. 117 gives for each year and district the deaths by suicide or accident in absolute numbers, as a percentage of all deaths and per 1,000 inhabitants, with a printed mean row. All values are in the dataset as printed (no conversion). Suicides and accidents are not separated in the source."),
    "findings": [
        bi(f"Im Fürstenthum starben 1858–1867 insgesamt {tot} Menschen durch Selbstmord oder Unglück, im Mittel {fde(M['Reuß j. L.'][1], 1)} im Jahr; das Minimum ist {fue_n[lo]} ({lo}, {fde(fue_p[lo])} auf 1000 Einwohner), das Maximum {fue_n[hi]} ({hi}, {fde(fue_p[hi])} auf 1000).",
           f"In 1858–1867 a total of {tot} people in the principality died by suicide or accident, {fen(M['Reuß j. L.'][1], 1)} a year on average; the minimum is {fue_n[lo]} ({lo}, {fen(fue_p[lo])} per 1,000 inhabitants), the maximum {fue_n[hi]} ({hi}, {fen(fue_p[hi])} per 1,000)."),
        bi(f"Auf 1000 Einwohner kommen im Mittel {fde(M['Lobenstein-Ebersdorf'][3])} Fälle in Lobenstein-Ebersdorf, {fde(M['Gera'][3])} in Gera und {fde(M['Schleiz'][3])} in Schleiz (Fürstenthum {fde(M['Reuß j. L.'][3])}); wie Brückner schreibt, hat Schleiz die kleinste, Lobenstein-Ebersdorf die größte Ziffer.",
           f"The mean per 1,000 inhabitants is {fen(M['Lobenstein-Ebersdorf'][3])} in Lobenstein-Ebersdorf, {fen(M['Gera'][3])} in Gera and {fen(M['Schleiz'][3])} in Schleiz (principality {fen(M['Reuß j. L.'][3])}); as Brückner writes, Schleiz has the smallest, Lobenstein-Ebersdorf the largest rate."),
        bi(f"Die Fälle machen im Mittel {fde(M['Reuß j. L.'][2])} Procent aller Gestorbenen aus (Gera {fde(M['Gera'][2])}, Schleiz {fde(M['Schleiz'][2])}, Lobenstein-Ebersdorf {fde(M['Lobenstein-Ebersdorf'][2])}).",
           f"The cases make up {fen(M['Reuß j. L.'][2])} per cent of all deaths on average (Gera {fen(M['Gera'][2])}, Schleiz {fen(M['Schleiz'][2])}, Lobenstein-Ebersdorf {fen(M['Lobenstein-Ebersdorf'][2])})."),
        bi(f"Auffällig ist Lobenstein-Ebersdorf 1865 mit nur {lob[1865]} Fällen ({fde(C[(1865, 'Lobenstein-Ebersdorf')][4])} auf 1000 Einwohner) gegenüber {min(lob_other)} bis {max(lob_other)} in den übrigen Jahren; das Jahr drückt auch das Ergebnis des Fürstenthums auf den Tiefstwert {fue_n[1865]}. Ob es sich um eine tatsächliche Schwankung oder um lückenhafte Erfassung handelt, lässt sich aus der Tabelle nicht entscheiden.",
           f"Lobenstein-Ebersdorf 1865 stands out with only {lob[1865]} cases ({fen(C[(1865, 'Lobenstein-Ebersdorf')][4])} per 1,000 inhabitants) against {min(lob_other)} to {max(lob_other)} in the other years; the year also pulls the result for the principality down to its minimum of {fue_n[1865]}. Whether this is a genuine fluctuation or incomplete recording cannot be decided from the table."),
    ],
    "caveats": [
        bi("Selbstmorde und Unglücksfälle sind nicht getrennt; die Zahlen sind klein (Schleiz 7 bis 18 Fälle im Jahr), die Jahresschwankungen daher zufallsanfällig.",
           "Suicides and accidents are not separated; the numbers are small (Schleiz 7 to 18 cases a year), so the annual fluctuations are subject to chance."),
        bi("Die Zahlen wurden laut Brückner nur summarisch verzeichnet; Definition und Vollständigkeit der Meldungen sind unbekannt. Die Bezugsbevölkerung der Zahlen auf 1000 Einwohner nennt Brückner nicht.",
           "According to Brückner the figures were recorded only as totals; definition and completeness of the reports are unknown. Brückner does not state the reference population for the rates per 1,000 inhabitants."),
    ],
    "datasets": [
        {"name": "accidents", "title": bi("Todesfälle durch Selbstmord oder Unglück", "Deaths by suicide or accident"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landestheil", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("cases", "Todesfälle durch Selbstmord oder Unglück", "Deaths by suicide or accident", "integer", "Fälle"),
                     col("pct_deaths", "in Procenten der Gestorbenen", "As a percentage of all deaths", "number", "%"),
                     col("per_1000", "auf 1000 Einwohner", "Per 1,000 inhabitants", "number", "‰")],
         "rows": cases, "source_refs": [SRC]},
        {"name": "accidents_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("cases", "Fälle (Jahresmittel)", "Cases (annual mean)", "number", "Fälle"),
                     col("pct_deaths", "in Procenten der Gestorbenen", "As a percentage of all deaths", "number", "%"),
                     col("per_1000", "auf 1000 Einwohner", "Per 1,000 inhabitants", "number", "‰")],
         "rows": mean, "source_refs": [ref("117", "b2", "t14")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "accidents",
         "title": bi("Todesfälle durch Selbstmord oder Unglück auf 1000 Einwohner", "Deaths by suicide or accident per 1,000 inhabitants"),
         "caption": bi("Je Landestheil und für das Fürstenthum (Reuß j. L.), 1858–1867.",
                       "By district and for the principality (Reuß j. L.), 1858–1867."),
         "vegalite": {"height": 300, "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "per_1000", "type": "quantitative", "title": bi("auf 1000 Einwohner", "per 1,000 inhabitants"), "scale": {"domain": [0, 1]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("year", "Jahr", "Year"), tip("cases", "Todesfälle", "Deaths"),
                                      tip("per_1000", "auf 1000 Einwohner", "per 1,000 inhabitants", ".2f")]}}},
        {"id": "c2", "dataset": "accidents",
         "title": bi("Zahl der Todesfälle im Fürstenthum", "Number of deaths in the principality"),
         "caption": bi("Je Landestheil übereinander gestapelt; die Gesamthöhe ist die Zahl im Fürstenthum.",
                       "Stacked by district; the total height is the number for the principality."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.district != 'Reuß j. L.'"}, ordk("district", DISTRICTS[:3])], "mark": "bar",
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "cases", "type": "quantitative", "title": bi("Todesfälle", "deaths"), "stack": "zero"},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS[:3]}, "legend": {"labelLimit": 260}},
                          "order": {"field": "ordk", "type": "quantitative", "sort": "ascending"},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("year", "Jahr", "Year"), tip("cases", "Todesfälle", "Deaths")]}}},
        {"id": "c3", "dataset": "accidents_mean",
         "title": bi("Anteil an allen Gestorbenen", "Share of all deaths"),
         "caption": bi("Gedrucktes Mittel 1858–1867, Todesfälle durch Selbstmord oder Unglück in Procent aller Gestorbenen.",
                       "Printed mean 1858–1867, deaths by suicide or accident as a percentage of all deaths."),
         "vegalite": {"height": 260, "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "y": {"field": "pct_deaths", "type": "quantitative", "title": bi("% der Gestorbenen", "% of deaths")},
                          "color": {"field": "district", "type": "nominal", "scale": {"domain": DISTRICTS}, "legend": None},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("cases", "Fälle (Jahresmittel)", "Cases (annual mean)", ".1f"),
                                      tip("pct_deaths", "% der Gestorbenen", "% of deaths", ".2f"), tip("per_1000", "auf 1000 Einwohner", "per 1,000 inhabitants", ".2f")]}}},
    ],
    "keywords": {"de": ["Selbstmord", "Suizid", "Unglücksfälle", "Verunglückte", "Todesursachen", "Sterblichkeit", "Gesundheit"],
                 "en": ["suicide", "accidents", "causes of death", "mortality", "health"]},
    "related": ["bevoelkerung-sterblichkeit-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
