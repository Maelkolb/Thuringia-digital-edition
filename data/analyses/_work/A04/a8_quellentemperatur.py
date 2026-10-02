"""A04 / analysis 8: temperatures of springs and wells (pp. 69-70, prose values)."""
import sys
sys.path.insert(0, ".")
from common import *

R_TO_C = 1.25
T69 = block("69", "b3")["text"]
T70a = block("70", "b1")["text"]
T70b = block("70", "b2")["text"]

# (group key, order, site, kind, r_min, r_max, printed text, observer, date, block-text, check-string)
SPEC = [
    ("kraftsdorf", 1, "Queckbrunnen", "spring", 8, 8, "8°", "J. C. Seydel", "", T69, "Queckbrunnen mit 8°"),
    ("kraftsdorf", 1, "Hempelsquelle", "spring", 8, 8, "8°", "J. C. Seydel", "", T69, "Hempelsquelle mit 8°"),
    ("kraftsdorf", 1, "Martinsquelle", "spring", 9, 9, "9°", "J. C. Seydel", "", T69, "Martinsquelle mit 9°"),
    ("kraftsdorf", 1, "Scheffelsbrunnen", "spring", 8, 8, "8°", "J. C. Seydel", "", T69, "Scheffelsbrunnen mit 8°"),
    ("kraftsdorf", 1, "Prechtsquelle", "spring", 6.75, 6.75, "6 3/4°", "J. C. Seydel", "", T69, "Prechtsquelle mit 6 3/4° R."),
    ("brunnen", 2, "Hermsdorf", "well", 8, 8, "8°", "Pastor Dreyhaupt, Heukewalde", "", T69, "Hermsdorf von Pastor Dreyhaupt in Heukewalde mit 8°"),
    ("brunnen", 2, "Hohenleuben, Herrengasse (40 Fuß)", "well", 8, 8, "8°", "Dr. Schmidt, Hohenleuben", "", T69, "Herrengasse mit 8°"),
    ("brunnen", 2, "Döhlen", "well", 8, 8, "8°", "Dr. Schmidt, Hohenleuben", "", T69, "döhlener Brunnen gleichfalls mit 8° R."),
    ("roettersdorf", 3, "Röttersdorf, oberer Ziehbrunnen, 12. Mai", "well", 5.5, 5.5, "5 1/2°", "Dir. Bischoff, Lehesten", "12. Mai 1868", T70a, "Dorfziehbrunnen 5 1/2° R."),
    ("roettersdorf", 3, "Röttersdorf, oberer Ziehbrunnen, 27. Mai", "well", 6.5, 6.5, "6 1/2°", "Dir. Bischoff, Lehesten", "27. Mai 1868", T70a, "Ziehbrunnens 6 1/2° R."),
    ("roettersdorf", 3, "Röttersdorf, unterer Ziehbrunnen, 27. Mai", "well", 6, 6, "6°", "Dir. Bischoff, Lehesten", "27. Mai 1868", T70a, "abwärts liegenden 6° R."),
    ("elsaesser", 4, "Obere Quellen", "stage", 11, 12, "11° bis 12°", "Ing. Elsässer", "", T70b, "oberen Quellen auf 11° bis 12°"),
    ("elsaesser", 4, "Mittlere Quellen", "stage", 9, 10, "9° bis 10°", "Ing. Elsässer", "", T70b, "mittleren auf 9° bis 10°"),
    ("elsaesser", 4, "Untere Quellen", "stage", 7, 8, "7° bis 8°", "Ing. Elsässer", "", T70b, "unteren auf 7° bis 8° R."),
]
rows = []
for k, (grp, go, site, kind, rmin, rmax, printed, obs, date, text, chk) in enumerate(SPEC, start=1):
    assert chk in text, chk
    rows.append([k, grp, go, site, kind, printed, rmin, rmax, round(rmin * R_TO_C + 1e-9, 1), round(rmax * R_TO_C + 1e-9, 1), obs, date])
for r in rows:
    print(r)
spr = [r for r in rows if r[1] == "kraftsdorf"]
wells = [r for r in rows if r[1] == "brunnen"]
rott = [r for r in rows if r[1] == "roettersdorf"]
els = [r for r in rows if r[1] == "elsaesser"]
print("kraftsdorf C", min(r[8] for r in spr), max(r[9] for r in spr))
print("brunnen C", {r[8] for r in wells})
print("rott C", sorted(r[8] for r in rott))
print("elsaesser C", [(r[3], r[8], r[9]) for r in els])


def F(x, dec=1):
    return fmt(x, "de", dec), fmt(x, "en", dec)


GROUP_LABEL_CALC = {"calculate": bi(
    "{'kraftsdorf':'Kraftsdorf','brunnen':'Brunnen','roettersdorf':'Röttersdorf','elsaesser':'Elsässer'}[datum.group]",
    "{'kraftsdorf':'Kraftsdorf','brunnen':'Wells','roettersdorf':'Röttersdorf','elsaesser':'Elsässer'}[datum.group]"),
    "as": "group_label"}
SITE_EN = {"Hermsdorf": "Hermsdorf", "Hohenleuben, Herrengasse (40 Fuß)": "Hohenleuben, Herrengasse (40 ft)",
           "Röttersdorf, oberer Ziehbrunnen, 12. Mai": "Röttersdorf, upper well, 12 May",
           "Röttersdorf, oberer Ziehbrunnen, 27. Mai": "Röttersdorf, upper well, 27 May",
           "Röttersdorf, unterer Ziehbrunnen, 27. Mai": "Röttersdorf, lower well, 27 May",
           "Obere Quellen": "Upper springs", "Mittlere Quellen": "Middle springs", "Untere Quellen": "Lower springs"}
SITE_LABEL_CALC = {"calculate": bi("datum.site",
                                   "{" + ",".join('"%s":"%s"' % (k.replace('"', ''), v) for k, v in SITE_EN.items()).replace('"', "'") + "}[datum.site] || datum.site"),
                   "as": "site_label"}
KIND_CALC = {"calculate": bi("{'spring':'Quelle','well':'Brunnen','stage':'Quellen einer Höhenstufe (Spanne)'}[datum.kind]",
                             "{'spring':'Spring','well':'Well','stage':'Springs of an altitude stage (range)'}[datum.kind]"), "as": "kind_label"}

ana = {
    "id": "klima-quellentemperatur-brunnen",
    "title": bi("Temperatur von Quellen und Brunnen", "Temperature of springs and wells"),
    "category": "climate",
    "section": "t1-1-7",
    "sources": [{"page": "69", "block": "b3"}, {"page": "70", "block": "b1"}, {"page": "70", "block": "b2"}],
    "summary": bi(
        "Über die Temperatur von Quellen und Brunnen liegen laut Brückner noch keine ausreichend genauen Untersuchungen vor. Er nennt einzelne Messungen in Réaumur: fünf Quellen bei Kraftsdorf und Dessegrund (J. C. Seydel), Brunnen in Hermsdorf, Hohenleuben und Döhlen, zwei Ziehbrunnen in Röttersdorf im Mai 1868 sowie allgemeine Spannen für obere, mittlere und untere Quellen des Oberlandes (Ing. Elsässer). Umgerechnet in °C liegen die meisten Werte bei 8 bis 11 °C.",
        "According to Brückner, no sufficiently exact studies of the temperature of springs and wells yet exist. He gives individual readings in Réaumur: five springs near Kraftsdorf and Dessegrund (J. C. Seydel), wells at Hermsdorf, Hohenleuben and Döhlen, two draw-wells at Röttersdorf in May 1868, and general ranges for upper, middle and lower springs of the Oberland (engineer Elsässer). Converted to °C most values lie between 8 and 11 °C."),
    "method": bi(
        "Die Werte stehen im Fließtext (S. 69 b3, S. 70 b1 und b2) und wurden einzeln übernommen; der Datensatz nennt Fundstelle, Beobachter und, wo angegeben, Datum. Temperaturen in Réaumur wurden mit 1 °R = 1,25 °C in Grad Celsius umgerechnet; Brüche wie 6 3/4 und 5 1/2 sind im Druck als gemischte Brüche gesetzt und im Datensatz als Dezimalzahl ausgewiesen (Spalte »Wert im Druck«). Elsässers Angaben sind Spannen (z. B. 11° bis 12° R.) und werden als Balken dargestellt, Einzelmessungen als Punkte. Brückner nennt Seydels elf Quellen, aber nur fünf mit Namen; nur diese sind erfasst.",
        "The values are in the running text (p. 69 b3, p. 70 b1 and b2) and were taken one by one; the dataset gives the location, observer and, where stated, the date. Temperatures in Réaumur were converted to degrees Celsius with 1 °R = 1.25 °C; fractions such as 6 3/4 and 5 1/2 are set as mixed fractions in the print and appear as decimals in the dataset (column “Value as printed”). Elsässer's figures are ranges (e.g. 11° to 12° R.) and are drawn as bars, single readings as dots. Brückner names Seydel's eleven springs but only five by name; only these are included."),
    "findings": [
        bi(f"Die fünf Quellen bei Kraftsdorf und im Dessegrund liegen zwischen {F(min(r[8] for r in spr))[0]} und {F(max(r[9] for r in spr))[0]} °C; drei davon haben 8 °R (10 °C), die Martinsquelle 9 °R ({F(9*R_TO_C,2)[0]} °C), die Prechtsquelle mit 6 3/4 °R ({F(6.75*R_TO_C,1)[0]} °C) die niedrigste.",
           f"The five springs at Kraftsdorf and in the Dessegrund lie between {F(min(r[8] for r in spr))[1]} and {F(max(r[9] for r in spr))[1]} °C; three of them are at 8 °R (10 °C), the Martinsquelle at 9 °R ({F(9*R_TO_C,2)[1]} °C) and the Prechtsquelle, at 6 3/4 °R ({F(6.75*R_TO_C,1)[1]} °C), is the coldest."),
        bi("Die drei Brunnen in Hermsdorf, Hohenleuben und Döhlen werden einheitlich mit 8 °R (10 °C) angegeben.",
           "The three wells at Hermsdorf, Hohenleuben and Döhlen are all given as 8 °R (10 °C)."),
        bi(f"Die Ziehbrunnen in Röttersdorf (Oberland) messen im Mai 1868 nur {F(5.5*R_TO_C)[0]} bis {F(6.5*R_TO_C)[0]} °C, also {F(8*R_TO_C-6.5*R_TO_C)[0]} bis {F(8*R_TO_C-5.5*R_TO_C)[0]} Grad weniger als die Brunnen mit 10 °C. Das sind Einzelmessungen an zwei Tagen bei unterschiedlicher Luft; ein Jahresmittel lässt sich daraus nicht ableiten.",
           f"The draw-wells at Röttersdorf (Oberland) read only {F(5.5*R_TO_C)[1]} to {F(6.5*R_TO_C)[1]} °C in May 1868, {F(8*R_TO_C-6.5*R_TO_C)[1]} to {F(8*R_TO_C-5.5*R_TO_C)[1]} degrees less than the wells at 10 °C. These are single readings on two days under different air conditions; no annual mean can be derived from them."),
        bi(f"Elsässers allgemeine Spannen für das Oberland (obere Quellen 11–12 °R = {F(11*R_TO_C)[0]}–{F(12*R_TO_C)[0]} °C, mittlere 9–10 °R, untere 7–8 °R) liegen höher als die Röttersdorfer Messungen. Was »obere«, »mittlere« und »untere« Quellen bedeuten, sagt der Text nicht; Brückner merkt an, es sei unklar, ob die Zahlen auf Messungen beruhen und die Jahrestemperatur meinen.",
           f"Elsässer's general ranges for the Oberland (upper springs 11–12 °R = {F(11*R_TO_C)[1]}–{F(12*R_TO_C)[1]} °C, middle 9–10 °R, lower 7–8 °R) lie higher than the Röttersdorf readings. The text does not say what “upper”, “middle” and “lower” springs mean; Brückner remarks that it is unclear whether the figures rest on measurements and refer to the annual temperature."),
    ],
    "caveats": [
        bi("Brückner betont, dass »eine durch alle Monate des Jahres durchgeführte Beobachtung« fehlt und ein Vergleich von Wasser- und Luftwärme für die Stufen des Landes noch nicht möglich ist. Die Werte sind Einzelangaben unterschiedlicher Beobachter, Jahreszeiten und Quellarten und deshalb nicht untereinander vergleichbar; sie sind nur als Anhaltspunkte zu lesen.",
           "Brückner stresses that no observation “carried through all months of the year” exists and that a comparison of water and air temperature for the altitude stages of the country is not yet possible. The values are single statements by different observers, in different seasons and for different kinds of springs and are therefore not comparable with each other; they should be read as rough indications only."),
        bi("Die Genauigkeit der Réaumur-Angaben ist unbekannt (meist ganze Grade, einmal 6 3/4); Höhenlage und Lage der Quellen sind nicht genannt. Bei den Röttersdorfer Messungen stehen Luftwärme (im Schatten 18 1/2, in der Sonne 23 1/2 bzw. 26 1/2 °R) und Windlage im Text, sind hier aber nicht ausgewertet.",
           "The precision of the Réaumur values is unknown (mostly whole degrees, once 6 3/4); altitude and position of the springs are not given. For the Röttersdorf readings the text gives air temperature (in the shade 18 1/2, in the sun 23 1/2 and 26 1/2 °R) and wind conditions, which are not analysed here."),
    ],
    "conversions": [
        {"from": "Grad Réaumur (°R)", "to": "Grad Celsius (°C)", "factor_or_formula": "°C = °R × 1,25", "reference": "übliche Umrechnung (80 °R = 100 °C); Brückner nennt die Skala als »R.«"},
    ],
    "datasets": [
        {"name": "measurements", "title": bi("Temperaturangaben für Quellen und Brunnen", "Temperature statements for springs and wells"),
         "columns": [
             col("id", "Nr.", "No.", "integer", None, True, "laufende Nummer, editorisch"),
             col("group", "Gruppe", "Group", "string", None, True, "Beobachter bzw. Fundort, editorisch"),
             col("group_order", "Reihenfolge der Gruppe", "Group order", "integer", None, True),
             col("site", "Quelle / Brunnen", "Spring / well", "string", None, False, "Bezeichnung wie im Druck"),
             col("kind", "Art", "Kind", "string", None, True, "spring = Quelle, well = Brunnen, stage = Spanne für eine Stufe (Elsässer)"),
             col("value_printed", "Wert im Druck", "Value as printed", "string", None, False, "Réaumur"),
             col("temp_r_min", "Temperatur (Minimum)", "Temperature (minimum)", "number", "°R", True, "aus dem gedruckten Wert; Brüche als Dezimalzahl"),
             col("temp_r_max", "Temperatur (Maximum)", "Temperature (maximum)", "number", "°R", True, "gleich dem Minimum bei Einzelwerten"),
             col("temp_c_min", "Temperatur (Minimum)", "Temperature (minimum)", "number", "°C", True, "°R × 1,25"),
             col("temp_c_max", "Temperatur (Maximum)", "Temperature (maximum)", "number", "°C", True, "°R × 1,25"),
             col("observer", "Beobachter", "Observer", "string", None, False),
             col("date_text", "Datum", "Date", "string", None, False, "wo im Text angegeben"),
         ], "rows": rows,
         "source_refs": [{"page": "69", "block": "b3"}, {"page": "70", "block": "b1"}, {"page": "70", "block": "b2"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "measurements",
         "title": bi("Temperaturen von Quellen und Brunnen", "Temperatures of springs and wells"),
         "caption": bi("Punkte: Einzelmessungen; Balken: Spannen nach Elsässer (°R × 1,25 in °C). Die Kraftsdorfer Quellen und die Brunnen liegen bei 10 °C, die Röttersdorfer Ziehbrunnen im Mai 1868 darunter.",
                       "Dots: single readings; bars: ranges according to Elsässer (°R × 1.25 in °C). The Kraftsdorf springs and the wells lie at 10 °C, the Röttersdorf draw-wells in May 1868 below."),
         "vegalite": {
             "height": 380,
             "transform": [GROUP_LABEL_CALC, SITE_LABEL_CALC, KIND_CALC, {"calculate": "(datum.temp_c_min + datum.temp_c_max) / 2", "as": "temp_mid"}],
             "encoding": {
                 "y": {"field": "site_label", "type": "nominal", "title": None, "sort": {"field": "id", "op": "min"}, "axis": {"labelLimit": 400}},
                 "color": {"field": "group_label", "type": "nominal", "title": None, "sort": {"field": "group_order", "op": "min"}, "legend": {"columns": 2}},
                 "tooltip": [{"field": "site_label", "title": bi("Quelle / Brunnen", "Spring / well")},
                             {"field": "kind_label", "title": bi("Art", "Kind")},
                             {"field": "value_printed", "title": bi("Wert im Druck (°R)", "Value as printed (°R)")},
                             {"field": "temp_c_min", "title": bi("°C (von)", "°C (from)"), "format": ".1f"},
                             {"field": "temp_c_max", "title": bi("°C (bis)", "°C (to)"), "format": ".1f"},
                             {"field": "observer", "title": bi("Beobachter", "Observer")},
                             {"field": "date_text", "title": bi("Datum", "Date")}]},
             "layer": [
                 {"transform": [{"filter": "datum.kind == 'stage'"}],
                  "mark": {"type": "bar", "height": 10, "opacity": 0.8},
                  "encoding": {"x": {"field": "temp_c_min", "type": "quantitative", "title": "°C", "scale": {"domain": [0, 16], "zero": True}, "axis": {"grid": True}}, "x2": {"field": "temp_c_max"}}},
                 {"transform": [{"filter": "datum.kind != 'stage'"}],
                  "mark": {"type": "point", "filled": True, "size": 110, "opacity": 1},
                  "encoding": {"x": {"field": "temp_mid", "type": "quantitative", "title": "°C", "scale": {"domain": [0, 16], "zero": True}, "axis": {"grid": True}}}},
             ]}},
    ],
    "keywords": {
        "de": ["Quelltemperatur", "Quellen", "Brunnen", "Wassertemperatur", "Kraftsdorf", "Dessegrund", "Röttersdorf", "Réaumur", "Hohenleuben"],
        "en": ["spring temperature", "springs", "wells", "water temperature", "Kraftsdorf", "Dessegrund", "Röttersdorf", "Réaumur", "Hohenleuben"]},
    "related": ["klima-regenmenge-gera-1860-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
