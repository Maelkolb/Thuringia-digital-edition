"""A05: Sterblichkeit 1858-1867 (pp. 113-115): deaths per district, urban/rural, by sex, comparison of states."""
import re
from common import *

YEARS = list(range(1858, 1868))
g = grid("114", "b1")
LAYOUT = [("Gera", g[3:13], g[13], 1), ("Schleiz", g[3:13], g[13], 7),
          ("Lobenstein-Ebersdorf", g[15:25], g[25], 1), ("Reuß j. L.", g[15:25], g[25], 7)]
AREA_OFF = {"Städte": (0, 3), "Landorte": (1, 4), "Zusammen": (2, 5)}

deaths, deaths_mean = [], []
for k, rows, avg, j0 in LAYOUT:
    for r in rows:
        y = int(r[0])
        for area, (dn, dp) in AREA_OFF.items():
            deaths.append([y, k, area, inum(r[j0 + dn]), num(r[j0 + dp])])
    for area, (dn, dp) in AREA_OFF.items():
        deaths_mean.append([k, area, num(avg[j0 + dn]), num(avg[j0 + dp])])

# by sex (p.115 b5): r4 = Gera / Schleiz, r6 = Lobenstein-Ebersdorf / Fuerstenthum
gs = grid("115", "b5")
sx1, sx2 = gs[3], gs[5]
sex = []
for k, row, j0 in (("Gera", sx1, 1), ("Schleiz", sx1, 5), ("Lobenstein-Ebersdorf", sx2, 1), ("Reuß j. L.", sx2, 5)):
    sex.append([k, "männlich", num(row[j0]), num(row[j0 + 2])])
    sex.append([k, "weiblich", num(row[j0 + 1]), num(row[j0 + 3])])

# comparison of states (p.115 b3)
items = block("115", "b3")["items"]
states = []
for i, it in enumerate(items):
    name = it["text"].split(" . .")[0].strip()
    val = float(re.search(r"(\d+,\d+)", it["text"]).group(1).replace(",", "."))
    grp = "Reuß j. L." if name.startswith("Reuß") else ("übrige thüringische Staaten" if i < 8 else "andere Länder")
    states.append([name, grp, val, round(1000 / val, 1)])
print(states)

# ---- numbers for the texts
pct = {(r[0], r[1]): r[4] for r in deaths if r[2] == "Zusammen"}
cnt = {(r[0], r[1]): r[3] for r in deaths if r[2] == "Zusammen"}
mean_z = {r[0]: r[3] for r in deaths_mean if r[1] == "Zusammen"}
mean_n = {r[0]: r[2] for r in deaths_mean if r[1] == "Zusammen"}
mean_a = {(r[0], r[1]): r[3] for r in deaths_mean}
fue = {y: pct[(y, "Reuß j. L.")] for y in YEARS}
fue_n = {y: cnt[(y, "Reuß j. L.")] for y in YEARS}
lo = min(fue, key=fue.get)
hi = max(fue, key=fue.get)
dmax = max(((v, k, y) for (y, k), v in pct.items() if k != "Reuß j. L."))
print(mean_z, fue, dmax)
sx = {(r[0], r[1]): r[3] for r in sex}
sxn = {(r[0], r[1]): r[2] for r in sex}
excess = (sx[("Reuß j. L.", "männlich")] / sx[("Reuß j. L.", "weiblich")] - 1) * 100
assert all(sx[(k, "männlich")] > sx[(k, "weiblich")] for k in DISTRICTS)
sex_total = sxn[("Reuß j. L.", "männlich")] + sxn[("Reuß j. L.", "weiblich")]
sex_excess = (sex_total / mean_n["Reuß j. L."] - 1) * 100
print(excess, sex_total, mean_n["Reuß j. L."], sex_excess, (sx[("Reuß j. L.", "männlich")] + sx[("Reuß j. L.", "weiblich")]) / 2)
urban_hi = [k for k in DISTRICTS if mean_a[(k, "Städte")] > mean_a[(k, "Landorte")]]
print("urban higher:", urban_hi)
assert urban_hi == ["Lobenstein-Ebersdorf"]
st = {s[0]: s[3] for s in states}
stv = {s[0]: s[2] for s in states}
rank = sorted(states, key=lambda s: -s[3]).index([s for s in states if s[0] == "Reuß j. L."][0]) + 1
thu = [s for s in states if s[1] != "andere Länder"]
rank_thu = sorted(thu, key=lambda s: -s[3]).index([s for s in states if s[0] == "Reuß j. L."][0]) + 1
print(rank, rank_thu)
assert rank_thu == 2
d_hi = max(DISTRICTS[:3], key=lambda k: mean_z[k])
d_lo = min(DISTRICTS[:3], key=lambda k: mean_z[k])
assert d_hi == "Schleiz" and d_lo == "Lobenstein-Ebersdorf"

ST_EN = {"S.-Altenburg": "Saxe-Altenburg", "S.-Coburg": "Saxe-Coburg", "S.-Gotha": "Saxe-Gotha", "S.-Weimar": "Saxe-Weimar",
         "S.-Meiningen": "Saxe-Meiningen", "Reuß j. L.": "Reuss j. L.", "Oesterreich": "Austria", "Würtemberg": "Württemberg",
         "Preußen": "Prussia", "Sachsen": "Saxony (kingdom)", "Hannover": "Hanover", "Frankreich": "France",
         "Dänemark": "Denmark", "Norwegen": "Norway"}
GRP_EN = {"übrige thüringische Staaten": "Other Thuringian states", "andere Länder": "Other countries", "Reuß j. L.": "Reuß j. L."}
SEX_EN = {"männlich": "Male", "weiblich": "Female"}
GRPS = ["übrige thüringische Staaten", "andere Länder", "Reuß j. L."]

SRC = ref("114", "b1", "r4-t26")
ana = {
    "id": "bevoelkerung-sterblichkeit-1858-1867",
    "title": bi("Gestorbene und Sterblichkeit 1858–1867", "Deaths and mortality 1858–1867"),
    "category": "population",
    "section": "t1-2-1",
    "sources": [ref("113", "b5"), ref("113", "b6"), SRC, ref("114", "b2"), ref("115", "b2"), ref("115", "b3", "i1-i16"), ref("115", "b5", "r4-r6"), ref("115", "b6")],
    "summary": bi(
        f"Brückner verzeichnet die Gestorbenen 1858–1867 für die drei Landrathsbezirke und das Fürstenthum, getrennt nach Städten und Landorten, absolut und in Procenten der Bevölkerung, außerdem die Sterblichkeit nach Geschlecht und einen Vergleich mit anderen Staaten. Im Zehnjahresmittel starben {fde(mean_z['Reuß j. L.'])} Procent der Bevölkerung im Jahr ({fde(mean_n['Reuß j. L.'], 0)} Personen); die Spanne der Jahreswerte reicht von {fde(fue[lo])} ({lo}) bis {fde(fue[hi])} ({hi}). Männer starben häufiger als Frauen.",
        f"Brückner lists deaths for 1858–1867 in the three districts and the principality, split into towns and rural places, in absolute numbers and as a percentage of the population, plus mortality by sex and a comparison with other states. On the ten-year mean {fen(mean_z['Reuß j. L.'])} per cent of the population died each year ({fint_en(mean_n['Reuß j. L.'])} people); the annual values range from {fen(fue[lo])} ({lo}) to {fen(fue[hi])} ({hi}). Men died more often than women."),
    "method": bi(
        "Die Tabelle S. 114 enthält je Jahr und Landrathsbezirk (zwei Blöcke) die Gestorbenen in Städten, Landorten und zusammen sowie die entsprechenden Procente der Bevölkerung; die Mittelzeilen sind gedruckt. Die Geschlechtertabelle S. 115 gibt für 1858–1867 die durchschnittlichen Gestorbenen und die Procente der männlichen und weiblichen Bevölkerung an. Der Staatenvergleich (S. 115) nennt, auf wie viele Einwohner ein Sterbefall kommt; daraus wurden Sterbefälle auf 1000 Einwohner berechnet (1000 : Einwohner je Sterbefall; derived). Alle anderen Werte sind gedruckte Zahlen.",
        "The table on p. 114 gives for each year and district (two blocks) the deaths in towns, rural places and combined, with the corresponding percentages of the population; the mean rows are printed. The sex table on p. 115 gives for 1858–1867 the average deaths and the percentages of the male and female population. The comparison of states (p. 115) states how many inhabitants there are per death; deaths per 1,000 inhabitants were computed from this (1,000 ÷ inhabitants per death; derived). All other values are printed figures."),
    "findings": [
        bi(f"Im Fürstenthum starben jährlich im Mittel {fde(mean_n['Reuß j. L.'], 0)} Personen, {fde(mean_z['Reuß j. L.'])} Procent der Bevölkerung; das Minimum liegt bei {fde(fue[lo])} Procent ({lo}, {fue_n[lo]} Todesfälle), das Maximum bei {fde(fue[hi])} Procent ({hi}, {fue_n[hi]}).",
           f"In the principality {fint_en(mean_n['Reuß j. L.'])} people died a year on average, {fen(mean_z['Reuß j. L.'])} per cent of the population; the minimum is {fen(fue[lo])} per cent ({lo}, {fint_en(fue_n[lo])} deaths), the maximum {fen(fue[hi])} per cent ({hi}, {fint_en(fue_n[hi])})."),
        bi(f"Den höchsten Wert aller Landestheile und Jahre hat Lobenstein-Ebersdorf 1865 mit {fde(pct[(1865, 'Lobenstein-Ebersdorf')])} Procent; im Mittel hat Schleiz die höchste Sterblichkeit ({fde(mean_z['Schleiz'])}), vor Gera ({fde(mean_z['Gera'])}) und Lobenstein-Ebersdorf ({fde(mean_z['Lobenstein-Ebersdorf'])}).",
           f"The highest value of all districts and years is Lobenstein-Ebersdorf 1865 with {fen(pct[(1865, 'Lobenstein-Ebersdorf')])} per cent; on average Schleiz has the highest mortality ({fen(mean_z['Schleiz'])}), ahead of Gera ({fen(mean_z['Gera'])}) and Lobenstein-Ebersdorf ({fen(mean_z['Lobenstein-Ebersdorf'])})."),
        bi(f"Auf dem Land starben im Mittel mehr Menschen als in den Städten ({fde(mean_a[('Reuß j. L.', 'Landorte')])} gegenüber {fde(mean_a[('Reuß j. L.', 'Städte')])} Procent); nur in Lobenstein-Ebersdorf ist es umgekehrt ({fde(mean_a[('Lobenstein-Ebersdorf', 'Städte')])} gegenüber {fde(mean_a[('Lobenstein-Ebersdorf', 'Landorte')])}).",
           f"On average more people died in the countryside than in the towns ({fen(mean_a[('Reuß j. L.', 'Landorte')])} against {fen(mean_a[('Reuß j. L.', 'Städte')])} per cent); only in Lobenstein-Ebersdorf is it the other way round ({fen(mean_a[('Lobenstein-Ebersdorf', 'Städte')])} against {fen(mean_a[('Lobenstein-Ebersdorf', 'Landorte')])})."),
        bi(f"Die Sterblichkeit der Männer liegt in jedem Landestheil über der der Frauen; im Fürstenthum {fde(sx[('Reuß j. L.', 'männlich')])} gegenüber {fde(sx[('Reuß j. L.', 'weiblich')])} Procent der jeweiligen Bevölkerung, also um {fde(excess, 1)} Procent höher.",
           f"Male mortality is higher than female mortality in every district; in the principality it is {fen(sx[('Reuß j. L.', 'männlich')])} against {fen(sx[('Reuß j. L.', 'weiblich')])} per cent of the respective population, i.e. {fen(excess, 1)} per cent higher."),
        bi(f"Im Staatenvergleich kommt in Reuß j. L. ein Sterbefall auf {fde(stv['Reuß j. L.'])} Einwohner ({fde(st['Reuß j. L.'], 1)} auf 1000). Unter den thüringischen Staaten hat nur Sachsen-Altenburg ({fde(stv['S.-Altenburg'])}) eine höhere Sterblichkeit; Österreich, Württemberg, Preußen und Sachsen liegen ebenfalls darüber, Hannover, Frankreich, Dänemark und Norwegen darunter.",
           f"In the comparison of states there is one death per {fen(stv['Reuß j. L.'])} inhabitants in Reuss j. L. ({fen(st['Reuß j. L.'], 1)} per 1,000). Among the Thuringian states only Saxe-Altenburg ({fen(stv['S.-Altenburg'])}) has higher mortality; Austria, Württemberg, Prussia and Saxony are also above, Hanover, France, Denmark and Norway below."),
    ],
    "caveats": [
        bi("Die Geschlechtertabelle (S. 115) und die Haupttabelle (S. 114) stimmen nicht überein: Männer und Frauen zusammen ergeben im Fürstenthum durchschnittlich " + fde(sex_total, 1) + " Gestorbene im Jahr, die Haupttabelle " + fde(mean_n['Reuß j. L.'], 1) + " (rund " + fde(sex_excess, 1) + " Procent weniger); bei etwa gleich großer männlicher und weiblicher Bevölkerung müsste der Gesamtwert bei etwa 2,87 Procent liegen, nicht bei 2,75. Brückner erklärt das nicht.",
           "The sex table (p. 115) and the main table (p. 114) do not agree: men and women together give " + f"{sex_total:,.1f}" + " deaths a year on average in the principality, the main table " + f"{mean_n['Reuß j. L.']:,.1f}" + " (about " + fen(sex_excess, 1) + " per cent fewer); with roughly equal male and female populations the overall value should be about 2.87 per cent, not 2.75. Brückner does not explain this."),
        bi("In der Haupttabelle widersprechen sich einzelne Procentzahlen und Zahlen: Gera 1864 (2,63 Procent bei 1003 Gestorbenen; aus den Zahlen für Städte und Landorte ergäben sich etwa 2,73), Gera 1867 und Schleiz 1867 weichen ebenfalls um etwa 1 Procent ab. Nach der Tabelle ist die Sterblichkeit der Städte in Schleiz (2,81) etwas niedriger als die der Landorte (2,85), anders als Brückners Satz auf S. 114.",
           "Some percentages and counts in the main table contradict each other: Gera 1864 (2.63 per cent for 1,003 deaths; the figures for towns and rural places would give about 2.73), Gera 1867 and Schleiz 1867 also deviate by about 1 per cent. According to the table the mortality of the towns in Schleiz (2.81) is slightly lower than that of the rural places (2.85), unlike Brückner's sentence on p. 114."),
        bi("Rohe Sterbeziffern ohne Altersgliederung: Unterschiede zwischen Landestheilen und Staaten spiegeln auch Altersaufbau und Säuglingssterblichkeit. Brückner nennt für die Staaten keine Zeiträume; „Sachsen“ ist das Königreich.",
           "Crude death rates without age breakdown: differences between districts and states also reflect age structure and infant mortality. Brückner gives no periods for the states; “Sachsen” is the Kingdom of Saxony."),
    ],
    "datasets": [
        {"name": "deaths", "title": bi("Gestorbene nach Landrathsbezirk, Städten und Landorten", "Deaths by district, towns and rural places"),
         "columns": [col("year", "Jahr", "Year", "integer"),
                     col("district", "Landrathsbezirk", "District", "string", note="„Reuß j. L.“ = Fürstenthum insgesamt"),
                     col("area", "Gebiet", "Area", "string", note="Städte / Landorte / Zusammen"),
                     col("deaths", "Gestorbene", "Deaths", "integer", "Personen"),
                     col("pct_pop", "Procente der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": deaths, "source_refs": [ref("114", "b1", "r4-r13"), ref("114", "b1", "r16-r25")]},
        {"name": "deaths_mean", "title": bi("Gedrucktes Mittel 1858–1867", "Printed mean 1858–1867"),
         "columns": [col("district", "Landrathsbezirk", "District", "string"),
                     col("area", "Gebiet", "Area", "string"),
                     col("deaths", "Gestorbene (Jahresmittel)", "Deaths (annual mean)", "number", "Personen"),
                     col("pct_pop", "Procente der Bevölkerung", "Per cent of the population", "number", "%")],
         "rows": deaths_mean, "source_refs": [ref("114", "b1", "t14"), ref("114", "b1", "t26")]},
        {"name": "deaths_sex", "title": bi("Gestorbene nach Geschlecht, Mittel 1858–1867", "Deaths by sex, mean 1858–1867"),
         "columns": [col("district", "Landrathsbezirk", "District", "string"),
                     col("sex", "Geschlecht", "Sex", "string"),
                     col("deaths", "Gestorbene (Jahresmittel)", "Deaths (annual mean)", "number", "Personen"),
                     col("pct_pop", "Procente der männlichen bzw. weiblichen Bevölkerung", "Per cent of the male or female population", "number", "%")],
         "rows": sex, "source_refs": [ref("115", "b5", "r4"), ref("115", "b5", "r6")]},
        {"name": "deaths_states", "title": bi("Sterblichkeit im Staatenvergleich", "Mortality compared across states"),
         "columns": [col("state", "Staat", "State", "string"),
                     col("group", "Gruppe", "Group", "string"),
                     col("inhabitants_per_death", "Einwohner je Sterbefall", "Inhabitants per death", "number", "Einwohner"),
                     col("deaths_per_1000", "Sterbefälle auf 1000 Einwohner", "Deaths per 1,000 inhabitants", "number", "‰", derived=True, note="1000 : Einwohner je Sterbefall")],
         "rows": states, "source_refs": [ref("115", "b3", "i1-i16")]},
    ],
    "charts": [
        {"id": "c1", "dataset": "deaths",
         "title": bi("Gestorbene in Procent der Bevölkerung", "Deaths as a percentage of the population"),
         "caption": bi("Je Landrathsbezirk und für das ganze Fürstenthum (Reuß j. L.), Städte und Landorte zusammen, 1858–1867. Die Werte für Gera 1864 sind in der Vorlage uneinheitlich (siehe Anmerkungen).",
                       "By district and for the whole principality (Reuß j. L.), towns and rural places combined, 1858–1867. The values for Gera 1864 are inconsistent in the source (see notes)."),
         "vegalite": {"height": 300, "transform": [{"filter": "datum.area == 'Zusammen'"}],
                      "mark": {"type": "line", "point": True},
                      "encoding": {
                          "x": YEAR_AX,
                          "y": {"field": "pct_pop", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population"), "scale": {"domain": [2, 3.6]}},
                          "color": {"field": "district", "type": "nominal", "title": None, "scale": {"domain": DISTRICTS}, "legend": {"labelLimit": 260}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("year", "Jahr", "Year"),
                                      tip("deaths", "Gestorbene", "Deaths"),
                                      tip("pct_pop", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c2", "dataset": "deaths_mean",
         "title": bi("Städte und Landorte im Vergleich", "Towns and rural places compared"),
         "caption": bi("Gedrucktes Zehnjahresmittel 1858–1867, Gestorbene in Procent der Bevölkerung. Nur in Lobenstein-Ebersdorf liegen die Städte über dem Land.",
                       "Printed ten-year mean 1858–1867, deaths as a percentage of the population. Only in Lobenstein-Ebersdorf are the towns above the countryside."),
         "vegalite": {"height": 280, "transform": [{"filter": "datum.area != 'Zusammen'"}], "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "area", "type": "nominal", "sort": AREAS},
                          "y": {"field": "pct_pop", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population")},
                          "color": {"field": "area", "type": "nominal", "title": None, "scale": {"domain": AREAS}, "legend": {"labelExpr": lab_expr(AREA_EN)}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("area", "Gebiet", "Area"),
                                      tip("pct_pop", "% der Bevölkerung", "% of population", ".2f")]}}},
        {"id": "c3", "dataset": "deaths_sex",
         "title": bi("Sterblichkeit nach Geschlecht", "Mortality by sex"),
         "caption": bi("Durchschnitt 1858–1867, Gestorbene in Procent der männlichen bzw. weiblichen Bevölkerung. In allen Landestheilen sterben Männer häufiger.",
                       "Average 1858–1867, deaths as a percentage of the male or female population. In all districts men die more often."),
         "vegalite": {"height": 280, "mark": "bar",
                      "encoding": {
                          "x": {"field": "district", "type": "nominal", "sort": DISTRICTS, "title": DIST_TITLE, "axis": {"labelAngle": 0}},
                          "xOffset": {"field": "sex", "type": "nominal", "sort": ["männlich", "weiblich"]},
                          "y": {"field": "pct_pop", "type": "quantitative", "title": bi("% der Bevölkerung des Geschlechts", "% of population of that sex")},
                          "color": {"field": "sex", "type": "nominal", "title": None, "scale": {"domain": ["männlich", "weiblich"]}, "legend": {"labelExpr": lab_expr(SEX_EN)}},
                          "tooltip": [tip("district", "Landrathsbezirk", "District"), tip("sex", "Geschlecht", "Sex"),
                                      tip("deaths", "Gestorbene (Jahresmittel)", "Deaths (annual mean)", ".1f"),
                                      tip("pct_pop", "% der Bevölkerung des Geschlechts", "% of population of that sex", ".2f")]}}},
        {"id": "c4", "dataset": "deaths_states",
         "title": bi("Reuß j. L. im Vergleich mit anderen Staaten", "Reuß j. L. compared with other states"),
         "caption": bi("Sterbefälle auf 1000 Einwohner, aus Brückners Angabe »ein Sterbefall auf x Einwohner« (S. 115) umgerechnet; Zeiträume nicht angegeben.",
                       "Deaths per 1,000 inhabitants, converted from Brückner's “one death per x inhabitants” (p. 115); periods not stated."),
         "vegalite": {"height": 400, "mark": "bar",
                      "encoding": {
                          "y": {"field": "state", "type": "nominal", "sort": "-x", "title": None, "axis": {"labelExpr": lab_expr(ST_EN), "labelLimit": 300}},
                          "x": {"field": "deaths_per_1000", "type": "quantitative", "title": bi("Sterbefälle auf 1000 Einwohner", "deaths per 1,000 inhabitants")},
                          "color": {"field": "group", "type": "nominal", "title": None, "scale": {"domain": GRPS}, "legend": {"orient": "right", "direction": "vertical", "labelLimit": 240, "labelExpr": lab_expr(GRP_EN)}},
                          "tooltip": [tip("state", "Staat", "State"), tip("inhabitants_per_death", "Einwohner je Sterbefall", "Inhabitants per death", ".2f"),
                                      tip("deaths_per_1000", "Sterbefälle auf 1000 Einwohner", "Deaths per 1,000 inhabitants", ".1f")]}}},
    ],
    "transcription_issues": [
        {"page": "114", "block": "b1", "cell": "r10c7", "transcribed": "2,63", "facsimile": "2,63", "checked_facsimile": True,
         "note": "Gera 1864, total: 1003 deaths; the town and rural percentages (2,72 / 2,73) imply about 2,73. Printed so; the suicide table (p. 117) is consistent with 2,73."},
        {"page": "114", "block": "b1", "cell": "r13c13", "transcribed": "3,13", "facsimile": "3,13", "checked_facsimile": True,
         "note": "Schleiz 1867, total: 867 deaths and the town/rural percentages imply about 3,16; printed so."},
    ],
    "keywords": {"de": ["Sterblichkeit", "Gestorbene", "Sterbefälle", "Todesfälle", "Sterbeziffer", "Stadt und Land", "Geschlecht", "Staatenvergleich", "Bevölkerungsstatistik"],
                 "en": ["mortality", "deaths", "death rate", "town and country", "sex", "comparison of states", "population statistics"]},
    "related": ["bevoelkerung-natuerlicher-zuwachs-1858-1867", "bevoelkerung-sterblichkeit-lobenstein-1794-1804", "gesundheit-selbstmord-unglueck-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
