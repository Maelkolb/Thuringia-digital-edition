"""Analysis geologie-formationen-bodenguete: soil quality by formation, coded from Liebe's wording (pp. 26-41).

Each row is one rock unit with a verbatim German quotation about the soil it produces. The 1-5 rating is an
editorial coding of that wording (rubric in the method text); every quotation is asserted against the cited block."""
import re
from common import *

M = lambda de_, en_: {"de": de_, "en": en_}

# (section label in print, order, region, group, German name, English name, page, block, [quotations], rating, note)
U = [
    ("1a", "Oberland", "slate", "Kambrische Schiefer, Sandsteine", "Cambrian slates, sandstones", "26", "b2",
     ["wohl locker, aber nicht warm, jedoch der Vegetation nicht ungünstig"], 3,
     "uneinheitlich: dünnschieferig besser, sandsteinartig »dürftig«, als Quarzit »arm mager«"),
    ("1b", "Oberland", "crystalline", "Talkschiefer von Hirschberg (Kambrium)", "Talcose schist of Hirschberg (Cambrian)", "26", "b3",
     ["so liefert es eine sehr gute Ackererde"], 5, "Felder meist steil, daher der Auslaugung ausgesetzt"),
    ("1c", "Oberland", "crystalline", "Quarzreicher Gneis bei Göttengrün", "Quartz-rich gneiss near Göttengrün", "26", "b5",
     ["der Vegetation außerordentlich günstig"], 5, ""),
    ("2a", "Oberland", "slate", "Älterer Dachschiefer (unteres Silur)", "Older roofing slate (Lower Silurian)", "27", "b4",
     ["einen ziemlich kalten, thonigen Boden von mittlerer Fruchtbarkeit"], 3, ""),
    ("2b", "Oberland", "greenstone", "Grünsteinlager im unteren Silur", "Greenstone sheets in the Lower Silurian", "28", "b2",
     ["einen trefflichen lichtgefärbten lockeren Boden"], 5, ""),
    ("2d", "Oberland", "crystalline", "Gneisartiges Gestein bei Rothenacker", "Gneiss-like rock near Rothenacker", "28", "b4",
     ["der Vegetation nicht sehr günstig zu sein scheint"], 2, ""),
    ("3a", "Oberland", "slate", "Kieselschiefer (mittleres Silur)", "Siliceous slate (Middle Silurian)", "28", "b5",
     ["so giebt er einen wenig fruchtbaren Boden"], 2, "durch beigemengten Grünstein oder gute Bewirtschaftung ertragfähig"),
    ("3b", "Oberland", "slate", "Weicher Schiefer (mittleres Silur)", "Soft slate (Middle Silurian)", "30", "b1",
     ["einen hellgrauen, kalten, thonigen Boden von mittler Güte für Feld- und Wiesenkultur, aber sehr günstig für Nadelholzbestände"], 3,
     "für Nadelwald sehr günstig"),
    ("3c", "Oberland", "greenstone", "Grünsteine im mittleren Silur", "Greenstones in the Middle Silurian", "30", "b2",
     ["Er verwittert zu einem hellgelben, fruchtbaren, lehmigen Boden"], 4, ""),
    ("4a", "Oberland", "slate", "Tentaculitenschiefer (oberes Silur)", "Tentaculite slate (Upper Silurian)", "31", "b1",
     ["einen gelblichen bis bräunlichen Boden von sehr mittelmäßiger Fruchtbarkeit"], 3, "durch daneben anstehende Grünsteine bedeutend gehoben"),
    ("4b", "Oberland", "greenstone", "Titaneisendiabas (Tentaculitenformation)", "Titaniferous diabase (Tentaculite formation)", "31", "b2",
     ["einen lockeren warmen, röthlich gelb-braunen Boden von großer Fruchtbarkeit"], 5, ""),
    ("5a", "Oberland", "slate", "Phyllodocitesschiefer", "Phyllodocite slate", "32", "b3",
     ["eignet sich der Boden ziemlich gut, weit besser aber"], 3, "etwas kalter, thoniger Boden; für Wald weit besser als für Acker"),
    ("6a", "Oberland", "greenstone", "Untere devonische Tufflager", "“Lower Devonian” tuff beds", "33", "b4",
     ["einen rostbraunen, sehr fruchtbaren, lockeren und warmen"], 5, "Brückners Bezeichnung; auf Höhen zu locker und trocken"),
    ("6b", "Oberland", "greenstone", "Diabase der Tuffformation", "Diabases of the tuff formation", "34", "b1",
     ["Alle diese Diabase liefern einen ebenso günstigen Boden wie die älteren Diabase"], 5, ""),
    ("7a", "Oberland", "slate", "Cypridinenschiefer", "Cypridina slate", "34", "b3",
     ["zu einem schweren kalten thonigen Boden von mittler Fruchtbarkeit"], 3, ""),
    ("7b", "Oberland", "limestone", "Clymenienkalk", "Clymenia limestone", "35", "b1",
     ["einen bräunlichen, trockenen und hitzigen Boden", "Wo Schiefer und Kalk gemischt den Boden bilden, da ist letzterer sehr fruchtbar"], 4,
     "für Futterkräuter ausgezeichnet; mit Schiefer gemischt sehr fruchtbar"),
    ("7c", "Oberland", "greenstone", "Kalkdiabase", "Lime diabases", "36", "b1",
     ["einen bräunlichen, lockeren, warmen, sehr fruchtbaren Boden"], 5, ""),
    ("8", "Oberland", "slate", "Kulm (Grauwacke, Schiefer)", "Culm (greywacke, slate)", "37", "b1",
     ["etwas schweren und kalten, aber fruchtbaren Boden"], 4, "bei richtiger Behandlung für alle Kulturen gute Erträge"),
    ("9", "Unterland", "clastic", "Rothliegendes", "Rotliegend", "37", "b4",
     ["nur mittelmäßigen Boden", "geradezu unfruchtbar"], 2, "auf Höhen und Abhängen unfruchtbar"),
    ("10a", "Unterland", "limestone", "Zechstein (Kalk, Dolomit, Mergel)", "Zechstein (limestone, dolomite, marl)", "38", "b1",
     ["gut geeignet zu allen Culturen, namentlich auch zur Obstcultur"], 4, ""),
    ("11a", "Unterland", "clastic", "Buntsandstein", "Bunter sandstone", "39", "b2",
     ["ist sehr verschiedenartig", "dann ist er von mittler Güte"], 3, "von »Gaux« (unfruchtbar) bis gut, je nach Letten- und Kalkgehalt"),
    ("12c", "Unterland", "clastic", "Tertiäre Sande und Gerölle", "Tertiary sands and gravels", "40", "b3",
     ["einen wenig fruchtbaren Boden"], 2, ""),
    ("13a", "Unterland", "clastic", "Eiszeitliche Gerölle", "Ice-age gravels", "40", "b4",
     ["einen Boden von nur mittler Fruchtbarkeit"], 3, ""),
    ("13c", "Unterland", "clastic", "Alluviale Thone im Elsterthal", "Alluvial clays in the Elster valley", "41", "b1",
     ["Erstere geben einen sehr fruchtbaren"], 5, ""),
    ("13c", "Unterland", "clastic", "Alluviale Gerölle im Elsterthal", "Alluvial gravels in the Elster valley", "41", "b1",
     ["letztere einen sehr mittelmäßigen Boden, der stellenweise geradezu schlecht genannt werden muß"], 2, ""),
]
rows = []
refs = []
for i, (sec, reg, grp, dn, en_, pg, bl, quotes, rating, note) in enumerate(U, 1):
    t = re.sub(r"\s+", " ", text(pg, bl))
    t = t.replace("= ", "").replace("=", "")
    for q in quotes:
        assert q in t, (sec, q)
    rows.append([i, sec, reg, grp, dn, en_, " … ".join(quotes), rating, note, pg, bl])
    if {"page": pg, "block": bl} not in refs:
        refs.append({"page": pg, "block": bl})
print(len(rows), "rows")

from collections import defaultdict
bygrp = defaultdict(list)
for r in rows:
    bygrp[r[3]].append(r[7])
for g, v in bygrp.items():
    print(g, len(v), sum(v) / len(v), v)
mean = lambda v: sum(v) / len(v)
green = bygrp["greenstone"]
slate = bygrp["slate"]
assert min(green) >= 4
assert max(bygrp['slate']) < 5 and all(r[7] <= 2 for r in rows if r[7] <= 2) and len([r for r in rows if r[7] == 1]) == 0
n5 = sum(1 for r in rows if r[7] == 5)
n5_green = sum(1 for r in rows if r[7] == 5 and r[3] == "greenstone")
low = [r for r in rows if r[7] <= 2]
print(n5, n5_green, [(r[1], r[4]) for r in low])
ober = [r[7] for r in rows if r[2] == "Oberland"]
unter = [r[7] for r in rows if r[2] == "Unterland"]
print(mean(ober), mean(unter), len(ober), len(unter))
slate_wo_kulm = [r[7] for r in rows if r[3] == "slate" and r[1] != "8"]
print(slate_wo_kulm)

findings = [
    M(f"Alle {len(green)} Grünstein-, Diabas- und Tuffeinheiten (2b, 3c, 4b, 6a, 6b, 7c) liefern nach Liebe gute bis sehr gute Böden (Stufe {min(green)}–{max(green)}, Mittel {de(mean(green),1)}); {n5_green} von ihnen erreichen die Höchststufe. Sie stellen {n5_green} von {n5} der am besten bewerteten Einheiten.",
      f"All {len(green)} greenstone, diabase and tuff units (2b, 3c, 4b, 6a, 6b, 7c) yield good to very good soils according to Liebe (grades {min(green)}–{max(green)}, mean {en(mean(green),1)}); {n5_green} of them reach the top grade. They account for {n5_green} of the {n5} best-rated units."),
    M(f"Die Schiefer des Oberlandes bleiben im Mittel bei {de(mean(slate),1)} (mittlere Fruchtbarkeit); nur der Kulm erreicht Stufe 4, der Kieselschiefer fällt auf Stufe 2. Ohne den Kulm liegen alle Schieferböden bei höchstens {max(slate_wo_kulm)}.",
      f"The slates of the Oberland average {en(mean(slate),1)} (medium fertility); only the Culm reaches grade 4, the siliceous slate drops to grade 2. Without the Culm all slate soils lie at {max(slate_wo_kulm)} at most."),
    M(f"Schlechte Böden ({len(low)} Einheiten auf Stufe 2) tragen Kieselschiefer, das gneisartige Gestein von Rothenacker, das Rothliegende, die tertiären Sande und Gerölle sowie die alluvialen Gerölle im Elstertal. Im Mittel liegt das Unterland mit {de(mean(unter),1)} unter dem Oberland ({de(mean(ober),1)}); Grünsteinlager nennt Liebe im Unterland nicht.",
      f"Poor soils ({len(low)} units at grade 2) belong to siliceous slate, the gneiss-like rock of Rothenacker, the Rotliegend, the Tertiary sands and gravels and the alluvial gravels in the Elster valley. On average the Unterland, at {en(mean(unter),1)}, lies below the Oberland ({en(mean(ober),1)}); Liebe names no greenstone sheets in the Unterland."),
    M("Außer den Grünsteinen erreichen im Oberland nur zwei kleinräumige kristalline Vorkommen die Höchststufe (Talkschiefer von Hirschberg, quarzreicher Gneis bei Göttengrün); die weit verbreiteten Schiefer erreichen sie nie.",
      "Apart from the greenstones, only two small crystalline occurrences in the Oberland reach the top grade (talcose schist of Hirschberg, quartz-rich gneiss near Göttengrün); the widespread slates never do."),
]
for f in findings:
    print(f["de"])

COLS = [
    {"name": "order", "label": M("Reihenfolge (alt → jung)", "Order (old → young)"), "type": "integer", "unit": None, "derived": True, "note": "Reihenfolge nach Liebes Gliederung 1–13, innerhalb einer Nummer in der Reihenfolge des Textes"},
    {"name": "section", "label": M("Abschnitt bei Liebe", "Section in Liebe's text"), "type": "string", "unit": None, "note": "Nummer wie gedruckt, z. B. »7 b« (hier ohne Leerzeichen)"},
    {"name": "region", "label": M("Landesteil", "Part of the country"), "type": "string", "unit": None, "note": "Oberland = Abschnitte 1–8 (A.), Unterland = 9–13 (B.)"},
    {"name": "rock_group", "label": M("Gesteinsgruppe", "Rock group"), "type": "string", "unit": None, "derived": True, "note": "slate = Schiefer/Grauwacke, greenstone = Grünstein/Diabas/Tuff, limestone = Kalk, crystalline = Gneis/umgewandelter Schiefer, clastic = Sand, Sandstein, Gerölle, Ton; editorisch"},
    {"name": "formation", "label": M("Formation / Gestein", "Formation / rock"), "type": "string", "unit": None},
    {"name": "formation_en", "label": M("Formation / Gestein (englisch)", "Formation / rock (English)"), "type": "string", "unit": None, "derived": True},
    {"name": "quote", "label": M("Wortlaut zum Boden", "Wording on the soil"), "type": "string", "unit": None},
    {"name": "soil_grade", "label": M("Bodengüte (Stufe 1–5)", "Soil quality (grade 1–5)"), "type": "integer", "unit": None, "derived": True, "note": "Editorische Einstufung des Wortlauts: 5 = sehr fruchtbar/ausgezeichnet/trefflich, 4 = fruchtbar/gut geeignet, 3 = mittelmäßig/mittlere Güte, 2 = wenig fruchtbar/dürftig/nicht günstig, 1 = unfruchtbar/arm (kommt nicht vor)"},
    {"name": "remark", "label": M("Bemerkung", "Remark"), "type": "string", "unit": None},
    {"name": "page", "label": M("Seite", "Page"), "type": "string", "unit": None},
    {"name": "block", "label": M("Block", "Block"), "type": "string", "unit": None},
]
TT = lambda f, d, e: {"field": f, "title": M(d, e)}
GCODES = ["greenstone", "crystalline", "limestone", "clastic", "slate"]
GEXPR = {
    "de": "datum.value == 'greenstone' ? 'Grünstein' : datum.value == 'crystalline' ? 'Kristallin' : datum.value == 'limestone' ? 'Kalk' : datum.value == 'clastic' ? 'Sand/Ton' : 'Schiefer'",
    "en": "datum.value == 'greenstone' ? 'Greenstone' : datum.value == 'crystalline' ? 'Crystalline' : datum.value == 'limestone' ? 'Limestone' : datum.value == 'clastic' ? 'Sand/clay' : 'Slate'",
}
GLONG = {
    "de": "datum.rock_group == 'greenstone' ? 'Grünstein, Diabas, Tuff' : datum.rock_group == 'crystalline' ? 'Gneis, umgewandelter Schiefer' : datum.rock_group == 'limestone' ? 'Kalk' : datum.rock_group == 'clastic' ? 'Sand, Sandstein, Gerölle, Ton' : 'Schiefer, Grauwacke'",
    "en": "datum.rock_group == 'greenstone' ? 'Greenstone, diabase, tuff' : datum.rock_group == 'crystalline' ? 'Gneiss, altered slate' : datum.rock_group == 'limestone' ? 'Limestone' : datum.rock_group == 'clastic' ? 'Sand, sandstone, gravel, clay' : 'Slate, greywacke'",
}
GLAB = {"calculate": GLONG, "as": "group_l"}
FL = {"calculate": {"de": "datum.section + '  ' + datum.formation", "en": "datum.section + '  ' + datum.formation_en"}, "as": "formation_l"}
GRADE_EXPR = {"de": "datum.value == 1 ? 'unfruchtbar' : datum.value == 2 ? 'gering' : datum.value == 3 ? 'mittel' : datum.value == 4 ? 'gut' : 'sehr gut'",
              "en": "datum.value == 1 ? 'barren' : datum.value == 2 ? 'poor' : datum.value == 3 ? 'medium' : datum.value == 4 ? 'good' : 'very good'"}
c1 = {
    "height": 560,
    "transform": [GLAB, FL],
    "mark": "bar",
    "encoding": {
        "y": {"field": "formation_l", "type": "nominal", "title": None, "sort": {"field": "order", "op": "min"}, "axis": {"labelLimit": 400}},
        "x": {"field": "soil_grade", "type": "quantitative", "title": M("Bodengüte (Stufe 1–5)", "Soil quality (grade 1–5)"),
              "scale": {"domain": [0, 5]}, "axis": {"values": [1, 2, 3, 4, 5]}},
        "color": {"field": "rock_group", "type": "nominal", "title": None, "scale": {"domain": GCODES}, "legend": {"labelExpr": GEXPR, "columns": 2}},
        "tooltip": [TT("formation_l", "Einheit", "Unit"), TT("group_l", "Gesteinsgruppe", "Rock group"), TT("soil_grade", "Stufe", "Grade"),
                    TT("quote", "Liebe über den Boden", "Liebe on the soil"), TT("remark", "Bemerkung", "Remark")],
    },
}
c2 = {
    "height": 240,
    "transform": [GLAB, {"aggregate": [{"op": "mean", "field": "soil_grade", "as": "mean_grade"}, {"op": "count", "as": "n"}], "groupby": ["rock_group", "group_l"]}],
    "mark": "bar",
    "encoding": {
        "y": {"field": "group_l", "type": "nominal", "title": None, "sort": {"field": "mean_grade", "order": "descending"}, "axis": {"labelLimit": 300}},
        "x": {"field": "mean_grade", "type": "quantitative", "title": M("Mittlere Bodengüte (Stufe 1–5)", "Mean soil quality (grade 1–5)"), "scale": {"domain": [0, 5]}, "axis": {"values": [1, 2, 3, 4, 5]}},
        "color": {"field": "rock_group", "type": "nominal", "title": None, "scale": {"domain": GCODES}, "legend": None},
        "tooltip": [TT("group_l", "Gesteinsgruppe", "Rock group"), {"field": "mean_grade", "type": "quantitative", "format": ".2f", "title": M("Mittlere Stufe", "Mean grade")}, TT("n", "Zahl der Einheiten", "Number of units")],
    },
}

ana = {
    "id": "geologie-formationen-bodenguete",
    "title": M("Bodengüte nach Gesteinsformation im Oberland und Unterland", "Soil quality by rock formation in the Oberland and Unterland"),
    "category": "geology",
    "section": "t1-1-5",
    "sources": refs,
    "summary": M(
        "Prof. Liebe beschreibt in der geognostischen Übersicht für fast jede Gesteinsformation, welchen Boden ihre Verwitterung liefert (»sehr fruchtbar«, »mittlerer Güte«, »wenig fruchtbar« …). Die Auswertung ordnet diese Aussagen für 25 Gesteinseinheiten einer fünfstufigen Skala zu und vergleicht Gesteinsgruppen sowie Oberland und Unterland.",
        "In the geological overview Prof. Liebe describes for almost every rock formation what soil its weathering yields (“very fertile”, “of medium quality”, “poorly fertile” …). The analysis assigns these statements for 25 rock units to a five-grade scale and compares groups of rock and the Oberland with the Unterland."),
    "method": M(
        "Für jede Einheit wurde Liebes Satz über den Verwitterungsboden wörtlich übernommen (Spalte »Wortlaut«; jeder Wortlaut wurde im zitierten Block geprüft) und einer Stufe zugeordnet: 5 = sehr fruchtbar, ausgezeichnet, trefflich, außerordentlich günstig; 4 = fruchtbar, gut geeignet; 3 = mittelmäßig, von mittlerer Güte; 2 = wenig fruchtbar, nicht sehr günstig, dürftig; 1 = unfruchtbar (kommt nicht vor). Enthält ein Satz Unterschiede (z. B. beim Buntsandstein »von Gaux bis gut«), wurde die Mitte gewählt und die Spannweite im Bemerkungsfeld festgehalten. Die Gesteinsgruppen (Schiefer/Grauwacke, Grünstein/Diabas/Tuff, Kalk, kristalline Gesteine, Sand/Sandstein/Gerölle/Ton) sind editorisch; Einheiten ohne Aussage zum Boden (z. B. Granit von Helmsgrün, Süßwassersandstein) fehlen.",
        "For each unit Liebe's sentence about the weathering soil was taken verbatim (column “Wording”; every wording was checked in the cited block) and assigned a grade: 5 = very fertile, excellent, splendid, exceptionally favourable; 4 = fertile, well suited; 3 = mediocre, of medium quality; 2 = poorly fertile, not very favourable, meagre; 1 = barren (does not occur). Where a sentence contains differences (e.g. for the Bunter sandstone “from Gaux to good”) the middle was chosen and the range recorded in the remark field. The rock groups (slate/greywacke, greenstone/diabase/tuff, limestone, crystalline rocks, sand/sandstone/gravel/clay) are editorial; units without a statement about the soil (e.g. the granite of Helmsgrün, the freshwater sandstone) are omitted."),
    "findings": findings,
    "caveats": [
        M("Die Einstufung ist eine Deutung von Liebes Worten, keine Messung; sie fasst oft unterschiedlich fruchtbare Varianten einer Formation in einer Stufe zusammen, und die tatsächliche Fruchtbarkeit hängt auch von Lage, Neigung, Klima und Bewirtschaftung ab, die Liebe zum Teil erwähnt.",
          "The grading is an interpretation of Liebe's words, not a measurement; it often puts differently fertile varieties of a formation into one grade, and actual fertility also depends on position, slope, climate and farming, which Liebe partly mentions."),
        M("Die Einheiten sind nach Liebes Gliederung gewählt und nicht flächengewichtet: Ein kleinräumiges Gneisvorkommen zählt gleich wie der weit verbreitete Schiefer. Über die Flächenanteile der Formationen macht der Text keine Zahlenangaben.",
          "The units follow Liebe's division and are not weighted by area: a small gneiss outcrop counts as much as the widespread slate. The text gives no figures on the areas of the formations."),
        M("Die Bezeichnung »untere devonische Tufflager« ist Liebes eigene; er stellt sie nach den Versteinerungen in die unterste Abteilung des oberen Devon (S. 33).",
          "The name “lower Devonian tuff beds” is Liebe's own; on the evidence of the fossils he places them in the lowest division of the Upper Devonian (p. 33)."),
    ],
    "datasets": [
        {"name": "soils", "title": M("Böden der Gesteinseinheiten nach Liebe", "Soils of the rock units according to Liebe"), "columns": COLS, "rows": rows, "source_refs": refs},
    ],
    "charts": [
        {"id": "c1", "dataset": "soils",
         "title": M("Bodengüte der Gesteinseinheiten (von alt nach jung)", "Soil quality of the rock units (old to young)"),
         "caption": M("Reihenfolge wie in Liebes Gliederung (1 = älteste Formation, 13 = jüngste); Farbe = Gesteinsgruppe. Stufe 1 = unfruchtbar, 3 = mittel, 5 = sehr fruchtbar; die Stufen sind eine editorische Einordnung des Wortlauts, der im Tooltip steht.",
                      "Order as in Liebe's division (1 = oldest formation, 13 = youngest); colour = rock group. Grade 1 = barren, 3 = medium, 5 = very fertile; the grades are an editorial grading of the wording, which appears in the tooltip."),
         "vegalite": c1},
        {"id": "c2", "dataset": "soils",
         "title": M("Mittlere Bodengüte nach Gesteinsgruppe", "Mean soil quality by rock group"),
         "caption": M("Mittelwert der Stufen (1 = unfruchtbar, 5 = sehr fruchtbar) der Einheiten je Gruppe (Grünstein 6, Schiefer 8, Sand/Gerölle/Ton 6, Kalk 2, kristallin 3 Einheiten).",
                      "Mean of the grades (1 = barren, 5 = very fertile) of the units in each group (greenstone 6, slate 8, sand/gravel/clay 6, limestone 2, crystalline 3 units)."),
         "vegalite": c2},
    ],
    "keywords": {"de": ["Boden", "Bodengüte", "Fruchtbarkeit", "Gesteine", "Grünstein", "Diabas", "Schiefer", "Kalk", "Geologie", "Liebe"],
                 "en": ["soil", "soil quality", "fertility", "rocks", "greenstone", "diabase", "slate", "limestone", "geology", "Liebe"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
# check the group counts used in the caption
cnt = {g: len(v) for g, v in bygrp.items()}
assert cnt == {"slate": 8, "crystalline": 3, "greenstone": 6, "limestone": 2, "clastic": 6}, cnt
write_analysis(ana)
