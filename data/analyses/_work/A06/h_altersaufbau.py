"""A06 / analysis 8: age structure in single years, 1864 (pp. 101-103)."""
from common import *

# ------------------------------------------------ single years (p. 101 b1)
g = grid("101", "b1")
M, F, other = {}, {}, []
for r in g[1:]:
    for off in (0, 5):
        a = r[off]
        m, f, s = integer(r[off + 1]), integer(r[off + 2]), integer(r[off + 3])
        assert m + f == s, (a, m, f, s)
        if a.isdigit():
            M[int(a)], F[int(a)] = m, f
        else:
            other.append([a.rstrip('.'), m, f])
assert sorted(M) == list(range(1, 91))
long_rows = []
for a in range(1, 91):
    long_rows.append([a, "männlich", M[a]])
    long_rows.append([a, "weiblich", F[a]])
print(other)
tm = sum(M.values()) + sum(m for _, m, _ in other)
tf = sum(F.values()) + sum(f for _, _, f in other)
print("totals", tm, tf, tm + tf)
T = {a: M[a] + F[a] for a in M}

# deviation from the mean of neighbouring ages
dev_rows = []
for a in range(2, 71):
    nb = (T[a - 1] + T[a + 1]) / 2
    dev_rows.append([a, T[a], round(nb, 1), round((T[a] / nb - 1) * 100, 1)])
dips = [(r[0], r[3]) for r in dev_rows if r[3] <= -20 and r[0] >= 20]
peaks = [(r[0], r[3]) for r in dev_rows if r[3] >= 30 and r[0] >= 20]
print("dips", dips)
print("peaks", peaks)
every10 = [r for r in dev_rows if r[0] % 10 == 2 and r[0] >= 22]
print("ages ending in 2:", [(r[0], r[3]) for r in every10])

# ------------------------------------------------ age classes (p. 102)
b3 = grid("102", "b3")
abs_row, pct_row, cmp_row = b3[3], b3[4], b3[5]


def seq(row, offset=1):
    return [x for x in row[offset:]]


classes_econ = [("Jugend 0–14 Jahre", 0), ("Schaffendes Alter 15–60 Jahre", 9), ("Greisenalter über 60 Jahre", 3)]
# columns in b3: 1-3 Jugend, 4-6 Greisenalter, 7-9 unproductive, 10-12 schaffend
COLS = {"Jugend": 1, "Greisenalter": 4, "Schaffend": 10}
ECON = [("Jugend", "Jugend (0–14 Jahre)"), ("Schaffend", "Schaffendes Alter (15–60 Jahre)"), ("Greisenalter", "Greisenalter (über 60 Jahre)")]
econ_rows = []
for key, label in ECON:
    c = COLS[key]
    m, f, z = integer(abs_row[c]), integer(abs_row[c + 1]), integer(abs_row[c + 2])
    pm, pf, pz = num(pct_row[c]), num(pct_row[c + 1]), num(pct_row[c + 2])
    assert m + f == z
    econ_rows.append(["Reuß j. L. (1864)", label, m, f, z, pm, pf, pz])
for st_i, st in enumerate(("S.-Weimar", "Württemberg")):
    for key, label in ECON:
        c = COLS[key]
        vals = [num(cmp_row[c + k].split("\n")[st_i]) for k in range(3)]
        econ_rows.append([st, label, None, None, None, vals[0], vals[1], vals[2]])
# Reuss per mille sum
zs = sum(r[7] for r in econ_rows if r[0].startswith("Reuß"))
print("Reuss per mille sum", zs, [sum(r[7] for r in econ_rows if r[0] == s) for s in ("S.-Weimar", "Württemberg")])

# legal / military classes
b6, b9 = grid("102", "b6"), grid("102", "b9")
legal = []


def split2(cell):
    a, b = cell.split("\n")
    return integer(a), num(b)


LEG = [("Minderjährig (heiratsunbefugt)", "Familienrecht", 1), ("Großjährig (heiratsbefugt)", "Familienrecht", 4),
       ("Ohne Befugnis zum selbstständigen Gewerbsbetrieb", "Gewerberecht", 7), ("Mit Befugnis zum selbstständigen Gewerbsbetrieb", "Gewerberecht", 10)]
for label, scheme, c in LEG:
    m, pm = split2(b6[3][c])
    f, pf = split2(b6[3][c + 1])
    z, pz = split2(b6[3][c + 2])
    assert m + f == z, label
    legal.append([scheme, label, m, f, z, pm, pf, pz])
MIL = [("0 bis 18 Jahre", 1), ("19 (incl.) bis 45 Jahre", 10), ("Über 45 Jahre", 4)]
for label, c in MIL:
    m, pm = split2(b9[2][c])
    f, pf = split2(b9[2][c + 1])
    z, pz = split2(b9[2][c + 2])
    assert m + f == z, label
    legal.append(["Militärpflicht", label, m, f, z, pm, pf, pz])
for r in legal:
    print(r)

# military shares of inhabitants (p. 103 b1 running text)
t = block("103", "b1")["text"]
import re
mil_vals = [num(x) for x in re.findall(r"(\d{3},\d)", t)]
print(mil_vals)
assert len(mil_vals) == 5
mil = [["Reuß j. L.", "Reuß j. L.", mil_vals[0]], ["S.-Weimar", "übrige", mil_vals[1]], ["S.-Meiningen", "übrige", mil_vals[2]],
       ["S.-Altenburg", "übrige", mil_vals[3]], ["Schwarzburg-Sondershausen", "übrige", mil_vals[4]]]
MIL_EN = {"Reuß j. L.": ("Reuß j. L.", "Reuss j. L."), "S.-Weimar": ("S.-Weimar", "Saxe-Weimar"), "S.-Meiningen": ("S.-Meiningen", "Saxe-Meiningen"),
          "S.-Altenburg": ("S.-Altenburg", "Saxe-Altenburg"), "Schwarzburg-Sondershausen": ("Schwarzburg-Sondershausen", "Schwarzburg-Sondershausen")}

# ------------------------------------------------ prose numbers
pop_total = tm + tf
ECON_R = {r[1]: r for r in econ_rows if r[0].startswith("Reuß")}
jug, sch, gre = (ECON_R[l][7] for _, l in ECON)
wei = {r[1]: r[7] for r in econ_rows if r[0] == "S.-Weimar"}
wue = {r[1]: r[7] for r in econ_rows if r[0] == "Württemberg"}
lab_g = ECON[2][1]
lab_j = ECON[0][1]
lab_s = ECON[1][1]
inf = T[1]
first5 = sum(T[a] for a in range(1, 6))
age_41_45 = sum(T[a] for a in range(41, 46))
age_61_65 = sum(T[a] for a in range(61, 66))
mil_shr = mil_vals[0]
print(inf, first5, age_41_45, age_61_65, pop_total)
sr_all = tf / tm * 100
peak65 = next(r for r in dev_rows if r[0] == 65)
low_ages = [a for a, d in dips]
high_ages = [a for a, d in peaks]
print(low_ages, high_ages, peak65)
d2 = {r[0]: r[3] for r in dev_rows}
d2_vals = [d2[x] for x in (32, 42, 52, 62)]
pk_vals = [d2[x] for x in (31, 41, 61)]
lo2, hi2 = -max(d2_vals), -min(d2_vals)
plo, phi = min(pk_vals), max(pk_vals)
print(lo2, hi2, plo, phi)
# share 1-14 vs 15-60 in the single-year data vs. printed classes (reconciliation for the caveat)
s1_14_m = sum(M[a] for a in range(1, 15)); s1_14_f = sum(F[a] for a in range(1, 15))
s15_60_m = sum(M[a] for a in range(15, 61)); s15_60_f = sum(F[a] for a in range(15, 61))
s61_m = sum(M[a] for a in range(61, 91)) + 1; s61_f = sum(F[a] for a in range(61, 91)) + 5
print("single-year vs printed classes", (s1_14_m, s1_14_f), (14254, 14215), (s15_60_m, s15_60_f), (25165, 26385), (s61_m, s61_f), (3016, 3437))
unk = (75, 68)
diff_j = (14254 - s1_14_m, 14215 - s1_14_f)
diff_s = (25165 - s15_60_m, 26385 - s15_60_f)
print("differences", diff_j, diff_s, sum(diff_j) + sum(diff_s), "unknown age persons", sum(unk))

ana = {
    "id": "bevoelkerung-altersaufbau-1864",
    "title": {"de": "Altersaufbau der Bevölkerung 1864 nach Lebensjahren", "en": "Age structure of the population in single years, 1864"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("101", "b1", "r2-r47"), ("102", "b3", "r4-r6"), ("102", "b6", "r4"), ("102", "b9", "r3"), ("102", "b2"), ("103", "b1")),
    "summary": {
        "de": f"Brückner gibt die Bevölkerung des Fürstenthums nach der Zählung von 1864 für jedes Lebensjahr getrennt nach Geschlecht an und leitet daraus Altersklassen nach wirtschaftlichen, rechtlichen und militärischen Gesichtspunkten ab. Die Pyramide zeigt den starken Sockel der Kinderjahrgänge und das stetige Abschmelzen der Jahrgänge; {de(jug/10,1)} % der Einwohner sind unter 14, {de(sch/10,1)} % zwischen 15 und 60, {de(gre/10,1)} % über 60 Jahre alt.",
        "en": f"Brückner gives the population of the principality in the 1864 census for every year of life by sex and derives age classes from economic, legal and military points of view. The pyramid shows the broad base of the children's cohorts and the steady shrinking of cohorts with age; {en(jug/10,1)} % of the inhabitants are under 14, {en(sch/10,1)} % between 15 and 60 and {en(gre/10,1)} % over 60.",
    },
    "method": {
        "de": f"Aus der Tabelle auf S. 101 wurden Männer und Frauen je Lebensjahr (1–90, dazu »über 90« und »ohne Altersangabe«) in eine lange Tabelle übertragen; die Tabelle ist zweispaltig gedruckt (Lebensjahre 1–46 links, 47–90 rechts). Männer und Frauen ergeben in jeder Zeile die gedruckte Summe, die Gesamtsumme beträgt {de(tm,0)} Männer und {de(tf,0)} Frauen ({de(pop_total,0)}), Brückners Gesamtzahl für 1864 ist 86 472. Aus S. 102 und S. 103 wurden die Altersklassen (Jugend 0–14, schaffendes Alter 15–60, Greisenalter über 60; Heirats- und Gewerbebefugnis mit 21 bzw. 24 Jahren; Militärpflicht 19–45) mit den Vergleichszahlen für S.-Weimar und Württemberg übernommen; »Procental« bedeutet bei Brückner Promille der Gesamtbevölkerung (z. B. Jugend 329,23 ‰ = 14 254 + 14 215 : 86 472). Abgeleitet wurde die Abweichung jedes Lebensjahres vom Mittel der beiden Nachbarjahre (in %). Brückners Lebensjahr 1 ist vermutlich das erste Lebensjahr (Alter 0 bis unter 1); die Tabelle sagt es nicht.",
        "en": f"From the table on p. 101 men and women per year of life (1–90, plus “over 90” and “age not stated”) were transferred into a long table; the table is printed in two columns (years of life 1–46 on the left, 47–90 on the right). In every row men and women add up to the printed sum; the grand total is {en(tm,0)} men and {en(tf,0)} women ({en(pop_total,0)}), Brückner's total for 1864 is 86,472. From pp. 102 and 103 the age classes (youth 0–14, productive age 15–60, old age over 60; legal capacity to marry and to trade independently at 21 and 24; military liability 19–45) were taken over with the comparison figures for Saxe-Weimar and Württemberg; “Procental” means per mille of the total population in Brückner (e.g. youth 329.23 ‰ = 14,254 + 14,215 : 86,472). Derived is the deviation of each year of life from the mean of the two neighbouring years (in %). Brückner's year of life 1 is presumably the first year of life (age 0 to under 1); the table does not say.",
    },
    "findings": [
        {"de": f"Das erste Lebensjahr zählt {de(inf,0)} Personen, die Lebensjahre 1–5 zusammen {de(first5,0)}, die Jahrgänge 41–45 nur {de(age_41_45,0)} und die Jahrgänge 61–65 {de(age_61_65,0)}; auf 100 Männer kommen {de(sr_all,1)} Frauen.",
         "en": f"The first year of life counts {en(inf,0)} persons, years 1–5 together {en(first5,0)}, years 41–45 only {en(age_41_45,0)} and years 61–65 {en(age_61_65,0)}; there are {en(sr_all,1)} women per 100 men."},
        {"de": f"Brückners Dreiteilung: {de(jug,1)} ‰ Jugend, {de(sch,1)} ‰ schaffendes Alter, {de(gre,1)} ‰ Greisenalter. Gegenüber S.-Weimar ({de(wei[lab_g],1)} ‰ über 60) und Württemberg ({de(wue[lab_g],1)} ‰) ist der Greisenanteil im Fürstenthum kleiner, das schaffende Alter ({de(sch,1)} ‰) liegt zwischen Weimar ({de(wei[lab_s],1)}) und Württemberg ({de(wue[lab_s],1)}).",
         "en": f"Brückner's three-way division: {en(jug,1)} ‰ youth, {en(sch,1)} ‰ productive age, {en(gre,1)} ‰ old age. Compared with Saxe-Weimar ({en(wei[lab_g],1)} ‰ over 60) and Württemberg ({en(wue[lab_g],1)} ‰) the share of the old is smaller in the principality; the productive age ({en(sch,1)} ‰) lies between Weimar ({en(wei[lab_s],1)}) and Württemberg ({en(wue[lab_s],1)})."},
        {"de": f"Die Jahrgangsreihe ist stark gezackt: Die Lebensjahre 32, 42, 52 und 62 sind um {de(lo2,0)}–{de(hi2,0)} % schwächer besetzt als der Mittelwert ihrer Nachbarjahre, die Lebensjahre 31, 41 und 61 liegen {de(plo,0)}–{de(phi,0)} % darüber, das Lebensjahr 65 sogar {de(peak65[3],0)} %. Ein solches Muster deutet eher auf ungenaue Altersangaben und Vorliebe für bestimmte Zahlen als auf wirkliche Geburtenschwankungen hin; Brückner kommentiert es nicht.",
         "en": f"The cohort series is strongly jagged: years of life 32, 42, 52 and 62 are {en(lo2,0)}–{en(hi2,0)} % less populated than the mean of their neighbouring years, years 31, 41 and 61 are {en(plo,0)}–{en(phi,0)} % above it, and year 65 even {en(peak65[3],0)} %. Such a pattern points more to inexact age statements and digit preference than to real fluctuations in births; Brückner does not comment on it."},
        {"de": f"Als militärpflichtig gelten die Männer von 19 bis 45 Jahren: {de(legal[-2][2],0)} Männer, {de(mil_shr,1)} auf 1000 Einwohner, mehr als in Schwarzburg-Sondershausen ({de(mil_vals[4],1)}) und S.-Weimar ({de(mil_vals[1],1)}), weniger als in S.-Meiningen ({de(mil_vals[2],1)}) und S.-Altenburg ({de(mil_vals[3],1)}).",
         "en": f"Men aged 19 to 45 count as liable to military service: {en(legal[-2][2],0)} men, {en(mil_shr,1)} per 1,000 inhabitants, more than in Schwarzburg-Sondershausen ({en(mil_vals[4],1)}) and Saxe-Weimar ({en(mil_vals[1],1)}), fewer than in Saxe-Meiningen ({en(mil_vals[2],1)}) and Saxe-Altenburg ({en(mil_vals[3],1)})."},
    ],
    "caveats": [
        {"de": f"Die Altersklassen auf S. 102 lassen sich aus der Einzeljahrtabelle nicht ganz nachrechnen: Jugend 0–14 Jahre ist dort um {de(sum(diff_j),0)} Personen größer ({de(14254+14215,0)} gegen {de(s1_14_m+s1_14_f,0)} in S. 101), das schaffende Alter um {de(sum(diff_s),0)}; zusammen {de(sum(diff_j)+sum(diff_s),0)} Personen, was ungefähr den {de(sum(unk),0)} Personen ohne Altersangabe entspricht, die Brückner offenbar auf diese Klassen verteilt hat. Die Aufteilung nach Geschlecht auf S. 102 ({de(42435,0)} Männer, {de(44037,0)} Frauen) weicht von S. 101 ({de(tm,0)} bzw. {de(tf,0)}) und S. 92 (42 411 bzw. 44 061) um rund 25 Personen ab; die Gesamtzahl 86 472 wird erreicht (S. 101: {de(pop_total,0)}).",
         "en": f"The age classes on p. 102 cannot be recomputed exactly from the single-year table: youth 0–14 is larger there by {en(sum(diff_j),0)} persons ({en(14254+14215,0)} against {en(s1_14_m+s1_14_f,0)} on p. 101), the productive age by {en(sum(diff_s),0)}; together {en(sum(diff_j)+sum(diff_s),0)} persons, roughly the {en(sum(unk),0)} persons of unknown age whom Brückner apparently distributed over these classes. The sex split on p. 102 ({en(42435,0)} men, {en(44037,0)} women) differs by about 25 persons from p. 101 ({en(tm,0)} and {en(tf,0)}) and p. 92 (42,411 and 44,061); the total of 86,472 is reached (p. 101: {en(pop_total,0)})."},
        {"de": "Gedruckte Unstimmigkeiten (Transkription und Faksimile stimmen überein): S. 102, Militärpflicht, Spalte »Überhaupt« männlich 26 312 (17 845 + 8 477 = 26 322; die Summe 53 498 passt zu 26 322); bei den Promille des einzelnen Lebensjahres 23 steht 17,31 statt 17,51 (S. 101). Die Promillezahlen der Einzeljahre wurden nicht übernommen.",
         "en": "Printed inconsistencies (transcription and facsimile agree): p. 102, military liability, column “total” male 26,312 (17,845 + 8,477 = 26,322; the sum 53,498 fits 26,322); for year of life 23 the per-mille figure on p. 101 is 17.31 instead of 17.51. The per-mille figures of the single years were not taken over."},
        {"de": "Die Zählung erfasst die ortsanwesende bzw. Wohnbevölkerung zum Stichtag; Alter in Lebensjahren, nicht Geburtsjahrgänge. Die Altersklassengrenzen (14, 21, 24, 60) gelten nach Brückner für Schulpflicht/Konfirmation, Volljährigkeit und Heiratsbefugnis, Gewerbebefugnis und Arbeitsfähigkeit.",
         "en": "The census records the present or resident population at the reference date; ages are in years of life, not birth cohorts. According to Brückner the class limits (14, 21, 24, 60) correspond to school age/confirmation, majority and capacity to marry, trading licence and working capacity."},
    ],
    "datasets": [
        {"name": "single_years", "title": {"de": "Bevölkerung 1864 nach Lebensjahren und Geschlecht", "en": "Population in 1864 by year of life and sex"},
         "columns": [
             col("age", "Lebensjahr", "Year of life", "integer", None),
             col("sex", "Geschlecht", "Sex", "string"),
             col("persons", "Personen", "Persons", "integer", "Personen"),
         ],
         "rows": long_rows, "source_refs": refs(("101", "b1", "r2-r47"))},
        {"name": "age_other", "title": {"de": "Ohne Jahresangabe: über 90 und ohne Altersangabe", "en": "Not by single year: over 90 and age not stated"},
         "columns": [
             col("category", "Kategorie", "Category", "string"),
             col("male", "Männlich", "Male", "integer", "Personen"),
             col("female", "Weiblich", "Female", "integer", "Personen"),
         ],
         "rows": other, "source_refs": refs(("101", "b1", "r46-r47"))},
        {"name": "age_deviation", "title": {"de": "Abweichung der Jahrgangsstärke vom Mittel der Nachbarjahre", "en": "Deviation of cohort size from the mean of neighbouring years"},
         "columns": [
             col("age", "Lebensjahr", "Year of life", "integer"),
             col("persons", "Personen (Männer + Frauen)", "Persons (men + women)", "integer", "Personen", True, "Summe der gedruckten Männer- und Frauenzahlen"),
             col("neighbour_mean", "Mittel der Nachbarjahre", "Mean of neighbouring years", "number", "Personen", True),
             col("deviation_pct", "Abweichung vom Nachbarmittel", "Deviation from neighbour mean", "number", "%", True),
         ],
         "rows": dev_rows, "source_refs": refs(("101", "b1", "r2-r47"))},
        {"name": "age_classes_econ", "title": {"de": "Altersklassen nach Brückner, mit S.-Weimar und Württemberg", "en": "Brückner's age classes, with Saxe-Weimar and Württemberg"},
         "columns": [
             col("region", "Gebiet", "Region", "string"),
             col("age_class", "Altersklasse", "Age class", "string"),
             col("male", "Männlich", "Male", "integer", "Personen"),
             col("female", "Weiblich", "Female", "integer", "Personen"),
             col("total", "Zusammen", "Total", "integer", "Personen"),
             col("permille_male", "Promille der Gesamtbevölkerung, männlich", "Per mille of the total population, male", "number", "‰"),
             col("permille_female", "Promille der Gesamtbevölkerung, weiblich", "Per mille of the total population, female", "number", "‰"),
             col("permille_total", "Promille der Gesamtbevölkerung, zusammen", "Per mille of the total population, total", "number", "‰"),
         ],
         "rows": econ_rows, "source_refs": refs(("102", "b3", "r4-r6"))},
        {"name": "age_classes_legal", "title": {"de": "Rechtliche und militärische Altersklassen 1864", "en": "Legal and military age classes, 1864"},
         "columns": [
             col("scheme", "Gesichtspunkt", "Point of view", "string"),
             col("age_class", "Altersklasse", "Age class", "string"),
             col("male", "Männlich", "Male", "integer", "Personen"),
             col("female", "Weiblich", "Female", "integer", "Personen"),
             col("total", "Zusammen", "Total", "integer", "Personen"),
             col("permille_male", "Promille der Gesamtbevölkerung, männlich", "Per mille of the total population, male", "number", "‰"),
             col("permille_female", "Promille der Gesamtbevölkerung, weiblich", "Per mille of the total population, female", "number", "‰"),
             col("permille_total", "Promille der Gesamtbevölkerung, zusammen", "Per mille of the total population, total", "number", "‰"),
         ],
         "rows": legal, "source_refs": refs(("102", "b6", "r4"), ("102", "b9", "r3"))},
        {"name": "military", "title": {"de": "Militärpflichtige auf 1000 Einwohner", "en": "Persons liable to military service per 1,000 inhabitants"},
         "columns": [
             col("state", "Staat", "State", "string"),
             col("group", "Gruppe", "Group", "string", None, True, "Reuß j. L. gegenüber den übrigen Staaten (editorisch)"),
             col("per_1000", "Militärpflichtige auf 1000 Einwohner", "Liable to military service per 1,000 inhabitants", "number", "‰"),
         ],
         "rows": mil, "source_refs": refs(("103", "b1"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "single_years",
         "title": {"de": "Bevölkerungspyramide 1864", "en": "Population pyramid, 1864"},
         "caption": {"de": "Männer (links) und Frauen (rechts) je Lebensjahr nach der Zählung von 1864 (Brückner S. 101). Auffällig sind die Zacken in der Reihe, die wohl auf Altersangaben zurückgehen.",
                     "en": "Men (left) and women (right) per year of life in the 1864 census (Brückner p. 101). The jagged outline probably reflects the way ages were stated."},
         "vegalite": {
             "height": 420,
             "transform": [{"calculate": "datum.sex == 'männlich' ? -datum.persons : datum.persons", "as": "signed"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "age", "type": "ordinal", "sort": "descending", "title": {"de": "Lebensjahr", "en": "Year of life"},
                       "axis": {"values": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90], "labelAngle": 0, "ticks": False}},
                 "x": {"field": "signed", "type": "quantitative", "title": {"de": "Personen", "en": "Persons"}, "scale": {"domain": [-2700, 2700]},
                       "axis": {"labelExpr": "format(abs(datum.value), ',')"}},
                 "color": {"field": "sex", "type": "nominal", "scale": {"domain": ["männlich", "weiblich"]},
                           "legend": {"title": None, "labelExpr": {"de": "datum.label == 'männlich' ? 'Männer' : 'Frauen'", "en": "datum.label == 'männlich' ? 'Men' : 'Women'"}}},
                 "tooltip": [tt("age", "Lebensjahr", "Year of life"), {"field": "sex", "title": {"de": "Geschlecht", "en": "Sex"}}, tt_fmt("persons", "Personen", "Persons", ",")]}}},
        {"id": "c2", "dataset": "age_classes_econ",
         "title": {"de": "Jugend, schaffendes Alter und Greisenalter im Vergleich", "en": "Youth, productive age and old age in comparison"},
         "caption": {"de": "Promille der Gesamtbevölkerung nach Brückners Dreiteilung: Reuß j. L. (1864) im Vergleich mit S.-Weimar und Württemberg. Beim Vergleichsland S.-Weimar summieren sich die gedruckten Anteile auf 998,8 ‰.",
                     "en": "Per mille of the total population according to Brückner's three-way division: Reuss j. L. (1864) compared with Saxe-Weimar and Württemberg. For Saxe-Weimar the printed shares add up to 998.8 ‰."},
         "vegalite": {
             "height": 220,
             "transform": [{"calculate": "datum.age_class == 'Jugend (0–14 Jahre)' ? 0 : datum.age_class == 'Schaffendes Alter (15–60 Jahre)' ? 1 : 2", "as": "class_order"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "region", "type": "nominal", "title": None, "sort": ["Reuß j. L. (1864)", "S.-Weimar", "Württemberg"],
                       "axis": {"labelLimit": 240, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Reuß j. L. (1864)' ? 'Reuss j. L. (1864)' : datum.label == 'S.-Weimar' ? 'Saxe-Weimar' : datum.label"}}},
                 "x": {"field": "permille_total", "type": "quantitative", "title": {"de": "Promille der Gesamtbevölkerung", "en": "Per mille of the total population"}, "scale": {"domain": [0, 1000]}},
                 "color": {"field": "age_class", "type": "nominal", "scale": {"domain": ["Jugend (0–14 Jahre)", "Schaffendes Alter (15–60 Jahre)", "Greisenalter (über 60 Jahre)"]},
                           "legend": {"title": None, "labelLimit": 320, "columns": 2, "labelExpr": {"de": "datum.label", "en": "datum.label == 'Jugend (0–14 Jahre)' ? 'Youth (0–14)' : datum.label == 'Schaffendes Alter (15–60 Jahre)' ? 'Productive age (15–60)' : 'Old age (over 60)'"}}},
                 "order": {"field": "class_order", "type": "quantitative"},
                 "tooltip": [tt("region", "Gebiet", "Region"), tt("age_class", "Altersklasse", "Age class"), tt_fmt("permille_total", "Promille", "Per mille", ".1f")]}}},
        {"id": "c3", "dataset": "age_deviation",
         "title": {"de": "Wie glatt ist die Jahrgangsreihe?", "en": "How smooth is the series of cohorts?"},
         "caption": {"de": "Abweichung der Zahl der Personen eines Lebensjahres (Männer und Frauen) vom Mittel der beiden Nachbarjahre, in Prozent. Die Lebensjahre 32, 42, 52 und 62 sind um rund ein Viertel unterbesetzt, 31, 41, 61 und besonders 65 überbesetzt: ein Muster ungenauer Altersangaben.",
                     "en": "Deviation of the number of persons of a year of life (men and women) from the mean of the two neighbouring years, in per cent. Years of life 32, 42, 52 and 62 are under-populated by about a quarter, 31, 41, 61 and especially 65 are over-populated: a pattern of inexact age statements."},
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "age", "type": "ordinal", "title": {"de": "Lebensjahr", "en": "Year of life"}, "axis": {"values": [2, 10, 20, 30, 40, 50, 60, 70], "labelAngle": 0}},
                 "y": {"field": "deviation_pct", "type": "quantitative", "title": {"de": "Abweichung vom Nachbarmittel (%)", "en": "Deviation from neighbour mean (%)"}},
                 "color": {"field": "deviation_pct", "type": "quantitative", "scale": {"range": "diverging", "domainMid": 0, "domain": [-60, 60]}, "legend": None},
                 "tooltip": [tt("age", "Lebensjahr", "Year of life"), tt_fmt("persons", "Personen", "Persons", ","), tt_fmt("neighbour_mean", "Nachbarmittel", "Neighbour mean", ".0f"),
                             tt_fmt("deviation_pct", "Abweichung (%)", "Deviation (%)", ".1f")]}}},
        {"id": "c4", "dataset": "military",
         "title": {"de": "Militärpflichtige auf 1000 Einwohner", "en": "Persons liable to military service per 1,000 inhabitants"},
         "caption": {"de": "Männer von 19 bis 45 Jahren je 1000 Einwohner im Fürstenthum Reuß j. L. (1864) und in vier Vergleichsstaaten nach Brückners Text (S. 103).",
                     "en": "Men aged 19 to 45 per 1,000 inhabitants in the Principality of Reuss j. L. (1864) and in four comparison states according to Brückner's text (p. 103)."},
         "vegalite": {
             "height": 200,
             "transform": [relabel("state", "state_label", MIL_EN)],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "state_label", "type": "nominal", "title": None, "sort": "-x", "axis": {"labelLimit": 280}},
                 "x": {"field": "per_1000", "type": "quantitative", "title": {"de": "auf 1000 Einwohner", "en": "per 1,000 inhabitants"}, "scale": {"domain": [0, 200]}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige", "Reuß j. L."]}, "legend": None},
                 "tooltip": [tt("state_label", "Staat", "State"), tt_fmt("per_1000", "auf 1000 Einwohner", "per 1,000 inhabitants", ".1f")]}}},
    ],
    "keywords": {"de": ["Altersaufbau", "Bevölkerungspyramide", "Altersklassen", "Lebensjahre", "Jugend", "Greisenalter", "Militärpflichtige", "Volljährigkeit", "Heiratsalter", "1864", "Altersangaben"],
                 "en": ["age structure", "population pyramid", "age classes", "years of life", "youth", "old age", "military liability", "majority", "age heaping", "1864"]},
    "related": ["bevoelkerung-geschlecht-alter-1834-1867", "bevoelkerung-familienstand-ehen-1864", "gesundheit-militaer-tauglichkeit-1864-1866"],
}
write(ana)
