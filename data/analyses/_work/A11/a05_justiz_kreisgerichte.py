"""A11-05: Kreisgerichte 1864-1867 - Zivilsachen, Berufungen, Konkurse, Ehescheidungen (pp. 284, 286)."""
from common import *

g = grid("286", "b5")
g4 = grid("284", "b2")
# first panel rows idx 1..6 = Gera, Schleiz, Summe 1867, 1866, 1865, 1864 ; second panel idx 8..13 same order
assert g[3][0].startswith("Sme") and g[6][0] == "1864"
YEARS = {1867: 3, 1866: 4, 1865: 5, 1864: 6}
second = {1867: g[10], 1866: g[11], 1865: g[12], 1864: g[13]}
first = {y: g[i] for y, i in YEARS.items()}
# panel check on Gera + Schleiz = Summe (second panel)
for c in range(0, 4):
    assert num(g[8][c]) + num(g[9][c]) == num(g[10][c]) or (num(g[8][c]) or 0) + (num(g[9][c]) or 0) == num(g[10][c]), c

N = lambda x: num(x) or 0
# Ehescheidung durch Gnade: column present in the print but missing from the transcription (read from the facsimile)
GNADE = {1864: 3, 1865: 2, 1866: 7, 1867: 1}
# Konkurse bei den Einzelgerichten (neue), p. 284 civilia rows 13..16 = Summe 1867, 1866, 1865, 1864; column idx 10
konk_einzel = {1867: N(g4[12][10]), 1866: N(g4[13][10]), 1865: N(g4[14][10]), 1864: N(g4[15][10])}
assert list(konk_einzel.values()) == [30, 16, 13, 17]

yearly = []
for y in (1864, 1865, 1866, 1867):
    f, s = first[y], second[y]
    row = {
        "year": y, "rs_alt": N(f[1]), "rs_neu": N(f[2]), "erk_alt": N(f[3]), "erk_neu": N(f[4]), "verg_alt": N(f[5]), "verg_neu": N(f[6]),
        "unerl_alt": N(f[7]), "unerl_neu": N(f[8]), "ber_einzel_neu": N(f[10]), "b1_best": N(f[11]), "b1_abg": N(f[12]), "b1_zur": N(f[13]),
        "ehe_erk": N(f[14]), "b2_sum": N(f[15]), "b2_best": N(s[0]), "b2_abg": N(s[1]), "b2_zur": N(s[2]), "konk_kg": N(s[3]),
    }
    assert row["rs_neu"] == row["erk_neu"] + row["verg_neu"] + row["unerl_neu"] or y == 1864, (y, row)
    yearly.append(row)
for r in yearly:
    print(r)
Yd = {r["year"]: r for r in yearly}
print({y: (r["rs_neu"], r["erk_neu"] + r["verg_neu"] + r["unerl_neu"]) for y, r in Yd.items()})

# --- appeals, long format ---------------------------------------------------------------
LV1 = ("a", "Berufung gegen Einzelrichter", "Appeal against single judge")
LV2 = ("b", "Berufung gegen Kreisgericht", "Appeal against Kreisgericht")
appeals = []
rates = []
for y in (1864, 1865, 1866, 1867):
    r = Yd[y]
    pend1 = r["ber_einzel_neu"] - (r["b1_best"] + r["b1_abg"] + r["b1_zur"])
    pend2 = r["b2_sum"] - (r["b2_best"] + r["b2_abg"] + r["b2_zur"])
    for lv, items in ((LV1, [("a", "bestätigt", "upheld", r["b1_best"]), ("b", "abgeändert", "altered", r["b1_abg"]), ("c", "Vergleich/Zurücknahme", "settled/withdrawn", r["b1_zur"])]),
                      (LV2, [("a", "bestätigt", "upheld", r["b2_best"]), ("b", "abgeändert", "altered", r["b2_abg"]), ("c", "Vergleich/Zurücknahme", "settled/withdrawn", r["b2_zur"])])):
        for k, de, en, v in items:
            rk = f"{lv[0]}{y}"
            rde = ("Urteile der Einzelrichter, " if lv[0] == "a" else "Urteile der Kreisgerichte, ") + str(y)
            ren = ("Single-judge rulings, " if lv[0] == "a" else "Kreisgericht rulings, ") + str(y)
            appeals.append([lv[0], lv[1], lv[2], y, rk, rde, ren, k, de, en, v])
    rates.append([LV1[0], LV1[1], LV1[2], y, round(100 * r["b1_abg"] / (r["b1_best"] + r["b1_abg"]), 1)])
    rates.append([LV2[0], LV2[1], LV2[2], y, round(100 * r["b2_abg"] / (r["b2_best"] + r["b2_abg"]), 1)])
    print(y, "pending", pend1, pend2)

# --- new lawsuits at Kreisgerichte, long
lawsuits = []
for y in (1864, 1865, 1866, 1867):
    r = Yd[y]
    lawsuits += [[y, "a", "Erkenntnis", "Judgment", r["erk_neu"]],
                 [y, "b", "Vergleich", "Settled", r["verg_neu"]],
                 [y, "c", "Unerledigt", "Unresolved", r["unerl_neu"]]]

# --- konkurse and Ehescheidungen, long
other = []
for y in (1864, 1865, 1866, 1867):
    r = Yd[y]
    other += [[y, "a", "Konkurse (Kreisgerichte)", "Bankruptcies (Kreisgerichte)", r["konk_kg"]],
              [y, "b", "Neue Konkurse (Justizämter)", "New bankruptcies (Justizämter)", konk_einzel[y]],
              [y, "c", "Ehescheidung durch Urteil", "Divorce by judgment", r["ehe_erk"]],
              [y, "d", "Ehescheidung durch Gnade", "Divorce by dispensation", GNADE[y]]]

pct = lambda a, b: 100 * a / b
ab = {(lv, y): v for lv, _, _, y, v in rates}
print(rates)
rs_chg = pct(Yd[1867]["rs_neu"] - Yd[1864]["rs_neu"], Yd[1864]["rs_neu"])
erk_chg = pct(Yd[1867]["erk_neu"] - Yd[1864]["erk_neu"], Yd[1864]["erk_neu"])
reg_chg = pct(Yd[1867]["rs_neu"] * 0 + 19566 - 18537, 18537)
mean_ab1 = sum(ab[("a", y)] for y in (1864, 1865, 1866, 1867)) / 4
mean_ab2 = sum(ab[("b", y)] for y in (1864, 1865, 1866, 1867)) / 4
tot_b1 = sum(Yd[y]["b1_best"] + Yd[y]["b1_abg"] for y in Yd)
tot_ab1 = sum(Yd[y]["b1_abg"] for y in Yd)
tot_b2 = sum(Yd[y]["b2_best"] + Yd[y]["b2_abg"] for y in Yd)
tot_ab2 = sum(Yd[y]["b2_abg"] for y in Yd)
rate1, rate2 = pct(tot_ab1, tot_b1), pct(tot_ab2, tot_b2)
ehe = {y: Yd[y]["ehe_erk"] + GNADE[y] for y in Yd}
print(rs_chg, erk_chg, reg_chg, rate1, rate2, ehe)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "justiz-kreisgerichte-berufungen-konkurse-1864-1867",
    "title": bi("Kreisgerichte 1864–1867: Prozesse, Berufungen, Konkurse und Ehescheidungen", "Kreisgerichte 1864–1867: lawsuits, appeals, bankruptcies and divorces"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "286", "block": "b5", "rows": "r2-r14"}, {"page": "284", "block": "b2", "rows": "r13-r16"}, {"page": "289", "block": "b2"}],
    "summary": bi(
        f"Die beiden Kreisgerichte in Gera und Schleiz entscheiden die gewichtigeren bürgerlichen Rechtsstreitigkeiten, hören Berufungen gegen Urteile der Justizämter und behandeln Konkurse und Ehescheidungen. Die Auswertung stellt die vier Jahre 1864–1867 nebeneinander und zeigt, wie oft Urteile in der Berufung bestätigt oder geändert wurden.",
        f"The two Kreisgerichte at Gera and Schleiz decide the weightier civil lawsuits, hear appeals against rulings of the Justizämter and deal with bankruptcies and divorces. The analysis sets the four years 1864–1867 side by side and shows how often rulings were upheld or altered on appeal.",
    ),
    "method": bi(
        "Quelle ist die Tabelle »Civilia« der Kreisgerichte (S. 286, b5), deren zweite Hälfte (Berufungen gegen Kreisgerichtsurteile, Konkurse) im Druck auf einem zweiten Blatt neben der ersten steht; die Zeilen wurden nach Gera, Schleiz, Summe 1867, 1866, 1865, 1864 zugeordnet und durch Summenproben bestätigt. Die neuen Konkurse der Justizämter stammen aus S. 284. Die Spalte »Ehescheidung durch Gnade« fehlt in der Transkription und wurde dem Faksimile entnommen. Die »Abänderungsquote« ist abgeändert : (bestätigt + abgeändert) und abgeleitet; Berufungen, die per Vergleich oder Zurücknahme endeten oder 1867 noch offen waren, bleiben außen vor.",
        "The source is the table “Civilia” of the Kreisgerichte (p. 286, b5); its second half (appeals against Kreisgericht rulings, bankruptcies) is printed on a second panel beside the first; the rows were assigned to Gera, Schleiz, total 1867, 1866, 1865, 1864 and confirmed by sum checks. The new bankruptcies of the Justizämter come from p. 284. The column “divorce by dispensation” is missing from the transcription and was read from the facsimile. The “alteration rate” = altered : (upheld + altered) and is derived; appeals ended by settlement or withdrawal or still pending are left out.",
    ),
    "findings": [
        bi(f"Die neuen förmlichen Rechtsstreitigkeiten der Kreisgerichte stiegen von {D(Yd[1864]['rs_neu'])} (1864) auf {D(Yd[1867]['rs_neu'])} (1867), also um {D(rs_chg,1)} %; die Zahl der Erkenntnisse wuchs dabei um {D(erk_chg,1)} % (von {D(Yd[1864]['erk_neu'])} auf {D(Yd[1867]['erk_neu'])}), anders als bei den Justizämtern, wo sie sank.",
           f"New formal lawsuits at the Kreisgerichte rose from {E(Yd[1864]['rs_neu'])} (1864) to {E(Yd[1867]['rs_neu'])} (1867), i.e. by {E(rs_chg,1)} %; the number of judgments grew by {E(erk_chg,1)} % (from {E(Yd[1864]['erk_neu'])} to {E(Yd[1867]['erk_neu'])}), unlike at the Justizämter, where it fell."),
        bi(f"In der Berufung wurden Urteile der Einzelrichter öfter geändert ({D(rate1,1)} % der bestätigten oder abgeänderten Fälle 1864–1867) als Urteile der Kreisgerichte ({D(rate2,1)} %).",
           f"On appeal, rulings of single judges were altered more often ({E(rate1,1)} % of the upheld or altered cases in 1864–1867) than rulings of the Kreisgerichte ({E(rate2,1)} %)."),
        bi(f"Die Zahl der Konkurse bei den Kreisgerichten sprang von {D(Yd[1866]['konk_kg'])} (1866) auf {D(Yd[1867]['konk_kg'])} (1867); auch bei den Justizämtern stiegen die neuen Konkurse von {D(konk_einzel[1866])} auf {D(konk_einzel[1867])}. Brückner nennt für 1867 die Not der Arbeiterbevölkerung im reichenfelser Gebiet, allerdings im Zusammenhang mit den Staatsanwaltschaften (S. 289); ein Zusammenhang mit den Konkursen ist denkbar, aber nicht belegt.",
           f"The number of bankruptcies at the Kreisgerichte jumped from {E(Yd[1866]['konk_kg'])} (1866) to {E(Yd[1867]['konk_kg'])} (1867); new bankruptcies at the Justizämter also rose from {E(konk_einzel[1866])} to {E(konk_einzel[1867])}. For 1867 Brückner mentions the distress of the working population in the Reichenfels area, though in connection with the public prosecutors (p. 289); a link with the bankruptcies is conceivable but not documented."),
        bi(f"Förmliche Ehescheidungen (durch Urteil und durch landesherrliche Gnade) zählten {D(ehe[1864])}, {D(ehe[1865])}, {D(ehe[1866])} und {D(ehe[1867])} in den Jahren 1864 bis 1867.",
           f"Formal divorces (by judgment and by princely dispensation) numbered {E(ehe[1864])}, {E(ehe[1865])}, {E(ehe[1866])} and {E(ehe[1867])} in 1864 to 1867."),
    ],
    "caveats": [
        bi("Die Zeile 1866 trägt im Druck der Tabelle »Civilia« die Jahreszahl »1766« (Druckfehler; die übrigen Tabellen und die Reihenfolge der Zeilen sprechen für 1866). In der Tabelle Generalia steht die Summe 3201 der Strafhafttage, die Einzelwerte 1777 + 1446 ergeben jedoch 3223; diese Spalte wird hier nicht verwendet.",
           "In the printed table “Civilia” the 1866 row carries the year “1766” (a misprint; the other tables and the row order point to 1866). In the table Generalia the total of imprisonment days is printed as 3201 although the individual values 1777 + 1446 make 3223; that column is not used here."),
        bi("Für 1864 ergeben die Teilspalten der neuen Rechtsstreitigkeiten (121 + 293 + 157) 571 statt der gedruckten 561; die Abweichung steht so im Original (Faksimile geprüft). Die Balken für 1864 in Abb. 3 zeigen die Summe der Teilspalten.",
           "For 1864 the sub-columns of the new lawsuits (121 + 293 + 157) add up to 571 instead of the printed 561; the discrepancy is in the original (facsimile checked). The 1864 bar in chart 3 shows the sum of the sub-columns."),
        bi("Die Berufungsreihen sind nicht lückenlos: Fälle, die am Jahresende noch offen waren, sind weder bestätigt noch abgeändert; die Abänderungsquote bezieht sich nur auf entschiedene Fälle. Die Zahlen beider Berufungsarten sind klein (häufig unter 40 pro Jahr), die Quoten schwanken entsprechend.",
           "The appeal series are not complete: cases still pending at year end are neither upheld nor altered; the alteration rate refers to decided cases only. The numbers for both kinds of appeal are small (often under 40 a year), so the rates fluctuate accordingly."),
        bi("»Konkurse bei den Kreisgerichten« ist eine einzelne Zahl; ob sie neue oder alle Verfahren des Jahres zählt, geht aus Brückner nicht hervor. Sie ist daher nicht streng mit den »neuen« Konkursen der Justizämter vergleichbar.",
           "“Bankruptcies at the Kreisgerichte” is a single figure; Brückner does not say whether it counts new or all proceedings of the year. It is therefore not strictly comparable with the “new” bankruptcies of the Justizämter."),
    ],
    "datasets": [
        {"name": "appeals", "title": bi("Berufungen nach Instanz, Jahr und Ausgang", "Appeals by level, year and outcome"),
         "columns": [
             col("level_key", "Kürzel Instanz", "Level key", "string"),
             col("level_de", "Instanz", "Level", "string"), col("level_en", "Instanz (englisch)", "Level (English)", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("row_key", "Kürzel Zeile", "Row key", "string"),
             col("row_de", "Zeile", "Row", "string"), col("row_en", "Zeile (englisch)", "Row (English)", "string"),
             col("outcome_key", "Kürzel Ausgang", "Outcome key", "string"),
             col("outcome_de", "Ausgang", "Outcome", "string"), col("outcome_en", "Ausgang (englisch)", "Outcome (English)", "string"),
             col("cases", "Fälle", "Cases", "integer", "Fälle"),
         ],
         "rows": appeals, "source_refs": [{"page": "286", "block": "b5", "rows": "r4-r7"}, {"page": "286", "block": "b5", "rows": "r11-r14"}]},
        {"name": "rates", "title": bi("Abänderungsquote in der Berufung", "Alteration rate on appeal"),
         "columns": [
             col("level_key", "Kürzel Instanz", "Level key", "string"),
             col("level_de", "Instanz", "Level", "string"), col("level_en", "Instanz (englisch)", "Level (English)", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("alteration_rate", "Abänderungsquote", "Alteration rate", "number", "%", derived=True, note="abgeändert : (bestätigt + abgeändert)"),
         ],
         "rows": rates, "source_refs": [{"page": "286", "block": "b5", "rows": "r4-r7"}, {"page": "286", "block": "b5", "rows": "r11-r14"}]},
        {"name": "lawsuits", "title": bi("Neue förmliche Rechtsstreitigkeiten der Kreisgerichte nach Ausgang", "New formal lawsuits of the Kreisgerichte by outcome"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("outcome_key", "Kürzel", "Key", "string"),
             col("outcome_de", "Ausgang", "Outcome", "string"), col("outcome_en", "Ausgang (englisch)", "Outcome (English)", "string"),
             col("cases", "Fälle", "Cases", "integer", "Fälle"),
         ],
         "rows": lawsuits, "source_refs": [{"page": "286", "block": "b5", "rows": "r4-r7"}]},
        {"name": "other", "title": bi("Konkurse und Ehescheidungen", "Bankruptcies and divorces"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("measure_key", "Kürzel", "Key", "string"),
             col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
             col("count", "Anzahl", "Count", "integer", "Fälle", note="Ehescheidungen durch Gnade: dem Faksimile entnommen (Spalte fehlt in der Transkription)."),
         ],
         "rows": other, "source_refs": [{"page": "286", "block": "b5", "rows": "r4-r7"}, {"page": "286", "block": "b5", "rows": "r11-r14"}, {"page": "284", "block": "b2", "rows": "r13-r16"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "appeals",
         "title": bi("Berufungen und ihr Ausgang", "Appeals and their outcome"),
         "caption": bi("Berufungen je Jahr, die bestätigt, abgeändert oder durch Vergleich bzw. Zurücknahme erledigt wurden: oben gegen Urteile der Einzelrichter (beim Kreisgericht), unten gegen Urteile der Kreisgerichte (beim Appellationsgericht).",
                       "Appeals per year that were upheld, altered, or ended by settlement or withdrawal: top against single-judge rulings (at the Kreisgericht), bottom against Kreisgericht rulings (at the Appellate Court)."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("row"), "type": "nominal", "title": None, "sort": {"field": "row_key", "op": "min"}, "axis": {"labelLimit": 300}},
                 "x": {"field": "cases", "type": "quantitative", "title": bi("Berufungen", "Appeals"), "stack": "zero"},
                 "color": {"field": F("outcome"), "type": "nominal", "title": None, "sort": {"field": "outcome_key", "op": "min"}, "legend": {"labelLimit": 300}},
                 "order": {"field": "outcome_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [ttf("row", "Berufungen", "Appeals"), ttf("outcome", "Ausgang", "Outcome"), tt("cases", "Fälle", "Cases")]}}},
        {"id": "c2", "dataset": "rates",
         "title": bi("Abänderungsquote in der Berufung", "Alteration rate on appeal"),
         "caption": bi("Anteil der abgeänderten an den bestätigten oder abgeänderten Urteilen (Prozent). Die Zahlen sind klein, die Quoten schwanken.",
                       "Share of altered rulings among upheld or altered rulings (per cent). The numbers are small, so the rates fluctuate."),
         "vegalite": {
             "height": 240,
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "alteration_rate", "type": "quantitative", "title": bi("abgeändert (%)", "altered (%)"), "scale": {"domain": [0, 60]}},
                 "color": {"field": F("level"), "type": "nominal", "title": None, "sort": {"field": "level_key", "op": "min"}, "legend": {"labelLimit": 400, "columns": 1}},
                 "tooltip": [ttf("level", "Instanz", "Level"), tt("year", "Jahr", "Year"), {"field": "alteration_rate", "title": bi("abgeändert (%)", "altered (%)"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "lawsuits",
         "title": bi("Neue förmliche Rechtsstreitigkeiten der Kreisgerichte", "New formal lawsuits at the Kreisgerichte"),
         "caption": bi("Anzahl der im jeweiligen Jahr neu eingegangenen Rechtsstreitigkeiten nach Ausgang.", "New lawsuits of each year by outcome."),
         "vegalite": {
             "height": 260,
             "mark": {"type": "bar", "width": 55},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "cases", "type": "quantitative", "title": bi("Fälle", "Cases"), "stack": "zero"},
                 "color": {"field": F("outcome"), "type": "nominal", "title": None, "sort": {"field": "outcome_key", "op": "min"}},
                 "order": {"field": "outcome_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("outcome", "Ausgang", "Outcome"), tt("cases", "Fälle", "Cases")]}}},
        {"id": "c4", "dataset": "other",
         "title": bi("Konkurse und Ehescheidungen", "Bankruptcies and divorces"),
         "caption": bi("Anzahl je Jahr. 1867 verdoppelt sich die Zahl der Konkurse bei den Justizämtern, bei den Kreisgerichten vervierfacht sie sich.",
                       "Number per year. In 1867 bankruptcies at the Justizämter almost double, at the Kreisgerichte they quadruple."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "xOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "y": {"field": "count", "type": "quantitative", "title": bi("Anzahl", "Count")},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}, "legend": {"columns": 2, "labelLimit": 300}},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("measure", "Messgröße", "Measure"), tt("count", "Anzahl", "Count")]}}},
    ],
    "keywords": {"de": ["Kreisgericht", "Appellation", "Berufung", "Konkurs", "Ehescheidung", "Rechtsstreitigkeiten", "Gera", "Schleiz", "Gerichtsstatistik"],
                 "en": ["Kreisgericht", "appeal", "bankruptcy", "divorce", "lawsuits", "Gera", "Schleiz", "judicial statistics"]},
    "transcription_issues": [
        {"page": "286", "block": "b5", "cell": "r1c16", "transcribed": "(Spalte fehlt)", "facsimile": "Förmliche Ehescheidung durch Gnade: 1864: 3, 1865: 2, 1866: 7, 1867: 1 (Gera 1, Schleiz —)", "checked_facsimile": True, "note": "Die Kopfzeile »Förmliche Ehescheidung durch Erkenntniß / Gnade« hat zwei Spalten; die Transkription enthält nur die erste. Die Gnade-Werte wurden dem Faksimile entnommen."},
    ],
}
write(ana)
