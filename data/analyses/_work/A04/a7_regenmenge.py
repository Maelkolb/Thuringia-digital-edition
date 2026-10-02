"""A04 / analysis 7: rainfall and precipitation days at Gera 1860-1867 (pp. 68-69), with Brueckner's own corrigenda (p. 830)."""
import math
import sys
sys.path.insert(0, ".")
from common import *

LINE_MM = 1000 / 443.296     # 1 Pariser Linie in mm (Brueckner p. 831: 443,296 Linien = 1 m)
ZOLL_MM = 12 * LINE_MM       # 1 Pariser Zoll in mm
GAUGE_SQIN = math.pi * 6 ** 2   # area of a circle of 12 Paris inches diameter
THUERINGEN_ZOLL = 21.12
print("Zoll in mm", ZOLL_MM)

g = grid("69", "b1")
assert g[0][1].startswith("Schnee") and g[9][0] == "Mittel"
SEASONS = [("Winter", 1, 4, "winter_cuin"), ("Frühling", 2, 5, "spring_cuin"), ("Sommer", 3, 6, "summer_cuin"), ("Herbst", 4, 7, "autumn_cuin")]
# Brueckner's corrigenda for p. 69 (p. 830 b6): (column name, year or 'Mittel', printed, corrected)
CORR = [("winter_cuin", 1863, 319.28, 319.25), ("spring_cuin", 1860, 554.50, 534.50),
        ("annual_zoll", 1861, 18.74, 18.13), ("annual_zoll", 1862, 20.59, 23.70), ("annual_zoll", 1863, 20.98, 22.74),
        ("annual_zoll", 1864, 20.45, 18.21), ("annual_zoll", 1865, 20.42, 20.44), ("annual_zoll", "Mittel", 20.36, 20.57)]
CORR_LABEL = {"winter_cuin": ("Winter", "winter"), "spring_cuin": ("Frühling", "spring"), "annual_zoll": ("Jahresmittel (Zoll)", "annual mean (inches)")}
corr_map = {(c, y): (p, n) for c, y, p, n in CORR}

yearly, seasonal = [], []
Y = {}
for r in range(1, 9):
    year = int(g[r][0][:4])
    snow, rain, tot = int(num(g[r][1])), int(num(g[r][2])), int(num(g[r][3]))
    assert snow + rain == tot, year
    vals = {name: num(g[r][c]) for _, _, c, name in SEASONS}
    vals["annual_zoll"] = num(g[r][8])
    printed = dict(vals)
    notes = []
    for col_name in list(vals):
        if (col_name, year) in corr_map:
            p, n = corr_map[(col_name, year)]
            assert abs(vals[col_name] - p) < 1e-9, (year, col_name, vals[col_name], p)
            vals[col_name] = n
            notes.append(f"{CORR_LABEL[col_name][0]}: {fmt(n, 'de', 2)} statt {fmt(p, 'de', 2)}")
    corr_txt = "S. 830: " + "; ".join(notes) if notes else ""
    seas = [vals[name] for _, _, _, name in SEASONS]
    zoll = vals["annual_zoll"]
    yearly.append([year, snow, rain, tot, *seas, zoll, printed["annual_zoll"], round(zoll * ZOLL_MM), corr_txt])
    ssum = sum(seas)
    for (name, order, _, cname), v in zip(SEASONS, seas):
        seasonal.append([year, name, order, v, printed[cname], round(100 * v / ssum, 1)])
    Y[year] = dict(snow=snow, rain=rain, tot=tot, seas=seas, zoll=zoll, mm=zoll * ZOLL_MM, ssum=ssum)
mean_row = g[9]
assert abs(num(mean_row[8]) - corr_map[("annual_zoll", "Mittel")][0]) < 1e-9
mean_zoll_printed = num(mean_row[8])
mean_zoll = corr_map[("annual_zoll", "Mittel")][1]          # corrected printed mean 20,57
mean_zoll_rows = sum(Y[y]["zoll"] for y in Y) / 8
print("mean zoll corrected", mean_zoll, "from rows", mean_zoll_rows, "printed (uncorrected)", mean_zoll_printed)
mean_snow, mean_rain, mean_tot = num(mean_row[1]), num(mean_row[2]), num(mean_row[3])
mean_seas = [sum(Y[y]["seas"][i] for y in Y) / 8 for i in range(4)]           # recomputed from the corrected rows
printed_mean_seas = [num(mean_row[c]) for _, _, c, _ in SEASONS]
smean_tot = sum(mean_seas)
sh_mean = [100 * v / smean_tot for v in mean_seas]
print("season means from corrected rows", [round(v, 2) for v in mean_seas], "printed", printed_mean_seas)
print("season shares of the means", [round(v, 1) for v in sh_mean])
ymax = max(Y, key=lambda y: Y[y]["zoll"]); ymin = min(Y, key=lambda y: Y[y]["zoll"])
above = sorted(y for y in Y if Y[y]["zoll"] > THUERINGEN_ZOLL)
rank = sorted(Y, key=lambda y: -Y[y]["zoll"])
print("wettest", ymax, "driest", ymin, "above Thuringia", above, "ranking", rank)
srank = {y: sorted(range(4), key=lambda i: -Y[y]["seas"][i]) for y in Y}
summer_top = [y for y in Y if srank[y][0] == 2]
winter_low = [y for y in Y if srank[y][3] == 0]
print("summer wettest in", summer_top, "winter driest in", winter_low)
dmax = max(Y, key=lambda y: Y[y]["tot"]); dmin = min(Y, key=lambda y: Y[y]["tot"])
print("most days", dmax, Y[dmax]["tot"], "fewest", dmin, Y[dmin]["tot"])
ratios = {y: Y[y]["ssum"] / Y[y]["zoll"] for y in Y}
print("ratio seasonal sum / depth", {y: round(v, 2) for y, v in ratios.items()}, "gauge area 12-in circle", GAUGE_SQIN)
close = sorted(y for y in Y if abs(ratios[y] - GAUGE_SQIN) < 0.2)
far = sorted(y for y in Y if y not in close)
print("close", close, "far", far)

reference = [["Gera, Mittel 1860–1867", mean_zoll, mean_zoll_printed, round(mean_zoll * ZOLL_MM)],
             ["Thüringen (allgemein)", THUERINGEN_ZOLL, None, round(THUERINGEN_ZOLL * ZOLL_MM)]]
corrections = [[("Mittel" if y == "Mittel" else str(y)), c, p, n] for c, y, p, n in CORR]


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


diff_zoll = THUERINGEN_ZOLL - mean_zoll
RANK_DE = ['größte', 'zweitgrößte', 'drittgrößte', 'viertgrößte', 'fünftgrößte', 'sechstgrößte', 'siebtgrößte', 'kleinste']
RANK_EN = ['largest', 'second-largest', 'third-largest', 'fourth-largest', 'fifth-largest', 'sixth-largest', 'seventh-largest', 'smallest']
LABEL_TXT = {"calculate": bi("datum.label", "datum.label == 'Thüringen (allgemein)' ? 'Thuringia (general)' : 'Gera, mean 1860–1867'"), "as": "label_txt"}
SEASON_LABEL_CALC = {"calculate": bi("datum.season", "{'Winter':'Winter','Frühling':'Spring','Sommer':'Summer','Herbst':'Autumn'}[datum.season]"), "as": "season_label"}
SEASON_COLOR = {"field": "season", "type": "nominal", "title": None, "scale": {"domain": ["Winter", "Frühling", "Sommer", "Herbst"]},
                "legend": {"labelExpr": bi("datum.label", "{'Winter':'Winter','Frühling':'Spring','Sommer':'Summer','Herbst':'Autumn'}[datum.label]")}}
YEARS_ABOVE_DE = ", ".join(str(y) for y in above[:-1]) + (" und " if len(above) > 1 else "") + str(above[-1])
YEARS_ABOVE_EN = ", ".join(str(y) for y in above[:-1]) + (" and " if len(above) > 1 else "") + str(above[-1])
CLOSE_DE = ", ".join(str(y) for y in close)
FAR_DE = ", ".join(str(y) for y in far)

ana = {
    "id": "klima-regenmenge-gera-1860-1867",
    "title": bi("Regenmenge und Niederschlagstage in Gera 1860–1867", "Rainfall and precipitation days at Gera, 1860–1867"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "68", "block": "b7"}, {"page": "69", "block": "b1", "rows": "r2-r10"}, {"page": "69", "block": "b2"}, {"page": "69", "block": "fn1"},
                {"page": "830", "block": "b5", "rows": "i2"}, {"page": "830", "block": "b6"}],
    "summary": bi(
        f"Für Gera hat Dr. Rob. Schmidt (im Druck »Rud. Schmidt«, berichtigt auf S. 830) acht Jahre lang (1860–1867) die Regenmenge gemessen. Brückner druckt je Jahr die Zahl der Schnee- und Regentage, die Niederschlagsmenge der vier Jahreszeiten und das Jahresmittel in Pariser Zoll und vergleicht es mit dem thüringischen Mittel von 21,12 Zoll. Nach seinen Berichtigungen (S. 830) liegt Gera im Mittel mit {F(mean_zoll,2)[0]} Zoll um {F(diff_zoll,2)[0]} Zoll darunter (der Text auf S. 69 nennt noch 0,76); der meiste Niederschlag fällt im Sommer, der wenigste im Winter, 1867 weicht davon ab.",
        f"For Gera, Dr Rob. Schmidt (printed “Rud. Schmidt”, corrected on p. 830) measured rainfall for eight years (1860–1867). For each year Brückner prints the number of snow and rain days, the precipitation of the four seasons and the annual mean in Paris inches and compares it with the Thuringian mean of 21.12 inches. According to his corrections (p. 830) Gera averages {F(mean_zoll,2)[1]} inches, {F(diff_zoll,2)[1]} inch below it (the text on p. 69 still says 0.76); most precipitation falls in summer and least in winter, with 1867 as an exception."),
    "method": bi(
        f"Die acht Jahresreihen stammen aus S. 69 b1; die Vergleichszahl 21,12 Pariser Zoll für Thüringen und die Angabe der acht Messjahre stehen auf S. 68 b7. Brückner berichtigt die Tabelle in seinen »Zusätzen und Berichtigungen« (S. 830 b6): Winter 1863 319,25 statt 319,28; Frühling 1860 534,50 statt 554,50; Jahresmittel 1861 18,13 statt 18,74, 1862 23,70 statt 20,59, 1863 22,74 statt 20,98, 1864 18,21 statt 20,45, 1865 20,44 statt 20,42 und das Gesamtmittel 20,57 statt 20,36. Alle Datensätze enthalten die berichtigten Werte; die Spalten »laut Tabelle« zeigen die gedruckten, die Spalte »Berichtigung« kennzeichnet die betroffenen Jahre, und der Datensatz »Berichtigungen S. 830« listet alle acht Korrekturen. Die Jahreszeitenmittel der Tabelle (Zeile »Mittel«) werden nicht übernommen, sondern aus den berichtigten Zeilen neu berechnet. Brückners Jahre laufen von Dezember bis Dezember (S. 69, Fußnote), die Schnee- und Regentage der Tabellen auf S. 66/67 (Januar bis Januar) weichen deshalb ab. Das Jahresmittel »Mittel p. Z.« ist eine Tiefe in Pariser Zoll und wurde mit 1 Zoll = {fmt(ZOLL_MM,'de',2)} mm in Millimeter umgerechnet (443,296 Pariser Linien = 1 m nach S. 831, 1 Zoll = 12 Linien). Die Jahreszeitenspalten sind in »par. C.=Z.« (Pariser Kubikzoll) gedruckt, die Bezugsfläche ist nicht angegeben; sie werden deshalb nur als Anteile an der Summe der vier Jahreszeiten (%) ausgewertet. Die Jahreszeiten sind die Spalten des Drucks (Winter, Frühling, Sommer, Herbst), nicht neu abgegrenzt. Die gedruckten Zeilen »Schnee + Regen = Summe der Tage« stimmen für alle acht Jahre.",
        f"The eight annual series come from p. 69 b1; the comparison figure of 21.12 Paris inches for Thuringia and the statement of eight measuring years are on p. 68 b7. Brückner corrects the table in his “Additions and corrections” (p. 830 b6): winter 1863 319.25 instead of 319.28; spring 1860 534.50 instead of 554.50; annual mean 1861 18.13 instead of 18.74, 1862 23.70 instead of 20.59, 1863 22.74 instead of 20.98, 1864 18.21 instead of 20.45, 1865 20.44 instead of 20.42 and the overall mean 20.57 instead of 20.36. All datasets contain the corrected values; the columns “as in the table” show the printed ones, the column “Correction” marks the years concerned, and the dataset “Corrections p. 830” lists all eight corrections. The seasonal means of the table (row “Mittel”) are not taken over but recomputed from the corrected rows. Brückner's years run from December to December (p. 69, footnote), so the snow and rain days of the tables on pp. 66/67 (January to January) differ. The annual mean “Mittel p. Z.” is a depth in Paris inches and was converted to millimetres with 1 inch = {fmt(ZOLL_MM,'en',2)} mm (443.296 Paris lines = 1 m according to p. 831, 1 inch = 12 lines). The seasonal columns are printed in “par. C.=Z.” (Paris cubic inches) without a stated reference area, so they are analysed only as shares of the sum of the four seasons (%). The seasons are the print's columns (winter, spring, summer, autumn), not redefined. The printed rows “snow + rain = sum of days” are correct for all eight years."),
    "findings": [
        bi(f"Das berichtigte Jahresmittel beträgt {F(mean_zoll,2)[0]} Pariser Zoll (rund {F(mean_zoll*ZOLL_MM,0)[0]} mm) und liegt damit {F(diff_zoll,2)[0]} Zoll (rund {F(diff_zoll*ZOLL_MM,0)[0]} mm) unter dem thüringischen Mittel von {F(THUERINGEN_ZOLL,2)[0]} Zoll ({F(THUERINGEN_ZOLL*ZOLL_MM,0)[0]} mm). Brückners Text nennt noch den Abstand 0,76 Zoll, der zum unberichtigten Mittel 20,36 gehört.",
           f"The corrected annual mean is {F(mean_zoll,2)[1]} Paris inches (about {F(mean_zoll*ZOLL_MM,0)[1]} mm), {F(diff_zoll,2)[1]} inch (about {F(diff_zoll*ZOLL_MM,0)[1]} mm) below the Thuringian mean of {F(THUERINGEN_ZOLL,2)[1]} inches ({F(THUERINGEN_ZOLL*ZOLL_MM,0)[1]} mm). Brückner's text still gives the gap as 0.76 inch, which belongs to the uncorrected mean 20.36."),
        bi(f"Von Jahr zu Jahr schwankt die Menge zwischen {F(Y[ymin]['zoll'],2)[0]} Zoll ({ymin}) und {F(Y[ymax]['zoll'],2)[0]} Zoll ({ymax}); {YEARS_ABOVE_DE} liegen über dem thüringischen Mittel.",
           f"From year to year the amount varies between {F(Y[ymin]['zoll'],2)[1]} inches ({ymin}) and {F(Y[ymax]['zoll'],2)[1]} inches ({ymax}); {YEARS_ABOVE_EN} lie above the Thuringian mean."),
        bi(f"Im Mittel fallen {F(sh_mean[2],0)[0]} % des Jahresniederschlags im Sommer, {F(sh_mean[1],0)[0]} % im Frühling, {F(sh_mean[3],0)[0]} % im Herbst und {F(sh_mean[0],0)[0]} % im Winter. In {len(summer_top)} von 8 Jahren ist der Sommer die regenreichste Jahreszeit; 1867 fällt aus der Reihe: Der Winter ist mit {F(Y[1867]['seas'][0],0)[0]} Kubikzoll der feuchteste der acht Winter, der Sommer mit {F(Y[1867]['seas'][2],0)[0]} Kubikzoll der trockenste.",
           f"On average {F(sh_mean[2],0)[1]} % of the annual precipitation falls in summer, {F(sh_mean[1],0)[1]} % in spring, {F(sh_mean[3],0)[1]} % in autumn and {F(sh_mean[0],0)[1]} % in winter. In {len(summer_top)} of 8 years summer is the wettest season; 1867 stands out: its winter is the wettest of the eight winters at {F(Y[1867]['seas'][0],0)[1]} cubic inches, its summer the driest at {F(Y[1867]['seas'][2],0)[1]} cubic inches."),
        bi(f"Im Jahr gibt es durchschnittlich {F(mean_tot,0)[0]} Tage mit Niederschlag ({F(mean_rain,0)[0]} Regen-, {F(mean_snow,0)[0]} Schneetage), von {Y[dmin]['tot']} ({dmin}) bis {Y[dmax]['tot']} ({dmax}). Die Zahl der Tage folgt der Regenmenge nur grob: {dmin} hat die wenigsten Tage, aber mit {F(Y[dmin]['zoll'],2)[0]} Zoll die {RANK_DE[rank.index(dmin)]} Regenhöhe der acht Jahre.",
           f"On average there are {F(mean_tot,0)[1]} days with precipitation a year ({F(mean_rain,0)[1]} rain, {F(mean_snow,0)[1]} snow days), ranging from {Y[dmin]['tot']} ({dmin}) to {Y[dmax]['tot']} ({dmax}). The number of days follows the amount only roughly: {dmin} has the fewest days but, at {F(Y[dmin]['zoll'],2)[1]} inches, the {RANK_EN[rank.index(dmin)]} rainfall depth of the eight years."),
    ],
    "caveats": [
        bi(f"Die Berichtigungen auf S. 830 stehen nicht im Tabellentext; Brückners Fließtext (S. 69) ist nicht angepasst: Er nennt 0,76 Zoll Abstand zum thüringischen Mittel (richtig mit dem berichtigten Mittel: {F(diff_zoll,2)[0]}), und die gedruckten Mittel der Jahreszeitenspalten (Winter 377,09; Frühling 590,92; Sommer 891,46; Herbst 465,02) wurden nicht berichtigt. Aus den berichtigten Zeilen ergeben sich {F(mean_seas[0],2)[0]}, {F(mean_seas[1],2)[0]}, {F(mean_seas[2],2)[0]} und {F(mean_seas[3],2)[0]}; der gedruckte Frühlingswert 590,92 gehört zum unberichtigten Wert 554,50 von 1860. Das Gesamtmittel aus den berichtigten Zeilen ist {F(mean_zoll_rows,2)[0]}, berichtigt gedruckt 20,57.",
           f"The corrections on p. 830 are not in the table text, and Brückner's running text (p. 69) has not been adapted: it gives 0.76 inch below the Thuringian mean (correct with the corrected mean: {F(diff_zoll,2)[1]}), and the printed means of the seasonal columns (winter 377.09; spring 590.92; summer 891.46; autumn 465.02) were not corrected. The corrected rows give {F(mean_seas[0],2)[1]}, {F(mean_seas[1],2)[1]}, {F(mean_seas[2],2)[1]} and {F(mean_seas[3],2)[1]}; the printed spring value 590.92 belongs to the uncorrected value 554.50 of 1860. The overall mean from the corrected rows is {F(mean_zoll_rows,2)[1]}, printed after correction 20.57."),
        bi(f"Die Jahreszeitenspalten (Pariser Kubikzoll) und das Jahresmittel (Pariser Zoll) hängen eng zusammen: Teilt man die berichtigte Summe der vier Jahreszeiten durch das Jahresmittel, ergibt sich in {len(close)} von 8 Jahren ({CLOSE_DE}) ein Quotient von {F(min(ratios[y] for y in close),1)[0]} bis {F(max(ratios[y] for y in close),1)[0]}. Das entspricht der Fläche eines Kreises von 12 Pariser Zoll Durchmesser ({F(GAUGE_SQIN,1)[0]} Quadratzoll) und deutet darauf hin, dass die Jahreszeitenwerte Kubikzoll Wasser in einem solchen Auffanggefäß sind. Der Text sagt das nicht, deshalb werden die Jahreszeiten nur als Anteile ausgewertet. Bei {FAR_DE} weicht der Quotient ab ({', '.join(F(ratios[y],1)[0] for y in far)}); dort könnten weitere, nicht berichtigte Fehler stecken.",
           f"The seasonal columns (Paris cubic inches) and the annual mean (Paris inches) are closely related: dividing the corrected sum of the four seasons by the annual mean gives, in {len(close)} of 8 years ({CLOSE_DE}), a quotient of {F(min(ratios[y] for y in close),1)[1]} to {F(max(ratios[y] for y in close),1)[1]}. This equals the area of a circle of 12 Paris inches in diameter ({F(GAUGE_SQIN,1)[1]} square inches) and suggests that the seasonal values are cubic inches of water caught in such a gauge. The text does not say so, so the seasons are analysed only as shares. For {FAR_DE} the quotient deviates ({', '.join(F(ratios[y],1)[1] for y in far)}); further, uncorrected errors may lie there."),
        bi("Acht Jahre sind eine kurze Reihe; Brückner betont selbst, dass die Verteilung des Regens »bedeutenden Störungen« unterliegt (S. 69). Eine einzige Station (Gera) steht für das Unterland; für das Oberland nimmt Brückner eine gleiche oder größere Menge an, ohne Messungen vorzulegen.",
           "Eight years are a short series; Brückner himself stresses that the distribution of rain is subject to “considerable disturbances” (p. 69). A single station (Gera) stands for the Unterland; for the Oberland Brückner assumes an equal or greater amount without presenting measurements."),
    ],
    "conversions": [
        {"from": "Pariser Zoll (Regenhöhe)", "to": "mm", "factor_or_formula": f"mm = Zoll × {ZOLL_MM:.2f}", "reference": "1 Zoll = 12 Pariser Linien; 443,296 Pariser Linien = 1 m (Brückner S. 831)"},
    ],
    "datasets": [
        {"name": "yearly", "title": bi("Niederschlag in Gera nach Jahr (Dezember bis Dezember), nach Brückners Berichtigungen", "Precipitation at Gera by year (December to December), as corrected by Brückner"),
         "columns": [
             col("year", "Jahr", "Year", "integer", None, False, "Jahr von Dezember bis Dezember; 1860 mit Sternchen im Druck"),
             col("snow_days", "Schneetage", "Snow days", "integer", "Tage"),
             col("rain_days", "Regentage", "Rain days", "integer", "Tage"),
             col("days_total", "Summe der Tage", "Total days", "integer", "Tage"),
             col("winter_cuin", "Niederschlag Winter", "Precipitation winter", "number", "Pariser Kubikzoll", False, "berichtigt nach S. 830 (1863); Bezugsfläche nicht angegeben"),
             col("spring_cuin", "Niederschlag Frühling", "Precipitation spring", "number", "Pariser Kubikzoll", False, "berichtigt nach S. 830 (1860)"),
             col("summer_cuin", "Niederschlag Sommer", "Precipitation summer", "number", "Pariser Kubikzoll"),
             col("autumn_cuin", "Niederschlag Herbst", "Precipitation autumn", "number", "Pariser Kubikzoll"),
             col("annual_zoll", "Jahresmittel (Mittel)", "Annual mean", "number", "Pariser Zoll", False, "Spalte »Mittel p. Z.«; berichtigt nach S. 830 (1861–1865)"),
             col("annual_zoll_printed", "Jahresmittel laut Tabelle", "Annual mean as in the table", "number", "Pariser Zoll", False, "gedruckter Tabellenwert vor der Berichtigung"),
             col("annual_mm", "Jahresmittel", "Annual mean", "number", "mm", True, "berichtigte Pariser Zoll × 27,07"),
             col("correction", "Berichtigung", "Correction", "string", None, False, "Hinweis auf Brückners Berichtigung (S. 830)"),
         ], "rows": yearly, "source_refs": [{"page": "69", "block": "b1", "rows": "r2-r9"}, {"page": "830", "block": "b6"}]},
        {"name": "seasonal", "title": bi("Niederschlag nach Jahreszeit (Anteile), nach Berichtigung", "Precipitation by season (shares), as corrected"),
         "columns": [
             col("year", "Jahr", "Year", "integer", None, False),
             col("season", "Jahreszeit", "Season", "string", None, True, "Spaltenüberschrift im Druck"),
             col("season_order", "Reihenfolge der Jahreszeit", "Season order", "integer", None, True),
             col("amount", "Niederschlag", "Precipitation", "number", "Pariser Kubikzoll", False, "berichtigt nach S. 830 (Winter 1863, Frühling 1860); Bezugsfläche nicht angegeben"),
             col("amount_printed", "Niederschlag laut Tabelle", "Precipitation as in the table", "number", "Pariser Kubikzoll", False, "gedruckter Tabellenwert vor der Berichtigung"),
             col("share", "Anteil an der Jahressumme", "Share of the annual sum", "number", "%", True, "Anteil an der Summe der vier Jahreszeiten des Jahres"),
         ], "rows": seasonal, "source_refs": [{"page": "69", "block": "b1", "rows": "r2-r9"}, {"page": "830", "block": "b6"}]},
        {"name": "reference", "title": bi("Mittelwerte zum Vergleich", "Means for comparison"),
         "columns": [
             col("label", "Bezeichnung", "Label", "string", None, False),
             col("zoll", "Jahresmenge", "Annual amount", "number", "Pariser Zoll", False, "Gera: berichtigt nach S. 830 (20,57); Thüringen: Text S. 68"),
             col("zoll_printed", "Jahresmenge laut Tabelle", "Annual amount as in the table", "number", "Pariser Zoll", False, "Gera: gedruckt 20,36 (vor der Berichtigung)"),
             col("mm", "Jahresmenge", "Annual amount", "number", "mm", True),
         ], "rows": reference, "source_refs": [{"page": "69", "block": "b1", "rows": "r10"}, {"page": "68", "block": "b7"}, {"page": "830", "block": "b6"}]},
        {"name": "corrections", "title": bi("Berichtigungen S. 830 zur Tabelle auf S. 69", "Corrections on p. 830 to the table on p. 69"),
         "columns": [
             col("target", "Jahr bzw. Zeile", "Year or row", "string", None, False, "»Mittel« = Zeile Mittel; Jahreszuordnung nach der Reihenfolge der Berichtigung"),
             col("column", "Spalte", "Column", "string", None, True, "winter_cuin = Spalte 5, spring_cuin = Spalte 6, annual_zoll = Spalte 9"),
             col("printed", "Wert laut Tabelle", "Value as in the table", "number", None, False),
             col("corrected", "Berichtigter Wert", "Corrected value", "number", None, False),
         ], "rows": corrections, "source_refs": [{"page": "830", "block": "b6"}, {"page": "69", "block": "b1", "rows": "r2-r10"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "yearly", "extra_datasets": ["reference"],
         "title": bi("Jahresniederschlag in Gera", "Annual precipitation at Gera"),
         "caption": bi(f"Regenhöhe je Jahr in Millimetern (berichtigte Pariser Zoll × 27,07; die Achse beginnt bei 450 mm, nicht bei null). Die Linien zeigen das berichtigte Mittel 1860–1867 und das von Brückner angegebene Mittel für Thüringen (21,12 Zoll); darüber liegen {YEARS_ABOVE_DE}.",
                       f"Rainfall depth per year in millimetres (corrected Paris inches × 27.07; the axis starts at 450 mm, not at zero). The lines show the corrected 1860–1867 mean and the Thuringian mean given by Brückner (21.12 inches); {YEARS_ABOVE_EN} lie above."),
         "vegalite": {
             "height": 300,
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": bi("Jahr (Dezember bis Dezember)", "Year (December to December)"), "axis": {"labelAngle": 0}},
                      "y": {"field": "annual_mm", "type": "quantitative", "title": "mm", "scale": {"domain": [450, 650], "zero": False}},
                      "tooltip": [{"field": "year", "title": bi("Jahr", "Year")},
                                  {"field": "annual_zoll", "title": bi("Pariser Zoll (berichtigt)", "Paris inches (corrected)")},
                                  {"field": "annual_zoll_printed", "title": bi("Pariser Zoll laut Tabelle", "Paris inches as in the table")},
                                  {"field": "annual_mm", "title": "mm", "format": ".0f"}]}},
                 {"data": {"name": "reference"},
                  "mark": {"type": "rule", "strokeDash": [4, 3]},
                  "encoding": {"y": {"field": "mm", "type": "quantitative"}, "strokeDash": {"field": "label", "type": "nominal", "legend": None}}},
                 {"data": {"name": "reference"},
                  "transform": [{"filter": "datum.label == 'Thüringen (allgemein)'"}, LABEL_TXT],
                  "mark": {"type": "text", "align": "left", "baseline": "bottom", "dx": 4, "dy": -3},
                  "encoding": {"y": {"field": "mm", "type": "quantitative"}, "x": {"value": 0}, "text": {"field": "label_txt"}}},
                 {"data": {"name": "reference"},
                  "transform": [{"filter": "datum.label != 'Thüringen (allgemein)'"}, LABEL_TXT],
                  "mark": {"type": "text", "align": "left", "baseline": "top", "dx": 4, "dy": 3},
                  "encoding": {"y": {"field": "mm", "type": "quantitative"}, "x": {"value": 0}, "text": {"field": "label_txt"}}},
             ]}},
        {"id": "c2", "dataset": "seasonal",
         "title": bi("Niederschlag nach Jahreszeit", "Precipitation by season"),
         "caption": bi(f"Anteil der vier Jahreszeiten an der Jahressumme (%, nach Berichtigung). Der Sommer hat in {len(summer_top)} von 8 Jahren den größten Anteil, der Winter in {len(winter_low)} Jahren den kleinsten; 1867 kehrt das Bild um.",
                       f"Share of the four seasons in the annual sum (%, as corrected). Summer has the largest share in {len(summer_top)} of 8 years, winter the smallest in {len(winter_low)} years; 1867 reverses the picture."),
         "vegalite": {
             "height": 300,
             "transform": [SEASON_LABEL_CALC],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr (Dezember bis Dezember)", "Year (December to December)"), "axis": {"labelAngle": 0}},
                 "y": {"field": "share", "type": "quantitative", "stack": "zero", "title": bi("Anteil an der Jahressumme (%)", "Share of the annual sum (%)"), "scale": {"domain": [0, 100]}},
                 "color": SEASON_COLOR,
                 "order": {"field": "season_order", "type": "quantitative"},
                 "tooltip": [{"field": "year", "title": bi("Jahr", "Year")},
                             {"field": "season_label", "title": bi("Jahreszeit", "Season")},
                             {"field": "amount", "title": bi("Pariser Kubikzoll", "Paris cubic inches")},
                             {"field": "share", "title": "%", "format": ".1f"}]}}},
        {"id": "c3", "dataset": "yearly",
         "title": bi("Schnee- und Regentage", "Snow and rain days"),
         "caption": bi(f"Zahl der Tage mit Schnee und mit Regen je Jahr (Dezember bis Dezember). Das Jahr {dmin} hat mit {Y[dmin]['tot']} die wenigsten, {dmax} mit {Y[dmax]['tot']} die meisten Tage mit Niederschlag.",
                       f"Number of days with snow and with rain per year (December to December). {dmin} has the fewest days with precipitation at {Y[dmin]['tot']}, {dmax} the most at {Y[dmax]['tot']}."),
         "vegalite": {
             "height": 280,
             "transform": [{"fold": ["rain_days", "snow_days"], "as": ["kind", "days"]},
                           {"calculate": bi("datum.kind == 'rain_days' ? 'Regen' : 'Schnee'", "datum.kind == 'rain_days' ? 'Rain' : 'Snow'"), "as": "kind_label"},
                           {"calculate": "datum.kind == 'rain_days' ? 1 : 2", "as": "kind_order"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr (Dezember bis Dezember)", "Year (December to December)"), "axis": {"labelAngle": 0}},
                 "y": {"field": "days", "type": "quantitative", "stack": "zero", "title": bi("Tage", "Days")},
                 "color": {"field": "kind_label", "type": "nominal", "title": None, "sort": {"field": "kind_order", "op": "min"}},
                 "order": {"field": "kind_order", "type": "quantitative"},
                 "tooltip": [{"field": "year", "title": bi("Jahr", "Year")},
                             {"field": "kind_label", "title": bi("Art", "Kind")},
                             {"field": "days", "title": bi("Tage", "Days")},
                             {"field": "days_total", "title": bi("Summe der Tage", "Total days")}]}}},
    ],
    "keywords": {
        "de": ["Regenmenge", "Niederschlag", "Regentage", "Schneetage", "Gera", "Thüringen", "Rob. Schmidt", "Pariser Zoll", "Jahreszeiten", "Berichtigung"],
        "en": ["rainfall", "precipitation", "rain days", "snow days", "Gera", "Thuringia", "Rob. Schmidt", "Paris inch", "seasons", "correction"]},
    "related": ["klima-niederschlagstage-stationen", "klima-witterungserscheinungen-gera-1856-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
