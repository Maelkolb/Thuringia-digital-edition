"""A06 / analysis 6: births, deaths, population change and net migration per three-year period 1859-1867 (pp. 98-99)."""
from common import *

NAMES = {"Landrathsbezirk Gera.": "Gera", "Landrathsbezirk Schleiz.": "Schleiz",
         "Landrathsbezirk Lobenstein-Ebersdorf.": "Lobenstein-Ebersdorf", "Das Fürstenthum.": "Fürstenthum"}
rows = {}


def add(g):
    cur = None
    for r in g[1:]:
        if not r[0].isdigit():
            cur = NAMES[[x for x in r if x][0]]
            continue
        rows.setdefault(cur, []).append(r)


add(grid("98", "b4"))
add(grid("99", "b1"))
assert all(len(v) == 9 for v in rows.values()), {k: len(v) for k, v in rows.items()}

# census populations (p. 91/92) for 1858, 1861, 1864, 1867
g91, g92 = grid("91", "b4"), grid("92", "b1")
blocks = {"Gera": g91[2:17], "Schleiz": g91[18:32], "Lobenstein-Ebersdorf": g92[4:19], "Fürstenthum": g92[20:34]}
pop = {d: {int(r[0]): integer(r[10]) for r in rs} for d, rs in blocks.items()}

vital = []
periods = []
PER = [(1859, 1861), (1862, 1864), (1865, 1867)]
START = {1859: 1858, 1862: 1861, 1865: 1864}
for d in DIST_KEYS:
    rs = rows[d]
    for r in rs:
        y, b, dd = int(r[0]), integer(r[1]), integer(r[2])
        vital.append([d, y, b, dd, b - dd])
    for (y0, y1) in PER:
        first = next(r for r in rs if int(r[0]) == y0)
        sur, inc, em = integer(first[3]), integer(first[4]), integer(first[5])
        bsum = sum(integer(r[1]) for r in rs if y0 <= int(r[0]) <= y1)
        dsum = sum(integer(r[2]) for r in rs if y0 <= int(r[0]) <= y1)
        assert bsum - dsum == sur, (d, y0, bsum - dsum, sur)
        assert sur - inc == em, (d, y0)
        p0, p1 = pop[d][START[y0]], pop[d][y1]
        mean = (p0 + p1) / 2
        n = 3
        periods.append([d, f"{y0}–{y1}", y0, y1, bsum, dsum, sur, inc, em, -em, p0, p1, round(mean),
                        round(sur / n / mean * 1000, 2), round(-em / n / mean * 1000, 2), round(inc / n / mean * 1000, 2)])
        # check census change vs printed increase (Schleiz differs by 1 from the 27174/27175 misprint)
        if p1 - p0 != inc:
            print("census diff", d, y0, p1 - p0, inc)
# principality equals the sum of the districts every year
for i in range(9):
    for j in (1, 2):
        s = sum(integer(rows[d][i][j]) for d in DIST_KEYS[:3])
        assert s == integer(rows["Fürstenthum"][i][j])
print("principality = sum of districts: OK")

P = {(r[0], r[1]): r for r in periods}
PL = [f"{a}–{b}" for a, b in PER]
fp = {pl: P[("Fürstenthum", pl)] for pl in PL}
lob = {pl: P[("Lobenstein-Ebersdorf", pl)] for pl in PL}
ger = {pl: P[("Gera", pl)] for pl in PL}
sch = {pl: P[("Schleiz", pl)] for pl in PL}
tot_sur = sum(fp[pl][6] for pl in PL)
tot_em = sum(fp[pl][8] for pl in PL)
tot_inc = sum(fp[pl][7] for pl in PL)
print(tot_sur, tot_em, tot_inc, tot_em / tot_sur)
lob_em_rate = [lob[pl][14] for pl in PL]
print([lob[pl][14] for pl in PL], [sch[pl][14] for pl in PL], [ger[pl][14] for pl in PL], [fp[pl][14] for pl in PL])
lob_tot_em = sum(lob[pl][8] for pl in PL)
sch_tot_em = sum(sch[pl][8] for pl in PL)
ger_tot_em = sum(ger[pl][8] for pl in PL)
print(lob_tot_em, sch_tot_em, ger_tot_em)

ana = {
    "id": "bevoelkerung-geburtensaldo-wanderung-1859-1867",
    "title": {"de": "Geburtenüberschuss, Bevölkerungszunahme und Wanderung 1859–1867",
              "en": "Natural increase, population change and migration, 1859–1867"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("98", "b3"), ("98", "b4", "r3-r21"), ("99", "b1", "r3-r21"), ("91", "b4", "r14-r17"), ("92", "b1", "r16-r19")),
    "summary": {
        "de": f"Brückner stellt für 1859–1867 die Geborenen und Gestorbenen jedes Jahres den Zählungsergebnissen gegenüber und leitet daraus für drei Dreijahreszeiträume den Wanderungssaldo ab (»mehr ausgewandert als eingewandert«). Im ganzen Fürstenthum standen einem Geburtenüberschuss von {de(tot_sur,0)} Personen nur {de(tot_inc,0)} mehr Einwohner gegenüber; der Unterschied von {de(tot_em,0)} Personen ({de(tot_em/tot_sur*100,0)} %) wird als Netto-Auswanderung gedeutet, am stärksten in Lobenstein-Ebersdorf.",
        "en": f"For 1859–1867 Brückner sets the births and deaths of each year against the census results and derives the migration balance for three three-year periods (“more emigrated than immigrated”). In the whole principality a birth surplus of {en(tot_sur,0)} persons was matched by an increase of only {en(tot_inc,0)} inhabitants; the difference of {en(tot_em,0)} persons ({en(tot_em/tot_sur*100,0)} %) is interpreted as net emigration, strongest in Lobenstein-Ebersdorf.",
    },
    "method": {
        "de": "Übernommen wurden die Geborenen und Gestorbenen je Jahr und Bezirk sowie Brückners Dreijahresspalten (»Mehr Geborene als Gestorbene«, »Zunahme der Bevölkerung«, »Mehr ausgewandert als eingewandert«; S. 98–99, über zwei Seiten verteilt). Die Dreijahreswerte stehen in der ersten Zeile jeder Periode (1859, 1862, 1865). Kontrolle: Die Summe der Geborenen minus Gestorbenen über drei Jahre ergibt in allen 12 Fällen den gedruckten Geburtenüberschuss, Überschuss minus Zunahme den gedruckten Wanderungssaldo, die Bezirke summieren sich zum Fürstenthum, und die Zunahme entspricht der Differenz der Zählungen 1858–61–64–67 (S. 91–92). Abgeleitet wurden der Wanderungssaldo mit Vorzeichen (negativ = Auswanderungsüberschuss) und drei Raten je 1000 Einwohner und Jahr, bezogen auf die mittlere Bevölkerung (Mittel der beiden Zählungen, die den Zeitraum einschließen).",
        "en": "Taken over are the births and deaths per year and district and Brückner's three-year columns (“more born than died”, “increase of the population”, “more emigrated than immigrated”; pp. 98–99, spread over two pages). The three-year values stand in the first row of each period (1859, 1862, 1865). Checks: births minus deaths over three years give the printed birth surplus in all 12 cases, surplus minus increase gives the printed migration balance, the districts add up to the principality, and the increase equals the difference of the censuses 1858–61–64–67 (pp. 91–92). Derived are the migration balance with sign (negative = net emigration) and three rates per 1,000 inhabitants per year, related to the mean population (mean of the two censuses enclosing the period).",
    },
    "findings": [
        {"de": f"Im Fürstenthum standen den Geburtenüberschüssen von {de(fp[PL[0]][6],0)}, {de(fp[PL[1]][6],0)} und {de(fp[PL[2]][6],0)} Personen Zunahmen von nur {de(fp[PL[0]][7],0)}, {de(fp[PL[1]][7],0)} und {de(fp[PL[2]][7],0)} gegenüber; die Differenz (Wanderungssaldo) betrug {de(fp[PL[0]][8],0)}, {de(fp[PL[1]][8],0)} und {de(fp[PL[2]][8],0)}.",
         "en": f"In the principality the birth surpluses of {en(fp[PL[0]][6],0)}, {en(fp[PL[1]][6],0)} and {en(fp[PL[2]][6],0)} persons were matched by increases of only {en(fp[PL[0]][7],0)}, {en(fp[PL[1]][7],0)} and {en(fp[PL[2]][7],0)}; the difference (migration balance) was {en(fp[PL[0]][8],0)}, {en(fp[PL[1]][8],0)} and {en(fp[PL[2]][8],0)}."},
        {"de": f"Lobenstein-Ebersdorf verlor in jedem Zeitraum Einwohner durch Wanderung ({de(lob[PL[0]][8],0)}, {de(lob[PL[1]][8],0)}, {de(lob[PL[2]][8],0)}; {de(-max(lob[pl][14] for pl in PL),1)} bis {de(-min(lob[pl][14] for pl in PL),1)} je 1000 und Jahr); 1859–61 und 1865–67 überstieg der Wanderungsverlust den Geburtenüberschuss, so dass die Bevölkerung absolut abnahm ({de(lob[PL[0]][7],0)} bzw. {de(lob[PL[2]][7],0)}).",
         "en": f"Lobenstein-Ebersdorf lost inhabitants through migration in every period ({en(lob[PL[0]][8],0)}, {en(lob[PL[1]][8],0)}, {en(lob[PL[2]][8],0)}; {en(-max(lob[pl][14] for pl in PL),1)} to {en(-min(lob[pl][14] for pl in PL),1)} per 1,000 per year); in 1859–61 and 1865–67 the migration loss exceeded the birth surplus, so the population declined in absolute terms ({en(lob[PL[0]][7],0)} and {en(lob[PL[2]][7],0)})."},
        {"de": f"Schleiz hatte in allen drei Zeiträumen einen Auswanderungsüberschuss ({de(sch[PL[0]][8],0)}, {de(sch[PL[1]][8],0)}, {de(sch[PL[2]][8],0)}); der Bezirk Gera wechselt: 1862–64 gewann er per Saldo {de(-ger[PL[1]][8],0)} Personen durch Zuwanderung, sonst verlor er wenige ({de(ger[PL[0]][8],0)} und {de(ger[PL[2]][8],0)}).",
         "en": f"Schleiz had net emigration in all three periods ({en(sch[PL[0]][8],0)}, {en(sch[PL[1]][8],0)}, {en(sch[PL[2]][8],0)}); the district of Gera alternates: in 1862–64 it gained {en(-ger[PL[1]][8],0)} persons by net immigration, otherwise it lost few ({en(ger[PL[0]][8],0)} and {en(ger[PL[2]][8],0)})."},
        {"de": f"Über die neun Jahre summiert, verlor das Fürstenthum durch Wanderung {de(tot_em,0)} Personen, das sind {de(tot_em/tot_sur*100,0)} % des Geburtenüberschusses von {de(tot_sur,0)}: Lobenstein-Ebersdorf {de(lob_tot_em,0)}, Schleiz {de(sch_tot_em,0)}; Gera dagegen gewann per Saldo {de(-ger_tot_em,0)} Personen.",
         "en": f"Summed over the nine years, the principality lost {en(tot_em,0)} persons by migration, i.e. {en(tot_em/tot_sur*100,0)} % of the birth surplus of {en(tot_sur,0)}: Lobenstein-Ebersdorf {en(lob_tot_em,0)}, Schleiz {en(sch_tot_em,0)}; Gera, by contrast, gained {en(-ger_tot_em,0)} persons on balance."},
    ],
    "caveats": [
        {"de": "Der »Wanderungssaldo« ist ein Restwert (Geburtenüberschuss minus Zählungsunterschied) und enthält alle Zähl- und Registrierungsfehler sowie Unterschiede zwischen Wohn- und anwesender Bevölkerung; er ist keine Auswanderungsstatistik. Geburten und Todesfälle folgen den Kirchen- bzw. Standesbüchern, die Zählung dem Stichtag im Dezember.",
         "en": "The “migration balance” is a residual (birth surplus minus census difference) and contains all counting and registration errors and differences between resident and present population; it is not an emigration statistic. Births and deaths follow the parish and civil registers, the census the reference date in December."},
        {"de": "Die Zeiträume (1859–61, 1862–64, 1865–67) entsprechen den Zählintervallen 1858–61, 1861–64 und 1864–67 (Zählungen im Abstand von drei Jahren). Die gedruckte Zunahme von Schleiz 1862–64 (818) und 1865–67 (193) setzt die Gesamtzahl 27 175 für 1864 voraus, S. 91 druckt 27 174.",
         "en": "The periods (1859–61, 1862–64, 1865–67) correspond to the census intervals 1858–61, 1861–64 and 1864–67 (counts three years apart). The printed increase of Schleiz in 1862–64 (818) and 1865–67 (193) presupposes the total 27,175 for 1864, whereas p. 91 prints 27,174."},
        {"de": "Die Geborenen- und Gestorbenenzahlen je Jahr werden in den Auswertungen zu Geburten und Sterblichkeit (S. 107 ff., 113 ff.) im Einzelnen behandelt; hier dienen sie nur der Bilanz.",
         "en": "The births and deaths per year are treated in detail in the analyses of births and mortality (p. 107 ff., 113 ff.); here they serve only for the balance."},
    ],
    "datasets": [
        {"name": "vital", "title": {"de": "Geborene und Gestorbene je Jahr", "en": "Births and deaths per year"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("births", "Geborene", "Births", "integer", "Personen"),
             col("deaths", "Gestorbene", "Deaths", "integer", "Personen"),
             col("natural_increase", "Geborene minus Gestorbene", "Births minus deaths", "integer", "Personen", True),
         ],
         "rows": vital, "source_refs": refs(("98", "b4", "r3-r21"), ("99", "b1", "r3-r21"))},
        {"name": "periods", "title": {"de": "Dreijahresbilanz: Geburtenüberschuss, Zunahme, Wanderung", "en": "Three-year balance: birth surplus, increase, migration"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("period", "Zeitraum", "Period", "string", None, True),
             col("year_from", "Von Jahr", "From year", "integer", None, True),
             col("year_to", "Bis Jahr", "To year", "integer", None, True),
             col("births_sum", "Geborene (3 Jahre)", "Births (3 years)", "integer", "Personen", True),
             col("deaths_sum", "Gestorbene (3 Jahre)", "Deaths (3 years)", "integer", "Personen", True),
             col("natural_increase", "Mehr Geborene als Gestorbene", "Birth surplus", "integer", "Personen"),
             col("increase", "Zunahme der Bevölkerung", "Increase of the population", "integer", "Personen"),
             col("net_emigration", "Mehr ausgewandert als eingewandert", "Net emigration", "integer", "Personen"),
             col("net_migration", "Wanderungssaldo (negativ = Auswanderung)", "Net migration (negative = emigration)", "integer", "Personen", True),
             col("pop_start", "Bevölkerung zu Beginn (Zählung)", "Population at start (census)", "integer", "Personen"),
             col("pop_end", "Bevölkerung am Ende (Zählung)", "Population at end (census)", "integer", "Personen"),
             col("pop_mean", "Mittlere Bevölkerung", "Mean population", "integer", "Personen", True),
             col("natural_per_1000", "Geburtenüberschuss je 1000 und Jahr", "Birth surplus per 1,000 per year", "number", "‰", True),
             col("migration_per_1000", "Wanderungssaldo je 1000 und Jahr", "Net migration per 1,000 per year", "number", "‰", True),
             col("change_per_1000", "Zunahme je 1000 und Jahr", "Increase per 1,000 per year", "number", "‰", True),
         ],
         "rows": periods, "source_refs": refs(("98", "b4", "r3-r21"), ("99", "b1", "r3-r21"), ("91", "b4", "r14-r17"), ("92", "b1", "r16-r19"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "periods",
         "title": {"de": "Woher kam die Zunahme? Geburtenüberschuss und Wanderung je Dreijahreszeitraum", "en": "Where did the increase come from? Birth surplus and migration per three-year period"},
         "caption": {"de": "Je Bezirk und Zeitraum: Geburtenüberschuss (nach oben) und Wanderungssaldo (negativ = mehr Aus- als Einwanderung, nach unten). Die Zahl über dem Balken ist die Veränderung der Einwohnerzahl; der Zeitraum steht jeweils unter dem Bezirk in der Reihenfolge 1859–61, 1862–64, 1865–67.",
                     "en": "For each district and period: birth surplus (upwards) and migration balance (negative = more emigrants than immigrants, downwards). The figure above each bar is the change in the number of inhabitants; the periods follow in the order 1859–61, 1862–64, 1865–67 within each district."},
         "vegalite": {
             "height": 360,
             "transform": [{"filter": "datum.district != 'Fürstenthum'"},
                           {"fold": ["natural_increase", "net_migration"], "as": ["component", "persons"]},
                           {"calculate": "datum.increase >= 0 ? '+' + format(datum.increase, ',') : '−' + format(-datum.increase, ',')", "as": "inc_label"},
                           {"calculate": "max(datum.natural_increase, datum.increase)", "as": "label_y"}],
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "x": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DIST_KEYS[:3]}, "axis": {"labelAngle": 0, "labelPadding": 16}},
                      "xOffset": {"field": "period", "type": "nominal", "scale": {"domain": PL}},
                      "y": {"field": "persons", "type": "quantitative", "title": {"de": "Personen je Zeitraum", "en": "Persons per period"}, "scale": {"domain": [-1500, 2700]}},
                      "color": {"field": "component", "type": "nominal", "scale": {"domain": ["natural_increase", "net_migration"]},
                                "legend": {"title": None, "labelLimit": 320, "labelExpr": {"de": "datum.label == 'natural_increase' ? 'Geburtenüberschuss' : 'Wanderungssaldo'", "en": "datum.label == 'natural_increase' ? 'Birth surplus' : 'Net migration'"}}},
                      "tooltip": [tt("district", "Bezirk", "District"), tt("period", "Zeitraum", "Period"),
                                  tt_fmt("natural_increase", "Geburtenüberschuss", "Birth surplus", ","), tt_fmt("net_migration", "Wanderungssaldo", "Net migration", ","),
                                  tt_fmt("increase", "Zunahme der Bevölkerung", "Increase of the population", ",")]}},
                 {"transform": [{"filter": "datum.component == 'natural_increase'"}],
                  "mark": {"type": "text", "dy": -6, "fontSize": 11},
                  "encoding": {
                      "x": {"field": "district", "type": "nominal", "scale": {"domain": DIST_KEYS[:3]}},
                      "xOffset": {"field": "period", "type": "nominal", "scale": {"domain": PL}},
                      "y": {"field": "label_y", "type": "quantitative", "scale": {"domain": [-1500, 2700]}},
                      "text": {"field": "inc_label", "type": "nominal"}}},
                 {"transform": [{"filter": "datum.component == 'net_migration'"}],
                  "mark": {"type": "text", "fontSize": 10},
                  "encoding": {
                      "x": {"field": "district", "type": "nominal", "scale": {"domain": DIST_KEYS[:3]}},
                      "xOffset": {"field": "period", "type": "nominal", "scale": {"domain": PL}},
                      "y": {"value": 352},
                      "text": {"field": "period", "type": "nominal"}}},
             ]}},
        {"id": "c2", "dataset": "periods",
         "title": {"de": "Wanderungssaldo je 1000 Einwohner und Jahr", "en": "Net migration per 1,000 inhabitants per year"},
         "caption": {"de": "Wanderungssaldo bezogen auf die mittlere Bevölkerung des Zeitraums (negativ = Auswanderungsüberschuss). Lobenstein-Ebersdorf verliert in allen drei Zeiträumen deutlich mehr Menschen je 1000 Einwohner als Schleiz oder Gera.",
                     "en": "Net migration related to the mean population of the period (negative = net emigration). In all three periods Lobenstein-Ebersdorf loses markedly more people per 1,000 inhabitants than Schleiz or Gera."},
         "vegalite": {
             "height": 300,
             "transform": [DIST_TRANSFORM],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "period", "type": "nominal", "scale": {"domain": PL}, "title": {"de": "Zeitraum", "en": "Period"}, "axis": {"labelAngle": 0}},
                 "xOffset": {"field": "district", "type": "nominal", "scale": {"domain": DIST_KEYS}},
                 "y": {"field": "migration_per_1000", "type": "quantitative", "title": {"de": "‰ pro Jahr (negativ = Auswanderung)", "en": "‰ per year (negative = emigration)"}},
                 "color": color_dist(),
                 "tooltip": [tt("district_label", "Bezirk", "District"), tt("period", "Zeitraum", "Period"),
                             tt_fmt("migration_per_1000", "Wanderungssaldo je 1000 und Jahr", "Net migration per 1,000 per year", ".1f"),
                             tt_fmt("natural_per_1000", "Geburtenüberschuss je 1000 und Jahr", "Birth surplus per 1,000 per year", ".1f"),
                             tt_fmt("change_per_1000", "Zunahme je 1000 und Jahr", "Increase per 1,000 per year", ".1f")]}}},
    ],
    "keywords": {"de": ["Auswanderung", "Wanderung", "Geburtenüberschuss", "Bevölkerungszunahme", "Geborene", "Gestorbene", "Lobenstein", "Schleiz", "Gera", "Wanderungssaldo", "Bevölkerungsbilanz"],
                 "en": ["emigration", "migration", "natural increase", "population change", "births", "deaths", "Lobenstein", "Schleiz", "Gera", "net migration", "population balance"]},
    "related": ["bevoelkerung-entwicklung-1647-1867", "bevoelkerung-geburten-1858-1867", "bevoelkerung-sterblichkeit-1858-1867"],
}
write(ana)
