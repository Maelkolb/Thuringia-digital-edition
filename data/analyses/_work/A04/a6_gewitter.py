"""A04 / analysis 6: thunderstorms - frequency, annual cycle and direction (pp. 66-68)."""
import sys
sys.path.insert(0, ".")
from common import *

# ---- (a) Gera monthly, two periods (p. 67 b7) ---------------------------------------
g7 = grid("67", "b7")
assert [x.strip() for x in g7[0][1:]] == ["Jan.", "Febr.", "März.", "April.", "Mai.", "Juni.", "Juli.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
PERIODS = [("1853–1858", 1, 6, 1), ("1859–1867", 2, 9, 2)]  # label, order, years, grid row
# Brueckner's corrigenda (p. 830, 'S. 67', 11th column = October): 1853-1858: 1 instead of 2; Summe: 5 instead of 6
CORR = {("1853–1858", 10): (2, 1)}
CORR_SUM_OCT = (6, 5)
monthly = []
cnt = {}
for lab, po, yrs, r in PERIODS:
    assert g7[r][0].replace("-", "–") == lab, g7[r][0]
    for m in range(1, 13):
        cell = g7[r][m]
        v = num(cell)
        used, corr = v, ""
        if (lab, m) in CORR:
            assert int(v) == CORR[(lab, m)][0]
            used = CORR[(lab, m)][1]
            corr = f"S. 830: {used} statt {int(v)}"
        monthly.append([lab, po, m, g7[0][m].strip(" ."), None if used is None else int(used), None if v is None else int(v), corr, yrs, round((used or 0) / yrs, 2)])
        cnt[(lab, m)] = int(used or 0)
sumrow_printed = [int(num(x) or 0) for x in g7[3][1:]]
sumrow = list(sumrow_printed)
assert sumrow[9] == CORR_SUM_OCT[0]
sumrow[9] = CORR_SUM_OCT[1]
assert sumrow == [cnt[("1853–1858", m)] + cnt[("1859–1867", m)] for m in range(1, 13)]   # corrected total row agrees with the corrected rows
tot53, tot59 = sum(cnt[("1853–1858", m)] for m in range(1, 13)), sum(cnt[("1859–1867", m)] for m in range(1, 13))
tot_all = sum(sumrow)
jja = sum(sumrow[5:8])
jfd = sumrow[0] + sumrow[1] + sumrow[11]
print("tot53", tot53, "tot59", tot59, "all", tot_all, "JJA", jja, jja / tot_all, "JFD", jfd, jfd / tot_all)

# ---- (b) annual numbers --------------------------------------------------------------
g66 = grid("66", "b3")
gera_sum = int(num(g66[13][5]))
g67 = grid("67", "b2")
sch_sum = int(num(g67[13][5])); rot_sum = int(num(g67[13][10]))
assert (gera_sum, sch_sum, rot_sum) == (270, 31, 35)
annual = [
    ["Gera", "mean", "1856–1867", gera_sum, 12, round(gera_sum / 12, 1)],
    ["Gera", "maximum", "1861", 45, 1, 45.0],
    ["Gera", "minimum", "1864", 10, 1, 10.0],
    ["Schleiz", "mean", "1866–1867", sch_sum, 2, round(sch_sum / 2, 1)],
    ["Rothenacker", "mean", "Juni 1866–Mai 1868", rot_sum, 2, round(rot_sum / 2, 1)],
]
PY = {(r[0], r[1]): r[5] for r in annual}
print(PY)
per53, per59 = tot53 / 6, tot59 / 9
print("per year 53-58", per53, "59-67", per59)

# ---- (c) directions (p. 68 b2) ---------------------------------------------------------
g8 = grid("68", "b2")
assert [x.strip() for x in g8[0][1:]] == ["N.", "NO.", "O.", "SO.", "S.", "SW.", "W.", "NW."]
dirrows = []
dcount = {}
for st, r, tot in (("Gera", 1, 134), ("Hohenleuben", 3, 47)):
    vals = [int(num(x)) for x in g8[r][1:]]
    assert sum(vals) == tot, (st, sum(vals))
    for i, (d, v) in enumerate(zip(DIRS, vals), start=1):
        dirrows.append([st, 1 if st == "Gera" else 2, d, i, v, round(100 * v / tot, 1)])
        dcount[(st, d)] = v
shr = {(r[0], r[2]): r[5] for r in dirrows}
west_sec = {st: shr[(st, "SW")] + shr[(st, "W")] + shr[(st, "NW")] for st in ("Gera", "Hohenleuben")}
print(shr, west_sec)
# check p.68 b4 aggregates
g84 = grid("68", "b4")
assert int(num(g84[1][1])) == dcount[("Gera", "W")] + dcount[("Gera", "NW")] + dcount[("Gera", "SW")]
assert int(num(g84[1][2])) == dcount[("Hohenleuben", "W")] + dcount[("Hohenleuben", "NW")] + dcount[("Hohenleuben", "SW")]
assert int(num(g84[2][1])) == dcount[("Gera", "O")] + dcount[("Gera", "NO")] + dcount[("Gera", "SO")]


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


KIND_LABEL = bi("datum.station + ' ' + datum.period", "datum.station + ' ' + replace(replace(datum.period, 'Juni', 'June'), 'Mai', 'May')")

ana = {
    "id": "klima-gewitter-gera-stationen",
    "title": bi("Gewitter: Häufigkeit, Jahresgang und Zugrichtung", "Thunderstorms: frequency, annual cycle and direction"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "66", "block": "b3", "rows": "r2-r15"}, {"page": "67", "block": "b2", "rows": "r2-r15"}, {"page": "67", "block": "b4", "rows": "r2-r5"},
                {"page": "67", "block": "b6"}, {"page": "67", "block": "b7", "rows": "r2-r4"}, {"page": "830", "block": "b4", "rows": "i1"}, {"page": "830", "block": "b4", "rows": "i4"},
                {"page": "68", "block": "b1"}, {"page": "68", "block": "b2"}, {"page": "68", "block": "b3"}, {"page": "68", "block": "b4"}],
    "summary": bi(
        "Brückner wertet die Gewitter an mehreren Orten aus: die Zahl pro Jahr (Gera, Schleiz, Rothenacker) im Vergleich zum Durchschnitt von 19 für 50–52½° nördlicher Breite, die Verteilung auf die Monate in Gera (1853–1858 und 1859–1867) und die Zugrichtung für Gera und Hohenleuben. Gewitter häufen sich in Gera im Juni bis August, November bleibt frei; die meisten Gewitter ziehen aus dem Westen heran.",
        "Brückner analyses thunderstorms at several places: the number per year (Gera, Schleiz, Rothenacker) against the average of 19 for 50–52½° north, the distribution over the months at Gera (1853–1858 and 1859–1867), and the direction of approach for Gera and Hohenleuben. At Gera thunderstorms cluster in June to August, November stays free, and most storms approach from the west."),
    "method": bi(
        f"Quellen: Jahressummen aus den Tabellen S. 66 b3 (Gera, 1856–1867) und S. 67 b2 (Schleiz 1866/67, Rothenacker Juni 1866–Mai 1868); Höchst- und Tiefstwert für Gera (1861: 45, 1864: 10) aus dem Text S. 67 b6; Monatsverteilung für Gera aus S. 67 b7 (zwei Zeilen, 1853–1858 und 1859–1867, Gedankenstrich = nicht verzeichnet, im Datensatz leer; der Oktoberwert 1853–1858 ist nach Brückners Berichtigung S. 830 b4 auf 1 statt 2 gesetzt, die Summe auf 5 statt 6; die Spalte »Gewitter laut Tabelle« zeigt den gedruckten Wert, die Spalte »Berichtigung« die betroffene Zeile); Zugrichtung S. 68 b2 (Gera: 134 Gewitter 1853–1858; Hohenleuben: 47 Gewitter, Zeitraum nicht angegeben). Die Jahreszahlen wurden als Summe ÷ Jahre berechnet, die Monatswerte durch die Zahl der Jahre der Periode (6 bzw. 9) geteilt, damit die beiden Perioden vergleichbar sind; die Richtungsanteile sind Prozent der Gewitter des Ortes. Die Windrosen verwenden dieselbe Konstruktion wie in den Windauswertungen (Fläche ∝ Anteil; Ringe bei 10, 20, 30 und 40 %). Die Summenzeile von S. 67 b7 stimmt nach der Berichtigung mit den Zeilen überein. Die Vergleichszahl 19 ist Brückners Angabe »wissenschaftlicher Untersuchungen« (S. 67), ohne Quelle.",
        "Sources: annual totals from the tables p. 66 b3 (Gera, 1856–1867) and p. 67 b2 (Schleiz 1866/67, Rothenacker June 1866–May 1868); highest and lowest value for Gera (1861: 45, 1864: 10) from the text p. 67 b6; monthly distribution for Gera from p. 67 b7 (two rows, 1853–1858 and 1859–1867; a dash means not recorded and is left empty in the dataset; the October value for 1853–1858 is set to 1 instead of 2 and the total to 5 instead of 6 according to Brückner's correction on p. 830 b4; the column “Thunderstorms as in the table” shows the printed value, the column “Correction” the row concerned); direction of approach p. 68 b2 (Gera: 134 thunderstorms 1853–1858; Hohenleuben: 47 thunderstorms, period not stated). Annual figures were computed as total ÷ years, the monthly values were divided by the number of years of the period (6 and 9) to make the two periods comparable; direction shares are percentages of the place's thunderstorms. The wind roses use the same construction as in the wind analyses (area ∝ share; rings at 10, 20, 30 and 40 %). The total row of p. 67 b7 agrees with the rows after the correction. The comparison figure 19 is Brückner's statement of “scientific investigations” (p. 67), without a source."),
    "findings": [
        bi(f"In Gera fallen {F(100*jja/tot_all,0)[0]} % der Gewitter in die Monate Juni bis August ({jja} von {tot_all} in den Perioden 1853–1858 und 1859–1867); Januar, Februar und Dezember zusammen haben nur {jfd}, der November keines. Brückner spricht von »Hochfluthzeit«, »Ebbe« und »Anwachsen« bzw. »Rückgang« (S. 68).",
           f"At Gera {F(100*jja/tot_all,0)[1]} % of thunderstorms fall in June to August ({jja} of {tot_all} in the periods 1853–1858 and 1859–1867); January, February and December together have only {jfd}, November none. Brückner speaks of “high tide”, “ebb”, “rise” and “decline” (p. 68)."),
        bi(f"Die beiden Gera-Perioden stimmen im Jahresgang überein und liegen mit {F(per53)[0]} (1853–1858) und {F(per59)[0]} Gewittern pro Jahr (1859–1867) dicht beieinander; das Zwölfjahresmittel 1856–1867 beträgt {F(PY[('Gera','mean')])[0]}.",
           f"The two Gera periods agree in their annual cycle and lie close together at {F(per53)[1]} (1853–1858) and {F(per59)[1]} thunderstorms a year (1859–1867); the twelve-year mean for 1856–1867 is {F(PY[('Gera','mean')])[1]}."),
        bi(f"Gegenüber dem Durchschnitt von 19 für 50–52½° N liegt Gera mit {F(PY[('Gera','mean')])[0]} höher, Rothenacker ({F(PY[('Rothenacker','mean')])[0]}) und Schleiz ({F(PY[('Schleiz','mean')])[0]}) liegen darunter. Der Abstand ist klein gegenüber der Schwankung eines einzelnen Ortes: Gera zählte 1861 {PY[('Gera','maximum')]:.0f} und 1864 nur {PY[('Gera','minimum')]:.0f} Gewitter; Schleiz und Rothenacker beruhen auf nur zwei Jahren.",
           f"Against the average of 19 for 50–52½° N, Gera is higher at {F(PY[('Gera','mean')])[1]}, while Rothenacker ({F(PY[('Rothenacker','mean')])[1]}) and Schleiz ({F(PY[('Schleiz','mean')])[1]}) are below it. The gap is small compared with the fluctuation of a single place: Gera counted {PY[('Gera','maximum')]:.0f} thunderstorms in 1861 and only {PY[('Gera','minimum')]:.0f} in 1864; Schleiz and Rothenacker rest on only two years."),
        bi(f"Die meisten Gewitter ziehen aus dem Westen heran: in Hohenleuben {F(shr[('Hohenleuben','W')])[0]} % aus W ({F(west_sec['Hohenleuben'])[0]} % aus dem Sektor SW–W–NW), in Gera {F(shr[('Gera','W')])[0]} % aus W und {F(shr[('Gera','S')])[0]} % aus S ({F(west_sec['Gera'])[0]} % aus dem Westsektor).",
           f"Most thunderstorms approach from the west: at Hohenleuben {F(shr[('Hohenleuben','W')])[1]} % from W ({F(west_sec['Hohenleuben'])[1]} % from the SW–W–NW sector), at Gera {F(shr[('Gera','W')])[1]} % from W and {F(shr[('Gera','S')])[1]} % from S ({F(west_sec['Gera'])[1]} % from the western sector)."),
    ],
    "caveats": [
        bi(f"Brückner berichtigt in seinen Zusätzen (S. 830) den Oktoberwert 1853–1858 (1 statt 2) und die Oktobersumme (5 statt 6) sowie das Gera-Mittel auf 22,5 (statt 22,3, S. 67); die Auswertung verwendet diese Werte. Die berichtigte Summe der Monatswerte 1853–1858 ist {tot53}, im Text zur Windrichtung (S. 68) heißt es »134 Gewittern (1853 bis 1858)«; die Differenz von {tot53 - 134} bleibt ungeklärt. Das Mittel in der Tabelle S. 66 lautet 22,4 (Summe ÷ 12 ergibt 22,5); für Rothenacker steht 18,5 gedruckt, Summe ÷ 2 ergibt 17,5 (nicht berichtigt). Verwendet sind die aus den Summen berechneten Werte.",
           f"In his additions (p. 830) Brückner corrects the October value for 1853–1858 (1 instead of 2) and the October total (5 instead of 6), as well as the Gera mean to 22.5 (instead of 22.3, p. 67); the analysis uses these values. The corrected sum of the monthly values for 1853–1858 is {tot53}, whereas the text on wind direction (p. 68) speaks of “134 thunderstorms (1853 to 1858)”; the difference of {tot53 - 134} remains unexplained. The mean in the table on p. 66 is 22.4 (total ÷ 12 gives 22.5); for Rothenacker 18.5 is printed, total ÷ 2 gives 17.5 (not corrected). The values computed from the totals are used."),
        bi("Es ist nicht angegeben, ob Gewitter oder Gewittertage gezählt wurden; die Vergleichszahl 19 hat keinen genannten Ursprung. Für Hohenleuben fehlt die Monatsverteilung, für die Zugrichtung der dortigen 47 Gewitter der Zeitraum.",
           "It is not stated whether thunderstorms or thunderstorm days were counted; the comparison figure 19 has no named origin. For Hohenleuben the monthly distribution is missing, as is the period for the direction of its 47 thunderstorms."),
        bi("Die Richtungen geben die Herkunft der Gewitter nach 16 auf 8 Richtungen zusammengefasster Beobachtung an, bei Gera nach Brückners Zuordnung (S. 62); die Zahlen sind klein (134 und 47) und die Anteile entsprechend unsicher.",
           "The directions give the origin of the thunderstorms from observations merged from 16 to 8 points, for Gera according to Brückner's assignment (p. 62); the numbers are small (134 and 47) and the shares correspondingly uncertain."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Gewitter in Gera nach Monat, zwei Perioden", "Thunderstorms at Gera by month, two periods"),
         "columns": [
             col("period", "Zeitraum", "Period", "string", None, False, "Zeilenüberschrift im Druck"),
             col("period_order", "Reihenfolge des Zeitraums", "Period order", "integer", None, True),
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("count", "Gewitter", "Thunderstorms", "integer", "Zahl", False, "berichtigt nach S. 830 (Oktober 1853–1858); Gedankenstrich im Druck = leer"),
             col("count_printed", "Gewitter laut Tabelle", "Thunderstorms as in the table", "integer", "Zahl", False, "gedruckter Tabellenwert (S. 67), vor der Berichtigung"),
             col("correction", "Berichtigung", "Correction", "string", None, False, "Hinweis auf die Berichtigung in Brückners Zusätzen (S. 830)"),
             col("years", "Jahre im Zeitraum", "Years in the period", "integer", "Jahre", True, "aus der Jahresangabe der Zeile (1853–1858 = 6, 1859–1867 = 9)"),
             col("per_year", "Gewitter pro Jahr", "Thunderstorms per year", "number", "pro Jahr", True, "Zahl ÷ Jahre; Gedankenstrich = 0"),
         ], "rows": monthly, "source_refs": [{"page": "67", "block": "b7", "rows": "r2-r4"}, {"page": "830", "block": "b4", "rows": "i4"}]},
        {"name": "annual", "title": bi("Gewitter pro Jahr nach Ort", "Thunderstorms per year by station"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("kind", "Art der Angabe", "Kind of figure", "string", None, True, "mean = Mittel, maximum / minimum = Einzeljahr (Text S. 67)"),
             col("period", "Zeitraum", "Period", "string"),
             col("total", "Gewitter im Zeitraum", "Thunderstorms in the period", "integer", "Zahl", False, "gedruckte Summe bzw. Zahl aus dem Text"),
             col("years", "Jahre", "Years", "integer", "Jahre", True),
             col("per_year", "Gewitter pro Jahr", "Thunderstorms per year", "number", "pro Jahr", True),
         ], "rows": annual,
         "source_refs": [{"page": "66", "block": "b3", "rows": "r14"}, {"page": "67", "block": "b2", "rows": "r14"}, {"page": "67", "block": "b6"}]},
        {"name": "direction", "title": bi("Gewitter nach Zugrichtung", "Thunderstorms by direction of approach"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True),
             col("direction", "Richtung", "Direction", "string", None, False, "Original »N.« usw."),
             col("dir_index", "Reihenfolge der Richtung", "Direction order", "integer", None, True, "1 = N … 8 = NW im Uhrzeigersinn"),
             col("count", "Gewitter", "Thunderstorms", "integer", "Zahl", False),
             col("share", "Anteil", "Share", "number", "%", True, "an den Gewittern des Ortes (Gera 134, Hohenleuben 47)"),
         ], "rows": dirrows, "source_refs": [{"page": "68", "block": "b2", "rows": "r2-r4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "monthly",
         "title": bi("Gewitter in Gera nach Monat", "Thunderstorms at Gera by month"),
         "caption": bi("Gewitter pro Monat und Jahr, getrennt für 1853–1858 (6 Jahre) und 1859–1867 (9 Jahre). Beide Perioden zeigen dieselbe Jahreskurve mit Höhepunkt im Juni bis August und ohne Gewitter im November.",
                       "Thunderstorms per month and year, separately for 1853–1858 (6 years) and 1859–1867 (9 years). Both periods show the same annual curve with a peak in June to August and no thunderstorms in November."),
         "vegalite": {
             "height": 280,
             "transform": [MONTH_ABBR_CALC],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month"), "axis": {"labelAngle": 0}},
                 "y": {"field": "per_year", "type": "quantitative", "title": bi("Gewitter pro Monat und Jahr", "Thunderstorms per month and year")},
                 "color": {"field": "period", "type": "nominal", "title": None, "scale": {"domain": ["1853–1858", "1859–1867"]}},
                 "tooltip": [{"field": "period", "title": bi("Zeitraum", "Period")},
                             {"field": "mlabel", "title": bi("Monat", "Month")},
                             {"field": "count", "title": bi("Gewitter im Zeitraum", "Thunderstorms in the period")},
                             {"field": "per_year", "title": bi("pro Jahr", "per year"), "format": ".1f"}]}}},
        {"id": "c2", "dataset": "annual",
         "title": bi("Gewitter pro Jahr im Vergleich", "Thunderstorms per year compared"),
         "caption": bi("Mittel je Ort sowie Höchst- und Tiefstwert einzelner Jahre (Einzeljahr) in Gera. Die senkrechte Linie markiert den von Brückner genannten Durchschnitt von 19 Gewittern für 50–52½° nördlicher Breite. Der Unterschied zwischen den Orten liegt innerhalb der Jahresschwankung in Gera (10 bis 45).",
                       "Mean per place and highest and lowest value of single years at Gera. The vertical line marks the average of 19 thunderstorms for 50–52½° north latitude given by Brückner. The difference between places lies within the year-to-year fluctuation at Gera (10 to 45)."),
         "vegalite": {
             "height": 240,
             "layer": [
                 {"transform": [{"calculate": KIND_LABEL, "as": "label"}],
                  "mark": "bar",
                  "encoding": {
                      "y": {"field": "label", "type": "nominal", "title": None, "sort": {"field": "per_year", "order": "descending"}, "axis": {"labelLimit": 300}},
                      "x": {"field": "per_year", "type": "quantitative", "title": bi("Gewitter pro Jahr", "Thunderstorms per year")},
                      "color": {"field": "kind", "type": "nominal", "title": None, "scale": {"domain": ["mean", "maximum", "minimum"]},
                                "legend": {"labelExpr": bi("{'mean':'Mittel','maximum':'Höchstwert','minimum':'Tiefstwert'}[datum.label]",
                                                           "{'mean':'Mean','maximum':'Highest','minimum':'Lowest'}[datum.label]")}},
                      "tooltip": [{"field": "label", "title": bi("Angabe", "Figure")},
                                  {"field": "total", "title": bi("Gewitter im Zeitraum", "Thunderstorms in the period")},
                                  {"field": "years", "title": bi("Jahre", "Years")},
                                  {"field": "per_year", "title": bi("pro Jahr", "per year"), "format": ".1f"}]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]},
                  "encoding": {"x": {"datum": 19}}},
                 {"mark": {"type": "text", "align": "left", "baseline": "bottom", "dx": 4, "dy": -3},
                  "encoding": {"x": {"datum": 19}, "y": {"value": 240}, "text": {"value": "19"}}},
             ]}},
        {"id": "c3", "dataset": "direction",
         "title": bi("Zugrichtung der Gewitter", "Direction of approach of thunderstorms"),
         "caption": bi("Anteil der Gewitter nach Herkunftsrichtung (Fläche ∝ Anteil; Ringe bei 10, 20, 30 und 40 %). In Gera kommen Gewitter aus W und S, in Hohenleuben fast die Hälfte aus W.",
                       "Share of thunderstorms by direction of origin (area ∝ share; rings at 10, 20, 30 and 40 %). At Gera storms come from W and S, at Hohenleuben almost half from W."),
         "vegalite": rose_spec("station_label", "station_order", columns=2, cell=200, rmax=66, label_r=91, rings=(10, 20, 30, 40), dom_max=50,
                               extra_transform=[{"calculate": bi("{'Gera':'Gera (134 Gewitter, 1853–1858)','Hohenleuben':'Hohenleuben (47 Gewitter)'}[datum.station]",
                                                                 "{'Gera':'Gera (134 thunderstorms, 1853–1858)','Hohenleuben':'Hohenleuben (47 thunderstorms)'}[datum.station]"),
                                                 "as": "station_label"}],
                               tooltip_extra=[{"field": "count", "title": bi("Gewitter", "Thunderstorms")}])},
    ],
    "keywords": {
        "de": ["Gewitter", "Unwetter", "Zugrichtung", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Meteorologie", "Jahresgang"],
        "en": ["thunderstorm", "severe weather", "direction of approach", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "meteorology", "annual cycle"]},
    "related": ["klima-witterungserscheinungen-gera-1856-1867", "klima-niederschlagstage-stationen", "klima-wind-gera-1856-1865"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
