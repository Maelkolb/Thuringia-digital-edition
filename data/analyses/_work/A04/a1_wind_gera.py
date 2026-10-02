"""A04 / analysis 1: wind directions at Gera 1856-1865 (p. 62), seasonal roses + month x direction heatmap."""
import sys
sys.path.insert(0, ".")
from common import *

g = grid("62", "b3")  # r2..r13 months, t14 Summa, r15 Jahresmittel
assert g[0][1:] == ["N.", "NO.", "O.", "SO.", "S.", "SW.", "W.", "NW."]
SEASON_ORDER = {"Winter": 1, "Frühling": 2, "Sommer": 3, "Herbst": 4}
counts = {}  # (month, dir) -> n
monthly_rows = []
for m in range(1, 13):
    row = g[m]
    mt = sum(int(num(row[c])) for c in range(1, 9))
    for i, d in enumerate(DIRS, start=1):
        n = int(num(row[i]))
        counts[(m, d)] = n
        monthly_rows.append([m, row[0], d, i, n, round(100 * n / mt, 1), SEASON_DE[m], SEASON_ORDER[SEASON_DE[m]]])
# seasonal / annual shares
GROUPS = [("Gesamtjahr", 0, list(range(1, 13))), ("Winter", 1, [12, 1, 2]), ("Frühling", 2, [3, 4, 5]),
          ("Sommer", 3, [6, 7, 8]), ("Herbst", 4, [9, 10, 11])]
seasonal_rows = []
agg = {}
for name, order, months in GROUPS:
    tot = sum(counts[(m, d)] for m in months for d in DIRS)
    for i, d in enumerate(DIRS, start=1):
        n = sum(counts[(m, d)] for m in months)
        agg[(name, d)] = (n, 100 * n / tot, tot)
        seasonal_rows.append([name, order, d, i, n, round(100 * n / tot, 1)])
# check against printed Summa row
for i, d in enumerate(DIRS, start=1):
    assert agg[("Gesamtjahr", d)][0] == int(num(g[13][i])), d
TOTAL = agg[("Gesamtjahr", "N")][2]
assert TOTAL == 12796

sh = lambda grp, d: agg[(grp, d)][1]
S_year, SO_year = sh("Gesamtjahr", "S"), sh("Gesamtjahr", "SO")
N_year, W_year = sh("Gesamtjahr", "N"), sh("Gesamtjahr", "W")
S_win, S_aut, S_spr, S_sum = sh("Winter", "S"), sh("Herbst", "S"), sh("Frühling", "S"), sh("Sommer", "S")
W_sum = sh("Sommer", "W")
NW_sum = sh("Sommer", "NW")
N_spr, N_sum, N_win = sh("Frühling", "N"), sh("Sommer", "N"), sh("Winter", "N")
jan_tot = sum(counts[(1, d)] for d in DIRS)
jul_tot = sum(counts[(7, d)] for d in DIRS)
jun_tot = sum(counts[(6, d)] for d in DIRS)
S_jan = 100 * counts[(1, "S")] / jan_tot
W_jul = 100 * counts[(7, "W")] / jul_tot
S_jun = 100 * counts[(6, "S")] / jun_tot
top = {n: max(DIRS, key=lambda d: agg[(n, d)][0]) for n, _, _ in GROUPS}
print("top direction per period:", top)
print("N spr is max season share of N:", {n: round(agg[(n, 'N')][1], 1) for n, _, _ in GROUPS})
per_day10 = TOTAL / (10 * 365.25)


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


ana = {
    "id": "klima-wind-gera-1856-1865",
    "title": bi("Windrichtungen in Gera 1856–1865", "Wind directions at Gera, 1856–1865"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "54", "block": "b1"}, {"page": "62", "block": "b1"}, {"page": "62", "block": "b2"}, {"page": "62", "block": "b3", "rows": "r2-r15"},
                {"page": "64", "block": "b1"}],
    "summary": bi(
        f"Für Gera teilt Brückner die Windbeobachtungen von 1856 bis 1865 nach acht Himmelsrichtungen und zwölf Monaten auf (zusammen {fmt(TOTAL,'de')} Beobachtungen; Beobachter E. Kratzsch und Rob. Schmidt). Die Windrosen nach Jahreszeiten und die Monatsübersicht zeigen, wie stark der Südwind im Herbst und Winter überwiegt und wie er im Sommer von West- und Nordwinden abgelöst wird.",
        f"For Gera, Brückner breaks wind observations from 1856 to 1865 down by eight compass directions and twelve months ({fmt(TOTAL,'en')} observations in all; observers E. Kratzsch and Rob. Schmidt). The wind roses by season and the monthly overview show how strongly southerly winds prevail in autumn and winter and how they give way to westerly and northerly winds in summer."),
    "method": bi(
        "Die Zahlen stammen aus der Monatstabelle auf S. 62 (b3, Zeilen Januar–December). Brückner hat die ursprünglich 16 Richtungen der Windrose auf acht zurückgeführt, indem NON. und NWN. zu N., OSO. und ONO. zu O., SOS. und SWS. zu S., WSW. und WNW. zu W. geschlagen wurden (b1). Gezählt werden Beobachtungen der unteren allgemeinen Windströmung; Stärke und obere Strömung fehlen, Windstille wird nicht ausgewiesen. Eigene Rechenschritte: Prozentanteile der Richtungen an den Beobachtungen des jeweiligen Monats bzw. der Jahreszeit (meteorologische Jahreszeiten: Winter = Dezember–Februar, Frühling = März–Mai, Sommer = Juni–August, Herbst = September–November; Brückner selbst teilt nicht so ein). In den Windrosen ist die Fläche der Keile dem Anteil proportional (Radius ∝ √Anteil); die Ringe markieren 10, 20 und 30 %. Die Himmelsrichtungen folgen der Originalschreibung N, NO, O, SO, S, SW, W, NW (englisch NE, E, SE).",
        "The figures come from the monthly table on p. 62 (b3, rows January–December). Brückner reduced the original 16 points of the compass to eight by merging NNE and NNW into N, ENE and ESE into E, SSE and SSW into S, WSW and WNW into W (b1). What is counted are observations of the lower general wind current; strength and upper current are missing, and calms are not reported. Own calculations: percentage shares of each direction among the observations of the month or season (meteorological seasons: winter = December–February, spring = March–May, summer = June–August, autumn = September–November; Brückner does not group them this way). In the wind roses the area of each wedge is proportional to the share (radius ∝ √share); the rings mark 10, 20 and 30 %. Compass points follow the original spelling N, NO, O, SO, S, SW, W, NW (English: NE, E, SE)."),
    "findings": [
        bi(f"Der Südwind ist die häufigste Richtung: {fmt(agg[('Gesamtjahr','S')][0],'de')} von {fmt(TOTAL,'de')} Beobachtungen ({F(S_year)[0]} %). Es folgen N ({F(N_year)[0]} %) und W ({F(W_year)[0]} %); am seltensten ist SO ({F(SO_year)[0]} %).",
           f"Southerly wind is the most frequent direction: {fmt(agg[('Gesamtjahr','S')][0],'en')} of {fmt(TOTAL,'en')} observations ({F(S_year)[1]} %). N ({F(N_year)[1]} %) and W ({F(W_year)[1]} %) follow; SE is rarest ({F(SO_year)[1]} %)."),
        bi(f"Im Winter kommt mehr als jede dritte Beobachtung aus Süden ({F(S_win)[0]} %; Januar {F(S_jan)[0]} %), im Herbst {F(S_aut)[0]} %, im Sommer nur {F(S_sum)[0]} % (Juni {F(S_jun)[0]} %).",
           f"In winter more than every third observation is from the south ({F(S_win)[1]} %; January {F(S_jan)[1]} %), in autumn {F(S_aut)[1]} %, in summer only {F(S_sum)[1]} % (June {F(S_jun)[1]} %)."),
        bi(f"Im Sommer ist W die häufigste Richtung ({F(W_sum)[0]} %; Juli {F(W_jul)[0]} %), dazu kommen N ({F(N_sum)[0]} %) und NW ({F(NW_sum)[0]} %); der Nordwind erreicht im Frühling mit {F(N_spr)[0]} % seinen höchsten Jahreszeitenanteil, im Winter nur {F(N_win)[0]} %.",
           f"In summer W is the most frequent direction ({F(W_sum)[1]} %; July {F(W_jul)[1]} %), followed by N ({F(N_sum)[1]} %) and NW ({F(NW_sum)[1]} %); northerly wind peaks in spring at {F(N_spr)[1]} % and drops to {F(N_win)[1]} % in winter."),
        bi("Brückner erklärt das Übergewicht von Süd- und Nordwind in Gera damit, dass Strömungen aus SO und SW sowie aus NO und NW beim Eintritt ins Elstertal in die Talrichtung nach S bzw. N gelenkt werden (S. 64). Die geringen SO- und NO-Anteile passen zu dieser Deutung, belegen sie aber nicht.",
           "Brückner explains the preponderance of south and north winds at Gera by flows from SE and SW and from NE and NW being deflected into the valley axis, S or N, on entering the Elster valley (p. 64). The small SE and NE shares fit this reading but do not prove it."),
    ],
    "caveats": [
        bi(f"Die Tabelle nennt keine Einheit. Die Summe von {fmt(TOTAL,'de')} entspricht bei zehn Jahren rund {fmt(per_day10,'de',1)} Beobachtungen pro Tag; S. 54 nennt nur drei Ablesungen täglich (Kratzsch eine bis zwei). Zeitraum und Zähleinheit sind also nicht sicher. Die Prozentanteile hängen davon nicht ab; die von Brückner gedruckten Jahresmittel (Summe ÷ 10) schon, sie werden hier nicht verwendet.",
           f"The table names no unit. The total of {fmt(TOTAL,'en')} equals about {fmt(per_day10,'en',1)} observations per day over ten years, whereas p. 54 speaks of only three readings a day (Kratzsch one to two). Period and counting unit are therefore uncertain. The percentage shares do not depend on this; Brückner's printed annual means (sum ÷ 10) do, and they are not used here."),
        bi("Die Verteilung gilt für die Windfahne am Beobachtungsort (untere Strömung). Sie ist durch die Lage im Elstertal geprägt und nicht für das ganze Land repräsentativ; der Vergleich mit Hohenleuben, Schleiz und Rothenacker steht in einer eigenen Auswertung.",
           "The distribution is that of the wind vane at the observing site (lower current). It is shaped by the location in the Elster valley and is not representative of the whole country; the comparison with Hohenleuben, Schleiz and Rothenacker is given in a separate analysis."),
    ],
    "datasets": [
        {"name": "monthly", "title": bi("Windbeobachtungen in Gera nach Monat und Richtung, 1856–1865", "Wind observations at Gera by month and direction, 1856–1865"),
         "columns": [
             col("month", "Monat", "Month", "integer", None, True, "Monatsnummer 1–12, editorisch"),
             col("month_label", "Monat (Original)", "Month (original)", "string"),
             col("direction", "Richtung", "Direction", "string", None, False, "N, NO, O, SO, S, SW, W, NW; Original »N.« usw."),
             col("dir_index", "Reihenfolge der Richtung", "Direction order", "integer", None, True, "1 = N … 8 = NW im Uhrzeigersinn"),
             col("count", "Beobachtungen", "Observations", "integer", "Zahl", False),
             col("month_share", "Anteil im Monat", "Share within month", "number", "%", True),
             col("season", "Jahreszeit", "Season", "string", None, True, "meteorologische Jahreszeit"),
             col("season_order", "Reihenfolge der Jahreszeit", "Season order", "integer", None, True),
         ], "rows": monthly_rows, "source_refs": [{"page": "62", "block": "b3", "rows": "r2-r13"}]},
        {"name": "seasonal", "title": bi("Richtungsanteile nach Jahreszeit und im Gesamtjahr", "Direction shares by season and for the whole year"),
         "columns": [
             col("period", "Zeitraum", "Period", "string", None, True),
             col("period_order", "Reihenfolge", "Order", "integer", None, True),
             col("direction", "Richtung", "Direction", "string", None, False),
             col("dir_index", "Reihenfolge der Richtung", "Direction order", "integer", None, True),
             col("count", "Beobachtungen", "Observations", "integer", "Zahl", True, "Summe der Monatswerte"),
             col("share", "Anteil", "Share", "number", "%", True),
         ], "rows": seasonal_rows, "source_refs": [{"page": "62", "block": "b3", "rows": "r2-r15"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "seasonal",
         "title": bi("Windrosen nach Jahreszeit", "Wind roses by season"),
         "caption": bi("Anteil der acht Richtungen an den Beobachtungen in Gera, 1856–1865 (Fläche ∝ Anteil; Ringe bei 10, 20, 30 %). Das Gesamtjahr wird vom Südwind bestimmt; im Winter überwiegt er deutlich, im Sommer führt der Westwind.",
                       "Share of the eight directions among the observations at Gera, 1856–1865 (area ∝ share; rings at 10, 20, 30 %). The year as a whole is dominated by southerly wind; in winter it prevails clearly, in summer westerly wind leads."),
         "vegalite": rose_spec("period_label", "period_order", columns=3, cell=200, rmax=66, label_r=91,
                               extra_transform=[{"calculate": bi("datum.period", "{'Gesamtjahr':'Whole year','Winter':'Winter','Frühling':'Spring','Sommer':'Summer','Herbst':'Autumn'}[datum.period]"), "as": "period_label"}],
                               tooltip_extra=[{"field": "count", "title": bi("Beobachtungen", "Observations")}])},
        {"id": "c2", "dataset": "monthly",
         "title": bi("Windrichtung nach Monat", "Wind direction by month"),
         "caption": bi("Anteil jeder Richtung an den Beobachtungen des Monats (%). Der Südwind ist von September bis März die häufigste Richtung; im Frühjahr und Sommer verschiebt sich das Gewicht auf N, W und NW.",
                       "Share of each direction among the observations of the month (%). Southerly wind is the most frequent direction from September to March; in spring and summer the weight shifts to N, W and NW."),
         "vegalite": {
             "height": 340,
             "transform": [DIR_LABEL_CALC, MONTH_ABBR_CALC],
             "mark": "rect",
             "encoding": {
                 "x": {"field": "dir_label", "type": "ordinal", "sort": {"field": "dir_index", "op": "min"}, "title": bi("Richtung", "Direction"), "axis": {"labelAngle": 0, "orient": "top"}},
                 "y": {"field": "mlabel", "type": "ordinal", "sort": {"field": "month", "op": "min"}, "title": bi("Monat", "Month")},
                 "color": {"field": "month_share", "type": "quantitative", "title": bi("Anteil im Monat (%)", "Share within month (%)")},
                 "tooltip": [{"field": "month_label", "title": bi("Monat", "Month")},
                             {"field": "dir_label", "title": bi("Richtung", "Direction")},
                             {"field": "count", "title": bi("Beobachtungen", "Observations")},
                             {"field": "month_share", "title": "%", "format": ".1f"}]}}},
    ],
    "keywords": {
        "de": ["Wind", "Windrichtung", "Windrose", "Gera", "Elstertal", "Südwind", "Westwind", "Meteorologie"],
        "en": ["wind", "wind direction", "wind rose", "Gera", "Elster valley", "south wind", "west wind", "meteorology"]},
    "related": ["klima-wind-stationen-vergleich"],
    "supersedes_legacy": "p. 62 'Windverhältnisse zu Gera 1856–1865' (iframe: wind rose by season, monthly heatmap, bar chart)",
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
