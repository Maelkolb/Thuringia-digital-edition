from f8common import *
import statistics
from collections import defaultdict

h = arch("orte-handwerk-gewerbe-doerfer")
s = arch("orte-sozialstruktur-doerfer-1867")
f = arch("orte-flur-boden-pacht")

weaver = dataset(h, "weaver_places")
social = dataset(s, "social_places")
flur = dataset(f, "flur_places")
trades = dataset(h, "trade_summary")

# ------------------------------------------------------------ complete the coordinates from the base places (name + district)
bp = rows(base_places())
by = defaultdict(list)
for r in bp:
    by[r["ort"]].append(r)


def coords(name, district):
    c = [r for r in by.get(name, []) if r["landestheil"] == district]
    if len(c) == 1:
        return c[0]["lon"], c[0]["lat"]
    c = by.get(name, [])
    if len(c) == 1:
        return c[0]["lon"], c[0]["lat"]
    return None, None


for ds in (weaver, social, flur):
    cn = colnames(ds)
    il, ia, ii, idist = cn.index("lon"), cn.index("lat"), cn.index("name"), cn.index("landestheil")
    for r in ds["rows"]:
        if r[il] is None:
            lo, la = coords(r[ii], r[idist])
            if lo is not None:
                r[il], r[ia] = lo, la
    for c in ds["columns"]:
        if c["name"] in ("lon", "lat"):
            c["note"] = "GeoNames; fehlende Werte aus der Kartengrundlage (orte_basis) nach Name und Landesteil ergänzt"

W = rows(weaver)
S = rows(social)
F = rows(flur)

# ------------------------------------------------------------ numbers
tot_w = sum(r["weavers"] for r in W)
n_w_places = sum(1 for r in W if r["weavers"])
four = sum(r["weavers"] for r in W if r["name"] in ("Hohenleuben", "Langenwetzendorf", "Triebes", "Tanna"))
three = [r for r in W if r["name"] in ("Hohenleuben", "Langenwetzendorf", "Triebes")]
per100 = {r["name"]: r["weavers_per_100"] for r in three}
lo100, hi100 = min(per100.values()), max(per100.values())
nocoord_w = sum(r["weavers"] for r in W if r["lon"] is None)
nocoord_p = sum(1 for r in W if r["lon"] is None and r["weavers"])
dist_per1000 = {}
for lt in ("Gera", "Schleiz", "Lobenstein-Ebersdorf"):
    dist_per1000[lt] = 1000 * sum(r["weavers"] for r in W if r["landestheil"] == lt) / sum(r["inhabitants"] for r in W if r["landestheil"] == lt)
print("weavers", tot_w, n_w_places, four, round(100 * four / tot_w, 1), per100, nocoord_w, nocoord_p, dist_per1000)
gera_w = [r for r in W if r["name"] == "Gera"][0]
print("Gera", gera_w["weavers"], gera_w["weavers_per_100"])

# social groups (derived from social_places, villages with all four groups)
C = [r for r in S if r["complete"] == 1]
GROUPS = [("bauern", "Bauern", "Farmers"), ("haeusler", "Häusler", "Cottagers"), ("tagloehner", "Taglöhner", "Day laborers"), ("dienstboten", "Dienstboten", "Servants")]
DISTRICTS = ["Alle", "Gera", "Schleiz", "Lobenstein-Ebersdorf"]
sg_rows = []
sums = {}
for d in DISTRICTS:
    sel = C if d == "Alle" else [r for r in C if r["landestheil"] == d]
    tot = sum(r[k] for r in sel for k, _, _ in GROUPS)
    sums[d] = {"n": len(sel), "tot": tot}
    for gi, (k, de, en) in enumerate(GROUPS):
        cnt = sum(r[k] for r in sel)
        sums[d][k] = cnt
        sg_rows.append([d, len(sel), k, de, en, gi + 1, cnt, round(100 * cnt / tot, 1)])
social_groups = {
    "name": "social_groups",
    "title": bi("Bauern, Häusler, Taglöhner und Dienstboten nach Landesteil (Dörfer mit allen vier Angaben)", "Farmers, cottagers, day laborers and servants by district (villages with all four figures)"),
    "columns": [
        {"name": "district", "label": bi("Landesteil", "District"), "type": "string", "unit": None, "derived": True, "note": "Alle = Summe der drei Landesteile"},
        {"name": "n_places", "label": bi("Zahl der Dörfer", "Number of villages"), "type": "integer", "unit": "Dörfer", "derived": True},
        {"name": "group", "label": bi("Gruppe (Code)", "Group (code)"), "type": "string", "unit": None, "derived": True},
        {"name": "group_de", "label": bi("Gruppe", "Group"), "type": "string", "unit": None, "derived": True},
        {"name": "group_en", "label": bi("Gruppe (englisch)", "Group (English)"), "type": "string", "unit": None, "derived": True},
        {"name": "group_order", "label": bi("Reihenfolge der Gruppe", "Order of group"), "type": "integer", "unit": None, "derived": True},
        {"name": "count", "label": bi("Anzahl", "Count"), "type": "integer", "unit": "Haushalte oder Personen", "derived": True,
         "note": "Bauern und Häusler als Haushalte, Taglöhner und Dienstboten als Personen, wie in den Ortsartikeln"},
        {"name": "share", "label": bi("Anteil an den vier Gruppen", "Share of the four groups"), "type": "number", "unit": "%", "derived": True},
    ],
    "rows": sg_rows,
    "source_refs": copy.deepcopy(social["source_refs"]),
}
for d in DISTRICTS:
    print(d, sums[d]["n"], {k: round(100 * sums[d][k] / sums[d]["tot"], 1) for k, _, _ in GROUPS})
sh = lambda d, k: round(100 * sums[d][k] / sums[d]["tot"])
n_complete = len(C)
n_social_all = len(S)
tl_per100_h = {d: round(100 * sums[d]["tagloehner"] / sums[d]["haeusler"]) for d in DISTRICTS}
print(tl_per100_h)

# rent vs distance
R = [r for r in F if r["rent_mid"] is not None and r["dist_gera_km"] is not None]
n_rent = len([r for r in F if r["rent_mid"] is not None])
bands = [("near", 0, 10), ("mid", 10, 30), ("far", 30, 80)]
band_stats = {}
for b, lo, hi in bands:
    sel = [r["rent_mid"] for r in R if (r["dist_gera_km"] > lo or lo == 0) and r["dist_gera_km"] <= hi]
    band_stats[b] = (len(sel), statistics.median(sel))
print("rent", len(R), n_rent, band_stats)


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den


rho = spearman([r["dist_gera_km"] for r in R], [r["rent_mid"] for r in R])
print("rho", rho)
dearest = sorted(R, key=lambda r: -r["rent_mid"])[:4]
cheapest = sorted(R, key=lambda r: r["rent_mid"])[:1]
flur_n = len([r for r in F if r["flur_morgen"] is not None])
flur_sum = sum(r["flur_morgen"] for r in F if r["flur_morgen"] is not None)
print(flur_n, flur_sum, flur_sum * 0.255322)

# ------------------------------------------------------------ chart 1: map of the weavers
LABELLED = {
    "up": ["Hohenleuben", "Langenberg"],
    "down": ["Langenwetzendorf"],
    "right": ["Gera"],
    "left": ["Triebes", "Tanna", "Schleiz"],
}
LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}


def label_layers(names, dx, dy, align):
    flt = "indexof(" + json.dumps(names, ensure_ascii=False) + ", datum.name) >= 0 && isValid(datum.lon)"
    out = []
    for style in ("place-halo", "place-label"):
        out.append({
            "transform": [{"filter": flt}, {"calculate": "datum.name + ' ' + datum.weavers", "as": "lab"}],
            "mark": {"type": "text", "style": style, "dx": dx, "dy": dy, "align": align},
            "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "lab"}},
        })
    return out


c1 = {
    "id": "c1",
    "dataset": "weaver_places",
    "extra_datasets": ["orte_basis", "fluesse_basis"],
    "title": bi(
        "Die Weberei konzentriert sich um Hohenleuben, Langenwetzendorf und Triebes im Landesteil Schleiz",
        "Weaving is concentrated around Hohenleuben, Langenwetzendorf and Triebes in the district of Schleiz",
    ),
    "caption": bi(
        f"Webermeister je Ort (Fläche der Kreise), blau: mindestens 10 je 100 Einwohner. Gera zählt {gera_w['weavers']} Zeug- und Leinweber, aber nur {fmt_de(gera_w['weavers_per_100'], 1)} je 100 Einwohner. Quelle: Ortsartikel S. 418–825.",
        f"Master weavers per place (area of the circles), blue: at least 10 per 100 inhabitants. Gera counts {gera_w['weavers']} cloth and linen weavers, but only {gera_w['weavers_per_100']:.1f} per 100 inhabitants. Source: place articles pp. 418–825.",
    ),
    "vegalite": {
        "height": 470,
        "projection": {"type": "mercator"},
        "layer": [
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
            {
                "transform": [
                    {"filter": "isValid(datum.lon) && isValid(datum.lat) && datum.weavers > 0"},
                    {"calculate": "datum.weavers_per_100 >= 10 ? 'a' : 'b'", "as": "dense"},
                ],
                "mark": {"type": "circle", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.85},
                "encoding": {
                    "longitude": LON,
                    "latitude": LAT,
                    "size": {"field": "weavers", "type": "quantitative", "scale": {"type": "sqrt", "range": [8, 1500]}, "legend": None},
                    "color": {
                        "field": "dense", "type": "nominal",
                        "scale": {"domain": ["a", "b"], "range": ["@accent", "@muted"]},
                        "legend": {"title": bi("Webermeister je 100 Einwohner", "Master weavers per 100 inhabitants"), "titleLimit": 300, "orient": "top-left", "direction": "vertical",
                                   "labelExpr": {"de": "datum.value == 'a' ? '10 und mehr' : 'weniger als 10'", "en": "datum.value == 'a' ? '10 or more' : 'fewer than 10'"}},
                    },
                    "tooltip": [
                        {"field": "name", "title": bi("Ort", "Place")},
                        {"field": "weavers", "title": bi("Webermeister", "Master weavers"), "format": ",d"},
                        {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants"), "format": ",d"},
                        {"field": "weavers_per_100", "title": bi("je 100 Einwohner", "per 100 inhabitants"), "format": ".1f"},
                        {"field": "verbatim", "title": bi("Gedruckt", "As printed")},
                    ],
                },
            },
            *label_layers(LABELLED["up"], 0, -12, "center"),
            *label_layers(LABELLED["down"], 0, 17, "center"),
            *label_layers(LABELLED["right"], 12, 0, "left"),
            *label_layers(LABELLED["left"], -10, 0, "right"),
        ],
    },
}

# ------------------------------------------------------------ chart 2: social structure
c2 = {
    "id": "c2",
    "dataset": "social_groups",
    "title": bi(
        f"Bauern sind nur rund ein Fünftel der Dorfgruppen, im Landesteil Gera sogar nur {sh('Gera', 'bauern')} Prozent",
        f"Farmers are a fifth of the village groups, only {sh('Gera', 'bauern')} percent in Gera",
    ),
    "caption": bi(
        f"Anteil von Bauern, Häuslern (Haushalte) sowie Taglöhnern und Dienstboten (Personen) in den {n_complete} Dörfern, deren Ortsartikel alle vier Gruppen nennt. Quelle: Ortsartikel S. 418–825.",
        f"Share of farmers, cottagers (households) and day laborers and servants (persons) in the {n_complete} villages whose place article names all four groups. Source: place articles pp. 418–825.",
    ),
    "vegalite": {
        "height": {"step": 46},
        "padding": {"top": 26, "bottom": 4, "left": 4, "right": 8},
        "transform": [
            {"calculate": {"de": "datum.district == 'Alle' ? 'Alle Dörfer (' + datum.n_places + ')' : datum.district + ' (' + datum.n_places + ')'",
                           "en": "datum.district == 'Alle' ? 'All villages (' + datum.n_places + ')' : datum.district + ' (' + datum.n_places + ')'"}, "as": "ylab"},
            {"calculate": "datum.district == 'Alle' ? 0 : datum.district == 'Gera' ? 1 : datum.district == 'Schleiz' ? 2 : 3", "as": "yo"},
            {"window": [{"op": "sum", "field": "share", "as": "x1"}], "groupby": ["district"], "sort": [{"field": "group_order"}], "frame": [None, 0]},
            {"calculate": "datum.x1 - datum.share", "as": "x0"},
            {"calculate": "(datum.x0 + datum.x1) / 2", "as": "xm"},
        ],
        "encoding": {
            "y": {"field": "ylab", "type": "ordinal", "sort": {"field": "yo", "op": "min"},
                  "axis": {"title": None, "ticks": False, "domain": False, "labelLimit": 300}},
        },
        "layer": [
            {
                "mark": {"type": "bar", "stroke": "@paper", "strokeWidth": 2, "size": 32},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 100]}, "axis": None},
                    "x2": {"field": "x1"},
                    "color": {"field": "group", "type": "nominal", "legend": None,
                              "scale": {"domain": ["bauern", "haeusler", "tagloehner", "dienstboten"], "range": ["@accent", "@context", "@accent2", "@ink2"]}},
                    "tooltip": [
                        {"field": "ylab", "title": bi("Landesteil", "District")},
                        {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                        {"field": "count", "title": bi("Anzahl", "Count"), "format": ",d"},
                        {"field": "share", "title": bi("Anteil in %", "Share in %"), "format": ".1f"},
                    ],
                },
            },
            {
                "transform": [{"calculate": "format(datum.share, '.0f') + ' %'", "as": "pct"}],
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative", "scale": {"domain": [0, 100]}},
                    "text": {"field": "pct"},
                    "color": {"condition": {"test": "datum.group != 'haeusler'", "value": "@paper"}, "value": "@ink"},
                },
            },
            {
                "transform": [{"filter": "datum.district == 'Alle'"}],
                "mark": {"type": "text", "style": "label", "dy": -31},
                "encoding": {
                    "x": {"field": "xm", "type": "quantitative", "scale": {"domain": [0, 100]}},
                    "text": {"field": {"de": "group_de", "en": "group_en"}},
                    "color": {"condition": [{"test": "datum.group == 'bauern'", "value": "@accent"}, {"test": "datum.group == 'tagloehner'", "value": "@accent2"}], "value": "@ink2"},
                },
            },
        ],
    },
}

# ------------------------------------------------------------ chart 3: rent against distance from Gera
rent_filter = "isValid(datum.rent_mid) && isValid(datum.dist_gera_km)"
band_calc = "datum.dist_gera_km <= 10 ? 0 : datum.dist_gera_km <= 30 ? 1 : 2"
c3 = {
    "id": "c3",
    "dataset": "flur_places",
    "title": bi(
        f"Die Pacht sinkt mit der Entfernung von Gera von {fmt_de(band_stats['near'][1], 0)} auf {fmt_de(band_stats['far'][1], 2)} Taler je Morgen",
        f"Rent falls with the distance from Gera from {band_stats['near'][1]:.0f} to {band_stats['far'][1]:.2f} thalers per Morgen",
    ),
    "caption": bi(
        f"Pacht eines mittelguten Morgens in {len(R)} Dörfern nach Luftlinie zu Gera; Striche: Median je Entfernungsklasse (bis 10, 10 bis 30, über 30 km). Quelle: Ortsartikel S. 418–825.",
        f"Rent of a medium-quality Morgen in {len(R)} villages by straight-line distance from Gera; bars: median per distance class (up to 10, 10 to 30, over 30 km). Source: place articles pp. 418–825.",
    ),
    "vegalite": {
        "height": 340,
        "transform": [
            {"filter": rent_filter},
            {"calculate": band_calc, "as": "band"},
            {"joinaggregate": [{"op": "median", "field": "rent_mid", "as": "med"}, {"op": "count", "as": "nb"}], "groupby": ["band"]},
            {"calculate": "datum.band == 0 ? 0 : datum.band == 1 ? 10 : 30", "as": "bx0"},
            {"calculate": "datum.band == 0 ? 10 : datum.band == 1 ? 30 : 68", "as": "bx1"},
        ],
        "encoding": {
            "x": {"field": "dist_gera_km", "type": "quantitative", "scale": {"domain": [0, 68], "nice": False},
                  "axis": {"title": bi("Entfernung von Gera in km (Luftlinie)", "Distance from Gera in km (straight line)"), "values": [0, 10, 20, 30, 40, 50, 60], "grid": False}},
            "y": {"field": "rent_mid", "type": "quantitative", "scale": {"domain": [0, 13]},
                  "axis": {"title": bi("Pacht je Morgen in Talern", "Rent per Morgen in thalers"), "values": [0, 2, 4, 6, 8, 10, 12], "grid": True}},
        },
        "layer": [
            {
                "mark": {"type": "point", "filled": True, "size": 46, "color": "@accent", "opacity": 0.55, "stroke": "@paper", "strokeWidth": 0.6},
                "encoding": {
                    "tooltip": [
                        {"field": "name", "title": bi("Ort", "Place")},
                        {"field": "landestheil", "title": bi("Landesteil", "District")},
                        {"field": "dist_gera_km", "title": bi("Entfernung von Gera, km", "Distance from Gera, km"), "format": ".1f"},
                        {"field": "rent_mid", "title": bi("Pacht, Taler", "Rent, thalers"), "format": ".2f"},
                        {"field": "rent_text", "title": bi("Gedruckt", "As printed")},
                    ],
                },
            },
            {
                "transform": [{"aggregate": [{"op": "min", "field": "bx0", "as": "bx0"}, {"op": "min", "field": "bx1", "as": "bx1"}, {"op": "min", "field": "med", "as": "med"}], "groupby": ["band"]}],
                "mark": {"type": "rule", "strokeWidth": 3, "color": "@ink"},
                "encoding": {"x": {"field": "bx0", "type": "quantitative"}, "x2": {"field": "bx1"}, "y": {"field": "med", "type": "quantitative"}},
            },
            {
                "transform": [{"aggregate": [{"op": "min", "field": "bx0", "as": "bx0"}, {"op": "min", "field": "bx1", "as": "bx1"}, {"op": "min", "field": "med", "as": "med"}], "groupby": ["band"]},
                              {"calculate": "(datum.bx0 + datum.bx1) / 2", "as": "bxm"}],
                "mark": {"type": "text", "style": "label", "dy": -10},
                "encoding": {"x": {"field": "bxm", "type": "quantitative"}, "y": {"field": "med", "type": "quantitative"},
                             "text": {"field": "med", "type": "quantitative", "format": ".2~f"}},
            },
            {
                "transform": [{"filter": "indexof(['Hohenleuben', 'Blintendorf'], datum.name) >= 0"}],
                "mark": {"type": "text", "style": "annotation", "align": "left", "dx": 7, "dy": -4},
                "encoding": {"x": {"field": "dist_gera_km", "type": "quantitative"}, "y": {"field": "rent_mid", "type": "quantitative"}, "text": {"field": "name"}},
            },
            {
                "transform": [{"filter": "datum.name == 'Naundorf'"}],
                "mark": {"type": "text", "style": "annotation", "align": "left", "dx": 12, "dy": -3},
                "encoding": {"x": {"field": "dist_gera_km", "type": "quantitative"}, "y": {"field": "rent_mid", "type": "quantitative"},
                             "text": {"value": bi("je 12 Taler: Tinz, Langenberg, Söllmnitz, Naundorf", "12 thalers each: Tinz, Langenberg, Söllmnitz, Naundorf")}},
            },
        ],
    },
}

print("dearest", [(r["name"], r["rent_mid"], r["dist_gera_km"]) for r in dearest], cheapest[0]["name"], cheapest[0]["rent_mid"])

# ------------------------------------------------------------ text
sources_seen = []
for src in (h["sources"], s["sources"], f["sources"]):
    for x in src:
        key = (x["page"], x["block"])
        if key not in sources_seen:
            sources_seen.append(key)
sources = [{"page": p, "block": b} for p, b in sources_seen]
print("sources", len(sources))

summary = bi(
    f"Fast jeder Ortsartikel Brückners nennt Handwerker, Gliederung der Einwohner und Pacht. Die {fmt_de(tot_w)} Webermeister in {n_w_places} Orten konzentrieren sich im Landesteil Schleiz. "
    f"In den Dörfern stellen Bauern nur {sh('Alle', 'bauern')} Prozent der erfassten Gruppen, Häusler {sh('Alle', 'haeusler')} Prozent. Der Boden ist bei Gera am teuersten.",
    f"Almost every place article of Brückner names the craftsmen, the social divisions of the inhabitants and the rent. The {tot_w:,} master weavers in {n_w_places} places concentrate in the district of Schleiz. "
    f"In the villages farmers make up only {sh('Alle', 'bauern')} percent of the recorded groups, cottagers {sh('Alle', 'haeusler')} percent. Land is dearest around Gera.",
)
print(summary["de"])
findings = [
    bi(
        f"Hohenleuben, Langenwetzendorf, Triebes und Tanna stellen {round(100 * four / tot_w)} Prozent aller Webermeister; in den ersten dreien sind es {round(lo100)} bis {round(hi100)} je 100 Einwohner. Je 1.000 Einwohner: Schleiz {fmt_de(dist_per1000['Schleiz'], 1)}, Gera {fmt_de(dist_per1000['Gera'], 1)}.",
        f"Hohenleuben, Langenwetzendorf, Triebes and Tanna account for {round(100 * four / tot_w)} percent of all master weavers; in the first three there are {round(lo100)} to {round(hi100)} per 100 inhabitants. Per 1,000 inhabitants: Schleiz {dist_per1000['Schleiz']:.1f}, Gera {dist_per1000['Gera']:.1f}.",
    ),
    bi(
        f"Im Landesteil Gera kommen auf 100 Häusler {tl_per100_h['Gera']} Taglöhner, in Schleiz {tl_per100_h['Schleiz']} und in Lobenstein-Ebersdorf {tl_per100_h['Lobenstein-Ebersdorf']}. Das deutet auf Fabrikarbeit in und um Gera hin.",
        f"In the district of Gera there are {tl_per100_h['Gera']} day laborers per 100 cottagers, in Schleiz {tl_per100_h['Schleiz']} and in Lobenstein-Ebersdorf {tl_per100_h['Lobenstein-Ebersdorf']}. This suggests factory work in and around Gera.",
    ),
    bi(
        f"Die Pacht sinkt mit der Entfernung von Gera (Rangkorrelation {fmt_de(rho, 2).replace('-', '−')}, {len(R)} Orte); am teuersten sind Tinz, Langenberg, Söllmnitz und Naundorf mit je 12 Talern, am billigsten Blintendorf mit 1 bis 2 Talern.",
        f"Rent falls with the distance from Gera (rank correlation {f'{rho:.2f}'.replace('-', '−')}, {len(R)} places); dearest are Tinz, Langenberg, Söllmnitz and Naundorf at 12 thalers each, cheapest Blintendorf at 1 to 2 thalers.",
    ),
]
print(findings)

method = bi(
    "Grundlage sind die Angaben der Ortsartikel zu 173 Orten (Webermeister), 167 Landgemeinden (Sozialgefüge, Flur und Pacht); die sechs Städte fehlen beim Sozialgefüge. "
    "Die Weberzahl umfasst Weber, Leinweber und Webermeister ohne Gesellen; in Lobenstein stehen 121 Tuchmacher gesondert. Die Gruppen des Sozialgefüges fassen die uneinheitlichen Bezeichnungen der Artikel zu vier Klassen zusammen: "
    "Bauern (auch Pferde-, Kühbauern, Halb- und Viertelbauern, Landwirte), Häusler (auch Kleinhäusler, Hintersiedler, Hausgenossen), Taglöhner und Arbeiter, Dienstboten. Genannte Untergruppen wurden nicht doppelt gezählt. "
    f"Das Diagramm 2 zählt die {n_complete} Dörfer, die alle vier Gruppen nennen. Bauern und Häusler sind bei Brückner Haushalte, Taglöhner und Dienstboten Personen. "
    "Die Pacht ist die Angabe für einen mittelguten Morgen; bei Spannen steht die Mitte. Die Entfernung ist die Luftlinie zwischen den GeoNames-Koordinaten der Orte und Geras. "
    "Fehlende Koordinaten wurden aus der Kartengrundlage nach Name und Landesteil ergänzt; wo sie fehlen, fehlt der Ort auf der Karte. Ein preußischer Morgen sind 0,2553 ha (S. 832).",
    "The basis is the statements of the place articles for 173 places (master weavers) and 167 rural municipalities (social structure, field area and rent); the six towns are missing from the social structure. "
    "The weaver figure covers weavers, linen weavers and master weavers without journeymen; in Lobenstein 121 cloth makers are named separately. The groups of the social structure combine the varying terms of the articles into four classes: "
    "farmers (including horse and cow farmers, half and quarter farmers, agriculturists), cottagers (including small cottagers, Hintersiedler, Hausgenossen), day laborers and workers, servants. Subgroups named within a group were not counted twice. "
    f"Chart 2 counts the {n_complete} villages that name all four groups. Farmers and cottagers are households in Brückner, day laborers and servants persons. "
    "The rent is the figure for a medium-quality Morgen; for ranges the midpoint is used. The distance is the straight line between the GeoNames coordinates of the place and of Gera. "
    "Missing coordinates were completed from the base map by name and district; where they are still missing, the place is absent from the map. A Prussian Morgen is 0.2553 ha (p. 832).",
)
caveats = [
    bi(
        "Die Artikel nennen die Gewerbe sehr unterschiedlich vollständig. In Hohenleuben, Langenwetzendorf, Triebes und Tanna sind es »Webermeister«, in Gera »Zeug- und Leinweber«; Gesellen und Hausindustrie sind nicht einheitlich erfasst.",
        "The articles name the trades with very different completeness. In Hohenleuben, Langenwetzendorf, Triebes and Tanna they are “Webermeister”, in Gera “Zeug- und Leinweber”; journeymen and cottage industry are not recorded uniformly.",
    ),
    bi(
        f"Die Anteile des Sozialgefüges sind Mischanteile (Haushalte und Personen) und keine Anteile an der Bevölkerung; Frauen, Kinder, Handwerker und Arme fehlen. Für {n_social_all - n_complete} Dörfer nennt Brückner nicht alle vier Gruppen, sie fehlen im Diagramm.",
        f"The shares of the social structure are mixed shares (households and persons) and not shares of the population; wives, children, craftsmen and the poor are missing. For {n_social_all - n_complete} villages Brückner does not name all four groups; they are absent from the chart.",
    ),
    bi(
        f"Die Pacht ist das Urteil des Verfassers für einen mittelguten Morgen, kein gemessener Marktpreis. Das Gefälle zu Gera entspricht einem Marktgefälle, lässt sich aber nicht von Höhenlage und Bodengüte trennen (Deutung).",
        "The rent is the author’s judgment for a medium-quality Morgen, not a measured market price. The gradient toward Gera matches a market gradient but cannot be separated from altitude and soil quality (interpretation).",
    ),
    bi(
        f"Auf der Karte fehlen {nocoord_p} Orte mit zusammen {nocoord_w} Webermeistern ({fmt_de(100 * nocoord_w / tot_w, 1)} Prozent), weil für sie keine Koordinaten vorliegen, darunter Niederböhmsdorf mit 53 und Neuärgerniß mit 21.",
        f"The map lacks {nocoord_p} places with a total of {nocoord_w} master weavers ({100 * nocoord_w / tot_w:.1f} percent) because no coordinates are available for them, among them Niederböhmsdorf with 53 and Neuärgerniß with 21.",
    ),
]

a = {
    "id": "dorfleben",
    "title": bi("Bauern, Häusler und Handwerker in den Dörfern", "Farmers, cottagers and craftsmen in the villages"),
    "category": "places",
    "section": "t2",
    "merges": ["orte-sozialstruktur-doerfer-1867", "orte-handwerk-gewerbe-doerfer", "orte-flur-boden-pacht"],
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "conversions": copy.deepcopy(f["conversions"]),
    "datasets": [weaver, social_groups, flur, social, trades, {**base_places(), "name": "orte_basis"}, {**base_rivers(), "name": "fluesse_basis"}],
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Dörfer", "Weber", "Weberei", "Bauern", "Häusler", "Taglöhner", "Dienstboten", "Pacht", "Flur", "Handwerk", "Hohenleuben"],
        "en": ["villages", "weavers", "weaving", "farmers", "cottagers", "day laborers", "servants", "rent", "field area", "crafts", "Hohenleuben"],
    },
    "related": ["berufe-gewerbe", "landwirtschaft", "siedlung-wohnen"],
    "generated_by": "Claude Sonnet 5.5 (Agent F8), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    write_feature(a, "dorfleben")
