"""Build analysis flaeche-fuerstenthum-vermessung-nachbarn (A01): pp. 7-8 (+ 3, 4)."""
from common import *

T = lambda de, en: {"de": de, "en": en}

MORGEN_HA = 0.255322            # p. 832: 1 preuss. Morgen = 0,255322 Hectaren
GEO_MEILE_M = 0.9894 * 7500     # p. 832: 1 geographische Meile = 0,9894 kuenftige Meile (7500 m)
PR_MEILE_M = 1.0043 * 7500      # p. 832: 1 preuss. Meile = 1,0043 kuenftige Meile
QM_GEO_KM2 = (GEO_MEILE_M / 1000) ** 2
QM_PR_KM2 = (PR_MEILE_M / 1000) ** 2

# ---- printed values (read from the page grids) --------------------------------------------------
g7 = grid("7", "b7")
old = [(r[0], num(r[1].replace("=", "").strip())) for r in g7]
assert [round(v, 2) for _, v in old] == [7.25, 6.1, 7.75]
g8 = grid("8", "b2")
(_, eng_a, now_a, lv_a, m_gera) = g8[4]
(_, _, _, _, m_saal) = g8[5]
(_, eng_b, now_b, lv_b, m_reich) = g8[6]
(_, _, _, _, m_schl) = g8[7]
(_, eng_c, _, lv_c, m_lob) = g8[8]
(_, eng_t, now_t, lv_t, m_tot) = g8[9]
E = dict(a=num(eng_a), b=num(eng_b), c=num(eng_c), t=num(eng_t))
N = dict(a=num(now_a), b=num(now_b), t=num(now_t))
L = dict(a=num(lv_a), b=num(lv_b), c=num(lv_c), t=num(lv_t))
morgen = [("Gera", int(m_gera)), ("Saalburg", int(m_saal)), ("Reichenfels", int(m_reich)),
          ("Schleiz", int(m_schl)), ("Lobenstein-Ebersdorf", int(m_lob))]
assert sum(m for _, m in morgen) == int(m_tot)
assert abs(sum(v for _, v in old) - 21.1) < 1e-9
assert abs(E["a"] + E["b"] + E["c"] - E["t"]) < 1e-9
assert abs(N["a"] + N["b"] - N["t"]) < 1e-9
assert abs(L["a"] + L["b"] + L["c"] - L["t"]) < 1e-9

# ---- datasets -------------------------------------------------------------------------------------
HS, EN, NO, LV = "Hassel/Stein", "Engelhardt", "Nowack", "Landesvermessung"
estimates = [
    [HS, 1, "Gera mit Saalburg, Neuärgerniß und Pöllwitz", old[0][1]],
    [HS, 1, "Schleiz", old[1][1]],
    [HS, 1, "Lobenstein-Ebersdorf", old[2][1]],
    [EN, 2, "Gera + Saalburg", E["a"]],
    [EN, 2, "Reichenfels + Schleiz", E["b"]],
    [EN, 2, "Lobenstein-Ebersdorf", E["c"]],
    [NO, 3, "Gera", N["a"]],
    [NO, 3, "Saalburg + Reichenfels + Schleiz + Lobenstein-Ebersdorf", N["b"]],
    [LV, 4, "Gera", L["a"]],
    [LV, 4, "Saalburg + Reichenfels + Schleiz", L["b"]],
    [LV, 4, "Lobenstein-Ebersdorf", L["c"]],
]
est_rows = []
for q, o, grp, v in estimates:
    est_rows.append([q, o, grp, v, round(v * QM_GEO_KM2, 1)])

tot_vals = [(HS, 1, 21.1), (EN, 2, E["t"]), (NO, 3, N["t"]), (LV, 4, L["t"])]
tot_rows = [[q, o, v, round(v * QM_GEO_KM2, 1)] for q, o, v in tot_vals]
mean_el = (E["t"] + L["t"]) / 2

ha_total = int(m_tot) * MORGEN_HA
km2_total = ha_total / 100
lt_rows = []
for name, m in morgen:
    ha = m * MORGEN_HA
    lt_rows.append([name, m, round(ha, 0), round(ha / 100, 1), round(100 * m / int(m_tot), 1)])
km2_per_qm = km2_total / L["t"]

NB = [
    ("Fürstenthum Reuß ä. L.", 4.99, "über 3 Mal größer", 3.0),
    ("Herzogthum S.-Koburg", 10.2, "um 1/3 größer", 4 / 3),
    ("Schwarzburg-Sondershausen", 15.63, "fast gleich", 1.0),
    ("Herzogthum S.-Altenburg", 24.00, "gegen 5/8", 5 / 8),
    ("Herzogthum S.-Meiningen", 44.97, "1/3", 1 / 3),
    ("Großherzogthum S.-Weimar", 66.03, "5/22", 5 / 22),
]
nb_rows = [["Fürstenthum Reuß j. L.", "Reuß j. L.", N["t"], None, None, None, round(N["t"] * QM_GEO_KM2, 1)]]
for name, a, txt, f in NB:
    comp = N["t"] / a
    nb_rows.append([name, "Vergleichsstaat", a, txt, round(f, 4), round(comp, 4), round(a * QM_GEO_KM2, 1)])
# sanity: values printed
txt8 = text("8", "b3")
for name, a, *_ in NB:
    s = f"{a:.2f}".replace(".", ",")
    assert s in txt8 or s.rstrip("0") in txt8, (name, s)

share_jl = N["t"] / (N["t"] + NB[0][1])
ratios = [(m_ger / q) for m_ger, q in ((morgen[0][1], L['a']), (sum(x for _, x in morgen[1:4]), L['b']), (morgen[4][1], L['c']))]
spread_ratio = 100 * (max(ratios) / min(ratios) - 1)
print('morgen per qm', ratios, spread_ratio)
unter, ober = 4.03, 11.03
print("km2_per_qm", km2_per_qm, "geo", QM_GEO_KM2, "pr", QM_PR_KM2, "deviation", km2_per_qm / QM_GEO_KM2 - 1)
print("total km2", km2_total, "ha", ha_total, "mean_el", mean_el)
print("share jl", share_jl, "ober share", ober / (ober + unter))
print([r for r in lt_rows])
print([ (r[0], r[5]) for r in nb_rows])
lob_drop_e = 1 - E["c"] / old[2][1]
lob_drop_l = 1 - L["c"] / old[2][1]
print(lob_drop_e, lob_drop_l, 1 - L["t"] / 21.1, 1 - E["t"] / 21.1)

DE_LAND = lambda x, nd=1: fmt(x, nd)
EN_LAND = lambda x, nd=1: fmt(x, nd, "en")
rank = sorted([r[2] for r in nb_rows])
n_smaller = sum(1 for r in nb_rows[1:] if r[2] < N["t"])
share_lob = lt_rows[4][4]; share_gera = lt_rows[0][4]; share_schl = lt_rows[3][4]; share_saal = lt_rows[1][4]; share_reich = lt_rows[2][4]
koburg = nb_rows[2]
print("koburg", koburg)

ana = {
    "id": "flaeche-fuerstenthum-vermessung-nachbarn",
    "title": T("Fläche des Fürstentums: Schätzungen, Landesvermessung und Nachbarstaaten",
               "Area of the principality: estimates, land survey and neighbouring states"),
    "category": "geography",
    "section": "t1-1-3",
    "sources": [
        {"page": "7", "block": "b6"}, {"page": "7", "block": "b7", "rows": "r1-r3"}, {"page": "8", "block": "b1"},
        {"page": "8", "block": "b2", "rows": "r5-r10"}, {"page": "8", "block": "b3"},
        {"page": "4", "block": "b2"}, {"page": "3", "block": "b3"}, {"page": "832", "block": "b2"}, {"page": "832", "block": "b12"},
    ],
    "summary": T(
        "Brückner stellt die Flächenangaben für das Fürstentum Reuß j. L. zusammen: die älteren Schätzungen bis 1840 (21,1 Quadratmeilen), zwei preußische Berechnungen, das Ergebnis der Landesvermessung (mit der Fläche in preußischen Morgen) und einen Größenvergleich mit sechs Nachbarstaaten. Die Auswertung zeigt, wie stark die Zahl nach unten korrigiert wurde, wie sich die Morgen-Angaben in Quadratkilometer übersetzen und ob Brückners Vergleichsbrüche mit seinen Zahlen übereinstimmen.",
        "Brückner collects the area figures for the principality of Reuss (younger line): the older estimates until 1840 (21.1 square miles), two Prussian calculations, the result of the land survey (with the area in Prussian Morgen) and a size comparison with six neighbouring states. The analysis shows how strongly the figure was revised downwards, how the Morgen figures translate into square kilometres and whether Brückner's comparison fractions agree with his numbers."),
    "method": T(
        f"Quelle sind die Tabellen S. 7 (ältere Schätzung) und S. 8 (preußische Berechnungen, Landesvermessung, Morgen) sowie die Vergleichszahlen im Text S. 8; Oberland und Unterland (11,03 und 4,03 □M.) stehen auf S. 4, die Dreiviertel-Angabe auf S. 3. Die Teilwerte wurden so übernommen, wie die Klammern im Druck sie zusammenfassen (die Gruppierung unterscheidet sich von Quelle zu Quelle, daher sind nur die Summen unmittelbar vergleichbar); alle Summen wurden nachgerechnet. Morgen → Hektar mit Brückners Faktor 1 preuß. Morgen = 0,255322 ha (S. 832). Quadratmeilen (»□M.«) wurden mit der geographischen Quadratmeile (1 geogr. Meile = 0,9894 × 7500 m, S. 832; also 1 □M. = {fmt(QM_GEO_KM2, 2)} km²) in km² umgerechnet; dass Brückner diese Meile meint, ist eine Annahme, die durch die Gesamtzahlen gestützt wird ({fmt_int(int(m_tot))} Morgen = {fmt(km2_total, 1)} km² entsprechen bei 14,965 □M. {fmt(km2_per_qm, 1)} km² je □M.).",
        f"Sources are the tables on p. 7 (older estimate) and p. 8 (Prussian calculations, land survey, Morgen) and the comparison figures in the text on p. 8; Oberland and Unterland (11.03 and 4.03 □M.) are on p. 4, the three-quarters statement on p. 3. Partial values were taken as the braces in the print group them (the grouping differs between sources, so only the totals are directly comparable); all totals were re-added. Morgen → hectares with Brückner's factor 1 Prussian Morgen = 0.255322 ha (p. 832). Square miles (“□M.”) were converted to km² with the geographical square mile (1 geographical mile = 0.9894 × 7500 m, p. 832; so 1 □M. = {fmt(QM_GEO_KM2, 2, 'en')} km²); that Brückner means this mile is an assumption supported by the totals ({fmt_int(int(m_tot), 'en')} Morgen = {fmt(km2_total, 1, 'en')} km² correspond to {fmt(km2_per_qm, 1, 'en')} km² per □M. at 14.965 □M.)."),
    "findings": [
        T(f"Die Schätzung sank von 21,1 □M. (Hassel und Stein, bis 1840) auf 15,15 (Engelhardt, 1853), 15,06 (Nowack) und 14,965 □M. (Landesvermessung), also um {fmt(100 * (1 - L['t'] / 21.1), 0)} %. Nowacks »maßgebende« Zahl ist, wie Brückner schreibt, das Mittel der beiden anderen neueren Angaben: ({fmt(E['t'], 2)} + {fmt(L['t'], 3)}) / 2 = {fmt(mean_el, 2)}.",
          f"The estimate fell from 21.1 □M. (Hassel and Stein, until 1840) to 15.15 (Engelhardt, 1853), 15.06 (Nowack) and 14.965 □M. (land survey), i.e. by {fmt(100 * (1 - L['t'] / 21.1), 0, 'en')} %. Nowack's “authoritative” figure is, as Brückner writes, the mean of the two other recent values: ({fmt(E['t'], 2, 'en')} + {fmt(L['t'], 3, 'en')}) / 2 = {fmt(mean_el, 2, 'en')}."),
        T(f"Der einzige Landestheil, der in der alten und den neuen Aufstellungen gleich abgegrenzt ist, Lobenstein-Ebersdorf, schrumpfte von 7,75 auf 4,83 (Engelhardt) bzw. 4,923 □M. (Landesvermessung), um {fmt(100 * lob_drop_e, 0)} bzw. {fmt(100 * lob_drop_l, 0)} %.",
          f"The only part delimited identically in the old and the new tables, Lobenstein-Ebersdorf, shrank from 7.75 to 4.83 (Engelhardt) and 4.923 □M. (land survey), by {fmt(100 * lob_drop_e, 0, 'en')} and {fmt(100 * lob_drop_l, 0, 'en')} %."),
        T(f"Die Landesvermessung ergibt {fmt_int(int(m_tot))} preußische Morgen = {fmt_int(ha_total)} ha = {fmt(km2_total, 1)} km². Davon entfallen {fmt(share_lob, 1)} % auf Lobenstein-Ebersdorf, {fmt(share_gera, 1)} % auf Gera, {fmt(share_schl, 1)} % auf Schleiz, {fmt(share_saal, 1)} % auf Saalburg und {fmt(share_reich, 1)} % auf Reichenfels.",
          f"The land survey gives {fmt_int(int(m_tot), 'en')} Prussian Morgen = {fmt_int(ha_total, 'en')} ha = {fmt(km2_total, 1, 'en')} km². Of this, {fmt(share_lob, 1, 'en')} % belong to Lobenstein-Ebersdorf, {fmt(share_gera, 1, 'en')} % to Gera, {fmt(share_schl, 1, 'en')} % to Schleiz, {fmt(share_saal, 1, 'en')} % to Saalburg and {fmt(share_reich, 1, 'en')} % to Reichenfels."),
        T(f"Setzt man die Landesvermessung ({fmt_int(int(m_tot))} Morgen) mit ihren 14,965 □M. gleich, ergeben sich {fmt(km2_per_qm, 1)} km² je □M. – {fmt(100 * abs(km2_per_qm / QM_GEO_KM2 - 1), 1)} % weniger als eine geographische Quadratmeile ({fmt(QM_GEO_KM2, 2)} km²), aber deutlich weniger als eine preußische ({fmt(QM_PR_KM2, 2)} km²). Brückners □M. ist daher am ehesten die geographische.",
          f"Equating the land survey ({fmt_int(int(m_tot), 'en')} Morgen) with its 14.965 □M. gives {fmt(km2_per_qm, 1, 'en')} km² per □M. – {fmt(100 * abs(km2_per_qm / QM_GEO_KM2 - 1), 1, 'en')} % less than a geographical square mile ({fmt(QM_GEO_KM2, 2, 'en')} km²) and clearly less than a Prussian one ({fmt(QM_PR_KM2, 2, 'en')} km²). Brückner's □M. is therefore most likely the geographical one."),
        T(f"Von den sechs Vergleichsstaaten sind nur {n_smaller} kleiner als das Fürstentum; es ist rund {fmt(N['t'] / NB[0][1], 1)} Mal so groß wie Reuß ä. L., und {fmt(100 * share_jl, 1)} % des reußischen Landes gehören zur jüngeren Linie (Brückner S. 3: »drei Viertel«). Fünf der sechs Vergleichsbrüche stimmen mit Brückners Zahlen überein; nur »um 1/3 größer als S.-Koburg« nicht: 15,06 / 10,2 = {fmt(koburg[5], 2)}, das Fürstentum ist also um rund {fmt(100 * (koburg[5] - 1), 0)} % größer.",
          f"Of the six comparison states, only {n_smaller} are smaller than the principality; it is about {fmt(N['t'] / NB[0][1], 1, 'en')} times as large as Reuss (elder line), and {fmt(100 * share_jl, 1, 'en')} % of the Reuss lands belong to the younger line (Brückner p. 3: “three quarters”). Five of the six comparison fractions agree with Brückner's figures; only “a third larger than Saxe-Coburg” does not: 15.06 / 10.2 = {fmt(koburg[5], 2, 'en')}, so the principality is about {fmt(100 * (koburg[5] - 1), 0, 'en')} % larger."),
    ],
    "caveats": [
        T(f"Die Teilsummen der Quellen sind nicht gleich gruppiert (z. B. fasst Engelhardt Gera mit Saalburg zusammen, Nowack alle Landestheile außer Gera); die »Landestheile« der Morgen-Spalte sind daher keine genauen Entsprechungen der □M.-Gruppen. Die Morgen-Zahlen und □M.-Zahlen der Landesvermessung sind nicht proportional (Morgen je □M. schwanken zwischen den drei Gruppen um {fmt(spread_ratio, 0)} %), vermutlich weil die Vermessung unvollständig und nicht trigonometrisch war (S. 8).",
          f"The partial sums of the sources are not grouped identically (e.g. Engelhardt combines Gera with Saalburg, Nowack all parts except Gera); the “parts” of the Morgen column therefore do not map exactly onto the □M. groups. The Morgen and □M. figures of the land survey are not proportional (Morgen per □M. vary by {fmt(spread_ratio, 0, 'en')} % between the three groups), presumably because the survey was incomplete and not trigonometric (p. 8)."),
        T("Die Umrechnung der □M. in km² unterstellt die geographische Quadratmeile; Brückner definiert die Einheit nicht. Mit der preußischen Meile (S. 832) wären die km²-Werte um rund 3 % höher.",
          "The conversion of □M. to km² assumes the geographical square mile; Brückner does not define the unit. With the Prussian mile (p. 832) the km² values would be about 3 % higher."),
        T("Brückners Fläche gehört zu den Grenzen von 1870; sie ist mit modernen Flächenangaben des früheren Fürstentums nicht ohne Weiteres vergleichbar.",
          "Brückner's area refers to the boundaries of 1870; it cannot simply be compared with modern area figures for the former principality."),
    ],
    "conversions": [
        {"from": "preußischer Morgen", "to": "Hektar", "factor_or_formula": "1 Morgen = 0,255322 ha", "reference": "Brückner S. 832, II. Flächenmaße"},
        {"from": "geographische Quadratmeile (□M.)", "to": "km²",
         "factor_or_formula": f"1 geogr. Meile = 0,9894 × 7500 m = {GEO_MEILE_M:.1f} m; 1 □M. = {QM_GEO_KM2:.2f} km²",
         "reference": "Brückner S. 832, VII. Entfernungsmaße (Annahme, dass □M. die geographische Quadratmeile bedeutet)"},
        {"from": "preußische Quadratmeile (zum Vergleich)", "to": "km²",
         "factor_or_formula": f"1 preuß. Meile = 1,0043 × 7500 m = {PR_MEILE_M:.1f} m; 1 □M. = {QM_PR_KM2:.2f} km²", "reference": "Brückner S. 832"},
    ],
    "datasets": [
        {"name": "totals", "title": T("Gesamtfläche nach Quelle", "Total area by source"),
         "columns": [
             {"name": "quelle", "label": T("Quelle", "Source"), "type": "string", "unit": None},
             {"name": "reihenfolge", "label": T("Reihenfolge", "Order"), "type": "integer", "unit": None, "derived": True, "note": "chronologisch/redaktionell"},
             {"name": "flaeche_qm", "label": T("Fläche", "Area"), "type": "number", "unit": "□M."},
             {"name": "flaeche_km2", "label": T("Fläche", "Area"), "type": "number", "unit": "km²", "derived": True},
         ],
         "rows": tot_rows, "source_refs": [{"page": "7", "block": "b7", "rows": "r1-r3"}, {"page": "8", "block": "b2", "rows": "r10"}]},
        {"name": "estimates", "title": T("Teilwerte der Flächenangaben (wie im Druck gruppiert)", "Partial values of the area figures (grouped as in the print)"),
         "columns": [
             {"name": "quelle", "label": T("Quelle", "Source"), "type": "string", "unit": None},
             {"name": "reihenfolge", "label": T("Reihenfolge", "Order"), "type": "integer", "unit": None, "derived": True},
             {"name": "gruppe", "label": T("Landestheil (Gruppe)", "Part (group)"), "type": "string", "unit": None},
             {"name": "flaeche_qm", "label": T("Fläche", "Area"), "type": "number", "unit": "□M."},
             {"name": "flaeche_km2", "label": T("Fläche", "Area"), "type": "number", "unit": "km²", "derived": True},
         ],
         "rows": est_rows, "source_refs": [{"page": "7", "block": "b7", "rows": "r1-r3"}, {"page": "8", "block": "b2", "rows": "r5-r9"}]},
        {"name": "landestheile", "title": T("Landesvermessung: Fläche nach Landestheilen", "Land survey: area by part"),
         "columns": [
             {"name": "landestheil", "label": T("Landestheil", "Part"), "type": "string", "unit": None},
             {"name": "morgen", "label": T("Fläche", "Area"), "type": "integer", "unit": "preuß. Morgen"},
             {"name": "ha", "label": T("Fläche", "Area"), "type": "number", "unit": "ha", "derived": True},
             {"name": "km2", "label": T("Fläche", "Area"), "type": "number", "unit": "km²", "derived": True},
             {"name": "anteil", "label": T("Anteil an der Gesamtfläche", "Share of total area"), "type": "number", "unit": "%", "derived": True},
         ],
         "rows": lt_rows, "source_refs": [{"page": "8", "block": "b2", "rows": "r5-r9"}]},
        {"name": "neighbours", "title": T("Größe im Vergleich mit Nachbarstaaten", "Size compared with neighbouring states"),
         "columns": [
             {"name": "staat", "label": T("Staat", "State"), "type": "string", "unit": None},
             {"name": "gruppe", "label": T("Gruppe", "Group"), "type": "string", "unit": None, "derived": True},
             {"name": "flaeche_qm", "label": T("Fläche", "Area"), "type": "number", "unit": "□M."},
             {"name": "aussage", "label": T("Brückners Vergleich (Reuß j. L. gegenüber dem Staat)", "Brückner's comparison (Reuss j. L. relative to the state)"), "type": "string", "unit": None},
             {"name": "faktor_aussage", "label": T("Faktor nach Brückners Bruch", "Factor from Brückner's fraction"), "type": "number", "unit": None, "derived": True},
             {"name": "faktor_rechnung", "label": T("Faktor nach den Zahlen (15,06 / Fläche)", "Factor from the figures (15.06 / area)"), "type": "number", "unit": None, "derived": True},
             {"name": "flaeche_km2", "label": T("Fläche", "Area"), "type": "number", "unit": "km²", "derived": True},
         ],
         "rows": nb_rows, "source_refs": [{"page": "8", "block": "b3"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "totals",
         "title": T("Wie groß ist das Land? Die Schätzungen im Vergleich", "How large is the country? The estimates compared"),
         "caption": T("Gesamtfläche in Quadratmeilen (□M.) nach vier Quellen: ältere Angabe von Hassel und Stein (bis 1840), preußische Berechnungen von Engelhardt (1853) und Nowack (neuere), Landesvermessung (ab 1840). Die Zahl sank um fast ein Drittel; Nowacks Zahl liegt zwischen den beiden anderen neueren Angaben.",
                      "Total area in square miles (□M.) according to four sources: the older figure by Hassel and Stein (until 1840), Prussian calculations by Engelhardt (1853) and Nowack (more recent), and the land survey (from 1840). The figure fell by almost a third; Nowack's figure lies between the other two recent values."),
         "vegalite": {
             "height": 260,
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "x": {"field": "quelle", "type": "nominal", "sort": {"field": "reihenfolge", "op": "min"}, "title": None, "axis": {"labelAngle": 0, "labelLimit": 200}},
                      "y": {"field": "flaeche_qm", "type": "quantitative", "title": "□ M.", "scale": {"domain": [0, 24]}},
                      "tooltip": [{"field": "quelle", "title": T("Quelle", "Source")},
                                  {"field": "flaeche_qm", "title": "□ M."},
                                  {"field": "flaeche_km2", "title": "km²"}]}},
                 {"mark": {"type": "text", "dy": -7},
                  "encoding": {
                      "x": {"field": "quelle", "type": "nominal", "sort": {"field": "reihenfolge", "op": "min"}},
                      "y": {"field": "flaeche_qm", "type": "quantitative"},
                      "text": {"field": "flaeche_qm", "type": "quantitative", "format": ".3~f"}}},
             ]}},
        {"id": "c2", "dataset": "landestheile",
         "title": T("Landesvermessung: Fläche der Landestheile", "Land survey: area of the parts"),
         "caption": T("Fläche in Quadratkilometern (aus preußischen Morgen, 1 Morgen = 0,255322 ha). Lobenstein-Ebersdorf, Gera und Schleiz umfassen zusammen rund 88 % des Landes.",
                      "Area in square kilometres (from Prussian Morgen, 1 Morgen = 0.255322 ha). Lobenstein-Ebersdorf, Gera and Schleiz together make up about 88 % of the country."),
         "vegalite": {
             "height": 220,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "landestheil", "type": "nominal", "sort": "-x", "title": None},
                 "x": {"field": "km2", "type": "quantitative", "title": "km²"},
                 "tooltip": [{"field": "landestheil", "title": T("Landestheil", "Part")},
                             {"field": "morgen", "title": T("preuß. Morgen", "Prussian Morgen"), "format": ","},
                             {"field": "ha", "title": "ha", "format": ","},
                             {"field": "km2", "title": "km²"},
                             {"field": "anteil", "title": T("Anteil (%)", "Share (%)")}]}}},
        {"id": "c3", "dataset": "neighbours",
         "title": T("Das Fürstentum und seine Nachbarn in Thüringen", "The principality and its Thuringian neighbours"),
         "caption": T("Fläche in Quadratmeilen (□M.) nach Brückner S. 8. Das Fürstentum (Reuß j. L.) liegt zwischen S.-Koburg und Schwarzburg-Sondershausen; Reuß ä. L. ist etwa ein Drittel so groß.",
                      "Area in square miles (□M.) after Brückner p. 8. The principality (Reuss j. L.) lies between Saxe-Coburg and Schwarzburg-Sondershausen; Reuss (elder line) is about a third of its size."),
         "vegalite": {
             "height": 260,
             "mark": "bar",
             "encoding": {
                 "y": {"field": "staat", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 280}},
                 "x": {"field": "flaeche_qm", "type": "quantitative", "title": "□ M."},
                 "color": {"field": "gruppe", "type": "nominal", "title": T("Staat", "State"), "scale": {"domain": ["Reuß j. L.", "Vergleichsstaat"]}},
                 "tooltip": [{"field": "staat", "title": T("Staat", "State")},
                             {"field": "flaeche_qm", "title": "□ M."},
                             {"field": "flaeche_km2", "title": "km²"},
                             {"field": "aussage", "title": T("Brückners Vergleich", "Brückner's comparison")},
                             {"field": "faktor_rechnung", "title": T("Faktor nach den Zahlen", "Factor from the figures")}]}}},
    ],
    "keywords": T(["Fläche", "Areal", "Quadratmeile", "Morgen", "Landesvermessung", "Größe", "Nachbarstaaten", "Reuß ältere Linie", "Thüringen", "Nowack", "Engelhardt", "Hassel"],
                  ["area", "square mile", "Morgen", "land survey", "size", "neighbouring states", "Reuss elder line", "Thuringia", "Nowack", "Engelhardt"]),
    "related": ["lage-vermessene-punkte-laenge-breite", "grenzen-umfang-nachbarlaender"],
    "generated_by": "Claude Sonnet 5.5 (subagent A01)",
    "date": "2026-10-01",
}
write_analysis(ana)
