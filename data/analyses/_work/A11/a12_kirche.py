"""A11-12: Kirchenorganisation 1868: Ephorien, Parochien, Kirchen, Geistliche und Pfarrbesoldung (p. 294; p. 297 for comparison)."""
import re
from common import *

# --- Ephorien (p. 294 b6) -------------------------------------------------------------------
g6 = grid("294", "b6")
eph = []
for r in g6[1:4]:
    name = r[0].replace(".", "").strip()
    eph.append([name, int(num(r[1])), int(num(r[2])), int(num(r[3])), int(num(r[4])) if num(r[4]) is not None else 0])
tot = [int(num(x)) if num(x) is not None else 0 for x in g6[4][1:]]
assert [sum(e[i] for e in eph) for i in (1, 2, 3, 4)] == tot, tot
print(eph, tot)
long_e = []
MEAS = [("a", "Parochien", "Parishes", 1), ("b", "Kirchen", "Churches", 2), ("c", "Geistliche", "Clergy", 3)]
for e in eph:
    for k, de, en, i in MEAS:
        long_e.append([e[0], k, de, en, e[i]])

# --- salary classes (p. 294 b2) -------------------------------------------------------------
g2 = grid("294", "b2")
sal = []
for i, r in enumerate(g2[1:]):
    t = " ".join(r)
    nums = [int(x) for x in re.findall(r"\d+", t)]
    n = nums[0]
    if "Ephorus" in t:  # "12 " 2 " und 1 Ephorus 800 " 1000"
        d, e = nums[1], nums[2]
        lo, hi = nums[3], nums[4]
    elif "Ephoren" in t:  # "10 " 2 Ephoren über 1000"
        d, e = 0, nums[1]
        lo, hi = nums[2], None
    else:
        d, e = nums[1], 0
        lo, hi = nums[2], nums[3]
    sal.append((n, d, e, lo, hi))
print(sal)
assert [s[0] for s in sal] == [8, 12, 11, 6, 12, 10]
salary_rows = []
for i, (n, d, e, lo, hi) in enumerate(sal):
    label_de = f"{lo}–{hi}" if hi else f"über {lo}"
    label_en = f"{lo}–{hi}" if hi else f"over {lo}"
    pfarrer = n - d - e
    for k, de, en, v in (("a", "Pfarrer", "Pastors", pfarrer), ("b", "Diaconen", "Deacons", d), ("c", "Ephoren", "Ephors", e)):
        salary_rows.append([str(i + 1), label_de, label_en, k, de, en, v])
positions = sum(s[0] for s in sal)
deacons = sum(s[1] for s in sal)
ephors = sum(s[2] for s in sal)
mids = [450, 550, 650, 750, 900, 1000]
mean_low = sum(s[0] * m for s, m in zip(sal, mids)) / positions
cum = 0
median_class = None
for s in sal:
    cum += s[0]
    if cum >= positions / 2 and median_class is None:
        median_class = s
print(positions, deacons, ephors, mean_low, median_class)
below600 = sal[0][0] + sal[1][0]
above800 = sal[4][0] + sal[5][0]

# --- ratios printed in p. 294 b7 --------------------------------------------------------------
ratios = [
    ["a", "Seelen je Parochie", "Souls per parish", 1955, 45, 45 * 1955],
    ["b", "Seelen je Kirche", "Souls per church", 862.4, 102, round(102 * 862.4)],
    ["c", "Seelen je Geistlichem", "Souls per clergyman", 1293.8, 68, round(68 * 1293.8)],
]
print(ratios)

tmin_teacher = 180   # p. 297 b3: Minimalbesoldung auf dem Plattlande
pct = lambda a, b: 100 * a / b


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


kpp = {e[0]: e[2] / e[1] for e in eph}
gpp = {e[0]: e[3] / e[1] for e in eph}

ana = {
    "id": "kirche-ephorien-pfarreien-besoldung-1868",
    "title": bi("Kirchenorganisation 1868: Ephorien, Kirchen, Geistliche und Pfarrbesoldung", "Church organisation in 1868: ephories, churches, clergy and pastors' pay"),
    "category": "church",
    "section": "t1-4-5",
    "sources": [{"page": "294", "block": "b2", "rows": "r2-r7"}, {"page": "294", "block": "b6", "rows": "r2-t5"}, {"page": "294", "block": "b7"}, {"page": "297", "block": "b3"}],
    "summary": bi(
        f"Das Fürstentum gliederte sich kirchlich in drei Ephorien (Gera, Schleiz, Lobenstein) mit zusammen {D(tot[0])} Parochien, {D(tot[1])} Kirchen und {D(tot[2])} Geistlichen. Brückner ordnet außerdem {D(positions)} Pfarrstellen in Gehaltsklassen von 400 bis über 1000 Thalern. Die Auswertung zeigt die Unterschiede zwischen den Ephorien und die Verteilung der Besoldung.",
        f"Ecclesiastically the principality was divided into three ephories (Gera, Schleiz, Lobenstein) with {E(tot[0])} parishes, {E(tot[1])} churches and {E(tot[2])} clergy in total. Brückner also arranges {E(positions)} pastoral posts in salary classes from 400 to over 1,000 Thaler. The analysis shows the differences between the ephories and the distribution of pay.",
    ),
    "method": bi(
        "Die Zahlen der Ephorien stammen aus der Tabelle S. 294 (b6), die Gehaltsklassen aus der Tabelle S. 294 (b2, die Zeilen nennen die Zahl der Pfarreien einschließlich Diaconen und Ephoren). Die Zahl der Pfarrer je Klasse = Pfarreien − Diaconen − Ephoren (abgeleitet). Für den Mittelwert wurden Klassenmitten verwendet (450, 550, 650, 750, 900) und die offene oberste Klasse mit 1000 angesetzt; der Wert ist daher eine Untergrenze. Brückners Verhältniszahlen (1955 Seelen je Parochie usw.) sind im Datensatz ratios wiedergegeben; die daraus folgende Einwohnerzahl ist abgeleitet. Vergleichswert: gesetzliche Mindestbesoldung eines Landlehrers 180 Thaler (S. 297).",
        "The ephory figures come from the table on p. 294 (b6), the salary classes from the table on p. 294 (b2; the rows give the number of pastorates including deacons and ephors). Number of pastors per class = pastorates − deacons − ephors (derived). For the mean, class midpoints were used (450, 550, 650, 750, 900) and the open top class set at 1,000, so the value is a lower bound. Brückner's ratios (1,955 souls per parish etc.) are reproduced in the dataset ratios; the population they imply is derived. Comparison: the legal minimum pay of a village teacher is 180 Thaler (p. 297).",
    ),
    "findings": [
        bi(f"Gera hat mit {D(kpp['Gera'],1)} Kirchen je Parochie die meisten Kirchen pro Kirchspiel, Schleiz ({D(kpp['Schleiz'],1)}) und Lobenstein ({D(kpp['Lobenstein'],1)}) haben deutlich weniger; Schleiz zählt mit 27 die meisten Geistlichen bei nur {D(eph[1][2])} Kirchen.",
           f"Gera, with {E(kpp['Gera'],1)} churches per parish, has the most churches per parish; Schleiz ({E(kpp['Schleiz'],1)}) and Lobenstein ({E(kpp['Lobenstein'],1)}) have considerably fewer; Schleiz counts the most clergy (27) with only {E(eph[1][2])} churches."),
        bi(f"Auf eine Parochie kommen im Durchschnitt 1955 Seelen, auf eine Kirche 862,4 und auf einen Geistlichen 1293,8; aus den Verhältniszahlen folgt eine Bevölkerung von rund {D(ratios[0][5])}.",
           f"On average there are 1,955 souls per parish, 862.4 per church and 1,293.8 per clergyman; the ratios imply a population of about {E(ratios[0][5])}."),
        bi(f"Von {D(positions)} Pfarrstellen (einschließlich {D(deacons)} Diaconaten und {D(ephors)} Ephoren) haben {D(below600)} ({D(pct(below600, positions),0)} %) weniger als 600, {D(above800)} ({D(pct(above800, positions),0)} %) mindestens 800 Thaler; der Median liegt in der Klasse {median_class[3]}–{median_class[4]} Thaler.",
           f"Of {E(positions)} pastorates (including {E(deacons)} deaconates and {E(ephors)} ephors) {E(below600)} ({E(pct(below600, positions),0)} %) pay less than 600 and {E(above800)} ({E(pct(above800, positions),0)} %) at least 800 Thaler; the median lies in the class {median_class[3]}–{median_class[4]} Thaler."),
        bi(f"Das niedrigste Pfarrgehalt (400 Thaler) ist mehr als doppelt so hoch wie die gesetzliche Mindestbesoldung eines Lehrers auf dem Land (180 Thaler, S. 297).",
           f"The lowest pastor's salary (400 Thaler) is more than twice the legal minimum pay of a village teacher (180 Thaler, p. 297)."),
    ],
    "caveats": [
        bi("Brückner gibt die Gehaltsklassen ohne Jahr an (»gegenwärtig«, also 1868/69) und ohne Angabe, ob Naturalien und Nebeneinkünfte eingerechnet sind. Die Summe der Pfarreien in der Gehaltstabelle (59) ist nicht mit den 45 Parochien oder den 68 Geistlichen der Ephorientabelle identisch; die Tabellen zählen offenbar Stellen, Pfarrer und Diaconen unterschiedlich.",
           "Brückner gives the salary classes without a year (“at present”, i.e. 1868/69) and without saying whether payments in kind and incidental income are included. The total of pastorates in the salary table (59) is not identical with the 45 parishes or the 68 clergy of the ephory table; the tables evidently count posts, pastors and deacons differently."),
        bi("Der Mittelwert aus Klassenmitten (rund 720 Thaler) ist nur eine Untergrenze und eine grobe Näherung. Katecheten (2 im Landestheil Gera) sind in den Geistlichen nicht enthalten.",
           "The mean from class midpoints (about 720 Thaler) is only a lower bound and a rough approximation. Catechists (2 in the Gera region) are not included in the clergy."),
    ],
    "datasets": [
        {"name": "ephories", "title": bi("Parochien, Kirchen und Geistliche nach Ephorien", "Parishes, churches and clergy by ephory"),
         "columns": [col("ephory", "Ephorie", "Ephory", "string"), col("measure_key", "Kürzel", "Key", "string"),
                     col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
                     col("count", "Anzahl", "Count", "integer", "Anzahl")],
         "rows": long_e, "source_refs": [{"page": "294", "block": "b6", "rows": "r2-t5"}]},
        {"name": "salary", "title": bi("Pfarrstellen nach Gehaltsklasse", "Pastorates by salary class"),
         "columns": [col("class_key", "Kürzel Klasse", "Class key", "string"),
                     col("class_de", "Gehaltsklasse", "Salary class", "string"), col("class_en", "Gehaltsklasse (englisch)", "Salary class (English)", "string"),
                     col("kind_key", "Kürzel Art", "Kind key", "string"),
                     col("kind_de", "Art der Stelle", "Kind of post", "string"), col("kind_en", "Art der Stelle (englisch)", "Kind of post (English)", "string"),
                     col("posts", "Stellen", "Posts", "integer", "Stellen", derived=True, note="Pfarrer = Pfarreien − Diaconen − Ephoren; Diaconen und Ephoren wie gedruckt")],
         "rows": salary_rows, "source_refs": [{"page": "294", "block": "b2", "rows": "r2-r7"}]},
        {"name": "ratios", "title": bi("Brückners Verhältniszahlen", "Brückner's ratios"),
         "columns": [col("ratio_key", "Kürzel", "Key", "string"), col("ratio_de", "Verhältnis", "Ratio", "string"), col("ratio_en", "Verhältnis (englisch)", "Ratio (English)", "string"),
                     col("souls", "Seelen je Einheit", "Souls per unit", "number", "Seelen"), col("units", "Einheiten insgesamt", "Units in total", "integer", "Anzahl"),
                     col("implied_pop", "Daraus folgende Einwohnerzahl", "Implied population", "integer", "Einwohner", derived=True)],
         "rows": ratios, "source_refs": [{"page": "294", "block": "b7"}, {"page": "294", "block": "b6", "rows": "t5"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "ephories",
         "title": bi("Parochien, Kirchen und Geistliche je Ephorie", "Parishes, churches and clergy per ephory"),
         "caption": bi("Anzahl; Gera hat die meisten Kirchen, Schleiz die meisten Geistlichen.", "Counts; Gera has the most churches, Schleiz the most clergy."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "x": {"field": "ephory", "type": "nominal", "title": bi("Ephorie", "Ephory"), "axis": {"labelAngle": 0}},
                 "xOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "y": {"field": "count", "type": "quantitative", "title": bi("Anzahl", "Count")},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}},
                 "tooltip": [tt("ephory", "Ephorie", "Ephory"), ttf("measure", "Messgröße", "Measure"), tt("count", "Anzahl", "Count")]}}},
        {"id": "c2", "dataset": "salary",
         "title": bi("Pfarrstellen nach Gehaltsklasse", "Pastorates by salary class"),
         "caption": bi("Zahl der Stellen je Gehaltsklasse (Thaler), gegliedert in Pfarrer, Diaconen und Ephoren.", "Number of posts per salary class (Thaler), split into pastors, deacons and ephors."),
         "vegalite": {
             "height": 280,
             "mark": "bar",
             "encoding": {
                 "x": {"field": F("class"), "type": "nominal", "sort": {"field": "class_key", "op": "min"}, "title": bi("Gehalt (Thaler)", "Salary (Thaler)"), "axis": {"labelAngle": 0}},
                 "y": {"field": "posts", "type": "quantitative", "title": bi("Stellen", "Posts"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [ttf("class", "Gehaltsklasse", "Salary class"), ttf("kind", "Art", "Kind"), tt("posts", "Stellen", "Posts")]}}},
        {"id": "c3", "dataset": "ratios",
         "title": bi("Seelen je Parochie, Geistlichem und Kirche", "Souls per parish, clergyman and church"),
         "caption": bi("Durchschnitt für das ganze Fürstentum nach Brückner.", "Average for the whole principality according to Brückner."),
         "vegalite": {
             "height": 170,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("ratio"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 260}},
                 "x": {"field": "souls", "type": "quantitative", "title": bi("Seelen", "Souls")},
                 "tooltip": [ttf("ratio", "Verhältnis", "Ratio"), {"field": "souls", "title": bi("Seelen", "Souls"), "format": ",.1f"}]}}},
    ],
    "keywords": {"de": ["Kirche", "Ephorie", "Superintendentur", "Parochien", "Pfarreien", "Geistliche", "Pfarrgehalt", "Besoldung", "Gera", "Schleiz", "Lobenstein"],
                 "en": ["church", "ephory", "superintendency", "parishes", "clergy", "pastors' pay", "salary", "Gera", "Schleiz", "Lobenstein"]},
}
write(ana)
