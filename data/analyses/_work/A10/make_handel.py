"""A10: Handel und Transport 1864 nach Landesteilen, Staedten und Plattland (pp. 258-260)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from trade_data import *

D = load()
S = sum_rows()


def z(x):
    return x or 0


rows = []
for dn in DISTRICTS:
    for k, (tde, ten) in enumerate(TRADES):
        v, ref, raw = D[dn][k]
        for ai, area in enumerate(["Städte", "Plattland"]):
            s, g, d, f = v[4 * ai:4 * ai + 4]
            rows.append([tde, ten, dn, area, s, g, d, f, z(s) + z(g) + z(d) + z(f), z(s) + z(g), ref])
print(len(rows))


def agg(idx, **flt):
    return sum(r[idx] for r in rows if all(r[{"trade": 0, "district": 2, "area": 3}[k]] == v for k, v in flt.items()))


tot_s = agg(4 + 0) if False else sum(z(r[4]) for r in rows)
tot_p = sum(r[8] for r in rows)
dist_p = {dn: sum(r[8] for r in rows if r[2] == dn) for dn in DISTRICTS}
dist_s = {dn: sum(z(r[4]) for r in rows if r[2] == dn) for dn in DISTRICTS}
area_p = {a: sum(r[8] for r in rows if r[3] == a) for a in ["Städte", "Plattland"]}
trade_s = {r_[0]: sum(z(r[4]) for r in rows if r[0] == r_[0]) for r_ in TRADES for r_ in [r_]} if False else {t[0]: sum(z(r[4]) for r in rows if r[0] == t[0]) for t in TRADES}
trade_s_pl = {t[0]: sum(z(r[4]) for r in rows if r[0] == t[0] and r[3] == "Plattland") for t in TRADES}
trade_p = {t[0]: sum(r[8] for r in rows if r[0] == t[0]) for t in TRADES}
print(tot_s, tot_p, dist_p, dist_s, area_p)
rank_s = sorted(trade_s.items(), key=lambda kv: -kv[1])
rank_p = sorted(trade_p.items(), key=lambda kv: -kv[1])
print(rank_s[:6]); print(rank_p[:6])
gast = "Schenk- und Gastwirthe"
gast_pl_share = trade_s_pl[gast] / trade_s[gast] * 100
bank = "Banquiers"
bank_gera = sum(z(r[4]) for r in rows if r[0] == bank and r[2] == "Gera")
gera_p_share = dist_p["Gera"] / tot_p * 100
gera_s_share = dist_s["Gera"] / tot_s * 100
gera_colon = sum(z(r[4]) for r in rows if r[0] == "Colonial- und Materialhändler" and r[2] == "Gera") / trade_s["Colonial- und Materialhändler"] * 100
vieh_pl = trade_s_pl["Viehhändler"] / trade_s["Viehhändler"] * 100
holz_pl = trade_s_pl["Holzhändler"] / trade_s["Holzhändler"] * 100
town_p_share = area_p["Städte"] / tot_p * 100
def s_in(trade, dn=None):
    return sum(z(r[4]) for r in rows if r[0] == trade and (dn is None or r[2] == dn))
ag, grn = "Agenten, Spediteurs, Mäkler und Commissionäre", "Getreidehändler"
agents_gera, agents_tot, grain_gera, grain_tot = s_in(ag, "Gera"), s_in(ag), s_in(grn, "Gera"), s_in(grn)
print(agents_gera, agents_tot, grain_gera, grain_tot)
print(gast_pl_share, bank_gera, gera_p_share, gera_s_share, gera_colon, vieh_pl, holz_pl, town_p_share)
# mismatches (for caveats)
print("recomputed S per district", dist_s, "printed Summe row S", {dn: S[dn][8] for dn in DISTRICTS + ['Fürstenthum']})

AREA_LEGEND = {"de": "datum.label", "en": "{'Städte':'Towns','Plattland':'Countryside'}[datum.label]"}
AREA_CALC = {"de": "datum.area", "en": "{'Städte':'Towns','Plattland':'Countryside'}[datum.area]"}
ACOLOR = {"field": "area", "type": "nominal", "scale": {"domain": ["Städte", "Plattland"]}, "title": {"de": "Wohnort", "en": "Location"}, "legend": {"labelExpr": AREA_LEGEND}}
TRADE_LABEL = {"de": "datum.trade", "en": "datum.trade_en"}
DIST = {"de": "Landesteil", "en": "District"}

ana = {
    "id": "handel-gewerbe-nach-landesteilen-1864",
    "title": {"de": "Handel und Transport 1864: Gewerbe nach Landesteilen, Städten und Plattland", "en": "Trade and transport in 1864: trades by district, towns and countryside"},
    "category": "trade-transport",
    "section": "t1-3-7",
    "sources": [
        {"page": "258", "block": "b3"},
        {"page": "258", "block": "b4", "rows": "h1-t18"},
        {"page": "258", "block": "fn2"},
        {"page": "259", "block": "b1", "rows": "h1-t36"},
        {"page": "260", "block": "b1", "rows": "h1-t18"},
    ],
    "summary": {
        "de": f"Für das Jahr 1864 zählt Brückner die Handels- und Transportgewerbe in 15 Gruppen, getrennt nach Landesteilen, Städten und Plattland und jeweils nach Selbständigen, Gehilfen, Dienstboten und Familiengliedern. Insgesamt hängen {de(tot_p)} Personen an diesen Gewerben, davon {de(dist_p['Gera'] / tot_p * 100, 1)} % im Landesteil Gera. Die Auswertung zeigt die Rangfolge der Gewerbe, ihre Verteilung auf die Landesteile und den Gegensatz von Stadt und Land.",
        "en": f"For 1864 Brückner counts the trade and transport occupations in 15 groups, separated by district, towns and countryside and in each case by masters, assistants, servants and family members. In all, {en(tot_p)} persons depend on these trades, {en(dist_p['Gera'] / tot_p * 100, 1)} % of them in the district of Gera. The analysis shows the ranking of the trades, their distribution over the districts and the contrast between town and country.",
    },
    "method": {
        "de": "Die drei Landesteilstabellen (S. 258 b4, S. 259 b1) wurden für Städte und Plattland je Gewerbegruppe übernommen; ein Strich ist als leerer Wert kodiert, Verweiszeichen sind entfernt. Gewerbenamen sind ausgeschrieben (»Colon.- u. Materialhändl.« zu Colonial- und Materialhändler). Summen und Anteile wurden aus den Zahlen für Städte und Plattland neu berechnet; die gedruckten Summenspalten und die Tabelle des Fürstenthums (S. 260) dienten zur Kontrolle. Die Spalte persons ist S + G + D + F, sg = S + G.",
        "en": "The three district tables (p. 258 b4, p. 259 b1) were transferred for towns and countryside by group of trades; a dash is coded as an empty value, reference marks removed. Trade names are written out (“Colon.- u. Materialhändl.” to Colonial- und Materialhändler). Totals and shares were recomputed from the figures for towns and countryside; the printed total columns and the table for the principality (p. 260) served as a check. The column persons is S + G + D + F, sg = S + G.",
    },
    "findings": [
        {"de": f"Das zahlenmäßig größte Gewerbe sind die Schenk- und Gastwirte mit {de(trade_s[gast])} Selbständigen und {de(trade_p[gast])} Personen; von den Selbständigen sitzen {de(gast_pl_share, 1)} % auf dem Plattland. Es folgen Victualienhändler ({de(trade_s['Victualienhändler'])}), Sonstige Händler ({de(trade_s['Sonstige Händler'])}) und Colonial- und Materialhändler ({de(trade_s['Colonial- und Materialhändler'])} Selbständige).",
         "en": f"The largest trade by numbers is the innkeepers and publicans with {en(trade_s[gast])} masters and {en(trade_p[gast])} persons; {en(gast_pl_share, 1)} % of the masters live in the countryside. Next come provisions dealers ({en(trade_s['Victualienhändler'])}), other dealers ({en(trade_s['Sonstige Händler'])}) and colonial and general-goods dealers ({en(trade_s['Colonial- und Materialhändler'])} masters)."},
        {"de": f"Gera dominiert den Handel: {de(gera_s_share, 1)} % der Selbständigen und {de(gera_p_share, 1)} % aller Personen des Handels und Transports entfallen auf den Landesteil Gera (Schleiz {de(dist_p['Schleiz'] / tot_p * 100, 1)} %, Lobenstein-Ebersdorf {de(dist_p['Lobenstein-Ebersdorf'] / tot_p * 100, 1)} %), in Übereinstimmung mit Brückners Rangfolge Gera – Schleiz – Lobenstein-Ebersdorf. Alle {bank_gera} Bankiers des Landes sitzen in Gera.",
         "en": f"Gera dominates trade: {en(gera_s_share, 1)} % of the masters and {en(gera_p_share, 1)} % of all persons in trade and transport belong to the district of Gera (Schleiz {en(dist_p['Schleiz'] / tot_p * 100, 1)} %, Lobenstein-Ebersdorf {en(dist_p['Lobenstein-Ebersdorf'] / tot_p * 100, 1)} %), in agreement with Brückner's ranking Gera – Schleiz – Lobenstein-Ebersdorf. All {bank_gera} bankers of the principality are in Gera."},
        {"de": f"Auf dem Plattland dominieren Gewerbe der Landwirtschaft und des Gasthauswesens: {de(vieh_pl, 1)} % der Viehhändler, {de(holz_pl, 1)} % der Holzhändler und {de(gast_pl_share, 1)} % der Wirte sitzen dort, dagegen alle Bankiers, Agenten und Spediteure sowie die Buchhändler fast ausschließlich in den Städten. Insgesamt entfallen {de(town_p_share, 1)} % der Personen auf die Städte.",
         "en": f"In the countryside, trades tied to agriculture and the inn trade dominate: {en(vieh_pl, 1)} % of the cattle dealers, {en(holz_pl, 1)} % of the timber dealers and {en(gast_pl_share, 1)} % of the innkeepers are located there, whereas all bankers, agents and forwarders and almost all booksellers are in the towns. Overall {en(town_p_share, 1)} % of the persons belong to the towns."},
    ],
    "caveats": [
        {"de": "Im Druck stimmen einzelne Summen nicht (Faksimile S. 258–260 geprüft, die Transkription entspricht dem Druck): Colonial- und Materialhändler im Landesteil Gera, Dienstboten, Summe 74 statt 47 (Stadt 39 + Plattland 8); Viehhändler Gera, Familienglieder, Summe 16 statt 17; ferner kleine Abweichungen in den Summenzeilen. Die Auswertung rechnet deshalb aus den Zahlen für Städte und Plattland und weicht bei den Summen um bis zu 8 Personen von den gedruckten ab (z. B. Selbständige im Fürstenthum 957 statt gedruckt 951).",
         "en": "Some sums do not add up in the print (facsimile pp. 258–260 checked, the transcription corresponds to the print): colonial and general-goods dealers in the district of Gera, servants, total 74 instead of 47 (town 39 + countryside 8); cattle dealers Gera, family members, total 16 instead of 17; and small deviations in the total rows. The analysis therefore computes from the figures for towns and countryside and differs from the printed totals by up to 8 persons (e.g. masters in the principality 957 instead of the printed 951)."},
        {"de": "Brückner bemerkt selbst, dass die für Gera ermittelten Zahlen der Agenten, Spediteure usw. und der Wirte in der Stadt »offenbar zu niedrig« sind (S. 258, Fußnote **); die Gesamtgröße des Handels sei nicht ausreichend erhoben. Ein Vergleich mit der Gewerbetabelle S. 253 ist wegen unterschiedlicher Zeit und Zuordnung nur eingeschränkt möglich (S. 258, Fußnote *).",
         "en": "Brückner himself remarks that the figures found for Gera for agents, forwarders etc. and for innkeepers in the town are “evidently too low” (p. 258, footnote **); the overall size of trade has not been sufficiently surveyed. A comparison with the trades table on p. 253 is possible only to a limited extent because of differences in time and classification (p. 258, footnote *)."},
        {"de": "Die Zahlen sind Personen, nicht Betriebe oder Umsätze; Händler mit mehreren Geschäftszweigen können nur einer Gruppe angehören.",
         "en": "The figures are persons, not enterprises or turnover; dealers with several lines of business can belong to only one group."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "handel", "title": {"de": "Handel und Transport 1864 nach Gewerbe, Landesteil und Wohnort", "en": "Trade and transport 1864 by trade, district and location"},
         "columns": [
             {"name": "trade", "label": {"de": "Gewerbe", "en": "Trade"}, "type": "string", "unit": None},
             {"name": "trade_en", "label": {"de": "Gewerbe (englisch)", "en": "Trade (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "district", "label": DIST, "type": "string", "unit": None},
             {"name": "area", "label": {"de": "Wohnort", "en": "Location"}, "type": "string", "unit": None},
             {"name": "s", "label": {"de": "Selbständige", "en": "Masters"}, "type": "integer", "unit": "Personen"},
             {"name": "g", "label": {"de": "Gehilfen", "en": "Assistants"}, "type": "integer", "unit": "Personen"},
             {"name": "d", "label": {"de": "Dienstboten", "en": "Servants"}, "type": "integer", "unit": "Personen"},
             {"name": "f", "label": {"de": "Familienglieder", "en": "Family members"}, "type": "integer", "unit": "Personen"},
             {"name": "persons", "label": {"de": "Personen insgesamt", "en": "Persons in total"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "sg", "label": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": rows,
         "source_refs": [{"page": "258", "block": "b4", "rows": "r3-r17"}, {"page": "259", "block": "b1", "rows": "r4-r18"}, {"page": "259", "block": "b1", "rows": "r21-r35"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "handel",
         "title": {"de": "Selbständige im Handel und Transport nach Gewerbe", "en": "Masters in trade and transport by trade"},
         "caption": {"de": f"Fürstenthum 1864, nach Städten und Plattland. Die Wirte sind die größte Gruppe und überwiegend auf dem Land ansässig.",
                     "en": "Principality 1864, by towns and countryside. Innkeepers are the largest group and mostly live in the countryside."},
         "vegalite": {
             "height": 440,
             "transform": [{"aggregate": [{"op": "sum", "field": "s", "as": "s_sum"}], "groupby": ["trade", "trade_en", "area"]},
                           {"calculate": TRADE_LABEL, "as": "trade_label"}, {"calculate": AREA_CALC, "as": "area_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "s_sum", "op": "sum", "order": "descending"}, "title": None, "axis": {"labelLimit": 320}},
                 "x": {"field": "s_sum", "type": "quantitative", "title": {"de": "Selbständige", "en": "Masters"}},
                 "color": ACOLOR,
                 "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "area_label", "title": {"de": "Wohnort", "en": "Location"}},
                             {"field": "s_sum", "title": {"de": "Selbständige", "en": "Masters"}}]}}},
        {"id": "c2", "dataset": "handel",
         "title": {"de": "Selbständige nach Gewerbe und Landesteil", "en": "Masters by trade and district"},
         "caption": {"de": f"Anzahl der Selbständigen je Gewerbe in den drei Landesteilen. Bankiers (alle in Gera), Agenten und Spediteure ({agents_gera} von {agents_tot}) und Getreidehändler ({grain_gera} von {grain_tot}) konzentrieren sich im Landesteil Gera; die Wirte sind überall zahlreich.",
                     "en": f"Number of masters per trade in the three districts. Bankers (all in Gera), agents and forwarders ({agents_gera} of {agents_tot}) and grain dealers ({grain_gera} of {grain_tot}) are concentrated in the district of Gera; innkeepers are numerous everywhere."},
         "vegalite": {
             "height": 440,
             "transform": [{"aggregate": [{"op": "sum", "field": "s", "as": "s_sum"}], "groupby": ["trade", "trade_en", "district"]}, {"calculate": TRADE_LABEL, "as": "trade_label"}],
             "mark": "rect",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "s_sum", "op": "sum", "order": "descending"}, "title": None, "axis": {"labelLimit": 320}},
                 "color": {"field": "s_sum", "type": "quantitative", "title": {"de": "Selbständige", "en": "Masters"}},
                 "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "district", "title": DIST}, {"field": "s_sum", "title": {"de": "Selbständige", "en": "Masters"}}]}}},
        {"id": "c3", "dataset": "handel",
         "title": {"de": "Personen im Handel und Transport nach Landesteil", "en": "Persons in trade and transport by district"},
         "caption": {"de": "Selbständige, Gehilfen, Dienstboten und Familienglieder zusammen, nach Städten und Plattland. Gera steht an erster, Schleiz an zweiter, Lobenstein-Ebersdorf an dritter Stelle, wie Brückner schreibt.",
                     "en": "Masters, assistants, servants and family members together, by towns and countryside. Gera ranks first, Schleiz second, Lobenstein-Ebersdorf third, as Brückner writes."},
         "vegalite": {
             "height": 260,
             "transform": [{"aggregate": [{"op": "sum", "field": "persons", "as": "p_sum"}], "groupby": ["district", "area"]}, {"calculate": AREA_CALC, "as": "area_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "p_sum", "type": "quantitative", "title": {"de": "Personen", "en": "Persons"}},
                 "color": ACOLOR,
                 "tooltip": [{"field": "district", "title": DIST}, {"field": "area_label", "title": {"de": "Wohnort", "en": "Location"}}, {"field": "p_sum", "title": {"de": "Personen", "en": "Persons"}}]}}},
    ],
    "keywords": {"de": ["Handel", "Transport", "Gastwirte", "Kaufleute", "Banquiers", "Bankiers", "Gera", "Schleiz", "Lobenstein", "Städte", "Plattland", "1864"],
                 "en": ["trade", "transport", "innkeepers", "merchants", "bankers", "Gera", "Schleiz", "Lobenstein", "towns", "countryside", "1864"]},
    "related": ["handel-verkehr-begleitscheine-1858-1867", "verkehr-eisenbahn-geldinstitute-zeitleiste"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
