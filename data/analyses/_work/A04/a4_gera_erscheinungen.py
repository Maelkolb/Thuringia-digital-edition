"""A04 / analysis 4: weather phenomena at Gera 1856-1867 (p. 66, table b3)."""
import sys
sys.path.insert(0, ".")
from common import *

g = grid("66", "b3")
PH = [  # (key, de, en, years)
    ("Nebel", "Nebel", "Fog", 12),
    ("Regen", "Regen", "Rain", 12),
    ("Schnee", "Schnee/Graupen", "Snow/graupel", 12),
    ("Reif", "Reif", "Hoar frost", 12),
    ("Gewitter", "Gewitter", "Thunderstorms", 12),
    ("Sturm", "Sturm", "Storms", 12),
    ("Hoehenrauch", "Höhenrauch", "Haze (Höhenrauch)", 12),
    ("Sonnenhoefe", "Sonnenhöfe", "Solar halos", 12),
    ("Mondhoefe", "Mondhöfe", "Lunar halos", 12),
    ("Zodiakal", "Zodiakallicht", "Zodiacal light", 7),
    ("Nordlicht", "Nordlicht", "Northern lights", 7),
]
assert len(PH) == 11 and len(g[0]) == 12
vals = {}   # (key, month) -> value used (0 for dash)
printed_vals = {}   # value as printed in the body table
marks = {}          # Min./Max. marks as used (after correction)
dash = {}
# Brueckner's own corrigenda (p. 830, 'S. 66'): column 3 of the Gera table (Regen)
CORR_REGEN = {1: (79, 87), 7: (169, 181), 8: (142, 152), 12: (92, 84)}   # month: (printed, corrected)
CORR_TOTAL = (1540, 1544)
for k, (key, de, en, yrs) in enumerate(PH, start=1):
    for m in range(1, 13):
        cell = g[m][k]
        v = num(cell)
        printed_vals[(key, m)] = None if v is None else int(v)
        vals[(key, m)] = 0 if v is None else int(v)
        dash[(key, m)] = v is None
        marks[(key, m)] = mark(cell)
for m, (was, now) in CORR_REGEN.items():
    assert vals[("Regen", m)] == was, (m, vals[("Regen", m)], was)
    vals[("Regen", m)] = now
# corrected marker: Max. in July instead of May (p. 830)
assert marks[("Regen", 5)] == "Max." and marks[("Regen", 2)] == "Min."
marks[("Regen", 5)] = ""
marks[("Regen", 7)] = "Max."
tot = {key: sum(vals[(key, m)] for m in range(1, 13)) for key, *_ in PH}
printed_tot = {key: int(num(g[13][k])) for k, (key, *_) in enumerate(PH, start=1)}
assert printed_tot["Regen"] == CORR_TOTAL[0] and tot["Regen"] == CORR_TOTAL[1], (tot["Regen"], printed_tot["Regen"])
print({k: (tot[k], printed_tot[k]) for k in tot})
CORRECTION_NOTE = {}
for m, (was, now) in CORR_REGEN.items():
    CORRECTION_NOTE[("Regen", m)] = f"S. 830: {now} statt {was}"
CORRECTION_NOTE[("Regen", 5)] = "S. 830: Max.-Vermerk im Juli statt im Mai"
CORRECTION_NOTE[("Regen", 7)] = CORRECTION_NOTE[("Regen", 7)] + "; Max.-Vermerk (statt Mai)"

monthly = []
for k, (key, de, en, yrs) in enumerate(PH, start=1):
    for m in range(1, 13):
        v = vals[(key, m)]
        monthly.append([m, g[m][0], key, k, None if dash[(key, m)] else v, printed_vals[(key, m)], CORRECTION_NOTE.get((key, m), ""),
                        marks[(key, m)], yrs, round(v / yrs, 2), round(100 * v / tot[key], 1)])
annual = []
for k, (key, de, en, yrs) in enumerate(PH, start=1):
    annual.append([key, k, yrs, tot[key], printed_tot[key], round(tot[key] / yrs, 1)])
PY = {key: tot[key] / yrs for key, de, en, yrs in PH}

def share_of(key, months):
    return 100 * sum(vals[(key, m)] for m in months) / tot[key]

rain_summer = share_of("Regen", [5, 6, 7, 8])
snow_win = share_of("Schnee", [12, 1, 2, 3])
reif_win = share_of("Reif", [12, 1, 2, 3, 4])
nebel_on = share_of("Nebel", [10, 11])
gew_sum = share_of("Gewitter", [6, 7, 8])
sturm_jfm = share_of("Sturm", [12, 1, 2, 3])
hr_amj = share_of("Hoehenrauch", [4, 5, 6])
print(rain_summer, snow_win, reif_win, nebel_on, gew_sum, sturm_jfm, hr_amj)
print({key: max(range(1, 13), key=lambda m: vals[(key, m)]) for key, *_ in PH})
print("rain per year computed", PY["Regen"], "printed mean", g[14][2], "corrected mean 128,6")
zod_months = [m for m in range(1, 13) if vals[("Zodiakal", m)]]
nord_months = [m for m in range(1, 13) if vals[("Nordlicht", m)]]
print(zod_months, nord_months)
MN_DE = ["Jan.", "Febr.", "März", "April", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."]


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


PH_LABEL_CALC = {"calculate": bi("{" + ",".join(f"'{k}':'{de}'" for k, de, en, y in PH) + "}[datum.phenomenon]",
                                 "{" + ",".join(f"'{k}':'{en}'" for k, de, en, y in PH) + "}[datum.phenomenon]"), "as": "ph_label"}
DAYS_TXT = {"calculate": "datum.days == null ? '—' : datum.days", "as": "days_txt"}

ana = {
    "id": "klima-witterungserscheinungen-gera-1856-1867",
    "title": bi("Witterungserscheinungen in Gera 1856–1867", "Weather phenomena at Gera, 1856–1867"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "54", "block": "b1"}, {"page": "66", "block": "b1"}, {"page": "66", "block": "b2"}, {"page": "66", "block": "b3", "rows": "r2-r15"},
                {"page": "67", "block": "b5"}, {"page": "68", "block": "b5"}, {"page": "830", "block": "b3"}],
    "summary": bi(
        "Zu den Geraer Beobachtungen zählt Brückner nicht nur Luftdruck und Wärme, sondern auch Erscheinungen, die zum Teil »in gar keiner Beziehung zu den klimatischen Verhältnissen« stehen, aber für die Ortskunde von Interesse sind. Die Tabelle auf S. 66 verzeichnet für jeden Monat die Zahl von Nebel, Regen, Schnee und Graupen, Reif, Gewittern, Stürmen, Höhenrauch, Sonnen- und Mondhöfen (1856–1867) sowie Zodiakal- und Nordlicht (1859–1865). Die Auswertung zeigt für jede Erscheinung das Jahresprofil.",
        "Besides air pressure and temperature, Brückner reports at Gera phenomena that partly “stand in no relation at all to climatic conditions” but are of interest for local geography. The table on p. 66 gives for each month the number of fog, rain, snow and graupel, hoar frost, thunderstorms, storms, haze, solar and lunar halos (1856–1867) and of zodiacal light and northern lights (1859–1865). The analysis shows the annual profile of each phenomenon."),
    "method": bi(
        "Quelle ist die Monatstabelle S. 66 b3 (Zeile Januar–December), in der Regenspalte berichtigt nach Brückners »Zusätzen und Berichtigungen« (S. 830 b3, ›S. 66‹): Januar 87 statt 79, Juli 181 statt 169, August 152 statt 142, Dezember 84 statt 92, Summe 1544 statt 1540, Mittel 128,6 und »Max.« im Juli statt im Mai. Die Datensatzspalte »Zahl« enthält die berichtigten Werte, »Zahl laut Tabelle« die gedruckten, die Spalte »Berichtigung« kennzeichnet die betroffenen Zeilen. Die gedruckten Zahlen sind Summen über 12 Jahre (1856–1867), bei Zodiakal- und Nordlicht über die 7 Jahre 1859–1865; ob Tage oder einzelne Ereignisse gezählt wurden, sagt Brückner nicht (bei Regen und Schnee spricht er auf S. 69 von »Tagen«). Ein Gedankenstrich im Druck bedeutet: nicht verzeichnet; im Datensatz steht dafür ein leerer Wert, in den Berechnungen 0. Die Vermerke »Min.« und »Max.« (Regen: Februar bzw. berichtigt Juli) stehen in der Spalte »Druckvermerk«. Abgeleitet wurden Werte pro Jahr (Summe ÷ Jahre) und der Anteil jedes Monats an der Jahressumme der Erscheinung (%). Die Monatssummen wurden nachgerechnet und mit der gedruckten Summenzeile verglichen; sie stimmen für alle Spalten, bei Regen nur nach der Berichtigung (1544). Die Benennung der Erscheinungen folgt dem Druck (Reif = Raureif/Rauhreif; Höhenrauch = trockener Dunst, vgl. S. 68).",
        "The source is the monthly table p. 66 b3 (rows January–December), with the rain column corrected according to Brückner's “Additions and corrections” (p. 830 b3, ‘p. 66’): January 87 instead of 79, July 181 instead of 169, August 152 instead of 142, December 84 instead of 92, total 1544 instead of 1540, mean 128.6 and “Max.” in July instead of May. The dataset column “Count” holds the corrected values, “Count as in the table” the printed ones, and the column “Correction” marks the rows concerned. The printed figures are totals over 12 years (1856–1867), and for zodiacal light and northern lights over the 7 years 1859–1865; whether days or single events were counted, Brückner does not say (for rain and snow he speaks of “days” on p. 69). A dash in the print means not recorded; the dataset leaves the value empty and the calculations use 0. The marks “Min.” and “Max.” (rain: February and, as corrected, July) are in the column “Printed mark”. Derived are values per year (total ÷ years) and each month's share of the phenomenon's annual total (%). The monthly totals were recomputed and compared with the printed total row; they agree for all columns, for rain only after the correction (1544). The phenomena are named as in the print (Reif = hoar frost; Höhenrauch = dry haze, cf. p. 68)."),
    "findings": [
        bi(f"Am häufigsten sind Regen (im Mittel {F(PY['Regen'],0)[0]} pro Jahr), Nebel ({F(PY['Nebel'],0)[0]}), Reif ({F(PY['Reif'],0)[0]}) und Schnee/Graupen ({F(PY['Schnee'],0)[0]}); Gewitter ({F(PY['Gewitter'],0)[0]}) und Stürme ({F(PY['Sturm'],0)[0]}) kommen etwa gleich oft vor.",
           f"Rain is the most frequent phenomenon (on average {F(PY['Regen'],0)[1]} a year), followed by fog ({F(PY['Nebel'],0)[1]}), hoar frost ({F(PY['Reif'],0)[1]}) and snow/graupel ({F(PY['Schnee'],0)[1]}); thunderstorms ({F(PY['Gewitter'],0)[1]}) and storms ({F(PY['Sturm'],0)[1]}) occur about equally often."),
        bi(f"Regen und Gewitter häufen sich im Sommer: {F(rain_summer,0)[0]} % der Regenfälle liegen im Mai–August, {F(gew_sum,0)[0]} % der Gewitter im Juni–August, im November gibt es keines. Schnee ({F(snow_win,0)[0]} % im Dezember–März) und Reif ({F(reif_win,0)[0]} % im Dezember–April) treten im Winterhalbjahr auf und fehlen im August ganz.",
           f"Rain and thunderstorms pile up in summer: {F(rain_summer,0)[1]} % of the rain falls in May–August, {F(gew_sum,0)[1]} % of the thunderstorms in June–August, with none in November. Snow ({F(snow_win,0)[1]} % in December–March) and hoar frost ({F(reif_win,0)[1]} % in December–April) belong to the winter half-year and are absent in August."),
        bi(f"Nebel ist im Oktober und November am häufigsten ({F(nebel_on,0)[0]} % der Jahressumme), im August am seltensten; Stürme konzentrieren sich im Dezember bis März ({F(sturm_jfm,0)[0]} %) und sind im Mai und Juni selten (je {vals[('Sturm',5)]}).",
           f"Fog is most frequent in October and November ({F(nebel_on,0)[1]} % of the annual total) and rarest in August; storms concentrate in December to March ({F(sturm_jfm,0)[1]} %) and are rare in May and June ({vals[('Sturm',5)]} each)."),
        bi(f"Höhenrauch fällt zu {F(hr_amj,0)[0]} % in April bis Juni, am häufigsten im Mai ({vals[('Hoehenrauch',5)]} von {tot['Hoehenrauch']}); Brückner führt das auf den Moorrauch Nordwestdeutschlands im Frühjahr zurück und unterscheidet davon den Hochsommer-Höhenrauch (S. 68).",
           f"{F(hr_amj,0)[1]} % of haze falls in April to June, most often in May ({vals[('Hoehenrauch',5)]} of {tot['Hoehenrauch']}); Brückner traces this to the spring moor smoke of north-western Germany and distinguishes it from the high-summer haze (p. 68)."),
    ],
    "caveats": [
        bi(f"Regen: Im Druck ergeben die zwölf Monatswerte 1522, die gedruckte Summe lautet {CORR_TOTAL[0]}. Brückner berichtigt das selbst (S. 830): vier Monatswerte (Januar 87 statt 79, Juli 181 statt 169, August 152 statt 142, Dezember 84 statt 92), die Summe ({CORR_TOTAL[1]} statt {CORR_TOTAL[0]}), das Mittel (128,6) und den Höchstmonat (Juli statt Mai). Die Auswertung verwendet die berichtigten Werte; mit ihnen stimmt die Summe der Monatswerte ({tot['Regen']}). Die Berichtigung nennt als gedruckten Mittelwert 126,4, im Druck steht 128,4 (Faksimile S. 66 und S. 830 geprüft).",
           f"Rain: in the print the twelve monthly values add up to 1522, while the printed total is {CORR_TOTAL[0]}. Brückner corrects this himself (p. 830): four monthly values (January 87 instead of 79, July 181 instead of 169, August 152 instead of 142, December 84 instead of 92), the total ({CORR_TOTAL[1]} instead of {CORR_TOTAL[0]}), the mean (128.6) and the peak month (July instead of May). The analysis uses the corrected values; with them the monthly values add up to the total ({tot['Regen']}). The correction gives 126.4 as the printed mean, whereas the print shows 128.4 (facsimile of p. 66 and p. 830 checked)."),
        bi("Die Mittelwerte der Tabelle (Gewitter 22,4; Sturm 19) sind gerundet bzw. weichen leicht von Summe ÷ 12 ab (22,5 bzw. 19,1); S. 67 nennt für Gewitter 22,3, berichtigt (S. 830) zu 22,5. Zodiakal- und Nordlicht beruhen auf nur sieben Jahren und 25 bzw. 17 Fällen und sind entsprechend zufällig verteilt.",
           "The table's means (thunderstorms 22.4; storms 19) are rounded or deviate slightly from total ÷ 12 (22.5 and 19.1); p. 67 gives 22.3 for thunderstorms, corrected (p. 830) to 22.5. Zodiacal light and northern lights rest on only seven years and 25 and 17 cases and are distributed accordingly at random."),
        bi("Brückner hält die Geraer Reihe für die wertvollste, weil sie über Luftdruck und Wärme hinaus weitere Erscheinungen erfasst; zugleich notierte Kratzsch nur ein- bis zweimal täglich (S. 54). Kurzlebige Erscheinungen wie Gewitter, Nebel oder Höfe können dadurch untererfasst sein. Einen Ortsvergleich bietet die Auswertung »Niederschlagstage, Nebel und Reif an vier Orten«.",
           "Brückner regards the Gera series as the most valuable because it covers further phenomena beyond air pressure and temperature; at the same time Kratzsch noted only once or twice a day (p. 54). Short-lived phenomena such as thunderstorms, fog or halos may therefore be under-recorded. A comparison between places is given in the analysis “Precipitation days, fog and hoar frost at four places”."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Erscheinungen in Gera nach Monat (Summen über die Beobachtungsjahre)", "Phenomena at Gera by month (totals over the observation years)"),
         "columns": [
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("phenomenon", "Erscheinung", "Phenomenon", "string", None, True, "Schlüssel; Bezeichnung nach der Spaltenüberschrift des Drucks"),
             col("phenomenon_order", "Reihenfolge der Erscheinung", "Phenomenon order", "integer", None, True, "Spaltenfolge im Druck"),
             col("days", "Zahl", "Count", "integer", "Tage bzw. Fälle", False, "berichtigt nach S. 830 (nur Regen: Januar, Juli, August, Dezember); Gedankenstrich im Druck = leer"),
             col("days_printed", "Zahl laut Tabelle", "Count as in the table", "integer", "Tage bzw. Fälle", False, "gedruckter Tabellenwert (S. 66), vor der Berichtigung"),
             col("correction", "Berichtigung", "Correction", "string", None, False, "Hinweis auf die Berichtigung in Brückners Zusätzen (S. 830)"),
             col("mark", "Druckvermerk", "Printed mark", "string", None, False, "»Min.« oder »Max.«; Regen: Max. im Juli (S. 830), gedruckt im Mai"),
             col("years", "Jahre im Zeitraum", "Years in the period", "integer", "Jahre", True, "12 (1856–1867), bei Zodiakal- und Nordlicht 7 (1859–1865)"),
             col("per_year", "Zahl pro Jahr", "Count per year", "number", "pro Jahr", True, "Zahl ÷ Jahre"),
             col("share_of_year", "Anteil an der Jahressumme", "Share of annual total", "number", "%", True, "Monatswert ÷ Summe der zwölf Monate"),
         ], "rows": monthly, "source_refs": [{"page": "66", "block": "b3", "rows": "r2-r13"}, {"page": "830", "block": "b3"}]},
        {"name": "annual", "title": bi("Jahressummen und Häufigkeit pro Jahr", "Annual totals and frequency per year"),
         "columns": [
             col("phenomenon", "Erscheinung", "Phenomenon", "string", None, True),
             col("phenomenon_order", "Reihenfolge der Erscheinung", "Phenomenon order", "integer", None, True),
             col("years", "Jahre im Zeitraum", "Years in the period", "integer", "Jahre", True),
             col("total", "Summe der zwölf Monatswerte", "Sum of the twelve monthly values", "integer", "Tage bzw. Fälle", True, "mit den berichtigten Regenwerten; entspricht der berichtigten Summe 1544 (S. 830)"),
             col("total_printed", "Gedruckte Summe", "Printed total", "integer", "Tage bzw. Fälle", False, "Summenzeile S. 66; Regen gedruckt 1540, berichtigt 1544"),
             col("per_year", "Zahl pro Jahr", "Count per year", "number", "pro Jahr", True, "Summe der Monatswerte ÷ Jahre"),
         ], "rows": annual, "source_refs": [{"page": "66", "block": "b3", "rows": "r14"}, {"page": "830", "block": "b3"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "annual",
         "title": bi("Häufigkeit der Erscheinungen pro Jahr", "Frequency of the phenomena per year"),
         "caption": bi("Mittlere Zahl pro Jahr in Gera (Summe ÷ Jahre; Zodiakal- und Nordlicht: 1859–1865, übrige 1856–1867).",
                       "Average number per year at Gera (total ÷ years; zodiacal light and northern lights: 1859–1865, the rest 1856–1867)."),
         "vegalite": {
             "height": 300,
             "transform": [PH_LABEL_CALC],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "ph_label", "type": "nominal", "title": None, "sort": {"field": "per_year", "order": "descending"}},
                 "x": {"field": "per_year", "type": "quantitative", "title": bi("Zahl pro Jahr", "Count per year")},
                 "tooltip": [{"field": "ph_label", "title": bi("Erscheinung", "Phenomenon")},
                             {"field": "per_year", "title": bi("pro Jahr", "per year"), "format": ".1f"},
                             {"field": "total", "title": bi("Summe der Monatswerte", "Sum of monthly values")},
                             {"field": "years", "title": bi("Jahre", "Years")}]}}},
        {"id": "c2", "dataset": "monthly",
         "title": bi("Jahresprofil jeder Erscheinung", "Annual profile of each phenomenon"),
         "caption": bi("Anteil jedes Monats an der Jahressumme der jeweiligen Erscheinung (%). Regen und Gewitter im Sommer, Schnee, Reif und Stürme im Winter, Nebel im Herbst, Höhenrauch im Frühjahr. Zodiakal- und Nordlicht (7 Jahre, 25 bzw. 17 Fälle) sind zufallsbehaftet.",
                       "Share of each month in the phenomenon's annual total (%). Rain and thunderstorms in summer, snow, hoar frost and storms in winter, fog in autumn, haze in spring. Zodiacal light and northern lights (7 years, 25 and 17 cases) are subject to chance."),
         "vegalite": {
             "height": 340,
             "transform": [PH_LABEL_CALC, MONTH_ABBR_CALC, DAYS_TXT],
             "mark": "rect",
             "encoding": {
                 "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month"), "axis": {"labelAngle": 0}},
                 "y": {"field": "ph_label", "type": "nominal", "title": None, "sort": {"field": "phenomenon_order", "op": "min"}},
                 "color": {"field": "share_of_year", "type": "quantitative", "title": bi("Anteil (%)", "Share (%)")},
                 "tooltip": [{"field": "ph_label", "title": bi("Erscheinung", "Phenomenon")},
                             {"field": "mlabel", "title": bi("Monat", "Month")},
                             {"field": "days_txt", "title": bi("Zahl (Summe über die Jahre)", "Count (total over the years)")},
                             {"field": "share_of_year", "title": "%", "format": ".1f"}]}}},
        {"id": "c3", "dataset": "monthly",
         "title": bi("Häufige Erscheinungen im Jahresgang", "Frequent phenomena through the year"),
         "caption": bi("Zahl pro Monat und Jahr (Summe ÷ 12 Jahre). Der Regen erreicht im Mai bis Juli seine höchsten Werte, Schnee und Reif liegen im Winter, Gewitter im Hochsommer, der Nebel im Oktober und November.",
                       "Count per month and year (total ÷ 12 years). Rain peaks from May to July, snow and hoar frost fall in winter, thunderstorms in high summer and fog in October and November."),
         "vegalite": {
             "height": 320,
             "transform": [{"filter": "indexof(['Regen','Nebel','Reif','Schnee','Gewitter','Sturm'], datum.phenomenon) >= 0"}, PH_LABEL_CALC, MONTH_ABBR_CALC],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month"), "axis": {"labelAngle": 0}},
                 "y": {"field": "per_year", "type": "quantitative", "title": bi("Zahl pro Monat und Jahr", "Count per month and year")},
                 "color": {"field": "ph_label", "type": "nominal", "title": None,
                           "sort": {"field": "phenomenon_order", "op": "min"}},
                 "tooltip": [{"field": "ph_label", "title": bi("Erscheinung", "Phenomenon")},
                             {"field": "mlabel", "title": bi("Monat", "Month")},
                             {"field": "per_year", "title": bi("pro Monat und Jahr", "per month and year"), "format": ".1f"}]}}},
    ],
    "keywords": {
        "de": ["Nebel", "Regen", "Schnee", "Reif", "Gewitter", "Sturm", "Höhenrauch", "Haloerscheinungen", "Zodiakallicht", "Nordlicht", "Gera", "Witterung"],
        "en": ["fog", "rain", "snow", "hoar frost", "thunderstorm", "storm", "haze", "halo", "zodiacal light", "northern lights", "Gera", "weather"]},
    "related": ["klima-niederschlagstage-stationen", "klima-gewitter-gera-stationen"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
