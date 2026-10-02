"""Analysis: species counts of the fauna (pp. 82-90)."""
from common import *

# -------- overview (printed numbers) -------------------------------------------------------
# group key, de, en, n, approximate?, note de, note en, page, block
OV = [
    ("mammals", "Säugetiere", "Mammals", 50, 0, "»An Säugethieren kommen im Lande 50 Arten vor«", "“50 species of mammals occur in the country”", "82", "b2"),
    ("birds", "Vögel", "Birds", 280, 1, "Brutvögel »gegen 140«, Gesamtzahl »ca. 280«", "breeding birds “about 140”, total “ca. 280”", "83", "b2"),
    ("reptiles", "Reptilien, Amphibien", "Reptiles, amphibians", 19, 0, "»19 Arten«", "“19 species”", "86", "b3"),
    ("fish", "Fische", "Fish", None, 0, "34 Arten in der Tabelle S. 87–88 (Nummern 1–34)", "34 species in the table pp. 87–88 (numbers 1–34)", "87", "b2"),
    ("molluscs", "Weichtiere", "Molluscs", 82, 0, "9 Muscheln und 73 Schnecken in 22 Geschlechtern", "9 bivalves and 73 snails in 22 genera", "88", "b3"),
    ("butterflies", "Schmetterlinge", "Butterflies and moths", 489, 0, "Umgebung von Zeulenroda, nach Lehrer Schreck; nur ein Teil des Landes", "Zeulenroda area, after the teacher Schreck; only part of the territory", "89", "b4"),
]
g87 = grid("87", "b2")
g88 = grid("88", "b1")
nums = [int(r[0].split(".")[0]) for r in g87[1:]] + [int(r[0].split(".")[0]) for r in g88[1:]]
assert nums == list(range(1, 35)), nums
n_fish = len(nums)
need("50 Arten", "82", "b2")
need("gegen 140", "83", "b2")
need("ca. 280", "83", "b2")
need("19 Arten", "86", "b3")
need("82 Arten in 22 Geschlechtern", "88", "b3")
ov_rows = []
for k, d_, e_, n, approx, nd, ne, pg, bk in OV:
    n = n_fish if k == "fish" else n
    ov_rows.append([k, d_, e_, n, approx, nd, ne, pg, bk])
ov_rows.sort(key=lambda r: -r[3])
by = {r[0]: r for r in ov_rows}
vert = by["mammals"][3] + by["birds"][3] + by["reptiles"][3] + by["fish"][3]

# -------- insects compared with neighbouring regions ---------------------------------------
INS = [
    ("Reuß (Zeulenroda)", "Reuss (Zeulenroda)", "Schmetterlinge", "Butterflies and moths", 489, 0, "89", "b4"),
    ("Schwarzb. Oberland", "Schwarzburg Oberland", "Schmetterlinge", "Butterflies and moths", 601, 0, "89", "b4"),
    ("Franken", "Franconia", "Schmetterlinge", "Butterflies and moths", 1800, 0, "89", "b4"),
    ("Schwarzb. Oberland", "Schwarzburg Oberland", "Käfer", "Beetles", 1000, 1, "89", "fn2"),
    ("Franken", "Franconia", "Käfer", "Beetles", 2800, 1, "89", "b3"),
    ("Altbayern", "Old Bavaria", "Käfer", "Beetles", 3000, 1, "89", "b3"),
]
need("601 Arten", "89", "b4")
need("1800", "89", "b4")
need("beiläufig 2800", "89", "b3")
need("ca. 3000", "89", "b3")
need("1000 Arten", "89", "fn2")
ins_order = {"Reuß (Zeulenroda)": 1, "Schwarzb. Oberland": 2, "Franken": 3, "Altbayern": 4}
ins_rows = [[r[0], r[1], ins_order[r[0]], r[2], r[3], r[4], r[5], r[6], r[7]] for r in INS]

# -------- Lepidoptera families --------------------------------------------------------------
LEP = [("Tagfalter", "Butterflies", "Papilioniden", 84), ("Schwärmer", "Hawkmoths", "Sphingiden", 31),
       ("Spinner", "Bombycids", "Bombyciden (im Druck »Spanner«)", 73), ("Eulen", "Owlet moths", "Noctuiden", 166),
       ("Spanner", "Geometers", "Geometriden", 135)]
need("84 Arten Tagfalter", "89", "b4")
need("31 Schwärmer", "89", "b4")
need("73 Spanner oder Bombyciden", "89", "b4")
need("166 Eulen", "89", "b4")
need("135 Spanner oder Geometriden", "89", "b4")
assert sum(x[3] for x in LEP) == 489
lep_rows = [[a, b, c, n] for a, b, c, n in LEP]
lep_rows.sort(key=lambda r: -r[3])

# -------- molluscs by genus (p.88 b3, b4) -----------------------------------------------------
SNAIL = [
    ("Daudebardia", "Daudebardia (Nacktschnecke)", ["rufa"]),
    ("Arion", "Arion (Nacktschnecke)", ["ater", "rufus", "albus", "hortensis"]),
    ("Limax", "Limax (Nacktschnecke)", ["cinereus", "agrestis"]),
    ("Vitrina", "Vitrina (Glasschnecke)", ["pellucida", "diaphana"]),
    ("Zonites", "Zonites (Knoblauchschnecke)", ["cellarius", "glaber", "hyalinus", "crystallinus", "nitidulus", "nitidosus", "lucidus", "fulvus"]),
    ("Helix", "Helix (Schnirkelschnecke)", ["pygmaea", "aculeata", "strigella", "bidentata", "umbrosa", "rotundata", "obvoluta", "personata", "lapicida", "arbustorum", "pulchella", "costata", "sericea", "hispida", "incarnata", "fruticum", "ericetorum", "nemoralis", "hortensis", "pomatia"]),
    ("Sira", "Sira (Sira acicula)", ["acicula"]),
    ("Bulimus", "Bulimus", ["lubricus", "montanus", "obscurus"]),
    ("Pupa", "Pupa (Windelschnecke)", ["muscorum", "Venetzii", "pygmaea"]),
    ("Balea", "Balea (Gebirgsform)", ["fragilis"]),
    ("Clausilia", "Clausilia", ["ventricosa", "similis", "plicata", "rugosa", "obtusa", "filograna", "parvula", "bidens"]),
    ("Succinea", "Succinea (Bernsteinschnecke)", ["putris", "Pfeifferi", "oblonga"]),
    ("Carychium", "Carychium (Ohrschnecke)", ["minimum"]),
    ("Limnaeus", "Limnaeus (Schlammschnecke)", ["stagnalis", "auricularius", "ovatus", "pereger", "palustris", "minutus", "fuscus"]),
    ("Physa", "Physa (Blasenschnecke)", ["fontinalis"]),
    ("Planorbis", "Planorbis (Napfschnecke)", ["contortus", "nitidus", "marginatus", "leucostoma", "albus"]),
    ("Bythinia", "Bythinia (Kammkiemenschnecke)", ["impura"]),
]
MUSSEL = [
    ("Unio", "Unio (Malermuschel)", ["pictorum", "crassus", "batavus", "margaritifer"]),
    ("Anadonta", "Anadonta (Teichmuschel)", ["cygnea", "piscinalis"]),
    ("Pisidium", "Pisidium (Erbsenmuschel)", ["fontinale"]),
    ("Cyclas", "Cyclas", ["cornea", "calyculata"]),
]
t88 = text("88", "b3") + " " + text("88", "b4")
for g, _, sp in SNAIL + MUSSEL:
    need(g, "88", "b3") if (g, _, sp) in SNAIL else need(g, "88", "b4")
    for s in sp:
        assert s in t88, (g, s)
mol_rows = []
for kind_de, kind_en, lst in (("Schnecken", "Snails", SNAIL), ("Muscheln", "Bivalves", MUSSEL)):
    for g, lab, sp in lst:
        mol_rows.append([g, kind_de, kind_en, len(sp), ", ".join(sp)])
mol_rows.sort(key=lambda r: (-r[3], r[0]))
n_snail = sum(len(x[2]) for x in SNAIL)
n_mussel = sum(len(x[2]) for x in MUSSEL)
print("snails", n_snail, len(SNAIL), "mussels", n_mussel, len(MUSSEL), "total", n_snail + n_mussel, len(SNAIL) + len(MUSSEL))
helix = len(SNAIL[5][2])

pc = lambda a, b: 100 * a / b
REFS_OV = [{"page": "82", "block": "b2"}, {"page": "83", "block": "b2"}, {"page": "86", "block": "b3"}, {"page": "87", "block": "b2", "rows": "r2-r27"},
           {"page": "88", "block": "b1", "rows": "r2-r9"}, {"page": "88", "block": "b3"}, {"page": "89", "block": "b4"}]
ana = {
    "id": "fauna-artenzahlen-tiergruppen",
    "title": bi("Artenzahlen der Tierwelt", "Species counts of the fauna"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": REFS_OV + [{"page": "89", "block": "b3"}, {"page": "89", "block": "fn2"}, {"page": "88", "block": "b4"}, {"page": "88", "block": "b5"}, {"page": "89", "block": "b1"}],
    "summary": bi(
        f"Brückner nennt für einige Tiergruppen Artenzahlen des Fürstenthums: 50 Säugetiere, rund 280 Vögel, 19 Reptilien und Amphibien, 34 Fische, 82 Weichtiere und für die Umgebung von Zeulenroda 489 Schmetterlinge. Für die übrigen Insektenordnungen fehlen Zählungen; er verweist auf Nachbarländer. Die Diagramme ordnen die Zahlen, vergleichen die Insektenzahlen mit Nachbarregionen und gliedern Schmetterlinge und Weichtiere weiter auf.",
        f"Brückner gives species counts of the principality for a number of animal groups: 50 mammals, about 280 birds, 19 reptiles and amphibians, 34 fish, 82 molluscs and, for the Zeulenroda area, 489 butterflies and moths. For the other insect orders no counts exist; he refers to neighbouring regions. The charts arrange the figures, compare the insect numbers with neighbouring regions and break down the Lepidoptera and the molluscs."),
    "method": bi(
        "Die Zahlen stammen aus dem Fließtext (S. 82, 83, 86, 88, 89) und aus der Fischtabelle (S. 87–88; die 34 Arten sind in der Tabelle nummeriert). Die Gesamtzahl der Vögel (ca. 280) und die der Brutvögel (gegen 140) sind ungefähre Angaben. Die Aufschlüsselung der Weichtiere wurde aus den namentlich aufgeführten Arten (S. 88) gezählt (abgeleitet) und mit Brückners Summen verglichen. Die Schmetterlingszahl gilt nur für die Umgebung von Zeulenroda (Beobachtungen des Lehrers Schreck); die Vergleichszahlen für das Schwarzburger Oberland, Franken und Altbayern nennt Brückner ohne Quellenangabe, die Käferzahl für das Schwarzburger Oberland nach Prof. Sigismund.",
        "The figures come from the running text (pp. 82, 83, 86, 88, 89) and from the fish table (pp. 87–88; the 34 species are numbered in the table). The total for birds (ca. 280) and for breeding birds (about 140) are approximate statements. The breakdown of the molluscs was counted from the species named (p. 88; derived) and compared with Brückner's totals. The butterfly figure applies to the Zeulenroda area only (observations of the teacher Schreck); Brückner gives the comparison figures for the Schwarzburg Oberland, Franconia and Old Bavaria without citing a source, the beetle figure for the Schwarzburg Oberland after Prof. Sigismund."),
    "findings": [
        bi(f"Die Wirbeltiere des Landes machen nach Brückners Zahlen zusammen etwa {vert} Arten aus: {by['birds'][3]} Vögel, {by['mammals'][3]} Säugetiere, {by['fish'][3]} Fische und {by['reptiles'][3]} Reptilien und Amphibien. Unter den Wirbellosen nennt er Zahlen nur für Weichtiere ({by['molluscs'][3]}) und Schmetterlinge ({by['butterflies'][3]}, nur Raum Zeulenroda); die Schmetterlingszahl übersteigt jede einzelne Wirbeltierklasse, auch die Vögel.",
           f"According to Brückner's figures the vertebrates of the country amount to about {vert} species: {by['birds'][3]} birds, {by['mammals'][3]} mammals, {by['fish'][3]} fish and {by['reptiles'][3]} reptiles and amphibians. Among the invertebrates he gives figures only for molluscs ({by['molluscs'][3]}) and Lepidoptera ({by['butterflies'][3]}, Zeulenroda area only); the Lepidoptera figure exceeds every single vertebrate class, including the birds."),
        bi(f"Die 489 Schmetterlingsarten aus dem Raum Zeulenroda entsprechen {de(pc(489, 601), 0)} % der aus dem Schwarzburger Oberland gemeldeten 601 und {de(pc(489, 1800), 0)} % der 1800 Arten Frankens. Brückner hält seine Zahl selbst für zu klein. Am artenreichsten sind die Eulen (166, {de(pc(166, 489), 0)} %) und Spanner (135, {de(pc(135, 489), 0)} %).",
           f"The 489 species of butterflies and moths from the Zeulenroda area equal {en(pc(489, 601), 0)} % of the 601 reported from the Schwarzburg Oberland and {en(pc(489, 1800), 0)} % of Franconia's 1,800. Brückner himself considers his figure too small. The owlet moths (166, {en(pc(166, 489), 0)} %) and geometer moths (135, {en(pc(135, 489), 0)} %) are the richest groups."),
        bi(f"Bei den Weichtieren ist die Gattung Helix mit {helix} der {n_snail} aufgezählten Schneckenarten ({de(pc(helix, n_snail), 0)} %) am stärksten vertreten. Die Aufzählung ergibt {n_snail} Schnecken- und {n_mussel} Muschelarten ({n_snail + n_mussel}); Brückner nennt 73 und 9 (82). Fünf Arten kommen nur im Oberland, 17 nur im Unterland vor.",
           f"Among the molluscs the genus Helix is the best represented with {helix} of the {n_snail} listed snail species ({en(pc(helix, n_snail), 0)} %). The enumeration yields {n_snail} snail and {n_mussel} bivalve species ({n_snail + n_mussel}); Brückner gives 73 and 9 (82). Five species occur only in the Oberland, 17 only in the Unterland."),
        bi("Für Käfer fehlt jede Zahl aus dem Reußenland. Brückner verweist auf etwa 2800 Arten in Franken, etwa 3000 in Altbayern und 1000 im Schwarzburger Oberland (nach Sigismund) und erwartet, dass die Zahl auch im Reußenland »nicht gering« sei.",
           "No beetle figure exists for the Reuss territory. Brückner refers to about 2,800 species in Franconia, about 3,000 in Old Bavaria and 1,000 in the Schwarzburg Oberland (after Sigismund) and expects the number in the Reuss territory to be “not small”."),
    ],
    "caveats": [
        bi("Die Zahlen sind sehr unterschiedlich belastbar: Säugetiere, Reptilien und Fische sind Landeszahlen, die Vogelzahlen ungefähre Schätzungen (»ca. 280«), die Schmetterlingszahl bezieht sich nur auf einen Teil des Landes. Zwischen Gruppen sind die Werte daher nur als grobe Größenordnung vergleichbar.",
           "The figures differ greatly in reliability: mammals, reptiles and fish are national totals, the bird figures approximate estimates (“ca. 280”), the butterfly figure refers to only a part of the territory. Between groups the values are comparable only as rough orders of magnitude."),
        bi(f"Brückner nennt 73 Schneckenarten in 18 Geschlechtern und 9 Muscheln in 4 Geschlechtern; die namentliche Aufzählung ergibt {n_snail} Schneckenarten in {len(SNAIL)} und {n_mussel} Muscheln in {len(MUSSEL)} Geschlechtern, so dass zwei Arten und ein Geschlecht der Summe in der Aufzählung fehlen. Bei den Muscheln endet die Liste mit »etc. etc.«.",
           f"Brückner gives 73 snail species in 18 genera and 9 bivalves in 4 genera; the enumeration by name yields {n_snail} snail species in {len(SNAIL)} genera and {n_mussel} bivalves in {len(MUSSEL)} genera, so two species and one genus of the total are missing from the enumeration. The list of bivalves ends with “etc. etc.”."),
        bi("Im Druck steht bei den Schmetterlingen »73 Spanner oder Bombyciden«; gemeint sind nach dem Zusammenhang die Spinner (Bombyciden), die Spanner (Geometriden) folgen als eigene Gruppe mit 135 Arten. Die fünf Gruppen ergeben genau 489. Die Zahlen für Käfer (Franken, Altbayern) sind als »beiläufig« bzw. »ca.« gedruckt.",
           "In print the butterflies include “73 Spanner oder Bombyciden”; from the context the Spinner (Bombycidae) are meant, the Spanner (Geometridae) follow as a separate group with 135 species. The five groups add up to exactly 489. The beetle figures (Franconia, Old Bavaria) are printed as “approximately” and “ca.”."),
    ],
    "datasets": [
        {"name": "overview",
         "title": bi("Artenzahlen nach Tiergruppe (S. 82–89)", "Species counts by animal group (pp. 82–89)"),
         "columns": [
             col("group_key", "Gruppe (Schlüssel)", "Group (key)", "string", None, True),
             col("group_de", "Tiergruppe", "Animal group", "string", None, True),
             col("group_en", "Tiergruppe (EN)", "Animal group (EN)", "string", None, True),
             col("species", "Arten", "Species", "integer", "Arten", False, "Fische: Zahl der nummerierten Tabellenzeilen (abgeleitet)"),
             col("approximate", "Ungefähre Angabe (1 = ca.)", "Approximate (1 = ca.)", "integer", None, True),
             col("note_de", "Angabe bei Brückner", "Brückner's statement", "string", None),
             col("note_en", "Angabe (Übersetzung)", "Statement (translation)", "string", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": ov_rows, "source_refs": REFS_OV},
        {"name": "insect_comparison",
         "title": bi("Insektenzahlen im Vergleich (S. 89)", "Insect figures compared (p. 89)"),
         "columns": [
             col("region_de", "Gebiet", "Region", "string", None),
             col("region_en", "Gebiet (EN)", "Region (EN)", "string", None, True),
             col("region_order", "Reihenfolge", "Order", "integer", None, True),
             col("group_de", "Gruppe", "Group", "string", None),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("species", "Arten", "Species", "integer", "Arten"),
             col("approximate", "Ungefähre Angabe (1 = ca.)", "Approximate (1 = ca.)", "integer", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": ins_rows, "source_refs": [{"page": "89", "block": "b3"}, {"page": "89", "block": "b4"}, {"page": "89", "block": "fn2"}]},
        {"name": "lepidoptera",
         "title": bi("Schmetterlinge der Umgebung von Zeulenroda (S. 89)", "Butterflies and moths of the Zeulenroda area (p. 89)"),
         "columns": [
             col("group_de", "Gruppe", "Group", "string", None, True, "Brückner: Papilioniden, Sphingiden, Bombyciden, Noctuiden, Geometriden"),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("family_printed", "Bezeichnung bei Brückner", "Brückner's designation", "string", None),
             col("species", "Arten", "Species", "integer", "Arten"),
         ],
         "rows": lep_rows, "source_refs": [{"page": "89", "block": "b4"}]},
        {"name": "molluscs",
         "title": bi("Weichtiere nach Gattung (S. 88)", "Molluscs by genus (p. 88)"),
         "columns": [
             col("genus", "Gattung", "Genus", "string", None),
             col("kind_de", "Gruppe", "Group", "string", None, True),
             col("kind_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("species", "Arten (gezählt)", "Species (counted)", "integer", "Arten", True),
             col("species_names", "Arten bei Brückner", "Species in Brückner", "string", None),
         ],
         "rows": mol_rows, "source_refs": [{"page": "88", "block": "b3"}, {"page": "88", "block": "b4"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "overview",
         "title": bi("Artenzahlen nach Tiergruppen", "Species counts by animal group"),
         "caption": bi("Nach Brückner (ca. = ungefähre Angabe). Die Schmetterlingszahl gilt nur für die Umgebung von Zeulenroda; die Vogelzahl umfasst rund 140 Brutvögel und die Zug- und Gastvögel.",
                       "After Brückner (ca. = approximate). The butterfly figure applies to the Zeulenroda area only; the bird figure comprises about 140 breeding birds plus migrants and visitors."),
         "vegalite": {"height": 260, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": "-x", "title": None},
                          "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species")},
                          "tooltip": [{"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                      {"field": "species", "title": bi("Arten", "Species")},
                                      {"field": {"de": "note_de", "en": "note_en"}, "title": bi("Angabe", "Statement")}]}}},
        {"id": "c2", "dataset": "insect_comparison",
         "title": bi("Schmetterlinge und Käfer: Vergleichszahlen aus Nachbarregionen", "Butterflies and beetles: comparison figures from neighbouring regions"),
         "caption": bi("Nach Brückner (S. 89). Für das Reußenland liegt nur die Schmetterlingszahl für Zeulenroda vor; Käferzahlen sind ungefähr (ca.).",
                       "After Brückner (p. 89). For the Reuss territory only the butterfly figure for Zeulenroda exists; beetle figures are approximate (ca.)."),
         "vegalite": {"height": 280, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal", "sort": {"field": "region_order", "op": "min"}, "title": None},
                          "yOffset": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal"},
                          "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species")},
                          "color": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "title": bi("Gruppe", "Group"),
                                    "scale": {"domain": [{"de": "Schmetterlinge", "en": "Butterflies and moths"}, {"de": "Käfer", "en": "Beetles"}]}},
                          "tooltip": [{"field": {"de": "region_de", "en": "region_en"}, "title": bi("Gebiet", "Region")},
                                      {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                      {"field": "species", "title": bi("Arten", "Species")}]}}},
        {"id": "c3", "dataset": "lepidoptera",
         "title": bi("Schmetterlinge bei Zeulenroda nach Gruppen (489 Arten)", "Butterflies and moths near Zeulenroda by group (489 species)"),
         "caption": bi("Beobachtungen des Lehrers Schreck; die Gruppe »Spinner« steht im Druck als »Spanner oder Bombyciden«.",
                       "Observations of the teacher Schreck; the group “Spinner” appears in print as “Spanner oder Bombyciden”."),
         "vegalite": {"height": 220, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": "-x", "title": None},
                          "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species")},
                          "tooltip": [{"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                      {"field": "family_printed", "title": bi("Bei Brückner", "In Brückner")},
                                      {"field": "species", "title": bi("Arten", "Species")}]}}},
        {"id": "c4", "dataset": "molluscs",
         "title": bi("Weichtiere nach Gattung", "Molluscs by genus"),
         "caption": bi(f"Zahl der namentlich aufgeführten Arten ({n_snail} Schnecken, {n_mussel} Muscheln). Brückner zählt 73 Schnecken und 9 Muscheln.",
                       f"Number of species named ({n_snail} snails, {n_mussel} bivalves). Brückner counts 73 snails and 9 bivalves."),
         "vegalite": {"height": 400, "mark": "bar",
                      "encoding": {
                          "y": {"field": "genus", "type": "nominal", "sort": "-x", "title": None},
                          "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species"), "axis": {"tickMinStep": 1}},
                          "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": bi("Gruppe", "Group"),
                                    "scale": {"domain": [{"de": "Schnecken", "en": "Snails"}, {"de": "Muscheln", "en": "Bivalves"}]}},
                          "tooltip": [{"field": "genus", "title": bi("Gattung", "Genus")},
                                      {"field": "species", "title": bi("Arten", "Species")},
                                      {"field": "species_names", "title": bi("Arten bei Brückner", "Species in Brückner")}]}}},
    ],
    "keywords": {"de": ["Fauna", "Tierwelt", "Artenzahl", "Säugetiere", "Vögel", "Fische", "Schmetterlinge", "Käfer", "Schnecken", "Muscheln", "Zeulenroda"],
                 "en": ["fauna", "animals", "species count", "mammals", "birds", "fish", "butterflies", "beetles", "snails", "bivalves", "Zeulenroda"]},
    "related": ["fauna-fische-gewaesser"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
