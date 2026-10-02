"""A02: uneheliche Geburten 1858-1867 (pp. 109-110)."""
import re
from common import *

YEARS = list(range(1858, 1868))
g = grid("109", "b1")
BLOCKS = {"Gera": (4, 14, "r5-r14", "r15"), "Schleiz": (16, 26, "r17-r26", "r27"),
          "Lobenstein-Ebersdorf": (28, 38, "r29-r38", "r39"), "Reuß j. L.": (40, 50, "r41-r50", "r51")}
AREA_COLS = {"Städte": (1, 2, 3), "Landorte": (4, 5, 6), "Zusammen": (7, 8, 9)}

illegit, illegit_mean = [], []
for k, (a, b, _, _) in BLOCKS.items():
    for r in g[a:b]:
        y = int(r[0])
        for area, (jn, jl, ju) in AREA_COLS.items():
            illegit.append([y, k, area, inum(r[jn]), num(r[jl]), num(r[ju])])
    avg = g[b]
    assert avg[0].startswith("1858")
    for area, (jn, jl, ju) in AREA_COLS.items():
        illegit_mean.append([k, area, num(avg[jn]), num(avg[jl]), num(avg[ju])])

# five-year halves (derived: simple mean of the printed annual shares for 'Zusammen')
halves = []
for k in DISTRICTS:
    vals = {r[0]: r[5] for r in illegit if r[1] == k and r[2] == "Zusammen"}
    halves.append([k, "1858–1862", round(sum(vals[y] for y in range(1858, 1863)) / 5, 2)])
    halves.append([k, "1863–1867", round(sum(vals[y] for y in range(1863, 1868)) / 5, 2)])
print(halves)

# comparison with other states (p.110 b3)
t = grid("110", "b3")
states = []
def pv(s):
    return float(re.search(r"(\d+,\d+)", s).group(1).replace(",", "."))
for row in t:
    if row[0]:
        states.append([row[0], pv(row[1]), "übrige Staaten"])
    if row[2] == "Reuß j. L.":
        states.append(["Reuß j. L. 1858–64", pv(row[3]), "Reuß j. L."])
    elif row[2]:
        states.append([row[2], pv(row[3]), "übrige Staaten"])
    elif "1858—67" in row[3]:
        states.append(["Reuß j. L. 1858–67", pv(row[3]), "Reuß j. L."])
states.sort(key=lambda r: -r[1])
print(states)

# ------------------------------------------------------------------ numbers for the texts
mean_zus = {r[0]: r[4] for r in illegit_mean if r[1] == "Zusammen"}
mean_st = {(r[0], r[1]): r[4] for r in illegit_mean}
fue = {r[0]: r[5] for r in illegit if r[1] == "Reuß j. L." and r[2] == "Zusammen"}
h = {(r[0], r[1]): r[2] for r in halves}
n_better = sum(h[(k, "1863–1867")] < h[(k, "1858–1862")] for k in DISTRICTS)
rural_hi = sum(mean_st[(k, "Landorte")] > mean_st[(k, "Städte")] for k in DISTRICTS)
rank_vals = sorted([s[1] for s in states if s[0] != "Reuß j. L. 1858–64"], reverse=True)
rank = rank_vals.index(mean_zus["Reuß j. L."]) + 1
n_states = len(rank_vals)
print(mean_zus, mean_st, fue[1858], fue[1867], h, n_better, rural_hi, rank, n_states)
assert n_better == 4 and rural_hi == 4
drop = {k: h[(k, '1858–1862')] - h[(k, '1863–1867')] for k in DISTRICTS[:3]}
assert max(drop, key=drop.get) == 'Schleiz' and min(drop, key=drop.get) == 'Lobenstein-Ebersdorf', drop
lo_y = min(fue, key=fue.get)
hi_y = max(fue, key=fue.get)
st = {s[0]: s[1] for s in states}

SRC = ref("109", "b1", "r5-r51")
ST_EN = {"Preussen": "Prussia", "Sachsen": "Saxony (kingdom)", "Bayern": "Bavaria", "Sachsen-Gotha": "Saxe-Gotha",
         "Sachsen-Weimar": "Saxe-Weimar", "Sachsen-Altenburg": "Saxe-Altenburg", "Sachsen-Meiningen": "Saxe-Meiningen",
         "Sachsen-Coburg": "Saxe-Coburg", "Reuß j. L. 1858–64": "Reuss j. L. 1858–64", "Reuß j. L. 1858–67": "Reuss j. L. 1858–67"}

ana = {
    "id": "bevoelkerung-uneheliche-geburten-1858-1867",
    "title": bi("Uneheliche Geburten 1858–1867", "Illegitimate births 1858–1867"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [SRC, ref("110", "b1"), ref("110", "b2"), ref("110", "b3", "r1-r6"), ref("110", "b5"), ref("110", "b6"), ref("107", "b6")],
    "summary": bi(
        f"Brückner weist für 1858–1867 die unehelichen Geburten je Landestheil, getrennt nach Städten und Landorten, absolut und als Anteil an allen Geborenen aus und stellt das Land neben andere Staaten. Der Anteil lag im Fürstenthum im gedruckten Mittel bei {fde(mean_zus['Reuß j. L.'])} Procent, am höchsten in Lobenstein-Ebersdorf ({fde(mean_zus['Lobenstein-Ebersdorf'])}), am niedrigsten in Gera ({fde(mean_zus['Gera'])}); er sank im Lauf der zehn Jahre in allen Landestheilen.",
        f"For 1858–1867 Brückner gives illegitimate births per district, split into towns and rural places, in absolute numbers and as a share of all births, and compares the principality with other states. The printed ten-year mean for the principality is {fen(mean_zus['Reuß j. L.'])} per cent, highest in Lobenstein-Ebersdorf ({fen(mean_zus['Lobenstein-Ebersdorf'])}), lowest in Gera ({fen(mean_zus['Gera'])}); the share fell in every district over the ten years."),
    "method": bi(
        "Die Tabelle S. 109 enthält je Landestheil und für das Fürstenthum die unehelichen Geborenen (Zahl) sowie die Zahl der ehelichen und der unehelichen auf je 100 Geborene, jeweils für Städte, Landorte und zusammen. Alle diese Werte stehen als gedruckte Zahlen im Datensatz. Neu berechnet (derived) sind nur die Fünfjahresmittel 1858–1862 und 1863–1867 (einfaches Mittel der gedruckten Jahresanteile „Zusammen“); für das Fürstenthum entspricht das den von Brückner genannten 19,96 und 17,61 Procent (S. 110). Der Ländervergleich stammt aus S. 110; Brückner nennt für die anderen Staaten keinen Zeitraum.",
        "The table on p. 109 gives, for each district and for the principality, the number of illegitimate births and the numbers of legitimate and illegitimate births per 100 births, for towns, rural places and combined. All these values are in the dataset as printed. Only the five-year means 1858–1862 and 1863–1867 are computed (simple mean of the printed annual shares for “total”); for the principality they match the 19.96 and 17.61 per cent that Brückner quotes (p. 110). The comparison of states comes from p. 110; Brückner gives no period for the other states."),
    "findings": [
        bi(f"Im Fürstenthum fiel der Anteil der unehelichen Geburten von {fde(fue[1858])} Procent (1858) auf {fde(fue[1867])} Procent (1867); der Tiefstwert liegt bei {fde(fue[lo_y])} ({lo_y}), der Höchstwert bei {fde(fue[hi_y])} ({hi_y}). Die Fünfjahresmittel sinken von {fde(h[('Reuß j. L.', '1858–1862')])} auf {fde(h[('Reuß j. L.', '1863–1867')])} Procent.",
           f"In the principality the share of illegitimate births fell from {fen(fue[1858])} per cent (1858) to {fen(fue[1867])} per cent (1867); the low is {fen(fue[lo_y])} ({lo_y}), the high {fen(fue[hi_y])} ({hi_y}). The five-year means fall from {fen(h[('Reuß j. L.', '1858–1862')])} to {fen(h[('Reuß j. L.', '1863–1867')])} per cent."),
        bi(f"In allen drei Landestheilen ist der Anteil im zweiten Fünfjahreszeitraum niedriger; am deutlichsten in Schleiz ({fde(h[('Schleiz', '1858–1862')])} auf {fde(h[('Schleiz', '1863–1867')])}), am schwächsten in Lobenstein-Ebersdorf ({fde(h[('Lobenstein-Ebersdorf', '1858–1862')])} auf {fde(h[('Lobenstein-Ebersdorf', '1863–1867')])}).",
           f"In all three districts the share is lower in the second five-year period; most clearly in Schleiz ({fen(h[('Schleiz', '1858–1862')])} to {fen(h[('Schleiz', '1863–1867')])}), least in Lobenstein-Ebersdorf ({fen(h[('Lobenstein-Ebersdorf', '1858–1862')])} to {fen(h[('Lobenstein-Ebersdorf', '1863–1867')])})."),
        bi(f"In jedem Landestheil liegt der Anteil auf dem Land über dem in den Städten: Gera {fde(mean_st[('Gera', 'Landorte')])} gegenüber {fde(mean_st[('Gera', 'Städte')])}, Schleiz {fde(mean_st[('Schleiz', 'Landorte')])} gegenüber {fde(mean_st[('Schleiz', 'Städte')])}, Lobenstein-Ebersdorf {fde(mean_st[('Lobenstein-Ebersdorf', 'Landorte')])} gegenüber {fde(mean_st[('Lobenstein-Ebersdorf', 'Städte')])} Procent. Brückner führt das darauf zurück, dass weibliche Dienstboten ihre Kinder aus der Stadt aufs Land tragen (S. 107) und dass vor allem im Oberland junge Frauen in der Fremde Dienst suchen und von dort oft schwanger heimkehren (S. 110).",
           f"In every district the share in rural places exceeds that in towns: Gera {fen(mean_st[('Gera', 'Landorte')])} against {fen(mean_st[('Gera', 'Städte')])}, Schleiz {fen(mean_st[('Schleiz', 'Landorte')])} against {fen(mean_st[('Schleiz', 'Städte')])}, Lobenstein-Ebersdorf {fen(mean_st[('Lobenstein-Ebersdorf', 'Landorte')])} against {fen(mean_st[('Lobenstein-Ebersdorf', 'Städte')])} per cent. Brückner attributes this to female servants who carry children from the town into the countryside (p. 107) and, especially in the Oberland, to young women who seek service abroad and often return pregnant (p. 110)."),
        bi(f"Im Vergleich der Staaten liegt Reuß j. L. mit {fde(st['Reuß j. L. 1858–67'])} Procent (1858–1867) an dritter Stelle der {n_states} verglichenen Staaten, hinter Bayern ({fde(st['Bayern'])}) und Sachsen-Coburg ({fde(st['Sachsen-Coburg'])}); Preußen weist {fde(st['Preussen'])} Procent aus.",
           f"Compared with other states Reuss j. L. ranks third among the {n_states} states compared, with {fen(st['Reuß j. L. 1858–67'])} per cent (1858–1867), behind Bavaria ({fen(st['Bayern'])}) and Saxe-Coburg ({fen(st['Sachsen-Coburg'])}); Prussia has {fen(st['Preussen'])} per cent."),
    ],
    "caveats": [
        bi("Einzelne gedruckte Werte widersprechen sich: In der Zeile Lobenstein-Ebersdorf 1865 (Zusammen) ergeben 79,20 und 21,80 zusammen 101; die Zahl 196 passt zu 21,80 Procent der 899 Geborenen. Für Schleiz 1865 und das Fürstenthum 1865 passen die Anteile (15,31 und 16,62) nicht zu den Geburtenzahlen der Tabelle S. 107, sondern zu etwa 1136 bzw. 3585 Geborenen. Alle Werte stehen wie gedruckt im Datensatz.",
           "Some printed values contradict each other: in the row Lobenstein-Ebersdorf 1865 (total) 79.20 and 21.80 add up to 101; the figure 196 fits 21.80 per cent of the 899 births. For Schleiz 1865 and the principality 1865 the shares (15.31 and 16.62) do not fit the birth numbers of the table on p. 107 but about 1,136 and 3,585 births. All values are in the dataset as printed."),
        bi("Im Text (S. 110) nennt Brückner für Lobenstein-Ebersdorf 24,94 Procent, in der Tabelle steht dieser Wert für die Landorte, für den Landestheil insgesamt 24,17.",
           "In the text (p. 110) Brückner gives 24.94 per cent for Lobenstein-Ebersdorf; in the table this is the value for rural places, the district as a whole has 24.17."),
        bi("Der Staatenvergleich nennt keinen einheitlichen Zeitraum und keine Quelle; Reuß j. L. ist in zwei Zeiträumen angegeben (1858–1864 und 1858–1867). „Sachsen“ ist das Königreich Sachsen.",
           "The comparison of states names neither a uniform period nor a source; Reuss j. L. is given for two periods (1858–1864 and 1858–1867). “Sachsen” is the Kingdom of Saxony."),
    ],
    "datasets": [
        {"name": "illegit", "title": bi("Uneheliche Geborene nach Landestheil, Städten und Landorten", "Illegitimate births by district, towns and rural places"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landestheil", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Zusammen"),
                     col("illegitimate", "Uneheliche Geborene", "Illegitimate births", "integer", "Geburten"),
                     col("legit_pct", "Eheliche auf 100 Geborene", "Legitimate per 100 births", "number", "%"),
                     col("illegit_pct", "Uneheliche auf 100 Geborene", "Illegitimate per 100 births", "number", "%")],
         "rows": illegit, "source_refs": [SRC]},
        {"name": "illegit_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("area", "Gebiet", "Area", "string"),
                     col("illegitimate", "Uneheliche Geborene (Jahresmittel)", "Illegitimate births (annual mean)", "number", "Geburten"),
                     col("legit_pct", "Eheliche auf 100 Geborene", "Legitimate per 100 births", "number", "%"),
                     col("illegit_pct", "Uneheliche auf 100 Geborene", "Illegitimate per 100 births", "number", "%")],
         "rows": illegit_mean, "source_refs": [ref("109", "b1", "r15"), ref("109", "b1", "r27"), ref("109", "b1", "r39"), ref("109", "b1", "r51")]},
        {"name": "illegit_halves", "title": bi("Unehelichenanteil in zwei Fünfjahreszeiträumen", "Illegitimacy share in two five-year periods"),
         "columns": [col("district", "Landestheil", "District", "string"),
                     col("period", "Zeitraum", "Period", "string"),
                     col("illegit_pct", "Uneheliche auf 100 Geborene (Mittel)", "Illegitimate per 100 births (mean)", "number", "%", derived=True,
                         note="einfaches Mittel der gedruckten Jahresanteile 'Zusammen'")],
         "rows": halves, "source_refs": [SRC]},
        {"name": "illegit_states", "title": bi("Uneheliche Geburten in verschiedenen Staaten", "Illegitimate births in various states"),
         "columns": [col("state", "Staat", "State", "string"),
                     col("illegit_pct", "Uneheliche auf 100 Geborene", "Illegitimate per 100 births", "number", "%"),
                     col("group", "Gruppe", "Group", "string")],
         "rows": states, "source_refs": [ref("110", "b3", "r1-r6")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "illegit",
         "title": bi("Uneheliche Geborene auf 100 Geborene", "Illegitimate births per 100 births"),
         "caption": bi("Je Landestheil und für das ganze Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1858–1867.",
                       "By district and for the whole principality (Reuß j. L.), towns and rural places combined, 1858–1867."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.area == 'Zusammen'"}],
                      "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "illegit_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births"), "scale": {"domain": [10, 30]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("year", "Jahr", "Year"),
                                      tip("illegitimate", "Uneheliche Geborene", "Illegitimate births"),
                                      tip("illegit_pct", "% der Geborenen", "% of births", ".2f")]}}},
        {"id": "c2", "dataset": "illegit_halves",
         "title": bi("Erste und zweite Hälfte des Jahrzehnts", "First and second half of the decade"),
         "caption": bi("Mittel der gedruckten Jahresanteile 1858–1862 und 1863–1867. In jedem Landestheil ist der Anteil im zweiten Zeitraum niedriger.",
                       "Mean of the printed annual shares 1858–1862 and 1863–1867. In every district the share is lower in the second period."),
         "vegalite": {"height": 280, "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "period", "type": "nominal"},
                          "y": {"field": "illegit_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births")},
                          "color": {"field": "period", "type": "nominal", "title": None, "scale": {"domain": ["1858–1862", "1863–1867"]}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("period", "Zeitraum", "Period"),
                                      tip("illegit_pct", "% der Geborenen", "% of births", ".2f")]}}},
        {"id": "c3", "dataset": "illegit_mean",
         "title": bi("Städte und Landorte im Vergleich", "Towns and rural places compared"),
         "caption": bi("Gedrucktes Zehnjahresmittel 1858–1867. Auf dem Land liegt der Anteil in jedem Landestheil über dem der Städte.",
                       "Printed ten-year mean 1858–1867. In the countryside the share is above that of the towns in every district."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.area != 'Zusammen'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": AREAS},
                          "y": {"field": "illegit_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("district", "Landestheil", "District"), tip("area", "Gebiet", "Area"),
                                      tip("illegit_pct", "% der Geborenen", "% of births", ".2f")]}}},
        {"id": "c4", "dataset": "illegit_states",
         "title": bi("Reuß j. L. im Vergleich mit anderen Staaten", "Reuß j. L. compared with other states"),
         "caption": bi("Uneheliche Geburten in Procent aller Geburten, nach Brückner S. 110 (Zeitraum der übrigen Staaten nicht angegeben). Reuß j. L. ist hervorgehoben.",
                       "Illegitimate births as a percentage of all births, after Brückner p. 110 (period of the other states not stated). Reuß j. L. is highlighted."),
         "vegalite": {"height": 340, "mark": "bar",
                      "encoding": {
                          "y": {"field": "state", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelExpr": lab_expr(ST_EN), "labelLimit": 300}},
                          "x": {"field": "illegit_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births")},
                          "color": {"field": "group", "type": "nominal", "scale": {"domain": ["übrige Staaten", "Reuß j. L."]}, "legend": None},
                          "tooltip": [tip("state", "Staat", "State"), tip("illegit_pct", "% der Geborenen", "% of births", ".2f")]}}},
    ],
    "transcription_issues": [
        {"page": "109", "block": "b1", "cell": "r36c9", "transcribed": "79,20", "facsimile": "79,20", "checked_facsimile": True,
         "note": "Lobenstein-Ebersdorf 1865, total: 79,20 + 21,80 = 101; printed so (196 of 899 births = 21,80 %). Original inconsistency, not a misreading."},
        {"page": "109", "block": "b1", "cell": "r24c9", "transcribed": "84,69", "facsimile": "84,69", "checked_facsimile": True,
         "note": "Schleiz 1865 total (84,69 / 15,31): 174 illegitimate of 1064 births (p. 107) would be 16,35 %; the printed share implies about 1136 births. Original inconsistency."},
        {"page": "110", "block": "b5", "transcribed": "Lobenstein-Ebersdorf 24,94", "facsimile": "Lobenstein-Ebersdorf 24,94", "checked_facsimile": True,
         "note": "Text value equals the Landorte mean of the table (24,94); the table gives 24,17 for the whole district."},
    ],
    "keywords": {"de": ["uneheliche Geburten", "Unehelichkeit", "Illegitimität", "eheliche Geburten", "Dienstboten", "Stadt und Land", "Staatenvergleich", "Bevölkerungsstatistik"],
                 "en": ["illegitimate births", "illegitimacy", "legitimate births", "servants", "town and country", "comparison of states", "population statistics"]},
    "related": ["bevoelkerung-geburten-1858-1867", "bevoelkerung-todtgeborene-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
