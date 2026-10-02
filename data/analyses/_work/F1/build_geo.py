"""Feature geologie-boden (agent F1): merges geologie-formationen-bodenguete, geologie-formationen-rohstoffe,
geologie-fossilfunde-zechstein-clymenienkalk."""
import collections
import statistics
from common import *

a_soil = load("geologie-formationen-bodenguete")
a_res = load("geologie-formationen-rohstoffe")
a_fos = load("geologie-fossilfunde-zechstein-clymenienkalk")

soils_ds = json.loads(json.dumps(ds_of(a_soil, "soils")))
res_ds = json.loads(json.dumps(ds_of(a_res, "resources")))
zech_ds = ds_of(a_fos, "zechstein")
clym_ds = ds_of(a_fos, "clymenien")

# ------------------------------------------------------------------ derived columns
soils = rows_as_dicts(soils_ds)
order_by_grade = sorted(soils, key=lambda s: (-s["soil_grade"], s["order"]))
rank = {s["order"]: i + 1 for i, s in enumerate(order_by_grade)}
soils_ds["columns"].append(col("rang_gueteliste", "Rang in der Güteliste (Stufe absteigend, dann nach Alter)", "Rank in the quality list (grade descending, then by age)", "integer", None, True))
for r, s in zip(soils_ds["rows"], soils):
    r.append(rank[s["order"]])
soils = rows_as_dicts(soils_ds)

# ------------------------------------------------------------------ numbers
green = [s for s in soils if s["rock_group"] == "greenstone"]
slate = [s for s in soils if s["rock_group"] == "slate"]
n_green = len(green)
mean_green = statistics.mean(s["soil_grade"] for s in green)
n_green_top = sum(s["soil_grade"] == 5 for s in green)
min_green = min(s["soil_grade"] for s in green)
mean_slate = statistics.mean(s["soil_grade"] for s in slate)
top_units = [s for s in soils if s["soil_grade"] == 5]
n_top = len(top_units)
n_top_green = sum(s["rock_group"] == "greenstone" for s in top_units)
mean_o = statistics.mean(s["soil_grade"] for s in soils if s["region"] == "Oberland")
mean_u = statistics.mean(s["soil_grade"] for s in soils if s["region"] == "Unterland")
n_units = len(soils)
n_poor = sum(s["soil_grade"] == 2 for s in soils)
print("soils", n_units, "green", n_green, mean_green, n_green_top, min_green, "slate", mean_slate, "top5", n_top, n_top_green, "O/U", mean_o, mean_u, "poor", n_poor)

res = rows_as_dicts(res_ds)
by_res = collections.defaultdict(set)
for r in res:
    by_res[r["resource"]].add((r["formation_no"], r["region"]))
n_formations = 13
iron = by_res["iron"]
n_iron = len(iron)
n_iron_o = sum(1 for f in iron if f[1] == "Oberland")
only_o = sorted(k for k, v in by_res.items() if {x[1] for x in v} == {"Oberland"})
only_u = sorted(k for k, v in by_res.items() if {x[1] for x in v} == {"Unterland"})
both = sorted(k for k, v in by_res.items() if len({x[1] for x in v}) == 2)
print("iron", n_iron, n_iron_o, "only Oberland", only_o, "only Unterland", only_u, "both", both)
n_entries = len(res)
n_former = sum(r["status"] == "formerly" for r in res)
per_formation = collections.Counter(r["formation_no"] for r in res)
print("entries", n_entries, "formerly", n_former, per_formation.most_common(3))
res_order = [k for k, _ in sorted(((r["resource_de"], r["resource_order"]) for r in res), key=lambda t: t[1])]
count_res = collections.Counter(r["resource_de"] for r in res)
col_order = [k for k, _ in sorted(count_res.items(), key=lambda kv: (-kv[1], kv[0]))]
print("column order", col_order)
formations = []
for r in sorted(res, key=lambda r: r["formation_no"]):
    if r["formation"] not in formations:
        formations.append(r["formation"])
form_o = [f for f in formations if any(r["formation"] == f and r["region"] == "Oberland" for r in res)]
form_u = [f for f in formations if f not in form_o]
print(formations)

KLASSE = {"ächte Muscheln": "bivalve", "Muscheln": "bivalve", "Armfußmuscheln": "brachiopod",
          "Kammerschnecke": "cephalopod", "Gradhorn": "cephalopod", "Keulenhorn": "cephalopod", "Clymenien": "cephalopod", "Goniatiten": "cephalopod"}
for ds_ in (zech_ds, clym_ds):
    ds_["columns"].append(col("klasse", "Klasse für die Hervorhebung", "Class used for highlighting", "string", None, True,
                              "editorisch: Muscheln, Armfüßer, Kopffüßer (nach Liebes Bezeichnung), sonst übrige"))
    for r in ds_["rows"]:
        r.append(KLASSE.get(r[1], "other"))
zech = rows_as_dicts(zech_ds)
clym = rows_as_dicts(clym_ds)
n_zech = sum(z["species"] for z in zech)
n_clym = sum(c["species"] for c in clym)
biv_z = sum(z["species"] for z in zech if z["klasse"] == "bivalve")
bra_z = sum(z["species"] for z in zech if z["klasse"] == "brachiopod")
pla_z = sum(z["species"] for z in zech if z["taxon_group"] == "plant")
mol_c = sum(c["species"] for c in clym if c["taxon_group"] == "mollusc")
ceph_c = sum(c["species"] for c in clym if c["klasse"] == "cephalopod")
top_z = sorted(zech, key=lambda z: -z["species"])[:3]
gonia = next(c for c in clym if c["taxon"] == "Goniatiten")["species"]
print("fossils", n_zech, n_clym, "bivalves Z", biv_z, "brach", bra_z, "plants", pla_z, "molluscs C", mol_c, "cephalopods C", ceph_c, [(z["taxon"], z["species"]) for z in top_z], "goniatites", gonia)
assert (n_zech, n_clym) == (95, 42)

# ------------------------------------------------------------------ charts
OBER, UNTER = "@accent2", "@accent"
grade_label = {"de": "datum.value == 2 ? 'wenig' : datum.value == 3 ? 'mittel' : datum.value == 4 ? 'gut' : datum.value == 5 ? 'sehr gut' : ''",
               "en": "datum.value == 2 ? 'poor' : datum.value == 3 ? 'medium' : datum.value == 4 ? 'good' : datum.value == 5 ? 'very good' : ''"}
c1 = {
    "height": {"step": 20},
    "transform": [{"calculate": {"de": "datum.formation", "en": "datum.formation_en"}, "as": "label"}],
    "encoding": {"y": {"field": "label", "type": "nominal", "sort": {"field": "rang_gueteliste", "op": "min"},
                       "axis": {"title": None, "labelLimit": 400}}},
    "layer": [
        {"mark": {"type": "rule", "strokeWidth": 1.4},
         "encoding": {"x": {"field": "soil_grade", "type": "quantitative", "scale": {"domain": [1.6, 5.4]},
                            "axis": {"title": {"de": "Fruchtbarkeit des Bodens", "en": "Soil fertility"}, "values": [2, 3, 4, 5], "labelExpr": grade_label, "labelOverlap": False, "grid": True}},
                      "x2": {"datum": 1.6},
                      "color": {"condition": {"test": "datum.rock_group == 'greenstone'", "value": "@accent"}, "value": "@context"}}},
        {"mark": {"type": "point", "filled": True, "size": 95, "opacity": 1},
         "encoding": {"x": {"field": "soil_grade", "type": "quantitative"},
                      "color": {"condition": {"test": "datum.rock_group == 'greenstone'", "value": "@accent"}, "value": "@muted"},
                      "tooltip": tooltip(("formation", "Einheit", "Unit"), ("section", "Liebes Gliederung", "Liebe’s numbering"),
                                         ("region", "Landesteil", "Part"), ("soil_grade", "Stufe (1 bis 5)", "Grade (1 to 5)"),
                                         ("quote", "Liebes Wortlaut", "Liebe’s wording"), ("remark", "Bemerkung", "Remark"))}},
    ],
}

# c2: resource matrix
res_label = {"de": "datum.resource_de", "en": "datum.resource_en"}
status_label = {"de": "datum.status == 'worked' ? 'genutzt' : datum.status == 'formerly' ? 'früher genutzt' : 'nur vorkommend'",
                "en": "datum.status == 'worked' ? 'worked' : datum.status == 'formerly' ? 'formerly worked' : 'merely occurring'"}
res_en = {r["resource_de"]: r["resource_en"] for r in res}
col_order_en = [res_en[k] for k in col_order]
x_enc = {"field": "res_label", "type": "nominal",
         "sort": {"op": "count", "order": "descending"},
         "axis": {"orient": "top", "title": None, "labelAngle": -40, "labelAlign": "left", "labelLimit": 260, "grid": True, "ticks": False}}
y_enc = {"field": "formation_l", "type": "nominal", "sort": {"field": "formation_no", "op": "min"},
         "axis": {"title": None, "labelLimit": 420}}
band_y = {"field": "formation_l", "type": "nominal", "sort": {"field": "formation_no", "op": "min"}}
c2 = {
    "height": {"step": 26},
    "transform": [{"calculate": res_label, "as": "res_label"}, {"calculate": status_label, "as": "status_label"},
                  {"calculate": {"de": "datum.formation", "en": "datum.formation_en"}, "as": "formation_l"}],
    "encoding": {"y": y_enc, "x": x_enc},
    "layer": [
        {"transform": [{"filter": "datum.region == 'Oberland'"}, {"aggregate": [{"op": "min", "field": "formation_no", "as": "formation_no"}], "groupby": ["formation_l"]}],
         "mark": {"type": "rect", "color": OBER, "opacity": 0.12, "clip": True}, "encoding": {"x": None, "y": {**band_y, "axis": {"title": None, "labelLimit": 420}}}},
        {"transform": [{"filter": "datum.region == 'Unterland'"}, {"aggregate": [{"op": "min", "field": "formation_no", "as": "formation_no"}], "groupby": ["formation_l"]}],
         "mark": {"type": "rect", "color": UNTER, "opacity": 0.12, "clip": True}, "encoding": {"x": None, "y": {**band_y, "axis": {"title": None, "labelLimit": 420}}}},
        {"transform": [{"filter": "datum.status == 'worked'"}], "mark": {"type": "point", "filled": True, "size": 200, "color": "@ink", "strokeWidth": 0},
         "encoding": {"tooltip": tooltip(("formation", "Formation", "Formation"), ("resource_de", "Rohstoff", "Resource"), ("status_label", "Nutzung", "Use"),
                                         ("localities", "Orte", "Places"), ("evidence", "Liebes Wortlaut", "Liebe’s wording"))}},
        {"transform": [{"filter": "datum.status == 'formerly'"}], "mark": {"type": "point", "filled": False, "size": 200, "color": "@ink", "strokeWidth": 2.2},
         "encoding": {"tooltip": tooltip(("formation", "Formation", "Formation"), ("resource_de", "Rohstoff", "Resource"), ("status_label", "Nutzung", "Use"),
                                         ("localities", "Orte", "Places"), ("evidence", "Liebes Wortlaut", "Liebe’s wording"))}},
        {"transform": [{"filter": "datum.status == 'occurs'"}], "mark": {"type": "point", "filled": True, "size": 80, "color": "@muted", "strokeWidth": 0},
         "encoding": {"tooltip": tooltip(("formation", "Formation", "Formation"), ("resource_de", "Rohstoff", "Resource"), ("status_label", "Nutzung", "Use"),
                                         ("localities", "Orte", "Places"), ("evidence", "Liebes Wortlaut", "Liebe’s wording"))}},
    ],
}

# legend row below the matrix (symbols and region tints), built from one flattened row so that it needs no extra data
n_rows = len(formations)
leg_y = n_rows * 26 + 30
FLAT = [{"aggregate": [{"op": "count", "as": "n"}]}, {"calculate": "[0, 1, 2, 3, 4]", "as": "k"}, {"flatten": ["k"]}]
leg_items = [
    (8, leg_y, {"mark": {"type": "point", "filled": True, "size": 200, "color": "@ink", "strokeWidth": 0}}, {"de": "genutzt", "en": "worked"}),
    (74, leg_y, {"mark": {"type": "point", "filled": False, "size": 200, "color": "@ink", "strokeWidth": 2.2}}, {"de": "früher genutzt", "en": "formerly worked"}),
    (192, leg_y, {"mark": {"type": "point", "filled": True, "size": 80, "color": "@muted", "strokeWidth": 0}}, {"de": "nur vorkommend", "en": "merely occurring"}),
    (8, leg_y + 26, {"mark": {"type": "point", "shape": "square", "filled": True, "size": 220, "color": OBER, "opacity": 0.35, "strokeWidth": 0}}, {"de": "Oberland", "en": "Oberland"}),
    (92, leg_y + 26, {"mark": {"type": "point", "shape": "square", "filled": True, "size": 220, "color": UNTER, "opacity": 0.35, "strokeWidth": 0}}, {"de": "Unterland", "en": "Unterland"}),
]
for i, (xpix, ypix, mark, label) in enumerate(leg_items):
    c2["layer"].append({"transform": FLAT + [{"filter": f"datum.k == {i}"}], **mark,
                        "encoding": {"x": {"value": xpix}, "y": {"value": ypix}}})
    c2["layer"].append({"transform": FLAT + [{"filter": f"datum.k == {i}"}],
                        "mark": {"type": "text", "style": "annotation", "align": "left", "baseline": "middle", "dx": 12},
                        "encoding": {"x": {"value": xpix}, "y": {"value": ypix}, "text": {"value": label}}})
c2["padding"] = {"top": 4, "left": 4, "right": 4, "bottom": 66}

# c3: fossils
GROUP_COLOR = {"condition": [{"test": "datum.klasse == 'bivalve'", "value": "@accent"},
                             {"test": "datum.klasse == 'brachiopod'", "value": "@accent2"},
                             {"test": "datum.klasse == 'cephalopod'", "value": "@accent3"}], "value": "@context"}


def fossil_panel(name, title, last):
    return {
        "data": {"name": name},
        "width": 440,
        "height": {"step": 21},
        "title": {"text": title, "anchor": "start", "fontSize": 13, "offset": 6},
        "transform": [{"calculate": {"de": "datum.taxon", "en": "datum.taxon_en"}, "as": "label"},
                      {"calculate": {"de": "isValid(datum.qualifier) && datum.qualifier == 'über' ? 'über ' + datum.species : '' + datum.species",
                                     "en": "isValid(datum.qualifier) && datum.qualifier == 'über' ? 'over ' + datum.species : '' + datum.species"}, "as": "wert"}],
        "encoding": {"y": {"field": "label", "type": "nominal", "sort": {"field": "species", "op": "max", "order": "descending"},
                           "axis": {"title": None, "labelLimit": 400, "labelAlign": "left", "labelPadding": 232, "minExtent": 235}}},
        "layer": [
            {"mark": {"type": "bar", "cornerRadiusEnd": 3},
             "encoding": {"x": {"field": "species", "type": "quantitative", "scale": {"domain": [0, 30]},
                                "axis": {"title": ({"de": "Zahl der Arten", "en": "Number of species"} if last else None), "values": [0, 5, 10, 15, 20, 25, 30]}},
                          "color": GROUP_COLOR,
                          "tooltip": tooltip(("taxon", "Gruppe (Liebe)", "Group (Liebe)"), ("taxon_en", "Gruppe, englisch", "Group, English"), ("species", "Arten", "Species"))}},
            {"mark": {"type": "text", "align": "left", "dx": 5, "style": "label"},
             "encoding": {"x": {"field": "species", "type": "quantitative"}, "text": {"field": "wert"}}},
        ],
    }


c3 = {"vconcat": [
    fossil_panel("zechstein", {"de": f"Zechstein von Gera: {n_zech} Arten in {len(zech)} Gruppen", "en": f"Zechstein of Gera: {n_zech} species in {len(zech)} groups"}, False),
    fossil_panel("clymenien", {"de": f"Clymenienkalk: {n_clym} Arten in {len(clym)} Gruppen", "en": f"Clymenia limestone: {n_clym} species in {len(clym)} groups"}, True),
], "spacing": 22}

# ------------------------------------------------------------------ texts
lead_de = (f"In der geognostischen Übersicht beschreibt Prof. Liebe die {n_formations} Gesteinsformationen des Landes: den Boden, den ihre Verwitterung liefert, die "
           f"nutzbaren Stoffe und die Versteinerungen. Grünstein und Diabas tragen die besten Böden, Eisenerz ist der am weitesten verbreitete Rohstoff, und aus dem "
           f"Zechstein von Gera zählt Liebe {n_zech} Arten von Versteinerungen.")
lead_en = (f"In the geological overview Prof. Liebe describes the {n_formations} rock formations of the country: the soil their weathering yields, the usable "
           f"materials and the fossils. Greenstone and diabase carry the best soils, iron ore is the most widespread resource, and Liebe counts {n_zech} fossil species "
           f"from the Zechstein of Gera.")
f1_de = (f"Alle {n_green} Grünstein-, Diabas- und Tuffeinheiten liefern gute bis sehr gute Böden (Mittel {de(mean_green, 1)}), die Schiefer im Mittel nur {de(mean_slate, 1)}. "
         f"Im Mittel der Einheiten liegt das Unterland mit {de(mean_u, 1)} unter dem Oberland mit {de(mean_o, 1)}.")
f1_en = (f"All {n_green} greenstone, diabase and tuff units yield good to very good soils (mean {en(mean_green, 1)}), the slates only {en(mean_slate, 1)}. "
         f"On average over the units the Unterland, at {en(mean_u, 1)}, lies below the Oberland, at {en(mean_o, 1)}.")
f2_de = (f"Eisenerz nennt Liebe in {n_iron} der {n_formations} Formationen, {n_iron_o} davon im Oberland. Antimonerz, Alaunschiefer und Dachschiefer kommen nur dort vor, "
         f"Gips und Salz nur im Unterland.")
f2_en = (f"Liebe names iron ore in {n_iron} of the {n_formations} formations, {n_iron_o} of them in the Oberland. Antimony ore, alum shale and roofing slate occur only there, "
         f"gypsum and salt only in the Unterland.")
f3_de = (f"Muscheln und Armfüßer stellen {biv_z + bra_z} der {n_zech} Zechstein-Arten ({de((biv_z + bra_z) / n_zech * 100, 0)} Prozent). Im Clymenienkalk sind {ceph_c} der {n_clym} Arten "
         f"({de(ceph_c / n_clym * 100, 0)} Prozent) Kopffüßer, allen voran die Goniatiten mit {gonia}.")
f3_en = (f"Bivalves and brachiopods make up {biv_z + bra_z} of the {n_zech} Zechstein species ({en((biv_z + bra_z) / n_zech * 100, 0)} percent). In the Clymenia limestone {ceph_c} of the {n_clym} species "
         f"({en(ceph_c / n_clym * 100, 0)} percent) are cephalopods, led by the goniatites with {gonia}.")
assert (n_green, n_green_top) == (6, 5)

title1_de = "Auf Grünstein und Diabas wachsen die besten Böden, auf Schiefer nur mittlere"
title1_en = "The best soils lie on greenstone and diabase, only medium ones on slate"
cap1_de = (f"Bodengüte der {n_units} von Liebe beschriebenen Gesteinseinheiten, von mir aus seinen Worten (»sehr fruchtbar«, »mittlerer Güte« …) in fünf Stufen eingeordnet. "
           f"Blau: Grünstein, Diabas, Tuff. Quelle: S. 26 bis 41.")
cap1_de = cap1_de.replace("von mir aus seinen Worten", "aus seinen Worten")
cap1_en = (f"Soil quality of the {n_units} rock units Liebe describes, graded in five steps from his words (“very fertile”, “of medium quality” …). "
           f"Blue: greenstone, diabase, tuff. Source: pp. 26 to 41.")
title2_de = "Eisenerz kommt in sieben Formationen vor, Salz und Gips nur im Zechstein"
title2_en = "Iron ore occurs in seven formations, salt and gypsum only in the Zechstein"
assert n_iron == 7 and by_res["gypsum"] == {(10, "Unterland")}
cap2_de = ("Nutzbare Stoffe je Formation nach Liebe, nach Alter geordnet (oben das älteste Oberland-Gestein), mit Angabe, ob sie genutzt werden. "
           "Für das Rothliegende nennt Liebe keinen Rohstoff. Quelle: S. 26 bis 40.")
cap2_en = ("Usable materials per formation according to Liebe, ordered by age (oldest Oberland rock at the top), with the state of use. "
           "For the Rotliegend Liebe names no resource. Source: pp. 26 to 40.")
title3_de = "Im Zechstein überwiegen Muscheln und Armfüßer, im Clymenienkalk Kopffüßer"
title3_en = "Bivalves and brachiopods prevail in the Zechstein, cephalopods in the Clymenia limestone"
cap3_de = ("Von Liebe gezählte Arten von Versteinerungen je Gruppe, wie er sie nennt. Blau: Muscheln, orange: Armfüßer, grün: Kopffüßer. Beide Listen sind Zwischenstände (»bis jetzt gefunden«). "
           "Quelle: S. 35 und 38.")
cap3_en = ("Fossil species counted by Liebe per group, as he names them. Blue: bivalves, orange: brachiopods, green: cephalopods. Both lists are interim tallies (“so far found”). "
           "Source: pp. 35 and 38.")

for k, v in (("lead", lead_de), ("f1", f1_de), ("f2", f2_de), ("f3", f3_de), ("t1", title1_de), ("cap1", cap1_de), ("t2", title2_de), ("cap2", cap2_de),
             ("t3", title3_de), ("cap3", cap3_de), ("t3en", title3_en), ("cap1en", cap1_en)):
    print(f"[{words(v)}] {k}: {v}")

method_de = (
    "Grundlage ist die geognostische Übersicht (S. 25 bis 41), die Prof. Liebe für Brückners Buch verfasst hat. Für jede Gesteinseinheit wurde Liebes Satz über den "
    "Verwitterungsboden wörtlich übernommen und einer Stufe zugeordnet: 5 = sehr fruchtbar, ausgezeichnet, trefflich; 4 = fruchtbar, gut geeignet; 3 = mittelmäßig, von "
    "mittlerer Güte; 2 = wenig fruchtbar, dürftig; 1 = unfruchtbar (kommt nicht vor). Wo ein Satz Unterschiede macht, wurde die Mitte gewählt und die Spanne im Bemerkungsfeld "
    "festgehalten. Die Gesteinsgruppen sind editorisch. Für die Rohstoffe wurde jede genannte Kombination aus Formation und nutzbarem Stoff einmal erfasst, mit wörtlichem "
    "Beleg und Orten; die Stoffgruppen und die Nutzungsstufen (genutzt, früher genutzt, nur vorkommend) ordnen Liebes Wortlaut ein. Die Zahlen der Versteinerungen stammen aus "
    "Liebes Aufzählungen auf S. 38 (Zechstein) und S. 35 (Clymenienkalk); Zahlwörter wurden in Ziffern gesetzt, »über 7« als 7 gezählt. Die Zuordnung zu Klassen "
    "(Muscheln, Armfüßer, Kopffüßer) ist editorisch.")
method_en = (
    "The basis is the geological overview (pp. 25 to 41) that Prof. Liebe wrote for Brückner’s book. For each rock unit Liebe’s sentence about the weathering soil was taken "
    "verbatim and assigned a grade: 5 = very fertile, excellent, splendid; 4 = fertile, well suited; 3 = mediocre, of medium quality; 2 = poorly fertile, meager; 1 = barren "
    "(does not occur). Where a sentence distinguishes varieties, the middle was chosen and the range recorded in the remark field. The rock groups are editorial. For the "
    "resources every named combination of formation and usable material was recorded once, with a verbatim piece of evidence and the places; the resource groups and the use "
    "grades (worked, formerly worked, merely occurring) classify Liebe’s wording. The fossil counts come from Liebe’s lists on p. 38 (Zechstein) and p. 35 (Clymenia limestone); "
    "number words were set in digits, “over 7” was counted as 7. The assignment to classes (bivalves, brachiopods, cephalopods) is editorial.")
assert words(method_de) <= 260 and words(method_en) <= 260, (words(method_de), words(method_en))

caveats = [
    {"de": "Die Einstufung ist eine Deutung von Liebes Worten, keine Messung. Sie fasst oft verschieden fruchtbare Varianten einer Formation in einer Stufe zusammen. Die Einheiten sind nicht nach Fläche gewichtet: Ein kleines Gneisvorkommen zählt so viel wie der weit verbreitete Schiefer.",
     "en": "The grading is an interpretation of Liebe’s words, not a measurement. It often puts differently fertile varieties of a formation into one grade. The units are not weighted by area: a small gneiss outcrop counts as much as the widespread slate."},
    {"de": "Die Matrix zeigt, was Liebe nennt, nicht was es an Vorkommen gibt; für manche Formationen führt er Orte und Gruben ausführlich auf, für andere nur nebenbei. Ob ein Abbau 1870 wirklich in Betrieb war, lässt sich nicht in jedem Fall entscheiden; Fördermengen nennt der Abschnitt nicht.",
     "en": "The matrix shows what Liebe names, not what exists; for some formations he lists places and mines at length, for others only in passing. Whether working was really in progress in 1870 cannot always be decided; the section gives no production figures."},
    {"de": "Die Einteilung der Versteinerungen nach Großgruppen ist eine Deutung; Begriffe wie Strahlthiere oder Wurzelfüßer hatten 1870 teils einen anderen Umfang als heute. Die Zahlen sind Mindestzahlen aus Liebes Wissensstand, und beide Listen sind verschieden gegliedert, daher nur eingeschränkt vergleichbar.",
     "en": "The division of the fossils into major groups is an interpretation; terms such as Strahlthiere or Wurzelfüßer partly had a different scope in 1870 than today. The figures are minimum counts from Liebe’s state of knowledge, and the two lists are divided differently, so they are only partly comparable."},
]
for c in caveats:
    assert words(c["de"]) <= 60 and words(c["en"]) <= 60, (words(c["de"]), words(c["en"]))

sources = []
for a_ in (a_soil, a_res, a_fos):
    for s_ in a_["sources"]:
        if s_ not in sources:
            sources.append(s_)
print("sources", len(sources))

feature = {
    "id": "geologie-boden",
    "title": T("Gesteine, Böden und Bodenschätze", "Rocks, soils and mineral resources"),
    "category": "geology",
    "section": "t1-1-5",
    "merges": ["geologie-formationen-bodenguete", "geologie-formationen-rohstoffe", "geologie-fossilfunde-zechstein-clymenienkalk"],
    "sources": sources,
    "summary": T(lead_de, lead_en),
    "findings": [T(f1_de, f1_en), T(f2_de, f2_en), T(f3_de, f3_en)],
    "method": T(method_de, method_en),
    "caveats": caveats,
    "transcription_issues": a_fos.get("transcription_issues", []),
    "datasets": [soils_ds, res_ds, zech_ds, clym_ds],
    "charts": [
        {"id": "c1", "dataset": "soils", "title": T(title1_de, title1_en), "caption": T(cap1_de, cap1_en), "vegalite": c1},
        {"id": "c2", "dataset": "resources", "title": T(title2_de, title2_en), "caption": T(cap2_de, cap2_en), "vegalite": c2},
        {"id": "c3", "dataset": "zechstein", "extra_datasets": ["clymenien"], "title": T(title3_de, title3_en), "caption": T(cap3_de, cap3_en), "vegalite": c3},
    ],
    "keywords": {
        "de": ["Geologie", "Gesteine", "Böden", "Bodengüte", "Grünstein", "Diabas", "Schiefer", "Zechstein", "Eisenerz", "Versteinerungen", "Liebe"],
        "en": ["geology", "rocks", "soils", "soil quality", "greenstone", "diabase", "slate", "Zechstein", "iron ore", "fossils", "Liebe"],
    },
    "related": ["relief-hoehen", "gewaesser", "bergbau", "landwirtschaft"],
    "generated_by": "Claude Sonnet 5.5 (Agent F1), aus 3 Einzelauswertungen zusammengeführt",
    "date": "2026-10-02",
}
dump(feature)
if "--no-validate" not in sys.argv:
    validate("geologie-boden")
