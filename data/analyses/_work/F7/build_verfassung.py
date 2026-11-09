"""Feature F7a: verfassung-verwaltung (Landtag, Verwaltung und Militär)."""
import json
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F7")
from common import *

FID = "verfassung-verwaltung"

# ---------------------------------------------------------------- data
towns = {"Gera": 16283, "Schleiz": 7968, "Lobenstein-Ebersdorf": 4671}   # S. 95, r7 r13 r19, Städte 1867
rural = {"Gera": 21969, "Schleiz": 19400, "Lobenstein-Ebersdorf": 17683}
pop = {"Gera": 38252, "Schleiz": 27368, "Lobenstein-Ebersdorf": 22354}
for d in pop:
    assert towns[d] + rural[d] == pop[d]
pop_towns = sum(towns.values())
pop_rural = sum(rural.values())
pop_total = pop_towns + pop_rural
assert pop_total == sum(pop.values()) == 87974

seats_towns, seats_rural = 6, 3
seats_elected = seats_towns + seats_rural
seats_all = 13
seat_share_towns = seats_towns / seats_elected * 100
seat_share_rural = seats_rural / seats_elected * 100
pop_share_towns = pop_towns / pop_total * 100
pop_share_rural = pop_rural / pop_total * 100
per_seat_towns = pop_towns / seats_towns
per_seat_rural = pop_rural / seats_rural
factor_seat = per_seat_rural / per_seat_towns

area = {"Gera": 4.03, "Schleiz": 6.03, "Lobenstein-Ebersdorf": 5.0}
area_total = sum(area.values())
counts = {
    "Gendarmen": {"Gera": 7, "Schleiz": 9, "Lobenstein-Ebersdorf": 8},
    "Ärzte": {"Gera": 14, "Schleiz": 10, "Lobenstein-Ebersdorf": 8},
    "Justizämter": {"Gera": 2, "Schleiz": 3, "Lobenstein-Ebersdorf": 3},
}
measure_en = {"Gendarmen": "Gendarmes", "Ärzte": "Physicians", "Justizämter": "Justizämter"}
measure_order = {"Ärzte": 1, "Gendarmen": 2, "Justizämter": 3}
tot = {m: sum(c.values()) for m, c in counts.items()}
assert tot == {"Gendarmen": 24, "Ärzte": 32, "Justizämter": 8}

off_rows = []
stats = {}
for m, c in counts.items():
    cp = tot[m] / pop_total * 1e4
    ca = tot[m] / area_total
    for d in pop:
        p10 = c[d] / pop[d] * 1e4
        ps = c[d] / area[d]
        ip = p10 / cp * 100
        ia = ps / ca * 100
        stats[(m, d)] = (p10, ps, ip, ia)
        off_rows.append([d, measure_order[m], m, measure_en[m], c[d], tot[m], pop[d], area[d],
                         round(p10, 2), round(ps, 2), round(ip, 1), round(ia, 1)])
off_rows.sort(key=lambda r: (r[1], list(pop).index(r[0])))

# contingent
REICH, BUND = "Reichskontingent", "Bundeskontingent"
cont_rows = [
    [1, "bis 1681", "until 1681", REICH, 24, None, 24],
    [2, "1681 bis 1702", "1681 to 1702", REICH, 71.5, None, 71.5],
    [3, "ab 1702, mit Schwarzburg", "from 1702, with Schwarzburg", REICH, 333, None, 333],
    [4, "Deutscher Bund, zuerst", "German Confederation, at first", BUND, 522, 261, 783],
    [5, "Deutscher Bund ab 1842", "German Confederation from 1842", BUND, 608, 261, 869],
    [6, "Norddeutscher Bund 1867", "North German Confederation, 1867", BUND, 885, None, 885],
]
cont_first = int(cont_rows[0][6])
cont_last = int(cont_rows[-1][6])
factor_cont = cont_last / cont_first

# ---------------------------------------------------------------- datasets
ds_rep = dataset(
    "representation",
    bi("Sitze im Landtag und Einwohner 1867: Städte und übrige Gemeinden", "Landtag seats and inhabitants in 1867: towns and other communities"),
    [col("group_de", "Gruppe", "Group", "string"),
     col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
     col("seats", "Von den Gemeinden gewählte Sitze", "Seats chosen by the communities", "integer", "Sitze", True, "Im Druck als Zahlwort (sechs, drei)"),
     col("population", "Einwohner 1867", "Inhabitants 1867", "integer", "Personen", True, "Summe der drei Landesteile, S. 95"),
     col("seat_share", "Anteil an den von den Gemeinden gewählten Sitzen", "Share of the seats chosen by the communities", "number", "%", True),
     col("pop_share", "Anteil an den Einwohnern", "Share of the inhabitants", "number", "%", True),
     col("per_seat", "Einwohner je Sitz", "Inhabitants per seat", "number", "Personen", True),
     col("rank", "Reihenfolge", "Order", "integer", None, True)],
    [["Städte", "Towns", seats_towns, pop_towns, round(seat_share_towns, 1), round(pop_share_towns, 1), round(per_seat_towns), 1],
     ["Übrige Gemeinden", "Other communities", seats_rural, pop_rural, round(seat_share_rural, 1), round(pop_share_rural, 1), round(per_seat_rural), 2]],
    [ref(268, "b2"), ref(95, "b4", "r7, r13, r19")],
)

ds_off = dataset(
    "officials",
    bi("Gendarmen, Ärzte und Justizämter in den drei Landesteilen", "Gendarmes, physicians and Justizämter in the three districts"),
    [col("district", "Landesteil", "District", "string"),
     col("measure_order", "Reihenfolge", "Order", "integer", None, True),
     col("measure_de", "Merkmal", "Measure", "string"),
     col("measure_en", "Merkmal (englisch)", "Measure (English)", "string"),
     col("count", "Anzahl", "Number", "integer", "Stellen", True, "Gendarmen und Ärzte wie gedruckt, Justizämter nach Amtssitz zugeordnet"),
     col("total", "Anzahl im Land", "Number in the country", "integer", "Stellen", True),
     col("population", "Einwohner 1867", "Inhabitants 1867", "integer", "Personen"),
     col("area_sqm", "Fläche", "Area", "number", "□Meilen", False, "Lobenstein-Ebersdorf: circa 5"),
     col("per_10000", "je 10.000 Einwohner", "per 10,000 inhabitants", "number", None, True),
     col("per_sqm", "je □Meile", "per square mile", "number", None, True),
     col("index_pop", "Index je Einwohner (Landesdurchschnitt = 100)", "Index per inhabitant (national average = 100)", "number", None, True),
     col("index_area", "Index je Fläche (Landesdurchschnitt = 100)", "Index per area (national average = 100)", "number", None, True)],
    off_rows,
    [ref(273, "b3"), ref(274, "b1"), ref(280, "b5"), ref(281, "b1"), ref(95, "b4", "r7, r13, r19"),
     ref(407, "b3"), ref(574, "b1"), ref(709, "b2")],
)

ds_cont = dataset(
    "contingent",
    bi("Zu stellende Mannschaft nach Zeitabschnitt", "Troops to be provided by period"),
    [col("period_order", "Reihenfolge", "Order", "integer", None, True),
     col("period_de", "Zeitabschnitt", "Period", "string"),
     col("period_en", "Zeitabschnitt (englisch)", "Period (English)", "string"),
     col("era", "Art des Kontingents", "Kind of contingent", "string", None, True),
     col("main", "Hauptkontingent", "Main contingent", "number", "Mann", True, "71 1/2 im Druck"),
     col("reserve", "Reservekontingent", "Reserve contingent", "number", "Mann", True, "Nach 1842 als unverändert angenommen"),
     col("total", "Zu stellende Mannschaft", "Troops to be provided", "number", "Mann", True)],
    cont_rows,
    [ref(271, "b3"), ref(271, "b4")],
)

ds_landtag = dataset(
    "landtag",
    bi("Zusammensetzung des Landtags", "Composition of the Landtag"),
    [col("group_de", "Gruppe", "Group", "string"),
     col("group_en", "Gruppe (englisch)", "Group (English)", "string"),
     col("seats", "Sitze", "Seats", "integer", "Sitze", True, "Im Druck teils als Zahlwort"),
     col("mode_de", "Wahlart", "Mode of election", "string"),
     col("mode_en", "Wahlart (englisch)", "Mode of election (English)", "string")],
    [["Besitzer des Köstritzer Paragiums", "Holder of the Köstritz appanage", 1, "eigene Stimme", "seat by right"],
     ["Übrige Rittergutsbesitzer", "Other manor owners", 3, "Urwahl, ein Wahlbezirk für das ganze Land", "direct election, one district for the whole country"],
     ["Stadtgemeinden", "Towns", 6, "Wahlmänner", "electors (indirect election)"],
     ["Übrige Gemeinden", "Other communities", 3, "Wahlmänner", "electors (indirect election)"]],
    [ref(268, "b2"), ref(268, "b3")],
)

council_src = archive_dataset("verfassung-landtag-gemeinderaete-vertretung", "council")
council_rows = [[r[1], r[2], r[3], r[4], r[5], r[6]] for r in council_src["rows"]]
ds_council = dataset(
    "council",
    bi("Größe des Gemeinderats nach Einwohnerklasse", "Size of the municipal council by population class"),
    [col("class_de", "Einwohnerklasse", "Population class", "string"),
     col("class_en", "Einwohnerklasse (englisch)", "Population class (English)", "string"),
     col("lower", "Untere Grenze", "Lower limit", "integer", "Einwohner"),
     col("upper", "Obere Grenze", "Upper limit", "integer", "Einwohner"),
     col("members", "Mitglieder des Gemeinderats", "Members of the council", "integer", "Personen"),
     col("per_1000", "Mitglieder je 1000 Einwohner an der oberen Klassengrenze", "Members per 1,000 inhabitants at the upper class limit", "number", None, True)],
    council_rows,
    [ref(269, "b2")],
)

# ---------------------------------------------------------------- charts
n = de_num
e = en_num
GERA, SCHL, LOBE = "Gera", "Schleiz", "Lobenstein-Ebersdorf"
tip_district = {"field": "district", "title": bi("Landesteil", "District")}

share_label = {
    "de": "datum.measure === 'seat_share' ? [datum.group_de, datum.seats + ' (' + format(datum.pct, '.0f') + ' %)'] : [datum.group_de, format(datum.population, ',d') + ' (' + format(datum.pct, '.0f') + ' %)']",
    "en": "datum.measure === 'seat_share' ? [datum.group_en, datum.seats + ' (' + format(datum.pct, '.0f') + '%)'] : [datum.group_en, format(datum.population, ',d') + ' (' + format(datum.pct, '.0f') + '%)']"}

c1 = {
    "id": "c1",
    "dataset": "representation",
    "title": bi("Städte hatten zwei Drittel der von den Gemeinden gewählten Sitze, aber nur ein Drittel der Einwohner",
                "Towns held two thirds of the community-elected seats but only a third of the population"),
    "caption": bi(
        f"Anteil der Städte und der übrigen Gemeinden an den {seats_elected} von den Gemeinden gewählten Sitzen des Landtags und an den Einwohnern 1867. Nicht gezeigt: vier Sitze des Köstritzer Paragiums und der Rittergutsbesitzer. Quellen: S. 268, 95.",
        f"Share of the towns and of the other communities in the {seats_elected} Landtag seats elected by the communities and in the population of 1867. Not shown: four seats of the Köstritz appanage and the manor owners. Sources: pp. 268, 95."),
    "vegalite": {
        "height": {"step": 88},
        "transform": [
            {"fold": ["seat_share", "pop_share"], "as": ["measure", "pct"]},
            {"stack": "pct", "groupby": ["measure"], "sort": [{"field": "rank"}], "as": ["x0", "x1"]},
            {"calculate": share_label, "as": "label"},
            {"calculate": {
                "de": "datum.measure === 'seat_share' ? 'Landtagssitze (" + str(seats_elected) + ")' : 'Einwohner 1867 (" + n(pop_total) + ")'",
                "en": "datum.measure === 'seat_share' ? 'Landtag seats (" + str(seats_elected) + ")' : 'Population 1867 (" + e(pop_total) + ")'"},
             "as": "measure_label"},
            {"calculate": "datum.measure === 'seat_share' ? 1 : 2", "as": "measure_order"},
        ],
        "encoding": {
            "y": {"field": "measure_label", "type": "nominal", "sort": {"field": "measure_order", "op": "min"},
                  "axis": {"title": None, "labelFontSize": 12, "labelFontWeight": 600, "labelLimit": 300, "ticks": False, "domain": False, "labelOffset": 12}},
        },
        "layer": [
            {
                "mark": {"type": "bar", "height": 30, "yOffset": 12, "cornerRadiusEnd": 0},
                "encoding": {
                    "x": {"field": "x0", "type": "quantitative", "scale": {"domain": [0, 100]},
                          "axis": {"values": [0, 25, 50, 75, 100], "labelExpr": {"de": "datum.value + ' %'", "en": "datum.value + '%'"}, "title": None, "grid": False}},
                    "x2": {"field": "x1"},
                    "color": {"field": "group_de", "type": "nominal", "legend": None,
                              "scale": {"domain": ["Städte", "Übrige Gemeinden"], "range": ["@accent", "@accent2"]}},
                    "tooltip": [
                        {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                        {"field": "seats", "title": bi("Von den Gemeinden gewählte Sitze", "Seats elected by the communities")},
                        {"field": "population", "title": bi("Einwohner 1867", "Population 1867"), "format": ",d"},
                        {"field": "pct", "title": bi("Anteil in Prozent", "Share in percent"), "format": ".1f"},
                        {"field": "per_seat", "title": bi("Einwohner je Sitz", "Inhabitants per seat"), "format": ",d"},
                    ],
                },
            },
            {
                "transform": [{"filter": "datum.rank === 1"}],
                "mark": {"type": "text", "align": "left", "baseline": "bottom", "dx": 2, "dy": -21, "lineHeight": 15, "style": "label"},
                "encoding": {"x": {"field": "x0", "type": "quantitative"}, "text": {"field": "label"}},
            },
            {
                "transform": [{"filter": "datum.rank === 2"}],
                "mark": {"type": "text", "align": "right", "baseline": "bottom", "dx": -2, "dy": -21, "lineHeight": 15, "style": "label"},
                "encoding": {"x": {"field": "x1", "type": "quantitative"}, "text": {"field": "label"}},
            },
        ],
    },
}

dist_domain = [GERA, SCHL, LOBE]
dist_range = ["@accent", "@accent2", "@accent3"]
idx_scale = {"domain": [40, 180], "nice": False}
dot_tooltip = [
    tip_district,
    {"field": {"de": "measure_de", "en": "measure_en"}, "title": bi("Merkmal", "Measure")},
    {"field": "count", "title": bi("Anzahl", "Number")},
    {"field": "per_10000", "title": bi("je 10.000 Einwohner", "per 10,000 inhabitants"), "format": ".2f"},
    {"field": "per_sqm", "title": bi("je Quadratmeile", "per square mile"), "format": ".2f"},
    {"field": "index", "title": bi("Index", "Index"), "format": ".0f"},
]
row_label = {
    "de": "datum.measure_de + ' (' + datum.total + ') ' + (datum.basis === 'index_pop' ? 'je Einwohner' : 'je Quadratmeile')",
    "en": "datum.measure_en + ' (' + datum.total + ') ' + (datum.basis === 'index_pop' ? 'per inhabitant' : 'per square mile')"}

c2 = {
    "id": "c2",
    "dataset": "officials",
    "title": bi("Ärzte folgten den Einwohnern, Gendarmen und Justizämter eher der Fläche",
                "Physicians were spread by population, gendarmes and Justizämter rather by area"),
    "caption": bi(
        "Gendarmen, promovierte Ärzte und Justizämter in den drei Landesteilen je Einwohner und je Quadratmeile, als Index (Landesdurchschnitt = 100); die Linie reicht vom kleinsten zum größten Wert. Quellen: S. 273, 274, 280, 95, 407, 574, 709.",
        "Gendarmes, physicians with a doctorate and Justizämter in the three districts per inhabitant and per square mile, as an index (national average = 100); the line spans the lowest to the highest value. Sources: pp. 273, 274, 280, 95, 407, 574, 709."),
    "vegalite": {
        "height": {"step": 34},
        "transform": [
            {"fold": ["index_pop", "index_area"], "as": ["basis", "index"]},
            {"calculate": row_label, "as": "row"},
            {"calculate": "datum.measure_order * 2 + (datum.basis === 'index_area' ? 1 : 0)", "as": "row_order"},
            {"joinaggregate": [{"op": "min", "field": "index", "as": "lo"}, {"op": "max", "field": "index", "as": "hi"}], "groupby": ["row"]},
        ],
        "encoding": {
            "y": {"field": "row", "type": "nominal", "sort": {"field": "row_order", "op": "min"},
                  "axis": {"title": None, "ticks": False, "domain": False, "grid": False, "labelLimit": 260}},
        },
        "layer": [
            {"mark": {"type": "rule", "color": "@ink2", "strokeWidth": 1},
             "encoding": {"x": {"datum": 100, "type": "quantitative", "scale": idx_scale,
                                "axis": {"values": [50, 100, 150], "title": bi("Index, Landesdurchschnitt = 100", "Index, national average = 100"), "grid": False}},
                          "y": None}},
            {"transform": [{"filter": "datum.district === 'Gera'"}],
             "mark": {"type": "rule", "color": "@context", "strokeWidth": 3, "strokeCap": "round"},
             "encoding": {"x": {"field": "lo", "type": "quantitative", "scale": idx_scale}, "x2": {"field": "hi"}}},
            *[{"transform": [{"filter": f"datum.district === '{district}'"}],
               "mark": {"type": "circle", "size": 110, "opacity": 1, "stroke": "@paper", "strokeWidth": 1.5, "yOffset": shift},
               "encoding": {
                   "x": {"field": "index", "type": "quantitative", "scale": idx_scale},
                   "color": {"field": "district", "type": "nominal", "scale": {"domain": dist_domain, "range": dist_range},
                             "legend": {"title": None, "orient": "top", "direction": "vertical"}},
                   "tooltip": dot_tooltip}}
              for district, shift in zip(dist_domain, (-6, 0, 6))],
        ],
    },
}

BAR_SHIFT = 8
c3 = {
    "id": "c3",
    "dataset": "contingent",
    "title": bi(f"Das Militärkontingent wuchs von {cont_first} Mann bis 1681 auf {cont_last} Mann im Jahr 1867",
                f"The military contingent grew from {cont_first} men (until 1681) to {cont_last} men in 1867"),
    "caption": bi(
        "Zu stellende Mannschaft in sechs Zeitabschnitten. Grau: Kontingent zum Reichsheer, Blau: Bundeskontingent, beim Deutschen Bund mit der Reserve. Quelle: S. 271.",
        "Troops to be provided in six periods. Grey: contingent to the imperial army, blue: confederation contingent, including the reserve under the German Confederation. Source: p. 271."),
    "vegalite": {
        "height": {"step": 44},
        "transform": [
            {"calculate": {"de": "datum.period_de", "en": "datum.period_en"}, "as": "period"},
            {"calculate": "isValid(datum.reserve) ? format(datum.total, ',.0f') + ' (' + format(datum.main, ',.0f') + ' + ' + format(datum.reserve, ',.0f') + ')' : format(datum.total, ',.1~f')", "as": "total_label"},
        ],
        "encoding": {"y": {"field": "period", "type": "nominal", "sort": {"field": "period_order", "op": "min"}, "axis": None}},
        "layer": [
            {"transform": [{"fold": ["main", "reserve"], "as": ["part", "men"]},
                           {"filter": "isValid(datum.men)"},
                           {"calculate": "datum.part === 'main' ? 1 : 2", "as": "part_order"},
                           {"calculate": {"de": "datum.part === 'main' ? 'Hauptkontingent' : 'Reserve'", "en": "datum.part === 'main' ? 'main contingent' : 'reserve'"}, "as": "part_label"}],
             "mark": {"type": "bar", "height": 16, "yOffset": BAR_SHIFT, "cornerRadiusEnd": 0},
             "encoding": {
                 "x": {"field": "men", "type": "quantitative", "stack": "zero",
                       "scale": {"domain": [0, 1250]},
                       "axis": {"title": bi("Mann", "Men"), "values": [0, 250, 500, 750, 1000], "format": ",d"}},
                 "order": {"field": "part_order", "type": "quantitative"},
                 "color": {"condition": {"test": f"datum.era === '{BUND}'", "value": "@accent"}, "value": "@context"},
                 "opacity": {"condition": {"test": "datum.part === 'reserve'", "value": 0.45}, "value": 1},
                 "tooltip": [
                     {"field": "period", "title": bi("Zeitabschnitt", "Period")},
                     {"field": "part_label", "title": bi("Teil", "Part")},
                     {"field": "men", "title": bi("Mann", "Men"), "format": ",.1~f"},
                     {"field": "total", "title": bi("Zusammen", "Total"), "format": ",.1~f"},
                 ]}},
            {"mark": {"type": "text", "align": "left", "baseline": "bottom", "dy": -2},
             "encoding": {"x": {"datum": 0, "type": "quantitative"}, "text": {"field": "period"}}},
            {"transform": [{"filter": "datum.period_order === 4"}, {"calculate": "(datum.main + datum.total) / 2", "as": "mid"}],
             "mark": {"type": "text", "align": "center", "baseline": "middle", "dy": BAR_SHIFT, "style": "annotation", "color": "@ink"},
             "encoding": {"x": {"field": "mid", "type": "quantitative"}, "text": {"value": bi("Reserve", "reserve")}}},
            {"mark": {"type": "text", "align": "left", "baseline": "middle", "dx": 6, "dy": BAR_SHIFT, "style": "label"},
             "encoding": {"x": {"field": "total", "type": "quantitative"}, "text": {"field": "total_label"}}},
        ],
    },
}

# ---------------------------------------------------------------- texts
n = de_num
e = en_num
summary = bi(
    f"Nach Brückner zählte der Landtag {seats_all} Mitglieder, davon {seats_elected} aus Wahlen der Städte und der übrigen Gemeinden. Ein städtischer Abgeordneter vertrat {n(per_seat_towns)} Einwohner, ein ländlicher {n(per_seat_rural)}. Die drei Landesteile hatten {tot['Gendarmen']} Gendarmen, {tot['Ärzte']} promovierte Ärzte und {tot['Justizämter']} Justizämter. Das Militärkontingent stieg von {cont_first} Mann nach der alten Reichsmatrikel auf {cont_last} Mann im Norddeutschen Bund (1867).",
    f"According to Brückner the Landtag had {seats_all} members, {seats_elected} of them elected by the towns and the other communities. An urban deputy represented {e(per_seat_towns)} inhabitants, a rural deputy {e(per_seat_rural)}. The three districts together had {tot['Gendarmen']} gendarmes, {tot['Ärzte']} physicians with a doctorate and {tot['Justizämter']} Justizämter. The military contingent grew from {cont_first} men under the old imperial register to {cont_last} men in the North German Confederation (1867).")

p10 = lambda m, d: stats[(m, d)][0]
ps = lambda m, d: stats[(m, d)][1]
doc_lo = min(p10("Ärzte", d) for d in pop)
doc_hi = max(p10("Ärzte", d) for d in pop)
gen_lo = p10("Gendarmen", GERA)
gen_hi = p10("Gendarmen", LOBE)
gen_a_lo = min(ps("Gendarmen", d) for d in pop)
gen_a_hi = max(ps("Gendarmen", d) for d in pop)

findings = [
    bi(f"Die Städte stellten {seats_towns} von {seats_elected} von den Gemeinden gewählten Abgeordneten, hatten aber nur {n(pop_share_towns)} Prozent der Einwohner. Ein ländlicher Sitz entsprach {n(per_seat_rural)} Einwohnern, ein städtischer {n(per_seat_towns)} (Faktor {n(factor_seat, 1)}).",
       f"The towns held {seats_towns} of the {seats_elected} seats elected by the communities but had only {e(pop_share_towns)} percent of the inhabitants. One rural seat corresponded to {e(per_seat_rural)} inhabitants, one urban seat to {e(per_seat_towns)} (factor {e(factor_seat, 1)})."),
    bi(f"Je Einwohner schwankte die Zahl der Ärzte kaum ({n(doc_lo, 1)} bis {n(doc_hi, 1)} je 10.000), die der Gendarmen stark ({n(gen_lo, 1)} im Landesteil Gera, {n(gen_hi, 1)} in Lobenstein-Ebersdorf). Je Quadratmeile lagen die Gendarmen näher beieinander ({n(gen_a_lo, 1)} bis {n(gen_a_hi, 1)}).",
       f"Physicians per inhabitant hardly varied ({e(doc_lo, 1)} to {e(doc_hi, 1)} per 10,000), gendarmes a great deal ({e(gen_lo, 1)} in the Gera district, {e(gen_hi, 1)} in Lobenstein-Ebersdorf). Per square mile gendarmes ranged only from {e(gen_a_lo, 1)} to {e(gen_a_hi, 1)}."),
    bi(f"Das zu stellende Kontingent wuchs von {cont_first} Mann (Reichsmatrikel bis 1681) auf {cont_last} Mann (1867), fast auf das {n(factor_cont)}fache.",
       f"The contingent to be provided grew from {cont_first} men (imperial register until 1681) to {cont_last} men (1867), almost {e(factor_cont)}-fold."),
]

method = bi(
    "Quellen sind die Abschnitte zu Verfassung, Militär und Staatsverwaltung (S. 267 bis 281) und die Bevölkerungstabellen (S. 93 bis 96). Die Sitzverteilung des Landtags steht im Fließtext S. 268; Zahlwörter wurden in Ziffern übertragen. Die Einwohner der sechs Städte und der übrigen Gemeinden 1867 sind die Summen der drei Landesteile aus der Tabelle S. 95. Der dort gedruckte Landeswert für die ländliche Bevölkerung (58052) ist ein Druckfehler und wird nicht verwendet. Anteile und Einwohner je Sitz sind berechnet. Die vier Sitze des Köstritzer Paragiums und der Rittergutsbesitzer (als eigene Gruppe gewählt) bleiben außerhalb der Rechnung, weil Brückner dafür keine Einwohner- oder Wählerzahl nennt. Gendarmen (S. 273) und promovierte Ärzte (S. 274) stehen im Fließtext. Die acht Justizämter (S. 280) sind den Landesteilen nach dem Sitz des Amtes zugeordnet: Gera I und II; Schleiz I und II sowie Hohenleuben; Lobenstein I und II sowie Hirschberg. Die Flächen der Landesteile in Quadratmeilen stammen aus den Landesteilartikeln (S. 407, 574, 709). Für jedes Merkmal wurde die Zahl je Einwohner und je Quadratmeile berechnet und auf den Landesdurchschnitt (= 100) bezogen. Die Reihe des Militärkontingents (S. 271) ordnet Brückners Angaben zu sechs Zeitabschnitten; für die Zeit ab 1842 wird die Reserve von 261 Mann als unverändert angenommen (608 + 261 = 869, wie Brückner für das Bataillon angibt). Die Größen der Gemeinderäte nach Einwohnerklasse (S. 269) stehen als weitere Tabelle zum Herunterladen.",
    "Sources are the sections on constitution, military and administration (pp. 267 to 281) and the population tables (pp. 93 to 96). The seat allocation of the Landtag is in the running text of p. 268; numerals written as words were converted into digits. The inhabitants of the six towns and of the other communities in 1867 are the sums of the three districts from the table on p. 95. The national figure printed there for the rural population (58052) is a misprint and is not used. Shares and inhabitants per seat are calculated. The four seats of the Köstritz appanage and the manor owners (elected as a group of their own) are left out of the calculation because Brückner gives no population or voters for them. Gendarmes (p. 273) and physicians with a doctorate (p. 274) are given in the running text. The eight Justizämter (p. 280) are assigned to the districts by the seat of the office: Gera I and II; Schleiz I and II and Hohenleuben; Lobenstein I and II and Hirschberg. District areas in square miles come from the district articles (pp. 407, 574, 709). Each measure was calculated per inhabitant and per square mile and related to the national average (= 100). The contingent series (p. 271) arranges Brückner’s statements into six periods; for the time from 1842 the reserve of 261 men is assumed unchanged (608 + 261 = 869, as Brückner gives for the battalion). The sizes of the municipal councils by population class (p. 269) are a further table for download.")

caveats = [
    bi("Brückner nennt weder Wahlberechtigte noch Einwohner je Wahlkörper. Die Rechnung bezieht die Sitze auf die gesamte Bevölkerung 1867, nicht auf die Wähler. Wahlberechtigt waren nur Staatsangehörige mit Ortsbürgerrecht, Volljährigkeit, Eintrag in der Steuerrolle und christlichem Bekenntnis (S. 268); das Verhältnis der Wähler kann deshalb anders ausfallen.",
       "Brückner gives neither the eligible voters nor the inhabitants per electoral body. The calculation relates the seats to the whole population of 1867, not to the voters. Only nationals with local citizenship, full age, an entry in the tax roll and a Christian confession were entitled to vote (p. 268); the ratio per voter may therefore differ."),
    bi("Gendarmen und Ärzte gelten für den Stand der Beschreibung (1868/69), die Einwohner für 1867. Gezählt sind nur promovierte Ärzte. Das Amt Hohenleuben gehört zum Kreisgericht Gera, liegt aber im Landesteil Schleiz und wird hier diesem zugerechnet. Mit 2 bis 14 Stellen je Gruppe sind die Indexwerte grob; dass die Verteilung der Fläche folgte, ist eine Deutung.",
       "Gendarmes and physicians apply to 1868/69, the inhabitants to 1867. Only physicians with a doctorate are counted. The Hohenleuben office belongs to the Gera district court but lies in the Schleiz district and is counted there. With 2 to 14 posts per group the index values are rough; that the distribution followed the area is an interpretation."),
    bi("Brückner schreibt, das Hauptkontingent sei 1842 »um 87 Mann, also auf 608« erhöht worden; 522 + 87 ergibt 609. Der Widerspruch steht im Druck (Faksimile geprüft), verwendet wird 608. Bis 1681 gilt die Zahl für ganz Reuß; die Spitzen der Kriegszeit (das Vier- bis Fünffache) fehlen in der Reihe.",
       "Brückner writes that the main contingent was raised in 1842 “by 87 men, i.e. to 608”; 522 + 87 makes 609. The contradiction is in the print (facsimile checked); 608 is used. Until 1681 the figure applies to all of Reuss; the peaks of wartime (four to five times as many) are not in the series."),
]

transcription = [
    {"page": "271", "block": "b4", "transcribed": "608", "facsimile": "608", "checked_facsimile": True,
     "note": "Rechenfehler im Druck: 522 + 87 = 609. Die Transkription entspricht dem Druck."},
    {"page": "95", "block": "b4", "cell": "r25c3", "transcribed": "58052", "facsimile": "58052", "checked_facsimile": True,
     "note": "Druckfehler im Original; richtig 59052 (28922 + 59052 = 87974). Der Wert wird nicht verwendet; die Summe stammt aus den Landesteilzeilen r7, r13, r19."},
]

obj = {
    "id": FID,
    "title": bi("Landtag, Verwaltung und Militär", "Landtag, administration and military"),
    "category": "state",
    "section": "t1-4-1b",
    "merges": ["verfassung-landtag-gemeinderaete-vertretung", "verwaltung-aerzte-gendarmen-justizaemter-landestheile", "militaer-kontingent-reichsmatrikel-bis-1867"],
    "sources": [ref(267, "b3"), ref(268, "b1"), ref(268, "b2"), ref(268, "b3"), ref(269, "b2"), ref(271, "b3"), ref(271, "b4"),
                ref(273, "b3"), ref(274, "b1"), ref(280, "b5"), ref(281, "b1"), ref(95, "b4", "r7, r13, r19"), ref(93, "b4"),
                ref(407, "b3"), ref(574, "b1"), ref(709, "b2")],
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "datasets": [ds_rep, ds_off, ds_cont, ds_landtag, ds_council],
    "charts": [c1, c2, c3],
    "transcription_issues": transcription,
    "keywords": {
        "de": ["Landtag", "Landesvertretung", "Wahlrecht", "Abgeordnete", "Rittergutsbesitzer", "Gemeinderat", "Gendarmerie", "Ärzte", "Justizämter", "Militär", "Kontingent", "Reichsmatrikel", "Norddeutscher Bund"],
        "en": ["Landtag", "representation", "suffrage", "deputies", "manor owners", "municipal council", "gendarmerie", "physicians", "Justizämter", "military", "contingent", "imperial register", "North German Confederation"],
    },
    "related": ["bevoelkerung-1647-1867", "rechtspflege", "staatsfinanzen", "gesundheit"],
    "date": "2026-10-02",
}

if __name__ == "__main__":
    probs = check_limits(obj)
    print("limit problems:", probs)
    print(write_feature(obj))
    ok = validate(FID)
    print("OK" if ok else "FAIL")
