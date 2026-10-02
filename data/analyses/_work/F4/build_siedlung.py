from common import *

MERGES = [
    "bevoelkerung-gemeindegroessen-1867",
    "wohnen-wohnhaeuser-wohndichte-1867",
    "orte-siedlungsbild-1867",
    "wohnen-kirchenneubauten-1611-1842",
]

places = dataset("orte-siedlungsbild-1867", "places")
houses = dataset("wohnen-wohnhaeuser-wohndichte-1867", "houses")
churches = dataset("wohnen-kirchenneubauten-1611-1842", "new_churches")
size_total = dataset("bevoelkerung-gemeindegroessen-1867", "size_total")
compare = dataset("wohnen-wohnhaeuser-wohndichte-1867", "persons_per_house_compare")
orte_basis = shared("base_places.json")
fluesse_basis = shared("base_rivers.json")

# ---------------------------------------------------------------- numbers
PL = rows_of(places)
n_places = len(PL)
total_pop = sum(r["inhabitants"] for r in PL)
big = [r for r in PL if r["inhabitants"] >= 1000]
small = [r for r in PL if r["inhabitants"] < 1000]
n_big, n_small = len(big), len(small)
share_big = sum(r["inhabitants"] for r in big) / total_pop * 100
share_small = 100 - share_big
gera = next(r for r in PL if r["name"] == "Gera")
schleiz = next(r for r in PL if r["name"] == "Schleiz")
share_gera = gera["inhabitants"] / total_pop * 100
n_up_to_500 = sum(1 for r in PL if r["inhabitants"] <= 500)
located = sum(1 for r in PL if r["lon"] is not None)
assert n_places == 173 and n_big == 14 and n_small == 159

H = {(r["district"], r["settlement"]): r for r in rows_of(houses)}
pph_towns = H[("Fürstentum", "Städte")]["persons_per_house"]
pph_rural = H[("Fürstentum", "Landorte")]["persons_per_house"]
pph_all = H[("Fürstentum", "Zusammen")]["persons_per_house"]
pph_gera_town = H[("Gera", "Städte")]["persons_per_house"]
pph_gera_rural = H[("Gera", "Landorte")]["persons_per_house"]
fam_towns = H[("Fürstentum", "Städte")]["families_per_house"]
CMP = {r["region"]: r["persons_per_house"] for r in rows_of(compare)}
for d in ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstentum"]:
    assert H[(d, "Städte")]["persons_per_house"] > H[(d, "Landorte")]["persons_per_house"]

CH = rows_of(churches)
decade = lambda y: y // 10 * 10
n_churches = len(CH)
n_dec1710 = sum(1 for r in CH if 1710 <= r['year_start'] < 1720)
assert n_dec1710 == 6
peak = [r for r in CH if 1710 <= r["year_start"] <= 1739]
n_peak = len(peak)
n17 = sum(1 for r in CH if r["year_start"] < 1700)
n18 = sum(1 for r in CH if 1700 <= r["year_start"] < 1800)
first_year, last_year = min(r["year_start"] for r in CH), max(r["year_start"] for r in CH)
assert n_churches == 30 and n_peak == 12

n = lambda x, d=0: pair(x, d)
log = [("places", n_places), ("total_pop", total_pop), ("big/small", (n_big, n_small)), ("shares", (share_big, share_small, share_gera)),
       ("<=500", n_up_to_500), ("located", located), ("pph", (pph_towns, pph_rural, pph_all, pph_gera_town)),
       ("churches", (n_churches, n_peak, n17, n18, first_year, last_year))]

# ---------------------------------------------------------------- chart 1: map
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}
BIG_NAMES = [r["name"] for r in big]


def label_layers(names, **mark):
    flt = {"transform": [{"filter": f"indexof({json.dumps(names, ensure_ascii=False)}, datum.name) >= 0"}]}
    enc = {"longitude": LON, "latitude": LAT, "text": {"field": "name"}}
    return [
        {**flt, "mark": {"type": "text", "style": "place-halo", **mark}, "encoding": enc},
        {**flt, "mark": {"type": "text", "style": "place-label", **mark}, "encoding": enc},
    ]


RIGHT = ["Gera", "Langenberg", "Langenwetzendorf", "Tanna", "Schleiz", "Hirschberg", "Ebersdorf"]
LEFT = ["Untermhaus", "Köstritz", "Triebes", "Lobenstein", "Saalburg"]
ABOVE = ["Hohenleuben", "Wurzbach"]
assert sorted(RIGHT + LEFT + ABOVE) == sorted(BIG_NAMES), set(BIG_NAMES) ^ set(RIGHT + LEFT + ABOVE)

TT_PLACE = [tooltip("name", "Ort", "Place"), tooltip("landestheil", "Landesteil", "District"),
            tooltip("inhabitants", "Einwohner 1867", "Inhabitants 1867", ",d"), tooltip("houses", "Häuser", "Houses", ",d"),
            tooltip("persons_per_house", "Personen je Haus", "Persons per house", ".1f")]

c1 = {
    "height": 600,
    "projection": {"type": "mercator"},
    "layer": [
        {"data": {"name": "fluesse_basis"},
         "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2, "interpolate": "monotone"},
         "encoding": {"longitude": LON, "latitude": LAT, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
        {"data": {"name": "orte_basis"},
         "mark": {"type": "circle", "size": 10, "color": "@land", "opacity": 1},
         "encoding": {"longitude": LON, "latitude": LAT}},
        {"transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat)"}, {"calculate": "datum.inhabitants >= 1000", "as": "big"}],
         "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8},
         "encoding": {
             "longitude": LON, "latitude": LAT,
             "order": {"field": "inhabitants", "type": "quantitative", "sort": "descending"},
             "size": {"field": "inhabitants", "type": "quantitative", "scale": {"type": "sqrt", "domain": [0, 16283], "range": [4, 800]},
                      "legend": {"title": {"de": "Einwohner 1867", "en": "Inhabitants 1867"}, "values": [100, 1000, 5000, 15000], "format": ",d",
                                 "orient": "none", "legendX": 6, "legendY": 58, "direction": "vertical", "symbolFillColor": "@muted", "symbolStrokeColor": "@paper"}},
             "color": {"condition": {"test": "datum.big", "value": "@accent"}, "value": "@muted"},
             "opacity": {"condition": {"test": "datum.big", "value": 0.95}, "value": 0.55},
             "tooltip": TT_PLACE}},
        {"transform": [{"filter": "datum.name === 'Gera'"}],
         "mark": {"type": "text", "style": "label", "align": "left", "color": "@accent"},
         "encoding": {"x": {"value": 6}, "y": {"value": 14},
                      "text": {"value": {"de": f"{n_big} Orte mit 1.000 und mehr Einwohnern", "en": f"{n_big} places with 1,000 or more inhabitants"}}}},
        {"transform": [{"filter": "datum.name === 'Gera'"}],
         "mark": {"type": "text", "style": "label-muted", "align": "left"},
         "encoding": {"x": {"value": 6}, "y": {"value": 33},
                      "text": {"value": {"de": f"{n_small} kleinere Orte", "en": f"{n_small} smaller places"}}}},
        *label_layers(RIGHT, align="left", dx=12),
        *label_layers(LEFT, align="right", dx=-12),
        *label_layers(ABOVE, dy=-14),
    ],
}


# ---------------------------------------------------------------- chart 2: persons per house
ORDER_H = ["Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstentum"]
TT_H = [tooltip("district", "Bezirk", "District"), tooltip("Städte", "Städte, Personen je Haus", "Towns, persons per house", ".2f"),
        tooltip("Landorte", "Landorte, Personen je Haus", "Villages, persons per house", ".2f")]
c2 = {
    "height": {"step": 56},
    "transform": [
        {"filter": "datum.settlement === 'Städte' || datum.settlement === 'Landorte'"},
        {"pivot": "settlement", "value": "persons_per_house", "groupby": ["district"]},
    ],
    "encoding": {
        "y": {"field": "district", "type": "nominal", "sort": ORDER_H,
              "axis": {"title": None, "labelLimit": 400,
                       "labelExpr": {"de": "datum.value", "en": "datum.value == 'Fürstentum' ? 'Principality' : datum.value"},
                       "labelFontWeight": {"condition": {"test": "datum.value == 'Fürstentum'", "value": 700}, "value": 400}}},
    },
    "layer": [
        {"mark": {"type": "rule", "color": "@context", "strokeWidth": 3},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative", "scale": {"domain": [4, 17]},
                            "axis": {"values": [5, 10, 15], "title": {"de": "Einwohner je bewohntes Wohnhaus, 1867", "en": "Inhabitants per inhabited house, 1867"}}},
                      "x2": {"field": "Städte"}}},
        {"mark": {"type": "point", "filled": True, "size": 110, "color": "@muted"},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"}, "tooltip": TT_H}},
        {"mark": {"type": "point", "filled": True, "size": 130, "color": "@accent"},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"}, "tooltip": TT_H}},
        {"mark": {"type": "text", "style": "label-muted", "align": "right", "dx": -11},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"}, "text": {"field": "Landorte", "format": ".1f"}}},
        {"mark": {"type": "text", "style": "label", "align": "left", "dx": 12, "color": "@accent"},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"}, "text": {"field": "Städte", "format": ".1f"}}},
        {"transform": [{"filter": "datum.district === 'Gera'"}],
         "mark": {"type": "text", "style": "label-muted", "align": "center", "dy": -17},
         "encoding": {"x": {"field": "Landorte", "type": "quantitative"}, "text": {"value": {"de": "Landorte", "en": "Villages"}}}},
        {"transform": [{"filter": "datum.district === 'Gera'"}],
         "mark": {"type": "text", "style": "label", "align": "center", "dy": -17, "color": "@accent"},
         "encoding": {"x": {"field": "Städte", "type": "quantitative"}, "text": {"value": {"de": "Städte", "en": "Towns"}}}},
    ],
}

# ---------------------------------------------------------------- chart 3: church building
TT_C = [tooltip("place_label", "Kirche", "Church"), tooltip("year_start", "Baujahr (Beginn)", "Year of building (start)", "d"),
        tooltip("year_end", "Ende", "End", "d")]
c3 = {
    "height": 300,
    "transform": [
        {"calculate": "floor(datum.year_start / 10) * 10", "as": "decade"},
        {"window": [{"op": "row_number", "as": "rank"}], "groupby": ["decade"], "sort": [{"field": "year_start"}]},
        {"calculate": "datum.year_start >= 1710 && datum.year_start < 1740", "as": "peak"},
        {"calculate": "datum.decade + 10", "as": "decade_end"},
        {"calculate": "datum.rank - 1", "as": "rank_from"},
    ],
    "layer": [
        {"mark": {"type": "rect", "strokeWidth": 2, "cornerRadius": 2},
         "encoding": {
             "x": {"field": "decade", "type": "quantitative", "scale": {"domain": [1600, 1850], "nice": False},
                   "axis": {"values": [1600, 1650, 1700, 1750, 1800, 1850], "format": "d", "title": None}},
             "x2": {"field": "decade_end"},
             "y": {"field": "rank_from", "type": "quantitative", "scale": {"domain": [0, 7.6]},
                   "axis": {"values": [0, 2, 4, 6], "title": {"de": "Neubauten je Jahrzehnt", "en": "New buildings per decade"}}},
             "y2": {"field": "rank"},
             "color": {"condition": {"test": "datum.peak", "value": "@accent"}, "value": "@context"},
             "tooltip": TT_C}},
        {"transform": [{"filter": "datum.year_start == 1721"}],
         "mark": {"type": "text", "style": "label", "align": "center", "color": "@accent"},
         "encoding": {"x": {"datum": 1725}, "y": {"datum": 7.3},
                      "text": {"value": {"de": f"{n_peak} Kirchen 1710 bis 1739", "en": f"{n_peak} churches 1710 to 1739"}}}},
        {"transform": [{"filter": "datum.year_start == 1721"}],
         "mark": {"type": "rule", "color": "@accent", "strokeWidth": 2},
         "encoding": {"x": {"datum": 1710}, "x2": {"datum": 1740}, "y": {"datum": 6.75}}},
    ],
}

# ---------------------------------------------------------------- texts
NUM_WORD_DE = {12: "Zwölf"}
NUM_WORD_EN = {12: "Twelve"}
title = bi("Siedlungen und Häuser 1867", "Settlements and houses in 1867")
a, b = n(total_pop), n(n_big)
summary = bi(
    f"Brückner beschreibt {n_places} Gemeinden mit zusammen {a[0]} Einwohnern. {n_small} hatten weniger als 1.000 Einwohner; die {n_big} größeren Orte vereinten {n(share_big)[0]} Prozent der Bevölkerung, Gera allein {n(share_gera, 1)[0]} Prozent. "
    f"Auf ein Wohnhaus kamen im Fürstentum {n(pph_all, 1)[0]} Menschen, in den Städten {n(pph_towns, 1)[0]}, in Gera {n(pph_gera_town, 1)[0]}. "
    f"Aus der Neuzeit nennt er {n_churches} neu gebaute Kirchen, {n_peak} davon aus den Jahren 1710 bis 1739.",
    f"Brückner describes {n_places} municipalities with {a[1]} inhabitants in total. {n_small} had fewer than 1,000 inhabitants; the {n_big} larger places held {n(share_big)[1]} percent of the population, Gera alone {n(share_gera, 1)[1]} percent. "
    f"Per house there were {n(pph_all, 1)[1]} people in the principality, {n(pph_towns, 1)[1]} in the towns, {n(pph_gera_town, 1)[1]} in Gera. "
    f"For modern times he names {n_churches} newly built churches, {n_peak} of them from 1710 to 1739.",
)
CMP_TH = CMP["Thüringen (Durchschnitt)"]
CMP_SX = CMP["Sachsen"]
findings = [
    bi(f"{n_small} der {n_places} Gemeinden zählten unter 1.000 Einwohner und zusammen {n(share_small)[0]} Prozent der Bevölkerung; {n_up_to_500} Gemeinden hatten höchstens 500. Auf Gera folgt Schleiz mit {n(schleiz['inhabitants'])[0]} Einwohnern.",
       f"{n_small} of the {n_places} municipalities had under 1,000 inhabitants and together {n(share_small)[1]} percent of the population; {n_up_to_500} municipalities had at most 500. After Gera comes Schleiz with {n(schleiz['inhabitants'])[1]} inhabitants."),
    bi(f"Auf ein Wohnhaus kamen {n(pph_all, 2)[0]} Einwohner, in den Städten {n(pph_towns, 2)[0]}, auf dem Land {n(pph_rural, 2)[0]}, in der Stadt Gera {n(pph_gera_town, 2)[0]}. Für Thüringen nennt Brückner im Mittel {n(CMP_TH, 2)[0]}, für Sachsen {n(CMP_SX, 2)[0]}.",
       f"There were {n(pph_all, 2)[1]} inhabitants per house, {n(pph_towns, 2)[1]} in the towns, {n(pph_rural, 2)[1]} in the country, {n(pph_gera_town, 2)[1]} in the town of Gera. For Thuringia Brückner gives {n(CMP_TH, 2)[1]} on average, for Saxony {n(CMP_SX, 2)[1]}."),
    bi(f"Von den {n_churches} neuen Kirchen stammen {n17} aus dem 17., {n18} aus dem 18. und eine aus dem 19. Jahrhundert (Hirschberg 1842). Allein 1710 bis 1719 entstanden {n_dec1710}.",
       f"Of the {n_churches} new churches, {n17} date from the 17th, {n18} from the 18th and one from the 19th century (Hirschberg 1842). In 1710 to 1719 alone, {n_dec1710} were built."),
]
charts = [
    {"id": "c1", "dataset": "places", "extra_datasets": ["orte_basis", "fluesse_basis"],
     "title": bi(f"Nur {n_big} der {n_places} Gemeinden hatten 1867 mindestens 1.000 Einwohner, Gera allein {n(gera['inhabitants'])[0]}",
                 f"Only {n_big} of the {n_places} municipalities had 1,000 or more inhabitants in 1867, Gera alone {n(gera['inhabitants'])[1]}"),
     "caption": bi(f"Gemeinden nach der Einwohnerzahl 1867 (Kreisfläche); blau die {n_big} größten. Verortet sind {located} von {n_places} Orten, die Lage folgt GeoNames. Grundlage sind die Ortsartikel; Größenklassen S. 98.",
                   f"Municipalities by population in 1867 (area of circles); blue the {n_big} largest. {located} of {n_places} places are located, positions follow GeoNames. Based on the place articles; size classes p. 98."),
     "vegalite": c1},
    {"id": "c2", "dataset": "houses",
     "title": bi(f"Stadthäuser beherbergten mehr Menschen als Landhäuser, in Gera {n(pph_gera_town, 1)[0]} gegenüber {n(pph_gera_rural, 1)[0]}",
                 f"Town houses held more people than rural houses, in Gera {n(pph_gera_town, 1)[1]} against {n(pph_gera_rural, 1)[1]}"),
     "caption": bi("Einwohner je bewohntes Wohnhaus 1867 in den Städten und den Landorten der drei Bezirke. Gemeint ist das Haus, nicht die Wohnung; Brückner führt Geras Wert auf mehr Stockwerke zurück. Quelle: S. 94.",
                   "Inhabitants per inhabited house in 1867 in the towns and villages of the three districts. The house is meant, not the flat; Brückner attributes Gera’s value to more storeys. Source: p. 94."),
     "vegalite": c2},
    {"id": "c3", "dataset": "new_churches",
     "title": bi(f"{NUM_WORD_DE[n_peak]} der {n_churches} genannten Kirchenneubauten entstanden zwischen 1710 und 1739",
                 f"{NUM_WORD_EN[n_peak]} of the {n_churches} new churches named were built between 1710 and 1739"),
     "caption": bi(f"Von Brückner genannte Kirchenneubauten {first_year} bis {last_year}, je ein Block pro Kirche, nach Jahrzehnt des Baubeginns. Keine vollständige Zählung. Quelle: S. 133 f.",
                   f"New churches named by Brückner, {first_year} to {last_year}, one block per church, by decade of the start of building. Not a complete count. Source: pp. 133 f."),
     "vegalite": c3},
]

datasets = [places, houses, churches, size_total, compare, orte_basis, fluesse_basis]


def refs_pages(dss):
    out, seen = [], set()
    for ds in dss:
        for r in ds["source_refs"]:
            k = (r["page"], r["block"])
            if k not in seen:
                seen.add(k)
                out.append({"page": r["page"], "block": r["block"]})
    return out


sources = refs_pages([houses, churches, size_total, compare]) + [{"page": "418", "block": "b3"}]

feature = {
    "id": "siedlung-wohnen",
    "title": title,
    "category": "housing",
    "section": "t2",
    "merges": MERGES,
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": bi(
        "Die Gemeinden mit Einwohner- und Häuserzahl stammen aus den Ortsartikeln des zweiten Teils (S. 418 bis 825). Aufgenommen wurden die 173 politischen Gemeinden; Orte, die Brückner in die Zahlen anderer Gemeinden einrechnet, blieben unberücksichtigt. Es gilt die Zählung 1867, bei zweiherrischen Orten nur der reußische Anteil. "
        "Die Größenklassen und ihre Summen stehen in Brückners Tabelle S. 98; sie stimmen mit den Ortsartikeln in allen Klassen bei der Zahl der Orte und in den meisten bei der Volksmenge überein. Die Koordinaten stammen aus GeoNames, sie sind abgeleitet und beziehen sich auf die heutigen Orte; für zehn Orte fehlt eine verlässliche Zuordnung. "
        "Die Einwohner je Wohnhaus stehen in der Tabelle S. 94 (Städte, Landorte, Landesteile); die Zahlen für Thüringen und Sachsen stammen aus dem Text derselben Seite. "
        "Die Kirchenneubauten wurden aus dem Fließtext S. 133 f. ausgelesen; bei Baujahren in Spannen (Gera 1611 bis 1613, Tanna 1640 bis 1642) zählt das erste Jahr. Jahrzehnte entsprechen dem Jahr des Baubeginns. "
        "Nicht verwendet wurden die Häuser je Quadratmeile, die Familien je Haus und die älteren Bauteile (Sakristei Schleiz 1101, Kapelle Untermhaus 1193); sie stehen in den Einzelauswertungen.",
        "The municipalities with their population and number of houses come from the place articles of the second part (pp. 418 to 825). The 173 political municipalities were included; places that Brückner counts within the figures of other municipalities were left out. The count of 1867 applies, and for places under two lords only the Reuss share. "
        "The size classes and their totals are in Brückner’s table on p. 98; they agree with the place articles in all classes for the number of places and in most for the population. The coordinates come from GeoNames, they are derived and refer to today’s places; for ten places no reliable assignment exists. "
        "The inhabitants per house are in the table on p. 94 (towns, villages, districts); the figures for Thuringia and Saxony come from the text of the same page. "
        "The new churches were read from the running text on pp. 133 f.; for building years given as spans (Gera 1611 to 1613, Tanna 1640 to 1642) the first year counts. Decades correspond to the year the building began. "
        "Not used are the houses per square mile, the families per house and the older building parts (sacristy Schleiz 1101, chapel Untermhaus 1193); they are in the single analyses."),
    "caveats": [
        bi("Gezählt werden politische Gemeinden, nicht Siedlungen im Sinn von Ortschaften; mehrere Dörfer können eine Gemeinde bilden. Die Einwohnerzahlen der Landesteil-Einleitungen weichen von den Summen der Orte ab (Gera +105, Schleiz +2, Lobenstein-Ebersdorf −15); Brückners Quellen sind nicht ganz einheitlich.",
           "Political municipalities are counted, not settlements in the sense of localities; several villages can form one municipality. The population figures in the district introductions differ from the sums of the places (Gera +105, Schleiz +2, Lobenstein-Ebersdorf −15); Brückner’s sources are not entirely consistent."),
        bi("Die Koordinaten sind GeoNames-Positionen der heutigen Orte, nicht Brückners Angaben. Zehn Orte sind unverortet oder wegen zweifelhafter Zuordnung ausgelassen; die Karte zeigt 163 der 173 Orte.",
           "The coordinates are GeoNames positions of today’s places, not Brückner’s statements. Ten places are unlocated or left out because of doubtful assignment; the map shows 163 of the 173 places."),
        bi("Die Zahl der Häuser ist nicht überall gleich definiert (Privathäuser, bewohnte Gebäude; bei Gera einschließlich Pöppeln). Einwohner je Haus ist daher nur ein grobes Maß der Haushaltsgröße. Die Städte-Spalte umfasst nur die sechs Städte des Landes und ist stark von Gera geprägt.",
           "The number of houses is not defined the same way everywhere (private houses, inhabited buildings; for Gera including Pöppeln). Inhabitants per house is therefore only a rough measure of household size. The towns column covers only the six towns of the country and is strongly shaped by Gera."),
        bi("Die Kirchenliste gibt, was Brückner als neue Kirchen hervorhebt; Umbauten und Erweiterungen sind nicht erfasst, das 19. Jahrhundert ist nur durch Hirschberg (1842) vertreten. Die Häufung 1710 bis 1739 zeigt Brückners Auswahl und nicht notwendig die Bautätigkeit.",
           "The list of churches gives what Brückner highlights as new churches; conversions and extensions are not covered, and the 19th century is represented only by Hirschberg (1842). The cluster in 1710 to 1739 shows Brückner’s selection and not necessarily the building activity."),
    ],
    "datasets": datasets,
    "charts": charts,
    "keywords": {
        "de": ["Siedlungen", "Gemeinden", "Ortsgrößen", "Einwohner", "Häuser", "Wohnhäuser", "Wohndichte", "Kirchenbau", "Kirchen", "Gera"],
        "en": ["settlements", "municipalities", "size of places", "inhabitants", "houses", "dwellings", "housing density", "church building", "churches", "Gera"],
    },
    "related": ["bevoelkerung-1647-1867", "dorfleben", "ortsnamen", "kirche-schule"],
    "generated_by": "Claude Sonnet 5.5 (Agent F4), aus 4 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    check_limits(feature)
    write_feature(feature)
    with open("C:/Users/totom/Projects/reuss-edition/data/analyses/_work/F4/check_siedlung.txt", "w", encoding="utf-8") as f:
        for k, v in log:
            f.write(f"{k}: {v}\n")
