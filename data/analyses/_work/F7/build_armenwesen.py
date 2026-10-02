"""Feature F7c: armenwesen-stiftungen (Armenpflege, Kassen und Stiftungen)."""
import json
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F7")
from common import *

FID = "armenwesen-stiftungen"
n, e = de_num, en_num

A_SOC = "armenwesen-selbsthilfe-kassen-gruendungsjahre-1777-1869"
A_FOU = "armenwesen-stiftungen-kapital-1828-1866"
A_STI = "schule-stipendien-stiftungen-betraege-gruendung"

soc_src = archive_dataset(A_SOC, "societies")
fou_src = archive_dataset(A_FOU, "foundations")
sti_src = archive_dataset(A_STI, "stipends")
cap_src = archive_dataset(A_STI, "capital_only")
soc = rows_as_dicts(soc_src)
fou = rows_as_dicts(fou_src)
sti = rows_as_dicts(sti_src)
cap = rows_as_dicts(cap_src)

# ---------------------------------------------------------------- places named by each society (print, p. 302 to 303)
PLACES = {
    "a1": ["Schleiz"], "a2": ["Schleiz"], "a3": ["Hirschberg"], "a4": ["Hirschberg"], "a5": ["Wurzbach"], "a6": ["Harra"], "a7": ["Tanna"],
    "a8": ["Gera"], "a9": ["Gera"],
    "b1": ["Gera", "Untermhaus", "Cuba", "Debschwitz", "Pforten", "Bieblach", "Pöppeln"],
    "b2": ["Gera"], "b3": ["Gera"],
    "b4": ["Triebes", "Niederböhmsdorf", "Weißendorf"],
    "b5": ["Langenberg"], "b6": ["Roschitz"], "b7": ["Gera"], "b8": ["Gera"], "b9": ["Frankenthal"], "b10": ["Naundorf"],
    "b11": ["Leumnitz", "Laasen", "Trebnitz", "Zwötzen", "Zschippern", "Kaimberg"],
    "b12": ["Hohenleuben"],
    "b13": ["Dürrenebersdorf", "Weißig", "Zeulsdorf"],
    "c1": ["Grüna", "Stübnitz", "Rüdersdorf", "Hartmannsdorf"], "c2": ["Großsaara"], "c3": ["Gera"], "c4": ["Köstritz"],
    "c5": ["Langenberg"], "c6": ["Gera"], "c7": ["Gera"], "c8": ["Gera"],
    "d1": ["Schleiz"], "d2": ["Gera"],
}
assert set(PLACES) == {r["key"] for r in soc}
base_places = shared_dataset("base_places.json")
base_rivers = shared_dataset("base_rivers.json")
base_by_name = {}
for r in base_places["rows"]:
    base_by_name.setdefault(r[0], []).append(r)

place_count = {}
for k, ps in PLACES.items():
    for p in ps:
        place_count[p] = place_count.get(p, 0) + 1
place_rows = []
for p, c in sorted(place_count.items(), key=lambda t: (-t[1], t[0])):
    b = base_by_name.get(p)
    place_rows.append([p, b[0][3] if b else None, c, b[0][1] if b else None, b[0][2] if b else None])
no_coord = [r[0] for r in place_rows if r[3] is None]
school_lt = {r["name"]: r["landestheil"] for r in rows_as_dicts(archive_dataset("orte-schulen-gemeindehaushalt", "schools"))}
first_region = {}
for r in soc:
    first = PLACES[r["key"]][0]
    b = base_by_name.get(first)
    first_region[r["key"]] = (b[0][3] if b else None) or school_lt.get(first)
region_count = {}
for k, v in first_region.items():
    region_count[v] = region_count.get(v, 0) + 1
n_soc = len(soc)
gera_n = region_count["Gera"]
assert sum(region_count.values()) == n_soc
n_places = len(place_rows)

# ---------------------------------------------------------------- the common timeline of all dated institutions
KIND = {"Stipendium": (1, "Stipendien und Schulstiftungen", "Stipends and school foundations"),
        "Armenstiftung": (2, "Stiftungen für Arme", "Foundations for the poor"),
        "Selbsthilfe": (3, "Selbsthilfe der Arbeiter", "Self-help of the workers")}
tl = []
for r in soc:
    tl.append(("Selbsthilfe", "S-" + r["key"], f"{r['type_de']}: {r['place_de']}", f"{r['type_en']}: {r['place_en']}", r["year"]))
for r in sti:
    if r["year"] is not None:
        tl.append(("Stipendium", "T-" + r["key"], r["name_de"], r["name_en"], r["year"]))
for r in cap:
    tl.append(("Stipendium", "T-" + r["key"], r["name_de"], r["name_en"], r["year"]))
for r in fou:
    if r["year"] is not None:
        tl.append(("Armenstiftung", "F-" + r["key"], r["name_de"], r["name_en"], r["year"]))
tl.sort(key=lambda t: (t[4], KIND[t[0]][0], t[1]))
tl_rows = [[key, kind, KIND[kind][0], KIND[kind][1], KIND[kind][2], de, en, yr, yr // 10 * 10, yr // 10 * 10 + 10] for kind, key, de, en, yr in tl]
count_kind = {k: sum(1 for t in tl if t[0] == k) for k in KIND}
soc_1860s = sum(1 for r in soc if 1860 <= r["year"] <= 1869)
soc_before_1850 = sum(1 for r in soc if r["year"] < 1850)
first_stipend = min(t[4] for t in tl if t[0] == "Stipendium")
last_year = max(t[4] for t in tl)

refs_union = []
seen = set()
for src in (soc_src, fou_src, sti_src, cap_src):
    for r in src["source_refs"]:
        k = (r["page"], r["block"])
        if k not in seen:
            seen.add(k)
            refs_union.append({"page": r["page"], "block": r["block"]})

ds_tl = dataset(
    "gruendungen",
    bi("Gründungsjahre der erfassten Einrichtungen: Stipendien, Stiftungen für Arme, Selbsthilfe", "Founding years of the recorded institutions: stipends, foundations for the poor, self-help"),
    [col("key", "Kennung", "Key", "string", None, True),
     col("kind", "Art", "Kind", "string", None, True),
     col("kind_rank", "Reihenfolge der Art", "Order of the kind", "integer", None, True),
     col("kind_de", "Art", "Kind", "string", None, True),
     col("kind_en", "Art (englisch)", "Kind (English)", "string", None, True),
     col("name_de", "Einrichtung", "Institution", "string"),
     col("name_en", "Einrichtung (englisch)", "Institution (English)", "string"),
     col("year", "Gründungsjahr", "Year of founding", "integer", None, False, "Teils Jahr der Errichtung, des Testaments oder des Todes des Stifters"),
     col("decade", "Jahrzehnt", "Decade", "integer", None, True),
     col("decade_end", "Ende des Jahrzehnts", "End of the decade", "integer", None, True)],
    tl_rows,
    refs_union,
)

# ---------------------------------------------------------------- foundations with capital
LABEL = {
    "a": ("Christiane Louise Reuß (1828): verschiedene Zwecke", "Christiane Louise Reuss (1828): various purposes"),
    "b": ("Heinrich LXII.: verschämte Arme", "Heinrich LXII: needy poor"),
    "c": ("Heinrich LXII.: Dienstboten", "Heinrich LXII: servants"),
    "d": ("Heinrich LXVII. (1862): Waisen", "Heinrich LXVII (1862): orphans"),
    "e": ("Rettungshaus Hohenleuben (1853): Kinder", "Rescue house Hohenleuben (1853): children"),
    "f": ("Ebeling, Gera (1833): bedürftige Bürger", "Ebeling, Gera (1833): needy citizens"),
    "g": ("Friederici (1856): Armenfreischule", "Friederici (1856): free school for the poor"),
    "h": ("Münch, Gera (1854): arme Frauen", "Münch, Gera (1854): poor women"),
    "i": ("Zenker, Schleiz (1858): Hospitaliten", "Zenker, Schleiz (1858): hospital inmates"),
    "j": ("Gräfin Therese, Köstritz (1858): Witwen, Waisen", "Countess Therese, Köstritz (1858): widows, orphans"),
    "k": ("Bauer, Gera: Witwen, Waisen von Kaufleuten", "Bauer, Gera: widows, orphans of merchants"),
    "l": ("Dinger, Gera (1860): Wäscherinnen, Waisen", "Dinger, Gera (1860): washerwomen, orphans"),
    "m": ("Ungenannter, Gera (1854): Kranke", "Anonymous, Gera (1854): the sick"),
}
fou_rows = []
for r in sorted(fou, key=lambda r: -r["capital"]):
    fou_rows.append([r["key"], LABEL[r["key"]][0], LABEL[r["key"]][1], r["group_de"], r["group_en"], r["purpose_de"], r["purpose_en"],
                     r["capital"], r["year"], r["year_de"], r["year_en"], r["income"], r["yield"]])
cap_total = sum(r["capital"] for r in fou)
cap_first = max(r["capital"] for r in fou)
cap_rest = cap_total - cap_first
cap_prince = sum(r["capital"] for r in fou if r["group_de"] == "Fürstenhaus")
cap_private = cap_total - cap_prince
assert cap_total == 49010 and cap_first == 30000
n_fou = len(fou)

ds_fou = dataset(
    "foundations",
    bi("Stiftungen für Arme, Waisen und Bedürftige mit genanntem Kapital", "Foundations for the poor, orphans and the needy with a stated capital"),
    [col("key", "Kennung", "Key", "string"),
     col("label_de", "Bezeichnung", "Label", "string", None, True),
     col("label_en", "Bezeichnung (englisch)", "Label (English)", "string", None, True),
     col("group_de", "Stifter", "Donor", "string"),
     col("group_en", "Stifter (englisch)", "Donor (English)", "string"),
     col("purpose_de", "Zweck", "Purpose", "string"),
     col("purpose_en", "Zweck (englisch)", "Purpose (English)", "string"),
     col("capital", "Kapital", "Capital", "integer", "Taler", False, "Dinger-Stiftung: 200 + 500 Taler"),
     col("year", "Jahr", "Year", "integer"),
     col("year_de", "Zeitpunkt", "Point in time", "string"),
     col("year_en", "Zeitpunkt (englisch)", "Point in time (English)", "string"),
     col("income", "Jahresertrag", "Annual income", "integer", "Taler"),
     col("yield", "Verzinsung", "Yield", "number", "%", True)],
    fou_rows,
    fou_src["source_refs"],
)

# ---------------------------------------------------------------- self-help societies (download) and places (map)
soc_rows = [[r["key"], r["type_de"], r["type_en"], r["place_de"], r["place_en"], "; ".join(PLACES[r["key"]]), r["year"], r["region_de"], r["region_en"]] for r in soc]
ds_soc = dataset(
    "societies",
    bi("Selbsthilfeeinrichtungen mit Gründungsjahr und genannten Orten", "Self-help institutions with founding year and named places"),
    [col("key", "Kennung", "Key", "string"),
     col("type_de", "Art", "Type", "string"),
     col("type_en", "Art (englisch)", "Type (English)", "string"),
     col("place_de", "Ort und Mitglieder", "Place and members", "string"),
     col("place_en", "Ort und Mitglieder (englisch)", "Place and members (English)", "string"),
     col("places", "Genannte Orte", "Named places", "string", None, True, "Orte in Brückners Wortlaut, durch Semikolon getrennt"),
     col("year", "Gründungsjahr", "Year of founding", "integer"),
     col("region_de", "Gebiet (redaktionell)", "Area (editorial)", "string", None, True),
     col("region_en", "Gebiet (englisch)", "Area (English)", "string", None, True)],
    soc_rows,
    soc_src["source_refs"],
)
ds_orte = dataset(
    "selbsthilfe_orte",
    bi("Orte mit Selbsthilfeeinrichtungen", "Places with self-help institutions"),
    [col("place", "Ort", "Place", "string"),
     col("landestheil", "Landesteil", "District", "string", None, True),
     col("institutions", "Einrichtungen, die den Ort nennen", "Institutions naming the place", "integer", "Einrichtungen", True),
     col("lon", "Länge", "Longitude", "number", "°", True, "GeoNames"),
     col("lat", "Breite", "Latitude", "number", "°", True, "GeoNames")],
    place_rows,
    [r for r in soc_src["source_refs"] if (r["page"], r["block"]) not in {("303", "b3"), ("303", "b4")}],
)

sti_rows = [[r["name_de"], r["name_en"], r["level_de"], r["level_en"], r["founder_de"], r["founder_en"], r["place"], r["year"],
             r["recipients"], r["per_recipient"], r["annual_total"], r["capital"]] for r in sti]
ds_sti = dataset(
    "stipends",
    bi("Stipendien und Schulstiftungen mit Jahresbetrag", "Stipends and school foundations with an annual amount"),
    [col("name_de", "Stipendium", "Stipend", "string"),
     col("name_en", "Stipendium (englisch)", "Stipend (English)", "string"),
     col("level_de", "Stufe", "Level", "string"),
     col("level_en", "Stufe (englisch)", "Level (English)", "string"),
     col("founder_de", "Stifter", "Donor", "string"),
     col("founder_en", "Stifter (englisch)", "Donor (English)", "string"),
     col("place", "Ort", "Place", "string"),
     col("year", "Gründungsjahr", "Year of founding", "integer"),
     col("recipients", "Stipendiaten", "Recipients", "integer", "Personen", True),
     col("per_recipient", "Betrag je Stipendiat", "Amount per recipient", "number", "Taler", True),
     col("annual_total", "Jahresbetrag insgesamt", "Annual total", "number", "Taler", True),
     col("capital", "Kapital", "Capital", "integer", "Taler")],
    sti_rows,
    sti_src["source_refs"],
)
sti_total = sum(r["annual_total"] for r in sti)
n_sti = len(sti)

# ---------------------------------------------------------------- charts
KIND_DOMAIN = ["Stipendium", "Armenstiftung", "Selbsthilfe"]
KIND_RANGE = ["@accent", "@accent3", "@accent2"]


def key_of(kind, year=None, pick=0):
    xs = [t for t in tl if t[0] == kind and (year is None or t[4] == year)]
    return xs[pick][1]


# tallest stack per decade, to place the labels
stack_h = {}
for t in tl:
    d = t[4] // 10 * 10
    stack_h[d] = stack_h.get(d, 0) + 1
sti_label_key = key_of("Stipendium", 1696)
fou_label_key = key_of("Armenstiftung", 1853)
soc_label_key = key_of("Selbsthilfe", 1865)

c1 = {
    "id": "c1",
    "dataset": "gruendungen",
    "title": bi(f"Die erfassten Stipendien beginnen {first_stipend}, {soc_1860s} von {n_soc} Selbsthilfekassen entstanden 1860 bis 1869",
                f"The recorded stipends begin in {first_stipend}, {soc_1860s} of {n_soc} self-help societies arose from 1860 to 1869"),
    "caption": bi(
        f"Gründungsjahr aller {len(tl)} datierten Stipendien, Stiftungen für Arme und Selbsthilfeeinrichtungen, je Jahrzehnt; ein Block ist eine Einrichtung. Nicht datiert sind {n_fou + n_sti - count_kind['Armenstiftung'] - sum(1 for r in sti if r['year'] is not None)} weitere. Quelle: S. 302 bis 310.",
        f"Founding year of all {len(tl)} dated stipends, foundations for the poor and self-help institutions, by decade; one block is one institution. {n_fou + n_sti - count_kind['Armenstiftung'] - sum(1 for r in sti if r['year'] is not None)} further ones are undated. Source: pp. 302 to 310."),
    "vegalite": {
        "height": 320,
        "encoding": {
            "x": {"field": "decade", "type": "quantitative", "scale": {"domain": [1600, 1872], "nice": False},
                  "axis": {"values": [1600, 1650, 1700, 1750, 1800, 1850], "format": "d", "title": None, "labelOverlap": False}},
            "y": {"type": "quantitative", "scale": {"domain": [0, 30]}, "axis": {"title": bi("Zahl der Einrichtungen", "Number of institutions"), "tickCount": 6}},
        },
        "layer": [
            {"mark": {"type": "bar", "stroke": "@paper", "strokeWidth": 1.2, "cornerRadiusEnd": 0},
             "encoding": {
                 "x2": {"field": "decade_end"},
                 "y": {"aggregate": "count", "type": "quantitative", "scale": {"domain": [0, 30]}, "axis": {"title": bi("Zahl der Einrichtungen", "Number of institutions"), "tickCount": 6}},
                 "color": {"field": "kind", "type": "nominal", "legend": None, "scale": {"domain": KIND_DOMAIN, "range": KIND_RANGE}},
                 "order": {"field": "kind_rank", "type": "quantitative"},
                 "tooltip": [{"field": "name_de", "title": bi("Einrichtung", "Institution")},
                             {"field": "kind_de", "title": bi("Art", "Kind")},
                             {"field": "year", "title": bi("Jahr", "Year")}]}},
            {"transform": [{"filter": f"datum.key === '{sti_label_key}'"}],
             "mark": {"type": "text", "align": "center", "baseline": "bottom", "dy": -8, "style": "label"},
             "encoding": {"x": {"datum": 1700, "type": "quantitative"}, "y": {"datum": 3.2, "type": "quantitative"}, "color": {"value": "@accent"},
                          "text": {"value": bi("Stipendien und Schulstiftungen", "Stipends and school foundations")}}},
            {"transform": [{"filter": f"datum.key === '{fou_label_key}'"}],
             "mark": {"type": "text", "align": "right", "baseline": "middle", "dx": -4, "style": "label"},
             "encoding": {"x": {"datum": 1850, "type": "quantitative"}, "y": {"datum": 9.5, "type": "quantitative"}, "color": {"value": "@accent3"},
                          "text": {"value": bi("Stiftungen für Arme", "Foundations for the poor")}}},
            {"transform": [{"filter": f"datum.key === '{soc_label_key}'"}],
             "mark": {"type": "text", "align": "right", "baseline": "middle", "dx": -4, "style": "label"},
             "encoding": {"x": {"datum": 1860, "type": "quantitative"}, "y": {"datum": 22, "type": "quantitative"}, "color": {"value": "@accent2"},
                          "text": {"value": bi(f"Selbsthilfe der Arbeiter: {soc_1860s} Gründungen 1860 bis 1869", f"Self-help of the workers: {soc_1860s} foundings from 1860 to 1869")}}},
        ],
    },
}

c2 = {
    "id": "c2",
    "dataset": "foundations",
    "title": bi("Das Kapital der Fürstin Christiane Louise von 1828 übertraf die zwölf übrigen Stiftungen zusammen",
                "Princess Christiane Louise’s capital of 1828 exceeded the twelve other foundations together"),
    "caption": bi(
        f"Kapital der {n_fou} Stiftungen für Arme, Waisen und Bedürftige, für die Brückner ein Kapital in Talern nennt; zusammen {n(cap_total)} Taler. Gestrichelt: Kapital aller übrigen zusammen. Quelle: S. 308 bis 310.",
        f"Capital of the {n_fou} foundations for the poor, orphans and the needy for which Brückner states a capital in thalers; together {e(cap_total)} thalers. Dashed: capital of all the others together. Source: pp. 308 to 310."),
    "vegalite": {
        "height": {"step": 26},
        "transform": [{"calculate": {"de": "datum.label_de", "en": "datum.label_en"}, "as": "label"}],
        "encoding": {"y": {"field": "label", "type": "nominal", "sort": [bi(r[1], r[2]) for r in fou_rows],
                           "axis": {"title": None, "labelLimit": 520, "ticks": False, "domain": False}}},
        "layer": [
            {"mark": {"type": "bar", "height": 15},
             "encoding": {"x": {"field": "capital", "type": "quantitative", "scale": {"domain": [0, 36000]},
                                "axis": {"title": bi("Kapital in Taler", "Capital in thalers"), "values": [0, 10000, 20000, 30000], "format": ",d", "labelOverlap": False}},
                          "color": {"condition": {"test": f"datum.capital === {cap_first}", "value": "@accent3"}, "value": "@context"},
                          "tooltip": [{"field": "label", "title": bi("Stiftung", "Foundation")},
                                      {"field": "group_de", "title": bi("Stifter", "Donor")},
                                      {"field": "capital", "title": bi("Kapital in Taler", "Capital in thalers"), "format": ",d"},
                                      {"field": "year_de", "title": bi("Zeitpunkt", "Point in time")}]}},
            {"mark": {"type": "rule", "strokeDash": [4, 3], "color": "@ink2"},
             "encoding": {"x": {"datum": cap_rest, "type": "quantitative"}, "y": None}},
            {"transform": [{"filter": f"datum.capital === {cap_first}"}],
             "mark": {"type": "text", "align": "right", "baseline": "bottom", "dx": -4, "dy": -17, "style": "annotation"},
             "encoding": {"x": {"datum": cap_rest, "type": "quantitative"}, "y": {"value": 0},
                          "text": {"value": bi(f"alle übrigen zusammen: {n(cap_rest)}", f"all the others together: {e(cap_rest)}")}}},
            {"mark": {"type": "text", "align": "left", "dx": 6, "style": "label"},
             "encoding": {"x": {"field": "capital", "type": "quantitative"}, "text": {"field": "capital", "format": ",d"}}},
        ],
    },
}

LON = {"field": "lon", "type": "quantitative"}
LAT = {"field": "lat", "type": "quantitative"}


def panel(title, center, scale, width, height, labels, with_legend, bar_at, bbox, labels_left=()):
    flt = "indexof(" + json.dumps(labels, ensure_ascii=False).replace('"', "'") + ", datum.place) >= 0 && isValid(datum.lon)"
    flt_left = "indexof(" + json.dumps(list(labels_left), ensure_ascii=False).replace('"', "'") + ", datum.place) >= 0 && isValid(datum.lon)"
    west, east, south, north = bbox
    geo = f"datum.lon > {west} && datum.lon < {east} && datum.lat > {south} && datum.lat < {north}"
    lon0, lat0 = bar_at
    dlon = 5 / (111.32 * 0.634)
    size_legend = ({"title": bi("Einrichtungen", "Institutions"), "values": [1, 3, 6, 12], "orient": "none", "legendX": width - 132, "legendY": height - 150, "direction": "vertical",
                    "symbolFillColor": "@muted", "symbolStrokeColor": "@paper"} if with_legend else None)
    return {
        "title": {"text": title, "anchor": "start", "fontSize": 12, "fontWeight": 600, "offset": 6},
        "width": width, "height": height,
        "view": {"stroke": "@context", "strokeWidth": 1},
        "projection": {"type": "mercator", "center": center, "scale": scale, "translate": [width / 2, height / 2]},
        "layer": [
            {"data": {"name": "fluesse_basis"}, "transform": [{"filter": geo}], "mark": {"type": "line", "color": "@river", "strokeWidth": 1.2},
             "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                          "detail": {"field": "abschnitt"}, "order": {"field": "folge"}}},
            {"data": {"name": "orte_basis"}, "transform": [{"filter": geo}], "mark": {"type": "circle", "size": 10, "color": "@land", "opacity": 1},
             "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"}}},
            {"transform": [{"filter": "isValid(datum.lon) && " + geo}],
             "mark": {"type": "circle", "color": "@accent2", "stroke": "@paper", "strokeWidth": 0.8, "opacity": 0.88},
             "encoding": {"longitude": LON, "latitude": LAT,
                          "size": {"field": "institutions", "type": "quantitative", "scale": {"type": "sqrt", "domain": [0, 12], "range": [40, 1300]}, "legend": size_legend},
                          "tooltip": [{"field": "place", "title": bi("Ort", "Place")},
                                      {"field": "landestheil", "title": bi("Landesteil", "District")},
                                      {"field": "institutions", "title": bi("Einrichtungen, die den Ort nennen", "Institutions naming the place")}]}},
            {"transform": [{"filter": flt}], "mark": {"type": "text", "style": "place-halo", "dy": -11},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}}},
            {"transform": [{"filter": flt}], "mark": {"type": "text", "style": "place-label", "dy": -11},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}}},
            {"transform": [{"filter": flt_left}], "mark": {"type": "text", "style": "place-halo", "align": "right", "dx": -9, "dy": 0},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}}},
            {"transform": [{"filter": flt_left}], "mark": {"type": "text", "style": "place-label", "align": "right", "dx": -9, "dy": 0},
             "encoding": {"longitude": LON, "latitude": LAT, "text": {"field": "place"}}},
            {"transform": [{"filter": "datum.place === 'Gera'"}], "mark": {"type": "rule", "color": "@ink2", "strokeWidth": 2},
             "encoding": {"longitude": {"datum": lon0}, "latitude": {"datum": lat0}, "longitude2": {"datum": lon0 + dlon}, "latitude2": {"datum": lat0}}},
            {"transform": [{"filter": "datum.place === 'Gera'"}], "mark": {"type": "text", "style": "annotation", "dy": -7},
             "encoding": {"longitude": {"datum": lon0 + dlon / 2}, "latitude": {"datum": lat0}, "text": {"value": "5 km"}}},
        ],
    }


c3 = {
    "id": "c3",
    "dataset": "selbsthilfe_orte",
    "extra_datasets": ["orte_basis", "fluesse_basis"],
    "title": bi("Die Selbsthilfe der Arbeiter konzentrierte sich auf Gera und sein Umland",
                "The self-help of the workers was concentrated on Gera and its surroundings"),
    "caption": bi(
        f"Orte, die Brückner bei den {n_soc} Selbsthilfeeinrichtungen nennt; die Größe zeigt, wie viele Einrichtungen den Ort nennen, ein Verein für mehrere Orte zählt bei jedem. {len(no_coord)} Orte ohne Koordinaten fehlen. Quelle: S. 302 bis 303.",
        f"Places that Brückner names for the {n_soc} self-help institutions; the size shows how many institutions name the place, a society for several places counts for each. {len(no_coord)} places without coordinates are missing. Source: pp. 302 to 303."),
    "vegalite": {
        "hconcat": [
            panel(bi("Unterland (Landesteil Gera)", "Unterland (Gera district)"), [12.112, 50.89], 74000, 418, 400,
                  ["Gera", "Köstritz", "Langenberg", "Frankenthal", "Großsaara", "Trebnitz", "Kaimberg", "Weißig"], False, (11.955, 50.815), (11.86, 12.34, 50.74, 51.05), ["Naundorf"]),
            panel(bi("Oberland (Schleiz, Lobenstein-Ebersdorf)", "Oberland (Schleiz, Lobenstein-Ebersdorf)"), [11.80, 50.56], 37000, 418, 400,
                  ["Schleiz", "Hirschberg", "Tanna", "Wurzbach", "Harra", "Hohenleuben", "Triebes"], True, (12.0, 50.43), (11.30, 12.35, 50.28, 50.80)),
        ],
        "spacing": 8,
        "resolve": {"legend": {"color": "independent", "size": "independent"}},
    },
}

# ---------------------------------------------------------------- texts
soc_dated_before = soc_before_1850
undated = n_fou + n_sti - count_kind["Armenstiftung"] - sum(1 for r in sti if r["year"] is not None)
summary = bi(
    f"Brückner nennt {n_soc} Selbsthilfeeinrichtungen der arbeitenden Klassen mit Gründungsjahr, {n_fou} Stiftungen für Arme mit {n(cap_total)} Taler Kapital und {n_sti} Stipendien mit {n(round(sti_total))} Taler Jahresbetrag, die ältesten von {first_stipend}. {soc_1860s} der {n_soc} Selbsthilfeeinrichtungen entstanden 1860 bis 1869. Die Stiftungen der Fürstin Christiane Louise von 1828 hielten {n(cap_first)} Taler.",
    f"Brückner names {n_soc} self-help institutions of the working classes with a founding year, {n_fou} foundations for the poor with {e(cap_total)} thalers of capital and {n_sti} stipends with {e(round(sti_total))} thalers a year, the oldest of {first_stipend}. {soc_1860s} of the {n_soc} self-help institutions arose from 1860 to 1869. The foundations of Princess Christiane Louise of 1828 held {e(cap_first)} thalers.")

findings = [
    bi(f"Nur {soc_dated_before} der {n_soc} Selbsthilfeeinrichtungen entstanden vor 1850, {soc_1860s} dagegen 1860 bis 1869; die meisten Gründungen eines Jahres fielen auf 1866 und 1867 mit je {max(sum(1 for r in soc if r['year'] == y) for y in (1866, 1867))}.",
       f"Only {soc_dated_before} of the {n_soc} self-help institutions arose before 1850, {soc_1860s} from 1860 to 1869; the most foundings in one year fell on 1866 and 1867 with {max(sum(1 for r in soc if r['year'] == y) for y in (1866, 1867))} each."),
    bi(f"Die Stiftungen der Fürstin Christiane Louise ({n(cap_first)} Taler, {n(cap_first / cap_total * 100)} Prozent des Kapitals) übertreffen alle übrigen zwölf zusammen ({n(cap_rest)}). Auf das Fürstenhaus entfielen {n(cap_prince / cap_total * 100)} Prozent des Kapitals.",
       f"The foundations of Princess Christiane Louise ({e(cap_first)} thalers, {e(cap_first / cap_total * 100)} percent of the capital) exceed all twelve others together ({e(cap_rest)}). The princely house accounted for {e(cap_prince / cap_total * 100)} percent of the capital."),
    bi(f"Brückner nennt die Selbsthilfe »mehr im geraer und reichenfelser Gebiete« entwickelt: {gera_n} der {n_soc} Einrichtungen lagen im Landesteil Gera, {region_count['Schleiz']} in Schleiz, {region_count['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf; allein {place_count['Gera']} nennen die Stadt Gera.",
       f"Brückner calls self-help more developed “in the Gera and Reichenfels area”: {gera_n} of the {n_soc} institutions lay in the Gera district, {region_count['Schleiz']} in Schleiz, {region_count['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf; {place_count['Gera']} name the town of Gera alone."),
]

method = bi(
    f"Aus den Aufzählungen S. 302 bis 310 wurden alle Einrichtungen mit Gründungsjahr erfasst: {n_soc} Selbsthilfeeinrichtungen (Sterbekassen, Begräbnis- und Krankenkassen, Krankenunterstützungsvereine, zwei Vorschussvereine), {n_fou} Stiftungen für Arme mit Kapitalangabe (davon {count_kind['Armenstiftung']} mit Jahr) und Stipendien (davon {count_kind['Stipendium']} mit Jahr). Einrichtungen, die Brückner mit zwei Jahreszahlen nennt, zählen doppelt. Das Jahr bezeichnet teils die Errichtung, teils das Testament oder den Tod des Stifters. Das erste Diagramm ordnet die Einrichtungen nach Jahrzehnt. Das Kapital im zweiten Diagramm steht, wo Brückner es nennt, in Talern; bei der Dinger-Stiftung sind 200 und 500 Taler addiert. Die Orte im dritten Diagramm sind die in Brückners Aufzählung genannten Orte; ein Verein für mehrere Orte zählt bei jedem Ort, bei Wendungen wie »und Umgegend« nur der genannte Ort. Das Gebiet einer Einrichtung folgt dem Landesteil des zuerst genannten Ortes. Koordinaten stammen von GeoNames. Weitere Tabellen: die Stipendien mit Jahresbetrag und die Selbsthilfeeinrichtungen mit ihren Orten. Nicht übernommen sind die Mitglieder- und Bilanzzahlen der beiden Vorschussvereine (Ende 1867), die Verteilung der Stiftung von 1867 auf sieben Städte und Stiftungen ohne Kapital- oder Jahresangabe.",
    f"From the lists on pp. 302 to 310 all institutions with a founding year were recorded: {n_soc} self-help institutions (burial funds, burial and sickness funds, sickness-benefit societies, two credit associations), {n_fou} foundations for the poor with a stated capital ({count_kind['Armenstiftung']} of them with a year) and stipends ({count_kind['Stipendium']} of them with a year). Institutions that Brückner gives with two years count twice. The year denotes partly the establishment, partly the will or the death of the founder. The first chart arranges the institutions by decade. The capital in the second chart is given in thalers where Brückner states it; for the Dinger foundation 200 and 500 thalers are added. The places in the third chart are those named in Brückner’s lists; a society for several places counts for each place, with phrases such as “and surroundings” only the named place. The area of an institution follows the district of the place named first. Coordinates come from GeoNames. Further tables: the stipends with annual amount and the self-help institutions with their places. Not included are the member and balance figures of the two credit associations (end of 1867), the distribution of the 1867 foundation among seven towns and foundations without a capital or a year.")

caveats = [
    bi("Die Aufzählungen nennen Gründungsjahre, aber weder Mitglieder noch Kassenstände der Sterbe- und Krankenkassen; die Zahl der Einrichtungen sagt nichts über ihre Größe oder ihren Bestand 1868. Die Zahl der Stiftungen und Stipendien hängt davon ab, welche Brückner mit Jahr oder Betrag nennt."
       , "The lists give founding years but neither the members nor the funds of the burial and sickness societies; the number of institutions says nothing about their size or existence in 1868. The number of foundations and stipends depends on which of them Brückner gives with a year or an amount."),
    bi(f"Beim Kapital zählt nur, was Brückner in Talern nennt. Für Christiane Louise ist es das ursprüngliche Kapital; ob es 1868 noch bestand, sagt er nicht. Zahlreiche kleine Stiftungen (Gera allein hat »an 100 kleine Legate«), die Schleizer Legate in Mark und Aßo und {undated} Einrichtungen ohne Jahr fehlen im ersten Diagramm.",
       f"Capital counts only where Brückner states it in thalers. For Christiane Louise it is the original capital; he does not say whether it still existed in 1868. Numerous small foundations (Gera alone has “about 100 small legacies”), the Schleiz legacies in Mark and Aßo and {undated} institutions without a year are missing from the first chart."),
    bi(f"Ortsangaben wie »Naundorf und Umgegend« oder »Großsaara und anderen Nachbarorten« lassen offen, welche Orte gemeint sind; der Verein von 1849 nennt {len(PLACES['b1'])} Orte. {len(no_coord)} Orte ({', '.join(no_coord[:-1])} und {no_coord[-1]}) haben keine Koordinaten und fehlen auf der Karte.",
       f"Place names such as “Naundorf and surroundings” or “Großsaara and other neighbouring places” leave open which places are meant; the society of 1849 names {len(PLACES['b1'])} places. {len(no_coord)} places ({', '.join(no_coord[:-1])} and {no_coord[-1]}) have no coordinates and are missing from the map."),
]

obj = {
    "id": FID,
    "title": bi("Armenpflege, Kassen und Stiftungen", "Poor relief, funds and foundations"),
    "category": "welfare",
    "section": "t1-4-8",
    "merges": [A_SOC, A_FOU, A_STI],
    "sources": [ref(302, "b3"), ref(302, "b4"), ref(302, "b5"), ref(302, "b6"), ref(303, "b1"), ref(305, "b9"), ref(305, "b11"), ref(305, "b12"), ref(306, "b7"), ref(306, "b9"),
                ref(308, "b13"), ref(308, "b14"), ref(308, "b15"), ref(309, "b1"), ref(309, "b4"), ref(309, "b10"), ref(309, "b12"), ref(310, "b3")],
    "summary": summary,
    "findings": findings,
    "method": method,
    "caveats": caveats,
    "datasets": [ds_tl, ds_fou, ds_orte, base_places, base_rivers, ds_soc, ds_sti],
    "charts": [c1, c2, c3],
    "keywords": {
        "de": ["Armenwesen", "Stiftungen", "Stipendien", "Selbsthilfe", "Sterbekassen", "Krankenkassen", "Vorschussverein", "Christiane Louise", "Kapital", "Waisen", "verschämte Arme"],
        "en": ["poor relief", "foundations", "stipends", "self-help", "burial societies", "sickness funds", "credit association", "Christiane Louise", "capital", "orphans", "needy poor"],
    },
    "related": ["kirche-schule", "geburten-sterbefaelle", "berufe-gewerbe", "gesundheit"],
    "generated_by": "Claude Sonnet 5.5 (Agent F7), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}

if __name__ == "__main__":
    print("kinds", count_kind, "n", len(tl), "1860s", soc_1860s, "before 1850", soc_before_1850)
    print("capital", cap_total, cap_first, cap_rest, cap_first / cap_total, cap_prince, cap_prince / cap_total)
    print("stipends", n_sti, sti_total, "first", first_stipend)
    print("regions", region_count, "gera places", place_count["Gera"], "n places", n_places, "no coord", no_coord)
    print("undated", undated, "stack", sorted(stack_h.items())[-5:])
    probs = check_limits(obj)
    print("limit problems:", probs)
    print(write_feature(obj))
    ok = validate(FID)
    print("OK" if ok else "FAIL")
