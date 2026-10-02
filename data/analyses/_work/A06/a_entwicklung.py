"""A06 / analysis 1: population development 1647-1867 per Landrathsbezirk (pp. 91-92)."""
from common import *

g91 = grid("91", "b4")
g92 = grid("92", "b1")
blocks = {
    "Gera": g91[2:17],                  # r3-r17
    "Schleiz": g91[18:32],              # r19-r32
    "Lobenstein-Ebersdorf": g92[4:19],  # r5-r19
    "Fürstenthum": g92[20:34],          # r21-r34
}
rows = []
for d, rs in blocks.items():
    for r in rs:
        assert r[0].isdigit(), r
        y = int(r[0])
        male, female, total = integer(r[8]), integer(r[9]), integer(r[10])
        rows.append([d, y, integer(r[1]), male, female, total, num(r[11])])

by = {}
for r in rows:
    by.setdefault(r[0], []).append(r)

# consistency: districts add up to the principality in every common year
tot_by = {d: {r[1]: r[5] for r in rs} for d, rs in by.items()}
for y, t in tot_by["Fürstenthum"].items():
    s = sum(tot_by[d].get(y, 0) for d in DIST_KEYS[:3])
    print("sum check", y, s, t, "OK" if s == t else "MISMATCH")

census = []
for d, rs in by.items():
    base = rs[0][5]
    prev = None
    for r in rs:
        d_, y, fam, m, f, t, gp = r
        gc = None
        if prev:
            n = y - prev[0]
            gc = round(((t / prev[1]) ** (1 / n) - 1) * 100, 2)
        census.append([d_, y, fam, m, f, t, gp, gc, round(t / base * 100, 1)])
        prev = (y, t)


def tot(d, y):
    return tot_by[d][y]


factors = []
for d in DIST_KEYS:
    for (y0, y1) in ((1647, 1867), (1833, 1867)):
        fac = tot(d, y1) / tot(d, y0)
        rate = (fac ** (1 / (y1 - y0)) - 1) * 100
        factors.append([d, f"{y0}–{y1}", y0, y1, round(fac, 2), round(rate, 2)])

rates = []
for d in DIST_KEYS:
    seq = [r for r in by[d] if r[1] >= 1834]
    for a, b in zip(seq, seq[1:]):
        n = b[1] - a[1]
        rates.append([d, a[1], b[1], n, round(((b[5] / a[5]) ** (1 / n) - 1) * 100, 2)])

F = {(r[0], r[1]): r for r in factors}
f_all = {d: F[(d, "1647–1867")][4] for d in DIST_KEYS}
f_33 = {d: F[(d, "1833–1867")][4] for d in DIST_KEYS}
r_all = {d: F[(d, "1647–1867")][5] for d in DIST_KEYS}
LOB = "Lobenstein-Ebersdorf"
lob = [r for r in rows if r[0] == LOB and r[1] >= 1833]
lob_peak = max(lob, key=lambda r: r[5])
lob_1867 = tot(LOB, 1867)
neg = [(r[1], r[2]) for r in rates if r[0] == LOB and r[4] < 0]
print("Lob negative intervals", neg, "peak", lob_peak[1], lob_peak[5])
jump_g = (tot("Gera", 1834) / tot("Gera", 1833) - 1) * 100
jump_l = (tot(LOB, 1834) / tot(LOB, 1833) - 1) * 100
neg_de = ", ".join(f"{a}–{str(b)[2:]}" for a, b in neg)
neg_en = ", ".join(f"{a}–{str(b)[2:]}" for a, b in neg)
print(f_all, f_33, r_all, jump_g, jump_l)

ana = {
    "id": "bevoelkerung-entwicklung-1647-1867",
    "title": {"de": "Bevölkerungsentwicklung 1647–1867 nach Landrathsbezirken",
              "en": "Population development 1647–1867 by district"},
    "category": "population",
    "section": SECTION,
    "sources": refs(("91", "b4", "r3-r32"), ("92", "b1", "r5-r34"), ("92", "b2")),
    "summary": {
        "de": f"Brückner stellt die Einwohnerzahl der drei Landrathsbezirke Gera, Schleiz und Lobenstein-Ebersdorf und des ganzen Fürstenthums für 1647, 1784/94 und die Zählungen von 1833 bis 1867 zusammen. Die Bevölkerung wuchs von {de(tot('Fürstenthum',1647),0)} auf {de(tot('Fürstenthum',1867),0)} Einwohner, am stärksten im Bezirk Gera, während Lobenstein-Ebersdorf seit 1855 stagniert und leicht zurückgeht.",
        "en": f"Brückner compiles the number of inhabitants of the three districts Gera, Schleiz and Lobenstein-Ebersdorf and of the whole principality for 1647, 1784/94 and the censuses from 1833 to 1867. The population grew from {en(tot('Fürstenthum',1647),0)} to {en(tot('Fürstenthum',1867),0)}, most strongly in the district of Gera, while Lobenstein-Ebersdorf has stagnated and declined slightly since 1855.",
    },
    "method": {
        "de": "Aus den Tabellen auf S. 91–92 wurden je Bezirk die Zahl der Familien, die männliche, weibliche und gesamte Bevölkerung sowie Brückners »jährliche Zu- oder Abnahme in Proc.« übernommen (die Altersklassen derselben Tabellen behandelt die Auswertung zu Geschlecht und Alter). Abgeleitet wurden der Index (1647 = 100), die durchschnittliche jährliche Zuwachsrate zwischen je zwei aufeinanderfolgenden Zählungen als Zinseszinsrate ((N₂/N₁)^(1/Jahre) − 1) und die Vermehrungsfaktoren 1647–1867 und 1833–1867. Brückners gedruckte Raten sind für 1647–1794 bzw. 1647–1833 Zinseszinsraten, für 1794–1833 (Gera) und 1784–1833 (Lobenstein-Ebersdorf) aber lineare Mittel; die berechneten Raten sind daher durchgehend vergleichbar. Die Zwischenzählung vor 1833 trägt bei Gera das Jahr 1794, bei Lobenstein-Ebersdorf 1784, Schleiz und das Fürstenthum haben keine. Die Summen der drei Bezirke stimmen in allen gemeinsamen Zählungen mit den gedruckten Zahlen für das Fürstenthum überein, außer 1864 (86 471 statt gedruckt 86 472; Ursache ist der unten genannte Druckfehler bei Schleiz).",
        "en": "From the tables on pp. 91–92 the number of families, the male, female and total population per district and Brückner's “annual increase or decrease in per cent” were taken (the age classes of the same tables are treated in the analysis of sex and age). Derived are the index (1647 = 100), the mean annual growth rate between successive counts as a compound rate ((N₂/N₁)^(1/years) − 1), and the growth factors 1647–1867 and 1833–1867. Brückner's printed rates are compound rates for 1647–1794 and 1647–1833 but linear means for 1794–1833 (Gera) and 1784–1833 (Lobenstein-Ebersdorf); the computed rates are therefore consistently comparable. The intermediate count before 1833 carries the year 1794 for Gera and 1784 for Lobenstein-Ebersdorf; Schleiz and the principality have none. In every common census the sums of the three districts agree with the printed figures for the principality, except 1864 (86,471 against the printed 86,472), which stems from the Schleiz misprint mentioned below.",
    },
    "findings": [
        {"de": f"Von 1647 bis 1867 vergrößerte sich die Bevölkerung des Fürstenthums auf das {de(f_all['Fürstenthum'],2)}fache ({de(r_all['Fürstenthum'],2)} % pro Jahr); Gera wuchs auf das {de(f_all['Gera'],2)}fache, Lobenstein-Ebersdorf auf das {de(f_all[LOB],2)}fache, Schleiz auf das {de(f_all['Schleiz'],2)}fache.",
         "en": f"From 1647 to 1867 the principality's population grew by a factor of {en(f_all['Fürstenthum'],2)} ({en(r_all['Fürstenthum'],2)} % per year); Gera grew by {en(f_all['Gera'],2)}, Lobenstein-Ebersdorf by {en(f_all[LOB],2)} and Schleiz by {en(f_all['Schleiz'],2)}."},
        {"de": f"Seit 1833 nahm Gera um {de((f_33['Gera']-1)*100,0)} %, Schleiz um {de((f_33['Schleiz']-1)*100,0)} % und Lobenstein-Ebersdorf nur um {de((f_33[LOB]-1)*100,0)} % zu (Fürstenthum: {de((f_33['Fürstenthum']-1)*100,0)} %).",
         "en": f"Since 1833 Gera has grown by {en((f_33['Gera']-1)*100,0)} %, Schleiz by {en((f_33['Schleiz']-1)*100,0)} % and Lobenstein-Ebersdorf by only {en((f_33[LOB]-1)*100,0)} % (principality: {en((f_33['Fürstenthum']-1)*100,0)} %)."},
        {"de": f"Lobenstein-Ebersdorf erreichte 1855 mit {de(lob_peak[5],0)} Einwohnern seinen Höchststand und lag 1867 mit {de(lob_1867,0)} um {de((1-lob_1867/lob_peak[5])*100,1)} % darunter; negative Zuwachsraten zeigen die Intervalle {neg_de}. Brückner führt dies auf den Niedergang der Eisen- und Wollindustrie und die dadurch ausgelöste Auswanderung zurück.",
         "en": f"Lobenstein-Ebersdorf reached its peak in 1855 with {en(lob_peak[5],0)} inhabitants and stood {en((1-lob_1867/lob_peak[5])*100,1)} % lower in 1867 ({en(lob_1867,0)}); negative growth rates appear in the intervals {neg_en}. Brückner attributes this to the decline of the iron and wool industries and the emigration it caused."},
        {"de": f"Zwischen den Zählungen 1833 und 1834 springt Gera um {de(jump_g,1)} % nach oben, Lobenstein-Ebersdorf um {de(-jump_l,1)} % nach unten; solche gegenläufigen Sprünge innerhalb eines Jahres deuten darauf hin, dass die Zählung von 1833 nicht nach denselben Regeln erfolgte wie die ab 1834.",
         "en": f"Between the counts of 1833 and 1834 Gera jumps up by {en(jump_g,1)} % while Lobenstein-Ebersdorf falls by {en(-jump_l,1)} %; opposite jumps within one year suggest that the 1833 count followed different rules than those from 1834 on."},
    ],
    "caveats": [
        {"de": "Die Zählungen vor 1833 (1647, 1784/1794) beruhen auf Verzeichnissen anderer Art; die Wachstumsraten über die lange Spanne 1647–1833 sind Durchschnitte über Kriege, Seuchen und Hungerjahre und sagen nichts über den Verlauf dazwischen.",
         "en": "The counts before 1833 (1647, 1784/1794) rest on registers of a different kind; the growth rates over the long span 1647–1833 are averages across wars, epidemics and famines and say nothing about the course in between."},
        {"de": "Druckfehler im Original (die Transkription entspricht dem Faksimile): Im Text auf S. 92 nennt Brückner eine Vermehrung des Landes »um das 2,63fache« (aus seinen Zahlen folgt 3,68) und für Gera »4,55fache« (4,56); die Rate 1833–34 des Fürstenthums ist mit 0,69 statt 0,87 % gedruckt. Gera 1834: Summe der über 14-Jährigen 18 698 statt 18 693; Schleiz 1864: männlich + weiblich ergibt 27 175, gedruckt 27 174.",
         "en": "Misprints in the original (the transcription matches the facsimile): in the text on p. 92 Brückner gives an increase of the country “by 2.63 times” (his own figures give 3.68) and “4.55” for Gera (4.56); the 1833–34 rate of the principality is printed as 0.69 instead of 0.87 %. Gera 1834: sum of the over-14s printed as 18,698 instead of 18,693; Schleiz 1864: male + female add up to 27,175, the printed total is 27,174."},
        {"de": "Die Jahre der Zwischenzählung weichen voneinander ab (Gera 1794, Lobenstein-Ebersdorf 1784), Schleiz hat keine; die Linie im Diagramm verbindet dort nur die gedruckten Punkte.",
         "en": "The years of the intermediate counts differ (Gera 1794, Lobenstein-Ebersdorf 1784) and Schleiz has none; the line in the chart merely connects the printed points."},
    ],
    "datasets": [
        {"name": "census", "title": {"de": "Einwohner und Familien nach Zählungen", "en": "Inhabitants and families by census"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year", "Jahr", "Year", "integer"),
             col("families", "Zahl der Familien", "Number of families", "integer", "Familien"),
             col("male", "Männlich", "Male", "integer", "Personen"),
             col("female", "Weiblich", "Female", "integer", "Personen"),
             col("total", "Einwohner insgesamt", "Inhabitants, total", "integer", "Personen"),
             col("growth_printed", "Jährliche Zu-/Abnahme (gedruckt)", "Annual change (as printed)", "number", "%"),
             col("growth_computed", "Jährliche Zu-/Abnahme (berechnet, Zinseszins)", "Annual change (computed, compound)", "number", "%", True),
             col("index_1647", "Index (1647 = 100)", "Index (1647 = 100)", "number", None, True),
         ],
         "rows": census,
         "source_refs": refs(("91", "b4", "r3-r32"), ("92", "b1", "r5-r34"))},
        {"name": "growth_factors", "title": {"de": "Vermehrungsfaktoren", "en": "Growth factors"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("period", "Zeitraum", "Period", "string", None, True),
             col("year_from", "Von Jahr", "From year", "integer", None, True),
             col("year_to", "Bis Jahr", "To year", "integer", None, True),
             col("factor", "Vermehrung um das …fache", "Growth factor", "number", "×", True),
             col("rate_pa", "Mittlere jährliche Zunahme", "Mean annual increase", "number", "%", True),
         ],
         "rows": factors,
         "source_refs": refs(("91", "b4", "r3-r32"), ("92", "b1", "r5-r34"))},
        {"name": "growth_rates", "title": {"de": "Jährliche Zuwachsrate je Zählintervall", "en": "Annual growth rate per census interval"},
         "columns": [
             col("district", "Bezirk", "District", "string"),
             col("year_from", "Von Jahr", "From year", "integer", None, True),
             col("year_to", "Bis Jahr", "To year", "integer", None, True),
             col("years", "Jahre", "Years", "integer", "Jahre", True),
             col("rate_pa", "Zuwachs pro Jahr", "Growth per year", "number", "%", True),
         ],
         "rows": rates,
         "source_refs": refs(("91", "b4", "r6-r17"), ("92", "b1", "r8-r19"))},
    ],
    "charts": [
        {"id": "c1", "dataset": "census",
         "title": {"de": "Einwohner 1647–1867", "en": "Inhabitants 1647–1867"},
         "caption": {"de": "Einwohnerzahl der drei Landrathsbezirke und des Fürstenthums nach den gedruckten Zählungen. Zwischen 1647 und 1833 gibt es höchstens eine Zwischenzählung (Gera 1794, Lobenstein-Ebersdorf 1784).",
                     "en": "Number of inhabitants of the three districts and the principality according to the printed counts. Between 1647 and 1833 there is at most one intermediate count (Gera 1794, Lobenstein-Ebersdorf 1784)."},
         "vegalite": {
             "height": 340,
             "transform": [DIST_TRANSFORM],
             "mark": {"type": "line", "point": True},
             "encoding": {
                 "x": {"field": "year", "type": "quantitative", "title": YEAR, "scale": {"domain": [1640, 1875]},
                       "axis": {"format": "d", "labelAngle": 0, "values": [1650, 1700, 1750, 1800, 1850]}},
                 "y": {"field": "total", "type": "quantitative", "title": {"de": "Einwohner", "en": "Inhabitants"}},
                 "color": color_dist(),
                 "tooltip": [tt("district_label", "Bezirk", "District"), tt("year", "Jahr", "Year"),
                             tt_fmt("total", "Einwohner", "Inhabitants", ","),
                             tt("growth_printed", "Zu-/Abnahme p. a. (gedruckt, %)", "Change p.a. (printed, %)")]}}},
        {"id": "c2", "dataset": "growth_factors",
         "title": {"de": "Vermehrung der Bevölkerung", "en": "Growth of the population"},
         "caption": {"de": "Faktor, um den die Einwohnerzahl 1867 größer war als 1647 bzw. 1833 (aus den gedruckten Einwohnerzahlen berechnet).",
                     "en": "Factor by which the number of inhabitants in 1867 exceeded that of 1647 and 1833 (computed from the printed figures)."},
         "vegalite": {
             "height": 280,
             "transform": [DIST_TRANSFORM],
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DIST_KEYS},
                       "axis": {"labelAngle": 0, "labelExpr": DIST_LABEL_EXPR}},
                 "y": {"field": "factor", "type": "quantitative", "title": {"de": "Faktor (×)", "en": "Factor (×)"}},
                 "tooltip": [tt("district_label", "Bezirk", "District"), tt("period", "Zeitraum", "Period"),
                             tt_fmt("factor", "Faktor", "Factor", ".2f"), tt_fmt("rate_pa", "Zuwachs p. a. (%)", "Growth p.a. (%)", ".2f")]},
             "layer": [
                 {"mark": "bar",
                  "encoding": {"xOffset": {"field": "period", "type": "nominal", "scale": {"domain": ["1647–1867", "1833–1867"]}}, "color": {"field": "period", "type": "nominal", "scale": {"domain": ["1647–1867", "1833–1867"]},
                                         "legend": {"title": {"de": "Zeitraum", "en": "Period"}}}}},
                 {"mark": {"type": "text", "dy": -6, "fontSize": 11},
                  "encoding": {"xOffset": {"field": "period", "type": "nominal", "scale": {"domain": ["1647–1867", "1833–1867"]}}, "text": {"field": "factor", "type": "quantitative", "format": ".2f"}}},
             ]}},
        {"id": "c3", "dataset": "growth_rates",
         "title": {"de": "Jährlicher Zuwachs je Zählintervall 1834–1867", "en": "Annual growth per census interval, 1834–1867"},
         "caption": {"de": "Durchschnittliche jährliche Zu- oder Abnahme zwischen zwei Zählungen (berechnet), eingetragen beim Jahr der späteren Zählung. Die gestrichelte Linie bei 0 trennt Wachstum von Schrumpfung.",
                     "en": "Mean annual increase or decrease between two counts (computed), plotted at the year of the later count. The dashed rule at 0 separates growth from shrinkage."},
         "vegalite": {
             "height": 320,
             "transform": [DIST_TRANSFORM],
             "layer": [
                 {"mark": {"type": "line", "point": True},
                  "encoding": {
                      "x": {"field": "year_to", "type": "quantitative", "title": {"de": "Jahr (Ende des Zählintervalls)", "en": "Year (end of the census interval)"}, "scale": {"domain": [1835, 1868]},
                            "axis": {"format": "d", "labelAngle": 0, "values": [1837, 1843, 1849, 1855, 1861, 1867]}},
                      "y": {"field": "rate_pa", "type": "quantitative", "title": {"de": "Zuwachs pro Jahr (%)", "en": "Growth per year (%)"}},
                      "color": color_dist(),
                      "tooltip": [tt("district_label", "Bezirk", "District"), tt("year_from", "Von", "From"), tt("year_to", "Bis", "To"),
                                  tt_fmt("rate_pa", "Zuwachs p. a. (%)", "Growth p.a. (%)", ".2f")]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 0}}},
             ]}},
    ],
    "keywords": {"de": ["Bevölkerung", "Einwohnerzahl", "Bevölkerungswachstum", "Volkszählung", "Gera", "Schleiz", "Lobenstein", "Ebersdorf", "1647", "Zuwachs"],
                 "en": ["population", "inhabitants", "population growth", "census", "Gera", "Schleiz", "Lobenstein", "Ebersdorf", "1647", "growth rate"]},
}
write(ana)
