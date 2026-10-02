"""A11-03: Staatschausseen 1868 - Länge je Landestheil und Kosten (p. 275)."""
from common import *

g = grid("275", "b4")
RUTHE_PER_MILE = {"s": 1640.79, "r": 1970.25}      # footnote fn1 on p. 275
MILE_KM = 0.9894 * 7.5                               # 1 geogr. Meile = 0.9894 x 7500 m (Brückner p. 832)
import re
def parse(r):
    t = " ".join(r)
    ruthen = int(re.search(r"(\d{5})", t).group(1))
    miles = num(re.search(r"=\s*(\d+,\d)", t).group(1))
    return ruthen, miles
pr = [parse(r) for r in g[:3]]
assert [p[0] for p in pr] == [16938, 26202, 19188] and [p[1] for p in pr] == [10.3, 13.3, 9.7], pr
parts = [
    ("Gera", "Gera", pr[0][0], "s", "sächsische achtellige Ruthen", "Saxon eight-ell rods", pr[0][1]),
    ("Schleiz", "Schleiz", pr[1][0], "r", "rheinische sechsellige Ruthen", "Rhenish six-ell rods", pr[1][1]),
    ("Ebersdorf", "Ebersdorf", pr[2][0], "r", "rheinische sechsellige Ruthen", "Rhenish six-ell rods", pr[2][1]),
]
print(g)
rows = []
for nde, nen, ruthen, k, tde, ten, miles_printed in parts:
    miles = ruthen / RUTHE_PER_MILE[k]
    rows.append([nde, nen, ruthen, tde, ten, miles_printed, round(miles, 2), round(miles * MILE_KM, 1)])
tot_miles = sum(r[6] for r in rows)
tot_km = sum(r[7] for r in rows)
print(rows, tot_miles, tot_km)

NET, UPKEEP = 15200, 26835
deficit = UPKEEP - NET
cost_rows = [
    ["Reinertrag Chausseegelder", "Net toll revenue", "a", "Einnahme", "Revenue", NET],
    ["Unterhaltungsaufwand", "Maintenance cost", "b", "Ausgabe", "Expenditure", UPKEEP],
]
per_km = UPKEEP / tot_km
cover = 100 * NET / UPKEEP


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "staat-chausseen-laenge-kosten-1868",
    "title": bi("Staatschausseen 1868: Länge und Unterhaltungskosten", "State highways in 1868: length and maintenance cost"),
    "category": "trade-transport",
    "section": "t1-4-3",
    "sources": [{"page": "275", "block": "b4", "rows": "r1-g4"}, {"page": "275", "block": "b5"}, {"page": "275", "fn": "fn1", "block": "fn1"}, {"page": "832", "block": "b12"}],
    "summary": bi(
        f"Alle Chausseen des Fürstentums wurden 1868 vom Staat unterhalten: zusammen {D(tot_km,0)} km in drei Landestheilen. Den Unterhaltungskosten von {D(UPKEEP)} Thalern standen nur {D(NET)} Thaler Reinertrag aus den Chausseegeldern gegenüber.",
        f"In 1868 all highways of the principality were maintained by the state: {E(tot_km,0)} km in total across three regions. Maintenance cost {E(UPKEEP)} Thaler, against a net toll revenue of only {E(NET)} Thaler.",
    ),
    "method": bi(
        f"Die Längen stehen in zwei verschiedenen Ruthenmaßen (sächsische achtellige Ruthen für Gera, rheinische sechsellige für Schleiz und Ebersdorf). Brückner rechnet sie in geographische Meilen um (10,3 / 13,3 / 9,7). Hier wurden die Ruthen mit Brückners Fußnote (1640,79 sächsische bzw. 1970,25 rheinische Ruthen = 1 geographische Meile) selbst umgerechnet und die Meilen mit 1 geographische Meile = 0,9894 × 7500 m = {D(MILE_KM*1000,0)} m (S. 832) in Kilometer. Kosten und Ertrag stehen im Fließtext (S. 275, b5); die Differenz ist abgeleitet. Alle Beträge in Thalern (1 Thaler = 30 Silbergroschen).",
        f"The lengths are given in two different rod units (Saxon eight-ell rods for Gera, Rhenish six-ell rods for Schleiz and Ebersdorf). Brückner converts them into geographical miles (10.3 / 13.3 / 9.7). Here the rods were converted again using his footnote (1,640.79 Saxon or 1,970.25 Rhenish rods = 1 geographical mile) and the miles into kilometres with 1 geographical mile = 0.9894 × 7,500 m = {E(MILE_KM*1000,0)} m (p. 832). Cost and revenue are in the running text (p. 275, b5); the difference is derived. All amounts in Thaler (1 Thaler = 30 Silbergroschen).",
    ),
    "findings": [
        bi(f"Die drei Landestheile besitzen {D(rows[0][6],1)} (Gera), {D(rows[1][6],1)} (Schleiz) und {D(rows[2][6],1)} (Ebersdorf) geographische Meilen Chaussee, zusammen {D(tot_miles,1)} Meilen oder rund {D(tot_km,0)} km; der Landestheil Schleiz hat {D(100*rows[1][6]/tot_miles,0)} % davon.",
           f"The three regions have {E(rows[0][6],1)} (Gera), {E(rows[1][6],1)} (Schleiz) and {E(rows[2][6],1)} (Ebersdorf) geographical miles of highway, together {E(tot_miles,1)} miles or about {E(tot_km,0)} km; the Schleiz region holds {E(100*rows[1][6]/tot_miles,0)} % of it."),
        bi(f"Der Reinertrag der Chausseegelder deckt nur {D(cover,1)} % des Unterhaltungsaufwands; es bleiben {D(deficit)} Thaler jährlich zulasten der Staatskasse.",
           f"The net toll revenue covers only {E(cover,1)} % of the maintenance cost; {E(deficit)} Thaler a year remain a charge on the state treasury."),
        bi(f"Der Unterhaltungsaufwand beträgt rechnerisch rund {D(per_km,0)} Thaler je Kilometer und Jahr.",
           f"Maintenance works out at roughly {E(per_km,0)} Thaler per kilometre and year."),
    ],
    "caveats": [
        bi("Brückners Meilenwerte (10,3; 13,3; 9,7) und die neu berechneten (10,32; 13,30; 9,74) weichen nur durch Rundung voneinander ab. Die Kilometerwerte beruhen auf der Umrechnung der geographischen Meile (7,42 km) und sind keine Messwerte.",
           "Brückner's mile values (10.3; 13.3; 9.7) and the recomputed ones (10.32; 13.30; 9.74) differ only by rounding. The kilometre values rest on the conversion of the geographical mile (7.42 km) and are not measurements."),
        bi("Nicht enthalten sind die Strecken Frössen–Blintendorf–Gefell und Gefell–Reuth, die Preußen bzw. Sachsen vertragsmäßig unterhalten, sowie die Gemeindewege (Längen »fehlen noch«). Die Obstbaumnutzung an den Chausseen (600–2000 Thaler im Landestheil Gera) ist im Reinertrag nicht erkennbar mitgerechnet.",
           "Not included are the stretches Frössen–Blintendorf–Gefell and Gefell–Reuth, which Prussia and Saxony maintain by treaty, nor the village roads (lengths “not yet available”). It is unclear whether the fruit-tree yield along the highways (600–2,000 Thaler in the Gera region) is part of the net revenue."),
    ],
    "conversions": [
        {"from": "sächsische (achtellige) Ruthe", "to": "geographische Meile", "factor_or_formula": "Meilen = Ruthen / 1640,79", "reference": "Brückner S. 275, Fußnote"},
        {"from": "rheinische (sechsellige) Ruthe", "to": "geographische Meile", "factor_or_formula": "Meilen = Ruthen / 1970,25", "reference": "Brückner S. 275, Fußnote"},
        {"from": "geographische Meile", "to": "km", "factor_or_formula": "1 Meile = 0,9894 × 7,5 km = 7,4205 km", "reference": "Brückner S. 832 (VII. Entfernungsmaße)"},
    ],
    "datasets": [
        {"name": "length", "title": bi("Chausseelänge nach Landestheilen", "Highway length by region"),
         "columns": [
             col("region_de", "Landestheil", "Region", "string", note="Landestheil"), col("region_en", "Landestheil (englisch)", "Region (English)", "string"),
             col("ruthen", "Länge", "Length", "integer", "Ruthen"),
             col("rod_de", "Ruthenart", "Rod type", "string"), col("rod_en", "Ruthenart (englisch)", "Rod type (English)", "string"),
             col("miles_printed", "Länge (von Brückner umgerechnet)", "Length (converted by Brückner)", "number", "geogr. Meilen"),
             col("miles_calc", "Länge (neu berechnet)", "Length (recomputed)", "number", "geogr. Meilen", derived=True),
             col("km", "Länge", "Length", "number", "km", derived=True),
         ],
         "rows": rows, "source_refs": [{"page": "275", "block": "b4", "rows": "r1-g4"}]},
        {"name": "costs", "title": bi("Chausseeunterhaltung: Ertrag und Aufwand", "Highway maintenance: revenue and cost"),
         "columns": [
             col("item_de", "Posten", "Item", "string"), col("item_en", "Posten (englisch)", "Item (English)", "string"),
             col("item_key", "Kürzel", "Key", "string"),
             col("kind_de", "Art", "Kind", "string"), col("kind_en", "Art (englisch)", "Kind (English)", "string"),
             col("thaler", "Betrag", "Amount", "integer", "Thaler"),
         ],
         "rows": cost_rows, "source_refs": [{"page": "275", "block": "b5"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "length",
         "title": bi("Länge der Staatschausseen nach Landestheilen", "Length of state highways by region"),
         "caption": bi("Kilometer (aus Ruthen umgerechnet, siehe Methode). Stand 1868.", "Kilometres (converted from rods, see method). Situation in 1868."),
         "vegalite": {
             "height": 150,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("region"), "type": "nominal", "sort": "-x", "title": None},
                 "x": {"field": "km", "type": "quantitative", "title": "km"},
                 "tooltip": [ttf("region", "Landestheil", "Region"), {"field": "ruthen", "title": bi("Ruthen", "Rods"), "format": ","}, {"field": "miles_printed", "title": bi("Meilen (Brückner)", "Miles (Brückner)")}, {"field": "km", "title": "km", "format": ".1f"}]}}},
        {"id": "c2", "dataset": "costs",
         "title": bi("Chausseegelder und Unterhaltungsaufwand", "Toll revenue and maintenance cost"),
         "caption": bi("Thaler jährlich. Der Reinertrag der Chausseegelder deckt etwas mehr als die Hälfte des Unterhaltungsaufwands (Differenz 11.635 Thaler).", "Thaler per year. The net toll revenue covers a little more than half of the maintenance cost (difference 11,635 Thaler)."),
         "vegalite": {
             "height": 130,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("item"), "type": "nominal", "sort": {"field": "item_key", "op": "min"}, "title": None, "axis": {"labelLimit": 280}},
                 "x": {"field": "thaler", "type": "quantitative", "title": "Thaler", "axis": {"format": ",d"}},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "item_key", "op": "min"}},
                 "tooltip": [ttf("item", "Posten", "Item"), {"field": "thaler", "title": "Thaler", "format": ","}]}}},
    ],
    "keywords": {"de": ["Chaussee", "Straßen", "Straßenbau", "Chausseegelder", "Unterhaltung", "Staatsstraßen", "Ruthe", "Meile"],
                 "en": ["highway", "roads", "road maintenance", "tolls", "state roads", "rod", "geographical mile"]},
    "transcription_issues": [
        {"page": "275", "block": "b4", "cell": "r2c5", "transcribed": "rhein. sechstellige Ruthen", "facsimile": "rhein. sechsellige Ruthen", "checked_facsimile": True, "note": "Wortlaut (sechsellig = sechs Ellen), keine Zahl betroffen."},
    ],
}
# 'fn' key is not part of the ref schema: drop it
for r in ana["sources"]:
    r.pop("fn", None)
write(ana)
