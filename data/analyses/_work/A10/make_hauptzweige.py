"""A10: Industriezweige 1864 - Staedte und Plattland (pp. 255-257)."""
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from industry_data import *

g = grid("255", "b1")
BR_ROWS = {"Nahrung": 0, "Kleidung": 1, "Bauhandwerker": 2, "Hausausstattung": 3, "Sonstige": 4}
START = {"Gera": 3, "Schleiz": 10, "Lobenstein-Ebersdorf": 17}
AREA = {"Städte": 0, "Plattland": 4}


def z(x):
    return x or 0


rows = []
for dn, r0 in START.items():
    for br, off in BR_ROWS.items():
        r = g[r0 - 1 + off]
        for area, c0 in AREA.items():
            s, gg, d, f = [num(x) for x in r[1 + c0:5 + c0]]
            rows.append([dn, br, area, s, gg, d, f, z(s) + z(gg) + z(d) + z(f), z(s) + z(gg), f"r{r0 + off}"])
print(len(rows))

# totals
def tot(area=None, branch=None, district=None, idx=8):
    return sum(r[idx] for r in rows if (area is None or r[2] == area) and (branch is None or r[1] == branch) and (district is None or r[0] == district))

sg_all, p_all = tot(), tot(idx=7)
sg_st, p_st = tot("Städte"), tot("Städte", idx=7)
sg_share_st = sg_st / sg_all * 100
p_share_st = p_st / p_all * 100
print("S+G", sg_all, sg_st, sg_share_st, "persons", p_all, p_st, p_share_st, 100 - p_share_st)
share_branch = {b: tot("Städte", b) / tot(None, b) * 100 for b in BRANCHES}
print(share_branch)
pers_branch = {b: tot(None, b, None, 7) for b in BRANCHES}
pers_dist = {d: tot(None, None, d, 7) for d in DISTRICTS}
print(pers_branch, pers_dist)
kl = {d: tot(None, "Kleidung", d, 7) / tot(None, None, d, 7) * 100 for d in DISTRICTS}
bau = {d: tot(None, "Bauhandwerker", d, 7) / tot(None, None, d, 7) * 100 for d in DISTRICTS}
print(kl, bau)
bau_pl = tot("Plattland", "Bauhandwerker") / tot(None, "Bauhandwerker") * 100

# towns (pp. 256-257) ----------------------------------------------------------------
TOWNS = [("Gera", 2016, "256 b2"), ("Schleiz", 674, "256 b2"), ("Tanna", 329, "256 b2"), ("Lobenstein", 305, "257 b1"), ("Hirschberg", 285, "257 b1"), ("Saalburg", 185, "257 b1")]
town_rows = [[t, s, 2168 if t == "Gera" else None, "S. " + src] for t, s, src in TOWNS]
five = sum(s for t, s, _ in TOWNS if t != "Gera")
gera_share = 2016 / sum(s for _, s, _ in TOWNS) * 100
print("five", five, "gera share", gera_share, "gera g share of towns", 2168 / (2168 + 1136) * 100)
assert five == 1778

# food trades: totals vs. towns (p. 257 b2) -----------------------------------------------
FOOD = [("Getreidemühlen", "Grain mills", 164, 20), ("Bäcker und Conditoren", "Bakers and confectioners", 166, 102), ("Fleischer", "Butchers", 208, 110),
        ("Brauereien", "Breweries", 41, 27), ("Branntweinbrennereien", "Distilleries", 37, 5), ("Materialwarenhändler", "Grocers (Materialwarenhändler)", 117, 76)]
food_rows = [[de_, en_, tot_, st, tot_ - st, round(st / tot_ * 100, 1)] for de_, en_, tot_, st in FOOD]
print(food_rows)

AREA_EN = {"Städte": "Towns", "Plattland": "Countryside"}
AREA_LEGEND = {"de": "datum.label", "en": "{'Städte':'Towns','Plattland':'Countryside'}[datum.label]"}
AREA_CALC = {"de": "datum.area", "en": "{'Städte':'Towns','Plattland':'Countryside'}[datum.area]"}
BRANCH_SHORT_EN = {"Nahrung": "Food", "Kleidung": "Clothing", "Bauhandwerker": "Building", "Hausausstattung": "House and farm", "Sonstige": "Other"}
BRANCH_LEGEND = {"de": "datum.label", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in BRANCH_SHORT_EN.items()) + "}[datum.label]"}
BRANCH_AXIS = BRANCH_LEGEND
BRANCH_CALC = {"de": "datum.branch", "en": "{" + ",".join(f"'{k}':'{v}'" for k, v in BRANCH_SHORT_EN.items()) + "}[datum.branch]"}
ACOLOR = {"field": "area", "type": "nominal", "scale": {"domain": ["Städte", "Plattland"]}, "title": {"de": "Wohnort", "en": "Location"}, "legend": {"labelExpr": AREA_LEGEND}}
BCOLOR = {"field": "branch", "type": "nominal", "scale": {"domain": BRANCHES}, "title": {"de": "Gewerbegruppe", "en": "Group of trades"}, "legend": {"labelExpr": BRANCH_LEGEND, "columns": 3}}

ana = {
    "id": "industrie-hauptzweige-staedte-plattland-1864",
    "title": {"de": "Industriezweige 1864: Städte und Plattland, Landesteile", "en": "Branches of industry in 1864: towns and countryside, districts"},
    "category": "industry",
    "section": "t1-3-6",
    "sources": [
        {"page": "255", "block": "b1", "rows": "h1-r29"},
        {"page": "255", "block": "b2"},
        {"page": "255", "block": "b3"},
        {"page": "256", "block": "b2"},
        {"page": "257", "block": "b1"},
        {"page": "257", "block": "b2"},
    ],
    "summary": {
        "de": f"Brückners »Zusammenstellung der Hauptindustriezweige« (S. 255) verteilt die {de(p_all)} Personen der Industrie des Jahres 1864 auf fünf Gewerbegruppen, drei Landesteile sowie Städte und Plattland. Entgegen dem Mittelalter, so Brückner, lebt die Mehrheit der Industriellen auf dem Land: {de(100 - sg_share_st, 1)} % der Selbständigen und Gehilfen. Die Auswertung zeigt, welche Gruppen städtisch und welche ländlich sind, wie sich die Landesteile unterscheiden und wie stark Gera unter den Städten hervortritt.",
        "en": f"Brückner's “summary of the main branches of industry” (p. 255) distributes the {en(p_all)} persons of industry in 1864 over five groups of trades, three districts, and towns and countryside. Contrary to the Middle Ages, Brückner says, most industrial people now live in the countryside: {en(100 - sg_share_st, 1)} % of the masters and assistants. The analysis shows which groups are urban and which rural, how the districts differ and how strongly Gera stands out among the towns.",
    },
    "method": {
        "de": f"Aus der Tabelle S. 255 wurden die Spalten »Städte« und »Plattland« für alle drei Landesteile und fünf Gewerbegruppen übernommen (S. = Selbständige, G. = Gehilfen, D. = Dienstboten, F. = Familienglieder). Die gedruckten Summenspalten (»Summe«) und Zeilen des Fürstenthums sind nicht verwendet, weil sie an mehreren Stellen von den Teilzahlen abweichen (siehe Vorbehalte); alle Summen und Anteile wurden aus den Städte- und Plattland-Zahlen neu berechnet. »Sonst. Industrie« heißt hier »Sonstige«. Der Anteil der Städte bezieht sich auf Selbständige + Gehilfen (sg) bzw. auf alle Personen (persons). Die Zahlen zu den Nahrungsgewerben stammen aus dem Text S. 257 (b2), die zu den Städten aus S. 256 (b2) und S. 257 (b1); der Landanteil ist die Differenz der Gesamtzahl und der städtischen Zahl.",
        "en": f"From the table on p. 255 the columns “Städte” (towns) and “Plattland” (countryside) were taken for all three districts and five groups of trades (S. = masters, G. = assistants, D. = servants, F. = family members). The printed total columns (“Summe”) and the rows for the principality are not used because they deviate from the component figures in several places (see caveats); all totals and shares were recomputed from the town and countryside figures. “Sonst. Industrie” is called “Sonstige” here. The share of the towns refers to masters + assistants (sg) or to all persons (persons). The figures for the food trades come from the text on p. 257 (b2), those for the towns from p. 256 (b2) and p. 257 (b1); the rural share is the difference between the total and the urban figure.",
    },
    "findings": [
        {"de": f"Die Städte stellen {de(sg_share_st, 1)} % der Selbständigen und Gehilfen und {de(p_share_st, 1)} % aller industriellen Personen; das Plattland entsprechend {de(100 - sg_share_st, 1)} % und {de(100 - p_share_st, 1)} %. Brückner druckt 43,70 / 56,30 % und 41,88 / 49,12 %; die letzte Zahl ist ein Druckfehler für 58,12.",
         "en": f"The towns account for {en(sg_share_st, 1)} % of the masters and assistants and {en(p_share_st, 1)} % of all industrial persons; the countryside for {en(100 - sg_share_st, 1)} % and {en(100 - p_share_st, 1)} % respectively. Brückner prints 43.70 / 56.30 % and 41.88 / 49.12 %; the last figure is a misprint for 58.12."},
        {"de": f"Am städtischsten sind die Hausausstattung ({de(share_branch['Hausausstattung'], 1)} % der Selbständigen und Gehilfen wohnen in den Städten) und die sonstigen Industriellen ({de(share_branch['Sonstige'], 1)} %); Kleidung ({de(share_branch['Kleidung'], 1)} %) und Nahrung ({de(share_branch['Nahrung'], 1)} %) liegen knapp unter der Hälfte, die Bauhandwerker sitzen mit {de(100 - share_branch['Bauhandwerker'], 1)} % überwiegend auf dem Land.",
         "en": f"The most urban groups are household and farm equipment ({en(share_branch['Hausausstattung'], 1)} % of the masters and assistants live in the towns) and other industry ({en(share_branch['Sonstige'], 1)} %); clothing ({en(share_branch['Kleidung'], 1)} %) and food ({en(share_branch['Nahrung'], 1)} %) are slightly below one half, and the building trades are mainly rural with {en(100 - share_branch['Bauhandwerker'], 1)} %."},
        {"de": f"Die Landesteile haben ein verschiedenes Profil: In Schleiz entfallen {de(kl['Schleiz'], 1)} % der industriellen Personen auf die Kleidung (Gera {de(kl['Gera'], 1)} %, Lobenstein-Ebersdorf {de(kl['Lobenstein-Ebersdorf'], 1)} %), in Lobenstein-Ebersdorf {de(bau['Lobenstein-Ebersdorf'], 1)} % auf die Bauhandwerker (Gera {de(bau['Gera'], 1)} %, Schleiz {de(bau['Schleiz'], 1)} %).",
         "en": f"The districts have different profiles: in Schleiz {en(kl['Schleiz'], 1)} % of the industrial persons belong to clothing (Gera {en(kl['Gera'], 1)} %, Lobenstein-Ebersdorf {en(kl['Lobenstein-Ebersdorf'], 1)} %), in Lobenstein-Ebersdorf {en(bau['Lobenstein-Ebersdorf'], 1)} % to the building trades (Gera {en(bau['Gera'], 1)} %, Schleiz {en(bau['Schleiz'], 1)} %)."},
        {"de": f"Unter den sechs Städten hat Gera 2016 selbständige Industrielle, die fünf anderen zusammen {de(five)}; Gera stellt damit {de(gera_share, 1)} % der städtischen Selbständigen und {de(2168 / (2168 + 1136) * 100, 1)} % der städtischen Gehilfen (2168 von 3304).",
         "en": f"Among the six towns Gera has 2,016 independent industrial people, the five others together {en(five)}; Gera thus accounts for {en(gera_share, 1)} % of the urban masters and {en(2168 / (2168 + 1136) * 100, 1)} % of the urban assistants (2,168 of 3,304)."},
        {"de": "Bei den Nahrungsgewerben sind Brauer (27 von 41), Bäcker (102 von 166), Fleischer (110 von 208) und Materialwarenhändler (76 von 117) mehrheitlich städtisch, Getreidemühlen (20 von 164) und Branntweinbrennereien (5 von 37) dagegen überwiegend ländlich.",
         "en": "Among the food trades brewers (27 of 41), bakers (102 of 166), butchers (110 of 208) and grocers (76 of 117) are mostly urban, grain mills (20 of 164) and distilleries (5 of 37) mostly rural."},
    ],
    "caveats": [
        {"de": "Die gedruckte Tabelle enthält Rechenfehler: In der Summenspalte des Landesteils Gera steht bei »Hausausstattung« S. 687 und G. 1187, die Städte- und Plattlandzahlen ergeben 685 und 1062 (die Zahl 1062 nennt auch S. 254); entsprechend stimmen die gedruckten Summen des Landesteils Gera und ihre Fortsetzung im Fürstenthum nicht. Beim Fürstenthum steht bei »Hausausstattung« im Plattland G. 707 (Summe der Landesteile: 582). Die Transkription stimmt mit dem Druck überein (Faksimile S. 255); die Neuberechnung aus den Teilzahlen stimmt in allen 15 Landesteil-Gruppen genau mit den gedruckten Gruppensummen der Detailtabellen S. 252–254 überein.",
         "en": "The printed table contains arithmetic errors: in the total column of the Gera district “Hausausstattung” shows S. 687 and G. 1187, while the town and countryside figures add up to 685 and 1062 (p. 254 also gives 1062); the printed totals of the Gera district and their continuation in the principality therefore do not match. For the principality, “Hausausstattung” in the countryside shows G. 707 (sum of the districts: 582). The transcription agrees with the print (facsimile p. 255); the recomputation from the component figures agrees exactly, in all 15 district-group cells, with the printed group totals of the detail tables on pp. 252–254."},
        {"de": "Wer zu »Städten« zählt, sagt die Tabelle nicht; Brückner spricht von sechs Städten (Gera, Schleiz, Tanna, Lobenstein, Hirschberg, Saalburg). Die städtischen Selbständigen der Tabelle (3806) liegen um 12 über der Summe der sechs Städte im Text (3794).",
         "en": "The table does not say what counts as a “town”; Brückner speaks of six towns (Gera, Schleiz, Tanna, Lobenstein, Hirschberg, Saalburg). The urban masters in the table (3,806) exceed the sum of the six towns in the text (3,794) by 12."},
        {"de": "Die Gewerbegruppen sind Brückners Einteilung (Nahrung, Kleidung, Bauhandwerker, Ausstattung für Haus und Hof, sonstige Industrielle); Dienstboten und Familienglieder sind den Gewerben zugerechnet, nicht der Landwirtschaft.",
         "en": "The groups are Brückner's classification (food, clothing, building trades, equipment for house and farm, other industrial people); servants and family members are attributed to the trades, not to agriculture."},
    ],
    "conversions": [],
    "datasets": [
        {"name": "zweige", "title": {"de": "Industrie nach Zweigen, Landesteilen, Städten und Plattland 1864", "en": "Industry by branch, district, towns and countryside, 1864"},
         "columns": [
             {"name": "district", "label": {"de": "Landesteil", "en": "District"}, "type": "string", "unit": None},
             {"name": "branch", "label": {"de": "Gewerbegruppe", "en": "Group of trades"}, "type": "string", "unit": None},
             {"name": "area", "label": {"de": "Wohnort", "en": "Location"}, "type": "string", "unit": None},
             {"name": "s", "label": {"de": "Selbständige", "en": "Masters"}, "type": "integer", "unit": "Personen"},
             {"name": "g", "label": {"de": "Gehilfen", "en": "Assistants"}, "type": "integer", "unit": "Personen"},
             {"name": "d", "label": {"de": "Dienstboten", "en": "Servants"}, "type": "integer", "unit": "Personen"},
             {"name": "f", "label": {"de": "Familienglieder", "en": "Family members"}, "type": "integer", "unit": "Personen"},
             {"name": "persons", "label": {"de": "Personen insgesamt", "en": "Persons in total"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "sg", "label": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}, "type": "integer", "unit": "Personen", "derived": True},
             {"name": "row", "label": {"de": "Tabellenzeile S. 255", "en": "Table row p. 255"}, "type": "string", "unit": None},
         ],
         "rows": rows, "source_refs": [{"page": "255", "block": "b1", "rows": "r3-r29"}]},
        {"name": "nahrung_staedte", "title": {"de": "Nahrungsgewerbe: Betriebe insgesamt und in den Städten", "en": "Food trades: enterprises in total and in the towns"},
         "columns": [
             {"name": "trade", "label": {"de": "Gewerbe", "en": "Trade"}, "type": "string", "unit": None},
             {"name": "trade_en", "label": {"de": "Gewerbe (englisch)", "en": "Trade (English)"}, "type": "string", "unit": None, "derived": True},
             {"name": "total", "label": {"de": "im ganzen Land", "en": "in the whole country"}, "type": "integer", "unit": "Betriebe"},
             {"name": "in_towns", "label": {"de": "davon in den Städten", "en": "of which in the towns"}, "type": "integer", "unit": "Betriebe"},
             {"name": "in_country", "label": {"de": "auf dem Land", "en": "in the countryside"}, "type": "integer", "unit": "Betriebe", "derived": True},
             {"name": "share_towns", "label": {"de": "Anteil der Städte", "en": "Share of the towns"}, "type": "number", "unit": "%", "derived": True},
         ],
         "rows": food_rows, "source_refs": [{"page": "257", "block": "b2"}]},
        {"name": "staedte", "title": {"de": "Selbständige Industrielle in den sechs Städten", "en": "Independent industrial people in the six towns"},
         "columns": [
             {"name": "town", "label": {"de": "Stadt", "en": "Town"}, "type": "string", "unit": None},
             {"name": "masters", "label": {"de": "Selbständige", "en": "Masters"}, "type": "integer", "unit": "Personen"},
             {"name": "assistants", "label": {"de": "Gehilfen (nur Gera einzeln genannt)", "en": "Assistants (given for Gera only)"}, "type": "integer", "unit": "Personen"},
             {"name": "source", "label": {"de": "Quelle", "en": "Source"}, "type": "string", "unit": None},
         ],
         "rows": town_rows, "source_refs": [{"page": "256", "block": "b2"}, {"page": "257", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "zweige",
         "title": {"de": "Anteil der Städte an Selbständigen und Gehilfen je Gewerbegruppe", "en": "Share of the towns in masters and assistants by group of trades"},
         "caption": {"de": f"Gesamtes Fürstenthum 1864, Anteile in Prozent. Insgesamt wohnen {de(sg_share_st, 1)} % der Selbständigen und Gehilfen in den Städten; nur die Bauhandwerker (Maurer, Zimmerleute, Dachdecker) sitzen überwiegend auf dem Land, bei Nahrung und Kleidung liegt der städtische Anteil knapp unter der Hälfte.",
                     "en": f"Whole principality, 1864, shares in percent. Overall {en(sg_share_st, 1)} % of the masters and assistants live in the towns; only the building trades (masons, carpenters, roofers) are mainly rural, while for food and clothing the urban share is just below one half."},
         "vegalite": {
             "height": 260,
             "transform": [{"aggregate": [{"op": "sum", "field": "sg", "as": "sg_sum"}], "groupby": ["branch", "area"]}, {"calculate": AREA_CALC, "as": "area_label"}, {"calculate": BRANCH_CALC, "as": "branch_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "branch", "type": "nominal", "sort": BRANCHES, "title": None, "axis": {"labelExpr": BRANCH_AXIS}},
                 "x": {"field": "sg_sum", "type": "quantitative", "stack": "normalize", "title": {"de": "Anteil an Selbständigen und Gehilfen", "en": "Share of masters and assistants"}, "axis": {"format": "%"}},
                 "color": ACOLOR,
                 "tooltip": [{"field": "branch_label", "title": {"de": "Gruppe", "en": "Group"}}, {"field": "area_label", "title": {"de": "Wohnort", "en": "Location"}},
                             {"field": "sg_sum", "title": {"de": "Selbständige und Gehilfen", "en": "Masters and assistants"}}]}}},
        {"id": "c2", "dataset": "zweige",
         "title": {"de": "Gewerbestruktur der Landesteile", "en": "Structure of industry by district"},
         "caption": {"de": "Anteil der Gewerbegruppen an allen industriellen Personen des Landesteils (Selbständige, Gehilfen, Dienstboten, Familienglieder). Schleiz ist besonders stark von der Bekleidung (Weberei) geprägt, Lobenstein-Ebersdorf von den Bauhandwerkern.",
                     "en": "Share of the groups of trades in all industrial persons of the district (masters, assistants, servants, family members). Schleiz is particularly marked by clothing (weaving), Lobenstein-Ebersdorf by the building trades."},
         "vegalite": {
             "height": 300,
             "transform": [{"aggregate": [{"op": "sum", "field": "persons", "as": "persons_sum"}], "groupby": ["district", "branch"]}, {"calculate": BRANCH_CALC, "as": "branch_label"}],
             "mark": "bar",
             "encoding": {
                 "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": None, "axis": {"labelAngle": 0}},
                 "y": {"field": "persons_sum", "type": "quantitative", "stack": "normalize", "title": {"de": "Anteil an den Personen des Landesteils", "en": "Share of the persons in the district"}, "axis": {"format": "%"}},
                 "color": BCOLOR,
                 "tooltip": [{"field": "district", "title": {"de": "Landesteil", "en": "District"}}, {"field": "branch_label", "title": {"de": "Gruppe", "en": "Group"}},
                             {"field": "persons_sum", "title": {"de": "Personen", "en": "Persons"}}]}}},
        {"id": "c3", "dataset": "nahrung_staedte",
         "title": {"de": "Nahrungsgewerbe: wie städtisch sind sie?", "en": "Food trades: how urban are they?"},
         "caption": {"de": "Anteil der Betriebe in den Städten und auf dem Land nach Brückners Angaben (S. 257). Brauer, Bäcker, Fleischer und Händler sind mehrheitlich städtisch, Mühlen und Brennereien überwiegend ländlich.",
                     "en": "Share of enterprises in the towns and in the countryside according to Brückner (p. 257). Brewers, bakers, butchers and grocers are mostly urban, mills and distilleries mostly rural."},
         "vegalite": {
             "height": 260,
             "transform": [{"fold": ["in_towns", "in_country"], "as": ["where", "n"]},
                           {"calculate": "datum.where == 'in_towns' ? 'Städte' : 'Plattland'", "as": "area"},
                           {"calculate": {"de": "datum.trade", "en": "datum.trade_en"}, "as": "trade_label"},
                           {"calculate": AREA_CALC, "as": "area_label"}],
             "mark": "bar",
             "encoding": {
                 "y": {"field": "trade_label", "type": "nominal", "sort": {"field": "share_towns", "order": "descending"}, "title": None, "axis": {"labelLimit": 260}},
                 "x": {"field": "n", "type": "quantitative", "stack": "normalize", "title": {"de": "Anteil der Betriebe", "en": "Share of enterprises"}, "axis": {"format": "%"}},
                 "color": ACOLOR,
                 "tooltip": [{"field": "trade_label", "title": {"de": "Gewerbe", "en": "Trade"}}, {"field": "area_label", "title": {"de": "Wohnort", "en": "Location"}},
                             {"field": "n", "title": {"de": "Betriebe", "en": "Enterprises"}}, {"field": "total", "title": {"de": "im ganzen Land", "en": "in the whole country"}}]}}},
        {"id": "c4", "dataset": "staedte",
         "title": {"de": "Selbständige Industrielle in den sechs Städten", "en": "Independent industrial people in the six towns"},
         "caption": {"de": f"Gera zählt 2016 Selbständige, die fünf anderen Städte zusammen {de(five)}; dazu kommen in Gera 2168 Gehilfen, in den anderen fünf zusammen 1136.",
                     "en": f"Gera counts 2,016 masters, the five other towns together {en(five)}; Gera also has 2,168 assistants, the other five together 1,136."},
         "vegalite": {
             "height": 240,
             "layer": [
                 {"mark": "bar"},
                 {"mark": {"type": "text", "align": "left", "dx": 5}, "encoding": {"text": {"field": "masters", "type": "quantitative"}}},
             ],
             "encoding": {
                 "y": {"field": "town", "type": "nominal", "sort": ["Gera", "Schleiz", "Tanna", "Lobenstein", "Hirschberg", "Saalburg"], "title": None},
                 "x": {"field": "masters", "type": "quantitative", "title": {"de": "Selbständige Industrielle", "en": "Independent industrial people"}},
                 "tooltip": [{"field": "town", "title": {"de": "Stadt", "en": "Town"}}, {"field": "masters", "title": {"de": "Selbständige", "en": "Masters"}}]}}},
    ],
    "keywords": {"de": ["Industrie", "Gewerbe", "Städte", "Plattland", "Landesteile", "Gera", "Schleiz", "Lobenstein", "Weberei", "Bauhandwerker", "1864"],
                 "en": ["industry", "trades", "towns", "countryside", "districts", "Gera", "Schleiz", "Lobenstein", "weaving", "building trades", "1864"]},
    "related": ["industrie-gewerbe-1864-einzelne-gewerbe"],
    "generated_by": GENERATED_BY,
    "date": DATE,
}
write_analysis(ana)
