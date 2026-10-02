"""A01: Geburten 1858-1867 (pp. 107-108): per district, urban/rural, by sex, long-run 1604-1867."""
import re
from common import *

YEARS = list(range(1858, 1868))
g107 = grid("107", "b3")
g108a = grid("108", "b1")
g108b = grid("108", "b3")

# --- births per district (p.107)
births_district = []
for r in g107[1:11]:
    y = int(r[0])
    for k, (ja, jp) in zip(DISTRICTS, [(1, 2), (3, 4), (5, 6), (7, 8)]):
        births_district.append([y, k, inum(r[ja]), num(r[jp])])
mean_row = g107[11]
births_district_mean = []
for k, (ja, jp) in zip(DISTRICTS, [(1, 2), (3, 4), (5, 6), (7, 8)]):
    births_district_mean.append([k, inum(mean_row[ja]), num(mean_row[jp])])

# --- urban / rural births in % of population (p.108 b1)
births_area = []
for r in g108a[2:12]:
    y = int(r[0])
    for k, (js, jl) in zip(DISTRICTS, [(1, 2), (3, 4), (5, 6), (7, 8)]):
        for area, j in (("Städte", js), ("Landorte", jl)):
            v = num(r[j])
            if k == "Lobenstein-Ebersdorf" and y == 1865 and area == "Landorte":
                v = 4.03   # transcribed 4,103; facsimile 4,03 (checked)
            births_area.append([y, k, area, v])
am = g108a[12]
births_area_mean = []
for k, (js, jl) in zip(DISTRICTS, [(1, 2), (3, 4), (5, 6), (7, 8)]):
    births_area_mean.append([k, "Städte", num(am[js])])
    births_area_mean.append([k, "Landorte", num(am[jl])])

# --- sex ratio (p.108 b3)
sex = []
for r in g108b[2:12]:
    y = int(r[0])
    for area, (jm, jw, jr) in (("Städte", (1, 2, 3)), ("Landorte", (4, 5, 6)), ("Zusammen", (7, 8, 9))):
        sex.append([y, area, inum(r[jm]), inum(r[jw]), num(r[jr])])
sm = g108b[12]
sex_mean = []
for area, (jm, jw, jr) in (("Städte", (1, 2, 3)), ("Landorte", (4, 5, 6)), ("Zusammen", (7, 8, 9))):
    sex_mean.append([area, inum(sm[jm]), inum(sm[jw]), num(sm[jr])])

# --- long-run (p.107 b5)
lst = block("107", "b5")["items"]
longrun = []
for it in lst:
    m = re.match(r"(\d{4})\s*:\s*(\d+)", it["text"])
    longrun.append([int(m.group(1)), int(m.group(2))])
print(longrun)


# ------------------------------------------------------------------ numbers for the texts
def series(k, idx=3):
    return {row[0]: row[idx] for row in births_district if row[1] == k}


fue_pct = series("Reuß j. L.")
fue_abs = series("Reuß j. L.", 2)
y_min = min(fue_pct, key=fue_pct.get)
y_max = max(fue_pct, key=fue_pct.get)
mean_pct = {r[0]: r[2] for r in births_district_mean}
abs_growth = (fue_abs[1867] / fue_abs[1858] - 1) * 100
am_d = {(r[0], r[1]): r[2] for r in births_area_mean}
rural_hi = [k for k in DISTRICTS if am_d[(k, "Landorte")] > am_d[(k, "Städte")]]
fue_a = {(r[0], r[2]): r[3] for r in births_area if r[1] == "Reuß j. L."}
n_rural_hi = sum(fue_a[(y, "Landorte")] > fue_a[(y, "Städte")] for y in YEARS)
sx = {(r[0], r[1]): r[4] for r in sex}
fue_ratio = {y: sx[(y, "Zusammen")] for y in YEARS}
r_min = min(fue_ratio, key=fue_ratio.get)
r_max = max(fue_ratio, key=fue_ratio.get)
n_above_100 = sum(r[4] > 100 for r in sex)
sxm = {r[0]: r[3] for r in sex_mean}
lr = dict(longrun)
growth_lr = lr[1867] / lr[1604]
print(y_min, fue_pct[y_min], y_max, fue_pct[y_max], mean_pct, abs_growth, rural_hi, n_rural_hi,
      r_min, fue_ratio[r_min], r_max, fue_ratio[r_max], n_above_100, len(sex), sxm, growth_lr)
assert len(rural_hi) == 4 and n_above_100 == len(sex)

R107 = ref("107", "b3", "r2-r12")
ana = {
    "id": "bevoelkerung-geburten-1858-1867",
    "title": bi("Geburten 1858–1867: Landestheile, Stadt und Land, Geschlecht", "Births 1858–1867: districts, town and country, sex"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [R107, ref("107", "b4"), ref("107", "b5", "i1-i5"), ref("107", "b6"),
                ref("108", "b1", "r3-t13"), ref("108", "b3", "r3-t13"), ref("108", "b4")],
    "summary": bi(
        f"Brückner gibt die Geburten der drei Landestheile und des Fürstenthums für zehn Jahre (1858–1867) absolut und in Procenten der Bevölkerung an, getrennt nach Städten und Landorten sowie nach Geschlecht, dazu eine Reihe für das alte Amt Lobenstein von 1604 bis 1867. Die Diagramme zeigen, dass die Geburtenziffer des Landes zwischen {fde(fue_pct[y_min])} und {fde(fue_pct[y_max])} Procent der Bevölkerung schwankt, auf dem Land höher liegt als in den Städten und dass stets mehr Knaben als Mädchen geboren wurden.",
        f"Brückner prints births for the three districts and the principality over ten years (1858–1867), in absolute numbers and as a percentage of the population, split into towns and rural places and by sex, plus a series for the old Amt Lobenstein from 1604 to 1867. The charts show that the birth rate of the principality varies between {fen(fue_pct[y_min])} and {fen(fue_pct[y_max])} per cent of the population, is higher in the countryside than in the towns, and that boys always outnumber girls."),
    "method": bi(
        "Übernommen wurden die Tabellen auf S. 107 (Geborene absolut und in Procenten der Bevölkerung je Landestheil, 1858–1867 mit gedrucktem Zehnjahresmittel), S. 108 oben (Procent der Bevölkerung getrennt nach Städten und Landorten) und S. 108 unten (männliche und weibliche Geburten, Knabenziffer je 100 Mädchen) sowie die Liste S. 107 (Amt Lobenstein 1604–1867). Alle Zahlen sind gedruckte Werte; „Geborene“ schließen nach der Tabelle S. 111 die Todtgeborenen ein. Die Säulen in Diagramm 2 zeigen die gedruckten Zehnjahresmittel. Der Wert Lobenstein-Ebersdorf, Landorte 1865 steht in der Transkription als 4,103; die Vorlage druckt 4,03 und wurde so übernommen.",
        "The tables on p. 107 (births in absolute numbers and as a percentage of the population per district, 1858–1867, with the printed ten-year mean), p. 108 top (percentage of the population split into towns and rural places) and p. 108 bottom (male and female births, boys per 100 girls) were used, as well as the list on p. 107 (Amt Lobenstein 1604–1867). All figures are printed values; “births” include stillbirths according to the table on p. 111. The bars in chart 2 show the printed ten-year means. The value for Lobenstein-Ebersdorf, rural places, 1865 is transcribed as 4,103; the print reads 4,03, which is used here."),
    "findings": [
        bi(f"Die Geburtenziffer des Fürstenthums liegt in allen zehn Jahren zwischen {fde(fue_pct[y_min])} Procent ({y_min}) und {fde(fue_pct[y_max])} Procent ({y_max}) der Bevölkerung, im gedruckten Mittel bei {fde(mean_pct['Reuß j. L.'])}; Gera ({fde(mean_pct['Gera'])}) und Schleiz ({fde(mean_pct['Schleiz'])}) liegen darüber, Lobenstein-Ebersdorf ({fde(mean_pct['Lobenstein-Ebersdorf'])}) darunter.",
           f"In all ten years the principality's birth rate lies between {fen(fue_pct[y_min])} per cent ({y_min}) and {fen(fue_pct[y_max])} per cent ({y_max}) of the population, with a printed mean of {fen(mean_pct['Reuß j. L.'])}; Gera ({fen(mean_pct['Gera'])}) and Schleiz ({fen(mean_pct['Schleiz'])}) are above it, Lobenstein-Ebersdorf ({fen(mean_pct['Lobenstein-Ebersdorf'])}) below."),
        bi(f"Die Zahl der Geburten stieg von {fue_abs[1858]} (1858) auf {fue_abs[1867]} (1867), also um {fde(abs_growth, 1)} Procent; die Ziffer blieb dabei im selben Band, die Bevölkerung wuchs also etwa im gleichen Maß.",
           f"The number of births rose from {fint_en(fue_abs[1858])} (1858) to {fint_en(fue_abs[1867])} (1867), an increase of {fen(abs_growth, 1)} per cent; the rate stayed within the same band, so the population grew by about the same proportion."),
        bi(f"Auf dem Land wird im Mittel öfter geboren als in den Städten ({fde(am_d[('Reuß j. L.', 'Landorte')])} gegenüber {fde(am_d[('Reuß j. L.', 'Städte')])} Procent). In allen drei Landestheilen liegt das Mittel der Landorte höher; im Fürstenthum übertreffen die Landorte die Städte {'in jedem der zehn Jahre' if n_rural_hi == 10 else f'in {n_rural_hi} von 10 Jahren'}.",
           f"On average more births occur in the countryside than in the towns ({fen(am_d[('Reuß j. L.', 'Landorte')])} against {fen(am_d[('Reuß j. L.', 'Städte')])} per cent). In all three districts the mean for rural places is higher; in the principality rural places exceed the towns {'in every one of the ten years' if n_rural_hi == 10 else f'in {n_rural_hi} of 10 years'}."),
        bi(f"Auf 100 Mädchen kommen im Zehnjahresmittel {fde(sxm['Zusammen'])} Knaben (Städte {fde(sxm['Städte'])}, Landorte {fde(sxm['Landorte'])}); der Wert schwankt im Fürstenthum zwischen {fde(fue_ratio[r_min])} ({r_min}) und {fde(fue_ratio[r_max])} ({r_max}) und liegt in allen Jahren über 100.",
           f"Over the ten years there are {fen(sxm['Zusammen'])} boys per 100 girls (towns {fen(sxm['Städte'])}, rural places {fen(sxm['Landorte'])}); in the principality the figure varies between {fen(fue_ratio[r_min])} ({r_min}) and {fen(fue_ratio[r_max])} ({r_max}) and is above 100 in every year."),
        bi(f"Für das alte Amt Lobenstein nennt Brückner 46 Geburten im Jahr 1604 und 863 im Jahr 1867, das {fde(growth_lr, 1)}-Fache.",
           f"For the old Amt Lobenstein Brückner gives 46 births in 1604 and 863 in 1867, {fen(growth_lr, 1)} times as many."),
    ],
    "caveats": [
        bi("Die Zahlen für Schleiz 1865 sind in Brückners Tabellen nicht einheitlich: S. 107 und S. 108 unten geben 1064 Geburten (3513 im Fürstenthum), die Prozentzahlen auf S. 108 oben und die Tabellen S. 109/111 setzen etwa 1136 (3585) voraus. Das gedruckte Mittel für Schleiz (1061) liegt unter dem Mittel der zehn Jahreswerte (1067,3). Die Vorlage druckt für Gera 1862 „8,95“ statt 3,95 Procent (aus der Geburtenzahl und den Nachbarjahren als 3,95 zu erschließen).",
           "Brückner's tables are not consistent for Schleiz 1865: pp. 107 and 108 (bottom) give 1,064 births (3,513 for the principality), whereas the percentages on p. 108 (top) and the tables on pp. 109 and 111 imply about 1,136 (3,585). The printed mean for Schleiz (1,061) is below the mean of the ten annual values (1,067.3). For Gera 1862 the print reads “8,95” instead of 3.95 per cent (3.95 can be inferred from the number of births and the neighbouring years)."),
        bi("Die Reihe 1604–1867 ist nicht homogen: Sie nennt für 1604–1804 das „alte Amt Lobenstein“, für 1867 den Bezirk Lobenstein-Ebersdorf (863 Geburten, wie in der Tabelle S. 107). Die frühen Pfarrbücher waren lückenhaft; die Reihe zeigt die Größenordnung, nicht ein exaktes Wachstum.",
           "The series 1604–1867 is not homogeneous: for 1604–1804 it names the “old Amt Lobenstein”, for 1867 the district of Lobenstein-Ebersdorf (863 births, as in the table on p. 107). Early parish registers were incomplete; the series shows an order of magnitude, not exact growth."),
    ],
    "datasets": [
        {"name": "births_district", "title": bi("Geborene je Landestheil", "Births per district"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landestheil", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("births", "Geborene", "Births", "integer", "Geburten"),
                     col("births_pct", "Geborene in Procent der Bevölkerung", "Births in per cent of the population", "number", "%")],
         "rows": births_district, "source_refs": [R107]},
        {"name": "births_district_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("births", "Geborene (Jahresmittel)", "Births (annual mean)", "integer", "Geburten"),
                     col("births_pct", "Geborene in Procent der Bevölkerung", "Births in per cent of the population", "number", "%")],
         "rows": births_district_mean, "source_refs": [ref("107", "b3", "r12")]},
        {"name": "births_area", "title": bi("Geborene in Procent der Bevölkerung, Städte und Landorte", "Births in per cent of the population, towns and rural places"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landestheil", "District", "string"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte"),
                     col("births_pct", "Geborene in Procent der Bevölkerung", "Births in per cent of the population", "number", "%")],
         "rows": births_area, "source_refs": [ref("108", "b1", "r3-r12")]},
        {"name": "births_area_mean", "title": bi("Gedrucktes Mittel 1858–1867, Städte und Landorte", "Printed mean 1858–1867, towns and rural places"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("area", "Gebiet", "Area", "string"),
                     col("births_pct", "Geborene in Procent der Bevölkerung", "Births in per cent of the population", "number", "%")],
         "rows": births_area_mean, "source_refs": [ref("108", "b1", "t13")]},
        {"name": "sex_ratio", "title": bi("Geborene nach Geschlecht", "Births by sex"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Zusammen (Fürstenthum)"),
                     col("boys", "Knaben", "Boys", "integer", "Geburten"),
                     col("girls", "Mädchen", "Girls", "integer", "Geburten"),
                     col("boys_per_100_girls", "Knaben auf 100 Mädchen", "Boys per 100 girls", "number", "Knaben je 100 Mädchen")],
         "rows": sex, "source_refs": [ref("108", "b3", "r3-r12")]},
        {"name": "sex_ratio_mean", "title": bi("Gedrucktes Mittel 1858–1867, nach Geschlecht", "Printed mean 1858–1867, by sex"),
         "columns": [col("area", "Gebiet", "Area", "string"),
                     col("boys", "Knaben (Jahresmittel)", "Boys (annual mean)", "integer", "Geburten"),
                     col("girls", "Mädchen (Jahresmittel)", "Girls (annual mean)", "integer", "Geburten"),
                     col("boys_per_100_girls", "Knaben auf 100 Mädchen", "Boys per 100 girls", "number", "Knaben je 100 Mädchen")],
         "rows": sex_mean, "source_refs": [ref("108", "b3", "t13")]},
        {"name": "births_longrun", "title": bi("Geburten im Amt Lobenstein 1604–1867", "Births in the Amt Lobenstein, 1604–1867"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("births", "Geburten", "Births", "integer", "Geburten")],
         "rows": longrun, "source_refs": [ref("107", "b5", "i1-i5")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "births_district",
         "title": bi("Geborene in Procent der Bevölkerung", "Births in per cent of the population"),
         "caption": bi("Je Landestheil und für das ganze Fürstenthum (Reuß j. L.), 1858–1867. Die Achse beginnt nicht bei null.",
                       "By district and for the whole principality (Reuß j. L.), 1858–1867. The axis does not start at zero."),
         "vegalite": {"height": 300, "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "births_pct", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population"), "scale": {"domain": [3.4, 4.4]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("year", "Jahr", "Year"),
                                      tip("births", "Geborene", "Births"), tip("births_pct", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c2", "dataset": "births_area_mean",
         "title": bi("Städte und Landorte im Vergleich", "Towns and rural places compared"),
         "caption": bi("Gedrucktes Zehnjahresmittel 1858–1867, Geborene in Procent der Bevölkerung. In jedem Landestheil liegen die Landorte über den Städten.",
                       "Printed ten-year mean 1858–1867, births in per cent of the population. In every district rural places lie above the towns."),
         "vegalite": {"height": 280, "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": AREAS},
                          "y": {"field": "births_pct", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("area", "Gebiet", "Area"),
                                      tip("births_pct", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c3", "dataset": "sex_ratio",
         "title": bi("Knaben auf 100 Mädchen", "Boys per 100 girls"),
         "caption": bi("Städte, Landorte und Fürstenthum, 1858–1867. Die gestrichelte Linie bei 100 würde gleich viele Knaben und Mädchen bedeuten.",
                       "Towns, rural places and principality, 1858–1867. The dashed rule at 100 would mean equal numbers of boys and girls."),
         "vegalite": {"height": 300,
                      "layer": [
                          {"mark": {"type": "line", "point": True},
                           "encoding": {
                               "x": YEAR_AX,
                               "y": {"field": "boys_per_100_girls", "type": "quantitative", "title": bi("Knaben je 100 Mädchen", "boys per 100 girls"), "scale": {"domain": [98, 118]}},
                               "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": ["Städte", "Landorte", "Zusammen"]}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                               "tooltip": [tip("area", "Gebiet", "Area"), tip("year", "Jahr", "Year"), tip("boys", "Knaben", "Boys"),
                                           tip("girls", "Mädchen", "Girls"), tip("boys_per_100_girls", "Knaben je 100 Mädchen", "Boys per 100 girls", ".2f")]}},
                          {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 100}}}]}},
        {"id": "c4", "dataset": "births_longrun",
         "title": bi("Geburten im Amt Lobenstein, 1604–1867", "Births in the Amt Lobenstein, 1604–1867"),
         "caption": bi("Die fünf von Brückner genannten Jahre; zwischen den Punkten ist die Reihe nur interpoliert. Der Wert 1867 gilt für den Bezirk Lobenstein-Ebersdorf.",
                       "The five years Brückner names; the line between the points is interpolated. The 1867 value refers to the district of Lobenstein-Ebersdorf."),
         "vegalite": {"height": 260,
                      "layer": [
                          {"mark": {"type": "line", "point": True},
                           "encoding": {
                               "x": {"field": "year", "type": "quantitative", "title": YEAR, "axis": {"format": "d", "values": [1600, 1700, 1800]}, "scale": {"domain": [1590, 1880], "nice": False}},
                               "y": {"field": "births", "type": "quantitative", "title": bi("Geburten", "births"), "scale": {"domain": [0, 1000]}},
                               "tooltip": [tip("year", "Jahr", "Year"), tip("births", "Geburten", "Births")]}},
                          {"mark": {"type": "text", "dy": -12},
                           "encoding": {"x": {"field": "year", "type": "quantitative"}, "y": {"field": "births", "type": "quantitative"}, "text": {"field": "births", "type": "quantitative"}}}]}},
    ],
    "transcription_issues": [
        {"page": "108", "block": "b1", "cell": "r10c7", "transcribed": "4,103", "facsimile": "4,03", "checked_facsimile": True,
         "note": "Lobenstein-Ebersdorf, Landorte 1865; in the dataset corrected to the printed 4,03."},
        {"page": "107", "block": "b3", "cell": "r6c3", "transcribed": "3,95", "facsimile": "8,95", "checked_facsimile": True,
         "note": "Gera 1862: the print shows 8,95, an evident printer's error (1354 births, neighbouring years 3,87-4,23); the transcription reads 3,95, which is used here."},
        {"page": "107", "block": "b3", "cell": "r12c4", "transcribed": "1061", "facsimile": "1061", "checked_facsimile": True,
         "note": "Printed ten-year mean for Schleiz; the mean of the ten printed annual values is 1067,3 (the mean for the principality, 3358, fits 1067)."},
    ],
    "keywords": {"de": ["Geburten", "Geburtenziffer", "Knabenziffer", "Geschlechterverhältnis", "Stadt und Land", "Amt Lobenstein", "Bevölkerungsstatistik"],
                 "en": ["births", "birth rate", "sex ratio", "town and country", "Amt Lobenstein", "population statistics"]},
    "related": ["bevoelkerung-uneheliche-geburten-1858-1867", "bevoelkerung-todtgeborene-1858-1867", "bevoelkerung-natuerlicher-zuwachs-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
