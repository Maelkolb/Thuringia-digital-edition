"""G7 analysis 6: deserted villages (Wuestungen) in the place articles."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
import collections

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)
W = sorted([e for e in ents if e["type"] == "Wüstung" or e.get("wuestung")], key=sort_key)
byname = collections.defaultdict(list)
for e in U:
    byname[e["name"]].append(e)

# reference village ("near") of each Wuestung, from the printed location statement
NEAR = {
    "pottendorf": "Ernsee", "vollersdorf": "Gera", "texdorf": "Rubitz", "cosse": "Mühlsdorf", "desse": "Kraftsdorf",
    "schliffstein": "Rüdersdorf", "oelsdorf": "Hartmannsdorf", "etzdorf": "Köstritz", "eschewinsdorf": "Köstritz",
    "lichtenau": "Steinbrücken", "rosenhof": "Steinbrücken", "hermannsdorf-gera": "Steinbrücken", "roedel": "Kleinaga",
    "wolstieg": "Kretzschwitz", "betzdorf": "Söllmnitz", "wuestenhain": "Dorna", "werteln": "Schwaara",
    "zoche": "Trebnitz", "speutewitz": "Trebnitz",
    "wuestendittersdorf-schleiz": "Schleiz", "triemsdorf": "Oettersdorf", "igelsdorf": "Pahren", "rumalt": "Saalburg",
    "wettera": "Saalburg", "kaemmera": "Tanna", "weidendorf": "Tanna", "dittersdorf-tanna": "Tanna",
    "mangelsdorf": "Schilbach", "hermannsdorf-schleiz": "Zollgrün", "alte-klause": "Mielesdorf", "traundorf": "Tanna",
    "hohendorf": "Pöritzsch", "wuestenheinersdorf": "Heinersdorf", "platte": "Kießling",
}
assert len(W) == 34 and all(uid(e) in NEAR for e in W), [uid(e) for e in W if uid(e) not in NEAR]

# ---- datasets -------------------------------------------------------------------------------------
wu_rows, ev_rows = [], []
for e in W:
    u = uid(e)
    forms = [(f["year"], f["form"], "Namensform") for f in (e.get("historic_forms") or []) if f.get("year")]
    evs = [(x["year"], x["event_de"], "Ereignis") for x in (e.get("events") or []) if x.get("year")]
    allyears = [(y, t, k) for y, t, k in forms + evs if y <= 1700]
    fy = e.get("first_mention_year")
    ys = [y for y, _, _ in allyears] + ([fy] if fy else [])
    near = NEAR[u]
    cand = [x for x in byname[near] if x["landestheil"] == e["landestheil"]] or byname[near]
    ne = cand[0]
    wu_rows.append([u, e["name"], e["landestheil"], e["type_verbatim"], (e.get("location") or {}).get("verbatim"), near,
                    fy, min(ys) if ys else None, max(ys) if ys else None, len(allyears),
                    e["start"]["page"], e["start"]["block"]])
    for y, t, k in sorted(allyears):
        ev_rows.append([u, e["name"], e["landestheil"], y, k, t, e["start"]["page"], e["start"]["block"]])
# order by earliest year (undated last) for the timeline
order = {r[0]: i for i, r in enumerate(sorted([r for r in wu_rows if r[7]], key=lambda r: (r[7], r[1])), start=1)}
ev_rows = [r + [order.get(r[0])] for r in ev_rows]
wcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Wüstung", "Deserted place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("type_verbatim", "Bezeichnung im Artikel", "Designation in the article", "string"),
    col("location", "Lage (gedruckt)", "Location (printed)", "string"),
    col("near", "Nächstgelegener Bezugsort", "Reference village", "string", derived=True, note="aus der gedruckten Lageangabe abgeleitet"),
    col("first_year", "Erste Erwähnung", "First mention", "integer", "Jahr", note="leer = im Artikel kein Jahr genannt"),
    col("earliest_year", "Frühestes Jahr im Artikel", "Earliest year in the article", "integer", "Jahr", derived=True, note="früheste Namensform, frühestes Ereignis oder Erstnennung bis 1700"),
    col("latest_year", "Spätestes Jahr bis 1700", "Latest year up to 1700", "integer", "Jahr", derived=True),
    col("n_years", "Datierte Namensformen und Ereignisse bis 1700", "Dated name forms and events up to 1700", "integer", derived=True),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
ecols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Wüstung", "Deserted place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("year", "Jahr", "Year", "integer", "Jahr"),
    col("kind", "Art der Angabe", "Kind of entry", "string", derived=True, note="Namensform oder Ereignis"),
    col("text", "Namensform bzw. Ereignis", "Name form or event", "string"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
    col("order", "Rang nach frühestem Jahr", "Rank by earliest year", "integer", derived=True),
]
nU = {lt: sum(1 for e in U if e["landestheil"] == lt) for lt in LT_ORDER}
nW = {lt: sum(1 for r in wu_rows if r[2] == lt) for lt in LT_ORDER}
dist_rows = [[lt, nW[lt], nU[lt], round(10 * nW[lt] / nU[lt], 2), sum(1 for r in wu_rows if r[2] == lt and r[7])] for lt in LT_ORDER]
dist_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("wuestungen", "Wüstungen", "Deserted places", "integer", derived=True),
    col("gemeinden", "Gemeinden", "Municipalities", "integer", derived=True),
    col("per_10", "Wüstungen je 10 Gemeinden", "Deserted places per 10 municipalities", "number", derived=True),
    col("dated", "davon mit Jahresangabe bis 1700", "of which dated up to 1700", "integer", derived=True),
]
near_rows = []
grp = collections.OrderedDict()
for r in wu_rows:
    grp.setdefault((r[5], r[2]), []).append(r[1])
for (near, lt), names in grp.items():
    cand = [x for x in byname[near] if x["landestheil"] == lt] or byname[near]
    ne = cand[0]
    lon, lat, gn = coord(ne, C)
    near_rows.append([near, lt, len(names), "; ".join(names), lon, lat])
near_cols = [
    col("near", "Bezugsort", "Reference village", "string", derived=True),
    col("landestheil", "Landestheil", "District", "string"),
    col("n", "Wüstungen in der Nähe", "Deserted places nearby", "integer", derived=True),
    col("names", "Wüstungen", "Deserted places", "string"),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json), Lage des Bezugsorts"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json), Lage des Bezugsorts"),
]
pos_rows = []
for e in U:
    lon, lat, gn = coord(e, C)
    pos_rows.append([uid(e), e["name"], e["landestheil"], lon, lat])
pos_cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
]
refs = uniq_refs(W)
refs_u = uniq_refs(U)

# ---- statistics ----------------------------------------------------------------------------------
nw = len(wu_rows)
n_dated = sum(1 for r in wu_rows if r[7])
n_first = sum(1 for r in wu_rows if r[6])
last_cnt = collections.Counter(r[8] for r in wu_rows if r[8])
top_last = last_cnt.most_common(3)
last1364 = last_cnt[1364]
last1533 = last_cnt[1533]
last1647 = last_cnt[1647]
earliest = sorted([r for r in wu_rows if r[7]], key=lambda r: r[7])[:3]
near_top = sorted(near_rows, key=lambda r: -r[2])[:3]
n_near_places = len(near_rows)
n_ev = len(ev_rows)
n_form = sum(1 for r in ev_rows if r[4] == "Namensform")
no_year = [r[1] for r in wu_rows if not r[7]]
fn = lambda x: fnum(x, 1)
fe = lambda x: fnum(x, 1, "en")
pd_ = {r[0]: r[3] for r in dist_rows}

findings = [
    bi(f"Brückner behandelt {nw} Wüstungen mit eigenem Absatz: {nW['Gera']} im Landestheil Gera, {nW['Schleiz']} in Schleiz und {nW['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf. Auf 10 Gemeinden kommen damit {fn(pd_['Gera'])} Wüstungen im Unterland, {fn(pd_['Schleiz'])} in Schleiz und nur {fn(pd_['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf, dessen Orte im Mittel später erstmals erwähnt werden (Deutung: jüngere Besiedlung).",
       f"Brückner treats {nw} deserted villages in paragraphs of their own: {nW['Gera']} in the district of Gera, {nW['Schleiz']} in Schleiz and {nW['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf. Per 10 municipalities that is {fe(pd_['Gera'])} deserted places in the lowland, {fe(pd_['Schleiz'])} in Schleiz and only {fe(pd_['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf, whose places are on average first mentioned later (interpretation: later settlement)."),
    bi(f"{n_dated} der {nw} Wüstungen haben datierte Namensformen oder Ereignisse bis 1700 ({n_ev} Angaben, davon {n_form} Namensformen); die ältesten stammen aus dem Jahr {earliest[0][7]} ({earliest[0][1]}; genannt wird ein nach dem Ort benannter Ritter) und {earliest[1][7]} ({earliest[1][1]}). {len(no_year)} Wüstungen nennen im Artikel kein Jahr, bei ihnen ist nur der Flurname oder das Gelände überliefert.",
       f"{n_dated} of the {nw} deserted places have dated name forms or events up to 1700 ({n_ev} entries, {n_form} of them name forms); the oldest date from {earliest[0][7]} ({earliest[0][1]}; a knight named after the place is mentioned) and {earliest[1][7]} ({earliest[1][1]}). {len(no_year)} deserted places give no year in the article; for them only the field name or the terrain survives."),
    bi(f"Das jüngste Jahr, das die Artikel bis 1700 für eine Wüstung nennen, ist bei {last1364} Wüstungen 1364, bei {last1533} 1533 und bei {last1647} 1647 – dieselben Stichjahre wie bei den Ersterwähnungen der Dörfer. Sie belegen teils das Bestehen des Ortes (1364), teils eine bereits eingetretene Wüstung (1533, 1647); wann ein Ort wüst wurde, lässt sich daraus nur eingrenzen, nicht datieren.",
       f"The latest year the articles give up to 1700 for a deserted place is 1364 for {last1364} of them, 1533 for {last1533} and 1647 for {last1647} – the same reference years as for the first mentions of villages. They attest in part the existence of the place (1364), in part a desertion that had already happened (1533, 1647); when a place was deserted can thus be narrowed down but not dated."),
    bi(f"Die Wüstungen liegen nahe bei {n_near_places} Bezugsorten; die meisten nennen die Artikel bei {near_top[0][0]} ({near_top[0][2]}: {near_top[0][3].replace('; ', ', ')}), {near_top[1][0]} ({near_top[1][2]}) und {near_top[2][0]} ({near_top[2][2]}). Mehrere Wüstungen sind in der Flur der Nachbardörfer aufgegangen (z. B. Triemsdorf, Werteln).",
       f"The deserted places lie near {n_near_places} reference villages; the articles name most of them near {near_top[0][0]} ({near_top[0][2]}: {near_top[0][3].replace('; ', ', ')}), {near_top[1][0]} ({near_top[1][2]}) and {near_top[2][0]} ({near_top[2][2]}). Several deserted places were absorbed into the field area of the neighbouring villages (e.g. Triemsdorf, Werteln)."),
]
LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
charts = [
    {"id": "c1", "dataset": "wuest_events",
     "title": bi("Datierte Nennungen der Wüstungen bis 1700", "Dated mentions of the deserted places up to 1700"),
     "caption": bi("Je Wüstung ein Strich vom frühesten bis zum spätesten Jahr, das der Artikel bis 1700 nennt; Kreise: Namensformen, Rauten: Ereignisse (Verkauf, Zerstörung, Erwähnung in Akten). Wüstungen ohne Jahresangabe fehlen.",
                   "One line per deserted place from the earliest to the latest year the article gives up to 1700; circles: name forms, diamonds: events (sale, destruction, mention in records). Deserted places without a year are missing."),
     "vegalite": {"height": 440, "transform": [{"filter": "isValid(datum.order)"}], "layer": [
         {"mark": {"type": "rule", "strokeWidth": 2, "opacity": 0.5},
          "encoding": {"y": {"field": "name", "type": "nominal", "sort": {"field": "order", "op": "min"}, "title": None},
                       "x": {"aggregate": "min", "field": "year", "type": "quantitative", "scale": {"zero": False}},
                       "x2": {"aggregate": "max", "field": "year"},
                       "color": LT_COLOR}},
         {"mark": {"type": "point", "filled": True, "size": 60, "opacity": 0.9},
          "encoding": {"y": {"field": "name", "type": "nominal", "sort": {"field": "order", "op": "min"}},
                       "x": {"field": "year", "type": "quantitative", "title": bi("Jahr", "Year"), "scale": {"zero": False}, "axis": {"format": "d"}},
                       "shape": {"field": "kind", "type": "nominal", "title": bi("Art der Angabe", "Kind of entry"),
                                 "scale": {"domain": ["Namensform", "Ereignis"], "range": ["circle", "diamond"]},
                                 "legend": {"orient": "bottom"}},
                       "color": LT_COLOR,
                       "tooltip": [{"field": "name", "title": bi("Wüstung", "Deserted place")},
                                   {"field": "year", "title": bi("Jahr", "Year")},
                                   {"field": "kind", "title": bi("Art", "Kind")},
                                   {"field": "text", "title": bi("Angabe", "Entry")},
                                   {"field": "page", "title": bi("Seite", "Page")}]}},
     ]}},
    {"id": "c2", "dataset": "wuest_district",
     "title": bi("Wüstungen je 10 Gemeinden", "Deserted places per 10 municipalities"),
     "caption": bi("Zahl der von Brückner behandelten Wüstungen bezogen auf die Gemeinden des Landestheils (173 Gemeinden); in den Balken steht die absolute Zahl im Tooltip.",
                   "Number of deserted places treated by Brückner in relation to the municipalities of the district (173 municipalities); the absolute number is in the tooltip."),
     "vegalite": {"height": 200, "mark": "bar", "encoding": {
         "y": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None},
         "x": {"field": "per_10", "type": "quantitative", "title": bi("Wüstungen je 10 Gemeinden", "Deserted places per 10 municipalities")},
         "color": {"field": "landestheil", "type": "nominal", "scale": {"domain": LT_ORDER}, "legend": None},
         "tooltip": [{"field": "landestheil", "title": bi("Landestheil", "District")},
                     {"field": "wuestungen", "title": bi("Wüstungen", "Deserted places")},
                     {"field": "gemeinden", "title": bi("Gemeinden", "Municipalities")},
                     {"field": "per_10", "title": bi("je 10 Gemeinden", "per 10 municipalities")}]}}},
    {"id": "c3", "dataset": "wuest_near", "extra_datasets": ["places_pos"],
     "title": bi("Wo Dörfer wüst wurden", "Where villages were deserted"),
     "caption": bi("Die Kreise stehen bei dem Dorf, in dessen Nähe der Artikel die Wüstung verortet (Fläche nach Zahl der Wüstungen); graue Punkte: alle Gemeinden. Die Lage der Wüstungen selbst ist nicht genauer bekannt. Koordinaten aus GeoNames.",
                   "The circles stand at the village near which the article locates the deserted place (area by number of deserted places); small dots: all municipalities. The exact position of the deserted places is not known. Coordinates from GeoNames."),
     "vegalite": {"height": 460, "projection": {"type": "mercator"}, "layer": [
         {"data": {"name": "places_pos"}, "transform": [{"filter": "isValid(datum.lat)"}],
          "mark": {"type": "circle", "size": 22, "opacity": 0.22},
          "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                       "color": {"field": "landestheil", "type": "nominal", "scale": {"domain": LT_ORDER}}}},
         {"transform": [{"filter": "isValid(datum.lat)"}],
          "mark": {"type": "circle", "opacity": 0.8},
          "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                       "size": {"field": "n", "type": "quantitative", "title": bi("Wüstungen", "Deserted places"),
                                "scale": {"type": "linear", "range": [100, 700], "domain": [1, 4]}, "legend": {"values": [1, 2, 4], "format": "d"}},
                       "color": LT_COLOR,
                       "tooltip": [{"field": "near", "title": bi("Bezugsort", "Reference village")},
                                   {"field": "n", "title": bi("Wüstungen", "Deserted places")},
                                   {"field": "names", "title": bi("Namen", "Names")}]}},
     ]}},
]

a = {
    "id": "orte-wuestungen-ortskunde",
    "title": bi("Wüstungen im Fürstenthum: Lage und Nennungen", "Deserted villages of the principality: location and mentions"),
    "category": "places",
    "section": "t2",
    "sources": refs + [r for r in refs_u if r not in refs],
    "summary": bi(
        f"Neben den bestehenden Orten beschreibt Brückner {nw} Wüstungen: untergegangene Dörfer, Vorwerke und Kultplätze, von denen oft nur noch Flurnamen, Mauerreste oder Sagen zeugen. Die Auswertung zeigt, in welchem Landestheil sie liegen, bei welchen Dörfern sie verortet werden und welche Jahre die Artikel zu ihnen nennen.",
        f"Besides the existing places Brückner describes {nw} deserted settlements: vanished villages, outlying farms and places of worship, of which often only field names, wall remains or legends survive. The analysis shows in which district they lie, near which villages they are located and which years the articles give for them."),
    "method": bi(
        f"Grundlage sind alle Gazetteer-Einträge des Typs Wüstung ({nw}). Aufgenommen sind auch Einträge, die Brückner als Wüstung führt, die aber anderes meinen (Wüstendittersdorf, das heute noch aus zwei Höfen, einer Mühle u. a. besteht; die Kupferplatte, ein ehemaliger Kupferhammer; die Alte Klause; Wüstenhain, ein Waldbezirk). Die Zeitleiste verwendet alle datierten Namensformen (historic_forms) und Ereignisse (events) der Einträge bis 1700 sowie das Jahr der Erstnennung; spätere Jahre (z. B. Funde 1800, 1853, 1866) betreffen die Wiederentdeckung und bleiben außer Betracht. Der Bezugsort ('near') ist das Dorf, bei dem der Artikel die Wüstung verortet (gedruckte Lageangabe, z. B. 'im N. von Steinbrücken'); bei Triemsdorf, das zwischen fünf Dörfern liegt, ist Oettersdorf gewählt. Die Karte zeichnet die Wüstungen am Bezugsort, nicht an ihrer tatsächlichen Lage. Wüstungen je 10 Gemeinden = Wüstungen : Gemeinden des Landestheils × 10 (173 Gemeinden, vgl. orte-siedlungsbild-1867).",
        f"The basis are all gazetteer entries of the type Wüstung ({nw}). Included are also entries that Brückner lists as Wüstung but that mean something else (Wüstendittersdorf, which still consists of two farms, a mill etc.; the Kupferplatte, a former copper hammer; the Alte Klause; Wüstenhain, a forest district). The timeline uses all dated name forms (historic_forms) and events (events) of the entries up to 1700 as well as the year of first mention; later years (e.g. finds in 1800, 1853, 1866) concern the rediscovery and are left out. The reference village ('near') is the village near which the article locates the deserted place (printed statement of location, e.g. 'N. of Steinbrücken'); for Triemsdorf, which lies between five villages, Oettersdorf was chosen. The map draws the deserted places at the reference village, not at their actual position. Deserted places per 10 municipalities = deserted places : municipalities of the district × 10 (173 municipalities, cf. orte-siedlungsbild-1867)."),
    "findings": findings,
    "caveats": [
        bi("Die Zahl der Wüstungen hängt davon ab, was Brückner in einem eigenen Absatz behandelt; manche erwähnt er nur beiläufig in anderen Artikeln (z. B. Eschewinsdorf bei Etzdorf, Hermannsdorf bei Rosenhof) oder ohne eigenen Absatz (Wüstenhain, Rumalt). Die Zählung ist daher ein Mindestwert und kein Verzeichnis aller Wüstungen.",
           "The number of deserted places depends on what Brückner treats in a paragraph of its own; some he mentions only in passing in other articles (e.g. Eschewinsdorf at Etzdorf, Hermannsdorf at Rosenhof) or without a separate paragraph (Wüstenhain, Rumalt). The count is therefore a minimum and not a list of all deserted places."),
        bi("Zwei Einträge heißen Hermannsdorf (bei Steinbrücken im Landestheil Gera und bei Zollgrün im Landestheil Schleiz) und zwei Dittersdorf (Wüstendittersdorf bei Schleiz, Dittersdorf bei Tanna); Brückner warnt selbst vor Verwechslungen. Die Gazetteer-Koordinaten für diese und einige weitere Wüstungen sind unsicher und wurden nicht verwendet.",
           "Two entries are called Hermannsdorf (near Steinbrücken in the district of Gera and near Zollgrün in the district of Schleiz) and two Dittersdorf (Wüstendittersdorf near Schleiz, Dittersdorf near Tanna); Brückner himself warns against confusion. The gazetteer coordinates for these and some other deserted places are uncertain and were not used."),
        bi("Ein Jahr, in dem ein Ort als bestehend bezeugt ist, gibt nur eine Untergrenze für den Untergang; die Zerstörung im Dreißigjährigen Krieg wird in den Artikeln teils nur vermutet oder durch Sagen überliefert.",
           "A year in which a place is attested as existing gives only a lower bound for its abandonment; destruction in the Thirty Years' War is in part only presumed in the articles or handed down in legends."),
    ],
    "datasets": [
        {"name": "wuest_district", "title": bi("Wüstungen und Gemeinden je Landestheil", "Deserted places and municipalities per district"),
         "columns": dist_cols, "rows": dist_rows, "source_refs": refs + [r for r in refs_u if r not in refs]},
        {"name": "wuestungen", "title": bi("Die Wüstungen der Ortsartikel", "The deserted places of the place articles"),
         "columns": wcols, "rows": wu_rows, "source_refs": refs},
        {"name": "wuest_events", "title": bi("Datierte Namensformen und Ereignisse der Wüstungen bis 1700", "Dated name forms and events of the deserted places up to 1700"),
         "columns": ecols, "rows": ev_rows, "source_refs": refs},
        {"name": "wuest_near", "title": bi("Wüstungen je Bezugsort", "Deserted places per reference village"),
         "columns": near_cols, "rows": near_rows, "source_refs": refs},
        {"name": "places_pos", "title": bi("Lage der Gemeinden (Hintergrund der Karte)", "Position of the municipalities (map background)"),
         "columns": pos_cols, "rows": pos_rows, "source_refs": refs_u},
    ],
    "charts": charts,
    "keywords": {"de": ["Wüstungen", "wüste Orte", "Dorfwüstungen", "Siedlungsgeschichte", "Flurnamen", "Ortskunde"],
                 "en": ["deserted villages", "abandoned settlements", "settlement history", "field names", "topography"]},
    "related": ["orte-erste-erwaehnungen-namensformen", "orte-siedlungsbild-1867", "ortsnamen-sorbische-wurzeln"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
