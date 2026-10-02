"""G7 analysis 3: crafts and trades in the places (frequency, regional profile, weaving cluster)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
from trades import *
import collections

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)
byu = {uid(e): e for e in U}

# ---- per place and canonical trade ------------------------------------------------------------
rec = collections.OrderedDict()   # uid -> canon -> [count, [verbatim pieces]]
for e in U:
    u = uid(e)
    d = collections.OrderedDict()
    for k, v in (e.get("crafts") or {}).items():
        c = canon(k)
        if c and isinstance(v, (int, float)) and v > 0:
            x = d.setdefault(c, [0, []])
            x[0] += v
            x[1].append(f"{k} {v}")
    for k, v in (e.get("occupations") or {}).items():
        if k in ("Webermeister", "Weber") and v > 0:
            x = d.setdefault("Weber", [0, []])
            x[0] += v
            x[1].append(f"{k} {v} (Berufsangabe)")
    rec[u] = d

base = {lt: sum(eff(e)[0] for e in U if e["landestheil"] == lt) for lt in LT_ORDER}
n_places = len(U)

trade_places = collections.defaultdict(set)
trade_masters = collections.Counter()
trade_lt = collections.defaultdict(collections.Counter)
trade_lt_places = collections.defaultdict(collections.Counter)
for u, d in rec.items():
    lt = byu[u]["landestheil"]
    for c, (n, _) in d.items():
        trade_places[c].add(u)
        trade_masters[c] += n
        trade_lt[c][lt] += n
        trade_lt_places[c][lt] += 1
total_masters = sum(trade_masters.values())
ranked = sorted(trade_places, key=lambda c: (-len(trade_places[c]), -trade_masters[c]))
top20 = ranked[:20]
top14 = ranked[:14]
for_c1 = top20

# ---- datasets -------------------------------------------------------------------------------------
long_rows = []
for e in U:
    u = uid(e)
    inh, hou = eff(e)
    lon, lat, gn = coord(e, C)
    for c, (n, vs) in rec[u].items():
        g, en = info(c)
        long_rows.append([u, e["name"], e["landestheil"], place_class(e), inh, c, en, g, n, "; ".join(vs),
                          lon, lat, e["start"]["page"], e["start"]["block"]])
long_cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("trade_de", "Gewerbe", "Trade", "string", derived=True, note="vereinheitlichte Bezeichnung"),
    col("trade_en", "Gewerbe (en)", "Trade (en)", "string", derived=True),
    col("group_order", "Gruppe (Nr.)", "Group (no.)", "integer", derived=True),
    col("count", "Gewerbetreibende", "Craftsmen", "integer", "Personen", derived=True, note="Summe der gedruckten Angaben (ohne Gesellen)"),
    col("verbatim", "Gedruckte Angaben", "Printed entries", "string"),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]

sum_rows = []
for i, c in enumerate(top20, start=1):
    g, en = info(c)
    sum_rows.append([i, c, en, g, GROUPS[g][0], GROUPS[g][1], len(trade_places[c]), round(100 * len(trade_places[c]) / n_places, 1), trade_masters[c]])
sum_cols = [
    col("rank", "Rang", "Rank", "integer", derived=True),
    col("trade_de", "Gewerbe", "Trade", "string", derived=True),
    col("trade_en", "Gewerbe (en)", "Trade (en)", "string", derived=True),
    col("group_order", "Gruppe (Nr.)", "Group (no.)", "integer", derived=True),
    col("group_de", "Gruppe", "Group", "string", derived=True),
    col("group_en", "Gruppe (en)", "Group (en)", "string", derived=True),
    col("places", "Orte mit dem Gewerbe", "Places with the trade", "integer", "Orte", derived=True),
    col("places_pct", "Anteil der 173 Orte", "Share of the 173 places", "number", "%", derived=True),
    col("masters", "Gewerbetreibende insgesamt", "Craftsmen in total", "integer", "Personen", derived=True),
]

dens_rows = []
for i, c in enumerate(top14, start=1):
    g, en = info(c)
    for lt in LT_ORDER:
        m = trade_lt[c][lt]
        dens_rows.append([i, c, en, g, lt, trade_lt_places[c][lt], m, base[lt], round(1000 * m / base[lt], 2)])
dens_cols = [
    col("trade_order", "Rang nach Orten", "Rank by places", "integer", derived=True),
    col("trade_de", "Gewerbe", "Trade", "string", derived=True),
    col("trade_en", "Gewerbe (en)", "Trade (en)", "string", derived=True),
    col("group_order", "Gruppe (Nr.)", "Group (no.)", "integer", derived=True),
    col("landestheil", "Landestheil", "District", "string"),
    col("places", "Orte mit dem Gewerbe", "Places with the trade", "integer", "Orte", derived=True),
    col("masters", "Gewerbetreibende", "Craftsmen", "integer", "Personen", derived=True),
    col("population", "Einwohner der Orte des Landestheils", "Inhabitants of the district's places", "integer", "Personen", derived=True),
    col("per_1000", "je 1 000 Einwohner", "per 1,000 inhabitants", "number", "je 1 000 Einw.", derived=True),
]

weav_rows = []
for e in U:
    u = uid(e)
    inh, hou = eff(e)
    w = rec[u].get("Weber", [0, []])
    lon, lat, gn = coord(e, C)
    weav_rows.append([u, e["name"], e["landestheil"], inh, w[0], round(100 * w[0] / inh, 2), "; ".join(w[1]), lon, lat,
                      e["start"]["page"], e["start"]["block"]])
weav_cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("weavers", "Weber (Meister)", "Weavers (masters)", "integer", "Personen", derived=True, note="Weber, Leinweber, Webermeister; ohne Gesellen; 0 = keine genannt"),
    col("weavers_per_100", "Weber je 100 Einwohner", "Weavers per 100 inhabitants", "number", "je 100 Einw.", derived=True),
    col("verbatim", "Gedruckte Angaben", "Printed entries", "string"),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
refs = uniq_refs(U)

# ---- statistics ----------------------------------------------------------------------------------
def pl(c):
    return len(trade_places[c])


wv = trade_masters["Weber"]
w_sorted = sorted(weav_rows, key=lambda r: -r[4])
w_top4 = [r for r in w_sorted if r[2] == "Schleiz"][:4]
w_top4_names = ", ".join(r[1] for r in w_top4)
w_top4_share = 100 * sum(r[4] for r in w_top4) / wv
n_weav_places = sum(1 for r in weav_rows if r[4] > 0)
w_gera_city = [r for r in weav_rows if r[1] == "Gera"][0][4]
w_dens = {lt: 1000 * trade_lt["Weber"][lt] / base[lt] for lt in LT_ORDER}
dach = {lt: 1000 * trade_lt["Dachdecker"][lt] / base[lt] for lt in LT_ORDER}
maur = {lt: 1000 * trade_lt["Maurer"][lt] / base[lt] for lt in LT_ORDER}
zimm = {lt: 1000 * trade_lt["Zimmerer"][lt] / base[lt] for lt in LT_ORDER}
bau_lob = 1000 * sum(trade_lt[c]["Lobenstein-Ebersdorf"] for c in ("Maurer", "Zimmerer", "Dachdecker")) / base["Lobenstein-Ebersdorf"]
bau_oth = 1000 * sum(trade_lt[c][lt] for c in ("Maurer", "Zimmerer", "Dachdecker") for lt in ("Gera", "Schleiz")) / (base["Gera"] + base["Schleiz"])
schn = {lt: 1000 * trade_lt["Schneider"][lt] / base[lt] for lt in LT_ORDER}
tr_names = lambda cs, lang="de": ", ".join(info(c)[1] if lang == "en" else c for c in cs)
top5 = ranked[:5]


def f1(x):
    return fnum(x, 1)


def e1(x):
    return fnum(x, 1, "en")


findings = [
    bi(f"Die häufigsten Gewerbe sind die des Alltags: {', '.join(f'{c} ({pl(c)} Orte)' for c in top5[:3])}, {top5[3]} ({pl(top5[3])}) und {top5[4]} ({pl(top5[4])}) – das Maurerhandwerk allein kommt in {fnum(100*pl('Maurer')/n_places,0)} % der {n_places} Orte vor. Die Artikel nennen insgesamt {fnum(total_masters)} Gewerbetreibende (ohne Gesellen) in {len(trade_places)} unterschiedenen Gewerben.",
       f"The most frequent trades are everyday ones: {', '.join(f'{info(c)[1].lower()} ({pl(c)} places)' for c in top5[:3])}, {info(top5[3])[1].lower()} ({pl(top5[3])}) and {info(top5[4])[1].lower()} ({pl(top5[4])}); masonry alone occurs in {fnum(100*pl('Maurer')/n_places,0,'en')}% of the {n_places} places. The articles name {fnum(total_masters,0,'en')} craftsmen in total (journeymen excluded) in {len(trade_places)} distinct trades."),
    bi(f"Das Weben ist das größte Gewerbe: {fnum(wv)} Weber (Meister) in {n_weav_places} Orten, das sind {pct(100*wv/total_masters,0)} aller genannten Gewerbetreibenden. Auf 1 000 Einwohner kommen im Landestheil Schleiz {f1(w_dens['Schleiz'])} Weber, in Gera {f1(w_dens['Gera'])} und in Lobenstein-Ebersdorf {f1(w_dens['Lobenstein-Ebersdorf'])}.",
       f"Weaving is the largest trade: {fnum(wv,0,'en')} weavers (masters) in {n_weav_places} places, or {pct(100*wv/total_masters,0,'en')} of all craftsmen named. Per 1,000 inhabitants there are {e1(w_dens['Schleiz'])} weavers in the district of Schleiz, {e1(w_dens['Gera'])} in Gera and {e1(w_dens['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf."),
    bi(f"Das Weberei-Gebiet liegt im Landestheil Schleiz um Hohenleuben, Langenwetzendorf und Triebes: {w_top4_names} stellen zusammen {pct(w_top4_share,0)} aller Weber; außerhalb davon nennt die Stadt Gera {w_gera_city} Zeug- und Leinweber und der Marktflecken Langenberg {[r for r in weav_rows if r[1]=='Langenberg'][0][4]}.",
       f"The weaving area lies in the district of Schleiz around Hohenleuben, Langenwetzendorf and Triebes: {w_top4_names} together account for {pct(w_top4_share,0,'en')} of all weavers; outside it the town of Gera names {w_gera_city} cloth and linen weavers and the market place Langenberg {[r for r in weav_rows if r[1]=='Langenberg'][0][4]}."),
    bi(f"Im Landestheil Lobenstein-Ebersdorf prägen Bau- und Dachdeckerhandwerk das Bild: {f1(dach['Lobenstein-Ebersdorf'])} Dachdecker (überwiegend Schieferdecker) je 1 000 Einwohner gegen {f1(dach['Gera'])} in Gera und {f1(dach['Schleiz'])} in Schleiz, dazu {f1(maur['Lobenstein-Ebersdorf'])} Maurer (Gera {f1(maur['Gera'])}); Maurer, Zimmerer und Dachdecker zusammen stellen dort {f1(bau_lob)} je 1 000 Einwohner gegenüber {f1(bau_oth)} in den beiden anderen Landestheilen.",
       f"In the district of Lobenstein-Ebersdorf the building and roofing trades dominate: {e1(dach['Lobenstein-Ebersdorf'])} roofers (mostly slaters) per 1,000 inhabitants against {e1(dach['Gera'])} in Gera and {e1(dach['Schleiz'])} in Schleiz, plus {e1(maur['Lobenstein-Ebersdorf'])} masons (Gera {e1(maur['Gera'])}); masons, carpenters and roofers together reach {e1(bau_lob)} per 1,000 inhabitants there against {e1(bau_oth)} in the other two districts."),
    bi(f"Schneider sind im Unterland häufiger ({f1(schn['Gera'])} je 1 000 Einwohner) als in Schleiz ({f1(schn['Schleiz'])}) und Lobenstein-Ebersdorf ({f1(schn['Lobenstein-Ebersdorf'])}); die Strumpfwirker konzentrieren sich im Landestheil Schleiz ({f1(1000*trade_lt['Strumpfwirker']['Schleiz']/base['Schleiz'])} je 1 000 Einwohner, in Gera keiner genannt).",
       f"Tailors are more frequent in the lowland ({e1(schn['Gera'])} per 1,000 inhabitants) than in Schleiz ({e1(schn['Schleiz'])}) and Lobenstein-Ebersdorf ({e1(schn['Lobenstein-Ebersdorf'])}); stocking weavers concentrate in the district of Schleiz ({e1(1000*trade_lt['Strumpfwirker']['Schleiz']/base['Schleiz'])} per 1,000 inhabitants, none named in Gera)."),
]

GRP = {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "title": bi("Gewerbegruppe", "Trade group"),
       "sort": {"field": "group_order", "op": "min"}, "legend": {"labelLimit": 300, "columns": 3}}
TRADE_Y = lambda sortfield: {"field": {"de": "trade_de", "en": "trade_en"}, "type": "nominal",
                             "sort": {"field": sortfield, "op": "min"}, "title": None}
charts = [
    {"id": "c1", "dataset": "trade_summary",
     "title": bi("Die 20 häufigsten Gewerbe der Orte", "The 20 most frequent trades of the places"),
     "caption": bi(f"Zahl der Orte (von {n_places}), in denen die Artikel das Gewerbe nennen; Gesellen nicht mitgezählt. Die Zahl der Gewerbetreibenden steht im Tooltip und im Datensatz.",
                   f"Number of places (of {n_places}) whose articles name the trade; journeymen are not counted. The number of craftsmen is given in the tooltip and the dataset."),
     "vegalite": {"height": 440, "mark": "bar", "encoding": {
         "y": TRADE_Y("rank"),
         "x": {"field": "places", "type": "quantitative", "title": bi("Orte mit dem Gewerbe", "Places with the trade")},
         "color": GRP,
         "tooltip": [{"field": {"de": "trade_de", "en": "trade_en"}, "title": bi("Gewerbe", "Trade")},
                     {"field": "places", "title": bi("Orte", "Places")},
                     {"field": "places_pct", "title": bi("Anteil der Orte (%)", "Share of places (%)")},
                     {"field": "masters", "title": bi("Gewerbetreibende", "Craftsmen")}]}}},
    {"id": "c2", "dataset": "trade_density",
     "title": bi("Gewerbedichte nach Landestheil", "Trade density by district"),
     "caption": bi("Gewerbetreibende je 1 000 Einwohner der Orte des Landestheils (Fläche und Zahl). Weber im Landestheil Schleiz und Dachdecker in Lobenstein-Ebersdorf heben sich ab; die Alltagsgewerbe sind überall vertreten.",
                   "Craftsmen per 1,000 inhabitants of the district's places (area and figure). Weavers in the district of Schleiz and roofers in Lobenstein-Ebersdorf stand out; the everyday trades occur everywhere."),
     "vegalite": {"height": 440, "encoding": {
         "y": TRADE_Y("trade_order"),
         "x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labelAngle": 0, "orient": "top"}}},
         "layer": [
             {"mark": {"type": "circle", "opacity": 0.8},
              "encoding": {"size": {"field": "per_1000", "type": "quantitative", "title": bi("je 1 000 Einwohner", "per 1,000 inhabitants"),
                                    "scale": {"type": "sqrt", "range": [8, 1500], "domain": [0, 65]}, "legend": {"values": [1, 10, 50], "format": "d"}},
                           "color": {"field": "landestheil", "type": "nominal", "scale": {"domain": LT_ORDER}, "legend": None},
                           "tooltip": [{"field": {"de": "trade_de", "en": "trade_en"}, "title": bi("Gewerbe", "Trade")},
                                       {"field": "landestheil", "title": bi("Landestheil", "District")},
                                       {"field": "masters", "title": bi("Gewerbetreibende", "Craftsmen")},
                                       {"field": "places", "title": bi("Orte", "Places")},
                                       {"field": "per_1000", "title": bi("je 1 000 Einwohner", "per 1,000 inhabitants"), "format": ".1f"}]}},
             {"mark": {"type": "text", "align": "left", "dx": 24, "fontSize": 10},
              "encoding": {"text": {"field": "per_1000", "type": "quantitative", "format": ".1f"}}},
         ]}},
    {"id": "c3", "dataset": "weaver_places",
     "title": bi("Das Weberei-Gebiet", "The weaving area"),
     "caption": bi("Weber (Meister) je Ort; Fläche nach Zahl, Farbe nach Landestheil; kleine blasse Punkte: Orte ohne Weberangabe. Beschriftet sind Orte mit mindestens 100 Webern. Koordinaten aus GeoNames.",
                   "Weavers (masters) per place; area by number, colour by district; small pale dots: places without weaver figures. Places with at least 100 weavers are labelled. Coordinates from GeoNames."),
     "vegalite": {"height": 460, "projection": {"type": "mercator"}, "layer": [
         {"transform": [{"filter": "isValid(datum.lat) && datum.weavers > 0"}],
          "mark": {"type": "circle", "opacity": 0.75},
          "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                       "size": {"field": "weavers", "type": "quantitative", "title": bi("Weber", "Weavers"),
                                "scale": {"type": "sqrt", "range": [20, 1800], "domain": [0, 420]}, "legend": {"values": [10, 100, 400], "format": "d"}},
                       "color": {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
                                 "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}},
                       "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                                   {"field": "landestheil", "title": bi("Landestheil", "District")},
                                   {"field": "weavers", "title": bi("Weber (Meister)", "Weavers (masters)")},
                                   {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants")},
                                   {"field": "weavers_per_100", "title": bi("Weber je 100 Einwohner", "Weavers per 100 inhabitants")},
                                   {"field": "page", "title": bi("Seite", "Page")}]}},
         {"transform": [{"filter": "isValid(datum.lat) && datum.weavers == 0"}],
          "mark": {"type": "circle", "size": 28, "opacity": 0.28},
          "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                       "color": {"field": "landestheil", "type": "nominal", "scale": {"domain": LT_ORDER}}}},
         {"transform": [{"filter": "isValid(datum.lat) && datum.weavers >= 100"}],
          "mark": {"type": "text", "align": "left", "dx": 16, "dy": -3, "fontSize": 10},
          "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                       "text": {"field": "name"}}},
     ]}},
]

a = {
    "id": "orte-handwerk-gewerbe-doerfer",
    "title": bi("Handwerk und Gewerbe in den Orten", "Crafts and trades in the places"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Fast jeder Ortsartikel zählt die ansässigen Handwerker nach Gewerben auf. Aus den Angaben zu {n_places} Orten ergibt sich, welche Gewerbe überall zu finden sind (Maurer, Zimmerer, Schuhmacher, Schneider, Schmiede), wie sich die drei Landestheile unterscheiden und wo sich die Weberei konzentriert.",
        f"Almost every place article lists the resident craftsmen by trade. The data on {n_places} places show which trades are found everywhere (masons, carpenters, shoemakers, tailors, smiths), how the three districts differ and where weaving is concentrated."),
    "method": bi(
        f"Grundlage sind die Felder crafts (Gewerbe mit Zahl) und, für die Weberei, occupations (Webermeister) der Gazetteer-Einträge der {n_places} Gemeinden (G1–G6). Die gedruckten Berufsbezeichnungen wurden zu {len(trade_places)} Gewerben vereinheitlicht (z. B. Zimmerleute, Zimmermann, Zimmerer; Schieferdecker, Dachdecker; Schmied, Schmiede, Hufschmied; Weber, Leinweber, Zeug- und Leinweber, Webermeister; Wirth, Wirthe); die Zuordnung steht je Ort in der Spalte verbatim. Gesellen, Gehilfen und Lehrlinge (z. B. Maurergesellen, Zimmergesellen, Webergesellen) wurden nicht mitgezählt, ebenso nicht die Berufsklassen (Handwerker, Kapitalisten, Dienstboten). Wo mehrere Schreibweisen im selben Artikel stehen, wurden die Zahlen addiert. Die Gruppierung der Gewerbe (Bau und Stein, Holz, Metall, Textil, Leder und Kleidung, Nahrung und Wirte, Übrige) ist eine Zuordnung der Auswertung. Die Gewerbedichte setzt die Gewerbetreibenden eines Landestheils in Beziehung zu den Einwohnern aller Gemeinden des Landestheils ({fnum(base['Gera'])}, {fnum(base['Schleiz'])} und {fnum(base['Lobenstein-Ebersdorf'])}); Orte, deren Artikel keine Gewerbe nennt (6 Orte), gehen mit null Gewerbetreibenden ein. Alle Zahlen zu Gewerbetreibenden sind Summen der gedruckten Angaben (derived), die Koordinaten stammen aus GeoNames.",
        f"The basis are the fields crafts (trades with numbers) and, for weaving, occupations (master weavers) of the gazetteer entries of the {n_places} municipalities (G1–G6). The printed names of the occupations were combined into {len(trade_places)} trades (e.g. Zimmerleute, Zimmermann, Zimmerer; Schieferdecker, Dachdecker; Schmied, Schmiede, Hufschmied; Weber, Leinweber, Zeug- und Leinweber, Webermeister; Wirth, Wirthe); the assignment is given per place in the column verbatim. Journeymen, assistants and apprentices (e.g. Maurergesellen, Zimmergesellen, Webergesellen) were not counted, nor were the occupational classes (Handwerker, Kapitalisten, Dienstboten). Where several spellings occur in the same article the figures were added. The grouping of the trades (building and stone, wood, metal, textiles, leather and clothing, food and innkeepers, other) is an assignment of this analysis. Trade density relates the craftsmen of a district to the inhabitants of all municipalities of the district ({fnum(base['Gera'],0,'en')}, {fnum(base['Schleiz'],0,'en')} and {fnum(base['Lobenstein-Ebersdorf'],0,'en')}); places whose article names no trades (6 places) enter with zero craftsmen. All figures on craftsmen are sums of the printed figures (derived); coordinates come from GeoNames."),
    "findings": findings,
    "caveats": [
        bi("Die Artikel nennen die Gewerbe mit sehr unterschiedlicher Vollständigkeit; Zahlenangaben wie 'über 20 Steinhauer' (Harpersdorf) oder 'mehrere' wurden nur als genannte Zahl bzw. gar nicht übernommen. Brückner führt für Gera die Handwerkerzahl 1 120 an, während die einzeln genannten Gewerbe 1 174 ergeben (Hinweis im Gazetteer-Eintrag).",
           "The articles name the trades with very different completeness; statements such as 'more than 20 stonecutters' (Harpersdorf) or 'several' were taken only as the number given or not at all. For Gera Brückner gives 1,120 craftsmen, whereas the trades named individually add up to 1,174 (note in the gazetteer entry)."),
        bi("Bei Weberei und Tuchmacherei unterscheiden die Artikel nicht einheitlich zwischen Meistern, Gesellen und Hausindustrie; in Hohenleuben, Langenwetzendorf, Triebes und Tanna sind es 'Webermeister', in Gera 'Zeug- und Leinweber', in Lobenstein werden 121 Tuchmacher gesondert genannt (hier unter Tuchmacher, nicht unter Weber).",
           "For weaving and cloth making the articles do not distinguish uniformly between masters, journeymen and cottage industry; in Hohenleuben, Langenwetzendorf, Triebes and Tanna they are 'Webermeister', in Gera 'Zeug- und Leinweber', and in Lobenstein 121 cloth makers are named separately (counted under Tuchmacher here, not under Weber)."),
        bi("Wirte, Krämer und Händler stehen in manchen Artikeln unter den Gewerben, in anderen unter den Berufsgruppen; ihre Zahlen sind nicht vergleichbar.",
           "Innkeepers, shopkeepers and dealers appear under the trades in some articles and under the occupational groups in others; their figures are not comparable."),
    ],
    "datasets": [
        {"name": "trade_summary", "title": bi("Die 20 häufigsten Gewerbe", "The 20 most frequent trades"),
         "columns": sum_cols, "rows": sum_rows, "source_refs": refs},
        {"name": "trade_density", "title": bi("Gewerbetreibende je Landestheil und 1 000 Einwohner (14 häufigste Gewerbe)", "Craftsmen per district and 1,000 inhabitants (14 most frequent trades)"),
         "columns": dens_cols, "rows": dens_rows, "source_refs": refs},
        {"name": "weaver_places", "title": bi("Weber je Gemeinde", "Weavers per municipality"),
         "columns": weav_cols, "rows": weav_rows, "source_refs": refs},
        {"name": "trades_long", "title": bi("Gewerbetreibende je Ort und Gewerbe", "Craftsmen per place and trade"),
         "columns": long_cols, "rows": long_rows, "source_refs": refs},
    ],
    "charts": charts,
    "keywords": {"de": ["Handwerk", "Gewerbe", "Weber", "Weberei", "Maurer", "Schieferdecker", "Handwerker", "Dörfer"],
                 "en": ["crafts", "trades", "weavers", "weaving", "masons", "slaters", "craftsmen", "villages"]},
    "related": ["industrie-gewerbe-1864-einzelne-gewerbe", "handel-gewerbe-nach-landesteilen-1864", "orte-sozialstruktur-doerfer-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
