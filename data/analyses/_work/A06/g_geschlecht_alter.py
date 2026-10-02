"""A06 / analysis 7: sex and age structure (over/under 14) 1834-1867 by district and town/country (pp. 91-92, 99-100)."""
from common import *

# ------------------------------------------------ districts (p. 91 b4, p. 92 b1)
g91, g92 = grid("91", "b4"), grid("92", "b1")
blocks = {"Gera": g91[2:17], "Schleiz": g91[18:32], "Lobenstein-Ebersdorf": g92[4:19], "Fürstenthum": g92[20:34]}
dist_rows = []
for d, rs in blocks.items():
    for r in rs:
        if r[2] == "—":
            continue
        y = int(r[0])
        om, of, um, uf = integer(r[2]), integer(r[3]), integer(r[5]), integer(r[6])
        tm, tf = integer(r[8]), integer(r[9])
        assert om + um == tm and of + uf == tf, (d, y)
        under = um + uf
        total = tm + tf
        dist_rows.append([d, y, om, of, um, uf, tm, tf, round(under / total * 100, 2), round(tf / tm * 100, 1)])

# ------------------------------------------------ urban / rural (p. 99 b3)
g99 = grid("99", "b3")
ur_rows = []
for r in g99[3:]:
    y = int(r[0])
    v = [integer(x) for x in r[1:]]
    for area, o in (("Städte", 0), ("Landorte", 4)):
        om, of, um, uf = v[o:o + 4]
        total = om + of + um + uf
        ur_rows.append([area, y, om, of, um, uf, round((um + uf) / total * 100, 2), round(of / om * 100, 1), round(uf / um * 100, 1),
                        round((of + uf) / (om + um) * 100, 1)])

# ------------------------------------------------ printed composition (p. 100 b2)
g100 = grid("100", "b2")
comp = []
labels = {3: ("Städte", "1867"), 4: ("Städte", "Durchschnitt 1837–1867"),
          6: ("Landorte", "1867"), 7: ("Landorte", "Durchschnitt 1837–1867"),
          9: ("Fürstenthum", "1867"), 10: ("Fürstenthum", "Durchschnitt 1837–1867")}
CLS = ["over14_m", "over14_f", "under14_m", "under14_f"]
for idx, (area, per) in labels.items():
    r = g100[idx]
    v = [num(x) for x in r[1:]]
    # v: over14 m, f, zus, under14 m, f, zus, total m, f
    parts = [v[0], v[1], v[3], v[4]]
    assert abs(sum(parts) - 100) < 0.02, (area, per, sum(parts))
    assert abs(v[0] + v[1] - v[2]) < 0.02 and abs(v[3] + v[4] - v[5]) < 0.02
    for c, p in zip(CLS, parts):
        comp.append([area, per, c, p])

# check: printed 1867 composition = computed from p. 99; printed average = mean of the 11 census years
UR = {(r[0], r[1]): r for r in ur_rows}
for area in ("Städte", "Landorte"):
    r = UR[(area, 1867)]
    tot = r[2] + r[3] + r[4] + r[5]
    comp_calc = [round(x / tot * 100, 2) for x in r[2:6]]
    printed = [c[3] for c in comp if c[0] == area and c[1] == "1867"]
    print(area, "1867 computed", comp_calc, "printed", printed)
    avg = []
    for k in range(4):
        vals = []
        for y in range(1837, 1868, 3):
            rr = UR[(area, y)]
            t = rr[2] + rr[3] + rr[4] + rr[5]
            vals.append(rr[2 + k] / t * 100)
        avg.append(round(sum(vals) / len(vals), 2))
    print(area, "avg computed", avg, "printed", [c[3] for c in comp if c[0] == area and c[1].startswith("Durch")])

# ------------------------------------------------ prose numbers
DR = {(r[0], r[1]): r for r in dist_rows}
sr67 = {d: DR[(d, 1867)][9] for d in DIST_KEYS}
sr37 = {d: DR[(d, 1837)][9] for d in DIST_KEYS}
print(sr37, sr67)
u67, r67 = UR[("Städte", 1867)], UR[("Landorte", 1867)]
u37, r37 = UR[("Städte", 1837)], UR[("Landorte", 1837)]
sh37 = DR[("Fürstenthum", 1837)][8]
sh67 = DR[("Fürstenthum", 1867)][8]
print(sh37, sh67, u67[6], r67[6], u37[6], r37[6])
print("women/100 men >14 urban", [UR[("Städte", y)][7] for y in range(1837, 1868, 3)])
print("women/100 men >14 rural", [UR[("Landorte", y)][7] for y in range(1837, 1868, 3)])
print("girls/100 boys urban", [UR[("Städte", y)][8] for y in range(1837, 1868, 3)])
print("girls/100 boys rural", [UR[("Landorte", y)][8] for y in range(1837, 1868, 3)])
over_u = [UR[("Städte", y)][7] for y in range(1837, 1868, 3)]
over_r = [UR[("Landorte", y)][7] for y in range(1837, 1868, 3)]
un_u = [UR[("Städte", y)][8] for y in range(1837, 1868, 3)]
un_r = [UR[("Landorte", y)][8] for y in range(1837, 1868, 3)]
avg = lambda l: sum(l) / len(l)
print(avg(over_u), avg(over_r), avg(un_u), avg(un_r))
sh_u = [UR[("Städte", y)][6] for y in range(1837, 1868, 3)]
sh_r = [UR[("Landorte", y)][6] for y in range(1837, 1868, 3)]
print(min(sh_u), max(sh_u), min(sh_r), max(sh_r))
girls_gt_boys_rural = [y for y in range(1837, 1868, 3) if UR[("Landorte", y)][4] < UR[("Landorte", y)][5]]
print("rural years with more girls than boys:", girls_gt_boys_rural)
boys_urban_more = [y for y in range(1837, 1868, 3) if UR[("Städte", y)][4] > UR[("Städte", y)][5]]
print("urban years with more boys:", boys_urban_more)

ana = {
    "id": "bevoelkerung-geschlecht-alter-1834-1867",
    "title": {"de": "Geschlecht und Alter der Bevölkerung 1834–1867", "en": "Sex and age structure of the population, 1834–1867"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("91", "b4", "r6-r17"), ("91", "b4", "r21-r32"), ("92", "b1", "r9-r19"), ("92", "b1", "r24-r34"), ("99", "b3", "r4-r14"), ("100", "b2", "r4-r11"), ("100", "b3")),
    "summary": {
        "de": f"Brückner gliedert die Bevölkerung seit 1834 nach Geschlecht und nach dem Alter unter und über 14 Jahren, für die Landrathsbezirke und, getrennt nach Stadt und Land, für das ganze Fürstenthum. Im Fürstenthum überwiegen in allen Zählungen die Frauen, am stärksten in Lobenstein-Ebersdorf (1867: {de(sr67['Lobenstein-Ebersdorf'],0)} Frauen auf 100 Männer); auf dem Land ist der Frauenüberschuss bei den Erwachsenen größer, der Kinderanteil höher als in den Städten.",
        "en": f"Brückner divides the population since 1834 by sex and by age under and over 14, for the districts and, separated into town and country, for the whole principality. In the principality women outnumber men in every count, most strongly in Lobenstein-Ebersdorf (1867: {en(sr67['Lobenstein-Ebersdorf'],0)} women per 100 men); in the countryside the surplus of women among adults is larger and the share of children higher than in the towns.",
    },
    "method": {
        "de": "Übernommen wurden die Altersklassen über und unter 14 Jahren nach Geschlecht für die Bezirke (S. 91–92, ab 1834), die gleiche Gliederung für Städte und Landorte des Fürstenthums 1837–1867 (S. 99) und Brückners Prozentverhältnisse (S. 100). Abgeleitet wurden der Anteil der unter 14-Jährigen an der Gesamtbevölkerung, die Zahl der Frauen auf 100 Männer (gesamt und über 14 Jahre) und der Mädchen auf 100 Knaben (unter 14 Jahre). Die gedruckten Prozentzahlen für 1867 stimmen mit den aus S. 99 berechneten überein; Brückners »Durchschnitt von 1837–1867« entspricht für die Landorte und das Fürstenthum dem einfachen Mittel der elf Zählungen, für die Städte nicht (gedruckt 34,17 / 34,76 / 15,41 / 15,66, aus S. 99 errechnet 34,36 / 35,14 / 15,33 / 15,18). Die Summen von Stadt und Land stimmen für alle Jahre außer 1864 mit den Zahlen für das Fürstenthum auf S. 92 überein.",
        "en": "Taken over are the age classes over and under 14 by sex for the districts (pp. 91–92, from 1834), the same breakdown for the towns and rural places of the principality 1837–1867 (p. 99) and Brückner's percentage proportions (p. 100). Derived are the share of under-14s in the total population, the number of women per 100 men (overall and over 14) and of girls per 100 boys (under 14). The printed percentages for 1867 agree with those computed from p. 99; Brückner's “average of 1837–1867” equals the simple mean of the eleven counts for the rural places and the principality but not for the towns (printed 34.17 / 34.76 / 15.41 / 15.66, computed from p. 99 34.36 / 35.14 / 15.33 / 15.18). The sums of town and country agree with the figures for the principality on p. 92 for all years except 1864.",
    },
    "findings": [
        {"de": f"Auf 100 Männer kommen 1867 im Fürstenthum {de(sr67['Fürstenthum'],1)} Frauen; in Lobenstein-Ebersdorf {de(sr67['Lobenstein-Ebersdorf'],1)} (1837: {de(sr37['Lobenstein-Ebersdorf'],1)}), in Schleiz {de(sr67['Schleiz'],1)}, in Gera {de(sr67['Gera'],1)} (1837: {de(sr37['Gera'],1)}). Brückner führt den Frauenüberschuss auf stärkere Auswanderung und rascheres Sterben der Männer zurück.",
         "en": f"In 1867 there are {en(sr67['Fürstenthum'],1)} women per 100 men in the principality; {en(sr67['Lobenstein-Ebersdorf'],1)} in Lobenstein-Ebersdorf (1837: {en(sr37['Lobenstein-Ebersdorf'],1)}), {en(sr67['Schleiz'],1)} in Schleiz and {en(sr67['Gera'],1)} in Gera (1837: {en(sr37['Gera'],1)}). Brückner attributes the surplus of women to stronger emigration and faster mortality of men."},
        {"de": f"Bei den über 14-Jährigen kommen im Mittel der elf Zählungen {de(avg(over_u),1)} Frauen auf 100 Männer in den Städten, aber {de(avg(over_r),1)} auf dem Land; bei den unter 14-Jährigen sind es {de(avg(un_u),1)} Mädchen auf 100 Knaben in der Stadt und {de(avg(un_r),1)} auf dem Land, d. h. in beiden ein leichter Knabenüberschuss.",
         "en": f"For persons over 14 there are on average {en(avg(over_u),1)} women per 100 men in the towns but {en(avg(over_r),1)} in the countryside over the eleven counts; for under-14s the figures are {en(avg(un_u),1)} girls per 100 boys in town and {en(avg(un_r),1)} in the countryside, i.e. a slight surplus of boys in both."},
        {"de": f"Der Anteil der unter 14-Jährigen liegt auf dem Land mit {de(min(sh_r),1)}–{de(max(sh_r),1)} % (1867: {de(r67[6],2)} %) stets über dem in den Städten ({de(min(sh_u),1)}–{de(max(sh_u),1)} %, 1867: {de(u67[6],2)} %); Brückner erklärt das mit dem Zuzug der 14- bis 30-jährigen Landbewohner in die Städte und der geringeren Kindersterblichkeit auf dem Land.",
         "en": f"The share of under-14s in the countryside, {en(min(sh_r),1)}–{en(max(sh_r),1)} % (1867: {en(r67[6],2)} %), is always higher than in the towns ({en(min(sh_u),1)}–{en(max(sh_u),1)} %, 1867: {en(u67[6],2)} %); Brückner explains this by the move of 14- to 30-year-old country people to the towns and by lower child mortality in the countryside."},
        {"de": f"Im Fürstenthum insgesamt stieg der Anteil der Kinder unter 14 Jahren von {de(sh37,1)} % (1837) auf {de(sh67,1)} % (1867).",
         "en": f"In the principality as a whole the share of children under 14 rose from {en(sh37,1)} % (1837) to {en(sh67,1)} % (1867)."},
    ],
    "caveats": [
        {"de": "Die Zeile 1864 der Stadt/Land-Tabelle (S. 99) summiert sich zu 86 508 Personen, die Zeile für das Fürstenthum (S. 92) zu 86 472; die Altersklassen weichen um bis zu 70 Personen ab (Faksimile geprüft, so gedruckt). Weitere Druckfehler im Original: Summe der über 14-Jährigen Gera 1834 (18 698 statt 18 693), Fürstenthum 1858 (54 758 statt 54 753) und 1867 (58 720 statt 58 725). Die berechneten Größen benutzen die Einzelwerte.",
         "en": "The 1864 row of the town/country table (p. 99) adds up to 86,508 persons, the row for the principality (p. 92) to 86,472; the age classes differ by up to 70 persons (checked against the facsimile; printed so). Further misprints in the original: sum of over-14s Gera 1834 (18,698 instead of 18,693), principality 1858 (54,758 instead of 54,753) and 1867 (58,720 instead of 58,725). The derived quantities use the individual values."},
        {"de": "Die gedruckte Durchschnittszeile für die Städte (S. 100) lässt sich nicht aus den Zählungen von S. 99 reproduzieren (z. B. Frauen über 14: gedruckt 34,76 %, errechnet 35,14 %), während die Zeilen für das Land und das Fürstenthum stimmen; Transkription und Faksimile stimmen überein. Im Diagramm zur Zusammensetzung sind die gedruckten Werte wiedergegeben.",
         "en": "The printed average row for the towns (p. 100) cannot be reproduced from the counts of p. 99 (e.g. women over 14: printed 34.76 %, computed 35.14 %), whereas the rows for the countryside and the principality agree; transcription and facsimile agree. The chart of the composition reproduces the printed values."},
        {"de": "Die Altersgrenze 14 Jahre trennt Kinder von Erwachsenen nach Brückners Einteilung; die Zählungen stammen aus verschiedenen Jahren im Abstand von drei Jahren (1837, 1840, … 1867), die Bezirke zusätzlich 1834. Die starke Lobenstein-Ebersdorfer Frauenzahl hängt mit der Auswanderung zusammen (siehe die Auswertung zum Wanderungssaldo).",
         "en": "The age limit of 14 years separates children from adults according to Brückner's division; the counts come from different years three years apart (1837, 1840, … 1867), the districts also 1834. The high number of women in Lobenstein-Ebersdorf is connected with emigration (see the analysis of the migration balance)."},
    ],
    "datasets": [
        {"name": "districts", "title": {"de": "Alter und Geschlecht nach Bezirken", "en": "Age and sex by district"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("over14_m", "Über 14 Jahre, männlich", "Over 14, male", "integer", "Personen"),
             col("over14_f", "Über 14 Jahre, weiblich", "Over 14, female", "integer", "Personen"),
             col("under14_m", "Unter 14 Jahre, männlich", "Under 14, male", "integer", "Personen"),
             col("under14_f", "Unter 14 Jahre, weiblich", "Under 14, female", "integer", "Personen"),
             col("male", "Gesamtbewohner männlich", "Total male", "integer", "Personen"),
             col("female", "Gesamtbewohner weiblich", "Total female", "integer", "Personen"),
             col("share_under14", "Anteil der unter 14-Jährigen", "Share of under-14s", "number", "%", True),
             col("women_per_100_men", "Frauen auf 100 Männer", "Women per 100 men", "number", None, True),
         ],
         "rows": dist_rows, "source_refs": refs(("91", "b4", "r6-r17"), ("91", "b4", "r21-r32"), ("92", "b1", "r9-r19"), ("92", "b1", "r24-r34"))},
        {"name": "urban_rural", "title": {"de": "Alter und Geschlecht in Stadt und Land (Fürstenthum)", "en": "Age and sex in town and country (principality)"},
         "columns": [
             col("area", "Siedlungsart", "Settlement type", "string", None, False, "Städte oder Landorte"),
             col("year", "Jahr", "Year", "integer"),
             col("over14_m", "Über 14 Jahre, männlich", "Over 14, male", "integer", "Personen"),
             col("over14_f", "Über 14 Jahre, weiblich", "Over 14, female", "integer", "Personen"),
             col("under14_m", "Unter 14 Jahre, männlich", "Under 14, male", "integer", "Personen"),
             col("under14_f", "Unter 14 Jahre, weiblich", "Under 14, female", "integer", "Personen"),
             col("share_under14", "Anteil der unter 14-Jährigen", "Share of under-14s", "number", "%", True),
             col("women_per_100_men_over14", "Frauen auf 100 Männer (über 14)", "Women per 100 men (over 14)", "number", None, True),
             col("girls_per_100_boys_under14", "Mädchen auf 100 Knaben (unter 14)", "Girls per 100 boys (under 14)", "number", None, True),
             col("females_per_100_males", "Frauen auf 100 Männer (alle)", "Females per 100 males (all)", "number", None, True),
         ],
         "rows": ur_rows, "source_refs": refs(("99", "b3", "r4-r14"))},
        {"name": "composition", "title": {"de": "Zusammensetzung nach Brückner (Procentverhältnisse)", "en": "Composition according to Brückner (percentage proportions)"},
         "columns": [
             col("area", "Siedlungsart", "Settlement type", "string"),
             col("period", "Jahr/Zeitraum", "Year/period", "string"),
             col("group", "Gruppe", "Group", "string", None, True, "over14_m, over14_f, under14_m, under14_f"),
             col("percent", "Anteil an der Gesamtbevölkerung", "Share of the total population", "number", "%"),
         ],
         "rows": comp, "source_refs": refs(("100", "b2", "r4-r11"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "districts",
         "title": {"de": "Frauen auf 100 Männer nach Bezirken", "en": "Women per 100 men by district"},
         "caption": {"de": "Zahl der weiblichen Einwohner auf 100 männliche (alle Altersklassen) nach den gedruckten Zählungen; die gestrichelte Linie bei 100 markiert Gleichstand. In Lobenstein-Ebersdorf ist der Frauenüberschuss am größten.",
                     "en": "Number of female inhabitants per 100 male (all ages) according to the printed counts; the dashed rule at 100 marks parity. The surplus of women is largest in Lobenstein-Ebersdorf."},
         "vegalite": {
             "height": 320,
             "transform": [DIST_TRANSFORM],
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                      "y": {"field": "women_per_100_men", "type": "quantitative", "title": {"de": "Frauen auf 100 Männer", "en": "Women per 100 men"}, "scale": {"zero": False, "domain": [98, 110]}},
                      "color": color_dist(),
                      "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"),
                                  tt_fmt("women_per_100_men", "Frauen auf 100 Männer", "Women per 100 men", ".1f"),
                                  tt_fmt("male", "Männer", "Men", ","), tt_fmt("female", "Frauen", "Women", ",")]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 100}}},
             ]}},
        {"id": "c2", "dataset": "urban_rural",
         "title": {"de": "Frauen auf 100 Männer in Stadt und Land, nach Altersklasse", "en": "Women per 100 men in town and country, by age class"},
         "caption": {"de": "Bei den über 14-Jährigen (durchgezogen) überwiegen die Frauen, auf dem Land stärker; bei den unter 14-Jährigen (gestrichelt) liegt die Zahl der Mädchen auf 100 Knaben meist knapp unter 100.",
                     "en": "Among persons over 14 (solid) women predominate, more so in the countryside; among under-14s (dashed) the number of girls per 100 boys is mostly just below 100."},
         "vegalite": {
             "height": 320,
             "transform": [{"fold": ["women_per_100_men_over14", "girls_per_100_boys_under14"], "as": ["age_class", "ratio"]}],
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                      "y": {"field": "ratio", "type": "quantitative", "title": {"de": "Frauen/Mädchen auf 100 Männer/Knaben", "en": "Women/girls per 100 men/boys"}, "scale": {"zero": False, "domain": [94, 110]}},
                      "color": {"field": "area", "type": "nominal", "scale": {"domain": ["Städte", "Landorte"]},
                                "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'Towns' : 'Rural places'"}}},
                      "strokeDash": {"field": "age_class", "type": "nominal", "scale": {"domain": ["women_per_100_men_over14", "girls_per_100_boys_under14"], "range": [[1, 0], [5, 4]]},
                                     "legend": {"title": None, "labelLimit": 300, "labelExpr": {"de": "datum.label == 'women_per_100_men_over14' ? 'über 14 Jahre' : 'unter 14 Jahre'", "en": "datum.label == 'women_per_100_men_over14' ? 'over 14' : 'under 14'"}}},
                      "tooltip": [tt("area", "Siedlungsart", "Settlement"), tt("year", "Jahr", "Year"),
                                  tt_fmt("women_per_100_men_over14", "Frauen auf 100 Männer (über 14)", "Women per 100 men (over 14)", ".1f"),
                                  tt_fmt("girls_per_100_boys_under14", "Mädchen auf 100 Knaben (unter 14)", "Girls per 100 boys (under 14)", ".1f")]}},
                 {"mark": {"type": "rule", "strokeDash": [2, 3]}, "encoding": {"y": {"datum": 100}}},
             ]}},
        {"id": "c3", "dataset": "urban_rural",
         "title": {"de": "Anteil der unter 14-Jährigen in Stadt und Land", "en": "Share of under-14s in town and country"},
         "caption": {"de": "Kinder unter 14 Jahren in Prozent der jeweiligen Gesamtbevölkerung (berechnet). Auf dem Land ist der Kinderanteil in jedem Jahr höher als in den Städten.",
                     "en": "Children under 14 as a per cent of the respective total population (computed). In every year the share of children is higher in the countryside than in the towns."},
         "vegalite": {
             "height": 300,
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": YEAR, "axis": {"labelAngle": 0}},
                 "y": {"field": "share_under14", "type": "quantitative", "title": {"de": "Unter 14-Jährige (%)", "en": "Under-14s (%)"}, "scale": {"zero": False}},
                 "color": {"field": "area", "type": "nominal", "scale": {"domain": ["Städte", "Landorte"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'Towns' : 'Rural places'"}}},
                 "tooltip": [tt("area", "Siedlungsart", "Settlement"), tt("year", "Jahr", "Year"), tt_fmt("share_under14", "Anteil unter 14 (%)", "Under-14 share (%)", ".2f")]}}},
        {"id": "c4", "dataset": "composition",
         "title": {"de": "Zusammensetzung der Bevölkerung nach Geschlecht und Alter", "en": "Composition of the population by sex and age"},
         "caption": {"de": "Anteile in Prozent der Gesamtbevölkerung nach Brückners Procentverhältnissen (S. 100): 1867 und Durchschnitt der Zählungen 1837–1867.",
                     "en": "Shares in per cent of the total population according to Brückner's percentage proportions (p. 100): 1867 and mean of the counts 1837–1867."},
         "vegalite": {
             "height": 300,
             "transform": [{"calculate": "datum.period == '1867' ? datum.area + ' 1867' : datum.area + ' Ø 1837–67'", "as": "row_key"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "row_key", "type": "nominal", "title": None, "sort": ["Städte 1867", "Städte Ø 1837–67", "Landorte 1867", "Landorte Ø 1837–67", "Fürstenthum 1867", "Fürstenthum Ø 1837–67"],
                       "axis": {"labelLimit": 240, "labelExpr": {"de": "datum.label", "en": "replace(replace(replace(datum.label, 'Städte', 'Towns'), 'Landorte', 'Rural places'), 'Fürstenthum', 'Principality')"}}},
                 "x": {"field": "percent", "type": "quantitative", "title": {"de": "Anteil an der Gesamtbevölkerung (%)", "en": "Share of the total population (%)"}, "scale": {"domain": [0, 100]}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["over14_m", "over14_f", "under14_m", "under14_f"]},
                           "legend": {"title": None, "labelLimit": 260, "columns": 2, "labelExpr": {"de": "datum.label == 'over14_m' ? 'Männer über 14' : datum.label == 'over14_f' ? 'Frauen über 14' : datum.label == 'under14_m' ? 'Knaben unter 14' : 'Mädchen unter 14'",
                                                                                      "en": "datum.label == 'over14_m' ? 'Men over 14' : datum.label == 'over14_f' ? 'Women over 14' : datum.label == 'under14_m' ? 'Boys under 14' : 'Girls under 14'"}}},
                 "tooltip": [tt("area", "Siedlungsart", "Settlement"), tt("period", "Jahr/Zeitraum", "Year/period"), tt("group", "Gruppe", "Group"), tt_fmt("percent", "Anteil (%)", "Share (%)", ".2f")]}}},
    ],
    "keywords": {"de": ["Geschlechterverhältnis", "Frauenüberschuss", "Altersstruktur", "Kinder unter 14", "Stadt und Land", "Altersklassen", "Männer", "Frauen", "Knaben", "Mädchen"],
                 "en": ["sex ratio", "surplus of women", "age structure", "children under 14", "town and country", "age classes", "men", "women", "boys", "girls"]},
    "related": ["bevoelkerung-entwicklung-1647-1867", "bevoelkerung-altersaufbau-1864", "bevoelkerung-geburtensaldo-wanderung-1859-1867"],
}
write(ana)
