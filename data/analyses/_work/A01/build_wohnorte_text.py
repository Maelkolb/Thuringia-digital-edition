"""Part 2: texts, datasets, charts for relief-wohnorte-hoehenlage."""
from build_wohnorte import *      # noqa: F401,F403

LB = T("Landesteil", "Part of the country")
COL = {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland"]}}

# ---- recount against Brückner's classes (p. 11) -----------------------------------------------------------------
Uo = [p for p in U if p["kind"] == "ort"]
core = [p for p in Uo if p["name"] not in ("Caaschwitz", "Käseschenke")]
edges = (500, 600, 700, 800, 900)
recount = [0] * 5
for p in core:
    for i, e in enumerate(edges):
        if p["lo"] < e:
            recount[i] += 1
            break
brueckner = [6, 23, 23, 28, 5]
assert sum(recount) == len(core)
klass_rows = []
for lab, e, b, r in zip(["unter 500′", "500–600′", "600–700′", "700–800′", "800–900′"], edges, brueckner, recount):
    klass_rows.append([lab, e, b, r])
print("recount", recount, "n ort", len(Uo))

u = unit_checks()
n_ob_ort = sum(1 for p in O if p["kind"] == "ort")
d_ob = (highO["hi"] - lowO["lo"])
mean_ext_O = (lowO["lo"] + highO["hi"]) / 2
m = lambda ft: ft * D
f0 = lambda x: fmt(x, 0)
f0e = lambda x: fmt(x, 0, "en")
diffU = highU["hi"] - lowU["lo"]
diffU_m = m(diffU)

ana = {
    "id": "relief-wohnorte-hoehenlage",
    "title": T("Höhenlage der Wohnorte in Ober- und Unterland", "Altitude of the inhabited places in the Oberland and Unterland"),
    "category": "relief",
    "section": "t1-1-4",
    "sources": [
        {"page": "11", "block": "b11"}, {"page": "11", "block": "b13"}, {"page": "11", "block": "fn1"},
        {"page": "12", "block": "b1"}, {"page": "12", "block": "b3"}, {"page": "12", "block": "b4"},
        {"page": "13", "block": "b1"},
        {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}, {"page": "22", "block": "b2"},
        {"page": "831", "block": "b8"},
    ],
    "summary": T(
        f"Brückner verzeichnet die Meereshöhe von rund {len(PLACES)} bewohnten Punkten des Landes, meist als Spanne von der untersten bis zur obersten Grenze des Ortes: im Unterland getrennt nach rechtem und linkem Elsterufer, im Oberland in einer einzigen aufsteigenden Liste. Umgerechnet liegen die Orte des Unterlandes im Median bei {f0(m(med_U))} m, die des Oberlandes bei {f0(m(med_O))} m; die beiden Höhenstufen überschneiden sich nur in einem schmalen Band.",
        f"Brückner lists the altitude of about {len(PLACES)} inhabited points of the country, mostly as a range from the lowest to the highest limit of the place: in the Unterland separated by the right and left bank of the Elster, in the Oberland in a single ascending list. Converted, the places of the Unterland lie at a median of {f0e(m(med_U))} m, those of the Oberland at {f0e(m(med_O))} m; the two altitude belts overlap only in a narrow band."),
    "method": T(
        f"Quellen sind die Höhenlisten der bewohnten Orte auf S. 11–13 (Unterland) und S. 20–22 (Oberland); die Überschriften nennen »Auf dem rechten/linken Ufer der Elster« bzw. »Die Höhe der bewohnten Punkte des Oberlandes«. Als Wohnpunkt zählt jeder Eintrag am linken Rand der Liste; eingerückte Einzelwerte darunter (Kirche, Dorfmitte, Ziegelei, Teich, Schloss u. Ä., {len(DETAILS)} Einträge) gehören zum Ort davor und wurden nicht gezählt. Die Einrückung geht im Digitalisat verloren; die Zuordnung folgt dem Faksimile und den Benennungen. Brückner gibt meist die Spanne vom untersten bis zum obersten Haus an (S. 11 Anm.); bei Einzelwerten ist Minimum = Maximum. Die Mitte ist das Mittel aus beiden. Höhen sind preußische Dezimalfuß (nicht Pariser Fuß!) auf den Pegel von Swinemünde bezogen; Umrechnung 1 Dezimalfuß = 0,3766242 m (siehe Umrechnungen). Die Spalte »Art« trennt Orte von Einzelstellen (Mühlen, Hämmer, Bahnhöfe, Einzelhäuser, Wirtshäuser u. Ä.) und ist eine redaktionelle Einordnung nach dem Namen. Die vier in Klammern gedruckten Einträge (Roschitz, Der goldne Hahn, St. Gangloff, Markersdorf) stehen in der Tabelle, sind aber aus Diagrammen und Zählungen ausgenommen; vermutlich liegen sie außerhalb des Fürstentums. Die Häufigkeitsverteilung (Diagramm 1) verwendet die Mitte der Spanne in Klassen von 25 m.",
        f"The sources are the altitude lists of the inhabited places on pp. 11–13 (Unterland) and pp. 20–22 (Oberland); the headings read “Auf dem rechten/linken Ufer der Elster” and “Die Höhe der bewohnten Punkte des Oberlandes”. Every entry at the left margin of the list counts as an inhabited point; indented single values below it (church, village centre, brickworks, pond, castle etc., {len(DETAILS)} entries) belong to the place before them and were not counted. The indentation is lost in the digitised text; the assignment follows the facsimile and the names. Brückner mostly gives the range from the lowest to the highest house (p. 11 note); for single values minimum = maximum. The midpoint is the mean of both. Heights are Prussian decimal feet (not Paris feet!) relative to the Swinemünde gauge; conversion 1 decimal foot = 0.3766242 m (see conversions). The column “Art” separates places from single sites (mills, hammers, railway stations, single houses, inns etc.) and is an editorial classification by name. The four entries printed in brackets (Roschitz, Der goldne Hahn, St. Gangloff, Markersdorf) are in the table but excluded from charts and counts; presumably they lie outside the principality. The frequency distribution (chart 1) uses the midpoint of the range in classes of 25 m."),
    "findings": [
        T(f"Das Unterland ist mit {nU} Wohnpunkten verzeichnet ({nR['Unterland, rechtes Elsterufer']} am rechten, {nR['Unterland, linkes Elsterufer']} am linken Elsterufer), das Oberland mit {nO} (dazu vier in Klammern gedruckte Punkte, die nicht mitgezählt sind); bei {n_range} von {nU + nO} steht eine Spanne.",
          f"The Unterland is listed with {nU} inhabited points ({nR['Unterland, rechtes Elsterufer']} on the right, {nR['Unterland, linkes Elsterufer']} on the left bank of the Elster), the Oberland with {nO} (plus four points printed in brackets, not counted); {n_range} of {nU + nO} have a range."),
        T(f"Der Median der Ortshöhen liegt im Unterland bei {f0(m(med_U))} m ({f0(med_U)}′), im Oberland bei {f0(m(med_O))} m ({f0(med_O)}′), also rund {f0(m(med_O - med_U))} m höher. Das Mittel der Oberland-Orte ({f0(mean_O)}′) liegt nahe bei Brückners »ca. 1340′« (S. 22); das der Unterland-Orte ({f0(mean_U)}′) unter seiner Terrassenhöhe von 730′ (S. 4).",
          f"The median altitude of places is {f0e(m(med_U))} m ({f0e(med_U)}′) in the Unterland and {f0e(m(med_O))} m ({f0e(med_O)}′) in the Oberland, i.e. about {f0e(m(med_O - med_U))} m higher. The mean of the Oberland places ({f0e(mean_O)}′) is close to Brückner's “ca. 1340′” (p. 22); that of the Unterland places ({f0e(mean_U)}′) lies below his terrace height of 730′ (p. 4)."),
        T(f"Im Unterland ist Caaschwitz (460–465′, {f0(m(460))}–{f0(m(465))} m) der tiefste, die Käseschenke ({f0(highU['hi'])}′, {f0(m(highU['hi']))} m) der höchste Ort; Unterschied {f0(diffU)}′ = {f0(diffU_m)} m, wie Brückner angibt (S. 11). Im Oberland sind Schloßmühle (Reichenfels) und Neue Mühle (Hohenleuben) mit 800′ ({f0(m(800))} m) die tiefsten, Karolinensfeld ({fmt(highO['hi'], 1)}′, {f0(m(highO['hi']))} m) der höchste Punkt.",
          f"In the Unterland Caaschwitz (460–465′, {f0e(m(460))}–{f0e(m(465))} m) is the lowest and the Käseschenke ({f0e(highU['hi'])}′, {f0e(m(highU['hi']))} m) the highest place; difference {f0e(diffU)}′ = {f0e(diffU_m)} m, as Brückner states (p. 11). In the Oberland the Schloßmühle (Reichenfels) and the Neue Mühle (Hohenleuben) at 800′ ({f0e(m(800))} m) are the lowest, Karolinensfeld ({fmt(highO['hi'], 1, 'en')}′, {f0e(m(highO['hi']))} m) the highest point."),
        T(f"Die beiden Höhenstufen überlappen nur schmal: {O_below_359} Oberland-Orte liegen (nach der Mitte) unter {f0(m(highU['hi']))} m, {U_above_301} Unterland-Orte über {f0(m(lowO['lo']))} m. Brückners Unterschied für das Oberland (»874′«, S. 22) passt nicht zu seinen Zahlen: {fmt(highO['hi'], 1)} − 800 = {fmt(d_ob, 1)}′; sein Durchschnitt »ca. 1340′« entspricht dagegen dem Mittel beider Extreme ({f0(mean_ext_O)}′).",
          f"The two altitude belts overlap only narrowly: {O_below_359} Oberland places lie (by midpoint) below {f0e(m(highU['hi']))} m, {U_above_301} Unterland places above {f0e(m(lowO['lo']))} m. Brückner's difference for the Oberland (“874′”, p. 22) does not fit his figures: {fmt(highO['hi'], 1, 'en')} − 800 = {fmt(d_ob, 1, 'en')}′; his average “ca. 1340′” does match the mean of both extremes ({f0e(mean_ext_O)}′)."),
        T(f"Zählt man nur Orte (ohne Bahnhöfe, Mühlen, Einzelhäuser) nach der unteren Grenze, ergibt sich für das Unterland außer Caaschwitz und Käseschenke {recount[0]}/{recount[1]}/{recount[2]}/{recount[3]}/{recount[4]} Orte unter 500/600/700/800/900′; Brückner nennt 6/23/23/28/5 (S. 11) – eine Abweichung um höchstens einen Ort. Innerhalb eines Ortes steigt das Gelände im Median um {f0(spreadU)}′ ({f0(m(spreadU))} m) im Unterland und {f0(spreadO)}′ ({f0(m(spreadO))} m) im Oberland an; die größte Spanne hat {maxspread['name']} ({f0(maxspread['lo'])}–{f0(maxspread['hi'])}′).",
          f"Counting only places (without railway stations, mills, single houses) by their lower limit gives for the Unterland, apart from Caaschwitz and the Käseschenke, {recount[0]}/{recount[1]}/{recount[2]}/{recount[3]}/{recount[4]} places below 500/600/700/800/900′; Brückner gives 6/23/23/28/5 (p. 11) – a deviation of at most one place. Within a place the ground rises by a median of {f0e(spreadU)}′ ({f0e(m(spreadU))} m) in the Unterland and {f0e(spreadO)}′ ({f0e(m(spreadO))} m) in the Oberland; the largest range is that of {maxspread['name']} ({f0e(maxspread['lo'])}–{f0e(maxspread['hi'])}′)."),
    ],
    "caveats": [
        T("Die Höhen sind preußische Dezimalfuß (Brückner S. 11 Anm.), nicht Pariser Fuß; das ist für alle Höhenangaben der Landeskunde wichtig. Die Umrechnung ist durch Brückners eigene Gegenproben gestützt (siehe Umrechnungen), die Bezugsfläche (Pegel Swinemünde) weicht von heutigem Normalhöhennull um höchstens wenige Meter ab (Annahme).",
          "The heights are Prussian decimal feet (Brückner p. 11 note), not Paris feet; this matters for all altitude figures in the Landeskunde. The conversion is supported by Brückner's own cross-checks (see conversions); the datum (Swinemünde gauge) differs from present-day mean sea level by at most a few metres (assumption)."),
        T("Die Spanne eines Ortes bezeichnet das unterste und oberste Haus (S. 11 Anm.); die hier verwendete Mitte ist nur eine Kennzahl, keine Ortshöhe im heutigen Sinn. Die Einordnung als Ort oder Einzelstelle und die Trennung von Haupt- und Untereinträgen sind redaktionell.",
          "A place's range denotes its lowest and highest house (p. 11 note); the midpoint used here is only a summary figure, not a place altitude in the modern sense. The classification as place or single site and the separation of main and sub-entries are editorial."),
        T(f"Brückners Zählung für das Oberland (»63 Wohnpunkte höher«, »74 unter« dem Durchschnitt von 1340′, zusammen 137, S. 22) lässt sich aus der Liste nicht nachvollziehen: sie enthält {nO} Einträge ({n_ob_ort} Orte), von denen {sum(1 for p in O if mid(p) > 1340)} über und {sum(1 for p in O if mid(p) < 1340)} unter 1340′ liegen.",
          f"Brückner's count for the Oberland (“63 inhabited points higher”, “74 lower” than the average of 1340′, 137 in total, p. 22) cannot be reproduced from the list: it contains {nO} entries ({n_ob_ort} places), of which {sum(1 for p in O if mid(p) > 1340)} lie above and {sum(1 for p in O if mid(p) < 1340)} below 1340′."),
        T("Gleichnamige Orte (zum Beispiel zwei Burkersdorf, zwei Göttengrün) erscheinen als getrennte Einträge. Die beiden Bahnhöfe Köstritz und Gera stammen aus dem Nivellement der Thüringer Eisenbahn (S. 12 Anm.).",
          "Places with the same name (for example two Burkersdorf, two Göttengrün) appear as separate entries. The two railway stations of Köstritz and Gera stem from the levelling of the Thuringian railway (p. 12 note)."),
    ],
    "conversions": conversions_height(),
    "datasets": [
        {"name": "places", "title": T("Bewohnte Punkte mit Höhenangabe", "Inhabited points with altitude"),
         "columns": [
             {"name": "nr", "label": T("Nr.", "No."), "type": "integer", "unit": None, "derived": True, "note": "Reihenfolge der Listen (Unterland rechts, links, Oberland)"},
             {"name": "name", "label": T("Ort (wie gedruckt)", "Place (as printed)"), "type": "string", "unit": None},
             {"name": "landesteil", "label": LB, "type": "string", "unit": None, "derived": True, "note": "aus der Überschrift der Liste"},
             {"name": "gruppe", "label": T("Liste", "List"), "type": "string", "unit": None, "derived": True},
             {"name": "art", "label": T("Art", "Kind"), "type": "string", "unit": None, "derived": True, "note": "redaktionell nach dem Namen"},
             {"name": "hoehe_min_fuss", "label": T("Höhe unten", "Altitude, lowest"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "hoehe_max_fuss", "label": T("Höhe oben", "Altitude, highest"), "type": "number", "unit": "preuß. Dezimalfuß", "note": "bei Einzelwerten gleich der unteren Höhe"},
             {"name": "hoehe_mitte_fuss", "label": T("Höhe, Mitte", "Altitude, midpoint"), "type": "number", "unit": "preuß. Dezimalfuß", "derived": True},
             {"name": "hoehe_min_m", "label": T("Höhe unten", "Altitude, lowest"), "type": "number", "unit": "m", "derived": True},
             {"name": "hoehe_max_m", "label": T("Höhe oben", "Altitude, highest"), "type": "number", "unit": "m", "derived": True},
             {"name": "hoehe_mitte_m", "label": T("Höhe, Mitte", "Altitude, midpoint"), "type": "number", "unit": "m", "derived": True},
             {"name": "rang", "label": T("Rang in der Höhe (im Landesteil)", "Rank by altitude (within the part)"), "type": "integer", "unit": None, "derived": True},
             {"name": "anteil_rang", "label": T("Anteil der Orte, die niedriger liegen", "Share of places lying lower"), "type": "number", "unit": "%", "derived": True, "note": "(Rang − 0,5) / Anzahl"},
             {"name": "spanne", "label": T("Spanne gedruckt (1 = ja)", "Range printed (1 = yes)"), "type": "integer", "unit": None, "derived": True},
             {"name": "in_klammern", "label": T("In Klammern gedruckt (1 = ja)", "Printed in brackets (1 = yes)"), "type": "integer", "unit": None, "derived": True},
             {"name": "seite", "label": T("Seite", "Page"), "type": "string", "unit": None},
             {"name": "zelle", "label": T("Zelle", "Cell"), "type": "string", "unit": None},
         ],
         "rows": rows,
         "source_refs": [{"page": "11", "block": "b13"}, {"page": "12", "block": "b1"}, {"page": "12", "block": "b3"}, {"page": "13", "block": "b1"},
                         {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}]},
        {"name": "classes", "title": T("Orte des Unterlandes nach Höhenklassen: Brückner und Nachzählung", "Places of the Unterland by altitude class: Brückner and recount"),
         "columns": [
             {"name": "klasse", "label": T("Höhenklasse", "Altitude class"), "type": "string", "unit": None},
             {"name": "obergrenze", "label": T("Obergrenze", "Upper limit"), "type": "integer", "unit": "preuß. Dezimalfuß"},
             {"name": "brueckner", "label": T("Anzahl nach Brückner (S. 11)", "Number according to Brückner (p. 11)"), "type": "integer", "unit": None},
             {"name": "nachzaehlung", "label": T("Anzahl nach der Liste (nur Orte, untere Grenze)", "Number from the list (places only, lower limit)"), "type": "integer", "unit": None, "derived": True},
         ],
         "rows": klass_rows, "source_refs": [{"page": "11", "block": "b11"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "places",
         "title": T("Wie hoch liegen die Wohnorte?", "How high do the inhabited places lie?"),
         "caption": T("Anzahl der Wohnpunkte je Höhenklasse von 25 m (Mitte der gedruckten Spanne), gestapelt nach Landesteil. Das Unterland liegt zwischen rund 170 und 360 m, das Oberland zwischen rund 300 und 710 m.",
                      "Number of inhabited points per altitude class of 25 m (midpoint of the printed range), stacked by part. The Unterland lies between about 170 and 360 m, the Oberland between about 300 and 710 m."),
         "vegalite": {
             "height": 280,
             "transform": [{"filter": "datum.in_klammern == 0"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "hoehe_mitte_m", "type": "quantitative", "bin": {"step": 25}, "title": T("Höhe (m)", "Altitude (m)")},
                 "y": {"aggregate": "count", "type": "quantitative", "title": T("Wohnpunkte", "Inhabited points")},
                 "color": COL,
                 "tooltip": [{"field": "landesteil", "title": LB},
                             {"field": "hoehe_mitte_m", "bin": {"step": 25}, "title": T("Höhenklasse (m)", "Altitude class (m)")},
                             {"aggregate": "count", "title": T("Wohnpunkte", "Inhabited points")}]}}},
        {"id": "c2", "dataset": "places",
         "title": T("Die Orte nach Höhe geordnet, mit der Höhenspanne jedes Ortes", "The places ordered by altitude, with the altitude range of each place"),
         "caption": T("Jeder senkrechte Strich ist ein Wohnpunkt: von der untersten bis zur obersten Höhe (m), geordnet nach der Mitte; waagerecht der Anteil der Orte, die niedriger liegen. Die beiden Landesteile sind fast getrennte Höhenstufen.",
                      "Each vertical stroke is an inhabited point: from its lowest to its highest altitude (m), ordered by midpoint; horizontally the share of places lying lower. The two parts form almost separate altitude belts."),
         "vegalite": {
             "height": 340,
             "transform": [{"filter": "datum.in_klammern == 0"}],
             "layer": [
                 {"mark": {"type": "bar", "width": 3, "cornerRadiusEnd": 0},
                  "encoding": {
                      "x": {"field": "anteil_rang", "type": "quantitative", "title": T("Anteil der Orte, die niedriger liegen (%)", "Share of places lying lower (%)"), "scale": {"domain": [0, 100]}},
                      "y": {"field": "hoehe_min_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"domain": [150, 750]}},
                      "y2": {"field": "hoehe_max_m"},
                      "color": COL,
                      "tooltip": [{"field": "name", "title": T("Ort", "Place")},
                                  {"field": "landesteil", "title": LB},
                                  {"field": "hoehe_min_fuss", "title": T("unten (Dezimalfuß)", "lowest (dec. feet)")},
                                  {"field": "hoehe_max_fuss", "title": T("oben (Dezimalfuß)", "highest (dec. feet)")},
                                  {"field": "hoehe_min_m", "title": T("unten (m)", "lowest (m)")},
                                  {"field": "hoehe_max_m", "title": T("oben (m)", "highest (m)")}]}},
                 {"mark": {"type": "point", "filled": True, "size": 22, "strokeWidth": 0},
                  "encoding": {
                      "x": {"field": "anteil_rang", "type": "quantitative", "scale": {"domain": [0, 100]}},
                      "y": {"field": "hoehe_mitte_m", "type": "quantitative", "scale": {"domain": [150, 750]}},
                      "color": COL}},
             ]}},
        {"id": "c3", "dataset": "classes",
         "title": T("Gegenprobe: Brückners Höhenklassen im Unterland", "Cross-check: Brückner's altitude classes in the Unterland"),
         "caption": T("Balken: Anzahl der Orte nach Brückner (S. 11), ohne Caaschwitz und Käseschenke. Punkte: Nachzählung aus der Liste (nur Orte, nach der unteren Grenze). Beide stimmen bis auf einen Ort überein.",
                      "Bars: number of places according to Brückner (p. 11), excluding Caaschwitz and the Käseschenke. Dots: recount from the list (places only, by lower limit). Both agree except for one place."),
         "vegalite": {
             "height": 220,
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "x": {"field": "klasse", "type": "ordinal", "sort": {"field": "obergrenze", "op": "min"}, "title": T("Höhenklasse (preußische Dezimalfuß)", "Altitude class (Prussian decimal feet)"), "axis": {"labelAngle": 0}},
                      "y": {"field": "brueckner", "type": "quantitative", "title": T("Anzahl Orte", "Number of places")},
                      "color": {"datum": "Unterland", "type": "nominal", "scale": {"domain": ["Oberland", "Unterland"]}, "legend": None},
                      "tooltip": [{"field": "klasse", "title": T("Höhenklasse", "Altitude class")},
                                  {"field": "brueckner", "title": T("nach Brückner", "according to Brückner")},
                                  {"field": "nachzaehlung", "title": T("Nachzählung", "recount")}]}},
                 {"mark": {"type": "point", "filled": True, "size": 90, "shape": "diamond"},
                  "encoding": {
                      "x": {"field": "klasse", "type": "ordinal", "sort": {"field": "obergrenze", "op": "min"}},
                      "y": {"field": "nachzaehlung", "type": "quantitative"}}},
             ]}},
    ],
    "transcription_issues": [
        {"page": "20", "block": "b3", "cell": "r12c1", "transcribed": "Törbizmühle a. d. Weida 920'", "facsimile": "Sörbitzmühle a. d. Weida 920'", "checked_facsimile": True, "note": "Name; Zahl stimmt. Im Datensatz nach dem Faksimile korrigiert."},
    ],
    "keywords": T(["Höhenlage", "Meereshöhe", "Wohnorte", "bewohnte Orte", "Oberland", "Unterland", "Elster", "Dezimalfuß", "Höhenangaben", "Höhenstufen", "Gera", "Tanna", "Schleiz", "Karolinensfeld"],
                  ["altitude", "elevation", "inhabited places", "settlements", "Oberland", "Unterland", "Elster", "decimal foot", "altitude belts", "Gera", "Tanna", "Schleiz"]),
    "related": ["relief-hoehenstufen-oberland-unterland", "relief-hoehe-und-lage-neigung", "relief-erhebungen-hoechste-punkte"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
