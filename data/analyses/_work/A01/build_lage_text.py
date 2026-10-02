"""Part 2 of the build for lage-vermessene-punkte-laenge-breite: texts, datasets, charts."""
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from build_lage import *   # noqa: F401,F403  (computes all numbers)

el1, el2 = [p for p in P if p["name"] == "Eliasbrunn"]
dy = (el2["lat_dec"] - el1["lat_dec"]) * 111.2
dx = (el2["lon_dec"] - el1["lon_dec"]) * 111.32 * math.cos(math.radians(el1["lat_dec"]))
eli_km = math.hypot(dx, dy)
FERRO_PRECISE = 17 + 39 / 60 + 46 / 3600
ferro_diff_km = (FERRO - FERRO_PRECISE) * 70.5


def lonlat_gw(p):
    return f"{fmt_dms(p['lon_gw'])} / {fmt_dms(p['lat_dec'])}"


T = lambda de, en: {"de": de, "en": en}
LB = T("Landesteil", "Part of the country")
CHART_COLOR = {"field": "landesteil", "type": "nominal", "title": LB,
               "scale": {"domain": ["Oberland", "Unterland"]}}

ana = {
    "id": "lage-vermessene-punkte-laenge-breite",
    "title": T("Mathematische Lage: vermessene Punkte und Ausdehnung des Landes",
               "Mathematical position: surveyed points and extent of the country"),
    "category": "geography",
    "section": "t1-1-2",
    "sources": [
        {"page": "6", "block": "b2"}, {"page": "6", "block": "b3", "rows": "r1-r37"}, {"page": "6", "block": "fn1"},
        {"page": "7", "block": "b1", "rows": "r1-r20"}, {"page": "7", "block": "b2"},
        {"page": "4", "block": "b3"}, {"page": "5", "block": "b1"}, {"page": "5", "block": "b2"},
    ],
    "summary": T(
        f"Brückner druckt die geographische Länge und Breite von {n_all} trigonometrisch bestimmten Punkten im Fürstentum (Kirchen, Turmknöpfe, Signale, Mühlen), dazu die Grenzwerte von Ober- und Unterland. Die Längen sind von Ferro aus gezählt; mit Abzug von 17° 40′ ergeben sich Greenwich-Längen, so dass die Punkte auf einer Karte dargestellt werden können. Die Karte zeigt zwei getrennte Punktwolken: das große, nach Südwesten ausgreifende Oberland und das kleinere Unterland um Gera.",
        f"Brückner prints the geographic longitude and latitude of {n_all} points of the principality fixed by triangulation (churches, tower finials, signals, mills), together with the limits of the Oberland and Unterland. Longitudes are counted from Ferro; subtracting 17° 40′ gives Greenwich longitudes, so the points can be drawn on a map. The map shows two separate clouds of points: the large Oberland, reaching to the south-west, and the smaller Unterland around Gera."),
    "method": T(
        f"Quelle sind die Tabellen auf S. 6 (Punkte 1–37) und S. 7 (Punkte 38–57) sowie die Grenzwerte auf S. 6 (über der Tabelle), die im Fließtext S. 4–5 als Anfangswert plus Ausdehnung wiederholt werden. Grad, Minuten und Sekunden wurden wie gedruckt übernommen und in Dezimalgrad umgerechnet. Brückner zählt die Länge östlich von Ferro (»L.«); Greenwich-Länge = Ferro-Länge − 17° 40′ (Ferro liegt genauer 17° 39′ 46″ westlich von Greenwich; der Unterschied von 14″ entspricht rund {fmt(ferro_diff_km, 1)} km). Die Breite wird übernommen. Die Zuordnung zu Ober- oder Unterland folgt der gedruckten Südgrenze des Unterlandes (Breite ≥ 50° 47′ 48″); Geissen wird abweichend dem Unterland zugerechnet, weil es in den Höhenlisten des Unterlandes (S. 13) steht. Die gestrichelten Rechtecke der Karte sind die gedruckten Grenzwerte (Länge/Breite) beider Landesteile, keine Landesgrenzen. Kilometerangaben sind Näherungen (1° Breite = 111,2 km; 1° Länge = 111,32 km · cos Breite). Drei im Digitalisat falsch gelesene Sekundenwerte wurden nach dem Faksimile korrigiert.",
        f"The sources are the tables on p. 6 (points 1–37) and p. 7 (points 38–57) and the limits printed on p. 6 above the table, which the running text on pp. 4–5 repeats as a starting value plus an extent. Degrees, minutes and seconds were taken as printed and converted to decimal degrees. Brückner counts longitude east of Ferro (“L.”); Greenwich longitude = Ferro longitude − 17° 40′ (more precisely Ferro lies 17° 39′ 46″ west of Greenwich; the 14″ difference is about {fmt(ferro_diff_km, 1, 'en')} km). Latitude is used as printed. Assignment to Oberland or Unterland follows the printed southern limit of the Unterland (latitude ≥ 50° 47′ 48″); Geissen is assigned to the Unterland against this rule because the Unterland height lists (p. 13) include it. The dashed rectangles on the map are the printed longitude/latitude limits of the two parts, not borders. Kilometre figures are approximations (1° latitude = 111.2 km; 1° longitude = 111.32 km · cos latitude). Three seconds values misread in the digitised text were corrected from the facsimile."),
    "findings": [
        T(f"Die Tabelle enthält {n_all} Punkte ({by_lt['Oberland']} im Oberland, {by_lt['Unterland']} im Unterland); {n_map} haben Länge und Breite (Kleinfriesa nur die Länge). {n_tower} Punkte sind Kirchen, Turmknöpfe, Türme oder Schlösser, {cls_count['Signalpunkt/-stein']} Signalpunkte oder -steine.",
          f"The table lists {n_all} points ({by_lt['Oberland']} in the Oberland, {by_lt['Unterland']} in the Unterland); {n_map} have longitude and latitude (Kleinfriesa only longitude). {n_tower} points are churches, tower finials, towers or castles, {cls_count['Signalpunkt/-stein']} are signal points or stones."),
        T(f"Westlichster Punkt ist {west['name']} ({fmt_dms(west['lon_gw'])} östlich von Greenwich), östlichster {east['name']} ({fmt_dms(east['lon_gw'])}), südlichster {south['name']} ({fmt_dms(south['lat_dec'])} N), nördlichster {north['name']} ({fmt_dms(north['lat_dec'])} N) – wie Brückner auf S. 7 schreibt. Das eingeklammerte {north_all['name']} liegt mit {fmt_dms(north_all['lat_dec'], 2)} N noch etwas nördlicher und gehört vermutlich nicht zum Fürstentum.",
          f"The westernmost point is {west['name']} ({fmt_dms(west['lon_gw'])} east of Greenwich), the easternmost {east['name']} ({fmt_dms(east['lon_gw'])}), the southernmost {south['name']} ({fmt_dms(south['lat_dec'])} N), the northernmost {north['name']} ({fmt_dms(north['lat_dec'])} N), as Brückner states on p. 7. The bracketed {north_all['name']} lies slightly further north at {fmt_dms(north_all['lat_dec'], 2)} N and probably is not part of the principality."),
        T(f"Gera (Nikolaiturm) liegt bei {lonlat_gw(gera)} (Greenwich-Länge / Breite), Schleiz (Schloss) bei {lonlat_gw(schleiz)}, Tanna (Mühle) bei {lonlat_gw(tanna)}. Brückners »dicht bei Tanna« gelegener Schnittpunkt von 29° 30′ Länge und 50° 30′ Breite entspricht 11° 50′ O, 50° 30′ N.",
          f"Gera (St. Nicholas tower) lies at {lonlat_gw(gera)} (Greenwich longitude / latitude), Schleiz (castle) at {lonlat_gw(schleiz)}, Tanna (mill) at {lonlat_gw(tanna)}. Brückner's intersection of 29° 30′ longitude and 50° 30′ latitude “close to Tanna” corresponds to 11° 50′ E, 50° 30′ N."),
        T(f"Nach den gedruckten Grenzwerten füllt das Oberland ein Rechteck von rund {fmt(EXT['Oberland']['w_km'], 1)} km (Ost–West) × {fmt(EXT['Oberland']['h_km'], 1)} km (Nord–Süd), das Unterland eines von rund {fmt(EXT['Unterland']['w_km'], 1)} × {fmt(EXT['Unterland']['h_km'], 1)} km; zwischen beiden liegt ein Breitenstreifen von 3′ 58″ (≈ {fmt(gap_km, 1)} km). Alle Punkte außer Geissen liegen innerhalb der Rechtecke ihres Landesteils.",
          f"According to the printed limits the Oberland fills a rectangle of about {fmt(EXT['Oberland']['w_km'], 1, 'en')} km (east–west) × {fmt(EXT['Oberland']['h_km'], 1, 'en')} km (north–south), the Unterland one of about {fmt(EXT['Unterland']['w_km'], 1, 'en')} × {fmt(EXT['Unterland']['h_km'], 1, 'en')} km; between them lies a latitude gap of 3′ 58″ (≈ {fmt(gap_km, 1, 'en')} km). All points except Geissen lie within the rectangle of their part."),
    ],
    "caveats": [
        T("Geissen (Br. 50° 45′ 44″) liegt südlich der gedruckten Südgrenze des Unterlandes (50° 47′ 48″), obwohl der Ort zu den Unterland-Orten gehört (S. 13). Das Faksimile zeigt den Wert wie transkribiert; vermutlich liegt ein Druckfehler im Original vor (nicht anderweitig geprüft). Der Punkt ist wie gedruckt eingetragen.",
          "Geissen (lat. 50° 45′ 44″) lies south of the printed southern limit of the Unterland (50° 47′ 48″), although the village belongs to the Unterland places (p. 13). The facsimile shows the value as transcribed; probably a printing error in the original (not checked elsewhere). The point is plotted as printed."),
        T(f"Gemessen wurde nicht überall derselbe Gegenstand (Kirche, Turmknopf, Signal, Mühle, Schornstein, einzelner Baum); Eliasbrunn erscheint zweimal (Signalpunkt und Turmknopf), die beiden Positionen liegen rund {fmt(eli_km, 2)} km auseinander. Die Angabe von Hundertstel-Sekunden täuscht eine Genauigkeit vor, die die Methode nicht hatte. Brückner nennt kein geodätisches Datum; gegenüber heutigen Koordinaten sind Abweichungen von einigen hundert Metern möglich.",
          f"Not the same kind of object was measured everywhere (church, tower finial, signal, mill, chimney, single tree); Eliasbrunn appears twice (signal point and tower finial), the two positions being about {fmt(eli_km, 2, 'en')} km apart. Hundredths of seconds imply a precision the method did not have. Brückner names no geodetic datum; deviations of a few hundred metres from present-day coordinates are possible."),
        T("Die Klammern um St. Gangloff und Heukenwalde erklärt Brückner nicht; die Auslegung als »außerhalb des Fürstentums« ist eine Vermutung (beide Orte dürften damals im Herzogtum Sachsen-Altenburg gelegen haben; nicht geprüft).",
          "Brückner does not explain the brackets around St. Gangloff and Heukenwalde; reading them as “outside the principality” is a conjecture (both places were probably in the Duchy of Saxe-Altenburg at the time; not checked)."),
        T("Die Randwerte auf S. 4 sind im Digitalisat falsch gelesen (»bis 30° 7′ 40″«); der Druck gibt »um 40′ 20″« und stimmt damit mit S. 6 überein.",
          "The limits on p. 4 are misread in the digitised text (“bis 30° 7′ 40″”); the print says “um 40′ 20″” and thus agrees with p. 6."),
    ],
    "conversions": [
        {"from": "Länge östlich von Ferro", "to": "Länge östlich von Greenwich",
         "factor_or_formula": "L_Greenwich = L_Ferro − 17° 40′ (= 17,6667°)",
         "reference": "Ferro = 20° westlich von Paris; Paris = 2° 20′ 14″ östlich von Greenwich, daher genau 17° 39′ 46″; gerundet 17° 40′"},
        {"from": "Grad, Minuten, Sekunden", "to": "Dezimalgrad",
         "factor_or_formula": "° + ′/60 + ″/3600", "reference": "Brückner S. 6–7 (Werte wie gedruckt)"},
    ],
    "datasets": [
        {"name": "points",
         "title": T("Trigonometrisch bestimmte Punkte", "Points fixed by triangulation"),
         "columns": [
             {"name": "nr", "label": T("Nr.", "No."), "type": "integer", "unit": None, "derived": True, "note": "Reihenfolge im Druck (S. 6, dann S. 7)"},
             {"name": "name", "label": T("Ort", "Place"), "type": "string", "unit": None},
             {"name": "landesteil", "label": LB, "type": "string", "unit": None, "derived": True, "note": "aus der Breite abgeleitet (Geissen: Unterland nach S. 13)"},
             {"name": "objekt", "label": T("Gemessener Gegenstand", "Object measured"), "type": "string", "unit": None},
             {"name": "objektart", "label": T("Objektart", "Object class"), "type": "string", "unit": None, "derived": True, "note": "redaktionelle Gruppierung"},
             {"name": "lon_grad", "label": T("Länge: Grad (Ferro)", "Longitude: degrees (Ferro)"), "type": "integer", "unit": "°"},
             {"name": "lon_min", "label": T("Länge: Minuten", "Longitude: minutes"), "type": "integer", "unit": "′"},
             {"name": "lon_sek", "label": T("Länge: Sekunden", "Longitude: seconds"), "type": "number", "unit": "″"},
             {"name": "lat_grad", "label": T("Breite: Grad", "Latitude: degrees"), "type": "integer", "unit": "°"},
             {"name": "lat_min", "label": T("Breite: Minuten", "Latitude: minutes"), "type": "integer", "unit": "′"},
             {"name": "lat_sek", "label": T("Breite: Sekunden", "Latitude: seconds"), "type": "number", "unit": "″"},
             {"name": "lon_ferro", "label": T("Länge östlich von Ferro", "Longitude east of Ferro"), "type": "number", "unit": "°", "derived": True},
             {"name": "lon_gw", "label": T("Länge östlich von Greenwich", "Longitude east of Greenwich"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat", "label": T("Breite", "Latitude"), "type": "number", "unit": "°", "derived": True},
             {"name": "in_klammern", "label": T("In Klammern gedruckt (1 = ja)", "Printed in brackets (1 = yes)"), "type": "integer", "unit": None, "derived": True, "note": "Codierung 0/1 editorisch"},
             {"name": "beschriftet", "label": T("Auf der Karte beschriftet (1 = ja)", "Labelled on the map (1 = yes)"), "type": "integer", "unit": None, "derived": True, "note": "Codierung 0/1 editorisch"},
             {"name": "seite", "label": T("Seite", "Page"), "type": "string", "unit": None},
         ],
         "rows": [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16]] for r in pt_rows],
         "source_refs": [{"page": "6", "block": "b3", "rows": "r1-r37"}, {"page": "7", "block": "b1", "rows": "r1-r20"}]},
        {"name": "extent",
         "title": T("Grenzwerte von Ober- und Unterland", "Limits of the Oberland and Unterland"),
         "columns": [
             {"name": "landesteil", "label": LB, "type": "string", "unit": None},
             {"name": "laenge_text", "label": T("Länge (Ferro), wie gedruckt", "Longitude (Ferro), as printed"), "type": "string", "unit": None},
             {"name": "breite_text", "label": T("Breite, wie gedruckt", "Latitude, as printed"), "type": "string", "unit": None},
             {"name": "lon_min_ferro", "label": T("Länge West (Ferro)", "Longitude west (Ferro)"), "type": "number", "unit": "°", "derived": True},
             {"name": "lon_max_ferro", "label": T("Länge Ost (Ferro)", "Longitude east (Ferro)"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat_min", "label": T("Breite Süd", "Latitude south"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat_max", "label": T("Breite Nord", "Latitude north"), "type": "number", "unit": "°", "derived": True},
             {"name": "lon_min_gw", "label": T("Länge West (Greenwich)", "Longitude west (Greenwich)"), "type": "number", "unit": "°", "derived": True},
             {"name": "lon_max_gw", "label": T("Länge Ost (Greenwich)", "Longitude east (Greenwich)"), "type": "number", "unit": "°", "derived": True},
             {"name": "breite_km", "label": T("Ost–West-Ausdehnung", "East–west extent"), "type": "number", "unit": "km", "derived": True},
             {"name": "hoehe_km", "label": T("Nord–Süd-Ausdehnung", "North–south extent"), "type": "number", "unit": "km", "derived": True},
         ],
         "rows": [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]] for r in ext_rows],
         "source_refs": [{"page": "6", "block": "b2"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "points", "extra_datasets": ["extent"],
         "title": T("Die vermessenen Punkte auf einer Karte", "The surveyed points on a map"),
         "caption": T("Längen nach Abzug von 17° 40′ (Ferro → Greenwich), Mercator-Projektion. Die gestrichelten Rechtecke sind die von Brückner gedruckten Grenzwerte (Länge/Breite) der beiden Landesteile, keine Landesgrenzen. Rauten: in Klammern gedruckte Punkte. Name und Koordinaten erscheinen beim Überfahren eines Punkts.",
                      "Longitudes after subtracting 17° 40′ (Ferro → Greenwich), Mercator projection. The dashed rectangles are the longitude/latitude limits printed by Brückner for the two parts, not borders. Diamonds: points printed in brackets. Name and coordinates appear when hovering over a point."),
         "vegalite": {
             "height": 420,
             "projection": {"type": "mercator", "center": [11.83, 50.67], "scale": 22000},
             "layer": [
                 {"data": {"name": "extent"},
                  "mark": {"type": "rect", "fillOpacity": 0.07},
                  "encoding": {
                      "longitude": {"field": "lon_min_gw", "type": "quantitative"},
                      "latitude": {"field": "lat_min", "type": "quantitative"},
                      "longitude2": {"field": "lon_max_gw"},
                      "latitude2": {"field": "lat_max"},
                      "color": CHART_COLOR}},
                 {"data": {"name": "extent"},
                  "mark": {"type": "rect", "filled": False, "strokeDash": [5, 4], "strokeWidth": 1.2},
                  "encoding": {
                      "longitude": {"field": "lon_min_gw", "type": "quantitative"},
                      "latitude": {"field": "lat_min", "type": "quantitative"},
                      "longitude2": {"field": "lon_max_gw"},
                      "latitude2": {"field": "lat_max"},
                      "color": CHART_COLOR}},
                 {"transform": [{"filter": "isValid(datum.lat)"}],
                  "mark": {"type": "point", "filled": True, "size": 60},
                  "encoding": {
                      "longitude": {"field": "lon_gw", "type": "quantitative"},
                      "latitude": {"field": "lat", "type": "quantitative"},
                      "color": CHART_COLOR,
                      "shape": {"condition": {"test": "datum.in_klammern == 1", "value": "diamond"}, "value": "circle"},
                      "tooltip": [
                          {"field": "name", "title": T("Ort", "Place")},
                          {"field": "objekt", "title": T("Gemessener Gegenstand", "Object measured")},
                          {"field": "lon_gw", "title": T("Länge Greenwich (°)", "Longitude Greenwich (°)"), "format": ".4f"},
                          {"field": "lat", "title": T("Breite (°)", "Latitude (°)"), "format": ".4f"},
                          {"field": "lon_ferro", "title": T("Länge Ferro (°)", "Longitude Ferro (°)"), "format": ".4f"},
                          {"field": "seite", "title": T("Seite", "Page")}]}},
                 {"transform": [{"filter": "datum.beschriftet == 1"}],
                  "mark": {"type": "text", "align": "left", "dx": 7, "dy": -5, "fontSize": 11},
                  "encoding": {
                      "longitude": {"field": "lon_gw", "type": "quantitative"},
                      "latitude": {"field": "lat", "type": "quantitative"},
                      "text": {"field": "name", "type": "nominal"}}},
             ]}},
        {"id": "c2", "dataset": "points",
         "title": T("Was wurde angepeilt?", "What was sighted?"),
         "caption": T("Anzahl der Punkte nach Art des gemessenen Gegenstands (redaktionelle Gruppierung der Angaben in der vierten Spalte).",
                      "Number of points by the kind of object measured (editorial grouping of the entries in the fourth column)."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "objektart", "type": "nominal", "sort": "-x", "title": None},
                 "x": {"aggregate": "count", "type": "quantitative", "title": T("Anzahl Punkte", "Number of points"), "axis": {"tickMinStep": 1}},
                 "color": {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland"]}},
                 "tooltip": [{"field": "objektart", "title": T("Objektart", "Object class")},
                             {"field": "landesteil", "title": LB},
                             {"aggregate": "count", "title": T("Anzahl", "Number")}]}}},
    ],
    "transcription_issues": [
        {"page": "6", "block": "b3", "cell": "r12c2", "transcribed": "29° 18' 27,154\" L. (Lobenstein)", "facsimile": "29° 18' 27,54\" L.", "checked_facsimile": True, "note": "zusätzliche »1« hinter dem Komma"},
        {"page": "6", "block": "b3", "cell": "r13c2", "transcribed": "29° 19' 28,105\" L. (Bellevue)", "facsimile": "29° 19' 28,05\" L.", "checked_facsimile": True, "note": "zusätzliche »1« hinter dem Komma"},
        {"page": "6", "block": "b3", "cell": "r36c2", "transcribed": "29° 34' 6,127\" L. (St. Gangloff)", "facsimile": "29° 34' 6,27\" L.", "checked_facsimile": True, "note": "zusätzliche »1« hinter dem Komma"},
        {"page": "4", "block": "b3", "transcribed": "vom 29° 7' 20\" bis 30° 7' 40\" in östlicher Länge und vom 50° 22' 45\" bis [50°] 21' 5\"", "facsimile": "vom 29° 7' 20\" um 40' 20\" in östlicher Länge und vom 50° 22' 45\" um 21' 5\" in nördlicher Breite", "checked_facsimile": True, "note": "»um« als »bis« gelesen; 40' 20\" als 30° 7' 40\""},
    ],
    "keywords": T(["Koordinaten", "geographische Länge", "geographische Breite", "Ferro", "Greenwich", "Triangulation", "Landesvermessung", "Generalstab", "Lage", "Ausdehnung", "Karte", "Gera", "Schleiz", "Lobenstein"],
                  ["coordinates", "longitude", "latitude", "Ferro meridian", "Greenwich", "triangulation", "survey", "General Staff", "position", "extent", "map", "Gera", "Schleiz", "Lobenstein"]),
    "related": ["grenzen-umfang-nachbarlaender", "flaeche-fuerstenthum-vermessung-nachbarn", "relief-hoehenstufen-oberland-unterland"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
