"""A04 / analysis 2: wind directions at Gera, Hohenleuben, Schleiz, Rothenacker (pp. 62-64)."""
import sys
sys.path.insert(0, ".")
from common import *

STATIONS = [("Gera", "62", "b3", "r2-r14"), ("Hohenleuben", "63", "b2", "r2-r14"),
            ("Schleiz", "63", "b4", "r2-r14"), ("Rothenacker", "63", "b6", "r2-r14")]
monthly_rows, annual_rows = [], []
cnt = {}
for so, (st, p, b, _rows) in enumerate(STATIONS, start=1):
    g = grid(p, b)
    assert g[0][1:] == ["N.", "NO.", "O.", "SO.", "S.", "SW.", "W.", "NW."]
    for m in range(1, 13):
        for i, d in enumerate(DIRS, start=1):
            cell = g[m][i]
            n = num(cell)
            n = 0 if n is None else int(n)  # '—' (Schleiz, Januar, N.) = no observation
            cnt[(st, m, d)] = n
            monthly_rows.append([st, so, m, g[m][0], d, i, n, mark(cell)])
    tot = sum(cnt[(st, m, d)] for m in range(1, 13) for d in DIRS)
    for i, d in enumerate(DIRS, start=1):
        n = sum(cnt[(st, m, d)] for m in range(1, 13))
        assert n == int(num(g[13][i])), (st, d)
        annual_rows.append([st, so, d, i, n, round(100 * n / tot, 1)])
TOT = {st: sum(cnt[(st, m, d)] for m in range(1, 13) for d in DIRS) for st, *_ in STATIONS}
SHARE = {(r[0], r[2]): r[5] for r in annual_rows}
print(TOT)
west = {st: SHARE[(st, "SW")] + SHARE[(st, "W")] + SHARE[(st, "NW")] for st in TOT}
east = {st: SHARE[(st, "NO")] + SHARE[(st, "O")] + SHARE[(st, "SO")] for st in TOT}
ns = {st: SHARE[(st, "N")] + SHARE[(st, "S")] for st in TOT}
print("west", west, "east", east, "N+S", ns)
top = {st: sorted(DIRS, key=lambda d: -SHARE[(st, d)])[:3] for st in TOT}
print(top)
# monthly west share
mw = {}
for st in TOT:
    for m in range(1, 13):
        t = sum(cnt[(st, m, d)] for d in DIRS)
        mw[(st, m)] = 100 * (cnt[(st, m, "SW")] + cnt[(st, m, "W")] + cnt[(st, m, "NW")]) / t
for st in TOT:
    vals = [mw[(st, m)] for m in range(1, 13)]
    print(st, "west share monthly min/max", round(min(vals), 1), vals.index(min(vals)) + 1, round(max(vals), 1), vals.index(max(vals)) + 1)
# Hohenleuben month totals vs 15 x days
mt = [sum(cnt[("Hohenleuben", m, d)] for d in DIRS) for m in range(1, 13)]
dim = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print("Hohenleuben month totals", mt, [t / d for t, d in zip(mt, dim)], TOT["Hohenleuben"] / 365)
# Gera ratio to 3 obs/day over 12 y
print("Gera total / (12*365.25*3)", TOT["Gera"] / (12 * 365.25 * 3))


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


G, H, S_, R = "Gera", "Hohenleuben", "Schleiz", "Rothenacker"
ana = {
    "id": "klima-wind-stationen-vergleich",
    "title": bi("Windrichtungen an vier Beobachtungsorten", "Wind directions at four observing stations"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "62", "block": "b3", "rows": "r2-r15"}, {"page": "63", "block": "b1"}, {"page": "63", "block": "b2", "rows": "r2-r15"},
                {"page": "63", "block": "b3"}, {"page": "63", "block": "b4", "rows": "r2-r15"}, {"page": "63", "block": "b5"},
                {"page": "63", "block": "b6", "rows": "r2-r15"}, {"page": "64", "block": "b1"}, {"page": "64", "block": "b2"},
                {"page": "64", "block": "b3"}],
    "summary": bi(
        "Brückner stellt die Windrichtungen von Gera (Elstertal, Unterland) denen von Hohenleuben, Schleiz und Rothenacker (Oberland) gegenüber. Die Beobachtungsreihen sind verschieden lang (10, 7, 2 und 1 Jahr); verglichen werden deshalb Prozentanteile. Im Unterland dominieren Süd- und Nordwind, im Oberland Südwest- bis Westwind.",
        "Brückner compares wind directions at Gera (Elster valley, Unterland) with those at Hohenleuben, Schleiz and Rothenacker (Oberland). The series differ in length (10, 7, 2 and 1 years), so percentage shares are compared. In the Unterland southerly and northerly winds dominate, in the Oberland south-westerly to westerly winds."),
    "method": bi(
        "Quellen sind die vier Monatstabellen auf S. 62 (Gera, 1856–1865, E. Kratzsch und Rob. Schmidt) und S. 63 (Hohenleuben »in sieben Jahren«, Beobachter Alberti; Schleiz 1866 und 1867, Dr. Mauke; Rothenacker 1867, Lehrer G. Oswald). Verwendet werden die gedruckten Monatswerte je Richtung; die Jahressummen ergeben sich als Summe der zwölf Monate und stimmen mit den gedruckten Summenzeilen überein (der Gedankenstrich bei Schleiz, Januar, N. gilt als 0). Die Gera-Zahlen hat Brückner von 16 auf 8 Richtungen zurückgeführt (S. 62); ob dies auch für die übrigen Orte gilt, sagt der Text nicht. Eigene Rechenschritte: Anteil jeder Richtung an der Jahressumme des Ortes, Anteil der Winde aus dem westlichen Sektor (SW, W, NW) je Monat. Die gedruckten Jahresmittel und die Vergleichstabelle auf S. 64 werden nicht verwendet, weil sie von den Zeilensummen abweichende Werte enthalten (siehe Hinweise). Die Fläche der Windrosenkeile ist dem Anteil proportional (Radius ∝ √Anteil); die Ringe liegen bei 10, 20 und 30 %.",
        "The sources are the four monthly tables on p. 62 (Gera, 1856–1865, E. Kratzsch and Rob. Schmidt) and p. 63 (Hohenleuben “in seven years”, observer Alberti; Schleiz 1866 and 1867, Dr Mauke; Rothenacker 1867, teacher G. Oswald). The printed monthly values per direction are used; annual totals are the sum of the twelve months and agree with the printed total rows (the dash for Schleiz, January, N. is read as 0). Brückner reduced the Gera figures from 16 to 8 points (p. 62); the text does not say whether the same applies to the other sites. Own calculations: share of each direction in the station's annual total, and the share of winds from the western sector (SW, W, NW) per month. The printed annual means and the comparison table on p. 64 are not used because they contain values that differ from the row sums (see caveats). The area of the rose wedges is proportional to the share (radius ∝ √share); the rings are at 10, 20 and 30 %."),
    "findings": [
        bi(f"Gera: S {F(SHARE[(G,'S')])[0]} % und N {F(SHARE[(G,'N')])[0]} % zusammen {F(ns[G])[0]} %; der westliche Sektor (SW, W, NW) erreicht {F(west[G])[0]} %.",
           f"Gera: S {F(SHARE[(G,'S')])[1]} % and N {F(SHARE[(G,'N')])[1]} % together make {F(ns[G])[1]} %; the western sector (SW, W, NW) reaches {F(west[G])[1]} %."),
        bi(f"Hohenleuben (freie Plateaulage) hat mit W {F(SHARE[(H,'W')])[0]} % die klarste Hauptrichtung; der westliche Sektor umfasst {F(west[H])[0]} %. Schleiz fällt durch SW ({F(SHARE[(S_,'SW')])[0]} %) auf, danach folgt W ({F(SHARE[(S_,'W')])[0]} %); westlicher Sektor {F(west[S_])[0]} %.",
           f"Hohenleuben (open plateau) has the clearest main direction with W {F(SHARE[(H,'W')])[1]} %; the western sector makes up {F(west[H])[1]} %. Schleiz stands out for SW ({F(SHARE[(S_,'SW')])[1]} %), followed by W ({F(SHARE[(S_,'W')])[1]} %); western sector {F(west[S_])[1]} %."),
        bi(f"Rothenacker (nur ein Jahr) verteilt sich breiter: W {F(SHARE[(R,'W')])[0]} %, SW {F(SHARE[(R,'SW')])[0]} %, S {F(SHARE[(R,'S')])[0]} %; westlicher Sektor {F(west[R])[0]} %.",
           f"Rothenacker (one year only) is more evenly spread: W {F(SHARE[(R,'W')])[1]} %, SW {F(SHARE[(R,'SW')])[1]} %, S {F(SHARE[(R,'S')])[1]} %; western sector {F(west[R])[1]} %."),
        bi(f"Im Jahresgang erreicht der westliche Sektor in Gera im Juli sein Maximum ({F(mw[(G,7)])[0]} %) und im Mai sein Minimum ({F(mw[(G,5)])[0]} %); in Hohenleuben liegt er im Februar am höchsten ({F(mw[(H,2)])[0]} %) und im April am niedrigsten ({F(mw[(H,4)])[0]} %). Im Winter ist der Abstand zwischen beiden Orten am größten (Februar {F(mw[(H,2)]-mw[(G,2)])[0]} Prozentpunkte).",
           f"Over the year the western sector at Gera peaks in July ({F(mw[(G,7)])[1]} %) with a minimum in May ({F(mw[(G,5)])[1]} %); at Hohenleuben it is highest in February ({F(mw[(H,2)])[1]} %) and lowest in April ({F(mw[(H,4)])[1]} %). The gap between the two sites is widest in winter (February {F(mw[(H,2)]-mw[(G,2)])[1]} percentage points)."),
        bi("Brückner führt den Unterschied auf die Lage zurück: Die Oberlandstationen liegen auf freiem Plateau, die Winde werden dort kaum abgelenkt, in Gera werden sie vom Elstertal in die Talrichtung gelenkt (S. 64).",
           "Brückner attributes the difference to location: the Oberland stations lie on an open plateau where winds are hardly deflected, while at Gera the Elster valley channels them along its axis (p. 64)."),
    ],
    "caveats": [
        bi(f"Die Reihen sind sehr verschieden lang: Schleiz hat zwei Jahre, Rothenacker eines. Deren Monatswerte schwanken stark (Westanteil Rothenacker {F(min(mw[(R,m)] for m in range(1,13)),0)[0]}–{F(max(mw[(R,m)] for m in range(1,13)),0)[0]} %) und sind in Chart 3 nicht abgebildet; im Datensatz stehen sie vollständig. Die Aussagen zum Jahresgang stützen sich auf Gera und Hohenleuben.",
           f"The series differ greatly in length: Schleiz has two years, Rothenacker one. Their monthly values fluctuate strongly (western share at Rothenacker {F(min(mw[(R,m)] for m in range(1,13)),0)[1]}–{F(max(mw[(R,m)] for m in range(1,13)),0)[1]} %) and are not plotted in chart 3; they are given in full in the dataset. Statements on the annual cycle rest on Gera and Hohenleuben."),
        bi(f"Bei Hohenleuben liegen alle Monatssummen nahe 15 × Monatslänge (Januar {mt[0]} = 15 × 31; Gesamtsumme {fmt(TOT[H],'de')} ≈ 15 × 365). Das deutet auf 15 Jahre mit einer Ablesung täglich statt der in der Überschrift genannten sieben Jahre (Brückners Jahresmittel sind Summe ÷ 7). Für die Prozentanteile ist das gleichgültig; ein Vergleich der absoluten Jahresmittel zwischen den Orten (S. 64) ist dagegen unsicher.",
           f"For Hohenleuben all monthly totals lie close to 15 × the length of the month (January {mt[0]} = 15 × 31; grand total {fmt(TOT[H],'en')} ≈ 15 × 365). This suggests 15 years with one reading a day rather than the seven years named in the heading (Brückner's annual means are sum ÷ 7). It does not matter for the percentage shares, but a comparison of the absolute annual means between stations (p. 64) is uncertain."),
        bi("Druckabweichungen in Brückners Jahresmitteln: Schleiz, SW: gedruckt 400,4, Summe 808 ÷ 2 = 404; S. 64 gibt für Gera W 204,6 an, S. 62 (1986 ÷ 10) dagegen 198,6; Hohenleuben, SW: gedruckt 108,0 statt 107,9. Die Faksimiles bestätigen die gedruckten Werte, die Transkription ist also korrekt; die Fehler liegen im Original.",
           "Misprints in Brückner's annual means: Schleiz, SW: printed 400.4, sum 808 ÷ 2 = 404; p. 64 gives 204.6 for Gera W, whereas p. 62 (1986 ÷ 10) gives 198.6; Hohenleuben, SW: printed 108.0 instead of 107.9. The facsimiles confirm the printed values, so the transcription is correct; the errors are in the original."),
        bi("Die Zähleinheit ist nicht angegeben (Beobachtungen oder Tage), Windstille und Windstärke fehlen. Brückner weist selbst auf die Standortabhängigkeit hin; die Beobachter und Instrumente sind nicht einheitlich.",
           "The counting unit is not stated (observations or days); calms and wind strength are missing. Brückner himself points to the dependence on location; observers and instruments were not uniform."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Windbeobachtungen nach Ort, Monat und Richtung", "Wind observations by station, month and direction"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True, "Reihenfolge wie bei Brückner"),
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("direction", "Richtung", "Direction", "string", None, False, "N, NO, O, SO, S, SW, W, NW; Original »N.« usw."),
             col("dir_index", "Reihenfolge der Richtung", "Direction order", "integer", None, True, "1 = N … 8 = NW im Uhrzeigersinn"),
             col("count", "Beobachtungen", "Observations", "integer", "Zahl", False, "Gedankenstrich (Schleiz, Januar, N.) = 0"),
             col("mark", "Druckvermerk", "Printed mark", "string", None, False, "»Max.« oder »Min.« im Original (nur Hohenleuben)"),
         ], "rows": monthly_rows,
         "source_refs": [{"page": "62", "block": "b3", "rows": "r2-r13"}, {"page": "63", "block": "b2", "rows": "r2-r13"},
                         {"page": "63", "block": "b4", "rows": "r2-r13"}, {"page": "63", "block": "b6", "rows": "r2-r13"}]},
        {"name": "annual", "title": bi("Jahressummen und Richtungsanteile je Ort", "Annual totals and direction shares by station"),
         "columns": [
             col("station", "Beobachtungsort", "Station", "string"),
             col("station_order", "Reihenfolge des Ortes", "Station order", "integer", None, True),
             col("direction", "Richtung", "Direction", "string"),
             col("dir_index", "Reihenfolge der Richtung", "Direction order", "integer", None, True),
             col("count", "Beobachtungen im Beobachtungszeitraum", "Observations in the observation period", "integer", "Zahl", False, "gedruckte Summenzeile"),
             col("share", "Anteil", "Share", "number", "%", True),
         ], "rows": annual_rows,
         "source_refs": [{"page": "62", "block": "b3", "rows": "r14"}, {"page": "63", "block": "b2", "rows": "r14"},
                         {"page": "63", "block": "b4", "rows": "r14"}, {"page": "63", "block": "b6", "rows": "r14"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "annual",
         "title": bi("Windrosen der vier Orte", "Wind roses of the four stations"),
         "caption": bi("Anteil der acht Richtungen an der Jahressumme (Fläche ∝ Anteil; Ringe bei 10, 20, 30 %). Gera: Süd- und Nordwind; Hohenleuben und Schleiz: Westsektor, in Hohenleuben vor allem W, in Schleiz vor allem SW.",
                       "Share of the eight directions in the annual total (area ∝ share; rings at 10, 20, 30 %). Gera: south and north winds; Hohenleuben and Schleiz: western sector, mainly W at Hohenleuben and mainly SW at Schleiz."),
         "vegalite": rose_spec("station_label", "station_order", columns=2, cell=200, rmax=66, label_r=91,
                               extra_transform=[{"calculate": bi(
                                   "{'Gera':'Gera 1856–1865','Hohenleuben':'Hohenleuben (7 Jahre)','Schleiz':'Schleiz 1866–1867','Rothenacker':'Rothenacker 1867'}[datum.station]",
                                   "{'Gera':'Gera 1856–1865','Hohenleuben':'Hohenleuben (7 years)','Schleiz':'Schleiz 1866–1867','Rothenacker':'Rothenacker 1867'}[datum.station]"),
                                   "as": "station_label"}],
                               tooltip_extra=[{"field": "count", "title": bi("Beobachtungen", "Observations")}])},
        {"id": "c2", "dataset": "annual",
         "title": bi("Richtungsanteile im Vergleich", "Direction shares compared"),
         "caption": bi("Anteil jeder Richtung an der Jahressumme des Ortes (%). Die Gruppen folgen der Windrose im Uhrzeigersinn von Norden aus.",
                       "Share of each direction in the station's annual total (%). Groups follow the compass clockwise from north."),
         "vegalite": {
             "height": 300,
             "transform": [DIR_LABEL_CALC],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "dir_label", "type": "ordinal", "sort": {"field": "dir_index", "op": "min"}, "title": bi("Richtung", "Direction"), "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "station", "sort": {"field": "station_order", "op": "min"}},
                 "y": {"field": "share", "type": "quantitative", "title": bi("Anteil der Beobachtungen (%)", "Share of observations (%)")},
                 "color": {"field": "station", "type": "nominal", "title": None, "scale": {"domain": ["Gera", "Hohenleuben", "Schleiz", "Rothenacker"]}},
                 "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                             {"field": "dir_label", "title": bi("Richtung", "Direction")},
                             {"field": "share", "title": "%", "format": ".1f"},
                             {"field": "count", "title": bi("Beobachtungen", "Observations")}]}}},
        {"id": "c3", "dataset": "monthly",
         "title": bi("Westwinde im Jahresgang", "Westerly winds through the year"),
         "caption": bi("Anteil der Beobachtungen aus SW, W und NW an allen Beobachtungen des Monats (%). Gera hat im Sommer, Hohenleuben im Winter den größten Westanteil. Schleiz (2 Jahre) und Rothenacker (1 Jahr) sind wegen der kurzen Reihen nicht dargestellt.",
                       "Share of observations from SW, W and NW among all observations of the month (%). Gera has its largest westerly share in summer, Hohenleuben in winter. Schleiz (2 years) and Rothenacker (1 year) are not shown because their series are short."),
         "vegalite": {
             "height": 300,
             "transform": [MONTH_ABBR_CALC,
                           {"filter": "datum.station == 'Gera' || datum.station == 'Hohenleuben'"},
                           {"joinaggregate": [{"op": "sum", "field": "count", "as": "tot"}], "groupby": ["station", "month"]},
                           {"filter": "indexof(['SW','W','NW'], datum.direction) >= 0"},
                           {"aggregate": [{"op": "sum", "field": "count", "as": "west"}, {"op": "max", "field": "tot", "as": "tot"}], "groupby": ["station", "month", "mlabel"]},
                           {"calculate": "100*datum.west/datum.tot", "as": "west_share"}],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month"), "axis": {"labelAngle": 0}},
                 "y": {"field": "west_share", "type": "quantitative", "title": bi("Anteil SW + W + NW (%)", "Share SW + W + NW (%)"), "scale": {"domain": [0, 100]}},
                 "color": {"field": "station", "type": "nominal", "title": None, "scale": {"domain": ["Gera", "Hohenleuben"]}},
                 "tooltip": [{"field": "station", "title": bi("Ort", "Station")},
                             {"field": "mlabel", "title": bi("Monat", "Month")},
                             {"field": "west_share", "title": "%", "format": ".1f"},
                             {"field": "west", "title": bi("Beobachtungen SW + W + NW", "Observations SW + W + NW")},
                             {"field": "tot", "title": bi("Beobachtungen insgesamt", "Observations in total")}]}}},
    ],
    "keywords": {
        "de": ["Wind", "Windrichtung", "Windrose", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "Westwind", "Unterland", "Oberland", "Meteorologie"],
        "en": ["wind", "wind direction", "wind rose", "Gera", "Hohenleuben", "Schleiz", "Rothenacker", "west wind", "Unterland", "Oberland", "meteorology"]},
    "related": ["klima-wind-gera-1856-1865"],
    "supersedes_legacy": "p. 63 'Windverhältnisse' (iframe: wind roses by season for Hohenleuben, Schleiz, Rothenacker); also the station comparison of p. 64",
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
