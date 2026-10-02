"""A03: Todtgeborene 1858-1867 (pp. 111-112)."""
from common import *

YEARS = list(range(1858, 1868))
g = grid("111", "b1")
BLOCKS = {"Gera": (3, 13), "Schleiz": (15, 25), "Lobenstein-Ebersdorf": (27, 37), "Reuß j. L.": (39, 49)}
ROWREF = {"Gera": "r4-r13", "Schleiz": "r16-r25", "Lobenstein-Ebersdorf": "r28-r37", "Reuß j. L.": "r40-r49"}
AVGREF = {"Gera": "t14", "Schleiz": "t26", "Lobenstein-Ebersdorf": "t38", "Reuß j. L.": "t50"}
AREA_COLS = {"Städte": (1, 7), "Landorte": (2, 8), "Zusammen": (3, 9)}   # (count, pct)

still, still_mean = [], []
for k, (a, b) in BLOCKS.items():
    for r in g[a:b]:
        y = int(r[0])
        for area, (jn, jp) in AREA_COLS.items():
            still.append([y, k, area, inum(r[jn]), num(r[jp])])
    avg = g[b]
    assert avg[0].startswith("Durchschn")
    for area, (jn, jp) in AREA_COLS.items():
        still_mean.append([k, area, num(avg[jn]), num(avg[jp])])

# ---- numbers for the texts
zus = {(r[0], r[1]): r[4] for r in still if r[2] == "Zusammen"}
cnt = {(r[0], r[1], r[2]): r[3] for r in still}
fue = {y: zus[(y, "Reuß j. L.")] for y in YEARS}
mean_zus = {r[0]: r[3] for r in still_mean if r[1] == "Zusammen"}
mean_a = {(r[0], r[1]): r[3] for r in still_mean}
mean_n = {(r[0], r[1]): r[2] for r in still_mean}
b107 = grid("107", "b3")
births_fue = {int(r[0]): inum(r[7]) for r in b107[1:11]}
n_fue = {y: cnt[(y, "Reuß j. L.", "Zusammen")] for y in YEARS}
lo = min(mean_zus, key=mean_zus.get)
hi = max(mean_zus, key=mean_zus.get)
print(mean_zus, lo, hi, fue[1858], fue[1867], n_fue[1858], n_fue[1867], births_fue[1858], births_fue[1867])
assert lo == "Schleiz" and hi == "Gera"
urban_hi = [k for k in DISTRICTS if mean_a[(k, "Städte")] > mean_a[(k, "Landorte")]]
print("urban higher in", urban_hi)
assert urban_hi == ["Gera", "Reuß j. L."]
n_under = sum(fue[y] < mean_zus["Reuß j. L."] for y in YEARS)
hist_pct = 23.2 / 595.4 * 100
print(hist_pct)
yr_hi = max(fue, key=fue.get)
yr_lo = min(fue, key=fue.get)

SRC = ref("111", "b1", "r4-t50")
ana = {
    "id": "bevoelkerung-todtgeborene-1858-1867",
    "title": bi("Todtgeborene 1858–1867", "Stillbirths 1858–1867"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [SRC, ref("112", "b1")],
    "summary": bi(
        f"Brückner gibt für 1858–1867 die Zahl der Todtgeborenen je Landrathsbezirk, getrennt nach Städten und Landorten, und ihren Anteil an allen Geborenen an. Im Fürstenthum lag der Anteil im Zehnjahresmittel bei {fde(mean_zus['Reuß j. L.'])} Procent; er war in Gera am höchsten ({fde(mean_zus['Gera'])}), in Schleiz am niedrigsten ({fde(mean_zus['Schleiz'])}) und ging im Lauf der Jahre von {fde(fue[1858])} Procent (1858) auf {fde(fue[1867])} Procent (1867) zurück.",
        f"For 1858–1867 Brückner gives the number of stillbirths per district, split into towns and rural places, and their share of all births. For the principality the ten-year mean was {fen(mean_zus['Reuß j. L.'])} per cent; it was highest in Gera ({fen(mean_zus['Gera'])}), lowest in Schleiz ({fen(mean_zus['Schleiz'])}) and fell from {fen(fue[1858])} per cent (1858) to {fen(fue[1867])} per cent (1867)."),
    "method": bi(
        "Die Tabelle S. 111 nennt je Landrathsbezirk und für das Fürstenthum die Zahl der Todtgeborenen (Städte, Landorte, zusammen) sowie je 100 Geborene die Lebendgeborenen und die Todtgeborenen. Der Datensatz übernimmt die Zahlen und die gedruckten Procentsätze der Todtgeborenen (die Lebendgeborenen ergeben sich als Rest auf 100); „Geborene“ schließen die Todtgeborenen ein (Summe aus Lebend- und Todtgeborenen = 100). Die gedruckten Zehnjahresmittel stehen in einem eigenen Datensatz. Die Zahlen für 1794–1804 stammen aus dem Text S. 112 (lobensteiner Intelligenzblatt).",
        "The table on p. 111 gives, for each district and for the principality, the number of stillbirths (towns, rural places, total) and the live births and stillbirths per 100 births. The dataset takes the numbers and the printed percentages of stillbirths (live births are the remainder to 100); “births” include stillbirths (live plus stillborn = 100). The printed ten-year means are in a separate dataset. The figures for 1794–1804 come from the text on p. 112 (lobensteiner Intelligenzblatt)."),
    "findings": [
        bi(f"Im Zehnjahresmittel sind {fde(mean_zus['Reuß j. L.'])} Procent aller Geborenen todtgeboren; Gera hat mit {fde(mean_zus['Gera'])} den höchsten, Schleiz mit {fde(mean_zus['Schleiz'])} den niedrigsten Anteil, Lobenstein-Ebersdorf liegt mit {fde(mean_zus['Lobenstein-Ebersdorf'])} dazwischen.",
           f"On average {fen(mean_zus['Reuß j. L.'])} per cent of all births are stillbirths; Gera has the highest share ({fen(mean_zus['Gera'])}), Schleiz the lowest ({fen(mean_zus['Schleiz'])}), Lobenstein-Ebersdorf lies in between ({fen(mean_zus['Lobenstein-Ebersdorf'])})."),
        bi(f"Der Anteil im Fürstenthum fällt von {fde(fue[1858])} Procent (1858, {n_fue[1858]} Todtgeborene bei {births_fue[1858]} Geborenen) auf {fde(fue[1867])} Procent (1867, {n_fue[1867]} bei {births_fue[1867]}); in {n_under} der zehn Jahre liegt er unter dem Mittel.",
           f"The share in the principality falls from {fen(fue[1858])} per cent (1858, {n_fue[1858]} stillbirths among {fint_en(births_fue[1858])} births) to {fen(fue[1867])} per cent (1867, {n_fue[1867]} among {fint_en(births_fue[1867])}); in {n_under} of the ten years it is below the mean."),
        bi(f"Städte und Landorte unterscheiden sich je nach Landestheil: In Gera ({fde(mean_a[('Gera', 'Städte')])} gegenüber {fde(mean_a[('Gera', 'Landorte')])}) und im Fürstenthum ({fde(mean_a[('Reuß j. L.', 'Städte')])} gegenüber {fde(mean_a[('Reuß j. L.', 'Landorte')])}) liegen die Städte höher, in Schleiz und Lobenstein-Ebersdorf etwas niedriger als das Land.",
           f"Towns and rural places differ by district: in Gera ({fen(mean_a[('Gera', 'Städte')])} against {fen(mean_a[('Gera', 'Landorte')])}) and in the principality ({fen(mean_a[('Reuß j. L.', 'Städte')])} against {fen(mean_a[('Reuß j. L.', 'Landorte')])}) the towns are higher; in Schleiz and Lobenstein-Ebersdorf they are slightly lower than the countryside."),
        bi(f"Für Lobenstein-Ebersdorf nennt Brückner aus dem Intelligenzblatt 1794–1804 im Jahresmittel 23,2 Todtgeborene bei 595,4 Geborenen und 4,18 Procent Todtgeborene; 1858–1867 sind es {fde(mean_zus['Lobenstein-Ebersdorf'])} Procent, der Anteil hat dort also zugenommen (auch bei der Nachrechnung 23,2 : 595,4 = {fde(hist_pct)} Procent).",
           f"For Lobenstein-Ebersdorf Brückner quotes from the Intelligenzblatt, for 1794–1804, an annual mean of 23.2 stillbirths among 595.4 births and 4.18 per cent stillbirths; for 1858–1867 the figure is {fen(mean_zus['Lobenstein-Ebersdorf'])} per cent, so the share has increased there (also when recomputed: 23.2 : 595.4 = {fen(hist_pct)} per cent)."),
    ],
    "caveats": [
        bi("Die Zeilen für 1865 sind in der Vorlage nicht durchgehend stimmig: Die gedruckten Anteile für Schleiz (3,87), Lobenstein-Ebersdorf (4,34) und das Fürstenthum (5,38) passen nicht zu den Geburtenzahlen der Tabelle S. 107; aus den Zahlen ergäben sich etwa 4,14, 4,23 und 5,21 Procent (für Schleiz passt der gedruckte Wert zu etwa 1136 Geborenen, vgl. die Auswertung der Geburten).",
           "The 1865 rows in the source are not entirely consistent: the printed shares for Schleiz (3.87), Lobenstein-Ebersdorf (4.34) and the principality (5.38) do not fit the birth numbers of the table on p. 107; the counts would give about 4.14, 4.23 and 5.21 per cent (for Schleiz the printed value fits about 1,136 births, cf. the analysis of births)."),
        bi("Auch im Text S. 112 stimmen die gedruckten Zahlen nicht ganz: 23,2 Todtgeborene bei 595,4 Geborenen ergeben 3,90, nicht 4,18 Procent. Die Zahlen sind klein (in Städten oft unter 20 Fälle je Jahr), die Jahresschwankungen der Städte daher zufallsanfällig. Ob die Todtgeborenen im Sinne der Zeit auch bei den Gestorbenen gezählt wurden, sagt Brückner nicht.",
           "The printed figures in the text on p. 112 are not entirely consistent either: 23.2 stillbirths among 595.4 births give 3.90, not 4.18 per cent. The numbers are small (often fewer than 20 cases a year in the towns), so annual swings in the towns are subject to chance. Brückner does not say whether stillbirths were also counted among the deaths in the sense of the period."),
    ],
    "datasets": [
        {"name": "stillbirths", "title": bi("Todtgeborene nach Landrathsbezirk, Städten und Landorten", "Stillbirths by district, towns and rural places"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landrathsbezirk", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Zusammen"),
                     col("stillborn", "Todtgeborene", "Stillbirths", "integer", "Fälle"),
                     col("stillborn_pct", "Todtgeborene auf 100 Geborene", "Stillbirths per 100 births", "number", "%")],
         "rows": still, "source_refs": [ref("111", "b1", "r4-r13"), ref("111", "b1", "r16-r25"), ref("111", "b1", "r28-r37"), ref("111", "b1", "r40-r49")]},
        {"name": "stillbirths_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landrathsbezirk", "District", "string"),
                     col("area", "Gebiet", "Area", "string"),
                     col("stillborn", "Todtgeborene (Jahresmittel)", "Stillbirths (annual mean)", "number", "Fälle"),
                     col("stillborn_pct", "Todtgeborene auf 100 Geborene", "Stillbirths per 100 births", "number", "%")],
         "rows": still_mean, "source_refs": [ref("111", "b1", "t14"), ref("111", "b1", "t26"), ref("111", "b1", "t38"), ref("111", "b1", "t50")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "stillbirths",
         "title": bi("Todtgeborene auf 100 Geborene", "Stillbirths per 100 births"),
         "caption": bi("Je Landrathsbezirk und für das ganze Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1858–1867.",
                       "By district and for the whole principality (Reuß j. L.), towns and rural places combined, 1858–1867."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.area == 'Zusammen'"}],
                      "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "stillborn_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births"), "scale": {"domain": [2, 8]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"),
                                      tip("stillborn", "Todtgeborene", "Stillbirths"),
                                      tip("stillborn_pct", "% der Geborenen", "% of births", ".2f")]}}},
        {"id": "c2", "dataset": "stillbirths_mean",
         "title": bi("Städte und Landorte im Vergleich", "Towns and rural places compared"),
         "caption": bi("Gedrucktes Zehnjahresmittel 1858–1867. In Gera und im Fürstenthum insgesamt liegen die Städte über dem Land, in Schleiz und Lobenstein-Ebersdorf knapp darunter.",
                       "Printed ten-year mean 1858–1867. In Gera and in the principality as a whole the towns lie above the countryside, in Schleiz and Lobenstein-Ebersdorf just below."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.area != 'Zusammen'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": AREAS},
                          "y": {"field": "stillborn_pct", "type": "quantitative", "title": bi("% der Geborenen", "% of births")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("area", "Gebiet", "Area"),
                                      tip("stillborn_pct", "% der Geborenen", "% of births", ".2f")]}}},
        {"id": "c3", "dataset": "stillbirths",
         "title": bi("Zahl der Todtgeborenen im Fürstenthum", "Number of stillbirths in the principality"),
         "caption": bi("Städte und Landorte übereinander gestapelt; die Gesamthöhe ist die Zahl im Fürstenthum.",
                       "Towns and rural places stacked; the total height is the number for the principality."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.district == 'Reuß j. L.' && datum.area != 'Zusammen'"}],
                      "mark": "bar",
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "stillborn", "type": "quantitative", "title": bi("Todtgeborene", "stillbirths"), "stack": "zero"},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "order": {"field": "area", "type": "nominal", "sort": "descending"},
                          "tooltip": [tip("year", "Jahr", "Year"), tip("area", "Gebiet", "Area"), tip("stillborn", "Todtgeborene", "Stillbirths")]}}},
    ],
    "transcription_issues": [
        {"page": "111", "block": "b1", "cell": "r47c10", "transcribed": "5,38", "facsimile": "5,38", "checked_facsimile": True,
         "note": "Fürstenthum 1865, total: 183 stillbirths of 3513 births (p. 107) would be 5,21 %; as printed. Original inconsistency, not a misreading."},
        {"page": "111", "block": "b1", "cell": "r35c10", "transcribed": "4,34", "facsimile": "4,34", "checked_facsimile": True,
         "note": "Lobenstein-Ebersdorf 1865, total: 38 of 899 would be 4,23 %; as printed."},
    ],
    "keywords": {"de": ["Todtgeborene", "Totgeburten", "Fehlgeburten", "Geburten", "Stadt und Land", "Landrathsbezirk", "Bevölkerungsstatistik"],
                 "en": ["stillbirths", "births", "town and country", "district", "population statistics"]},
    "related": ["bevoelkerung-geburten-1858-1867", "bevoelkerung-uneheliche-geburten-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
