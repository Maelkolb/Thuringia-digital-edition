"""Analysis: sorbische Wurzeln der Ortsnamen (p. 121 table, with p. 119-122 text)."""
import re
from collections import OrderedDict
from _common import *

g = block("121", "b1")["grid"]
assert g[0][:3] == ["Slav. Wurzel.", "Bedeutung.", "Localnamen."]

# analyst's grouping of Brückner's meanings (meaning as printed -> group)
GROUPS = OrderedDict([
    ("form", bi("Bodenform: Berg, Sattel, Tiefe", "Landform: mountain, saddle, depression")),
    ("flach", bi("Flach, glatt, eben", "Flat, smooth, level")),
    ("wald", bi("Wald und Rodung", "Forest and clearing")),
    ("wasser", bi("Wasser: Quelle, Fluss, Wildwasser", "Water: spring, river, torrent")),
    ("boden", bi("Boden: feucht, sumpfig, lehmig, steinig", "Soil: damp, marshy, loamy, stony")),
    ("pflanze", bi("Pflanzen", "Plants")),
    ("tier", bi("Tiere", "Animals")),
    ("kirche", bi("Kirche", "Church")),
])
MEANING = {
    "Berg": "form", "Sattel": "form", "Tiefe": "form",
    "flach, glatt, eben": "flach",
    "waldig": "wald", "reuten": "wald",
    "Quelle, Spring": "wasser", "Quelle": "wasser", "am Flusse": "wasser", "Wildwasser": "wasser",
    "feuchter Boden": "boden", "Sumpf": "boden", "Lehm": "boden", "steinig": "boden", "Steinbach": "boden",
    "Weissbuche": "pflanze", "Pappel": "pflanze", "Busch": "pflanze", "Erle": "pflanze",
    "Katze": "tier", "Kirche": "kirche",
}
MEANING_EN = {
    "Berg": "mountain", "Sattel": "saddle", "Tiefe": "depression", "flach, glatt, eben": "flat, smooth, level",
    "waldig": "wooded", "reuten": "to clear (Reuten)", "Quelle, Spring": "spring", "Quelle": "spring",
    "am Flusse": "at the river", "Wildwasser": "torrent", "feuchter Boden": "damp soil", "Sumpf": "swamp",
    "Lehm": "loam", "steinig": "stony", "Steinbach": "stone brook", "Weissbuche": "hornbeam", "Pappel": "poplar",
    "Busch": "bush", "Erle": "alder", "Katze": "cat", "Kirche": "church",
}

KIND_L = bi("Landschaftsmerkmal", "Landscape feature")
KIND_O = bi("Pflanze, Tier, Kirche", "Plant, animal, church")
rows = []
for i, r in enumerate(g[1:], start=1):
    root, meaning, names = r
    meaning = meaning.strip()
    names = names.strip().rstrip(".")
    names = re.sub(r"\s*\*\)", "", names)
    for n in [x.strip() for x in names.split(",")]:
        rows.append([i, root.strip(), meaning, MEANING_EN[meaning], GROUPS[MEANING[meaning]]["de"], GROUPS[MEANING[meaning]]["en"], n])
print(len(g) - 1, "root rows;", len(rows), "name entries;", len({r[6] for r in rows}), "distinct names")
assert {r[2] for r in rows} == set(MEANING), set(MEANING) ^ {r[2] for r in rows}

# group summary (distinct names; roots)
gs = []
for k, lab in GROUPS.items():
    rr = [r for r in rows if r[4] == lab["de"]]
    names = list(OrderedDict.fromkeys(r[6] for r in rr))
    roots = list(OrderedDict.fromkeys(r[1] for r in rr))
    land_k = k in ("form", "flach", "wald", "wasser", "boden")
    gs.append([k, lab["de"], lab["en"], len(names), len(roots), ", ".join(names), KIND_L["de"] if land_k else KIND_O["de"], KIND_L["en"] if land_k else KIND_O["en"]])
gs_sorted = sorted(gs, key=lambda x: -x[3])
for x in gs_sorted:
    print(x[1], x[3], x[4])
n_all = len({r[6] for r in rows})
land = sum(x[3] for x in gs if x[0] in ("form", "flach", "wald", "wasser", "boden"))
print("landscape", land, "of", n_all)
share_land = round(100 * land / n_all)
gora = [r[6] for r in rows if r[1].startswith("gora")]
print(gora)
dup = [n for n in {r[6] for r in rows} if sum(1 for r in rows if r[6] == n) > 1]
print("duplicates", dup)
wald_roots = [x for x in gs if x[0] == "wald"][0]
flach_roots = len({r[1] for r in rows if r[2].startswith("flach")})
print(wald_roots, flach_roots)
assert "40 auf dorf" in text("121", "b3") and "Hälfte" in text("119", "b3")

ana = {
    "id": "ortsnamen-sorbische-wurzeln",
    "title": bi("Sorbische Wurzeln der Ortsnamen nach Bedeutung", "Sorbian roots of place names by meaning"),
    "category": "places",
    "section": "t1-2-2",
    "sources": [{"page": "121", "block": "b1", "rows": "r1-r30"}, {"page": "121", "block": "b2"}, {"page": "119", "block": "b3"}, {"page": "120", "block": "b2"}],
    "summary": bi(
        f"Brückner gibt »nur in historischer Hinsicht« eine Übersicht der versuchten Erklärungen sorbischer Ortsnamen (S. 121): {len(g) - 1} slawische Wurzeln mit ihrer Bedeutung und den davon abgeleiteten Orten. Gruppiert nach der Bedeutung der Wurzel zeigt sich, dass die Namen fast ausschließlich Bodenformen, Wald, Wasser und Boden beschreiben: {land} von {n_all} Namen ({share_land} %).",
        f"Brückner gives “only from a historical point of view” a survey of the attempted explanations of Sorbian place names (p. 121): {len(g) - 1} Slavic roots with their meaning and the places derived from them. Grouped by the meaning of the root, the names turn out to describe almost exclusively landform, forest, water and soil: {land} of {n_all} names ({share_land} %).",
    ),
    "method": bi(
        "Die Tabelle (S. 121, b1) wurde Zeile für Zeile übernommen und die Ortsnamen jeder Zeile einzeln erfasst (Fußnotenzeichen entfernt). Die Zuordnung der gedruckten Bedeutungen zu acht Sachgruppen ist eine Entscheidung des Bearbeiters; gezählt werden verschiedene Ortsnamen (Triebes steht unter zwei Wurzeln und zählt einmal). Brückner übernimmt diese Deutungen nicht; er hält eine sichere Etymologie ohne die ältesten urkundlichen Formen für unmöglich (S. 120).",
        "The table (p. 121, b1) was taken over row by row and the place names of each row were recorded individually (footnote marks removed). The assignment of the printed meanings to eight subject groups is the analyst’s decision; distinct place names are counted (Triebes stands under two roots and counts once). Brückner does not adopt these interpretations; he holds a secure etymology to be impossible without the oldest documentary forms (p. 120).",
    ),
    "findings": [
        bi(
            f"Die größte Gruppe sind Namen nach der Bodenform ({gs_sorted[0][3]}: darunter sieben zur Wurzel gora/hora »Berg«, u. a. Gera, Görkwitz, Göritz, Harra), gefolgt von »Wald und Rodung« ({[x for x in gs if x[0]=='wald'][0][3]}, vier Wurzeln für »waldig«) und »flach, glatt, eben« ({[x for x in gs if x[0]=='flach'][0][3]}).",
            f"The largest group is names after landform ({gs_sorted[0][3]}: among them seven from the root gora/hora “mountain”, including Gera, Görkwitz, Göritz, Harra), followed by “forest and clearing” ({[x for x in gs if x[0]=='wald'][0][3]}, four roots for “wooded”) and “flat, smooth, level” ({[x for x in gs if x[0]=='flach'][0][3]}).",
        ),
        bi(
            f"Landschaftsmerkmale (Bodenform, flach, Wald, Wasser, Boden) machen {land} von {n_all} Namen aus ({share_land} %); Pflanzen ({[x for x in gs if x[0]=='pflanze'][0][3]}), ein Tier (Kattenstein) und die Kirche (Köstritz) bleiben die Ausnahme. Das entspricht Brückners Aussage, die Namen gingen auf »Eindrücke physischer Formen und Eigenschaften« zurück.",
            f"Landscape features (landform, flat, forest, water, soil) make up {land} of {n_all} names ({share_land} %); plants ({[x for x in gs if x[0]=='pflanze'][0][3]}), one animal (Kattenstein) and the church (Köstritz) remain the exception. This agrees with Brückner’s statement that the names go back to “impressions of physical forms and properties”.",
        ),
        bi(
            "Der Ortsname Gera erscheint unter der Wurzel gora/hora (»Berg«); Köstritz wird von kostriza (»Kirche«) abgeleitet, Hohenleuben von leube (»Busch«). Brückner nennt außerdem die Namen Schleiz (Slowitz), Schwarm, Sormitz, Sormbach und Böhmsdorf als mögliche Völkernamen.",
            "The place name Gera appears under the root gora/hora (“mountain”); Köstritz is derived from kostriza (“church”), Hohenleuben from leube (“bush”). Brückner also names Schleiz (Slowitz), Schwarm, Sormitz, Sormbach and Böhmsdorf as possible ethnic names.",
        ),
    ],
    "caveats": [
        bi(
            "Die Deutungen sind zeitgenössische Versuche, die Brückner ausdrücklich nur referiert; vieles ist nach heutiger Kenntnis unsicher oder falsch (Volksetymologie). Auch der Jenaer Slawist Schleicher, den Brückner zitiert, warnt vor sicheren Deutungen und rechnet die Slawen des Landes zum polabischen Stamm (S. 120).",
            "The interpretations are contemporary attempts which Brückner expressly only reports; much of it is uncertain or wrong by present knowledge (folk etymology). The Jena Slavist Schleicher whom Brückner quotes also warns against confident interpretations and counts the Slavs of the country as Polabian (p. 120).",
        ),
        bi(
            "Die Tabelle ist eine Auswahl: Nach S. 119 hat etwa die Hälfte der Ortsnamen sorbischen Laut (und ein Sechzigstel der Flurnamen); hier erscheinen nur die Namen, für die Brückner eine Wurzel nennt. Die Gruppenbildung vereinfacht (z. B. »Steinbach« unter Boden).",
            "The table is a selection: according to p. 119 about half of the place names have a Sorbian sound (and one sixtieth of the field names); only the names for which Brückner gives a root appear here. The grouping simplifies (e.g. “Steinbach” under soil).",
        ),
    ],
    "datasets": [
        {
            "name": "names",
            "title": bi("Slawische Wurzeln, Bedeutung und Ortsnamen (S. 121)", "Slavic roots, meaning and place names (p. 121)"),
            "columns": [
                {"name": "row", "label": bi("Zeile der Tabelle", "Table row"), "type": "integer", "unit": None, "derived": True},
                {"name": "root", "label": bi("Slawische Wurzel", "Slavic root"), "type": "string", "unit": None},
                {"name": "meaning_de", "label": bi("Bedeutung (de)", "Meaning (de)"), "type": "string", "unit": None},
                {"name": "meaning_en", "label": bi("Bedeutung (en)", "Meaning (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "group_de", "label": bi("Sachgruppe (de)", "Subject group (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "group_en", "label": bi("Sachgruppe (en)", "Subject group (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "name", "label": bi("Ortsname", "Place name"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": [{"page": "121", "block": "b1", "rows": "r2-r30"}],
        },
        {
            "name": "groups",
            "title": bi("Sachgruppen: Zahl der Namen und Wurzeln", "Subject groups: number of names and roots"),
            "columns": [
                {"name": "key", "label": bi("Schlüssel", "Key"), "type": "string", "unit": None, "derived": True},
                {"name": "group_de", "label": bi("Sachgruppe (de)", "Subject group (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "group_en", "label": bi("Sachgruppe (en)", "Subject group (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "names", "label": bi("Verschiedene Ortsnamen", "Distinct place names"), "type": "integer", "unit": "Namen", "derived": True},
                {"name": "roots", "label": bi("Verschiedene Wurzeln", "Distinct roots"), "type": "integer", "unit": "Wurzeln", "derived": True},
                {"name": "list", "label": bi("Ortsnamen", "Place names"), "type": "string", "unit": None, "derived": True},
                {"name": "kind_de", "label": bi("Art (de)", "Kind (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "kind_en", "label": bi("Art (en)", "Kind (en)"), "type": "string", "unit": None, "derived": True},
            ],
            "rows": gs,
            "source_refs": [{"page": "121", "block": "b1", "rows": "r2-r30"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "groups",
            "title": bi("Was die sorbischen Ortsnamen benennen", "What the Sorbian place names denote"),
            "caption": bi(
                f"Zahl der Ortsnamen je Bedeutungsgruppe der Wurzel (nach Brückners Tabelle S. 121; Gruppenbildung durch den Bearbeiter). {share_land} % der Namen bezeichnen Landschaftsmerkmale (Bodenform, Wald, flach, Boden, Wasser).",
                f"Number of place names per meaning group of the root (after Brückner’s table, p. 121; grouping by the analyst). {share_land} % of the names denote landscape features (landform, forest, flat, soil, water).",
            ),
            "vegalite": {
                "height": 300,
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": {"field": "names", "order": "descending"}, "title": None, "axis": {"labelLimit": 420}},
                    "x": {"field": "names", "type": "quantitative", "title": bi("Ortsnamen", "Place names"), "axis": {"tickMinStep": 1}},
                    "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": None, "scale": {"domain": [KIND_L, KIND_O]}, "legend": {"labelLimit": 400, "columns": 1}},
                    "tooltip": [
                        {"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                        {"field": "names", "title": bi("Ortsnamen", "Place names")},
                        {"field": "roots", "title": bi("Wurzeln", "Roots")},
                        {"field": "list", "title": bi("Namen", "Names")},
                    ],
                },
            },
        }
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Ortsnamen", "Sorben", "Slawen", "Etymologie", "Namensdeutung", "Berg", "Wald", "Wasser", "Gera", "Köstritz"],
        "en": ["place names", "Sorbs", "Slavs", "etymology", "name interpretation", "mountain", "forest", "water", "Gera", "Köstritz"],
    },
    "related": ["fauna-tiernamen-in-flurnamen", "wald-baumarten-flurnamen"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
