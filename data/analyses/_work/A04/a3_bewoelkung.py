"""A04 / analysis 3: degrees of cloudiness ('Ansicht des Himmels': bedeckt / gemischt / hell), pp. 64-65."""
import sys
sys.path.insert(0, ".")
from common import *

CATS = [("bedeckt", 1), ("gemischt", 2), ("hell", 3)]
# ---- monthly series -----------------------------------------------------------------
g64 = grid("64", "b6")   # r3..r14 (grid idx 2..13): cols 1-3 = 10 years, 4-6 = 1 year
g65 = grid("65", "b1")   # r4..r15 (grid idx 3..14): cols 1-3 Hohenleuben 15 y, 4-6 1 y, 7-9 Schleiz 2 y, 10-12 1 y
monthly = []
tot_period = {}
for so, (st, years) in enumerate([("Gera", 10), ("Hohenleuben", 15), ("Schleiz", 2)], start=1):
    for m in range(1, 13):
        if st == "Gera":
            row = g64[1 + m]; c0 = 1
        elif st == "Hohenleuben":
            row = g65[2 + m]; c0 = 1
        else:
            row = g65[2 + m]; c0 = 7
        for k, (cat, co) in enumerate(CATS):
            v = num(row[c0 + k])
            assert float(v).is_integer(), (st, m, cat, v)
            monthly.append([st, so, m, row[0], cat, co, int(v), years, round(v / years, 1)])
            tot_period[(st, cat)] = tot_period.get((st, cat), 0) + int(v)
print(tot_period)
# check against printed totals
assert tot_period[("Gera", "bedeckt")] == 663 and tot_period[("Gera", "gemischt")] == 2432 and tot_period[("Gera", "hell")] == 555
assert tot_period[("Hohenleuben", "bedeckt")] == 2611 and tot_period[("Hohenleuben", "gemischt")] == 824 and tot_period[("Hohenleuben", "hell")] == 2041
assert tot_period[("Schleiz", "bedeckt")] == 291 and tot_period[("Schleiz", "gemischt")] == 293 and tot_period[("Schleiz", "hell")] == 147  # printed total for bedeckt: 290

# ---- annual comparison (p. 65 b4) -------------------------------------------------------
g4 = grid("65", "b4")
annual = []
ann = {}
for so, r in enumerate(range(1, 7), start=1):
    st = g4[r][0].replace(".", "").strip()
    vals = [num(g4[r][c]) for c in (1, 2, 3)]
    tot = sum(vals)
    for k, (cat, co) in enumerate(CATS):
        ann[(st, cat)] = vals[k]
        annual.append([st, so, cat, co, vals[k], round(100 * vals[k] / tot, 1)])
    ann[(st, "total")] = tot
print(ann)
STS = ["Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Hof", "Arnstadt"]
assert [a[0] for a in annual[::3]] == STS
SH = {(a[0], a[2]): a[5] for a in annual}
# monthly extremes (days per year, derived)
mp = {(r[0], r[2], r[4]): r[8] for r in monthly}
def argmax(st, cat):
    vs = [(mp[(st, m, cat)], m) for m in range(1, 13)]
    return max(vs), min(vs)
for st in ("Gera", "Hohenleuben", "Schleiz"):
    for cat, _ in CATS:
        print(st, cat, argmax(st, cat))

MN_DE = MONTH_FULL_DE
MN_EN = MONTH_FULL_EN


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


(gb_max, gb_min) = argmax("Gera", "bedeckt")
(hb_max, hb_min) = argmax("Hohenleuben", "bedeckt")
(gh_max, gh_min) = argmax("Gera", "hell")
(hh_max, hh_min) = argmax("Hohenleuben", "hell")
(sb_max, sb_min) = argmax("Schleiz", "bedeckt")

CAT_LABEL_CALC = {"calculate": bi("datum.category", "{'bedeckt':'Overcast','gemischt':'Mixed','hell':'Clear'}[datum.category]"), "as": "cat_label"}
CAT_LEGEND = {"labelExpr": bi("datum.label", "{'bedeckt':'Overcast','gemischt':'Mixed','hell':'Clear'}[datum.label]")}
CAT_COLOR = {"field": "category", "type": "nominal", "title": None, "scale": {"domain": ["bedeckt", "gemischt", "hell"]}, "legend": CAT_LEGEND}

ana = {
    "id": "klima-bewoelkung-stationen",
    "title": bi("Bewölkung: bedeckte, gemischte und helle Tage an sechs Orten", "Cloud cover: overcast, mixed and clear days at six places"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "64", "block": "b4"}, {"page": "64", "block": "b5"}, {"page": "64", "block": "b6", "rows": "r3-r15"},
                {"page": "65", "block": "b1", "rows": "r4-r16"}, {"page": "65", "block": "b2"}, {"page": "65", "block": "b3"},
                {"page": "65", "block": "b4", "rows": "r2-r7"}, {"page": "65", "block": "b5"}, {"page": "65", "block": "fn1"}],
    "summary": bi(
        "Unter »Grade der Bewölkung oder die Ansicht des Himmels« zählt Brückner die Tage, an denen der Himmel bedeckt, gemischt oder hell war: monatlich für Gera (10 Jahre), Hohenleuben (15 Jahre) und Schleiz (2 Jahre), im Jahresmittel auch für Rothenacker sowie die auswärtigen Orte Hof und Arnstadt. Die Orte weichen stark voneinander ab, vor allem bei den »gemischten« Tagen; Brückner führt das auf uneinheitliche Abgrenzungen der Beobachter zurück.",
        "Under “Degrees of cloudiness, or the view of the sky”, Brückner counts the days on which the sky was overcast, mixed or clear: by month for Gera (10 years), Hohenleuben (15 years) and Schleiz (2 years), and as annual means also for Rothenacker and for the outside places Hof and Arnstadt. The places differ greatly, above all in the “mixed” days; Brückner attributes this to observers not drawing the categories alike."),
    "method": bi(
        "Gera: S. 64, Tabelle b6 (Summe über 10 Jahre je Monat); Hohenleuben und Schleiz: S. 65, Tabelle b1 (Summen über 15 bzw. 2 Jahre); Jahresmittel aller sechs Orte: S. 65, Tabelle b4 (Rothenacker: Mittel der zwei Jahre Juni 1866 bis Mai 1868, S. 65 b2 und Fußnote). Für die Monatskurven wurden die gedruckten Periodensummen durch die Zahl der Jahre geteilt (Tage pro Monat und Jahr); Brückners eigene Spalten »in 1 Jahr« sind gerundet bzw. enthalten Druckabweichungen und werden nicht verwendet. Die Anteile in Chart 1 beziehen sich auf die Summe der drei gedruckten Jahreswerte des jeweiligen Orts (Hohenleuben: 364,3 statt 365 Tage wegen gerundeter Monatswerte). Der Druck gibt für die Gera-Reihe nur »in 10 Jahren« an, keinen Zeitraum.",
        "Gera: p. 64, table b6 (sum over 10 years per month); Hohenleuben and Schleiz: p. 65, table b1 (sums over 15 and 2 years); annual means for all six places: p. 65, table b4 (Rothenacker: mean of the two years June 1866 to May 1868, p. 65 b2 and footnote). For the monthly curves the printed period totals were divided by the number of years (days per month and year); Brückner's own “in 1 year” columns are rounded or contain misprints and are not used. The shares in chart 1 refer to the sum of the three printed annual values of each place (Hohenleuben: 364.3 instead of 365 days because of rounded monthly values). For the Gera series the print gives only “in 10 years”, no period."),
    "findings": [
        bi(f"Am stärksten unterscheiden sich die »gemischten« Tage: Gera {F(ann[('Gera','gemischt')])[0]} Tage im Jahr ({F(SH[('Gera','gemischt')])[0]} %), Hohenleuben nur {F(ann[('Hohenleuben','gemischt')])[0]} ({F(SH[('Hohenleuben','gemischt')])[0]} %). Umgekehrt zählt Gera nur {F(ann[('Gera','bedeckt')])[0]} bedeckte Tage ({F(SH[('Gera','bedeckt')])[0]} %), Hohenleuben {F(ann[('Hohenleuben','bedeckt')])[0]} ({F(SH[('Hohenleuben','bedeckt')])[0]} %).",
           f"The “mixed” days differ most: Gera {F(ann[('Gera','gemischt')])[1]} days a year ({F(SH[('Gera','gemischt')])[1]} %), Hohenleuben only {F(ann[('Hohenleuben','gemischt')])[1]} ({F(SH[('Hohenleuben','gemischt')])[1]} %). Conversely Gera counts only {F(ann[('Gera','bedeckt')])[1]} overcast days ({F(SH[('Gera','bedeckt')])[1]} %), Hohenleuben {F(ann[('Hohenleuben','bedeckt')])[1]} ({F(SH[('Hohenleuben','bedeckt')])[1]} %)."),
        bi(f"Helle Tage reichen von {F(ann[('Rothenacker','hell')])[0]} (Rothenacker) bis {F(ann[('Hohenleuben','hell')])[0]} im Jahr (Hohenleuben); Hof ({F(ann[('Hof','hell')],0)[0]}) und Arnstadt ({F(ann[('Arnstadt','hell')],0)[0]}) liegen dazwischen. Rothenacker und Schleiz folgen bei den bedeckten Tagen mit {F(ann[('Rothenacker','bedeckt')],0)[0]} und {F(ann[('Schleiz','bedeckt')],0)[0]} der Größenordnung von Hof ({F(ann[('Hof','bedeckt')],0)[0]}) und Arnstadt ({F(ann[('Arnstadt','bedeckt')],0)[0]}).",
           f"Clear days range from {F(ann[('Rothenacker','hell')])[1]} (Rothenacker) to {F(ann[('Hohenleuben','hell')])[1]} a year (Hohenleuben); Hof ({F(ann[('Hof','hell')],0)[1]}) and Arnstadt ({F(ann[('Arnstadt','hell')],0)[1]}) lie in between. With {F(ann[('Rothenacker','bedeckt')],0)[1]} and {F(ann[('Schleiz','bedeckt')],0)[1]} overcast days, Rothenacker and Schleiz are of the order of Hof ({F(ann[('Hof','bedeckt')],0)[1]}) and Arnstadt ({F(ann[('Arnstadt','bedeckt')],0)[1]})."),
        bi(f"In allen drei Monatsreihen liegt das Maximum der bedeckten Tage im Spätherbst/Winter (Gera {MN_DE[gb_max[1]-1]} mit {F(gb_max[0])[0]} Tagen, Hohenleuben {MN_DE[hb_max[1]-1]} mit {F(hb_max[0])[0]}, Schleiz {MN_DE[sb_max[1]-1]} mit {F(sb_max[0])[0]}), das Minimum im Hochsommer (Gera {MN_DE[gb_min[1]-1]} {F(gb_min[0])[0]}, Hohenleuben {MN_DE[hb_min[1]-1]} {F(hb_min[0])[0]}).",
           f"In all three monthly series the maximum of overcast days falls in late autumn/winter (Gera {MN_EN[gb_max[1]-1]} with {F(gb_max[0])[1]} days, Hohenleuben {MN_EN[hb_max[1]-1]} with {F(hb_max[0])[1]}, Schleiz {MN_EN[sb_max[1]-1]} with {F(sb_max[0])[1]}), the minimum in high summer (Gera {MN_EN[gb_min[1]-1]} {F(gb_min[0])[1]}, Hohenleuben {MN_EN[hb_min[1]-1]} {F(hb_min[0])[1]})."),
        bi("Brückner erklärt die Abweichungen der inländischen Orte untereinander und von Hof und Arnstadt damit, dass »nicht überall die gleiche Abgrenzung des Trüben, Gemischten und Heiteren eingehalten ist« (S. 65). Die Zahlen sind daher als Maß der Beobachterkonvention, nicht der tatsächlichen Bewölkung zu lesen.",
           "Brückner explains the deviations of the local stations from one another and from Hof and Arnstadt by the categories “overcast, mixed and clear” not having been delimited the same way everywhere (p. 65). The figures should therefore be read as a measure of observer convention rather than of actual cloudiness."),
    ],
    "caveats": [
        bi("Die Gera-Tabelle (S. 64) nennt nur »in 10 Jahren«, keinen Zeitraum. Die frühere Fassung der Edition gab »1783–1792« an; im gedruckten Text steht das nicht. Wahrscheinlich gehört die Reihe zu den Geraer Beobachtungen seit 1856 (S. 54), belegt ist das nicht.",
           "The Gera table (p. 64) says only “in 10 years” and gives no period. The earlier version of the edition stated “1783–1792”; this is not in the printed text. The series probably belongs to the Gera observations since 1856 (p. 54), but this is not documented."),
        bi("Druckabweichungen (am Faksimile bestätigt, Transkription stimmt mit dem Druck überein): Gera, April, gemischt »in 1 Jahr« gedruckt 20,1, richtig 21,1 (211 ÷ 10; Spalte summiert sich sonst auf 242,2 statt der gedruckten 243,2). Schleiz, April, bedeckt gedruckt 23, die Zeile ergibt dann 61 statt 60 Tage; gedruckter Jahreswert 11 und Summe 290 passen zu 22. Schleiz, Oktober und November summieren sich auf 64 bzw. 58 statt 62 und 60 Tage.",
           "Misprints (confirmed on the facsimile; the transcription matches the print): Gera, April, mixed “in 1 year” printed 20.1, should be 21.1 (211 ÷ 10; otherwise the column sums to 242.2 instead of the printed 243.2). Schleiz, April, overcast printed 23, which makes the row 61 instead of 60 days; the printed annual value 11 and the total 290 fit 22. Schleiz, October and November sum to 64 and 58 instead of 62 and 60 days."),
        bi("Die Reihen sind sehr unterschiedlich lang (15, 10, 2 und 1 Jahr). Schleiz (2 Jahre) und Rothenacker (Jahresmittel) sind nur Anhaltspunkte; Hof und Arnstadt stammen von auswärtigen Beobachtern, Quelle und Zeitraum nennt Brückner nicht.",
           "The series are of very different lengths (15, 10, 2 and 1 years). Schleiz (2 years) and Rothenacker (annual mean) are only indications; Hof and Arnstadt come from outside observers, whose source and period Brückner does not give."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Tage mit bedecktem, gemischtem und hellem Himmel nach Monat", "Days with overcast, mixed and clear sky by month"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True),
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("category", "Himmelsansicht", "Sky condition", "string", None, False, "bedeckt / gemischt / hell (Hohenleuben und Schleiz im Druck: bed., gem., hell)"),
             col("category_order", "Reihenfolge der Himmelsansicht", "Sky condition order", "integer", None, True),
             col("days_period", "Tage im Beobachtungszeitraum", "Days in the observation period", "integer", "Tage", False, "gedruckte Summe über den gesamten Zeitraum"),
             col("years", "Jahre im Zeitraum", "Years in the period", "integer", "Jahre", False, "Gera 10, Hohenleuben 15, Schleiz 2 (Spaltenköpfe)"),
             col("days_per_year", "Tage pro Monat und Jahr", "Days per month and year", "number", "Tage", True, "Tage im Zeitraum ÷ Jahre"),
         ], "rows": monthly,
         "source_refs": [{"page": "64", "block": "b6", "rows": "r3-r14"}, {"page": "65", "block": "b1", "rows": "r4-r15"}]},
        {"name": "annual", "title": bi("Himmelsansicht im Jahresmittel, sechs Orte", "Sky condition as annual mean, six places"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string", None, False, "Orte wie im Druck; Hof und Arnstadt liegen außerhalb des Fürstentums"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True, "Reihenfolge wie bei Brückner"),
             col("category", "Himmelsansicht", "Sky condition", "string", None, False),
             col("category_order", "Reihenfolge der Himmelsansicht", "Sky condition order", "integer", None, True),
             col("days_per_year", "Tage pro Jahr", "Days per year", "number", "Tage", False),
             col("share", "Anteil", "Share", "number", "%", True, "an der Summe der drei gedruckten Jahreswerte des Orts"),
         ], "rows": annual, "source_refs": [{"page": "65", "block": "b4", "rows": "r2-r7"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "annual",
         "title": bi("Himmelsansicht im Jahresmittel", "Sky condition, annual mean"),
         "caption": bi("Anteil der bedeckten, gemischten und hellen Tage am Jahr (%), nach Anteil der bedeckten Tage geordnet. Gera meldet zwei Drittel »gemischte« Tage, Hohenleuben nur 15 %; die Spannweite spiegelt unterschiedliche Abgrenzungen wider.",
                       "Share of overcast, mixed and clear days in the year (%), ordered by the share of overcast days. Gera reports two thirds “mixed” days, Hohenleuben only 15 %; the range reflects different delimitations."),
         "vegalite": {
             "height": 280,
             "transform": [CAT_LABEL_CALC, {"calculate": "datum.category == 'bedeckt' ? datum.share : 0", "as": "ovc"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "station", "type": "nominal", "title": None,
                       "sort": {"field": "ovc", "op": "max", "order": "descending"}},
                 "x": {"field": "share", "type": "quantitative", "stack": "zero", "title": bi("Anteil der Tage im Jahr (%)", "Share of days in the year (%)"), "scale": {"domain": [0, 100]}},
                 "color": CAT_COLOR,
                 "order": {"field": "category_order", "type": "quantitative"},
                 "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                             {"field": "cat_label", "title": bi("Himmelsansicht", "Sky condition")},
                             {"field": "days_per_year", "title": bi("Tage pro Jahr", "Days per year")},
                             {"field": "share", "title": "%", "format": ".1f"}]}}},
        {"id": "c2", "dataset": "monthly",
         "title": bi("Jahresgang der Himmelsansicht", "Annual cycle of sky condition"),
         "caption": bi("Tage pro Monat und Jahr (Periodensumme ÷ Jahre). In Gera dominieren »gemischte« Tage das ganze Jahr, in Hohenleuben bedeckte und helle; bedeckte Tage häufen sich überall im Spätherbst und Winter. Schleiz beruht nur auf zwei Jahren.",
                       "Days per month and year (period total ÷ years). At Gera “mixed” days dominate all year, at Hohenleuben overcast and clear ones; overcast days pile up everywhere in late autumn and winter. Schleiz rests on two years only."),
         "vegalite": {
             "autosize": {"type": "pad"},
             "transform": [MONTH_ABBR_CALC, CAT_LABEL_CALC,
                           {"calculate": bi("{'Gera':'Gera (10 Jahre)','Hohenleuben':'Hohenleuben (15 Jahre)','Schleiz':'Schleiz (2 Jahre)'}[datum.station]",
                                            "{'Gera':'Gera (10 years)','Hohenleuben':'Hohenleuben (15 years)','Schleiz':'Schleiz (2 years)'}[datum.station]"), "as": "station_label"}],
             "facet": {"row": {"field": "station_label", "type": "nominal", "title": None,
                               "sort": {"field": "station_order", "op": "min"},
                               "header": {"labelAngle": 0, "labelOrient": "top", "labelAlign": "left", "labelPadding": 4}}},
             "spec": {
                 "width": 560, "height": 84,
                 "mark": {"type": "line", "point": True},
                 "encoding": {
                     "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": None, "axis": {"labelAngle": 0}},
                     "y": {"field": "days_per_year", "type": "quantitative", "title": bi("Tage/Monat", "Days/month"), "scale": {"domain": [0, 30]}, "axis": {"tickCount": 4}},
                     "color": CAT_COLOR,
                     "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                                 {"field": "mlabel", "title": bi("Monat", "Month")},
                                 {"field": "cat_label", "title": bi("Himmelsansicht", "Sky condition")},
                                 {"field": "days_period", "title": bi("Tage im Zeitraum", "Days in the period")},
                                 {"field": "years", "title": bi("Jahre", "Years")},
                                 {"field": "days_per_year", "title": bi("Tage pro Monat und Jahr", "Days per month and year"), "format": ".1f"}]}}}},
    ],
    "keywords": {
        "de": ["Bewölkung", "Himmelsansicht", "bedeckt", "heiter", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Hof", "Arnstadt", "Meteorologie"],
        "en": ["cloud cover", "sky condition", "overcast", "clear sky", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Hof", "Arnstadt", "meteorology"]},
    "related": ["klima-wind-stationen-vergleich", "klima-witterungserscheinungen-gera-1856-1867"],
    "supersedes_legacy": "p. 64 'Grade der Bewölkung' for Gera (iframe; its stated period 1783–1792 is not in the printed text) and p. 65 'Grade der Bewölkung' for Hohenleuben, Schleiz and the six-place comparison (iframe)",
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
