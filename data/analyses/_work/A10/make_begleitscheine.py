"""A10: Begleitscheine 1858-1867 and Gera declarations 1867 (p. 261)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

g = grid("261", "b3")
years = [int(x.strip(" .")) for x in g[1][1:]]
assert years == list(range(1858, 1868)), years
OFFICES = {"Gera": 2, "Schleiz": 3, "Lobenstein": 4, "Hirschberg": 5}
REGION = {"Gera": "Unterland", "Schleiz": "Oberland", "Lobenstein": "Oberland", "Hirschberg": "Oberland"}
rows = []
cnt = {}
for off, ri in OFFICES.items():
    r = g[ri]
    for j, y in enumerate(years):
        v = num(r[1 + j])
        rows.append([off, y, v, REGION[off], f"r{ri + 1}"])
        cnt[(off, y)] = v or 0


def z(x):
    return x or 0


# regional index (1858 = 100)
reg = {}
for y in years:
    reg[("Unterland", y)] = cnt[("Gera", y)]
    reg[("Oberland", y)] = sum(cnt[(o, y)] for o in ("Schleiz", "Lobenstein", "Hirschberg"))
idx_rows = []
for rg in ("Unterland", "Oberland"):
    base = reg[(rg, 1858)]
    for y in years:
        idx_rows.append([rg, y, reg[(rg, y)], round(reg[(rg, y)] / base * 100, 1)])
gera58, gera67 = cnt[("Gera", 1858)], cnt[("Gera", 1867)]
ob_max = max(reg[("Oberland", y)] for y in years)
ob_max_years = [y for y in years if reg[("Oberland", y)] == ob_max]
ob67 = reg[("Oberland", 1867)]
gera_share58 = gera58 / (gera58 + reg[("Oberland", 1858)]) * 100
gera_share67 = gera67 / (gera67 + ob67) * 100
sch58, sch67 = cnt[("Schleiz", 1858)], cnt[("Schleiz", 1867)]
gera_max = max(cnt[("Gera", y)] for y in years)
gera_decl = [y for y in years[1:] if cnt[("Gera", y)] < cnt[("Gera", y - 1)]]
ob58 = reg[("Oberland", 1858)]
print(gera_decl, reg, ob_max, ob_max_years, gera_share58, gera_share67)

# declarations 1867 (p. 261 b1) --------------------------------------------------------
DECL = [("Windisch-Warnow", 225), ("Herbesthal", 13), ("Bremen", 10), ("Bremerhaven", 7), ("Schaidt", 6), ("Harburg", 2),
        ("Geestemünde", 1), ("Passau", 1), ("Boitersreuth", 1)]
dtot = sum(n for _, n in DECL)
assert dtot == 266, dtot
decl_rows = [[p, n, round(n / dtot * 100, 1)] for p, n in DECL]
north_sea = sum(n for p, n in DECL if p in ("Bremen", "Bremerhaven", "Geestemünde", "Harburg"))
print("north sea", north_sea, north_sea / dtot * 100, 225 / dtot * 100)

OFF_ORDER = ["Gera", "Schleiz", "Lobenstein", "Hirschberg"]
OFF = {"de": "Erledigungsamt", "en": "Office"}
REG_CALC = {"de": "datum.region", "en": "{'Unterland':'Unterland (Gera)','Oberland':'Oberland (Schleiz, Lobenstein, Hirschberg)'}[datum.region]"}

ana = {
    "id": "handel-verkehr-begleitscheine-1858-1867",
    "title": {"de": "Begleitscheine 1858–1867: Handelstätigkeit in Ober- und Unterland", "en": "Customs transit documents 1858–1867: commercial activity in the Oberland and Unterland"},
    "category": "trade-transport",
    "section": "t1-3-7",
    "sources": [
        {"page": "261", "block": "b1"},
        {"page": "261", "block": "b2"},
        {"page": "261", "block": "b3", "rows": "h1-r6"},
        {"page": "261", "block": "b4"},
    ],
    "summary": {
        "de": f"Als Maß für die Entwicklung des Handels über die Landesgrenze druckt Brückner die Zahl der bei den Erledigungsämtern in Gera, Schleiz, Lobenstein und Hirschberg erledigten Begleitscheine für die zehn Jahre 1858–1867. Die Zahl in Gera steigt von {gera58} auf {gera67}, im Oberland sinkt sie von {ob58} auf {ob67}. Dazu nennt er die Bestimmungsorte der 266 Deklarationen, die 1867 in Gera erfolgten.",
        "en": f"As a gauge of the development of trade across the border Brückner prints the number of transit documents (Begleitscheine) cleared at the offices in Gera, Schleiz, Lobenstein and Hirschberg for the ten years 1858–1867. The number at Gera rises from {gera58} to {gera67}, in the Oberland it falls from {ob58} to {ob67}. He also names the destinations of the 266 declarations made at Gera in 1867.",
    },
    "method": {
        "de": "Die Tabelle S. 261 (4 Ämter × 10 Jahre) wurde ins Langformat übertragen; ein Strich ist als leerer Wert kodiert. Für den Vergleich der Landesteile wurden Schleiz, Lobenstein und Hirschberg zum Oberland zusammengefasst, Gera bildet das Unterland (Brückner: das Geschäft »des Oberlandes … rückwärts, die des Unterlandes vorwärts«); beide Reihen sind auf 1858 = 100 indiziert. Die Deklarationen 1867 stehen im Text S. 261 (b1); gezählt sind die Deklarationen, »lautend auf« den jeweiligen Ort, Prozentwerte sind berechnet.",
        "en": "The table on p. 261 (4 offices × 10 years) was transferred to long format; a dash is coded as an empty value. For the comparison of the districts Schleiz, Lobenstein and Hirschberg were combined as the Oberland, Gera forms the Unterland (Brückner: the business “of the Oberland … moved backward, that of the Unterland forward”); both series are indexed to 1858 = 100. The declarations of 1867 are in the text on p. 261 (b1); the declarations “addressed to” each place are counted, percentages are computed.",
    },
    "findings": [
        {"de": f"Die Zahl der in Gera erledigten Begleitscheine wächst von {gera58} (1858) auf {gera67} (1867), also um {de((gera67 / gera58 - 1) * 100)} %; Höchststand 1867; Rückgänge gegenüber dem Vorjahr nur in {' und '.join(str(y) for y in gera_decl)}.",
         "en": f"The number of transit documents cleared at Gera grows from {gera58} (1858) to {gera67} (1867), that is by {en((gera67 / gera58 - 1) * 100)} %; peak in 1867; declines against the previous year only in {' and '.join(str(y) for y in gera_decl)}."},
        {"de": f"In den drei oberländischen Ämtern zusammen steigen die Zahlen bis {ob_max} ({', '.join(str(y) for y in ob_max_years)}) und sinken bis 1867 auf {ob67}; Schleiz geht von {sch58} (1858) auf {sch67} (1867) zurück. Der Anteil Geras an allen Begleitscheinen steigt damit von {de(gera_share58, 1)} % auf {de(gera_share67, 1)} %.",
         "en": f"In the three Oberland offices together the numbers rise to {ob_max} ({', '.join(str(y) for y in ob_max_years)}) and fall to {ob67} by 1867; Schleiz declines from {sch58} (1858) to {sch67} (1867). Gera's share of all transit documents thus rises from {en(gera_share58, 1)} % to {en(gera_share67, 1)} %."},
        {"de": f"Von den 266 Deklarationen in Gera 1867 lauteten 225 ({de(225 / 266 * 100, 1)} %) auf Windisch-Warnow; Bremen, Bremerhaven, Geestemünde und Harburg (Hafenorte an Weser und Elbe) zusammen nur {north_sea} ({de(north_sea / dtot * 100, 1)} %). Brückner bemerkt, dass sich die Absatzwege des überseeischen Handels gegenüber früher (Bremen, Hamburg) verändert und vermehrt haben.",
         "en": f"Of the 266 declarations at Gera in 1867, 225 ({en(225 / 266 * 100, 1)} %) were addressed to Windisch-Warnow; Bremen, Bremerhaven, Geestemünde and Harburg (ports on the Weser and Elbe) together only {north_sea} ({en(north_sea / dtot * 100, 1)} %). Brückner remarks that the routes of overseas trade have changed and multiplied compared with earlier times (Bremen, Hamburg)."},
    ],
    "caveats": [
        {"de": "Die Begleitscheine erfassen nach Brückner nur einen Teil der Aus- und Einfuhr; er hält sie aber für kennzeichnend für den Gang des übrigen Verkehrs. Die Zahl der Scheine sagt nichts über Wert oder Menge der Waren.",
         "en": "According to Brückner the transit documents cover only a part of exports and imports; he nevertheless considers them characteristic of the course of the remaining traffic. The number of documents says nothing about the value or quantity of the goods."},
        {"de": "Die Zahl der Scheine hängt auch von der Lage und Zuständigkeit der Ämter ab (Hirschberg erscheint nur 1864–1866 mit je einem Schein). Brückner führt den Gegensatz von Ober- und Unterland auf die verschiedene Stellung zu den großen Verkehrsströmen zurück.",
         "en": "The number of documents also depends on the location and competence of the offices (Hirschberg appears only in 1864–1866 with one document each). Brückner traces the contrast between Oberland and Unterland to their different positions relative to the major traffic flows."},
        {"de": "Die Bedeutung der Orte der Deklarationen (z. B. Windisch-Warnow, Schaidt, Boitersreuth) erklärt der Text nicht; sie werden hier nur wie gedruckt wiedergegeben.",
         "en": "The text does not explain the significance of the places named in the declarations (e.g. Windisch-Warnow, Schaidt, Boitersreuth); they are reproduced here as printed."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "begleitscheine", "title": {"de": "Erledigte Begleitscheine nach Amt und Jahr", "en": "Cleared transit documents by office and year"},
         "columns": [
             {"name": "office", "label": OFF, "type": "string", "unit": None},
             {"name": "year", "label": {"de": "Jahr", "en": "Year"}, "type": "integer", "unit": None},
             {"name": "count", "label": {"de": "Erledigte Begleitscheine", "en": "Cleared transit documents"}, "type": "integer", "unit": "Scheine", "note": "Strich im Druck = leer"},
             {"name": "region", "label": {"de": "Landesteil", "en": "Region"}, "type": "string", "unit": None, "derived": True},
             {"name": "row", "label": {"de": "Tabellenzeile", "en": "Table row"}, "type": "string", "unit": None},
         ],
         "rows": rows, "source_refs": [{"page": "261", "block": "b3", "rows": "r2-r6"}]},
        {"name": "index", "title": {"de": "Begleitscheine nach Landesteil, Index 1858 = 100", "en": "Transit documents by region, index 1858 = 100"},
         "columns": [
             {"name": "region", "label": {"de": "Landesteil", "en": "Region"}, "type": "string", "unit": None, "derived": True},
             {"name": "year", "label": {"de": "Jahr", "en": "Year"}, "type": "integer", "unit": None},
             {"name": "count", "label": {"de": "Begleitscheine", "en": "Transit documents"}, "type": "integer", "unit": "Scheine", "derived": True},
             {"name": "index", "label": {"de": "Index 1858 = 100", "en": "Index 1858 = 100"}, "type": "number", "unit": None, "derived": True},
         ],
         "rows": idx_rows, "source_refs": [{"page": "261", "block": "b3", "rows": "r2-r6"}]},
        {"name": "deklarationen", "title": {"de": "Deklarationen in Gera 1867 nach Ort", "en": "Declarations at Gera in 1867 by place"},
         "columns": [
             {"name": "place", "label": {"de": "Ort (»lautend auf«)", "en": "Place (“addressed to”)"}, "type": "string", "unit": None},
             {"name": "count", "label": {"de": "Deklarationen", "en": "Declarations"}, "type": "integer", "unit": None},
             {"name": "share", "label": {"de": "Anteil", "en": "Share"}, "type": "number", "unit": "%", "derived": True},
         ],
         "rows": decl_rows, "source_refs": [{"page": "261", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "begleitscheine",
         "title": {"de": "Erledigte Begleitscheine je Amt", "en": "Cleared transit documents per office"},
         "caption": {"de": "Anzahl pro Jahr, 1858–1867. Gera wächst fast stetig, die oberländischen Ämter Schleiz und Lobenstein bleiben klein und gehen zurück; Hirschberg erscheint nur 1864–66 mit je einem Schein.",
                     "en": "Number per year, 1858–1867. Gera grows almost steadily, the Oberland offices of Schleiz and Lobenstein remain small and decline; Hirschberg appears only in 1864–66 with one document each."},
         "vegalite": {
             "height": 300,
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": {"de": "Jahr", "en": "Year"}, "axis": {"labelAngle": 0}},
                 "y": {"field": "count", "type": "quantitative", "title": {"de": "Begleitscheine", "en": "Transit documents"}},
                 "color": {"field": "office", "type": "nominal", "scale": {"domain": OFF_ORDER}, "title": OFF},
                 "tooltip": [{"field": "office", "title": OFF}, {"field": "year", "title": {"de": "Jahr", "en": "Year"}}, {"field": "count", "title": {"de": "Begleitscheine", "en": "Transit documents"}}]}}},
        {"id": "c2", "dataset": "index",
         "title": {"de": "Unterland und Oberland im Vergleich (Index 1858 = 100)", "en": "Unterland and Oberland compared (index 1858 = 100)"},
         "caption": {"de": "Gera (Unterland) gegen Schleiz, Lobenstein und Hirschberg zusammen (Oberland), je auf das Jahr 1858 bezogen. Die Reihen entwickeln sich in entgegengesetzte Richtungen, wie Brückner im Text feststellt.",
                     "en": "Gera (Unterland) against Schleiz, Lobenstein and Hirschberg together (Oberland), each relative to 1858. The series move in opposite directions, as Brückner states in the text."},
         "vegalite": {
             "height": 280,
             "transform": [{"calculate": REG_CALC, "as": "region_label"}],
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year", "type": "ordinal", "title": {"de": "Jahr", "en": "Year"}, "axis": {"labelAngle": 0}},
                      "y": {"field": "index", "type": "quantitative", "title": {"de": "Index (1858 = 100)", "en": "Index (1858 = 100)"}, "scale": {"zero": False}},
                      "color": {"field": "region", "type": "nominal", "scale": {"domain": ["Unterland", "Oberland"]}, "title": {"de": "Landesteil", "en": "Region"},
                                "legend": {"labelExpr": {"de": "datum.label", "en": "{'Unterland':'Unterland (Gera)','Oberland':'Oberland (3 offices)'}[datum.label]"}},},
                      "tooltip": [{"field": "region_label", "title": {"de": "Landesteil", "en": "Region"}}, {"field": "year", "title": {"de": "Jahr", "en": "Year"}},
                                  {"field": "count", "title": {"de": "Begleitscheine", "en": "Transit documents"}}, {"field": "index", "title": {"de": "Index", "en": "Index"}}]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 100}}},
             ]}},
        {"id": "c3", "dataset": "deklarationen",
         "title": {"de": "Deklarationen in Gera 1867 nach Ort", "en": "Declarations at Gera in 1867 by place"},
         "caption": {"de": "266 Deklarationen, »lautend auf« die genannten Orte (S. 261). Windisch-Warnow nimmt über vier Fünftel auf.",
                     "en": "266 declarations “addressed to” the places named (p. 261). Windisch-Warnow accounts for over four fifths."},
         "vegalite": {
             "height": 300,
             "layer": [
                 {"mark": "bar"},
                 {"mark": {"type": "text", "align": "left", "dx": 5}, "encoding": {"text": {"field": "count", "type": "quantitative"}}},
             ],
             "encoding": {
                 "y": {"field": "place", "type": "nominal", "sort": [p for p, _ in DECL], "title": None},
                 "x": {"field": "count", "type": "quantitative", "title": {"de": "Deklarationen", "en": "Declarations"}},
                 "tooltip": [{"field": "place", "title": {"de": "Ort", "en": "Place"}}, {"field": "count", "title": {"de": "Deklarationen", "en": "Declarations"}}, {"field": "share", "title": {"de": "Anteil (%)", "en": "Share (%)"}}]}}},
    ],
    "keywords": {"de": ["Begleitscheine", "Zoll", "Handel", "Außenhandel", "Gera", "Schleiz", "Lobenstein", "Hirschberg", "Deklarationen", "Windisch-Warnow", "Zollverein"],
                 "en": ["transit documents", "customs", "trade", "foreign trade", "Gera", "Schleiz", "Lobenstein", "Hirschberg", "declarations", "Zollverein"]},
    "related": ["handel-gewerbe-nach-landesteilen-1864", "verkehr-eisenbahn-geldinstitute-zeitleiste"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
