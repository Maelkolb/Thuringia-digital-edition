"""Analysis: Sagenorte nach Typ und Landestheil (pp. 201-207).

Localities named in Brückner's lists of legend sites (Wiedenheer, headless riders and ghosts, witch animals, white lady,
treasure sites, legendary monasteries, sorcerers, will-o'-the-wisps). The Landestheil of each place is taken from the
gazetteer packages (data/gazetteer/G1-G6, Brückner Part II) or, failing that, from the page of the place's article in the
register of places (data/registers/ortsregister.json) and the page ranges of the three Landestheile.
"""
import glob
import json
from collections import Counter, OrderedDict, defaultdict
from _common import *

# --- lookups -------------------------------------------------------------------------------------------------
GAZ = defaultdict(set)   # name -> set of landestheil
GAZ_N = Counter()        # settlements per Landestheil (Stadt, Marktflecken, Dorf)
for f in sorted(glob.glob(str(ROOT / "data" / "gazetteer" / "G*.json"))):
    d = json.loads(open(f, encoding="utf-8").read())
    for e in d["entries"]:
        if e.get("landestheil"):
            GAZ[e["name"]].add(e["landestheil"])
        if e.get("type") in ("Stadt", "Marktflecken", "Dorf"):
            GAZ_N[e["landestheil"]] += 1
REG = defaultdict(set)
reg = json.loads((ROOT / "data" / "registers" / "ortsregister.json").read_text(encoding="utf-8"))
RANGES = [("Gera", 407, 569), ("Schleiz", 570, 705), ("Lobenstein-Ebersdorf", 706, 825)]


def lt_of_page(p):
    for name, a, b in RANGES:
        if a <= p <= b:
            return name


for e in reg["entries"]:
    for pg in e.get("pages") or []:
        if pg.isdigit() and lt_of_page(int(pg)):
            REG[e["name"]].add(lt_of_page(int(pg)))

LT_ORDER = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]


def district(gname):
    if gname in GAZ and len(GAZ[gname]) == 1:
        return next(iter(GAZ[gname])), "Gazetteer"
    if gname in REG and len(REG[gname]) == 1:
        return next(iter(REG[gname])), "Ortsregister"
    return None, None


TYPES = OrderedDict([
    ("wiede", bi("Wiedenheer (Wotans Nachtjagd)", "Wild Hunt (Wotan’s night hunt)")),
    ("spuk", bi("Reiter, Jäger, Spukgestalten", "Riders, huntsmen, ghostly figures")),
    ("hexe", bi("Hexentiere und Hexenplätze", "Witch animals and witch places")),
    ("weiss", bi("Weiße Frau", "White lady")),
    ("schatz", bi("Schatzstellen", "Treasure sites")),
    ("kloster", bi("Sagenhafte Klöster", "Legendary monasteries")),
    ("zauberer", bi("Zauberer", "Sorcerers")),
    ("irr", bi("Irrlichter", "Will-o’-the-wisps")),
])
# type -> (candidate blocks, [(token in the text, name for the lookup)])
L = {
    "wiede": ([("202", "b2")], [("Frankenthal", "Frankenthal"), ("Töppeln", "Töppeln"), ("Milbiz", "Milbitz"), ("Rubitz", "Rubitz"), ("Kraftsdorf", "Kraftsdorf"), ("Großsaara", "Großsaara"), ("Waltersdorf", "Waltersdorf"), ("Cuba", "Cuba"), ("Langenberg", "Langenberg"), ("Pohlitz", "Pohlitz"), ("Leumnitz", "Leumnitz"), ("Hermsdorf", "Hermsdorf"), ("Pohlen", "Pohlen"), ("Lichtenberg", "Lichtenberg"), ("hohenleubner Wahlteich", "Hohenleuben"), ("Hirschbach", "Hirschbach"), ("Löhma", "Löhma"), ("Ruppersdorf", "Ruppersdorf"), ("Heinersdorf", "Heinersdorf"), ("Pottiga", "Pottiga"), ("Frankendorf", "Frankendorf"), ("Unterkoskau", "Unterkoskau"), ("Kämmera", "Kämmera")]),
    "spuk": ([("202", "b2"), ("203", "b1")], [("In Gera auf der Stätte", "Gera"), ("Cuba, Roschitz", "Cuba"), ("Roschitz", "Roschitz"), ("Roben, Speutewitz", "Roben"), ("Speutewitz", "Speutewitz"), ("Dürrenberg bei der Schäferei", "Dürrenberg"), ("Neuärgerniß trifft", "Neuärgerniss"), ("Lothra", "Lothra"), ("Dessegrund", "Desse"), ("Debschwitz", "Debschwitz"), ("Dürrenebersdorf", "Dürrenebersdorf"), ("Otticha", "Otticha"), ("Wüstfalke", "Wüstfalke"), ("Zeulsdorf", "Zeulsdorf"), ("Weißig", "Weißig"), ("Gerberg bei Kulm", "Kulm"), ("Langengrobsdorf", "Langengrobsdorf")]),
    "hexe": ([("204", "b1")], [("Zwötzen", "Zwötzen"), ("Rusitz", "Rusitz"), ("Langenberg am Lausebirnbaum", "Langenberg"), ("Großaga", "Großaga"), ("Kleinaga", "Kleinaga"), ("Dorna", "Dorna"), ("Lichtenberg", "Lichtenberg"), ("Kaimberg", "Kaimberg"), ("Pforten", "Pforten"), ("Köstritz", "Köstritz"), ("bei Gera", "Gera"), ("Töppeln", "Töppeln"), ("Kraftsdorf", "Kraftsdorf"), ("Harpersdorf", "Harpersdorf"), ("Niederndorf", "Niederndorf"), ("Scheubengrobsdorf", "Scheubengrobsdorf"), ("Pahren", "Pahren"), ("Saalburg", "Saalburg"), ("Hohenleuben", "Hohenleuben"), ("Hundhaupten", "Hundhaupten")]),
    "weiss": ([("205", "b3")], [("Caaschwitz", "Caaschwitz"), ("Köstritz", "Köstritz"), ("Kaimberg", "Kaimberg"), ("Oschitz", "Oschitz"), ("Hartmannsdorf", "Hartmannsdorf"), ("Türkengraben bei Gera", "Gera"), ("Desse bei Kraftsdorf", "Kraftsdorf"), ("Kaltenborn", "Kaltenborn"), ("Kreml zwischen Dorna", "Dorna"), ("Söllmnitz", "Söllmnitz"), ("Wertheln", "Wertheln"), ("Pottiga", "Pottiga"), ("Hirschberg", "Hirschberg"), ("Reichenfels", "Reichenfels")]),
    "schatz": ([("205", "b3"), ("206", "b1")], [("zu Gera", "Gera"), ("in Langenberg", "Langenberg"), ("Köstritz", "Köstritz"), ("Dürrenberg", "Dürrenberg"), ("Kraftsdorf", "Kraftsdorf"), ("Töppeln", "Töppeln"), ("Ernsee", "Ernsee"), ("Collis", "Collis"), ("Stelzen", "Stelzen"), ("Hohenleuben", "Hohenleuben"), ("Kretzschwitz", "Kretzschwitz"), ("Scheubengrobsdorf", "Scheubengrobsdorf"), ("Frankendorf", "Frankendorf"), ("Zollgrün", "Zollgrün"), ("Lichtenau", "Lichtenau"), ("Dittersdorf", "Dittersdorf"), ("Künsdorf", "Künsdorf"), ("Oberkoskau", "Oberkoskau"), ("Untermhaus", "Untermhaus")]),
    "kloster": ([("201", "b1")], [("fünf in Gera", "Gera"), ("Zwötzen", "Zwötzen"), ("Lusan", "Lusan"), ("Untermhaus", "Untermhaus"), ("Cubamühle", "Cuba"), ("Pottendorf", "Pottendorf"), ("Roschitz", "Roschitz"), ("Rubitz", "Rubitz"), ("Dessegrund", "Desse"), ("Roben", "Roben"), ("Kaimberg", "Kaimberg"), ("Reichenfels", "Reichenfels"), ("Pahren", "Pahren"), ("Schleiz auf dem Schweinsberg", "Schleiz"), ("Oschitz", "Oschitz"), ("Weißbach", "Weißbach"), ("Triebes", "Triebes"), ("Lothra", "Lothra"), ("Arlas", "Arlas")]),
    "zauberer": ([("204", "b1")], [("Gera den alten Ebeling", "Gera"), ("Bieblach", "Bieblach"), ("Langenberg einen alten Dachdecker", "Langenberg"), ("Töppeln den Müllerburschen", "Töppeln"), ("Rüdersdorf den alten Caspar", "Rüdersdorf"), ("Kraftsdorf seinen Poser", "Kraftsdorf"), ("Windischenbernsdorf", "Windischenbernsdorf"), ("Waltersdorf einen Doctor", "Waltersdorf"), ("Otticha den Brösel", "Otticha"), ("Hohenleuben den Kresse", "Hohenleuben"), ("Burkersdorf den alten Golle", "Burkersdorf"), ("Bauer in Tinz", "Tinz"), ("Langenwetzendorf einen Erdspiegel", "Langenwetzendorf")]),
    "irr": ([("207", "b3")], [("Rüdersdorfer", "Rüdersdorf"), ("Köstritz", "Köstritz"), ("bei Dorna", "Dorna"), ("von Lobenstein", "Lobenstein"), ("Pohlitz", "Pohlitz"), ("Oberröppisch", "Oberröppisch"), ("Neundorfer", "Neundorf"), ("Harpersdorf", "Harpersdorf"), ("Görkwitz", "Görkwitz")]),
}

rows = []
unmatched = []
for tkey, (blocks, items) in L.items():
    for token, gname in items:
        blk = None
        for p, b in blocks:
            if token in text(p, b):
                blk = (p, b)
                break
        assert blk, (tkey, token)
        lt, basis = district(gname)
        if lt is None:
            unmatched.append((tkey, token, gname))
            continue
        rows.append([TYPES[tkey]["de"], TYPES[tkey]["en"], token if len(token.split()) == 1 else gname, gname, lt, basis, blk[0], blk[1]])
print("unmatched:", unmatched)
print(len(rows), "type-place rows")
# ambiguous names are excluded by district() (Wernsdorf not used; Dittersdorf both Schleiz)
print(GAZ["Dittersdorf"], GAZ["Neundorf"], REG.get("Neuärgerniss"))
for r in rows:
    if r[5] == "Ortsregister":
        print("via register:", r[3], r[4])

# --- per place -----------------------------------------------------------------------------------------------
place_types = defaultdict(set)
place_lt = {}
for r in rows:
    place_types[r[3]].add(r[0])
    place_lt[r[3]] = r[4]
places = sorted(place_types, key=lambda p: (-len(place_types[p]), p))
rows_pl = [[p, place_lt[p], len(place_types[p])] for p in places]
print(len(places), "distinct places;", rows_pl[:12])
lt_places = Counter(place_lt.values())
print(lt_places, dict(GAZ_N))
sets = Counter(r[4] for r in rows)
print("rows per district:", sets)
tot_rows = len(rows)
n_places = len(places)
rows_d = []
for lt in LT_ORDER:
    rows_d.append([lt, GAZ_N[lt], lt_places[lt], round(100 * lt_places[lt] / GAZ_N[lt], 1), sets[lt], round(100 * sets[lt] / tot_rows, 1), round(100 * GAZ_N[lt] / sum(GAZ_N[x] for x in LT_ORDER), 1)])
print(rows_d)
by_type_lt = defaultdict(Counter)
for r in rows:
    by_type_lt[r[0]][r[4]] += 1
for t in TYPES.values():
    print(t["de"], dict(by_type_lt[t["de"]]))
multi = [p for p in places if len(place_types[p]) >= 3]
print("places in >= 3 lists:", [(p, len(place_types[p]), place_lt[p]) for p in multi])
type_counts = Counter(r[0] for r in rows)
print(type_counts)
unmatched_names = sorted({u[2] for u in unmatched})

# sources
blks = sorted({(r[6], r[7]) for r in rows}, key=lambda x: (int(x[0]), int(x[1][1:])))
src = [{"page": p, "block": b} for p, b in blks]

TYPE_DOMAIN = [TYPES[k] for k in TYPES]
top3 = rows_pl[:3]
share_gera_places = round(100 * lt_places["Gera"] / n_places)
share_gera_settl = round(100 * GAZ_N["Gera"] / sum(GAZ_N.values()))
share_le_places = round(100 * lt_places["Lobenstein-Ebersdorf"] / n_places)
share_le_settl = round(100 * GAZ_N["Lobenstein-Ebersdorf"] / sum(GAZ_N.values()))
d_by = {r[0]: r for r in rows_d}

ana = {
    "id": "kultur-sagenorte-nach-typ-und-landestheil",
    "title": bi("Sagenorte nach Typ und Landestheil", "Legend sites by type and district"),
    "category": "culture",
    "section": "t1-2-8",
    "sources": src,
    "summary": bi(
        f"Im Abschnitt »Sage und Glaube« nennt Brückner zu acht Sagentypen die Orte, an denen sie lokalisiert werden (Wiedenheer, Spukreiter, Hexentiere, weiße Frauen, Schätze, Klöster, Zauberer, Irrlichter). Ordnet man die {n_places} genannten Orte den drei Landestheilen zu, so liegt der Schwerpunkt im Landestheil Gera ({lt_places['Gera']} Orte); aus dem Landestheil Lobenstein-Ebersdorf stammen nur {lt_places['Lobenstein-Ebersdorf']}. Brückner merkt an, dass vieles noch nicht durchforscht ist, besonders die Saalgegend.",
        f"In the section “Sage und Glaube” Brückner names, for eight types of legend, the places where they are located (Wild Hunt, ghostly riders, witch animals, white ladies, treasures, monasteries, sorcerers, will-o’-the-wisps). If the {n_places} places named are assigned to the three districts, the emphasis lies in the district of Gera ({lt_places['Gera']} places); only {lt_places['Lobenstein-Ebersdorf']} come from the district of Lobenstein-Ebersdorf. Brückner remarks that much has not yet been explored, especially the Saale area.",
    ),
    "method": bi(
        f"Aus den Aufzählungen auf S. 201–207 wurden alle Ortsangaben in acht Listen übernommen (»bei X«, »in X«; ein Ort kann in mehreren Listen stehen). Der Landestheil jedes Ortes stammt aus dem Gazetteer der Ortskunde (Teil II) und, wo dort kein Eintrag besteht, aus der Seite des Ortsregisters (S. 826–829) und den Seitenbereichen der Landestheile (Gera 407–569, Schleiz 570–705, Lobenstein-Ebersdorf 706–825). {len(unmatched_names)} Namen ließen sich nicht eindeutig zuordnen und fehlen (Wernsdorf ist doppelt vorhanden und nicht verwendet; {', '.join(unmatched_names)}). Als Bezugsgröße dienen die Dörfer, Märkte und Städte des Gazetteers je Landestheil (Gera {GAZ_N['Gera']}, Schleiz {GAZ_N['Schleiz']}, Lobenstein-Ebersdorf {GAZ_N['Lobenstein-Ebersdorf']}).",
        f"All place references in the enumerations on pp. 201–207 were taken into eight lists (“bei X”, “in X”; a place can appear in several lists). The district of each place comes from the gazetteer of the topography (Part II) and, where it has no entry, from the page of the register of places (pp. 826–829) and the page ranges of the districts (Gera 407–569, Schleiz 570–705, Lobenstein-Ebersdorf 706–825). {len(unmatched_names)} names could not be assigned unambiguously and are missing (Wernsdorf exists twice and was not used; {', '.join(unmatched_names)}). The villages, market towns and towns of the gazetteer per district serve as the reference (Gera {GAZ_N['Gera']}, Schleiz {GAZ_N['Schleiz']}, Lobenstein-Ebersdorf {GAZ_N['Lobenstein-Ebersdorf']}).",
    ),
    "findings": [
        bi(
            f"Von {n_places} verschiedenen Orten in den acht Listen liegen {lt_places['Gera']} ({share_gera_places} %) im Landestheil Gera, {lt_places['Schleiz']} im Landestheil Schleiz und nur {lt_places['Lobenstein-Ebersdorf']} ({share_le_places} %) im Landestheil Lobenstein-Ebersdorf; der Landestheil Gera hat im Gazetteer {share_gera_settl} %, Lobenstein-Ebersdorf {share_le_settl} % der Dörfer, Märkte und Städte.",
            f"Of {n_places} distinct places in the eight lists, {lt_places['Gera']} ({share_gera_places} %) lie in the district of Gera, {lt_places['Schleiz']} in the district of Schleiz and only {lt_places['Lobenstein-Ebersdorf']} ({share_le_places} %) in the district of Lobenstein-Ebersdorf; in the gazetteer the district of Gera has {share_gera_settl} %, Lobenstein-Ebersdorf {share_le_settl} % of the villages, market towns and towns.",
        ),
        bi(
            f"Je 100 Dörfer, Märkte und Städte ergeben sich {dz(d_by['Gera'][3])} Sagenorte im Landestheil Gera, {dz(d_by['Schleiz'][3])} in Schleiz und {dz(d_by['Lobenstein-Ebersdorf'][3])} in Lobenstein-Ebersdorf.",
            f"Per 100 villages, market towns and towns there are {ez(d_by['Gera'][3])} legend places in the district of Gera, {ez(d_by['Schleiz'][3])} in Schleiz and {ez(d_by['Lobenstein-Ebersdorf'][3])} in Lobenstein-Ebersdorf.",
        ),
        bi(
            f"Am häufigsten genannt sind {top3[0][0]} ({top3[0][2]} Listen), {top3[1][0]} ({top3[1][2]}) und {top3[2][0]} ({top3[2][2]}); {len(multi)} Orte stehen in mindestens drei Listen, darunter Brückners »Schatzkästlein der Sage«.",
            f"Named most often are {top3[0][0]} ({top3[0][2]} lists), {top3[1][0]} ({top3[1][2]}) and {top3[2][0]} ({top3[2][2]}); {len(multi)} places appear in at least three lists, among them Brückner’s “treasure chests of legend”.",
        ),
        bi(
            f"Die längsten Listen sind Wiedenheer ({type_counts[TYPES['wiede']['de']]} Orte), Hexentiere ({type_counts[TYPES['hexe']['de']]}), Schatzstellen ({type_counts[TYPES['schatz']['de']]}) und sagenhafte Klöster ({type_counts[TYPES['kloster']['de']]}); Brückner zählt 23 Klosterstätten in 19 Orten (fünf davon in Gera).",
            f"The longest lists are the Wild Hunt ({type_counts[TYPES['wiede']['de']]} places), witch animals ({type_counts[TYPES['hexe']['de']]}), treasure sites ({type_counts[TYPES['schatz']['de']]}) and legendary monasteries ({type_counts[TYPES['kloster']['de']]}); Brückner counts 23 monastery sites at 19 places (five of them in Gera).",
        ),
    ],
    "caveats": [
        bi(
            "Die Verteilung spiegelt auch die Sammlung wider: Brückner stützt sich auf die Aufzeichnungen von R. Eisel in Gera und eigene Wanderungen und nennt die Saalgegend des Landes ausdrücklich als noch nicht durchforscht (zu ihr gehört ein Teil des Landestheils Lobenstein-Ebersdorf). Aus der Verteilung lässt sich daher nicht schließen, dass es dort weniger Sagen gab.",
            "The distribution also reflects the collecting: Brückner relies on the notes of R. Eisel at Gera and his own walks and expressly names the Saale area of the country as not yet explored (part of the district of Lobenstein-Ebersdorf belongs to it). The distribution therefore does not show that there were fewer legends there.",
        ),
        bi(
            "Die Ortslisten sind redaktionell aus Prosa gewonnen (»bei Pohlen«, »in der Wüstung Kämmera«): Gemeint sind teils Fluren, Gräben oder Wüstungen in der Nähe des genannten Ortes; Mehrfachnennungen eines Ortes in einer Liste zählen einmal. Die Zahl der Sagenorte enthält auch Wüstungen und Weiler, die Bezugsgröße (Dörfer, Märkte, Städte) nicht; die Quote je 100 Siedlungen ist daher ein grober Anhalt. Orte ohne Eintrag in Gazetteer oder Ortsregister (z. B. Loitsch, Markersdorf, Wertheln, Grüne) fehlen; die Zuordnung zum Landestheil ist abgeleitet, nicht gedruckt.",
            "The place lists are drawn editorially from prose (“bei Pohlen”, “in der Wüstung Kämmera”): in part fields, ditches or deserted places near the named place are meant; repeated mentions of a place within a list count once. The number of legend places also includes deserted places and hamlets, the reference (villages, market towns, towns) does not; the rate per 100 settlements is therefore a rough guide only. Places without an entry in the gazetteer or register (e.g. Loitsch, Markersdorf, Wertheln, Grüne) are missing; the assignment to a district is derived, not printed.",
        ),
    ],
    "datasets": [
        {
            "name": "sites",
            "title": bi("Orte in Brückners Sagenlisten", "Places in Brückner’s legend lists"),
            "columns": [
                {"name": "type_de", "label": bi("Sagentyp (de)", "Legend type (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "type_en", "label": bi("Sagentyp (en)", "Legend type (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "place", "label": bi("Ort (wie genannt)", "Place (as named)"), "type": "string", "unit": None},
                {"name": "gazetteer_name", "label": bi("Ort (Gazetteer-Name)", "Place (gazetteer name)"), "type": "string", "unit": None, "derived": True},
                {"name": "district", "label": bi("Landestheil", "District"), "type": "string", "unit": None, "derived": True},
                {"name": "district_basis", "label": bi("Quelle der Zuordnung", "Basis of assignment"), "type": "string", "unit": None, "derived": True},
                {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": src,
        },
        {
            "name": "places",
            "title": bi("Orte nach Zahl der Sagenlisten", "Places by number of legend lists"),
            "columns": [
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None, "derived": True},
                {"name": "district", "label": bi("Landestheil", "District"), "type": "string", "unit": None, "derived": True},
                {"name": "lists", "label": bi("Zahl der Listen", "Number of lists"), "type": "integer", "unit": "Listen", "derived": True},
            ],
            "rows": rows_pl,
            "source_refs": src,
        },
        {
            "name": "districts",
            "title": bi("Landestheile: Sagenorte im Verhältnis zu den Siedlungen", "Districts: legend places relative to settlements"),
            "columns": [
                {"name": "district", "label": bi("Landestheil", "District"), "type": "string", "unit": None, "derived": True},
                {"name": "settlements", "label": bi("Dörfer, Märkte, Städte (Gazetteer)", "Villages, market towns, towns (gazetteer)"), "type": "integer", "unit": "Orte", "derived": True},
                {"name": "legend_places", "label": bi("Verschiedene Sagenorte", "Distinct legend places"), "type": "integer", "unit": "Orte", "derived": True},
                {"name": "per_100", "label": bi("Sagenorte je 100 Siedlungen", "Legend places per 100 settlements"), "type": "number", "unit": "Orte", "derived": True},
                {"name": "entries", "label": bi("Einträge in den Listen", "Entries in the lists"), "type": "integer", "unit": "Einträge", "derived": True},
                {"name": "entries_pct", "label": bi("Anteil der Einträge", "Share of the entries"), "type": "number", "unit": "%", "derived": True},
                {"name": "settlements_pct", "label": bi("Anteil der Siedlungen", "Share of the settlements"), "type": "number", "unit": "%", "derived": True},
            ],
            "rows": rows_d,
            "source_refs": src,
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "sites",
            "title": bi("Sagenorte je Typ und Landestheil", "Legend places per type and district"),
            "caption": bi(
                "Zahl der in Brückners Listen genannten Orte, nach Sagentyp und Landestheil (derselbe Ort kann in mehreren Listen stehen). Im Landestheil Gera liegt in jeder Liste die Mehrzahl.",
                "Number of places named in Brückner’s lists, by legend type and district (the same place can appear in several lists). In the district of Gera lies the majority in every list.",
            ),
            "vegalite": {
                "height": 340,
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "type_de", "en": "type_en"}, "type": "nominal", "sort": [t["de"] for t in TYPE_DOMAIN], "title": None, "axis": {"labelLimit": 420}},
                    "x": {"aggregate": "count", "type": "quantitative", "title": bi("Orte", "Places"), "axis": {"tickMinStep": 1}},
                    "color": {"field": "district", "type": "nominal", "title": bi("Landestheil", "District"), "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 400}},
                    "tooltip": [
                        {"field": {"de": "type_de", "en": "type_en"}, "title": bi("Sagentyp", "Legend type")},
                        {"field": "district", "title": bi("Landestheil", "District")},
                        {"aggregate": "count", "title": bi("Orte", "Places")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "districts",
            "title": bi("Sagenorte im Verhältnis zur Zahl der Siedlungen", "Legend places relative to the number of settlements"),
            "caption": bi(
                "Verschiedene Sagenorte je 100 Dörfer, Märkte und Städte des Landestheils. Auch im Verhältnis zur Größe liegt Gera vorn; Lobenstein-Ebersdorf bleibt deutlich zurück, was zu Brückners Hinweis auf die noch lückenhafte Sammlung passt.",
                "Distinct legend places per 100 villages, market towns and towns of the district. Gera also leads relative to size; Lobenstein-Ebersdorf stays far behind, which fits Brückner’s remark on the still incomplete collection.",
            ),
            "vegalite": {
                "height": 240,
                "mark": "bar",
                "encoding": {
                    "x": {"field": "district", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labelAngle": 0, "labelLimit": 400}},
                    "y": {"field": "per_100", "type": "quantitative", "title": bi("Sagenorte je 100 Siedlungen", "Legend places per 100 settlements")},
                    "color": {"field": "district", "type": "nominal", "legend": None, "scale": {"domain": LT_ORDER}},
                    "tooltip": [
                        {"field": "district", "title": bi("Landestheil", "District")},
                        {"field": "legend_places", "title": bi("Sagenorte", "Legend places")},
                        {"field": "settlements", "title": bi("Siedlungen", "Settlements")},
                        {"field": "per_100", "title": bi("Je 100 Siedlungen", "Per 100 settlements")},
                    ],
                },
            },
        },
        {
            "id": "c3",
            "dataset": "places",
            "title": bi("Orte mit den meisten Sagentypen", "Places with the most legend types"),
            "caption": bi(
                "Orte, die in mindestens drei der acht Sagenlisten vorkommen (Zahl der Listen).",
                "Places that appear in at least three of the eight legend lists (number of lists).",
            ),
            "vegalite": {
                "height": 300,
                "transform": [{"filter": "datum.lists >= 3"}],
                "mark": "bar",
                "encoding": {
                    "y": {"field": "place", "type": "nominal", "sort": {"field": "lists", "order": "descending"}, "title": None},
                    "x": {"field": "lists", "type": "quantitative", "title": bi("Zahl der Sagenlisten", "Number of legend lists"), "axis": {"tickMinStep": 1}},
                    "color": {"field": "district", "type": "nominal", "title": bi("Landestheil", "District"), "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 400}},
                    "tooltip": [
                        {"field": "place", "title": bi("Ort", "Place")},
                        {"field": "district", "title": bi("Landestheil", "District")},
                        {"field": "lists", "title": bi("Listen", "Lists")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Sagen", "Sagenorte", "Wiedenheer", "Hexen", "Weiße Frau", "Schätze", "Zauberer", "Irrlichter", "Gera", "Landestheile"],
        "en": ["legends", "legend sites", "Wild Hunt", "witches", "white lady", "treasures", "sorcerers", "will-o’-the-wisps", "Gera", "districts"],
    },
    "related": ["kultur-volkskalender-bauernjahr"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
