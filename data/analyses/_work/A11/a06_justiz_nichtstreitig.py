"""A11-06: Nichtstreitige Gerichtsbarkeit der Justizämter 1864-1867 (p. 285): Uebereignungen, Pfandbestellungen, Vormundschaft, Nachlass."""
from common import *


def expand(row):
    out = []
    for c in row:
        parts = str(c).split()
        if len(parts) > 1 and all(p.isdigit() for p in parts):
            out += parts
        else:
            out.append(c)
    return out


g = [expand(r) for r in grid("285", "b2")]
assert len(g) == 15 and all(len(r) == 18 for r in g[3:]), [len(r) for r in g]
names = ["Gera I", "Gera II", "Hirschberg", "Hohenleuben", "Lobenstein I", "Lobenstein II", "Schleiz I", "Schleiz II"]
court_rows = {n: g[3 + i] for i, n in enumerate(names)}
assert court_rows["Gera I"][0].startswith("Gera I") and court_rows["Schleiz II"][0].startswith("Schleiz II")
year_rows = {1867: g[11], 1866: g[12], 1865: g[13], 1864: g[14]}
assert g[11][0] == "Summe 1867" and g[14][1] == "178", g[14]

N = lambda x: num(x) or 0
# column map (0-based): 1 ue_alt 2 ue_neu 3 ue_erl_alt 4 ue_erl_neu 5 rest_alt 6 rest_neu 7 pf_alt 8 pf_neu 9 pf_erl_alt 10 pf_erl_neu 11 pf_rest_neu
# 12 vm_mit 13 vm_ohne 14 nl_alt 15 nl_neu 16 nl_erl_alt 17 nl_erl_neu
yearly = []
for y in (1864, 1865, 1866, 1867):
    r = year_rows[y]
    yearly.append([y, N(r[1]), N(r[2]), N(r[7]), N(r[8]), N(r[12]), N(r[13]), N(r[14]), N(r[15])])
print(yearly)

courts = []
guard = []
for n in names:
    r = court_rows[n]
    ue, pf, vm, vo = N(r[2]), N(r[8]), N(r[12]), N(r[13])
    courts.append([n, ue, pf, vm, vo, round(pf / ue, 2)])
    guard.append([n, "a", "Mit Verwaltung", "With administration", vm])
    guard.append([n, "b", "Ohne Verwaltung", "Without administration", vo])
long_land = []
for n, ue, pf, vm, vo, ratio in courts:
    long_land.append([n, "a", "Übereignungen (neu)", "Conveyances (new)", ue])
    long_land.append([n, "b", "Pfandbestellungen (neu)", "Mortgage registrations (new)", pf])
# year series long format
series = []
for y, ue_a, ue_n, pf_a, pf_n, vm, vo, nl_a, nl_n in yearly:
    series += [[y, "a", "Übereignungen (neu)", "Conveyances (new)", ue_n], [y, "b", "Pfandbestellungen (neu)", "Mortgage registrations (new)", pf_n],
               [y, "c", "Nachlassregulierungen (neu)", "Estate settlements (new)", nl_n]]
Y = {r[0]: r for r in yearly}
pct = lambda a, b: 100 * a / b
chg = lambda i: pct(Y[1867][i] - Y[1864][i], Y[1864][i])
vm_tot = lambda y: Y[y][5] + Y[y][6]
tot_ue = sum(c[1] for c in courts)
tot_pf = sum(c[2] for c in courts)
assert tot_ue == Y[1867][2] and tot_pf == Y[1867][4]
gera_ue = pct(courts[0][1] + courts[1][1], tot_ue)
gera_pf = pct(courts[0][2] + courts[1][2], tot_pf)
hi = max(courts, key=lambda c: c[5])
lo = min(courts, key=lambda c: c[5])
print(chg(2), chg(4), chg(8), vm_tot(1864), vm_tot(1867), gera_ue, gera_pf, hi, lo)


def D(x, nd=0):
    return fmt_de(x, nd)


def E(x, nd=0):
    return fmt_en(x, nd)


ana = {
    "id": "justiz-freiwillige-gerichtsbarkeit-1864-1867",
    "title": bi("Freiwillige Gerichtsbarkeit der Justizämter 1864–1867: Eigentumsübertragungen, Pfandbestellungen, Vormundschaften, Nachlässe", "Non-contentious jurisdiction of the Justizämter, 1864–1867: conveyances, mortgages, guardianships, estates"),
    "category": "justice",
    "section": "t1-4-4",
    "sources": [{"page": "285", "block": "b2", "rows": "r4-r15"}, {"page": "285", "block": "b3"}],
    "summary": bi(
        f"Neben den Prozessen führten die Justizämter die »nichtstreitige Gerichtsbarkeit«: Eigentumsübertragungen (Uebereignungen) und Pfandbestellungen im Grund- und Hypothekenwesen, Vormundschaften und Nachlassregulierungen. Brückner gibt die Zahlen für die acht Gerichtsabteilungen und die Jahre 1864–1867. Die Auswertung zeigt, wie Hypotheken und Nachlässe schneller zunahmen als Eigentumswechsel und wie sich die Geschäfte auf die Gerichte verteilen.",
        f"Besides lawsuits the Justizämter handled “non-contentious jurisdiction”: conveyances of property and mortgage registrations in the land and mortgage registry, guardianships and estate settlements. Brückner gives the figures for the eight court divisions and the years 1864–1867. The analysis shows how mortgages and estates grew faster than changes of ownership and how the business is distributed among the courts.",
    ),
    "method": bi(
        "Quelle ist die Tabelle »Nichtstreitige Gerichtsbarkeit« (S. 285, b2). Jede Zelle der Spalten Nachlassregulierung (alt/neu) ist im Transkript als »32 117« zusammengefasst und wurde getrennt. Die Jahresreihe nutzt die Zeilen Summe 1867, 1866, 1865, 1864; die Verteilung auf Gerichte bezieht sich auf 1867. »neu« = im Jahr neu eingegangene Nummern, »alt« = aus Vorjahren übernommene. Das Verhältnis Pfandbestellungen : Uebereignungen ist abgeleitet.",
        "The source is the table “Nichtstreitige Gerichtsbarkeit” (p. 285, b2). In the transcript the cells of the estate-settlement columns (old/new) are fused as “32 117” and were separated. The yearly series uses the rows Summe 1867, 1866, 1865, 1864; the distribution among the courts refers to 1867. “new” = numbers received in the year, “old” = carried over from earlier years. The ratio of mortgage registrations to conveyances is derived.",
    ),
    "findings": [
        bi(f"Von 1864 bis 1867 nahmen die neuen Pfandbestellungen um {D(chg(4),1)} % zu ({D(Y[1864][4])} auf {D(Y[1867][4])}), die neuen Nachlassregulierungen um {D(chg(8),1)} % ({D(Y[1864][8])} auf {D(Y[1867][8])}), die neuen Eigentumsübertragungen nur um {D(chg(2),1)} % ({D(Y[1864][2])} auf {D(Y[1867][2])}).",
           f"From 1864 to 1867 new mortgage registrations rose by {E(chg(4),1)} % ({E(Y[1864][4])} to {E(Y[1867][4])}), new estate settlements by {E(chg(8),1)} % ({E(Y[1864][8])} to {E(Y[1867][8])}), new conveyances by only {E(chg(2),1)} % ({E(Y[1864][2])} to {E(Y[1867][2])})."),
        bi(f"1867 kamen auf 100 neue Eigentumsübertragungen {D(100*tot_pf/tot_ue,0)} neue Pfandbestellungen (1864: {D(100*Y[1864][4]/Y[1864][2],0)}). Der Quotient reicht 1867 von {D(lo[5],2)} ({lo[0]}) bis {D(hi[5],2)} ({hi[0]}).",
           f"In 1867 there were {E(100*tot_pf/tot_ue,0)} new mortgage registrations per 100 new conveyances (1864: {E(100*Y[1864][4]/Y[1864][2],0)}). The ratio ranges in 1867 from {E(lo[5],2)} ({lo[0]}) to {E(hi[5],2)} ({hi[0]})."),
        bi(f"Die beiden geraer Justizämter führen {D(gera_ue,1)} % der Eigentumsübertragungen und {D(gera_pf,1)} % der Pfandbestellungen des Landes.",
           f"The two Gera Justizämter handle {E(gera_ue,1)} % of the conveyances and {E(gera_pf,1)} % of the mortgage registrations of the country."),
        bi(f"Vormundschaften: 1867 {D(vm_tot(1867))} (davon nur {D(Y[1867][5])} mit Verwaltung), 1864 {D(vm_tot(1864))}; die Zahl wuchs um {D(pct(vm_tot(1867)-vm_tot(1864), vm_tot(1864)),1)} %.",
           f"Guardianships: {E(vm_tot(1867))} in 1867 (only {E(Y[1867][5])} of them with administration), {E(vm_tot(1864))} in 1864; the number grew by {E(pct(vm_tot(1867)-vm_tot(1864), vm_tot(1864)),1)} %."),
    ],
    "caveats": [
        bi("Brückner erklärt die Spalten nicht näher. »Vormundschaft mit/ohne Verwaltung« wird hier als Zahl der laufenden Vormundschaften gelesen (nicht als Neueingänge); das ergibt sich aus der Größenordnung (3.668 gegenüber 449 neuen Nachlassfällen), ist aber eine Deutung.",
           "Brückner does not explain the columns. “Guardianship with/without administration” is read here as the number of ongoing guardianships (not new receipts); this follows from the order of magnitude (3,668 against 449 new estate cases) but is an interpretation."),
        bi("Nach der Anmerkung der Tabelle kamen Reste vorjähriger Nummern bei den Pfandbestellungen in keinem Jahr vor; die Spalte »Rest« betrifft daher nur neue Nummern. Einwohnerzahlen je Gerichtsbezirk fehlen, daher sind keine Pro-Kopf-Raten möglich.",
           "According to the table's note, remainders of earlier numbers never occurred for the mortgage registrations; the “remainder” column therefore refers to new numbers only. Population figures per court district are missing, so no per-capita rates are possible."),
    ],
    "datasets": [
        {"name": "series", "title": bi("Neue Fälle der nichtstreitigen Gerichtsbarkeit je Jahr", "New non-contentious cases per year"),
         "columns": [
             col("year", "Jahr", "Year", "integer"),
             col("measure_key", "Kürzel", "Key", "string"),
             col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
             col("cases", "Anzahl neuer Nummern", "Number of new cases", "integer", "Fälle"),
         ],
         "rows": series, "source_refs": [{"page": "285", "block": "b2", "rows": "r12-r15"}]},
        {"name": "land", "title": bi("Eigentumsübertragungen und Pfandbestellungen nach Gericht, 1867", "Conveyances and mortgage registrations by court, 1867"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("measure_key", "Kürzel", "Key", "string"),
             col("measure_de", "Messgröße", "Measure", "string"), col("measure_en", "Messgröße (englisch)", "Measure (English)", "string"),
             col("cases", "Anzahl neuer Nummern", "Number of new cases", "integer", "Fälle"),
         ],
         "rows": long_land, "source_refs": [{"page": "285", "block": "b2", "rows": "r4-r11"}]},
        {"name": "guardianship", "title": bi("Vormundschaften nach Gericht, 1867", "Guardianships by court, 1867"),
         "columns": [
             col("court", "Gericht", "Court", "string"),
             col("kind_key", "Kürzel", "Key", "string"),
             col("kind_de", "Art", "Kind", "string"), col("kind_en", "Art (englisch)", "Kind (English)", "string"),
             col("cases", "Vormundschaften", "Guardianships", "integer", "Fälle"),
         ],
         "rows": guard, "source_refs": [{"page": "285", "block": "b2", "rows": "r4-r11"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "series",
         "title": bi("Neue Fälle der nichtstreitigen Gerichtsbarkeit", "New non-contentious cases"),
         "caption": bi("Alle Justizämter, neue Nummern je Jahr. Pfandbestellungen und Nachlassregulierungen wachsen schneller als Eigentumsübertragungen.",
                       "All Justizämter, new numbers per year. Mortgage registrations and estate settlements grow faster than conveyances."),
         "vegalite": {
             "height": 280,
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "ordinal", "title": bi("Jahr", "Year"), "axis": {"labelAngle": 0}},
                 "y": {"field": "cases", "type": "quantitative", "title": bi("Fälle", "Cases"), "scale": {"zero": True}},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}, "legend": {"labelLimit": 400, "columns": 2}},
                 "tooltip": [tt("year", "Jahr", "Year"), ttf("measure", "Messgröße", "Measure"), tt("cases", "Fälle", "Cases")]}}},
        {"id": "c2", "dataset": "land",
         "title": bi("Eigentumsübertragungen und Pfandbestellungen nach Gericht, 1867", "Conveyances and mortgage registrations by court, 1867"),
         "caption": bi(f"Neue Nummern 1867. Die geraer Justizämter führen die meisten Geschäfte; in Gera I ({D(hi[5],2)} Pfandbestellungen je Übertragung) überwiegen die Pfandbestellungen deutlich, in Schleiz I ({D(lo[5],2)}) die Eigentumsübertragungen.",
                       f"New numbers in 1867. The Gera Justizämter handle the most business; in Gera I ({E(hi[5],2)} mortgage registrations per conveyance) mortgages clearly predominate, in Schleiz I ({E(lo[5],2)}) conveyances do."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": {"field": "cases", "op": "sum", "order": "descending"}},
                 "yOffset": {"field": F("measure"), "sort": {"field": "measure_key", "op": "min"}},
                 "x": {"field": "cases", "type": "quantitative", "title": bi("Fälle", "Cases")},
                 "color": {"field": F("measure"), "type": "nominal", "title": None, "sort": {"field": "measure_key", "op": "min"}, "legend": {"labelLimit": 400}},
                 "tooltip": [tt("court", "Gericht", "Court"), ttf("measure", "Messgröße", "Measure"), tt("cases", "Fälle", "Cases")]}}},
        {"id": "c3", "dataset": "guardianship",
         "title": bi("Vormundschaften nach Gericht, 1867", "Guardianships by court, 1867"),
         "caption": bi("Zahl der Vormundschaften; ganz überwiegend ohne Verwaltung des Mündelvermögens durch das Gericht. Hohenleuben hat mit 53 von 375 den höchsten Anteil mit Verwaltung.",
                       "Number of guardianships; the vast majority without administration of the ward's property by the court. Hohenleuben has the highest share with administration (53 of 375)."),
         "vegalite": {
             "height": 300,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "court", "type": "nominal", "title": None, "sort": {"field": "cases", "op": "sum", "order": "descending"}},
                 "x": {"field": "cases", "type": "quantitative", "title": bi("Vormundschaften", "Guardianships"), "stack": "zero"},
                 "color": {"field": F("kind"), "type": "nominal", "title": None, "sort": {"field": "kind_key", "op": "min"}, "legend": {"labelLimit": 400}},
                 "order": {"field": "kind_key", "type": "nominal", "sort": "descending"},
                 "tooltip": [tt("court", "Gericht", "Court"), ttf("kind", "Art", "Kind"), tt("cases", "Fälle", "Cases")]}}},
    ],
    "keywords": {"de": ["Nichtstreitige Gerichtsbarkeit", "Freiwillige Gerichtsbarkeit", "Uebereignungen", "Pfandbestellungen", "Hypotheken", "Vormundschaft", "Nachlass", "Grundbuch", "Justizamt"],
                 "en": ["non-contentious jurisdiction", "conveyance", "mortgage", "guardianship", "estate", "land registry", "Justizamt"]},
}
write(ana)
