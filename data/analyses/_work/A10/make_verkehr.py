"""A10: Eisenbahnen, Geldinstitute und Handelsrecht - Zeitleiste (pp. 258, 261, 262)."""
import sys
from datetime import date
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

EB, GI, RV = "Eisenbahn", "Geldinstitut", "Recht und Verwaltung"
KIND_EN = {EB: "Railway", GI: "Financial institution", RV: "Law and administration"}
# name_de, name_en, kind, place, start, end, precision, source, note_de, note_en
E = [
    ("Eisenbahn Weißenfels–Gera", "Railway Weißenfels–Gera", EB, "Gera", "1855-04-02", "1859-03-19", "Tag", "S. 262 b4",
     "Thüringer Zweigbahn; Vertrag vom 2. April 1855, am 19. März 1859 eröffnet.", "Thuringian branch line; treaty of 2 April 1855, opened on 19 March 1859."),
    ("Eisenbahn Gößnitz–Gera", "Railway Gößnitz–Gera", EB, "Gera", "1863-07-30", "1865-12-27", "Tag", "S. 262 b4",
     "Vertrag vom 30. Juli 1863, am 27. Dezember 1865 eröffnet; führt über Ronneburg an die sächsisch-bayerische Staatseisenbahn.", "Treaty of 30 July 1863, opened on 27 December 1865; runs via Ronneburg to the Saxon-Bavarian state railway."),
    ("Eisenbahn Gera–Eichicht (im Bau)", "Railway Gera–Eichicht (under construction)", EB, "Gera", "1867-12-04", None, "Tag", "S. 262 b4",
     "Vertrag vom 4. Dezember 1867, Zinsgarantie der fünf beteiligten Staaten; Bau bereits begonnen.", "Treaty of 4 December 1867, interest guarantee by the five states involved; construction already begun."),
    ("Sparkasse Schleiz", "Savings bank Schleiz", GI, "Schleiz", "1842", None, "Jahr", "S. 261 b4", "Seit 1842.", "Since 1842."),
    ("Sparkasse Gera", "Savings bank Gera", GI, "Gera", "1843", None, "Jahr", "S. 261 b4", "Seit 1843.", "Since 1843."),
    ("Sparkassenfiliale Hohenleuben", "Savings bank branch Hohenleuben", GI, "Hohenleuben", "1843", None, "Jahr", "S. 261 b4", "Filiale der Sparkasse Schleiz, seit 1843.", "Branch of the Schleiz savings bank, since 1843."),
    ("Sparkasse Lobenstein", "Savings bank Lobenstein", GI, "Lobenstein", "1853", None, "Jahr", "S. 261 b4", "Seit 1853.", "Since 1853."),
    ("Geraer Bank", "Bank of Gera (Geraer Bank)", GI, "Gera", "1855", None, "Jahr", "S. 261 b4", "1855 errichtet; Grundkapital 4 Millionen Thaler.", "Founded 1855; share capital 4 million thalers."),
    ("Sparkassenfiliale Hirschberg", "Savings bank branch Hirschberg", GI, "Hirschberg", "1866", None, "Jahr", "S. 261 b4", "Filiale der Sparkasse Lobenstein, seit 1866.", "Branch of the Lobenstein savings bank, since 1866."),
    ("Deutsches Handelsgesetzbuch eingeführt", "German commercial code introduced", RV, "Fürstenthum", "1863-02-23", None, "Tag", "S. 258 b3", "Durch Gesetz vom 23. Februar 1863.", "By law of 23 February 1863."),
    ("Hauptsteueramt und Packhof Gera", "Main tax office and customs warehouse, Gera", RV, "Gera", "1867", None, "Jahr", "S. 261 b4",
     "1867 das reußische Steueramt in ein Hauptsteueramt des thüringischen Zollvereins umgewandelt; Packhof mit unbedingten Niederlagerechten eröffnet.", "In 1867 the Reuss tax office was converted into a main tax office of the Thuringian Zollverein; a customs warehouse with unconditional storage rights was opened."),
]
rows = []
for nd, ne, kind, place, st, en_, prec, src, nde, nen in E:
    rows.append([nd, ne, kind, place, st, en_, prec, src, nde, nen])


def d(s):
    return date.fromisoformat(s) if len(s) == 10 else None


durs = {}
for nd, ne, kind, place, st, en_, prec, src, nde, nen in E:
    if kind == EB and en_:
        days = (d(en_) - d(st)).days
        durs[nd] = (days, days / 365.25)
print(durs)
wg = durs["Eisenbahn Weißenfels–Gera"]
gg = durs["Eisenbahn Gößnitz–Gera"]
spark = sorted([(r[4], r[0]) for r in rows if r[2] == GI and "Sparkasse" in r[0]])
print(spark)

# figures on the Gera money market (p. 261 b4, p. 262 b1) -------------------------------------------
KAP, UMS, VOH, VMIT = 4_000_000, 75_367_300, 10_000_000, 100_000_000
fin = [
    ["Grundkapital der Geraer Bank", "Share capital of the Geraer Bank", "Geraer Bank", KAP, "S. 262 b1"],
    ["Gesamtumsatz der Geraer Bank 1868", "Total turnover of the Geraer Bank, 1868", "Geraer Bank", UMS, "S. 262 b1"],
    ["Gesamtverkehr Geras ohne Geldinstitute (Schätzung)", "Total traffic of Gera without financial institutions (estimate)", "Schätzung Gesamtverkehr", VOH, "S. 261 b4"],
    ["Gesamtverkehr Geras mit Geldinstituten (Schätzung)", "Total traffic of Gera with financial institutions (estimate)", "Schätzung Gesamtverkehr", VMIT, "S. 261 b4"],
]
fin.sort(key=lambda r: -r[3])
turn_x = UMS / KAP
fin_share = (VMIT - VOH) / VMIT * 100
bank_share = UMS / VMIT * 100
print(turn_x, fin_share, bank_share)

KIND_CALC = {"de": "datum.kind", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.kind]"}
KIND_LEGEND = {"de": "datum.label", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in KIND_EN.items()) + "}[datum.label]"}
KCOLOR = {"field": "kind", "type": "nominal", "scale": {"domain": [EB, GI, RV]}, "title": {"de": "Art", "en": "Type"}, "legend": {"labelExpr": KIND_LEGEND, "labelLimit": 300, "columns": 1}}
NAME_CALC = {"de": "datum.name_de", "en": "datum.name_en"}
SORT = {"field": "date_start", "op": "min", "order": "ascending"}
TT = [{"field": "name_label", "title": {"de": "Einrichtung", "en": "Item"}}, {"field": "kind_label", "title": {"de": "Art", "en": "Type"}}, {"field": "place", "title": {"de": "Ort", "en": "Place"}},
      {"field": "date_start", "title": {"de": "Datum/Beginn", "en": "Date/start"}}, {"field": "date_end", "title": {"de": "Eröffnung", "en": "Opening"}},
      {"field": "note_de", "title": {"de": "Anmerkung", "en": "Note (German)"}}]

ana = {
    "id": "verkehr-eisenbahn-geldinstitute-zeitleiste",
    "title": {"de": "Eisenbahnen, Geldinstitute und Handelsrecht: Zeitleiste 1842–1867", "en": "Railways, financial institutions and commercial law: timeline 1842–1867"},
    "category": "trade-transport",
    "section": "t1-3-7",
    "sources": [
        {"page": "258", "block": "b3"},
        {"page": "261", "block": "b4"},
        {"page": "262", "block": "b1"},
        {"page": "262", "block": "b4"},
    ],
    "summary": {
        "de": f"Brückner nennt für Handel und Verkehr eine Reihe datierter Einrichtungen: die Eisenbahnen Weißenfels–Gera (Vertrag 1855, Eröffnung 19. März 1859) und Gößnitz–Gera (Vertrag 1863, Eröffnung 27. Dezember 1865), die Sparkassen in Schleiz, Gera, Lobenstein und ihre Filialen, die 1855 errichtete Geraer Bank sowie die Einführung des Handelsgesetzbuchs 1863. Die Zeitleiste ordnet diese elf Daten; ein zweites Diagramm vergleicht die Zahlen zum Geldverkehr Geras.",
        "en": f"For trade and transport Brückner names a series of dated institutions: the railways Weißenfels–Gera (treaty 1855, opened 19 March 1859) and Gößnitz–Gera (treaty 1863, opened 27 December 1865), the savings banks at Schleiz, Gera and Lobenstein and their branches, the Geraer Bank founded in 1855 and the introduction of the commercial code in 1863. The timeline arranges these eleven dates; a second chart compares the figures on Gera's money market.",
    },
    "method": {
        "de": f"Die Daten stammen aus dem Text S. 258 (b3) und S. 261–262 (b4/b1/b4). Vollständige Tagesdaten (Vertragsabschluss, Eröffnung, Gesetz) sind als ISO-Datum übernommen, bloße Jahresangaben als Jahr (Spalte precision). Bei den Eisenbahnen reicht der Balken vom Vertragsabschluss bis zur Eröffnung; die Dauer in Tagen bzw. Jahren (1 Jahr = 365,25 Tage) ist abgeleitet. Die Gera-Zahlen (Grundkapital, Umsatz 1868, geschätzter Gesamtverkehr) stehen im Text S. 261–262; Anteile sind berechnet. Nicht datiert (und daher nicht eingetragen) sind die Gewerbebank in Gera und der Vorschussverein in Schleiz sowie die Handelskammer.",
        "en": f"The dates come from the text on p. 258 (b3) and pp. 261–262 (b4/b1/b4). Full dates (conclusion of the treaty, opening, law) are given as ISO dates, mere years as a year (column precision). For the railways the bar runs from the conclusion of the treaty to the opening; the duration in days or years (1 year = 365.25 days) is derived. The figures for Gera (share capital, turnover 1868, estimated total traffic) are in the text on pp. 261–262; shares are computed. Not dated (and therefore not plotted) are the Gewerbebank in Gera, the Vorschussverein in Schleiz and the chamber of commerce.",
    },
    "findings": [
        {"de": f"Vom Vertragsabschluss bis zur Eröffnung vergingen bei Weißenfels–Gera {de(wg[0])} Tage ({de(wg[1], 1)} Jahre), bei Gößnitz–Gera {de(gg[0])} Tage ({de(gg[1], 1)} Jahre); für Gera–Eichicht ist 1867 der Vertrag, der Bau läuft nach Brückner bereits.",
         "en": f"From the conclusion of the treaty to the opening, Weißenfels–Gera took {en(wg[0])} days ({en(wg[1], 1)} years), Gößnitz–Gera {en(gg[0])} days ({en(gg[1], 1)} years); for Gera–Eichicht the treaty dates from 1867, and according to Brückner construction has already begun."},
        {"de": "Die Sparkassen entstanden zuerst im Oberland (Schleiz 1842, mit Filiale Hohenleuben 1843) und im Unterland (Gera 1843), Lobenstein folgt 1853, die Filiale Hirschberg 1866. Die Geraer Bank (1855) wurde im selben Jahr errichtet, in dem der Vertrag für die erste Eisenbahn geschlossen wurde.",
         "en": "The savings banks arose first in the Oberland (Schleiz 1842, with a branch at Hohenleuben in 1843) and in the Unterland (Gera 1843); Lobenstein follows in 1853, the Hirschberg branch in 1866. The Geraer Bank (1855) was founded in the same year in which the treaty for the first railway was concluded."},
        {"de": f"Die Geraer Bank hatte 1868 einen Gesamtumsatz von 75.367.300 Thalern, das {de(turn_x, 1)}fache ihres Grundkapitals von 4 Millionen. Brückner schätzt den Gesamtverkehr der Stadt Gera ohne die Geldinstitute auf 10, mit ihnen auf 100 Millionen Thaler; die Geldinstitute machen also {de(fin_share)} % dieser Schätzung aus, die Geraer Bank allein ihr Umsatz {de(bank_share, 1)} %.",
         "en": f"In 1868 the Geraer Bank had a total turnover of 75,367,300 thalers, {en(turn_x, 1)} times its share capital of 4 million. Brückner estimates the total traffic of the town of Gera at 10 million thalers without the financial institutions and 100 million with them; the financial institutions thus make up {en(fin_share)} % of this estimate, the turnover of the Geraer Bank alone {en(bank_share, 1)} %."},
    ],
    "caveats": [
        {"de": "Die Zeitleiste enthält nur die von Brückner mit Jahres- oder Tagesdatum genannten Einrichtungen; weitere Einrichtungen (Gewerbebank Gera, Vorschussverein Schleiz, Handelskammer, Telegraphenlinien) nennt er ohne Datum. Weitere geplante Bahnen (Gera–Leipzig, –Weimar, –Plauen, Erfurt–Hof) sind nur als »in Aussicht« erwähnt.",
         "en": "The timeline contains only the institutions that Brückner gives with a year or full date; he mentions further institutions (Gewerbebank Gera, Vorschussverein Schleiz, chamber of commerce, telegraph lines) without a date. Further planned railways (Gera–Leipzig, –Weimar, –Plauen, Erfurt–Hof) are mentioned only as “in prospect”."},
        {"de": "»Vertrag« bezeichnet bei den Bahnen den Staatsvertrag bzw. den Vertrag mit der Eisenbahngesellschaft, nicht den Baubeginn. Der Gesamtverkehr Geras (10 bzw. 100 Millionen Thaler) ist Brückners Schätzung; Umsatz und Kapital sind Betriebsgrößen der Bank und nicht mit Handelswerten gleichzusetzen.",
         "en": "“Treaty” means, for the railways, the state treaty or the treaty with the railway company, not the start of construction. The total traffic of Gera (10 and 100 million thalers) is Brückner's estimate; turnover and capital are operating figures of the bank and not equivalent to trade values."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "ereignisse", "title": {"de": "Datierte Einrichtungen von Handel und Verkehr", "en": "Dated institutions of trade and transport"},
         "columns": [
             {"name": "name_de", "label": {"de": "Einrichtung", "en": "Item"}, "type": "string", "unit": None},
             {"name": "name_en", "label": {"de": "Einrichtung (englisch)", "en": "Item (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "kind", "label": {"de": "Art", "en": "Type"}, "type": "string", "unit": None, "derived": True},
             {"name": "place", "label": {"de": "Ort", "en": "Place"}, "type": "string", "unit": None},
             {"name": "date_start", "label": {"de": "Datum bzw. Beginn", "en": "Date or start"}, "type": "date", "unit": None},
             {"name": "date_end", "label": {"de": "Eröffnung", "en": "Opening"}, "type": "date", "unit": None},
             {"name": "precision", "label": {"de": "Genauigkeit", "en": "Precision"}, "type": "string", "unit": None, "derived": True},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
             {"name": "note_de", "label": {"de": "Anmerkung (de)", "en": "Note (German)"}, "type": "string", "unit": None},
             {"name": "note_en", "label": {"de": "Anmerkung (en)", "en": "Note (English)"}, "type": "string", "unit": None},
         ],
         "rows": rows, "source_refs": [{"page": "258", "block": "b3"}, {"page": "261", "block": "b4"}, {"page": "262", "block": "b1"}, {"page": "262", "block": "b4"}]},
        {"name": "geldverkehr", "title": {"de": "Geraer Bank und Gesamtverkehr der Stadt Gera", "en": "Geraer Bank and total traffic of the town of Gera"},
         "columns": [
             {"name": "item_de", "label": {"de": "Größe", "en": "Item"}, "type": "string", "unit": None},
             {"name": "item_en", "label": {"de": "Größe (englisch)", "en": "Item (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "group", "label": {"de": "Gruppe", "en": "Group"}, "type": "string", "unit": None, "derived": True},
             {"name": "thaler", "label": {"de": "Betrag", "en": "Amount"}, "type": "integer", "unit": "Thaler", "derived": True, "note": "Brückner nennt 4, 10 und 100 Millionen (Zahlwort) und 75.367.300 Thaler (Ziffern)"},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": fin, "source_refs": [{"page": "261", "block": "b4"}, {"page": "262", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "ereignisse",
         "title": {"de": "Eisenbahnen, Sparkassen, Bank und Handelsrecht", "en": "Railways, savings banks, bank and commercial law"},
         "caption": {"de": "Balken: Zeit zwischen Vertragsabschluss und Eröffnung einer Bahn; Punkte: Gründungs- bzw. Einführungsjahr. Die Strecke Gera–Eichicht (Vertrag 1867) war bei Erscheinen des Buches im Bau.",
                     "en": "Bars: time between the conclusion of the treaty and the opening of a railway; dots: year of foundation or introduction. The Gera–Eichicht line (treaty 1867) was under construction when the book appeared."},
         "vegalite": {
             "height": 360,
             "transform": [{"calculate": NAME_CALC, "as": "name_label"}, {"calculate": KIND_CALC, "as": "kind_label"}],
             "layer": [
                 {"transform": [{"filter": "datum.date_end != null"}],
                  "mark": {"type": "bar", "height": {"band": 0.5}},
                  "encoding": {
                      "y": {"field": "name_label", "type": "nominal", "sort": SORT, "title": None, "axis": {"labelLimit": 360}},
                      "x": {"field": "date_start", "type": "temporal", "scale": {"nice": "year", "padding": 14}, "axis": {"format": "%Y", "title": {"de": "Jahr", "en": "Year"}, "tickCount": {"interval": "year", "step": 5}}},
                      "x2": {"field": "date_end"},
                      "color": KCOLOR, "tooltip": TT}},
                 {"transform": [{"filter": "datum.date_end == null"}],
                  "mark": {"type": "point", "filled": True, "size": 90, "opacity": 1},
                  "encoding": {
                      "y": {"field": "name_label", "type": "nominal", "sort": SORT},
                      "x": {"field": "date_start", "type": "temporal", "scale": {"nice": "year", "padding": 14}},
                      "color": KCOLOR, "tooltip": TT}},
             ]}},
        {"id": "c2", "dataset": "geldverkehr",
         "title": {"de": "Geraer Bank und Gesamtverkehr Geras", "en": "Geraer Bank and total traffic of Gera"},
         "caption": {"de": "Beträge in Thalern nach Brückner (S. 261–262). Kapital und Umsatz der Geraer Bank (blau) gegen Brückners Schätzung des Gesamtverkehrs der Stadt Gera ohne bzw. mit Geldinstituten (orange).",
                     "en": "Amounts in thalers according to Brückner (pp. 261–262). Capital and turnover of the Geraer Bank (blue) against Brückner's estimate of the total traffic of the town of Gera without and with financial institutions (orange)."},
         "vegalite": {
             "height": 220,
             "transform": [{"calculate": {"de": "datum.item_de", "en": "datum.item_en"}, "as": "item_label"}, {"calculate": "datum.thaler / 1000000", "as": "mio"}],
             "layer": [
                 {"mark": "bar"},
                 {"mark": {"type": "text", "align": "left", "dx": 5}, "encoding": {"text": {"field": "mio", "type": "quantitative", "format": ".4~f"}}},
             ],
             "encoding": {
                 "y": {"field": "item_label", "type": "nominal", "sort": None, "title": None, "axis": {"labelLimit": 520}},
                 "x": {"field": "mio", "type": "quantitative", "title": {"de": "Millionen Thaler", "en": "Million thalers"}, "scale": {"domainMax": 125}},
                 "color": {"field": "group", "type": "nominal", "scale": {"domain": ["Geraer Bank", "Schätzung Gesamtverkehr"]}, "title": {"de": "Größe", "en": "Item"},
                           "legend": {"labelExpr": {"de": "datum.label", "en": "{'Geraer Bank':'Geraer Bank','Schätzung Gesamtverkehr':'Estimate of total traffic'}[datum.label]"}, "labelLimit": 300, "columns": 1}},
                 "tooltip": [{"field": "item_label", "title": {"de": "Größe", "en": "Item"}}, {"field": "thaler", "title": {"de": "Thaler", "en": "Thalers"}, "format": ","}]}}},
    ],
    "keywords": {"de": ["Eisenbahn", "Weißenfels", "Gößnitz", "Eichicht", "Sparkasse", "Geraer Bank", "Handelsgesetzbuch", "Zollverein", "Verkehr", "Gera", "Schleiz", "Lobenstein"],
                 "en": ["railway", "Weißenfels", "Gößnitz", "Eichicht", "savings bank", "Geraer Bank", "commercial code", "Zollverein", "transport", "Gera", "Schleiz", "Lobenstein"]},
    "related": ["handel-verkehr-begleitscheine-1858-1867", "handel-gewerbe-nach-landesteilen-1864"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
