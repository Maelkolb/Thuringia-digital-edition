import copy
from common import *

ID = "viehzucht"
A1 = "viehzucht-bestand-1843-1867"
A2 = "orte-viehbestand-1867"

bestand = copy.deepcopy(dataset(A1, "bestand"))
je100 = copy.deepcopy(dataset(A1, "je100"))
arbeit = copy.deepcopy(dataset(A1, "arbeitstiere"))
stufen = copy.deepcopy(dataset(A1, "schafe_stufen"))
places_src = dataset(A2, "livestock_places")
prow = rows_as_dicts(places_src)

# ---------------------------------------------------------------- numbers
b = rows_as_dicts(bestand)
fu = [r for r in b if r["lt_nr"] == 4]


def count(species, year):
    return [r["anzahl"] for r in fu if r["tierart_de"] == species and r["jahr"] == year][0]


chg = {sp: (count(sp, 1867) / count(sp, 1843) - 1) * 100 for sp in ["Pferde", "Rinder", "Schafe", "Ziegen", "Schweine"]}
print({k: round(v, 2) for k, v in chg.items()})
j = rows_as_dicts(je100)


def j100(lt, sp, key):
    return [r for r in j if r["landestheil_de"] == lt and r["tierart_de"] == sp][0][key]


# ---------------------------------------------------------------- village table for the map
village_cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landesteil", "District", "string"),
    col("class_de", "Art des Ortes", "Kind of place", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("horses", "Pferde", "Horses", "integer", "Stück", note="leer = nicht genannt"),
    col("cattle", "Rinder", "Cattle", "integer", "Stück", note="leer = nicht genannt"),
    col("sheep", "Schafe", "Sheep", "integer", "Stück", note="leer = nicht genannt"),
    col("goats", "Ziegen", "Goats", "integer", "Stück", note="leer = nicht genannt"),
    col("leittier", "Zahlreichere Tierart (Schafe oder Rinder)", "More numerous species (sheep or cattle)", "string", derived=True,
        note="schafe = mehr Schafe als Rinder; rinder = gleich viele oder mehr Rinder; Städte ausgenommen"),
    col("tiere", "Schafe und Rinder zusammen", "Sheep and cattle together", "integer", "Stück", derived=True),
    col("lon", "Länge", "Longitude", "number", "°", True, "GeoNames"),
    col("lat", "Breite", "Latitude", "number", "°", True, "GeoNames"),
    col("page", "Seite", "Page", "string"),
    col("block", "Block", "Block", "string"),
]
village_rows = []
cnt = {lt: {"n": 0, "schafe": 0, "mapped": 0} for lt in DISTRICTS}
for r in prow:
    town = r["class_de"] == "Stadt"
    sheep, cattle = r["sheep"] or 0, r["cattle"] or 0
    lead = None if town else ("schafe" if sheep > cattle else "rinder")
    village_rows.append([
        r["place_id"], r["name"], r["landestheil"], r["class_de"], r["inhabitants"], r["horses"], r["cattle"], r["sheep"], r["goats"],
        lead, None if town else sheep + cattle, r["lon"], r["lat"], r["page"], r["block"],
    ])
    if not town:
        cnt[r["landestheil"]]["n"] += 1
        cnt[r["landestheil"]]["schafe"] += lead == "schafe"
        cnt[r["landestheil"]]["mapped"] += r["lon"] is not None
print(cnt)
vieh_orte = {
    "name": "vieh_orte",
    "title": bi("Viehbestand der Orte 1867 (aus den Ortsartikeln)", "Livestock of the places in 1867 (from the place articles)"),
    "columns": village_cols,
    "rows": village_rows,
    "source_refs": places_src["source_refs"],
}
n_villages = sum(c["n"] for c in cnt.values())
n_mapped = sum(c["mapped"] for c in cnt.values())
n_towns = len(prow) - n_villages

# ---------------------------------------------------------------- working animals
a = {r["landestheil_de"]: r for r in rows_as_dicts(arbeit)}
share_h = {lt: a[lt]["pferde_arbeit"] / (a[lt]["pferde_arbeit"] + a[lt]["rinder_arbeit"]) * 100 for lt in a}
print({k: round(v, 1) for k, v in share_h.items()})

d1 = lambda x: num_de(x, 1)
e1 = lambda x: num_en(x, 1)
d0 = lambda x: num_de(x, 0)
e0 = lambda x: num_en(x, 0)

sheep_1843, sheep_1867 = count("Schafe", 1843), count("Schafe", 1867)
summary = bi(
    f"Die Viehzählungen von 1843 bis 1867 zeigen eine Verschiebung: Die Zahl der Ziegen stieg um {d0(chg['Ziegen'])} Prozent, die der Schweine um {d0(chg['Schweine'])} und die der Pferde um {d0(chg['Pferde'])} Prozent, "
    f"die der Rinder nur um {d0(chg['Rinder'])} Prozent, während die der Schafe um {d0(-chg['Schafe'])} Prozent auf {num_de(sheep_1867)} zurückging. "
    f"Das Unterland hielt Schafe und Pferde, das Oberland Rinder und Ziegen.",
    f"The livestock counts from 1843 to 1867 show a shift: goats increased by {e0(chg['Ziegen'])} percent, pigs by {e0(chg['Schweine'])} and horses by {e0(chg['Pferde'])} percent, "
    f"cattle by only {e0(chg['Rinder'])} percent, while sheep fell by {e0(-chg['Schafe'])} percent to {num_en(sheep_1867)}. "
    f"The Unterland kept sheep and horses, the Oberland cattle and goats.",
)

findings = [
    bi(
        f"Die Zahl der Schafe sank um {d1(-chg['Schafe'])} Prozent von {num_de(sheep_1843)} auf {num_de(sheep_1867)}, die der Ziegen stieg um {d1(chg['Ziegen'])} Prozent von {num_de(count('Ziegen', 1843))} auf {num_de(count('Ziegen', 1867))}.",
        f"The number of sheep fell by {e1(-chg['Schafe'])} percent from {num_en(sheep_1843)} to {num_en(sheep_1867)}, that of goats rose by {e1(chg['Ziegen'])} percent from {num_en(count('Ziegen', 1843))} to {num_en(count('Ziegen', 1867))}.",
    ),
    bi(
        f"Je 100 Einwohner gingen Rinder ({d1(j100('Fürstentum', 'Rinder', 'je100_1843'))} auf {d1(j100('Fürstentum', 'Rinder', 'je100_1867'))}) und Schafe ({d1(j100('Fürstentum', 'Schafe', 'je100_1843'))} auf {d1(j100('Fürstentum', 'Schafe', 'je100_1867'))}) zurück; am stärksten sanken die Schafe in Gera ({d1(j100('Gera', 'Schafe', 'je100_1843'))} auf {d1(j100('Gera', 'Schafe', 'je100_1867'))}).",
        f"Per 100 inhabitants cattle ({e1(j100('Fürstentum', 'Rinder', 'je100_1843'))} to {e1(j100('Fürstentum', 'Rinder', 'je100_1867'))}) and sheep ({e1(j100('Fürstentum', 'Schafe', 'je100_1843'))} to {e1(j100('Fürstentum', 'Schafe', 'je100_1867'))}) declined; sheep fell most in Gera ({e1(j100('Gera', 'Schafe', 'je100_1843'))} to {e1(j100('Gera', 'Schafe', 'je100_1867'))}).",
    ),
    bi(
        f"Ziegen, nach Brückner das Vieh der Armen ohne Feldboden, nahmen am stärksten in Lobenstein-Ebersdorf zu: von {d1(j100('Lobenstein-Ebersdorf', 'Ziegen', 'je100_1843'))} auf {d1(j100('Lobenstein-Ebersdorf', 'Ziegen', 'je100_1867'))} je 100 Einwohner (Gera {d1(j100('Gera', 'Ziegen', 'je100_1867'))}).",
        f"Goats, in Brückner’s words the livestock of the poor without arable land, increased most in Lobenstein-Ebersdorf: from {e1(j100('Lobenstein-Ebersdorf', 'Ziegen', 'je100_1843'))} to {e1(j100('Lobenstein-Ebersdorf', 'Ziegen', 'je100_1867'))} per 100 inhabitants (Gera {e1(j100('Gera', 'Ziegen', 'je100_1867'))}).",
    ),
]

_row = lambda lt, y, st: [r["anzahl"] for r in rows_as_dicts(stufen) if r["landestheil_de"] == lt and r["jahr"] == y and r["stufe_de"] == st][0]
_fue_unv = _row("Fürstentum", 1861, "unveredelt")
# Fürstentum 1867 per Fürstentum row on p. 234: 13,293 unimproved sheep (not part of the dataset); implied Gera value:
_gera_implied = 13293 - 2604 - 4311
_total_alt = sheep_1867 - (7351 - _gera_implied)
assert _gera_implied == 6378 and _total_alt == 29144, (_gera_implied, _total_alt)
assert abs((_total_alt / sheep_1843 - 1) * 100 + 25.4) < 0.05
method = bi(
    "Die Zählergebnisse stammen aus den Tabellen auf S. 233 und 234 und der Vergleichstabelle S. 234 (Block b3), die Arbeitstiere von 1867 von S. 235. "
    "Die Zeitreihe zeigt nur die Jahre, in denen alle drei Landesteile gezählt wurden (1843, 1849, 1858, 1861, 1864, 1867); 1846, 1852 und 1855 sind nach Brückner unvollständig. "
    "»Pferde« umfasst Pferde und Füllen, »Rinder« Stiere, Ochsen, Kühe und Jungvieh, »Schafe« die drei Veredelungsstufen; die Werte des Fürstentums sind die Summen der Landesteile. "
    "Der Index setzt die Zählung von 1843 gleich 100. Die Karte beruht auf den Viehzahlen am Schluss der Ortsartikel (S. 418 bis 825), deren Orte mit Koordinaten aus GeoNames verbunden wurden; "
    "Orte ohne Koordinaten fehlen auf der Karte. Städte sind ausgenommen, weil dort Vieh von Gütern und Haushalten gemischt ist. Ein Dorf zählt als Schafdorf, wenn es mehr Schafe als Rinder hat.",
    "The count results come from the tables on pp. 233 and 234 and the comparison table on p. 234 (block b3), the working animals of 1867 from p. 235. "
    "The time series shows only the years in which all three districts were counted (1843, 1849, 1858, 1861, 1864, 1867); 1846, 1852 and 1855 are incomplete according to Brückner. "
    "“Horses” includes horses and foals, “cattle” bulls, oxen, cows and young cattle, “sheep” the three degrees of improvement; the figures for the principality are the sums of the districts. "
    "The index sets the count of 1843 to 100. The map is based on the livestock figures at the end of the place articles (pp. 418 to 825), whose places were joined to coordinates from GeoNames; "
    "places without coordinates are missing from the map. Towns are excluded because livestock of estates and households is mixed there. A village counts as a sheep village if it has more sheep than cattle.",
)

caveats = [
    bi(
        "Die Vorlage ist nicht in allen Zahlen stimmig. Für Gera 1867 steht bei den unveredelten Schafen 7351, dieselbe Zahl wie bei den Schweinen; die Zeile des Fürstentums (13 293) verlangt 6378. "
        "Dann gäbe es 29 144 statt 30 117 Schafe, ein Rückgang von 25,4 statt 22,9 Prozent. Gezeigt sind die gedruckten Zahlen.",
        "The source is not consistent in every figure. For Gera in 1867 the unimproved sheep are printed as 7351, the same number as for pigs; the row for the principality (13,293) requires 6378. "
        "That would give 29,144 instead of 30,117 sheep, a fall of 25.4 instead of 22.9 percent. The printed figures are shown.",
    ),
    bi(
        "Die Zählungen von 1846, 1852 und 1855 sind unvollständig und fehlen in der Reihe. 1843 ist Lobenstein-Ebersdorf nur summarisch gezählt, Alter und Veredelung gibt es erst ab 1849.",
        "The counts of 1846, 1852 and 1855 are incomplete and missing from the series. In 1843 Lobenstein-Ebersdorf was counted only in total; age and improvement are given from 1849 on.",
    ),
    bi(
        "Die Dorfzahlen sind Zählergebnisse von 1867. Manche Schafe und Pferde gehören Gütern (z. B. Zschippern, Laasen), das verzerrt die Aussage über einzelne Dörfer. Ob ein Rind und ein Schaf als Vergleich taugen, ist eine Setzung dieser Auswertung.",
        "The village figures are results of the 1867 count. Some sheep and horses belong to estates (for example Zschippern, Laasen), which distorts the picture for individual villages. Comparing a head of cattle with a sheep is a convention of this analysis.",
    ),
]

transcription_issues = [
    {
        "page": "234", "block": "b3", "cell": "r5c3", "transcribed": "1774", "facsimile": "1774", "checked_facsimile": True,
        "note": "Gera 1867, Pferde: Druckfehler für 1874 (Einzeltabelle: 1731 + 143 = 1874; die Summe 2689 des Fürstentums passt zu 1874). Die Auswertung rechnet mit 1874. / Printing error for 1874; the analysis uses 1874.",
    },
    {
        "page": "233", "block": "b4", "cell": "r13c10", "transcribed": "7351", "facsimile": "7351", "checked_facsimile": True,
        "note": "Gera 1867, unveredelte Schafe: so gedruckt, aber identisch mit der Zahl der Schweine (r13c12); die Zeile des Fürstentums (S. 234, 13 293) verlangt 6378. Die Auswertung übernimmt den Druck. / Printed so, identical to the pig count; the principality row requires 6378.",
    },
]

# ---------------------------------------------------------------- charts
SPECIES_DOMAIN = ["Schafe", "Ziegen", "Schweine", "Rinder", "Pferde"]
SPECIES_RANGE = ["@accent2", "@ink2", "@muted", "@accent3", "@accent"]

c1 = {
    "id": "c1",
    "dataset": "bestand",
    "title": bi(
        "Ziegen und Schweine nahmen von 1843 bis 1867 stark zu, die Schafe gingen zurück",
        "Goats and pigs increased sharply from 1843 to 1867, while sheep declined",
    ),
    "caption": bi(
        "Viehbestand des Fürstentums bei den Zählungen 1843 bis 1867, 1843 gleich 100; ohne die unvollständigen Zählungen 1846, 1852 und 1855. Zahl am Linienende: Veränderung gegenüber 1843. Quelle: S. 233 bis 234.",
        "Livestock of the principality at the counts of 1843 to 1867, 1843 = 100; without the incomplete counts of 1846, 1852 and 1855. Number at the line end: change since 1843. Source: pp. 233 to 234.",
    ),
    "vegalite": {
        "height": 320,
        "transform": [
            {"filter": "datum.lt_nr == 4"},
            {"window": [{"op": "first_value", "field": "anzahl", "as": "basis"}], "groupby": ["tierart_de"], "sort": [{"field": "jahr"}], "frame": [None, None]},
            {"calculate": "datum.anzahl / datum.basis * 100", "as": "index"},
        ],
        "encoding": {
            "x": {
                "field": "jahr", "type": "quantitative",
                "scale": {"domain": [1843, 1878], "nice": False},
                "axis": {"values": [1843, 1849, 1858, 1861, 1864, 1867], "format": "d", "title": None},
            },
            "y": {
                "field": "index", "type": "quantitative",
                "scale": {"domain": [65, 215]},
                "axis": {"title": {"de": "Bestand, 1843 = 100", "en": "Count, 1843 = 100"}, "values": [75, 100, 125, 150, 175, 200]},
            },
            "color": {"field": "tierart_de", "type": "nominal", "legend": None, "scale": {"domain": SPECIES_DOMAIN, "range": SPECIES_RANGE}},
        },
        "layer": [
            {"mark": {"type": "rule", "strokeDash": [3, 3], "color": "@muted"}, "encoding": {"y": {"datum": 100}, "x": None, "color": None}},
            {"mark": {"type": "line", "strokeWidth": 2.5}},
            {
                "mark": {"type": "point", "filled": True, "size": 36},
                "encoding": {
                    "tooltip": [
                        {"field": {"de": "tierart_de", "en": "tierart_en"}, "type": "nominal", "title": bi("Tierart", "Species")},
                        tooltip("jahr", "Zählung", "Census", "d"),
                        tooltip("anzahl", "Tiere", "Animals", ",d"),
                        tooltip("index", "1843 = 100", "1843 = 100", ".0f"),
                    ],
                },
            },
            {
                "transform": [
                    {"filter": "datum.jahr == 1867"},
                    {"calculate": {"de": "datum.tierart_de + ' ' + format(datum.index - 100, '+.0f') + ' %'", "en": "datum.tierart_en + ' ' + format(datum.index - 100, '+.0f') + ' %'"}, "as": "endlabel"},
                ],
                "mark": {"type": "text", "align": "left", "dx": 9, "style": "label"},
                "encoding": {"text": {"field": "endlabel"}, "color": None},
            },
        ],
    },
}

BASE_LABELS = ["Gera", "Schleiz", "Lobenstein", "Hirschberg", "Saalburg", "Tanna", "Ebersdorf", "Hohenleuben"]
lon = {"field": "lon", "type": "quantitative"}
lat = {"field": "lat", "type": "quantitative"}
town_filter = "indexof(" + json.dumps(["Gera", "Schleiz", "Lobenstein", "Hirschberg", "Saalburg", "Tanna", "Hohenleuben"], ensure_ascii=False).replace('"', "'") + ", datum.ort) >= 0"
c2 = {
    "id": "c2",
    "dataset": "vieh_orte",
    "extra_datasets": ["orte_basis", "fluesse_basis"],
    "title": bi(
        "Im Unterland hielten die meisten Dörfer mehr Schafe als Rinder, im Oberland meist umgekehrt",
        "In the Unterland most villages kept more sheep than cattle, in the Oberland mostly the reverse",
    ),
    "caption": bi(
        f"Dörfer und Marktflecken nach der zahlreicheren Tierart 1867, Größe nach Schafen und Rindern zusammen; ohne die sechs Städte, {n_mapped} von {n_villages} Orten haben Koordinaten. Gera: {cnt['Gera']['schafe']} von {cnt['Gera']['n']} mit mehr Schafen, Schleiz {cnt['Schleiz']['schafe']} von {cnt['Schleiz']['n']}, Lobenstein-Ebersdorf {cnt['Lobenstein-Ebersdorf']['schafe']} von {cnt['Lobenstein-Ebersdorf']['n']}. Quelle: Ortsartikel.",
        f"Villages and market towns by the more numerous species in 1867, size by sheep and cattle together; without the six towns, {n_mapped} of {n_villages} places have coordinates. Gera: {cnt['Gera']['schafe']} of {cnt['Gera']['n']} with more sheep, Schleiz {cnt['Schleiz']['schafe']} of {cnt['Schleiz']['n']}, Lobenstein-Ebersdorf {cnt['Lobenstein-Ebersdorf']['schafe']} of {cnt['Lobenstein-Ebersdorf']['n']}. Source: place articles.",
    ),
    "vegalite": {
        "height": 560,
        "projection": {"type": "mercator"},
        "layer": [
            {
                "data": {"name": "fluesse_basis"},
                "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2},
                "encoding": {"longitude": lon, "latitude": lat, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}},
            },
            {
                "data": {"name": "orte_basis"},
                "mark": {"type": "circle", "size": 10, "color": "@land"},
                "encoding": {"longitude": lon, "latitude": lat},
            },
            {
                "transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat) && isValid(datum.leittier)"}],
                "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85},
                "encoding": {
                    "longitude": lon, "latitude": lat,
                    "size": {"field": "tiere", "type": "quantitative", "scale": {"type": "sqrt", "range": [6, 210]}, "legend": None},
                    "color": {
                        "field": "leittier", "type": "nominal",
                        "scale": {"domain": ["schafe", "rinder"], "range": ["@accent2", "@accent3"]},
                        "legend": {
                            "title": None, "orient": "top-left", "direction": "vertical",
                            "labelExpr": {"de": "datum.value == 'schafe' ? 'mehr Schafe als Rinder' : 'mehr Rinder als Schafe'", "en": "datum.value == 'schafe' ? 'more sheep than cattle' : 'more cattle than sheep'"},
                        },
                    },
                    "tooltip": [
                        tooltip("name", "Ort", "Place"),
                        tooltip("landestheil", "Landesteil", "District"),
                        tooltip("inhabitants", "Einwohner", "Inhabitants", ",d"),
                        tooltip("cattle", "Rinder", "Cattle", ",d"),
                        tooltip("sheep", "Schafe", "Sheep", ",d"),
                        tooltip("goats", "Ziegen", "Goats", ",d"),
                        tooltip("horses", "Pferde", "Horses", ",d"),
                    ],
                },
            },
            {
                "data": {"name": "orte_basis"},
                "transform": [{"filter": town_filter}],
                "mark": {"type": "text", "style": "place-halo", "dy": -11},
                "encoding": {"longitude": lon, "latitude": lat, "text": {"field": "ort"}},
            },
            {
                "data": {"name": "orte_basis"},
                "transform": [{"filter": town_filter}],
                "mark": {"type": "text", "style": "place-label", "dy": -11},
                "encoding": {"longitude": lon, "latitude": lat, "text": {"field": "ort"}},
            },
        ],
    },
}

c3 = {
    "id": "c3",
    "dataset": "arbeitstiere",
    "title": bi(
        "Im Unterland zogen Pferde und Rinder je etwa zur Hälfte, im Oberland fast nur Rinder",
        "In the Unterland horses and cattle worked in equal numbers, in the Oberland almost only cattle",
    ),
    "caption": bi(
        "Zur Arbeit herangezogene Pferde und Rinder 1867 je Landesteil, in Prozent aller Arbeitstiere; die Zahlen in den Balken sind Stück. Quelle: S. 235.",
        "Horses and cattle used for work in 1867 by district, as percent of all working animals; the numbers in the bars are head. Source: p. 235.",
    ),
    "vegalite": {
        "height": {"step": 52},
        "transform": [
            {"fold": ["pferde_arbeit", "rinder_arbeit"], "as": ["art", "stueck"]},
            {"calculate": "datum.art == 'pferde_arbeit' ? 'pferde' : 'rinder'", "as": "tierart"},
            {"calculate": "datum.art == 'pferde_arbeit' ? 1 : 2", "as": "tierart_nr"},
            {"stack": "stueck", "groupby": ["landestheil_de"], "sort": [{"field": "tierart_nr", "order": "ascending"}], "offset": "normalize", "as": ["x0", "x1"]},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
            {"calculate": {
                "de": "datum.landestheil_de == 'Gera' ? (datum.tierart == 'pferde' ? 'Pferde ' : 'Rinder ') + format(datum.stueck, ',d') : format(datum.stueck, ',d')",
                "en": "datum.landestheil_de == 'Gera' ? (datum.tierart == 'pferde' ? 'Horses ' : 'Cattle ') + format(datum.stueck, ',d') : format(datum.stueck, ',d')"},
             "as": "segment_label"},
        ],
        "encoding": {
            "y": {
                "field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal",
                "sort": {"field": "lt_nr", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelFontSize": 12, "labelLimit": 260},
            },
        },
        "layer": [
            {
                "mark": {"type": "bar", "height": {"band": 0.72}},
                "encoding": {
                    "x": {
                        "field": "x0", "type": "quantitative", "scale": {"domain": [0, 1]},
                        "axis": {"title": {"de": "Anteil an den Arbeitstieren", "en": "Share of working animals"}, "format": "%"},
                    },
                    "x2": {"field": "x1"},
                    "color": {
                        "field": "tierart", "type": "nominal", "legend": None,
                        "scale": {"domain": ["pferde", "rinder"], "range": ["@accent", "@accent3"]},
                    },
                    "tooltip": [
                        tooltip("landestheil_de", "Landesteil", "District"),
                        {"field": "segment_label", "type": "nominal", "title": bi("Arbeitstiere", "Working animals")},
                    ],
                },
            },
            {
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative"},
                    "text": {"field": "segment_label", "type": "nominal"},
                    "color": {"condition": {"test": "datum.tierart == 'pferde'", "value": "@paper"}, "value": "@ink"},
                },
            },
        ],
    },
}

datasets = [bestand, vieh_orte, arbeit, je100, stufen, shared_dataset("orte_basis"), shared_dataset("fluesse_basis")]

feature = {
    "id": ID,
    "title": bi("Viehbestand 1843 bis 1867", "Livestock, 1843 to 1867"),
    "category": "livestock",
    "section": "t1-3-3",
    "merges": [A1, A2],
    "sources": [
        {"page": "233", "block": "b4"}, {"page": "234", "block": "b1"}, {"page": "234", "block": "b3"},
        {"page": "235", "block": "b3"}, {"page": "233", "block": "b2"},
    ],
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "transcription_issues": transcription_issues,
    "datasets": datasets,
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Viehzucht", "Viehzählung", "Schafe", "Ziegen", "Rinder", "Pferde", "Schweine", "Arbeitstiere", "Veredelung"],
        "en": ["livestock", "cattle census", "sheep", "goats", "cattle", "horses", "pigs", "working animals", "sheep improvement"],
    },
    "related": ["landwirtschaft", "dorfleben", "siedlung-wohnen", "tierwelt"],
    "generated_by": "Claude Sonnet 5.5 (Agent F5), aus 2 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    for k in ["title", "summary"]:
        for lang in ["de", "en"]:
            print(k, lang, words(feature[k][lang]))
    write_feature(feature)
    validate(ID)
