"""A06 / analysis 9: marital status 1864, married persons by age, age difference between spouses (pp. 103-104)."""
from common import *

STATUS = ["unverheiratet", "verheiratet", "verwitwet", "geschieden"]
STATUS_EN = {"unverheiratet": "unmarried", "verheiratet": "married", "verwitwet": "widowed", "geschieden": "divorced"}

# ------------------------------------------------ counts (p. 103 b3)
g = grid("103", "b3")
AREAS = [("Gera", "Städte"), ("Gera", "Dörfer"), ("Gera", "Landestheil"),
         ("Schleiz", "Städte"), ("Schleiz", "Dörfer"), ("Schleiz", "Landestheil"),
         ("Lobenstein-Ebersdorf", "Städte"), ("Lobenstein-Ebersdorf", "Dörfer"), ("Lobenstein-Ebersdorf", "Landestheil"),
         ("Fürstenthum", "Städte"), ("Fürstenthum", "Dörfer"), ("Fürstenthum", "insgesamt")]
data_rows = g[2:14]
assert len(data_rows) == 12
counts = []
C = {}
for (d, s), r in zip(AREAS, data_rows):
    v = [integer(x) for x in r[1:]]
    for si, st in enumerate(STATUS):
        m, w, z = v[3 * si:3 * si + 3]
        counts.append([d, s, "männlich", st, m])
        counts.append([d, s, "weiblich", st, w])
        C[(d, s, st)] = (m, w, z)
# internal consistency: print mismatches (print errors)
for (d, s), r in zip(AREAS, data_rows):
    v = [integer(x) for x in r[1:]]
    for si, st in enumerate(STATUS):
        m, w, z = v[3 * si:3 * si + 3]
        if m + w != z:
            print("printed sum mismatch", d, s, st, m, w, z, "->", m + w)
for d in ("Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstenthum"):
    for st in STATUS:
        for k, sx in ((0, "m"), (1, "w")):
            a = C[(d, "Städte", st)][k] + C[(d, "Dörfer", st)][k]
            b = C[(d, "Landestheil" if d != "Fürstenthum" else "insgesamt", st)][k]
            assert a == b, (d, st, sx, a, b)
for st in STATUS:
    for k in (0, 1):
        s = sum(C[(d, "Landestheil", st)][k] for d in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"))
        assert s == C[("Fürstenthum", "insgesamt", st)][k], (st, k)
print("counts: Stadt+Dörfer = Landestheil, districts = Fürstenthum: OK")

# ------------------------------------------------ per 1000 (p. 103 b5)
g5 = grid("103", "b5")
REG = ["Gera (Stadt)", "Gera (Dörfer)", "Gera (Landestheil)", "Schleiz (Städte)", "Schleiz (Dörfer)", "Schleiz (Landestheil)",
       "Lobenstein-Ebersdorf (Städte)", "Lobenstein-Ebersdorf (Dörfer)", "Lobenstein-Ebersdorf (Landestheil)",
       "Fürstenthum (Städte)", "Fürstenthum (Dörfer)", "Fürstenthum (insgesamt)",
       "S.-Weimar", "S.-Meiningen", "S.-Altenburg", "Schwarzburg-Rudolstadt", "Preußen", "Württemberg"]
rows5 = g5[2:20]
assert len(rows5) == 18, len(rows5)
GROUPS = ["Männer", "Frauen", "Einwohner"]
mille = []
PM = {}
for reg, r in zip(REG, rows5):
    v = [num(x) for x in r[1:]]
    rtype = "Reuß j. L." if reg.startswith(("Gera", "Schleiz", "Lobenstein", "Fürstenthum")) else "Vergleich"
    for gi, grp in enumerate(GROUPS):
        for si, st in enumerate(STATUS):
            mille.append([reg, rtype, grp, st, v[4 * gi + si]])
            PM[(reg, grp, st)] = v[4 * gi + si]
# check recomputation for the 12 Reuss rows
for (d, s), reg in zip(AREAS, REG[:12]):
    for gi, grp in enumerate(("Männer", "Frauen")):
        tot = sum(C[(d, s, st)][gi] for st in STATUS)
        for st in STATUS:
            comp = C[(d, s, st)][gi] / tot * 1000
            assert abs(comp - PM[(reg, grp, st)]) < 0.15, (reg, grp, st, comp, PM[(reg, grp, st)])
print("per-1000 table agrees with counts (±0.1)")

# ------------------------------------------------ married by age (p. 104 b3)
g104 = grid("104", "b3")
AGE = ["unter 30", "30–45", "45–60", "über 60"]
absr = {"Städte": g104[2], "Dörfer": g104[3], "Fürstenthum": g104[4]}
pctr = {"Städte": g104[6], "Dörfer": g104[7], "Fürstenthum": g104[8]}
married_age = []
couples = {}
for area in ("Städte", "Dörfer", "Fürstenthum"):
    a, p = absr[area], pctr[area]
    couples[area] = integer(a[1])
    mm = [integer(x) for x in a[2:6]]
    ww = [integer(x) for x in a[6:10]]
    assert sum(mm) == couples[area] and sum(ww) == couples[area], area
    pm = [num(x) for x in p[2:6]]
    pw = [num(x) for x in p[6:10]]
    for i, ac in enumerate(AGE):
        married_age.append([area, "männlich", ac, mm[i], pm[i]])
        married_age.append([area, "weiblich", ac, ww[i], pw[i]])
# Städte + Dörfer = Fürstenthum
for k in range(8):
    pass
for sx in ("männlich", "weiblich"):
    for ac in AGE:
        s = sum(r[3] for r in married_age if r[0] != "Fürstenthum" and r[1] == sx and r[2] == ac)
        f = next(r[3] for r in married_age if r[0] == "Fürstenthum" and r[1] == sx and r[2] == ac)
        assert s == f
print("married by age: Städte + Dörfer = Fürstenthum: OK; couples", couples)

# ------------------------------------------------ spouse age difference (p. 104 b6)
g6 = grid("104", "b6")[1]
v = [num(x) for x in g6[1:]]
spouse = [
    ["Frau 3 Klassen älter", "Frau älter", 3, None, 1],
    ["Frau 2 Klassen älter", "Frau älter", 2, v[7], 2],
    ["Frau 1 Klasse älter", "Frau älter", 1, v[6], 3],
    ["Frau älter, gleiche Altersklasse", "Frau älter", 0, v[5], 4],
    ["Mann älter, gleiche Altersklasse", "Mann älter", 0, v[0], 5],
    ["Mann 1 Klasse älter", "Mann älter", 1, v[1], 6],
    ["Mann 2 Klassen älter", "Mann älter", 2, v[2], 7],
    ["Mann 3 Klassen älter", "Mann älter", 3, v[3], 8],
]
assert abs(sum(r[3] or 0 for r in spouse) - 1000) < 0.15
assert abs(v[4] - sum(x or 0 for x in v[0:4])) < 0.15 and abs(v[9] - sum(x or 0 for x in v[5:9])) < 0.15
SPOUSE_EN = {
    "Frau 3 Klassen älter": "Wife 3 classes older", "Frau 2 Klassen älter": "Wife 2 classes older", "Frau 1 Klasse älter": "Wife 1 class older",
    "Frau älter, gleiche Altersklasse": "Wife older, same age class", "Mann älter, gleiche Altersklasse": "Husband older, same age class",
    "Mann 1 Klasse älter": "Husband 1 class older", "Mann 2 Klassen älter": "Husband 2 classes older", "Mann 3 Klassen älter": "Husband 3 classes older"}
SPOUSE_TRANSFORM = relabel("category", "category_label", {k: (k, e) for k, e in SPOUSE_EN.items()})

# ------------------------------------------------ prose numbers
T = {st: tuple(C[("Fürstenthum", "insgesamt", st)][:2]) for st in STATUS}
pop_tot = sum(sum(T[st]) for st in STATUS)
PMr = lambda reg, grp, st: PM[(reg, grp, st)]
F_ = "Fürstenthum (insgesamt)"
wid_m, wid_w = T["verwitwet"]
div_m, div_w = T["geschieden"]
widow_ratio = wid_w / wid_m
print(pop_tot, T, widow_ratio)
mar_inh = {r: PM[(r, "Einwohner", "verheiratet")] for r in REG}
print({k: mar_inh[k] for k in REG})
div_st, div_dö = PM[("Fürstenthum (Städte)", "Einwohner", "geschieden")], PM[("Fürstenthum (Dörfer)", "Einwohner", "geschieden")]
wid_st, wid_dö = PM[("Fürstenthum (Städte)", "Einwohner", "verwitwet")], PM[("Fürstenthum (Dörfer)", "Einwohner", "verwitwet")]
MA = {(r[0], r[1], r[2]): r for r in married_age}
man_older = v[4]
woman_older = v[9]
same = v[0] + v[5]
big_diff = v[2] + v[3] + v[7]
print(man_older, woman_older, same)
wid_per_w = PM[(F_, "Frauen", "verwitwet")]
wid_per_m = PM[(F_, "Männer", "verwitwet")]

ana = {
    "id": "bevoelkerung-familienstand-ehen-1864",
    "title": {"de": "Familienstand und Ehen 1864", "en": "Marital status and marriages, 1864"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("103", "b3", "r3-r14"), ("103", "b5", "r3-r20"), ("104", "b1"), ("104", "b3", "r3-r9"), ("104", "b6", "r2"), ("104", "b4"), ("104", "b5")),
    "summary": {
        "de": f"Brückner gliedert die Bevölkerung des Fürstenthums 1864 nach dem Familienstand, getrennt nach Landestheilen, Städten und Dörfern, vergleicht mit sechs anderen Staaten und gibt die Verheiratheten nach Altersklassen sowie die Altersunterschiede der Ehepartner an. Von 1000 Einwohnern sind {de(PM[(F_,'Einwohner','unverheiratet')],0)} unverheiratet, {de(PM[(F_,'Einwohner','verheiratet')],0)} verheiratet, {de(PM[(F_,'Einwohner','verwitwet')],0)} verwitwet und {de(PM[(F_,'Einwohner','geschieden')],0)} geschieden; Witwen sind mehr als doppelt so häufig wie Witwer.",
        "en": f"Brückner classifies the population of the principality in 1864 by marital status, separated into districts, towns and villages, compares it with six other states, and gives the married by age class and the age differences of spouses. Of 1,000 inhabitants {en(PM[(F_,'Einwohner','unverheiratet')],0)} are unmarried, {en(PM[(F_,'Einwohner','verheiratet')],0)} married, {en(PM[(F_,'Einwohner','verwitwet')],0)} widowed and {en(PM[(F_,'Einwohner','geschieden')],0)} divorced; widows are more than twice as frequent as widowers.",
    },
    "method": {
        "de": "Übernommen wurden die Zählung des Familienstands 1864 (S. 103, Männer und Frauen je Landestheil, Städte, Dörfer), die Verhältniszahlen auf 1000 Männer, Frauen und Einwohner einschließlich der Vergleichsstaaten (S. 103), die Verheiratheten nach Altersklassen mit den gedruckten Prozentzahlen (S. 104) und die Ehen nach dem Altersunterschied der Partner auf 1000 Ehen (S. 104). Die Zählung wurde auf Männer und Frauen je Familienstand heruntergebrochen (die gedruckten »zus.«-Spalten wurden nicht übernommen, sondern lassen sich summieren). Kontrolle: Städte + Dörfer = Landestheil, die drei Landestheile = Fürstenthum, die Verhältniszahlen stimmen mit den Zählzahlen auf ±0,1 ‰ überein (alle 12 Reuß-Zeilen), die Altersunterschiede summieren sich zu 1000 ‰. Die Prozentzahlen der Verheiratheten nach Alter sind die gedruckten; der Nenner (Zahl der Personen der Altersklasse) ist nicht angegeben; Nachrechnung mit der Einzeljahrtabelle (S. 101) deutet darauf hin, dass für die Männer die Lebensjahre 25–30, 31–45, 46–60 und über 60, für die Frauen 17–30, 31–45, 46–60 und über 60 zugrunde liegen.",
        "en": "Taken over are the count of marital status in 1864 (p. 103, men and women per district, towns, villages), the proportions per 1,000 men, women and inhabitants including the comparison states (p. 103), the married by age class with the printed percentages (p. 104) and the marriages by age difference of the partners per 1,000 marriages (p. 104). The count was broken down to men and women per status (the printed “total” columns were not taken over since they can be summed). Checks: towns + villages = district, the three districts = principality, the proportions agree with the counts to ±0.1 ‰ (all 12 Reuss rows), the age differences add up to 1,000 ‰. The percentages of the married by age are the printed ones; the denominator (number of persons of the age class) is not stated; a recomputation with the single-year table (p. 101) suggests that for men the years of life 25–30, 31–45, 46–60 and over 60 are the basis, for women 17–30, 31–45, 46–60 and over 60.",
    },
    "findings": [
        {"de": f"1864 zählt das Fürstenthum {de(wid_m,0)} Witwer und {de(wid_w,0)} Witwen (Verhältnis 1 : {de(widow_ratio,1)}); auf 1000 Männer kommen {de(wid_per_m,1)} Verwitwete, auf 1000 Frauen {de(wid_per_w,1)}. Geschieden sind {de(div_m,0)} Männer und {de(div_w,0)} Frauen.",
         "en": f"In 1864 the principality counts {en(wid_m,0)} widowers and {en(wid_w,0)} widows (ratio 1 : {en(widow_ratio,1)}); per 1,000 men there are {en(wid_per_m,1)} widowed, per 1,000 women {en(wid_per_w,1)}. {en(div_m,0)} men and {en(div_w,0)} women are divorced."},
        {"de": f"Die Städte haben auf 1000 Einwohner mehr Geschiedene ({de(div_st,1)} gegen {de(div_dö,1)}) und Verwitwete ({de(wid_st,1)} gegen {de(wid_dö,1)}) und weniger Verheiratete ({de(PM[('Fürstenthum (Städte)','Einwohner','verheiratet')],1)} gegen {de(PM[('Fürstenthum (Dörfer)','Einwohner','verheiratet')],1)}) als die Dörfer.",
         "en": f"Per 1,000 inhabitants the towns have more divorced ({en(div_st,1)} against {en(div_dö,1)}) and widowed ({en(wid_st,1)} against {en(wid_dö,1)}) and fewer married ({en(PM[('Fürstenthum (Städte)','Einwohner','verheiratet')],1)} against {en(PM[('Fürstenthum (Dörfer)','Einwohner','verheiratet')],1)}) than the villages."},
        {"de": f"Unter den Landestheilen hat Schleiz die meisten Verheiratheten ({de(mar_inh['Schleiz (Landestheil)'],1)} ‰), Gera ({de(mar_inh['Gera (Landestheil)'],1)} ‰) liegt nahe am Landesmittel ({de(mar_inh[F_],1)} ‰), Lobenstein-Ebersdorf hat die wenigsten ({de(mar_inh['Lobenstein-Ebersdorf (Landestheil)'],1)} ‰). Im Vergleich der Staaten liegt Reuß j. L. zwischen S.-Weimar ({de(mar_inh['S.-Weimar'],1)}) und Württemberg ({de(mar_inh['Württemberg'],1)}).",
         "en": f"Among the districts Schleiz has the most married ({en(mar_inh['Schleiz (Landestheil)'],1)} ‰), Gera ({en(mar_inh['Gera (Landestheil)'],1)} ‰) is close to the national mean ({en(mar_inh[F_],1)} ‰), Lobenstein-Ebersdorf has the fewest ({en(mar_inh['Lobenstein-Ebersdorf (Landestheil)'],1)} ‰). In the comparison of states Reuss j. L. lies between Saxe-Weimar ({en(mar_inh['S.-Weimar'],1)}) and Württemberg ({en(mar_inh['Württemberg'],1)})."},
        {"de": f"Männer sind in jeder Altersklasse häufiger verheiratet als Frauen: unter 30 Jahren {de(MA[('Fürstenthum','männlich','unter 30')][4],1)} % gegen {de(MA[('Fürstenthum','weiblich','unter 30')][4],1)} %, über 60 Jahren {de(MA[('Fürstenthum','männlich','über 60')][4],1)} % gegen {de(MA[('Fürstenthum','weiblich','über 60')][4],1)} %; Brückner erklärt es mit der ungleichen Zahl der heiratsfähigen Geschlechter und damit, dass der Witwer leichter wieder heiratet als die Witwe.",
         "en": f"Men are more often married than women in every age class: under 30 {en(MA[('Fürstenthum','männlich','unter 30')][4],1)} % against {en(MA[('Fürstenthum','weiblich','unter 30')][4],1)} %, over 60 {en(MA[('Fürstenthum','männlich','über 60')][4],1)} % against {en(MA[('Fürstenthum','weiblich','über 60')][4],1)} %; Brückner explains this by the unequal number of the two sexes of marriageable age and by the fact that a widower remarries more easily than a widow."},
        {"de": f"In {de(man_older,1)} von 1000 Ehen ist der Mann in einer höheren Altersklasse oder (innerhalb derselben Klasse) älter, in {de(woman_older,1)} die Frau; Ehen innerhalb einer Altersklasse machen {de(same,1)} ‰ aus, Ehen mit zwei oder drei Klassen Unterschied zusammen nur {de(big_diff,1)} ‰.",
         "en": f"In {en(man_older,1)} of 1,000 marriages the husband belongs to a higher age class or is older within the same class, in {en(woman_older,1)} the wife; marriages within one age class make up {en(same,1)} ‰, marriages with a difference of two or three classes together only {en(big_diff,1)} ‰."},
    ],
    "caveats": [
        {"de": "Druckfehler im Original (Transkription und Faksimile stimmen überein): In der Zeile Lobenstein-Ebersdorf, Dörfer, steht für die Verheiratheten zusammen »5573«; 2 768 + 2 810 ergeben 5 578 (so auch die Summen 7 052 und 19 890 sowie die Gesamtzahl 17 887 auf S. 95). Die Auswertung nutzt nur die Zahlen für Männer und Frauen.",
         "en": "Misprint in the original (transcription and facsimile agree): in the row Lobenstein-Ebersdorf, villages, the married total is printed as “5573”; 2,768 + 2,810 make 5,578 (as do the totals 7,052 and 19,890 and the overall figure 17,887 on p. 95). The analysis uses only the figures for men and women."},
        {"de": "Die Zahl der verheirateten Männer (14 433) und Frauen (14 395) ist nicht gleich, obwohl jede Ehe einen Mann und eine Frau enthält; Ehepaare werden auf S. 104 mit 13 945 angegeben. Abwesende Ehepartner und Erfassungsunterschiede erklären die Abweichung vermutlich; Brückner äußert sich nicht dazu.",
         "en": "The numbers of married men (14,433) and married women (14,395) are not equal although every marriage includes one man and one woman; p. 104 gives 13,945 couples. Absent spouses and differences of recording probably explain the deviation; Brückner does not comment."},
        {"de": "Für die Vergleichsstaaten (S.-Weimar, S.-Meiningen, S.-Altenburg, Schwarzburg-Rudolstadt, Preußen, Württemberg) nennt Brückner weder Jahr noch Quelle; sie stammen vermutlich aus Hildebrands »Statistik Thüringens« (S. 104, Fußnote). Die Altersklassen der Ehepartner (S. 104, letzte Tabelle) sind nicht ausdrücklich definiert; vermutlich sind es die vier Klassen der vorangehenden Tabelle.",
         "en": "For the comparison states (Saxe-Weimar, Saxe-Meiningen, Saxe-Altenburg, Schwarzburg-Rudolstadt, Prussia, Württemberg) Brückner names neither year nor source; they probably come from Hildebrand's “Statistik Thüringens” (p. 104, footnote). The age classes of the spouses (p. 104, last table) are not explicitly defined; presumably they are the four classes of the preceding table."},
    ],
    "datasets": [
        {"name": "civil_counts", "title": {"de": "Familienstand 1864 nach Gebieten (Zählung)", "en": "Marital status in 1864 by area (count)"},
         "columns": [
             col("district", "Landestheil", "District", "string"),
             col("settlement", "Gebiet", "Area", "string", None, False, "Städte, Dörfer oder Landestheil/insgesamt"),
             col("sex", "Geschlecht", "Sex", "string"),
             col("status", "Familienstand", "Marital status", "string", None, False, "unverheiratet, verheiratet, verwitwet, geschieden"),
             col("persons", "Personen", "Persons", "integer", "Personen"),
         ],
         "rows": counts, "source_refs": refs(("103", "b3", "r3-r14"))},
        {"name": "civil_per_mille", "title": {"de": "Familienstand auf 1000 Männer, Frauen, Einwohner", "en": "Marital status per 1,000 men, women, inhabitants"},
         "columns": [
             col("region", "Gebiet", "Region", "string"),
             col("region_type", "Art", "Type", "string", None, True, "Reuß j. L. oder Vergleichsstaat (editorisch)"),
             col("group", "Bezugsgruppe", "Reference group", "string", None, False, "Männer, Frauen oder Einwohner"),
             col("status", "Familienstand", "Marital status", "string"),
             col("per_1000", "Auf 1000", "Per 1,000", "number", "‰"),
         ],
         "rows": mille, "source_refs": refs(("103", "b5", "r3-r20"))},
        {"name": "married_by_age", "title": {"de": "Verheirathete nach Altersklassen 1864", "en": "Married persons by age class, 1864"},
         "columns": [
             col("area", "Gebiet", "Area", "string"),
             col("sex", "Geschlecht", "Sex", "string"),
             col("age_class", "Altersklasse", "Age class", "string", None, False, "unter 30, 30–45, 45–60, über 60 Jahre"),
             col("married", "Verheirathete (absolut)", "Married (absolute)", "integer", "Personen"),
             col("share_pct", "Verheirathete (Prozent, gedruckt)", "Married (per cent, printed)", "number", "%"),
         ],
         "rows": married_age, "source_refs": refs(("104", "b3", "r3-r9"))},
        {"name": "spouse_age", "title": {"de": "Ehen nach dem Altersunterschied der Partner", "en": "Marriages by age difference of the partners"},
         "columns": [
             col("category", "Kategorie", "Category", "string"),
             col("older", "Älterer Partner", "Older partner", "string"),
             col("class_difference", "Unterschied in Altersklassen", "Difference in age classes", "integer", "Klassen", True, "aus den Spaltenüberschriften codiert (0–3)"),
             col("per_1000", "Auf 1000 Ehen", "Per 1,000 marriages", "number", "‰"),
             col("order", "Ordnung", "Order", "integer", None, True, "editorische Reihenfolge von »Frau älter« nach »Mann älter«"),
         ],
         "rows": spouse, "source_refs": refs(("104", "b6", "r2"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "civil_per_mille",
         "title": {"de": "Familienstand auf 1000 Einwohner", "en": "Marital status per 1,000 inhabitants"},
         "caption": {"de": "Anteil der Unverheirateten, Verheirateten, Verwitweten und Geschiedenen auf 1000 Einwohner (Brückner S. 103): die Landestheile, das Fürstenthum (Städte, Dörfer, insgesamt) und sechs Vergleichsstaaten.",
                     "en": "Share of unmarried, married, widowed and divorced per 1,000 inhabitants (Brückner p. 103): the districts, the principality (towns, villages, total) and six comparison states."},
         "vegalite": {
             "height": 400,
             "transform": [{"filter": "datum.group == 'Einwohner'"},
                           {"filter": "indexof(['Gera (Landestheil)','Schleiz (Landestheil)','Lobenstein-Ebersdorf (Landestheil)','Fürstenthum (Städte)','Fürstenthum (Dörfer)','Fürstenthum (insgesamt)','S.-Weimar','S.-Meiningen','S.-Altenburg','Schwarzburg-Rudolstadt','Preußen','Württemberg'], datum.region) >= 0"},
                           relabel("region", "region_label", {
                               "Gera (Landestheil)": ("Gera", "Gera"), "Schleiz (Landestheil)": ("Schleiz", "Schleiz"),
                               "Lobenstein-Ebersdorf (Landestheil)": ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"),
                               "Fürstenthum (Städte)": ("Fürstenthum: Städte", "Principality: towns"), "Fürstenthum (Dörfer)": ("Fürstenthum: Dörfer", "Principality: villages"),
                               "Fürstenthum (insgesamt)": ("Fürstenthum insgesamt", "Principality, total"),
                               "S.-Weimar": ("S.-Weimar", "Saxe-Weimar"), "S.-Meiningen": ("S.-Meiningen", "Saxe-Meiningen"), "S.-Altenburg": ("S.-Altenburg", "Saxe-Altenburg"),
                               "Schwarzburg-Rudolstadt": ("Schwarzburg-Rudolstadt", "Schwarzburg-Rudolstadt"), "Preußen": ("Preußen", "Prussia"), "Württemberg": ("Württemberg", "Württemberg")}),
                           {"calculate": "indexof(['unverheiratet','verheiratet','verwitwet','geschieden'], datum.status)", "as": "status_order"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "region", "type": "nominal", "title": None,
                       "sort": ["Gera (Landestheil)", "Schleiz (Landestheil)", "Lobenstein-Ebersdorf (Landestheil)", "Fürstenthum (Städte)", "Fürstenthum (Dörfer)", "Fürstenthum (insgesamt)", "S.-Weimar", "S.-Meiningen", "S.-Altenburg", "Schwarzburg-Rudolstadt", "Preußen", "Württemberg"],
                       "axis": {"labelLimit": 260, "labelExpr": {"de": "replace(replace(replace(replace(datum.label, ' (Landestheil)', ''), ' (Städte)', ': Städte'), ' (Dörfer)', ': Dörfer'), ' (insgesamt)', ' insgesamt')",
                                                                  "en": "replace(replace(replace(replace(replace(replace(replace(replace(datum.label, ' (Landestheil)', ''), ' (Städte)', ': towns'), ' (Dörfer)', ': villages'), ' (insgesamt)', ', total'), 'Fürstenthum', 'Principality'), 'S.-', 'Saxe-'), 'Preußen', 'Prussia'), 'Schwarzburg-Rudolstadt', 'Schwarzburg-Rudolstadt')"}}},
                 "x": {"field": "per_1000", "type": "quantitative", "title": {"de": "Auf 1000 Einwohner", "en": "Per 1,000 inhabitants"}, "scale": {"domain": [0, 1000]}},
                 "color": {"field": "status", "type": "nominal", "scale": {"domain": STATUS},
                           "legend": {"title": None, "columns": 2, "labelExpr": {"de": "datum.label == 'unverheiratet' ? 'unverheiratet' : datum.label",
                                                                    "en": "datum.label == 'unverheiratet' ? 'unmarried' : datum.label == 'verheiratet' ? 'married' : datum.label == 'verwitwet' ? 'widowed' : 'divorced'"}}},
                 "order": {"field": "status_order", "type": "quantitative"},
                 "tooltip": [tt("region_label", "Gebiet", "Area"), tt("status", "Familienstand", "Marital status"), tt_fmt("per_1000", "Auf 1000 Einwohner", "Per 1,000 inhabitants", ".1f")]}}},
        {"id": "c2", "dataset": "civil_per_mille",
         "title": {"de": "Verwitwete auf 1000 Männer und auf 1000 Frauen", "en": "Widowed per 1,000 men and per 1,000 women"},
         "caption": {"de": "Verwitwete je 1000 Männer bzw. Frauen (Brückner S. 103). In allen Gebieten ist der Anteil der Witwen deutlich höher als der der Witwer.",
                     "en": "Widowed per 1,000 men and per 1,000 women (Brückner p. 103). In every area the share of widows is markedly higher than that of widowers."},
         "vegalite": {
             "height": 400,
             "transform": [{"filter": "datum.status == 'verwitwet' && datum.group != 'Einwohner'"},
                           {"filter": "indexof(['Gera (Landestheil)','Schleiz (Landestheil)','Lobenstein-Ebersdorf (Landestheil)','Fürstenthum (Städte)','Fürstenthum (Dörfer)','Fürstenthum (insgesamt)','S.-Weimar','S.-Meiningen','S.-Altenburg','Schwarzburg-Rudolstadt','Preußen','Württemberg'], datum.region) >= 0"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "region", "type": "nominal", "title": None,
                       "sort": ["Gera (Landestheil)", "Schleiz (Landestheil)", "Lobenstein-Ebersdorf (Landestheil)", "Fürstenthum (Städte)", "Fürstenthum (Dörfer)", "Fürstenthum (insgesamt)", "S.-Weimar", "S.-Meiningen", "S.-Altenburg", "Schwarzburg-Rudolstadt", "Preußen", "Württemberg"],
                       "axis": {"labelLimit": 260, "labelExpr": {"de": "replace(replace(replace(replace(datum.label, ' (Landestheil)', ''), ' (Städte)', ': Städte'), ' (Dörfer)', ': Dörfer'), ' (insgesamt)', ' insgesamt')",
                                                                  "en": "replace(replace(replace(replace(replace(replace(replace(datum.label, ' (Landestheil)', ''), ' (Städte)', ': towns'), ' (Dörfer)', ': villages'), ' (insgesamt)', ', total'), 'Fürstenthum', 'Principality'), 'S.-', 'Saxe-'), 'Preußen', 'Prussia')"}}},
                 "yOffset": {"field": "group", "type": "nominal", "scale": {"domain": ["Männer", "Frauen"]}},
                 "x": {"field": "per_1000", "type": "quantitative", "title": {"de": "Verwitwete auf 1000 Männer bzw. Frauen", "en": "Widowed per 1,000 men or women"}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["Männer", "Frauen"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Männer' ? 'Men' : 'Women'"}}},
                 "tooltip": [tt("region", "Gebiet", "Area"), tt("group", "Gruppe", "Group"), tt_fmt("per_1000", "Verwitwete auf 1000", "Widowed per 1,000", ".1f")]}}},
        {"id": "c3", "dataset": "married_by_age",
         "title": {"de": "Anteil der Verheirateten nach Altersklasse", "en": "Share of married persons by age class"},
         "caption": {"de": "Verheiratete in Prozent der jeweiligen Altersklasse (gedruckte Werte, Brückner S. 104), nach Geschlecht in den Städten (helle Balken) und Dörfern (dunkle Balken). Bei den Frauen erreicht der Anteil sein Maximum in der Klasse 30–45, bei den Männern in der Klasse 45–60; danach sinkt er durch Verwitwung, bei den Frauen deutlich stärker.",
                     "en": "Married persons as a per cent of the respective age class (printed values, Brückner p. 104), by sex in the towns (light bars) and villages (dark bars). For women the share peaks in the class 30–45, for men in the class 45–60; afterwards it falls through widowhood, much more strongly for women."},
         "vegalite": {
             "height": 320,
             "transform": [{"filter": "datum.area != 'Fürstenthum'"},
                           {"calculate": "datum.sex + ', ' + datum.area", "as": "series"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "age_class", "type": "ordinal", "scale": {"domain": AGE}, "title": {"de": "Altersklasse (Jahre)", "en": "Age class (years)"},
                       "axis": {"labelAngle": 0, "labelExpr": {"de": "datum.label", "en": "replace(replace(datum.label, 'unter', 'under'), 'über', 'over')"}}},
                 "xOffset": {"field": "series", "type": "nominal", "scale": {"domain": ["männlich, Städte", "männlich, Dörfer", "weiblich, Städte", "weiblich, Dörfer"]}},
                 "y": {"field": "share_pct", "type": "quantitative", "title": {"de": "Verheiratete (%)", "en": "Married (%)"}},
                 "color": {"field": "sex", "type": "nominal", "scale": {"domain": ["männlich", "weiblich"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label == 'männlich' ? 'Männer' : 'Frauen'", "en": "datum.label == 'männlich' ? 'Men' : 'Women'"}}},
                 "opacity": {"field": "area", "type": "ordinal", "sort": ["Städte", "Dörfer"], "scale": {"domain": ["Städte", "Dörfer"], "range": [0.5, 1]},
                             "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Städte' ? 'towns' : 'villages'"}}},
                 "tooltip": [tt("area", "Gebiet", "Area"), tt("sex", "Geschlecht", "Sex"), tt("age_class", "Altersklasse", "Age class"),
                             tt_fmt("share_pct", "Verheiratete (%)", "Married (%)", ".2f"), tt_fmt("married", "Verheiratete (absolut)", "Married (absolute)", ",")]}}},
        {"id": "c4", "dataset": "spouse_age",
         "title": {"de": "Altersunterschied der Ehepartner", "en": "Age difference of spouses"},
         "caption": {"de": "Ehen auf 1000 Ehen nach dem Altersunterschied der Partner in Altersklassen (Brückner S. 104, nach Hildebrand). In rund der Hälfte der Ehen ist der Mann innerhalb derselben Klasse der ältere, in knapp einem Viertel die Frau.",
                     "en": "Marriages per 1,000 marriages by age difference of the partners in age classes (Brückner p. 104, after Hildebrand). In about half of the marriages the husband is the older partner within the same class, in just under a quarter the wife."},
         "vegalite": {
             "height": 320,
             "transform": [SPOUSE_TRANSFORM, {"calculate": "datum.per_1000 == null ? 0 : datum.per_1000", "as": "value0"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "category", "type": "nominal", "sort": {"field": "order", "op": "min"}, "title": None,
                       "axis": {"labelAngle": -35, "labelLimit": 320, "labelExpr": {"de": "datum.label", "en": "{'Frau 3 Klassen älter':'Wife 3 classes older','Frau 2 Klassen älter':'Wife 2 classes older','Frau 1 Klasse älter':'Wife 1 class older','Frau älter, gleiche Altersklasse':'Wife older, same class','Mann älter, gleiche Altersklasse':'Husband older, same class','Mann 1 Klasse älter':'Husband 1 class older','Mann 2 Klassen älter':'Husband 2 classes older','Mann 3 Klassen älter':'Husband 3 classes older'}[datum.label]"}}},
                 "y": {"field": "value0", "type": "quantitative", "title": {"de": "Ehen auf 1000 Ehen", "en": "Marriages per 1,000 marriages"}},
                 "color": {"field": "older", "type": "nominal", "scale": {"domain": ["Mann älter", "Frau älter"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Mann älter' ? 'Husband older' : 'Wife older'"}}},
                 "tooltip": [tt("category_label", "Altersunterschied", "Age difference"), tt_fmt("per_1000", "Auf 1000 Ehen", "Per 1,000 marriages", ".1f")]}}},
    ],
    "keywords": {"de": ["Familienstand", "Verheiratete", "Verwitwete", "Geschiedene", "Unverheiratete", "Ehen", "Altersunterschied", "Witwen", "Scheidung", "Ehepaare", "Heiratsalter"],
                 "en": ["marital status", "married", "widowed", "divorced", "unmarried", "marriages", "age difference", "widows", "divorce", "couples", "age at marriage"]},
    "related": ["bevoelkerung-altersaufbau-1864", "bevoelkerung-eheschliessungen-1858-1867"],
}
write(ana)
