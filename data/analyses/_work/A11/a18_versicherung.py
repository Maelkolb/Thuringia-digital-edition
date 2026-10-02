"""A11-18: Feuerversicherung 1867: versicherte Gebäude und Mobilien nach Orten; konzessionierte Versicherungsgesellschaften (pp. 303-304)."""
from common import *

g2 = grid("304", "b2")
g3 = grid("304", "b3")
AREAS = [
    ("a", "Gera", "Gera", "Stadt", "Town", 1), ("b", "Schleiz", "Schleiz", "Stadt", "Town", 2), ("c", "Tanna", "Tanna", "Stadt", "Town", 3),
    ("d", "Saalburg", "Saalburg", "Stadt", "Town", 4), ("e", "Lobenstein", "Lobenstein", "Stadt", "Town", 5), ("f", "Hirschberg", "Hirschberg", "Stadt", "Town", 6),
    ("g", "Landgemeinden Gera", "Rural communities, Gera", "Land", "Country", 7), ("h", "Landgemeinden Schleiz", "Rural communities, Schleiz", "Land", "Country", 8),
    ("i", "Landgemeinden Lobenstein-Ebersdorf", "Rural communities, Lobenstein-Ebersdorf", "Land", "Country", 9),
]
rows = []
for k, nde, nen, kde, ken, ri in AREAS:
    r2, r3 = g2[ri], g3[ri]
    b = int(num(r2[2]))
    val_b = int(num(r2[4])) if ri == 1 else int(num(r2[5]))
    m = int(num(r3[2]))
    val_m = int(num(r3[4]))
    rows.append([k, nde, nen, kde, ken, b, val_b, m, val_m, round(val_b / b, 0), round(100 * m / b, 1), round(val_m / m, 0)])
tot_b = sum(r[5] for r in rows)
tot_vb = sum(r[6] for r in rows)
tot_m = sum(r[7] for r in rows)
tot_vm = sum(r[8] for r in rows)
assert (tot_b, tot_vb, tot_m, tot_vm) == (18773, 20079612, 6771, 12524342), (tot_b, tot_vb, tot_m, tot_vm)
print(rows)
rows_out = [[r[0], r[1], r[2], 'a' if r[3] == 'Stadt' else 'b', r[3], r[4]] + r[5:] for r in rows]

town = [r for r in rows if r[3] == "Stadt"]
land = [r for r in rows if r[3] == "Land"]
tb, tvb = sum(r[5] for r in town), sum(r[6] for r in town)
lb, lvb = sum(r[5] for r in land), sum(r[6] for r in land)
tm, lm = sum(r[7] for r in town), sum(r[7] for r in land)
tvm, lvm = sum(r[8] for r in town), sum(r[8] for r in land)
print(tb, tvb / tb, lb, lvb / lb, tm / tb * 100, lm / lb * 100, tvm / tvb, lvm / lvb)

# long format: value by area and kind
val_long = []
for r in rows:
    val_long.append([r[0], r[1], r[2], "a", "Gebäude", "Buildings", r[6]])
    val_long.append([r[0], r[1], r[2], "b", "Mobilien", "Movables", r[8]])

# insurance companies authorised (p. 303 b5)
COMP = [("a", "Feuer", "Fire", 31), ("b", "Leben und Renten", "Life and annuities", 35), ("c", "Hagel", "Hail", 12), ("d", "Vieh", "Livestock", 8), ("e", "Sonstige", "Other", 4)]
comp = [list(c) for c in COMP]
comp_total = sum(c[3] for c in COMP)
print(comp_total)
hi = max(rows, key=lambda r: r[9])
lo = min(rows, key=lambda r: r[9])
pctf = lambda a, b: 100 * a / b
mh = max(rows, key=lambda r: r[10])
ml = min(rows, key=lambda r: r[10])


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "versicherung-feuerversicherung-1867-orte",
    "title": bi("Feuerversicherung 1867: versicherte Gebäude und Mobilien nach Orten", "Fire insurance in 1867: insured buildings and movables by place"),
    "category": "finance",
    "section": "t1-4-8",
    "sources": [{"page": "304", "block": "b2", "rows": "r2-r11"}, {"page": "304", "block": "b3", "rows": "r2-r11"}, {"page": "303", "block": "b5"}, {"page": "304", "block": "b1"}],
    "summary": bi(
        f"Ende 1867 waren im Fürstentum {D(tot_b)} Gebäude mit {D(tot_vb)} Thalern und {D(tot_m)} Mobiliarversicherungen über {D(tot_vm)} Thaler gegen Feuer versichert. Brückner nennt die Zahlen für sechs Städte und die Landgemeinden der drei Bezirke. Die Auswertung zeigt, wie sich die Versicherungssummen auf Orte verteilen und wo die Mobiliarversicherung verbreitet war; außerdem die Zahl der im Land zugelassenen Versicherungsgesellschaften nach Sparten.",
        f"At the end of 1867 {E(tot_b)} buildings insured for {E(tot_vb)} Thaler and {E(tot_m)} movables policies for {E(tot_vm)} Thaler were covered against fire in the principality. Brückner gives the figures for six towns and the rural communities of the three districts. The analysis shows how the insured sums are distributed among places and where movables insurance was widespread; it also shows the number of insurance companies licensed in the country by branch.",
    ),
    "method": bi(
        "Quelle sind die beiden Tabellen »An Immobiliar« und »An Mobilien« (S. 304, b2/b3); die Summen des Fürstentums (18.773 Gebäude, 20.079.612 Thaler; 6771 und 12.524.342 Thaler) stimmen mit der Addition der Einzelzeilen überein. Abgeleitet sind die Versicherungssumme je Gebäude, die Zahl der Mobiliarversicherungen je 100 Gebäude und die Summe je Mobiliarversicherung. Die Zahl der Gesellschaften steht im Text S. 303 (b5). Alle Beträge in Thalern.",
        "The sources are the two tables “Real estate” and “Movables” (p. 304, b2/b3); the totals of the principality (18,773 buildings, 20,079,612 Thaler; 6,771 and 12,524,342 Thaler) agree with the sum of the individual rows. Derived are the insured sum per building, the number of movables policies per 100 buildings and the sum per movables policy. The number of companies is in the text of p. 303 (b5). All amounts in Thaler.",
    ),
    "findings": [
        bi(f"Im Durchschnitt sind die Gebäude mit {D(tot_vb/tot_b,0)} Thalern versichert; in den sechs Städten mit {D(tvb/tb,0)}, in den Landgemeinden mit {D(lvb/lb,0)} Thalern je Gebäude. Am höchsten liegt die Summe in {hi[1]} ({D(hi[9],0)}), am niedrigsten in {lo[1]} ({D(lo[9],0)}).",
           f"On average buildings are insured for {E(tot_vb/tot_b,0)} Thaler; in the six towns for {E(tvb/tb,0)}, in the rural communities for {E(lvb/lb,0)} Thaler per building. The sum is highest in {hi[2]} ({E(hi[9],0)}) and lowest in {lo[2]} ({E(lo[9],0)})."),
        bi(f"Die Landgemeinden stellen {D(pctf(lb,tot_b),0)} % der versicherten Gebäude, aber nur {D(pctf(lvb,tot_vb),0)} % der Versicherungssumme; die Stadt Gera allein hat {D(pctf(rows[0][5],tot_b),0)} % der Gebäude und {D(pctf(rows[0][6],tot_vb),0)} % der Summe.",
           f"The rural communities account for {E(pctf(lb,tot_b),0)} % of the insured buildings but only {E(pctf(lvb,tot_vb),0)} % of the insured sum; the town of Gera alone has {E(pctf(rows[0][5],tot_b),0)} % of the buildings and {E(pctf(rows[0][6],tot_vb),0)} % of the sum."),
        bi(f"Mobiliarversicherungen gibt es in den Städten {D(pctf(tm,tb),0)} je 100 Gebäude, in den Landgemeinden nur {D(pctf(lm,lb),0)}; Spitzenwerte haben {mh[1]} ({D(mh[10],0)}) und {sorted(rows, key=lambda r: -r[10])[1][1]} ({D(sorted(rows, key=lambda r: -r[10])[1][10],0)}), den niedrigsten Wert {ml[1]} ({D(ml[10],0)}).",
           f"There are {E(pctf(tm,tb),0)} movables policies per 100 buildings in the towns but only {E(pctf(lm,lb),0)} in the rural communities; the highest values are in {mh[2]} ({E(mh[10],0)}) and {sorted(rows, key=lambda r: -r[10])[1][2]} ({E(sorted(rows, key=lambda r: -r[10])[1][10],0)}), the lowest in {ml[2]} ({E(ml[10],0)})."),
        bi(f"Im Land sind {D(comp_total)} Versicherungsgesellschaften zugelassen: 31 Feuer-, 35 Lebens- und Renten-, 12 Hagel-, 8 Vieh- und 4 sonstige; Versicherungszwang besteht nur im früheren Fürstenthum Lobenstein (S. 303).",
           f"{E(comp_total)} insurance companies are licensed in the country: 31 fire, 35 life and annuity, 12 hail, 8 livestock and 4 others; compulsory insurance exists only in the former principality of Lobenstein (p. 303)."),
    ],
    "caveats": [
        bi("Brückner erklärt nicht, was bei den Mobilien gezählt wird; die Zahl (z. B. 2996 in Gera) wird hier als Zahl der Mobiliarversicherungen gelesen, nicht als Zahl der Gebäude. Die Quote je 100 Gebäude ist daher nur ein Anhaltspunkt für die Verbreitung. Nach Brückner sind insbesondere alle Staatsgebäude, Kirchen, Pfarreien und Schulen versichert (S. 304).",
           "Brückner does not explain what is counted for movables; the figure (e.g. 2,996 in Gera) is read here as the number of movables policies, not of buildings. The ratio per 100 buildings is therefore only an indication of prevalence. According to Brückner, all state buildings, churches, parsonages and schools in particular are insured (p. 304)."),
        bi("Die Versicherungssummen sind Versicherungswerte, keine Schätzungen des tatsächlichen Gebäudewerts; Gera, Lobenstein, Tanna und Wurzbach sind von der magdeburger Landfeuersocietät ausgeschlossen (S. 303), die Gesellschaften sind nicht aufgeschlüsselt. Die Gebäudezahlen gelten Ende 1867 und sind nicht mit der Hausstatistik (Wohnhäuser) gleichzusetzen.",
           "The sums are insured values, not estimates of actual building values; Gera, Lobenstein, Tanna and Wurzbach are excluded from the Magdeburg rural fire society (p. 303), the companies are not broken down. The building numbers refer to the end of 1867 and are not identical with the housing statistics (dwelling houses)."),
    ],
    "datasets": [
        {"name": "places", "title": bi("Versicherte Gebäude und Mobilien nach Orten, Ende 1867", "Insured buildings and movables by place, end of 1867"),
         "columns": [
             col("key", "Kürzel", "Key", "string"),
             col("place_de", "Ort", "Place", "string"), col("place_en", "Ort (englisch)", "Place (English)", "string"),
             col("kind_key", "Kürzel Art", "Kind key", "string"), col("kind_de", "Art", "Kind", "string"), col("kind_en", "Art (englisch)", "Kind (English)", "string"),
             col("buildings", "Versicherte Gebäude", "Insured buildings", "integer", "Gebäude"),
             col("buildings_value", "Versicherungssumme Gebäude", "Insured sum, buildings", "integer", "Thaler"),
             col("movables", "Mobiliarversicherungen", "Movables policies", "integer", "Anzahl"),
             col("movables_value", "Versicherungssumme Mobilien", "Insured sum, movables", "integer", "Thaler"),
             col("value_per_building", "Summe je Gebäude", "Sum per building", "number", "Thaler", derived=True),
             col("policies_per_100", "Mobiliarversicherungen je 100 Gebäude", "Movables policies per 100 buildings", "number", "je 100", derived=True),
             col("value_per_policy", "Summe je Mobiliarversicherung", "Sum per movables policy", "number", "Thaler", derived=True),
         ],
         "rows": rows_out, "source_refs": [{"page": "304", "block": "b2", "rows": "r2-r10"}, {"page": "304", "block": "b3", "rows": "r2-r10"}]},
        {"name": "values", "title": bi("Versicherungssummen nach Ort und Art (lang)", "Insured sums by place and kind (long format)"),
         "columns": [col("key", "Kürzel", "Key", "string"), col("place_de", "Ort", "Place", "string"), col("place_en", "Ort (englisch)", "Place (English)", "string"),
                     col("kind_key", "Kürzel Art", "Kind key", "string"), col("kind_de", "Art", "Kind", "string"), col("kind_en", "Art (englisch)", "Kind (English)", "string"),
                     col("value", "Versicherungssumme", "Insured sum", "integer", "Thaler")],
         "rows": val_long, "source_refs": [{"page": "304", "block": "b2", "rows": "r2-r10"}, {"page": "304", "block": "b3", "rows": "r2-r10"}]},
        {"name": "companies", "title": bi("Zugelassene Versicherungsgesellschaften nach Sparte", "Licensed insurance companies by branch"),
         "columns": [col("key", "Kürzel", "Key", "string"), col("branch_de", "Sparte", "Branch", "string"), col("branch_en", "Sparte (englisch)", "Branch (English)", "string"), col("companies", "Gesellschaften", "Companies", "integer", "Gesellschaften")],
         "rows": comp, "source_refs": [{"page": "303", "block": "b5"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "places",
         "title": bi("Versicherungssumme je Gebäude", "Insured sum per building"),
         "caption": bi("Thaler je versichertes Gebäude, Ende 1867. Blau: Städte, orange: Landgemeinden.", "Thaler per insured building, end of 1867. Blue: towns, orange: rural communities."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("place"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "value_per_building", "type": "quantitative", "title": bi("Thaler je Gebäude", "Thaler per building"), "axis": {"format": ",d"}},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}},
                 "tooltip": [ttf("place", "Ort", "Place"), tt("buildings", "Gebäude", "Buildings"), {"field": "buildings_value", "title": bi("Summe (Thaler)", "Sum (Thaler)"), "format": ","}, {"field": "value_per_building", "title": bi("je Gebäude", "per building"), "format": ",.0f"}]}}},
        {"id": "c2", "dataset": "places",
         "title": bi("Mobiliarversicherungen je 100 Gebäude", "Movables policies per 100 buildings"),
         "caption": bi("Anzahl der Mobiliarversicherungen bezogen auf die Zahl der versicherten Gebäude (Anhaltspunkt für die Verbreitung).", "Number of movables policies relative to the number of insured buildings (indication of prevalence)."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("place"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "policies_per_100", "type": "quantitative", "title": bi("Mobiliarversicherungen je 100 Gebäude", "Movables policies per 100 buildings")},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}},
                 "tooltip": [ttf("place", "Ort", "Place"), tt("movables", "Mobiliarversicherungen", "Movables policies"), tt("buildings", "Gebäude", "Buildings"), {"field": "policies_per_100", "title": bi("je 100 Gebäude", "per 100 buildings"), "format": ".1f"}]}}},
        {"id": "c3", "dataset": "values",
         "title": bi("Versicherungssummen nach Ort", "Insured sums by place"),
         "caption": bi("Millionen Thaler; Gebäude und Mobilien gestapelt.", "Millions of Thaler; buildings and movables stacked."),
         "vegalite": {
             "height": 320,
             "mark": "bar",
             "transform": [{"calculate": "datum.value / 1000000", "as": "mio"}],
             "encoding": {
                 "y": {"field": F("place"), "type": "nominal", "sort": {"field": "value", "op": "sum", "order": "descending"}, "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "mio", "type": "quantitative", "title": bi("Millionen Thaler", "Million Thaler"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "ascending"},
                 "tooltip": [ttf("place", "Ort", "Place"), ttf("kind", "Art", "Kind"), {"field": "value", "title": bi("Thaler", "Thaler"), "format": ","}]}}},
        {"id": "c4", "dataset": "companies",
         "title": bi("Zugelassene Versicherungsgesellschaften nach Sparte", "Licensed insurance companies by branch"),
         "caption": bi("Gesellschaften mit Betriebskonzession im Fürstentum (meist über Agenten vertreten); »Sonstige« = Hypotheken-, Glas-, Mühlen- und Transportversicherung.", "Companies with an operating licence in the principality (mostly represented by agents); “Other” = mortgage, glass, mill and transport insurance."),
         "vegalite": {
             "height": 220,
             "mark": "bar",
             "encoding": {
                 "y": {"field": F("branch"), "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 360}},
                 "x": {"field": "companies", "type": "quantitative", "title": bi("Gesellschaften", "Companies")},
                 "tooltip": [ttf("branch", "Sparte", "Branch"), tt("companies", "Gesellschaften", "Companies")]}}},
    ],
    "keywords": {"de": ["Feuerversicherung", "Brandversicherung", "Versicherung", "Gebäude", "Mobilien", "Versicherungsgesellschaften", "Gera", "Schleiz"],
                 "en": ["fire insurance", "insurance", "buildings", "movables", "insurance companies", "Gera", "Schleiz"]},
}
write(ana)
