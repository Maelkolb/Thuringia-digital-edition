"""Analysis: Motive der Ortssiegel (pp. 124-125)."""
import re
from collections import Counter, OrderedDict
from _common import *

t124 = text("124", "b3")
t125 = text("125", "b1")
ALL = t124 + " " + t125

CLASSES = OrderedDict([
    ("baum", bi("Ein Baum", "One tree")),
    ("baeume", bi("Mehrere Bäume", "Several trees")),
    ("baumtier", bi("Baum und Tier", "Tree and animal")),
    ("tier", bi("Tier", "Animal")),
    ("landw", bi("Landwirtschaftliche Bilder", "Agricultural images")),
    ("kirche", bi("Kirche (auch mit Baum)", "Church (also with tree)")),
    ("bau", bi("Schloss, Brücke, Brunnen, Figur u. a.", "Castle, bridge, well, figure and others")),
    ("neu", bi("Kranz, Anker, Sonne (neuere Erfindung)", "Wreath, anchor, sun (recent invention)")),
])
OLD = bi("nach Brückner alt", "old, according to Brückner")
NEW = bi("nach Brückner neuere Erfindung", "recent invention, according to Brückner")

rows = []


def add(cls, place, motif_de, motif_en, page, block):
    assert place in ALL, place
    rows.append([cls, CLASSES[cls]["de"], CLASSES[cls]["en"], (NEW if cls == "neu" else OLD)["de"], (NEW if cls == "neu" else OLD)["en"], place, motif_de, motif_en, page, block])


def split_names(s):
    return [x.strip() for x in re.split(r",| und ", s) if x.strip()]


# 22 villages with a single tree
m = re.search(r"22 Dörfer \((.*?)\) haben in ihrem Siegel nur einen Baum", t124)
names = split_names(m.group(1))
assert len(names) == 22, len(names)
SPECIES = {"Lerchenhügel": ("Lärche", "larch"), "Dürrenebersdorf": ("Fichte", "spruce"), "Ernsee": ("Palmbaum", "palm tree"), "Helmsgrün": ("Palmbaum", "palm tree"), "Hartmannsdorf": ("Buche", "beech"), "Reichenbach": ("Eiche", "oak"), "Wernsdorf": ("Eiche", "oak"), "Pirk": ("Birke", "birch")}
for n in names:
    de, en = SPECIES.get(n, ("Baum (meist Linde)", "tree (mostly lime)"))
    add("baum", n, de, en, "124", "b3")
# 6 villages with two to four trees
for n, de, en in [("Gleina", "zwei Linden mit Brunnen dazwischen", "two limes with a well between"), ("Oberröppisch", "drei Linden", "three limes"), ("Kulm", "zwei Bäume", "two trees"), ("Hirschfeld", "drei Bäume", "three trees"), ("Waaswitz", "drei Bäume", "three trees"), ("Großaga", "vier Pappeln", "four poplars")]:
    add("baeume", n, de, en, "124", "b3")
# trees with animals
for n, de, en in [("Hirschbach", "Fichte und Hirsch", "spruce and stag"), ("Gahma", "drei Fichten mit Hirsch", "three spruces with stag"), ("Rüdersdorf", "drei Fichten mit Hirsch", "three spruces with stag"), ("Frössen", "giebelloser Baum und Reiher", "gableless tree and heron")]:
    add("baumtier", n, de, en, "124", "b3")
# animals
for n, de, en in [("Langenberg", "Kranich", "crane"), ("Frankenthal", "aufgerichteter Löwe", "rampant lion"), ("Langengrobsdorf", "aufgerichteter Löwe", "rampant lion"), ("Pöritzsch", "aufgerichteter Löwe", "rampant lion"), ("Söllmnitz", "aufgerichteter Löwe", "rampant lion"), ("Köstritz", "Löwe mit Schwert und Schild (zwei verschlungene Hände)", "lion with sword and shield (two clasped hands)"), ("Stublach", "Löwe mit drei Zweigen", "lion with three twigs"), ("Langenwolschendorf", "Löwe und Baum", "lion and tree"), ("Göschitz", "Bienenkorb und Baumstamm", "beehive and tree trunk")]:
    add("tier", n, de, en, "124", "b3")
assert len([r for r in rows if r[0] == "tier"]) == 9 and "Neun Ortssiegel führen Thiere" in t124
# agricultural
m = re.search(r"In sieben Ortssiegeln \((.*?)\) finden sich landwirthschaftliche", t124)
names = split_names(m.group(1))
assert len(names) == 7
for n in names:
    add("landw", n, "Rechen, Sense, Dreschflegel, Garbe oder Pflug", "rake, scythe, flail, sheaf or plough", "124", "b3")
# churches
for n in ["Dittersdorf", "Oschitz", "Thieschitz", "Zollgrün", "Zschippach"]:
    add("kirche", n, "Kirche ohne Beigabe", "church without additions", "125", "b1")
add("kirche", "Oberböhmsdorf", "Kirche mit Baumgruppe", "church with group of trees", "125", "b1")
add("kirche", "Stelzen", "Kirche mit dem Stelzenbaum", "church with the Stelzenbaum", "125", "b1")
# buildings and others
for n, de, en in [("Hohenleuben", "Schloss mit Park", "castle with park"), ("Harpersdorf", "Landhaus mit Forellenbach, Garten, Feld und Fichte", "country house with trout stream, garden, field and spruce"), ("Collis", "Brücke", "bridge"), ("Weckersdorf", "Brücke", "bridge"), ("Töppeln", "Pumpbrunnen", "pump well"), ("Kaltenborn", "Pumpbrunnen mit Pumperin", "pump well with pump woman"), ("Burkersdorf", "Pyramide zwischen zwei Palmen", "pyramid between two palms"), ("Dettersdorf", "tanzender Jüngling", "dancing youth")]:
    add("bau", n, de, en, "125", "b1")
# recent inventions (p. 124 b3)
for n, de, en in [("Steinbrücken", "Blumenkranz", "flower wreath"), ("Pforten", "Zweigkranz", "wreath of twigs"), ("Schöna", "Zweigkranz", "wreath of twigs"), ("Pohlitz", "Halbkranz aus Zweigen", "half wreath of twigs"), ("Seifarthsdorf", "Halbkranz aus Zweigen", "half wreath of twigs"), ("Tinz", "Halbkranz aus Zweigen", "half wreath of twigs"), ("Ebersdorf", "Anker mit Weinstock (Brüdergemeinde)", "anchor with vine (Moravian congregation)"), ("Rusitz", "Sonne", "sun")]:
    # the place name Ebersdorf occurs in 'Brüdergemeinde zu Ebersdorf'
    add("neu", n, de, en, "124", "b3")
print(len(rows), "village seals")
cnt = Counter(r[0] for r in rows)
print(cnt)
dup = [n for n, c in Counter(r[5] for r in rows).items() if c > 1]
print("dup", dup)

rows_c = []
for k, lab in CLASSES.items():
    rows_c.append([lab["de"], lab["en"], (NEW if k == "neu" else OLD)["de"], (NEW if k == "neu" else OLD)["en"], cnt[k]])
n_total = len(rows)
tree_n = cnt["baum"] + cnt["baeume"] + cnt["baumtier"]
animal_n = cnt["tier"] + cnt["baumtier"]
print(tree_n, animal_n)
assert "größere Hälfte der Orte Schriftsiegel" in t124
assert "22 Dörfer" in t124 and "sechs Orten" in t124 and "vier Ortssiegeln" in t124

ana = {
    "id": "kultur-ortssiegel-motive",
    "title": bi("Motive der Ortssiegel", "Motifs of the village seals"),
    "category": "culture",
    "section": "t1-2-2",
    "sources": [{"page": "124", "block": "b3"}, {"page": "125", "block": "b1"}],
    "summary": bi(
        f"Brückner beschreibt die Siegel der Landgemeinden: Die größere Hälfte der Orte führt nur ein Schriftsiegel, die kleinere ein Bildersiegel. Er nennt {n_total} Dörfer mit Siegelbild und ordnet sie nach Motiven; die Zählung zeigt, dass Bäume (vor allem die Linde) das Bild beherrschen, gefolgt von Tieren, Landwirtschaft, Kirchen und Bauwerken.",
        f"Brückner describes the seals of the rural communes: the larger half of the places has only a lettered seal, the smaller half a pictorial seal. He names {n_total} villages with a seal picture and arranges them by motif; the count shows that trees (above all the lime) dominate the picture, followed by animals, agriculture, churches and buildings.",
    ),
    "method": bi(
        "Die Namen der Orte und die Motive wurden aus den Aufzählungen S. 124 f. übernommen (die 22 Orte mit einem Baum und die sieben mit landwirtschaftlichen Bildern per Skript aus dem Text gelesen, die übrigen aus den Sätzen zusammengestellt; jeder Name wurde im Text geprüft). Die Einteilung in acht Motivklassen ist die des Bearbeiters. Die sechs Stadtwappen (Gera: Löwe, Schleiz: Auerstierkopf, Lobenstein: Bracke, Tanna: Tanne, Saalburg: Rathaus und Löwe, Hirschberg: Hirsch und Halbadler) sind nicht mitgezählt.",
        "The place names and motifs were taken from the enumerations on pp. 124 f. (the 22 places with one tree and the seven with agricultural pictures were read from the text by script, the others compiled from the sentences; every name was checked against the text). The division into eight motif classes is the analyst’s. The six town arms (Gera: lion, Schleiz: aurochs head, Lobenstein: hound’s head, Tanna: fir, Saalburg: town hall and lion, Hirschberg: stag and half-eagle) are not counted.",
    ),
    "findings": [
        bi(
            f"Von {n_total} Dörfern mit Siegelbild führen {tree_n} einen oder mehrere Bäume im Siegel ({cnt['baum']} einen Baum, {cnt['baeume']} mehrere, {cnt['baumtier']} Baum und Tier); die Linde ist nach Brückner der häufigste Baum.",
            f"Of {n_total} villages with a seal picture, {tree_n} bear one or more trees in the seal ({cnt['baum']} one tree, {cnt['baeume']} several, {cnt['baumtier']} tree and animal); the lime is according to Brückner the commonest tree.",
        ),
        bi(
            f"Tiere erscheinen in {animal_n} Siegeln, darunter der Löwe in sieben (Frankenthal, Langengrobsdorf, Pöritzsch, Söllmnitz, Köstritz, Stublach, Langenwolschendorf); {cnt['landw']} Siegel zeigen landwirtschaftliche Geräte, {cnt['kirche']} eine Kirche.",
            f"Animals appear in {animal_n} seals, among them the lion in seven (Frankenthal, Langengrobsdorf, Pöritzsch, Söllmnitz, Köstritz, Stublach, Langenwolschendorf); {cnt['landw']} seals show agricultural implements, {cnt['kirche']} a church.",
        ),
        bi(
            f"{cnt['neu']} Siegelbilder (Kränze und Halbkränze, Anker, Sonne) nennt Brückner neuere Erfindungen »ohne allen historischen Werth«; alle übrigen stammen nach ihm aus früherer Zeit.",
            f"{cnt['neu']} seal pictures (wreaths and half wreaths, anchor, sun) Brückner calls recent inventions “without any historical value”; all the others date, according to him, from earlier times.",
        ),
    ],
    "caveats": [
        bi(
            "Die Liste ist Brückners Auswahl und nennt keine Zahl der Orte ohne Bild; die Angabe »größere Hälfte Schriftsiegel« ist nicht beziffert. Die Zuordnung zu Motivklassen vereinfacht (z. B. Langenwolschendorf: Löwe und Baum unter »Tier«, Göschitz: Bienenkorb und Baumstamm unter »Tier«).",
            "The list is Brückner’s selection and gives no number of places without a picture; the statement “larger half lettered seals” is not quantified. The assignment to motif classes simplifies (e.g. Langenwolschendorf: lion and tree under “animal”, Göschitz: beehive and tree trunk under “animal”).",
        ),
    ],
    "datasets": [
        {
            "name": "seals",
            "title": bi("Orte mit Siegelbild und Motiv", "Places with a seal picture and motif"),
            "columns": [
                {"name": "class_key", "label": bi("Motivklasse (Schlüssel)", "Motif class (key)"), "type": "string", "unit": None, "derived": True},
                {"name": "class_de", "label": bi("Motivklasse (de)", "Motif class (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "class_en", "label": bi("Motivklasse (en)", "Motif class (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "age_de", "label": bi("Alter laut Brückner (de)", "Age according to Brückner (de)"), "type": "string", "unit": None},
                {"name": "age_en", "label": bi("Alter laut Brückner (en)", "Age according to Brückner (en)"), "type": "string", "unit": None},
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "motif_de", "label": bi("Motiv (de)", "Motif (de)"), "type": "string", "unit": None},
                {"name": "motif_en", "label": bi("Motiv (en)", "Motif (en)"), "type": "string", "unit": None},
                {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": [{"page": "124", "block": "b3"}, {"page": "125", "block": "b1"}],
        },
        {
            "name": "classes",
            "title": bi("Zahl der Orte je Motivklasse", "Number of places per motif class"),
            "columns": [
                {"name": "class_de", "label": bi("Motivklasse (de)", "Motif class (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "class_en", "label": bi("Motivklasse (en)", "Motif class (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "age_de", "label": bi("Alter laut Brückner (de)", "Age according to Brückner (de)"), "type": "string", "unit": None},
                {"name": "age_en", "label": bi("Alter laut Brückner (en)", "Age according to Brückner (en)"), "type": "string", "unit": None},
                {"name": "places", "label": bi("Orte", "Places"), "type": "integer", "unit": "Orte", "derived": True},
            ],
            "rows": rows_c,
            "source_refs": [{"page": "124", "block": "b3"}, {"page": "125", "block": "b1"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "classes",
            "title": bi("Siegelmotive der Dörfer", "Seal motifs of the villages"),
            "caption": bi(
                "Zahl der von Brückner genannten Dörfer je Motivklasse. Bäume stehen in 32 der 71 Siegel; die jüngeren Bilder (Kränze, Anker, Sonne) nennt Brückner ohne historischen Wert.",
                "Number of the villages named by Brückner per motif class. Trees appear in 32 of the 71 seals; the younger pictures (wreaths, anchor, sun) Brückner calls without historical value.",
            ),
            "vegalite": {
                "height": 300,
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "class_de", "en": "class_en"}, "type": "nominal", "sort": {"field": "places", "order": "descending"}, "title": None, "axis": {"labelLimit": 420}},
                    "x": {"field": "places", "type": "quantitative", "title": bi("Dörfer", "Villages"), "axis": {"tickMinStep": 1}},
                    "color": {"field": {"de": "age_de", "en": "age_en"}, "type": "nominal", "title": None, "scale": {"domain": [OLD, NEW]}, "legend": {"labelLimit": 400, "columns": 1}},
                    "tooltip": [
                        {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Motivklasse", "Motif class")},
                        {"field": "places", "title": bi("Dörfer", "Villages")},
                    ],
                },
            },
        }
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Ortssiegel", "Wappen", "Siegel", "Linde", "Löwe", "Dorfwappen", "Gemeindesiegel", "Heraldik"],
        "en": ["village seals", "coats of arms", "seals", "lime tree", "lion", "village arms", "heraldry"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
# check caption numbers against the count
assert tree_n == 32 and n_total == 71, (tree_n, n_total)
write(ana)
