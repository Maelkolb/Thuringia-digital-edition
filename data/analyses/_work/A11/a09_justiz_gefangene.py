"""A11-09: Gefangene und Hafttage bei Justizämtern und Kreisgerichten 1864-1867 (pp. 283, 286)."""
from common import *

g3 = grid("283", "b4")
g6 = grid("286", "b3")
N = lambda x: num(x) or 0
YEARS = (1864, 1865, 1866, 1867)

# Einzelgerichte: rows idx 10..13 = Summe 1867, 1866, 1865, 1864 ; cols 7 U, 8 S, 9 TageU, 10 TageS
ez = {1867: g3[10], 1866: g3[11], 1865: g3[12], 1864: g3[13]}
assert g3[10][0] == "Summe 1867" and g3[13][0] == "1864"
# Kreisgerichte: first panel idx 3..6 = 1867..1864 ; cols 6 U, 7 S, 8 TageU ; second panel idx 10..13: [TageS, Amtsrevisionen]
kg1 = {1867: g6[3], 1866: g6[4], 1865: g6[5], 1864: g6[6]}
kg2 = {1867: g6[10], 1866: g6[11], 1865: g6[12], 1864: g6[13]}
assert g6[3][0] == "Summe 1867" and g6[6][0] == "1864" and N(kg2[1867][0]) == 3201 and N(kg2[1864][0]) == 1999

COMBO = [
    ("a", "Untersuchungshaft, Justizämter", "Pre-trial detention, Justizämter"),
    ("b", "Strafhaft, Justizämter", "Imprisonment, Justizämter"),
    ("c", "Untersuchungshaft, Kreisgerichte", "Pre-trial detention, Kreisgerichte"),
    ("d", "Strafhaft, Kreisgerichte", "Imprisonment, Kreisgerichte"),
]
yearly = []
for y in YEARS:
    vals = {"a": (N(ez[y][7]), N(ez[y][9])), "b": (N(ez[y][8]), N(ez[y][10])),
            "c": (N(kg1[y][6]), N(kg1[y][8])), "d": (N(kg1[y][7]), N(kg2[y][0]))}
    for k, de, en in COMBO:
        p, d = vals[k]
        yearly.append([y, k, de, en, p, d, round(d / p, 1)])
V = {(r[0], r[1]): r for r in yearly}

# per Justizamt 1867
names = ["Gera I", "Gera II", "Hirschberg", "Hohenleuben", "Lobenstein I", "Lobenstein II", "Schleiz I", "Schleiz II"]
rows = {r[0].rstrip("."): r for r in g3[2:10]}
courts = []
for n in names:
    r = rows[n]
    u, s, tu, ts = N(r[7]), N(r[8]), N(r[9]), N(r[10])
    courts.append([n, "a", "Untersuchungshaft", "Pre-trial detention", u, tu])
    courts.append([n, "b", "Strafhaft", "Imprisonment", s, ts])
assert sum(c[4] for c in courts if c[1] == "a") == 164 and sum(c[4] for c in courts if c[1] == "b") == 926
assert sum(c[5] for c in courts if c[1] == "b") == 5232

pct = lambda a, b: 100 * a / b
tot = lambda y, ks: sum(V[(y, k)][4] for k in ks)
days = lambda y, ks: sum(V[(y, k)][5] for k in ks)
b_chg = pct(V[(1867, "b")][4] - V[(1864, "b")][4], V[(1864, "b")][4])
b_chg67 = pct(V[(1867, "b")][4] - V[(1866, "b")][4], V[(1866, "b")][4])
top = max((c for c in courts if c[1] == "b"), key=lambda c: c[4])
topu = max((c for c in courts if c[1] == "a"), key=lambda c: c[4])
print(b_chg, b_chg67, top, topu, tot(1867, "abcd"), tot(1864, "abcd"), days(1867, "abcd"), days(1864, "abcd"))


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "justiz-gefangene-hafttage-1864-1867",
    "title": bi("Gefangene und Hafttage bei Justizämtern und Kreisgerichten 1864–1867", "Prisoners and days of detention at the Justizämter and Kreisgerichte, 1864–1867"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "283", "block": "b4", "rows": "r3-r14"}, {"page": "286", "block": "b3", "rows": "r2-r14"}, {"page": "287", "block": "b4", "rows": "r5-r6", "note": "nur für den Vergleich der Verurteilungen 1866/1867"}],
    "summary": bi(
        f"Die Tabellen »Generalia« der Justizämter und der Kreisgerichte nennen die Zahl der Untersuchungs- und Strafgefangenen und die Hafttage. 1867 zählten die Justizämter {D(tot(1867,'ab'))} und die Kreisgerichte {D(tot(1867,'cd'))} Gefangene; die Strafgefangenen der Justizämter nahmen gegenüber 1866 stark zu. Die Auswertung stellt Zahl und durchschnittliche Haftdauer gegenüber.",
        f"The “Generalia” tables of the Justizämter and the Kreisgerichte give the number of pre-trial and convicted prisoners and the days of detention. In 1867 the Justizämter counted {E(tot(1867,'ab'))} prisoners and the Kreisgerichte {E(tot(1867,'cd'))}; the convicted prisoners of the Justizämter rose sharply against 1866. The analysis sets numbers against the average length of detention.",
    ),
    "method": bi(
        "Für die Justizämter wurden die Summenzeilen 1867, 1866, 1865, 1864 der Tabelle S. 283 verwendet (Spalten Untersuchungsgefangene, Strafgefangene, Hafttage), für die Kreisgerichte die entsprechenden Zeilen der Tabelle S. 286; deren Spalte »Tage der Haft: Strafgefangene« steht im Druck auf dem zweiten Blatt der Tabelle. Die durchschnittliche Haftdauer = Hafttage : Gefangene (abgeleitet). Die Verteilung auf die acht Justizämter bezieht sich auf 1867.",
        "For the Justizämter the total rows 1867, 1866, 1865, 1864 of the table on p. 283 were used (columns pre-trial prisoners, convicted prisoners, days of detention), for the Kreisgerichte the corresponding rows of the table on p. 286; its column “days of detention: convicted prisoners” is printed on the second panel of the table. The average length of detention = days : prisoners (derived). The distribution among the eight Justizämter refers to 1867.",
    ),
    "findings": [
        bi(f"Die Zahl der Strafgefangenen der Justizämter sprang von {D(V[(1866,'b')][4])} (1866) auf {D(V[(1867,'b')][4])} (1867), also um {D(b_chg67,0)} %; gegenüber 1864 ({D(V[(1864,'b')][4])}) beträgt der Zuwachs {D(b_chg,0)} %. Im selben Jahr stiegen die Verurteilungen wegen Übertretungen um {D(100*(1834-1457)/1457,1)} % (S. 287), also deutlich weniger.",
           f"The number of convicted prisoners of the Justizämter jumped from {E(V[(1866,'b')][4])} (1866) to {E(V[(1867,'b')][4])} (1867), i.e. by {E(b_chg67,0)} %; against 1864 ({E(V[(1864,'b')][4])}) the increase is {E(b_chg,0)} %. In the same year convictions for minor offences rose by {E(100*(1834-1457)/1457,1)} % (p. 287), i.e. considerably less."),
        bi(f"Bei den Justizämtern dauerte die Strafhaft 1867 im Durchschnitt {D(V[(1867,'b')][6],1)} Tage, bei den Kreisgerichten {D(V[(1867,'d')][6],1)} Tage; die Untersuchungshaft {D(V[(1867,'a')][6],1)} bzw. {D(V[(1867,'c')][6],1)} Tage.",
           f"At the Justizämter imprisonment lasted on average {E(V[(1867,'b')][6],1)} days in 1867, at the Kreisgerichte {E(V[(1867,'d')][6],1)} days; pre-trial detention {E(V[(1867,'a')][6],1)} and {E(V[(1867,'c')][6],1)} days respectively."),
        bi(f"Die Hafttage aller vier Gruppen zusammen stiegen von {D(days(1864,'abcd'))} (1864) auf {D(days(1867,'abcd'))} (1867), also um {D(pct(days(1867,'abcd')-days(1864,'abcd'), days(1864,'abcd')),1)} %.",
           f"Days of detention of all four groups together rose from {E(days(1864,'abcd'))} (1864) to {E(days(1867,'abcd'))} (1867), i.e. by {E(pct(days(1867,'abcd')-days(1864,'abcd'), days(1864,'abcd')),1)} %."),
        bi(f"Unter den Justizämtern hatte {top[0]} 1867 mit {D(top[4])} die meisten Strafgefangenen ({D(pct(top[4], 926),1)} % aller) und {'ebenfalls' if topu[0]==top[0] else topu[0]} mit {D(topu[4])} die meisten Untersuchungsgefangenen ({D(pct(topu[4], 164),1)} %).",
           f"Among the Justizämter, {top[0]} had the most convicted prisoners in 1867 ({E(top[4])}, {E(pct(top[4], 926),1)} % of all) and {'also' if topu[0]==top[0] else topu[0]} the most pre-trial prisoners ({E(topu[4])}, {E(pct(topu[4], 164),1)} %)."),
    ],
    "caveats": [
        bi("Gezählt sind die im Jahr in Haft genommenen Personen und die Hafttage, kein Stichtagsbestand; Mehrfachhaft derselben Person ist nicht ausgeschlossen. Die Haftdauer ist ein Durchschnitt aus Tagen und Personen und sagt nichts über Einzelstrafen.",
           "The figures count persons taken into custody during the year and days of detention, not a snapshot stock; repeated detention of the same person is not excluded. The duration is an average of days and persons and says nothing about individual sentences."),
        bi("Bei den Kreisgerichten ist die gedruckte Summe der Strafhafttage 1867 (3201) kleiner als die Summe der Einzelwerte (1777 + 1446 = 3223); hier wird die gedruckte Summe verwendet. Die Tage der Untersuchungshaft stimmen (1448 + 1996 = 3444).",
           "For the Kreisgerichte the printed total of imprisonment days in 1867 (3201) is smaller than the sum of the individual values (1777 + 1446 = 3223); the printed total is used here. The days of pre-trial detention agree (1448 + 1996 = 3444)."),
    ],
    "datasets": [
        {"name": "yearly", "title": bi("Gefangene und Hafttage nach Ebene und Haftart", "Prisoners and days of detention by court level and kind of detention"),
         "columns": [col("year", "Jahr", "Year", "integer"), col("kind_key", "Kürzel", "Key", "string"),
                     col("kind_de", "Gruppe", "Group", "string"), col("kind_en", "Gruppe (englisch)", "Group (English)", "string"),
                     col("prisoners", "Gefangene", "Prisoners", "integer", "Personen"), col("days", "Tage der Haft", "Days of detention", "integer", "Tage"),
                     col("avg_days", "Durchschnittliche Haftdauer", "Average length of detention", "number", "Tage", derived=True)],
         "rows": yearly, "source_refs": [{"page": "283", "block": "b4", "rows": "r11-r14"}, {"page": "286", "block": "b3", "rows": "r4-r7"}, {"page": "286", "block": "b3", "rows": "r11-r14"}]},
        {"name": "courts", "title": bi("Gefangene und Hafttage je Justizamt, 1867", "Prisoners and days of detention by Justizamt, 1867"),
         "columns": [col("court", "Gericht", "Court", "string"), col("kind_key", "Kürzel", "Key", "string"),
                     col("kind_de", "Haftart", "Kind", "string"), col("kind_en", "Haftart (englisch)", "Kind (English)", "string"),
                     col("prisoners", "Gefangene", "Prisoners", "integer", "Personen"), col("days", "Tage der Haft", "Days of detention", "integer", "Tage")],
         "rows": courts, "source_refs": [{"page": "283", "block": "b4", "rows": "r3-r10"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "yearly",
         "title": bi("Gefangene pro Jahr nach Gerichtsebene und Haftart", "Prisoners per year by court level and kind of detention"),
         "caption": bi("Im Jahr in Haft genommene Personen. Der Zuwachs 1867 liegt bei den Strafgefangenen der Justizämter.", "Persons taken into custody during the year. The increase in 1867 is among the convicted prisoners of the Justizämter."),
         "vegalite": {
             "height": 300,
             "mark": {"type": "bar", "width": 55},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "prisoners", "type": "quantitative", "title": bi("Gefangene", "Prisoners"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("kind", "Gruppe", "Group"), tt("prisoners", "Gefangene", "Prisoners"), tt("days", "Tage der Haft", "Days")]}}},
        {"id": "c2", "dataset": "yearly",
         "title": bi("Durchschnittliche Haftdauer", "Average length of detention"),
         "caption": bi("Hafttage je Gefangenem. Bei den Kreisgerichten ist die durchschnittliche Haft in allen vier Jahren deutlich länger als bei den Justizämtern.", "Days of detention per prisoner. At the Kreisgerichte the average detention is markedly longer than at the Justizämter in all four years."),
         "vegalite": {
             "height": 280,
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "avg_days", "type": "quantitative", "title": bi("Tage je Gefangenem", "Days per prisoner"), "scale": {"zero": True}},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("kind", "Gruppe", "Group"), {"field": "avg_days", "title": bi("Tage je Gefangenem", "Days per prisoner"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "courts",
         "title": bi("Gefangene der Justizämter 1867", "Prisoners of the Justizämter in 1867"),
         "caption": bi("Im Jahr 1867 in Haft genommene Personen je Justizamt (Untersuchungs- und Strafhaft).", "Persons taken into custody in 1867 per Justizamt (pre-trial detention and imprisonment)."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": {"field": "prisoners", "op": "sum", "order": "descending"}},
                 "x": {"field": "prisoners", "type": "quantitative", "title": bi("Gefangene", "Prisoners"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [tt("court", "Gericht", "Court"), ttf("kind", "Haftart", "Kind"), tt("prisoners", "Gefangene", "Prisoners"), tt("days", "Tage der Haft", "Days")]}}},
    ],
    "keywords": {"de": ["Gefangene", "Haft", "Hafttage", "Untersuchungshaft", "Strafhaft", "Gefängnis", "Justizamt", "Kreisgericht", "Rechtspflege"],
                 "en": ["prisoners", "detention", "days of detention", "pre-trial detention", "imprisonment", "prison", "Justizamt", "Kreisgericht"]},
}
write(ana)
