"""G7 analysis 5: first documentary mentions and historical name forms of the places."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\G7")
from common import *
import collections, math

ents = load_entries()
C = load_coords()
U = sorted(gemeinden(ents), key=sort_key)

rows = []
for e in U:
    u = uid(e)
    forms = e.get("historic_forms") or []
    dated = [f for f in forms if f.get("year")]
    fy = e.get("first_mention_year")
    basis = None
    if fy:
        basis = "Angabe im Artikel"
    else:
        cand = [f["year"] for f in dated if f["year"] <= 1700]
        if cand:
            fy, basis = min(cand), "früheste datierte Namensform"
    inh, hou = eff(e)
    pc = place_class(e)
    fv = "; ".join((f"{f['year']} {f['form']}" if f.get("year") else f["form"]) for f in forms)
    lon, lat, gn = coord(e, C)
    rows.append([u, e["name"], e["landestheil"], pc, PLACE_CLASS_EN[pc], inh, fy, basis,
                 (fy // 50) * 50 if fy else None, len(forms), len(dated), fv,
                 e["start"]["page"], e["start"]["block"]])
cols = [
    col("place_id", "Kennung", "ID", "string"),
    col("name", "Ort", "Place", "string"),
    col("landestheil", "Landestheil", "District", "string"),
    col("class_de", "Ortsklasse", "Place class", "string", derived=True),
    col("class_en", "Ortsklasse (en)", "Place class (en)", "string", derived=True),
    col("inhabitants", "Einwohner", "Inhabitants", "integer", "Personen"),
    col("first_year", "Erste Erwähnung", "First mention", "integer", "Jahr", note="Jahr der ersten urkundlichen Nennung laut Artikel; leer = nicht genannt"),
    col("first_basis", "Herkunft der Jahreszahl", "Source of the year", "string"),
    col("half_century", "Halbjahrhundert (Beginn)", "Half-century (start)", "integer", "Jahr", derived=True),
    col("n_forms", "Zahl der Namensformen", "Number of name forms", "integer", derived=True, note="alle im Artikel genannten urkundlichen und mundartlichen Formen außer der heutigen"),
    col("n_dated", "davon mit Jahr", "of which dated", "integer", derived=True),
    col("forms", "Namensformen (gedruckt)", "Name forms (printed)", "string"),
    col("page", "Seite (Artikelbeginn)", "Page (article start)", "string"),
    col("block", "Block (Artikelbeginn)", "Block (article start)", "string"),
]
refs = uniq_refs(U)

# ---- statistics ----------------------------------------------------------------------------------
n = len(rows)
dated_rows = [r for r in rows if r[6]]
nd = len(dated_rows)
cnt_year = collections.Counter(r[6] for r in dated_rows)
clusters = [(y, c) for y, c in cnt_year.most_common() if c >= 5]
cl_years = sorted(y for y, c in clusters)
cl_total = sum(c for y, c in clusters)
y_med = {lt: median([r[6] for r in dated_rows if r[2] == lt]) for lt in LT_ORDER}
n_lt = {lt: sum(1 for r in dated_rows if r[2] == lt) for lt in LT_ORDER}
early = {lt: sum(1 for r in dated_rows if r[2] == lt and r[6] < 1200) for lt in LT_ORDER}
share_c14 = 100 * sum(1 for r in dated_rows if 1300 <= r[6] < 1400) / nd
n_c14 = sum(1 for r in dated_rows if 1300 <= r[6] < 1400)
earliest = sorted(dated_rows, key=lambda r: r[6])[:3]
latest = [r for r in dated_rows if r[6] >= 1500]
n_late = len(latest)
n_forms = [r[9] for r in rows]
mean_forms = mean(n_forms)
n_no_forms = sum(1 for r in rows if r[9] == 0)
forms_cls = {c: mean([r[9] for r in rows if r[3] == c]) for c in ("Stadt", "Marktflecken", "Dorf")}
most_forms = sorted(rows, key=lambda r: -r[9])[:3]


def spearman(a, b):
    ra = [sorted(a).index(x) + (a.count(x) - 1) / 2 for x in a]
    rb = [sorted(b).index(x) + (b.count(x) - 1) / 2 for x in b]
    ma, mb = mean(ra), mean(rb)
    return sum((p - ma) * (q - mb) for p, q in zip(ra, rb)) / math.sqrt(sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb))


rho = spearman([r[6] for r in dated_rows], [r[9] for r in dated_rows])
# the 1364 / 1121 clusters and the Pflege Langenberg
lang = 0
n1364 = 0
for e in U:
    if e.get("first_mention_year") == 1364:
        n1364 += 1
        if "Langenberg" in article_text(e):
            lang += 1
lt1364 = collections.Counter(r[2] for r in dated_rows if r[6] == 1364)
lt1121 = collections.Counter(r[2] for r in dated_rows if r[6] == 1121)
cl_txt_de = ", ".join(f"{y} ({c})" for y, c in sorted(clusters))
fn = lambda x, nd_=0: fnum(x, nd_)
fe = lambda x, nd_=0: fnum(x, nd_, "en")

findings = [
    bi(f"Für {nd} der {n} Gemeinden nennen die Artikel eine erste urkundliche Erwähnung. Die älteste ist {earliest[0][1]} ({earliest[0][6]}), gefolgt von {earliest[1][1]} und {earliest[2][1]} ({earliest[1][6]}). {n_c14} Orte ({pct(share_c14,0)}) werden erstmals im 14. Jahrhundert erwähnt, {n_late} erst ab 1500.",
       f"For {nd} of the {n} municipalities the articles give a first documentary mention. The oldest is {earliest[0][1]} ({earliest[0][6]}), followed by {earliest[1][1]} and {earliest[2][1]} ({earliest[1][6]}). {n_c14} places ({pct(share_c14,0,'en')}) are first mentioned in the 14th century, {n_late} only from 1500."),
    bi(f"Die Erstnennungen häufen sich auf wenige Jahre: {cl_txt_de} – diese {len(clusters)} Jahre stehen für {cl_total} von {nd} Orten ({pct(100*cl_total/nd,0)}). Das spiegelt eher die Überlieferung einzelner Urkunden und Verzeichnisse als die Gründungszeit der Dörfer (Deutung); allein auf 1364 entfallen {cnt_year[1364]} Orte, {'alle' if lt1364['Gera'] == cnt_year[1364] else lt1364['Gera']} davon im Landestheil Gera.",
       f"First mentions pile up in a few years: {', '.join(f'{y} ({c})' for y, c in sorted(clusters))}; these {len(clusters)} years account for {cl_total} of {nd} places ({pct(100*cl_total/nd,0,'en')}). This reflects the survival of individual charters and registers rather than the founding period of the villages (interpretation); 1364 alone accounts for {cnt_year[1364]} places, {'all' if lt1364['Gera'] == cnt_year[1364] else lt1364['Gera']} of them in the district of Gera."),
    bi(f"Das Unterland ist früher belegt: Im Median werden Orte im Landestheil Gera {int(y_med['Gera'])} erstmals erwähnt, in Schleiz {int(y_med['Schleiz'])} und in Lobenstein-Ebersdorf {int(y_med['Lobenstein-Ebersdorf'])}; vor 1200 stehen {early['Gera']} Orte aus Gera, {early['Schleiz']} aus Schleiz und {early['Lobenstein-Ebersdorf']} aus Lobenstein-Ebersdorf.",
       f"The lowland is documented earlier: the median first mention of places in the district of Gera is {int(y_med['Gera'])}, in Schleiz {int(y_med['Schleiz'])} and in Lobenstein-Ebersdorf {int(y_med['Lobenstein-Ebersdorf'])}; before 1200 there are {early['Gera']} places from Gera, {early['Schleiz']} from Schleiz and {early['Lobenstein-Ebersdorf']} from Lobenstein-Ebersdorf."),
    bi(f"Im Mittel nennt ein Artikel {fnum(mean_forms,1)} abweichende Namensformen (Städte {fnum(forms_cls['Stadt'],1)}, Dörfer {fnum(forms_cls['Dorf'],1)}); am meisten haben {most_forms[0][1]} ({most_forms[0][9]}), {most_forms[1][1]} ({most_forms[1][9]}) und {most_forms[2][1]} ({most_forms[2][9]}). Früher belegte Orte haben mehr Formen (Rangkorrelation zwischen Erstnennung und Zahl der Formen {fnum(rho,2)}), {n_no_forms} Orte nennen keine.",
       f"On average an article gives {fnum(mean_forms,1,'en')} variant name forms (towns {fnum(forms_cls['Stadt'],1,'en')}, villages {fnum(forms_cls['Dorf'],1,'en')}); {most_forms[0][1]} ({most_forms[0][9]}), {most_forms[1][1]} ({most_forms[1][9]}) and {most_forms[2][1]} ({most_forms[2][9]}) have the most. Earlier documented places have more forms (rank correlation between first mention and number of forms {fnum(rho,2,'en')}); {n_no_forms} places give none."),
]

LT_COLOR = {"field": "landestheil", "type": "nominal", "title": bi("Landestheil", "District"),
            "scale": {"domain": LT_ORDER}, "legend": {"labelLimit": 300}}
charts = [
    {"id": "c1", "dataset": "mentions",
     "title": bi("Erste Erwähnungen nach Halbjahrhundert", "First mentions by half-century"),
     "caption": bi(f"Zahl der Gemeinden ({nd} mit Jahresangabe), deren erste urkundliche Nennung in das jeweilige Halbjahrhundert fällt, nach Landestheil. Das 14. Jahrhundert und das Jahr 1533 dominieren.",
                   f"Number of municipalities ({nd} with a year) whose first documentary mention falls in the half-century, by district. The 14th century and the year 1533 dominate."),
     "vegalite": {"height": 280, "transform": [{"filter": "isValid(datum.first_year)"}], "mark": "bar", "encoding": {
         "x": {"field": "half_century", "type": "ordinal", "title": bi("Halbjahrhundert (Beginn)", "Half-century (start)"), "axis": {"labelAngle": 0}},
         "y": {"aggregate": "count", "type": "quantitative", "title": bi("Anzahl der Orte", "Number of places"), "axis": {"tickMinStep": 1}},
         "color": LT_COLOR,
         "tooltip": [{"field": "half_century", "title": bi("ab Jahr", "from year")},
                     {"field": "landestheil", "title": bi("Landestheil", "District")},
                     {"aggregate": "count", "title": bi("Orte", "Places")}]}}},
    {"id": "c2", "dataset": "mentions",
     "title": bi("Jahre mit gehäuften Erstnennungen", "Years with clustered first mentions"),
     "caption": bi("Jahre, in denen mindestens drei Gemeinden erstmals erwähnt werden. Einzelne Verzeichnisse und Urkunden (1121, 1325, 1333, 1364, 1533) erfassen jeweils zahlreiche Orte auf einmal.",
                   "Years in which at least three municipalities are first mentioned. Individual registers and charters (1121, 1325, 1333, 1364, 1533) each cover many places at once."),
     "vegalite": {"height": 280, "transform": [{"filter": "isValid(datum.first_year)"},
                                              {"joinaggregate": [{"op": "count", "as": "n_year"}], "groupby": ["first_year"]},
                                              {"filter": "datum.n_year >= 3"}],
                  "mark": "bar", "encoding": {
                      "x": {"field": "first_year", "type": "ordinal", "title": bi("Jahr der ersten Erwähnung", "Year of first mention"), "axis": {"labelAngle": -45}},
                      "y": {"aggregate": "count", "type": "quantitative", "title": bi("Anzahl der Orte", "Number of places"), "axis": {"tickMinStep": 1}},
                      "color": LT_COLOR,
                      "tooltip": [{"field": "first_year", "title": bi("Jahr", "Year")},
                                  {"field": "landestheil", "title": bi("Landestheil", "District")},
                                  {"aggregate": "count", "title": bi("Orte", "Places")}]}}},
    {"id": "c3", "dataset": "mentions",
     "title": bi("Namensformen und Alter der Erstnennung", "Name forms and age of the first mention"),
     "caption": bi("Jeder Punkt ist eine Gemeinde; die Linie ist die lineare Regression über alle Orte. Früher belegte Orte haben im Mittel mehr verzeichnete Namensformen; die Städte (rechts der Punktwolke ausgenommen) liegen oben.",
                   "Each dot is a municipality; the line is the linear regression over all places. Places documented earlier have on average more recorded name forms; the towns lie at the top."),
     "vegalite": {"height": 300, "transform": [{"filter": "isValid(datum.first_year)"}], "layer": [
         {"mark": {"type": "circle", "opacity": 0.6, "size": 60},
          "encoding": {"x": {"field": "first_year", "type": "quantitative", "title": bi("Jahr der ersten Erwähnung", "Year of first mention"), "scale": {"zero": False}, "axis": {"format": "d"}},
                       "y": {"field": "n_forms", "type": "quantitative", "title": bi("Zahl der Namensformen", "Number of name forms"), "axis": {"tickMinStep": 1}},
                       "color": LT_COLOR,
                       "tooltip": [{"field": "name", "title": bi("Ort", "Place")},
                                   {"field": "first_year", "title": bi("Erste Erwähnung", "First mention")},
                                   {"field": "n_forms", "title": bi("Namensformen", "Name forms")},
                                   {"field": "landestheil", "title": bi("Landestheil", "District")},
                                   {"field": "page", "title": bi("Seite", "Page")}]}},
         {"transform": [{"regression": "n_forms", "on": "first_year"}],
          "mark": {"type": "line", "strokeDash": [4, 3]},
          "encoding": {"x": {"field": "first_year", "type": "quantitative"}, "y": {"field": "n_forms", "type": "quantitative"}}},
     ]}},
]
charts[2]["caption"] = bi("Jeder Punkt ist eine Gemeinde; die gestrichelte Linie ist die lineare Regression über alle Orte. Früher belegte Orte haben im Mittel mehr verzeichnete Namensformen.",
                         "Each dot is a municipality; the dashed line is the linear regression over all places. Places documented earlier have on average more recorded name forms.")

a = {
    "id": "orte-erste-erwaehnungen-namensformen",
    "title": bi("Erste Erwähnungen und Namensformen der Orte", "First mentions and name forms of the places"),
    "category": "places",
    "section": "t2",
    "sources": refs,
    "summary": bi(
        f"Die Ortsartikel beginnen mit den urkundlichen Namensformen und dem Jahr der ersten Nennung (»urkundlich 1358 Czwoczen …«). Für {nd} der {n} Gemeinden lässt sich daraus ablesen, wann die Orte erstmals belegt sind und wie viele Namensformen überliefert sind. Die Diagramme zeigen die zeitliche Verteilung nach Landestheil, die Häufung auf wenige Quellenjahre und den Zusammenhang zwischen Alter und Zahl der Formen.",
        f"The place articles begin with the documentary name forms and the year of first mention ('urkundlich 1358 Czwoczen …'). For {nd} of the {n} municipalities this shows when the places are first documented and how many name forms are recorded. The charts show the distribution over time by district, the clustering in a few source years and the relation between age and number of forms."),
    "method": bi(
        f"Grundlage sind die Felder first_mention_year und historic_forms der Gazetteer-Einträge der {n} Gemeinden (G1–G6). Das Jahr der ersten Erwähnung ist das im Artikel genannte früheste Jahr der urkundlichen Nennung des Ortsnamens; fehlt eine ausdrückliche Angabe, wurde die früheste datierte Namensform bis 1700 verwendet (Spalte first_basis). Zahl der Namensformen = alle im Artikel genannten urkundlichen und mundartlichen Formen außer der heutigen Schreibweise (mundartliche Formen in Anführungszeichen mitgezählt, soweit im Eintrag historic_forms erfasst). Halbjahrhundert = Jahr, auf Vielfache von 50 abgerundet. Die Rangkorrelation (Spearman) wurde über die Orte mit Jahresangabe berechnet. Wüstungen sind nicht berücksichtigt (vgl. die Auswertung zu den Wüstungen).",
        f"The basis are the fields first_mention_year and historic_forms of the gazetteer entries of the {n} municipalities (G1–G6). The year of first mention is the earliest year of documentary mention of the place name given in the article; where no explicit statement exists, the earliest dated name form up to 1700 was used (column first_basis). Number of name forms = all documentary and dialect forms named in the article except today's spelling (dialect forms in quotation marks are counted as far as they are recorded in the entry historic_forms). Half-century = year rounded down to a multiple of 50. The rank correlation (Spearman) was computed over the places with a year. Deserted villages are not included (see the analysis of the Wüstungen)."),
    "findings": findings,
    "caveats": [
        bi("Das Jahr der Erstnennung ist das früheste vom Verfasser genannte, nicht notwendig das früheste überlieferte; Brückner zitiert nach Urkundenbüchern und Verzeichnissen seiner Zeit. Bei einzelnen Orten bezieht es sich auf eine Person, die sich nach dem Ort nannte, oder auf eine Landestheilungsakte (1647: Grumbach, Titschendorf).",
           "The year of first mention is the earliest named by the author, not necessarily the earliest that survives; Brückner cites charter books and registers of his time. For some places it refers to a person who took the place's name, or to a partition record (1647: Grumbach, Titschendorf)."),
        bi(f"Bei {len([r for r in rows if r[7] == 'früheste datierte Namensform'])} Orten fehlt die ausdrückliche Jahresangabe und wurde aus der frühesten datierten Namensform übernommen; {n - nd} Orte haben gar kein Jahr. Die Zahl der Namensformen hängt davon ab, wie ausführlich der Verfasser sie anführt, und ist kein Maß der historischen Überlieferung.",
           f"For {len([r for r in rows if r[7] == 'früheste datierte Namensform'])} places the explicit year is missing and was taken from the earliest dated name form; {n - nd} places have no year at all. The number of name forms depends on how extensively the author lists them and is no measure of the historical record."),
    ],
    "datasets": [
        {"name": "mentions", "title": bi("Erste Erwähnung und Namensformen je Gemeinde", "First mention and name forms per municipality"),
         "columns": cols, "rows": rows, "source_refs": refs},
    ],
    "charts": charts,
    "keywords": {"de": ["Ersterwähnung", "urkundliche Erwähnung", "Ortsnamen", "Namensformen", "Dörfer", "Mittelalter", "Urkunden"],
                 "en": ["first mention", "documentary evidence", "place names", "name forms", "villages", "Middle Ages", "charters"]},
    "related": ["ortsnamen-sorbische-wurzeln", "orte-wuestungen-ortskunde", "orte-siedlungsbild-1867"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(a)
