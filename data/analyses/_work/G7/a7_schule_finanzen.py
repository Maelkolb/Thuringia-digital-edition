"""G7 analysis 7: schools and municipal finances in the place articles."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
import collections, math

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)
n_all = len(U)

# ---------------------------------------------------------------- schools
school_rows = []
for e in U:
    s = e.get("school") or {}
    inh, hou = eff(e)
    so, sc = size_class(inh)
    own = bool(s.get("exists"))
    pupils = s.get("pupils")
    pc = place_class(e)
    status = "eigene Schule" if own else "Schule im Nachbarort"
    status_en = "own school" if own else "school in a neighbouring place"
    per100 = round(100 * pupils / inh, 1) if (pupils and not own) else None
    school_rows.append([uid(e), e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, so, sc, status, status_en,
                        pupils, s.get("note"), per100, e["start"]["page"], e["start"]["block"]])
scols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("size_order", "Größenklasse (Nr.)", "Size class (no.)", "integer", derived=True),
    col("size_class", "Größenklasse", "Size class", "string", "Einwohner", derived=True),
    col("status_de", "Schulort", "School status", "string", derived=True),
    col("status_en", "Schulort (en)", "School status (en)", "string", derived=True),
    col("pupils", "Schüler", "Pupils", "integer", "Kinder", note="bei Orten mit eigener Schule alle Kinder der Schule (auch aus eingeschulten Nachbarorten), sonst die Kinder des Orts in der auswärtigen Schule; leer = nicht genannt"),
    col("note", "Vermerk im Gazetteer", "Gazetteer note", "string"),
    col("pupils_per_100", "Schüler je 100 Einwohner", "Pupils per 100 inhabitants", "number", "je 100 Einw.", derived=True, note="nur für Orte ohne eigene Schule"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
own_places = [r for r in school_rows if r[8] == "eigene Schule"]
own_pupils = [r for r in own_places if r[10]]
# Part I (p. 299 b3): schools and pupils 1868 per Landestheil (Staedte + Land)
PART1 = {"Gera": (3 + 30, 2529 + 3163), "Schleiz": (4 + 37, 1373 + 3356), "Lobenstein-Ebersdorf": (2 + 39, 838 + 2980)}
chk_rows = []
for lt in LT_ORDER:
    ow = [r for r in own_places if r[2] == lt]
    pu = sum(r[10] for r in ow if r[10])
    chk_rows.append([lt, len(ow), pu, PART1[lt][0], PART1[lt][1]])
chk_cols = [
    col("landestheil", "Landestheil", "District", "string"),
    col("places_own_school", "Orte mit eigener Schule (Ortsartikel)", "Places with own school (place articles)", "integer", "Orte", derived=True),
    col("pupils_places", "Schüler dieser Schulen (Ortsartikel)", "Pupils of these schools (place articles)", "integer", "Kinder", derived=True),
    col("schools_part1", "Volksschulen 1868 (Teil I, S. 299)", "Elementary schools 1868 (Part I, p. 299)", "integer", "Schulen", derived=True, note="Summe Städte + Land der gedruckten Tabelle"),
    col("pupils_part1", "Schüler 1868 (Teil I, S. 299)", "Pupils 1868 (Part I, p. 299)", "integer", "Kinder", derived=True, note="Summe Städte + Land der gedruckten Tabelle"),
]

# ---------------------------------------------------------------- finances
def fin(e):
    m = e.get("municipal_finances") or {}
    g = lambda k: m.get(k)

    def mid(k, kmax):
        v = g(k)
        if v is None:
            return None
        return (v + g(kmax)) / 2 if g(kmax) is not None else v

    parts = [mid("assets_thaler", "assets_thaler_max")]
    parts += [g(k) for k in ("capital_thaler", "activa_thaler", "property_value_thaler", "property_value_narrower_thaler",
                             "property_value_wider_thaler", "forest_bavaria_value_thaler")]
    parts = [p for p in parts if p is not None]
    A = sum(parts) if parts else None
    D = g("debts_thaler")
    if g("expenditure_thaler") is not None:
        X = mid("expenditure_thaler", "expenditure_thaler_max")
    elif g("expenditure_thaler_min") is not None:
        X = (g("expenditure_thaler_min") + g("expenditure_thaler_max")) / 2
    elif g("salary_expenditure_thaler") is not None:
        X = g("salary_expenditure_thaler") + (g("roads_expenditure_thaler") or 0)
    else:
        X = None
    return A, D, X, m.get("verbatim")


fin_rows, long_rows = [], []
MEAS = [(1, "Vermögen", "Assets", 5), (2, "Schulden", "Debts", 6), (3, "Jahresausgabe", "Annual expenditure", 7)]
for e in U:
    A, D, X, vb = fin(e)
    inh, hou = eff(e)
    pc = place_class(e)
    if A and D:
        pos, pos_en = "Vermögen und Schulden", "assets and debts"
    elif A:
        pos, pos_en = "nur Vermögen", "assets only"
    elif D:
        pos, pos_en = "nur Schulden", "debts only"
    else:
        pos, pos_en = "keine Angabe", "none stated"
    po = {"Vermögen und Schulden": 1, "nur Vermögen": 2, "nur Schulden": 3}.get(pos, 4)
    row = [uid(e), e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh,
           A, D, X, pos, pos_en, po,
           round(A / inh, 2) if A else None, round(D / inh, 2) if D else None, round(X / inh, 2) if X else None,
           vb, e["start"]["page"], e["start"]["block"]]
    fin_rows.append(row)
    for o, de, en, idx in MEAS:
        v = {5: A, 6: D, 7: X}[idx]
        if v:
            long_rows.append([uid(e), e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, o, de, en, v, round(v / inh, 3), e["start"]["page"], e["start"]["block"]])
fcols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("assets", "Vermögen", "Assets", "number", "Thaler", derived=True, note="Wert des Gemeindegrundbesitzes plus Kapital (Summe der gedruckten Beträge; bei Spannen Mittelwert); leer = keines genannt"),
    col("debts", "Schulden", "Debts", "number", "Thaler", note="leer = keine genannt"),
    col("expenditure", "Jahresausgabe", "Annual expenditure", "number", "Thaler", derived=True, note="gedruckter Betrag, bei Spannen ('150–170') der Mittelwert"),
    col("position_de", "Vermögenslage", "Financial position", "string", derived=True),
    col("position_en", "Vermögenslage (en)", "Financial position (en)", "string", derived=True),
    col("position_order", "Vermögenslage (Nr.)", "Financial position (no.)", "integer", derived=True),
    col("assets_per_inh", "Vermögen je Einwohner", "Assets per inhabitant", "number", "Thlr/Einw.", derived=True),
    col("debts_per_inh", "Schulden je Einwohner", "Debts per inhabitant", "number", "Thlr/Einw.", derived=True),
    col("exp_per_inh", "Jahresausgabe je Einwohner", "Expenditure per inhabitant", "number", "Thlr/Einw.", derived=True),
    col("verbatim", "Angabe im Artikel (gedruckt)", "Entry in the article (printed)", "string"),
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
    col("measure_order", "Größe (Nr.)", "Measure (no.)", "integer", derived=True),
    col("measure_de", "Größe", "Measure", "string", derived=True),
    col("measure_en", "Größe (en)", "Measure (en)", "string", derived=True),
    col("thaler", "Betrag", "Amount", "number", "Thaler", derived=True),
    col("thaler_per_inh", "je Einwohner", "per inhabitant", "number", "Thlr/Einw.", derived=True),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
refs = uniq_refs(U)

# ---------------------------------------------------------------- statistics
n_own = len(own_places)
own_share_size = {}
for o, lab, lo, hi in SIZE_CLASSES:
    rs = [r for r in school_rows if r[6] == o]
    if rs:
        own_share_size[lab] = (sum(1 for r in rs if r[8] == "eigene Schule"), len(rs))
small_noschool = [r for r in school_rows if r[8] != "eigene Schule"]
n_no = len(small_noschool)
med_inh_no = median([r[5] for r in small_noschool])
n_no_300 = sum(1 for r in small_noschool if r[5] >= 300)
own_ge300 = [r for r in school_rows if r[5] >= 300]
own_ge300_share = 100 * sum(1 for r in own_ge300 if r[8] == "eigene Schule") / len(own_ge300)
pup_med = median([r[10] for r in own_pupils if r[10] < 700])
pup_by_lt = {lt: median([r[10] for r in own_pupils if r[2] == lt and r[10] < 700]) for lt in LT_ORDER}
per100 = [r[12] for r in school_rows if r[12] is not None]
per100_med = median(per100)
chk_tot = (sum(r[1] for r in chk_rows), sum(r[2] for r in chk_rows), sum(r[3] for r in chk_rows), sum(r[4] for r in chk_rows))

rural = [r for r in fin_rows if r[3] != "Stadt"]
nr = len(rural)
pos_cnt = collections.Counter(r[9] for r in rural)
n_debt = {lt: sum(1 for r in rural if r[2] == lt and r[7]) for lt in LT_ORDER}
n_lt_r = {lt: sum(1 for r in rural if r[2] == lt) for lt in LT_ORDER}
debt_med = {lt: median([r[13] for r in rural if r[2] == lt and r[13] is not None]) for lt in LT_ORDER}
exp_med = {lt: median([r[14] for r in rural if r[2] == lt and r[14] is not None]) for lt in LT_ORDER}
ass_med = {lt: median([r[12] for r in rural if r[2] == lt and r[12] is not None]) for lt in LT_ORDER}
n_exp = {lt: sum(1 for r in rural if r[2] == lt and r[14] is not None) for lt in LT_ORDER}
debt_sum = sum(r[7] for r in rural if r[7])
ass_sum = sum(r[6] for r in rural if r[6])
top_debt = sorted([r for r in rural if r[7]], key=lambda r: -r[7])[:3]
n_geo_dummy = 0
fn1 = lambda x: fnum(x, 1)
fe1 = lambda x: fnum(x, 1, "en")
fn2 = lambda x: fnum(x, 2)
fe2 = lambda x: fnum(x, 2, "en")
sc = own_share_size

findings = [
    bi(f"{n_own} der {n_all} Gemeinden haben eine eigene Schule, {n_no} gehen in einem Nachbarort zur Schule. Die Schüler dieser {len(own_pupils)} Schulen (Angaben vorhanden) zählen zusammen {fnum(sum(r[10] for r in own_pupils))}; Teil I nennt für 1868 {chk_tot[2]} Volksschulen mit {fnum(chk_tot[3])} Schülern. Die Ortsartikel decken damit {pct(100*sum(r[10] for r in own_pupils)/chk_tot[3],0)} der Schüler ab.",
       f"{n_own} of the {n_all} municipalities have a school of their own, {n_no} send their children to a neighbouring place. The pupils of these {len(own_pupils)} schools (with figures) add up to {fnum(sum(r[10] for r in own_pupils),0,'en')}; Part I gives {chk_tot[2]} elementary schools with {fnum(chk_tot[3],0,'en')} pupils for 1868. The place articles thus cover {pct(100*sum(r[10] for r in own_pupils)/chk_tot[3],0,'en')} of the pupils."),
    bi(f"Eine eigene Schule hängt von der Ortsgröße ab: Von den Orten mit mindestens 300 Einwohnern haben {pct(own_ge300_share,0)} eine Schule, von den Orten unter 100 Einwohnern {sc['< 100'][0]} von {sc['< 100'][1]}; unter den {n_no} Orten ohne Schule liegt der Median bei {fnum(med_inh_no)} Einwohnern, nur {n_no_300} haben mehr als 300.",
       f"Having a school depends on place size: {pct(own_ge300_share,0,'en')} of the places with at least 300 inhabitants have one, against {sc['< 100'][0]} of {sc['< 100'][1]} places below 100 inhabitants; among the {n_no} places without a school the median is {fnum(med_inh_no,0,'en')} inhabitants, and only {n_no_300} have more than 300."),
    bi(f"Eine Dorfschule zählt im Median {fnum(pup_med)} Kinder ({fnum(pup_by_lt['Gera'])} im Landestheil Gera, {fnum(pup_by_lt['Schleiz'])} in Schleiz, {fnum(pup_by_lt['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf; Gera mit 2 700 ausgenommen), meist einschließlich der Kinder eingeschulter Nachbardörfer. In den {len(per100)} Orten ohne Schule gehen im Median {fn1(per100_med)} Kinder je 100 Einwohner auswärts zur Schule.",
       f"A village school has a median of {fnum(pup_med,0,'en')} children ({fnum(pup_by_lt['Gera'],0,'en')} in the district of Gera, {fnum(pup_by_lt['Schleiz'],0,'en')} in Schleiz, {fnum(pup_by_lt['Lobenstein-Ebersdorf'],0,'en')} in Lobenstein-Ebersdorf; Gera with 2,700 excluded), mostly including the children of neighbouring villages assigned to it. In the {len(per100)} places without a school a median of {fe1(per100_med)} children per 100 inhabitants attend school elsewhere."),
    bi(f"Die Gemeindehaushalte der {nr} Landgemeinden sind klein und häufig verschuldet: {sum(n_debt.values())} nennen Schulden, zusammen {fnum(debt_sum)} Thaler (Vermögen: {fnum(ass_sum)} Thaler). Die Schulden je Einwohner liegen im Median der verschuldeten Gemeinden mit {fn2(debt_med['Gera'])} (Gera), {fn2(debt_med['Schleiz'])} (Schleiz) und {fn2(debt_med['Lobenstein-Ebersdorf'])} Thalern (Lobenstein-Ebersdorf) überall etwa gleich hoch; am höchsten sind sie bei {top_debt[0][1]} ({fnum(top_debt[0][7])} Thlr), {top_debt[1][1]} ({fnum(top_debt[1][7])}) und {top_debt[2][1]} ({fnum(top_debt[2][7])}).",
       f"The budgets of the {nr} rural municipalities are small and often indebted: {sum(n_debt.values())} name debts, {fnum(debt_sum,0,'en')} thalers in total (assets: {fnum(ass_sum,0,'en')} thalers). Debts per inhabitant of the indebted municipalities have a median of {fe2(debt_med['Gera'])} (Gera), {fe2(debt_med['Schleiz'])} (Schleiz) and {fe2(debt_med['Lobenstein-Ebersdorf'])} thalers (Lobenstein-Ebersdorf), about the same everywhere; they are highest at {top_debt[0][1]} ({fnum(top_debt[0][7],0,'en')} thalers), {top_debt[1][1]} ({fnum(top_debt[1][7],0,'en')}) and {top_debt[2][1]} ({fnum(top_debt[2][7],0,'en')})."),
    bi(f"Die laufenden Ausgaben unterscheiden sich stärker als die Schulden: Im Median geben die Gemeinden im Landestheil Gera {fn2(exp_med['Gera'])} Thaler je Einwohner und Jahr aus, in Schleiz {fn2(exp_med['Schleiz'])} und in Lobenstein-Ebersdorf {fn2(exp_med['Lobenstein-Ebersdorf'])}; das Gemeindevermögen je Einwohner beträgt im Landestheil Gera {fn1(ass_med['Gera'])}, in Schleiz {fn1(ass_med['Schleiz'])} und in Lobenstein-Ebersdorf {fn1(ass_med['Lobenstein-Ebersdorf'])} Thaler.",
       f"Current expenditure differs more than debts: the median municipality in the district of Gera spends {fe2(exp_med['Gera'])} thalers per inhabitant and year, in Schleiz {fe2(exp_med['Schleiz'])} and in Lobenstein-Ebersdorf {fe2(exp_med['Lobenstein-Ebersdorf'])}; municipal assets per inhabitant are {fe1(ass_med['Gera'])} thalers in the district of Gera, {fe1(ass_med['Schleiz'])} in Schleiz and {fe1(ass_med['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf."),
]

LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
charts = [
    {"id": "c1", "dataset": "schools",
     "title": bi("Eigene Schule nach Ortsgröße", "Own school by place size"),
     "caption": bi("Anteil der Gemeinden mit eigener Schule bzw. mit Schulgang im Nachbarort, nach Einwohnerzahl. Ab 300 Einwohnern hat fast jeder Ort eine Schule; die Zahlen der Gemeinden je Klasse stehen im Tooltip.",
                   "Share of municipalities with a school of their own or sending children to a neighbouring place, by number of inhabitants. From 300 inhabitants almost every place has a school; the number of municipalities per class is in the tooltip."),
     "vegalite": {"height": 280, "mark": "bar", "encoding": {
         "y": {"field": "size_class", "type": "ordinal", "sort": {"field": "size_order", "op": "min"}, "title": bi("Einwohner", "Inhabitants")},
         "x": {"aggregate": "count", "type": "quantitative", "stack": "normalize", "title": bi("Anteil der Gemeinden", "Share of municipalities"), "axis": {"format": "%"}},
         "color": {"field": {"de": "status_de", "en": "status_en"}, "type": "nominal", "title": bi("Schulort", "School"),
                   "sort": {"field": "status_de", "order": "descending"}, "legend": {"labelLimit": 300}},
         "tooltip": [{"field": "size_class", "title": bi("Größenklasse", "Size class")},
                     {"field": {"de": "status_de", "en": "status_en"}, "title": bi("Schulort", "School")},
                     {"aggregate": "count", "title": bi("Gemeinden", "Municipalities")}]}}},
    {"id": "c2", "dataset": "schools",
     "title": bi("Kinder je Schule", "Children per school"),
     "caption": bi("Zahl der Schüler in den Schulorten (ohne Gera: 2 700); die Angabe schließt in der Regel die Kinder eingeschulter Nachbarorte ein.",
                   "Number of pupils in the school places (without Gera: 2,700); the figure usually includes the children of neighbouring places assigned to the school."),
     "vegalite": {"height": 260, "transform": [{"filter": "datum.status_de == 'eigene Schule' && isValid(datum.pupils) && datum.pupils < 700"}],
                  "mark": "bar", "encoding": {
                      "x": {"field": "pupils", "bin": {"step": 25}, "type": "quantitative", "title": bi("Schüler je Schule", "Pupils per school")},
                      "y": {"aggregate": "count", "type": "quantitative", "title": bi("Anzahl der Schulorte", "Number of school places"), "axis": {"tickMinStep": 1}},
                      "color": LT_COLOR,
                      "tooltip": [{"field": "pupils", "bin": {"step": 25}, "title": bi("Schüler (Klasse)", "Pupils (class)")},
                                  {"field": "landestheil", "title": bi("Landestheil", "District")},
                                  {"aggregate": "count", "title": bi("Schulorte", "School places")}]}}},
    {"id": "c3", "dataset": "finance",
     "title": bi("Vermögenslage der Landgemeinden", "Financial position of the rural municipalities"),
     "caption": bi("Gemeinden nach dem, was der Artikel über Vermögen (Grundbesitz, Kapital) und Schulden mitteilt, je Landestheil (ohne die sechs Städte). Im Landestheil Lobenstein-Ebersdorf sind verschuldete Gemeinden häufiger.",
                   "Municipalities by what the article states about assets (land, capital) and debts, per district (without the six towns). In the district of Lobenstein-Ebersdorf indebted municipalities are more frequent."),
     "vegalite": {"height": 220, "transform": [{"filter": "datum.class_de != 'Stadt'"}], "mark": "bar", "encoding": {
         "y": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None},
         "x": {"aggregate": "count", "type": "quantitative", "stack": "normalize", "title": bi("Anteil der Gemeinden", "Share of municipalities"), "axis": {"format": "%"}},
         "color": {"field": {"de": "position_de", "en": "position_en"}, "type": "nominal", "title": bi("Vermögenslage", "Financial position"),
                   "sort": {"field": "position_order", "op": "min"}, "legend": {"labelLimit": 300, "columns": 2}},
         "order": {"field": "position_order", "type": "quantitative"},
         "tooltip": [{"field": "landestheil", "title": bi("Landestheil", "District")},
                     {"field": {"de": "position_de", "en": "position_en"}, "title": bi("Vermögenslage", "Financial position")},
                     {"aggregate": "count", "title": bi("Gemeinden", "Municipalities")}]}}},
    {"id": "c4", "dataset": "finance_long",
     "title": bi("Vermögen, Schulden und Ausgaben je Einwohner", "Assets, debts and expenditure per inhabitant"),
     "caption": bi("Thaler je Einwohner in den Landgemeinden, soweit der Artikel den Betrag nennt (Kasten: Median und Quartile, Punkte: Ausreißer, Skala bis 12 Thaler). Die Ausgaben je Einwohner sinken von Gera über Schleiz nach Lobenstein-Ebersdorf deutlich, die Schulden nicht.",
                   "Thalers per inhabitant in the rural municipalities where the article gives the amount (box: median and quartiles, dots: outliers, scale up to 12 thalers). Expenditure per inhabitant falls markedly from Gera through Schleiz to Lobenstein-Ebersdorf, debts do not."),
     "vegalite": {"height": 300, "transform": [{"filter": "datum.class_de != 'Stadt' && datum.thaler_per_inh <= 12"}],
                  "mark": {"type": "boxplot", "extent": 1.5, "size": 16},
                  "encoding": {
                      "column": {"field": {"de": "measure_de", "en": "measure_en"}, "type": "nominal", "sort": {"field": "measure_order", "op": "min"}, "title": None, "header": {"labelFontSize": 12}},
                      "x": {"field": "landestheil", "type": "nominal", "sort": LT_ORDER, "title": None, "axis": {"labels": False, "ticks": False}},
                      "y": {"field": "thaler_per_inh", "type": "quantitative", "title": bi("Thaler je Einwohner", "thalers per inhabitant")},
                      "color": LT_COLOR}}},
]

a = {
    "id": "orte-schulen-gemeindehaushalt",
    "title": bi("Schulorte und Gemeindehaushalte der Orte", "School places and municipal budgets of the places"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Jeder Ortsartikel nennt, ob der Ort eine eigene Schule hat oder in einem Nachbarort zur Schule geht, und beschreibt die Gemeindekasse: Grundbesitz, Kapital, Schulden und Jahresausgabe. Für {n_all} Gemeinden ergibt das ein Bild der Schullandschaft nach Ortsgröße und der Finanzlage der Landgemeinden in den drei Landestheilen.",
        f"Every place article states whether the place has a school of its own or sends its children to a neighbouring place, and describes the municipal budget: land, capital, debts and annual expenditure. For {n_all} municipalities this gives a picture of the school network by place size and of the financial situation of the rural municipalities in the three districts."),
    "method": bi(
        f"Grundlage sind die Felder school und municipal_finances der Gazetteer-Einträge der {n_all} Gemeinden (G1–G6). Schulort = Gemeinde mit eigener Schule (school.exists); die Schülerzahl ist die im Artikel genannte (bei Schulorten einschließlich eingeschulter Kinder anderer Orte, bei Orten ohne Schule die Kinder des Ortes im auswärtigen Schulort; 'etwa 20–25' o. ä. Spannen wurden nicht übernommen). Schüler je 100 Einwohner wurde nur für Orte ohne eigene Schule berechnet. Vergleichswerte aus Teil I (S. 299 b3): Volksschulen und Schüler 1868 der Landestheile als Summe der gedruckten Zeilen Städte und Land. Gemeindefinanzen: Vermögen = Wert des Gemeindegrundbesitzes (z. B. 'im Werthe von 3500 Thlr.') plus Kapital und Außenstände (Summe der im Eintrag erfassten Beträge, bei Spannen wie '600–700 Thlr.' der Mittelwert); Schulden = genannte Schulden; Jahresausgabe = genannter Betrag oder bei Spannen ('150–170 Thlr.') der Mittelwert. Kirchbauschulden (Großsaara) und Vermögen der Kirche wurden nicht mitgezählt. Betrachtet sind die {nr} Landgemeinden; die sechs Städte haben andere Größenordnungen (Gera: Vermögen 540 600 Thlr.). Je-Einwohner-Werte beziehen sich auf die Einwohnerzahl der Gemeinde (Göritz, Neundorf mit den Gemeindezahlen). Alle Beträge sind Thaler, wie im Druck; eine Umrechnung findet nicht statt.",
        f"The basis are the fields school and municipal_finances of the gazetteer entries of the {n_all} municipalities (G1–G6). School place = municipality with a school of its own (school.exists); the number of pupils is the one given in the article (for school places including children of other places assigned to it, for places without a school the children of the place in the school elsewhere; ranges such as 'about 20–25' were not taken over). Pupils per 100 inhabitants was calculated only for places without a school of their own. Comparison values from Part I (p. 299 b3): elementary schools and pupils of the districts in 1868 as the sum of the printed rows for towns and country. Municipal finances: assets = value of the municipal land (e.g. 'valued at 3,500 thalers') plus capital and outstanding claims (sum of the amounts recorded in the entry; for ranges such as '600–700 thalers' the mean); debts = debts named; annual expenditure = amount named or, for ranges ('150–170 thalers'), the mean. Church building debts (Großsaara) and church assets were not counted. The {nr} rural municipalities are considered; the six towns have different orders of magnitude (Gera: assets 540,600 thalers). Per-inhabitant values relate to the municipality's inhabitants (Göritz and Neundorf with the municipal figures). All amounts are thalers as in the print; no conversion takes place."),
    "findings": findings,
    "caveats": [
        bi("Die Gemeindefinanzen sind im Druck nicht einheitlich gegliedert: Brückner unterscheidet die engere Gemeinde (Besitz der Bauern, z. B. Anger, Hutung) und die weitere politische Gemeinde, teilt Vermögen und Schulden mal der einen, mal der anderen zu und gibt Steuerwerte oder Verkehrswerte an. Die Auswertung addiert die genannten Beträge und zeigt nur Größenordnungen.",
           "The municipal finances are not structured uniformly in the print: Brückner distinguishes the narrower municipality (property of the farmers, e.g. green, pasture) from the wider political municipality, assigns assets and debts sometimes to one and sometimes to the other, and gives tax values or market values. The analysis adds the amounts named and shows only orders of magnitude."),
        bi("Fehlt eine Angabe zu Schulden oder Vermögen, bleibt die Zelle leer; ob der Ort keine hat oder der Artikel sie nicht nennt, ist nicht immer zu unterscheiden (häufig steht 'weder Vermögen noch Schulden', dann ist 0 gemeint und die Zelle ebenfalls leer).",
           "If an amount for debts or assets is missing the cell stays empty; whether the place has none or the article does not name them cannot always be told (often the article says 'neither assets nor debts', meaning 0, and the cell is likewise empty)."),
        bi("Die Schülerzahlen betreffen verschiedene Jahre (z. B. 1866 für Saaldorf) und bei Schulorten auch Kinder anderer Orte; 'Schüler je 100 Einwohner' ist deshalb nur für Orte ohne eigene Schule berechnet. Der Vergleich mit Teil I (115 Schulen) ist nur ungefähr, weil größere Orte mehrere Schulen haben können.",
           "The pupil numbers refer to different years (e.g. 1866 for Saaldorf) and for school places also include children from other places; 'pupils per 100 inhabitants' is therefore calculated only for places without a school of their own. The comparison with Part I (115 schools) is only approximate because larger places may have several schools."),
    ],
    "datasets": [
        {"name": "schools", "title": bi("Schulort und Schüler je Gemeinde", "School place and pupils per municipality"),
         "columns": scols, "rows": school_rows, "source_refs": refs},
        {"name": "school_check", "title": bi("Vergleich mit den Volksschulen in Teil I (1868)", "Comparison with the elementary schools in Part I (1868)"),
         "columns": chk_cols, "rows": chk_rows, "source_refs": [{"page": "299", "block": "b3", "rows": "r2-r16"}]},
        {"name": "finance", "title": bi("Gemeindevermögen, Schulden und Jahresausgabe je Gemeinde", "Municipal assets, debts and annual expenditure per municipality"),
         "columns": fcols, "rows": fin_rows, "source_refs": refs},
        {"name": "finance_long", "title": bi("Vermögen, Schulden und Ausgaben (Langformat)", "Assets, debts and expenditure (long format)"),
         "columns": lcols, "rows": long_rows, "source_refs": refs},
    ],
    "charts": charts,
    "keywords": {"de": ["Schule", "Schulort", "Schüler", "Gemeindefinanzen", "Gemeindevermögen", "Schulden", "Jahresausgabe", "Dörfer"],
                 "en": ["school", "school place", "pupils", "municipal finances", "municipal assets", "debts", "annual expenditure", "villages"]},
    "related": ["schule-volksschulen-schueler-lehrer-1863-1868", "orte-siedlungsbild-1867", "verfassung-landtag-gemeinderaete-vertretung"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
