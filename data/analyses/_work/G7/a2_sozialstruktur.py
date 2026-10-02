"""G7 analysis 2: social structure of the villages (Bauern, Haeusler, Taglohner, Dienstboten)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
from soc_classes import *

ents = load_entries()
C = load_coords()
U = [e for e in gemeinden(ents) if place_class(e) != "Stadt"]

CLASSES = [("Bauern", "Bauern", "Farmers"), ("Häusler", "Häusler", "Cottagers"),
           ("Taglöhner", "Taglöhner und Arbeiter", "Day labourers and workers"),
           ("Dienstboten", "Dienstboten", "Servants")]
KEYS = {"Bauern": FARM, "Häusler": HAUS, "Taglöhner": TAG, "Dienstboten": DIENST}

places, longrows, used = [], [], []
for e in sorted(U, key=sort_key):
    u = uid(e)
    occ = e.get("occupations") or {}
    c = classes_for(u, occ)
    if c is None or c["Bauern"] is None or c["Häusler"] is None:
        continue
    inh, hou = eff(e)
    so, sc = size_class(inh)
    ign = SUBSET.get(u, set())
    basis = []
    for name in KEYS:
        ks = [f"{k} {v}" for k, v in occ.items() if k in KEYS[name] and k not in ign and isinstance(v, (int, float))]
        if u == "niederboehmsdorf" and name in ("Häusler", "Taglöhner"):
            ks = ["Häusler 60 + Hintersiedler 26 abzüglich 15 Taglöhner"] if name == "Häusler" else ["Taglöhner 15 (Teil der Hintersiedler)"]
        if u in OVERRIDE and name in OVERRIDE[u]:
            ks = [f"Text: {OVERRIDE[u][name]}"]
        if ks:
            basis.append(f"{name}: " + " + ".join(ks))
    complete = int(all(v is not None for v in c.values()))
    b, h = c["Bauern"], c["Häusler"]
    fshare = round(b / (b + h), 3) if b + h else None
    spf = round(c["Dienstboten"] / b, 2) if (b and c["Dienstboten"] is not None) else None
    lon, lat, gn = coord(e, C)
    places.append([u, e["name"], e["landestheil"], inh, so, sc, c["Bauern"], c["Häusler"], c["Taglöhner"], c["Dienstboten"],
                   "; ".join(basis), complete, fshare, spf, lon, lat, e["start"]["page"], e["start"]["block"]])
    used.append(e)
    if complete:
        for i, (k, de, en) in enumerate(CLASSES, start=1):
            longrows.append([u, e["name"], e["landestheil"], so, sc, i, de, en, c[k]])

pcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("size_order", "Größenklasse (Nr.)", "Size class (no.)", "integer", derived=True),
    col("size_class", "Größenklasse", "Size class", "string", "Einwohner", derived=True),
    col("bauern", "Bauern", "Farmers", "integer", "Haushalte", derived=True, note="Summe der gedruckten Bauernangaben (Bauern, Pferde-, Kühbauern, Halb-, Viertelsbauern, Oeconomen, Landwirthe ...); leer = nicht angegeben"),
    col("haeusler", "Häusler", "Cottagers", "integer", "Haushalte", derived=True, note="Häusler, Kleinhäusler, Feldhäusler, Hintersiedler, Hausgenossen, Kleinleute; leer = nicht angegeben"),
    col("tagloehner", "Taglöhner und Arbeiter", "Day labourers and workers", "integer", "Personen", derived=True, note="Taglöhner, Handarbeiter, Fabrikarbeiter; leer = nicht angegeben"),
    col("dienstboten", "Dienstboten", "Servants", "integer", "Personen", derived=True, note="Dienstboten (Knechte, Mägde); leer = nicht angegeben"),
    col("basis", "Gedruckte Angaben", "Printed entries used", "string"),
    col("complete", "Alle vier Gruppen angegeben", "All four groups stated", "integer", derived=True, note="1 = ja"),
    col("farmer_share", "Bauernanteil an Bauern und Häuslern", "Farmers' share of farmers plus cottagers", "number", "Anteil", derived=True),
    col("servants_per_farmer", "Dienstboten je Bauer", "Servants per farmer", "number", "Personen/Bauer", derived=True),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
lcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("size_order", "Größenklasse (Nr.)", "Size class (no.)", "integer", derived=True),
    col("size_class", "Größenklasse", "Size class", "string", "Einwohner", derived=True),
    col("class_order", "Gruppe (Nr.)", "Group (no.)", "integer", derived=True),
    col("class_de", "Gruppe", "Group", "string"),
    col("class_en", "Gruppe (en)", "Group (en)", "string"),
    col("count", "Anzahl", "Number", "integer", derived=True),
]
refs = uniq_refs(used)

# ---- statistics ----------------------------------------------------------------------------------
comp = [r for r in places if r[11] == 1]
n_comp, n_all = len(comp), len(places)
n_lt = {lt: sum(1 for r in comp if r[2] == lt) for lt in LT_ORDER}
n_lt_all = {lt: sum(1 for r in places if r[2] == lt) for lt in LT_ORDER}


def tot(rs):
    return {"B": sum(r[6] for r in rs), "H": sum(r[7] for r in rs), "T": sum(r[8] for r in rs), "D": sum(r[9] for r in rs)}


def shares(t):
    s = sum(t.values())
    return {k: 100 * v / s for k, v in t.items()}


T_all = tot(comp)
S_all = shares(T_all)
S_lt = {lt: shares(tot([r for r in comp if r[2] == lt])) for lt in LT_ORDER}
T_lt = {lt: tot([r for r in comp if r[2] == lt]) for lt in LT_ORDER}
spf_lt = {lt: T_lt[lt]["D"] / T_lt[lt]["B"] for lt in LT_ORDER}
tph_lt = {lt: T_lt[lt]["T"] / T_lt[lt]["H"] for lt in LT_ORDER}
small = shares(tot([r for r in comp if r[4] <= 3]))
mid = shares(tot([r for r in comp if r[4] in (4,)]))
big = shares(tot([r for r in comp if r[4] >= 5]))
n_small = sum(1 for r in comp if r[4] <= 3)
n_big = sum(1 for r in comp if r[4] >= 5)
n_big1 = sum(1 for r in comp if r[4] >= 6)
fs = [(r[12], r[1], r[2]) for r in places if r[12] is not None]
fs_med = {lt: median([x[0] for x in fs if x[2] == lt]) for lt in LT_ORDER}
n_fs = len(fs)
n_low = sum(1 for x in fs if x[0] < 0.2)
n_high = sum(1 for x in fs if x[0] >= 0.5)
low_named = [x[1] for x in sorted(fs) if x[0] < 0.1]
high_named = [x[1] for x in sorted(fs, reverse=True)[:3]]
low_gera = sum(1 for x in fs if x[0] < 0.2 and x[2] == "Gera")
low_gera_names = [x[1] for x in sorted(fs) if x[0] < 0.1 and x[2] == "Gera"]
import math


def spearman(a, b):
    ra = [sorted(a).index(x) + (a.count(x) - 1) / 2 for x in a]
    rb = [sorted(b).index(x) + (b.count(x) - 1) / 2 for x in b]
    ma, mb = mean(ra), mean(rb)
    return sum((p - ma) * (q - mb) for p, q in zip(ra, rb)) / math.sqrt(sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb))


rho = spearman([r[12] for r in places if r[12] is not None], [r[3] for r in places if r[12] is not None])
n_geo = sum(1 for r in places if r[14] is not None)
excluded_combined = ["Töppeln", "Rusitz", "Trebnitz", "Lückenmühle", "Röttersdorf"]


def f1(x):
    return fnum(x, 1)


def e1(x):
    return fnum(x, 1, "en")


findings = [
    bi(f"In den {n_comp} Dörfern, für die Brückner Bauern, Häusler, Taglöhner und Dienstboten alle nennt, entfallen auf die vier Gruppen zusammen {pct(S_all['B'],0)} Bauern, {pct(S_all['H'],0)} Häusler, {pct(S_all['T'],0)} Taglöhner und {pct(S_all['D'],0)} Dienstboten. Das Dorf besteht also überwiegend aus Kleinbesitzern und Gesinde, nicht aus Bauern.",
       f"In the {n_comp} villages for which Brückner gives farmers, cottagers, day labourers and servants, the four groups together consist of {pct(S_all['B'],0,'en')} farmers, {pct(S_all['H'],0,'en')} cottagers, {pct(S_all['T'],0,'en')} day labourers and {pct(S_all['D'],0,'en')} servants. The village thus consists mostly of smallholders and servants, not of farmers."),
    bi(f"Im Landestheil Gera sind nur {pct(S_lt['Gera']['B'],0)} der erfassten Haushalte und Personen Bauern gegenüber {pct(S_lt['Schleiz']['B'],0)} in Schleiz und {pct(S_lt['Lobenstein-Ebersdorf']['B'],0)} in Lobenstein-Ebersdorf; dafür stehen im Unterland {fnum(tph_lt['Gera']*100,0)} Taglöhner auf 100 Häusler (Schleiz {fnum(tph_lt['Schleiz']*100,0)}, Lobenstein-Ebersdorf {fnum(tph_lt['Lobenstein-Ebersdorf']*100,0)}) – ein Hinweis auf die Fabrikarbeit in und um Gera.",
       f"In the district of Gera only {pct(S_lt['Gera']['B'],0,'en')} of the recorded households and persons are farmers, against {pct(S_lt['Schleiz']['B'],0,'en')} in Schleiz and {pct(S_lt['Lobenstein-Ebersdorf']['B'],0,'en')} in Lobenstein-Ebersdorf; in the lowland there are {fnum(tph_lt['Gera']*100,0,'en')} day labourers per 100 cottagers (Schleiz {fnum(tph_lt['Schleiz']*100,0,'en')}, Lobenstein-Ebersdorf {fnum(tph_lt['Lobenstein-Ebersdorf']*100,0,'en')}), which points to factory work in and around Gera."),
    bi(f"Auf einen Bauern kommen im Unterland {fnum(spf_lt['Gera'],1)} Dienstboten, in Schleiz {fnum(spf_lt['Schleiz'],1)} und in Lobenstein-Ebersdorf {fnum(spf_lt['Lobenstein-Ebersdorf'],1)}: Das deutet auf größere, mehr Gesinde beschäftigende Höfe im Unterland hin (Dienstboten sind Einzelpersonen, Bauern und Häusler Haushaltsvorstände).",
       f"In the lowland there are {fnum(spf_lt['Gera'],1,'en')} servants per farmer, in Schleiz {fnum(spf_lt['Schleiz'],1,'en')} and in Lobenstein-Ebersdorf {fnum(spf_lt['Lobenstein-Ebersdorf'],1,'en')}: this suggests larger farms with more servants in the lowland (servants are individuals, farmers and cottagers are heads of household)."),
    bi(f"Mit der Ortsgröße verschiebt sich das Gefüge: In den {n_small} Orten unter 300 Einwohnern stellen Bauern {pct(small['B'],0)} und Dienstboten {pct(small['D'],0)} der vier Gruppen, in den {n_big} Orten ab 500 Einwohnern nur noch {pct(big['B'],0)} Bauern und {pct(big['D'],0)} Dienstboten, aber {pct(big['H'],0)} Häusler.",
       f"Size shifts the structure: in the {n_small} places below 300 inhabitants farmers make up {pct(small['B'],0,'en')} and servants {pct(small['D'],0,'en')} of the four groups, in the {n_big} places with 500 or more inhabitants only {pct(big['B'],0,'en')} farmers and {pct(big['D'],0,'en')} servants, but {pct(big['H'],0,'en')} cottagers."),
    bi(f"Der Bauernanteil an Bauern und Häuslern liegt im Median bei {pct(100*fs_med['Gera'],0)} (Gera), {pct(100*fs_med['Schleiz'],0)} (Schleiz) und {pct(100*fs_med['Lobenstein-Ebersdorf'],0)} (Lobenstein-Ebersdorf), streut aber stark: {n_high} von {n_fs} Orten haben mindestens 50 %, {n_low} unter 20 % ({low_gera} davon im Landestheil Gera, z. B. {', '.join(low_gera_names[:3])}). Der Bauernanteil sinkt mit der Ortsgröße (Rangkorrelation {fnum(rho,2)}).",
       f"The farmers' share of farmers plus cottagers has a median of {pct(100*fs_med['Gera'],0,'en')} (Gera), {pct(100*fs_med['Schleiz'],0,'en')} (Schleiz) and {pct(100*fs_med['Lobenstein-Ebersdorf'],0,'en')} (Lobenstein-Ebersdorf) but varies widely: {n_high} of {n_fs} places reach at least 50%, {n_low} stay below 20% ({low_gera} of them in the district of Gera, e.g. {', '.join(low_gera_names[:3])}). The farmers' share falls with place size (rank correlation {fnum(rho,2,'en')})."),
]

LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"), "scale": {"domain": LT_ORDER}}
CLS = {"field": {"de": "class_de", "en": "class_en"}, "type": "nominal", "title": bi("Gruppe", "Group"),
       "sort": {"field": "class_order", "op": "min"}, "legend": {"labelLimit": 300}}
charts = [
    {"id": "c1", "dataset": "social_long",
     "title": bi("Sozialgefüge der Dörfer nach Landestheil", "Social structure of the villages by district"),
     "caption": bi(f"Anteile von Bauern, Häuslern, Taglöhnern und Dienstboten an der Summe der vier Gruppen, aufsummiert über die {n_comp} Dörfer mit vollständigen Angaben (Gera {n_lt['Gera']}, Schleiz {n_lt['Schleiz']}, Lobenstein-Ebersdorf {n_lt['Lobenstein-Ebersdorf']}). Bauern und Häusler sind Haushalte, Taglöhner und Dienstboten Personen.",
                   f"Shares of farmers, cottagers, day labourers and servants in the sum of the four groups, added up over the {n_comp} villages with complete figures (Gera {n_lt['Gera']}, Schleiz {n_lt['Schleiz']}, Lobenstein-Ebersdorf {n_lt['Lobenstein-Ebersdorf']}). Farmers and cottagers are households, day labourers and servants are persons."),
     "vegalite": {"height": 200, "mark": "bar", "encoding": {
         "y": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None},
         "x": {"aggregate": "sum", "field": "count", "type": "quantitative", "stack": "normalize",
               "title": bi("Anteil der vier Gruppen", "Share of the four groups"), "axis": {"format": "%"}},
         "color": CLS, "order": {"field": "class_order", "type": "quantitative"},
         "tooltip": [{"field": "landestheil", "title": bi("Landestheil", "District")},
                     {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Gruppe", "Group")},
                     {"aggregate": "sum", "field": "count", "title": bi("Anzahl", "Number")},
                     {"aggregate": "distinct", "field": "place_id", "title": bi("Orte", "Places")}]}}},
    {"id": "c2", "dataset": "social_long",
     "title": bi("Sozialgefüge nach Ortsgröße", "Social structure by place size"),
     "caption": bi("Dieselben Anteile nach Einwohnerzahl der Orte. Je größer der Ort, desto kleiner der Anteil der Bauern und Dienstboten; die Klassen ab 1 000 Einwohnern umfassen nur wenige Dörfer.",
                   "The same shares by number of inhabitants. The larger the place, the smaller the share of farmers and servants; the classes from 1,000 inhabitants contain only a few villages."),
     "vegalite": {"height": 260, "mark": "bar", "encoding": {
         "y": {"field": "size_class", "type": "ordinal", "sort": {"field": "size_order", "op": "min"}, "title": bi("Einwohner", "Inhabitants")},
         "x": {"aggregate": "sum", "field": "count", "type": "quantitative", "stack": "normalize",
               "title": bi("Anteil der vier Gruppen", "Share of the four groups"), "axis": {"format": "%"}},
         "color": CLS, "order": {"field": "class_order", "type": "quantitative"},
         "tooltip": [{"field": "size_class", "title": bi("Größenklasse", "Size class")},
                     {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Gruppe", "Group")},
                     {"aggregate": "sum", "field": "count", "title": bi("Anzahl", "Number")},
                     {"aggregate": "distinct", "field": "place_id", "title": bi("Orte", "Places")}]}}},
    {"id": "c3", "dataset": "social_places",
     "title": bi("Bauernanteil in den Dörfern", "Farmers' share in the villages"),
     "caption": bi(f"Anteil der Bauern an Bauern plus Häuslern ({n_geo} von {n_fs} Orten verortet; Fläche nach Einwohnerzahl). Dunkel: überwiegend Bauern, hell: überwiegend Häusler. Koordinaten aus GeoNames.",
                   f"Farmers' share of farmers plus cottagers ({n_geo} of {n_fs} places located; area by inhabitants). Dark: mostly farmers, light: mostly cottagers. Coordinates from GeoNames."),
     "vegalite": {"height": 460, "projection": {"type": "mercator"},
                  "mark": {"type": "circle", "opacity": 0.9},
                  "transform": [{"filter": "isValid(datum.lat) && isValid(datum.farmer_share)"}],
                  "encoding": {
                      "longitude": {"field": "lon", "type": "quantitative"},
                      "latitude": {"field": "lat", "type": "quantitative"},
                      "size": {"field": "inhabitants", "type": "quantitative", "title": bi("Einwohner", "Inhabitants"),
                               "scale": {"type": "sqrt", "range": [30, 700], "domain": [0, 3000]},
                               "legend": {"values": [100, 500, 2000], "format": "d"}},
                      "color": {"field": "farmer_share", "type": "quantitative", "title": bi("Bauernanteil", "Farmers' share"),
                                "scale": {"range": "ramp", "domain": [0, 1]}, "legend": {"format": "%"}},
                      "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                                  {"field": "landestheil", "title": bi("Landestheil", "District")},
                                  {"field": "bauern", "title": bi("Bauern", "Farmers")},
                                  {"field": "haeusler", "title": bi("Häusler", "Cottagers")},
                                  {"field": "farmer_share", "title": bi("Bauernanteil", "Farmers' share"), "format": ".0%"},
                                  {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants")},
                                  {"field": "page", "title": bi("Seite", "Page")}]}}},
]

a = {
    "id": "orte-sozialstruktur-doerfer-1867",
    "title": bi("Sozialstruktur der Dörfer: Bauern, Häusler, Taglöhner, Dienstboten", "Social structure of the villages: farmers, cottagers, day labourers, servants"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Fast jeder Dorfartikel nennt, wie sich die Einwohner nach Besitz und Arbeit gliedern: in Bauern, Häusler, Taglöhner und Dienstboten. Für {n_all} Landgemeinden lassen sich Bauern und Häusler vergleichen, für {n_comp} alle vier Gruppen. Die Diagramme zeigen die Gruppenanteile nach Landestheil und Ortsgröße und auf einer Karte den Bauernanteil.",
        f"Almost every village article states how the inhabitants divide by property and work: into farmers, cottagers, day labourers and servants. For {n_all} rural municipalities farmers and cottagers can be compared, for {n_comp} all four groups. The charts show the group shares by district and place size and, on a map, the farmers' share."),
    "method": bi(
        f"Grundlage sind die Berufsangaben (occupations) der Gazetteer-Einträge der {len(U)} Landgemeinden (ohne die sechs Städte). Die in den Artikeln verschieden benannten Gruppen wurden zu vier Klassen zusammengefasst: Bauern (Bauern, Pferde-, Kühbauern, Ochsenbauern, Hofbauern, Halb- und Viertelsbauern, große und halbe Bauern, Kleinbauern, Gutsbauer, Landwirthe, Oeconomen, Bäuerlein mit Nebengeschäft), Häusler (Häusler, Kleinhäusler, Feldhäusler, Hintersiedler, Hintersattler, Tropfhäusler, Hausgenossen, Kleinleute), Taglöhner und Arbeiter (Taglöhner, Handarbeiter, Fabrikarbeiter) und Dienstboten (Dienstboten, Knechte, Mägde). Wo ein Artikel eine Untergruppe als Teil einer Hauptgruppe nennt ('15 Bauern, darunter 14 Pferdebauern'; Lusan, Lessen, Wernsdorf bei Gera, Hirschfeld, Collis, Otticha), wurde sie nicht addiert; bei Niederböhmsdorf (26 Hintersiedler, darunter 15 Taglöhner) wurden die Taglöhner abgezogen. Für Lerchenhügel, Karolinenfield und Pirk wurde nach dem Text null Bauern, für Blankenstein ein Bauer angesetzt. Nicht aufgenommen wurden Orte, deren Artikel Gruppen nur zusammengefasst nennt ('Häusler und Taglöhner': {', '.join(excluded_combined[:2])}, {excluded_combined[3]}; 'Taglöhner und Dienstboten': {excluded_combined[2]}, {excluded_combined[4]}), und Orte ohne Angabe zu Bauern und Häuslern; das gilt auch für Orte, die die Bevölkerung nur nach Familien mit Ackerbau gliedern (Pottiga, Altengesees, Wurzbach). Fehlt eine einzelne Gruppe (meist Taglöhner oder Dienstboten), bleibt die Zelle leer und der Ort geht nur in den Bauernanteil, nicht in die Gruppenanteile ein. Webermeister und Handwerker sind keine eigene Klasse, sondern überschneiden sich mit den Häuslern, und werden in der Auswertung zu den Gewerben behandelt. Bauernanteil = Bauern : (Bauern + Häusler); Dienstboten je Bauer = Dienstboten : Bauern. Alle Gruppenzahlen sind abgeleitete Summen der gedruckten Zahlen (derived).",
        f"The basis are the occupation data (occupations) of the gazetteer entries of the {len(U)} rural municipalities (without the six towns). The groups, which the articles name in various ways, were combined into four classes: farmers (Bauern, Pferde-, Kühbauern, Ochsenbauern, Hofbauern, half and quarter farmers, large and half farmers, small farmers, Gutsbauer, Landwirthe, Oeconomen, 'Bäuerlein mit Nebengeschäft'), cottagers (Häusler, Kleinhäusler, Feldhäusler, Hintersiedler, Hintersattler, Tropfhäusler, Hausgenossen, Kleinleute), day labourers and workers (Taglöhner, Handarbeiter, Fabrikarbeiter) and servants (Dienstboten, Knechte, Mägde). Where an article names a subgroup as part of a main group ('15 farmers, among them 14 horse farmers'; Lusan, Lessen, Wernsdorf near Gera, Hirschfeld, Collis, Otticha) it was not added; at Niederböhmsdorf (26 Hintersiedler, among them 15 day labourers) the day labourers were deducted. For Lerchenhügel, Karolinenfield and Pirk the text implies zero farmers, for Blankenstein one farmer. Places whose article names groups only in combination ('cottagers and day labourers': {', '.join(excluded_combined[:2])}, {excluded_combined[3]}; 'day labourers and servants': {excluded_combined[2]}, {excluded_combined[4]}) and places without figures for farmers and cottagers were left out; this also applies to places that divide the population only by families engaged in farming (Pottiga, Altengesees, Wurzbach). If a single group is missing (mostly day labourers or servants) the cell stays empty and the place enters only the farmers' share, not the group shares. Master weavers and craftsmen are not a class of their own but overlap with the cottagers and are treated in the analysis of the trades. Farmers' share = farmers : (farmers + cottagers); servants per farmer = servants : farmers. All group figures are derived sums of the printed numbers."),
    "findings": findings,
    "caveats": [
        bi("Bauern und Häusler zählt Brückner als Haushalte, Taglöhner und Dienstboten als Personen; die Anteile sind daher Mischanteile und keine Anteile an der Bevölkerung. Die vier Gruppen erfassen nur einen Teil der Einwohner (Frauen und Kinder der Haushalte, Kapitalisten, Handwerker und Arme fehlen).",
           "Brückner counts farmers and cottagers as households and day labourers and servants as persons; the shares are therefore mixed shares and not shares of the population. The four groups cover only part of the inhabitants (wives and children of the households, rentiers, craftsmen and the poor are missing)."),
        bi("Die Gruppenbezeichnungen sind nicht einheitlich (z. B. 'Hausgenossen', 'Kleinleute', 'Bäuerlein'); die Zuordnung zu vier Klassen ist eine Entscheidung der Auswertung und im Datensatz (Spalte basis) nachvollziehbar.",
           "The group names are not uniform (e.g. 'Hausgenossen', 'Kleinleute', 'Bäuerlein'); the assignment to four classes is a decision of this analysis and can be traced in the dataset (column basis)."),
        bi("Bei Göritz, Venzka, Titschendorf und anderen Orten gelten die Berufsangaben für einen größeren Gemeindeverband oder nur für das Hauptdorf; bei zweiherrischen Orten nur für den reußischen Anteil.",
           "For Göritz, Venzka, Titschendorf and other places the occupation figures refer to a larger municipal group or only to the main village; for places shared with a neighbouring state only to the Reuss share."),
    ],
    "datasets": [
        {"name": "social_places", "title": bi("Bauern, Häusler, Taglöhner und Dienstboten je Landgemeinde", "Farmers, cottagers, day labourers and servants per rural municipality"),
         "columns": pcols, "rows": places, "source_refs": refs},
        {"name": "social_long", "title": bi("Gruppenzahlen der vollständig erfassten Orte (Langformat)", "Group figures of the completely recorded places (long format)"),
         "columns": lcols, "rows": longrows, "source_refs": refs},
    ],
    "charts": charts,
    "keywords": {"de": ["Sozialstruktur", "Bauern", "Häusler", "Taglöhner", "Dienstboten", "Dörfer", "Berufe", "Gesinde"],
                 "en": ["social structure", "farmers", "cottagers", "day labourers", "servants", "villages", "occupations"]},
    "related": ["orte-siedlungsbild-1867", "wirtschaft-berufsklassen-1864", "landwirtschaft-grundbesitz-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
