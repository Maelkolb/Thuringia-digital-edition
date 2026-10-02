"""A04: Eheschliessungen 1858-1867 (pp. 112-113)."""
from common import *

YEARS = list(range(1858, 1868))
g = grid("112", "b5")
# block 1 (Gera, Schleiz): rows g[2:12], avg g[12]; block 2 (Lobenstein-Ebersdorf, Fuerstenthum): rows g[14:24], avg g[24]
LAYOUT = [("Gera", g[2:12], g[12], 1), ("Schleiz", g[2:12], g[12], 7),
          ("Lobenstein-Ebersdorf", g[14:24], g[24], 1), ("Reuß j. L.", g[14:24], g[24], 7)]
AREA_OFF = {"Städte": (0, 3), "Landorte": (1, 4), "Zusammen": (2, 5)}   # (pairs, pct)

marr, marr_mean = [], []
for k, rows, avg, j0 in LAYOUT:
    for r in rows:
        y = int(r[0])
        for area, (dn, dp) in AREA_OFF.items():
            marr.append([y, k, area, inum(r[j0 + dn]), num(r[j0 + dp])])
    for area, (dn, dp) in AREA_OFF.items():
        marr_mean.append([k, area, num(avg[j0 + dn]), num(avg[j0 + dp])])

# comparison with other Thuringian states (p.113 b2)
t = grid("113", "b2")
states = []
for row in t:
    for i in (0, 2):
        name, v = row[i], num(row[i + 1])
        states.append([name, v, "Reuß j. L." if name == "Reuß j. L." else "übrige Staaten"])
states.sort(key=lambda r: -r[1])
print(states)

# ---- numbers for the texts
pct = {(r[0], r[1]): r[4] for r in marr if r[2] == "Zusammen"}
pairs = {(r[0], r[1]): r[3] for r in marr if r[2] == "Zusammen"}
mean_z = {r[0]: r[3] for r in marr_mean if r[1] == "Zusammen"}
mean_a = {(r[0], r[1]): r[3] for r in marr_mean}
fue_pct = {y: pct[(y, "Reuß j. L.")] for y in YEARS}
fue_n = {y: pairs[(y, "Reuß j. L.")] for y in YEARS}
lo = min(fue_pct, key=fue_pct.get)
hi = max(fue_pct, key=fue_pct.get)
nhi = max(fue_n, key=fue_n.get)
nlo = min(fue_n, key=fue_n.get)
print(mean_z, fue_pct, fue_n)
print({k: (mean_a[(k, 'Städte')], mean_a[(k, 'Landorte')]) for k in DISTRICTS})
d_hi = max(DISTRICTS[:3], key=lambda k: mean_z[k])
d_lo = min(DISTRICTS[:3], key=lambda k: mean_z[k])
assert d_hi == "Schleiz" and d_lo == "Lobenstein-Ebersdorf"
st = {s[0]: s[1] for s in states}
others = [s[1] for s in states if s[0] != "Reuß j. L."]
assert st["Reuß j. L."] > max(others)

SRC = ref("112", "b5", "r3-t25")
ST_EN = {"S.-Coburg": "Saxe-Coburg", "S.-Gotha": "Saxe-Gotha", "S.-Altenburg": "Saxe-Altenburg", "S.-Meiningen": "Saxe-Meiningen",
         "S.-Weimar": "Saxe-Weimar", "Reuß j. L.": "Reuss j. L."}
ana = {
    "id": "bevoelkerung-eheschliessungen-1858-1867",
    "title": bi("Eheschließungen 1858–1867", "Marriages 1858–1867"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [ref("112", "b4"), SRC, ref("113", "b1"), ref("113", "b2", "r1-r4"), ref("113", "b3")],
    "summary": bi(
        f"Brückner gibt die Zahl der getrauten Paare 1858–1867 für die drei Landrathsbezirke und das Fürstenthum an, getrennt nach Städten und Landorten, dazu den Anteil an der Bevölkerung, und vergleicht ihn mit anderen thüringischen Staaten. Im Fürstenthum kamen im Zehnjahresmittel {fde(mean_z['Reuß j. L.'])} getraute Paare auf 100 Einwohner, mehr als in jedem der verglichenen Staaten; die Jahreswerte reichen von {fde(fue_pct[lo])} ({lo}) bis {fde(fue_pct[hi])} ({hi}).",
        f"Brückner gives the number of married couples for 1858–1867 for the three districts and the principality, split into towns and rural places, together with the share of the population, and compares it with other Thuringian states. In the principality the ten-year mean was {fen(mean_z['Reuß j. L.'])} married couples per 100 inhabitants, more than in any of the states compared; the annual values range from {fen(fue_pct[lo])} ({lo}) to {fen(fue_pct[hi])} ({hi})."),
    "method": bi(
        "Die Tabelle S. 112 (zwei Blöcke: Gera und Schleiz, Lobenstein-Ebersdorf und Fürstenthum) enthält je Jahr die getrauten Paare in Städten, Landorten und zusammen sowie dieselben Zahlen in Procenten der Bevölkerung. Alle Werte stehen wie gedruckt im Datensatz; die gedruckten Zehnjahresmittel bilden einen eigenen Datensatz. Der Staatenvergleich stammt aus S. 113. Die Procentzahl bezieht sich auf die Zahl der Paare, nicht der Eheschließenden.",
        "The table on p. 112 (two blocks: Gera and Schleiz, Lobenstein-Ebersdorf and the principality) gives, for each year, the married couples in towns, rural places and combined, and the same figures as a percentage of the population. All values are in the dataset as printed; the printed ten-year means form a separate dataset. The comparison of states comes from p. 113. The percentage refers to the number of couples, not of persons marrying."),
    "findings": [
        bi(f"Die Zahl der Trauungen im Fürstenthum schwankt zwischen {fue_n[nlo]} ({nlo}) und {fue_n[nhi]} ({nhi}); im Zehnjahresmittel sind es {fde(854.8, 1)} Paare im Jahr. Auf 100 Einwohner kamen {fde(fue_pct[lo])} ({lo}) bis {fde(fue_pct[hi])} ({hi}).",
           f"The number of marriages in the principality varies between {fint_en(fue_n[nlo])} ({nlo}) and {fint_en(fue_n[nhi])} ({nhi}); the ten-year mean is {fen(854.8, 1)} couples a year. Per 100 inhabitants the range is {fen(fue_pct[lo])} ({lo}) to {fen(fue_pct[hi])} ({hi})."),
        bi(f"Schleiz hat mit {fde(mean_z['Schleiz'])} den höchsten, Lobenstein-Ebersdorf mit {fde(mean_z['Lobenstein-Ebersdorf'])} den niedrigsten Mittelwert unter den Landestheilen (Gera {fde(mean_z['Gera'])}).",
           f"Schleiz has the highest mean among the districts ({fen(mean_z['Schleiz'])}), Lobenstein-Ebersdorf the lowest ({fen(mean_z['Lobenstein-Ebersdorf'])}; Gera {fen(mean_z['Gera'])})."),
        bi(f"Im Fürstenthum wird auf dem Land deutlich öfter geheiratet als in den Städten ({fde(mean_a[('Reuß j. L.', 'Landorte')])} gegenüber {fde(mean_a[('Reuß j. L.', 'Städte')])}); der Abstand ist in Gera am größten ({fde(mean_a[('Gera', 'Landorte')])} gegenüber {fde(mean_a[('Gera', 'Städte')])}). In Schleiz ({fde(mean_a[('Schleiz', 'Städte')])} gegenüber {fde(mean_a[('Schleiz', 'Landorte')])}) und in Lobenstein-Ebersdorf ({fde(mean_a[('Lobenstein-Ebersdorf', 'Städte')])} gegenüber {fde(mean_a[('Lobenstein-Ebersdorf', 'Landorte')])}) sind die Unterschiede gering.",
           f"In the principality marriages are clearly more frequent in the countryside than in the towns ({fen(mean_a[('Reuß j. L.', 'Landorte')])} against {fen(mean_a[('Reuß j. L.', 'Städte')])}); the gap is widest in Gera ({fen(mean_a[('Gera', 'Landorte')])} against {fen(mean_a[('Gera', 'Städte')])}). In Schleiz ({fen(mean_a[('Schleiz', 'Städte')])} against {fen(mean_a[('Schleiz', 'Landorte')])}) and in Lobenstein-Ebersdorf ({fen(mean_a[('Lobenstein-Ebersdorf', 'Städte')])} against {fen(mean_a[('Lobenstein-Ebersdorf', 'Landorte')])}) the differences are small."),
        bi(f"Unter den thüringischen Staaten, die Brückner vergleicht, steht Reuß j. L. mit {fde(st['Reuß j. L.'])} an der Spitze; die übrigen liegen zwischen {fde(min(others))} (Sachsen-Coburg) und {fde(max(others))} (Schwarzburg-Sondershausen).",
           f"Among the Thuringian states Brückner compares, Reuss j. L. is at the top with {fen(st['Reuß j. L.'])}; the others lie between {fen(min(others))} (Saxe-Coburg) and {fen(max(others))} (Schwarzburg-Sondershausen)."),
    ],
    "caveats": [
        bi("Die Tabelle enthält mehrere Druckfehler oder Unstimmigkeiten: Das Mittel der Gera-Landorte steht als 252,2 (die zehn Jahreswerte ergeben 255,2; 85,0 + 255,2 = 340,2 passt zur gedruckten Summe); die Mittelzeile des Blocks Lobenstein-Ebersdorf/Fürstenthum ist mit „1858–97“ überschrieben; für Schleiz 1861 (Städte) steht 1,42 Procent bei 101 Paaren, was zu den Nachbarjahren nicht passt (≈ 1,3 zu erwarten).",
           "The table contains several misprints or inconsistencies: the mean for Gera rural places is printed as 252.2 (the ten annual values give 255.2; 85.0 + 255.2 = 340.2 fits the printed total); the mean row of the block Lobenstein-Ebersdorf/principality is headed “1858–97”; for Schleiz 1861 (towns) 1.42 per cent is printed for 101 couples, which does not fit the neighbouring years (about 1.3 expected)."),
        bi("Die Quote ist auf die Gesamtbevölkerung bezogen, nicht auf die heiratsfähigen Altersklassen; Altersstruktur und Wanderungen sind nicht berücksichtigt. Brückner nennt keinen Grund für das Maximum 1864 (Gera 463 Paare).",
           "The rate refers to the total population, not to the marriageable age groups; age structure and migration are not taken into account. Brückner gives no reason for the maximum in 1864 (Gera: 463 couples)."),
    ],
    "datasets": [
        {"name": "marriages", "title": bi("Getraute Paare nach Landrathsbezirk, Städten und Landorten", "Married couples by district, towns and rural places"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landrathsbezirk", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Zusammen"),
                     col("pairs", "Getraute Paare", "Married couples", "integer", "Paare"),
                     col("pct_pop", "Procente der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": marr, "source_refs": [ref("112", "b5", "r3-r12"), ref("112", "b5", "r15-r24")]},
        {"name": "marriages_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landrathsbezirk", "District", "string"),
                     col("area", "Gebiet", "Area", "string"),
                     col("pairs", "Getraute Paare (Jahresmittel)", "Married couples (annual mean)", "number", "Paare"),
                     col("pct_pop", "Procente der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": marr_mean, "source_refs": [ref("112", "b5", "t13"), ref("112", "b5", "t25")]},
        {"name": "marriages_states", "title": bi("Trauungsziffer thüringischer Staaten", "Marriage rate of Thuringian states"),
         "columns": [col("state", "Staat", "State", "string"),
                     col("pct_pop", "Trauungsziffer (durchschnittlich)", "Marriage rate (average)", "number", "% der Bevölkerung"),
                     col("group", "Gruppe", "Group", "string")],
         "rows": states, "source_refs": [ref("113", "b2", "r1-r4")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "marriages",
         "title": bi("Getraute Paare auf 100 Einwohner", "Married couples per 100 inhabitants"),
         "caption": bi("Je Landrathsbezirk und für das ganze Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1858–1867.",
                       "By district and for the whole principality (Reuß j. L.), towns and rural places combined, 1858–1867."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.area == 'Zusammen'"}],
                      "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "pct_pop", "type": "quantitative", "title": bi("Paare je 100 Einwohner", "couples per 100 inhabitants"), "scale": {"domain": [0.6, 1.4]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"),
                                      tip("pairs", "Getraute Paare", "Married couples"),
                                      tip("pct_pop", "Paare je 100 Einwohner", "Couples per 100 inhabitants", ".2f")]}}},
        {"id": "c2", "dataset": "marriages",
         "title": bi("Zahl der Trauungen im Fürstenthum", "Number of marriages in the principality"),
         "caption": bi("Getraute Paare in Städten und Landorten, übereinander gestapelt; die Gesamthöhe ist die Zahl im Fürstenthum.",
                       "Married couples in towns and rural places, stacked; the total height is the number for the principality."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.district == 'Reuß j. L.' && datum.area != 'Zusammen'"}],
                      "mark": "bar",
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "pairs", "type": "quantitative", "title": bi("getraute Paare", "married couples"), "stack": "zero"},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "order": {"field": "area", "type": "nominal", "sort": "descending"},
                          "tooltip": [tip("year", "Jahr", "Year"), tip("area", "Gebiet", "Area"), tip("pairs", "Getraute Paare", "Married couples")]}}},
        {"id": "c3", "dataset": "marriages_mean",
         "title": bi("Städte und Landorte im Vergleich", "Towns and rural places compared"),
         "caption": bi("Gedrucktes Zehnjahresmittel 1858–1867, getraute Paare auf 100 Einwohner. In Gera ist der Abstand am größten, in Schleiz und Lobenstein-Ebersdorf gering.",
                       "Printed ten-year mean 1858–1867, married couples per 100 inhabitants. The gap is widest in Gera and small in Schleiz and Lobenstein-Ebersdorf."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.area != 'Zusammen'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": AREAS},
                          "y": {"field": "pct_pop", "type": "quantitative", "title": bi("Paare je 100 Einwohner", "couples per 100 inhabitants")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("area", "Gebiet", "Area"),
                                      tip("pct_pop", "Paare je 100 Einwohner", "Couples per 100 inhabitants", ".2f")]}}},
        {"id": "c4", "dataset": "marriages_states",
         "title": bi("Reuß j. L. im Vergleich mit thüringischen Staaten", "Reuß j. L. compared with Thuringian states"),
         "caption": bi("Durchschnittliche Trauungsziffer (Paare je 100 Einwohner) nach Brückner S. 113; Zeitraum der übrigen Staaten nicht angegeben. Reuß j. L. ist hervorgehoben.",
                       "Average marriage rate (couples per 100 inhabitants) after Brückner p. 113; period of the other states not stated. Reuß j. L. is highlighted."),
         "vegalite": {"height": 260, "mark": "bar",
                      "encoding": {
                          "y": {"field": "state", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelExpr": lab_expr(ST_EN), "labelLimit": 300}},
                          "x": {"field": "pct_pop", "type": "quantitative", "title": bi("Paare je 100 Einwohner", "couples per 100 inhabitants")},
                          "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige Staaten", "Reuß j. L."]}, "legend": None},
                          "tooltip": [tip("state", "Staat", "State"), tip("pct_pop", "Paare je 100 Einwohner", "Couples per 100 inhabitants", ".2f")]}}},
    ],
    "transcription_issues": [
        {"page": "112", "block": "b5", "cell": "r13c3", "transcribed": "252,2", "facsimile": "252,2", "checked_facsimile": True,
         "note": "Printed mean of the Gera rural couples; the ten annual values (187, 249, 299, 264, 232, 250, 324, 260, 251, 236) sum to 2552, i.e. 255,2. Printer's error in the original."},
        {"page": "112", "block": "b5", "cell": "r25c1", "transcribed": "Durchschn. 1858-97", "facsimile": "1858—97", "checked_facsimile": True,
         "note": "Label of the mean row of the lower block as printed (should read 1858-67)."},
        {"page": "112", "block": "b5", "cell": "r6c11", "transcribed": "1,42", "facsimile": "1,42", "checked_facsimile": True,
         "note": "Schleiz 1861, towns: 101 couples = 1,42 % would imply a town population of about 7,100 (neighbouring years about 7,700); printed so."},
    ],
    "keywords": {"de": ["Eheschließungen", "Trauungen", "Heiraten", "Trauungsziffer", "Stadt und Land", "Thüringische Staaten", "Bevölkerungsstatistik"],
                 "en": ["marriages", "marriage rate", "weddings", "town and country", "Thuringian states", "population statistics"]},
    "related": ["bevoelkerung-geburten-1858-1867", "bevoelkerung-sterblichkeit-1858-1867", "bevoelkerung-natuerlicher-zuwachs-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
