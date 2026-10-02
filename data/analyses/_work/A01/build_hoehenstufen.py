"""Build analysis relief-hoehenstufen-oberland-unterland (A01): key altitude levels (pp. 4-5, 10)."""
from common import *

T = lambda de, en: {"de": de, "en": en}
D = DFUSS_M
LB = T("Landesteil", "Part of the country")
COL = {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland"]}}
f0 = lambda x: fmt(x, 0)
f0e = lambda x: fmt(x, 0, "en")
m = lambda ft: ft * D

# ---- printed key levels (pp. 4-5, 10) ----------------------------------------------------------------------
t4b2, t4b3, t5b2, t10b1 = text("4", "b2"), text("4", "b3"), text("5", "b2"), text("10", "b1")
assert "1360'" in t4b2 and "730'" in t4b2 and "Fichteberg, 1925' hoch" in t4b3 and "800' hohes Niveau" in t4b3
assert "459' hoch" in t5b2 and "989' hoch" in t5b2 and "500'" in t10b1 and "394'" in t10b1
levels = [
    # landesteil, merkmal, ort, hoehe_fuss, label, label_links, seite, block
    ["Oberland", "höchster Punkt", "Fichteberg (Frankenwald)", 1925.0, "Fichteberg 1925′", 0, "4", "b3"],
    ["Oberland", "Mittel der Terrasse", "Saal-Elsterterrasse", 1360.0, "Terrasse im Mittel 1360′", 0, "4", "b2"],
    ["Oberland", "tiefster Punkt", "an der Leube", 800.0, "Leube 800′", 0, "4", "b3"],
    ["Unterland", "höchster Punkt", "Scheidberg", 989.0, "Scheidberg 989′", 0, "5", "b2"],
    ["Unterland", "Mittel der Terrasse", "mittleres Elstergebiet", 730.0, "Terrasse im Mittel 730′", 0, "4", "b2"],
    ["Unterland", "Mittel des Elsterbettes", "Elster im Unterland", 500.0, "Elsterbett im Mittel 500′", 0, "10", "b1"],
    ["Unterland", "tiefster Punkt", "Austritt der Elster aus dem Land", 459.0, "Elsteraustritt 459′", 1, "5", "b2"],
]
level_rows = [[a, b, c, d, round(m(d), 1), e, f, g] for a, b, c, d, e, f, g, _ in levels]

# ---- the six highest points of the Elster landscapes (p. 10 b2) ----------------------------------------------
g10 = grid("10", "b2")
land = []
import re
for ri, side, order in ((1, "Norden", 3), (2, "Mitte", 2), (3, "Süden", 1)):
    row = g10[ri]
    mw = re.match(r"^(\w+) (\d+)' (.*?),?$", row[0]); me = re.match(r"^(\d+)' (.*?),?$", row[2])
    assert mw.group(1) == side
    land.append(["Westlandschaft", side, order, mw.group(3).strip(), float(mw.group(2))])
    land.append(["Ostlandschaft", side, order, "Höhe bei " + me.group(2).replace("Höhe bei ", "").strip(), float(me.group(1))])
land_rows = [[a, b, c, d, e, round(m(e), 1)] for a, b, c, d, e in land]
print(land_rows)
W = {r[1]: r[4] for r in land if r[0] == "Westlandschaft"}
E = {r[1]: r[4] for r in land if r[0] == "Ostlandschaft"}

# ---- derived numbers -----------------------------------------------------------------------------------------------
rangeO = 1925 - 800; rangeU = 989 - 459
overlap = 989 - 800
bank_mean = 500 + 394
valley_depth = bank_mean - 500

# checks of Brückner's relative statements (pp. 16-18, 24)
t17, t18, t16 = text("17", "b2"), text("18", "b3"), text("16", "b4")
assert "213' tiefer" in t17 and "230' tiefer" in t18 and "1685'" in t16
rel_elias = 1925 - 213
rel_diebs = 1913 - 230
t24 = grid("24", "b1")
assert any("Nordhöhe von Eliasbrunn 1712'" in c for r in t24 for c in r)
assert any("Kulm 1913'" in c for r in t24 for c in r)
print(rel_elias, rel_diebs)

ana = {
    "id": "relief-hoehenstufen-oberland-unterland",
    "title": T("Höhenstufen des Landes: Ober- und Unterland im Vergleich", "Altitude belts of the country: Oberland and Unterland compared"),
    "category": "relief",
    "section": "t1-1-4",
    "sources": [
        {"page": "4", "block": "b2"}, {"page": "4", "block": "b3"}, {"page": "5", "block": "b2"},
        {"page": "10", "block": "b1"}, {"page": "10", "block": "b2"}, {"page": "10", "block": "b3"},
        {"page": "16", "block": "b4"}, {"page": "17", "block": "b2"}, {"page": "18", "block": "b3"}, {"page": "24", "block": "b1"},
        {"page": "11", "block": "fn1"},
    ],
    "summary": T(
        f"Brückner beschreibt das Land als zwei übereinanderliegende Terrassen und nennt dafür die wichtigsten Höhen im Text: tiefster und höchster Punkt sowie die mittlere Terrassenhöhe von Oberland und Unterland, das mittlere Elsterbett und die höchsten Punkte der West- und Ostlandschaft des Unterlandes. Umgerechnet liegt die Oberland-Terrasse im Mittel {f0(m(1360))} m hoch, die Unterland-Terrasse {f0(m(730))} m; die Höhenbereiche überschneiden sich auf {f0(overlap)}′ ({f0(m(overlap))} m).",
        f"Brückner describes the country as two terraces one above the other and gives the key altitudes in the text: lowest and highest points as well as the mean terrace altitude of the Oberland and Unterland, the mean bed of the Elster and the highest points of the west and east landscapes of the Unterland. Converted, the Oberland terrace lies at a mean of {f0e(m(1360))} m, the Unterland terrace at {f0e(m(730))} m; the altitude ranges overlap by {f0e(overlap)}′ ({f0e(m(overlap))} m)."),
    "method": T(
        "Die Zahlen stammen aus dem Fließtext auf S. 4–5 (Terrassenmittel, höchste und tiefste Punkte), S. 10 (Elsterbett und die Tabelle der höchsten Punkte der Uferlandschaften) und S. 16–18, 24 (Vergleichsangaben). Alle Höhen sind preußische Dezimalfuß (nicht Pariser Fuß), bezogen auf den Pegel bei Swinemünde (S. 11 Anm.); Umrechnung 1 Dezimalfuß = 0,3766242 m (siehe Umrechnungen). Die Angabe »Mitte« (Diagramm 1) ist Brückners Terrassenmittel, nicht aus den Ortslisten berechnet. Abgeleitet sind nur die Meterwerte und einzelne Differenzen im Text.",
        "The figures come from the running text on pp. 4–5 (terrace means, highest and lowest points), p. 10 (Elster bed and the table of the highest points of the bank landscapes) and pp. 16–18, 24 (comparison statements). All heights are Prussian decimal feet (not Paris feet) relative to the Swinemünde gauge (p. 11 note); conversion 1 decimal foot = 0.3766242 m (see conversions). The “mean” in chart 1 is Brückner's terrace mean, not computed from the place lists. Only the metre values and some differences in the text are derived."),
    "findings": [
        T(f"Das Oberland reicht von 800′ ({f0(m(800))} m, an der Leube) bis 1925′ ({f0(m(1925))} m, Fichteberg), also über {f0(rangeO)}′ ({f0(m(rangeO))} m); das Unterland von 459′ ({f0(m(459))} m, Austritt der Elster) bis 989′ ({f0(m(989))} m, Scheidberg), über {f0(rangeU)}′ ({f0(m(rangeU))} m). Das Oberland hat also mehr als das Doppelte an Höhenunterschied.",
          f"The Oberland ranges from 800′ ({f0e(m(800))} m, at the Leube) to 1925′ ({f0e(m(1925))} m, Fichteberg), i.e. over {f0e(rangeO)}′ ({f0e(m(rangeO))} m); the Unterland from 459′ ({f0e(m(459))} m, where the Elster leaves the country) to 989′ ({f0e(m(989))} m, Scheidberg), over {f0e(rangeU)}′ ({f0e(m(rangeU))} m). The Oberland thus has more than twice the relief."),
        T(f"Die mittleren Terrassenhöhen (1360′ und 730′) liegen {f0(1360 - 730)}′ ({f0(m(1360 - 730))} m) auseinander. Die beiden Höhenbereiche überschneiden sich: Das tiefste Niveau des Oberlandes (800′) liegt {f0(overlap)}′ unter dem Scheidberg, dem höchsten Punkt des Unterlandes.",
          f"The mean terrace altitudes (1360′ and 730′) are {f0e(1360 - 730)}′ ({f0e(m(1360 - 730))} m) apart. The two altitude ranges overlap: the lowest level of the Oberland (800′) lies {f0e(overlap)}′ below the Scheidberg, the highest point of the Unterland."),
        T(f"Das mittlere Bett der Elster im Unterland liegt bei 500′ ({f0(m(500))} m) und nach Brückner 394′ unter der mittleren Höhe der Uferlandschaften, die damit bei {bank_mean}′ ({f0(m(bank_mean))} m) liegt; das Tal ist im Mittel also rund {f0(m(valley_depth))} m eingeschnitten.",
          f"The mean bed of the Elster in the Unterland lies at 500′ ({f0e(m(500))} m) and, according to Brückner, 394′ below the mean altitude of the bank landscapes, which is thus {bank_mean}′ ({f0e(m(bank_mean))} m); the valley is therefore incised by about {f0e(m(valley_depth))} m on average."),
        T(f"Brückner schließt aus den sechs höchsten Punkten der Uferlandschaften, jede senke sich von Süden nach Norden (S. 10). Die Westlandschaft tut das (989′, 975′, 800′), die Ostlandschaft nicht: Mitte {f0(E['Mitte'])}′ liegt unter dem Norden {f0(E['Norden'])}′ (Süden {f0(E['Süden'])}′). Die Westlandschaft ist im Süden und in der Mitte höher als die Ostlandschaft (+{f0(W['Süden'] - E['Süden'])}′ bzw. +{f0(W['Mitte'] - E['Mitte'])}′), im Norden aber {f0(E['Norden'] - W['Norden'])}′ niedriger.",
          f"From the six highest points of the bank landscapes Brückner concludes that each falls from south to north (p. 10). The west landscape does (989′, 975′, 800′), the east landscape does not: the middle {f0e(E['Mitte'])}′ lies below the north {f0e(E['Norden'])}′ (south {f0e(E['Süden'])}′). The west landscape is higher than the east in the south and middle (+{f0e(W['Süden'] - E['Süden'])}′ and +{f0e(W['Mitte'] - E['Mitte'])}′) but {f0e(E['Norden'] - W['Norden'])}′ lower in the north."),
        T(f"Brückners Relativangaben passen zu seinen Höhenlisten: Eliasbrunn liegt »nur 213′ tiefer« als der höchste Berg des Frankenwaldes (1925 − 213 = {rel_elias}′ = »Nordhöhe von Eliasbrunn«, S. 24), der Diebsweg »nur 230′ tiefer« als der Kulm (1913 − 230 = {rel_diebs}′; Diebsweg 1685′, S. 16).",
          f"Brückner's relative statements agree with his altitude lists: Eliasbrunn lies “only 213′ lower” than the highest mountain of the Frankenwald (1925 − 213 = {rel_elias}′ = “Nordhöhe von Eliasbrunn”, p. 24), the Diebsweg “only 230′ lower” than the Kulm (1913 − 230 = {rel_diebs}′; Diebsweg 1685′, p. 16)."),
    ],
    "caveats": [
        T("Das Wort »Fuß« steht bei Brückner für den preußischen Dezimalfuß (S. 11 Anm.): 1 Fuß = 0,3766 m, nicht der Pariser Fuß (0,3248 m). Wer die Zahlen mit dem Pariser Fuß umrechnet, unterschätzt alle Höhen um rund 14 %.",
          "Brückner's “Fuß” means the Prussian decimal foot (p. 11 note): 1 foot = 0.3766 m, not the Paris foot (0.3248 m). Converting with the Paris foot underestimates all altitudes by about 14 %."),
        T("»Mittel der Terrasse« und »mittlere Höhe der Uferlandschaften« sind Brückners Schätzungen ohne Angabe der Berechnung; sie sind mit den Mitteln der Ortslisten (siehe »Höhenlage der Wohnorte«) nur lose vergleichbar.",
          "“Mean of the terrace” and “mean altitude of the bank landscapes” are Brückner's estimates without a stated calculation; they are only loosely comparable with the means of the place lists (see “Altitude of the inhabited places”)."),
        T("Die sechs Punkte auf S. 10 sind »die Lage ihrer höchsten Punkte« im Norden, in der Mitte und im Süden; welche Teile der Landschaft Brückner mit Norden, Mitte und Süden meint, sagt er nicht. Der Schluss auf eine Senkung ist daher nur an diesen sechs Werten geprüft.",
          "The six points on p. 10 are “the position of their highest points” in the north, middle and south; Brückner does not say which parts of the landscape he means by north, middle and south. The conclusion of a descent is therefore tested on these six values only."),
    ],
    "conversions": conversions_height(),
    "datasets": [
        {"name": "levels", "title": T("Höhenmarken im Text", "Altitude markers in the text"),
         "columns": [
             {"name": "landesteil", "label": LB, "type": "string", "unit": None},
             {"name": "merkmal", "label": T("Merkmal", "Feature"), "type": "string", "unit": None},
             {"name": "ort", "label": T("Ort / Gebiet", "Place / area"), "type": "string", "unit": None},
             {"name": "hoehe_fuss", "label": T("Höhe", "Altitude"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "hoehe_m", "label": T("Höhe", "Altitude"), "type": "number", "unit": "m", "derived": True},
             {"name": "beschriftung", "label": T("Beschriftung", "Label"), "type": "string", "unit": None, "derived": True},
             {"name": "label_links", "label": T("Beschriftung links (1 = ja)", "Label on the left (1 = yes)"), "type": "integer", "unit": None, "derived": True},
             {"name": "seite", "label": T("Seite", "Page"), "type": "string", "unit": None},
         ],
         "rows": level_rows,
         "source_refs": [{"page": "4", "block": "b2"}, {"page": "4", "block": "b3"}, {"page": "5", "block": "b2"}, {"page": "10", "block": "b1"}]},
        {"name": "landscapes", "title": T("Höchste Punkte der West- und Ostlandschaft des Unterlandes", "Highest points of the west and east landscape of the Unterland"),
         "columns": [
             {"name": "landschaft", "label": T("Landschaft", "Landscape"), "type": "string", "unit": None},
             {"name": "lage", "label": T("Lage", "Position"), "type": "string", "unit": None},
             {"name": "lage_nr", "label": T("Reihenfolge Süden → Norden", "Order south → north"), "type": "integer", "unit": None, "derived": True},
             {"name": "punkt", "label": T("Punkt", "Point"), "type": "string", "unit": None},
             {"name": "hoehe_fuss", "label": T("Höhe", "Altitude"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "hoehe_m", "label": T("Höhe", "Altitude"), "type": "number", "unit": "m", "derived": True},
         ],
         "rows": land_rows, "source_refs": [{"page": "10", "block": "b2", "rows": "r2-r4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "levels",
         "title": T("Zwei Terrassen: tiefste, mittlere und höchste Höhen", "Two terraces: lowest, mean and highest altitudes"),
         "caption": T("Höhen aus Brückners Text in Metern (Dezimalfuß × 0,3766). Der Strich verbindet den tiefsten mit dem höchsten Punkt des Landesteils; die Rauten sind die mittleren Terrassenhöhen. Beide Spannen überschneiden sich zwischen 301 und 372 m.",
                      "Altitudes from Brückner's text in metres (decimal foot × 0.3766). The line connects the lowest and highest point of each part; the diamonds are the mean terrace altitudes. Both ranges overlap between 301 and 372 m."),
         "vegalite": {
             "height": 380,
             "layer": [
                 {"transform": [{"aggregate": [{"op": "min", "field": "hoehe_m", "as": "lo"}, {"op": "max", "field": "hoehe_m", "as": "hi"}], "groupby": ["landesteil"]}],
                  "mark": {"type": "rule", "strokeWidth": 3},
                  "encoding": {
                      "x": {"field": "landesteil", "type": "nominal", "sort": ["Oberland", "Unterland"], "title": None, "axis": {"labelAngle": 0, "labelFontSize": 13}},
                      "y": {"field": "lo", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"domain": [100, 780]}},
                      "y2": {"field": "hi"}}},
                 {"mark": {"type": "point", "filled": True, "size": 110},
                  "encoding": {
                      "x": {"field": "landesteil", "type": "nominal", "sort": ["Oberland", "Unterland"]},
                      "y": {"field": "hoehe_m", "type": "quantitative", "scale": {"domain": [100, 780]}},
                      "color": {**COL, "legend": None},
                      "shape": {"field": "merkmal", "type": "nominal", "title": T("Merkmal", "Feature"), "legend": None,
                                "scale": {"domain": ["höchster Punkt", "Mittel der Terrasse", "Mittel des Elsterbettes", "tiefster Punkt"],
                                          "range": ["triangle-up", "diamond", "square", "triangle-down"]}},
                      "tooltip": [{"field": "landesteil", "title": LB},
                                  {"field": "merkmal", "title": T("Merkmal", "Feature")},
                                  {"field": "ort", "title": T("Ort / Gebiet", "Place / area")},
                                  {"field": "hoehe_fuss", "title": T("Dezimalfuß", "Decimal feet")},
                                  {"field": "hoehe_m", "title": T("Meter", "Metres")},
                                  {"field": "seite", "title": T("Seite", "Page")}]}},
                 {"transform": [{"filter": "datum.label_links == 0"}],
                  "mark": {"type": "text", "align": "left", "dx": 12, "baseline": "middle", "fontSize": 11},
                  "encoding": {
                      "x": {"field": "landesteil", "type": "nominal", "sort": ["Oberland", "Unterland"]},
                      "y": {"field": "hoehe_m", "type": "quantitative", "scale": {"domain": [100, 780]}},
                      "text": {"field": "beschriftung", "type": "nominal"}}},
                 {"transform": [{"filter": "datum.label_links == 1"}],
                  "mark": {"type": "text", "align": "right", "dx": -12, "baseline": "middle", "fontSize": 11},
                  "encoding": {
                      "x": {"field": "landesteil", "type": "nominal", "sort": ["Oberland", "Unterland"]},
                      "y": {"field": "hoehe_m", "type": "quantitative", "scale": {"domain": [100, 780]}},
                      "text": {"field": "beschriftung", "type": "nominal"}}},
             ]}},
        {"id": "c2", "dataset": "landscapes",
         "title": T("Fallen beide Uferlandschaften des Unterlandes nach Norden?", "Do both bank landscapes of the Unterland fall towards the north?"),
         "caption": T("Höchste Punkte der West- und der Ostlandschaft der Elster im Süden, in der Mitte und im Norden (m). Die Westlandschaft sinkt gleichmäßig von Süden nach Norden, die Ostlandschaft steigt im Norden wieder an.",
                      "Highest points of the west and east landscape of the Elster in the south, middle and north (m). The west landscape falls steadily from south to north, the east landscape rises again in the north."),
         "vegalite": {
             "height": 260,
             "layer": [
                 {"mark": {"type": "line", "point": {"filled": True, "size": 90}},
                  "encoding": {
                      "x": {"field": "lage", "type": "ordinal", "sort": {"field": "lage_nr", "op": "min"}, "title": T("Lage in der Landschaft (Süden → Norden)", "Position in the landscape (south → north)"), "axis": {"labelAngle": 0}},
                      "y": {"field": "hoehe_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"domain": [250, 390]}},
                      "color": {"datum": "Unterland", "type": "nominal", "scale": {"domain": ["Oberland", "Unterland"]}, "legend": None},
                      "strokeDash": {"field": "landschaft", "type": "nominal", "title": T("Landschaft", "Landscape"),
                                     "scale": {"domain": ["Westlandschaft", "Ostlandschaft"], "range": [[1, 0], [5, 4]]}},
                      "tooltip": [{"field": "landschaft", "title": T("Landschaft", "Landscape")},
                                  {"field": "lage", "title": T("Lage", "Position")},
                                  {"field": "punkt", "title": T("Punkt", "Point")},
                                  {"field": "hoehe_fuss", "title": T("Dezimalfuß", "Decimal feet")},
                                  {"field": "hoehe_m", "title": T("Meter", "Metres")}]}},
             ]}},
    ],
    "keywords": T(["Höhenstufen", "Terrasse", "Oberland", "Unterland", "Fichteberg", "Scheidberg", "Elster", "Elsterbett", "Westlandschaft", "Ostlandschaft", "Plastik", "Dezimalfuß"],
                  ["altitude belts", "terrace", "Oberland", "Unterland", "Fichteberg", "Scheidberg", "Elster", "relief", "decimal foot"]),
    "related": ["relief-wohnorte-hoehenlage", "relief-erhebungen-hoechste-punkte", "relief-hoehe-und-lage-neigung"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
