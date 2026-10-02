"""Part 2: analysis dict for relief-erhebungen-hoechste-punkte."""
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from build_erhebungen import *     # noqa: F401,F403

KB = KIND_LABEL["berg"]
medU_diff = medU_h - medU_p
medO_diff = medO_h - medO_p
kar = max(p["hi"] for p in PLACES if p["landesteil"] == "Oberland" and not p["bracket"])
kas = max(p["hi"] for p in PLACES if p["landesteil"] == "Unterland" and not p["bracket"])
fich = topO[0]
top5O = ", ".join(f"{short(s['name'])} {f0(s['h'])}′" for s in topO[:5])
top3U = ", ".join(f"{short(s['name'])} {f0(s['h'])}′" for s in topU[:3])
top5O_m = ", ".join(f"{short(s['name'])} {f0(m(s['h']))} m" for s in topO[:5])


def dotspec(landesteil, domain_max):
    return {
        "height": 400,
        "transform": [
            {"filter": f"datum.landesteil == '{landesteil}' && datum.art == '{KB}' && datum.in_klammern == 0"},
            {"window": [{"op": "row_number", "as": "r"}], "sort": [{"field": "hoehe_fuss", "order": "descending"}]},
            {"filter": "datum.r <= 15"},
            {"calculate": "format(datum.hoehe_fuss, '.0f') + '′ · ' + format(datum.hoehe_m, '.0f') + ' m'", "as": "beschriftung"},
        ],
        "layer": [
            {"mark": "bar",
             "encoding": {
                 "y": {"field": "kurzname", "type": "nominal", "sort": {"field": "hoehe_fuss", "op": "max", "order": "descending"}, "title": None, "axis": {"labelLimit": 420}},
                 "x": {"field": "hoehe_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"domain": [0, domain_max]}},
                 "color": {"datum": landesteil, "type": "nominal", "scale": {"domain": ["Oberland", "Unterland"]}, "legend": None},
                 "tooltip": [{"field": "name", "title": T("Bezeichnung (wie gedruckt)", "Designation (as printed)")},
                             {"field": "hoehe_fuss", "title": T("Dezimalfuß", "Decimal feet")},
                             {"field": "hoehe_m", "title": T("Meter", "Metres")},
                             {"field": "seite", "title": T("Seite", "Page")}]}},
            {"mark": {"type": "text", "align": "left", "dx": 5, "baseline": "middle", "fontSize": 11},
             "encoding": {
                 "y": {"field": "kurzname", "type": "nominal", "sort": {"field": "hoehe_fuss", "op": "max", "order": "descending"}},
                 "x": {"field": "hoehe_m", "type": "quantitative"},
                 "text": {"field": "beschriftung", "type": "nominal"}}},
        ]}


ana = {
    "id": "relief-erhebungen-hoechste-punkte",
    "title": T("Berge und Höhenpunkte: die höchsten Erhebungen von Ober- und Unterland", "Mountains and height points: the highest elevations of the Oberland and Unterland"),
    "category": "relief",
    "section": "t1-1-4",
    "sources": [
        {"page": "10", "block": "b3"},
        {"page": "13", "block": "b3"}, {"page": "14", "block": "b1"}, {"page": "14", "block": "b2"}, {"page": "15", "block": "b1"},
        {"page": "17", "block": "b1"},
        {"page": "22", "block": "b4"}, {"page": "22", "block": "b2"}, {"page": "23", "block": "b1"}, {"page": "24", "block": "b1"},
        {"page": "11", "block": "fn1"}, {"page": "831", "block": "b8"},
    ],
    "summary": T(
        f"Neben den Wohnorten listet Brückner {nU + nO} »Höhenpunkte« und »Berghöhen« in aufsteigender Folge auf – für das Unterland (S. 13–15) und das Oberland (S. 22–24): benannte Berge, Höhen nach Himmelsrichtung (»Nordhöhe von …«) und einzelne Bauwerke. Umgerechnet erreicht das Unterland höchstens {f0(m(extremeU['h']))} m (Scheidberg), das Oberland {f0(m(extremeO['h']))} m (Fichteberg im Frankenwald). Die Auswertung zeigt die höchsten benannten Erhebungen und wie hoch die Berge über den Orten liegen.",
        f"Besides the inhabited places Brückner lists {nU + nO} “height points” and “mountain heights” in ascending order – for the Unterland (pp. 13–15) and the Oberland (pp. 22–24): named mountains, heights by compass direction (“Nordhöhe von …”) and single structures. Converted, the Unterland reaches at most {f0e(m(extremeU['h']))} m (Scheidberg), the Oberland {f0e(m(extremeO['h']))} m (Fichteberg in the Frankenwald). The analysis shows the highest named elevations and how far the mountains rise above the places."),
    "method": T(
        "Quellen sind die Liste »Höhenpunkte des Unterlandes« (S. 13 unten bis S. 15; auf S. 14 als Fließtext, auf S. 15 als kleine Tabelle gesetzt) und »Die Berghöhen des Oberlandes« (S. 22–24). Jede Zeile besteht aus einer Bezeichnung und einer Höhe in preußischen Dezimalfuß (nicht Pariser Fuß; 1 Dezimalfuß = 0,3766242 m, siehe Umrechnungen); durch Zeilenumbrüche getrennte Einträge wurden wieder zusammengesetzt, Silbentrennungen aufgelöst. Die Spalte »Art« ist eine redaktionelle Einordnung nach der Bezeichnung: »Berg, Hügel (benannt)« (Eigenname wie Fichteberg, Galgenberg), »Höhenpunkt (nach Himmelsrichtung)« (z. B. Südwesthöhe von Neundorf) und »Bauwerk, Straße, Quelle u. Ä.« (Windmühle, Ziegelei, Chaussee). Der Eintrag »Signal 1008′« unter Lerchenhügel bei Triebes (S. 22) ist ein Untereintrag und fehlt; der eingeklammerte »Bahnhof Reuth« bleibt in der Tabelle, aber außerhalb der Auswertungen. Die Listen sind nach der Höhe geordnet; die Ordnung diente als Plausibilitätsprüfung der Zahlen (keine Abweichung außer dem Signal-Eintrag). Das Diagramm 3 stellt die Höhen dieser Listen den Mitten der Ortsspannen (Analyse »Höhenlage der Wohnorte«) gegenüber.",
        "Sources are the list “Höhenpunkte des Unterlandes” (p. 13 bottom to p. 15; set as running text on p. 14 and as a small table on p. 15) and “Die Berghöhen des Oberlandes” (pp. 22–24). Each line consists of a designation and an altitude in Prussian decimal feet (not Paris feet; 1 decimal foot = 0.3766242 m, see conversions); entries split by line breaks were rejoined and hyphenations resolved. The column “Art” is an editorial classification by designation: “Berg, Hügel (benannt)” (proper name such as Fichteberg, Galgenberg), “Höhenpunkt (nach Himmelsrichtung)” (e.g. Südwesthöhe von Neundorf) and “Bauwerk, Straße, Quelle u. Ä.” (windmill, brickworks, road). The entry “Signal 1008′” under Lerchenhügel bei Triebes (p. 22) is a sub-entry and is left out; the bracketed “Bahnhof Reuth” stays in the table but outside the analyses. The lists are ordered by altitude; the order served as a plausibility check of the numbers (no deviation except the signal entry). Chart 3 compares the altitudes of these lists with the midpoints of the place ranges (analysis “Altitude of the inhabited places”)."),
    "findings": [
        T(f"Das Unterland ist mit {nU}, das Oberland mit {nO} Höhenpunkten vertreten. Im Unterland sind {cnt['Unterland']['berg']} benannte Berge, {cnt['Unterland']['richtungshoehe']} Himmelsrichtungs-Höhen und {cnt['Unterland']['bauwerk']} Bauwerke o. Ä.; im Oberland {cnt['Oberland']['berg']}, {cnt['Oberland']['richtungshoehe']} und {cnt['Oberland']['bauwerk'] - 1} (ohne den eingeklammerten Bahnhof).",
          f"The Unterland is represented by {nU}, the Oberland by {nO} height points. In the Unterland {cnt['Unterland']['berg']} are named mountains, {cnt['Unterland']['richtungshoehe']} are compass-direction heights and {cnt['Unterland']['bauwerk']} are structures or similar; in the Oberland {cnt['Oberland']['berg']}, {cnt['Oberland']['richtungshoehe']} and {cnt['Oberland']['bauwerk'] - 1} (without the bracketed railway station)."),
        T(f"Höchste Erhebungen des Oberlandes sind {top5O} ({top5O_m}). Sechs der sieben höchsten benannten Erhebungen (Fichteberg, Kulm, Hohe Tanne, Sieglitzberg, Finkenberg, Oßlahügel) stehen in Brückners Aufzählung der Berge des Frankenwaldes (S. 17). Im Unterland führen {top3U}.",
          f"The highest elevations of the Oberland are {top5O} ({top5O_m}). Six of the seven highest named elevations (Fichteberg, Kulm, Hohe Tanne, Sieglitzberg, Finkenberg, Oßlahügel) appear in Brückner's enumeration of the mountains of the Frankenwald (p. 17). In the Unterland the highest are {top3U}."),
        T(f"Nur je sechs Höhenpunkte liegen über dem höchsten bewohnten Ort ({fmt(kar, 1)}′ Karolinensfeld im Oberland, {f0(kas)}′ Käseschenke im Unterland); der Fichteberg überragt Karolinensfeld um {f0(fich['h'] - kar)}′ ({f0(m(fich['h'] - kar))} m). Die bewohnte Fläche reicht fast bis zu den Gipfeln.",
          f"Only six height points each lie above the highest inhabited place (Karolinensfeld, {fmt(kar, 1, 'en')}′, in the Oberland; Käseschenke, {f0e(kas)}′, in the Unterland); the Fichteberg exceeds Karolinensfeld by {f0e(fich['h'] - kar)}′ ({f0e(m(fich['h'] - kar))} m). The inhabited area reaches almost to the summits."),
        T(f"Der mittlere Höhenpunkt liegt im Unterland bei {f0(medU_h)}′ ({f0(m(medU_h))} m), im Oberland bei {f0(medO_h)}′ ({f0(m(medO_h))} m) – nur {f0(medU_diff)}′ ({f0(m(medU_diff))} m) bzw. {f0(medO_diff)}′ ({f0(m(medO_diff))} m) über dem mittleren Wohnort. Das passt zu Brückners Bemerkung, das Land sei an Bergnamen reicher als an wirklichen Bergen, weil schon Anhöhen und niedrige Buckel Berg hießen (S. 10).",
          f"The median height point lies at {f0e(medU_h)}′ ({f0e(m(medU_h))} m) in the Unterland and {f0e(medO_h)}′ ({f0e(m(medO_h))} m) in the Oberland – only {f0e(medU_diff)}′ ({f0e(m(medU_diff))} m) and {f0e(medO_diff)}′ ({f0e(m(medO_diff))} m) above the median inhabited place. This fits Brückner's remark that the country is richer in mountain names than in real mountains because even rises and low humps are called mountains (p. 10)."),
    ],
    "caveats": [
        T("Die Listen sind eine Auswahl Brückners (meist Höhen, die für die Karte trigonometrisch bestimmt wurden), keine systematische Erfassung der Erhebungen; die Verteilung der Höhenpunkte spiegelt die Messpunkte, nicht das Relief. Höhere Gipfel können fehlen.",
          "The lists are a selection by Brückner (mostly heights determined trigonometrically for the map), not a systematic survey of elevations; the distribution of height points reflects the measuring points, not the relief. Higher summits may be missing."),
        T("Die Höhen sind preußische Dezimalfuß, nicht Pariser Fuß (siehe Umrechnungen). Einige Zahlen stehen mit Zehntelfuß (z. B. 1183,2′), die Genauigkeit der Listen liegt aber eher bei ganzen Fuß.",
          "The heights are Prussian decimal feet, not Paris feet (see conversions). Some numbers carry tenths of a foot (e.g. 1183.2′), but the accuracy of the lists is rather whole feet."),
        T("Die Einteilung in Berg, Himmelsrichtungs-Höhe und Bauwerk ist redaktionell; Brückner trennt die Typen nicht. Dubletten wie »Kulm« (1913′, Frankenwald) und »Kulm bei Kulm« (1522′) sind verschiedene Punkte.",
          "The division into mountain, compass-direction height and structure is editorial; Brückner does not separate the types. Duplicates such as “Kulm” (1913′, Frankenwald) and “Kulm bei Kulm” (1522′) are different points."),
        T("Auf S. 22 steht unter »Lerchenhügel bei Triebes 1091′« ein Untereintrag »Signal 1008′«, der niedriger ist als der Hügel selbst; er ist wie gedruckt zu lesen und hier nicht gezählt (möglicher Druckfehler, nicht geprüft).",
          "On p. 22 a sub-entry “Signal 1008′” appears under “Lerchenhügel bei Triebes 1091′” that is lower than the hill itself; it is to be read as printed and is not counted here (possible printing error, not checked)."),
    ],
    "conversions": conversions_height(),
    "datasets": [
        {"name": "heights", "title": T("Höhenpunkte und Berghöhen", "Height points and mountain heights"),
         "columns": [
             {"name": "nr", "label": T("Nr.", "No."), "type": "integer", "unit": None, "derived": True, "note": "Reihenfolge der Listen"},
             {"name": "name", "label": T("Bezeichnung (wie gedruckt)", "Designation (as printed)"), "type": "string", "unit": None},
             {"name": "kurzname", "label": T("Kurzbezeichnung", "Short designation"), "type": "string", "unit": None, "derived": True},
             {"name": "landesteil", "label": LB, "type": "string", "unit": None, "derived": True, "note": "aus der Überschrift der Liste"},
             {"name": "art", "label": T("Art", "Kind"), "type": "string", "unit": None, "derived": True, "note": "redaktionell nach der Bezeichnung"},
             {"name": "hoehe_fuss", "label": T("Höhe", "Altitude"), "type": "number", "unit": "preuß. Dezimalfuß"},
             {"name": "hoehe_m", "label": T("Höhe", "Altitude"), "type": "number", "unit": "m", "derived": True},
             {"name": "in_klammern", "label": T("In Klammern gedruckt (1 = ja)", "Printed in brackets (1 = yes)"), "type": "integer", "unit": None, "derived": True},
             {"name": "seite", "label": T("Seite", "Page"), "type": "string", "unit": None},
             {"name": "zelle", "label": T("Zelle / Zeile", "Cell / line"), "type": "string", "unit": None},
         ],
         "rows": rows,
         "source_refs": [{"page": "13", "block": "b3"}, {"page": "14", "block": "b1"}, {"page": "14", "block": "b2"}, {"page": "15", "block": "b1"},
                         {"page": "22", "block": "b4"}, {"page": "23", "block": "b1"}, {"page": "24", "block": "b1"}]},
        {"name": "compare", "title": T("Wohnorte und Erhebungen: Höhen im Vergleich", "Places and elevations: altitudes compared"),
         "columns": [
             {"name": "gruppe", "label": T("Gruppe", "Group"), "type": "string", "unit": None, "derived": True},
             {"name": "gruppe_nr", "label": T("Reihenfolge der Gruppen", "Order of groups"), "type": "integer", "unit": None, "derived": True},
             {"name": "landesteil", "label": LB, "type": "string", "unit": None, "derived": True},
             {"name": "art", "label": T("Art", "Kind"), "type": "string", "unit": None, "derived": True},
             {"name": "bezeichnung", "label": T("Bezeichnung", "Designation"), "type": "string", "unit": None},
             {"name": "hoehe_m", "label": T("Höhe (Orte: Mitte der Spanne)", "Altitude (places: midpoint of range)"), "type": "number", "unit": "m", "derived": True},
         ],
         "rows": cmp_rows,
         "source_refs": [{"page": "11", "block": "b13"}, {"page": "12", "block": "b1"}, {"page": "12", "block": "b3"}, {"page": "13", "block": "b1"},
                         {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "heights",
         "title": T("Die 15 höchsten benannten Erhebungen des Oberlandes", "The 15 highest named elevations of the Oberland"),
         "caption": T("Höhe in Metern (aus preußischen Dezimalfuß); Beschriftung: Dezimalfuß · Meter. Die höchsten Berge stehen im Frankenwald an der Südgrenze des Landes.",
                      "Altitude in metres (from Prussian decimal feet); label: decimal feet · metres. The highest mountains are in the Frankenwald on the southern border of the country."),
         "vegalite": dotspec("Oberland", 900)},
        {"id": "c2", "dataset": "heights",
         "title": T("Die 15 höchsten benannten Erhebungen des Unterlandes", "The 15 highest named elevations of the Unterland"),
         "caption": T("Höhe in Metern; Beschriftung: Dezimalfuß · Meter. Die höchsten Punkte liegen im Westen des Unterlandes bei Hundhaupten und Kraftsdorf.",
                      "Altitude in metres; label: decimal feet · metres. The highest points lie in the west of the Unterland near Hundhaupten and Kraftsdorf."),
         "vegalite": dotspec("Unterland", 470)},
        {"id": "c3", "dataset": "compare",
         "title": T("Wohnorte und Erhebungen: wie hoch ragen die Berge über die Orte?", "Places and elevations: how far do the mountains rise above the places?"),
         "caption": T("Verteilung der Höhen (m): Kasten = mittlere Hälfte, Strich = Median, Linien = Minimum und Maximum. Orte: Mitte der gedruckten Spanne. Die Höhenpunkte liegen im Mittel nur wenig über den Orten.",
                      "Distribution of altitudes (m): box = middle half, line = median, whiskers = minimum and maximum. Places: midpoint of the printed range. The height points lie on average only a little above the places."),
         "vegalite": {
             "height": 320,
             "mark": {"type": "boxplot", "extent": "min-max"},
             "encoding": {
                 "x": {"field": "gruppe", "type": "nominal", "sort": {"field": "gruppe_nr", "op": "min"}, "title": None, "axis": {"labelAngle": 0, "labelLimit": 240}},
                 "y": {"field": "hoehe_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"zero": False}},
                 "color": {**COL, "legend": None}}}},
    ],
    "transcription_issues": [
        {"page": "14", "block": "b1", "cell": "l2", "transcribed": "Südwesthöhe von Rusitz nach Frankenthal 768'", "facsimile": "Südwesthöhe von Rubitz nach Frankenthal 768'", "checked_facsimile": True, "note": "Ortsname; Zahl stimmt. Im Datensatz nach dem Faksimile korrigiert."},
        {"page": "24", "block": "b1", "cell": "r5c1", "transcribed": "Tummelplatz bei Kießling 1600'", "facsimile": "Tummelsplatz bei Kießling 1600'", "checked_facsimile": True, "note": "Name; Zahl stimmt. Im Datensatz nach dem Faksimile korrigiert."},
    ],
    "keywords": T(["Berge", "Erhebungen", "Höhenpunkte", "Berghöhen", "Fichteberg", "Kulm", "Sieglitzberg", "Hohe Tanne", "Scheidberg", "Frankenwald", "höchster Punkt", "Dezimalfuß"],
                  ["mountains", "elevations", "height points", "Fichteberg", "Kulm", "Frankenwald", "highest point", "decimal foot"]),
    "related": ["relief-hoehenstufen-oberland-unterland", "relief-wohnorte-hoehenlage", "relief-bergnamen"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
