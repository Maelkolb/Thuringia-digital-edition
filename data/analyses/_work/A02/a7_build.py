"""Analysis geologie-formationen-rohstoffe: which usable rocks and ores each formation holds (pp. 26-41).

Editorial coding of Liebe's statements: one row per (formation, resource) with a verbatim quotation as evidence;
every quotation is asserted against the cited block."""
import re
from collections import Counter, defaultdict
from common import *

M = lambda de_, en_: {"de": de_, "en": en_}

FORM = {  # no: (order, region, German, English)
    1: ("Oberland", "Kambrium", "Cambrian"),
    2: ("Oberland", "Unteres Silur", "Lower Silurian"),
    3: ("Oberland", "Mittleres Silur", "Middle Silurian"),
    4: ("Oberland", "Oberes Silur (Tentaculiten)", "Upper Silurian (tentaculites)"),
    5: ("Oberland", "Phyllodocitesschiefer", "Phyllodocite slate"),
    6: ("Oberland", "Devonische Tuffe", "Devonian tuffs"),
    7: ("Oberland", "Cypridinenschiefer, Clymenienkalk", "Cypridina slate, Clymenia limestone"),
    8: ("Oberland", "Kulm", "Culm"),
    9: ("Unterland", "Rothliegendes", "Rotliegend"),
    10: ("Unterland", "Zechstein", "Zechstein"),
    11: ("Unterland", "Buntsandstein", "Bunter sandstone"),
    12: ("Unterland", "Tertiär", "Tertiary"),
    13: ("Unterland", "Eiszeit, Alluvium", "Ice age, alluvium"),
}
RES = {  # code: (order, German, English)
    "iron": (1, "Eisenerz", "Iron ore"),
    "antimony": (2, "Antimonerz", "Antimony ore"),
    "nonferrous": (3, "Kupfer-/Nickelerz", "Copper/nickel ore"),
    "alum": (4, "Alaunschiefer", "Alum shale"),
    "slate": (5, "Dachschiefer", "Roofing slate"),
    "limestone": (6, "Kalkstein", "Limestone"),
    "building": (7, "Bausteine, Bausand", "Building stone, sand"),
    "road": (8, "Straßenmaterial", "Road metal"),
    "gypsum": (9, "Gips, Salz", "Gypsum, salt"),
    "coal": (10, "Kohle", "Coal"),
}
# (formation, resource, status, evidence quotation, page, block, locality note)
E = [
    (1, "iron", "worked", "Weit wichtiger sind die Gänge von Spatheisenstein", "27", "b2", "Rücken zwischen Dobareuther und Ullersreuther Thal (Grube »Arme Hilfe«), Tännig bei Lobenstein, Pottiga"),
    (1, "building", "worked", "als Ersatzmittel für Sand beim Bauen benutzt", "26", "b4", "Granit bei Helmsgrün, zu Grieß verwittert"),
    (2, "slate", "worked", "stehen die Dachschieferbrüche von Ullersreuth, Blintendorf, Helmsgrün, Heinersdorf", "28", "b1", "Ullersreuth, Blintendorf, Helmsgrün, Heinersdorf"),
    (2, "iron", "occurs", "Gänge von Eisenspath und von aus ihm entstandenem Brauneisenstein in guter Anzahl anstehen", "28", "b3", "Eisenspatgänge, Brauneisenstein"),
    (3, "alum", "formerly", "früher als Alaunschiefer zur Bereitung von Alaun und Eisenvitriol abgebaut", "28", "b5", "Gräfenwarth, Gottliebsthal"),
    (3, "road", "worked", "Die wichtigste Verwendung des Kieselschiefers ist aber die zur Beschotterung der Straßen", "28", "b5", "Kieselschiefer auf einer Packlage von Grünstein: die Chausseen des Oberlandes"),
    (3, "antimony", "formerly", "Noch bis vor Kurzem wurden die Erze abgebaut", "30", "b3", "Gruben »Heinrichsfreude« und »Halbmondfundgrube«, ältere Baue bei Schleiz und Weckersdorf"),
    (3, "iron", "occurs", "Unbedeutend sind die Eisenerzvorkommnisse innerhalb dieser Formation", "30", "b4", "Brauneisenstein bei Lössau, Rotheisenstein bei Oberböhmsdorf"),
    (4, "limestone", "occurs", "die Verwendbarkeit des Kalkes zum Brennen wegen seiner Unreinheit sehr schlecht", "31", "b1", "Kalklager in der Nähe der Nereitenschichten"),
    (4, "building", "worked", "unter dem Namen Sand zum Bereiten des Mörtels beim Bauen verwendet", "32", "b1", "Grünsteingrieß bei Schleiz (Sandberge), Wüstendittersdorf, Triebes, Weckersdorf"),
    (4, "iron", "occurs", "daß ein Abbau darauf vorgenommen werden könnte", "32", "b2", "Rotheisenerz an den Grünsteinwänden, meist zu geringmächtig"),
    (5, "slate", "worked", "stehen die Dachschieferbrüche von Gebersreuth, am Franzensberg, bei Benignengrün", "32", "b3", "Gebersreuth, Franzensberg, Benignengrün (Wurzbach), Vogelberg"),
    (5, "limestone", "worked", "Der Kalk in den Brüchen auf der Kalch bei Wurzbach gehört wahrscheinlich hierher", "33", "b2", "Franzensberg, Blankenstein, Kalch bei Wurzbach"),
    (6, "iron", "worked", "Gänge mit Spatheisenstein, daraus entstandenem Brauneisenstein und Graunickelkies, welche noch abgebaut werden", "34", "b2", "kleine Friesa bei Lobenstein; Rotheisenstein allenthalben häufig"),
    (6, "nonferrous", "worked", "Graunickelkies, welche noch abgebaut werden", "34", "b2", "Graunickelkies an der kleinen Friesa; Kupferkies und Fahlerz bei Schleiz und Löhma längst auflässig"),
    (7, "limestone", "worked", "Die Kalke lassen sich im Allgemeinen gut brennen", "35", "b1", "Brüche an der Thomasmühle bei Schleiz, Pahren, Kirschkau"),
    (7, "building", "worked", "giebt der Clymenienkalk aber noch gute Bausteine", "35", "b1", "Clymenienkalk, auch poliert für Tischplatten und Grabmäler"),
    (7, "iron", "worked", "eine Menge theils auflässiger, theils noch gangbarer Gruben", "36", "b3", "Strich von Oschitz bis Göschitz; großes Glanzeisenerz-Lager bei Ebersdorf/Schönbrunn"),
    (8, "building", "worked", "Die Grauwackenbänke liefern gute Bausteine", "37", "b1", "Brüche bei Plothen und Dittersdorf"),
    (8, "coal", "occurs", "finden sich in der Grauwacke Nester von Kohlenblende", "36", "b6", "Carolinenfeld, Schleizer Streitwald"),
    (10, "limestone", "worked", "Sie werden gebrannt und zum Pflastern verwendet", "38", "b1", "Kalk- und Mergelzechstein"),
    (10, "building", "worked", "aus einer großen Anzahl von Steinbrüchen Bausteine und Wegebaumaterial", "38", "b1", "Rauchwacke und obere Kalkplatten"),
    (10, "nonferrous", "formerly", "Sehr stark ist die Ausbeute wohl nie gewesen", "38", "b2", "Kupfererze im Weißliegenden bei Trebnitz, bei Gera verhüttet"),
    (10, "gypsum", "worked", "vollkommen gesättigte Salzsohle in hinreichender Menge", "38", "b3", "Gipsstöcke bei Thieschitz, Rubitz, Köstritz; Salzsohle der Saline Heinrichshall"),
    (11, "building", "worked", "liefert dann gute Werkstücke, die weithin verführt werden", "39", "b2", "Brüche von Falke, Kraftsdorf, Harpersdorf, Rüdersdorf"),
    (11, "iron", "formerly", "daß man sonst diese Erze bergmännisch gewonnen hat", "39", "b3", "Ronneburger Höhe, Geiersberg"),
    (12, "coal", "worked", "das seeligenstädter hingegen wird unter Tag noch bergmännisch fortbetrieben", "40", "b2", "Braunkohle bei Seeligenstädt (in Betrieb) und Kleinaga (auflässig)"),
    (12, "road", "worked", "desto wichtiger aber sind sie als Pflastermaterial", "40", "b1", "Süßwassersandstein (»Wacke«); die Pflastersteine für Gera kommen aus der zeitzer Gegend"),
    (13, "road", "worked", "ein sehr mittelmäßiges Straßenmaterial, aber ein gutes Material für Fußwege", "40", "b4", "Eiszeitgerölle bei Ronneburg, Trebnitz, Loitzsch"),
]
rows = []
refs = []
for i, (fno, res, st, quote, pg, bl, note) in enumerate(E, 1):
    t = re.sub(r"\s+", " ", text(pg, bl)).replace("= ", "")
    assert quote in t, (fno, res, quote)
    reg, fde, fen = FORM[fno]
    rows.append([fno, fde, fen, reg, res, RES[res][0], RES[res][1], RES[res][2], st, quote, note, pg, bl])
    if {"page": pg, "block": bl} not in refs:
        refs.append({"page": pg, "block": bl})
refs.sort(key=lambda r: (int(r["page"]), int(r["block"][1:])))
print(len(rows), "rows")

# statistics for the findings
per_res = defaultdict(set)
for r in rows:
    per_res[r[4]].add(r[0])
for k, v in sorted(per_res.items(), key=lambda kv: -len(kv[1])):
    print(k, sorted(v))
per_form = Counter(r[0] for r in rows)
print(per_form)
st = Counter(r[8] for r in rows)
print(st)
iron = sorted(per_res["iron"])
iron_ober = [f for f in iron if FORM[f][0] == "Oberland"]
only_ober = [k for k, v in per_res.items() if all(FORM[f][0] == "Oberland" for f in v)]
only_unter = [k for k, v in per_res.items() if all(FORM[f][0] == "Unterland" for f in v)]
print(only_ober, only_unter)
no_res = [f for f in FORM if f not in per_form]
print("formations without entry:", no_res)
rich = [f for f, n in per_form.items() if n == max(per_form.values())]
print("richest", rich, max(per_form.values()))
assert sorted(rich) == [3, 10] and sorted(only_ober) == ["alum", "antimony", "slate"] and only_unter == ["gypsum"], (rich, only_ober, only_unter)
assert sorted(k for k in per_res if k not in only_ober and k not in only_unter) == sorted(["iron", "nonferrous", "limestone", "building", "road", "coal"])
formerly = [(FORM[r[0]][1], RES[r[4]][1]) for r in rows if r[8] == "formerly"]
worked_ores = sorted({(RES[r[4]][1]) for r in rows if r[8] == "worked" and r[4] in ("iron", "nonferrous", "antimony", "gypsum", "coal")})
print(formerly, worked_ores)
n_form_with = len(per_form)
ober_n = sum(1 for f in per_form if FORM[f][0] == "Oberland")
unter_n = sum(1 for f in per_form if FORM[f][0] == "Unterland")

findings = [
    M(f"Eisenerz ist der am weitesten verbreitete Rohstoff: Liebe nennt es in {len(iron)} der 13 Formationen (Kambrium, Silur, devonische Tuffe und Cypridinenschiefer, Buntsandstein), davon {len(iron_ober)} im Oberland. In keiner anderen Rohstoffgruppe sind es so viele (Kalkstein {len(per_res['limestone'])}, Bausteine/Bausand {len(per_res['building'])}).",
      f"Iron ore is the most widespread resource: Liebe names it in {len(iron)} of the 13 formations (Cambrian, Silurian, Devonian tuffs and Cypridina slate, Bunter sandstone), {len(iron_ober)} of them in the Oberland. No other resource group occurs in as many (limestone {len(per_res['limestone'])}, building stone/sand {len(per_res['building'])})."),
    M("Antimonerz, Alaunschiefer und Dachschiefer kommen nur im Oberland vor, Gips und Salz nur im Unterland; Eisenerz, Kupfer-/Nickelerz, Kalkstein, Bausteine, Straßenmaterial und Kohle treten in beiden Landesteilen auf (Kohle im Oberland nur als »Nester von Kohlenblende«, im Unterland als Braunkohle).",
      "Antimony ore, alum shale and roofing slate occur only in the Oberland, gypsum and salt only in the Unterland; iron ore, copper/nickel ore, limestone, building stone, road metal and coal occur in both parts (coal in the Oberland only as “nests of Kohlenblende”, in the Unterland as lignite)."),
    M(f"Am vielfältigsten sind das mittlere Silur und der Zechstein mit je {max(per_form.values())} nutzbaren Stoffen; für das Rothliegende nennt Liebe keinen Rohstoff. Zu {st['formerly']} der {len(rows)} Einträge heißt es, der Abbau sei früher betrieben worden und liege still (Alaunschiefer, Antimon, Kupfererz des Zechsteins, Eisenerz des Buntsandsteins).",
      f"The Middle Silurian and the Zechstein are the most varied, with {max(per_form.values())} usable materials each; for the Rotliegend Liebe names no resource. For {st['formerly']} of the {len(rows)} entries he says that working took place formerly and has stopped (alum shale, antimony, Zechstein copper ore, iron ore of the Bunter sandstone)."),
    M("Als noch betriebene Bergbaue nennt Liebe Spateisenstein mit Graunickelkies an der kleinen Friesa bei Lobenstein, die Eisengruben zwischen Oschitz und Göschitz, die Braunkohle von Seeligenstädt sowie das Salz von Heinrichshall.",
      "As mines still in operation Liebe names spar iron ore with grey nickel pyrites at the Kleine Friesa near Lobenstein, the iron mines between Oschitz and Göschitz, the lignite of Seeligenstädt and the salt of Heinrichshall."),
]
for f in findings:
    print(f["de"])

COLS = [
    {"name": "formation_no", "label": M("Formation (Nummer bei Liebe)", "Formation (number in Liebe)"), "type": "integer", "unit": None, "derived": True, "note": "Hauptnummern 1–13 der Gliederung (1 = Kambrium … 13 = Eiszeit/Alluvium); Reihenfolge alt → jung"},
    {"name": "formation", "label": M("Formation", "Formation"), "type": "string", "unit": None, "derived": True, "note": "Kurzbezeichnung nach Liebe"},
    {"name": "formation_en", "label": M("Formation (englisch)", "Formation (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "region", "label": M("Landesteil", "Part of the country"), "type": "string", "unit": None, "note": "Oberland = 1–8, Unterland = 9–13 (Liebes Teile A. und B.)"},
    {"name": "resource", "label": M("Rohstoff (Code)", "Resource (code)"), "type": "string", "unit": None, "derived": True},
    {"name": "resource_order", "label": M("Rohstoff (Ordnung)", "Resource (order)"), "type": "integer", "unit": None, "derived": True},
    {"name": "resource_de", "label": M("Rohstoff", "Resource"), "type": "string", "unit": None, "derived": True},
    {"name": "resource_en", "label": M("Rohstoff (englisch)", "Resource (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "status", "label": M("Nutzung", "Use"), "type": "string", "unit": None, "derived": True, "note": "worked = genutzt bzw. abgebaut (auch: berühmt, in Betrieb), formerly = früher genutzt, aufgelassen, occurs = nur vorkommend, unbedeutend oder nicht abbauwürdig; editorische Einordnung des Wortlauts"},
    {"name": "evidence", "label": M("Wortlaut", "Wording"), "type": "string", "unit": None},
    {"name": "localities", "label": M("Orte / Bemerkung", "Places / remark"), "type": "string", "unit": None},
    {"name": "page", "label": M("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": M("Block", "Block"), "type": "string", "unit": None},
]
TT = lambda f, d, e: {"field": f, "title": M(d, e)}
STAT = ["worked", "formerly", "occurs"]
SEXPR = {"de": "datum.value == 'worked' ? 'genutzt' : datum.value == 'formerly' ? 'früher' : 'vorhanden'",
         "en": "datum.value == 'worked' ? 'worked' : datum.value == 'formerly' ? 'formerly' : 'present'"}
SLAB = {"calculate": {"de": SEXPR["de"].replace("datum.value", "datum.status"), "en": SEXPR["en"].replace("datum.value", "datum.status")}, "as": "status_l"}
FL = {"calculate": {"de": "datum.formation_no + '  ' + datum.formation", "en": "datum.formation_no + '  ' + datum.formation_en"}, "as": "formation_l"}
RL = {"calculate": {"de": "datum.resource_de", "en": "datum.resource_en"}, "as": "resource_l"}
c1 = {
    "height": 420,
    "transform": [SLAB, FL, RL],
    "mark": {"type": "circle", "size": 200},
    "encoding": {
        "x": {"field": "resource_l", "type": "nominal", "title": None, "sort": {"field": "resource_order", "op": "min"}, "axis": {"labelAngle": -40, "labelLimit": 160}},
        "y": {"field": "formation_l", "type": "nominal", "title": None, "sort": {"field": "formation_no", "op": "min"}, "axis": {"labelLimit": 330, "grid": True}},
        "color": {"field": "status", "type": "nominal", "title": None, "scale": {"domain": STAT}, "legend": {"labelExpr": SEXPR}},
        "tooltip": [TT("formation_l", "Formation", "Formation"), TT("resource_l", "Rohstoff", "Resource"), TT("status_l", "Nutzung", "Use"),
                    TT("evidence", "Wortlaut", "Wording"), TT("localities", "Orte", "Places")],
    },
}
c2 = {
    "height": 300,
    "transform": [SLAB, RL],
    "mark": "bar",
    "encoding": {
        "y": {"field": "resource_l", "type": "nominal", "title": None, "sort": {"op": "count", "order": "descending"}, "axis": {"labelLimit": 260}},
        "x": {"aggregate": "count", "type": "quantitative", "title": M("Zahl der Formationen mit Angabe", "Number of formations with an entry"), "axis": {"tickMinStep": 1}},
        "color": {"field": "status", "type": "nominal", "title": None, "scale": {"domain": STAT}, "legend": {"labelExpr": SEXPR}},
        "order": {"field": "status", "type": "nominal", "sort": "descending"},
        "tooltip": [TT("resource_l", "Rohstoff", "Resource"), TT("status_l", "Nutzung", "Use"), {"aggregate": "count", "type": "quantitative", "title": M("Formationen", "Formations")}],
    },
}

ana = {
    "id": "geologie-formationen-rohstoffe",
    "title": M("Nutzbare Gesteine und Erze nach Formation", "Usable rocks and ores by formation"),
    "category": "geology",
    "section": "t1-1-5",
    "sources": refs,
    "summary": M(
        "Neben den Böden beschreibt Prof. Liebe in der geognostischen Übersicht, welche Erze, Kalke, Schiefer, Bausteine und Salze die einzelnen Formationen liefern und ob sie genutzt werden oder wurden. Die Auswertung stellt diese Angaben für 12 der 13 Formationen in einer Matrix zusammen und zählt, in wie vielen Formationen jeder Rohstoff auftritt.",
        "Besides the soils, Prof. Liebe's geological overview describes which ores, limestones, slates, building stones and salts the individual formations yield and whether they are or were worked. The analysis puts these statements for 12 of the 13 formations into a matrix and counts in how many formations each resource occurs."),
    "method": M(
        "Für jede Formation (Liebes Hauptnummern 1–13, S. 25–41) wurden die genannten nutzbaren Stoffe als Einträge erfasst, jeweils mit einem wörtlichen Beleg (Spalte »Wortlaut«; jeder Beleg wurde im zitierten Block geprüft) und den Orten. Die Rohstoffgruppen (Eisenerz, Antimonerz, Kupfer-/Nickelerz, Alaunschiefer, Dachschiefer, Kalkstein, Bausteine/Bausand, Straßenmaterial, Gips/Salz, Kohle) und die Nutzungsstufen (genutzt, früher genutzt, nur vorkommend) sind editorische Einordnungen des Wortlauts. Jede Kombination aus Formation und Rohstoff erscheint nur einmal; Gestein, das Liebe nur als Bodenbildner erwähnt, ist nicht erfasst.",
        "For each formation (Liebe's main numbers 1–13, pp. 25–41) the usable materials he names were recorded as entries, each with a verbatim piece of evidence (column “Wording”; every piece of evidence was checked in the cited block) and the places. The resource groups (iron ore, antimony ore, copper/nickel ore, alum shale, roofing slate, limestone, building stone/sand, road metal, gypsum/salt, coal) and the use grades (worked, formerly worked, merely occurring) are editorial classifications of the wording. Each combination of formation and resource appears only once; rock that Liebe mentions only as a soil former is not recorded."),
    "findings": findings,
    "caveats": [
        M("Die Matrix zeigt, was Liebe nennt, nicht was es an Vorkommen gibt; für manche Formationen führt er Orte und Gruben ausführlich auf, für andere nur nebenbei. Die Anzahl der Einträge ist deshalb auch ein Maß für die Ausführlichkeit seiner Beschreibung.",
          "The matrix shows what Liebe names, not what exists; for some formations he lists places and mines at length, for others only in passing. The number of entries is therefore also a measure of how detailed his description is."),
        M("Die Einstufung »genutzt« beruht auf Gegenwartsformen, Ortsangaben von Brüchen oder Wertungen wie »berühmt«; ob ein Abbau 1870 tatsächlich in Betrieb war, lässt sich aus Liebes Text nicht in jedem Fall entscheiden. Die Abschnitte dieses Kapitels geben keine Fördermengen an.",
          "The grade “worked” rests on present-tense forms, places of quarries or judgements such as “famous”; whether working was actually in progress in 1870 cannot always be decided from Liebe's text. The sections of this chapter give no production figures."),
        M("Wirtschaftliche Zahlen zum Bergbau stehen an anderer Stelle des Werks (Abschnitt Bergbau); hier geht es nur um Liebes geologische Beschreibung.",
          "Economic figures on mining are given elsewhere in the work (section on mining); this analysis covers only Liebe's geological description."),
    ],
    "datasets": [
        {"name": "resources", "title": M("Rohstoffe der Formationen nach Liebe", "Resources of the formations according to Liebe"), "columns": COLS, "rows": rows, "source_refs": refs},
    ],
    "charts": [
        {"id": "c1", "dataset": "resources",
         "title": M("Welche Formation liefert welchen Rohstoff?", "Which formation yields which resource?"),
         "caption": M("Jeder Punkt ist eine Angabe Liebes (Formationen von alt nach jung); Farbe = Art der Nutzung (genutzt / früher genutzt / nur vorhanden). Der Wortlaut und die Orte stehen im Tooltip. Für das Rothliegende (9) nennt Liebe keinen Rohstoff.",
                      "Each dot is a statement by Liebe (formations from old to young); colour = type of use (worked / formerly worked / merely present). Wording and places appear in the tooltip. For the Rotliegend (9) Liebe names no resource."),
         "vegalite": c1},
        {"id": "c2", "dataset": "resources",
         "title": M("In wie vielen Formationen kommt jeder Rohstoff vor?", "In how many formations does each resource occur?"),
         "caption": M("Zahl der Formationen mit einer Angabe zum Rohstoff, nach Nutzungsart gestapelt (genutzt / früher genutzt / nur vorhanden).",
                      "Number of formations with an entry for the resource, stacked by type of use (worked / formerly worked / merely present)."),
         "vegalite": c2},
    ],
    "keywords": {"de": ["Bodenschätze", "Eisenerz", "Antimon", "Kalkstein", "Dachschiefer", "Gips", "Salz", "Braunkohle", "Steinbrüche", "Bergbau", "Geologie"],
                 "en": ["mineral resources", "iron ore", "antimony", "limestone", "roofing slate", "gypsum", "salt", "lignite", "quarries", "mining", "geology"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
