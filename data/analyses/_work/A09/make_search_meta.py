"""A09: search metadata for pages 208-241 -> data/search/pages/A09.json"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = [str(i) for i in range(208, 242)]
TEXT = {p: (ROOT / "data" / "text" / "pages" / f"{p}.txt").read_text(encoding="utf-8") for p in PAGES}

P = {}


def page(no, sde, sen, kde, ken, subj):
    P[no] = dict(page=no, summary_de=sde, summary_en=sen, keywords_de=kde, keywords_en=ken, subjects=subj)


page("208",
     "Beginn des Kapitels »Die Volksbetriebsamkeit«, Abschnitt »Berufsklassen im Allgemeinen«: Ende des Zunftwesens, Ausbreitung der Weber im Oberland seit 1700 (in der reichenfelser Pflege überflügeln sie die Landwirthschaft), Folgen von 1848, Gewerbeordnung vom 11. April 1863 und Ausführungsverordnung vom 8. Juni; Ausnahmen für Landbau, Forstwirthschaft, Bergwesen u. a.",
     "Start of chapter III “Die Volksbetriebsamkeit”, section on occupational classes in general: end of the guild system, spread of weavers in the Upper Land since 1700 (in the Reichenfels district they outstrip agriculture), consequences of 1848, trade regulations of 11 April 1863 and implementing decree of 8 June; exceptions for farming, forestry, mining and others.",
     ["Volksbetriebsamkeit", "Gewerbeordnung 1863", "Gewerbefreiheit", "Zunftwesen", "Innungen", "Weber", "Reichenfels", "Oberland", "Revolution 1848"],
     ["economic activity", "trade regulations 1863", "freedom of trade", "guilds", "weavers", "Reichenfels", "Upper Land", "revolution of 1848"],
     ["Berufe", "Handwerk", "Textilgewerbe", "Verwaltung"])
page("209",
     "Schluss der Darstellung der Gewerbeordnung (Anzeige beim Landrathsamt oder Gemeindevorstand, Concession für Gast- und Schankwirthschaften, Gewerbeordnung des Norddeutschen Bundes vom 1. October 1869, Auflösung der Innungen). Tabelle der Berufsklassen 1864 (Land- und Forstwirthschaft, Bergbau, Industrie, Handel) nach Selbstständigen, Gehilfen, Dienstboten und Familiengliedern; Fürstenthum: 17 820, 949, 43 129 und 3833 Personen.",
     "End of the account of the trade regulations (notification to the Landrath's office or municipal head, licences for inns and taverns, North German trade regulations of 1 October 1869, dissolution of guilds). Table of occupational classes in 1864 (agriculture and forestry, mining, industry, trade) by independents, assistants, servants and family members; principality: 17,820, 949, 43,129 and 3,833 persons.",
     ["Berufsklassen", "Berufsstatistik 1864", "Industrie", "Landwirtschaft", "Bergbau", "Handel", "Gewerbeordnung", "Innungen", "Dienstboten", "Städte und Plattland"],
     ["occupational classes", "occupational statistics 1864", "industry", "agriculture", "mining", "trade", "trade regulations", "guilds", "servants", "towns and countryside"],
     ["Berufe", "Bevölkerung", "Industrie", "Handel"])
page("210",
     "Berufsklassen 1864, Fortsetzung der Tabelle nach Landestheilen, Städten und Plattland: Transportgewerbe (333 Personen), Handarbeiter und Taglöhner (10 632), Geistliche und Lehrer (1116), Beamte und Angestellte (2862), Militär (494) sowie in Wissenschaft und Kunst Bethätigte (826).",
     "Occupational classes in 1864, continuation of the table by district, towns and countryside: transport trades (333 persons), manual and day labourers (10,632), clergy and teachers (1,116), officials and employees (2,862), military (494) and those active in science and the arts (826).",
     ["Berufsklassen", "Taglöhner", "Handarbeiter", "Geistliche", "Lehrer", "Beamte", "Militär", "Transportgewerbe", "Wissenschaft und Kunst", "Berufsstatistik 1864"],
     ["occupational classes", "day labourers", "manual workers", "clergy", "teachers", "officials", "military", "transport trades", "science and arts"],
     ["Berufe", "Bevölkerung", "Militär"])
page("211",
     "Schluss der Berufsklassentabelle 1864: Pensionärs und Rentiers (2552), Personen ohne Berufsausübung (140), Personen ohne angegebenen Beruf (1780) und alle Berufsklassen zusammen: 86 472 Personen im Fürstenthum, davon 36 798 im Landestheil Gera, 27 175 in Schleiz und 22 499 in Lobenstein-Ebersdorf.",
     "End of the table of occupational classes for 1864: pensioners and annuitants (2,552), persons without occupation (140), persons with no stated occupation (1,780) and all classes together: 86,472 persons in the principality, of whom 36,798 in the district of Gera, 27,175 in Schleiz and 22,499 in Lobenstein-Ebersdorf.",
     ["Berufsklassen", "Rentiers", "Pensionäre", "Gesamtbevölkerung 1864", "Einwohnerzahl", "Gera", "Schleiz", "Lobenstein-Ebersdorf", "Selbstständige", "Familienglieder"],
     ["occupational classes", "pensioners", "annuitants", "total population 1864", "inhabitants", "Gera", "Schleiz", "Lobenstein-Ebersdorf", "independents", "family members"],
     ["Berufe", "Bevölkerung", "Volkszählung"])
page("212",
     "Anteile der Berufsklassen an der Bevölkerung in Procent je Landestheil, Städte und Plattland (Fürstenthum: Industrie 49,87, Land- und Forstwirthschaft 20,61, Handarbeiter und Taglöhner 12,30); nach Brückner stellen drei Klassen nahe 83 Procent. Ferner der Anteil der Selbstständigen (26,61), Gehilfen (10,54), Dienstboten (6,29) und Familienglieder (56,56 Procent).",
     "Shares of the occupational classes in the population in per cent by district, towns and countryside (principality: industry 49.87, agriculture and forestry 20.61, manual and day labourers 12.30); according to Brückner three classes make up nearly 83 per cent. Also the shares of independents (26.61), assistants (10.54), servants (6.29) and family members (56.56 per cent).",
     ["Berufsklassen Anteile", "Industrie", "Land- und Forstwirtschaft", "Taglöhner", "Selbstständige", "Gehilfen", "Dienstboten", "Familienglieder", "Stadt und Land", "Prozent der Bevölkerung"],
     ["occupational shares", "industry", "agriculture and forestry", "day labourers", "independents", "assistants", "servants", "family members", "town and country"],
     ["Berufe", "Bevölkerung", "Industrie", "Landwirtschaft"])
page("213",
     "Vergleich der Landestheile nach der Stellung im Beruf; Verhältnis der producirenden zur unproducirenden Bevölkerung (Fürstenthum 40,25 : 59,75 Procent, Gera 43,42, Schleiz 38,46, Lobenstein-Ebersdorf 37,23). Beginn des Abschnitts »Landwirthschaft«: Unterland und Oberland nach Boden, Klima und Erntezeit (zwei bis drei Wochen früher), verbesserte Dreifelderwirthschaft; Fußnote zu den Bewirthschaftungsarten.",
     "Comparison of the districts by position within the occupation; ratio of the productive to the non-productive population (principality 40.25 : 59.75 per cent, Gera 43.42, Schleiz 38.46, Lobenstein-Ebersdorf 37.23). Start of the section “Landwirthschaft”: Lower and Upper Land by soil, climate and harvest time (two to three weeks earlier), improved three-field system; footnote on the systems of cultivation.",
     ["producirende Bevölkerung", "Erwerbstätige", "Landwirtschaft", "Unterland", "Oberland", "Dreifelderwirtschaft", "Fruchtwechselwirtschaft", "Vierfelderwirtschaft", "Erntezeit", "Elstertal"],
     ["productive population", "agriculture", "Lower Land", "Upper Land", "three-field system", "crop rotation", "four-field system", "harvest time"],
     ["Berufe", "Landwirtschaft", "Ackerbau"])
page("214",
     "Landwirthschaft des Unterlandes, Schluss: Fruchtwechsel- und Vierfelderwirthschaft, Kleebau, Kartoffeln, Flachs, Raps, Tabakbau seit 1867, Rückgang des Hopfenbaus, Vorbild der Kammer- und Rittergüter. Gartenbau in Köstritz (Rosen, Georginen) und Gera (Verein Flora), Obstzucht, Wein, Spätfrost. Beginn der Schilderung des Oberlandes.",
     "Agriculture of the Lower Land, conclusion: crop-rotation and four-field systems, clover, potatoes, flax, rape, tobacco growing since 1867, decline of hop growing, model role of the chamber and manorial estates. Horticulture at Köstritz (roses, dahlias) and Gera (society Flora), fruit growing, vines, late frost. Start of the description of the Upper Land.",
     ["Kleebau", "Kartoffeln", "Raps", "Tabakbau", "Hopfen", "Gartenbau Köstritz", "Rosen", "Georginen", "Obstbau", "Weinbau", "Gärtnerverein Flora", "Fruchtwechsel"],
     ["clover", "potatoes", "rape", "tobacco", "hops", "horticulture", "Köstritz", "roses", "dahlias", "fruit growing", "viticulture"],
     ["Ackerbau", "Obst- und Gartenbau", "Feldfrüchte"])
page("215",
     "Oberland: Klima und Boden, härtere Fruchtarten (Korn, Gerste, Hafer, Kartoffeln, Kraut, Flachs); Verhältnis der Halmfrüchte zu Kartoffeln 4 : 1 in Schleiz und 3 1/2 : 1 in Lobenstein-Ebersdorf, Gerste : Hafer : Roggen = 1 : 3 : 4; Weizen nur für den Hausbedarf, Raps, Erbsen, Klee, Luzerne, Esparsette, Flachs; Weinrebe nur bis Schleiz und Saalburg.",
     "Upper Land: climate and soil, hardier crops (rye, barley, oats, potatoes, cabbage, flax); ratio of grain to potatoes 4 : 1 in Schleiz and 3 1/2 : 1 in Lobenstein-Ebersdorf, barley : oats : rye = 1 : 3 : 4; wheat only for household needs, rape, peas, clover, lucerne, sainfoin, flax; vine only as far as Schleiz and Saalburg.",
     ["Oberland", "Getreide", "Roggen", "Gerste", "Hafer", "Kartoffeln", "Weizen", "Klee", "Luzerne", "Esparsette", "Flachs", "Schleiz"],
     ["Upper Land", "grain", "rye", "barley", "oats", "potatoes", "wheat", "clover", "lucerne", "sainfoin", "flax"],
     ["Ackerbau", "Feldfrüchte", "Landwirtschaft"])
page("216",
     "Oberland, Fortsetzung: Runkeln als Kaffee-Ersatz, Kohlrüben und Kraut, Stallfütterung statt Waldhut, Wiesen (ein-, zwei-, dreischürig), Gartenbau. Obstbäume im Landestheil Lobenstein-Ebersdorf 1866 (23 944, davon 8619 Apfelbäume; 5 je Familie; Harra 1572, Grumbach 112). Einleitung zur Landesvermessung von 1854.",
     "Upper Land, continuation: beet roots as coffee substitute, kohlrabi and cabbage, stall feeding instead of forest grazing, meadows (one-, two- and three-cut), gardening. Fruit trees in the district of Lobenstein-Ebersdorf in 1866 (23,944, of which 8,619 apple trees; 5 per family; Harra 1,572, Grumbach 112). Introduction to the land survey of 1854.",
     ["Obstbäume", "Apfelbäume", "Runkeln", "Stallfütterung", "Wiesen", "Heu", "Lobenstein-Ebersdorf", "Harra", "Grumbach", "Landesvermessung 1854"],
     ["fruit trees", "apple trees", "beet", "stall feeding", "meadows", "hay", "Lobenstein-Ebersdorf", "Harra", "Grumbach", "land survey 1854"],
     ["Ackerbau", "Obst- und Gartenbau", "Landwirtschaft"])
page("217",
     "Bodenverwendung nach der Vermessung von 1854 in Morgen und Procent für Gera, Schleiz und Lobenstein-Ebersdorf (Gehöfte, Gärten, Feld, Wiese, Hutung, Teiche, Laub- und Nadelholz, steuerfreier Boden; Gesamtfläche 322 746 Morgen); landwirthschaftlicher Boden 188 542 Morgen, 10 Morgen auf eine Familie. Fußnoten zum Zuwachs der Feldfläche und zum nur croquirten Lobenstein-Ebersdorf.",
     "Land use according to the survey of 1854 in Morgen and per cent for Gera, Schleiz and Lobenstein-Ebersdorf (farmsteads, gardens, arable land, meadow, pasture, ponds, deciduous and coniferous woodland, tax-exempt land; total area 322,746 Morgen); agricultural land 188,542 Morgen, 10 Morgen per family. Footnotes on the growth of arable land and on Lobenstein-Ebersdorf being only sketched.",
     ["Bodennutzung", "Flächennutzung", "Landesvermessung 1854", "Feld", "Wiese", "Hutung", "Nadelwald", "Laubwald", "landwirtschaftlicher Boden", "Morgen"],
     ["land use", "land survey 1854", "arable land", "meadow", "pasture", "coniferous forest", "deciduous forest", "agricultural land", "Morgen"],
     ["Landwirtschaft", "Ackerbau", "Fläche", "Wald"])
page("218",
     "Tabelle der Kammergüter, linke Hälfte (Hofraum, Gärten, Feld, Wiese, Nadelwald in Morgen): Landestheil Gera (Bieblach, Ernsee, Großaga, Niederndorf u. a.; Summe Feld 3308), Schleiz (Schleiz, Saalburg, Oschitz, Pahren u. a.; Summe Feld 2400) und Anfang von Lobenstein-Ebersdorf (Dobareuth, Ebersdorf, Grumbach).",
     "Table of the chamber estates, left half (farmstead, gardens, arable land, meadow, coniferous wood in Morgen): district of Gera (Bieblach, Ernsee, Großaga, Niederndorf and others; arable total 3,308), Schleiz (Schleiz, Saalburg, Oschitz, Pahren and others; arable total 2,400) and the beginning of Lobenstein-Ebersdorf (Dobareuth, Ebersdorf, Grumbach).",
     ["Kammergüter", "Domänen", "Kammergut Oschitz", "Niederndorf", "Großaga", "Gutsflächen", "Feld", "Wiese", "Nadelwald", "Gera", "Schleiz"],
     ["chamber estates", "domains", "Oschitz", "Niederndorf", "estate area", "arable land", "meadow", "coniferous wood"],
     ["Kammergut", "Landwirtschaft"])
page("219",
     "Tabelle der Kammergüter, rechte Hälfte: Laubwald, Hut und Wasser in Morgen, Steuerwerth und Gewinnzeit der einzelnen Güter (z. B. Laasen seit 1574, Großaga seit 1710, Niederndorf seit 1778, Tinz, Untermhaus; Schleiz: Saalburg, Dittersdorf, Oschitz; Lobenstein-Ebersdorf: Dobareuth, Ebersdorf). Summe Steuerwerth Gera 88 033.",
     "Table of the chamber estates, right half: deciduous wood, pasture and water in Morgen, tax value and date of acquisition of the individual estates (e.g. Laasen since 1574, Großaga since 1710, Niederndorf since 1778, Tinz, Untermhaus; Schleiz: Saalburg, Dittersdorf, Oschitz; Lobenstein-Ebersdorf: Dobareuth, Ebersdorf). Total tax value of Gera 88,033.",
     ["Kammergüter", "Steuerwerth", "Gewinnzeit", "Erwerbung der Güter", "Laubwald", "Hutung", "Laasen", "Großaga", "Niederndorf"],
     ["chamber estates", "tax value", "date of acquisition", "deciduous wood", "pasture", "Laasen", "Großaga", "Niederndorf"],
     ["Kammergut", "Landwirtschaft", "Steuern"])
page("220",
     "Kammergüter von Lobenstein-Ebersdorf (Harra, Haueisen, Hirschberg, Karolinenfeld, Kießling, Pöritzsch, Benzka u. a.) und Hauptsumme aller Kammergüter (Feld 8825, Wiese 3827, Nadelwald 8116 Morgen). Beginn der Tabelle der Rittergüter: Caaschwitz, Cretzschwitz, Culm, Dorna, Hartmannsdorf mit Dürrenberg u. a. im Landestheil Gera.",
     "Chamber estates of Lobenstein-Ebersdorf (Harra, Haueisen, Hirschberg, Karolinenfeld, Kießling, Pöritzsch, Benzka and others) and grand total of all chamber estates (arable 8,825, meadow 3,827, coniferous wood 8,116 Morgen). Start of the table of manorial estates: Caaschwitz, Cretzschwitz, Culm, Dorna, Hartmannsdorf with Dürrenberg and others in the district of Gera.",
     ["Kammergüter", "Rittergüter", "Harra", "Hirschberg", "Kießling", "Pöritzsch", "Benzka", "Caaschwitz", "Culm", "Hartmannsdorf", "Hauptsumme"],
     ["chamber estates", "manorial estates", "Harra", "Hirschberg", "Kießling", "Pöritzsch", "Benzka", "Caaschwitz", "Culm"],
     ["Kammergut", "Rittergut", "Landwirtschaft"])
page("221",
     "Rechte Tabellenhälften: Kammergüter von Lobenstein-Ebersdorf (Laubwald, Hut, Wasser, Steuerwerth, Gewinnzeit; Hauptsumme Steuerwerth 163 287) und Rittergüter im Landestheil Gera (Hut und Weg, Wasser, Steuerwerth und Besitzer: Nägler, Winkler, Heinke, Hausse, Kahnt, Heynisch, Fürst Reuß-Köstritz u. a.).",
     "Right table halves: chamber estates of Lobenstein-Ebersdorf (deciduous wood, pasture, water, tax value, date of acquisition; grand total of tax value 163,287) and manorial estates in the district of Gera (pasture and tracks, water, tax value and owner: Nägler, Winkler, Heinke, Hausse, Kahnt, Heynisch, Prince Reuss-Köstritz and others).",
     ["Kammergüter", "Rittergüter", "Besitzer", "Steuerwerth", "Gewinnzeit", "Heinrich LXIX. Reuß-Köstritz", "Nägler", "Gera"],
     ["chamber estates", "manorial estates", "owners", "tax value", "date of acquisition", "Reuss-Köstritz"],
     ["Kammergut", "Rittergut", "Steuern"])
page("222",
     "Rittergüter, linke Hälfte: Köstritz, Pohlitz, Kaimberg, Leumnitz, Lichtenberg, Naundorf, Pforten, Söllmnitz, Steinbrücken, Zwötzen u. a. (Gera), Frankendorf, Hohenleuben, Schilbach, Triebes u. a. (Schleiz), Blankenstein, Frössen, Mödlareuth, Pirk (Lobenstein-Ebersdorf) mit Hofraum, Garten, Feld, Wiese, Nadel- und Laubwald; Hauptsumme Feld 9638 Morgen.",
     "Manorial estates, left half: Köstritz, Pohlitz, Kaimberg, Leumnitz, Lichtenberg, Naundorf, Pforten, Söllmnitz, Steinbrücken, Zwötzen and others (Gera), Frankendorf, Hohenleuben, Schilbach, Triebes and others (Schleiz), Blankenstein, Frössen, Mödlareuth, Pirk (Lobenstein-Ebersdorf) with farmstead, garden, arable, meadow, coniferous and deciduous wood; grand total of arable 9,638 Morgen.",
     ["Rittergüter", "Köstritz", "Steinbrücken", "Söllmnitz", "Hohenleuben", "Frankendorf", "Blankenstein", "Mödlareuth", "Frössen", "Pirk", "Gutsflächen"],
     ["manorial estates", "Köstritz", "Steinbrücken", "Söllmnitz", "Hohenleuben", "Frankendorf", "Blankenstein", "Mödlareuth", "Frössen"],
     ["Rittergut", "Landwirtschaft"])
page("223",
     "Rittergüter, rechte Hälfte: Hut und Weg, Wasser, Steuerwerth und Namen der Besitzer 1867 (u. a. Fürst Heinrich LXIX. Reuß-Köstritz, Th. Schmidt, Ampach, v. Ziegenhierd, v. Naundorf, Keil, Preller, Knoch, v. Brandenstein, Rümmler, Dick); Hauptsumme Steuerwerth 169 713.",
     "Manorial estates, right half: pasture and tracks, water, tax value and names of the owners in 1867 (including Prince Heinrich LXIX Reuss-Köstritz, Th. Schmidt, Ampach, v. Ziegenhierd, v. Naundorf, Keil, Preller, Knoch, v. Brandenstein, Rümmler, Dick); grand total of tax value 169,713.",
     ["Rittergutsbesitzer", "Besitzer 1867", "Steuerwerth", "Köstritz", "Knoch", "Brandenstein", "Ampach", "Rümmler", "Rittergüter"],
     ["manorial estate owners", "owners 1867", "tax value", "Köstritz", "Knoch", "Brandenstein", "Ampach", "Rümmler"],
     ["Rittergut", "Steuern", "Landwirtschaft"])
page("224",
     "Bäuerlicher Grundbesitz: 2881 geschlossene Bauerngüter nach Größenklassen (1–20 bis über 100 Morgen), 890 Grundstücksverbände, 17 284 ledige Grundstücke, 8368 Hofraithen der Kleinhäusler; 30,69 Procent große und 69,31 Procent kleine Güter. Zerstückelung; Vergleich der Städte (Gera, Schleiz, Saalburg, Tanna, Lobenstein, Hirschberg) mit dem Flachland.",
     "Peasant landholding: 2,881 closed peasant farms by size class (1–20 to over 100 Morgen), 890 plot associations, 17,284 free-standing plots, 8,368 cottagers' house plots; 30.69 per cent large and 69.31 per cent small farms. Fragmentation; comparison of the towns (Gera, Schleiz, Saalburg, Tanna, Lobenstein, Hirschberg) with the lowland countryside.",
     ["Bauerngüter", "Grundbesitz", "Zersplitterung", "Zerstückelung", "ledige Grundstücke", "Kleinhäusler", "Größenklassen", "Städte und Flachland", "Tanna", "Bauernhöfe"],
     ["peasant farms", "landholding", "fragmentation", "free-standing plots", "cottagers", "size classes", "towns and countryside", "Tanna"],
     ["Landwirtschaft", "Stadt", "Dorf"])
page("225",
     "Zerstückelung der Höfe und Erbfolge (Hof an den jüngsten Sohn, Gesetz vom 30. April 1866 zu Abspaltungssachen); Vergleichung des landwirthschaftlichen Bodens der drei Hauptgrundbesitzer (Kammergüter 14 323, Rittergüter 12 871, bäuerlicher Grundbesitz 161 349 Morgen). Beginn der Gegenüberstellung von jährlicher Production und Consumtion (Schätzung des Landraths Fuchs, 1861).",
     "Break-up of farms and inheritance (farm goes to the youngest son, law of 30 April 1866 on splitting cases); comparison of the agricultural land of the three main landholders (chamber estates 14,323, manorial estates 12,871, peasant landholding 161,349 Morgen). Start of the comparison of annual production and consumption (estimate by Landrath Fuchs, 1861).",
     ["Erbfolge", "Jüngstenrecht", "Hofgelänge", "Grundbesitzer", "Kammergüter", "Rittergüter", "bäuerlicher Besitz", "Produktion und Konsum", "Landrath Fuchs", "Gesetz 1866"],
     ["inheritance", "ultimogeniture", "landholders", "chamber estates", "manorial estates", "peasant holdings", "production and consumption", "Landrath Fuchs"],
     ["Landwirtschaft", "Rittergut", "Ackerbau"])
page("226",
     "Annahmen zu Fruchtvertheilung und Ertrag (Weizen, Roggen, Gerste, Hafer, Kartoffeln, Hülsen- und Hackfrüchte; Säcke je Morgen, Nährwerth in Roggenwerth) und Tabellen der Anbauflächen, Säcke und Roggenwerth für Gera, Schleiz, Lobenstein-Ebersdorf und das Fürstenthum (121 170 Morgen Ackerland, 584 761 Centner Roggenwerth).",
     "Assumptions on crop distribution and yield (wheat, rye, barley, oats, potatoes, pulses and root crops; sacks per Morgen, nutritional value in rye equivalent) and tables of acreage, sacks and rye value for Gera, Schleiz, Lobenstein-Ebersdorf and the principality (121,170 Morgen of arable land, 584,761 hundredweights of rye value).",
     ["Fruchtvertheilung", "Ertrag", "Roggenwert", "Weizen", "Roggen", "Gerste", "Hafer", "Kartoffeln", "Hackfrüchte", "Hülsenfrüchte", "Säcke", "Ackerfläche"],
     ["crop distribution", "yield", "rye value", "wheat", "rye", "barley", "oats", "potatoes", "root crops", "pulses", "sacks"],
     ["Ackerbau", "Feldfrüchte", "Landwirtschaft", "Maße und Gewichte"])
page("227",
     "Bilanz von Production und Consumtion in Centnern Roggenwerth (Land: 599 532 gegen 549 816, Überschuss 49 716; Lobenstein-Ebersdorf nur 3500) und Gemeinden im Landestheil Schleiz mit Über- oder Unterproduktion; Pachtpreise, Tag- und Gesindelohn; Taglöhner und landwirthschaftliche Dienstboten 1864 (8481 bzw. 3141).",
     "Balance of production and consumption in hundredweights of rye value (country: 599,532 against 549,816, surplus 49,716; Lobenstein-Ebersdorf only 3,500) and municipalities in the district of Schleiz with surplus or shortfall; rents, day wages and servants' wages; day labourers and farm servants in 1864 (8,481 and 3,141).",
     ["Getreidebilanz", "Überschuss", "Selbstversorgung", "Pachtpreis", "Pacht", "Tagelohn", "Gesindelohn", "Knechte", "Mägde", "Taglöhner", "Dienstboten", "Schleiz"],
     ["grain balance", "surplus", "self-sufficiency", "rent", "day wage", "servants' wages", "farm hands", "maids", "day labourers", "servants"],
     ["Landwirtschaft", "Feldfrüchte", "Preise und Löhne"])
page("228",
     "»Geschichte der Landwirthschaft«: bäuerliche Lasten vor der Ablösung (Frohnen, Triften, Lehngelder, Siegelgeld, Beet- und Klauensteuer, Erbzinsen, Naturalzinsen, Decem) und Zahl der Lehnsherren in Unter- und Oberland (u. a. Langgrün mit elf Lehn); Beginn der Darstellung der Ablösung der Lehnsverhältnisse.",
     "“History of agriculture”: peasant burdens before redemption (corvées, grazing rights, feudal fees, seal money, Beete and Klauen taxes, hereditary rents, rents in kind, tithes) and number of feudal lords in the Lower and Upper Land (including Langgrün with eleven fiefs); start of the account of the redemption of feudal relations.",
     ["Feudallasten", "Frohnen", "Triften", "Lehngeld", "Klauensteuer", "Beetezins", "Erbzinsen", "Zehnt", "Lehnsherren", "Leibeigenschaft", "Langgrün"],
     ["feudal burdens", "corvée", "grazing servitudes", "feudal fees", "tithes", "feudal lords", "serfdom", "Langgrün"],
     ["Landwirtschaft", "+Agrarreform", "Territorialgeschichte"])
page("229",
     "Ablösungsgesetze: Lobenstein-Ebersdorf 22. März 1836, Schleiz 27. Dezember 1842, 18. Februar 1843 und 17. Juli 1845, Gera 23. März 1838, Entwurf 1849, Gesetz vom 15. Januar 1858 für das ganze Fürstenthum (Landrentenbank, 20faches Kapital, Amortisation in 61 Jahren), Novelle vom 16. Juli 1864; Fußnoten zu Beete und Feudallasten.",
     "Redemption laws: Lobenstein-Ebersdorf 22 March 1836, Schleiz 27 December 1842, 18 February 1843 and 17 July 1845, Gera 23 March 1838, draft of 1849, law of 15 January 1858 for the whole principality (land annuity bank, capital at 20 times the rent, amortization in 61 years), amendment of 16 July 1864; footnotes on Beete and feudal burdens.",
     ["Ablösung", "Ablösungsgesetz", "Landrentenbank", "Frohnablösung", "Triftablösung", "Lehnsablösung", "Gesetz 1858", "Novelle 1864", "Grundentlastung", "Rente"],
     ["redemption", "redemption law", "land annuity bank", "abolition of corvée", "feudal redemption", "law of 1858", "amendment of 1864", "rent"],
     ["+Agrarreform", "Landwirtschaft", "Banken und Geld"])
page("230",
     "Schluss der Ablösung: überwiesene Jahresrenten Ende Juli 1867 (Gera 4926, Schleiz 6433, Lobenstein-Ebersdorf 12 957, zusammen 24 317 Thlr. 9 Sgr.); Zerschlagung von Kammergütern (Gräfenwarth 1614 bis Frössen 1867); Rittergüter 1647 (72) und 1867 (41) nach Landestheilen und Besitzern; Beginn der landwirthschaftlichen Vereine.",
     "End of the redemption account: annual rents assigned at the end of July 1867 (Gera 4,926, Schleiz 6,433, Lobenstein-Ebersdorf 12,957, together 24,317 Thaler 9 groschen); break-up of chamber estates (Gräfenwarth 1614 to Frössen 1867); manors in 1647 (72) and 1867 (41) by district and owner; start of the agricultural societies.",
     ["Ablösungsrenten 1867", "Zerschlagung der Kammergüter", "Rittergüter 1647 und 1867", "bürgerliche Besitzer", "Gräfenwarth", "Mödlareuth", "Frössen", "Benzka", "Landwirtschaftliche Vereine"],
     ["redemption rents 1867", "break-up of chamber estates", "manors 1647 and 1867", "bourgeois owners", "Gräfenwarth", "Mödlareuth", "Frössen", "Benzka"],
     ["+Agrarreform", "Rittergut", "Kammergut", "Landwirtschaft"])
page("231",
     "Landwirthschaftliche Vereine (Gera 1844, Hohenleuben 1860, Schleiz 1845/1855, Ebersdorf 1853; Mitglieder 1868 und Bibliotheken); Einführung von Kartoffeln (um 1730), Runkeln (um 1770) und Klee (um 1780) durch große Güter; Zusammenlegungsgesetz vom 8. October 1860. Beginn des Abschnitts »Viehzucht« (Bedeutung, Pferdezucht).",
     "Agricultural societies (Gera 1844, Hohenleuben 1860, Schleiz 1845/1855, Ebersdorf 1853; members in 1868 and libraries); introduction of potatoes (c. 1730), beet (c. 1770) and clover (c. 1780) by large estates; law on consolidation of plots of 8 October 1860. Start of the section “Viehzucht” (importance, horse breeding).",
     ["Landwirtschaftlicher Verein", "Gera", "Hohenleuben", "Ebersdorf", "Kartoffeln Einführung", "Klee Einführung", "Zusammenlegung", "Viehzucht", "Pferdezucht"],
     ["agricultural society", "Gera", "Hohenleuben", "Ebersdorf", "introduction of potatoes", "introduction of clover", "consolidation of plots", "livestock breeding", "horse breeding"],
     ["Landwirtschaft", "Viehzucht", "Pferde", "Feldfrüchte"])
page("232",
     "Pferdehalterei statt Pferdezucht, Maulthiere und Esel (sechs 1864, vier 1867), Rindviehzucht (Stallfütterung, Kleebau, Märkte Schleiz und Tanna, Jungvieh aus Oberfranken), Schafzucht (Rückgang gegen das Rindvieh, Veredelung seit Mitte des 18. Jahrhunderts, Dürrenhof), Beginn der Schweinezucht.",
     "Keeping rather than breeding of horses, mules and donkeys (six in 1864, four in 1867), cattle breeding (stall feeding, clover, markets of Schleiz and Tanna, young cattle from Upper Franconia), sheep farming (decline against cattle, improvement since the mid-18th century, Dürrenhof), start of pig breeding.",
     ["Pferdehaltung", "Maultiere", "Esel", "Rindviehzucht", "Schafzucht", "Veredelung", "Schweinezucht", "Viehmärkte", "Tanna", "Schleiz"],
     ["horse keeping", "mules", "donkeys", "cattle breeding", "sheep farming", "improvement", "pig breeding", "livestock markets", "Tanna"],
     ["Viehzucht", "Pferde", "Rinder", "Schafe"])
page("233",
     "Schweinezucht (Oberland führt Ferkel ein und Mastschweine aus), Ziegen als Vieh der Armen; Viehzählungen seit 1834 bzw. 1843; Tabelle des Viehstands 1843–1867 für Gera und Schleiz (Pferde, Füllen, Stiere, Ochsen, Kühe, Jungvieh, Schafe nach Veredelung, Böcke und Ziegen, Schweine).",
     "Pig breeding (the Upper Land imports piglets and exports fattened pigs), goats as the animals of the poor; livestock counts since 1834 and 1843 respectively; table of livestock 1843–1867 for Gera and Schleiz (horses, foals, bulls, oxen, cows, young cattle, sheep by degree of improvement, bucks and goats, pigs).",
     ["Schweinezucht", "Ziegen", "Viehzählung", "Viehbestand", "Rinder", "Schafe", "Pferde", "Gera", "Schleiz", "1843", "1867"],
     ["pig breeding", "goats", "livestock census", "livestock numbers", "cattle", "sheep", "horses", "Gera", "Schleiz"],
     ["Viehzucht", "Schweine", "Rinder", "Schafe"])
page("234",
     "Viehzählung für Lobenstein-Ebersdorf und das Fürstenthum 1843–1867; Resultate der Viehzuchtbewegung in 24 Jahren (Tabelle A absolut, B auf 100 Seelen): Schafe nehmen ab (39 082 auf 30 117), Pferde, Ziegen und Schweine nehmen zu, Rinder je Einwohner ab; Beginn der Deutung.",
     "Livestock count for Lobenstein-Ebersdorf and the principality 1843–1867; results of the movement in livestock over 24 years (table A absolute, B per 100 inhabitants): sheep decrease (39,082 to 30,117), horses, goats and pigs increase, cattle per inhabitant decrease; start of the interpretation.",
     ["Viehzuchtbewegung", "Viehzählung 1867", "Schafe Rückgang", "Ziegen Zunahme", "Schweine", "Tiere je 100 Einwohner", "Lobenstein-Ebersdorf", "Fürstenthum", "Pferde"],
     ["livestock development", "livestock census 1867", "decline of sheep", "increase of goats", "pigs", "animals per 100 inhabitants", "Lobenstein-Ebersdorf"],
     ["Viehzucht", "Pferde", "Rinder", "Schafe"])
page("235",
     "Deutung der Viehzuchtbewegung nach Landestheilen; Arbeitsthiere 1867 (Rinder 32,60, Pferde 88,80 Procent; Stuten, Hengste, Wallachen); Federvieh (Lobenstein-Ebersdorf 1866: 6576 Gänse, 12 970 Hühner); Beginn der Bienenzucht (Ganzstöcke, Magazin- und Dzierzonstöcke, nur 18 Orte ohne Bienen).",
     "Interpretation of the livestock movement by district; working animals in 1867 (cattle 32.60, horses 88.80 per cent; mares, stallions, geldings); poultry (Lobenstein-Ebersdorf 1866: 6,576 geese, 12,970 hens); start of bee keeping (log hives, magazine and Dzierzon hives, only 18 places without bees).",
     ["Arbeitstiere", "Zugochsen", "Wallache", "Stuten", "Hengste", "Federvieh", "Gänse", "Hühner", "Bienenzucht", "Dzierzonstock", "Lobenstein-Ebersdorf"],
     ["working animals", "draught oxen", "geldings", "mares", "stallions", "poultry", "geese", "hens", "bee keeping", "Dzierzon hive"],
     ["Viehzucht", "Bienenzucht", "Pferde", "Rinder"])
page("236",
     "Bienenstöcke und Besitzer 1864 und 1867 nach Landestheilen (Fürstenthum 2168 bzw. 1909 Stöcke). Beginn von »4. Forstwirthschaft«: der Wald älter als das Ackerland, Rodung, Jagd als frühere Hauptnutzung, Flößerei auf Saale, Rodach, Moschwitz, Kettel, Sormitz und Elster, Köhler, Berg- und Hüttenleute und Glasmacher als Holzabnehmer.",
     "Beehives and owners in 1864 and 1867 by district (principality 2,168 and 1,909 hives). Start of “4. Forstwirthschaft”: the forest older than the arable land, clearing, hunting as the earlier main use, timber rafting on the Saale, Rodach, Moschwitz, Kettel, Sormitz and Elster, charcoal burners, miners, smelters and glassmakers as timber consumers.",
     ["Bienenstöcke", "Imker", "Forstwirtschaft Entwicklung", "Flößerei", "Saale", "Rodach", "Köhler", "Glasmacher", "Rodung", "Jagd"],
     ["beehives", "beekeepers", "history of forestry", "timber rafting", "Saale", "Rodach", "charcoal burners", "glassmakers", "clearing", "hunting"],
     ["Bienenzucht", "Forstwirtschaft", "Wald", "Holz"])
page("237",
     "Schäden des Waldes: Harzgewinnung, Viehtrieb, Waldstreu, Frevel, Windbruch, Schneedruck, Nonne und Borkenkäfer (Verwüstung 1795, Windbrüche 1819–1834, 1846/47, 1860, 1868/69; 68 000 Massenklaftern im Winter 1868/69); Waldbeschreibung von 1647 (Buchen, Tannen, Fichten); mangelhafte frühere Forstverwaltung.",
     "Damage to the forest: resin tapping, grazing, litter raking, theft, wind-break, snow-break, nun moth and bark beetle (devastation in 1795, wind-breaks 1819–1834, 1846/47, 1860, 1868/69; 68,000 cubic cords in the winter of 1868/69); description of the woods in 1647 (beech, fir, spruce); deficient earlier forest administration.",
     ["Windbruch", "Schneebruch", "Borkenkäfer", "Nonne", "Waldschäden", "Fichtenwald", "Harznutzung", "Waldstreu", "Holzfrevel", "Waldbeschreibung 1647", "Waldweide"],
     ["wind-break", "snow-break", "bark beetle", "nun moth", "forest damage", "spruce forest", "resin tapping", "litter raking", "timber theft", "woodland 1647"],
     ["Forstwirtschaft", "Wald", "Naturkatastrophen", "Insekten"])
page("238",
     "Frühere Waldnutzung (Wäldner, Plenterhieb, Kahlhieb, Holzhändler aus Grumbach, Titschendorf, Nordhalben) und forstliche Neuordnung: Waldordnungen 1751 (Lobenstein-Ebersdorf), 1806, 1807 und 1823, Ausbildung der Forstgehilfen an der Forstlehranstalt Eisenach (Regulativ 1851), durchgreifende Besserungen seit 1848, Wegebau, Aufforstung, Ablösung von Abgaben.",
     "Earlier forest use (Wäldner, selective felling, clear felling, timber merchants from Grumbach, Titschendorf, Nordhalben) and forestry reorganization: forest ordinances of 1751 (Lobenstein-Ebersdorf), 1806, 1807 and 1823, training of forest assistants at the Eisenach forestry school (regulation of 1851), thorough improvements since 1848, road building, reforestation, redemption of dues.",
     ["Waldordnung", "Forstreform", "Plenterhieb", "Kahlhieb", "Holzhändler", "Forstlehranstalt Eisenach", "Aufforstung", "Wegebau", "Forstpersonal", "Grumbach", "Titschendorf"],
     ["forest ordinance", "forestry reform", "selective felling", "clear felling", "timber merchants", "forestry school Eisenach", "reforestation", "road building"],
     ["Forstwirtschaft", "Wald", "Holz", "Verwaltung"])
page("239",
     "Forstreform, Schluss (Forstschutzgesetz vom 14. April 1852, gemischte Bestände, Arrondirung, Servituten), Forsteinrichtung in Lobenstein-Ebersdorf seit 1862, Überhauung der Privatwaldungen seit 1848, Aufsicht über Gemeinde-, Kirchen-, Pfarr- und Schulhölzer; Organisation des Forstwesens Ende 1868 (Forstdirection Schleiz, Forstinspection Ebersdorf, 26 Revierförster, 30 Forstwärter).",
     "Forestry reform, conclusion (forest protection law of 14 April 1852, mixed stands, rounding off of forests, servitudes), forest management in Lobenstein-Ebersdorf since 1862, over-felling of private woodland since 1848, supervision of municipal, church, parsonage and school woods; organization of forestry at the end of 1868 (forestry directorate Schleiz, inspection Ebersdorf, 26 district foresters, 30 forest wardens).",
     ["Forstschutzgesetz 1852", "Privatwald", "Gemeindewald", "Kirchenwald", "Forstdirection Schleiz", "Forstinspection Ebersdorf", "Revierförster", "Forstorganisation 1868", "Forsteinrichtung", "Waldservitute"],
     ["forest protection law 1852", "private woodland", "municipal forest", "church woods", "forestry directorate Schleiz", "district foresters", "forest organization 1868", "forest management"],
     ["Forstwirtschaft", "Wald", "Ämter und Behörden", "Verwaltung"])
page("240",
     "»Umfang und Vertheilung der Wälder«: Kammerforste, Gemeinde-, Stiftungs- und Privatwald nach Laub- und Nadelholz je Landestheil und Teilgebiet (Fürstenthum 133 635 Morgen, davon Nadelholz 126 339) sowie Vergleich nach Procenten, Raum, Einwohnern und Besitzstand; der Wald bedeckt 41 1/5 Procent der Oberfläche; Domainenforsten nach Forsteien.",
     "“Extent and distribution of the forests”: chamber forests, municipal, foundation and private woodland by deciduous and coniferous wood for each district and subdivision (principality 133,635 Morgen, of which coniferous 126,339) and comparison by per cent, area, inhabitants and ownership; the forest covers 41 1/5 per cent of the surface; domain forests by forestry district.",
     ["Waldfläche", "Kammerforste", "Domänenwald", "Gemeindewald", "Stiftungswald", "Privatwald", "Nadelwald", "Laubwald", "Waldanteil", "Lobenstein-Ebersdorf"],
     ["forest area", "chamber forests", "domain forest", "municipal forest", "foundation forest", "private woodland", "coniferous", "deciduous", "forest share"],
     ["Wald", "Forstwirtschaft", "Fläche"])
page("241",
     "Domänenwald 1647 (41 747 Acker, 61 786 Morgen plus Geräumde) im Vergleich zu heute; Zuwachs und Ertrag der Wälder nach Besitzart; Preise der Normalklafter Domanialholz im Oberland (Nutzholz 6–15, Brennholz 2–6 Thaler); Holzpreise je Cubikfuß 1800–1868 (Bauholz von 1 1/6 auf 3 Sgr.); Nettoertrag des Frankenwalds 1647 (1730 Thlr.); Ertrag der Privatwälder.",
     "Domain forest in 1647 (41,747 Acker, 61,786 Morgen plus cleared land) compared with today; growth and yield of the forests by type of owner; prices of the standard cord of domain timber in the Upper Land (timber 6–15, firewood 2–6 Thaler); timber prices per cubic foot 1800–1868 (construction timber from 1 1/6 to 3 groschen); net yield of the Frankenwald in 1647 (1,730 Thaler); yield of private woodland.",
     ["Holzpreise", "Normalklafter", "Bauholz", "Brennholz", "Zuwachs", "Waldertrag", "Domänenwald 1647", "Frankenwald", "Nutzholz", "Preisentwicklung"],
     ["timber prices", "standard cord", "construction timber", "firewood", "growth", "forest yield", "domain forest 1647", "Frankenwald", "price development"],
     ["Forstwirtschaft", "Holz", "Preise und Löhne", "Maße und Gewichte"])

assert list(P) == PAGES, [p for p in PAGES if p not in P]

# ------------------------------------------------------------------ glossary (pages are found automatically from variants)
GL = []


def gl(term, variants, kind, de, en, search=None):
    s = search or ([term] + variants)
    pages = [p for p in PAGES if any(re.search(v[3:] if v.startswith('re:') else re.escape(v), TEXT[p], re.I) for v in s)]
    GL.append(dict(term=term, variants=variants, kind=kind, de=de, en=en, pages=pages))


gl("Morgen", ["Mrg.", "preußischer Morgen"], "unit",
   "Flächenmaß; 1 preuß. Morgen (180 Quadratruthen) = 0,255322 ha (Brückners Tabelle S. 832).",
   "Unit of area; 1 Prussian Morgen (180 square rods) = 0.255322 ha (Brückner's table, p. 832).", search=["Morgen"])
gl("Quadratmeile", ["□ M.", "□ Meile", "Quadrat-Meile"], "unit",
   "Flächenmaß für Landes- und Verwaltungsflächen; Brückner rechnet Flächen und Dichten in Quadratmeilen (1 preuß. Meile = 2000 Ruthen = 1,0043 künftige Meile zu 7500 m, S. 832; die Quadratmeile entspricht danach rund 56,7 km², berechnet).",
   "Unit of area for territories and administrative areas; Brückner gives areas and densities in square miles (1 Prussian mile = 2,000 rods = 1.0043 future miles of 7,500 m, p. 832; the square mile thus corresponds to about 56.7 km², computed).",
   search=["□ M.", "□ Meile", "Quadratmeile", "[Quadrat] M"])
gl("Sack", ["Säcke", "Sack Getreide"], "unit",
   "Getreidemaß in Brückners Ernteberechnung: 1 Sack = 2 preußische Scheffel (S. 226).",
   "Grain measure in Brückner's harvest calculation: 1 sack = 2 Prussian bushels (p. 226).", search=["Säcke", "Sack ("])
gl("Scheffel", ["preußischer Scheffel", "dresdner Scheffel"], "unit",
   "Getreidemaß; die örtlichen Scheffel sind verschieden (dresdner Scheffel in Gera 1,0383 hl, Scheffel in Schleiz 1,4237 hl, S. 832); Brückner rechnet mit dem preußischen Scheffel (1 Sack = 2 Scheffel).",
   "Grain measure; the local bushels differ (Dresden bushel in Gera 1.0383 hl, Schleiz bushel 1.4237 hl, p. 832); Brückner calculates with the Prussian bushel (1 sack = 2 bushels).", search=["Scheffel"])
gl("Centner", ["Ctr.", "Ctnr.", "Zollcentner"], "unit",
   "Gewichtsmaß (Hundertpfund); Brückners Tabelle S. 832 nennt nur das Zollpfund (0,5 kg), ein Centner entspricht danach 100 Pfund (nicht von Brückner angegeben).",
   "Unit of weight (hundredweight); Brückner's table on p. 832 gives only the Zollpfund (0.5 kg), a Centner corresponds to 100 pounds (not stated by Brückner).",
   search=["Ctr.", "Ctnr.", "Centner"])
gl("Roggenwerth", ["Roggenwert"], "term",
   "Rechengröße für den Nährwerth von Früchten und Futter, mit Roggen = 1 (Weizen und Hülsenfrüchte 1,29, Gerste 0,76, Hafer 0,47, Kartoffeln 0,25); dient zur Gegenüberstellung von Production und Consumtion (S. 226).",
   "Accounting unit for the nutritional value of crops and fodder, with rye = 1 (wheat and pulses 1.29, barley 0.76, oats 0.47, potatoes 0.25); used to compare production and consumption (p. 226).")
gl("Klafter", ["Normalklafter", "Massenklafter", "Klaster"], "unit",
   "Raummaß für Holz; die Normalklafter umfasst 126 Cubikfuß Rauminhalt (S. 241), die geraer Klafter von 6 × 6 Fuß und 3 1/2 Fuß Scheitlänge entspricht 2,8454 m³ (S. 832); Massenklafter = geschätzte Holzmasse.",
   "Volume measure for wood; the standard cord (Normalklafter) comprises 126 cubic feet of volume (p. 241), the Gera cord of 6 × 6 feet and 3 1/2 feet log length corresponds to 2.8454 m³ (p. 832); Massenklafter = estimated mass of wood.",
   search=["Klafter", "Klaster", "Klaftern"])
gl("Cubikfuß", ["Kubikfuß", "Cubikfuss"], "unit",
   "Raummaß; 1 leipziger Kubikfuß = 0,022582 m³ (S. 832); Holzpreise und Erträge nennt Brückner je Cubikfuß.",
   "Unit of volume; 1 Leipzig cubic foot = 0.022582 m³ (p. 832); Brückner gives timber prices and yields per cubic foot.", search=["Cubikfuß"])
gl("Thaler", ["Thlr.", "Thlr"], "currency",
   "Preußische Währung; 1 Thaler = 30 Silbergroschen (Währungsrelation des preußischen Münzsystems, bei Brückner nicht erläutert).",
   "Prussian currency; 1 Thaler = 30 silver groschen (monetary relation of the Prussian coinage system, not explained by Brückner).", search=["Thlr", "Thaler"])
gl("Silbergroschen", ["Sgr.", "Ggr."], "currency",
   "Preußische Münze, 1/30 Thaler; Brückner nennt Tagelöhne und Holzpreise in Silbergroschen (»Ggr.« in älteren Angaben, S. 228 und 236, vermutlich Gutegroschen).",
   "Prussian coin, 1/30 Thaler; Brückner gives day wages and timber prices in silver groschen (“Ggr.” in older statements, pp. 228 and 236, presumably Gutegroschen).", search=["Sgr.", "Ggr.", "Silbergroschen"])
gl("Berufsklassen", ["Berufsklasse"], "term",
   "Brückners Gliederung der Bevölkerung nach dem Beruf in 14 Klassen (Land- und Forstwirthschaft, Bergbau, Industrie, Handel, Transport, Handarbeiter und Taglöhner usw.); in jeder Klasse zählt er Selbstständige, Gehilfen, Dienstboten und Familienglieder (Zählung 1864).",
   "Brückner's division of the population by occupation into 14 classes (agriculture and forestry, mining, industry, trade, transport, manual and day labourers, etc.); in every class he counts independents, assistants, servants and family members (count of 1864).")
gl("Familienglieder", ["Famil.-glieder", "Fam.glieder"], "term",
   "In der Berufsstatistik die Angehörigen des Selbstständigen (Frau, Kinder, weitere Verwandte), die der Berufsklasse des Haushaltsvorstands zugerechnet werden.",
   "In occupational statistics the dependents of the independent person (wife, children, other relatives), counted in the class of the head of household.", search=[r"re:Fam(il(ien)?)?\.?-?glieder"])
gl("Taglöhner", ["Tagelöhner", "Handarbeiter"], "term",
   "Lohnarbeiter ohne eigenen Betrieb, die tage- oder saisonweise arbeiten; Brückner führt sie mit den Handarbeitern in einer Berufsklasse (12,3 Procent der Bevölkerung 1864).",
   "Wage labourers without their own business who work by the day or season; Brückner counts them with manual workers in one occupational class (12.3 per cent of the population in 1864).", search=["Taglöhner"])
gl("Gewerbeordnung", ["Gewerbefreiheit"], "institution",
   "Gesetz vom 11. April 1863 (Ausführungsverordnung 8. Juni), das im Fürstenthum die Gewerbefreiheit einführte; ersetzt durch die Gewerbeordnung des Norddeutschen Bundes vom 1. October 1869.",
   "Law of 11 April 1863 (implementing decree 8 June) that introduced freedom of trade in the principality; replaced by the trade regulations of the North German Confederation of 1 October 1869.")
gl("Innung", ["Innungen", "Zunft", "Zunftwesen"], "institution",
   "Zunftmäßige Handwerkerkorporation; nach Einführung der Gewerbefreiheit lösten sich die Innungen großenteils auf oder gaben sich neue Statuten (S. 209).",
   "Guild-like corporation of craftsmen; after the introduction of freedom of trade the Innungen largely dissolved or adopted new statutes (p. 209).", search=[r"re:\bInnung", "Zunft"])
gl("Landrathsamt", ["Landrathsbezirk"], "office",
   "Staatliche Bezirksbehörde des Fürstenthums (Verwaltungsbehörde der Landestheile); bei ihr sind Gewerbe in Orten über 1000 Einwohner anzumelden (S. 209).",
   "State district authority of the principality (administrative authority of the districts); trades in places of more than 1,000 inhabitants had to be notified to it (p. 209).")
gl("Dreifelderwirthschaft", ["Dreifelderwirtschaft", "verbesserte Dreifelderwirthschaft"], "term",
   "Anbausystem mit Wintergetreide, Sommergetreide und Brachschlag (zu zwei Dritteln mit Futterkräutern, Handels- und Knollengewächsen bepflanzt, daher »verbessert«); im Unterland die Regel (S. 213, Fußnote).",
   "System of cultivation with winter grain, summer grain and a fallow part (two-thirds planted with fodder plants, commercial crops and tubers, hence “improved”); the rule in the Lower Land (p. 213, footnote).")
gl("Fruchtwechselwirthschaft", ["Fruchtwechsel", "Fruchtwechselwirtschaft"], "term",
   "Anbausystem, bei dem auf eine Halmfrucht nicht wieder eine Halmfrucht folgt, sondern Futterkraut, Hackfrucht oder Handelsgewächs; nach Brückner die vorteilhafteste Wirthschaft (S. 213–214).",
   "System of cultivation in which a grain crop is not followed by another grain crop but by fodder plants, root crops or commercial crops; according to Brückner the most advantageous system (pp. 213–214).")
gl("Vierfelderwirthschaft", ["Vierfelderwirtschaft"], "term",
   "Anbausystem, bei dem auf Winterfrucht Gerste und dann Hafer folgt; nach Brückner die am tiefsten stehende Wirthschaft, die die Felder aussauge (S. 214).",
   "System of cultivation in which barley and then oats follow the winter crop; according to Brückner the lowest form of farming, which exhausts the fields (p. 214).")
gl("Hackfrüchte", ["Hackfrucht", "Hackfr."], "term",
   "Hackfrüchte, Knollen- und Wurzelgewächse wie Runkeln und Rüben, die behackt werden; in Brückners Rechnung mit 125 Centner (= 78 Sack) je Morgen angesetzt (S. 226).",
   "Root and tuber crops such as beet and turnips that are hoed; in Brückner's calculation set at 125 hundredweights (= 78 sacks) per Morgen (p. 226).", search=["Hackfr"])
gl("Runkel", ["Runkeln", "Runkelrübe"], "term",
   "Runkelrübe, Futter- und Zuckerrübe; im Oberland Hauptbestandteil des einheimischen Kaffee-Ersatzes (S. 216); durch große Güter um 1770 eingeführt (S. 231).",
   "Beet, fodder or sugar beet; in the Upper Land the main ingredient of the local coffee substitute (p. 216); introduced by large estates around 1770 (p. 231).", search=["Runkel"])
gl("Esparsette", ["Luzerne"], "term",
   "Futterpflanzen (Esparsette = Süßklee, Luzerne = Schneckenklee), auf größeren Gütern vor kurzem eingeführt (S. 215, 231).",
   "Fodder plants (sainfoin and lucerne), recently introduced on larger estates (pp. 215, 231).")
gl("Hutung", ["Hut", "Hutung", "Waldhut", "Hut, Weg"], "term",
   "Weideland ohne Ackernutzung (Gemeinde- und Gutshutung); bei den Rittergütern fasst die Spalte »Hut, Weg« auch die Wege; Waldhut = Weide im Wald.",
   "Grazing land without arable use (communal and estate pasture); for the manorial estates the column “Hut, Weg” also includes tracks; Waldhut = grazing in the forest.", search=["Hutung", "Waldhut", "Hut, Weg", "Hut. Morgen"])
gl("Altheu", ["einschürig", "zweischürig", "dreischürig"], "term",
   "Heu der einschürigen Wiesen auf trockenen Hochflächen und in Waldgeräumden (S. 216); Wiesen werden nach der Zahl der Schnitte (ein-, zwei-, dreischürig) unterschieden, die dreischürigen sind meist Beunten an den Ortsrändern.",
   "Hay of the single-cut meadows on dry plateaus and in forest clearings (p. 216); meadows are distinguished by the number of cuts (one, two, three), the three-cut ones are mostly Beunten at the edges of villages.", search=["Altheu", "schürig"])
gl("Beunte", ["Beunten"], "dialect",
   "Ortsnahes Wiesenstück; bei Brückner sind die dreischürigen Wiesen meist Beunten, die an die Orte anstoßen und von deren Abflüssen genährt werden (S. 216).",
   "Meadow plot near the village; in Brückner the three-cut meadows are mostly Beunten, adjoining the villages and fed by their drainage (p. 216).")
gl("Geräumde", ["Wiesengeräumde", "Waldgeräumde"], "term",
   "Gerodete oder verwüstete Waldfläche, die als Weide oder Wiese liegen blieb (S. 237, 241); »Geräumde« des Domänenwalds 1647: 2240 Morgen.",
   "Cleared or devastated forest land left as pasture or meadow (pp. 237, 241); “Geräumde” of the domain forest in 1647: 2,240 Morgen.", search=["Geräumde"])
gl("Kammergut", ["Kammergüter", "Kammergut", "Domainen", "Domänen"], "institution",
   "Landesherrliches Gut (Domäne) in der Verwaltung der fürstlichen Kammer; Brückner führt sie mit Flächen, Steuerwerth und Gewinnzeit auf (S. 218–221).",
   "Estate of the ruling house (domain) administered by the princely chamber; Brückner lists them with areas, tax value and date of acquisition (pp. 218–221).", search=["Kammergut", "Kammergüter"])
gl("Rittergut", ["Rittergüter", "Rittersitz", "Ritterlehnstück"], "institution",
   "Adliges Gut mit besonderen Rechten (Rittersitz), 1647 alle in adligem Besitz, 1867 überwiegend bürgerlich (S. 230); die Tabellen S. 220–223 nennen Fläche, Steuerwerth und Besitzer.",
   "Noble estate with special rights (knightly seat), all in noble hands in 1647, mostly bourgeois in 1867 (p. 230); the tables pp. 220–223 give area, tax value and owner.", search=["Rittergut", "Rittergüter"])
gl("Gewinnzeit", [], "term",
   "Tabellenspalte der Kammergüter: Zeitpunkt, seit dem das Gut zur Kammer gehört (z. B. »seit 1710«, »seit frühester Zeit«).",
   "Table column of the chamber estates: date from which the estate belongs to the chamber (e.g. “since 1710”, “since earliest times”).")
gl("Steuerwerth", ["Steuereinheit", "Steuereinheiten"], "term",
   "Steuerlicher Wert eines Guts; die Spalten S. 219, 221 und 223 sind nach Brückners Berichtigung (S. 831) in Steuereinheiten zu 10 Thlr. zu lesen.",
   "Taxable value of an estate; according to Brückner's correction (p. 831) the columns on pp. 219, 221 and 223 are to be read in tax units of 10 Thaler.", search=["Steuerwerth"])
gl("Gebundene Güter", ["geschlossene Bauerngüter", "gebundenes Gut", "Bindung der Güter"], "term",
   "Geschlossene Bauerngüter, deren Zerschlagung rechtlich beschränkt ist (Bindung der Güter); Brückner zählt 2881 und teilt sie nach Größe in Klassen von 1–20 bis über 100 Morgen (S. 224).",
   "Closed peasant farms whose break-up is legally restricted (binding of estates); Brückner counts 2,881 and divides them by size into classes from 1–20 to over 100 Morgen (p. 224).", search=["geschlossene", "gebundenen Güter", "gebundene Güter", "Bindung der Güter"])
gl("Grundstücksverband", ["Grundstücksverbände"], "term",
   "Besitzform des bäuerlichen Grundbesitzes: ein Verband mehrerer Grundstücke ohne Hofstelle; 890 im Fürstenthum (S. 224).",
   "Form of peasant landholding: an association of several plots without a farmstead; 890 in the principality (p. 224).", search=["Grundstücksverband", "Grundstücksverbände", "Grundstückverband"])
gl("Ledige Grundstücke", ["ledige Grundstück", "ledigen Grundstücke"], "term",
   "Einzelne, von keinem Gutsverband erfasste Grundstücke; Brückner zählt 17 284 und rechnet sechs auf ein geschlossenes Gut (S. 224–225).",
   "Single plots not part of any estate association; Brückner counts 17,284 and reckons six per closed farm (pp. 224–225).", search=["ledige Grundstück", "ledigen Grundstück"])
gl("Hofraithe", ["Hofraith", "Hofraithen", "Hofraum"], "term",
   "Hofstelle, Haus mit Hof; »Hofraithen Kleinhäusler« sind die Hofstellen der Häusler ohne geschlossenes Gut (8368 im Fürstenthum, S. 224).",
   "Farmstead, house with yard; “Hofraithen Kleinhäusler” are the house plots of cottagers without a closed farm (8,368 in the principality, p. 224).", search=["Hofraith", "Hofraum"])
gl("Kleinhäusler", ["Häusler", "Hintersiedler"], "term",
   "Bewohner eines kleinen Hauses mit wenig oder keinem Land (Häusler, Hintersiedler); in Brückners Güterstatistik eigene Besitzgruppe.",
   "Inhabitant of a small house with little or no land (cottager); a separate group of holders in Brückner's landholding statistics.", search=["Kleinhäusler", "Hintersiedler"])
gl("Pertinenzen", ["Pertinenz"], "term",
   "Zubehörstücke zu Gütern, die in anderen Fluren liegen (Spalte der Bauerngut-Tabelle, S. 224).",
   "Appurtenances of estates lying in other parishes (column of the peasant-farm table, p. 224).")
gl("Hofgelänge", [], "term",
   "Schmaler, vom Hof aus meist bis zur Flurgrenze reichender Landstreifen, der hintereinander Feld, Wiese, Wald oder Hutung enthält (S. 225); Form der Gemengelage der Flur.",
   "Narrow strip of land, mostly running from the farm to the boundary of the parish, containing in succession field, meadow, woodland or pasture (p. 225); form of intermixed field strips.")
gl("Frohnen", ["Frohn", "Fröhner", "Hand- und Spanndienste"], "term",
   "Dienstleistungen der Hörigen für den Grundherrn (Hand- und Spanndienste, gemessen oder ungemessen); die wichtigste der bäuerlichen Lasten vor der Ablösung (S. 228).",
   "Services of serfs for the lord of the manor (hand and team services, fixed or unfixed); the most important of the peasant burdens before redemption (p. 228).", search=["Frohn", "Fröhner"])
gl("Trift", ["Triften", "Triftbann"], "term",
   "Recht, Vieh oder Schafe über fremde Fluren zu treiben und dort zu weiden (Triftbann, Mithutung); 1842 in Schleiz, 1836 in Lobenstein-Ebersdorf ablösbar (S. 228–229, 232).",
   "Right to drive cattle or sheep across other people's fields and graze them there (grazing servitude); redeemable from 1842 in Schleiz and 1836 in Lobenstein-Ebersdorf (pp. 228–229, 232).", search=["Trift"])
gl("Lehn", ["Lehngeld", "Lehnsherr", "Lehnpflicht", "Lehnware", "Laudemium"], "term",
   "Feudale Abgabe oder Bindung: das kleine Lehngeld bei Sterbefällen, das hohe Lehngeld (10 Procent des Werts) bei Veräußerung; Lehnsherren waren Ämter, Rittergüter, Pfarren und Kirchenkästen (S. 228–230).",
   "Feudal due or tie: the small fief fee on deaths, the high fief fee (10 per cent of the value) on sale; feudal lords were offices, manors, parsonages and church chests (pp. 228–230).", search=["Lehn"])
gl("Beete", ["Beet- und Klauensteuer", "Beetzins"], "term",
   "Alle fünf Jahre fällige bäuerliche Abgabe; die Beete ist ein nach dem Viehstand bemessener Haferzins, die Klauensteuer richtet sich nach der Kinderzahl (S. 228–229, Fußnote).",
   "Peasant due payable every five years; the Beete is an oat rent assessed by the number of livestock, the Klauensteuer depends on the number of children (pp. 228–229, footnote).", search=[r"re:\bBeete\b", r"re:Beet- und", "Klauensteuer"])
gl("Erbzins", ["Erbzinsen", "Naturalzinsen"], "term",
   "Dauernder Zins vom überlassenen Boden in Geld (zu Walpurgi und Michaeli) oder in Naturalien (oft eine alte Henne; bei Kirchen und Schulen Mehl, Brot, Eier u. a.), S. 228.",
   "Perpetual rent for land granted, in money (at Walpurgis and Michaelmas) or in kind (often an old hen; for churches and schools flour, bread, eggs etc.), p. 228.", search=["Erbzins", "Naturalzins"])
gl("Decem", ["Zehnt", "Rauchzehnt", "Sackzehnt", "Zehnten"], "term",
   "Zehntabgabe in zwei Formen, Rauchzehnt und Sackzehnt; 1864 konnte der Rauchzehnt in eine feste Körnerabgabe verwandelt werden (S. 228–229).",
   "Tithe in two forms, smoke tithe (Rauchzehnt) and sack tithe (Sackzehnt); in 1864 the smoke tithe could be converted into a fixed grain levy (pp. 228–229).", search=[r"re:\bDecem\b", "Rauchzehnt", "Sackzehnt", "Kirchzehnt"])
gl("Landrentenbank", [], "institution",
   "Nach dem Ablösungsgesetz von 1858 errichtete Bank, die Ablösungsrenten übernahm und mit Zinsen und Zinseszinsen zu 3 1/2 Procent in 61 Jahren tilgte (S. 229).",
   "Bank established under the redemption law of 1858 that took over redemption rents and repaid them in 61 years at 3 1/2 per cent interest and compound interest (p. 229).")
gl("Ablösung", ["Ablösungsrente", "Frohnablösung", "Lehnsablösung"], "term",
   "Beseitigung der bäuerlichen Feudallasten gegen Rente oder Kapitalzahlung (20- bis 25faches der Rente), im Fürstenthum seit 1836 gesetzlich geregelt (S. 228–230).",
   "Abolition of peasant feudal burdens against a rent or capital payment (20 to 25 times the rent), regulated by law in the principality since 1836 (pp. 228–230).", search=["Ablösung"])
gl("Pflege", ["Pflege Reichenfels", "Pflege Saalburg", "reichenfelser Pflege"], "term",
   "Historischer Verwaltungsbezirk: die Pflegen Reichenfels und Saalburg bilden mit der Herrschaft Schleiz den Landestheil Schleiz (Waldstatistik S. 240; Reichenfels als Webergebiet S. 208).",
   "Historical administrative district: the Pflegen Reichenfels and Saalburg together with the Herrschaft Schleiz form the district of Schleiz (forest statistics p. 240; Reichenfels as a weaving area p. 208).", search=[r"re:Pfl\. (Reichenfels|Saalburg)", r"re:Pflege (Reichenfels|Saalburg)", r"re:reichenfelser Pflege"])
gl("Arbeitsthiere", ["Arbeitstiere", "Zugthiere"], "term",
   "Zur Arbeit herangezogene Tiere (Pferde, Ochsen, Kühe); die Zählung von 1867 erfasst sie erstmals (S. 235).",
   "Animals used for work (horses, oxen, cows); the count of 1867 records them for the first time (p. 235).", search=["Arbeitsthier"])
gl("Wallach", ["Wallachen", "Stute", "Hengst"], "term",
   "Kastrierter Hengst; die Zählung 1867 unterscheidet Stuten, Hengste und Wallachen (S. 235).",
   "Gelding; the count of 1867 distinguishes mares, stallions and geldings (p. 235).", search=["Wallach"])
gl("Dzierzonstock", ["Dzierzonstöcke", "Magazinstock", "Ganzstock", "Ganzstöcke"], "term",
   "Bienenwohnung: der alte Ganzstock (ungeteilter Stock) ist landüblich, Magazin- und Dzierzonstöcke (Beuten mit beweglichen Waben) finden zunehmend Eingang (S. 235).",
   "Bee dwelling: the old log hive (undivided) is customary, magazine and Dzierzon hives (hives with movable combs) are increasingly adopted (p. 235).", search=["Dzierzon", "Ganzstöcke"])
gl("Flößerei", ["Flöße", "Flößen", "Floß"], "term",
   "Holztransport auf Wasserläufen (Saale, Rodach, Moschwitz, Kettel, Sormitz, Elster); urkundlich seit dem 13. Jahrhundert (Urkunde 1258, S. 236). Auf Saale und Rodach wurden Stamm-, Bloch- und Klafterholz, auf kleinen Flüssen nur Klafterholz geflößt.",
   "Transport of timber on watercourses (Saale, Rodach, Moschwitz, Kettel, Sormitz, Elster); documented since the 13th century (deed of 1258, p. 236). On the Saale and Rodach logs, blocks and cordwood were rafted, on smaller rivers only cordwood.", search=["Flöße", "Flößen"])
gl("Wäldner", ["Holzhändler"], "dialect",
   "Im Oberland Bezeichnung für Holzhändler, die im Wald selbst Stämme anwiesen bekamen und aufarbeiteten (im Lobensteiner Gebiet aus Grumbach, Titschendorf und Nordhalben, S. 238).",
   "Upper Land term for timber merchants who were allotted trees in the forest and processed them themselves (in the Lobenstein area from Grumbach, Titschendorf and Nordhalben, p. 238).", search=["Wäldner"])
gl("Plentern", ["Pläntern", "Plenterhieb", "Kahlhieb"], "term",
   "Rohes Plentern = ungeregelter Einzelstammhieb, später teilweise Kahlhieb (flächiger Einschlag); frühere Form der Holzgewinnung (S. 238).",
   "Rough selective felling = unregulated felling of individual trees, later partly clear felling; earlier form of timber extraction (p. 238).", search=["Pläntern", "Kahlhieb"])
gl("Waldservitut", ["Waldservituten", "Servitute", "Leseholz"], "term",
   "Nutzungsrechte Dritter im Wald (Harzgewinnung, Viehtrieb, Streubezug, Gras- und Moosnutzung); die forstliche Reform beschränkte oder löste sie ab (S. 237–239); Leseholzholen blieb für Arme zugelassen.",
   "Rights of third parties in the forest (resin tapping, grazing, litter raking, grass and moss use); the forestry reform restricted or redeemed them (pp. 237–239); gathering of fallen wood remained permitted for the poor.", search=["Servitut", "Leseholz"])
gl("Windbruch", ["Schneedruck", "Duftbruch", "Eisdruck", "Duft"], "term",
   "Waldschäden durch Sturm (Windbruch), Schnee, Duft (Raureif) und Eis; Brückner nennt die Jahre 1819, 1821/22, 1833/34, 1846/47, 1860 und 1868/69 (S. 237).",
   "Forest damage caused by storm (windbreak), snow, hoarfrost and ice; Brückner names the years 1819, 1821/22, 1833/34, 1846/47, 1860 and 1868/69 (p. 237).", search=["Windbruch", "Windbrüche", "Schneedruck", "Duftbruch"])
gl("Nonne", ["Borkenkäfer"], "term",
   "Forstschädlinge: Nonne (Schmetterling, Raupenfraß an Fichten) und Borkenkäfer; 1795 verwüsteten sie nacheinander die schleizer und lobenstein-ebersdorfer Wälder (S. 237).",
   "Forest pests: the nun moth (caterpillar damage to spruce) and the bark beetle; in 1795 they devastated in succession the woods of Schleiz and Lobenstein-Ebersdorf (p. 237).", search=[r"re:\bNonne\b", "Borkenkäfer"])
gl("Kammerforste", ["Kammerforst", "Domainenwald", "Domanialwald", "Domanialholz"], "term",
   "Staatlich-landesherrliche Forsten (Domänenwald); 63 767 Morgen, fast die Hälfte der Waldfläche (S. 240–241).",
   "State forests of the ruling house (domain forest); 63,767 Morgen, almost half of the forest area (pp. 240–241).", search=["Kammerforste", "Domainenwald", "Domanialforste", "Domainenforst", "Domanialholz"])
gl("Forstdirection", ["Forstinspection", "Forstmeister", "Oberforstmeister", "Revierförster"], "office",
   "Forstbehörden: seit Ende 1868 eine Forstdirection in Schleiz (Oberforstmeister, Forstrath, Forstsecretär) mit der Forstinspection Ebersdorf; 26 Revierförster, 4 Forstadjuncten, 13 Forstgehilfen und 30 Forstwärter (S. 239).",
   "Forestry authorities: since the end of 1868 a forestry directorate in Schleiz (chief forester, forestry councillor, secretary) with the forestry inspection at Ebersdorf; 26 district foresters, 4 forest adjuncts, 13 forest assistants and 30 forest wardens (p. 239).", search=["Forstdirection", "Forstinspection", "Revierförster"])
gl("Waldordnung", ["Waldordnungen"], "term",
   "Forstgesetzliche Ordnung der Waldnutzung; die lobenstein-ebersdorfer Waldordnung erschien am 14. Mai 1751, die übrigen aus dem Anfang des 19. Jahrhunderts (1806, 1807, 1823), S. 238.",
   "Forest ordinance regulating forest use; the Lobenstein-Ebersdorf forest ordinance appeared on 14 May 1751, the others at the beginning of the 19th century (1806, 1807, 1823), p. 238.", search=["Waldordnung"])
gl("Bauholz", ["Blochholz", "Nutzholz", "Feuerholz", "Brennholz", "Stock- und Wurzelholz"], "term",
   "Sortimente des Holzes: Bauholz und Blochholz (Stammholz) als Nutzholz, Feuer- oder Brennholz und Stock- und Wurzelholz; Brückners Preisreihe 1800–1868 nennt Bau-, Bloch- und Feuerholz (S. 241).",
   "Assortments of wood: construction timber and log timber (stem wood) as timber for use, firewood and stump and root wood; Brückner's price series 1800–1868 gives construction, log and firewood (p. 241).", search=["Bauholz", "Blochholz", "Nutzholz", "Feuerholz", "Brennholz"])
gl("Gemeinde", [], "term", "", "")
GL.pop()  # not needed

def add_pages(term, extra):
    for g in GL:
        if g['term'] == term:
            g['pages'] = sorted(set(g['pages']) | set(extra), key=int)


add_pages("Kammergut", ["219", "221"])
add_pages("Rittergut", ["221", "223"])
add_pages("Wallach", ["235"])
add_pages("Hutung", ["218", "219", "220"])

out = {"package": "A09", "pages": [P[p] for p in PAGES], "glossary": GL}
(ROOT / "data" / "search" / "pages").mkdir(parents=True, exist_ok=True)
(ROOT / "data" / "search" / "pages" / "A09.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for g in GL:
    print(f"{g['term']:26s} {g['pages']}")
