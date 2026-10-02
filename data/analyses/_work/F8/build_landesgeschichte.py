from f8common import *
from collections import Counter

ch = arch("geschichte-chronik-ereignisse-530-1867")
la = arch("geschichte-landerwerb-landverlust-1248-1690")
lt = arch("geschichte-landesteilungen-linien-1240-1870")

houses = dataset(lt, "houses")
transactions = dataset(la, "transactions")
events = dataset(ch, "events")

H = rows(houses)
T = rows(transactions)
E = rows(events)

# ---------------------------------------------------------------- derived columns on houses
SHORT = {
    1: ("Weida", "Weida"),
    2: ("Gera", "Gera"),
    3: ("Plauen (bis 1305)", "Plauen (to 1305)"),
    4: ("Plauen, ältere Linie", "Plauen, older branch"),
    5: ("Reuß-Plauen", "Reuss-Plauen"),
    6: ("Untergreiz (Heinrich d. ä.)", "Untergreiz (Heinrich the elder)"),
    7: ("Obergreiz (mittlere Linie)", "Obergreiz (middle line)"),
    8: ("Dölau (Heinrich V.)", "Dölau (Heinrich V)"),
    9: ("Burgk (1596)", "Burgk (1596)"),
    10: ("Untergreiz (Heinrich V.)", "Untergreiz (Heinrich V)"),
    11: ("Dölau (1616)", "Dölau (1616)"),
    12: ("Untergreiz (Specialhaus)", "Untergreiz (special house)"),
    13: ("Obergreiz (Specialhaus)", "Obergreiz (special house)"),
    14: ("Burgk (1668)", "Burgk (1668)"),
    15: ("Rothenthal", "Rothenthal"),
    16: ("Dölau (1694)", "Dölau (1694)"),
    17: ("Gera (Heinrich Posthumus)", "Gera (Heinrich Posthumus)"),
    18: ("Gera (Specialhaus)", "Gera (special house)"),
    19: ("Schleiz", "Schleiz"),
    20: ("Lobenstein (bis 1678)", "Lobenstein (to 1678)"),
    21: ("Saalburg", "Saalburg"),
    22: ("Lobenstein (Zweig)", "Lobenstein (branch)"),
    23: ("Hirschberg", "Hirschberg"),
    24: ("Ebersdorf", "Ebersdorf"),
}
add_column(houses, "short_de", "Kurzname", "Short name", [SHORT[r["ord"]][0] for r in H], typ="string")
add_column(houses, "short_en", "Kurzname (englisch)", "Short name (English)", [SHORT[r["ord"]][1] for r in H], typ="string")

# ---------------------------------------------------------------- lines per year (derived)
BR = [("voigte", "Voigte", "Voigts", 0), ("alt", "Reuß ä. L.", "Reuss older line", 1), ("jung", "Reuß j. L.", "Reuss younger line", 2)]
years = sorted({r["start_year"] for r in H} | {r["end_plot"] for r in H})
lpy_rows = []
for y in years:
    for code, de, en, o in BR:
        n = sum(1 for r in H if r["branch"] == code and r["start_year"] <= y and (y < r["end_plot"] or (y == years[-1] and r["end_year"] is None)))
        lpy_rows.append([y, code, de, en, o, n])
lines_per_year = {
    "name": "lines_per_year",
    "title": bi("Gleichzeitig bestehende Linien und Häuser je Zweig", "Simultaneously existing lines and houses by branch"),
    "columns": [
        {"name": "year", "label": bi("Ab Jahr", "From year"), "type": "integer", "unit": None, "derived": True},
        {"name": "branch", "label": bi("Zweig (Code)", "Branch (code)"), "type": "string", "unit": None, "derived": True},
        {"name": "branch_de", "label": bi("Zweig", "Branch"), "type": "string", "unit": None, "derived": True},
        {"name": "branch_en", "label": bi("Zweig (englisch)", "Branch (English)"), "type": "string", "unit": None, "derived": True},
        {"name": "branch_order", "label": bi("Reihenfolge des Zweigs", "Order of branch"), "type": "integer", "unit": None, "derived": True},
        {"name": "n_lines", "label": bi("Zahl der Linien und Häuser", "Number of lines and houses"), "type": "integer", "unit": "Linien", "derived": True,
         "note": "gilt von diesem Jahr bis zum nächsten Eintrag; aus den Zeilen von houses berechnet"},
    ],
    "rows": lpy_rows,
    "source_refs": copy.deepcopy(houses["source_refs"]),
}

# ---------------------------------------------------------------- numbers for the texts
tot_by_year = {}
for y in years:
    tot_by_year[y] = sum(r[5] for r in lpy_rows if r[0] == y)
peak = max(tot_by_year.values())
peak_years = [y for y in years if tot_by_year[y] == peak]
peak_end = years[years.index(peak_years[-1]) + 1]
start_n = tot_by_year[1240]
end_n = tot_by_year[1870]
print("peak", peak, peak_years, peak_end, "start", start_n, "end", end_n)
peak_alt = [r[5] for r in lpy_rows if r[0] == peak_years[0] and r[1] == "alt"][0]
peak_jung = [r[5] for r in lpy_rows if r[0] == peak_years[0] and r[1] == "jung"][0]
print("peak split", peak_alt, peak_jung)

acq = lambda a, b: sum(1 for r in T if r["kind"] == "acq" and a <= r["year"] <= b)
los = lambda a, b: sum(1 for r in T if r["kind"] == "loss" and a <= r["year"] <= b)
a1, l1 = acq(0, 1349), los(0, 1349)
a2, l2 = acq(1350, 1399), los(1350, 1399)
modes2 = Counter(r["mode"] for r in T if r["kind"] == "loss" and 1350 <= r["year"] <= 1399)
m2 = modes2["pfand"] + modes2["verkauf"] + modes2["lehnsauftrag"]
print("a1 l1 a2 l2", a1, l1, a2, l2, "modes", modes2, m2)
wei_a = sum(1 for r in T if r["house"] == "weida" and r["kind"] == "acq")
wei_l = sum(1 for r in T if r["house"] == "weida" and r["kind"] == "loss")
pla_a = sum(1 for r in T if r["house"] == "plauen" and r["kind"] == "acq")
pla_l = sum(1 for r in T if r["house"] == "plauen" and r["kind"] == "loss")
print("weida", wei_a, wei_l, "plauen", pla_a, pla_l)
regn = [r for r in T if r["object"] == "Regnitzland" and r["kind"] == "loss"][0]
print(regn["year"], regn["price"], regn["price_unit"])
n_events = len(E)
kc = Counter(r["kind"] for r in E)
print("events", n_events, kc)
land_early = sum(1 for r in E if 1200 <= r["year"] <= 1499 and r["kind"] in ("acq", "loss"))
all_early = sum(1 for r in E if 1200 <= r["year"] <= 1499)
land_late = sum(1 for r in E if r["year"] >= 1600 and r["kind"] in ("acq", "loss"))
all_late = sum(1 for r in E if r["year"] >= 1600)
other_late = sum(1 for r in E if r["year"] >= 1600 and r["kind"] in ("dyn", "found", "disaster"))
print("early", land_early, all_early, "late", land_late, all_late, other_late)
alt_end = max(r["start_year"] for r in H if r["branch"] == "alt" and r["end_year"] is None)
reunion_alt = 1768
reunion_jung = 1848
assert reunion_jung - reunion_alt == 80
# the reunification years come from the data
alt_single = [y for y in years if [r for r in lpy_rows if r[0] == y and r[1] == "alt"][0][5] == 1 and y > 1700]
print("alt single from", alt_single[0])
jung_single = [y for y in years if [r for r in lpy_rows if r[0] == y and r[1] == "jung"][0][5] == 1 and y > 1700]
print("jung single from", jung_single[0])
assert alt_single[0] == 1768 and jung_single[0] == 1848

# ---------------------------------------------------------------- chart 1: Gantt of the lines and the count below
label_expr = lambda idx: "{" + ",".join(f"'{o}':'{SHORT[o][idx].replace(chr(39), chr(8217))}'" for o in SHORT) + "}[datum.value]"
X_DOMAIN = [1225, 1990]
BRANCH_SCALE = {"domain": ["jung", "alt", "voigte"], "range": ["@accent", "@accent2", "@accent3"]}

c1 = {
    "id": "c1",
    "dataset": "houses",
    "extra_datasets": ["lines_per_year"],
    "title": bi(
        "Aus drei Linien um 1240 wurden bis 1694 zehn gleichzeitig regierende Häuser",
        "From three lines around 1240 the family grew to ten simultaneously ruling houses by 1694",
    ),
    "caption": bi(
        "Oben Beginn und Ende der 24 Linien und Häuser nach Brückners Tafel XV (ungefähre Jahre als Punktwerte), Pfeil: besteht 1870 fort. Unten die Zahl der gleichzeitig bestehenden. Quelle: S. 333–403.",
        "Top: start and end of the 24 lines and houses after Brückner’s Table XV (approximate years as point values), arrow: still exists in 1870. Bottom: how many existed at once. Source: pp. 333–403.",
    ),
    "vegalite": {
        "vconcat": [
            {
                "width": 540,
                "height": {"step": 17},
                "encoding": {
                    "y": {
                        "field": "ord",
                        "type": "ordinal",
                        "sort": "ascending",
                        "axis": {"title": None, "ticks": False, "domain": False, "grid": False,
                                 "labelExpr": {"de": label_expr(0), "en": label_expr(1)}, "labelLimit": 400},
                    },
                    "color": {"field": "branch", "type": "nominal", "legend": None, "scale": BRANCH_SCALE},
                },
                "layer": [
                    {
                        "mark": {"type": "bar", "size": 11, "cornerRadius": 2, "stroke": None},
                        "encoding": {
                            "x": {"field": "start_year", "type": "quantitative",
                                  "scale": {"domain": X_DOMAIN, "nice": False},
                                  "axis": {"orient": "top", "format": "d", "values": [1300, 1400, 1500, 1600, 1700, 1800, 1870],
                                           "title": None, "grid": True, "domain": False, "labelFlush": False}},
                            "x2": {"field": "end_plot"},
                            "tooltip": [
                                {"field": {"de": "label_de", "en": "label_en"}, "title": bi("Linie", "Line")},
                                {"field": "start_year", "title": bi("Beginn", "Start"), "format": "d"},
                                {"field": "end_year", "title": bi("Ende", "End"), "format": "d"},
                                {"field": {"de": "event_de", "en": "event_en"}, "title": bi("Brückner", "Brückner")},
                            ],
                        },
                    },
                    {
                        "transform": [{"filter": "!isValid(datum.end_year)"}],
                        "mark": {"type": "point", "shape": "triangle-right", "filled": True, "size": 70, "stroke": None},
                        "encoding": {"x": {"field": "end_plot", "type": "quantitative", "scale": {"domain": X_DOMAIN, "nice": False}}},
                    },
                    {
                        "transform": [
                            {"filter": "indexof([3, 8, 17], datum.ord) >= 0"},
                            {"calculate": "datum.ord == 3 ? 1325 : datum.ord == 8 ? 1650 : 1665", "as": "label_x"},
                        ],
                        "mark": {"type": "text", "align": "left", "style": "label", "fontSize": 12},
                        "encoding": {
                            "x": {"field": "label_x", "type": "quantitative", "scale": {"domain": X_DOMAIN, "nice": False}},
                            "text": {"field": {"de": "branch_de", "en": "branch_en"}},
                        },
                    },
                    {
                        "transform": [
                            {"filter": "indexof([13, 19], datum.ord) >= 0"},
                            {"calculate": {"de": "datum.ord == 13 ? 'seit 1768 allein' : 'seit 1848 allein'", "en": "datum.ord == 13 ? 'alone from 1768' : 'alone from 1848'"}, "as": "note"},
                        ],
                        "mark": {"type": "text", "align": "left", "dx": 9, "style": "label-muted"},
                        "encoding": {
                            "x": {"field": "end_plot", "type": "quantitative", "scale": {"domain": X_DOMAIN, "nice": False}},
                            "text": {"field": "note"},
                        },
                    },
                ],
            },
            {
                "data": {"name": "lines_per_year"},
                "width": 540,
                "height": 90,
                "encoding": {
                    "x": {"field": "year", "type": "quantitative", "scale": {"domain": X_DOMAIN, "nice": False},
                          "axis": {"values": [1300, 1400, 1500, 1600, 1700, 1800, 1870], "format": "d", "title": None, "grid": True, "domain": True}},
                },
                "layer": [
                    {
                        "mark": {"type": "area", "interpolate": "step-after", "opacity": 0.9, "line": False},
                        "encoding": {
                            "y": {"field": "n_lines", "type": "quantitative", "stack": "zero",
                                  "axis": {"title": bi("Linien", "Lines"), "values": [0, 5, 10], "grid": True},
                                  "scale": {"domain": [0, 11.5]}},
                            "color": {"field": "branch", "type": "nominal", "legend": None, "scale": BRANCH_SCALE},
                            "order": {"field": "branch_order", "type": "quantitative"},
                            "tooltip": [
                                {"field": "year", "title": bi("ab Jahr", "from year"), "format": "d"},
                                {"field": {"de": "branch_de", "en": "branch_en"}, "title": bi("Zweig", "Branch")},
                                {"field": "n_lines", "title": bi("Linien und Häuser", "Lines and houses")},
                            ],
                        },
                    },
                    {
                        "transform": [
                            {"joinaggregate": [{"op": "sum", "field": "n_lines", "as": "total"}], "groupby": ["year"]},
                            {"filter": "datum.branch == 'jung' && datum.year == 1694"},
                        ],
                        "mark": {"type": "text", "align": "left", "baseline": "middle", "dx": 6, "style": "label"},
                        "encoding": {
                            "x": {"field": "year", "type": "quantitative"},
                            "y": {"field": "total", "type": "quantitative", "stack": None},
                            "text": {"value": bi("10 (1694–1698)", "10 (1694–1698)")},
                        },
                    },
                    {
                        "transform": [
                            {"joinaggregate": [{"op": "sum", "field": "n_lines", "as": "total"}], "groupby": ["year"]},
                            {"filter": "datum.branch == 'jung' && (datum.year == 1240 || datum.year == 1848)"},
                        ],
                        "mark": {"type": "text", "align": "left", "dx": 3, "dy": -8, "style": "label"},
                        "encoding": {
                            "x": {"field": "year", "type": "quantitative"},
                            "y": {"field": "total", "type": "quantitative", "stack": None},
                            "text": {"field": "total", "type": "quantitative"},
                        },
                    },
                ],
            },
        ],
        "spacing": 14,
    },
}

# ---------------------------------------------------------------- chart 2: bricks of acquisitions and losses
c2 = {
    "id": "c2",
    "dataset": "transactions",
    "title": bi(
        "Bis 1349 überwogen die Erwerbungen, in der zweiten Hälfte des 14. Jahrhunderts die Verluste",
        "Acquisitions prevailed until 1349, losses in the second half of the 14th century",
    ),
    "caption": bi(
        "Jedes Feld ist ein von Brückner erzählter Besitzwechsel (85), nach Jahr geordnet: oben Erwerb, unten Verlust (Verkauf, Pfand, Lehnsauftrag, Krieg, Tausch). Die Zahlen nennen die Summe je Halbjahrhundert. Quelle: S. 321–389.",
        "Each square is a change of ownership told by Brückner (85), ordered by year: acquisition above, loss below (sale, pledge, feudal surrender, war, exchange). The figures give the total per half-century. Source: pp. 321–389.",
    ),
    "vegalite": {
        "height": 300,
        "transform": [
            {"window": [{"op": "row_number", "as": "rn"}], "groupby": ["half_label", "kind"], "sort": [{"field": "year"}, {"field": "ord"}]},
            {"joinaggregate": [{"op": "max", "field": "rn", "as": "n"}], "groupby": ["half_label", "kind"]},
            {"calculate": "datum.kind == 'acq' ? datum.rn - 1 : -(datum.rn - 1)", "as": "y0"},
            {"calculate": "datum.kind == 'acq' ? datum.rn : -datum.rn", "as": "y1"},
        ],
        "encoding": {
            "x": {"field": "half_label", "type": "ordinal", "axis": {"title": None, "labelAngle": 0, "ticks": False, "labelPadding": 8, "domain": False}},
        },
        "layer": [
            {
                "mark": {"type": "bar", "size": 44, "cornerRadius": 2, "stroke": "@paper", "strokeWidth": 2},
                "encoding": {
                    "y": {"field": "y0", "type": "quantitative",
                          "axis": {"title": None, "labelExpr": "abs(datum.value)", "values": [-15, -10, -5, 0, 5, 10], "grid": True, "domain": False},
                          "scale": {"domain": [-16.5, 11.5]}},
                    "y2": {"field": "y1"},
                    "color": {"field": "kind", "type": "nominal", "legend": None,
                              "scale": {"domain": ["acq", "loss"], "range": ["@positive", "@negative"]}},
                    "tooltip": [
                        {"field": "year", "title": bi("Jahr", "Year"), "format": "d"},
                        {"field": {"de": "house_de", "en": "house_en"}, "title": bi("Haus", "House")},
                        {"field": "object", "title": bi("Gegenstand", "Object")},
                        {"field": {"de": "mode_de", "en": "mode_en"}, "title": bi("Form", "Form")},
                        {"field": {"de": "text_de", "en": "text_en"}, "title": bi("Vorgang", "Event")},
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.rn == datum.n && datum.kind == 'acq'"}],
                "mark": {"type": "text", "dy": -9, "style": "label"},
                "encoding": {"y": {"field": "y1", "type": "quantitative"}, "text": {"field": "n", "type": "quantitative"}},
            },
            {
                "transform": [{"filter": "datum.rn == datum.n && datum.kind == 'loss'"}],
                "mark": {"type": "text", "dy": 10, "style": "label"},
                "encoding": {"y": {"field": "y1", "type": "quantitative"}, "text": {"field": "n", "type": "quantitative"}},
            },
            {
                "transform": [{"filter": "datum.half_label == '1650–1699' && datum.rn == 1 && datum.kind == 'acq'"}],
                "mark": {"type": "text", "style": "label", "dy": -34, "color": "@positive"},
                "encoding": {"y": {"datum": 8, "type": "quantitative"}, "text": {"value": bi("Erwerbungen", "Acquisitions")}},
            },
            {
                "transform": [{"filter": "datum.half_label == '1650–1699' && datum.rn == 1 && datum.kind == 'acq'"}],
                "mark": {"type": "text", "style": "label", "color": "@negative"},
                "encoding": {"y": {"datum": -8, "type": "quantitative"}, "text": {"value": bi("Verluste", "Losses")}},
            },
        ],
    },
}

# ---------------------------------------------------------------- chart 3: heatmap of all events
KINDS = ["acq", "loss", "dyn", "war", "treaty", "found", "disaster"]
kind_de = {"acq": "Landerwerb", "loss": "Landverlust", "dyn": "Teilung, Erbfolge", "war": "Krieg, Aufstand", "treaty": "Vertrag, Bündnis",
           "found": "Stiftung, Reform", "disaster": "Brand, Not"}
kind_en = {"acq": "Acquisition", "loss": "Loss of land", "dyn": "Partition, succession", "war": "War, uprising", "treaty": "Treaty, alliance",
           "found": "Foundation, reform", "disaster": "Fire, hardship"}
kind_expr = lambda d: "{" + ",".join(f"'{k}':'{d[k]}'" for k in KINDS) + "}[datum.value]"

c3 = {
    "id": "c3",
    "dataset": "events",
    "title": bi(
        "Bis 1500 erzählt Brückner von Landgewinn und Landverlust, seit 1600 von Reformen, Teilungen und Bränden",
        "Until 1500 the story is land gained and lost, from 1600 reforms, divisions and fires",
    ),
    "caption": bi(
        f"Zahl der {n_events} datierten Ereignisse in Brückners Erzählung je Halbjahrhundert (Beginn) und Art; ›bis 1199‹ fasst die Zeit ab 530 zusammen, die letzte Spalte reicht bis 1867. Quelle: S. 313–403.",
        f"Number of the {n_events} dated events in Brückner’s narrative per half-century (start) and kind; “to 1199” gathers the time from 530, the last column runs to 1867. Source: pp. 313–403.",
    ),
    "vegalite": {
        "height": {"step": 30},
        "transform": [
            {"calculate": "datum.half_century < 1200 ? 1150 : datum.half_century", "as": "hc"},
            {"calculate": {"de": "datum.hc == 1150 ? 'bis 1199' : toString(datum.hc)", "en": "datum.hc == 1150 ? 'to 1199' : toString(datum.hc)"}, "as": "hc_label"},
            {"aggregate": [{"op": "count", "as": "n"}], "groupby": ["hc", "hc_label", "kind"]},
        ],
        "encoding": {
            "x": {"field": "hc_label", "type": "ordinal", "sort": {"field": "hc", "op": "min"},
                  "axis": {"title": None, "labelAngle": 0, "ticks": False, "domain": False, "orient": "top", "labelPadding": 6,
                           "labelExpr": {"de": "datum.value == 'bis 1199' ? ['bis', '1199'] : datum.value == '1850' ? ['1850', 'bis 67'] : datum.value",
                                         "en": "datum.value == 'to 1199' ? ['to', '1199'] : datum.value == '1850' ? ['1850', 'to 67'] : datum.value"}}},
            "y": {"field": "kind", "type": "ordinal", "sort": KINDS,
                  "axis": {"title": None, "ticks": False, "domain": False, "labelExpr": {"de": kind_expr(kind_de), "en": kind_expr(kind_en)}, "labelLimit": 180}},
        },
        "layer": [
            {
                "mark": {"type": "rect", "stroke": "@paper", "strokeWidth": 2, "cornerRadius": 2},
                "encoding": {
                    "color": {"field": "n", "type": "quantitative", "legend": None, "scale": {"range": "heatmap", "domain": [0, 16]}},
                    "tooltip": [
                        {"field": {"de": "hc_label", "en": "hc_label"}, "title": bi("Halbjahrhundert", "Half-century")},
                        {"field": "kind", "title": bi("Art", "Kind")},
                        {"field": "n", "title": bi("Ereignisse", "Events")},
                    ],
                },
            },
            {
                "mark": {"type": "text", "style": "label"},
                "encoding": {
                    "text": {"field": "n", "type": "quantitative"},
                    "color": {"condition": {"test": "datum.n >= 6", "value": "@paper"}, "value": "@ink"},
                },
            },
        ],
    },
}

# ---------------------------------------------------------------- text
sources_seen = []
for src in (ch["sources"], la["sources"], lt["sources"]):
    for s in src:
        key = (s["page"], s["block"])
        if key not in sources_seen:
            sources_seen.append(key)
sources = [{"page": p, "block": b} for p, b in sources_seen]

summary = bi(
    f"Brückner erzählt die Geschichte der Voigte von Weida, Gera und Plauen und des Hauses Reuß als Folge von Käufen, Pfändern, Erbfällen und Teilungen. "
    f"Aus {n_events} datierten Ereignissen ergeben sich {kc['acq']} Erwerbungen und {kc['loss']} Verluste von Land sowie {kc['dyn']} Teilungen und Erbfälle. "
    f"Aus drei Linien um 1240 wurden bis 1694 zehn Häuser; die ältere Linie war 1768, die jüngere 1848 wieder in einer Hand.",
    f"Brückner tells the history of the Voigts of Weida, Gera and Plauen and of the house of Reuss as a series of purchases, pledges, successions and divisions. "
    f"His {n_events} dated events include {kc['acq']} acquisitions and {kc['loss']} losses of land and {kc['dyn']} divisions and successions. "
    f"From three lines around 1240 the family grew to ten houses by 1694; the older line was reunited in 1768, the younger in 1848.",
)
assert peak == 10 and start_n == 3

findings = [
    bi(
        f"Bis 1349 stehen {a1} Erwerbungen nur {l1} Verlusten gegenüber; von 1350 bis 1399 sind es {a2} Erwerbungen und {l2} Verluste, {m2} davon durch Pfand, Verkauf oder Lehnsauftrag.",
        f"Until 1349 there are {a1} acquisitions against only {l1} losses; from 1350 to 1399 there are {a2} acquisitions and {l2} losses, {m2} of them by pledge, sale or feudal surrender.",
    ),
    bi(
        f"Weida verzeichnet {wei_l} Verluste und {wei_a} Erwerbungen, die Burggrafen von Plauen {pla_a} Erwerbungen und {pla_l} Verluste. 1373 verkauft Weida das Regnitzland für {regn['price']} Schock Groschen.",
        f"Weida records {wei_l} losses and {wei_a} acquisitions, the burgraves of Plauen {pla_a} acquisitions and {pla_l} losses. In 1373 Weida sells the Regnitzland for {regn['price']} Schock Groschen.",
    ),
    bi(
        f"Die ältere Linie war seit {alt_single[0]} wieder in einer Hand, die jüngere erst seit {jung_single[0]}, also {jung_single[0] - alt_single[0]} Jahre später.",
        f"The older line was back in one hand from {alt_single[0]}, the younger only from {jung_single[0]}, that is {jung_single[0] - alt_single[0]} years later.",
    ),
]

method = bi(
    "Die Ereignisse (Diagramm 3) wurden beim vollständigen Lesen der Erzählung von S. 313–393 gesammelt: jedes Ereignis mit gedruckter Jahreszahl, das Gebietswechsel, Teilung oder Aussterben, Krieg, Vertrag, Stiftung, Reform oder Unglück betrifft. "
    "Die Beschreibungen sind knappe Paraphrasen; die Art und das handelnde Haus sind redaktionelle Zuordnungen. Die 85 Besitzwechsel (Diagramm 2) sind die Erwerbungen und Verluste daraus, mit Form (Kauf, Pfand, Lehnsauftrag …) und, wo genannt, Preis. "
    "Die Linien und Häuser (Diagramm 1) stammen aus Brückners Tafel XV (S. 403), der Tabelle der älteren Linie (S. 390) und dem Fließtext. Als Linie zählt, was Brückner als eigene Herrschaft bezeichnet; wo sich die Zusammensetzung ändert, ist die Linie in Abschnitte zerlegt. "
    "Ungefähre Jahre (»um 1240«, »ca. 1305«) stehen als Punktwerte; noch bestehende Linien sind bis 1870 gezeichnet. Die Zahl der gleichzeitig bestehenden Linien ist aus den Zeilen berechnet und stimmt für 1625 bis 1768 mit der gedruckten Tabelle auf S. 390 überein.",
    "The events (chart 3) were collected by reading the narrative on pp. 313–393 in full: every event with a printed year that concerns a change of territory, a division or extinction, a war, a treaty, a foundation, a reform or a calamity. "
    "The descriptions are brief paraphrases; the kind and the house involved are editorial assignments. The 85 changes of ownership (chart 2) are the acquisitions and losses among them, with form (purchase, pledge, feudal surrender …) and, where stated, price. "
    "The lines and houses (chart 1) come from Brückner’s Table XV (p. 403), the table of the older line (p. 390) and the running text. A line counts if Brückner treats it as a lordship of its own; where its composition changes, it is split into periods. "
    "Approximate years (“c. 1240”, “ca. 1305”) are entered as point values; lines that still exist are drawn up to 1870. The number of simultaneously existing lines is computed from the rows and agrees with the printed table on p. 390 for 1625 to 1768.",
)

caveats = [
    bi(
        "Die Auswahl folgt Brückners Erzählung. Die Zahlen sagen etwas über seine Gewichtung, nicht über die tatsächliche Häufigkeit von Ereignissen; das 17. und 18. Jahrhundert erzählt er knapp.",
        "The selection follows Brückner’s narrative. The figures say something about his emphasis, not about the true frequency of events; he tells the 17th and 18th centuries briefly.",
    ),
    bi(
        "Ob ein Vorgang als Erwerb oder Verlust zählt, ist bei Lehnsaufträgen, Belehnungen, Pfändern und Prozessen eine Deutung. Manche Vorgänge stehen doppelt, weil sie zwei Häuser betreffen (1319 Verkauf durch Weida, Kauf durch Gera).",
        "Whether a transaction counts as gain or loss is an interpretation for feudal surrenders, enfeoffments, pledges and lawsuits. Some transactions appear twice because they concern two houses (1319 sale by Weida, purchase by Gera).",
    ),
    bi(
        "Die Gliederung in Linien, Zweige und Häuser folgt Brückners Begriffen, ist aber nicht überall trennscharf (Burgk und Dölau entstehen zweimal). Die Paragiate Köstritz und die Nebenlinie Lobenstein-Selbitz sind nicht gezählt.",
        "The division into lines, branches and houses follows Brückner’s terms but is not sharp everywhere (Burgk and Dölau arise twice). The appanages of Köstritz and the side line Lobenstein-Selbitz are not counted.",
    ),
    bi(
        "Brückner nennt Jahre oft nur ungefähr (»um«, »ca.«) oder als Spanne; gezeichnet ist die gedruckte Jahreszahl. Das Brandjahr von Schleiz (1474) ist aus der Angabe »zwei Jahre vor 1476« errechnet.",
        "Brückner often gives years only approximately (“um”, “ca.”) or as a span; the printed year is drawn. The year of the fire of Schleiz (1474) is computed from the statement “two years before 1476”.",
    ),
]

a = {
    "id": "landesgeschichte",
    "title": bi("Landesgeschichte: Erwerb, Verlust und Teilungen", "History of the land: gains, losses and divisions"),
    "category": "history",
    "section": "t1-5",
    "merges": [
        "geschichte-chronik-ereignisse-530-1867",
        "geschichte-landerwerb-landverlust-1248-1690",
        "geschichte-landesteilungen-linien-1240-1870",
    ],
    "sources": sources,
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "datasets": [houses, lines_per_year, transactions, events],
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Landesgeschichte", "Voigte", "Weida", "Gera", "Plauen", "Reuß", "Landesteilung", "Landerwerb", "Landverlust", "Linien", "Chronik"],
        "en": ["history", "Voigts", "Weida", "Gera", "Plauen", "Reuss", "partition", "acquisition of land", "loss of land", "lines", "chronology"],
    },
    "related": ["haus-reuss", "ortsnamen", "bergbau"],
    "generated_by": "Claude Sonnet 5.5 (Agent F8), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    write_feature(a, "landesgeschichte")
