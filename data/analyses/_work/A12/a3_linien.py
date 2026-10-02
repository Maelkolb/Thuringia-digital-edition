"""Analysis: lines and houses of the Voigte/Reuss family 1240-1870 (Landesteilungen)."""
import statistics
from common import *

BR = {  # branch codes -> (de, en)
    "voigte": ("Voigte", "Voigts"),
    "alt": ("Reuß ä. L.", "Reuss older line"),
    "jung": ("Reuß j. L.", "Reuss younger line"),
}
END = 1870  # year of publication: "open" lines are shown up to here

# (branch, label_de, label_en, start, end(None=open), start_note, end_note, [(page, block)...])
H = [
 ("voigte","Weida","Weida",1240,1535,"Teilung um 1240","stirbt ca. 1535 aus",[("403","b1"),("403","b2"),("333","b3")]),
 ("voigte","Gera","Gera",1240,1550,"Teilung um 1240","stirbt 1550 aus",[("403","b1"),("403","b2"),("341","b4")]),
 ("voigte","Plauen (bis zur Teilung)","Plauen (until the division)",1240,1305,"Teilung um 1240","Teilung ca. 1305",[("403","b1"),("403","b2"),("355","b1")]),
 ("voigte","Plauen, älterer Zweig (burggräflich)","Plauen, older branch (burgraves)",1305,1572,"Teilung ca. 1305","stirbt 1572 aus",[("403","b3"),("355","b1"),("363","b1")]),
 ("voigte","Reuß-Plauen (jüngerer Zweig)","Reuss-Plauen (younger branch)",1305,1564,"Teilung ca. 1305","Teilung 1564 in drei Linien",[("403","b3"),("355","b1"),("374","b2")]),
 ("alt","Untergreiz (Heinrich d. ä. und Söhne)","Untergreiz (Heinrich the elder and sons)",1564,1596,"Teilung 1564","Teilung 1596",[("403","b4"),("389","b4"),("374","b2")]),
 ("alt","Obergreiz (mittlere Linie)","Obergreiz (middle line)",1564,1616,"Teilung 1564","stirbt 1616 aus",[("403","b4"),("375","b1"),("374","b2")]),
 ("alt","Dölau (Heinrich V., Residenz)","Dölau (Heinrich V., residence)",1583,1596,"Teilung 1583","Teilung 1596",[("389","b4")]),
 ("alt","Burgk (Zweig, 1. Mal)","Burgk (branch, first time)",1596,1640,"Teilung 1596","stirbt 1640 aus",[("403","b5"),("389","b4"),("390","b2")]),
 ("alt","Untergreiz (Zweig Heinrichs V.)","Untergreiz (Heinrich V.'s branch)",1596,1625,"Teilung 1596","Teilung 1625",[("403","b5"),("390","b3")]),
 ("alt","Dölau (1. Mal)","Dölau (first time)",1616,1636,"Teilung unter den Burgker Brüdern 1616","stirbt 1636 erblos",[("390","b2")]),
 ("alt","Untergreiz (Specialhaus)","Untergreiz (special house)",1625,1768,"Teilung 1625","stirbt 1768 aus",[("403","b5"),("390","b3"),("390","b4"),("391","b1")]),
 ("alt","Obergreiz (Specialhaus)","Obergreiz (special house)",1625,None,"Teilung 1625","besteht fort als Fürstentum Reuß ä. L. (ab 1768 Greiz)",[("403","b6"),("390","b3"),("390","b4"),("391","b1")]),
 ("alt","Burgk (2. Mal)","Burgk (second time)",1668,1698,"Teilung 1668","Heinrich II. stirbt 1697 ohne Erben",[("390","b4"),("390","b5"),("391","b1")]),
 ("alt","Rothenthal","Rothenthal",1668,1698,"Teilung 1668","Heinrich V. stirbt 1698 ohne Erben",[("390","b4"),("390","b5"),("391","b1")]),
 ("alt","Dölau (2. Mal)","Dölau (second time)",1694,1698,"Teilung 1694","erlischt 1698",[("390","b4"),("391","b2"),("403","b6")]),
 ("jung","Gera (Heinrich Posthumus, ungeteilt)","Gera (Heinrich Posthumus, undivided)",1564,1647,"Teilung 1564","Teilung 1647",[("375","b2"),("376","b1"),("403","b4")]),
 ("jung","Gera (Specialhaus)","Gera (special house)",1647,1802,"Teilung 1647","stirbt 1802 aus",[("376","b1"),("376","b2"),("379","b2"),("380","b1"),("403","b6")]),
 ("jung","Schleiz (Specialhaus)","Schleiz (special house)",1647,None,"Teilung 1647","erbt 1848 das ganze Land",[("376","b1"),("376","b2"),("383","b2"),("385","b1"),("403","b6")]),
 ("jung","Lobenstein (bis 1678 ungeteilt)","Lobenstein (undivided until 1678)",1647,1678,"Teilung 1647","Teilung 1678",[("376","b1"),("376","b2"),("380","b2"),("403","b6")]),
 ("jung","Saalburg","Saalburg",1647,1666,"Teilung 1647","1666 zertheilt",[("376","b1"),("376","b2"),("403","b5")]),
 ("jung","Lobenstein (Zweig)","Lobenstein (branch)",1678,1824,"Teilung 1678","erlischt 1824",[("380","b2"),("381","b1"),("403","b6")]),
 ("jung","Hirschberg (Zweig)","Hirschberg (branch)",1678,1711,"Teilung 1678","stirbt 1711 aus",[("380","b2"),("403","b6")]),
 ("jung","Ebersdorf (Zweig)","Ebersdorf (branch)",1678,1848,"Teilung 1678","tritt 1848 das Land an Schleiz ab (hatte 1824 Lobenstein geerbt)",[("380","b2"),("381","b2"),("382","b1"),("403","b6")]),
]

# check years against the cited blocks
for h in H:
    for yr in (h[3], h[4]):
        if yr is None:
            continue
        ys = set()
        for pb in h[7]:
            ys |= years_in(*pb)
        assert yr in ys, (h[1], yr, "not found in", h[7])


def active(h, y):
    end = h[4] if h[4] is not None else END
    return h[3] <= y < end


periods = []
for br in ("voigte", "alt", "jung"):
    hs = [h for h in H if h[0] == br]
    cps = sorted({h[3] for h in hs} | {h[4] if h[4] is not None else END for h in hs})
    for x, y in zip(cps, cps[1:]):
        names = [h[1] for h in hs if active(h, x)]
        if names:
            periods.append((br, x, y, len(names), names))

# printed table (p. 390, b4): houses of the older line 1625-1768
printed = {(1625, 1636): 4, (1636, 1640): 3, (1640, 1667): 2, (1668, 1694): 4, (1694, 1698): 5, (1698, 1768): 2}
for (x, y), n in printed.items():
    ca = sum(1 for h in H if h[0] == "alt" and active(h, x))
    assert ca == n, (x, y, n, ca)

years = sorted({p[1] for p in periods} | {p[2] for p in periods})
yearly = []
for y in years + [END]:
    for br in ("voigte", "alt", "jung"):
        yy = y if y != END else END - 1
        n = sum(1 for h in H if h[0] == br and active(h, yy))
        yearly.append([y, br, BR[br][0], BR[br][1], n])
tot = {}
for r in yearly:
    tot[r[0]] = tot.get(r[0], 0) + r[4]
mx = max(tot.values())
mxyears = sorted(y for y, t in tot.items() if t == mx)
nxt = [y for y in sorted(tot) if y > mxyears[0]][0]
reuss_closed = [h for h in H if h[0] in ("alt", "jung") and h[4] is not None]
dur = [h[4] - h[3] for h in reuss_closed]
wei = 1535 - 1240
ger = 1550 - 1240
pla = 1572 - 1305
maxalt = max(p[3] for p in periods if p[0] == "alt")
maxjung = max(p[3] for p in periods if p[0] == "jung")
assert maxalt == maxjung == 5 and mx == 10 and mxyears[0] == 1694 and nxt == 1698
j_first5 = [p[1:3] for p in periods if p[0] == "jung" and p[3] == 5][0]
med = int(statistics.median(dur))

EN = {
 "Teilung um 1240": "division c. 1240", "stirbt ca. 1535 aus": "dies out c. 1535", "stirbt 1550 aus": "dies out 1550", "Teilung ca. 1305": "division c. 1305",
 "stirbt 1572 aus": "dies out 1572", "Teilung 1564 in drei Linien": "division of 1564 into three lines", "Teilung 1564": "division 1564", "Teilung 1596": "division 1596",
 "stirbt 1616 aus": "dies out 1616", "Teilung 1583": "division 1583", "stirbt 1640 aus": "dies out 1640", "Teilung 1625": "division 1625",
 "Teilung unter den Burgker Brüdern 1616": "division between the Burgk brothers 1616", "stirbt 1636 erblos": "dies out 1636 without heirs",
 "stirbt 1768 aus": "dies out 1768", "besteht fort als Fürstentum Reuß ä. L. (ab 1768 Greiz)": "continues as principality Reuss o. l. (Greiz from 1768)", "Teilung 1668": "division 1668",
 "Heinrich II. stirbt 1697 ohne Erben": "Heinrich II. dies 1697 without heirs", "Heinrich V. stirbt 1698 ohne Erben": "Heinrich V. dies 1698 without heirs",
 "Teilung 1694": "division 1694", "erlischt 1698": "extinct 1698", "Teilung 1647": "division 1647", "stirbt 1802 aus": "dies out 1802",
 "erbt 1848 das ganze Land": "inherits the whole land 1848", "Teilung 1678": "division 1678", "1666 zertheilt": "split up 1666", "erlischt 1824": "extinct 1824",
 "stirbt 1711 aus": "dies out 1711", "tritt 1848 das Land an Schleiz ab (hatte 1824 Lobenstein geerbt)": "cedes the land to Schleiz 1848 (had inherited Lobenstein in 1824)", "Teilung 1647 ": "division 1647",
}
rows_h = []
for i, h in enumerate(H, 1):
    rows_h.append([i, h[0], BR[h[0]][0], BR[h[0]][1], h[1], h[2], h[3], h[4], h[4] if h[4] is not None else END,
                   f"{h[5]}; {h[6]}", f"{EN[h[5]]}; {EN[h[6]]}"])
rows_p = [[i, p[0], BR[p[0]][0], BR[p[0]][1], p[1], p[2], p[3], "; ".join(p[4])] for i, p in enumerate(periods, 1)]

H_REFS = refs_from([pb for h in H for pb in h[7]])
BRDOM = [bi(BR[b][0], BR[b][1]) for b in ("voigte", "alt", "jung")]
YEAR = bi("Jahr", "Year")
BRCOL = {"field": bi("branch_de", "branch_en"), "type": "nominal", "title": bi("Linie", "Line"), "scale": {"domain": BRDOM}}
LABEL = bi("label_de", "label_en")

a = {
 "id": "geschichte-landesteilungen-linien-1240-1870",
 "title": bi("Landesteilungen und Linien des Hauses Weida–Reuß 1240–1870", "Divisions of the land and lines of the house of Weida–Reuss, 1240–1870"),
 "category": "history",
 "section": "t1-5-3",
 "sources": H_REFS,
 "summary": bi(
  "Brückner beschreibt die Geschichte des Voigt- und Reußenhauses als Folge von Landesteilungen und Aussterben von Linien und fasst sie in Tab. XV (S. 403) sowie in einer Tabelle der älteren Linie (S. 390) zusammen. Der Datensatz erfasst 24 Linien und Häuser mit Anfangs- und Endjahr; die Diagramme zeigen ihre Lebensdauer und die Zahl der gleichzeitig regierenden Linien. Aus drei Linien um 1240 wurden bis 1694 zehn gleichzeitig regierende Häuser; die Wiedervereinigung erfolgte in der älteren Linie 1768, in der jüngeren 1848.",
  "Brückner presents the history of the Voigt and Reuss house as a sequence of divisions of the land and extinctions of lines, summarised in Tab. XV (p. 403) and in a table for the older line (p. 390). The dataset records 24 lines and houses with their start and end years; the charts show their duration and the number of lines ruling at the same time. From three lines around 1240 the family grew to ten simultaneously ruling houses by 1694; the land was reunited in the older line in 1768 and in the younger line in 1848."),
 "method": bi(
  "Jede Linie bzw. jedes Haus ist eine Zeile mit Anfangs- und Endjahr, entnommen aus Tab. XV (S. 403 b1–b6), der Tabelle der Häuser der älteren Linie (S. 390 b4) und dem Fließtext (S. 333, 355, 363, 374–376, 379–385, 389–391). Ungefähre Angaben (»um 1240«, »ca. 1305«, »ca. 1535«) stehen als Jahreszahl. Als Linie oder Haus zählt, was Brückner als eigene Herrschaft (Specialhaus, Zweig, Stammlinie) bezeichnet; die Paragiate Köstritz und die Nebenlinie Lobenstein-Selbitz sind nicht gezählt. Wo sich die Zusammensetzung mitten in einer Linie ändert, ist sie in Abschnitte zerlegt (z. B. Gera 1564–1647 ungeteilt, ab 1647 Specialhaus). Die Zahl der gleichzeitig bestehenden Linien (Datensätze »periods« und »yearly«) ist abgeleitet: Sie wurde aus den Zeilen berechnet; für 1625–1768 stimmt sie mit der gedruckten Tabelle auf S. 390 überein (4, 3, 2, 4, 5, 2, 1). Noch bestehende Linien sind bis 1870, dem Erscheinungsjahr, gezeichnet.",
  "Each line or house is one row with its start and end year, taken from Tab. XV (p. 403 b1–b6), the table of the houses of the older line (p. 390 b4) and the running text (pp. 333, 355, 363, 374–376, 379–385, 389–391). Approximate statements (“c. 1240”, “c. 1305”, “c. 1535”) are entered as years. A line or house is whatever Brückner treats as a separate lordship (special house, branch, parent line); the appanages of Köstritz and the side line Lobenstein-Selbitz are not counted. Where the composition changes within a line it is split into periods (e.g. Gera undivided 1564–1647, special house from 1647). The number of simultaneously existing lines (datasets “periods” and “yearly”) is derived: it was computed from the rows; for 1625–1768 it agrees with the printed table on p. 390 (4, 3, 2, 4, 5, 2, 1). Lines that still exist are drawn up to 1870, the year of publication."),
 "findings": [
  bi(f"Aus drei Linien (Weida, Gera, Plauen) um 1240 wurden durch Teilungen bis {mxyears[0]} insgesamt {mx} gleichzeitig regierende Linien und Häuser: je {maxalt} in der älteren und in der jüngeren Reuß-Linie (Höchststand {mxyears[0]}–{nxt}; die jüngere Linie hatte schon {j_first5[0]}–{j_first5[1]} fünf).",
     f"Divisions turned the three lines (Weida, Gera, Plauen) of c. 1240 into as many as {mx} simultaneously ruling lines and houses by {mxyears[0]}: {maxalt} each in the older and the younger Reuss line (peak {mxyears[0]}–{nxt}; the younger line already had five in {j_first5[0]}–{j_first5[1]})."),
  bi(f"Von den drei Voigt-Linien starben Weida (1240–1535, {wei} Jahre), Gera (1240–1550, {ger} Jahre) und der ältere Zweig von Plauen (1305–1572, {pla} Jahre) aus; fortgeführt wurde nur der jüngere Zweig Reuß-Plauen, der 1564 in drei Linien geteilt wurde.",
     f"Of the three Voigt lines, Weida (1240–1535, {wei} years), Gera (1240–1550, {ger} years) and the older branch of Plauen (1305–1572, {pla} years) died out; only the younger branch Reuss-Plauen continued, divided into three lines in 1564."),
  bi(f"Die ältere Linie war seit 1768 wieder in einer Hand, die jüngere erst seit 1848, also {1848-1768} Jahre später; die jüngere Linie blieb von 1564 bis 1647 ({1647-1564} Jahre) ungeteilt, die ältere Linie bestand dagegen seit 1564 aus zwei, ab 1583 aus drei Häusern.",
     f"The older line was reunited in 1768, the younger one only in 1848, {1848-1768} years later; the younger line stayed undivided from 1564 to 1647 ({1647-1564} years), whereas the older line consisted of two houses from 1564 and of three from 1583."),
  bi(f"Von den {len(reuss_closed)} Häusern und Zweigen der Reuß-Zeit (ab 1564), die vor 1870 endeten, bestand die Hälfte höchstens {med} Jahre (Median); am längsten hielten sich Ebersdorf (170), Gera (155), Lobenstein (146) und Untergreiz (143 Jahre).",
     f"Of the {len(reuss_closed)} houses and branches of the Reuss period (from 1564) that ended before 1870, half lasted at most {med} years (median); the longest-lived were Ebersdorf (170), Gera (155), Lobenstein (146) and Untergreiz (143 years)."),
 ],
 "caveats": [
  bi("Die Einteilung in Linien, Zweige und Häuser folgt Brückners Terminologie, ist aber nicht überall trennscharf (z. B. entstehen Burgk und Dölau zweimal); die Zählung gleichzeitiger Linien ist eine redaktionelle Ableitung.",
     "The division into lines, branches and houses follows Brückner's terminology but is not sharp everywhere (e.g. Burgk and Dölau arise twice); the count of simultaneous lines is an editorial derivation."),
  bi("Ungefähre Jahreszahlen (um 1240, ca. 1305, ca. 1535) sind als Punktwerte eingetragen. Brückner nennt für Schleiz 204 Jahre, für Lobenstein 201 Jahre (S. 380, 383); bei gleichem Beginn 1647 und dem Ende 1848 ergeben sich für beide 201 Jahre, hier gilt daher 1647–1848 für beide.",
     "Approximate years (c. 1240, c. 1305, c. 1535) are entered as point values. Brückner gives 204 years for Schleiz and 201 for Lobenstein (pp. 380, 383); with the same start in 1647 and an end in 1848 both come to 201 years, so 1647–1848 is used for both."),
  bi("Die Greizer Tabelle (S. 390) nennt 1667 und 1668 als Grenzjahre; das Jahr dazwischen bleibt, wie gedruckt, ohne Angabe.",
     "The Greiz table (p. 390) gives 1667 and 1668 as boundary years; the year in between is left blank, as printed."),
 ],
 "datasets": [
  {"name": "houses", "title": bi("Linien und Häuser mit Anfangs- und Endjahr", "Lines and houses with start and end year"),
   "columns": [
     {"name": "ord", "label": bi("Reihenfolge", "Order"), "type": "integer", "unit": None, "derived": True},
     {"name": "branch", "label": bi("Zweig (Code)", "Branch (code)"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_de", "label": bi("Zweig", "Branch"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_en", "label": bi("Zweig (englisch)", "Branch (English)"), "type": "string", "unit": None, "derived": True},
     {"name": "label_de", "label": bi("Linie/Haus", "Line/house"), "type": "string", "unit": None},
     {"name": "label_en", "label": bi("Linie/Haus (englisch)", "Line/house (English)"), "type": "string", "unit": None, "derived": True},
     {"name": "start_year", "label": bi("Beginn", "Start"), "type": "integer", "unit": None},
     {"name": "end_year", "label": bi("Ende (leer = besteht fort)", "End (empty = continues)"), "type": "integer", "unit": None},
     {"name": "end_plot", "label": bi("Ende für die Zeichnung", "End for plotting"), "type": "integer", "unit": None, "derived": True, "note": "offene Linien bis 1870"},
     {"name": "event_de", "label": bi("Beginn und Ende (Brückner)", "Start and end (Brückner)"), "type": "string", "unit": None},
     {"name": "event_en", "label": bi("Beginn und Ende (englisch)", "Start and end (English)"), "type": "string", "unit": None, "derived": True},
   ], "rows": rows_h, "source_refs": H_REFS},
  {"name": "periods", "title": bi("Zahl der gleichzeitig regierenden Linien nach Abschnitten", "Number of simultaneously ruling lines by period"),
   "columns": [
     {"name": "ord", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
     {"name": "branch", "label": bi("Zweig (Code)", "Branch (code)"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_de", "label": bi("Zweig", "Branch"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_en", "label": bi("Zweig (englisch)", "Branch (English)"), "type": "string", "unit": None, "derived": True},
     {"name": "from_year", "label": bi("von", "from"), "type": "integer", "unit": None},
     {"name": "to_year", "label": bi("bis", "to"), "type": "integer", "unit": None, "derived": True, "note": "Wechseljahr bzw. 1870 (Erscheinungsjahr) für noch bestehende Linien"},
     {"name": "n_lines", "label": bi("Anzahl", "Count"), "type": "integer", "unit": None, "derived": True},
     {"name": "lines", "label": bi("Linien/Häuser", "Lines/houses"), "type": "string", "unit": None, "derived": True},
   ], "rows": rows_p, "source_refs": H_REFS},
  {"name": "yearly", "title": bi("Zahl der Linien je Zweig an den Wechseljahren", "Number of lines per branch at the years of change"),
   "columns": [
     {"name": "year", "label": YEAR, "type": "integer", "unit": None, "derived": True, "note": "Wechseljahre aus den Linien; 1870 = Erscheinungsjahr"},
     {"name": "branch", "label": bi("Zweig (Code)", "Branch (code)"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_de", "label": bi("Zweig", "Branch"), "type": "string", "unit": None, "derived": True},
     {"name": "branch_en", "label": bi("Zweig (englisch)", "Branch (English)"), "type": "string", "unit": None, "derived": True},
     {"name": "n_lines", "label": bi("Anzahl", "Count"), "type": "integer", "unit": None, "derived": True},
   ], "rows": yearly, "source_refs": H_REFS},
 ],
 "charts": [
  {"id": "c1", "dataset": "houses",
   "title": bi("Lebensdauer der Linien und Häuser", "Duration of the lines and houses"),
   "caption": bi("Jeder Balken eine Linie oder ein Haus von der Teilung (oder dem Anfall) bis zum Aussterben oder zur Vereinigung; ein Pfeil bedeutet, dass die Linie 1870 noch besteht.",
                 "Each bar is a line or house from its division (or inheritance) to extinction or merger; an arrow means that the line still exists in 1870."),
   "vegalite": {"height": 440,
    "layer": [
     {"mark": {"type": "bar", "height": 11},
      "encoding": {
       "y": {"field": LABEL, "type": "ordinal", "sort": {"field": "ord", "op": "min"}, "title": None, "axis": {"labelLimit": 330}},
       "x": {"field": "start_year", "type": "quantitative", "title": YEAR, "axis": {"format": "d", "tickCount": 10}, "scale": {"domain": [1230, 1880]}},
       "x2": {"field": "end_plot"},
       "color": BRCOL,
       "tooltip": [{"field": LABEL, "title": bi("Linie/Haus", "Line/house")},
                   {"field": "start_year", "title": bi("Beginn", "Start")},
                   {"field": "end_plot", "title": bi("Ende (1870 = besteht fort)", "End (1870 = continues)")},
                   {"field": bi("event_de", "event_en"), "title": bi("Brückner", "Brückner")}]}},
     {"transform": [{"filter": "datum.end_year == null"}],
      "mark": {"type": "point", "shape": "triangle-right", "size": 90, "filled": True},
      "encoding": {"y": {"field": LABEL, "type": "ordinal", "sort": {"field": "ord", "op": "min"}},
                   "x": {"field": "end_plot", "type": "quantitative"}, "color": BRCOL}},
    ]}},
  {"id": "c2", "dataset": "yearly",
   "title": bi("Gleichzeitig regierende Linien und Häuser", "Simultaneously ruling lines and houses"),
   "caption": bi("Gestapelt nach Zweig, jeweils ab einem Jahr, in dem sich die Zahl änderte. Der Höchststand liegt 1694–1698 bei zehn (fünf ältere, fünf jüngere Reuß-Linie).",
                 "Stacked by branch, each step starting in a year in which the number changed. The peak is ten in 1694–1698 (five of the older, five of the younger Reuss line)."),
   "vegalite": {"height": 260,
    "mark": {"type": "area", "interpolate": "step-after", "opacity": 0.85, "line": False},
    "encoding": {
      "x": {"field": "year", "type": "quantitative", "title": YEAR, "axis": {"format": "d", "tickCount": 10}, "scale": {"domain": [1240, 1870]}},
      "y": {"field": "n_lines", "type": "quantitative", "title": bi("Anzahl Linien/Häuser", "Number of lines/houses"), "stack": True},
      "color": BRCOL,
      "tooltip": [{"field": "year", "title": bi("ab Jahr", "from year")},
                  {"field": bi("branch_de", "branch_en"), "title": bi("Zweig", "Branch")},
                  {"field": "n_lines", "title": bi("Anzahl", "Count")}]}}},
 ],
 "keywords": {"de": ["Landesteilung", "Teilung", "Linien", "Weida", "Gera", "Plauen", "Greiz", "Schleiz", "Lobenstein", "Reuß", "Voigte", "Primogenitur", "Erbteilung"],
              "en": ["partition", "division of territory", "lines", "Weida", "Gera", "Plauen", "Greiz", "Schleiz", "Lobenstein", "Reuss", "Voigts", "primogeniture"]},
 "generated_by": "Claude Sonnet 5.5 (subagent A12)",
 "date": "2026-10-01",
}

if __name__ == "__main__":
    write_analysis(a)
    print("max total", mx, mxyears, nxt, "closed", len(reuss_closed), "median", med)
