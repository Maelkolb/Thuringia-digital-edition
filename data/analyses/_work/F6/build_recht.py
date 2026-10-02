from common import *
import recht_charts as C
import re

IDS = ["justiz-freiwillige-gerichtsbarkeit-1864-1867", "justiz-gefangene-hafttage-1864-1867",
       "justiz-kreisgerichte-berufungen-konkurse-1864-1867", "justiz-strafsachen-einzelrichter-uebertretungen-1864-1867",
       "justiz-strafsachen-kreisgerichte-staatsanwaltschaft-1864-1867", "justiz-zivilrechtspflege-einzelgerichte-1864-1867"]
A = {i: archive(i) for i in IDS}
a_frei, a_gef, a_kreis, a_einz, a_staat, a_ziv = (A[k] for k in IDS)

# ---------------------------------------------------------------- dataset 1: new lawsuits by outcome (both court levels)
OUT = {"a": ("Erkenntnis", "Judgment"), "b": ("Vergleich", "Settlement"), "c": ("Unerledigt", "Unresolved")}
ziv = rows(dataset(a_ziv, "yearly"))
kreis = rows(dataset(a_kreis, "lawsuits"))
proz = []
for r in ziv:
    for key, fld in (("a", "erk_neu"), ("b", "verg_neu"), ("c", "unerl_neu")):
        proz.append(dict(level="Justizämter", year=r["year"], outcome_key=key, outcome_de=OUT[key][0], outcome_en=OUT[key][1], cases=r[fld]))
for r in kreis:
    proz.append(dict(level="Kreisgerichte", year=r["year"], outcome_key=r["outcome_key"], outcome_de=OUT[r["outcome_key"]][0],
                     outcome_en=OUT[r["outcome_key"]][1], cases=r["cases"]))
ds_proz = new_dataset(
    "neue_prozesse", "Neue förmliche Rechtsstreitigkeiten nach Gerichtsebene, Jahr und Ausgang",
    "New formal lawsuits by court level, year and outcome",
    [col("level", "Gerichtsebene", "Court level"), col("year", "Jahr", "Year", "integer"),
     col("outcome_key", "Ausgang (Schlüssel)", "Outcome (key)"), col("outcome_de", "Ausgang", "Outcome"),
     col("outcome_en", "Ausgang (en)", "Outcome (en)"), col("cases", "Fälle", "Cases", "integer", "Fälle")],
    proz,
    [{"page": "284", "block": "b2", "rows": "r13-r16"}, {"page": "286", "block": "b5", "rows": "r4-r7"}])

# ---------------------------------------------------------------- dataset 2: convictions for Uebertretungen 1867 by court (p. 287 b6)
t = (ROOT / "data" / "text" / "pages" / "287.txt").read_text(encoding="utf-8")
blk = t[t.index("[b6 TABLE"):]
raw = {}
for line in blk.splitlines():
    m = re.match(r"\s+(r\d+) \| (.*)", line)
    if m:
        raw[m.group(1)] = [c.strip() for c in m.group(2).split(" | ")]


def num(x):
    return None if x == "—" else int(x)


COURTS = {"r3": ("Gera I", "Gera"), "r4": ("Gera II", "Gera"), "r5": ("Hohenleuben", "Gera"), "r7": ("Schleiz I", "Schleiz"),
          "r8": ("Schleiz II", "Schleiz"), "r9": ("Lobenstein I", "Schleiz"), "r10": ("Lobenstein II", "Schleiz"), "r11": ("Hirschberg", "Schleiz")}
ueb = []
for k, (name, kg) in COURTS.items():
    c = raw[k]
    common, forest, police, defr, honour, total = num(c[3]), num(c[4]), num(c[6]), num(c[8]), num(c[10]), num(c[12])
    assert common + (police or 0) + (defr or 0) + (honour or 0) == total, name
    ueb.append(dict(court=name, kreisgericht=kg, common_convicted=common, forest_convicted=forest, common_other=common - forest,
                    police_convicted=police, defraud_convicted=defr, honour_convicted=honour, total_convicted=total))
# check against the printed sums of the two Kreisgerichte and the Hauptsumme
for k, kg in (("r6", "Gera"), ("r12", "Schleiz")):
    c = raw[k]
    sub = [r for r in ueb if r["kreisgericht"] == kg]
    assert sum(r["common_convicted"] for r in sub) == num(c[3]) and sum(r["forest_convicted"] for r in sub) == num(c[4])
    assert sum(r["police_convicted"] or 0 for r in sub) == num(c[6]) and sum(r["honour_convicted"] or 0 for r in sub) == num(c[10])
    assert sum(r["total_convicted"] for r in sub) == num(c[12])
hs = raw["r13"]
assert sum(r["total_convicted"] for r in ueb) == num(hs[12]) == 1837
ds_ueb = new_dataset(
    "uebertretungen_1867", "Verurteilte wegen Übertretungen 1867 nach Gericht und Art",
    "Persons convicted of petty offences in 1867 by court and kind",
    [col("court", "Justizamt", "Court"),
     col("kreisgericht", "Bezirk des Kreisgerichts", "Kreisgericht district", derived=True,
         note="Kreisgericht Gera: Justizämter Gera I, Gera II, Hohenleuben; Kreisgericht Schleiz: Schleiz I und II, Lobenstein I und II, Hirschberg (S. 281)"),
     col("common_convicted", "Verurteilt wegen gemeiner Übertretungen", "Convicted of common offences", "integer", "Personen"),
     col("forest_convicted", "Davon wegen Forstdiebstahls", "Of which forest theft", "integer", "Personen"),
     col("common_other", "Übrige gemeine Übertretungen", "Other common offences", "integer", "Personen", True),
     col("police_convicted", "Verurteilt wegen polizeilicher Übertretungen", "Convicted of police offences", "integer", "Personen"),
     col("defraud_convicted", "Verurteilt wegen Defraudationen", "Convicted of defraudations", "integer", "Personen"),
     col("honour_convicted", "Verurteilt wegen Ehrenkränkungen", "Convicted of insults to honour", "integer", "Personen"),
     col("total_convicted", "Summe aller Verurteilten", "All persons convicted", "integer", "Personen")],
    ueb, [{"page": "287", "block": "b6", "rows": "r3-r13"}])

# ---------------------------------------------------------------- dataset 3: prisoners
KINDS = {"a": ("Justizämter", "Untersuchungshaft"), "b": ("Justizämter", "Strafhaft"), "c": ("Kreisgerichte", "Untersuchungshaft"),
         "d": ("Kreisgerichte", "Strafhaft")}
gef_rows = rows(dataset(a_gef, "yearly"))
gef = [dict(year=r["year"], level=KINDS[r["kind_key"]][0], haftart=KINDS[r["kind_key"]][1], prisoners=r["prisoners"], days=r["days"],
            avg_days=r["avg_days"]) for r in gef_rows]
ds_gef = new_dataset(
    "gefangene", "Gefangene und Hafttage nach Gerichtsebene und Haftart", "Prisoners and days of custody by court level and kind of custody",
    [col("year", "Jahr", "Year", "integer"), col("level", "Gerichtsebene", "Court level"), col("haftart", "Haftart", "Kind of custody"),
     col("prisoners", "Gefangene", "Prisoners", "integer", "Personen"), col("days", "Tage der Haft", "Days of custody", "integer", "Tage"),
     col("avg_days", "Haftdauer je Gefangenem", "Days per prisoner", "number", "Tage", True)],
    gef, [{"page": "283", "block": "b4", "rows": "r11-r14"}, {"page": "286", "block": "b3", "rows": "r4-r7"}, {"page": "286", "block": "b3", "rows": "r11-r14"}])

# ---------------------------------------------------------------- further table: public prosecutors
ds_staat = dataset(a_staat, "index", new_name="staatsanwaltschaften")
staat = rows(ds_staat)

# ---------------------------------------------------------------- numbers
pop67 = 87974
assert_in_page("92", "87974")
assert_in_page("289", "177")
CONV = {"1865": 139, "1866": 167, "1867": 177}
for k, v in CONV.items():
    assert_in_page("289", f"{k}: {v}") if k != "1865" else assert_in_page("289", "1865: 139")


def cases(level, year, key=None):
    return sum(r["cases"] for r in proz if r["level"] == level and r["year"] == year and (key is None or r["outcome_key"] == key))


ja67, kg67 = cases("Justizämter", 1867), cases("Kreisgerichte", 1867)
assert (ja67, kg67) == (2269, 738)
suits67 = ja67 + kg67
per1000 = suits67 / pop67 * 1000
ja_per, kg_per = ja67 / pop67 * 1000, kg67 / pop67 * 1000
ja_verg, ja_erk = cases("Justizämter", 1867, "b"), cases("Justizämter", 1867, "a")
kg_verg, kg_erk = cases("Kreisgerichte", 1867, "b"), cases("Kreisgerichte", 1867, "a")
ratio_min = min(cases("Justizämter", y, "b") / cases("Justizämter", y, "a") for y in range(1864, 1868))
assert ja_verg > ja_erk and kg_verg > kg_erk

tot_conv = sum(r["total_convicted"] for r in ueb)
forest = sum(r["forest_convicted"] for r in ueb)
police = sum(r["police_convicted"] or 0 for r in ueb)
assert forest > police
forest_schleiz = sum(r["forest_convicted"] for r in ueb if r["kreisgericht"] == "Schleiz")
forest_schleiz_share = forest_schleiz / forest * 100
assert 75 < forest_schleiz_share < 85          # "vier Fünftel"
lob1 = next(r for r in ueb if r["court"] == "Lobenstein I")
gera1 = next(r for r in ueb if r["court"] == "Gera I")

def custody(year, haft=None, level=None, field="prisoners"):
    return sum(r[field] for r in gef if r["year"] == year and (haft is None or r["haftart"] == haft) and (level is None or r["level"] == level))

p64, p66, p67 = (custody(y) for y in (1864, 1866, 1867))
p_chg = (p67 / p66 - 1) * 100
d64, d67 = custody(1864, field="days"), custody(1867, field="days")
days_chg = (d67 / d64 - 1) * 100
pris_chg = (p67 / p64 - 1) * 100
avg_ja = custody(1867, "Strafhaft", "Justizämter", "days") / custody(1867, "Strafhaft", "Justizämter")
avg_kg = custody(1867, "Strafhaft", "Kreisgerichte", "days") / custody(1867, "Strafhaft", "Kreisgerichte")
strafe_ja = [custody(y, "Strafhaft", "Justizämter") for y in (1866, 1867)]

vor = {(r["measure_key"], r["year"]): r["value"] for r in staat}
vor64, vor67 = vor[("c", 1864)], vor[("c", 1867)]
vor_chg = (vor67 / vor64 - 1) * 100

print(dict(suits67=suits67, per1000=round(per1000, 1), ja_per=round(ja_per, 1), kg_per=round(kg_per, 1), ratio_min=round(ratio_min, 2),
           tot_conv=tot_conv, forest=forest, police=police, forest_schleiz=forest_schleiz, share=round(forest_schleiz_share, 1),
           lob1=(lob1["forest_convicted"], lob1["common_convicted"]), gera1=(gera1["forest_convicted"], gera1["common_convicted"]),
           prisoners=(p64, p66, p67), p_chg=round(p_chg, 1), pris_chg=round(pris_chg, 1), days=(d64, d67), days_chg=round(days_chg, 1),
           avg=(round(avg_ja, 1), round(avg_kg, 1)), strafe_ja=strafe_ja, vor=(vor64, vor67, round(vor_chg))))

# ---------------------------------------------------------------- texts
title = {"de": "Gerichte und Strafen 1864–1867", "en": "Courts and punishments, 1864–1867"}

verg_all = ja_verg + kg_verg
assert verg_all / suits67 > 0.5
summary = {
    "de": (f"Die Rechtspflege lag bei acht Justizämtern, zwei Kreisgerichten und den Staatsanwaltschaften. 1867 wurden {de(tot_conv)} Personen wegen Übertretungen verurteilt, {de(forest)} davon wegen Forstdiebstahls. "
           f"Von {de(suits67)} neuen förmlichen Rechtsstreitigkeiten endeten die meisten durch Vergleich. {de(p67)} Menschen kamen in Haft, {de(p_chg)} Prozent mehr als 1866."),
    "en": (f"Justice was administered by eight Justizämter (single-judge courts), two Kreisgerichte (district courts) and the public prosecutors. In 1867, {en(tot_conv)} persons were convicted of petty offences, {en(forest)} of them for forest theft. "
           f"Of {en(suits67)} new formal lawsuits most ended in a settlement. {en(p67)} people were taken into custody, {en(p_chg)} percent more than in 1866."),
}

findings = [
    {"de": (f"Auf 1.000 Einwohner kamen 1867 {de(per1000, 1)} neue förmliche Rechtsstreitigkeiten: {de(ja_per, 1)} vor den Justizämtern, {de(kg_per, 1)} vor den Kreisgerichten."),
     "en": (f"Per 1,000 inhabitants there were {en(per1000, 1)} new formal lawsuits in 1867: {en(ja_per, 1)} before the Justizämter, {en(kg_per, 1)} before the Kreisgerichte.")},
    {"de": (f"Die Staatsanwaltschaften leiteten 1867 {vor67} Voruntersuchungen ein, 1864 waren es {vor64}. Vor Kreisgerichten und Schwurgericht wurden 1867 {CONV['1867']} Personen verurteilt, 1865 waren es {CONV['1865']}."),
     "en": (f"The public prosecutors ordered {vor67} preliminary investigations in 1867, against {vor64} in 1864. {CONV['1867']} persons were convicted before the Kreisgerichte and the jury court in 1867, {CONV['1865']} in 1865.")},
    {"de": (f"Die Strafhaft dauerte bei den Justizämtern 1867 im Durchschnitt {de(avg_ja, 1)} Tage, bei den Kreisgerichten {de(avg_kg, 1)} Tage. "
            f"Die Zahl der Gefangenen stieg von 1864 bis 1867 um {de(pris_chg)} Prozent, die Hafttage um {de(days_chg)} Prozent."),
     "en": (f"Imprisonment lasted {en(avg_ja, 1)} days on average at the Justizämter in 1867, {en(avg_kg, 1)} days at the Kreisgerichte. "
            f"From 1864 to 1867 the number of prisoners rose by {en(pris_chg)} percent, the days of custody by {en(days_chg)} percent.")},
]

charts = [
    {"id": "c1", "dataset": "uebertretungen_1867",
     "title": {"de": "Forstdiebstahl brachte 1867 mehr Verurteilungen als alle polizeilichen Übertretungen, vier Fünftel im Kreisgerichtsbezirk Schleiz",
               "en": "Forest theft led to more convictions than all police offences, four fifths in the Schleiz district"},
     "caption": {"de": "Verurteilte Personen vor den Einzelrichtern 1867 nach Art der Übertretung. Bezirk Gera: Justizämter Gera I und II, Hohenleuben; Bezirk Schleiz: Schleiz, Lobenstein, Hirschberg. Quelle: S. 281, 287.",
                 "en": "Persons convicted before the single judges in 1867 by kind of offence. Gera district: Justizämter Gera I and II, Hohenleuben; Schleiz district: Schleiz, Lobenstein, Hirschberg. Source: pp. 281, 287."},
     "vegalite": C.c2},
    {"id": "c2", "dataset": "neue_prozesse",
     "title": {"de": "Neue Prozesse endeten deutlich häufiger durch Vergleich als durch Urteil",
               "en": "New lawsuits ended in a settlement much more often than in a judgment"},
     "caption": {"de": "Neue förmliche Rechtsstreitigkeiten je Jahr nach Ausgang. Für 1864 ergeben die Teilzahlen der Kreisgerichte 571, gedruckt sind 561. Quelle: S. 280–281, 284, 286.",
                 "en": "New formal lawsuits per year by outcome. For 1864 the parts for the Kreisgerichte add up to 571, the printed total is 561. Source: pp. 280–281, 284, 286."},
     "vegalite": C.c1},
    {"id": "c3", "dataset": "gefangene",
     "title": {"de": f"1867 kamen {de(p67)} Menschen in Haft, {de(p_chg)} Prozent mehr als 1866",
               "en": f"In 1867, {en(p67)} people were taken into custody, {en(p_chg)} percent more than in 1866"},
     "caption": {"de": "Im Jahr in Untersuchungs- oder Strafhaft genommene Personen bei den Justizämtern und Kreisgerichten zusammen, kein Stichtagsbestand. Quelle: S. 283, 286.",
                 "en": "Persons taken into pre-trial detention or imprisonment during the year at the Justizämter and Kreisgerichte together, not a count on a fixed date. Source: pp. 283, 286."},
     "vegalite": C.c3},
]

method = {
    "de": ("Grundlage ist Brückners »Statistik der Rechtspflege« (S. 283–289) für die Jahre 1864 bis 1867. Für die Rechtsstreitigkeiten wurden die Spalten der neuen förmlichen Rechtsstreitigkeiten und ihres Ausgangs (Erkenntnis, Vergleich, unerledigt) "
           "aus den Tabellen der Justizämter (S. 284) und der Kreisgerichte (S. 286) zusammengestellt; Einwohner je Gericht sind nicht gedruckt, daher beziehen sich die Raten auf die Landeseinwohner 1867 (87.974, S. 92). "
           "Die Verurteilten wegen Übertretungen stammen aus der Tabelle »Speciell für 1867« (S. 287); ein Strich gilt als keine Verurteilten. »Übrige gemeine Übertretungen« ist die Differenz der Verurteilten wegen gemeiner Übertretungen und wegen Forstdiebstahls. "
           "Die Gefangenen und Hafttage stammen aus den Tabellen Generalia (S. 283, 286); die durchschnittliche Haftdauer ist Hafttage geteilt durch Gefangene. Die Zahlen der Staatsanwaltschaften (S. 288) sind für beide Ämter addiert."),
    "en": ("The basis is Brückner’s “Statistics of the administration of justice” (pp. 283–289) for 1864 to 1867. For the lawsuits, the columns for new formal lawsuits and their outcome (judgment, settlement, unresolved) "
           "were compiled from the tables of the Justizämter (p. 284) and the Kreisgerichte (p. 286); inhabitants per court are not printed, so the rates refer to the principality’s population in 1867 (87,974, p. 92). "
           "The convictions for petty offences come from the table “Specially for 1867” (p. 287); a dash counts as no convictions. “Other common offences” is the difference between convictions for common offences and for forest theft. "
           "The prisoners and days of custody come from the General tables (pp. 283, 286); the average length of custody is days divided by prisoners. The figures of the public prosecutors (p. 288) are added up for both offices."),
}

caveats = [
    {"de": ("Brückner erklärt die Spalten nicht. Gezählt sind verurteilte Personen und die im Jahr in Haft genommenen Personen samt Hafttagen, kein Stichtagsbestand; Mehrfachhaft derselben Person ist nicht ausgeschlossen. "
            "Die Haftdauer ist ein Durchschnitt und sagt nichts über Einzelstrafen."),
     "en": ("Brückner does not explain the columns. The figures count persons convicted and persons taken into custody during the year with their days of custody, not a count on a fixed date; repeated custody of one person is not excluded. "
            "The length of custody is an average and says nothing about individual sentences.")},
    {"de": ("Im Druck stimmen einige Summen nicht: Für 1864 ergeben die Teilspalten der neuen Rechtsstreitigkeiten bei den Kreisgerichten 571 statt 561, bei den Justizämtern 2.015 statt 2.021. "
            "Die Summe der Strafhafttage der Kreisgerichte 1867 ist mit 3.201 gedruckt, die Einzelwerte ergeben 3.223. Verwendet sind die Werte der Teilspalten bzw. die gedruckte Summe."),
     "en": ("Some sums in the print do not add up: for 1864 the parts of the new lawsuits give 571 instead of 561 at the Kreisgerichte and 2,015 instead of 2,021 at the Justizämter; "
            "the days of imprisonment at the Kreisgerichte in 1867 are printed as 3,201, the parts give 3,223. The parts and the printed sum are used respectively.")},
    {"de": ("Dass Vergleiche häufig waren, fällt in die Zeit nach dem Gesetz vom 28. April 1863 über Friedensgerichte (S. 282); ein Zusammenhang ist eine Vermutung, Brückner äußert sich nicht dazu."),
     "en": ("That settlements were frequent falls in the time after the law of 28 April 1863 on courts of conciliation (p. 282); a connection is a conjecture, Brückner does not comment.")},
    {"de": ("Brückner führt die Mehrarbeit der Staatsanwaltschaften 1867 auf die Not der Arbeiterbevölkerung im reichenfelser Gebiet zurück (S. 289). "
            "Die Zugehörigkeit der Justizämter zu den Kreisgerichtsbezirken folgt S. 281; das Justizamt Hohenleuben gehört zum Bezirk Gera."),
     "en": ("Brückner attributes the extra work of the public prosecutors in 1867 to the hardship of the working population in the Reichenfels area (p. 289). "
            "The assignment of the Justizämter to the Kreisgericht districts follows p. 281; the Justizamt Hohenleuben belongs to the Gera district.")},
]

sources = uniq_sources(*[A[i]["sources"] for i in IDS], [{"page": "92", "block": "b1"}, {"page": "280", "block": "b5"}, {"page": "281", "block": "b1"}, {"page": "289", "block": "b2"}])

a = {
    "id": "rechtspflege",
    "title": title,
    "category": "justice",
    "section": "t1-4-4",
    "merges": IDS,
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "datasets": [ds_proz, ds_ueb, ds_gef, ds_staat],
    "charts": charts,
    "transcription_issues": [],
    "keywords": {
        "de": ["Rechtspflege", "Justizämter", "Kreisgerichte", "Prozesse", "Vergleich", "Forstdiebstahl", "Übertretungen", "Gefangene", "Staatsanwaltschaft", "Strafen"],
        "en": ["administration of justice", "courts", "lawsuits", "settlement", "forest theft", "petty offences", "prisoners", "public prosecutor", "punishment"]},
    "related": ["verfassung-verwaltung", "wald-holz", "staatsfinanzen", "armenwesen-stiftungen"],
    "generated_by": GENERATED_BY.format(n=len(IDS)),
    "date": DATE,
}
for i in IDS:
    a["transcription_issues"] += A[i].get("transcription_issues", [])
if not a.get("transcription_issues"):
    a.pop("transcription_issues", None)
check_limits(a)
write_analysis(a)
