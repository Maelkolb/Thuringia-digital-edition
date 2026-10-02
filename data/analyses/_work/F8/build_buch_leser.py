from f8common import *
import math
from collections import Counter, defaultdict

sub = arch("subskribenten-leserschaft-1870")
cor = arch("zusaetze-berichtigungen-1870")
mas = arch("masse-gewichte-umrechnung-1869")

subscribers = dataset(sub, "subscribers")
by_place = dataset(sub, "by_place")
by_group = dataset(sub, "by_group")
corrections = dataset(cor, "corrections")
units = dataset(mas, "units")

SUB = rows(subscribers)
BP = rows(by_place)
BG = rows(by_group)
COR = rows(corrections)
UN = rows(units)

# ------------------------------------------------------------ coordinates for the places in the principality
base = rows(base_places())
bmap = {r["ort"]: r for r in base}
reg = {e["id"]: e for e in load(os.path.join(ROOT, "data", "entities", "registry.json"))["entities"]}
REGISTRY_FALLBACK = {"Heinrichsruhe": "place:heinrichsruhe", "Oertelsbruch": "place:oertelsbruch"}
lon_vals, lat_vals, note_src = [], [], []
for r in BP:
    lo = la = None
    if r["region"] != "outside":
        if r["place"] in bmap:
            lo, la = bmap[r["place"]]["lon"], bmap[r["place"]]["lat"]
        elif r["place"] in REGISTRY_FALLBACK and reg[REGISTRY_FALLBACK[r["place"]]].get("coords"):
            la, lo = reg[REGISTRY_FALLBACK[r["place"]]]["coords"]
    lon_vals.append(lo)
    lat_vals.append(la)
add_column(by_place, "lon", "Länge", "Longitude", lon_vals, typ="number", unit="° O", note="GeoNames (Kartengrundlage orte_basis, zwei Orte aus dem Register der Entitäten); nur Orte im Fürstentum")
add_column(by_place, "lat", "Breite", "Latitude", lat_vals, typ="number", unit="° N", note="GeoNames (Kartengrundlage orte_basis, zwei Orte aus dem Register der Entitäten); nur Orte im Fürstentum")
BP = rows(by_place)

GROUP_NAMES = {
    "officials": ("Beamte, Juristen", "Officials, jurists"),
    "teachers": ("Lehrer", "Teachers"),
    "trade": ("Kaufleute, Gewerbe", "Trade, industry"),
    "booksellers": ("Buchhandlungen", "Booksellers"),
    "institutions": ("Behörden, Vereine", "Authorities, societies"),
    "clergy": ("Geistliche", "Clergy"),
    "forestry_mining": ("Forst, Bergbau", "Forestry, mining"),
    "others": ("übrige", "Others"),
    "farmers": ("Landwirte", "Farmers"),
    "court": ("Hof", "Court"),
    "craftsmen": ("Handwerker", "Craftsmen"),
}
add_column(by_group, "group_de", "Gruppe (deutsch)", "Group (German)", [GROUP_NAMES[r["group"]][0] for r in BG], typ="string")
add_column(by_group, "group_en", "Gruppe (englisch)", "Group (English)", [GROUP_NAMES[r["group"]][1] for r in BG], typ="string")
STATE = ["officials", "teachers", "clergy", "forestry_mining", "court"]
add_column(by_group, "service", "Staats-, Schul- oder Kirchendienst", "State, school or church service",
           [1 if r["group"] in STATE else 0 for r in BG], typ="integer", note="1 = Beamte, Lehrer, Geistliche, Forst/Berg, Hof")
BG = rows(by_group)

# ------------------------------------------------------------ chapters of the book (table of contents, pp. VII-VIII)
CH = [
    ("t1-1", "Die Natur des Landes", "The nature of the land", "Natur", "Nature", 3, 90),
    ("t1-2", "Das Volk", "The people", "Volk", "People", 91, 207),
    ("t1-3", "Die Volksbetriebsamkeit", "Economic activity", "Gewerbe", "Economy", 208, 262),
    ("t1-4", "Der Staat", "The state", "Staat", "State", 262, 310),
    ("t1-5", "Geschichte des Landes und seines Fürstenhauses", "History of the land and its princely house", "Geschichte", "History", 311, 403),
    ("t2-1", "Der Landestheil Gera", "The district of Gera", "Gera", "Gera", 407, 569),
    ("t2-2", "Der Landestheil Schleiz", "The district of Schleiz", "Schleiz", "Schleiz", 570, 705),
    ("t2-3", "Der Landestheil Lobenstein-Ebersdorf", "The district of Lobenstein-Ebersdorf", "Lobenstein", "Lobenstein", 706, 825),
]
chapters = {
    "name": "chapters",
    "title": bi("Kapitel des Buchs nach der Inhaltsübersicht", "Chapters of the book according to the table of contents"),
    "columns": [
        {"name": "chapter", "label": bi("Kapitel (Code)", "Chapter (code)"), "type": "string", "unit": None, "derived": True},
        {"name": "chapter_de", "label": bi("Kapitel", "Chapter"), "type": "string", "unit": None},
        {"name": "chapter_en", "label": bi("Kapitel (englisch)", "Chapter (English)"), "type": "string", "unit": None, "derived": True},
        {"name": "short_de", "label": bi("Kurzname", "Short name"), "type": "string", "unit": None, "derived": True},
        {"name": "short_en", "label": bi("Kurzname (englisch)", "Short name (English)"), "type": "string", "unit": None, "derived": True},
        {"name": "start_page", "label": bi("Erste Seite", "First page"), "type": "integer", "unit": None},
        {"name": "end_page", "label": bi("Letzte Seite", "Last page"), "type": "integer", "unit": None},
        {"name": "band", "label": bi("Streifen (2 = Natur des Landes, sonst abwechselnd 0 und 1)", "Band (2 = nature of the land, otherwise alternating 0 and 1)"), "type": "integer", "unit": None, "derived": True},
    ],
    "rows": [[c[0], c[1], c[2], c[3], c[4], c[5], c[6], 2 if i == 0 else i % 2] for i, c in enumerate(CH)],
    "source_refs": [
        {"page": "VII", "block": "b4", "rows": "r2-r10"},
        {"page": "VII", "block": "b6", "rows": "r1-r8"},
        {"page": "VII", "block": "b8", "rows": "r1-r7"},
        {"page": "VIII", "block": "b2", "rows": "r2-r11"},
        {"page": "VIII", "block": "b3", "rows": "r1"},
        {"page": "VIII", "block": "b5", "rows": "r1-r3"},
    ],
}

# ------------------------------------------------------------ numbers
n_entries = len(SUB)
n_copies = sum(r["copies"] for r in SUB)
inside = [r for r in BP if r["region"] != "outside"]
n_in = sum(r["entries"] for r in inside)
c_in = sum(r["copies"] for r in inside)
n_out = n_entries - n_in
c_out = n_copies - c_in
top3 = {p: [r for r in BP if r["place"] == p][0]["entries"] for p in ("Gera", "Schleiz", "Lobenstein")}
n_top3 = sum(top3.values())
c_top3 = sum([r for r in BP if r["place"] == p][0]["copies"] for p in top3)
untermhaus = [r for r in BP if r["place"] == "Untermhaus"][0]["entries"]
teich = max(SUB, key=lambda r: r["copies"])
print("entries", n_entries, n_copies, "inside", n_in, c_in, "outside", n_out, c_out, "top3", top3, n_top3, c_top3, "teich", teich["name_printed"], teich["copies"])
state_n = sum(r["entries"] for r in BG if r["group"] in STATE)
land_craft = sum(r["entries"] for r in BG if r["group"] in ("farmers", "craftsmen"))
out_books = sum(1 for r in SUB if r["region"] == "outside" and r["group"] == "booksellers")
print("state", state_n, round(100 * state_n / n_entries, 1), "farm+craft", land_craft, round(100 * land_craft / n_entries, 1), "outside booksellers", out_books)
missing_place_entries = sum(r["entries"] for r in inside if r["lon"] is None)
missing_places = sum(1 for r in inside if r["lon"] is None)
print("missing on map", missing_places, missing_place_entries)

n_cor = len(COR)
kc = Counter(r["kind"] for r in COR)
nat = [r for r in COR if r["chapter"] == "t1-1"]
nat_lo, nat_hi = min(r["target_page"] for r in nat), max(r["target_page"] for r in nat)
n_upd = kc["update"]
print("corrections", n_cor, kc, len(nat), nat_lo, nat_hi, round(100 * len(nat) / n_cor, 1))
part1 = sum(1 for r in COR if r["chapter"].startswith("t1"))
print("part1", part1, n_cor - part1)

U = {(r["unit"], r["district"]): r for r in UN}
spread = {}
for u in ("Kanne", "Eimer", "Elle"):
    vals = [r["value_base"] for r in UN if r["unit"] == u]
    spread[u] = (max(vals) / min(vals) - 1) * 100
    print(u, [(r["district"], r["value_base"]) for r in UN if r["unit"] == u], round(spread[u], 1))
kmax = max((r for r in UN if r["unit"] == "Kanne"), key=lambda r: r["value_base"])
kmin = min((r for r in UN if r["unit"] == "Kanne"), key=lambda r: r["value_base"])
print(kmax["district"], kmin["district"])

# ------------------------------------------------------------ chart 1: map + professions
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}


def lab_layers(names, dx, dy, align):
    flt = "indexof(" + json.dumps(names, ensure_ascii=False) + ", datum.place) >= 0"
    out = []
    for style in ("place-halo", "place-label"):
        out.append({
            "transform": [{"filter": flt}],
            "mark": {"type": "text", "style": style, "dx": dx, "dy": dy, "align": align},
            "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}},
        })
    return out


group_expr = lambda i: "{" + ",".join(f"'{k}':'{v[i]}'" for k, v in GROUP_NAMES.items()) + "}[datum.value]"

map_panel = {
    "data": {"name": "by_place"},
    "width": 340,
    "height": 470,
    "projection": {"type": "mercator"},
    "layer": [
        {
            "data": {"name": "fluesse_basis"},
            "mark": {"type": "line", "color": "@river", "strokeWidth": 1.1, "interpolate": "monotone"},
            "encoding": {"longitude": LON, "latitude": LAT, "detail": {"field": "abschnitt"}, "order": {"field": "folge"}},
        },
        {
            "data": {"name": "orte_basis"},
            "mark": {"type": "circle", "size": 8, "color": "@land", "opacity": 1},
            "encoding": {"longitude": LON, "latitude": LAT},
        },
        {
            "transform": [{"filter": "isValid(datum.lon) && isValid(datum.lat)"}],
            "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85, "color": "@accent2"},
            "encoding": {
                "longitude": LON,
                "latitude": LAT,
                "size": {"field": "entries", "type": "quantitative", "scale": {"type": "sqrt", "range": [14, 1700], "domain": [0, 56]},
                         "legend": {"title": bi("Subskribenten", "Subscribers"), "values": [1, 10, 50], "orient": "top-left", "direction": "vertical",
                                    "symbolFillColor": "@accent2", "symbolStrokeColor": "@paper", "symbolOpacity": 0.85}},
                "tooltip": [
                    {"field": "place", "title": bi("Ort", "Place")},
                    {"field": "entries", "title": bi("Einträge", "Entries")},
                    {"field": "copies", "title": bi("Exemplare", "Copies")},
                ],
            },
        },
        *lab_layers(["Gera", "Schleiz", "Lobenstein"], 11, 0, "left"),
        *lab_layers(["Ebersdorf", "Hohenleuben"], -8, -9, "right"),
        {
            "transform": [{"filter": "datum.place == 'Gera'"}],
            "mark": {"type": "text", "style": "annotation", "align": "left", "baseline": "top"},
            "encoding": {"longitude": {"datum": 11.5}, "latitude": {"datum": 50.8},
                         "text": {"value": bi(f"Nicht abgebildet: {n_out} Einträge von außerhalb", f"Not shown: {n_out} entries from outside")}},
        },
    ],
}

bar_panel = {
    "data": {"name": "by_group"},
    "width": 240,
    "height": {"step": 25},
    "encoding": {
        "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": {"field": "order", "op": "min"},
              "axis": {"title": None, "ticks": False, "domain": False, "labelLimit": 400}},
        "x": {"field": "entries", "type": "quantitative", "scale": {"domain": [0, 50]}, "axis": None},
    },
    "layer": [
        {
            "mark": {"type": "bar", "size": 14, "cornerRadiusEnd": 2},
            "encoding": {
                "color": {"condition": {"test": "datum.service == 1", "value": "@accent"}, "value": "@context"},
                "tooltip": [
                    {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                    {"field": "entries", "title": bi("Einträge", "Entries")},
                    {"field": "copies", "title": bi("Exemplare", "Copies")},
                ],
            },
        },
        {
            "transform": [{"filter": "datum.group == 'craftsmen'"},
                          {"calculate": {"de": "['Blau: Staats-, Schul-', 'und Kirchendienst (' + " + str(state_n) + " + ')']",
                                         "en": "['Blue: state, school', 'and church service (' + " + str(state_n) + " + ')']"}, "as": "note"},
                          {"calculate": "16", "as": "nx"}],
            "mark": {"type": "text", "align": "left", "baseline": "middle", "style": "label", "color": "@accent", "lineHeight": 14},
            "encoding": {"x": {"field": "nx", "type": "quantitative"}, "text": {"field": "note"}},
        },
        {
            "transform": [{"calculate": {"de": "datum.copies > datum.entries + 4 ? datum.entries + ' (' + datum.copies + ' Expl.)' : '' + datum.entries",
                                         "en": "datum.copies > datum.entries + 4 ? datum.entries + ' (' + datum.copies + ' copies)' : '' + datum.entries"}, "as": "lab"}],
            "mark": {"type": "text", "align": "left", "dx": 5, "style": "label"},
            "encoding": {"text": {"field": "lab"}},
        },
    ],
}

c1 = {
    "id": "c1",
    "dataset": "by_place",
    "extra_datasets": ["by_group", "orte_basis", "fluesse_basis"],
    "title": bi(
        "Subskribenten: fast die Hälfte aus drei Städten, über die Hälfte im Staats-, Schul- oder Kirchendienst",
        "Subscribers: almost half from three towns, more than half in state, school or church service",
    ),
    "caption": bi(
        f"Links die Orte der {n_in} Subskribenten im Fürstentum (Fläche: Zahl der Einträge), rechts alle {n_entries} nach Beruf; blau: Staats-, Schul-, Kirchendienst. In Klammern die Exemplare, wo sie stark abweichen. Quelle: S. 835–840.",
        f"Left the places of the {n_in} subscribers within the principality (area: number of entries), right all {n_entries} by occupation; blue: state, school and church service. Copies in brackets where they differ strongly. Source: pp. 835–840.",
    ),
    "vegalite": {"hconcat": [map_panel, bar_panel], "spacing": 18, "resolve": {"scale": {"size": "independent"}}},
}

# ------------------------------------------------------------ chart 2: corrections along the book
BIN = 10
c2 = {
    "id": "c2",
    "dataset": "corrections",
    "extra_datasets": ["chapters"],
    "title": bi(
        f"Fast die Hälfte der {n_cor} Zusätze und Berichtigungen betrifft die Natur des Landes ({nat_hi - nat_lo + 1} Seiten)",
        f"Almost half of the {n_cor} addenda and corrigenda concern the nature of the land ({nat_hi - nat_lo + 1} pages)",
    ),
    "caption": bi(
        f"Jeder Punkt ist ein Zusatz oder eine Berichtigung aus Brückners Anhang, nach der Seite im Buch geordnet (je {BIN} Seiten übereinander); Streifen: Kapitel. Blau: Natur des Landes. Quelle: S. 830–834.",
        f"Each dot is an addendum or correction from Brückner’s appendix, ordered by page in the book ({BIN} pages per stack); bands: chapters. Blue: nature of the land. Source: pp. 830–834.",
    ),
    "vegalite": {
        "height": 300,
        "layer": [
            {
                "data": {"name": "chapters"},
                "mark": {"type": "rect"},
                "encoding": {
                    "x": {"field": "start_page", "type": "quantitative", "scale": {"domain": [0, 830], "nice": False},
                          "axis": {"title": bi("Seite des Buchs", "Page of the book"), "values": [3, 91, 208, 311, 407, 570, 706, 825], "format": "d", "grid": False, "domain": True}},
                    "x2": {"field": "end_page"},
                    "color": {"condition": [{"test": "datum.band == 2", "value": "@accent"}, {"test": "datum.band == 1", "value": "@land"}], "value": "@paper"},
                    "opacity": {"condition": {"test": "datum.band == 2", "value": 0.16}, "value": 0.6},
                },
            },
            {
                "data": {"name": "chapters"},
                "transform": [{"calculate": "(datum.start_page + datum.end_page) / 2", "as": "mid"}],
                "mark": {"type": "text", "style": "annotation", "baseline": "top", "dy": 4},
                "encoding": {
                    "x": {"field": "mid", "type": "quantitative", "scale": {"domain": [0, 830], "nice": False}},
                    "y": {"datum": 17.5, "type": "quantitative", "scale": {"domain": [0, 17.5]}, "axis": None},
                    "text": {"field": {"de": "short_de", "en": "short_en"}},
                },
            },
            {
                "transform": [
                    {"calculate": f"floor(datum.target_page / {BIN}) * {BIN} + {BIN // 2}", "as": "bin"},
                    {"window": [{"op": "row_number", "as": "rn"}], "groupby": ["bin"], "sort": [{"field": "target_page"}, {"field": "corr_id"}]},
                ],
                "mark": {"type": "circle", "size": 46, "stroke": "@paper", "strokeWidth": 0.8, "opacity": 1},
                "encoding": {
                    "x": {"field": "bin", "type": "quantitative", "scale": {"domain": [0, 830], "nice": False}},
                    "y": {"field": "rn", "type": "quantitative", "scale": {"domain": [0, 17.5]}, "axis": None},
                    "color": {"condition": {"test": "datum.chapter == 't1-1'", "value": "@accent"}, "value": "@muted"},
                    "tooltip": [
                        {"field": "target_page", "title": bi("Seite", "Page"), "format": "d"},
                        {"field": "line_ref", "title": bi("Zeile", "Line")},
                        {"field": "kind", "title": bi("Art", "Kind")},
                        {"field": "text_printed", "title": bi("Wortlaut", "Wording")},
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.corr_id == 'K001'"}, {"calculate": "90", "as": "xa"}, {"calculate": "13.5", "as": "ya"}],
                "mark": {"type": "text", "style": "label", "align": "left", "dx": 14, "dy": 8, "color": "@accent"},
                "encoding": {
                    "x": {"field": "xa", "type": "quantitative", "scale": {"domain": [0, 830], "nice": False}},
                    "y": {"field": "ya", "type": "quantitative", "scale": {"domain": [0, 17.5]}, "axis": None},
                    "text": {"value": bi(f"{len(nat)} Einträge auf S. {nat_lo} bis {nat_hi}", f"{len(nat)} entries on pp. {nat_lo} to {nat_hi}")},
                },
            },
        ],
    },
}

# ------------------------------------------------------------ chart 3: the units
UNIT_LABEL = {"Kanne": ("Kanne (Liter)", "Kanne (liters)"), "Eimer": ("Eimer (Liter)", "Eimer (liters)"), "Elle": ("Elle (Meter)", "Elle (meters)")}
unit_expr = lambda i: "{" + ",".join(f"'{k}':'{v[i]}'" for k, v in UNIT_LABEL.items()) + "}[datum.value]"
DISTRICT_ORDER = ["Gera", "Schleiz", "Saalburg", "Lobenstein", "Hirschberg"]
def cell_text(unit, fmt):
    return {
        "transform": [{"filter": f"datum.unit == '{unit}'"}],
        "mark": {"type": "text", "style": "label", "fontSize": 12},
        "encoding": {"text": {"field": "value_base", "type": "quantitative", "format": fmt},
                     "color": {"condition": {"test": "datum.rel >= 112", "value": "@paper"}, "value": "@ink"}},
    }


c3 = {
    "id": "c3",
    "dataset": "units",
    "title": bi(
        "Dieselbe Einheit, andere Größe: Die Kanne ist in Hirschberg ein Drittel größer als in Schleiz",
        "Same unit, different size: the Kanne is a third larger in Hirschberg than in Schleiz",
    ),
    "caption": bi(
        "Metrischer Wert von Kanne, Eimer und Elle in den Bezirken nach Brückners Umrechnungstabelle vom 20. März 1869; je dunkler, desto größer gegenüber dem kleinsten Wert der Zeile. Rechts die Spanne. Quelle: S. 831–832.",
        "Metric value of the Kanne, Eimer and Elle in the districts according to Brückner’s conversion table of 20 March 1869; the darker, the larger relative to the smallest value in the row. Range on the right. Source: pp. 831–832.",
    ),
    "vegalite": {
        "height": {"step": 56},
        "padding": {"top": 4, "bottom": 4, "left": 4, "right": 64},
        "transform": [
            {"filter": "indexof(['Kanne', 'Eimer', 'Elle'], datum.unit) >= 0 && isValid(datum.value_base)"},
            {"joinaggregate": [{"op": "min", "field": "value_base", "as": "vmin"}, {"op": "max", "field": "value_base", "as": "vmax"}], "groupby": ["unit"]},
            {"calculate": "datum.value_base / datum.vmin * 100", "as": "rel"},
            {"calculate": "datum.vmax / datum.vmin - 1", "as": "spread"},
        ],
        "encoding": {
            "x": {"field": "district", "type": "ordinal", "sort": DISTRICT_ORDER,
                  "axis": {"title": None, "orient": "top", "ticks": False, "domain": False, "labelAngle": 0, "labelPadding": 6}},
            "y": {"field": "unit", "type": "ordinal", "sort": {"field": "spread", "op": "max", "order": "descending"},
                  "axis": {"title": None, "ticks": False, "domain": False, "labelExpr": {"de": unit_expr(0), "en": unit_expr(1)}, "labelLimit": 300}},
        },
        "layer": [
            {
                "mark": {"type": "rect", "stroke": "@paper", "strokeWidth": 3, "cornerRadius": 3},
                "encoding": {
                    "color": {"field": "rel", "type": "quantitative", "legend": None, "scale": {"domain": [100, 140], "range": "heatmap"}},
                    "tooltip": [
                        {"field": "unit", "title": bi("Einheit", "Unit")},
                        {"field": "district_printed", "title": bi("Gedruckt", "As printed")},
                        {"field": "definition_printed", "title": bi("Definition", "Definition")},
                        {"field": "value_base", "title": bi("Wert (m oder L)", "Value (m or L)"), "format": ".4f"},
                        {"field": "rel", "title": bi("gegenüber kleinstem Wert (= 100)", "relative to the smallest value (= 100)"), "format": ".1f"},
                    ],
                },
            },
            cell_text("Kanne", ".3f"),
            cell_text("Eimer", ".1f"),
            cell_text("Elle", ".3f"),
            {
                "transform": [{"filter": "datum.district == 'Hirschberg'"}],
                "mark": {"type": "text", "style": "label", "align": "left", "dx": 78},
                "encoding": {"text": {"field": "spread", "type": "quantitative", "format": "+.1%"}},
            },
            {
                "transform": [{"filter": "datum.district == 'Hirschberg' && datum.unit == 'Kanne'"}],
                "mark": {"type": "text", "style": "annotation", "align": "left", "dx": 78, "dy": -40},
                "encoding": {"text": {"value": bi("Spanne", "Range")}},
            },
        ],
    },
}

# ------------------------------------------------------------ text
sources_seen = []
for src in (sub["sources"], cor["sources"], mas["sources"]):
    for x in src:
        key = (x["page"], x["block"])
        if key not in sources_seen:
            sources_seen.append(key)
sources = [{"page": p, "block": b} for p, b in sources_seen]

summary = bi(
    f"Der Anhang des Buchs enthält die Liste der {n_entries} Subskribenten, die zusammen {n_copies} Exemplare bestellten, Brückners {n_cor} Zusätze und Berichtigungen und die amtliche Umrechnung der Maße von 1869. "
    f"Fast die Hälfte der Subskribenten wohnte in Gera, Schleiz und Lobenstein. Von den Berichtigungen betreffen {len(nat)} die Natur des Landes. Die Kanne ist je nach Bezirk um bis zu {fmt_de(spread['Kanne'], 1)} Prozent größer.",
    f"The appendix contains the list of {n_entries} subscribers who ordered {n_copies} copies in all, Brückner’s {n_cor} addenda and corrigenda and the official conversion of weights and measures of 1869. "
    f"Almost half of the subscribers lived in Gera, Schleiz and Lobenstein. {len(nat)} of the corrections concern the nature of the land. The Kanne is up to {spread['Kanne']:.1f} percent larger depending on the district.",
)
findings = [
    bi(
        f"{n_in} der {n_entries} Einträge ({fmt_de(100 * n_in / n_entries, 1)} Prozent) stammen aus dem Fürstentum, {n_top3} aus Gera, Schleiz und Lobenstein; {state_n} stehen im Staats-, Schul- oder Kirchendienst, {land_craft} sind Landwirte oder Handwerker.",
        f"{n_in} of the {n_entries} entries ({100 * n_in / n_entries:.1f} percent) come from the principality, {n_top3} from Gera, Schleiz and Lobenstein; {state_n} are in state, school or church service, {land_craft} are farmers or craftsmen.",
    ),
    bi(
        f"Von {n_cor} Änderungen betreffen {len(nat)} die Natur des Landes (S. {nat_lo} bis {nat_hi}); {n_upd} sind Aktualisierungen, die Ereignisse bis 1869 melden.",
        f"Of {n_cor} changes, {len(nat)} concern the nature of the land (pp. {nat_lo} to {nat_hi}); {n_upd} are updates reporting events up to 1869.",
    ),
    bi(
        f"Die Kanne misst in Schleiz {fmt_de(kmin['value_base'], 4)} Liter, in Hirschberg {fmt_de(kmax['value_base'], 4)}; bei Eimer ({fmt_de(spread['Eimer'], 1)} Prozent) und Elle ({fmt_de(spread['Elle'], 1)} Prozent) ist die Spanne kleiner.",
        f"The Kanne measures {kmin['value_base']:.4f} liters in Schleiz and {kmax['value_base']:.4f} in Hirschberg; for the Eimer ({spread['Eimer']:.1f} percent) and the Elle ({spread['Elle']:.1f} percent) the range is smaller.",
    ),
]
print(findings)

method = bi(
    "Die Subskriptionsliste (S. 835–840) wurde Zeile für Zeile übernommen: Exemplare, Name, Beruf oder Stand und Ort wie gedruckt. Der Ort ist in der Schreibung des Ortsregisters angegeben; die Lage (Landesteil oder außerhalb) folgt aus der Seite des Ortes im Register. "
    "Die Berufsgruppen sind eine redaktionelle Zuordnung nach dem gedruckten Titel (zehn Gruppen für Personen und Firmen, dazu Behörden, Bibliotheken und Vereine). Die Koordinaten der Orte stammen aus GeoNames. "
    "Von den Zusätzen und Berichtigungen (S. 830–834) ist jede gedruckte Anweisung eine Zeile mit Bezugsseite und Zeile des Haupttextes; Art und Kapitel sind redaktionell. "
    "Die Umrechnungstabelle (S. 831–832) ist der amtliche Text vom 20. März 1869 mit 39 Einheitendefinitionen. Die Werte wurden, wo möglich, aus den übrigen Angaben nachgerechnet; 32 von 34 stimmen auf höchstens 0,014 Prozent. "
    "Die Farbe im Diagramm 3 zeigt den Wert gegenüber dem kleinsten der Zeile. Die Kapitelgrenzen im Diagramm 2 stammen aus der Inhaltsübersicht (S. VII–VIII).",
    "The subscription list (pp. 835–840) was taken line by line: copies, name, occupation or rank and place as printed. The place is given in the spelling of the index of places; the location (district or outside) follows from the page of the place in the index. "
    "The occupational groups are an editorial assignment based on the printed title (ten groups for persons and firms, plus authorities, libraries and societies). The coordinates of the places come from GeoNames. "
    "Of the addenda and corrigenda (pp. 830–834) each printed instruction is one row with the target page and line of the main text; kind and chapter are editorial. "
    "The conversion table (pp. 831–832) is the official text of 20 March 1869 with 39 unit definitions. Where possible the values were recomputed from the other entries; 32 of 34 agree to within 0.014 percent. "
    "The color in chart 3 shows the value relative to the smallest in the row. The chapter boundaries in chart 2 come from the table of contents (pp. VII–VIII).",
)
caveats = [
    bi(
        "Eine Subskriptionsliste verzeichnet Vorbestellungen, nicht Leser. Buchhandlungen (50 Exemplare bei Teich in Lobenstein) bestellten vermutlich zum Weiterverkauf, Bibliotheken und Vereine für mehrere Nutzer. Käufer nach Erscheinen fehlen.",
        "A subscription list records advance orders, not readers. Booksellers (50 copies at Teich in Lobenstein) presumably ordered for resale, libraries and societies for several users. Buyers after publication are missing.",
    ),
    bi(
        f"Die Berufsgruppen folgen allein dem gedruckten Titel und sind eine Setzung. Auf der Karte fehlen {missing_places} Orte mit {missing_place_entries} Einträgen ohne Koordinaten sowie die {n_out} Einträge von außerhalb, vor allem Buchhandlungen in Berlin, Dresden und Leipzig.",
        f"The occupational groups follow the printed title alone and are a convention. The map lacks {missing_places} places with {missing_place_entries} entries without coordinates and the {n_out} entries from outside, mostly booksellers in Berlin, Dresden and Leipzig.",
    ),
    bi(
        "Art und Kapitel der Berichtigungen sind redaktionelle Zuordnungen. Die Zeilenangaben wurden nicht nachgezählt, für die Verknüpfung gilt die Bezugsseite. Das Transkript hatte drei berichtigte Druckfehler stillschweigend geglättet oder verlesen (S. 277, 489, 496).",
        "Kind and chapter of the corrections are editorial assignments. The line numbers were not recounted, the target page is what matters for linking. The transcript had silently smoothed or misread three of the misprints being corrected (pp. 277, 489, 496).",
    ),
    bi(
        "Die Umrechnung von 1869 legt fest, was die Einheiten metrisch bedeuten, nicht wie genau die Maße im Gebrauch eingehalten wurden. Zwei Werte weichen im Druck ab: der Scheffel von Schleiz und die Elle von Gera. Das Diagramm 3 zeigt die gedruckten Werte.",
        "The conversion of 1869 fixes what the units mean in metric terms, not how precisely the measures were observed in use. Two values deviate in the print itself: the Scheffel of Schleiz and the Elle of Gera. Chart 3 shows the printed values.",
    ),
]

issues = []
for arc in (sub, cor, mas):
    issues += copy.deepcopy(arc.get("transcription_issues", []))

a = {
    "id": "buch-leser",
    "title": bi("Das Buch, seine Leser und seine Maße", "The book, its readers and its measures"),
    "category": "reception",
    "section": "subscribenten",
    "merges": ["subskribenten-leserschaft-1870", "zusaetze-berichtigungen-1870", "masse-gewichte-umrechnung-1869"],
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "conversions": copy.deepcopy(mas["conversions"]),
    "transcription_issues": issues,
    "datasets": [by_place, by_group, corrections, chapters, units, subscribers, {**base_places(), "name": "orte_basis"}, {**base_rivers(), "name": "fluesse_basis"}],
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Subskribenten", "Leserschaft", "Berichtigungen", "Zusätze", "Maße und Gewichte", "Umrechnung", "Elle", "Kanne", "Eimer", "Drucklegung 1870"],
        "en": ["subscribers", "readership", "corrigenda", "addenda", "weights and measures", "conversion", "Elle", "Kanne", "Eimer", "printing 1870"],
    },
    "related": ["kirche-schule", "klima-gera", "pflanzenwelt"],
    "generated_by": "Claude Sonnet 5.5 (Agent F8), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    write_feature(a, "buch-leser")
