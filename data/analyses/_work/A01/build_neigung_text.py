"""Part 2: texts, datasets, charts for relief-hoehe-und-lage-neigung."""
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from build_neigung import *     # noqa: F401,F403

f0 = lambda x: fmt(x, 0)
f0e = lambda x: fmt(x, 0, "en")
MIN = lambda t: t.replace("-", "−")
f1 = lambda x: fmt(x, 1)
f1e = lambda x: fmt(x, 1, "en")
f2 = lambda x: fmt(x, 2)
f2e = lambda x: fmt(x, 2, "en")

n = len(rows_src)
rows = []
for i, r in enumerate(rows_src, 1):
    rows.append([i, r["name"], r["hname"], r["lt"], round(r["lon"], 5), round(r["lat"], 5), round(r["x"], 2), round(r["y"], 2),
                 round(r["lo"], 1), round(r["hi"], 1), round(r["mid"], 1), round(r["fit"], 1), round(r["res"], 1), r["lab"], r["pg"], r["hp"]])

fit_rows = []
for lab, F in (("alle Orte", F_all), ("Oberland", F_ob), ("Unterland", F_un)):
    fit_rows.append([lab, F["n"], round(float(F["beta"][0]), 1), round(float(F["beta"][1]), 2), round(float(F["beta"][2]), 2),
                     round(F["slope"], 2), round(F["az"], 0), round(F["r2"], 3), round(F["rmse"], 1)])

# arrow along the steepest descent, starting at the centroid of the matched points
cx = float(np.mean([r["x"] for r in rows_src])); cy = float(np.mean([r["y"] for r in rows_src]))
L_KM = 20.0
az = math.radians(F_all["az"])
x2, y2 = cx + L_KM * math.sin(az), cy + L_KM * math.cos(az)
arrow_rows = [[round(LON0 + cx / KX, 5), round(LAT0 + cy / KY, 5), round(LON0 + x2 / KX, 5), round(LAT0 + y2 / KY, 5), round(F_all["az"], 0)]]

b_all, c_all = float(F_all["beta"][1]), float(F_all["beta"][2])
geissen = next(r for r in rows_src if r["name"] == "Geissen")
gei_alt = geissen["mid"] - (float(F_all["beta"][0]) + b_all * geissen["x"] + c_all * (geissen["y"] + 10 / 60 * KY))
neg = sorted(rows_src, key=lambda r: r["res"])[:4]
assert [r["name"] for r in neg] == ["Harra", "Geissen", "Saalburg", "Köstritz"], [r["name"] for r in neg]
pos = sorted(rows_src, key=lambda r: -r["res"])[:3]
print("geissen alt res", gei_alt, [(r["name"], round(r["res"])) for r in neg], [(r["name"], round(r["res"])) for r in pos])
drop_total = F_all["slope"] * 38    # over ~38 km (SW-NE extent), only for info
az_all = F_all["az"]
nm_all = len(pts)

COL3 = {"field": "landesteil", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland", "Regression"]}}

ana = {
    "id": "relief-hoehe-und-lage-neigung",
    "title": T("Höhe und Lage: Fällt das Land nach Nordosten?", "Altitude and position: does the land fall towards the north-east?"),
    "category": "relief",
    "section": "t1-1-4",
    "sources": [
        {"page": "6", "block": "b3", "rows": "r1-r37"}, {"page": "7", "block": "b1", "rows": "r1-r20"},
        {"page": "10", "block": "b3"},
        {"page": "11", "block": "b13"}, {"page": "12", "block": "b1"}, {"page": "12", "block": "b3"}, {"page": "13", "block": "b1"},
        {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}, {"page": "9", "block": "b2"},
    ],
    "summary": T(
        f"Brückner beschreibt das Land als »von Südwest nach Nordost sanft geneigtes Plateau« (S. 9) und spricht von einer »Neigung von Westen nach Osten oder genauer von Südwest nach Nordost« (S. 10). Verknüpft man seine Koordinatentabelle (S. 6–7) mit den Höhenlisten der Wohnorte (S. 11–22), lässt sich das prüfen: {n} Orte haben beides. Eine Ausgleichsebene durch ihre Höhen fällt tatsächlich nach {fmt(az_all, 0)}° (Nordost), mit rund {f1(F_all['slope'])} m je Kilometer.",
        f"Brückner describes the country as a plateau “gently inclined from south-west to north-east” (p. 9) and speaks of an “inclination from west to east or, more precisely, from south-west to north-east” (p. 10). Combining his coordinate table (pp. 6–7) with the altitude lists of the inhabited places (pp. 11–22) allows a check: {n} places have both. A plane fitted through their altitudes does fall towards {fmt(az_all, 0)}° (north-east), at about {f1e(F_all['slope'])} m per kilometre."),
    "method": T(
        f"Aus der Koordinatentabelle (S. 6–7, Greenwich-Längen wie in der Analyse »Mathematische Lage«) wurden alle Orte genommen, die in den Höhenlisten (S. 11–13, 20–22) als eigener Eintrag mit Höhe stehen; gleiche Namen wurden nur im selben Landesteil verknüpft. Abweichende Schreibungen wurden gleichgesetzt: Rödersdorf = Rüdersdorf, Geissen = Geißen, Bergkirche = Schleizer Bergkirche, Oettersdorf = Dettersdorf (im Ortsregister beide auf S. 602), Grumbach = Grumbach (Mitte), Schleiz = Schleiz (Wiesenthal), Kirschkau = Kirschkau (nördliche Häuser). Ausgelassen wurden Punkte ohne Ort in der Höhenliste (Signale, Hügel), die eingeklammerten Punkte, Kleinfriesa (ohne Breite) und der zweite Punkt von Eliasbrunn. Als Höhe dient die Mitte der gedruckten Spanne des Ortes (preußische Dezimalfuß × 0,3766242 = m). Die Ausgleichsebene H = a + b·x + c·y (x: Kilometer ostwärts, y: Kilometer nordwärts von 11,85° O / 50,70° N; 1° Breite = 111,2 km, 1° Länge = {fmt(KX, 1)} km) wurde nach der Methode der kleinsten Quadrate berechnet; die Fallrichtung ist der Azimut des steilsten Gefälles (von Nord im Uhrzeigersinn).",
        f"From the coordinate table (pp. 6–7, Greenwich longitudes as in the analysis “Mathematical position”) all places were taken that appear as an entry with altitude in the altitude lists (pp. 11–13, 20–22); equal names were joined only within the same part of the country. Differing spellings were equated: Rödersdorf = Rüdersdorf, Geissen = Geißen, Bergkirche = Schleizer Bergkirche, Oettersdorf = Dettersdorf (both on p. 602 of the place index), Grumbach = Grumbach (centre), Schleiz = Schleiz (Wiesenthal), Kirschkau = Kirschkau (northern houses). Omitted were points without a place in the altitude list (signals, hills), the bracketed points, Kleinfriesa (no latitude) and the second point of Eliasbrunn. The altitude is the midpoint of the place's printed range (Prussian decimal feet × 0.3766242 = m). The plane H = a + b·x + c·y (x: kilometres east, y: kilometres north of 11.85° E / 50.70° N; 1° latitude = 111.2 km, 1° longitude = {f1e(KX)} km) was computed by least squares; the direction of fall is the azimuth of steepest descent (from north, clockwise)."),
    "findings": [
        T(f"Die Ausgleichsebene durch {n} Orte fällt nach {fmt(az_all, 0)}° (Nordost) mit {f1(F_all['slope'])} m je km (≈ {f1(F_all['slope'] / 10)} %); sie erklärt {fmt(100 * F_all['r2'], 0)} % der Streuung der Ortshöhen (mittlerer Fehler {f0(F_all['rmse'])} m). Das bestätigt Brückners Angabe der Neigung von Südwest nach Nordost.",
          f"The plane through {n} places falls towards {fmt(az_all, 0)}° (north-east) at {f1e(F_all['slope'])} m per km (≈ {f1e(F_all['slope'] / 10)} %); it explains {fmt(100 * F_all['r2'], 0)} % of the variance of place altitudes (mean error {f0e(F_all['rmse'])} m). This confirms Brückner's statement of an inclination from south-west to north-east."),
        T(f"Allein nach der Breite betrachtet sinkt die Ortshöhe um {f0(-b_lat / KY * 10)} m je 10 km nach Norden (Korrelation {fmt(r_lat, 2)}). Die mittlere Ortshöhe beträgt im Oberland {f0(mO)} m, im Unterland {f0(mU)} m (für die {n} verknüpften Orte).",
          f"Considered by latitude alone, place altitude falls by {f0e(-b_lat / KY * 10)} m per 10 km towards the north (correlation {fmt(r_lat, 2)}). The mean place altitude is {f0e(mO)} m in the Oberland and {f0e(mU)} m in the Unterland (for the {n} linked places)."),
        T(f"Innerhalb der Landesteile ist das Bild verschieden: Im Oberland ({F_ob['n']} Orte) beträgt das Gefälle {f1(F_ob['slope'])} m/km nach {fmt(F_ob['az'], 0)}° (R² = {fmt(F_ob['r2'], 2)}), im Unterland ({F_un['n']} Orte) nur {f1(F_un['slope'])} m/km (R² = {fmt(F_un['r2'], 2)}). Im Unterland erklärt die Lage also kaum etwas; das Gefälle des Gesamtbildes entsteht vor allem durch den Sprung zwischen den beiden Landesteilen.",
          f"Within the parts the picture differs: in the Oberland ({F_ob['n']} places) the fall is {f1e(F_ob['slope'])} m/km towards {fmt(F_ob['az'], 0)}° (R² = {fmt(F_ob['r2'], 2)}), in the Unterland ({F_un['n']} places) only {f1e(F_un['slope'])} m/km (R² = {fmt(F_un['r2'], 2)}). Within the Unterland position thus explains little; the fall of the overall picture arises mainly from the step between the two parts."),
        T(f"Die größten Abweichungen nach unten haben Orte in tiefen Flusstälern: {neg[0]['name']} ({f0(neg[0]['res'])} m), {neg[2]['name']} ({f0(neg[2]['res'])} m, beide an der Saale) und {neg[3]['name']} ({f0(neg[3]['res'])} m, an der Elster) liegen rund 100 m unter der Ebene – passend zu Brückners Schilderung der tief eingeschnittenen Täler (S. 4). Nach oben weichen {pos[0]['name']} (+{f0(pos[0]['res'])} m), {pos[1]['name']} (+{f0(pos[1]['res'])} m) und {pos[2]['name']} (+{f0(pos[2]['res'])} m) ab.",
          f"The largest deviations downwards are places in deep river valleys: {neg[0]['name']} ({f0e(neg[0]['res'])} m), {neg[2]['name']} ({f0e(neg[2]['res'])} m, both on the Saale) and {neg[3]['name']} ({f0e(neg[3]['res'])} m, on the Elster) lie about 100 m below the plane, in line with Brückner's description of the deeply cut valleys (p. 4). Upwards the largest deviations are {pos[0]['name']} (+{f0e(pos[0]['res'])} m), {pos[1]['name']} (+{f0e(pos[1]['res'])} m) and {pos[2]['name']} (+{f0e(pos[2]['res'])} m)."),
    ],
    "caveats": [
        T(f"Geissen hat die zweitgrößte Abweichung ({f0(geissen['res'])} m). Das passt zum vermuteten Druckfehler der Breite (50° 45′ 44″ statt etwa 50° 55′ 44″; siehe »Mathematische Lage«): läge der Ort 10′ nördlicher, würde die Abweichung auf {f0(gei_alt)} m sinken. Das ist ein Hinweis, kein Beweis.",
          f"Geissen has the second-largest deviation ({f0e(geissen['res'])} m). This fits the suspected printing error in its latitude (50° 45′ 44″ instead of about 50° 55′ 44″; see “Mathematical position”): if the place lay 10′ further north the deviation would fall to {f0e(gei_alt)} m. This is a hint, not proof."),
        T("Die Höhenspanne eines Ortes und der gemessene Gegenstand der Koordinaten (Kirchturmknopf, Mühle, Signal) passen nicht genau zusammen; die Mitte der Spanne ist nur eine grobe Ortshöhe. Die Ebene ist eine Näherung (ebene Geometrie, lineare Fläche) und kein geologisches Modell.",
          "The altitude range of a place and the object whose coordinates were measured (church tower knob, mill, signal) do not match exactly; the midpoint of the range is only a rough place altitude. The plane is an approximation (flat geometry, linear surface), not a geological model."),
        T("Brückner schreibt die Neigung der »gedachten« Hochflächen zu, wenn man die Täler ausgefüllt dächte (S. 9). Die Ortshöhen liegen teils in den Tälern; die Ebene beschreibt deshalb eher einen Mittelwert aus Tal- und Hochflächenorten.",
          "Brückner ascribes the inclination to the “imagined” plateaus if the valleys were filled in (p. 9). Some place altitudes are in the valleys; the plane therefore describes rather an average of valley and plateau places."),
    ],
    "conversions": conversions_height(),
    "datasets": [
        {"name": "matched", "title": T("Orte mit Koordinaten und Höhe", "Places with coordinates and altitude"),
         "columns": [
             {"name": "nr", "label": T("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
             {"name": "ort_koord", "label": T("Ort (Koordinatentabelle)", "Place (coordinate table)"), "type": "string", "unit": None},
             {"name": "ort_hoehe", "label": T("Ort (Höhenliste)", "Place (altitude list)"), "type": "string", "unit": None},
             {"name": "landesteil", "label": LB, "type": "string", "unit": None, "derived": True},
             {"name": "lon_gw", "label": T("Länge östlich von Greenwich", "Longitude east of Greenwich"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat", "label": T("Breite", "Latitude"), "type": "number", "unit": "°", "derived": True},
             {"name": "x_km", "label": T("Ostabstand von 11,85° O", "Distance east of 11.85° E"), "type": "number", "unit": "km", "derived": True},
             {"name": "y_km", "label": T("Nordabstand von 50,70° N", "Distance north of 50.70° N"), "type": "number", "unit": "km", "derived": True},
             {"name": "hoehe_min_m", "label": T("Höhe unten", "Altitude, lowest"), "type": "number", "unit": "m", "derived": True},
             {"name": "hoehe_max_m", "label": T("Höhe oben", "Altitude, highest"), "type": "number", "unit": "m", "derived": True},
             {"name": "hoehe_mitte_m", "label": T("Höhe, Mitte", "Altitude, midpoint"), "type": "number", "unit": "m", "derived": True},
             {"name": "ebene_m", "label": T("Höhe der Ausgleichsebene", "Altitude of the fitted plane"), "type": "number", "unit": "m", "derived": True},
             {"name": "abweichung_m", "label": T("Abweichung von der Ebene", "Deviation from the plane"), "type": "number", "unit": "m", "derived": True},
             {"name": "beschriftet", "label": T("Auf der Karte beschriftet (1 = ja)", "Labelled on the map (1 = yes)"), "type": "integer", "unit": None, "derived": True},
             {"name": "seite_koord", "label": T("Seite (Koordinaten)", "Page (coordinates)"), "type": "string", "unit": None},
             {"name": "seite_hoehe", "label": T("Seite (Höhe)", "Page (altitude)"), "type": "string", "unit": None},
         ],
         "rows": rows,
         "source_refs": [{"page": "6", "block": "b3"}, {"page": "7", "block": "b1"}, {"page": "11", "block": "b13"}, {"page": "12", "block": "b1"}, {"page": "12", "block": "b3"},
                         {"page": "13", "block": "b1"}, {"page": "20", "block": "b3"}, {"page": "21", "block": "b1"}, {"page": "22", "block": "b1"}]},
        {"name": "fits", "title": T("Ausgleichsebenen", "Fitted planes"),
         "columns": [
             {"name": "gruppe", "label": T("Orte", "Places"), "type": "string", "unit": None},
             {"name": "n", "label": T("Anzahl", "Number"), "type": "integer", "unit": None, "derived": True},
             {"name": "a", "label": T("Höhe bei 11,85° O / 50,70° N", "Altitude at 11.85° E / 50.70° N"), "type": "number", "unit": "m", "derived": True},
             {"name": "b", "label": T("Änderung je km nach Osten", "Change per km eastwards"), "type": "number", "unit": "m/km", "derived": True},
             {"name": "c", "label": T("Änderung je km nach Norden", "Change per km northwards"), "type": "number", "unit": "m/km", "derived": True},
             {"name": "gefaelle", "label": T("Gefälle", "Slope"), "type": "number", "unit": "m/km", "derived": True},
             {"name": "azimut", "label": T("Richtung des Gefälles (von Nord, im Uhrzeigersinn)", "Direction of fall (from north, clockwise)"), "type": "number", "unit": "°", "derived": True},
             {"name": "r2", "label": T("R²", "R²"), "type": "number", "unit": None, "derived": True},
             {"name": "rmse", "label": T("Mittlerer Fehler", "Root mean square error"), "type": "number", "unit": "m", "derived": True},
         ],
         "rows": fit_rows, "source_refs": [{"page": "6", "block": "b3"}]},
        {"name": "arrow", "title": T("Pfeil des steilsten Gefälles (Karte)", "Arrow of steepest descent (map)"),
         "columns": [
             {"name": "lon1", "label": T("Länge Anfang", "Longitude start"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat1", "label": T("Breite Anfang", "Latitude start"), "type": "number", "unit": "°", "derived": True},
             {"name": "lon2", "label": T("Länge Ende", "Longitude end"), "type": "number", "unit": "°", "derived": True},
             {"name": "lat2", "label": T("Breite Ende", "Latitude end"), "type": "number", "unit": "°", "derived": True},
             {"name": "azimut", "label": T("Azimut", "Azimuth"), "type": "number", "unit": "°", "derived": True},
         ],
         "rows": arrow_rows, "source_refs": [{"page": "6", "block": "b3"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "matched", "extra_datasets": ["arrow"],
         "title": T("Die Ortshöhen auf der Karte", "Place altitudes on the map"),
         "caption": T(f"Orte, für die Brückner Koordinaten und Höhe nennt; Farbe = Höhe der Spannenmitte in m. Der Pfeil zeigt die Richtung des steilsten Gefälles der Ausgleichsebene ({fmt(az_all, 0)}°, {f1(F_all['slope'])} m/km). Die Höhen sind von dunkel (hoch) nach hell (niedrig) abgestuft.",
                      f"Places for which Brückner gives coordinates and altitude; colour = altitude of the range midpoint in m. The arrow shows the direction of steepest descent of the fitted plane ({fmt(az_all, 0)}°, {f1e(F_all['slope'])} m/km). Heights are shaded from dark (high) to light (low)."),
         "vegalite": {
             "height": 420,
             "projection": {"type": "mercator", "center": [11.83, 50.68], "scale": 22000},
             "layer": [
                 {"mark": {"type": "point", "filled": True, "size": 110},
                  "encoding": {
                      "longitude": {"field": "lon_gw", "type": "quantitative"},
                      "latitude": {"field": "lat", "type": "quantitative"},
                      "color": {"field": "hoehe_mitte_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"range": "ramp"}},
                      "tooltip": [{"field": "ort_koord", "title": T("Ort", "Place")},
                                  {"field": "landesteil", "title": LB},
                                  {"field": "hoehe_min_m", "title": T("Höhe unten (m)", "Altitude, lowest (m)")},
                                  {"field": "hoehe_max_m", "title": T("Höhe oben (m)", "Altitude, highest (m)")},
                                  {"field": "ebene_m", "title": T("Höhe der Ebene (m)", "Plane altitude (m)")},
                                  {"field": "abweichung_m", "title": T("Abweichung (m)", "Deviation (m)")}]}},
                 {"transform": [{"filter": "datum.beschriftet == 1"}],
                  "mark": {"type": "text", "align": "left", "dx": 9, "dy": -6, "fontSize": 11},
                  "encoding": {
                      "longitude": {"field": "lon_gw", "type": "quantitative"},
                      "latitude": {"field": "lat", "type": "quantitative"},
                      "text": {"field": "ort_koord", "type": "nominal"}}},
                 {"data": {"name": "arrow"},
                  "mark": {"type": "rule", "strokeWidth": 2.5},
                  "encoding": {
                      "longitude": {"field": "lon1", "type": "quantitative"},
                      "latitude": {"field": "lat1", "type": "quantitative"},
                      "longitude2": {"field": "lon2"},
                      "latitude2": {"field": "lat2"}}},
                 {"data": {"name": "arrow"},
                  "mark": {"type": "text", "fontSize": 20, "baseline": "middle"},
                  "encoding": {
                      "longitude": {"field": "lon2", "type": "quantitative"},
                      "latitude": {"field": "lat2", "type": "quantitative"},
                      "text": {"value": "▲"},
                      "angle": {"field": "azimut", "type": "quantitative"}}},
             ]}},
        {"id": "c2", "dataset": "matched",
         "title": T("Ortshöhe gegen geographische Breite", "Place altitude against latitude"),
         "caption": T(f"Jeder Punkt ist ein Ort (Höhe = Mitte der gedruckten Spanne). Die gestrichelte Gerade ist die Ausgleichsgerade über alle Orte ({f0(-b_lat / KY * 10)} m je 10 km nach Norden); die Orte der beiden Landesteile bilden zwei getrennte Wolken.",
                      f"Each point is a place (altitude = midpoint of the printed range). The dashed line is the least-squares line through all places ({f0e(-b_lat / KY * 10)} m per 10 km northwards); the places of the two parts form two separate clouds."),
         "vegalite": {
             "height": 340,
             "layer": [
                 {"mark": {"type": "point", "filled": True, "size": 70},
                  "encoding": {
                      "x": {"field": "lat", "type": "quantitative", "title": T("Breite (° N)", "Latitude (° N)"), "scale": {"zero": False}},
                      "y": {"field": "hoehe_mitte_m", "type": "quantitative", "title": T("Höhe (m)", "Altitude (m)"), "scale": {"zero": False}},
                      "color": COL3,
                      "tooltip": [{"field": "ort_koord", "title": T("Ort", "Place")},
                                  {"field": "lat", "title": T("Breite (°)", "Latitude (°)"), "format": ".3f"},
                                  {"field": "hoehe_mitte_m", "title": T("Höhe, Mitte (m)", "Altitude, midpoint (m)")},
                                  {"field": "abweichung_m", "title": T("Abweichung von der Ebene (m)", "Deviation from the plane (m)")}]}},
                 {"transform": [{"regression": "hoehe_mitte_m", "on": "lat"}],
                  "mark": {"type": "line", "strokeDash": [6, 4]},
                  "encoding": {
                      "x": {"field": "lat", "type": "quantitative"},
                      "y": {"field": "hoehe_mitte_m", "type": "quantitative"},
                      "color": {"datum": "Regression", "type": "nominal", "title": LB, "scale": {"domain": ["Oberland", "Unterland", "Regression"]}}}},
             ]}},
    ],
    "keywords": T(["Höhe", "Lage", "Neigung", "Gefälle", "Südwest", "Nordost", "Plateau", "Elster", "Saale", "Hochfläche", "Koordinaten", "Ausgleichsebene"],
                  ["altitude", "position", "inclination", "slope", "south-west", "north-east", "plateau", "Elster", "Saale", "regression plane"]),
    "related": ["lage-vermessene-punkte-laenge-breite", "relief-wohnorte-hoehenlage", "relief-hoehenstufen-oberland-unterland"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
import re as _re
def _minus(node):
    if isinstance(node, dict):
        return {k: _minus(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_minus(v) for v in node]
    if isinstance(node, str):
        return _re.sub(r"(?<=[\s(])-(?=\d)", "−", node)
    return node
for _k in ("summary", "method", "findings", "caveats"):
    ana[_k] = _minus(ana[_k])
write_analysis(ana)
