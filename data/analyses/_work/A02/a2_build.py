"""Analysis gewaesser-hauptfluesse-lauf-gefaelle: Saale, Weida, Elster - length, windings, fall; Elster profile."""
from common import *

M = lambda de_, en_: {"de": de_, "en": en_}

# printed numbers verified against the block text
sa_entry = num_in_text("1190", "46", "b2")
sa_exit = num_in_text("923", "46", "b2")
sa_air = num_in_text("6", "46", "b2")
sa_path = num_in_text("11", "46", "b2")  # "über 11 Stunden"
sa_fall_printed = num_in_text("267", "46", "b2")
we_entry = num_in_text("1055", "49", "b6")
we_exit = num_in_text("840", "49", "b6")
we_air = num_in_text("2", "50", "b1")
we_path = 3.5  # "3 1/2 Stunden" (p. 50 b1)
assert "3 1/2 Stunden" in text("50", "b1") and "2 Stunden" in text("50", "b1")
el_air = 3.5
el_path = 4 + 2 / 3  # "3 1/2 ... 4 2/3 Stunden" (p. 51 b1)
assert "3 1/2 und in der Krümmung 4 2/3 Stunden" in text("51", "b1")

rivers = [
    # river, air (Stunden), path (Stunden), entry ft, exit ft, path is lower bound
    ("Saale", sa_air, float(sa_path), sa_entry, sa_exit, "46", "b2"),
    ("Weida", we_air, we_path, we_entry, we_exit, "49", "b6"),
    ("Elster", el_air, round(el_path, 3), 525.0, 459.0, "51", "b1"),
]
assert num_in_text("525", "51", "b1") == 525.0 and num_in_text("459", "51", "b1") == 459.0
river_rows = []
length_rows = []
for name, air, path, ent, ext, pg, bl in rivers:
    fall = ent - ext
    river_rows.append([name, air, path, ent, ext, fall, round(path / air, 2), round(fall / path, 1), round(fall * FT_M, 1)])
    length_rows.append([name, "air", air])
    length_rows.append([name, "path", path])
assert river_rows[0][5] == sa_fall_printed  # 1190 - 923 = 267 as printed
for r in river_rows:
    print(r)

# Elster profile
ST = [("Eintritt ins Land", "525"), ("Zwötzen", "515"), ("Gera", "503"), ("oberhalb Untermhaus", "500"),
      ("Milbitz", "495"), ("Köstritz", "468"), ("Austritt aus dem Land", "459")]
prof_rows = []
prev = None
for i, (st, v) in enumerate(ST, 1):
    ft = num_in_text(v, "51", "b1")
    prof_rows.append([i, st, ft, round(ft * FT_M, 1), None if prev is None else prev - ft])
    prev = ft
for r in prof_rows:
    print(r)
total_fall = prof_rows[0][2] - prof_rows[-1][2]
maxseg = max(prof_rows[1:], key=lambda r: r[4])
seg_from = prof_rows[maxseg[0] - 2][1]
share = maxseg[4] / total_fall * 100
print("max seg", maxseg, seg_from, share)

sa, we, el = river_rows
findings = [
    M(f"Die Saale legt im Land mit über {de(sa[2],0)} Stunden mehr als das {de(sa[6],1)}fache der Luftlinie ({de(sa[1],0)} Stunden) zurück, die Weida das {de(we[6],2)}fache ({de(we[2])} gegenüber {de(we[1],0)} Stunden), die Elster nur das {de(el[6],2)}fache ({de(el[2],2)} gegenüber {de(el[1])} Stunden). Brückners »Schlangenbahn« der Saale ist also nach den Zahlen die am stärksten gewundene der drei.",
      f"Within the country the Saale covers more than {en(sa[6],1)} times its straight-line distance ({en(sa[2],0)}+ against {en(sa[1],0)} Stunden), the Weida {en(we[6],2)} times ({en(we[2])} against {en(we[1],0)} Stunden), the Elster only {en(el[6],2)} times ({en(el[2],2)} against {en(el[1])} Stunden). Brückner's “serpentine track” of the Saale is thus the most winding of the three by his own figures."),
    M(f"Das Gefälle je Stunde Lauflänge ist bei der Weida mit {de(we[7])}' am größten, bei der Saale mit höchstens {de(sa[7])}' und bei der Elster mit {de(el[7])}' am kleinsten. Die Weida fällt damit pro Stunde mindestens {de(we[7]/sa[7],1)}-mal so stark wie die Saale und {de(we[7]/el[7],1)}-mal so stark wie die Elster.",
      f"Fall per Stunde of course is greatest for the Weida at {en(we[7])}', for the Saale at most {en(sa[7])}', and smallest for the Elster at {en(el[7])}'. The Weida thus falls at least {en(we[7]/sa[7],1)} times as steeply per Stunde as the Saale and {en(we[7]/el[7],1)} times as steeply as the Elster."),
    M(f"Die Elster sinkt im Unterland von {de(ST and prof_rows[0][2],0)}' auf {de(prof_rows[-1][2],0)}', insgesamt {de(total_fall,0)}' ({de(total_fall*FT_M,0)} m). Der größte Höhenverlust einer Teilstrecke liegt zwischen {seg_from} und {maxseg[1]}: {de(maxseg[4],0)}' oder {de(share,0)} % des gesamten Gefälles.",
      f"In the Unterland the Elster descends from {en(prof_rows[0][2],0)}' to {en(prof_rows[-1][2],0)}', {en(total_fall,0)}' in all ({en(total_fall*FT_M,0)} m). The largest drop in a single reach lies between {seg_from} and {maxseg[1]}: {en(maxseg[4],0)}' or {en(share,0)} % of the total fall."),
    M(f"Bei der Saale stimmt Brückners gedrucktes Gefälle von {de(sa_fall_printed,0)}' genau mit der Differenz der beiden genannten Höhen ({de(sa_entry,0)}' − {de(sa_exit,0)}') überein; für Weida und Elster ist das Gefälle hier aus den Höhenangaben berechnet.",
      f"For the Saale, Brückner's printed fall of {en(sa_fall_printed,0)}' agrees exactly with the difference of the two stated heights ({en(sa_entry,0)}' − {en(sa_exit,0)}'); for the Weida and Elster the fall is computed here from the stated heights."),
]
for f in findings:
    print(f["de"])

TT = lambda f, d, e: {"field": f, "title": M(d, e)}
RIVER_COLS = [
    {"name": "river", "label": M("Fluss", "River"), "type": "string", "unit": None},
    {"name": "air_stunden", "label": M("Lauf im Luftmaß", "Course as the crow flies"), "type": "number", "unit": "Stunden", "derived": True, "note": "Zahlen im Druck: 6; 2; 3 1/2 (Bruchschreibweise, hier als Dezimalzahl)."},
    {"name": "path_stunden", "label": M("Lauf in der Windung", "Course along the windings"), "type": "number", "unit": "Stunden", "derived": True, "note": "Zahlen im Druck: über 11; 3 1/2; 4 2/3 (Bruchschreibweise, hier als Dezimalzahl); der Wert der Saale ist eine Untergrenze."},
    {"name": "entry_ft", "label": M("Höhe beim Eintritt", "Height at entry"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "exit_ft", "label": M("Höhe beim Austritt", "Height at exit"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "fall_ft", "label": M("Gefälle", "Fall"), "type": "number", "unit": "preuß. Dezimalfuß", "derived": True, "note": "Eintrittshöhe minus Austrittshöhe; für die Saale auch im Druck: 267'."},
    {"name": "sinuosity", "label": M("Windungsverhältnis", "Sinuosity ratio"), "type": "number", "unit": None, "derived": True, "note": "Lauf in der Windung / Lauf im Luftmaß; bei der Saale Untergrenze."},
    {"name": "fall_per_stunde_ft", "label": M("Gefälle je Stunde Lauf", "Fall per Stunde of course"), "type": "number", "unit": "preuß. Dezimalfuß je Stunde", "derived": True, "note": "Gefälle / Lauf in der Windung; bei der Saale Obergrenze."},
    {"name": "fall_m", "label": M("Gefälle", "Fall"), "type": "number", "unit": "m", "derived": True},
]
LEN_COLS = [
    {"name": "river", "label": M("Fluss", "River"), "type": "string", "unit": None},
    {"name": "measure", "label": M("Messung", "Measure"), "type": "string", "unit": None, "derived": True, "note": "air = Luftmaß, path = Windung (Codes editorisch)"},
    {"name": "stunden", "label": M("Länge", "Length"), "type": "number", "unit": "Stunden", "derived": True, "note": "Brüche (3 1/2, 4 2/3) als Dezimalzahlen; Saale: über 11."},
]
PROF_COLS = [
    {"name": "order", "label": M("Reihenfolge flussabwärts", "Order downstream"), "type": "integer", "unit": None, "derived": True},
    {"name": "station", "label": M("Ort", "Place"), "type": "string", "unit": None},
    {"name": "height_ft", "label": M("Höhe des Flussbetts", "Height of the riverbed"), "type": "number", "unit": "preuß. Dezimalfuß"},
    {"name": "height_m", "label": M("Höhe des Flussbetts", "Height of the riverbed"), "type": "number", "unit": "m", "derived": True},
    {"name": "drop_ft", "label": M("Höhenverlust seit dem vorigen Ort", "Drop since previous place"), "type": "number", "unit": "preuß. Dezimalfuß", "derived": True},
]

MEAS = {"calculate": {"de": "datum.measure == 'air' ? 'Luftmaß' : 'Windung'", "en": "datum.measure == 'air' ? 'Straight line' : 'Along the windings'"}, "as": "measure_l"}
c1 = {
    "height": 260,
    "transform": [MEAS],
    "mark": "bar",
    "encoding": {
        "x": {"field": "river", "type": "nominal", "title": None, "sort": ["Saale", "Weida", "Elster"], "axis": {"labelAngle": 0}},
        "xOffset": {"field": "measure", "type": "nominal", "sort": ["air", "path"]},
        "y": {"field": "stunden", "type": "quantitative", "title": M("Lauflänge im Land in Stunden", "Length of course in the country in Stunden")},
        "color": {"field": "measure_l", "type": "nominal", "title": None, "sort": {"field": "measure", "op": "min"}},
        "tooltip": [TT("river", "Fluss", "River"), TT("measure_l", "Messung", "Measure"), TT("stunden", "Länge (Stunden)", "Length (Stunden)")],
    },
}
c2 = {
    "height": 240,
    "mark": "bar",
    "encoding": {
        "x": {"field": "river", "type": "nominal", "title": None, "sort": ["Saale", "Weida", "Elster"], "axis": {"labelAngle": 0}},
        "y": {"field": "fall_per_stunde_ft", "type": "quantitative", "title": M("Gefälle in Dezimalfuß je Stunde Lauflänge", "Fall in decimal feet per Stunde of course")},
        "tooltip": [TT("river", "Fluss", "River"), TT("fall_ft", "Gefälle gesamt (Fuß)", "Total fall (ft)"), TT("path_stunden", "Lauf in Windung (Stunden)", "Course along windings (Stunden)"),
                    TT("fall_per_stunde_ft", "Fuß je Stunde", "Feet per Stunde")],
    },
}
c3 = {
    "height": 280,
    "transform": [{"calculate": {"de": "datum.station == 'Eintritt ins Land' ? 'Eintritt' : datum.station == 'Austritt aus dem Land' ? 'Austritt' : datum.station == 'oberhalb Untermhaus' ? 'ob. Untermhaus' : datum.station",
                                 "en": "datum.station == 'Eintritt ins Land' ? 'Entry' : datum.station == 'Austritt aus dem Land' ? 'Exit' : datum.station == 'oberhalb Untermhaus' ? 'above Untermhaus' : datum.station"},
                   "as": "station_l"}],
    "mark": {"type": "line", "point": True},
    "encoding": {
        "x": {"field": "station_l", "type": "ordinal", "title": M("Orte in Fließrichtung (nicht maßstäblich)", "Places in flow direction (not to scale)"),
              "sort": {"field": "order", "op": "min"}, "axis": {"labelAngle": -30, "labelLimit": 220}},
        "y": {"field": "height_m", "type": "quantitative", "title": M("Höhe des Flussbetts in m", "Height of the riverbed in m"), "scale": {"zero": False}},
        "tooltip": [TT("station_l", "Ort", "Place"), TT("height_ft", "Höhe (Dezimalfuß)", "Height (decimal feet)"), TT("height_m", "Höhe (m)", "Height (m)"), TT("drop_ft", "Verlust seit vorigem Ort (Fuß)", "Drop since previous place (ft)")],
    },
}

SRC = [{"page": "46", "block": "b2"}, {"page": "49", "block": "b6"}, {"page": "50", "block": "b1"}, {"page": "51", "block": "b1"}]
ana = {
    "id": "gewaesser-hauptfluesse-lauf-gefaelle",
    "title": M("Saale, Weida und Elster: Lauflänge, Windung und Gefälle", "Saale, Weida and Elster: length, windings and fall"),
    "category": "hydrology",
    "section": "t1-1-6",
    "sources": SRC,
    "summary": M(
        "Für Saale, Weida und Weiße Elster gibt Brückner an, wie lang ihr Lauf im Land in der Luftlinie und in den Windungen ist und auf welcher Höhe sie das Land betreten und verlassen. Daraus lassen sich das Verhältnis von Windung zu Luftlinie und das Gefälle je Stunde Lauf berechnen. Für die Elster nennt er zusätzlich sieben Höhen entlang ihres Laufs durch das Unterland.",
        "For the Saale, Weida and White Elster Brückner states how long their course in the country is as the crow flies and along the windings, and at what height they enter and leave the country. From this the ratio of windings to straight line and the fall per Stunde of course can be computed. For the Elster he also gives seven heights along its course through the Unterland."),
    "method": M(
        "Längen (S. 46, 50, 51) in »Stunden« und Höhen in preuß. Dezimalfuß (S. 46, 49, 51; Einheit nach Brückners Fußnote S. 11) sind den Gewässerbeschreibungen entnommen. Die Brüche »3 1/2« und »4 2/3« wurden in Dezimalzahlen umgesetzt, die Saale-Länge »über 11 Stunden« als 11 gerechnet (Untergrenze). Windungsverhältnis = Lauf in der Windung / Lauf im Luftmaß; Gefälle = Höhe beim Eintritt minus Höhe beim Austritt; Gefälle je Stunde = Gefälle / Lauf in der Windung. Für die Elster-Höhenreihe wurden die sieben Ortsangaben in der Reihenfolge des Textes übernommen; Entfernungen zwischen den Orten gibt Brückner nicht an.",
        "Lengths (pp. 46, 50, 51) in “Stunden” and heights in Prussian decimal feet (pp. 46, 49, 51; unit according to Brückner's footnote on p. 11) are taken from the river descriptions. The fractions “3 1/2” and “4 2/3” were converted to decimals; the Saale length “over 11 Stunden” was taken as 11 (lower bound). Sinuosity ratio = course along the windings / course as the crow flies; fall = height at entry minus height at exit; fall per Stunde = fall / course along the windings. For the Elster height series the seven place names were taken in the order of the text; Brückner gives no distances between them."),
    "findings": findings,
    "caveats": [
        M("Brückner erklärt die Längeneinheit »Stunde« nicht (vermutlich Wegstunde); die Verhältniszahlen sind davon unabhängig, absolute Kilometerwerte lassen sich aus seinem Text nicht belegen.",
          "Brückner does not define the unit “Stunde” (presumably a walking hour); the ratios are independent of it, but absolute kilometer values cannot be derived from his text."),
        M("Die Saale-Länge ist als »über 11 Stunden« angegeben; Windungsverhältnis und Gefälle je Stunde sind deshalb eine Unter- bzw. Obergrenze.",
          "The Saale length is given as “over 11 Stunden”; sinuosity and fall per Stunde are therefore a lower and an upper bound respectively."),
        M("Alle drei Flüsse entspringen außerhalb des Landes; die Angaben gelten nur für die Strecke im reußischen Gebiet, die bei der Weida (zwei Abschnitte im Amt Schleiz, S. 49) und bei der Saale (Grenzstrecken) nicht zusammenhängend im Landesinneren verläuft.",
          "All three rivers rise outside the country; the figures apply only to the stretch within Reuss territory, which for the Weida (two sections in the Schleiz district, p. 49) and the Saale (border stretches) does not lie wholly in the interior."),
    ],
    "conversions": [
        {"from": "preuß. Dezimalfuß (Höhen)", "to": "m", "factor_or_formula": "m = Dezimalfuß × 0.3766242 (1 Dezimalfuß = 1/10 preuß. Ruthe)", "reference": "Brückner S. 11 Fußnote (Dezimalfuß, Pegel Swinemünde); S. 831: 1 preuß. Ruthe = 3,766242 m"},
    ],
    "datasets": [
        {"name": "rivers", "title": M("Hauptflüsse im Land", "Main rivers in the country"), "columns": RIVER_COLS, "rows": river_rows,
         "source_refs": SRC},
        {"name": "lengths", "title": M("Lauflängen (Luftmaß und Windung)", "Course lengths (straight line and windings)"), "columns": LEN_COLS, "rows": length_rows,
         "source_refs": [{"page": "46", "block": "b2"}, {"page": "50", "block": "b1"}, {"page": "51", "block": "b1"}]},
        {"name": "elster_profile", "title": M("Höhen der Elster im Unterland", "Heights of the Elster in the Unterland"), "columns": PROF_COLS, "rows": prof_rows,
         "source_refs": [{"page": "51", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "lengths",
         "title": M("Lauf im Luftmaß und in den Windungen", "Course in a straight line and along the windings"),
         "caption": M("Länge des Laufs innerhalb des Landes in Stunden nach Brückner. Der Saale-Wert (11) ist eine Untergrenze (»über 11 Stunden«).",
                      "Length of the course within the country in Stunden according to Brückner. The Saale value (11) is a lower bound (“over 11 Stunden”)."),
         "vegalite": c1},
        {"id": "c2", "dataset": "rivers",
         "title": M("Gefälle je Stunde Lauflänge", "Fall per Stunde of course"),
         "caption": M("Gefälle zwischen Eintritt und Austritt geteilt durch die Lauflänge in den Windungen (Dezimalfuß je Stunde). Der Saale-Wert ist eine Obergrenze.",
                      "Fall between entry and exit divided by the course length along the windings (decimal feet per Stunde). The Saale value is an upper bound."),
         "vegalite": c2},
        {"id": "c3", "dataset": "elster_profile",
         "title": M("Höhenprofil der Weißen Elster im Unterland", "Height profile of the White Elster in the Unterland"),
         "caption": M("Höhe des Flussbetts an den sieben von Brückner genannten Stellen (Meter, aus Dezimalfuß umgerechnet). Die Abstände zwischen den Orten sind nicht bekannt; die Punkte stehen daher gleich weit auseinander.",
                      "Height of the riverbed at the seven places Brückner names (meters, converted from decimal feet). The distances between the places are not known, so the points are spaced evenly."),
         "vegalite": c3},
    ],
    "keywords": {"de": ["Saale", "Weida", "Weiße Elster", "Gefälle", "Flusslauf", "Windung", "Höhenprofil", "Gera", "Köstritz"],
                 "en": ["Saale", "Weida", "White Elster", "gradient", "river course", "meanders", "height profile", "Gera", "Köstritz"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
