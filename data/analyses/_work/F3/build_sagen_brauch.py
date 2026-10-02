import sys, collections
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F3")
from common import *

MERGES = [
    "kultur-sagenorte-nach-typ-und-landestheil",
    "kultur-volkskalender-bauernjahr",
    "gesundheit-volksmedizin-hausmittel-nach-leiden",
    "mundart-sprachproben-orte-und-textsorten",
]

coords = coordinate_lookup()
base_places, base_rivers = base_layers()

# ------------------------------------------------------------------ legend places (map)
sites = dicts(dataset("kultur-sagenorte-nach-typ-und-landestheil", "sites"))
places_arch = dataset("kultur-sagenorte-nach-typ-und-landestheil", "places")
TYPE_SHORT = {
    "Wiedenheer (Wotans Nachtjagd)": ("Wiedenheer", "Wild Hunt"),
    "Reiter, Jäger, Spukgestalten": ("Reiter und Jäger", "Riders and huntsmen"),
    "Hexentiere und Hexenplätze": ("Hexentiere", "Witch animals"),
    "Weiße Frau": ("Weiße Frau", "White lady"),
    "Schatzstellen": ("Schätze", "Treasures"),
    "Sagenhafte Klöster": ("Klöster", "Monasteries"),
    "Zauberer": ("Zauberer", "Sorcerers"),
    "Irrlichter": ("Irrlichter", "Will-o’-the-wisps"),
}
types_by_place = collections.defaultdict(list)
for s in sites:
    short = TYPE_SHORT[s["type_de"]]
    if short not in types_by_place[s["gazetteer_name"]]:
        types_by_place[s["gazetteer_name"]].append(short)
type_counts = collections.Counter()
for place, ts in types_by_place.items():
    for t in ts:
        type_counts[t[0]] += 1
print(type_counts)


def fn_place(d):
    c = coords.get(d["place"])
    ts = types_by_place[d["place"]]
    return [
        "; ".join(t[0] for t in ts),
        "; ".join(t[1] for t in ts),
        c[0] if c else None,
        c[1] if c else None,
    ]


places = places_arch
places["name"] = "legend_places"
places["title"] = bi("Sagenorte mit Zahl der Listen und Lage", "Legend sites with number of lists and position")
add_columns(
    places,
    [
        col("types_de", "Sagentypen", "Legend types", "string", None, True, "Brückners Listen auf S. 201–207, kurz benannt"),
        col("types_en", "Sagentypen (en)", "Legend types (en)", "string", None, True),
        col("lon", "Länge", "Longitude", "number", "° O", True, "GeoNames, über den Ortsnamen verknüpft; leer, wo der Ort im Ortsverzeichnis fehlt"),
        col("lat", "Breite", "Latitude", "number", "° N", True, "GeoNames"),
    ],
    fn_place,
)
pd_ = dicts(places)
for r in pd_:
    if r["place"] == "Arlas":
        pass
n_places = len(pd_)
mapped = [r for r in pd_ if r["lon"] is not None]
unmapped = [r["place"] for r in pd_ if r["lon"] is None]
print("places", n_places, "mapped", len(mapped), "unmapped", unmapped)
by_district = collections.Counter(r["district"] for r in pd_)
print(by_district)
top = sorted(pd_, key=lambda r: (-r["lists"], r["place"]))[:3]
print([(r["place"], r["lists"]) for r in top])
label_places = [r["place"] for r in pd_ if r["lists"] >= 3 and r["lon"] is not None]
print("labelled", label_places)
n_gera, n_schleiz, n_lob = by_district["Gera"], by_district["Schleiz"], by_district["Lobenstein-Ebersdorf"]

# ------------------------------------------------------------------ calendar
calendar = dataset("kultur-volkskalender-bauernjahr", "calendar")
cd = dicts(calendar)
KINDS = [
    ("Brauch und Fest", "Bräuche und Feste", "Customs and feasts"),
    ("Wetter- und Ernteregel", "Wetter- und Ernteregeln", "Weather and harvest lore"),
    ("Festspeise", "Festspeisen", "Feast dishes"),
    ("Landarbeit und Gesinde", "Landarbeit und Gesinde", "Farm work and servants"),
    ("Orakel, Zauber, Schutz", "Orakel, Zauber, Schutz", "Oracles, magic, protection"),
]
kc = collections.Counter(r["kind_de"] for r in cd)
assert [k[0] for k in sorted(KINDS, key=lambda k: -kc[k[0]])] == [k[0] for k in KINDS], kc
kind_order = {k[0]: i + 1 for i, k in enumerate(KINDS)}
add_columns(
    calendar,
    [col("kind_order", "Reihenfolge der Sorte in der Grafik", "Order of the kind in the chart", "integer", None, True)],
    lambda d: [kind_order[d["kind_de"]]],
)
month_counts = collections.Counter(r["month"] for r in cd)
peak_month = month_counts.most_common(1)[0]
print("months", sorted(month_counts.items()), "peak", peak_month)
weather = [r for r in cd if r["kind_de"] == "Wetter- und Ernteregel"]
weather_summer = sum(1 for r in weather if 6 <= r["month"] <= 8)
twelve = [r for r in cd if r["day"] and ((r["month"] == 12 and r["day"] >= 21) or (r["month"] == 1 and r["day"] <= 6))]
print("weather", len(weather), weather_summer, "twelve nights", len(twelve))
n_calendar = len(cd)
feb_dec_jan = {m: month_counts[m] for m in (12, 1, 2, 5)}
winter = month_counts[12] + month_counts[1] + month_counts[2]

# ------------------------------------------------------------------ medicine
remedies = dataset("gesundheit-volksmedizin-hausmittel-nach-leiden", "remedies")
rd = dicts(remedies)
order_use = collections.OrderedDict()
for r in rd:
    key = (r["use_key"], r["use_de"], r["use_en"], r["scope_de"], r["scope_en"])
    order_use.setdefault(key, []).append(r["remedy"])
ailment_rows = []
for (k, de, en, sde, sen), rem in order_use.items():
    if sde == "allgemein":
        household = len(rem)
        continue
    ailment_rows.append([de, en, sde, sen, len(rem), ", ".join(rem[:3]), 1 if k == "aussen" else 2])
ailment_rows.sort(key=lambda r: (-r[4], r[0]))
ailments = make_dataset(
    "ailments",
    "Zahl der Mittel je Leiden",
    "Number of remedies per ailment",
    [
        col("use_de", "Leiden oder Verwendung", "Ailment or use", "string", None, False),
        col("use_en", "Leiden (en)", "Ailment (en)", "string", None, True),
        col("scope_de", "Anwendung", "Application", "string", None, True),
        col("scope_en", "Anwendung (en)", "Application (en)", "string", None, True),
        col("remedies", "Zahl der Mittel", "Number of remedies", "integer", "Mittel", True),
        col("examples", "Die ersten drei Mittel (gedruckt)", "The first three remedies (as printed)", "string", None, False),
        col("focus", "Hervorhebung", "Focus", "integer", None, True),
    ],
    ailment_rows,
    dataset("gesundheit-volksmedizin-hausmittel-nach-leiden", "use_counts")["source_refs"],
)
print("household", household, [(r[0], r[4]) for r in ailment_rows])
external = ailment_rows[0]
assert external[0].startswith("Äußere")
epilepsy = next(r for r in ailment_rows if r[0] == "Epilepsie")
chest = next(r for r in ailment_rows if r[0] == "Brustmittel")
stomach = next(r for r in ailment_rows if r[0] == "Magenleiden")
n_remedies_single = sum(r[4] for r in ailment_rows)

# ------------------------------------------------------------------ dialect
samples = dataset("mundart-sprachproben-orte-und-textsorten", "samples")
sd = dicts(samples)
n_texts = len(sd)
n_sample_places = len({r["place"] for r in sd})
words_total = sum(r["words"] for r in sd)
print("dialect", n_texts, n_sample_places, words_total)

# ------------------------------------------------------------------ specs
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}
DISTRICT = {
    "field": "district",
    "type": "nominal",
    "scale": {"domain": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"], "range": ["@accent", "@accent2", "@accent3"]},
    "legend": {"title": None, "orient": "top", "direction": "horizontal"},
}
ZOOM = {"lon": (11.90, 12.20), "lat": (50.80, 50.99)}
SIZE = {
    "field": "lists",
    "type": "quantitative",
    "scale": {"type": "sqrt", "domain": [0, 6], "range": [0, 200]},
}
SIZE_LEGEND = {
    "title": {"de": "Zahl der Sagenlisten", "en": "Number of legend lists"},
    "titleLimit": 300,
    "values": [1, 3, 6],
    "orient": "top",
    "direction": "horizontal",
    "symbolFillColor": "@muted",
    "symbolStrokeColor": "@paper",
}


def inside(margin=0.0):
    lo, la = ZOOM["lon"], ZOOM["lat"]
    return f"datum.lon >= {lo[0] - margin} && datum.lon <= {lo[1] + margin} && datum.lat >= {la[0] - margin} && datum.lat <= {la[1] + margin}"


def lab_filter(names):
    return "indexof(" + str(names) + ", datum.place) >= 0 && isValid(datum.lon)"


def label_layers(names, dy=-11):
    return [
        {
            "transform": [{"filter": lab_filter(names)}],
            "mark": {"type": "text", "style": style, "dy": dy},
            "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}},
        }
        for style in ("place-halo", "place-label")
    ]


def sites_layer(legend, window=False):
    return {
        "transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat)" + (" && " + inside() if window else "")}],
        "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85},
        "encoding": {
            "longitude": LON,
            "latitude": LAT,
            "size": {**SIZE, "legend": SIZE_LEGEND},
            "color": {**DISTRICT, "legend": DISTRICT["legend"]},
            "tooltip": [
                tip("place", "Ort", "Place"),
                tip({"de": "types_de", "en": "types_en"}, "Sagentypen", "Legend types"),
                tip("lists", "Zahl der Listen", "Number of lists"),
                tip("district", "Landesteil", "District"),
            ],
        },
    }


BASE = [
    {
        "data": {"name": "fluesse_basis"},
        "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2, "interpolate": "monotone"},
        "encoding": {"longitude": LON, "latitude": LAT, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}},
    },
    {
        "data": {"name": "orte_basis"},
        "mark": {"type": "circle", "size": 10, "color": "@land", "opacity": 1},
        "encoding": {"longitude": LON, "latitude": LAT},
    },
]
zoom_frame = {
    "transform": [{"filter": "datum.place == 'Gera'"}],
    "mark": {"type": "rect", "fill": None, "stroke": "@ink2", "strokeWidth": 1, "strokeDash": [3, 3]},
    "encoding": {
        "longitude": {"datum": ZOOM["lon"][0]},
        "longitude2": {"datum": ZOOM["lon"][1]},
        "latitude": {"datum": ZOOM["lat"][0]},
        "latitude2": {"datum": ZOOM["lat"][1]},
    },
}
overview = {
    "width": 385,
    "height": 500,
    "projection": {"type": "mercator", "center": [11.835, 50.675], "scale": 28800, "translate": [192.5, 250]},
    "layer": BASE + [sites_layer(True), zoom_frame] + label_layers(["Hohenleuben", "Schleiz", "Lobenstein", "Saalburg", "Hirschberg"]),
}
detail = {
    "width": 430,
    "height": 430,
    "projection": {"type": "mercator", "center": [(ZOOM["lon"][0] + ZOOM["lon"][1]) / 2, (ZOOM["lat"][0] + ZOOM["lat"][1]) / 2], "scale": 81500, "translate": [215, 215]},
    "layer": [dict(BASE[0], transform=[{"filter": inside(0.003)}]), dict(BASE[1], transform=[{"filter": inside()}]), sites_layer(False, True)] + label_layers(label_places),
}
c1 = {"spacing": 14, "hconcat": [overview, detail], "resolve": {"legend": {"color": "shared", "size": "shared"}}}

MONTH_DE = "['Jan.','Feb.','März','Apr.','Mai','Juni','Juli','Aug.','Sept.','Okt.','Nov.','Dez.']"
MONTH_EN = "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']"
KIND_DE = "['Gesamt'," + ",".join(f"'{k[1]}'" for k in KINDS) + "]"
KIND_EN = "['Total'," + ",".join(f"'{k[2]}'" for k in KINDS) + "]"
X_MONTH = {
    "field": "month",
    "type": "ordinal",
    "scale": {"domain": list(range(1, 13))},
    "axis": {"title": None, "orient": "top", "labelAngle": 0, "labelExpr": bi(f"{MONTH_DE}[datum.value-1]", f"{MONTH_EN}[datum.value-1]"), "ticks": False, "labelFontSize": 12},
}
Y_KIND = {
    "field": "kind_order",
    "type": "ordinal",
    "scale": {"domain": [0, 1, 2, 3, 4, 5]},
    "axis": {"title": None, "labelExpr": bi(f"{KIND_DE}[datum.value]", f"{KIND_EN}[datum.value]"), "labelLimit": 300, "labelFontSize": 12, "grid": False},
}
NAMES_DE_EN = {"calculate": bi(f"{MONTH_DE}[datum.month-1]", f"{MONTH_EN}[datum.month-1]"), "as": "month_name"}
KIND_NAME = {"calculate": bi(f"{KIND_DE}[datum.kind_order]", f"{KIND_EN}[datum.kind_order]"), "as": "kind_name"}
c2 = {
    "height": {"step": 34},
    "encoding": {"x": X_MONTH, "y": Y_KIND},
    "layer": [
        {
            "transform": [{"aggregate": [{"op": "count", "as": "n"}], "groupby": ["month", "kind_order"]}, NAMES_DE_EN, KIND_NAME],
            "mark": {"type": "rect"},
            "encoding": {
                "color": {"field": "n", "type": "quantitative", "scale": {"domain": [0, 5], "range": "heatmap"}, "legend": None},
                "tooltip": [
                    tip("month_name", "Monat", "Month"),
                    tip("kind_name", "Sorte", "Kind"),
                    tip("n", "Einträge", "Entries"),
                ],
            },
        },
        {
            "transform": [{"aggregate": [{"op": "count", "as": "n"}], "groupby": ["month", "kind_order"]}],
            "mark": {"type": "text", "style": "label"},
            "encoding": {
                "text": {"field": "n"},
                "color": {"condition": {"test": "datum.n >= 3", "value": "@paper"}, "value": "@ink"},
            },
        },
        {
            "transform": [{"aggregate": [{"op": "count", "as": "n"}], "groupby": ["month"]}, {"calculate": "0", "as": "kind_order"}],
            "mark": {"type": "text", "style": "label", "fontSize": 13},
            "encoding": {"text": {"field": "n"}, "color": {"value": "@ink"}},
        },
    ],
}

c3 = {
    "height": {"step": 21},
    "encoding": {
        "y": {"field": {"de": "use_de", "en": "use_en"}, "type": "nominal", "sort": {"field": "remedies", "op": "max", "order": "descending"}, "axis": {"title": None, "labelLimit": 320, "labelFontSize": 12}},
        "x": {"field": "remedies", "type": "quantitative", "scale": {"domain": [0, 60]}, "axis": {"title": None, "values": [0, 20, 40, 60]}},
    },
    "layer": [
        {
            "mark": {"type": "bar", "height": {"band": 0.62}},
            "encoding": {
                "color": {"condition": {"test": "datum.focus == 1", "value": "@accent"}, "value": "@context"},
                "tooltip": [
                    tip({"de": "use_de", "en": "use_en"}, "Leiden", "Ailment"),
                    tip("remedies", "Zahl der Mittel", "Number of remedies"),
                    tip("examples", "Die ersten Mittel", "First remedies"),
                ],
            },
        },
        {
            "transform": [{"filter": "datum.remedies >= 10 || datum.remedies == 1"}],
            "mark": {"type": "text", "style": "label", "align": "left", "dx": 5},
            "encoding": {"text": {"field": "remedies"}},
        },
    ],
}

# ------------------------------------------------------------------ texts
sorted_types = type_counts.most_common()
summary_de = (
    f"Brückner verzeichnet Sagenorte, Jahresbräuche und Hausmittel des Landvolks. Acht Sagenlisten nennen {n_places} Orte, die meisten im Landesteil Gera. "
    f"Der Volkskalender gliedert sich in {n_calendar} Einträge, am dichtesten im April. Gegen äußere Übel kennt die Volksmedizin {external[4]} Mittel. "
    f"Mundartproben liegen aus {n_sample_places} Orten vor ({n_texts} Texte, rund {n_de(round(words_total, -2))} Wörter)."
)
summary_en = (
    f"Brückner records the legend sites, annual customs and household remedies of the country people. Eight lists of legends name {n_places} places, most of them in the district of Gera. "
    f"The folk calendar is divided into {n_calendar} entries, densest in April. For external ailments folk medicine knows {external[4]} remedies. "
    f"Dialect samples exist from {n_sample_places} places ({n_texts} texts, around {n_en(round(words_total, -2))} words)."
)
print("summary", words(summary_de), words(summary_en))

f1_de = (
    f"Die acht Sagenlisten nennen {n_places} Orte: {n_gera} im Landesteil Gera, {n_schleiz} in Schleiz und {n_lob} in Lobenstein-Ebersdorf. "
    f"Gera steht in {top[0]['lists']} Listen, Kraftsdorf in {top[1]['lists']}, Hohenleuben in {top[2]['lists']}."
)
f1_en = (
    f"The eight lists of legends name {n_places} places: {n_gera} in the district of Gera, {n_schleiz} in Schleiz and {n_lob} in Lobenstein-Ebersdorf. "
    f"Gera appears in {top[0]['lists']} lists, Kraftsdorf in {top[1]['lists']}, Hohenleuben in {top[2]['lists']}."
)
f2_de = (
    f"April hat mit {peak_month[1]} von {n_calendar} Einträgen die meisten (Gründonnerstag bis Ostern). Auf die zwölf Nächte vom 21. Dezember bis 6. Januar entfallen {len(twelve)}; "
    f"{weather_summer} der {len(weather)} Wetterregeln hängen an Tagen von Juni bis August."
)
f2_en = (
    f"April has the most entries, {peak_month[1]} of {n_calendar}. The twelve nights from 21 December to 6 January account for {len(twelve)}; "
    f"{weather_summer} of the {len(weather)} weather rules fall on days from June to August."
)
f3_de = (
    f"Für äußere Übel nennt Brückner {external[4]} Mittel, für Brustleiden {chest[4]}, für Magenleiden {stomach[4]}, für Epilepsie {epilepsy[4]}. "
    f"Daneben führt er {household} allgemeine Hausmittel auf; die größte Verehrung genieße die Johannisblume."
)
f3_en = (
    f"For external ailments Brückner names {external[4]} remedies, for chest complaints {chest[4]}, for stomach complaints {stomach[4]}, for epilepsy {epilepsy[4]}. "
    f"He also lists {household} general household remedies; the Johannisblume, he says, enjoys the greatest veneration."
)

title_c1 = bi(
    f"Sagenorte häufen sich im Norden um Gera; im Landesteil Lobenstein-Ebersdorf nennt Brückner nur {n_lob}",
    f"Legend sites cluster in the north around Gera; Brückner names only {n_lob} in the Lobenstein-Ebersdorf district",
)
march = month_counts[3]
title_c2 = bi(
    f"Der Volkskalender ist im April am dichtesten ({peak_month[1]} Einträge), im März am dünnsten ({march})",
    f"The folk calendar is densest in April ({peak_month[1]} entries) and thinnest in March ({march})",
)
assert march == min(month_counts.values())
title_c3 = bi(
    f"Gegen äußere Übel kennt das Volk {external[4]} Mittel, gegen Epilepsie nur eines",
    f"For external ailments the people know {external[4]} remedies, for epilepsy only one",
)
caption_c1 = bi(
    f"Orte in Brückners acht Sagenlisten (Wiedenheer, Reiter und Jäger, Hexen, Weiße Frau, Schätze, Klöster, Zauberer, Irrlichter); Größe: Zahl der Listen. {len(unmapped)} Orte ohne Koordinaten fehlen auf der Karte. S. 201–207.",
    f"Places in Brückner’s eight lists of legends (Wild Hunt, riders and huntsmen, witches, white lady, treasures, monasteries, sorcerers, will-o’-the-wisps); size: number of lists. {len(unmapped)} places without coordinates are not shown. Pp. 201–207.",
)
caption_c2 = bi(
    f"Einträge des Volkskalenders nach Monat und Sorte ({n_calendar} Einträge); bewegliche Feste stehen in dem Monat, unter dem Brückner sie behandelt. Obere Zeile: alle Einträge des Monats. S. 161, 185–193.",
    f"Entries of the folk calendar by month and kind ({n_calendar} entries); movable feasts are placed in the month under which Brückner treats them. Top row: all entries of the month. Pp. 161, 185–193.",
)
caption_c3 = bi(
    f"Zahl der Mittel, die Brückner für {len(ailment_rows) - 1} innere Leiden und für äußere Übel aufzählt; dazu {household} allgemeine Hausmittel (nicht gezeigt). Die ersten Mittel stehen in der Tabelle. S. 174 f.",
    f"Number of remedies that Brückner lists for {len(ailment_rows) - 1} internal ailments and for external ailments; plus {household} general household remedies (not shown). The first remedies are in the table. Pp. 174 f.",
)

method_de = (
    "Die Ortslisten der acht Sagentypen (S. 201–207) wurden aus der Prosa in einzelne Orte aufgelöst; jeder Ort ist über den Gazetteer der Ortskunde (Teil II) einem Landesteil zugeordnet und über den Ortsnamen mit den Koordinaten der Kartengrundlage verknüpft (GeoNames). Orte ohne Gazetteer-Eintrag stehen in der Tabelle, aber nicht auf der Karte. "
    "Der Volkskalender (S. 161, 185–193) wurde von Hand in Einträge gegliedert, je ein Brauch, eine Regel, eine Speise oder Arbeit an einem Tag oder Fest; die Einteilung in fünf Sorten ist eine Entscheidung des Bearbeiters. "
    "Die Mittel der Volksmedizin (S. 174 f.) wurden an Kommas und »und« in einzelne Nennungen zerlegt und den Leiden zugeordnet, für die Brückner sie aufzählt. "
    "Die Mundartproben (S. 145–151) sind als Tabelle beigefügt: 18 Texte aus 14 Orten, Umfang als Wortzahl nach Leerzeichen gezählt. In die Grafiken sind sie nicht eingegangen."
)
method_en = (
    "The place lists of the eight legend types (pp. 201–207) were resolved from the prose into single places; each place is assigned to a district through the gazetteer of the topography (Part II) and linked by name to the coordinates of the base map (GeoNames). Places without a gazetteer entry are in the table but not on the map. "
    "The folk calendar (pp. 161, 185–193) was divided by hand into entries, one custom, rule, dish or task per day or feast; the division into five kinds is the editor’s decision. "
    "The remedies of folk medicine (pp. 174 f.) were split at commas and “und” into single mentions and assigned to the ailments for which Brückner lists them. "
    "The dialect samples (pp. 145–151) are attached as a table: 18 texts from 14 places, length counted as words separated by spaces. They are not used in the charts."
)
print("method", words(method_de), words(method_en))

caveats = [
    bi(
        "Die Verteilung der Sagenorte spiegelt auch die Sammlung wider: Brückner stützt sich auf R. Eisel in Gera und eigene Wanderungen und nennt die Saalgegend ausdrücklich als noch nicht durchforscht. Aus der Karte lässt sich daher nicht schließen, dass es im Süden weniger Sagen gab.",
        "The distribution of legend sites also reflects the collecting: Brückner relies on R. Eisel in Gera and his own walks, and expressly calls the Saale region not yet explored. The map therefore does not show that there were fewer legends in the south.",
    ),
    bi(
        "Die Ortslisten sind aus Prosa gewonnen (»bei Pohlen«, »in der Wüstung Kämmera«): Gemeint sind teils Fluren, Gräben oder Wüstungen nahe dem genannten Ort. Mehrfachnennungen eines Ortes in einer Liste zählen einmal. Die Landesteile sind abgeleitet, nicht gedruckt.",
        "The place lists are taken from prose (“near Pohlen”, “in the deserted village Kämmera”): they partly mean fields, ditches or deserted villages near the named place. Repeated mentions of a place in one list count once. The districts are derived, not printed.",
    ),
    bi(
        "Die Einträge des Volkskalenders sind eine redaktionelle Gliederung, keine Zählung von Bräuchen: Brückner nennt weit mehr, mehrere Bräuche an einem Tag sind zusammengefasst, und die Dichte eines Monats hängt auch von der Ausführlichkeit seiner Darstellung ab. Tage ohne Druckangabe sind nach dem kirchlichen Kalender ergänzt.",
        "The entries of the folk calendar are an editorial division, not a count of customs: Brückner mentions many more, several customs on one day are combined, and the density of a month also depends on how fully he describes it. Days not printed are added from the church calendar.",
    ),
    bi(
        "Brückner zählt auf, was er für Hausmittel hält; er nennt weder Häufigkeit des Gebrauchs noch Wirksamkeit, und die Listen sind Auswahlen (»nur Einiges kann angemerkt werden«). Die Zerlegung der Prosa in einzelne Mittel ist redaktionell; die Namen sind historisch und nicht botanisch oder pharmazeutisch bestimmt.",
        "Brückner lists what he regards as household remedies; he gives neither frequency of use nor efficacy, and the lists are selections (“only some can be noted”). The splitting of the prose into single remedies is editorial; the names are historical and not identified botanically or pharmaceutically.",
    ),
]

feature = {
    "id": "sagen-brauch",
    "title": bi("Sagen, Bräuche und Volksmedizin", "Legends, customs and folk medicine"),
    "category": "culture",
    "section": "t1-2-8",
    "merges": MERGES,
    "sources": [{"page": "196", "block": "b2"}] + union_sources("kultur-sagenorte-nach-typ-und-landestheil", "kultur-volkskalender-bauernjahr", "gesundheit-volksmedizin-hausmittel-nach-leiden"),
    "summary": bi(summary_de, summary_en),
    "findings": [bi(f1_de, f1_en), bi(f2_de, f2_en), bi(f3_de, f3_en)],
    "method": bi(method_de, method_en),
    "caveats": caveats,
    "datasets": [places, calendar, ailments, remedies, samples, base_places, base_rivers],
    "charts": [
        {"id": "c1", "dataset": "legend_places", "extra_datasets": ["orte_basis", "fluesse_basis"], "title": title_c1, "caption": caption_c1, "vegalite": c1},
        {"id": "c2", "dataset": "calendar", "title": title_c2, "caption": caption_c2, "vegalite": c2},
        {"id": "c3", "dataset": "ailments", "title": title_c3, "caption": caption_c3, "vegalite": c3},
    ],
    "keywords": {
        "de": ["Sagen", "Volkskalender", "Bräuche", "Volksmedizin", "Hausmittel", "Mundart", "Hexen", "Wiedenheer", "Aberglaube", "Gera"],
        "en": ["legends", "folk calendar", "customs", "folk medicine", "household remedies", "dialect", "witches", "Wild Hunt", "superstition", "Gera"],
    },
    "related": ["gesundheit", "ortsnamen", "dorfleben", "phaenologie"],
    "generated_by": GENERATED_BY.format(k=len(MERGES)),
    "date": DATE,
}
ti = union_issues(*MERGES)
print("issues", ti)
if ti:
    feature["transcription_issues"] = ti
print(check_lengths(feature))
print(write_feature(feature))
