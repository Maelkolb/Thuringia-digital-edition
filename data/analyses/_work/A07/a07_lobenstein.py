"""A07: Sterblichkeit im Bezirk Lobenstein-Ebersdorf 1794-1804 (pp. 114-116)."""
from common import *

YEARS = list(range(1794, 1805))
g1 = grid("115", "b1")
g2 = grid("116", "b2")
g3 = grid("116", "b4")
assert g1[1][0] == "1794" and g2[1][0] == "1794" and g3[1][0] == "1794"

annual = [[int(r[0]), inum(r[1]), inum(r[2]), num(r[3])] for r in g1[1:12]]
mean_pct = num(g1[12][3])

CLS = [("Kinder", "männlich", 1), ("Kinder", "weiblich", 2), ("Ledige", "männlich", 3), ("Ledige", "weiblich", 4),
       ("Verheirathete", "männlich", 5), ("Verheirathete", "weiblich", 6)]
classes = []
for r in g2[1:12]:
    for c, s, j in CLS:
        classes.append([int(r[0]), c, s, inum(r[j])])
class_mean = []
for c, s, j in CLS:
    class_mean.append([c, s, num(g2[12][j])])
share = {int(r[0]): (num(r[7]), num(r[8]), num(r[9])) for r in g2[1:12]}

AGES = ["0–10", "10–20", "20–30", "30–40", "40–50", "50–60", "60–70", "70–80", "80–90", "90–100"]
ages = []
for r in g3[1:12]:
    for i, a in enumerate(AGES):
        ages.append([int(r[0]), a, inum(r[1 + i]) or 0])
age_mean_vals = [num(x) for x in g3[12][1:11]]
age_sum = sum(age_mean_vals)
ages_mean = [[a, v, round(v / age_sum * 100, 1)] for a, v in zip(AGES, age_mean_vals)]
print(ages_mean, age_sum)

# ---- numbers for the texts
A = {r[0]: r for r in annual}
d = {y: A[y][2] for y in YEARS}
pc = {y: A[y][3] for y in YEARS}
d_mean = sum(d.values()) / 11
d_mean_ex = (sum(d.values()) - d[1800]) / 10
pc_ex = (sum(pc.values()) - pc[1800]) / 10
print(d_mean, d_mean_ex, pc_ex, sum(pc.values()) / 11)
age = {(r[0], r[1]): r[2] for r in ages}
kids_ex = sorted(age[(y, "0–10")] for y in YEARS if y != 1800)
print(kids_ex, age[(1800, "0–10")])
cm = {(r[0], r[1]): r[2] for r in class_mean}
boys_girls = cm[("Kinder", "männlich")] / cm[("Kinder", "weiblich")]
others = sum(age_mean_vals[1:])
first_share = age_mean_vals[0] / age_sum * 100
print(boys_girls, others, first_share)
mx = max(pc, key=pc.get)
assert mx == 1800
k1800 = sum(v for (y, c, s), v in [((r[0], r[1], r[2]), r[3]) for r in classes] if y == 1800 and c == "Kinder")
print(k1800, k1800 / d[1800] * 100, share[1800])
second = sorted(pc.items(), key=lambda kv: -kv[1])[1]
print(second)
# check the claim of 1858-67 mean for the district: 2.69 (p.114 t26)
lob_58 = num(grid("114", "b1")[25][6])
print(lob_58)
assert lob_58 == 2.69
min_year = min(pc, key=pc.get)
print(min_year, pc[min_year])

ana = {
    "id": "bevoelkerung-sterblichkeit-lobenstein-1794-1804",
    "title": bi("Sterblichkeit im Bezirk Lobenstein-Ebersdorf 1794–1804", "Mortality in the district of Lobenstein-Ebersdorf, 1794–1804"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [ref("114", "b2"), ref("115", "b1", "r2-r13"), ref("116", "b1"), ref("116", "b2", "r2-t13"), ref("116", "b3"), ref("116", "b4", "r2-t13"), ref("116", "b5"),
                ref("114", "b1", "t26"), ref("105", "b3", "r10")],
    "summary": bi(
        f"Für den Bezirk Lobenstein-Ebersdorf hat Brückner aus dem lobensteiner Intelligenzblatt eine elfjährige Reihe (1794–1804) der Einwohner und Gestorbenen übernommen, dazu die Gestorbenen nach Kindern, Ledigen und Verheiratheten (getrennt nach Geschlecht) und nach zehnjährigen Altersklassen. Die Sterblichkeit lag im Mittel bei {fde(mean_pct)} Procent der Einwohner; das Jahr 1800 fällt mit {fde(pc[1800])} Procent heraus, vor allem durch Todesfälle von Kindern bis zehn Jahren. Etwa die Hälfte aller Gestorbenen war jünger als 14 bzw. 10 Jahre.",
        f"For the district of Lobenstein-Ebersdorf Brückner took from the lobensteiner Intelligenzblatt an eleven-year series (1794–1804) of inhabitants and deaths, plus deaths by children, unmarried and married persons (by sex) and by ten-year age classes. Mortality averaged {fen(mean_pct)} per cent of the inhabitants; the year 1800 stands out with {fen(pc[1800])} per cent, mainly through deaths of children under ten. About half of all deaths were of persons under 14 or under 10 years."),
    "method": bi(
        "Übernommen wurden die drei Tabellen auf S. 115 und S. 116: Einwohner, Gestorbene und Procent der Einwohner je Jahr; Gestorbene nach Kindern (bis zum 14. Lebensjahr), ledigen und verheiratheten bzw. verwittweten Personen und Geschlecht; Gestorbene nach Altersklassen von je zehn Jahren. Gedruckte Mittelzeilen bilden eigene Datensätze; die Anteile der Altersklassen an allen Gestorbenen (derived) sind das Mittel der Altersklasse geteilt durch die Summe der Mittel. Ein Strich „—“ in der Vorlage ist als 0 eingetragen.",
        "The three tables on pp. 115 and 116 were taken over: inhabitants, deaths and per cent of the inhabitants per year; deaths by children (up to age 14), unmarried and married or widowed persons and sex; deaths by age classes of ten years. The printed mean rows form separate datasets; the shares of the age classes in all deaths (derived) are the mean of the age class divided by the sum of the means. A dash “—” in the source is entered as 0."),
    "findings": [
        bi(f"Das Jahr 1800 hat {d[1800]} Gestorbene ({fde(pc[1800])} Procent der Einwohner), gegenüber im Mittel der übrigen Jahre {fde(d_mean_ex, 0)} ({fde(pc_ex)} Procent); das Maximum der übrigen Jahre liegt bei {fde(second[1])} Procent ({second[0]}). Brückner führt die großen Schwankungen der Sterbefälle zum Teil auf zeitweilige Verheerungen der Pocken zurück (S. 114).",
           f"The year 1800 has {d[1800]} deaths ({fen(pc[1800])} per cent of the inhabitants), against a mean of {fen(d_mean_ex, 0)} ({fen(pc_ex)} per cent) in the other years; the maximum of the other years is {fen(second[1])} per cent ({second[0]}). Brückner attributes the large fluctuations in deaths partly to temporary ravages of smallpox (p. 114)."),
        bi(f"1800 starben {age[(1800, '0–10')]} Kinder unter zehn Jahren, in den übrigen Jahren {kids_ex[0]} bis {kids_ex[-1]}; das ist der Hauptteil des Ausschlags (Kinder bis 14 Jahre insgesamt {k1800} von {d[1800]} Gestorbenen = {fde(share[1800][0])} Procent). Das deutet auf eine vor allem Kinder treffende Krankheit hin.",
           f"In 1800 {age[(1800, '0–10')]} children under ten died, in the other years {kids_ex[0]} to {kids_ex[-1]}; this is the main part of the peak (children up to 14 in total {k1800} of {d[1800]} deaths = {fen(share[1800][0])} per cent). This suggests a disease that mainly hit children."),
        bi(f"Im Mittel entfallen {fde(first_share, 1)} Procent der Gestorbenen auf die erste Lebensdekade ({fde(age_mean_vals[0])} im Jahr); alle übrigen Dekaden zusammen haben {fde(others)} (ebenso Brückners Summe). Am häufigsten sind unter den Erwachsenen die Altersklassen 60–70 ({fde(age_mean_vals[6])}) und 70–80 Jahre ({fde(age_mean_vals[7])}).",
           f"On average {fen(first_share, 1)} per cent of deaths fall in the first decade of life ({fen(age_mean_vals[0])} a year); all other decades together have {fen(others)} (as does Brückner's own sum). Among adults the age classes 60–70 ({fen(age_mean_vals[6])}) and 70–80 ({fen(age_mean_vals[7])}) are most frequent."),
        bi(f"Unter den gestorbenen Kindern überwiegen die Knaben ({fde(cm[('Kinder', 'männlich')])} gegenüber {fde(cm[('Kinder', 'weiblich')])} Mädchen im Jahr, {fde((boys_girls - 1) * 100, 0)} Procent mehr); unter den Verheiratheten und Verwitweten starben mehr Frauen ({fde(cm[('Verheirathete', 'weiblich')])}) als Männer ({fde(cm[('Verheirathete', 'männlich')])}).",
           f"Among the children who died boys predominate ({fen(cm[('Kinder', 'männlich')])} against {fen(cm[('Kinder', 'weiblich')])} girls a year, {fen((boys_girls - 1) * 100, 0)} per cent more); among married and widowed persons more women ({fen(cm[('Verheirathete', 'weiblich')])}) than men ({fen(cm[('Verheirathete', 'männlich')])}) died."),
        bi(f"Die Sterblichkeit 1794–1804 ({fde(mean_pct)} Procent) liegt über der desselben Bezirks 1858–1867 ({fde(lob_58)} Procent, S. 114), wie Brückner anmerkt.",
           f"Mortality in 1794–1804 ({fen(mean_pct)} per cent) is higher than in the same district in 1858–1867 ({fen(lob_58)} per cent, p. 114), as Brückner remarks."),
    ],
    "caveats": [
        bi("Die Einwohnerzahlen (14 279–15 204) liegen weit unter denen des Bezirks von 1864 (rund 22 500); die Abgrenzung des Bezirks im Intelligenzblatt war also nicht dieselbe wie 1858–1867. Die Reihen sind daher nur bedingt mit S. 114 vergleichbar.",
           "The population figures (14,279–15,204) are far below those of the district in 1864 (about 22,500); the delimitation of the district in the Intelligenzblatt was therefore not the same as in 1858–1867. The series are comparable with p. 114 only to a limited extent."),
        bi("Die Summen der Altersklassen stimmen nicht in allen Jahren mit der Zahl der Gestorbenen überein (1802: 484 gegenüber 492, 1803: 429 gegenüber 426). Die gedruckte Procentzahl 1795 für Ledige (6,49) weicht von der Rechnung (6,59) ab. „Verheirathete“ umfassen laut Brückner auch Verwitwete.",
           "The sums of the age classes do not agree with the number of deaths in every year (1802: 484 against 492, 1803: 429 against 426). The printed percentage for 1795 for unmarried persons (6.49) differs from the calculation (6.59). According to Brückner “married” includes widowed persons."),
        bi("Die Ursache des Ausschlags 1800 nennt Brückner nicht ausdrücklich; der Zusammenhang mit den Pocken ist seine allgemeine Erklärung für die Schwankungen und hier nur als Möglichkeit zu verstehen.",
           "Brückner does not name the cause of the peak in 1800 explicitly; the connection with smallpox is his general explanation for the fluctuations and is to be taken here only as a possibility."),
    ],
    "datasets": [
        {"name": "lob_annual", "title": bi("Einwohner und Gestorbene 1794–1804", "Inhabitants and deaths 1794–1804"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
                     col("deaths", "Gestorbene", "Deaths", "integer", "Personen"),
                     col("deaths_pct", "Gestorbene in Procent der Einwohner", "Deaths in per cent of the inhabitants", "number", "%")],
         "rows": annual, "source_refs": [ref("115", "b1", "r2-r12")]},
        {"name": "lob_classes", "title": bi("Gestorbene nach Kindern, Ledigen und Verheiratheten", "Deaths by children, unmarried and married persons"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("class", "Klasse", "Class", "string", note="Kinder (bis 14 Jahre) / Ledige / Verheirathete (und Verwitwete)"),
                     col("sex", "Geschlecht", "Sex", "string", note="Knaben/Mädchen bei den Kindern"),
                     col("deaths", "Gestorbene", "Deaths", "integer", "Personen")],
         "rows": classes, "source_refs": [ref("116", "b2", "r2-r12")]},
        {"name": "lob_ages", "title": bi("Gestorbene nach Altersklassen", "Deaths by age class"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("age_class", "Lebensalter (Jahre)", "Age (years)", "string"),
                     col("deaths", "Gestorbene", "Deaths", "integer", "Personen", note="„—“ der Vorlage als 0")],
         "rows": ages, "source_refs": [ref("116", "b4", "r2-r12")]},
        {"name": "lob_ages_mean", "title": bi("Altersklassen im Mittel 1794–1804", "Age classes, mean 1794–1804"),
         "columns": [col("age_class", "Lebensalter (Jahre)", "Age (years)", "string"),
                     col("deaths_mean", "Gestorbene (Jahresmittel)", "Deaths (annual mean)", "number", "Personen"),
                     col("share_pct", "Anteil an allen Gestorbenen", "Share of all deaths", "number", "%", derived=True, note="Mittel der Klasse : Summe der Mittel")],
         "rows": ages_mean, "source_refs": [ref("116", "b4", "t13")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "lob_annual",
         "title": bi("Gestorbene in Procent der Einwohner", "Deaths as a percentage of the inhabitants"),
         "caption": bi(f"Bezirk Lobenstein-Ebersdorf, 1794–1804. Die gestrichelte Linie ist Brückners Mittel von {fde(mean_pct)} Procent; das Jahr 1800 ragt heraus.",
                       f"District of Lobenstein-Ebersdorf, 1794–1804. The dashed rule is Brückner's mean of {fen(mean_pct)} per cent; the year 1800 stands out."),
         "vegalite": {"height": 280,
                      "layer": [
                          {"mark": {"type": "line", "point": True},
                           "encoding": {
                               "x": YEAR_AX,
                               "y": {"field": "deaths_pct", "type": "quantitative", "title": bi("% der Einwohner", "% of inhabitants"), "scale": {"domain": [0, 7.5]}},
                               "tooltip": [tip("year", "Jahr", "Year"), tip("inhabitants", "Einwohner", "Inhabitants"), tip("deaths", "Gestorbene", "Deaths"),
                                           tip("deaths_pct", "% der Einwohner", "% of inhabitants", ".2f")]}},
                          {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": mean_pct}}}]}},
        {"id": "c2", "dataset": "lob_classes",
         "title": bi("Gestorbene nach Kindern, Ledigen und Verheiratheten", "Deaths by children, unmarried and married persons"),
         "caption": bi("Beide Geschlechter zusammen, Personen je Jahr. Kinder sind alle Gestorbenen bis zum 14. Lebensjahr; „Verheirathete“ schließen Verwitwete ein.",
                       "Both sexes combined, people per year. Children are all who died up to the age of 14; “married” includes widowed persons."),
         "vegalite": {"height": 300, "mark": "bar",
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "deaths", "type": "quantitative", "title": bi("Gestorbene", "deaths"), "stack": "zero"},
                          "color": {"field": "class", "type": "nominal", "title": None, "scale": {"domain": ["Kinder", "Ledige", "Verheirathete"]},
                                    "legend": {"labelLimit": 300, "labelExpr": lab_expr2({"Kinder": "Kinder (bis 14 Jahre)", "Ledige": "Ledige", "Verheirathete": "Verheiratete und Verwitwete"},
                                                                                         {"Kinder": "Children (to age 14)", "Ledige": "Unmarried", "Verheirathete": "Married and widowed"})}},
                          "order": {"field": "class", "type": "nominal", "sort": "descending"},
                          "tooltip": [tip("year", "Jahr", "Year"), tip("class", "Klasse", "Class"), tip("sex", "Geschlecht", "Sex"), tip("deaths", "Gestorbene", "Deaths")]}}},
        {"id": "c3", "dataset": "lob_ages",
         "title": bi("Gestorbene nach Altersklasse und Jahr", "Deaths by age class and year"),
         "caption": bi("Jede Zelle ist die Zahl der Gestorbenen einer zehnjährigen Altersklasse in einem Jahr (Farbskala nach Quadratwurzel). Die Kinder bis zehn Jahre dominieren, vor allem 1800.",
                       "Each cell is the number of deaths in a ten-year age class in one year (colour scale by square root). Children under ten dominate, above all in 1800."),
         "vegalite": {"height": 340, "mark": "rect",
                      "encoding": {
                          "x": {"field": "age_class", "type": "ordinal", "sort": AGES, "title": bi("Lebensalter (Jahre)", "Age (years)"), "axis": {"labelAngle": 0}},
                          "y": {"field": "year", "type": "ordinal", "title": YEAR},
                          "color": {"field": "deaths", "type": "quantitative", "title": bi("Gestorbene", "Deaths"), "scale": {"type": "sqrt"}},
                          "tooltip": [tip("year", "Jahr", "Year"), tip("age_class", "Lebensalter (Jahre)", "Age (years)"), tip("deaths", "Gestorbene", "Deaths")]}}},
        {"id": "c4", "dataset": "lob_ages_mean",
         "title": bi("Altersverteilung der Gestorbenen", "Age distribution of the deaths"),
         "caption": bi("Anteil der zehnjährigen Altersklassen an allen Gestorbenen, Mittel 1794–1804 (nach den gedruckten Jahresmitteln).",
                       "Share of the ten-year age classes in all deaths, mean 1794–1804 (from the printed annual means)."),
         "vegalite": {"height": 260, "mark": "bar",
                      "encoding": {
                          "x": {"field": "age_class", "type": "ordinal", "sort": AGES, "title": bi("Lebensalter (Jahre)", "Age (years)"), "axis": {"labelAngle": 0}},
                          "y": {"field": "share_pct", "type": "quantitative", "title": bi("% der Gestorbenen", "% of deaths")},
                          "tooltip": [tip("age_class", "Lebensalter (Jahre)", "Age (years)"), tip("deaths_mean", "Gestorbene (Jahresmittel)", "Deaths (annual mean)", ".2f"),
                                      tip("share_pct", "% der Gestorbenen", "% of deaths", ".1f")]}}},
    ],
    "transcription_issues": [
        {"page": "116", "block": "b2", "cell": "r3c9", "transcribed": "6,49", "facsimile": "6,49", "checked_facsimile": True,
         "note": "1795, unmarried: (12+17)/440 = 6,59 %; printed 6,49. Printer's error in the original."},
        {"page": "116", "block": "b4", "cell": "r10", "transcribed": "252 9 24 24 23 39 63 40 10 —", "facsimile": "252 9 24 24 23 39 63 40 10 —", "checked_facsimile": True,
         "note": "1802: age classes sum to 484 while 492 deaths are given in the other tables; 1803: 429 against 426. As printed."},
    ],
    "keywords": {"de": ["Sterblichkeit", "Pocken", "Kindersterblichkeit", "Altersklassen", "Lobenstein", "Ebersdorf", "Intelligenzblatt", "Sterbefälle 1800"],
                 "en": ["mortality", "smallpox", "child mortality", "age classes", "Lobenstein", "Ebersdorf", "Intelligenzblatt", "deaths 1800"]},
    "related": ["bevoelkerung-sterblichkeit-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
