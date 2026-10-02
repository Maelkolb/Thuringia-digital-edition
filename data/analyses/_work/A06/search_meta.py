"""A06: search metadata for pp. 91-104 -> data/search/pages/A06.json"""
import json
from common import *

# numbers used in the summaries are read from the canonical pages
g91, g92 = grid("91", "b4"), grid("92", "b1")
gera = {int(r[0]): integer(r[10]) for r in g91[2:17]}
schl = {int(r[0]): integer(r[10]) for r in g91[18:32]}
lob = {int(r[0]): integer(r[10]) for r in g92[4:19]}
fue = {int(r[0]): integer(r[10]) for r in g92[20:34]}
g93 = grid("93", "b4")
dens = {int(r[0]): [num(x) for x in r[1:]] for r in g93[1:]}
g94 = grid("94", "b1")
states = {r[0]: (num(r[1]), int(r[2].replace(",", "")), num(r[3])) for r in g94[1:]}
houses = {r[0]: [integer(x) for x in r[1:4]] for r in grid("94", "b3")[3:]}
ur = {}
for r in grid("95", "b4")[1:]:
    if r[0].isdigit() and r[6] == "Gera.":
        ur["gera33"] = num(r[4])
    if r[0].isdigit():
        pass
g95 = grid("95", "b4")
pct_f33, pct_f67 = num(g95[20][4]), num(g95[24][4])
towns = {r[0].strip(" ."): [integer(x) for x in r[1:4]] for r in grid("96", "b3")[2:8]}
vill = {r[0].strip(" ."): [integer(x) for x in r[1:6]] for r in grid("96", "b5")[1:9]}
g98 = grid("98", "b1")
assert g98[4][9].split("\n") == ["173", "87974"]
g101 = grid("101", "b1")
g102 = grid("102", "b3")
assert integer(g102[3][3]) == 28469
assert integer(grid("103", "b3")[13][3]) == 52597
assert integer(grid("104", "b3")[4][1]) == 13945
assert fue[1647] == 23913 and fue[1867] == 87974 and gera[1867] == 38252 and schl[1867] == 27368 and lob[1867] == 22354

pages = []


def P(page, de_, en_, kde, ken, subj):
    pages.append({"page": page, "summary_de": de_, "summary_en": en_, "keywords_de": kde, "keywords_en": ken, "subjects": subj})


P("91",
  f"Beginn des Abschnitts »Das Volk – Statistik – Volksbewegung«: Tabelle der Bevölkerung der Landrathsbezirke Gera und Schleiz für 1647, 1794 bzw. 1833 und die Zählungen 1834–1867 mit Familien, Altersklassen unter und über 14 Jahre nach Geschlecht, Einwohnern und jährlichem Zuwachs. Gera wuchs von {de(gera[1647],0)} auf {de(gera[1867],0)}, Schleiz von {de(schl[1647],0)} auf {de(schl[1867],0)} Einwohner.",
  f"Start of the section “The people – statistics – population movement”: table of the population of the districts of Gera and Schleiz for 1647, 1794 or 1833 and the censuses 1834–1867 with families, age classes under and over 14 by sex, inhabitants and annual growth. Gera grew from {en(gera[1647],0)} to {en(gera[1867],0)}, Schleiz from {en(schl[1647],0)} to {en(schl[1867],0)} inhabitants.",
  ["Volksbewegung", "Bevölkerung", "Einwohnerzahl", "Volkszählung", "Gera", "Schleiz", "Familien", "Altersklassen", "Bevölkerungswachstum"],
  ["population movement", "population", "number of inhabitants", "census", "Gera", "Schleiz", "families", "age classes", "population growth"],
  ["Bevölkerung", "Volkszählung"])

P("92",
  f"Fortsetzung der Bevölkerungstabelle für Lobenstein-Ebersdorf ({de(lob[1647],0)} Einwohner 1647, {de(lob[1867],0)} 1867) und das ganze Fürstenthum ({de(fue[1647],0)} bzw. {de(fue[1867],0)}); im Text das Wachstum seit 1647 nach Bezirken und der Rückgang in Lobenstein-Ebersdorf infolge des Niedergangs der Eisen- und Wollindustrie und der Auswanderung.",
  f"Continuation of the population table for Lobenstein-Ebersdorf ({en(lob[1647],0)} inhabitants in 1647, {en(lob[1867],0)} in 1867) and the whole principality ({en(fue[1647],0)} and {en(fue[1867],0)}); the text discusses growth since 1647 by district and the decline in Lobenstein-Ebersdorf due to the decay of the iron and wool industries and to emigration.",
  ["Bevölkerung", "Fürstentum Reuß", "Lobenstein", "Ebersdorf", "Bevölkerungswachstum", "Auswanderung", "Eisenindustrie", "Wollindustrie", "Rückgang"],
  ["population", "principality of Reuss", "Lobenstein", "Ebersdorf", "population growth", "emigration", "iron industry", "wool industry", "decline"],
  ["Bevölkerung", "Volkszählung", "Auswanderung"])

P("93",
  f"Familiendichtigkeit (Seelen auf 1 Familie, 1647 und 1834–1867) und Bevölkerungsdichtigkeit (Familien und Einwohner auf 1 ☐Meile) der drei Bezirke und des Fürstenthums. 1867 kommen im Bezirk Gera {de(dens[1867][1],2)} Einwohner auf die ☐Meile, in Lobenstein-Ebersdorf {de(dens[1867][5],2)}; das Fürstenthum {de(dens[1867][7],2)}.",
  f"Family density (persons per family, 1647 and 1834–1867) and population density (families and inhabitants per square mile) of the three districts and the principality. In 1867 the district of Gera has {en(dens[1867][1],2)} inhabitants per square mile, Lobenstein-Ebersdorf {en(dens[1867][5],2)}; the principality {en(dens[1867][7],2)}.",
  ["Bevölkerungsdichte", "Familiendichte", "Familiengröße", "Quadratmeile", "Gera", "Lobenstein-Ebersdorf", "Dichte"],
  ["population density", "family density", "family size", "square mile", "Gera", "Lobenstein-Ebersdorf", "density"],
  ["Bevölkerung", "Fläche"])

sachsen = states["Königreich Sachsen"][2]
reuss = states["Fürstenthum Reuß j. L."][2]
P("94",
  f"Vergleichstabelle der Bevölkerungsdichte von 19 deutschen Staaten (Sachsen {de(sachsen,0)}, Reuß j. L. {de(reuss,0)}, Mecklenburg-Strelitz {de(states['Großherzogthum Mecklenburg-Strelitz'][2],0)} Einwohner auf der ☐Meile) und Tabelle der bewohnten Häuser 1867 mit Familien und Einwohnern je Wohnhaus nach Städten und Landorten ({de(houses['Fürstenthum'][2],0)} Häuser im Fürstenthum).",
  f"Comparison table of the population density of 19 German states (Saxony {en(sachsen,0)}, Reuss j. L. {en(reuss,0)}, Mecklenburg-Strelitz {en(states['Großherzogthum Mecklenburg-Strelitz'][2],0)} inhabitants per square mile) and table of the inhabited houses in 1867 with families and inhabitants per dwelling house in towns and rural places ({en(houses['Fürstenthum'][2],0)} houses in the principality).",
  ["Bevölkerungsdichte", "Staatenvergleich", "Sachsen", "Wohnhäuser", "Wohndichte", "Familien je Haus", "Einwohner je Haus", "Gera"],
  ["population density", "comparison of states", "Saxony", "dwelling houses", "housing density", "families per house", "inhabitants per house", "Gera"],
  ["Bevölkerung", "Wohnen", "Siedlungsform"])

P("95",
  f"Häuser je ☐Meile in den Landestheilen und im Vergleich mit Belgien, Sachsen, Baden und anderen Ländern; Tabelle der städtischen und ländlichen Bevölkerung 1833–1867 je Bezirk. Im Fürstenthum bleibt der Stadtanteil bei etwa einem Drittel ({de(pct_f33,2)} % 1833, {de(pct_f67,2)} % 1867).",
  f"Houses per square mile in the districts and in comparison with Belgium, Saxony, Baden and other countries; table of the urban and rural population 1833–1867 by district. In the principality the urban share stays at about one third ({en(pct_f33,2)} % in 1833, {en(pct_f67,2)} % in 1867).",
  ["Häuser", "Häuserdichte", "Stadt und Land", "Stadtbevölkerung", "Landbevölkerung", "Städte", "Landorte", "Belgien", "Sachsen"],
  ["houses", "house density", "town and country", "urban population", "rural population", "towns", "rural places", "Belgium", "Saxony"],
  ["Wohnen", "Stadt", "Dorf", "Bevölkerung"])

P("96",
  f"Entwicklung der Stadt- und Landbevölkerung in Gera, Schleiz und Lobenstein-Ebersdorf; Tabellen der sechs Städte (Gera {de(towns['Gera'][0],0)} Einwohner 1647, {de(towns['Gera'][2],0)} 1867; Hirschberg stärkste Zunahme) und der acht Landorte über 1000 Einwohner (Hohenleuben, Langenwetzendorf, Wurzbach, Triebes, Untermhaus, Köstritz, Langenberg, Ebersdorf).",
  f"Development of the urban and rural population in Gera, Schleiz and Lobenstein-Ebersdorf; tables of the six towns (Gera {en(towns['Gera'][0],0)} inhabitants in 1647, {en(towns['Gera'][2],0)} in 1867; Hirschberg with the strongest growth) and of the eight villages of more than 1,000 inhabitants (Hohenleuben, Langenwetzendorf, Wurzbach, Triebes, Untermhaus, Köstritz, Langenberg, Ebersdorf).",
  ["Städte", "Gera", "Schleiz", "Lobenstein", "Hirschberg", "Tanna", "Saalburg", "Hohenleuben", "Untermhaus", "Köstritz", "Einwohnerzahl"],
  ["towns", "Gera", "Schleiz", "Lobenstein", "Hirschberg", "Tanna", "Saalburg", "Hohenleuben", "Untermhaus", "Köstritz", "population"],
  ["Bevölkerung", "Stadt", "Dorf", "Eisenbahn"])

P("97",
  "Schluss der Besprechung der größeren Landorte (Ebersdorf nach dem Verlust der Residenz 1848 rückläufig); Tabelle der städtischen und ländlichen Bevölkerung nach Städten, den acht Landorten über 1000 Einwohner und den kleineren Landorten 1833 und 1867 samt Dichte je ☐Meile; Beginn des Abschnitts über die Bevölkerung im Verhältnis zu den Gemeinden.",
  "End of the discussion of the larger villages (Ebersdorf declining after the loss of the residence in 1848); table of the urban and rural population by towns, the eight villages of over 1,000 inhabitants and the smaller villages in 1833 and 1867 with density per square mile; start of the section on population in relation to the municipalities.",
  ["Landorte", "Städte", "Ebersdorf", "Residenz", "Stadt und Land", "Bevölkerungsdichte", "Gemeinden", "Gewerbe", "Landwirtschaft"],
  ["rural places", "towns", "Ebersdorf", "residence", "town and country", "population density", "municipalities", "trades", "agriculture"],
  ["Bevölkerung", "Stadt", "Dorf", "Gemeinden"])

P("98",
  "Verteilung der 173 politischen Gemeinden nach Größenklassen von 1–500 bis 16 000–17 000 Einwohnern, je Bezirk (159 Gemeinden unter, 14 über 1000 Einwohner); Beginn der Auswertung der Geburts- und Totenlisten 1859–1867 mit Geborenen, Gestorbenen, Geburtenüberschuss, Bevölkerungszunahme und Wanderungssaldo für Gera und Schleiz.",
  "Distribution of the 173 political municipalities by size class from 1–500 to 16,000–17,000 inhabitants, by district (159 municipalities under and 14 over 1,000 inhabitants); start of the evaluation of the birth and death registers 1859–1867 with births, deaths, birth surplus, population increase and migration balance for Gera and Schleiz.",
  ["Gemeinden", "Gemeindegröße", "Größenklassen", "Geborene", "Gestorbene", "Geburtenüberschuss", "Auswanderung", "Zuwanderung", "Gera", "Schleiz"],
  ["municipalities", "size classes", "births", "deaths", "birth surplus", "emigration", "immigration", "Gera", "Schleiz"],
  ["Gemeinden", "Geburten", "Sterblichkeit", "Auswanderung"])

P("99",
  "Fortsetzung der Geburts- und Sterbelisten 1859–1867 für Lobenstein-Ebersdorf und das Fürstenthum (Geburtenüberschuss, Zunahme, Auswanderungsüberschuss je Dreijahreszeitraum); Tabelle der Bevölkerung nach Geschlecht und Alter unter und über 14 Jahre in Städten und Landorten 1837–1867.",
  "Continuation of the birth and death registers 1859–1867 for Lobenstein-Ebersdorf and the principality (birth surplus, increase, emigration surplus per three-year period); table of the population by sex and age under and over 14 in towns and rural places 1837–1867.",
  ["Geborene", "Gestorbene", "Auswanderung", "Wanderungssaldo", "Geschlecht und Alter", "unter 14 Jahre", "über 14 Jahre", "Stadt und Land", "Lobenstein-Ebersdorf"],
  ["births", "deaths", "emigration", "net migration", "sex and age", "under 14", "over 14", "town and country", "Lobenstein-Ebersdorf"],
  ["Bevölkerung", "Auswanderung", "Geburten", "Sterblichkeit"])

P("100",
  "Procentverhältnisse der Bevölkerung nach Geschlecht und Altersklassen (1867 und Durchschnitt 1837–1867) für Städte, Landorte und das Fürstenthum; im Text Frauenüberschuss, höherer Kinderanteil auf dem Land und ihre Erklärung durch Wanderung und Sterblichkeit; Einleitung zur Altersstatistik nach Lebensjahren 1864.",
  "Percentage proportions of the population by sex and age class (1867 and mean 1837–1867) for towns, rural places and the principality; the text discusses the surplus of women, the higher share of children in the countryside and its explanation by migration and mortality; introduction to the age statistics by years of life for 1864.",
  ["Altersklassen", "Geschlechterverhältnis", "Frauenüberschuss", "Kinder", "Stadt und Land", "Prozentverhältnisse", "Thüringen", "Auswanderung", "Kindersterblichkeit"],
  ["age classes", "sex ratio", "surplus of women", "children", "town and country", "percentage proportions", "Thuringia", "emigration", "child mortality"],
  ["Bevölkerung", "Volkszählung"])

P("101",
  "Tabelle der Bevölkerung des Fürstenthums 1864 nach Lebensjahren 1–90, über 90 und ohne Altersangabe, getrennt nach Männern und Frauen, mit Summe und Promille auf 1000 Einwohner.",
  "Table of the population of the principality in 1864 by years of life 1–90, over 90 and age not stated, separated into men and women, with sum and per mille of 1,000 inhabitants.",
  ["Altersaufbau", "Lebensjahre", "Altersverteilung", "Männer und Frauen", "Volkszählung 1864", "Bevölkerungspyramide"],
  ["age structure", "years of life", "age distribution", "men and women", "census 1864", "population pyramid"],
  ["Bevölkerung", "Volkszählung"])

P("102",
  "Auswertung der Altersreihe: Jugend (0–14), schaffendes Alter (15–60) und Greisenalter (über 60) im Vergleich mit S.-Weimar und Württemberg, die Altersgrenzen der Volljährigkeit und Heiratsbefugnis (21 Jahre) und der Gewerbebefugnis (24 Jahre) sowie die Militärpflichtigen (19 bis 45 Jahre), absolut und auf 1000 der Bevölkerung.",
  "Evaluation of the age series: youth (0–14), productive age (15–60) and old age (over 60) compared with Saxe-Weimar and Württemberg, the age limits of majority and capacity to marry (21 years) and to trade (24 years) and the persons liable to military service (19 to 45 years), in absolute numbers and per 1,000 of the population.",
  ["Altersklassen", "Greisenalter", "schaffendes Alter", "Volljährigkeit", "Heiratsalter", "Militärpflichtige", "Weimar", "Württemberg"],
  ["age classes", "old age", "productive age", "majority", "age at marriage", "military liability", "Weimar", "Württemberg"],
  ["Bevölkerung", "Militär", "Eheschließungen"])

P("103",
  "Anteil der Militärpflichtigen auf 1000 Einwohner im Vergleich (Reuß 186,3; S.-Weimar, S.-Meiningen, S.-Altenburg, Schwarzburg-Sondershausen); Familienstand der Bevölkerung 1864 (unverheiratet, verheiratet, verwitwet, geschieden) nach Landestheilen, Städten und Dörfern, absolut und auf 1000 Männer, Frauen, Einwohner, mit Vergleichszahlen anderer Staaten.",
  "Share of persons liable to military service per 1,000 inhabitants in comparison (Reuss 186.3; Saxe-Weimar, Saxe-Meiningen, Saxe-Altenburg, Schwarzburg-Sondershausen); marital status of the population in 1864 (unmarried, married, widowed, divorced) by district, towns and villages, in absolute numbers and per 1,000 men, women and inhabitants, with figures for other states.",
  ["Familienstand", "Verheiratete", "Verwitwete", "Geschiedene", "Unverheiratete", "Militärpflichtige", "Preußen", "Württemberg"],
  ["marital status", "married", "widowed", "divorced", "unmarried", "military liability", "Prussia", "Württemberg"],
  ["Bevölkerung", "Eheschließungen", "Militär"])

P("104",
  "Auswertung des Familienstands (Schleiz mit den meisten, Lobenstein-Ebersdorf mit den wenigsten Verheirateten); Verheiratete nach Altersklassen unter 30, 30–45, 45–60 und über 60 Jahre, absolut und in Prozent, 13 945 Ehepaare; Ehen gleicher und ungleicher Altersklassen auf 1000 Ehen (nach Hildebrand, Statistik Thüringens).",
  "Evaluation of marital status (Schleiz with the most, Lobenstein-Ebersdorf with the fewest married); married persons by age classes under 30, 30–45, 45–60 and over 60, in absolute numbers and per cent, 13,945 couples; marriages of equal and unequal age classes per 1,000 marriages (after Hildebrand, Statistik Thüringens).",
  ["Verheiratete", "Ehepaare", "Altersunterschied", "Ehen", "Witwen", "Witwer", "Altersklassen", "Schleiz", "Hildebrand"],
  ["married persons", "couples", "age difference", "marriages", "widows", "widowers", "age classes", "Schleiz", "Hildebrand"],
  ["Bevölkerung", "Eheschließungen"])

glossary = [
    {"term": "Quadratmeile", "variants": ["☐Meile", "☐ Meile", "☐ M.", "□ M."], "kind": "unit",
     "de": "Flächenmaß der Statistik. Brückner nennt die Meile nicht näher; angenommen wird die geographische Quadratmeile (1 geographische Meile = 0,9894 künftige Meile zu 7 500 m, S. 832), das sind rund 55,06 km². Bei Brückner z. B. »Seelen auf die ☐Meile«.",
     "en": "Statistical unit of area. Brückner does not specify the mile; the geographical square mile is assumed (1 geographical mile = 0.9894 future mile of 7,500 m, p. 832), i.e. about 55.06 km². Used by Brückner e.g. for “souls per square mile”.",
     "pages": ["93", "94", "95", "97"]},
    {"term": "Landrathsbezirk", "variants": ["Landestheil", "Landestheile", "Bezirk"], "kind": "office",
     "de": "Verwaltungsbezirk des Fürstenthums Reuß j. L.; es gibt drei: Gera, Schleiz und Lobenstein-Ebersdorf. Brückner spricht auch von »Landestheilen«.",
     "en": "Administrative district of the Principality of Reuss j. L.; there are three: Gera, Schleiz and Lobenstein-Ebersdorf. Brückner also speaks of “Landestheile” (parts of the country).",
     "pages": ["91", "92", "93", "94", "95"]},
    {"term": "Landorte", "variants": ["Landort"], "kind": "term",
     "de": "Die ländlichen Ortschaften im Gegensatz zu den sechs Städten des Landes (Gera, Schleiz, Saalburg, Tanna, Lobenstein, Hirschberg); auch Gewerbe- und Beamtenorte wie Ebersdorf, Hohenleuben und Untermhaus zählen dazu.",
     "en": "The rural places as opposed to the six towns of the country (Gera, Schleiz, Saalburg, Tanna, Lobenstein, Hirschberg); trading and civil-service places such as Ebersdorf, Hohenleuben and Untermhaus are also counted here.",
     "pages": ["94", "95", "96", "97"]},
    {"term": "Seelen", "variants": ["Seele"], "kind": "term",
     "de": "Altes Wort für Einwohner, Personen (»Seelenzahl«); bei Brückner z. B. »Seelen auf 1 Familie«.",
     "en": "Old word for inhabitants or persons (“number of souls”); Brückner uses it e.g. for “souls per family”.",
     "pages": ["93", "94", "98"]},
    {"term": "Volksbewegung", "variants": [], "kind": "term",
     "de": "Überschrift des ersten Abschnitts der Bevölkerungsstatistik: die Entwicklung der Einwohnerzahl in den Zählungen (Familien, Alter, Geschlecht, Zuwachs).",
     "en": "Heading of the first section of the population statistics: the development of the number of inhabitants in the censuses (families, age, sex, growth).",
     "pages": ["91"]},
    {"term": "Civilstand", "variants": ["Familienstand"], "kind": "term",
     "de": "Familienstand: unverheirathet, verheirathet, verwittwet, geschieden.",
     "en": "Marital status: unmarried, married, widowed, divorced.",
     "pages": ["103", "104"]},
    {"term": "Procental", "variants": ["procentual", "Procentverhältnisse"], "kind": "term",
     "de": "In den Altersklassen-Tabellen auf S. 102 sind die »Procental«-Zahlen Promille der Gesamtbevölkerung (z. B. Jugend 329,23 auf 1000 Einwohner), nicht Prozent.",
     "en": "In the age-class tables on p. 102 the “Procental” figures are per mille of the total population (e.g. youth 329.23 per 1,000 inhabitants), not per cent.",
     "pages": ["101", "102"]},
    {"term": "schaffendes Alter", "variants": ["Greisenalter", "Jugend", "unproductives Alter"], "kind": "term",
     "de": "Brückners Einteilung nach der Arbeitskraft: Jugend 0 bis 14 Jahre, schaffendes (produktives) Alter 15 bis 60 Jahre, Greisenalter über 60 Jahre; Jugend und Greisenalter zusammen heißen »unproductives Alter«.",
     "en": "Brückner's division by capacity to work: youth 0 to 14 years, working (productive) age 15 to 60 years, old age over 60; youth and old age together are called the “unproductive age”.",
     "pages": ["102"]},
    {"term": "heirathsbefugt", "variants": ["Heirathsbefugniß", "großjährig", "Großjährigkeit"], "kind": "term",
     "de": "Nach Brückner (S. 102) treten Großjährigkeit und Befugnis zum Heiraten mit dem vollendeten 21. Lebensjahr ein, die Berechtigung zum selbstständigen Gewerbebetrieb mit dem vollendeten 24. Lebensjahr.",
     "en": "According to Brückner (p. 102) majority and the capacity to marry begin with the completed 21st year, the right to carry on a trade independently with the completed 24th year.",
     "pages": ["102"]},
    {"term": "Militärpflichtige", "variants": ["militärpflichtig"], "kind": "term",
     "de": "Wehrpflichtige; in Brückners Tabelle die Männer von 19 (einschließlich) bis 45 Jahren; sie machen im Fürstenthum 186,3 von 1000 Einwohnern aus.",
     "en": "Persons liable to military service; in Brückner's table the men from 19 (inclusive) to 45 years; they make up 186.3 of 1,000 inhabitants in the principality.",
     "pages": ["102", "103"]},
    {"term": "Reuß ä. L. / j. L.", "variants": ["Reuß älterer Linie", "Reuß jüngerer Linie"], "kind": "institution",
     "de": "Die beiden reußischen Fürstentümer: älterer Linie und jüngerer Linie; Gegenstand des Buches ist das Fürstenthum Reuß j. L. mit den Landrathsbezirken Gera, Schleiz und Lobenstein-Ebersdorf.",
     "en": "The two Reuss principalities, of the elder and the younger line; the subject of the book is the Principality of Reuss j. L. with the districts of Gera, Schleiz and Lobenstein-Ebersdorf.",
     "pages": ["94", "98"]},
    {"term": "Herrnhuter", "variants": ["Brüdergemeine"], "kind": "institution",
     "de": "Anhänger der Herrnhuter Brüdergemeine (pietistische Freikirche); Brückner nennt sie neben Gewerbe, Verkehr und fürstlicher Residenz als Ursache dafür, dass einzelne Landorte des Oberlandes stark bevölkert sind.",
     "en": "Members of the Moravian Church (Herrnhuter Brüdergemeine, a pietist free church); besides trade, traffic and a princely residence Brückner names them as a reason why some villages of the Oberland are densely populated.",
     "pages": ["96"]},
]
out = {"package": "A06", "pages": pages, "glossary": glossary}
path = ROOT / "data" / "search" / "pages" / "A06.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", path, len(pages), "pages")
