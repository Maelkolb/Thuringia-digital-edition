"""A09 / analysis 7: Löhne und Pacht in der Landwirthschaft (p. 227, Fließtext). Zahlen aus dem Text abgelesen (teils ausgeschrieben)."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

txt = block("227", "b3")["text"]
# sanity: the quoted passages are in the block
for needle in ["neun bis zwölf", "vier bis acht", "drei bis sechs", "im Winter 10, im Sommer 12 bis 20", "fünf bis sechs, im Sommer acht bis zehn",
               "fünf bis sechs, der weibliche drei Silbergroschen", "das Doppelte ohne Kost", "30 bis 50 und Mägde 18 bis 30 Thaler", "nahe um das Doppelte", "um das Doppelte gewachsen"]:
    assert needle in txt, needle

KAT = {1: ("Tagelohn", "Day wage", "Silbergroschen je Tag", "Silbergroschen per day"),
       2: ("Jahreslohn des Gesindes", "Annual wage of farm servants", "Thaler im Jahr", "Thaler per year"),
       3: ("Pachtpreis", "Rent", "Thaler je Morgen", "Thaler per Morgen")}
# nr, kat, label_de, label_en, gebiet_de, gebiet_en, min, max, derived-note
ROWS = [
    (1, 1, "Mann, Winter", "Man, winter", "Unterland", "Lower Land", 10, 10, None),
    (2, 1, "Mann, Sommer", "Man, summer", "Unterland", "Lower Land", 12, 20, None),
    (3, 1, "Frau, Winter", "Woman, winter", "Unterland", "Lower Land", 5, 6, None),
    (4, 1, "Frau, Sommer", "Woman, summer", "Unterland", "Lower Land", 8, 10, None),
    (5, 1, "Mann, mit Kost", "Man, with board", "Oberland", "Upper Land", 5, 6, None),
    (6, 1, "Frau, mit Kost", "Woman, with board", "Oberland", "Upper Land", 3, 3, None),
    (7, 1, "Mann, ohne Kost", "Man, without board", "Oberland", "Upper Land", 10, 12, "doppelter Satz laut Text"),
    (8, 1, "Frau, ohne Kost", "Woman, without board", "Oberland", "Upper Land", 6, 6, "doppelter Satz laut Text"),
    (9, 2, "Knechte", "Farm hands (men)", "Land", "Country", 30, 50, None),
    (10, 2, "Mägde", "Farm maids (women)", "Land", "Country", 18, 30, None),
    (11, 3, "Einzelne Grundstücke", "Single plots", "beide Gebiete", "both areas", 9, 12, None),
    (12, 3, "Große Güter, Unterland", "Large estates, Lower Land", "Unterland", "Lower Land", 4, 8, None),
    (13, 3, "Große Güter, Oberland", "Large estates, Upper Land", "Oberland", "Upper Land", 3, 6, None),
]
rows = []
for nr, kat, lde, len_, gde, gen, mn, mx, note in ROWS:
    kde, ken, ude, uen = KAT[kat]
    mid = (mn + mx) / 2
    if kat == 3:
        mn_ha = round(mn / MORGEN_HA, 1)
        mx_ha = round(mx / MORGEN_HA, 1)
    else:
        mn_ha = mx_ha = None
    rows.append([nr, kat, kde, ken, ude, uen, lde, len_, gde, gen, mn, mx, mid, mn_ha, mx_ha, note])

by = {r[0]: r for r in rows}
mid = {r[0]: r[12] for r in rows}
mann_sommer = by[2]
print(mid)
# numbers
ratio_sommer = by[2][11] / by[5][11]            # 20 / 6
ratio_f = by[4][11] / by[6][11]                 # 10 / 3
ratio_pacht = by[11][12] / by[12][12]
ratio_pacht_o = by[11][12] / by[13][12]
magd_knecht = 100 * mid[10] / mid[9]
pacht_ha_u = (by[12][13], by[12][14])
pacht_ha_single = (by[11][13], by[11][14])
print(ratio_sommer, ratio_f, ratio_pacht, ratio_pacht_o, magd_knecht, pacht_ha_u, pacht_ha_single)
frau_mann_winter = 100 * mid[3] / mid[1]
frau_mann_sommer = 100 * mid[4] / mid[2]
frau_mann_ober = 100 * mid[6] / mid[5]
print(frau_mann_winter, frau_mann_sommer, frau_mann_ober)

REF = {"page": "227", "block": "b3"}


def col(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


SPELL = "teils im Text ausgeschrieben (z. B. »fünf bis sechs«), hier in Ziffern"
ana = {
    "id": "wirtschaft-loehne-pacht-landwirtschaft-1860er",
    "title": bi("Tagelöhne, Gesindelöhne und Pachtpreise in der Landwirthschaft (um 1868)", "Day wages, servants' wages and rents in agriculture (c. 1868)"),
    "category": "economy",
    "section": "t1-3-2",
    "sources": [REF, {"page": "227", "block": "b4"}],
    "summary": bi(
        "Brückner nennt im Fließtext die Pachtpreise für Feld (je Morgen) sowie Tagelöhne, Jahreslöhne von Knechten und Mägden und ihre Entwicklung. Die Angaben sind meist Spannen (»von … bis …«) und unterscheiden Unter- und Oberland. Die Diagramme stellen die Spannen als Bereiche dar.",
        "In the running text Brückner gives rents for arable land (per Morgen) as well as day wages, annual wages of farm hands and maids and their development. The figures are mostly ranges (“from … to …”) and distinguish the Lower and the Upper Land. The charts show the ranges as intervals."),
    "method": bi(
        "Die Werte sind dem Absatz auf S. 227 (Block b3) entnommen; sie stehen dort teils in Ziffern (»10«, »12 bis 20«, »30 bis 50«), teils ausgeschrieben (»fünf bis sechs«, »vier bis acht«) und wurden einheitlich in Ziffern übertragen. Die Sätze für den Oberland ohne Kost sind nach Brückners Angabe »das Doppelte« der Sätze mit Kost (aus dem Text abgeleitet). Pachtpreise sind in Thaler je Morgen angegeben; für den Vergleich wurden sie mit Brückners Faktor (1 preuß. Morgen = 0,255322 ha, S. 832) auf Thaler je Hektar umgerechnet. Der Mittelwert einer Spanne ist das arithmetische Mittel ihrer Grenzen.",
        "The values are taken from the paragraph on p. 227 (block b3); there they are partly given in digits (“10”, “12 bis 20”, “30 bis 50”), partly spelled out (“fünf bis sechs”, “vier bis acht”) and were transferred uniformly into digits. The rates for the Upper Land without board are, according to Brückner, “double” the rates with board (derived from the text). Rents are given in Thaler per Morgen; for comparison they were converted to Thaler per hectare with Brückner's factor (1 Prussian Morgen = 0.255322 ha, p. 832). The mean of a range is the arithmetic mean of its limits."),
    "findings": [
        bi(f"Im Unterland, wo »durch Gera die Arbeitskräfte sehr gesucht sind«, verdient ein Taglöhner im Sommer 12–20 Silbergroschen, im Oberland mit Kost nur 5–6; die Obergrenze im Unterland ist damit mehr als dreimal so hoch (das {de_num(ratio_sommer,1)}-Fache). Der Winterlohn im Unterland (10 Sgr.) entspricht dem Oberland-Satz ohne Kost (10–12 Sgr.).",
           f"In the Lower Land, where “labour is much in demand because of Gera”, a day labourer earns 12–20 silver groschen in summer, in the Upper Land with board only 5–6; the upper limit in the Lower Land is thus more than three times as high ({en_num(ratio_sommer,1)} times). The winter wage in the Lower Land (10 Sgr.) equals the Upper Land rate without board (10–12 Sgr.)."),
        bi(f"Frauen erhalten im Unterland im Mittel {de_num(frau_mann_winter,0)} % (Winter) bzw. {de_num(frau_mann_sommer,0)} % (Sommer) des Männerlohns, im Oberland mit Kost {de_num(frau_mann_ober,0)} %.",
           f"Women receive on average {en_num(frau_mann_winter,0)} % (winter) or {en_num(frau_mann_sommer,0)} % (summer) of the men's wage in the Lower Land, and {en_num(frau_mann_ober,0)} % in the Upper Land with board."),
        bi(f"Knechte erhalten 30–50, Mägde 18–30 Thaler im Jahr; der Mittelwert der Mägde liegt bei {de_num(magd_knecht,0)} % des Knechtslohns. Tag- und Gesindelohn sind nach Brückner in den letzten 40 Jahren auf das Doppelte gestiegen.",
           f"Farm hands receive 30–50, maids 18–30 Thaler a year; the maids' mean is {en_num(magd_knecht,0)} % of the farm hands' wage. According to Brückner day and servants' wages have doubled in the last 40 years."),
        bi(f"Einzelne Grundstücke (mittelgutes Feld) werden mit 9–12 Thalern je Morgen verpachtet ({de_num(pacht_ha_single[0],0)}–{de_num(pacht_ha_single[1],0)} Thaler je Hektar), große Güter im Unterland mit 4–8 und im Oberland mit 3–6 Thalern je Morgen. Der mittlere Einzelpachtpreis ist damit rund das {de_num(ratio_pacht,1)}-Fache dessen der großen Güter des Unterlandes. Das Pachtgeld ist seit einem Menschenalter »nahe um das Doppelte« gestiegen.",
           f"Single plots (medium-quality field) are leased at 9–12 Thaler per Morgen ({en_num(pacht_ha_single[0],0)}–{en_num(pacht_ha_single[1],0)} Thaler per hectare), large estates at 4–8 Thaler per Morgen in the Lower Land and 3–6 in the Upper Land. The mean rent for single plots is thus about {en_num(ratio_pacht,1)} times that of the large estates of the Lower Land. Rents have risen “by nearly double” in a generation."),
    ],
    "caveats": [
        bi("Es handelt sich um Spannen aus dem Fließtext, nicht um Messreihen; Jahr und Quelle der Erhebung nennt Brückner nicht (Schilderung der Verhältnisse um 1868). Die Sätze für Frauen und die Oberland-Sätze ohne Kost sind aus den Angaben des Textes zusammengestellt.",
           "These are ranges from the running text, not measured series; Brückner does not name year or source of the survey (description of conditions around 1868). The rates for women and the Upper Land rates without board are compiled from the statements of the text."),
        bi("Im Oberland erhält der Taglöhner mit Kost die niedrigeren Sätze und ohne Kost das Doppelte, »doch gewöhnlich mit einem Früh- und Vespertrunke«; der Wert der Kost ist nicht beziffert und lässt sich nicht umrechnen. Die Währungseinheiten (Thaler, Silbergroschen) sind unverändert übernommen.",
           "In the Upper Land the labourer receives the lower rates with board and double without board, “usually with a morning and an afternoon drink”; the value of the board is not stated and cannot be converted. The monetary units (Thaler, silver groschen) are taken over unchanged."),
    ],
    "conversions": [
        {"from": "Thaler je preußischer Morgen", "to": "Thaler je Hektar", "factor_or_formula": "Thaler/ha = Thaler/Morgen ÷ 0,255322", "reference": "Brückner S. 832: 1 preuß. Morgen = 0,255322 Hectaren"},
    ],
    "datasets": [
        {"name": "loehne", "title": bi("Löhne und Pachtpreise (Spannen)", "Wages and rents (ranges)"),
         "columns": [
             col("nr", "Laufende Nummer", "Serial number", "integer", derived=True),
             col("kat_nr", "Reihenfolge Kategorie", "Category order", "integer", derived=True),
             col("kategorie_de", "Kategorie", "Category", "string"),
             col("kategorie_en", "Kategorie (englisch)", "Category (English)", "string"),
             col("einheit_de", "Einheit", "Unit", "string"),
             col("einheit_en", "Einheit (englisch)", "Unit (English)", "string"),
             col("merkmal_de", "Gruppe", "Group", "string"),
             col("merkmal_en", "Gruppe (englisch)", "Group (English)", "string"),
             col("gebiet_de", "Gebiet", "Area", "string"),
             col("gebiet_en", "Gebiet (englisch)", "Area (English)", "string"),
             col("min", "Untergrenze", "Lower limit", "number", None, derived=True, note=SPELL),
             col("max", "Obergrenze", "Upper limit", "number", None, derived=True, note=SPELL),
             col("mitte", "Mittelwert der Spanne", "Mean of the range", "number", None, derived=True),
             col("min_je_ha", "Untergrenze je Hektar (nur Pacht)", "Lower limit per hectare (rents only)", "number", "Thaler/ha", derived=True, note="Thaler je Morgen ÷ 0,255322"),
             col("max_je_ha", "Obergrenze je Hektar (nur Pacht)", "Upper limit per hectare (rents only)", "number", "Thaler/ha", derived=True, note="Thaler je Morgen ÷ 0,255322"),
             col("bemerkung", "Bemerkung", "Note", "string"),
         ],
         "rows": rows, "source_refs": [REF]},
    ],
    "charts": [],
    "keywords": {
        "de": ["Löhne", "Tagelohn", "Gesinde", "Knechte", "Mägde", "Pacht", "Pachtpreis", "Preise", "Silbergroschen", "Landwirtschaft", "Unterland", "Oberland"],
        "en": ["wages", "day wage", "farm servants", "rent", "lease price", "prices", "silver groschen", "agriculture", "Lower Land", "Upper Land"],
    },
    "related": ["landwirtschaft-ernte-versorgung", "wirtschaft-berufsklassen-1864"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}


def rangechart(cid, kat_nr, title, caption, unit_title, height, domain, extra_tip=None):
    y = {"field": {"de": "merkmal_de", "en": "merkmal_en"}, "type": "nominal", "sort": {"field": "nr", "op": "min"}, "title": None, "axis": {"labelLimit": 280}}
    colr = {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "type": "nominal", "title": None, "scale": {"domain": domain}}
    if len(domain) == 1:
        colr["legend"] = None
    tip = [{"field": {"de": "merkmal_de", "en": "merkmal_en"}, "title": bi("Gruppe", "Group")},
           {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "title": bi("Gebiet", "Area")},
           {"field": "min", "title": bi("von", "from")}, {"field": "max", "title": bi("bis", "to")}]
    if extra_tip:
        tip += extra_tip
    xx = {"type": "quantitative", "title": unit_title, "scale": {"zero": True}}
    return {"id": cid, "dataset": "loehne", "title": title, "caption": caption,
            "vegalite": {"height": height, "transform": [{"filter": f"datum.kat_nr == {kat_nr}"}],
                         "layer": [
                             {"mark": {"type": "rule", "strokeWidth": 6, "opacity": 1}, "encoding": {"y": y, "x": {"field": "min", **xx}, "x2": {"field": "max"}, "color": colr}},
                             {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1}, "encoding": {"y": y, "x": {"field": "min", **xx}, "color": colr}},
                             {"mark": {"type": "point", "filled": True, "size": 90, "opacity": 1}, "encoding": {"y": y, "x": {"field": "max", **xx}, "color": colr, "tooltip": tip}}]}}


ana["charts"] = [
    rangechart("c1", 1, bi("Tagelöhne im Unter- und Oberland", "Day wages in the Lower and Upper Land"),
               bi("Spannen der Tagelöhne in Silbergroschen je Tag. Die Sommerlöhne der Männer im Unterland reichen bis 20 Sgr., im Oberland mit Kost nur bis 6 Sgr.; ohne Kost verdoppeln sich die Oberland-Sätze (nach Brückner).",
                  "Ranges of day wages in silver groschen per day. Men's summer wages in the Lower Land reach up to 20 Sgr., in the Upper Land with board only up to 6 Sgr.; without board the Upper Land rates double (according to Brückner)."),
               bi("Silbergroschen je Tag", "Silver groschen per day"), 300, [bi("Unterland", "Lower Land"), bi("Oberland", "Upper Land")]),
    rangechart("c2", 2, bi("Jahreslohn von Knechten und Mägden", "Annual wages of farm hands and maids"),
               bi("Spanne des Jahreslohns in Thalern.", "Range of the annual wage in Thaler."),
               bi("Thaler im Jahr", "Thaler per year"), 160, [bi("Land", "Country")]),
    rangechart("c3", 3, bi("Pachtpreise für Feld", "Rents for arable land"),
               bi("Pachtpreis je Morgen und Jahr in Thalern (einzelne Grundstücke: mittelgutes Feld). Einzelne Grundstücke bringen knapp doppelt so viel wie die großen Güter.",
                  "Rent per Morgen and year in Thaler (single plots: medium-quality field). Single plots yield almost twice as much as the large estates."),
               bi("Thaler je Morgen", "Thaler per Morgen"), 200, [bi("Unterland", "Lower Land"), bi("Oberland", "Upper Land"), bi("beide Gebiete", "both areas")],
               [{"field": "min_je_ha", "title": bi("von, Thaler je ha", "from, Thaler per ha"), "format": ".0f"}, {"field": "max_je_ha", "title": bi("bis, Thaler je ha", "to, Thaler per ha"), "format": ".0f"}]),
]
write_analysis(ana)
