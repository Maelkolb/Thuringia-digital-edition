import sys, collections
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\F3")
from common import *

MERGES = [
    "flora-artenzahlen-phanerogamen-kryptogamen",
    "flora-exklusivarten-unterland-oberland",
    "flora-seltene-pflanzen-fundorte",
    "wald-baumarten-flurnamen",
]

# ------------------------------------------------------------ exclusive species by family
species = dataset("flora-exklusivarten-unterland-oberland", "species")
sp = dicts(species)
active = [r for r in sp if r["status_key"] in ("printed", "added")]
fam = collections.defaultdict(collections.Counter)
for r in active:
    fam[r["family"]][r["region_de"]] += 1
U, O = "Nur im Unterland", "Nur im Oberland"
n_u = sum(c[U] for c in fam.values())
n_o = sum(c[O] for c in fam.values())
print("exclusive after corrections", n_u, n_o)

families = dataset("flora-exklusivarten-unterland-oberland", "family_counts")
fd = dicts(families)
# archived table must equal a recount from the species list
for r in fd:
    assert fam[r["family_de"]][r["region_de"]] == r["species"], (r["family_de"], r["region_de"], fam[r["family_de"]][r["region_de"]], r["species"])
selected = sorted({r["family_de"] for r in fd})
for f, c in fam.items():
    if max(c[U], c[O]) >= 4:
        assert f in selected, f
print("families", len(selected))

FAMILY_NAMES = {
    "Asteraceae": ("Korbblütler", "Daisy family"),
    "Apiaceae": ("Doldenblütler", "Carrot family"),
    "Brassicaceae": ("Kreuzblütler", "Cabbage family"),
    "Orchidaceae": ("Orchideen", "Orchids"),
    "Rosaceae": ("Rosengewächse", "Rose family"),
    "Cyperaceae": ("Sauergräser", "Sedges"),
    "Ranunculaceae": ("Hahnenfußgewächse", "Buttercup family"),
    "Lamiaceae": ("Lippenblütler", "Mint family"),
    "Plantaginaceae": ("Wegerichgewächse", "Plantain family"),
    "Poaceae": ("Süßgräser", "Grasses"),
    "Crassulaceae": ("Dickblattgewächse", "Stonecrop family"),
    "Asparagaceae": ("Spargelgewächse", "Asparagus family"),
}
balance = {f: fam[f][U] - fam[f][O] for f in selected}
order = {f: i + 1 for i, f in enumerate(sorted(selected, key=lambda f: (-balance[f], -fam[f][U], f)))}


def fn_fam(d):
    f = d["family_de"]
    return [FAMILY_NAMES[f][0], FAMILY_NAMES[f][1], balance[f], order[f]]


add_columns(
    families,
    [
        col("family_label_de", "Familie (deutsch)", "Family (German)", "string", None, True, "gebräuchlicher deutscher Name, redaktionell"),
        col("family_label_en", "Familie (englisch)", "Family (English)", "string", None, True),
        col("balance", "Unterland minus Oberland", "Unterland minus Oberland", "integer", "Arten", True),
        col("chart_order", "Reihenfolge in der Grafik", "Order in the chart", "integer", None, True),
    ],
    fn_fam,
)
top_u = [(r["family_de"], r["species"]) for r in fd if r["region_de"] == U]
asteraceae_u, orchid_u = fam["Asteraceae"][U], fam["Orchidaceae"][U]
asteraceae_o, orchid_o = fam["Asteraceae"][O], fam["Orchidaceae"][O]
brass_o, apiac_o = fam["Brassicaceae"][O], fam["Apiaceae"][O]

# ------------------------------------------------------------ comparison table
phan = dataset("flora-artenzahlen-phanerogamen-kryptogamen", "phanerogams")
pd = {r["land_key"]: r for r in dicts(phan)}
reuss, thur, fran, germ = pd["Reußenland"]["species"], pd["Thüringen"]["species"], pd["Franken"]["species"], pd["Deutschland"]["species"]
only_u, only_o, both = pd["Dem Unterlande allein gehörig"]["species"], pd["Dem Oberlande allein gehörig"]["species"], pd["Beiden gemeinschaftlich"]["species"]
print("phanerogams", reuss, thur, fran, germ, only_u, only_o, both)

groups = dataset("flora-artenzahlen-phanerogamen-kryptogamen", "flora_groups")
gd = {r["group_key"]: r for r in dicts(groups)}
total_species = sum(r["species"] for r in dicts(groups))
crypto = sum(r["species"] for r in dicts(groups) if r["class_key"] == "crypto")
print("total", total_species, "crypto", crypto, "flowering share", reuss / total_species)
assert reuss == gd["Dicotylen"]["species"] + gd["Monocotylen"]["species"]

# ------------------------------------------------------------ trees
trees = dataset("wald-baumarten-flurnamen", "field_names")
ROLE = {
    "Buche": ("stand", 1, "größere Bestände", "larger stands", "Größere Bestände von Laubholz bilden blos die Birke (Betulus alba) und die Buche (Roth- und Weißbuche)"),
    "Birke": ("stand", 1, "größere Bestände", "larger stands", "Größere Bestände von Laubholz bilden blos die Birke (Betulus alba) und die Buche (Roth- und Weißbuche)"),
    "Kiefer": ("stand", 1, "ganze Schläge", "whole stands", "daneben bildet die Kiefer oft ganze Schläge"),
    "Fichte": ("stand", 1, "Hauptbestand", "main stand", "überwiegend aus der Rothtanne oder Fichte bestehend"),
    "Eiche": ("single", 2, "nur hie und da", "only here and there", "Eichen (häufiger Quercus pedunculata, seltener Quercus sessiliflora), Aspen, schwarze Pappeln, Zitterpappeln und Vogelbeerbäume finden sich hie und da in Wäldern, an Waldrändern und an Straßen"),
    "Linde": ("single", 2, "Dorfbaum", "village tree", "Große und schattige, oft uralte Linden, sowie auch italienische Pappeln sind meist Dorfzierden"),
    "Erle": ("single", 2, "an Bachufern", "along streams", "Weiden und Erlen fassen die Ufer der Bäche ein"),
    "Weide": ("single", 2, "an Bachufern", "along streams", "Weiden und Erlen fassen die Ufer der Bäche ein"),
    "Ahorn": ("single", 2, "bei den Orten", "near villages", "Ulmen, Ahorn, Eschen und Kastanien stehen oft in der Nähe der Orte und auf freiem Felde"),
    "Esche": ("single", 2, "bei den Orten", "near villages", "Ulmen, Ahorn, Eschen und Kastanien stehen oft in der Nähe der Orte und auf freiem Felde"),
    "Eibe": ("none", 3, "heute nicht genannt", "not mentioned today", None),
    "Tanne": ("unclear", 4, "Tanne oder Fichte?", "fir or spruce?", None),
}
td = dicts(trees)
for r in td:
    assert r["tree_de"] in ROLE, r["tree_de"]
trees["rows"].sort(key=lambda r: (-r[2], r[0]))
td = dicts(trees)
rank = {r["tree_de"]: i + 1 for i, r in enumerate(td)}


def fn_tree(d):
    k = ROLE[d["tree_de"]]
    return [rank[d["tree_de"]], k[0], k[1], k[2], k[3], k[4]]


add_columns(
    trees,
    [
        col("chart_order", "Reihenfolge in der Grafik", "Order in the chart", "integer", None, True),
        col("role_key", "Rolle im heutigen Wald (Gruppe)", "Role in today’s forest (group)", "string", None, True, "redaktionelle Einordnung nach Brückners Wortlaut; Oberland"),
        col("role_order", "Ordnung der Rolle", "Role order", "integer", None, True),
        col("role_de", "Rolle im heutigen Wald des Oberlandes", "Role in today’s forest of the Oberland", "string", None, True),
        col("role_en", "Rolle (en)", "Role (en)", "string", None, True),
        col("role_quote", "Brückners Wortlaut zur Rolle", "Brückner’s wording on the role", "string", None, False, "S. 78; leer, wo er den Baum nicht nennt oder nicht von der Fichte trennt"),
    ],
    fn_tree,
)
tdd = dicts(trees)
tree_names_total = sum(r["names"] for r in tdd)
no_stand = sum(r["names"] for r in tdd if r["role_key"] in ("single", "none"))
stand = sum(r["names"] for r in tdd if r["role_key"] == "stand")
unclear = sum(r["names"] for r in tdd if r["role_key"] == "unclear")
print("names", tree_names_total, "stand", stand, "single/none", no_stand, "unclear", unclear, no_stand / tree_names_total)
assert stand + no_stand + unclear == tree_names_total
n_field_names = 43
fichte_names = next(r["names"] for r in tdd if r["tree_de"] == "Fichte")
birke_names = next(r["names"] for r in tdd if r["tree_de"] == "Birke")
buche_names = next(r["names"] for r in tdd if r["tree_de"] == "Buche")
eiche_names = next(r["names"] for r in tdd if r["tree_de"] == "Eiche")
tanne_names = next(r["names"] for r in tdd if r["tree_de"] == "Tanne")

# ------------------------------------------------------------ specs
FAM_Y = {
    "field": {"de": "family_label_de", "en": "family_label_en"},
    "type": "nominal",
    "sort": {"field": "chart_order", "op": "min"},
    "axis": None,
}
X_AXIS_VALUES = [0, 5, 10, 15]


def side_panel(region, color, reverse, title_de, title_en, anchor, highlight):
    xs = {"domain": [0, 20], "nice": False}
    if reverse:
        xs["reverse"] = True
    return {
        "width": 290,
        "height": {"step": 22},
        "title": {"text": bi(title_de, title_en), "anchor": anchor, "fontSize": 12, "fontWeight": 600, "offset": 8},
        "transform": [{"filter": f"datum.region_de == '{region}'"}],
        "layer": [
            {
                "mark": {"type": "bar", "color": color, "height": {"band": 0.72}},
                "encoding": {
                    "opacity": {"condition": {"test": f"indexof({highlight!r}, datum.family_de) >= 0", "value": 1}, "value": 0.5},
                    "y": FAM_Y,
                    "x": {"field": "species", "type": "quantitative", "scale": xs, "axis": {"title": None, "values": X_AXIS_VALUES, "grid": False, "labelFontSize": 10}},
                    "tooltip": [
                        tip({"de": "family_label_de", "en": "family_label_en"}, "Familie", "Family"),
                        tip("family_de", "Wissenschaftlicher Name", "Scientific name"),
                        tip({"de": "region_de", "en": "region_en"}, "Vorkommen", "Occurrence"),
                        tip("species", "Arten", "Species"),
                    ],
                },
            },
            {
                "mark": {"type": "text", "style": "label", "align": "right" if reverse else "left", "dx": -5 if reverse else 5},
                "encoding": {"y": FAM_Y, "x": {"field": "species", "type": "quantitative", "scale": xs}, "text": {"field": "species"}},
            },
        ],
    }


c1 = {
    "spacing": 6,
    "hconcat": [
        side_panel(U, "@accent", True, f"Nur im Unterland ({n_u} Arten)", f"Unterland only ({n_u} species)", "end", ["Asteraceae", "Orchidaceae"]),
        {
            "width": 120,
            "height": {"step": 22},
            "title": {"text": " ", "fontSize": 12, "offset": 8},
            "transform": [{"filter": f"datum.region_de == '{U}'"}],
            "mark": {"type": "text", "style": "label", "align": "center", "fontSize": 12, "color": "@ink"},
            "encoding": {"y": FAM_Y, "x": {"value": 60}, "text": {"field": {"de": "family_label_de", "en": "family_label_en"}}},
        },
        side_panel(O, "@accent2", False, f"Nur im Oberland ({n_o} Arten)", f"Oberland only ({n_o} species)", "start", ["Brassicaceae", "Apiaceae"]),
    ],
}

c2 = {
    "height": {"step": 34},
    "transform": [{"filter": "indexof(['Deutschland','Thüringen','Franken','Reußenland'], datum.land_key) >= 0"}],
    "encoding": {
        "y": {"field": {"de": "land_de", "en": "land_en"}, "type": "nominal", "sort": {"field": "species", "op": "max", "order": "descending"}, "axis": {"title": None, "labelFontSize": 13, "labelLimit": 240}},
        "x": {"field": "species", "type": "quantitative", "scale": {"domain": [0, 3600], "nice": False}, "axis": {"title": None, "values": [0, 1000, 2000, 3000], "format": ",d"}},
    },
    "layer": [
        {
            "mark": {"type": "bar", "height": {"band": 0.55}},
            "encoding": {
                "color": {"condition": {"test": "datum.land_key == 'Reußenland'", "value": "@accent"}, "value": "@context"},
                "tooltip": [
                    tip({"de": "land_de", "en": "land_en"}, "Gebiet", "Area"),
                    tip("species", "Blütenpflanzenarten", "Flowering plant species", ",d"),
                    tip("dicots", "Zweikeimblättrige", "Dicotyledons", ",d"),
                    tip("monocots", "Einkeimblättrige", "Monocotyledons", ",d"),
                    tip("pct_of_germany", "Anteil an Deutschland (%)", "Share of Germany (%)", ".1f"),
                ],
            },
        },
        {
            "mark": {"type": "text", "style": "label", "align": "left", "dx": 6},
            "encoding": {"text": {"field": "species", "format": ",d"}},
        },
        {
            "transform": [{"filter": "datum.land_key != 'Deutschland'"}],
            "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 50},
            "encoding": {"text": {"field": "pct_label"}},
        },
    ],
}

c3 = {
    "height": {"step": 22},
    "encoding": {
        "y": {"field": {"de": "tree_de", "en": "tree_en"}, "type": "nominal", "sort": {"field": "chart_order", "op": "min"}, "axis": {"title": None, "labelFontSize": 12}},
        "x": {"field": "names", "type": "quantitative", "scale": {"domain": [0, 13], "nice": False}, "axis": None},
    },
    "layer": [
        {
            "mark": {"type": "bar", "height": {"band": 0.62}},
            "encoding": {
                "color": {
                    "condition": [
                        {"test": "datum.role_key == 'stand'", "value": "@context"},
                        {"test": "datum.role_key == 'unclear'", "value": "@muted"},
                    ],
                    "value": "@accent",
                },
                "tooltip": [
                    tip({"de": "tree_de", "en": "tree_en"}, "Baum", "Tree"),
                    tip("names", "Flurnamen", "Field names"),
                    tip("examples", "Beispiele", "Examples"),
                    tip({"de": "role_de", "en": "role_en"}, "Heute im Oberland", "Today in the Oberland"),
                    tip("role_quote", "Brückner", "Brückner"),
                ],
            },
        },
        {
            "mark": {"type": "text", "style": "label", "align": "left", "dx": 6},
            "encoding": {"text": {"field": "names"}},
        },
        {
            "mark": {"type": "text", "style": "label-muted", "align": "left", "dx": 24},
            "encoding": {"text": {"field": {"de": "role_de", "en": "role_en"}}},
        },
    ],
}

# pct label (derived column on phanerogams): "38 %"
add_columns(
    phan,
    [col("pct_label", "Anteil an Deutschland (Beschriftung)", "Share of Germany (label)", "string", None, True)],
    lambda d: [f"{round(d['pct_of_germany'])} %"],
)

# ------------------------------------------------------------ texts
share_flowering = reuss / total_species * 100
summary_de = (
    f"Brückner zählt für das Reußenland {n_de(reuss)} Blütenpflanzen und {n_de(crypto)} blütenlose Pflanzen, zusammen {n_de(total_species)} Arten. "
    f"Die Blütenflora entspricht {n_de(round(reuss / thur * 100))} Prozent der thüringischen und {n_de(round(reuss / germ * 100))} Prozent der deutschen. "
    f"Nach seinen berichtigten Listen wachsen {n_u} Arten nur im Unterland, {n_o} nur im Oberland, {n_de(both)} in beiden. Nach Brückner deuten Flurnamen mit Baumnamen auf einen früher größeren Baumartenreichtum."
)
summary_en = (
    f"For the Reuss territory Brückner counts {n_en(reuss)} flowering and {n_en(crypto)} flowerless plants, {n_en(total_species)} species in all. "
    f"The flowering flora equals {n_en(round(reuss / thur * 100))} percent of the Thuringian and {n_en(round(reuss / germ * 100))} percent of the German one. "
    f"By his corrected lists, {n_u} species grow in the Unterland only, {n_o} in the Oberland only, {n_en(both)} in both. According to Brückner, field names containing tree names point to a formerly greater variety of trees."
)
print("summary words", words(summary_de), words(summary_en))

f1_de = (
    f"Von {n_de(total_species)} Arten sind {n_de(share_flowering)} Prozent Blütenpflanzen. Unter den blütenlosen führen Laubmoose ({gd['Laubmoose']['species']}), Pilze ({gd['Pilze']['species']}) und Flechten ({gd['Flechten']['species']}). "
    f"Thüringen hat nur {n_de(thur - reuss)} Blütenpflanzenarten mehr als das Reußenland."
)
f1_en = (
    f"Of {n_en(total_species)} species, {n_en(share_flowering)} percent are flowering plants. Among the flowerless, mosses ({gd['Laubmoose']['species']}), fungi ({gd['Pilze']['species']}) and lichens ({gd['Flechten']['species']}) lead. "
    f"Thuringia has only {n_en(thur - reuss)} more flowering species than the Reuss territory."
)
f1_de = f1_de.replace(n_de(share_flowering), n_de(round(share_flowering)))
f1_en = f1_en.replace(n_en(share_flowering), n_en(round(share_flowering)))
f2_de = (
    f"Von den {n_u} nur im Unterland wachsenden Arten sind {asteraceae_u + orchid_u} Korbblütler oder Orchideen, von den {n_o} nur im Oberland {asteraceae_o + orchid_o}. "
    f"Dort führen Kreuz- und Doldenblütler mit zusammen {brass_o + apiac_o} Arten."
)
f2_en = (
    f"Of the {n_u} species growing only in the Unterland, {asteraceae_u + orchid_u} are composites or orchids; of the {n_o} only in the Oberland, {asteraceae_o + orchid_o}. "
    f"There, crucifers and umbellifers lead with {brass_o + apiac_o} species."
)
f3_de = (
    f"Von {n_field_names} Flurnamen des Oberlands enthalten {tree_names_total} einen Baumnamen; Birke und Buche je {birke_names}, Eiche {eiche_names}, Tanne {tanne_names}. "
    f"Die Fichte, heute Hauptbestand, steckt nur in {fichte_names} Namen."
)
f3_en = (
    f"Of {n_field_names} field names of the Oberland, {tree_names_total} contain a tree name; birch and beech {birke_names} each, oak {eiche_names}, fir {tanne_names}. "
    f"The spruce, today the main stand, appears in only {fichte_names} names."
)

title_c1 = bi(
    "Im Unterland ragen Korbblütler und Orchideen heraus, im Oberland Kreuz- und Doldenblütler",
    "The Unterland stands out for composites and orchids, the Oberland for crucifers and umbellifers",
)
title_c2 = bi(
    f"Das Reußenland zählt {n_de(reuss)} Blütenpflanzenarten, {n_de(round(reuss / germ * 100))} Prozent der deutschen Flora",
    f"The Reuss territory has {n_en(reuss)} flowering plant species, {n_en(round(reuss / germ * 100))} percent of the German flora",
)
title_c3 = bi(
    "Fast die Hälfte der Flurnamen mit Baumnamen nennt Bäume, die im Oberland heute keine Bestände bilden",
    "Nearly half of tree-based field names recall trees that form no stands in the Oberland today",
)
caption_c1 = bi(
    f"Pflanzen, die nur im Unterland (links) oder nur im Oberland (rechts) vorkommen, nach Familien; gezeigt sind Familien mit mindestens vier Arten in einem Landesteil. Listen nach Brückners Berichtigungen. S. 72–74, 830.",
    f"Plants occurring only in the Unterland (left) or only in the Oberland (right), by family; shown are families with at least four species in one part. Lists as corrected by Brückner. Pp. 72–74, 830.",
)
caption_c2 = bi(
    "Blütenpflanzenarten (Phanerogamen) im Vergleich; die graue Zahl nennt den Anteil an den deutschen Arten in Prozent. Brückner selbst rundet das Reußenland auf 38,4 Prozent ab. S. 72.",
    "Flowering plant species (phanerogams) compared; the grey number gives the share of the German species in percent. Brückner himself rounds the Reuss territory down to 38.4 percent. P. 72.",
)
caption_c3 = bi(
    f"Zahl der Flurnamen im Oberland je Baumart nach Brückners Liste von {n_field_names} Namen; die Beschriftung nennt die Rolle des Baums im heutigen Wald nach seinen Angaben. Grau: Baum bildet heute Bestände. S. 78.",
    f"Number of field names in the Oberland per tree species from Brückner’s list of {n_field_names} names; the label gives the tree’s role in today’s forest according to him. Grey: the tree forms stands today. P. 78.",
)

method_de = (
    "Die Tabelle auf S. 72 (Blütenpflanzen im Reußenland, in Thüringen, Franken und Deutschland) ist vollständig übernommen; die Kryptogamenzahlen stehen im Text auf S. 74 f. "
    "Die Verzeichnisse der Pflanzen, die nur im Unterland oder nur im Oberland vorkommen (S. 72–74), wurden Art für Art erfasst, Brückners Berichtigungen auf S. 830 sind eingearbeitet (drei Streichungen, drei Ergänzungen). "
    "Die Zuordnung zu Pflanzenfamilien folgt der heutigen Systematik; gezeigt sind die Familien mit mindestens vier Arten in einem der beiden Landesteile. "
    "Die Flurnamen (S. 78) wurden nach dem Baumnamen im Wortstamm ausgezählt; ›Tann-‹ bleibt eigene Gruppe, weil sich Tanne und Fichte nicht trennen lassen. "
    "Die Rolle jedes Baums im heutigen Wald des Oberlandes ist eine redaktionelle Einordnung nach Brückners Wortlaut (Hauptbestand, größere Bestände, nur einzeln). "
    "Nicht übernommen sind die Fundorte seltener Pflanzen bei Gera und Lobenstein (S. 76 f., 81), weil die wichtigsten Fundorte Flurstücke und Felsen sind, die im Ortsverzeichnis fehlen."
)
method_en = (
    "The table on p. 72 (flowering plants in the Reuss territory, Thuringia, Franconia and Germany) is taken over completely; the numbers for flowerless plants are in the text on pp. 74 f. "
    "The lists of plants occurring only in the Unterland or only in the Oberland (pp. 72–74) were recorded species by species, and Brückner’s corrections on p. 830 are included (three deletions, three additions). "
    "The assignment to plant families follows present-day systematics; shown are the families with at least four species in one of the two parts. "
    "The field names (p. 78) were counted by the tree name in the word stem; ‘Tann-’ remains a group of its own because fir and spruce cannot be told apart. "
    "The role of each tree in today’s forest of the Oberland is an editorial classification based on Brückner’s wording (main stand, larger stands, only singly). "
    "Not taken over are the sites of rare plants near Gera and Lobenstein (pp. 76 f., 81), because the most important sites are plots and rocks that are missing from the gazetteer."
)
print("method words", words(method_de), words(method_en))

caveats = [
    bi(
        "Die Verzeichnisse nennen keine Standorte. Die Unterschiede zwischen Unter- und Oberland deuten auf Boden und Klima hin (Brückner nennt das Unterland milder, das Oberland teich-, quell- und moorreich), sind aber damit nicht belegt. Brückner betont, dass die höheren Gebirgsgegenden botanisch noch nicht durchforscht sind (S. 71).",
        "The lists give no habitats. The differences between Unterland and Oberland point to soil and climate (Brückner calls the Unterland milder, the Oberland rich in ponds, springs and bogs) but are not proved by them. Brückner stresses that the higher mountain districts have not yet been botanically explored (p. 71).",
    ),
    bi(
        "Brückners Tabelle nennt 96 und 113 Arten, die berichtigten Listen enthalten 93 und 114. Die Tabellenzahlen hat er nicht geändert. Das gedruckte Verhältnis der Zwei- zu Einkeimblättrigen im Unterland (2,44 : 1) passt nicht zu 71 und 25 Arten (2,84 : 1); die Zahlen stimmen mit dem Faksimile überein.",
        "Brückner’s table gives 96 and 113 species, while the corrected lists contain 93 and 114. He did not change the table figures. The printed ratio of dicotyledons to monocotyledons in the Unterland (2.44 : 1) does not fit 71 and 25 species (2.84 : 1); the figures agree with the facsimile.",
    ),
    bi(
        "Die Zahlen für Thüringen (nach Schlechtendal) und Franken (nach der »Bavaria«) stammen aus anderen Florenwerken und sind wegen verschiedener Artbegriffe nur eingeschränkt vergleichbar. Für die blütenlosen Pflanzen gibt Brückner keine Aufteilung nach Landesteilen.",
        "The figures for Thuringia (after Schlechtendal) and Franconia (after the “Bavaria”) come from other floras and are comparable only to a limited extent because of different species concepts. For flowerless plants Brückner gives no division by part of the country.",
    ),
    bi(
        "Flurnamen lassen sich zeitlich nicht einordnen; ein Stamm wie Birk- oder Eich- kann auch auf einzelne Bäume zurückgehen. Die Einordnung der Rolle im heutigen Wald vereinfacht Brückners freie Beschreibungen und gilt nur innerhalb dieses Stücks.",
        "Field names cannot be dated, and a stem such as Birk- or Eich- may also refer to single trees. The classification of the role in today’s forest simplifies Brückner’s free descriptions and holds only within this piece.",
    ),
]

feature = {
    "id": "pflanzenwelt",
    "title": bi("Pflanzenwelt", "Flora"),
    "category": "flora",
    "section": "t1-1-8",
    "merges": MERGES,
    "sources": union_sources("flora-artenzahlen-phanerogamen-kryptogamen", "flora-exklusivarten-unterland-oberland", "wald-baumarten-flurnamen"),
    "summary": bi(summary_de, summary_en),
    "findings": [bi(f1_de, f1_en), bi(f2_de, f2_en), bi(f3_de, f3_en)],
    "method": bi(method_de, method_en),
    "caveats": caveats,
    "datasets": [families, phan, trees, groups, species],
    "charts": [
        {"id": "c1", "dataset": "family_counts", "title": title_c1, "caption": caption_c1, "vegalite": c1},
        {"id": "c2", "dataset": "phanerogams", "title": title_c2, "caption": caption_c2, "vegalite": c2},
        {"id": "c3", "dataset": "field_names", "title": title_c3, "caption": caption_c3, "vegalite": c3},
    ],
    "transcription_issues": [t for t in union_issues(*MERGES)],
    "keywords": {
        "de": ["Pflanzenwelt", "Flora", "Phanerogamen", "Kryptogamen", "Blütenpflanzen", "Korbblütler", "Orchideen", "Baumarten", "Flurnamen", "Fichte", "Unterland", "Oberland"],
        "en": ["flora", "plants", "phanerogams", "cryptogams", "flowering plants", "orchids", "tree species", "field names", "spruce", "Unterland", "Oberland"],
    },
    "related": ["phaenologie", "tierwelt", "wald-holz", "geologie-boden"],
    "generated_by": GENERATED_BY.format(k=len(MERGES)),
    "date": DATE,
}
print(check_lengths(feature))
print(write_feature(feature))
