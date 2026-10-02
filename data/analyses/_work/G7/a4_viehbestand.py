"""G7 analysis 4: livestock in the places 1867 (per district, per 100 inhabitants, per 100 Morgen)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
import collections

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)
SPECIES = [("Rinder", "Rinder", "Cattle"), ("Schafe", "Schafe", "Sheep"), ("Gänse", "Gänse", "Geese"),
           ("Schweine", "Schweine", "Pigs"), ("Ziegen", "Ziegen", "Goats"), ("Pferde", "Pferde", "Horses"),
           ("Bienenstöcke", "Bienenstöcke", "Beehives")]
SP_IDX = {k: i for i, (k, _, _) in enumerate(SPECIES, start=1)}

# ---- Part I table (p. 233/234): 1867 rows ---------------------------------------------------------
def grid(file, block):
    p = json.load(open(ROOT / "data" / "pages" / file, encoding="utf-8"))
    return next(b for b in p["blocks"] if b["id"] == block)["grid"]


def n(x):
    return int(str(x).replace(",", "").strip())


g233 = grid("0245.json", "b4")
g234 = grid("0246.json", "b1")
row = {"Gera": g233[12], "Schleiz": g233[22], "Lobenstein-Ebersdorf": g234[11], "Fürstenthum": g234[18]}
assert all(r[0] == "1867" for r in row.values())
# columns: Pferde, Fuellen, Stiere, Ochsen, Kuehe, Jungvieh, Schafe ganz, halb, unveredelt, Boecke u. Ziegen, Schweine
PART1 = {}
for lt, r in row.items():
    v = [n(x) for x in r[1:]]
    PART1[lt] = {"Pferde": v[0] + v[1], "Rinder": v[2] + v[3] + v[4] + v[5], "Schafe": v[6] + v[7] + v[8],
                 "Ziegen": v[9], "Schweine": v[10]}

G_UNV_IMPLIED = n(row['Fürstenthum'][9]) - n(row['Schleiz'][9]) - n(row['Lobenstein-Ebersdorf'][9])   # Gera unimproved sheep implied by the Fuerstenthum row
G_SHEEP_IMPLIED = n(row['Gera'][7]) + n(row['Gera'][8]) + G_UNV_IMPLIED
# ---- place level ----------------------------------------------------------------------------------
wide, long_ = [], []
for e in U:
    lv = e.get("livestock")
    if not lv:
        continue
    u = uid(e)
    inh, hou = eff(e)
    lon, lat, gn = coord(e, C)
    pc = place_class(e)
    fl = e.get("flur_morgen")
    vals = {k: lv.get(k) for k, _, _ in SPECIES}
    z = lambda k: vals[k] or 0
    wide.append([u, e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, round(fl, 2) if fl else None,
                 vals["Pferde"], vals["Rinder"], vals["Schafe"], vals["Schweine"], vals["Ziegen"], vals["Gänse"], vals["Bienenstöcke"],
                 round(100 * z("Rinder") / inh, 1), round(100 * z("Schafe") / inh, 1), lon, lat,
                 e["start"]["page"], e["start"]["block"]])
    for k, de, en in SPECIES:
        if vals[k] is None:
            continue
        long_.append([u, e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, SP_IDX[k], de, en, vals[k],
                      round(100 * vals[k] / inh, 2), round(100 * vals[k] / fl, 2) if fl else None,
                      e["start"]["page"], e["start"]["block"]])
refs = uniq_refs([e for e in U if e.get("livestock")])
n_pl = len(wide)

wcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("flur_morgen", "Flur", "Field area", "number", "Morgen", derived=True, note="gedruckte gemischte Zahlen (z. B. 706 7/13) in Dezimalzahlen umgerechnet"),
    col("horses", "Pferde", "Horses", "integer", "Stück", note="leer = nicht genannt"),
    col("cattle", "Rinder", "Cattle", "integer", "Stück", note="leer = nicht genannt"),
    col("sheep", "Schafe", "Sheep", "integer", "Stück", note="leer = nicht genannt"),
    col("pigs", "Schweine", "Pigs", "integer", "Stück", note="leer = nicht genannt"),
    col("goats", "Ziegen", "Goats", "integer", "Stück", note="leer = nicht genannt"),
    col("geese", "Gänse", "Geese", "integer", "Stück", note="leer = nicht genannt"),
    col("beehives", "Bienenstöcke", "Beehives", "integer", "Stück", note="leer = nicht genannt"),
    col("cattle_per_100", "Rinder je 100 Einwohner", "Cattle per 100 inhabitants", "number", "je 100 Einw.", derived=True),
    col("sheep_per_100", "Schafe je 100 Einwohner", "Sheep per 100 inhabitants", "number", "je 100 Einw.", derived=True),
    col("lon", "Länge", "Longitude", "number", "° O", derived=True, note="GeoNames (coords.json)"),
    col("lat", "Breite", "Latitude", "number", "° N", derived=True, note="GeoNames (coords.json)"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
lcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("species_order", "Tierart (Nr.)", "Species (no.)", "integer", derived=True),
    col("species_de", "Tierart", "Species", "string", derived=True),
    col("species_en", "Tierart (en)", "Species (en)", "string", derived=True),
    col("count", "Bestand", "Number of animals", "integer", "Stück"),
    col("per_100_inh", "je 100 Einwohner", "per 100 inhabitants", "number", "je 100 Einw.", derived=True),
    col("per_100_morgen", "je 100 Morgen Flur", "per 100 Morgen of field area", "number", "je 100 Morgen", derived=True),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]

# district aggregates
dist_rows = []
agg = {}
for lt in LT_ORDER:
    ws = [r for r in wide if r[2] == lt]
    P = sum(r[5] for r in ws)
    for k, de, en in SPECIES:
        idx = {"Pferde": 7, "Rinder": 8, "Schafe": 9, "Schweine": 10, "Ziegen": 11, "Gänse": 12, "Bienenstöcke": 13}[k]
        tot = sum(r[idx] or 0 for r in ws)
        npl = sum(1 for r in ws if r[idx] is not None)
        agg[(lt, k)] = tot
        dist_rows.append([lt, SP_IDX[k], de, en, tot, npl, P, round(100 * tot / P, 2)])
dist_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("species_order", "Tierart (Nr.)", "Species (no.)", "integer", derived=True),
    col("species_de", "Tierart", "Species", "string", derived=True),
    col("species_en", "Tierart (en)", "Species (en)", "string", derived=True),
    col("animals", "Bestand (Summe der Orte)", "Animals (sum of the places)", "integer", "Stück", derived=True),
    col("places", "Orte mit Angabe", "Places with a figure", "integer", "Orte", derived=True),
    col("population", "Einwohner der Orte", "Inhabitants of the places", "integer", "Personen", derived=True),
    col("per_100", "je 100 Einwohner", "per 100 inhabitants", "number", "je 100 Einw.", derived=True),
]
chk_rows = []
for lt in LT_ORDER + ["Fürstenthum"]:
    for k in ["Pferde", "Rinder", "Schafe", "Ziegen", "Schweine"]:
        mine = agg[(lt, k)] if lt != "Fürstenthum" else sum(agg[(l, k)] for l in LT_ORDER)
        p1 = PART1[lt][k]
        de, en = [(d, e_) for kk, d, e_ in SPECIES if kk == k][0]
        chk_rows.append([lt, SP_IDX[k], de, en, mine, p1, mine - p1, round(100 * (mine - p1) / p1, 1)])
chk_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("species_order", "Tierart (Nr.)", "Species (no.)", "integer", derived=True),
    col("species_de", "Tierart", "Species", "string", derived=True),
    col("species_en", "Tierart (en)", "Species (en)", "string", derived=True),
    col("places_sum", "Summe der Ortsartikel", "Sum of the place articles", "integer", "Stück", derived=True),
    col("table_1867", "Tabelle Teil I, Zeile 1867", "Part I table, row 1867", "integer", "Stück", derived=True, note="Summe der gedruckten Spalten (Pferde + Füllen; Stiere + Ochsen + Kühe + Jungvieh; drei Schafspalten)"),
    col("diff", "Differenz", "Difference", "integer", "Stück", derived=True),
    col("diff_pct", "Differenz", "Difference", "number", "%", derived=True),
]

# ---- statistics -----------------------------------------------------------------------------------
per = {(r[0], r[2]): r[7] for r in dist_rows}
tot_sp = {k: sum(agg[(lt, k)] for lt in LT_ORDER) for k, _, _ in SPECIES}
n_cmp = sum(1 for r in chk_rows if r[0] != "Fürstenthum")
n_close = sum(1 for r in chk_rows if r[0] != "Fürstenthum" and abs(r[7]) <= 5)
cmp_ex = {(r[0], r[2]): r for r in chk_rows}
rural = [r for r in long_ if r[3] == "Dorf"]


def med(lt, sp, idx):
    v = [r[idx] for r in rural if r[2] == lt and r[7] == sp and r[idx] is not None]
    return median(v), len(v)


sheep_morgen = {lt: med(lt, "Schafe", 11)[0] for lt in LT_ORDER}
cattle_morgen = {lt: med(lt, "Rinder", 11)[0] for lt in LT_ORDER}
# villages with the largest sheep numbers per 100 inhabitants
sh = sorted([r for r in wide if r[3] == "Dorf"], key=lambda r: -r[15])
n_sheep200 = sum(1 for r in wide if r[3] == "Dorf" and r[15] >= 200)
sheep200_gera = sum(1 for r in wide if r[3] == "Dorf" and r[15] >= 200 and r[2] == "Gera")
n_geo = sum(1 for r in wide if r[16] is not None)
fn1 = lambda x: fnum(x, 1)
en1 = lambda x: fnum(x, 1, "en")

findings = [
    bi(f"Die Viehzahlen der {n_pl} Ortsartikel sind die der Zählung von 1867 und stimmen mit der Tabelle in Teil I gut überein: In {n_close} von {n_cmp} Vergleichen (Tierart × Landestheil) liegt die Summe der Orte innerhalb von 5 % der Tabellenzeile 1867, für Schleiz bei Pferden, Rindern, Schafen und Schweinen exakt; die Summe der Pferde (Pferde und Füllen) im Fürstenthum ({fnum(sum(agg[(l,'Pferde')] for l in LT_ORDER))}) entspricht der gedruckten Gesamtzeile ({fnum(PART1['Fürstenthum']['Pferde'])}).",
       f"The livestock figures of the {n_pl} place articles are those of the 1867 census and agree well with the table in Part I: in {n_close} of {n_cmp} comparisons (species × district) the sum of the places lies within 5% of the 1867 row of the table, for Schleiz exactly for horses, cattle, sheep and pigs; the sum of horses (horses and foals) in the principality ({fnum(sum(agg[(l,'Pferde')] for l in LT_ORDER),0,'en')}) equals the printed total row ({fnum(PART1['Fürstenthum']['Pferde'],0,'en')})."),
    bi(f"Rinder ({fnum(tot_sp['Rinder'])}), Schafe ({fnum(tot_sp['Schafe'])}) und Gänse ({fnum(tot_sp['Gänse'])}) sind in den Orten fast gleich zahlreich; es folgen Schweine ({fnum(tot_sp['Schweine'])}), Ziegen ({fnum(tot_sp['Ziegen'])}), Pferde ({fnum(tot_sp['Pferde'])}) und {fnum(tot_sp['Bienenstöcke'])} Bienenstöcke. Auf Gänse, die in keiner Zählung des Teils I erscheinen, geht damit ein ebenso großer Stückzahlanteil wie auf das Rindvieh.",
       f"Cattle ({fnum(tot_sp['Rinder'],0,'en')}), sheep ({fnum(tot_sp['Schafe'],0,'en')}) and geese ({fnum(tot_sp['Gänse'],0,'en')}) are almost equally numerous in the places; they are followed by pigs ({fnum(tot_sp['Schweine'],0,'en')}), goats ({fnum(tot_sp['Ziegen'],0,'en')}), horses ({fnum(tot_sp['Pferde'],0,'en')}) and {fnum(tot_sp['Bienenstöcke'],0,'en')} beehives. Geese, which appear in no census table of Part I, thus account for as many animals as cattle."),
    bi(f"Je 100 Einwohner halten die Orte im Landestheil Gera {fn1(per[('Gera','Schafe')])} Schafe und {fn1(per[('Gera','Pferde')])} Pferde, aber nur {fn1(per[('Gera','Rinder')])} Rinder; in Lobenstein-Ebersdorf sind es {fn1(per[('Lobenstein-Ebersdorf','Rinder')])} Rinder, aber nur {fn1(per[('Lobenstein-Ebersdorf','Pferde')])} Pferde (Schleiz: {fn1(per[('Schleiz','Rinder')])} Rinder, {fn1(per[('Schleiz','Pferde')])} Pferde). Ziegen, nach Brückner (S. 233) das Vieh der Armen ohne Feldboden, nehmen von {fn1(per[('Gera','Ziegen')])} (Gera) über {fn1(per[('Schleiz','Ziegen')])} (Schleiz) auf {fn1(per[('Lobenstein-Ebersdorf','Ziegen')])} (Lobenstein-Ebersdorf) je 100 Einwohner zu.",
       f"Per 100 inhabitants the places in the district of Gera keep {en1(per[('Gera','Schafe')])} sheep and {en1(per[('Gera','Pferde')])} horses but only {en1(per[('Gera','Rinder')])} cattle; in Lobenstein-Ebersdorf the figure is {en1(per[('Lobenstein-Ebersdorf','Rinder')])} cattle but only {en1(per[('Lobenstein-Ebersdorf','Pferde')])} horses (Schleiz: {en1(per[('Schleiz','Rinder')])} cattle, {en1(per[('Schleiz','Pferde')])} horses). Goats, according to Brückner (p. 233) the livestock of the poor without field land, increase from {en1(per[('Gera','Ziegen')])} (Gera) through {en1(per[('Schleiz','Ziegen')])} (Schleiz) to {en1(per[('Lobenstein-Ebersdorf','Ziegen')])} (Lobenstein-Ebersdorf) per 100 inhabitants."),
    bi(f"Bezogen auf die Flur zeigt sich ein anderes Bild: Im Median der Dörfer stehen auf 100 Morgen {fn1(sheep_morgen['Gera'])} Schafe im Landestheil Gera, {fn1(sheep_morgen['Schleiz'])} in Schleiz und {fn1(sheep_morgen['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf, aber {fn1(cattle_morgen['Gera'])}, {fn1(cattle_morgen['Schleiz'])} und {fn1(cattle_morgen['Lobenstein-Ebersdorf'])} Rinder. Die Rinderdichte ist also überall ähnlich, die Schafhaltung ist eine Besonderheit des Unterlandes.",
       f"Related to the field area the picture differs: the median village keeps {en1(sheep_morgen['Gera'])} sheep per 100 Morgen in the district of Gera, {en1(sheep_morgen['Schleiz'])} in Schleiz and {en1(sheep_morgen['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf, but {en1(cattle_morgen['Gera'])}, {en1(cattle_morgen['Schleiz'])} and {en1(cattle_morgen['Lobenstein-Ebersdorf'])} cattle. The density of cattle is thus similar everywhere, whereas sheep keeping is a peculiarity of the lowland."),
    bi(f"{n_sheep200} Dörfer halten mindestens 200 Schafe je 100 Einwohner, {sheep200_gera} davon im Landestheil Gera (Spitzenreiter {sh[0][1]} mit {fn1(sh[0][15])}); die Artikel vermerken mehrfach, dass die Schafe dem Vorwerk oder Kammergut gehören (z. B. Zschippern, Laasen). Solche Herden verzerren den Vergleich je Einwohner.",
       f"{n_sheep200} villages keep at least 200 sheep per 100 inhabitants, {sheep200_gera} of them in the district of Gera (top place {sh[0][1]} with {en1(sh[0][15])}); the articles repeatedly note that the sheep belong to the Vorwerk or Kammergut (e.g. Zschippern, Laasen). Such flocks distort the comparison per inhabitant."),
]

LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
SPY = {"field": {"de": "species_de", "en": "species_en"}, "type": "nominal", "sort": {"field": "species_order", "op": "min"}, "title": None}
charts = [
    {"id": "c1", "dataset": "livestock_district",
     "title": bi("Viehbestand je 100 Einwohner nach Landestheil", "Livestock per 100 inhabitants by district"),
     "caption": bi("Summe der Ortsartikel (Zählung 1867), bezogen auf die Einwohner aller Orte des Landestheils. Pferde und Bienenstöcke sind selten, bleiben aber sichtbar; die Tierarten sind nach Gesamtzahl geordnet.",
                   "Sum of the place articles (1867 census), related to the inhabitants of all places of the district. Horses and beehives are rare but remain visible; the species are ordered by total number."),
     "vegalite": {"height": 380, "mark": "bar", "encoding": {
         "y": SPY, "yOffset": {"field": "landestheil", "sort": LT_ORDER},
         "x": {"field": "per_100", "type": "quantitative", "title": bi("je 100 Einwohner", "per 100 inhabitants")},
         "color": LT_COLOR,
         "tooltip": [{"field": {"de": "species_de", "en": "species_en"}, "title": bi("Tierart", "Species")},
                     {"field": "landestheil", "title": bi("Landestheil", "District")},
                     {"field": "animals", "title": bi("Bestand", "Animals")},
                     {"field": "per_100", "title": bi("je 100 Einwohner", "per 100 inhabitants"), "format": ".1f"}]}}},
    {"id": "c2", "dataset": "livestock_long",
     "title": bi("Viehdichte der Dörfer je 100 Morgen Flur", "Livestock density of the villages per 100 Morgen of field area"),
     "caption": bi("Rinder, Schafe und Schweine je 100 Morgen Flur in den Dörfern (ohne die sechs Städte); Kasten: Median und Quartile, Punkte: Ausreißer. Brückners Morgen = 0,2553 ha (S. 832).",
                   "Cattle, sheep and pigs per 100 Morgen of field area in the villages (without the six towns); box: median and quartiles, dots: outliers. Brückner's Morgen = 0.2553 ha (p. 832)."),
     "vegalite": {"height": 300, "transform": [{"filter": "datum.class_de == 'Dorf' && isValid(datum.per_100_morgen) && (datum.species_de == 'Rinder' || datum.species_de == 'Schafe' || datum.species_de == 'Schweine')"}],
                  "mark": {"type": "boxplot", "extent": 1.5, "size": 16},
                  "encoding": {
                      "column": {"field": {"de": "species_de", "en": "species_en"}, "type": "nominal", "sort": {"field": "species_order", "op": "min"}, "title": None,
                                 "header": {"labelFontSize": 12}},
                      "x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labels": False, "ticks": False}},
                      "y": {"field": "per_100_morgen", "type": "quantitative", "title": bi("Stück je 100 Morgen", "animals per 100 Morgen")},
                      "color": LT_COLOR}}},
    {"id": "c3", "dataset": "livestock_places",
     "title": bi("Rinder und Schafe je 100 Einwohner", "Cattle and sheep per 100 inhabitants"),
     "caption": bi("Jeder Punkt ist ein Dorf (ohne Städte); beschriftet sind die Dörfer mit mehr als 300 Schafen je 100 Einwohner, die ihre Herde meist dem Rittergut oder Vorwerk verdanken. Das Unterland (blau) liegt hoch bei den Schafen, Schleiz und Lobenstein-Ebersdorf bei den Rindern.",
                   "Each dot is a village (without towns); villages with more than 300 sheep per 100 inhabitants are labelled; their flocks mostly belong to the manor or Vorwerk. The lowland (blue) is high in sheep, Schleiz and Lobenstein-Ebersdorf in cattle."),
     "vegalite": {"height": 380, "transform": [{"filter": "datum.class_de == 'Dorf'"}], "layer": [
         {"mark": {"type": "circle", "opacity": 0.75, "size": 70},
          "encoding": {
              "x": {"field": "cattle_per_100", "type": "quantitative", "title": bi("Rinder je 100 Einwohner", "Cattle per 100 inhabitants")},
              "y": {"field": "sheep_per_100", "type": "quantitative", "title": bi("Schafe je 100 Einwohner", "Sheep per 100 inhabitants")},
              "color": LT_COLOR,
              "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                          {"field": "landestheil", "title": bi("Landestheil", "District")},
                          {"field": "cattle", "title": bi("Rinder", "Cattle")},
                          {"field": "sheep", "title": bi("Schafe", "Sheep")},
                          {"field": "inhabitants", "title": bi("Einwohner", "Inhabitants")},
                          {"field": "page", "title": bi("Seite", "Page")}]}},
         {"transform": [{"filter": "datum.sheep_per_100 > 300"}],
          "mark": {"type": "text", "align": "left", "dx": 6, "dy": -9, "fontSize": 10},
          "encoding": {"x": {"field": "cattle_per_100", "type": "quantitative"}, "y": {"field": "sheep_per_100", "type": "quantitative"},
                       "text": {"field": "name"}}},
     ]}},
]

a = {
    "id": "orte-viehbestand-1867",
    "title": bi("Viehbestand in den Orten 1867", "Livestock in the places, 1867"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Am Schluss jedes Ortsartikels nennt Brückner den Viehstand der Gemeinde: Pferde, Rinder, Schafe, Schweine, Ziegen, Gänse und Bienenstöcke. Für {n_pl} Orte zusammengeführt ergibt das ein Bild, das die Landestheil-Tabellen in Teil I ergänzt: Gänse und Bienenstöcke kommen dort nicht vor, und der Vergleich nach Einwohnern und Flur zeigt Unterschiede zwischen den Dörfern.",
        f"At the end of each place article Brückner gives the municipality's livestock: horses, cattle, sheep, pigs, goats, geese and beehives. Put together for {n_pl} places this gives a picture that complements the district tables in Part I: geese and beehives do not appear there, and the comparison by inhabitants and field area shows differences between the villages."),
    "method": bi(
        f"Grundlage sind die Felder livestock und flur_morgen der Gazetteer-Einträge der {n_pl} Gemeinden (G1–G6). Die Abkürzungen der Artikel (Pf., R., Schf., Schw., Z., G., Bnst.) sind in den Einträgen aufgelöst; Esel (6 Tiere in 5 Orten) wurden nicht berücksichtigt. Eine nicht genannte Tierart wird als 0 gewertet (z. B. Dragensdorf: 'kein Pferd im Orte'); die Zelle bleibt im Datensatz leer. Bezugsgröße je 100 Einwohner sind die Einwohner aller Orte des Landestheils (Göritz und Neundorf mit den Gemeindezahlen, vgl. orte-siedlungsbild-1867). Die Flur wurde aus den gedruckten Brüchen in Dezimalzahlen umgerechnet. Die Vergleichswerte aus Teil I (S. 233 b4 und S. 234 b1, Zeilen 1867) sind Summen der gedruckten Spalten: Pferde = Pferde + Füllen; Rinder = Stiere + Ochsen + Kühe + Jungvieh; Schafe = ganz veredelte + halb veredelte + unveredelte; Ziegen = Böcke und Ziegen. Bei Zwei-Herren-Orten gelten die Zahlen für den reußischen Anteil.",
        f"The basis are the fields livestock and flur_morgen of the gazetteer entries of the {n_pl} municipalities (G1–G6). The abbreviations of the articles (Pf., R., Schf., Schw., Z., G., Bnst.) are resolved in the entries; donkeys (6 animals in 5 places) were not considered. A species that is not named counts as 0 (e.g. Dragensdorf: 'no horse in the place'); the cell stays empty in the dataset. The reference for 'per 100 inhabitants' is the inhabitants of all places of the district (Göritz and Neundorf with the municipal figures, cf. orte-siedlungsbild-1867). The field area was converted from the printed fractions to decimals. The comparison values from Part I (p. 233 b4 and p. 234 b1, rows 1867) are sums of the printed columns: horses = horses + foals; cattle = bulls + oxen + cows + young cattle; sheep = fully improved + half improved + unimproved; goats = bucks and goats. For places shared with a neighbouring state the figures cover the Reuss share."),
    "findings": findings,
    "caveats": [
        bi("Einzelne Artikel nennen Zahlen anderer Jahre oder nur teilweise: Die Schafe von Langengrobsdorf (70) und Pörsdorf (130) stammen laut Fußnote von 1864 (für 1867 keine Angabe); Pforten hatte 1867 nur 4 Schweine; Pferde und Schafe in Laasen, Wüstfalke und Zschippern gehören dem Gut. Gänse und Bienenstöcke stehen teils als 'über 300' oder 'mehrere' (als Zahl übernommen, 'mehrere' nicht).",
           "Some articles give figures of other years or only partly: the sheep of Langengrobsdorf (70) and Pörsdorf (130) are from 1864 according to a footnote (no figure for 1867); Pforten had only 4 pigs in 1867; horses and sheep in Laasen, Wüstfalke and Zschippern belong to the estate. Geese and beehives are sometimes given as 'over 300' or 'several' (taken as the number, 'several' not at all)."),
        bi(f"In der Tabelle von Teil I (S. 233) steht für Gera 1867 bei den unveredelten Schafen 7351, dieselbe Zahl wie bei den Schweinen. Die Gesamtzeile des Fürstenthums (13 293 unveredelte Schafe) abzüglich Schleiz (2604) und Lobenstein-Ebersdorf (4311) ergibt für Gera nur {fnum(G_UNV_IMPLIED)}, zusammen {fnum(G_SHEEP_IMPLIED)} Schafe; die Summe der Ortsartikel ({fnum(agg[('Gera','Schafe')])}) liegt dem näher. Die Zahl 7351 ist im Druck wahrscheinlich versehentlich wiederholt; der Vergleich der Schafe im Landestheil Gera mit der Tabelle ist daher unsicher.",
           f"In the table of Part I (p. 233) the unimproved sheep for Gera in 1867 are given as 7,351, the same number as for pigs. The total row of the principality (13,293 unimproved sheep) minus Schleiz (2,604) and Lobenstein-Ebersdorf (4,311) leaves only {fnum(G_UNV_IMPLIED,0,'en')} for Gera, {fnum(G_SHEEP_IMPLIED,0,'en')} sheep in all; the sum of the place articles ({fnum(agg[('Gera','Schafe')],0,'en')}) is closer to that. The number 7,351 is probably repeated by mistake in the print; the comparison of sheep for the district of Gera with the table is therefore uncertain."),
        bi("Die Summe der Landestheil-Zeilen für Pferde in Teil I (1731 + 143 + 516 + 35 + 239 + 25 = 2689) weicht von der gedruckten Gesamtzeile des Fürstenthums (2482 + 203 = 2685) ab; die Ortsartikel ergeben 2685.",
           "The sum of the district rows for horses in Part I (1731 + 143 + 516 + 35 + 239 + 25 = 2,689) differs from the printed total row of the principality (2482 + 203 = 2,685); the place articles give 2,685."),
        bi("Städte und Orte mit Rittergut oder Kammergut haben oft Vieh, das nicht den Einwohnern gehört; je Einwohner berechnete Werte sind für Gera (Stadt: 50 Rinder, 193 Schafe) und andere Städte nicht aussagekräftig. Die Diagramme zu Dörfern lassen die Städte weg.",
           "Towns and places with a manor or Kammergut often have livestock that does not belong to the inhabitants; values per inhabitant are not meaningful for Gera (town: 50 cattle, 193 sheep) and other towns. The charts on villages leave out the towns."),
    ],
    "datasets": [
        {"name": "livestock_district", "title": bi("Viehbestand je Landestheil und Tierart", "Livestock per district and species"),
         "columns": dist_cols, "rows": dist_rows, "source_refs": refs},
        {"name": "official_check", "title": bi("Vergleich mit der Viehzählungstabelle in Teil I (Zeile 1867)", "Comparison with the livestock census table in Part I (row 1867)"),
         "columns": chk_cols, "rows": chk_rows, "source_refs": [{"page": "233", "block": "b4", "rows": "r13; r23"}, {"page": "234", "block": "b1", "rows": "r12; r19"}]},
        {"name": "livestock_places", "title": bi("Viehbestand je Ort (breit)", "Livestock per place (wide)"),
         "columns": wcols, "rows": wide, "source_refs": refs},
        {"name": "livestock_long", "title": bi("Viehbestand je Ort und Tierart (lang)", "Livestock per place and species (long)"),
         "columns": lcols, "rows": long_, "source_refs": refs},
    ],
    "charts": charts,
    "conversions": [{"from": "preuß. Morgen", "to": "Hektar", "factor_or_formula": "1 Morgen = 0,255322 ha (180 Quadratruthen)", "reference": "Brückner, S. 832"}],
    "keywords": {"de": ["Viehbestand", "Rinder", "Schafe", "Pferde", "Gänse", "Ziegen", "Schweine", "Bienenstöcke", "Viehzählung 1867"],
                 "en": ["livestock", "cattle", "sheep", "horses", "geese", "goats", "pigs", "beehives", "1867 livestock census"]},
    "related": ["viehzucht-bestand-1843-1867", "orte-flur-boden-pacht", "landwirtschaft-bodennutzung-1854"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
