"""G7 analysis 8: field area (Flur) per inhabitant and rent per Morgen ("Pacht") of the villages."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
from flur_extract import rent
import collections, math

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)
MORGEN_HA = 0.255322
GERA = (50.88029, 12.08187)   # GeoNames position of Gera (coords.json)
assert abs(C["gera"]["lat"] - GERA[0]) < 1e-6


def hav(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


rows = []
for e in U:
    fl = e.get("flur_morgen")
    t = article_text(e)
    r = rent(t)
    if not fl and not r:
        continue
    inh, hou = eff(e)
    pc = place_class(e)
    lon, lat, gn = coord(e, C)
    d = round(hav(lat, lon, *GERA), 1) if lat is not None else None
    snippet = None
    if r:
        snippet = re.sub(r"\s+", " ", r[2])
    rows.append([uid(e), e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, e.get("flur_verbatim"),
                 round(fl, 2) if fl else None, round(fl * MORGEN_HA, 1) if fl else None,
                 round(fl / inh, 2) if fl else None,
                 r[0] if r else None, r[1] if r else None, round((r[0] + r[1]) / 2, 2) if r else None, snippet,
                 d, lon, lat, e["start"]["page"], e["start"]["block"]])
cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("flur_verbatim", "Flur (gedruckt)", "Field area (printed)", "string"),
    col("flur_morgen", "Flur", "Field area", "number", "Morgen", derived=True, note="gedruckte gemischte Zahlen (z. B. 706 7/13) in Dezimalzahlen umgerechnet"),
    col("flur_ha", "Flur", "Field area", "number", "ha", derived=True, note="1 preuß. Morgen = 0,255322 ha (Brückner S. 832)"),
    col("morgen_per_inh", "Flur je Einwohner", "Field area per inhabitant", "number", "Morgen/Einw.", derived=True),
    col("rent_lo", "Pacht je Morgen, von", "Rent per Morgen, from", "number", "Thaler", derived=True, note="Pacht eines mittelguten Morgens aus der gedruckten Angabe (Brüche wie 2 1/4 in Dezimalzahlen); bei Einzelwerten gleich dem Höchstwert; leer = keine Angabe"),
    col("rent_hi", "Pacht je Morgen, bis", "Rent per Morgen, to", "number", "Thaler", derived=True),
    col("rent_mid", "Pacht je Morgen (Mitte)", "Rent per Morgen (midpoint)", "number", "Thaler", derived=True),
    col("rent_text", "Gedruckte Angabe", "Printed statement", "string"),
    col("dist_gera_km", "Entfernung von Gera (Luftlinie)", "Distance from Gera (straight line)", "number", "km", derived=True, note="aus GeoNames-Koordinaten berechnet"),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
refs = uniq_refs(U)

# ---- statistics ----------------------------------------------------------------------------------
vil = [r for r in rows if r[3] != "Stadt"]
fl_v = [r for r in vil if r[7]]
n_fl = len(fl_v)
fl_tot = sum(r[7] for r in rows if r[7])
fl_tot_ha = fl_tot * MORGEN_HA
n_flur_all = sum(1 for r in rows if r[7])
mpi = {lt: median([r[9] for r in fl_v if r[2] == lt]) for lt in LT_ORDER}
n_mpi = {lt: sum(1 for r in fl_v if r[2] == lt) for lt in LT_ORDER}
smallest = sorted(fl_v, key=lambda r: r[9])[:3]
largest = sorted(fl_v, key=lambda r: -r[9])[:3]
rv = [r for r in rows if r[12] is not None]
n_rent = len(rv)
rent_med = {lt: median([r[12] for r in rv if r[2] == lt]) for lt in LT_ORDER}
n_rent_lt = {lt: sum(1 for r in rv if r[2] == lt) for lt in LT_ORDER}
rent_max = max(r[12] for r in rv)
rent_min = min(r[12] for r in rv)
top_rent = [r[1] for r in sorted(rv, key=lambda r: -r[12])[:5]]
lowest = sorted(rv, key=lambda r: (r[12], r[1]))
low_first = lowest[0]
low_two = [r[1] for r in lowest[1:] if r[12] == 2.0][:4]
rd = [r for r in rv if r[14] is not None]


def spearman(a, b):
    ra = [sorted(a).index(x) + (a.count(x) - 1) / 2 for x in a]
    rb = [sorted(b).index(x) + (b.count(x) - 1) / 2 for x in b]
    ma, mb = mean(ra), mean(rb)
    return sum((p - ma) * (q - mb) for p, q in zip(ra, rb)) / math.sqrt(sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb))


rho = spearman([r[14] for r in rd], [r[12] for r in rd])
near = [r for r in rd if r[14] <= 10]
far = [r for r in rd if r[14] > 30]
rent_near = median([r[12] for r in near])
rent_far = median([r[12] for r in far])
rho_in = {lt: spearman([r[14] for r in rd if r[2] == lt], [r[12] for r in rd if r[2] == lt]) for lt in LT_ORDER if sum(1 for r in rd if r[2] == lt) > 5}
n_geo = sum(1 for r in rd)
fn1 = lambda x: fnum(x, 1)
fe1 = lambda x: fnum(x, 1, "en")

findings = [
    bi(f"Die Fluren der {n_flur_all} Orte mit Flurangabe umfassen zusammen {fnum(fl_tot)} Morgen, das sind {fnum(fl_tot_ha)} ha (Brückners Morgen = 0,2553 ha). Je Einwohner kommen in den Dörfern im Median {fnum(mpi['Gera'],1)} Morgen im Landestheil Gera, {fnum(mpi['Schleiz'],1)} in Schleiz und {fnum(mpi['Lobenstein-Ebersdorf'],1)} in Lobenstein-Ebersdorf (Spannen: {fnum(smallest[0][9],1)} in {smallest[0][1]} bis {fnum(largest[0][9],1)} in {largest[0][1]}).",
       f"The field areas of the {n_flur_all} places with a figure add up to {fnum(fl_tot,0,'en')} Morgen, i.e. {fnum(fl_tot_ha,0,'en')} ha (Brückner's Morgen = 0.2553 ha). Per inhabitant the villages have a median of {fnum(mpi['Gera'],1,'en')} Morgen in the district of Gera, {fnum(mpi['Schleiz'],1,'en')} in Schleiz and {fnum(mpi['Lobenstein-Ebersdorf'],1,'en')} in Lobenstein-Ebersdorf (range: {fnum(smallest[0][9],1,'en')} in {smallest[0][1]} to {fnum(largest[0][9],1,'en')} in {largest[0][1]})."),
    bi(f"Für {n_rent} Orte nennt Brückner die Pacht eines mittelguten Morgens: im Landestheil Gera im Median {fn1(rent_med['Gera'])} Thaler, in Schleiz {fn1(rent_med['Schleiz'])} und in Lobenstein-Ebersdorf {fn1(rent_med['Lobenstein-Ebersdorf'])}. Am teuersten ist das Land bei {', '.join(top_rent[:4])} (je {fnum(rent_max,0)} Thaler), am billigsten bei {low_first[1]} ({fnum(low_first[10],0)}–{fnum(low_first[11],0)} Thaler) sowie {', '.join(low_two[:-1])} und {low_two[-1]} (je 2 Thaler).",
       f"For {n_rent} places Brückner gives the rent of a medium-quality Morgen: a median of {fe1(rent_med['Gera'])} thalers in the district of Gera, {fe1(rent_med['Schleiz'])} in Schleiz and {fe1(rent_med['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf. Land is dearest at {', '.join(top_rent[:4])} ({fnum(rent_max,0,'en')} thalers each), cheapest at {low_first[1]} ({fnum(low_first[10],0,'en')}–{fnum(low_first[11],0,'en')} thalers) as well as {', '.join(low_two[:-1])} and {low_two[-1]} (2 thalers each)."),
    bi(f"Die Pacht sinkt mit der Entfernung von Gera (Rangkorrelation {fnum(rho,2)} über {len(rd)} Orte): Dörfer bis 10 km Luftlinie von Gera ({len(near)} Orte) liegen im Median bei {fn1(rent_near)} Thalern, Dörfer über 30 km ({len(far)} Orte) bei {fn1(rent_far)}. Das entspricht einem Marktgefälle zur größten Stadt, ist aber nicht von Höhenlage und Bodengüte zu trennen (Deutung).",
       f"Rent falls with the distance from Gera (rank correlation {fnum(rho,2,'en')} over {len(rd)} places): villages up to 10 km as the crow flies from Gera ({len(near)} places) have a median of {fe1(rent_near)} thalers, villages beyond 30 km ({len(far)} places) {fe1(rent_far)}. This matches a market gradient towards the largest town, but cannot be separated from altitude and soil quality (interpretation)."),
]
LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
charts = [
    {"id": "c1", "dataset": "flur_places",
     "title": bi("Flur je Einwohner in den Dörfern", "Field area per inhabitant in the villages"),
     "caption": bi(f"Morgen Flur je Einwohner ({n_fl} Dörfer und Märkte, ohne die sechs Städte); Kasten: Median und Quartile, Punkte: Ausreißer. 1 Morgen = 0,2553 ha.",
                   f"Morgen of field area per inhabitant ({n_fl} villages and market towns, without the six towns); box: median and quartiles, dots: outliers. 1 Morgen = 0.2553 ha."),
     "vegalite": {"height": 300, "transform": [{"filter": "datum.class_de != 'Stadt' && isValid(datum.morgen_per_inh)"}],
                  "mark": {"type": "boxplot", "extent": 1.5, "size": 40, "opacity": 0.8},
                  "encoding": {"x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labelAngle": 0}},
                               "y": {"field": "morgen_per_inh", "type": "quantitative", "title": bi("Morgen je Einwohner", "Morgen per inhabitant")},
                               "color": LT_COLOR}}},
    {"id": "c2", "dataset": "flur_places",
     "title": bi("Pacht eines mittelguten Morgens", "Rent of a medium-quality Morgen"),
     "caption": bi(f"Pacht in Thalern je Morgen ({n_geo} verortete Orte; Mitte der gedruckten Spanne). Die teuersten Felder liegen um Gera und Köstritz, die billigsten im südlichen Oberland. Koordinaten aus GeoNames.",
                   f"Rent in thalers per Morgen ({n_geo} located places; midpoint of the printed range). The dearest fields lie around Gera and Köstritz, the cheapest in the southern upland. Coordinates from GeoNames."),
     "vegalite": {"height": 460, "projection": {"type": "mercator"},
                  "transform": [{"filter": "isValid(datum.lat) && isValid(datum.rent_mid)"}],
                  "mark": {"type": "circle", "opacity": 0.9, "size": 150},
                  "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                               "color": {"field": "rent_mid", "type": "quantitative", "title": bi("Thaler je Morgen", "thalers per Morgen"),
                                         "scale": {"range": "ramp"}},
                               "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                                           {"field": "landestheil", "title": bi("Landestheil", "District")},
                                           {"field": "rent_lo", "title": bi("Pacht von", "Rent from")},
                                           {"field": "rent_hi", "title": bi("Pacht bis", "Rent to")},
                                           {"field": "rent_text", "title": bi("Gedruckt", "Printed")},
                                           {"field": "page", "title": bi("Seite", "Page")}]}}},
    {"id": "c3", "dataset": "flur_places",
     "title": bi("Pacht und Entfernung von Gera", "Rent and distance from Gera"),
     "caption": bi("Pacht je Morgen (Mitte der Spanne) gegen die Luftlinie von Gera in km; die gestrichelte Linie ist die lineare Regression über alle Orte. Die Städte sind enthalten, soweit sie eine Pacht nennen.",
                   "Rent per Morgen (midpoint of the range) against the straight-line distance from Gera in km; the dashed line is the linear regression over all places. Towns are included where they state a rent."),
     "vegalite": {"height": 340, "transform": [{"filter": "isValid(datum.dist_gera_km) && isValid(datum.rent_mid)"}], "layer": [
         {"mark": {"type": "circle", "opacity": 0.75, "size": 70},
          "encoding": {"x": {"field": "dist_gera_km", "type": "quantitative", "title": bi("Entfernung von Gera (km, Luftlinie)", "Distance from Gera (km, straight line)")},
                       "y": {"field": "rent_mid", "type": "quantitative", "title": bi("Thaler je Morgen", "thalers per Morgen")},
                       "color": LT_COLOR,
                       "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                                   {"field": "dist_gera_km", "title": bi("km von Gera", "km from Gera")},
                                   {"field": "rent_lo", "title": bi("Pacht von", "Rent from")},
                                   {"field": "rent_hi", "title": bi("Pacht bis", "Rent to")},
                                   {"field": "page", "title": bi("Seite", "Page")}]}},
         {"transform": [{"regression": "rent_mid", "on": "dist_gera_km"}],
          "mark": {"type": "line", "strokeDash": [4, 3]},
          "encoding": {"x": {"field": "dist_gera_km", "type": "quantitative"}, "y": {"field": "rent_mid", "type": "quantitative"}}},
     ]}},
]

a = {
    "id": "orte-flur-boden-pacht",
    "title": bi("Flur und Pacht: Fläche je Einwohner und Bodenpreis der Dörfer", "Field area and rent: land per inhabitant and land prices of the villages"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Zu jedem Dorf gibt Brückner die Größe der Flur in Morgen an und oft auch, was ein mittelguter Morgen an Pacht trägt. Daraus lassen sich die Landausstattung je Einwohner und ein Gefälle der Bodenpreise ablesen: hohe Pacht in der Nähe von Gera und Köstritz, niedrige im Oberland.",
        f"For each village Brückner gives the size of the field area in Morgen and often also what a medium-quality Morgen yields in rent. From this the land endowment per inhabitant and a gradient of land prices can be read: high rents near Gera and Köstritz, low rents in the upland."),
    "method": bi(
        f"Grundlage sind das Feld flur_morgen der Gazetteer-Einträge der {len(U)} Gemeinden (G1–G6) und die Pachtangabe in den Artikeltexten. Die Flur wurde aus den gedruckten gemischten Zahlen in Dezimalzahlen umgerechnet und mit 0,255322 ha je preuß. Morgen in Hektar (Brückner, S. 832). Bei zweiherrischen Orten gilt die reußische Flur; Cuba, Untermhaus und Blintendorf nennen keine Flur. Die Pacht eines Morgens wurde aus den Artikeltexten mit einer Mustersuche (Zahl vor oder nach 'Pacht' bzw. 'verpachtet' im Umfeld von 'Morgen', 'Acker' oder 'Feld') ermittelt und gegen die Texte geprüft; Spannen ('9–11 Thlr.') sind als Von-bis-Werte erfasst, die Mitte ist abgeleitet. Gemeint ist meist der mittelgute Morgen. Bei Wüstfalke bezieht sich die Pacht auf auswärtigen Boden, bei Rödersdorf nur auf Pfarrland, bei Göritz ist 'nicht unter 5 Thlr.' als 5 und bei Altengesees 'kaum 3 Thlr.' als 3 erfasst; für Neundorf ('auf ein Achtel 1 Thlr.') wurde die Angabe wegen unklaren Sinns nicht übernommen. Artikel, die keine Pacht nennen oder sagen, dass nicht verpachtet wird (z. B. Collis, Pohlen, Willersdorf), haben keinen Wert. Die Entfernung von Gera ist die Luftlinie zwischen den GeoNames-Koordinaten des Orts und Geras (Haversine-Formel).",
        f"The basis are the field flur_morgen of the gazetteer entries of the {len(U)} municipalities (G1–G6) and the rent statements in the article texts. The field area was converted from the printed mixed numbers to decimals and to hectares at 0.255322 ha per Prussian Morgen (Brückner, p. 832). For places shared with a neighbouring state the Reuss field area applies; Cuba, Untermhaus and Blintendorf give no field area. The rent of a Morgen was extracted from the article texts with a pattern search (a number before or after 'Pacht' or 'verpachtet' near 'Morgen', 'Acker' or 'Feld') and checked against the texts; ranges ('9–11 thalers') are recorded as from–to values, the midpoint is derived. Mostly the medium-quality Morgen is meant. For Wüstfalke the rent refers to land elsewhere, for Rödersdorf only to parsonage land; at Göritz 'not under 5 thalers' is recorded as 5 and at Altengesees 'hardly 3 thalers' as 3; for Neundorf ('on one eighth 1 thaler') the statement was not taken over because its meaning is unclear. Articles that give no rent or state that land is not leased (e.g. Collis, Pohlen, Willersdorf) have no value. The distance from Gera is the straight line between the GeoNames coordinates of the place and of Gera (haversine formula)."),
    "findings": findings,
    "caveats": [
        bi("Die Pacht ist ein Ortsurteil des Verfassers (meist die Pacht des mittelguten Morgens) und kein gemessener Marktpreis; Spannen und Formulierungen wie 'kaum' oder 'nicht unter' sind vereinfacht. Wo nur ein Teil der Flur oder fremder Boden gemeint ist, steht das im Artikel.",
           "The rent is the author's judgement for a place (mostly the rent of a medium-quality Morgen) and not a measured market price; ranges and wordings such as 'hardly' or 'not under' are simplified. Where only part of the field area or foreign land is meant, the article says so."),
        bi("Die Flur ist die Gemarkung der Gemeinde einschließlich Wald, Wiesen und Teichen (z. B. Hohenleuben: 889 Morgen Wald von 3 027 Morgen); bei Rittergutsdörfern gehört ein Teil dem Gut, so dass die Fläche je Einwohner nicht die Ausstattung der Bauern wiedergibt. Brückners Größenangaben schwanken zwischen genauen Brüchen und Abrundungen.",
           "The field area is the municipal territory including woods, meadows and ponds (e.g. Hohenleuben: 889 Morgen of woodland out of 3,027 Morgen); in manorial villages part of it belongs to the estate, so that the area per inhabitant does not reflect the farmers' endowment. Brückner's figures vary between exact fractions and roundings."),
        bi("Die Maßeinheit 'Morgen' ist in den Ortsartikeln nicht näher erklärt; hier wird Brückners Umrechnung des preußischen Morgens (180 Quadratruthen) angewandt.",
           "The unit 'Morgen' is not explained in the place articles; Brückner's conversion of the Prussian Morgen (180 square rods) is applied here."),
    ],
    "datasets": [
        {"name": "flur_places", "title": bi("Flur, Pacht und Entfernung von Gera je Gemeinde", "Field area, rent and distance from Gera per municipality"),
         "columns": cols, "rows": rows, "source_refs": refs},
    ],
    "charts": charts,
    "conversions": [{"from": "preuß. Morgen", "to": "Hektar", "factor_or_formula": "1 Morgen = 0,255322 ha (180 Quadratruthen)", "reference": "Brückner, S. 832"}],
    "keywords": {"de": ["Flur", "Pacht", "Bodenpreis", "Morgen", "Landwirtschaft", "Dörfer", "Bodengüte", "Entfernung"],
                 "en": ["field area", "rent", "land price", "Morgen", "agriculture", "villages", "soil quality", "distance"]},
    "related": ["orte-viehbestand-1867", "landwirtschaft-bodennutzung-1854", "landwirtschaft-grundbesitz-1854", "wirtschaft-loehne-pacht-landwirtschaft-1860er"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
