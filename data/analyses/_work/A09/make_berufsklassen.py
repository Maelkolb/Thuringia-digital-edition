"""A09 / analysis 1: Berufsklassen 1864 (pp. 209-213). Reads canonical page JSON."""
import sys, re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from a09common import *

# ---------------------------------------------------------------- extraction
CLASSES = {  # nr: (page, block, first_row, col_offset, de, en)
    1: ("209", "b3", 3, 1, "Land- u. Forstwirthschaft", "Agriculture and forestry"),
    2: ("209", "b3", 3, 6, "Bergbau", "Mining"),
    3: ("209", "b3", 17, 1, "Industrie", "Industry and crafts"),
    4: ("209", "b3", 17, 6, "Handel", "Trade"),
    5: ("210", "b1", 3, 1, "Transportgewerbe", "Transport trades"),
    6: ("210", "b1", 3, 6, "Handarbeiter u. Taglöhner", "Manual and day labourers"),
    7: ("210", "b1", 16, 1, "Geistliche und Lehrer", "Clergy and teachers"),
    8: ("210", "b1", 16, 6, "Beamte und Angestellte", "Officials and employees"),
    9: ("210", "b1", 29, 1, "Militär", "Military"),
    10: ("210", "b1", 29, 6, "In Wissenschaft und Kunst Bethätigte", "Science and the arts"),
    11: ("211", "b1", 3, 1, "Pensionärs u. Rentiers", "Pensioners and annuitants"),
    12: ("211", "b1", 3, 6, "Personen ohne Berufsausübung", "Persons without occupation"),
    13: ("211", "b2", 3, 1, "Personen ohne angegebenen Beruf", "Persons with no stated occupation"),
    14: ("211", "b2", 3, 6, "Alle Berufsklassen zusammen", "All occupational classes"),
}
REGIONS = [  # (landestheil_de, landestheil_en, gebiet_de, gebiet_en)
    ("Gera", "Gera", "Städte", "Towns"), ("Gera", "Gera", "Plattland", "Countryside"), ("Gera", "Gera", "zusammen", "Total"),
    ("Schleiz", "Schleiz", "Städte", "Towns"), ("Schleiz", "Schleiz", "Plattland", "Countryside"), ("Schleiz", "Schleiz", "zusammen", "Total"),
    ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", "Städte", "Towns"), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", "Plattland", "Countryside"),
    ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf", "zusammen", "Total"),
    ("Fürstenthum", "Principality", "Städte", "Towns"), ("Fürstenthum", "Principality", "Plattland", "Countryside"),
    ("Fürstenthum", "Principality", "zusammen", "Total"),
]
data = {}  # (nr, region_index) -> [selbst, gehilfen, dienst, fam, summe]
for nr, (page, bid, r0, off, de, en) in CLASSES.items():
    g = grid(page, bid)
    for i in range(12):
        r = g[r0 - 1 + i]
        data[(nr, i)] = [n0(x) for x in r[off:off + 5]]

# totals per region = class 14 'Summe'
total = {i: data[(14, i)][4] for i in range(12)}

rows = []
for nr, (page, bid, r0, off, de, en) in CLASSES.items():
    for i, (ltd, lten, gd, ge) in enumerate(REGIONS):
        s, g_, d, f, summe = data[(nr, i)]
        rows.append([nr, de, en, ltd, lten, gd, ge, i + 1, f"{ltd}, {gd}", f"{lten}, {ge.lower()}", s or None, g_ or None, d or None, f or None, summe or None, round(100 * summe / total[i], 2)])

# ---------------------------------------------------------------- producing / unproductive (p. 213 b3)
g = grid("213", "b3")
prod_rows = []
labels = [("Gera", "Gera"), ("Schleiz", "Schleiz"), ("Lobenstein-Ebersdorf", "Lobenstein-Ebersdorf"), ("Fürstenthum", "Principality")]
for k, (lde, len_) in enumerate(labels):
    for r_i, (gd, ge) in zip((2, 3, 4), (("Städte", "Towns"), ("Plattland", "Countryside"), ("Durchschnitt", "Average"))):
        r = g[r_i]
        prod_rows.append([lde, len_, gd, ge, num(r[1 + 2 * k]), num(r[2 + 2 * k])])

# ---------------------------------------------------------------- verification against p. 212 printed percentages
heads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
g212 = grid("212", "b2")
maxdiff = 0
for i in range(12):
    r = g212[1 + i]
    pct = [n0(x) for x in r[1:12]]
    for nr, p in zip(heads, pct):
        c_ = 100 * data[(nr, i)][4] / total[i]
        maxdiff = max(maxdiff, abs(c_ - p))
print("max diff computed vs printed % (p. 212):", round(maxdiff, 3))


# ---------------------------------------------------------------- numbers for the text
def sh(nr, i):
    return 100 * data[(nr, i)][4] / total[i]


F = 11  # Fürstenthum zusammen
FS, FP = 9, 10
top3 = sh(1, F) + sh(3, F) + sh(6, F)
ind_F, agr_F, man_F = sh(3, F), sh(1, F), sh(6, F)
ind_s, ind_p = sh(3, FS), sh(3, FP)
agr_s, agr_p = sh(1, FS), sh(1, FP)
ind_G, ind_S, ind_L = sh(3, 2), sh(3, 5), sh(3, 8)
min_L = sh(2, 8)
min_L_of_F = 100 * data[(2, 8)][4] / data[(2, F)][4]
geh_s = 100 * data[(14, FS)][1] / total[FS]
geh_p = 100 * data[(14, FP)][1] / total[FP]
gehilf_ind = 100 * data[(3, F)][1] / data[(3, F)][4]
dien_agr = 100 * data[(1, F)][2] / data[(1, F)][4]
gehilf_agr = 100 * data[(1, F)][1] / data[(1, F)][4]
prod = {(r[0], r[2]): r[4] for r in prod_rows}
print(ind_F, agr_F, man_F, top3, ind_s, ind_p, agr_s, agr_p, ind_G, ind_S, ind_L, min_L, min_L_of_F, geh_s, geh_p, gehilf_ind, dien_agr)
print(total[F], data[(3, F)][4])
print(prod)
towns_higher = all(prod[(l, "Städte")] > prod[(l, "Plattland")] for l in ("Gera", "Schleiz", "Lobenstein-Ebersdorf", "Fürstenthum"))
assert towns_higher
assert max(("Gera", "Schleiz", "Lobenstein-Ebersdorf"), key=lambda l: prod[(l, "Durchschnitt")]) == "Gera"
assert min(("Gera", "Schleiz", "Lobenstein-Ebersdorf"), key=lambda l: prod[(l, "Durchschnitt")]) == "Lobenstein-Ebersdorf"
assert max((ind_G, ind_S, ind_L)) == ind_S and min((ind_G, ind_S, ind_L)) == ind_L


# ---------------------------------------------------------------- analysis
def c(name, de, en, typ, unit=None, derived=False, note=None):
    d = {"name": name, "label": bi(de, en), "type": typ, "unit": unit}
    if derived:
        d["derived"] = True
    if note:
        d["note"] = note
    return d


ref_tabs = [
    {"page": "209", "block": "b3", "rows": "r3-r14; r17-r28"},
    {"page": "210", "block": "b1", "rows": "r3-r14; r16-r27; r29-r40"},
    {"page": "211", "block": "b1", "rows": "r3-r14"},
    {"page": "211", "block": "b2", "rows": "r3-r14"},
]
ana = {
    "id": "wirtschaft-berufsklassen-1864",
    "title": bi("Berufsklassen im Fürstenthum Reuß j. L. 1864", "Occupational classes in the Principality of Reuss (younger line), 1864"),
    "category": "economy",
    "section": "t1-3-1",
    "sources": ref_tabs + [
        {"page": "212", "block": "b2", "rows": "r2-r13"},
        {"page": "212", "block": "b3"},
        {"page": "212", "block": "b5", "rows": "r2-r13"},
        {"page": "213", "block": "b2"},
        {"page": "213", "block": "b3", "rows": "r3-t5"},
    ],
    "summary": bi(
        f"Brückner gliedert die gesamte Bevölkerung von 1864 ({de_num(total[F],0)} Personen) in 13 Berufsklassen und unterscheidet in jeder Klasse Selbstständige, Gehilfen, Dienstboten und Familienglieder, getrennt nach Städten und Plattland der drei Landestheile. Die Diagramme zeigen die Anteile der Klassen, den Gegensatz von Stadt und Land, die Stellung im Beruf und den Anteil der produzierenden Bevölkerung.",
        f"Brückner divides the whole population of 1864 ({en_num(total[F],0)} persons) into 13 occupational classes and, within each class, distinguishes independents, assistants, servants and family members, separately for the towns and the countryside of the three districts. The charts show the shares of the classes, the contrast between town and country, the position within the occupation, and the share of the productive population."),
    "method": bi(
        "Die Zahlen stammen aus den Tabellen auf S. 209–211 (Berufsklassen 1–14 mit je fünf Spalten) und S. 213 (Verhältnis der produzierenden zur nicht produzierenden Bevölkerung). Der Anteil einer Klasse (Spalte share_pct) ist ihre Summe geteilt durch die Summe aller Berufsklassen derselben Region; er stimmt mit den von Brückner auf S. 212 gedruckten Prozentzahlen überein (größte Abweichung unter 0,01 Prozentpunkten). Striche (—) in der Vorlage bedeuten »keine« und stehen im Datensatz als leere Werte (bei der Berechnung der Anteile als 0 behandelt). Die Einteilung »Landestheil« und »Städte/Plattland« folgt der Vorlage; »zusammen« bezeichnet die Summenzeile des Landestheils bzw. des Fürstenthums. Bei den Stellungen im Beruf (Abb. 3) wurden die Zahlen der Klassen 1–13 für das gesamte Fürstenthum verglichen.",
        "The figures come from the tables on pp. 209–211 (occupational classes 1–14 with five columns each) and p. 213 (ratio of the productive to the non-productive population). A class's share (column share_pct) is its total divided by the total of all occupational classes of the same region; it agrees with the percentages Brückner prints on p. 212 (largest deviation below 0.01 percentage points). Dashes (—) in the source mean “none” and appear as empty values in the dataset (treated as 0 when computing the shares). The division into district and towns/countryside follows the source; “Total” denotes the sum row of a district or of the principality. For the positions within the occupation (chart 3), the figures of classes 1–13 for the whole principality were compared."),
    "findings": [
        bi(f"Drei Berufsklassen bestimmen das Bild: Industrie (einschließlich Handwerk) {de_num(ind_F)} %, Land- und Forstwirthschaft {de_num(agr_F)} % und Handarbeiter und Taglöhner {de_num(man_F)} % der Bevölkerung, zusammen {de_num(top3)} % – Brückner spricht von »nahe an 83 Procent«.",
           f"Three classes dominate: industry (including crafts) {en_num(ind_F)} %, agriculture and forestry {en_num(agr_F)} % and manual and day labourers {en_num(man_F)} % of the population, together {en_num(top3)} % – Brückner speaks of “nearly 83 per cent”."),
        bi(f"In den Städten lebten {de_num(ind_s)} % der Einwohner von der Industrie und nur {de_num(agr_s)} % von der Land- und Forstwirthschaft; auf dem Plattland waren es {de_num(ind_p)} % und {de_num(agr_p)} %. Selbst das Plattland ist damit zu mehr als zwei Fünfteln gewerblich geprägt.",
           f"In the towns {en_num(ind_s)} % of the inhabitants lived from industry and only {en_num(agr_s)} % from agriculture and forestry; in the countryside the figures were {en_num(ind_p)} % and {en_num(agr_p)} %. Even the countryside is thus more than two-fifths industrial."),
        bi(f"Der Landestheil Schleiz hat den höchsten Industrieanteil ({de_num(ind_S)} %), Lobenstein-Ebersdorf den niedrigsten ({de_num(ind_L)} %; Gera {de_num(ind_G)} %). Der Bergbau ist praktisch auf Lobenstein-Ebersdorf konzentriert: {de_num(min_L)} % der dortigen Bevölkerung, {de_num(min_L_of_F)} % aller Personen dieser Klasse im Fürstenthum.",
           f"The district of Schleiz has the highest industrial share ({en_num(ind_S)} %), Lobenstein-Ebersdorf the lowest ({en_num(ind_L)} %; Gera {en_num(ind_G)} %). Mining is practically concentrated in Lobenstein-Ebersdorf: {en_num(min_L)} % of its population and {en_num(min_L_of_F)} % of all persons of this class in the principality."),
        bi(f"Gehilfen sind in den Städten häufiger ({de_num(geh_s)} % der Stadtbevölkerung) als auf dem Plattland ({de_num(geh_p)} %). In der Industrie sind {de_num(gehilf_ind)} % der Angehörigen Gehilfen, in der Land- und Forstwirthschaft dagegen {de_num(dien_agr)} % Dienstboten und nur {de_num(gehilf_agr)} % Gehilfen.",
           f"Assistants are more frequent in the towns ({en_num(geh_s)} % of the urban population) than in the countryside ({en_num(geh_p)} %). In industry {en_num(gehilf_ind)} % of the persons are assistants; in agriculture and forestry {en_num(dien_agr)} % are servants and only {en_num(gehilf_agr)} % assistants."),
        bi(f"Der Anteil der produzierenden Berufsklassen liegt im Fürstenthum bei {de_num(prod[('Fürstenthum','Durchschnitt')],2)} %, am höchsten in Gera ({de_num(prod[('Gera','Durchschnitt')],2)} %), am niedrigsten in Lobenstein-Ebersdorf ({de_num(prod[('Lobenstein-Ebersdorf','Durchschnitt')],2)} %); in den Städten ist er überall höher als auf dem Land.",
           f"The share of the productive occupational classes in the principality is {en_num(prod[('Fürstenthum','Durchschnitt')],2)} %, highest in Gera ({en_num(prod[('Gera','Durchschnitt')],2)} %) and lowest in Lobenstein-Ebersdorf ({en_num(prod[('Lobenstein-Ebersdorf','Durchschnitt')],2)} %); in every district it is higher in the towns than in the countryside."),
    ],
    "caveats": [
        bi("Die Zahlen gelten für 1864; Familienglieder und Dienstboten werden der Klasse des Haushaltsvorstands bzw. des Dienstherrn zugerechnet. Die Klasse »Industrie« umfasst auch das Handwerk, die Klasse »Handarbeiter u. Taglöhner« vor allem ungelernte Arbeiter ohne eigenen Betrieb.",
           "The figures refer to 1864; family members and servants are counted in the class of the head of household or employer. The class “Industrie” also includes crafts; “Handarbeiter u. Taglöhner” consists mainly of unskilled workers without their own business."),
        bi("Die Vorlage ist in sich nicht ganz stimmig: In Klasse 10 (Wissenschaft und Kunst) ergeben die Plattland-Zahlen von Gera 10 + 9 + 5 + 32 = 56, gedruckt ist die Summe 52 (auch die Landestheil-Summe von 153 Gehilfen passt nur zu 5 statt 9); in Klasse 13 ist die Summe des Fürstenthums mit 1780 gedruckt, die Summe der Landestheile ergibt 1786. Beides wurde am Faksimile geprüft (Druckfehler der Vorlage) und unverändert übernommen.",
           "The source is not entirely consistent: in class 10 (science and arts) the Gera countryside figures 10 + 9 + 5 + 32 add up to 56, but the printed total is 52 (the district total of 153 assistants also fits 5 rather than 9); in class 13 the principality total is printed as 1780 whereas the district totals give 1786. Both were checked against the facsimile (misprints in the original) and taken over unchanged."),
        bi("Bei den Prozentzahlen der produzierenden Bevölkerung (Abb. 4) bleibt offen, welche Klassen Brückner im Einzelnen als »producirend« zählt; er nennt nur das Verhältnis ›40 : 60‹.",
           "For the productive-population percentages (chart 4) it remains open which classes Brückner counts as “producing”; he gives only the ratio ‘40 : 60’."),
    ],
    "datasets": [
        {"name": "klassen", "title": bi("Berufsklassen 1864 nach Landestheil und Gebiet", "Occupational classes 1864 by district and area"),
         "columns": [
             c("klasse_nr", "Nr. der Berufsklasse", "Class number", "integer"),
             c("klasse_de", "Berufsklasse", "Occupational class", "string"),
             c("klasse_en", "Berufsklasse (englisch)", "Occupational class (English)", "string"),
             c("landestheil_de", "Landestheil", "District", "string"),
             c("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             c("gebiet_de", "Gebiet", "Area", "string"),
             c("gebiet_en", "Gebiet (englisch)", "Area (English)", "string"),
             c("region_nr", "Reihenfolge der Region", "Region order", "integer", derived=True, note="Laufende Nummer 1-12 der Regionszeile, editorisch"),
             c("region_de", "Region", "Region", "string", derived=True, note="Landestheil und Gebiet, editorisch zusammengesetzt"),
             c("region_en", "Region (englisch)", "Region (English)", "string", derived=True, note="district and area, composed editorially"),
             c("selbststaendige", "Selbstständige", "Independents", "integer", "Personen"),
             c("gehilfen", "Gehilfen", "Assistants", "integer", "Personen"),
             c("dienstboten", "Dienstboten", "Servants", "integer", "Personen"),
             c("familienglieder", "Familienglieder", "Family members", "integer", "Personen"),
             c("summe", "Summe", "Total", "integer", "Personen"),
             c("share_pct", "Anteil an der Bevölkerung", "Share of population", "number", "%", derived=True, note="Summe der Klasse / Summe aller Berufsklassen der Region × 100"),
         ],
         "rows": rows, "source_refs": ref_tabs},
        {"name": "produktiv", "title": bi("Producirende und unproducirende Bevölkerung", "Productive and non-productive population"),
         "columns": [
             c("landestheil_de", "Landestheil", "District", "string"),
             c("landestheil_en", "Landestheil (englisch)", "District (English)", "string"),
             c("gebiet_de", "Gebiet", "Area", "string"),
             c("gebiet_en", "Gebiet (englisch)", "Area (English)", "string"),
             c("produktiv_pct", "Producirend", "Productive", "number", "%"),
             c("unproduktiv_pct", "Unproducirend", "Non-productive", "number", "%"),
         ],
         "rows": prod_rows, "source_refs": [{"page": "213", "block": "b3", "rows": "r3-t5"}]},
    ],
    "charts": [],
    "keywords": {
        "de": ["Berufsklassen", "Berufe", "Berufsstatistik", "Volkszählung 1864", "Industrie", "Landwirtschaft", "Handel", "Bergbau", "Taglöhner", "Dienstboten", "Städte", "Plattland"],
        "en": ["occupational classes", "occupations", "census 1864", "industry", "agriculture", "trade", "mining", "day labourers", "servants", "towns", "countryside"],
    },
    "generated_by": GENERATED_BY,
    "date": DATE,
}

TIP_REG = [{"field": {"de": "landestheil_de", "en": "landestheil_en"}, "title": bi("Landestheil", "District")},
           {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "title": bi("Gebiet", "Area")}]
CLS = {"field": {"de": "klasse_de", "en": "klasse_en"}, "type": "nominal"}
ana["charts"] = [
    {"id": "c1", "dataset": "klassen",
     "title": bi("Anteil der Berufsklassen an der Bevölkerung", "Share of the occupational classes in the population"),
     "caption": bi("Fürstenthum insgesamt, 1864; jede Person wird der Klasse ihres Haushalts zugerechnet. Die Industrie (mit Handwerk) umfasst fast die Hälfte der Bevölkerung.",
                   "Principality as a whole, 1864; every person is counted in the class of their household. Industry (including crafts) comprises almost half of the population."),
     "vegalite": {
         "height": 340,
         "transform": [{"filter": "datum.klasse_nr < 14 && datum.landestheil_de == 'Fürstenthum' && datum.gebiet_de == 'zusammen'"}],
         "mark": "bar",
         "encoding": {
             "y": {**CLS, "sort": {"field": "share_pct", "order": "descending"}, "title": None, "axis": {"labelLimit": 360}},
             "x": {"field": "share_pct", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population")},
             "tooltip": [{"field": {"de": "klasse_de", "en": "klasse_en"}, "title": bi("Berufsklasse", "Class")},
                         {"field": "summe", "title": bi("Personen", "Persons"), "format": ","},
                         {"field": "share_pct", "title": bi("% der Bevölkerung", "% of population"), "format": ".2f"}]}}},
    {"id": "c2", "dataset": "klassen",
     "title": bi("Stadt und Land in den drei Landestheilen", "Town and country in the three districts"),
     "caption": bi("Berufsstruktur der Stadt- und der Plattlandbevölkerung jedes Landestheils (Anteile an der jeweiligen Bevölkerung). Die Städte sind überall stärker von der Industrie geprägt, das Plattland von Land- und Forstwirthschaft und Handarbeit; der Bergbau tritt nur im Oberland (Lobenstein-Ebersdorf) hervor.",
                   "Occupational structure of the urban and rural population of each district (shares of the respective population). Towns are everywhere more industrial, the countryside more agricultural and manual; mining is conspicuous only in the Upper Land (Lobenstein-Ebersdorf)."),
     "vegalite": {
         "height": 300,
         "transform": [
             {"filter": "datum.klasse_nr < 14 && datum.gebiet_de != 'zusammen'"},
             {"calculate": {"de": "datum.klasse_nr == 3 ? 'Industrie' : (datum.klasse_nr == 1 ? 'Land- u. Forstwirthschaft' : (datum.klasse_nr == 6 ? 'Handarbeiter u. Taglöhner' : (datum.klasse_nr == 4 ? 'Handel' : (datum.klasse_nr == 2 ? 'Bergbau' : 'übrige Klassen'))))",
                            "en": "datum.klasse_nr == 3 ? 'Industry and crafts' : (datum.klasse_nr == 1 ? 'Agriculture and forestry' : (datum.klasse_nr == 6 ? 'Manual and day labourers' : (datum.klasse_nr == 4 ? 'Trade' : (datum.klasse_nr == 2 ? 'Mining' : 'Other classes'))))"}, "as": "grp"},
             {"calculate": "datum.klasse_nr == 3 ? 1 : (datum.klasse_nr == 1 ? 2 : (datum.klasse_nr == 6 ? 3 : (datum.klasse_nr == 4 ? 4 : (datum.klasse_nr == 2 ? 5 : 6))))", "as": "grp_order"},
             {"aggregate": [{"op": "sum", "field": "share_pct", "as": "share"}, {"op": "sum", "field": "summe", "as": "persons"}],
              "groupby": ["region_de", "region_en", "region_nr", "grp", "grp_order"]}],
         "mark": "bar",
         "encoding": {
             "y": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal", "sort": {"field": "region_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 280}},
             "x": {"field": "share", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": bi("% der Bevölkerung", "% of population")},
             "color": {"field": "grp", "type": "nominal", "title": None,
                       "scale": {"domain": [bi("Industrie", "Industry and crafts"), bi("Land- u. Forstwirthschaft", "Agriculture and forestry"), bi("Handarbeiter u. Taglöhner", "Manual and day labourers"),
                                            bi("Handel", "Trade"), bi("Bergbau", "Mining"), bi("übrige Klassen", "Other classes")]},
                       "legend": {"columns": 1, "labelLimit": 300}},
             "order": {"field": "grp_order", "type": "quantitative"},
             "tooltip": [{"field": {"de": "region_de", "en": "region_en"}, "title": bi("Region", "Region")},
                         {"field": "grp", "title": bi("Berufsklasse", "Class")},
                         {"field": "persons", "title": bi("Personen", "Persons"), "format": ","},
                         {"field": "share", "title": bi("% der Bevölkerung", "% of population"), "format": ".1f"}]}}},
    {"id": "c3", "dataset": "klassen",
     "title": bi("Stellung im Beruf nach Berufsklassen", "Position within the occupation, by class"),
     "caption": bi("Fürstenthum insgesamt; Anteile der vier Gruppen an den Angehörigen jeder Klasse. In Industrie und Handel stehen viele Gehilfen neben den Selbstständigen, in der Landwirtschaft viele Dienstboten.",
                   "Principality as a whole; shares of the four groups among the members of each class. In industry and trade many assistants stand beside the independents, in agriculture many servants."),
     "vegalite": {
         "height": 340,
         "transform": [
             {"filter": "datum.klasse_nr < 14 && datum.landestheil_de == 'Fürstenthum' && datum.gebiet_de == 'zusammen'"},
             {"fold": ["selbststaendige", "gehilfen", "dienstboten", "familienglieder"], "as": ["rolle", "n"]},
             {"calculate": {"de": "datum.rolle == 'selbststaendige' ? 'Selbstständige' : (datum.rolle == 'gehilfen' ? 'Gehilfen' : (datum.rolle == 'dienstboten' ? 'Dienstboten' : 'Familienglieder'))",
                            "en": "datum.rolle == 'selbststaendige' ? 'Independents' : (datum.rolle == 'gehilfen' ? 'Assistants' : (datum.rolle == 'dienstboten' ? 'Servants' : 'Family members'))"}, "as": "rolle_label"},
             {"calculate": "datum.rolle == 'selbststaendige' ? 1 : (datum.rolle == 'gehilfen' ? 2 : (datum.rolle == 'dienstboten' ? 3 : 4))", "as": "rolle_order"}],
         "mark": "bar",
         "encoding": {
             "y": {**CLS, "sort": {"field": "klasse_nr", "op": "min"}, "title": None, "axis": {"labelLimit": 360}},
             "x": {"field": "n", "type": "quantitative", "stack": "normalize", "title": bi("Anteil an der Klasse", "Share of the class"), "axis": {"format": "%"}},
             "color": {"field": "rolle_label", "type": "nominal", "title": None,
                       "scale": {"domain": [bi("Selbstständige", "Independents"), bi("Gehilfen", "Assistants"), bi("Dienstboten", "Servants"), bi("Familienglieder", "Family members")]},
                       "legend": {"columns": 2}},
             "order": {"field": "rolle_order", "type": "quantitative"},
             "tooltip": [{"field": {"de": "klasse_de", "en": "klasse_en"}, "title": bi("Berufsklasse", "Class")},
                         {"field": "rolle_label", "title": bi("Gruppe", "Group")},
                         {"field": "n", "title": bi("Personen", "Persons"), "format": ","}]}}},
    {"id": "c4", "dataset": "produktiv",
     "title": bi("Producirende Bevölkerung", "Productive population"),
     "caption": bi("Anteil der producirenden Berufsklassen an der Gesamtbevölkerung, nach Landestheil und Gebiet (Brückner: im Allgemeinen 40 : 60).",
                   "Share of the productive occupational classes in the total population, by district and area (Brückner: in general 40 : 60)."),
     "vegalite": {
         "height": 260,
         "mark": "bar",
         "encoding": {
             "x": {"field": {"de": "landestheil_de", "en": "landestheil_en"}, "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf", bi("Fürstenthum", "Principality")], "title": None, "axis": {"labelAngle": 0}},
             "xOffset": {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "type": "nominal", "sort": [bi("Städte", "Towns"), bi("Plattland", "Countryside"), bi("Durchschnitt", "Average")]},
             "y": {"field": "produktiv_pct", "type": "quantitative", "title": bi("% der Bevölkerung", "% of population")},
             "color": {"field": {"de": "gebiet_de", "en": "gebiet_en"}, "type": "nominal", "title": None,
                       "scale": {"domain": [bi("Städte", "Towns"), bi("Plattland", "Countryside"), bi("Durchschnitt", "Average")]}},
             "tooltip": TIP_REG + [{"field": "produktiv_pct", "title": bi("producirend, %", "productive, %"), "format": ".2f"},
                                    {"field": "unproduktiv_pct", "title": bi("unproducirend, %", "non-productive, %"), "format": ".2f"}]}}},
]
write_analysis(ana)
