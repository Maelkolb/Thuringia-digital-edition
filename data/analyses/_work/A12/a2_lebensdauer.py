"""Analysis: life spans and child mortality of the members of the house of Reuss, Tab. VI-XIV (pp. 394-402)."""
import re, statistics
from common import *
import persons as PS
from parse_tabs import BLOCKS, HEADS, norm

ALL = PS.build()
n_birth = len(ALL)
P = [p for p in ALL if p["death"] is not None]
n_death = len(P)
n_birth_only = n_birth - n_death
BRANCH = {"VI": "jung", "VII": "jung", "VIII": "jung", "IX": "jung", "X": "jung", "XI": "jung", "XII": "alt", "XIII": "alt", "XIV": "alt"}

CLASSES = [
    (0, "im Geburtsjahr", "in the year of birth"),
    (1, "1–14 Jahre", "1–14 years"),
    (2, "15–44 Jahre", "15–44 years"),
    (3, "45–64 Jahre", "45–64 years"),
    (4, "65 und älter", "65 and older"),
]


def cls(age):
    if age == 0:
        return 0
    if age < 15:
        return 1
    if age < 45:
        return 2
    if age < 65:
        return 3
    return 4


SEX = {"m": ("männlich", "male"), "f": ("weiblich", "female")}
P.sort(key=lambda p: (p["birth"], p["death"], p["name"]))
rows = []
for i, p in enumerate(P, 1):
    age = p["death"] - p["birth"]
    c = cls(age)
    coh = p["birth"] // 50 * 50
    p.update(age=age, cls=c, cohort=coh)
    rows.append([i, p["name"], p["sex"], SEX[p["sex"]][0], SEX[p["sex"]][1], BRANCH[p["tab"]], p["tab"], p["birth"], p["death"], age,
                 coh, f"{coh}–{coh+49}", c, CLASSES[c][1], CLASSES[c][2], p["page"], p["block"]])

# cohort statistics for births 1550-1799 (later cohorts lack the survivors)
COH = list(range(1550, 1800, 50))
cstat = []
for coh in COH:
    g = [p for p in P if p["cohort"] == coh]
    a15 = [p["age"] for p in g if p["age"] >= 15]
    cstat.append([coh, f"{coh}–{coh+49}", len(g), sum(1 for p in g if p["age"] == 0), sum(1 for p in g if p["age"] < 15),
                  round(100 * sum(1 for p in g if p["age"] < 15) / len(g), 1), len(a15), statistics.median(a15)])
G = [p for p in P if 1550 <= p["birth"] < 1800]
nG = len(G)
g0 = sum(1 for p in G if p["age"] == 0)
g15 = sum(1 for p in G if p["age"] < 15)
g65 = sum(1 for p in G if p["age"] >= 65)
pct = lambda a, b: round(100 * a / b, 1)
PD = lambda x: f"{x:.1f}".replace(".", ",")
PE = lambda x: f"{x:.1f}"
D = lambda x: (str(int(x)) if float(x).is_integer() else f"{x:.1f}").replace(".", ",")  # German decimal comma
E = lambda x: (str(int(x)) if float(x).is_integer() else f"{x:.1f}")
men = [p for p in G if p["sex"] == "m"]
women = [p for p in G if p["sex"] == "f"]
m15 = sum(1 for p in men if p["age"] < 15)
w15 = sum(1 for p in women if p["age"] < 15)
peak = max(cstat, key=lambda r: r[5])
low = min(cstat, key=lambda r: r[5])
med_by = {r[0]: r[7] for r in cstat}
n15_by = {r[0]: r[6] for r in cstat}
oldest = max(P, key=lambda p: p["age"])
print(n_birth, n_death, nG, g0, g15, g65, m15, len(men), w15, len(women), peak, low, med_by, oldest["name"], oldest["age"])

BL = sorted({(p["page"], p["block"]) for p in P})
REFS = refs_from(BL)

# transcription issues
issues = [
 {"page": "394", "block": "b2", "cell": "r3c6, r4c6, r5c3, r5c5, r5c6, r6c1–r6c4, r6c6", "transcribed": "§ IV., § V., § II., § XIII. … (»§« vor der Zählung)", "facsimile": "H. IV., H. V., H. II., H. XIII. … (gedrucktes »H.« für Heinrich)", "checked_facsimile": True,
  "note": "Das gebrochene H des Drucks wurde als »§« gelesen; im Datensatz steht »H.«. Stichprobe am Faksimile (H. II., H. XIII.–XXII.)."},
 {"page": "398", "block": "b2", "cell": "r7c1", "transcribed": "Heinrich LX., g. 1784, † 1813", "facsimile": "H. LXI., g. 1784, † 1813", "checked_facsimile": True,
  "note": "Heinrich LX. (1784–1833) steht in Tab. XI; im Datensatz gilt H. LXI. nach dem Druck."},
 {"page": "398", "block": "b2", "cell": "r3c2", "transcribed": "… Gem. Joh. Christian Fürst v. Solms-Baruth, g. u. † 1749.", "facsimile": "ein eigener, im Druck senkrecht gesetzter Eintrag »… g. u. † 1749« neben dem Ehemann", "checked_facsimile": True,
  "note": "Der Eintrag ist in der Transkription an den Ehemann angehängt, ohne Namen; er wurde nicht aufgenommen."},
 {"page": "398", "block": "b2", "cell": "r6c3", "transcribed": "Heinrich LXXIV., g. 1798, † 1855", "facsimile": "nicht geprüft; Tab. XI (S. 399) und der Text (S. 388) nennen Heinrich LXXIV. als lebend, Tab. X r8c4 nennt Heinrich LXXIII. mit denselben Daten", "checked_facsimile": False,
  "note": "Widerspruch; der Eintrag wurde nicht aufgenommen."},
 {"page": "397", "block": "b4", "cell": "r1c1–r1c2", "transcribed": "Caroline, g. 1792, † 18.. geb. 1797, † 1853 | Heinrich LXXII., Sophie Adelheid, geb. 1800", "facsimile": "nicht geprüft", "checked_facsimile": False,
  "note": "Namen und Daten sind in der Transkription gegeneinander verschoben; Heinrich LXXII. (1797–1853) steht auch in Tab. X."},
]

YEAR = bi("Geburtsjahr", "Year of birth")
SEXDOM = [bi(SEX["m"][0], SEX["m"][1]), bi(SEX["f"][0], SEX["f"][1])]
SEXCOL = {"field": bi("sex_de", "sex_en"), "type": "nominal", "title": bi("Geschlecht", "Sex"), "scale": {"domain": SEXDOM}}
CLSDOM = [bi(c[1], c[2]) for c in CLASSES]
CLSFIELD = bi("class_de", "class_en")

a = {
 "id": "genealogie-reuss-lebensdauer-kindersterblichkeit-1550-1850",
 "title": bi("Lebensdauer und Kindersterblichkeit im Hause Reuß (Geburtsjahrgänge 1550–1850)", "Life span and child mortality in the house of Reuss (birth cohorts 1550–1850)"),
 "category": "genealogy",
 "section": "t1-5-3",
 "sources": REFS,
 "summary": bi(
  f"Brückners Stammtafeln VI–XIV (S. 394–402) nennen für die Nachkommen Heinrichs von Gera und Heinrichs V. von Untergreiz Geburts- und Sterbejahre. Für {n_death} Personen sind beide Jahre gedruckt; daraus lässt sich ein Sterbealter berechnen. Von den zwischen 1550 und 1799 Geborenen starben {g15} von {nG} ({PD(pct(g15, nG))} %) vor dem 15. Lebensjahr, {g0} schon im Geburtsjahr; wer das 15. Lebensjahr erreichte, wurde bei den Geburtsjahrgängen nach 1700 deutlich älter.",
  f"Brückner's genealogical tables VI–XIV (pp. 394–402) give birth and death years for the descendants of Heinrich of Gera and Heinrich V of Untergreiz. Both years are printed for {n_death} persons, which allows an age at death to be computed. Of those born between 1550 and 1799, {g15} of {nG} ({PE(pct(g15, nG))} %) died before the age of 15, {g0} of them in the year of birth; those who reached 15 lived markedly longer in the cohorts born after 1700."),
 "method": bi(
  f"Aus den Tafeln VI–XIV (jeweils die Zellen und Absätze mit »geb./g.« und »†«) wurden alle Personen mit gedrucktem Geburtsjahr übernommen ({n_birth}; Ehepartner nicht), davon {n_death} mit gedrucktem Sterbejahr. Der Text wurde automatisch zerlegt und stichprobenartig am Faksimile geprüft; doppelt vorkommende Personen (z. B. Heinrich XXIV. in Tab. VI, VII, X) wurden zusammengeführt. »g. u. †« und gleiche Jahre gelten als im Geburtsjahr gestorben. Das Sterbealter ist die Differenz der Jahreszahlen (Spalte »age«, abgeleitet) und daher auf ±1 Jahr genau. Das Geschlecht wurde aus dem Namen erschlossen (Heinrich/H. = männlich, sonst weiblich). Die Anteile (Diagramm 1, 3) beschränken sich auf die Geburtsjahrgänge 1550–1799; spätere Jahrgänge sind unvollständig, weil Lebende ohne Sterbejahr fehlen.",
  f"All persons with a printed year of birth were taken from tables VI–XIV (cells and paragraphs with “geb./g.” and “†”; spouses excluded): {n_birth}, of which {n_death} have a printed year of death. The text was split automatically and checked against the facsimile on a sample; persons occurring twice (e.g. Heinrich XXIV. in Tab. VI, VII, X) were merged. “g. u. †” and equal years count as died in the year of birth. Age at death is the difference of the two years (column “age”, derived) and therefore accurate to ±1 year. Sex was inferred from the name (Heinrich/H. = male, otherwise female). The shares (charts 1 and 3) are restricted to the birth cohorts 1550–1799; later cohorts are incomplete because living persons without a year of death are missing."),
 "findings": [
  bi(f"Von {nG} zwischen 1550 und 1799 geborenen Personen mit Sterbejahr starben {g0} ({PD(pct(g0, nG))} %) noch im Geburtsjahr, {g15} ({PD(pct(g15, nG))} %) vor dem 15. Lebensjahr; {g65} ({PD(pct(g65, nG))} %) wurden 65 Jahre oder älter.",
     f"Of {nG} persons born between 1550 and 1799 with a year of death, {g0} ({PE(pct(g0, nG))} %) died in the year of birth, {g15} ({PE(pct(g15, nG))} %) before the age of 15; {g65} ({PE(pct(g65, nG))} %) reached 65 or more."),
  bi(f"Der Anteil der vor dem 15. Jahr Gestorbenen war im Jahrgang {peak[1]} mit {PD(peak[5])} % am höchsten ({peak[4]} von {peak[2]}) und im Jahrgang {low[1]} mit {PD(low[5])} % am niedrigsten; ein stetiger Rückgang ist in den Tafeln nicht zu erkennen.",
     f"The share of those who died before 15 was highest in the cohort {peak[1]} at {PE(peak[5])} % ({peak[4]} of {peak[2]}) and lowest in the cohort {low[1]} at {PE(low[5])} %; no steady decline can be seen in the tables."),
  bi(f"Wer das 15. Lebensjahr erreichte, starb im Median mit {D(med_by[1550])} Jahren (Jahrgang 1550–1599, n = {n15_by[1550]}), {D(med_by[1600])} (1600–1649), {D(med_by[1650])} (1650–1699), {D(med_by[1700])} (1700–1749) und {D(med_by[1750])} Jahren (1750–1799, n = {n15_by[1750]}).",
     f"Those who reached 15 died at a median age of {E(med_by[1550])} (cohort 1550–1599, n = {n15_by[1550]}), {E(med_by[1600])} (1600–1649), {E(med_by[1650])} (1650–1699), {E(med_by[1700])} (1700–1749) and {E(med_by[1750])} years (1750–1799, n = {n15_by[1750]})."),
  bi(f"Bei den Männern starben {m15} von {len(men)} ({PD(pct(m15, len(men)))} %), bei den Frauen {w15} von {len(women)} ({PD(pct(w15, len(women)))} %) vor dem 15. Lebensjahr; der Unterschied ist bei diesen Fallzahlen klein.",
     f"Among the men {m15} of {len(men)} ({PE(pct(m15, len(men)))} %), among the women {w15} of {len(women)} ({PE(pct(w15, len(women)))} %) died before the age of 15; the difference is small at these sample sizes."),
 ],
 "caveats": [
  bi("Die Stichprobe ist nicht repräsentativ: Sie umfasst nur die Nachkommen der beiden Stammväter in den gedruckten Tafeln, und Personen ohne gedrucktes Sterbejahr fehlen (Lebende von 1870, vermutlich auch manche früh verstorbene Kinder, deren Daten Brückner nicht kannte). Der Befund beschreibt das Fürstenhaus, nicht die Bevölkerung.",
     "The sample is not representative: it covers only the descendants of the two ancestors in the printed tables, and persons without a printed year of death are missing (people alive in 1870, probably also some children who died early and whose dates Brückner did not know). The result describes the princely house, not the population."),
  bi("Sterbealter = Differenz der Jahreszahlen: »im Geburtsjahr gestorben« umfasst Totgeburten und Neugeborene; wer im Folgejahr starb, kann noch keinen Jahrestag erlebt haben und steht trotzdem bei »1–14 Jahre«.",
     "Age at death = difference of the years: “in the year of birth” includes stillbirths and newborns; someone who died in the following year may not have reached a first birthday and still falls under “1–14 years”."),
  bi("Die Tafeln sind quer gedruckt und in der Transkription teils verschoben oder verwechselt; trotz Stichprobenprüfung können einzelne Namen und Jahre fehlerhaft sein (siehe transcription_issues). Dieselbe Zählung kommt mehrfach vor (z. B. zwei »H. VI.«, geb. 1651); sie wurden als verschiedene Personen behandelt.",
     "The tables are printed sideways and partly shifted or confused in the transcription; despite a sample check individual names and years may be wrong (see transcription_issues). The same number occurs several times (e.g. two “H. VI.”, born 1651); they were treated as different persons."),
 ],
 "datasets": [
  {"name": "persons", "title": bi("Personen mit gedrucktem Geburts- und Sterbejahr (Tab. VI–XIV)", "Persons with printed years of birth and death (Tab. VI–XIV)"),
   "columns": [
    {"name": "ord", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
    {"name": "name", "label": bi("Name (wie gedruckt)", "Name (as printed)"), "type": "string", "unit": None},
    {"name": "sex", "label": bi("Geschlecht (Code)", "Sex (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "sex_de", "label": bi("Geschlecht", "Sex"), "type": "string", "unit": None, "derived": True},
    {"name": "sex_en", "label": bi("Geschlecht (englisch)", "Sex (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "branch", "label": bi("Linie (alt = Greiz/ä. L., jung = j. L.)", "Line (alt = Greiz/older, jung = younger)"), "type": "string", "unit": None, "derived": True},
    {"name": "tab", "label": bi("Tafel", "Table"), "type": "string", "unit": None},
    {"name": "birth_year", "label": bi("Geburtsjahr", "Year of birth"), "type": "integer", "unit": None},
    {"name": "death_year", "label": bi("Sterbejahr", "Year of death"), "type": "integer", "unit": None},
    {"name": "age", "label": bi("Sterbealter", "Age at death"), "type": "integer", "unit": "Jahre", "derived": True, "note": "Differenz der Jahreszahlen, ±1 Jahr"},
    {"name": "cohort", "label": bi("Geburtsjahrgang (50 Jahre) ab", "Birth cohort (50 years) from"), "type": "integer", "unit": None, "derived": True},
    {"name": "cohort_label", "label": bi("Geburtsjahrgang", "Birth cohort"), "type": "string", "unit": None, "derived": True},
    {"name": "class_code", "label": bi("Altersklasse (Code)", "Age class (code)"), "type": "integer", "unit": None, "derived": True},
    {"name": "class_de", "label": bi("Altersklasse", "Age class"), "type": "string", "unit": None, "derived": True},
    {"name": "class_en", "label": bi("Altersklasse (englisch)", "Age class (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
   ], "rows": rows, "source_refs": REFS},
  {"name": "cohorts", "title": bi("Kennzahlen je Geburtsjahrgang (1550–1799)", "Key figures per birth cohort (1550–1799)"),
   "columns": [
    {"name": "cohort", "label": bi("Geburtsjahrgang ab", "Birth cohort from"), "type": "integer", "unit": None, "derived": True},
    {"name": "cohort_label", "label": bi("Geburtsjahrgang", "Birth cohort"), "type": "string", "unit": None, "derived": True},
    {"name": "n_all", "label": bi("Personen", "Persons"), "type": "integer", "unit": None, "derived": True},
    {"name": "n_birth_year", "label": bi("davon im Geburtsjahr gestorben", "of these died in the year of birth"), "type": "integer", "unit": None, "derived": True},
    {"name": "n_under15", "label": bi("davon vor dem 15. Jahr gestorben", "of these died before 15"), "type": "integer", "unit": None, "derived": True},
    {"name": "share_under15", "label": bi("Anteil vor dem 15. Jahr gestorben", "Share died before 15"), "type": "number", "unit": "%", "derived": True},
    {"name": "n_15plus", "label": bi("Personen, die 15 erreichten", "Persons who reached 15"), "type": "integer", "unit": None, "derived": True},
    {"name": "median_age_15plus", "label": bi("Mediane Lebensdauer der über 15-Jährigen", "Median age at death of those aged 15 or more"), "type": "number", "unit": "Jahre", "derived": True},
   ], "rows": cstat, "source_refs": REFS},
  {"name": "limit", "title": bi("Größtmögliches Sterbealter bis 1870", "Largest possible age at death up to 1870"),
   "columns": [
    {"name": "birth_year", "label": bi("Geburtsjahr", "Year of birth"), "type": "integer", "unit": None, "derived": True},
    {"name": "max_age", "label": bi("größtmögliches Alter", "largest possible age"), "type": "integer", "unit": "Jahre", "derived": True},
   ], "rows": [[1770, 100], [1870, 0]], "source_refs": REFS[:1]},
 ],
 "charts": [
  {"id": "c1", "dataset": "persons",
   "title": bi("Alter beim Tod nach Geburtsjahrgang", "Age at death by birth cohort"),
   "caption": bi(f"Anteile der gestorbenen Personen je 50-Jahres-Jahrgang (Geburtsjahre 1550–1799, n = {min(r[2] for r in cstat)} bis {max(r[2] for r in cstat)} je Jahrgang). Unten stehen die im Geburtsjahr und die vor dem 15. Lebensjahr Gestorbenen.",
                 f"Shares of the deceased persons per 50-year birth cohort (births 1550–1799, n = {min(r[2] for r in cstat)} to {max(r[2] for r in cstat)} per cohort). At the bottom are those who died in the year of birth and before the age of 15."),
   "vegalite": {"height": 300,
    "transform": [{"filter": "datum.birth_year >= 1550 && datum.birth_year < 1800"}],
    "mark": "bar",
    "encoding": {
     "x": {"field": "cohort_label", "type": "ordinal", "title": bi("Geburtsjahrgang", "Birth cohort"), "axis": {"labelAngle": 0}},
     "y": {"aggregate": "count", "type": "quantitative", "stack": "normalize", "title": bi("Anteil der Personen", "Share of persons"), "axis": {"format": "%"}},
     "color": {"field": CLSFIELD, "type": "ordinal", "title": bi("Alter beim Tod", "Age at death"), "scale": {"domain": CLSDOM, "range": "ordinal"}, "legend": {"columns": 3}},
     "order": {"field": "class_code", "type": "quantitative", "sort": "ascending"},
     "tooltip": [{"field": "cohort_label", "title": bi("Jahrgang", "Cohort")},
                 {"field": CLSFIELD, "title": bi("Alter beim Tod", "Age at death")},
                 {"aggregate": "count", "type": "quantitative", "title": bi("Personen", "Persons")}]}}},
  {"id": "c2", "dataset": "persons", "extra_datasets": ["limit"],
   "title": bi("Sterbealter aller Personen nach Geburtsjahr", "Age at death of all persons by year of birth"),
   "caption": bi("Jeder Punkt eine Person mit gedrucktem Geburts- und Sterbejahr. Die gestrichelte Linie ist das größtmögliche Alter bis 1870; darüber fehlen die zur Zeit des Drucks noch Lebenden.",
                 "Each dot is a person with printed years of birth and death. The dashed line is the largest possible age up to 1870; above it the people still alive at the time of printing are missing."),
   "vegalite": {"height": 340,
    "layer": [
     {"mark": {"type": "point", "filled": True, "size": 36, "opacity": 0.75},
      "encoding": {
       "x": {"field": "birth_year", "type": "quantitative", "title": YEAR, "axis": {"format": "d", "tickCount": 8}, "scale": {"domain": [1500, 1870], "zero": False}},
       "y": {"field": "age", "type": "quantitative", "title": bi("Sterbealter (Jahre)", "Age at death (years)"), "scale": {"domain": [0, 100]}},
       "color": SEXCOL,
       "tooltip": [{"field": "name", "title": bi("Name", "Name")},
                   {"field": "birth_year", "title": bi("geboren", "born")},
                   {"field": "death_year", "title": bi("gestorben", "died")},
                   {"field": "age", "title": bi("Alter (Jahre)", "Age (years)")},
                   {"field": "tab", "title": bi("Tafel", "Table")}]}},
     {"data": {"name": "limit"},
      "mark": {"type": "line", "strokeDash": [4, 3], "color": "#898781"},
      "encoding": {"x": {"field": "birth_year", "type": "quantitative"}, "y": {"field": "max_age", "type": "quantitative", "scale": {"domain": [0, 100]}}}},
    ]}},
  {"id": "c3", "dataset": "cohorts",
   "title": bi("Mediane Lebensdauer derer, die 15 Jahre erreichten", "Median age at death of those who reached 15"),
   "caption": bi("Je Geburtsjahrgang der Median des Sterbealters aller Personen, die mindestens 15 Jahre alt wurden (n im Tooltip).",
                 "Per birth cohort the median age at death of all persons who lived to at least 15 (n in the tooltip)."),
   "vegalite": {"height": 240,
    "mark": {"type": "line", "point": True},
    "encoding": {
     "x": {"field": "cohort_label", "type": "ordinal", "title": bi("Geburtsjahrgang", "Birth cohort"), "axis": {"labelAngle": 0}},
     "y": {"field": "median_age_15plus", "type": "quantitative", "title": bi("Median (Jahre)", "Median (years)"), "scale": {"domain": [30, 70]}},
     "tooltip": [{"field": "cohort_label", "title": bi("Jahrgang", "Cohort")},
                 {"field": "median_age_15plus", "title": bi("Median (Jahre)", "Median (years)")},
                 {"field": "n_15plus", "title": bi("Personen ab 15 Jahren", "Persons aged 15+")},
                 {"field": "share_under15", "title": bi("vor dem 15. Jahr gestorben (%)", "died before 15 (%)")}]}}},
 ],
 "transcription_issues": issues,
 "keywords": {"de": ["Kindersterblichkeit", "Lebensdauer", "Sterbealter", "Fürstenhaus Reuß", "Genealogie", "Stammtafel", "Heinrich Posthumus", "Greiz", "Köstritz", "Ebersdorf"],
              "en": ["child mortality", "life expectancy", "age at death", "princely house of Reuss", "genealogy", "family tree"]},
 "related": ["genealogie-voigte-heinriche-1143-1572", "geschichte-landesteilungen-linien-1240-1870"],
 "generated_by": "Claude Sonnet 5.5 (subagent A12)",
 "date": "2026-10-01",
}

if __name__ == "__main__":
    write_analysis(a)
