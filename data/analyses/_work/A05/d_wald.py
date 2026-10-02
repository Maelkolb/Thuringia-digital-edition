"""Analysis: forest trees today (Unterland / Oberland) and tree names in field names (pp. 71, 77-79)."""
import re
from collections import Counter
from common import *

# ---------------------------------------------------------------- field names with tree words (p.78 b2)
t78 = text("78", "b2")
quoted = re.findall(r"„([^“]*)“", t78)
names = [n.strip() for n in re.split(r", | und ", quoted[1])]
assert len(names) == 43 and len(re.split(r", | und ", quoted[0])) == 21
TREE = [("Eich", "Eiche", "Oak", "Eiche"), ("Ficht", "Fichte", "Spruce", "Fichte"), ("Tann", "Tanne", "Fir (“Tanne”)", "Tanne"),
        ("lange Tannen", "Tanne", "Fir (“Tanne”)", "Tanne"), ("Tänn", "Tanne", "Fir (“Tanne”)", "Tanne"),
        ("Buch", "Buche", "Beech", "Buche"), ("Büch", "Buche", "Beech", "Buche"), ("Birk", "Birke", "Birch", "Birke"),
        ("Lind", "Linde", "Lime (linden)", "Linde"), ("Siebenlinden", "Linde", "Lime (linden)", "Linde"),
        ("Kief", "Kiefer", "Pine", "Kiefer"), ("kiefern", "Kiefer", "Pine", "Kiefer"), ("Erl", "Erle", "Alder", "Erle"),
        ("Eib", "Eibe", "Yew", "Eibe"), ("Ahorn", "Ahorn", "Maple", "Ahorn"), ("Esch", "Esche", "Ash", "Esche"),
        ("Weid", "Weide", "Willow", "Weide")]
fl_rows = []
unassigned = []
for n in names:
    for pre, de_, en_, key in TREE:
        if n.startswith(pre):
            fl_rows.append([n, de_, en_, 1])
            break
    else:
        unassigned.append(n)
print("unassigned", unassigned, "assigned", len(fl_rows))
cnt = Counter(r[1] for r in fl_rows)
print(cnt.most_common())
# collapse to a count table (one row per tree)
tree_en = {r[1]: r[2] for r in fl_rows}
fl_tab = []
for k, v in cnt.most_common():
    ex = [r[0] for r in fl_rows if r[1] == k]
    fl_tab.append([k, tree_en[k], v, ", ".join(ex)])
n_fl = len(fl_rows)

# ---------------------------------------------------------------- present-day roles (p.77 b3, p.78 b2, p.79 b1)
# level 3 = Hauptbestand ("Hauptbestandtheil", "überwiegend"), 2 = größere Bestände / ganze Schläge,
# 1 = nur kleine Bestände, zerstreut, einzeln, an bestimmten Stellen
LV = {3: ("Hauptbestand", "Main stand"), 2: ("größere Bestände", "Larger stands"), 1: ("zerstreut, örtlich", "Scattered, local")}
S = {
    "ul_main": ("Die Waldungen haben übrigens ihren Hauptbestandtheil in der Rothtanne.", "The woods have their main constituent in the spruce.", "77", "b3"),
    "ul_small": ("bilden nur auf wenig Stellen, namentlich um Osterstein, kleinere Bestände, sonst sind sie in den Fichtenwäldern zerstreut", "form smaller stands in few places only, notably around Osterstein, otherwise they are scattered in the spruce forests", "77", "b3"),
    "ul_oak": ("wird nur noch auf dem Hain- und Weinberg und auf der Lasur", "is now found only on the Hainberg, the Weinberg and the Lasur", "77", "b3"),
    "ul_lime": ("findet sich einzeln im Laubwalde, in Dörfern, Gärten und Alleen", "occurs singly in deciduous woods, in villages, gardens and avenues", "77", "b3"),
    "ul_larch": ("Waldbäumen auf dem Hainberg und im Martinsgrund hat man die Lärche beigepflanzt", "the larch has been planted among the forest trees on the Hainberg and in the Martinsgrund", "77", "b3"),
    "ul_scatter": ("Ulmen, weiße Ahorn, Vogelbeerbäume, Eschen und Ebereschen kommen zerstreut in Wald und Flur vor", "elms, sycamores, rowans and ashes occur scattered in forest and field", "77", "b3"),
    "ul_juniper": ("Wachholder auf den Berghöhen", "juniper on the mountain tops", "77", "b3"),
    "ol_main": ("überwiegend aus der Rothtanne oder Fichte bestehend", "consisting predominantly of spruce", "78", "b2"),
    "ol_pine": ("daneben bildet die Kiefer oft ganze Schläge", "besides, the pine often forms whole felling areas", "78", "b2"),
    "ol_fir": ("die Edeltanne und Lärche, letztere meist an Waldrändern, nur vereinzelt vorkommen", "the silver fir and the larch, the latter mostly at forest edges, occur only singly", "78", "b2"),
    "ol_decid": ("Größere Bestände von Laubholz bilden blos die Birke (Betulus alba) und die Buche (Roth- und Weißbuche)", "Only the birch and the beech (red beech and hornbeam) form larger stands of broadleaf trees", "78", "b2"),
    "ol_here": ("Aspen, schwarze Pappeln, Zitterpappeln und Vogelbeerbäume finden sich hie und da in Wäldern, an Waldrändern und an Straßen", "aspens, black poplars, trembling poplars and rowans are found here and there in woods, at forest edges and along roads", "78", "b2"),
    "ol_banks": ("Weiden und Erlen fassen die Ufer der Bäche ein", "willows and alders line the banks of the streams", "78", "b2"),
    "ol_lime": ("Große und schattige, oft uralte Linden, sowie auch italienische Pappeln sind meist Dorfzierden", "large, shady, often ancient limes and also Lombardy poplars are mostly village ornaments", "78", "b2"),
    "ol_near": ("ferner Ulmen, Ahorn, Eschen und Kastanien stehen oft in der Nähe der Orte und auf freiem Felde", "furthermore elms, maples, ashes and chestnuts often stand near the villages and in open fields", "78", "b2"),
}
SPR, FIR, PINE, BEECH, BIRCH, LARCH, OAK, LIME = ("Fichte (Rothtanne)", "Spruce"), ("Weißtanne", "Silver fir"), ("Kiefer", "Pine"), ("Buche, Weißbuche", "Beech, hornbeam"), ("Birke", "Birch"), ("Lärche", "Larch"), ("Eiche", "Oak"), ("Linde", "Lime (linden)")
ELM, ROWAN, POP, BANK, JUN = ("Ulme, Ahorn, Esche", "Elm, maple, ash"), ("Vogelbeere", "Rowan"), ("Espe, Pappel", "Aspen, poplar"), ("Weide, Erle", "Willow, alder"), ("Wacholder", "Juniper")
ROLES = [  # (tree, region, level, sentence key)
    (SPR, "UL", 3, "ul_main"), (FIR, "UL", 1, "ul_small"), (PINE, "UL", 1, "ul_small"), (BEECH, "UL", 1, "ul_small"), (BIRCH, "UL", 1, "ul_small"),
    (OAK, "UL", 1, "ul_oak"), (LIME, "UL", 1, "ul_lime"), (LARCH, "UL", 1, "ul_larch"), (ELM, "UL", 1, "ul_scatter"), (ROWAN, "UL", 1, "ul_scatter"),
    (JUN, "UL", 1, "ul_juniper"),
    (SPR, "OL", 3, "ol_main"), (PINE, "OL", 2, "ol_pine"), (FIR, "OL", 1, "ol_fir"), (LARCH, "OL", 1, "ol_fir"), (BIRCH, "OL", 2, "ol_decid"),
    (BEECH, "OL", 2, "ol_decid"), (OAK, "OL", 1, "ol_here"), (POP, "OL", 1, "ol_here"), (ROWAN, "OL", 1, "ol_here"), (BANK, "OL", 1, "ol_banks"),
    (LIME, "OL", 1, "ol_lime"), (ELM, "OL", 1, "ol_near"),
]
for k, (q, _, pg, bk) in S.items():
    need(q, pg, bk)
trees_order = [SPR[0], PINE[0], BIRCH[0], BEECH[0], FIR[0], LARCH[0], OAK[0], LIME[0], ELM[0], ROWAN[0], POP[0], BANK[0], JUN[0]]
role_rows = []
for (tr_de, tr_en), reg, lvl, key in ROLES:
    q, qe, pg, bk = S[key]
    rname = "Unterland" if reg == "UL" else "Oberland"
    role_rows.append([tr_de, tr_en, rname, rname, lvl, trees_order.index(tr_de) + 1, LV[lvl][0], LV[lvl][1], q, qe, pg, bk])

# numbers for the findings
oak_names, beech_names, birch_names = cnt["Eiche"], cnt["Buche"], cnt["Birke"]
top3 = cnt.most_common(3)
yew = cnt["Eibe"]
n_trees_names = len(cnt)
print(n_fl, n_trees_names, top3, yew)

REFS_FL = [{"page": "78", "block": "b2"}]
REFS_ROLE = [{"page": "77", "block": "b3"}, {"page": "78", "block": "b2"}]
ana = {
    "id": "wald-baumarten-flurnamen",
    "title": bi("Waldbäume heute und in Flurnamen", "Forest trees today and in field names"),
    "category": "forestry",
    "section": "t1-1-8",
    "sources": [{"page": "71", "block": "b1"}, {"page": "77", "block": "b3"}, {"page": "78", "block": "b2"}, {"page": "79", "block": "b2"}, {"page": "830", "block": "b12"}],
    "summary": bi(
        f"Brückner beschreibt die heutigen Waldbäume des Unterlandes und des Oberlandes und führt zum Beleg eines früheren Baumartenreichtums {len(names)} oberländische Flurnamen an, die Baumnamen enthalten. Ausgezählt zeigen die Flurnamen vor allem Birke, Buche, Eiche und Tanne, während heute die Fichte die Wälder beherrscht; die Rolle der übrigen Baumarten wurde nach Brückners Wortlaut in drei Stufen eingeordnet.",
        f"Brückner describes the present forest trees of the Unterland and the Oberland and, as evidence of a former wealth of tree species, cites {len(names)} Oberland field names that contain tree names. Counted, the field names show mainly birch, beech, oak and fir, whereas today the spruce dominates the woods; the role of the other species was classed in three levels following Brückner's wording."),
    "method": bi(
        f"Die Flurnamenliste (S. 78, {len(names)} Namen) wurde Wort für Wort ausgezählt und nach dem Baumnamen im Wortstamm geordnet (Eich-, Fichtig/Fichtere, Tann-, Buch-/Büch-, Birk-, Lind-, Kief-, Erl-, Eib-, Ahorn, Esch-, Weid-); {len(unassigned)} Namen ({', '.join(unassigned)}) enthalten keinen eindeutigen Baumnamen und wurden nicht gezählt. Die »Tann-«-Namen sind nicht von Fichte oder Weißtanne zu trennen und stehen für sich. Für die heutigen Waldbäume (S. 77 Unterland, S. 78 Oberland) wurde jede genannte Baumart nach Brückners Wortlaut in drei Stufen eingeordnet (3 Hauptbestand, 2 größere Bestände oder ganze Schläge, 1 nur kleine Bestände, zerstreut, einzeln oder örtlich). Die Stufen sind eine redaktionelle Kodierung (abgeleitet); der Wortlaut steht in der Datentabelle. Nicht aufgenommen sind angepflanzte Zier- und Gartenbäume sowie Sträucher. Aus S. 77 stammt außerdem die Angabe, dass westlich der Elster noch 3/5, östlich nur 2/5 der Fläche bewaldet sind.",
        f"The list of field names (p. 78, {len(names)} names) was counted word by word and ordered by the tree name in the word stem (Eich-, Fichtig/Fichtere, Tann-, Buch-/Büch-, Birk-, Lind-, Kief-, Erl-, Eib-, Ahorn, Esch-, Weid-); {len(unassigned)} names ({', '.join(unassigned)}) contain no unambiguous tree name and were not counted. The “Tann-” names cannot be separated from spruce or silver fir and stand on their own. For the present forest trees (p. 77 Unterland, p. 78 Oberland) every tree species mentioned was placed in three levels following Brückner's wording (3 main stand, 2 larger stands or whole felling areas, 1 only small stands, scattered, single or local). The levels are an editorial coding (derived); the wording is given in the data table. Ornamental and garden trees and shrubs are not included. P. 77 also states that west of the Elster 3/5 of the land is still wooded, east of it only 2/5."),
    "findings": [
        bi(f"Von {len(names)} Flurnamen enthalten {n_fl} einen Baumnamen. Am häufigsten sind Birke ({cnt['Birke']}) und Buche ({cnt['Buche']}), dann Eiche ({cnt['Eiche']}) und Tanne ({cnt['Tanne']}); zusammen sind es {n_trees_names} Baumarten.",
           f"Of {len(names)} field names, {n_fl} contain a tree name. Birch ({cnt['Birke']}) and beech ({cnt['Buche']}) are the most frequent, followed by oak ({cnt['Eiche']}) and fir ({cnt['Tanne']}); together there are {n_trees_names} tree species."),
        bi(f"Die Fichte ist nach Brückner in beiden Landesteilen der Hauptbestand; in den Flurnamen kommt sie nur mit {cnt['Fichte']} Namen vor (Fichtig, Fichtere). Eiben ({yew} Flurnamen) werden in der Beschreibung der heutigen Wälder gar nicht mehr genannt; Eichen sind im Unterland auf wenige Stellen (Hainberg, Weinberg, Lasur) beschränkt (S. 77).",
           f"According to Brückner the spruce is the main stand in both parts of the territory; in the field names it appears with only {cnt['Fichte']} names (Fichtig, Fichtere). Yews ({yew} field names) are no longer mentioned at all in the description of the present woods; oaks are confined to a few places (Hainberg, Weinberg, Lasur) in the Unterland (p. 77)."),
        bi("Im Unterland bilden außer der Fichte nur Weißtanne, Kiefer, Buche und Birke kleine Bestände; im Oberland kommen Kiefer, Birke und Buche zu größeren Beständen. Laubbäume sind in beiden Gebieten sonst zerstreut, an Bachufern oder als Dorfbäume zu finden.",
           "In the Unterland, apart from the spruce, only silver fir, pine, beech and birch form small stands; in the Oberland pine, birch and beech reach larger stands. Other broadleaf trees are scattered in both areas, found along stream banks or as village trees."),
    ],
    "caveats": [
        bi("Flurnamen lassen sich zeitlich nicht einordnen; Brückner nimmt an, dass sie auf einen früher größeren Reichtum an Baumarten in Beständen hinweisen. Ein Namensstamm wie Birk- oder Eich- kann auch auf einzelne Bäume oder Gehölzgruppen zurückgehen.",
           "Field names cannot be dated; Brückner assumes that they point to a formerly greater wealth of tree species in stands. A name stem such as Birk- or Eich- may also derive from single trees or small groves."),
        bi("Die Stufenkodierung vereinfacht freie Beschreibungen (»kleinere Bestände«, »vereinzelt«, »hie und da«) und ist nur innerhalb dieser Analyse vergleichbar; es gibt keine Flächenzahlen je Baumart.",
           "The level coding simplifies free descriptions (“smaller stands”, “singly”, “here and there”) and is comparable only within this analysis; there are no area figures per tree species."),
        bi("Brückner nennt »Rothtanne« und »Fichte« gleichbedeutend. Bei Namen wie Tanna oder Tännig bleibt offen, ob Tanne oder Fichte gemeint ist; drei Ortsnamen (Tanna, Lerchenhügel, Birk) trägt Brückner zusätzlich als Holznamen an.",
           "Brückner uses “Rothtanne” and “Fichte” as synonyms. For names such as Tanna or Tännig it remains open whether fir or spruce is meant; Brückner also notes three place names (Tanna, Lerchenhügel, Birk) as wood names."),
        bi("Brückners Berichtigungen zu S. 78–79 (S. 830) betreffen Einzelbäume und Pflanzenlisten, die hier nicht ausgewertet sind: Die auf S. 78 genannte »stolze Einzelfichte« auf der ernseer Höhe hat am 7. Dezember 1868 der Sturm gebrochen.",
           "Brückner's corrections to pp. 78–79 (p. 830) concern single trees and plant lists that are not analysed here: the “proud solitary spruce” on the Ernsee height named on p. 78 was broken by a storm on 7 December 1868."),
    ],
    "datasets": [
        {"name": "field_names",
         "title": bi("Flurnamen mit Baumnamen im Oberland (S. 78)", "Oberland field names with tree names (p. 78)"),
         "columns": [
             col("tree_de", "Baum", "Tree", "string", None, True, "redaktionelle Zuordnung nach dem Wortstamm"),
             col("tree_en", "Baum (EN)", "Tree (EN)", "string", None, True),
             col("names", "Flurnamen", "Field names", "integer", "Namen", True),
             col("examples", "Namen im Druck", "Names as printed", "string", None),
         ],
         "rows": fl_tab, "source_refs": REFS_FL},
        {"name": "tree_roles",
         "title": bi("Rolle der Baumarten im Wald nach Brückner (S. 77–78)", "Role of tree species in the forest according to Brückner (pp. 77–78)"),
         "columns": [
             col("tree_de", "Baum", "Tree", "string", None, True),
             col("tree_en", "Baum (EN)", "Tree (EN)", "string", None, True),
             col("region_de", "Landesteil", "Part of the territory", "string", None, True),
             col("region_en", "Landesteil (EN)", "Part (EN)", "string", None, True),
             col("level", "Stufe", "Level", "integer", None, True, "redaktionelle Kodierung 1–3"),
             col("tree_order", "Reihenfolge", "Order", "integer", None, True),
             col("level_de", "Stufe (Text)", "Level (text)", "string", None, True),
             col("level_en", "Stufe (EN)", "Level (EN)", "string", None, True),
             col("quote_de", "Wortlaut bei Brückner", "Brückner's wording", "string", None),
             col("quote_en", "Wortlaut (Übersetzung)", "Wording (translation)", "string", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": role_rows, "source_refs": REFS_ROLE},
    ],
    "charts": [
        {"id": "c1", "dataset": "field_names",
         "title": bi("Baumnamen in oberländischen Flurnamen", "Tree names in Oberland field names"),
         "caption": bi(f"Zahl der Flurnamen mit dem jeweiligen Baumnamen ({n_fl} von {len(names)} aufgezählten Flurnamen). Nach Brückner zeigen sie einen früher größeren Reichtum an Baumarten in Beständen an.",
                       f"Number of field names containing the respective tree name ({n_fl} of {len(names)} listed field names). According to Brückner they point to a formerly greater wealth of tree species in stands."),
         "vegalite": {"height": 300, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "tree_de", "en": "tree_en"}, "type": "nominal", "sort": "-x", "title": None},
                          "x": {"field": "names", "type": "quantitative", "title": bi("Flurnamen", "Field names"), "axis": {"tickMinStep": 1}},
                          "tooltip": [{"field": {"de": "tree_de", "en": "tree_en"}, "title": bi("Baum", "Tree")},
                                      {"field": "names", "title": bi("Flurnamen", "Field names")},
                                      {"field": "examples", "title": bi("Namen", "Names")}]}}},
        {"id": "c2", "dataset": "tree_roles",
         "title": bi("Rolle der Baumarten im heutigen Wald: Unterland und Oberland", "Role of tree species in today's forest: Unterland and Oberland"),
         "caption": bi("Dreistufige redaktionelle Einordnung nach Brückners Beschreibung (S. 77–78; »zerstreut, örtlich« umfasst kleine Bestände, einzelne Bäume und örtliches Vorkommen). Fehlende Punkte: nicht genannt. Zusammengefasste Zeilen (z. B. »Ulme, Ahorn, Esche«) geben eine gemeinsame Aussage Brückners wieder.",
                       "Three-level editorial classification following Brückner's description (pp. 77–78; “scattered, local” covers small stands, single trees and local occurrence). Missing dots: not mentioned. Combined rows (e.g. “Ulme, Ahorn, Esche”) reflect a joint statement by Brückner."),
         "vegalite": {"height": 380,
                      "mark": {"type": "circle", "opacity": 0.9},
                      "encoding": {
                          "y": {"field": {"de": "tree_de", "en": "tree_en"}, "type": "nominal", "sort": {"field": "tree_order", "op": "min"}, "title": None},
                          "x": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal", "title": None, "axis": {"labelAngle": 0, "orient": "top", "grid": True},
                                "sort": [{"de": "Unterland", "en": "Unterland"}, {"de": "Oberland", "en": "Oberland"}]},
                          "size": {"field": {"de": "level_de", "en": "level_en"}, "type": "ordinal", "title": bi("Rolle im Wald", "Role in the forest"),
                                   "scale": {"domain": [{"de": LV[3][0], "en": LV[3][1]}, {"de": LV[2][0], "en": LV[2][1]}, {"de": LV[1][0], "en": LV[1][1]}], "range": [700, 320, 90]}},
                          "tooltip": [{"field": {"de": "tree_de", "en": "tree_en"}, "title": bi("Baum", "Tree")},
                                      {"field": {"de": "region_de", "en": "region_en"}, "title": bi("Landesteil", "Part")},
                                      {"field": {"de": "level_de", "en": "level_en"}, "title": bi("Stufe", "Level")},
                                      {"field": {"de": "quote_de", "en": "quote_en"}, "title": bi("Brückner", "Brückner")}]}}},
    ],
    "keywords": {"de": ["Wald", "Fichte", "Eiche", "Buche", "Flurnamen", "Baumarten", "Forstwirtschaft", "Unterland", "Oberland", "Frankenwald"],
                 "en": ["forest", "spruce", "oak", "beech", "field names", "tree species", "forestry", "Unterland", "Oberland", "Frankenwald"]},
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
