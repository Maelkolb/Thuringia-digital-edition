"""A10: Gewerbe 1864 - die einzelnen Gewerbe nach Landesteilen (pp. 252-254, with pp. 255-256)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from industry_data import *

T = [t for t in parse_trades() if not all(v is None for v in t["vals"])]
dash_rows = [t["key"] for t in parse_trades() if all(v is None for v in t["vals"])]


def z(x):
    return x or 0


gew_rows, fst_rows = [], []
mismatch = []
for t in T:
    de_name, en_name = TR[t["key"]]
    v = t["vals"]
    for di, dn in enumerate(DISTRICTS):
        s, g, d, f = v[4 * di:4 * di + 4]
        gew_rows.append([t["branch"], de_name, en_name, dn, s, g, d, f, z(s) + z(g) + z(d) + z(f), t["ref"]])
    s, g, d, f = v[12:16]
    diffs = []
    for ci, cn in enumerate("SGDF"):
        comp = sum(z(v[4 * k + ci]) for k in range(3))
        if comp != z(v[12 + ci]):
            diffs.append(f"{cn}: Landesteile {comp}, gedruckt {z(v[12 + ci])}")
    sz, gz = z(s), z(g)
    ratio = round(gz / sz, 2) if sz else None
    fst_rows.append([t["branch"], de_name, en_name, s, g, d, f, sz + gz + z(d) + z(f), sz + gz, ratio, "; ".join(diffs) if diffs else None, t["ref"]])
    if diffs:
        mismatch.append((de_name, diffs, t["ref"]))
print("mismatches", len(mismatch))
for m in mismatch:
    print(m)

# ---- numbers for findings -----------------------------------------------------------
tot_persons = sum(r[7] for r in fst_rows)
by_branch = {}
for r in fst_rows:
    by_branch[r[0]] = by_branch.get(r[0], 0) + r[7]
weber = [r for r in fst_rows if r[1] == "Weber"][0]
weber_district = {}
for r in gew_rows:
    if r[1] == "Weber":
        weber_district[r[3]] = r[8]
dist_sg = {dn: sum(z(r[4]) + z(r[5]) for r in gew_rows if r[3] == dn) for dn in DISTRICTS}
weber_sg = {dn: sum(z(r[4]) + z(r[5]) for r in gew_rows if r[3] == dn and r[1] == "Weber") for dn in DISTRICTS}
weber_share = {dn: weber_sg[dn] / dist_sg[dn] * 100 for dn in DISTRICTS}
dach = {dn: sum(z(r[4]) + z(r[5]) for r in gew_rows if r[3] == dn and r[1] == "Dachdecker") for dn in DISTRICTS}
dach_share = {dn: dach[dn] / dist_sg[dn] * 100 for dn in DISTRICTS}
masch = {dn: sum(z(r[4]) + z(r[5]) for r in gew_rows if r[3] == dn and r[1] == "Maschinenbauer") for dn in DISTRICTS}
ratio_rows = sorted([r for r in fst_rows if z(r[3]) >= 40 and r[9] is not None and r[0] != "Sonstige"], key=lambda r: -r[9])
n_ratio = len(ratio_rows)
maurer = [r for r in fst_rows if r[1] == "Maurer, Steinhauer"][0]
zimmer = [r for r in fst_rows if r[1] == "Zimmerleute"][0]
n_over1 = sum(1 for r in ratio_rows if r[9] > 1)
over3 = [(r[1], r[9]) for r in ratio_rows if r[9] > 3]
print("ratio rows", n_ratio, "over1", n_over1, "over3", over3)
print("branch", by_branch, tot_persons)
print("weber", weber, weber_district, weber_share, dach_share, masch, dist_sg)
top15 = sorted([r for r in fst_rows if r[0] != "Sonstige"], key=lambda r: -r[7])[:15]
print([(r[1], r[7]) for r in top15])
top5_share = sum(r[7] for r in top15[:5]) / tot_persons * 100
kl_share = by_branch["Kleidung"] / tot_persons * 100
bau_share = by_branch["Bauhandwerker"] / tot_persons * 100

# ---- share dataset (heatmap): top 12 trades by S+G, share of district S+G -------------
sg_rank = sorted([r for r in fst_rows if r[0] != "Sonstige"], key=lambda r: -r[8])[:12]
anteil_rows = []
for r in sg_rank:
    for dn in DISTRICTS:
        sg = sum(z(x[4]) + z(x[5]) for x in gew_rows if x[3] == dn and x[1] == r[1])
        anteil_rows.append([r[1], r[2], dn, sg, dist_sg[dn], round(sg / dist_sg[dn] * 100, 1)])
print([(r[1], r[8]) for r in sg_rank])

TRADE_LABEL = {"de": "datum.trade", "en": "datum.trade_en"}
BRANCH_SHORT_EN = {"Nahrung": "Food", "Kleidung": "Clothing", "Bauhandwerker": "Building", "Hausausstattung": "House and farm", "Sonstige": "Other"}
BRANCH_LEGEND = {"de": "datum.label",
                 "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in BRANCH_SHORT_EN.items()) + "}[datum.label]"}
BRANCH_CALC = {"de": "datum.branch", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in BRANCH_EN.items()) + "}[datum.branch]"}
BCOLOR = {"field": "branch", "type": "nominal", "scale": {"domain": BRANCHES}, "title": {"de": "Gewerbegruppe", "en": "Group of trades"},
          "legend": {"labelExpr": BRANCH_LEGEND, "columns": 3}}
DIST = {"de": "Landesteil", "en": "District"}
PERS = {"de": "Personen (Selbständige, Gehilfen, Dienstboten, Familienglieder)", "en": "Persons (masters, assistants, servants, family members)"}

ana = {
    "id": "industrie-gewerbe-1864-einzelne-gewerbe",
    "title": {"de": "Gewerbe und Industrie 1864: die einzelnen Gewerbe nach Landesteilen", "en": "Trades and industry in 1864: individual trades by district"},
    "category": "industry",
    "section": "t1-3-6",
    "sources": [
        {"page": "252", "block": "b3"},
        {"page": "252", "block": "b4", "rows": "h1-t27"},
        {"page": "252", "block": "fn1"},
        {"page": "253", "block": "b1", "rows": "h1-r43"},
        {"page": "254", "block": "b1", "rows": "h1-t21"},
        {"page": "256", "block": "b1"},
    ],
    "summary": {
        "de": f"Nach den Recherchen von 1864 zählt Brückner für die drei Landesteile {len(T)} Gewerbe und Industriezweige, jeweils mit Selbständigen, Gehilfen, Dienstboten und Familiengliedern. Die Auswertung rangiert die Gewerbe nach den von ihnen ernährten Personen, stellt die Gewerbestruktur der Landesteile gegenüber und berechnet die Zahl der Gehilfen je Selbständigem. Die Weberei überragt alles: sie ernährt {de(weber[7])} Personen, das sind {de(weber[7] / tot_persons * 100, 1)} % aller in der Tabelle erfassten.",
        "en": f"Based on the 1864 inquiries Brückner counts {len(T)} trades and branches of industry for the three districts, each with masters, assistants, servants and family members. The analysis ranks the trades by the persons they support, compares the trade structure of the districts and computes the number of assistants per master. Weaving towers above everything: it supports {en(weber[7])} persons, {en(weber[7] / tot_persons * 100, 1)} % of all persons recorded in the table.",
    },
    "method": {
        "de": f"Die Tabellen S. 252–254 wurden Zeile für Zeile übernommen (S. = Selbständige, G. = Gehilfen, D. = Dienstboten, F. = Familienglieder, nach der Fußnote auf S. 252). Abkürzungen der Gewerbenamen sind aufgelöst, Verweisziffern und Punktlinien entfernt; ein Strich im Druck ist als leerer Wert kodiert. Fünf Zeilen ohne jeden Eintrag ({', '.join(dash_rows)}) sind weggelassen; die Arbeiter von Saline und chemischer Fabrik stehen nach der Fußnote unter 5). Die Spalte persons ist die Summe von S, G, D und F; sg = S + G; g_per_s = G / S. Die Anteile in der Heatmap sind der Anteil eines Gewerbes an allen Selbständigen und Gehilfen des Landesteils, berechnet aus den Zeilen der {len(T)} Gewerbe. Für die Rangfolge und die Quoten werden die gedruckten Spalten »Fürstenthum« verwendet; wo sie von der Summe der Landesteile abweichen, steht der Befund in der Spalte print_diff.",
        "en": f"The tables on pp. 252–254 were transferred row by row (S. = masters, G. = assistants, D. = servants, F. = family members, according to the footnote on p. 252). Abbreviated trade names are expanded, reference marks and dot leaders removed; a dash in the print is coded as an empty value. Five rows without any entry ({', '.join(dash_rows)}) are omitted; according to the footnote the workers of the saltworks and the chemical factory are listed under 5). The column persons is the sum of S, G, D and F; sg = S + G; g_per_s = G / S. The shares in the heatmap are the share of a trade in all masters and assistants of the district, computed from the rows of the {len(T)} trades. The ranking and the ratios use the printed “Fürstenthum” columns; where they differ from the sum of the districts, the finding is recorded in the column print_diff.",
    },
    "findings": [
        {"de": f"Das Bekleidungsgewerbe stellt {de(by_branch['Kleidung'])} der {de(tot_persons)} erfassten Personen ({de(kl_share, 1)} %), die Bauhandwerker {de(by_branch['Bauhandwerker'])} ({de(bau_share, 1)} %). Allein die fünf größten Gewerbe (Weber, Maurer und Steinhauer, Schuhmacher, Zimmerleute, Schneider) vereinen {de(top5_share, 1)} % aller Personen.",
         "en": f"The clothing trades account for {en(by_branch['Kleidung'])} of the {en(tot_persons)} persons recorded ({en(kl_share, 1)} %), the building trades for {en(by_branch['Bauhandwerker'])} ({en(bau_share, 1)} %). The five largest trades alone (weavers, masons and stonecutters, shoemakers, carpenters, tailors) account for {en(top5_share, 1)} % of all persons."},
        {"de": f"Die Weberei ernährt im Landesteil Schleiz {de(weber_district['Schleiz'])}, in Gera {de(weber_district['Gera'])} und in Lobenstein-Ebersdorf {de(weber_district['Lobenstein-Ebersdorf'])} Personen (zusammen {de(weber[7])}, wie Brückner S. 256 angibt). Im Landesteil Schleiz gehören {de(weber_share['Schleiz'], 1)} % aller Selbständigen und Gehilfen zur Weberei, in Gera {de(weber_share['Gera'], 1)} %, in Lobenstein-Ebersdorf {de(weber_share['Lobenstein-Ebersdorf'], 1)} %.",
         "en": f"Weaving supports {en(weber_district['Schleiz'])} persons in the district of Schleiz, {en(weber_district['Gera'])} in Gera and {en(weber_district['Lobenstein-Ebersdorf'])} in Lobenstein-Ebersdorf ({en(weber[7])} in all, as Brückner states on p. 256). In the district of Schleiz {en(weber_share['Schleiz'], 1)} % of all masters and assistants belong to weaving, in Gera {en(weber_share['Gera'], 1)} %, in Lobenstein-Ebersdorf {en(weber_share['Lobenstein-Ebersdorf'], 1)} %."},
        {"de": f"Auf einen selbständigen Maurer oder Steinhauer kommen {de(maurer[9], 1)} Gehilfen, auf einen Zimmermann {de(zimmer[9], 1)}; unter den {n_ratio} Gewerben mit mindestens 40 Selbständigen haben nur {n_over1} mehr Gehilfen als Meister. Das passt zu Brückners Hinweis, dass die oberländischen Maurer- und Zimmergesellen im Sommer auswärts arbeiten (S. 256).",
         "en": f"For every independent mason or stonecutter there are {en(maurer[9], 1)} assistants, for every carpenter {en(zimmer[9], 1)}; of the {n_ratio} trades with at least 40 masters only {n_over1} have more assistants than masters. This fits Brückner's remark that Oberland mason and carpenter journeymen work away from home in summer (p. 256)."},
        {"de": f"Im Landesteil Lobenstein-Ebersdorf entfallen {de(dach_share['Lobenstein-Ebersdorf'], 1)} % der Selbständigen und Gehilfen auf die Dachdecker (Schieferdecker), in Gera nur {de(dach_share['Gera'], 1)} %; die Maschinenbauer sitzen vor allem in Gera ({masch['Gera']} Selbständige und Gehilfen gegenüber {masch['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf und keinem in Schleiz).",
         "en": f"In the district of Lobenstein-Ebersdorf {en(dach_share['Lobenstein-Ebersdorf'], 1)} % of the masters and assistants are roofers (slate roofers), in Gera only {en(dach_share['Gera'], 1)} %; machine builders are concentrated in Gera ({masch['Gera']} masters and assistants against {masch['Lobenstein-Ebersdorf']} in Lobenstein-Ebersdorf and none in Schleiz)."},
    ],
    "caveats": [
        {"de": f"Im Druck stimmen einzelne Summen nicht: {len(mismatch)} der {len(T)} Gewerbezeilen weichen in der Spalte »Fürstenthum« von der Summe der drei Landesteile ab, meist um 1–2 Personen; größere Abweichungen: Fleischer F. (Lobenstein-Ebersdorf gedruckt 26, Summe der Fürstenthum-Spalte verlangt 206), Böttcher und Bürstenmacher F. (die Zahl 100 steht beim Landesteil Schleiz in der Zeile Bürstenmacher, passt aber zur Böttcher-Summe 321), Latus D. (68 gedruckt, Summe 168). Die Transkription stimmt in allen geprüften Fällen mit dem Druck überein (Faksimile S. 252, 253, 255).",
         "en": f"Some sums do not add up in the print: {len(mismatch)} of the {len(T)} trade rows differ in the “Fürstenthum” column from the sum of the three districts, mostly by 1–2 persons; larger deviations: butchers F. (Lobenstein-Ebersdorf printed 26, the Fürstenthum column implies 206), coopers and brush makers F. (the figure 100 stands under the district of Schleiz in the brush-maker row but fits the cooper total 321), Latus D. (68 printed, sum 168). The transcription agrees with the print in all cases checked (facsimile pp. 252, 253, 255)."},
        {"de": "Die Tabelle erfasst Selbständige, Gehilfen, Dienstboten und Familienglieder; die Personenzahl eines Gewerbes ist daher nicht die Zahl der Erwerbstätigen, sondern der von ihm ernährten Personen. Dienstboten und Familienglieder lassen sich nicht auf Gewerbe und Landwirtschaft aufteilen, wo ein Betrieb beides vereint.",
         "en": "The table counts masters, assistants, servants and family members; the number of persons of a trade is therefore not the number of gainfully employed but of persons supported by it. Servants and family members cannot be split between trade and agriculture where one household combines both."},
        {"de": "Die Quote Gehilfen je Selbständigem ist ein grobes Maß: sie sagt nichts über die Betriebsgröße im einzelnen, und die Gehilfen von Wandergewerben (Maurer, Zimmerleute) arbeiten teilweise außerhalb des Landes.",
         "en": "The ratio of assistants to masters is a rough measure: it says nothing about the size of individual enterprises, and the assistants of itinerant trades (masons, carpenters) partly work outside the principality."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "fuerstenthum", "title": {"de": "Gewerbe im Fürstenthum 1864 (gedruckte Gesamtzahlen)", "en": "Trades in the principality, 1864 (printed totals)"},
         "columns": [
             {"name": "branch", "label": {"de": "Gewerbegruppe", "en": "Group of trades"}, "type": "string", "unit": None},
             {"name": "trade", "label": {"de": "Gewerbe", "en": "Trade"}, "type": "string", "unit": None},
             {"name": "trade_en", "label": {"de": "Gewerbe (englisch)", "en": "Trade (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "s", "label": {"de": "Selbständige", "en": "Masters"}, "type": "integer", "unit": "Personen"},
             {"name": "g", "label": {"de": "Gehilfen", "en": "Assistants"}, "type": "integer", "unit": "Personen"},
             {"name": "d", "label": {"de": "Dienstboten", "en": "Servants"}, "type": "integer", "unit": "Personen"},
             {"name": "f", "label": {"de": "Familienglieder", "en": "Family members"}, "type": "integer", "unit": "Personen"},
             {"name": "persons", "label": {"de": "Personen insgesamt", "en": "Persons in total"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "sg", "label": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "g_per_s", "label": {"de": "Gehilfen je Selbständigem", "en": "Assistants per master"}, "type": "number", "unit": None, "derived": True},
             {"name": "print_diff", "label": {"de": "Abweichung im Druck", "en": "Deviation in the print"}, "type": "string", "unit": None, "derived": True},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": fst_rows,
         "source_refs": [{"page": "252", "block": "b4", "rows": "r4-r26"}, {"page": "253", "block": "b1", "rows": "r4-r42"}, {"page": "254", "block": "b1", "rows": "r4-r20"}]},
        {"name": "gewerbe", "title": {"de": "Gewerbe nach Landesteilen 1864", "en": "Trades by district, 1864"},
         "columns": [
             {"name": "branch", "label": {"de": "Gewerbegruppe", "en": "Group of trades"}, "type": "string", "unit": None},
             {"name": "trade", "label": {"de": "Gewerbe", "en": "Trade"}, "type": "string", "unit": None},
             {"name": "trade_en", "label": {"de": "Gewerbe (englisch)", "en": "Trade (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "district", "label": DIST, "type": "string", "unit": None},
             {"name": "s", "label": {"de": "Selbständige", "en": "Masters"}, "type": "integer", "unit": "Personen"},
             {"name": "g", "label": {"de": "Gehilfen", "en": "Assistants"}, "type": "integer", "unit": "Personen"},
             {"name": "d", "label": {"de": "Dienstboten", "en": "Servants"}, "type": "integer", "unit": "Personen"},
             {"name": "f", "label": {"de": "Familienglieder", "en": "Family members"}, "type": "integer", "unit": "Personen"},
             {"name": "persons", "label": {"de": "Personen insgesamt", "en": "Persons in total"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": gew_rows,
         "source_refs": [{"page": "252", "block": "b4", "rows": "r4-r26"}, {"page": "253", "block": "b1", "rows": "r4-r42"}, {"page": "254", "block": "b1", "rows": "r4-r20"}]},
        {"name": "anteile", "title": {"de": "Anteil der größten Gewerbe an Selbständigen und Gehilfen je Landesteil", "en": "Share of the largest trades in masters and assistants by district"},
         "columns": [
             {"name": "trade", "label": {"de": "Gewerbe", "en": "Trade"}, "type": "string", "unit": None},
             {"name": "trade_en", "label": {"de": "Gewerbe (englisch)", "en": "Trade (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "district", "label": DIST, "type": "string", "unit": None},
             {"name": "sg", "label": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "district_sg", "label": {"de": "Selbständige und Gehilfen im Landesteil insgesamt", "en": "Masters and assistants in the district in total"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "share_pct", "label": {"de": "Anteil", "en": "Share"}, "type": "number", "unit": "%", "derived": True},
         ],
         "rows": anteil_rows,
         "source_refs": [{"page": "252", "block": "b4", "rows": "r4-r26"}, {"page": "253", "block": "b1", "rows": "r4-r42"}, {"page": "254", "block": "b1", "rows": "r4-r20"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "fuerstenthum",
         "title": {"de": "Die 15 größten Gewerbe nach ernährten Personen", "en": "The 15 largest trades by persons supported"},
         "caption": {"de": "Selbständige, Gehilfen, Dienstboten und Familienglieder zusammen, Fürstenthum 1864 (gedruckte Gesamtzahlen). Ohne die Sammelposten »Fabrikarbeiter« und »Nichtbenannte Nahrungszweige«.",
                     "en": "Masters, assistants, servants and family members together, principality 1864 (printed totals). Without the catch-all items “factory workers” and “unnamed food trades”."},
         "vegalite": {
             "height": 420,
             "transform": [{"filter": "datum.branch != 'Sonstige'"},
                           {"window": [{"op": "rank", "as": "rk"}], "sort": [{"field": "persons", "order": "descending"}]},
                           {"filter": "datum.rk <= 15"},
                           {"calculate": TRADE_LABEL, "as": "trade_label"}, {"calculate": BRANCH_CALC, "as": "branch_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "persons", "order": "descending"}, "title": None, "axis": {"labelLimit": 320}},
                 "x": {"field": "persons", "type": "quantitative", "title": PERS},
                 "color": BCOLOR,
                 "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "branch_label", "title": {"de": "Gruppe", "en": "Group"}},
                             {"field": "s", "title": {"de": "Selbständige", "en": "Masters"}}, {"field": "g", "title": {"de": "Gehilfen", "en": "Assistants"}},
                             {"field": "d", "title": {"de": "Dienstboten", "en": "Servants"}}, {"field": "f", "title": {"de": "Familienglieder", "en": "Family members"}},
                             {"field": "persons", "title": {"de": "Personen", "en": "Persons"}}]}}},
        {"id": "c2", "dataset": "anteile",
         "title": {"de": "Gewerbestruktur der Landesteile", "en": "Trade structure of the districts"},
         "caption": {"de": "Anteil der zwölf größten Gewerbe (nach Selbständigen und Gehilfen) an allen Selbständigen und Gehilfen des Landesteils, in Prozent. Im Landesteil Schleiz stellt die Weberei über ein Drittel.",
                     "en": "Share of the twelve largest trades (by masters and assistants) in all masters and assistants of the district, in percent. In the district of Schleiz weaving accounts for over a third."},
         "vegalite": {
             "height": 380,
             "transform": [{"calculate": TRADE_LABEL, "as": "trade_label"}],
             "mark": "rect",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "sg", "op": "sum", "order": "descending"}, "title": None, "axis": {"labelLimit": 320}},
                 "color": {"field": "share_pct", "type": "quantitative", "title": {"de": "Anteil (%)", "en": "Share (%)"}},
                 "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "district", "title": DIST},
                             {"field": "sg", "title": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}}, {"field": "share_pct", "title": {"de": "Anteil (%)", "en": "Share (%)"}}]}}},
        {"id": "c3", "dataset": "fuerstenthum",
         "title": {"de": "Gehilfen je Selbständigem", "en": "Assistants per master"},
         "caption": {"de": "Gewerbe mit mindestens 40 Selbständigen im Fürstenthum. Die gestrichelte Linie markiert einen Gehilfen je Meister; die Bauhandwerker liegen weit darüber.",
                     "en": "Trades with at least 40 masters in the principality. The dashed line marks one assistant per master; the building trades lie far above it."},
         "vegalite": {
             "height": 560,
             "transform": [{"filter": "datum.s >= 40 && datum.g_per_s != null && datum.branch != 'Sonstige'"}, {"calculate": TRADE_LABEL, "as": "trade_label"}, {"calculate": BRANCH_CALC, "as": "branch_label"}],
             "layer": [
                 {"mark": "bar",
                  "encoding": {
                      "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "g_per_s", "order": "descending"}, "title": None, "axis": {"labelLimit": 320}},
                      "x": {"field": "g_per_s", "type": "quantitative", "title": {"de": "Gehilfen je Selbständigem", "en": "Assistants per master"}},
                      "color": BCOLOR,
                      "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "branch_label", "title": {"de": "Gruppe", "en": "Group"}},
                                  {"field": "s", "title": {"de": "Selbständige", "en": "Masters"}}, {"field": "g", "title": {"de": "Gehilfen", "en": "Assistants"}},
                                  {"field": "g_per_s", "title": {"de": "Gehilfen je Selbständigem", "en": "Assistants per master"}}]}},
                 {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"x": {"datum": 1}}},
             ]}},
    ],
    "keywords": {"de": ["Gewerbe", "Industrie", "Handwerk", "Weber", "Weberei", "Maurer", "Zimmerleute", "Schuhmacher", "Gehilfen", "Berufe", "Gera", "Schleiz", "Lobenstein", "1864"],
                 "en": ["trades", "industry", "crafts", "weavers", "weaving", "masons", "carpenters", "shoemakers", "assistants", "occupations", "Gera", "Schleiz", "Lobenstein", "1864"]},
    "related": ["industrie-hauptzweige-staedte-plattland-1864"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
