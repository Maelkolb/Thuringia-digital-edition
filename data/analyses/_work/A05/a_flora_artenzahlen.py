"""Analysis: species counts of the flora (pp. 72, 74-75)."""
from common import *

g = grid("72", "b3")  # header + 9 rows
LAND = {
    "Reußenland": ("Reußenland", "Reuss territory", "area"),
    "Dem Unterlande allein gehörig": ("Nur im Unterland", "Unterland only", "part"),
    "Dem Oberlande allein gehörig": ("Nur im Oberland", "Oberland only", "part"),
    "Beiden gemeinschaftlich": ("Beiden gemeinsam", "Shared", "part"),
    "Das Unterland im Ganzen": ("Unterland gesamt", "Unterland, total", "area"),
    "Das Oberland im Ganzen": ("Oberland gesamt", "Oberland, total", "area"),
    "Thüringen": ("Thüringen", "Thuringia", "area"),
    "Franken": ("Franken", "Franconia", "area"),
    "Deutschland": ("Deutschland", "Germany", "area"),
}
rows_p = []
for i, r in enumerate(g[1:], start=1):
    key = re.sub(r"[\s.*)]+$", "", r[0]).strip()
    key = re.sub(r"\*+\)?", "", key).strip(" .")
    de_l, en_l, kind = LAND[key]
    sp, di, mo = int(r[1]), int(r[2]), int(r[3])
    ratio_p = num(r[4].split(":")[0])
    assert sp == di + mo, (key, sp, di, mo)
    rows_p.append([key, de_l, en_l, kind, sp, di, mo, ratio_p, round(di / mo, 2), i])
byk = {r[0]: r for r in rows_p}
DEU = byk["Deutschland"][4]
for r in rows_p:
    r.append(round(100 * r[4] / DEU, 1))  # pct of German species
assert byk["Reußenland"][4] == byk["Beiden gemeinschaftlich"][4] + byk["Dem Unterlande allein gehörig"][4] + byk["Dem Oberlande allein gehörig"][4]
assert byk["Das Unterland im Ganzen"][4] == byk["Beiden gemeinschaftlich"][4] + byk["Dem Unterlande allein gehörig"][4]
assert byk["Das Oberland im Ganzen"][4] == byk["Beiden gemeinschaftlich"][4] + byk["Dem Oberlande allein gehörig"][4]

# ratio check: printed vs recomputed (ratio = dicots / monocots)
issues = []
for r in rows_p:
    if abs(r[7] - r[8]) > 0.011:
        issues.append((r[0], r[7], r[8]))
print("ratio deviations (printed, computed):", issues)
trunc = [(r[0], r[7], r[8]) for r in rows_p if abs(r[7] - r[8]) <= 0.011 and r[7] != r[8]]
print("deviation of 0.01 only (truncation vs rounding):", trunc)

# groups: Phanerogams (table) + Cryptogams (p.74/75 text)
t74 = text("74", "b2")
t75 = text("75", "b1")
need("658", "74", "b2")
need("200 Laubmoose, 60 Lebermoose, 131 Flechten, 101 Algen und 140 Pilze", "74", "b2")
need("26 Farn, Schachtelhalme und Bärlappen", "75", "b1")
crypto = [("Laubmoose", "Laubmoose", "Mosses", 200), ("Lebermoose", "Lebermoose", "Liverworts", 60),
          ("Flechten", "Flechten", "Lichens", 131), ("Algen", "Algen", "Algae", 101),
          ("Pilze", "Pilze", "Fungi", 140), ("Farne", "Farnpflanzen", "Ferns and allies", 26)]
assert sum(c[3] for c in crypto) == 658
CLASS = {
    "dicot": ("Zweikeimblättrige", "Dicotyledons"),
    "monocot": ("Einkeimblättrige", "Monocotyledons"),
    "crypto": ("Blütenlose", "Flowerless"),
}
groups = [
    ["Dicotylen", "Zweikeimblättrige", "Dicotyledons", "dicot", CLASS["dicot"][0], CLASS["dicot"][1], byk["Reußenland"][5]],
    ["Monocotylen", "Einkeimblättrige", "Monocotyledons", "monocot", CLASS["monocot"][0], CLASS["monocot"][1], byk["Reußenland"][6]],
]
for k, dl, el, n in crypto:
    groups.append([k, dl, el, "crypto", CLASS["crypto"][0], CLASS["crypto"][1], n])
total = sum(x[6] for x in groups)
assert total == 1093 + 658
print("total species", total)
pheno = byk["Reußenland"][4]
print("phanerogam share", pheno / total)

ul, ol, both = byk["Dem Unterlande allein gehörig"], byk["Dem Oberlande allein gehörig"], byk["Beiden gemeinschaftlich"]
reuss, thu, fra = byk["Reußenland"], byk["Thüringen"], byk["Franken"]
uland, oland = byk["Das Unterland im Ganzen"], byk["Das Oberland im Ganzen"]
pct_thu = 100 * reuss[4] / thu[4]
pct_fra = 100 * reuss[4] / fra[4]
pct_shared = 100 * both[4] / reuss[4]
print(pct_thu, pct_fra, pct_shared, 100 * reuss[4] / DEU)

# overlap dataset (long): three parts x two classes
overlap = []
for i, (key, de_l, en_l) in enumerate([("Dem Unterlande allein gehörig", "Nur im Unterland", "Unterland only"),
                                       ("Beiden gemeinschaftlich", "Beiden gemeinsam", "Shared"),
                                       ("Dem Oberlande allein gehörig", "Nur im Oberland", "Oberland only")], start=1):
    r = byk[key]
    overlap.append([de_l, en_l, i, CLASS["dicot"][0], CLASS["dicot"][1], r[5]])
    overlap.append([de_l, en_l, i, CLASS["monocot"][0], CLASS["monocot"][1], r[6]])

SRC72 = {"page": "72", "block": "b3", "rows": "r2-r10"}
ana = {
    "id": "flora-artenzahlen-phanerogamen-kryptogamen",
    "title": bi("Artenzahlen der Flora: Phanerogamen und Kryptogamen", "Species counts of the flora: flowering and flowerless plants"),
    "category": "flora",
    "section": "t1-1-8",
    "sources": [SRC72, {"page": "72", "block": "b4"}, {"page": "72", "block": "fn2"}, {"page": "74", "block": "b2"}, {"page": "75", "block": "b1"}, {"page": "830", "block": "b7"}, {"page": "830", "block": "b8"}, {"page": "830", "block": "b9"}],
    "summary": bi(
        "Brückner zählt für das Reußenland 1093 Arten Blütenpflanzen (Phanerogamen) und 658 Arten blütenlose Pflanzen (Kryptogamen) und vergleicht die Blütenpflanzen mit Thüringen, Franken und Deutschland. Die Diagramme zeigen die Zusammensetzung der Flora nach Pflanzengruppen, den Vergleich mit den Nachbarländern und die Aufteilung der Blütenpflanzen auf Unterland (Gera) und Oberland (Schleiz, Lobenstein).",
        "Brückner counts 1,093 species of flowering plants (phanerogams) and 658 species of flowerless plants (cryptogams) for the Reuss territory and compares the flowering plants with Thuringia, Franconia and Germany. The charts show the composition of the flora by plant group, the comparison with the neighbouring regions, and the split of the flowering plants between the Unterland (Gera) and the Oberland (Schleiz, Lobenstein)."),
    "method": bi(
        f"Die Tabelle auf S. 72 (neun Zeilen: Gesamtgebiet, nur Unter-/nur Oberland, gemeinsam, Unter- und Oberland insgesamt, Thüringen nach Schlechtendal (im Druck »Schachtendal«, berichtigt S. 830), Franken nach der »Bavaria«, Deutschland) wurde vollständig übernommen; die Summen sind konsistent (Arten = Dikotylen + Monokotylen, Gesamtgebiet = gemeinsam + nur Unterland + nur Oberland). Die Kryptogamenzahlen stehen im Fließtext auf S. 74–75 (200 Laubmoose, 60 Lebermoose, 131 Flechten, 101 Algen, 140 Pilze, 26 Gefäßkryptogamen = 658, ohne 78 Varietäten). Abgeleitet sind die Anteile an der deutschen Artenzahl und das Verhältnis Dikotylen : Monokotylen, das mit den gedruckten Verhältniszahlen verglichen wurde. Die Gattungszahl »zusammen 42 Genera (Franken 44, Deutschland 63)« auf S. 75 ist nicht eindeutig zuzuordnen und wurde nicht verwendet.",
        "The table on p. 72 (nine rows: whole territory, Unterland only, Oberland only, shared, Unterland and Oberland in total, Thuringia after Schlechtendal (printed “Schachtendal”, corrected p. 830), Franconia after the “Bavaria”, Germany) was taken over in full; the totals are consistent (species = dicotyledons + monocotyledons; whole territory = shared + Unterland only + Oberland only). The cryptogam figures are given in running text on pp. 74–75 (200 mosses, 60 liverworts, 131 lichens, 101 algae, 140 fungi, 26 vascular cryptogams = 658, excluding 78 varieties). Derived are the shares of the German species total and the dicot : monocot ratio, which was compared with the printed ratios. The genus count “together 42 genera (Franconia 44, Germany 63)” on p. 75 cannot be assigned unambiguously and was not used."),
    "findings": [
        bi(f"Zusammen nennt Brückner {total} Pflanzenarten für das Fürstenthum; {de(100 * pheno / total, 1)} % davon sind Blütenpflanzen. Unter den blütenlosen Gruppen sind Laubmoose ({crypto[0][3]}), Pilze ({crypto[4][3]}) und Flechten ({crypto[2][3]}) am artenreichsten.",
           f"In total Brückner names {total} plant species for the principality; {en(100 * pheno / total, 1)} % of them are flowering plants. Among the flowerless groups, mosses ({crypto[0][3]}), fungi ({crypto[4][3]}) and lichens ({crypto[2][3]}) are the richest."),
        bi(f"Die {reuss[4]} Blütenpflanzenarten des Reußenlandes entsprechen {de(reuss[9] if False else 100 * reuss[4] / DEU, 1)} % der {DEU} deutschen Arten, {de(pct_thu, 1)} % der Thüringer ({thu[4]}) und {de(pct_fra, 1)} % der fränkischen Flora ({fra[4]}). Brückner nennt 38,4 %; gerechnet ergeben sich {de(100 * reuss[4] / DEU, 2)} %, er hat also abgerundet.",
           f"The {reuss[4]} species of flowering plants of the Reuss territory correspond to {en(100 * reuss[4] / DEU, 1)} % of the {DEU} German species, {en(pct_thu, 1)} % of the Thuringian ({thu[4]}) and {en(pct_fra, 1)} % of the Franconian flora ({fra[4]}). Brückner gives 38.4 %; the computed value is {en(100 * reuss[4] / DEU, 2)} %, so he truncated."),
        bi(f"{both[4]} Arten ({de(pct_shared, 1)} % der Blütenpflanzen) wachsen in beiden Landesteilen; {ul[4]} kommen nur im Unterland, {ol[4]} nur im Oberland vor. Das Oberland ist mit {oland[4]} gegenüber {uland[4]} Arten etwas reicher, wie Brückner schreibt.",
           f"{both[4]} species ({en(pct_shared, 1)} % of the flowering plants) grow in both parts of the territory; {ul[4]} occur only in the Unterland and {ol[4]} only in the Oberland. With {oland[4]} against {uland[4]} species the Oberland is somewhat richer, as Brückner states."),
        bi(f"Das Verhältnis von Zwei- zu Einkeimblättrigen liegt im Reußenland bei {de(reuss[8], 2)} : 1, in Thüringen bei {de(thu[8], 2)} : 1, in Franken bei {de(fra[8], 2)} : 1 und in Deutschland bei {de(byk['Deutschland'][8], 2)} : 1. Nur im Oberland vorkommende Arten sind mit {de(ol[8], 2)} : 1 besonders reich an Zweikeimblättrigen, nur im Unterland vorkommende mit {de(ul[8], 2)} : 1 vergleichsweise reich an Einkeimblättrigen (darunter zehn Orchideen nach Brückners Berichtigungen, siehe die Analyse der Exklusivarten).",
           f"The ratio of dicotyledons to monocotyledons is {en(reuss[8], 2)} : 1 in the Reuss territory, {en(thu[8], 2)} : 1 in Thuringia, {en(fra[8], 2)} : 1 in Franconia and {en(byk['Deutschland'][8], 2)} : 1 in Germany. Species found only in the Oberland are particularly rich in dicotyledons at {en(ol[8], 2)} : 1, those found only in the Unterland relatively rich in monocotyledons at {en(ul[8], 2)} : 1 (among them ten orchids after Brückner's corrections, see the analysis of the exclusive species)."),
    ],
    "caveats": [
        bi(f"Gedruckt ist für »Dem Unterlande allein gehörig« das Verhältnis 2,44 : 1; aus 71 und 25 ergibt sich aber {de(ul[8], 2)} : 1 (2,44 steht so auch im Faksimile). Bei Deutschland ist 3,76 gedruckt, gerechnet {de(byk['Deutschland'][8], 2)}; bei »Dem Oberlande allein gehörig« 4,94, gerechnet {de(ol[8], 2)}. Die übrigen Verhältnisse stimmen auf die zweite Stelle. Die Diagramme verwenden die berechneten Werte.",
           f"For “Dem Unterlande allein gehörig” the printed ratio is 2.44 : 1, but 71 and 25 give {en(ul[8], 2)} : 1 (2.44 is also what the facsimile shows). For Germany 3.76 is printed, the computed value is {en(byk['Deutschland'][8], 2)}; for “Dem Oberlande allein gehörig” 4.94 is printed, the computed value {en(ol[8], 2)}. The other ratios agree to the second decimal. The charts use the computed values."),
        bi("Die Zahlen der Vergleichsgebiete (Thüringen nach Schlechtendal (im Druck »Schachtendal«, berichtigt S. 830), Franken nach der »Bavaria«) stammen aus verschiedenen Florenwerken und sind nach Umfang des Artbegriffs nur eingeschränkt vergleichbar. Brückner betont selbst, dass die höheren Gebirgsgegenden botanisch noch nicht durchforscht sind (S. 71).",
           "The figures for the comparison regions (Thuringia after Schlechtendal (printed “Schachtendal”, corrected p. 830), Franconia after the “Bavaria”) come from different floras and are only partly comparable in the scope of the species concept. Brückner himself stresses that the higher mountain areas have not yet been botanically surveyed (p. 71)."),
        bi("Die Kryptogamenzahlen schließen 78 Varietäten aus (S. 74); eine Aufteilung auf Unter- und Oberland gibt Brückner nicht, er schreibt nur, dass die weitaus größere Zahl dem Oberland angehöre (S. 75).",
           "The cryptogam figures exclude 78 varieties (p. 74); Brückner gives no split between Unterland and Oberland and only states that by far the larger number belongs to the Oberland (p. 75)."),
        bi("Brückner berichtigt auf S. 830 die Listen der nur im Unter- bzw. nur im Oberland vorkommenden Arten: drei Arten fallen aus der Unterlandliste (Laserpitium pruthenicum, Neottia Nidus avis, Gentiana ciliata), je eine (Unterland) bzw. zwei (Oberland) Arten kommen hinzu. Die Tabellenzahlen (96, 113) hat er nicht geändert; sie sind hier wie gedruckt wiedergegeben. Die Namensberichtigung »Schlechtendal statt Schachtendal« (S. 72, Fußnote) ist berücksichtigt.",
           "On p. 830 Brückner corrects the lists of species occurring only in the Unterland or only in the Oberland: three species drop out of the Unterland list (Laserpitium pruthenicum, Neottia Nidus avis, Gentiana ciliata), one (Unterland) and two (Oberland) species are added. He did not change the table figures (96, 113); they are reproduced here as printed. The name correction “Schlechtendal instead of Schachtendal” (p. 72, footnote) has been taken into account."),
    ],
    "datasets": [
        {"name": "phanerogams",
         "title": bi("Phanerogamen im Reußenland im Vergleich (S. 72)", "Phanerogams of the Reuss territory in comparison (p. 72)"),
         "columns": [
             col("land_key", "Zeile (Original)", "Row (original)", "string", None),
             col("land_de", "Gebiet", "Area", "string", None, True, "editorielle Kurzbezeichnung"),
             col("land_en", "Gebiet (EN)", "Area (EN)", "string", None, True),
             col("kind", "Art der Zeile", "Row type", "string", None, True, "area = Gebiet, part = Teilmenge des Reußenlandes"),
             col("species", "Arten", "Species", "integer", "Arten"),
             col("dicots", "Dikotylen", "Dicotyledons", "integer", "Arten"),
             col("monocots", "Monokotylen", "Monocotyledons", "integer", "Arten"),
             col("ratio_printed", "Verhältnis (gedruckt)", "Ratio (printed)", "number", "Dikotylen je Monokotyle"),
             col("ratio_computed", "Verhältnis (berechnet)", "Ratio (computed)", "number", "Dikotylen je Monokotyle", True),
             col("table_row", "Tabellenzeile", "Table row", "integer", None, True),
             col("pct_of_germany", "Anteil an Deutschland", "Share of Germany", "number", "%", True),
         ],
         "rows": rows_p, "source_refs": [SRC72]},
        {"name": "flora_groups",
         "title": bi("Pflanzengruppen im Reußenland (S. 72, 74, 75)", "Plant groups in the Reuss territory (pp. 72, 74, 75)"),
         "columns": [
             col("group_key", "Gruppe (Original)", "Group (original)", "string", None),
             col("group_de", "Gruppe", "Group", "string", None, True),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("class_key", "Klasse", "Class", "string", None, True),
             col("class_de", "Klasse (DE)", "Class (DE)", "string", None, True),
             col("class_en", "Klasse (EN)", "Class (EN)", "string", None, True),
             col("species", "Arten", "Species", "integer", "Arten"),
         ],
         "rows": groups,
         "source_refs": [{"page": "72", "block": "b3", "rows": "r2"}, {"page": "74", "block": "b2"}, {"page": "75", "block": "b1"}]},
        {"name": "overlap",
         "title": bi("Blütenpflanzen nach Landesteil und Klasse (S. 72)", "Flowering plants by part of the territory and class (p. 72)"),
         "columns": [
             col("part_de", "Teilmenge", "Subset", "string", None, True),
             col("part_en", "Teilmenge (EN)", "Subset (EN)", "string", None, True),
             col("part_order", "Reihenfolge", "Order", "integer", None, True),
             col("class_de", "Klasse (DE)", "Class (DE)", "string", None, True),
             col("class_en", "Klasse (EN)", "Class (EN)", "string", None, True),
             col("species", "Arten", "Species", "integer", "Arten"),
         ],
         "rows": overlap, "source_refs": [SRC72]},
    ],
    "charts": [],
    "keywords": {"de": ["Flora", "Phanerogamen", "Kryptogamen", "Artenzahl", "Moose", "Flechten", "Pilze", "Thüringen", "Franken", "Pflanzen"],
                 "en": ["flora", "phanerogams", "cryptogams", "species count", "mosses", "lichens", "fungi", "Thuringia", "Franconia", "plants"]},
    "related": ["flora-exklusivarten-unterland-oberland"],
    "generated_by": GEN,
    "date": DATE,
}

CLS = {"field": {"de": "class_de", "en": "class_en"}, "type": "nominal",
       "title": bi("Klasse", "Class"),
       "scale": {"domain": [{"de": CLASS[k][0], "en": CLASS[k][1]} for k in ("dicot", "monocot", "crypto")]}}
# the scale domain must be language specific -> resolved per language
ana["charts"] = [
    {"id": "c1", "dataset": "flora_groups",
     "title": bi("Pflanzenarten nach Gruppen", "Plant species by group"),
     "caption": bi("Arten je Pflanzengruppe im Fürstenthum Reuß j. L. nach Brückner. Blütenpflanzen sind nach Zwei- und Einkeimblättrigen getrennt, die blütenlosen Gruppen (ohne 78 Varietäten) zusammengefasst gefärbt.",
                   "Species per plant group in the principality of Reuss (younger line) according to Brückner. Flowering plants are split into dicotyledons and monocotyledons; the flowerless groups (excluding 78 varieties) share one colour."),
     "vegalite": {"height": 280, "mark": "bar",
                  "encoding": {
                      "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": "-x", "title": None},
                      "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species")},
                      "color": CLS,
                      "tooltip": [{"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                  {"field": "species", "title": bi("Arten", "Species")}]}}},
    {"id": "c2", "dataset": "phanerogams",
     "title": bi("Blütenpflanzen im Vergleich: Reußenland, Nachbarländer, Deutschland", "Flowering plants compared: Reuss territory, neighbouring regions, Germany"),
     "caption": bi("Arten der Blütenpflanzen, getrennt nach Zwei- und Einkeimblättrigen. Das Reußenland erreicht 38,5 % der deutschen Artenzahl, Thüringen 50,0 %, Franken 46,9 %.",
                   "Species of flowering plants, split into dicotyledons and monocotyledons. The Reuss territory reaches 38.5 % of the German species total, Thuringia 50.0 %, Franconia 46.9 %."),
     "vegalite": {"height": 260,
                  "transform": [{"filter": "datum.kind == 'area'"},
                                {"fold": ["dicots", "monocots"], "as": ["cls", "n"]},
                                {"calculate": {"de": "datum.cls == 'dicots' ? 'Zweikeimblättrige' : 'Einkeimblättrige'", "en": "datum.cls == 'dicots' ? 'Dicotyledons' : 'Monocotyledons'"}, "as": "cls_label"}],
                  "mark": "bar",
                  "encoding": {
                      "y": {"field": {"de": "land_de", "en": "land_en"}, "type": "nominal", "sort": {"field": "species", "order": "ascending"}, "title": None},
                      "x": {"field": "n", "type": "quantitative", "title": bi("Arten", "Species")},
                      "color": {"field": "cls_label", "type": "nominal", "title": bi("Klasse", "Class"),
                                "scale": {"domain": [{"de": "Zweikeimblättrige", "en": "Dicotyledons"}, {"de": "Einkeimblättrige", "en": "Monocotyledons"}]}},
                      "tooltip": [{"field": {"de": "land_de", "en": "land_en"}, "title": bi("Gebiet", "Area")},
                                  {"field": "cls_label", "title": bi("Klasse", "Class")},
                                  {"field": "n", "title": bi("Arten", "Species")},
                                  {"field": "species", "title": bi("Arten insgesamt", "Species in total")},
                                  {"field": "pct_of_germany", "title": bi("% der deutschen Arten", "% of German species")}]}}},
    {"id": "c3", "dataset": "overlap",
     "title": bi("Unterland und Oberland: gemeinsame und eigene Arten", "Unterland and Oberland: shared and exclusive species"),
     "caption": bi("Blütenpflanzen des Reußenlandes nach Vorkommen. Die nur im Oberland wachsenden Arten sind zu 83 % Zweikeimblättrige, die nur im Unterland wachsenden zu 74 %.",
                   "Flowering plants of the Reuss territory by occurrence. Of the species found only in the Oberland 83 % are dicotyledons, of those found only in the Unterland 74 %."),
     "vegalite": {"height": 200, "mark": "bar",
                  "encoding": {
                      "y": {"field": {"de": "part_de", "en": "part_en"}, "type": "nominal", "sort": {"field": "part_order", "op": "min"}, "title": None},
                      "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species"), "stack": True},
                      "color": {"field": {"de": "class_de", "en": "class_en"}, "type": "nominal", "title": bi("Klasse", "Class"),
                                "scale": {"domain": [{"de": "Zweikeimblättrige", "en": "Dicotyledons"}, {"de": "Einkeimblättrige", "en": "Monocotyledons"}]}},
                      "tooltip": [{"field": {"de": "part_de", "en": "part_en"}, "title": bi("Vorkommen", "Occurrence")},
                                  {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Klasse", "Class")},
                                  {"field": "species", "title": bi("Arten", "Species")}]}}},
]
# sanity for the percentages quoted in captions
assert round(100 * thu[4] / DEU, 1) == 50.0 and round(100 * fra[4] / DEU, 1) == 46.9 and round(100 * reuss[4] / DEU, 1) == 38.5, (thu[4] / DEU, fra[4] / DEU)
print("OL dicot share", 100 * ol[5] / ol[4], "UL", 100 * ul[5] / ul[4])
write(ana)
