"""A10: Marktorte und Jahrmaerkte nach Landesteilen (p. 262)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

KR, VI, RW = "Kram- und Jahrmärkte", "Viehmärkte", "Ross-, Woll- und Kornmärkte"
KIND_EN = {KR: "Fairs and general markets", VI: "Cattle markets", RW: "Horse, wool and grain markets"}
GE, SC, LO = "Gera", "Schleiz", "Lobenstein-Ebersdorf"
# place, district, [(printed market type, count, kind)], item, note
M = [
    ("Gera", GE, [("vier Jahrmärkte", 4, KR), ("zwei Rossmärkte", 2, RW), ("zwei Viehmärkte", 2, VI), ("ein Wollmarkt", 1, RW)], "i1", None),
    ("Langenberg", GE, [("zwei Krammärkte", 2, KR), ("ein Ross-, Vieh- und Kornmarkt", 1, RW)], "i1", None),
    ("Grossaga", GE, [("ein Krammarkt", 1, KR)], "i1", None),
    ("Schleiz", SC, [("sieben Kram- und Viehmärkte", 7, KR), ("drei Viehmärkte", 3, VI), ("ein Wollmarkt", 1, RW)], "i2", None),
    ("Hohenleuben", SC, [("vier Kram- und Viehmärkte", 4, KR)], "i2", None),
    ("Weissendorf", SC, [("zwei Kram- und Viehmärkte", 2, KR)], "i2", None),
    ("Langenwolschendorf", SC, [("zwei Kram-, Vieh- und Leinwandmärkte", 2, KR)], "i2", None),
    ("Rödersdorf", SC, [("ein Krammarkt", 1, KR)], "i2", None),
    ("Saalburg", SC, [("vier Kram- und Viehmärkte", 4, KR)], "i2", None),
    ("Tanna", SC, [("sieben Kram- und Viehmärkte", 7, KR)], "i2", None),
    ("Lobenstein", LO, [("sechs Kram-[märkte]", 6, KR), ("drei Viehmärkte", 3, VI), ("ein Wollmarkt", 1, RW)], "i3", None),
    ("Ebersdorf", LO, [("fünf Kram- und Viehmärkte", 5, KR), ("sieben Viehmärkte", 7, VI)], "i3", None),
    ("Hirschberg", LO, [("fünf Kram- und Viehmärkte", 5, KR), ("ein Krammarkt", 1, KR)], "i3", None),
    ("Langgrün", LO, [("ein Kram- und Viehmarkt", 1, KR)], "i3", None),
    ("Lothra", LO, [("drei Kram- und Viehmärkte", 3, KR)], "i3", None),
    ("Thimmendorf", LO, [("fünf Kram- und Viehmärkte", 5, KR)], "i3", None),
    ("Ruppersdorf", LO, [("vier Kram-[märkte]", 4, KR), ("fünf Viehmärkte", 5, VI)], "i3", None),
    ("Wurzbach", LO, [("sieben Kram- und Vieh-[märkte]", 7, KR), ("sieben Viehmärkte", 7, VI)], "i3", None),
    ("Titschendorf", LO, [("vier Kram- und Viehmärkte", 4, KR)], "i3", "angeblich zur Zeit eingestellt (Fußnote)"),
    ("Ossla", LO, [("ein Kram- und Schweinemarkt", 1, KR)], "i3", None),
    ("Pottiga", LO, [("ein Krammarkt", 1, KR)], "i3", None),
]
rows = []
for place, dist, items, it, note in M:
    for text, n, kind in items:
        rows.append([place, dist, text, kind, n, "S. 262 b3 " + it, note])
print(len(rows))
tot = sum(r[4] for r in rows)
by_d = {d: sum(r[4] for r in rows if r[1] == d) for d in (GE, SC, LO)}
places_d = {d: len({r[0] for r in rows if r[1] == d}) for d in (GE, SC, LO)}
by_p = {}
for r in rows:
    by_p[r[0]] = by_p.get(r[0], 0) + r[4]
rank = sorted(by_p.items(), key=lambda kv: -kv[1])
by_kind = {k: sum(r[4] for r in rows if r[3] == k) for k in (KR, VI, RW)}
print(tot, by_d, places_d, rank[:5], by_kind)
assert places_d == {GE: 3, SC: 7, LO: 11}
share_lo = by_d[LO] / tot * 100
avg = {d: by_d[d] / places_d[d] for d in by_d}
vieh_lo = sum(r[4] for r in rows if r[3] == VI and r[1] == LO)
vieh_share_lo = vieh_lo / by_kind[VI] * 100
n_ge_ge10 = [p for p, n in by_p.items() if n >= 10]
print(avg, vieh_lo, vieh_share_lo, n_ge_ge10)

KIND_CALC = {"de": "datum.kind", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.kind]"}
KIND_LEGEND = {"de": "datum.label", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.label]"}
KCOLOR = {"field": "kind", "type": "nominal", "scale": {"domain": [KR, VI, RW]}, "title": {"de": "Marktart", "en": "Type of market"}, "legend": {"labelExpr": KIND_LEGEND, "columns": 1, "labelLimit": 300}}
DIST = {"de": "Landesteil", "en": "District"}

ana = {
    "id": "handel-jahrmaerkte-marktorte-landesteile",
    "title": {"de": "Marktorte und Jahrmärkte der drei Landesteile", "en": "Market towns and annual fairs of the three districts"},
    "category": "trade-transport",
    "section": "t1-3-7",
    "sources": [
        {"page": "262", "block": "b2"},
        {"page": "262", "block": "b3", "rows": "i1-i3"},
        {"page": "262", "block": "fn1"},
    ],
    "summary": {
        "de": f"Brückner führt die Marktorte des Fürstenthums auf, geordnet nach Landesteilen, mit Zahl und Art ihrer Jahrmärkte: drei im Landesteil Gera, sieben in Schleiz und elf in Lobenstein-Ebersdorf. Aus den Zahlwörtern des Textes ergeben sich {tot} Märkte; Wurzbach, Ebersdorf und Schleiz haben die meisten. Die Wochenmärkte sind nicht erfasst.",
        "en": f"Brückner lists the market towns of the principality by district, with the number and kind of their annual fairs: three in the district of Gera, seven in Schleiz and eleven in Lobenstein-Ebersdorf. The number words in the text yield {tot} markets; Wurzbach, Ebersdorf and Schleiz have the most. Weekly markets are not recorded.",
    },
    "method": {
        "de": "Die Aufzählung S. 262 (b3, drei Listenpunkte) nennt je Ort Märkte in Zahlwörtern (»sieben Kram- und Viehmärkte«). Jede genannte Art wurde als eine Zeile mit der Anzahl erfasst (Spalte count, abgeleitet aus dem Zahlwort) und einer von drei Marktarten zugeordnet: Kram- und Jahrmärkte (auch kombiniert mit Vieh, Leinwand oder Schweinen), reine Viehmärkte, sowie Ross-, Woll- und Kornmärkte. Ein kombinierter Markt (»ein Ross-, Vieh- und Kornmarkt«, »ein Kram- und Viehmarkt«) zählt als ein Markt. Bei »sechs Kram-, drei Viehmärkte« (Lobenstein) und »vier Kram- und fünf Viehmärkte« (Ruppersdorf) sind sechs bzw. vier Krammärkte gelesen; in Klammern ergänzte Wortteile stehen in eckigen Klammern.",
        "en": "The list on p. 262 (b3, three list items) gives the markets of each place in number words (“sieben Kram- und Viehmärkte”). Each kind named was recorded as one row with its number (column count, derived from the number word) and assigned to one of three types: general fairs (also combined with cattle, linen or pigs), pure cattle markets, and horse, wool and grain markets. A combined market (“ein Ross-, Vieh- und Kornmarkt”, “ein Kram- und Viehmarkt”) counts as one market. In “sechs Kram-, drei Viehmärkte” (Lobenstein) and “vier Kram- und fünf Viehmärkte” (Ruppersdorf) six and four general markets are read; word parts supplied in brackets are shown in square brackets.",
    },
    "findings": [
        {"de": f"Das Unterland hat mit {places_d[GE]} Marktorten und {by_d[GE]} Märkten die wenigsten, Lobenstein-Ebersdorf mit {places_d[LO]} Marktorten und {by_d[LO]} Märkten ({de(share_lo, 1)} % aller {tot}) die meisten; das bestätigt Brückners Aussage. Schleiz liegt mit {places_d[SC]} Orten und {by_d[SC]} Märkten dazwischen.",
         "en": f"The Unterland has the fewest, with {places_d[GE]} market towns and {by_d[GE]} markets, Lobenstein-Ebersdorf the most, with {places_d[LO]} market towns and {by_d[LO]} markets ({en(share_lo, 1)} % of all {tot}); this confirms Brückner's statement. Schleiz lies in between with {places_d[SC]} places and {by_d[SC]} markets."},
        {"de": f"Die meisten Märkte haben Wurzbach ({by_p['Wurzbach']}), Ebersdorf ({by_p['Ebersdorf']}) und Schleiz ({by_p['Schleiz']}); Lobenstein ({by_p['Lobenstein']}), Gera ({by_p['Gera']}) und Ruppersdorf ({by_p['Ruppersdorf']}) folgen. Je Marktort sind es im Durchschnitt {de(avg[GE], 1)} (Gera), {de(avg[SC], 1)} (Schleiz) und {de(avg[LO], 1)} (Lobenstein-Ebersdorf).",
         "en": f"The most markets are held at Wurzbach ({by_p['Wurzbach']}), Ebersdorf ({by_p['Ebersdorf']}) and Schleiz ({by_p['Schleiz']}); Lobenstein ({by_p['Lobenstein']}), Gera ({by_p['Gera']}) and Ruppersdorf ({by_p['Ruppersdorf']}) follow. The average per market town is {en(avg[GE], 1)} (Gera), {en(avg[SC], 1)} (Schleiz) and {en(avg[LO], 1)} (Lobenstein-Ebersdorf)."},
        {"de": f"Von {by_kind[VI]} reinen Viehmärkten finden {vieh_lo} ({de(vieh_share_lo, 1)} %) im Landesteil Lobenstein-Ebersdorf statt (Ebersdorf 7, Wurzbach 7, Ruppersdorf 5, Lobenstein 3); Pferde- (Ross-) und Kornmärkte gibt es nur in Gera und Langenberg, Wollmärkte nur in den drei Landesteilshauptorten Gera, Schleiz und Lobenstein.",
         "en": f"Of {by_kind[VI]} pure cattle markets, {vieh_lo} ({en(vieh_share_lo, 1)} %) take place in the district of Lobenstein-Ebersdorf (Ebersdorf 7, Wurzbach 7, Ruppersdorf 5, Lobenstein 3); horse and grain markets exist only at Gera and Langenberg, wool markets only in the three district centers Gera, Schleiz and Lobenstein."},
    ],
    "caveats": [
        {"de": "Brückner nennt die Zahl der Märkte pro Jahr, nicht ihre Dauer oder Bedeutung; Wochenmärkte sind ausdrücklich ausgenommen. Die Typisierung in drei Arten ist eine Vereinfachung der gedruckten Bezeichnungen.",
         "en": "Brückner gives the number of markets per year, not their duration or importance; weekly markets are expressly excluded. The three-way typing is a simplification of the printed designations."},
        {"de": "Einzelne Formulierungen sind mehrdeutig (»sechs Kram-, drei Viehmärkte«, »sieben Kram- und Vieh- und sieben Viehmärkte«); die Lesart ist in der Methode beschrieben. Die Märkte in Titschendorf sind nach der Fußnote angeblich zur Zeit eingestellt, aber mitgezählt.",
         "en": "Some phrasings are ambiguous (“sechs Kram-, drei Viehmärkte”, “sieben Kram- und Vieh- und sieben Viehmärkte”); the reading is described under method. The markets at Titschendorf are, according to the footnote, reportedly suspended at present, but are included in the count."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "maerkte", "title": {"de": "Märkte nach Ort und Art", "en": "Markets by place and kind"},
         "columns": [
             {"name": "place", "label": {"de": "Marktort", "en": "Market town"}, "type": "string", "unit": None},
             {"name": "district", "label": DIST, "type": "string", "unit": None},
             {"name": "printed", "label": {"de": "Wortlaut der Angabe", "en": "Printed wording"}, "type": "string", "unit": None},
             {"name": "kind", "label": {"de": "Marktart", "en": "Type of market"}, "type": "string", "unit": None, "derived": True},
             {"name": "count", "label": {"de": "Anzahl Märkte", "en": "Number of markets"}, "type": "integer", "unit": "Märkte", "derived": True, "note": "aus dem Zahlwort"},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
             {"name": "note", "label": {"de": "Anmerkung", "en": "Note"}, "type": "string", "unit": None},
         ],
         "rows": rows, "source_refs": [{"page": "262", "block": "b3", "rows": "i1-i3"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "maerkte",
         "title": {"de": "Märkte je Marktort", "en": "Markets per market town"},
         "caption": {"de": "Anzahl der Jahrmärkte, Viehmärkte und sonstigen Märkte je Ort. Schleiz, Wurzbach und Ebersdorf stehen an der Spitze.",
                     "en": "Number of annual fairs, cattle markets and other markets per town. Schleiz, Wurzbach and Ebersdorf are at the top."},
         "vegalite": {
             "height": 480,
             "transform": [{"calculate": KIND_CALC, "as": "kind_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "place", "type": "nominal", "sort": {"field": "count", "op": "sum", "order": "descending"}, "title": None},
                 "x": {"field": "count", "type": "quantitative", "title": {"de": "Anzahl Märkte", "en": "Number of markets"}, "axis": {"tickMinStep": 1}},
                 "color": KCOLOR,
                 "tooltip": [{"field": "place", "title": {"de": "Marktort", "en": "Market town"}}, {"field": "district", "title": DIST}, {"field": "kind_label", "title": {"de": "Marktart", "en": "Type"}},
                             {"field": "printed", "title": {"de": "Wortlaut", "en": "Printed wording"}}, {"field": "count", "title": {"de": "Anzahl", "en": "Number"}}]}}},
        {"id": "c2", "dataset": "maerkte",
         "title": {"de": "Märkte je Landesteil", "en": "Markets per district"},
         "caption": {"de": f"Summe der Märkte nach Art. Es gibt {places_d[GE]} Marktorte im Landesteil Gera, {places_d[SC]} in Schleiz und {places_d[LO]} in Lobenstein-Ebersdorf.",
                     "en": f"Sum of markets by type. There are {places_d[GE]} market towns in the district of Gera, {places_d[SC]} in Schleiz and {places_d[LO]} in Lobenstein-Ebersdorf."},
         "vegalite": {
             "height": 260,
             "transform": [{"calculate": KIND_CALC, "as": "kind_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "sort": [GE, SC, LO], "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "count", "type": "quantitative", "aggregate": "sum", "title": {"de": "Anzahl Märkte", "en": "Number of markets"}},
                 "color": KCOLOR,
                 "tooltip": [{"field": "district", "title": DIST}, {"field": "kind_label", "title": {"de": "Marktart", "en": "Type"}}, {"field": "count", "aggregate": "sum", "title": {"de": "Anzahl", "en": "Number"}}]}}},
    ],
    "keywords": {"de": ["Märkte", "Jahrmärkte", "Viehmärkte", "Wollmarkt", "Marktorte", "Wurzbach", "Ebersdorf", "Schleiz", "Gera", "Tanna", "Lobenstein"],
                 "en": ["markets", "annual fairs", "cattle markets", "wool market", "market towns", "Wurzbach", "Ebersdorf", "Schleiz", "Gera", "Tanna", "Lobenstein"]},
    "related": ["handel-gewerbe-nach-landesteilen-1864"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
