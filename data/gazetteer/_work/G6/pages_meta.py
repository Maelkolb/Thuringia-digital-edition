# -*- coding: utf-8 -*-
"""G6 search metadata, pages 765-825 (page entries)."""

PAGES = []


def P(page, de, en, kde, ken, subj):
    PAGES.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})


P("765",
  "Schluss des Gahma-Artikels (Flur von 2501 Morgen, Flurnamen, sorbischer Ursprung, Silberbergwerk, Brand, Lehen) und Beginn von Weitisberga, einem zweiherrigen schwarzburgisch-reußischen Kirchdorf mit zwei Rittergütern, gemeinsamer Kirche, Reformation 1528 und Filialverhältnis zu Heberndorf.",
  "End of the Gahma article (2501 Morgen of land, field names, Sorbian origin, silver mine, fire, fiefs) and start of Weitisberga, a village shared between Schwarzburg and Reuss with two manors, a common church, the Reformation of 1528 and a filial relationship to Heberndorf.",
  ["Gahma", "Weitisberga", "Schwarzburg", "Heberndorf", "Rittergut", "Silberbergwerk", "Kirche", "Flurnamen"],
  ["Gahma", "Weitisberga", "Schwarzburg", "Heberndorf", "manor", "silver mine", "church", "field names"],
  ["Dorf", "Rittergut", "Sorben", "Kirche"])

P("766",
  "Weitisberga: Schule mit 56 Kindern, reußischer Anteil mit 36 Häusern und 265 Einwohnern, Gewerbe, strittige Flur (2148 Morgen), Köchermühle, sorbische Spuren am Hünenberg. Beginn des Artikels Wurzbach, des zweitgrößten Ortes im Landrathsbezirk Ebersdorf.",
  "Weitisberga: school with 56 children, the Reuss part with 36 houses and 265 inhabitants, trades, disputed land area (2148 Morgen), Köchermühle, Sorbian traces at the Hünenberg. Start of the Wurzbach article, the second largest place in the Ebersdorf district.",
  ["Weitisberga", "Hünenberg", "Köchermühle", "Schule", "Gemeindefinanzen", "Wurzbach", "Marktflecken", "Sorben"],
  ["Weitisberga", "Hünenberg", "Köchermühle", "school", "municipal finances", "Wurzbach", "market town", "Sorbs"],
  ["Dorf", "Schule", "Sorben", "Gemeindefinanzen"])

P("767",
  "Wurzbach: 236 Privathäuser, Hauptort an Thal- und Kirchbergschenkel, Rittergut der v. Watzdorf (bis 1750), Kirchengeschichte mit den Bränden von 1686 und 1757 und dem Neubau von 1763, Pfarrei und Orgel.",
  "Wurzbach: 236 private houses, main village on a valley and a church-hill branch, manor of the v. Watzdorf (until 1750), church history with the fires of 1686 and 1757 and the new building of 1763, rectory and organ.",
  ["Wurzbach", "Marktflecken", "Sormitz", "Watzdorf", "Rittergut", "Kirche", "Brand", "Pfarrer"],
  ["Wurzbach", "market town", "Sormitz", "Watzdorf", "manor", "church", "fire", "pastor"],
  ["Dorf", "Kirche", "Brände", "Rittergut"])

P("768",
  "Wurzbach: Pfarrer, Knaben- und Mädchenschule (345 Kinder), Gasthöfe, Mühlen, Märkte, Gemeindeschulden von 6857 Thlr., Bauerngüter und eine lange Aufzählung der Handwerker (u. a. 60 Schieferdecker, 41 Maurer, 21 Hüttenleute).",
  "Wurzbach: pastors, boys' and girls' schools (345 children), inns, mills, markets, municipal debts of 6857 Thlr., farms and a long list of trades (among them 60 slaters, 41 masons, 21 ironworkers).",
  ["Wurzbach", "Schule", "Schieferdecker", "Maurer", "Hüttenleute", "Mühlen", "Jahrmarkt", "Gemeindeschulden"],
  ["Wurzbach", "school", "slaters", "masons", "ironworkers", "mills", "fair", "municipal debt"],
  ["Schule", "Handwerk", "Gemeindefinanzen", "Märkte"])

P("769",
  "Wurzbach: Flur von 3505 3/5 Morgen mit Flurnamen, Herkunft des Ortsnamens, Folgen des Dreißigjährigen Krieges, Brände 1686 und 1757, Persönlichkeiten. Die Bestandtheile Oesterreich (18 Häuser) und Solmsgrün (früher Hammerwerk).",
  "Wurzbach: 3505 3/5 Morgen of land with field names, origin of the place name, effects of the Thirty Years' War, fires of 1686 and 1757, notable people. The dependencies Oesterreich (18 houses) and Solmsgrün (formerly a hammer works).",
  ["Wurzbach", "Flurnamen", "Ortsname", "Dreißigjähriger Krieg", "Brand", "Oesterreich", "Solmsgrün", "Hammerwerk"],
  ["Wurzbach", "field names", "place name", "Thirty Years' War", "fire", "Oesterreich", "Solmsgrün", "hammer works"],
  ["Flurnamen", "Ortsname", "Brände", "Hüttenwesen und Hammerwerke"])

P("770",
  "Eisenwerke und Wohnplätze bei Wurzbach: Heinrichshütte (gegründet 1729), Benignengrün, Haßlersberg, Pulvermühle (1858 explodiert). Beginn von Oßla, Kirch- und Grenzdorf mit 88 Privathäusern und 532 Einwohnern, Rittergut und Besitzgeschichte.",
  "Ironworks and hamlets near Wurzbach: Heinrichshütte (founded 1729), Benignengrün, Haßlersberg, Pulvermühle (blown up in 1858). Start of Oßla, a parish and border village with 88 private houses and 532 inhabitants, its manor and ownership history.",
  ["Heinrichshütte", "Benignengrün", "Haßlersberg", "Pulvermühle", "Eisenwerk", "Oßla", "Grenzdorf", "Rittergut"],
  ["Heinrichshütte", "Benignengrün", "Haßlersberg", "powder mill", "ironworks", "Oßla", "border village", "manor"],
  ["Hüttenwesen und Hammerwerke", "Dorf", "Rittergut", "Mühlen"])

P("771",
  "Oßla: Kirchengeschichte (Vicarie 1497, Reformation 1543, Brände 1718 und 1800, jetzige Kirche 1803), Pfarr- und Schulhaus, 61 Schulkinder, Mühlen, Gemeindefinanzen, 38 Bauerngüter. Fußnoten zur kirchlichen Zugehörigkeit (Erfurt oder Bamberg).",
  "Oßla: church history (vicarage 1497, Reformation 1543, fires of 1718 and 1800, present church 1803), rectory and school building, 61 pupils, mills, municipal finances, 38 farms. Footnotes on ecclesiastical affiliation (Erfurt or Bamberg).",
  ["Oßla", "Kirche", "Reformation", "Pfarrhaus", "Schule", "Knauermühle", "Gemeinde", "Bauerngüter"],
  ["Oßla", "church", "Reformation", "rectory", "school", "Knauermühle", "municipality", "farms"],
  ["Kirche", "Pfarreien", "Schule", "Gemeinden"])

P("772",
  "Oßla: Handwerker (57 Schieferdecker, 19 Maurer), Mundart mit dem Lieblingswort „olzig“, Flur von 2853 2/5 Morgen mit Flurnamen, sorbischer Ursprung, Brände 1718 und 1800; Altes Feld. Beginn von Röttersdorf, dem westlichsten Ort des Landrathsbezirks.",
  "Oßla: trades (57 slaters, 19 masons), dialect with the favourite word “olzig”, 2853 2/5 Morgen of land with field names, Sorbian origin, fires of 1718 and 1800; Altes Feld. Start of Röttersdorf, the westernmost place of the district.",
  ["Oßla", "Schieferdecker", "Mundart", "olzig", "Flurnamen", "Brand", "Altes Feld", "Röttersdorf"],
  ["Oßla", "slaters", "dialect", "olzig", "field names", "fire", "Altes Feld", "Röttersdorf"],
  ["Mundart", "Handwerk", "Flurnamen", "Brände"])

P("773",
  "Röttersdorf (44 Privathäuser, 276 Einwohner, Schule mit 42 Kindern, Flur von 921 Morgen, früheres Rittergut) und Dürrenbach, 1869 aus Dürrenbach, Pröstrich, Heinrichsort und Schweinshüter gebildet; das Dorf Dürrenbach zählt 17 Häuser und 124 Einwohner.",
  "Röttersdorf (44 private houses, 276 inhabitants, school with 42 children, 921 Morgen of land, former manor) and Dürrenbach, formed in 1869 from Dürrenbach, Pröstrich, Heinrichsort and Schweinshüter; the village of Dürrenbach has 17 houses and 124 inhabitants.",
  ["Röttersdorf", "Dürrenbach", "Heinrichsort", "Gemeinde 1869", "Schule", "Schieferdecker", "Kohlhauhäuser", "Rittergut"],
  ["Röttersdorf", "Dürrenbach", "Heinrichsort", "municipality of 1869", "school", "slaters", "Kohlhauhäuser", "manor"],
  ["Dorf", "Schule", "Gemeinden", "Gemeindefinanzen"])

P("774",
  "Pröstrich und Schweinshüter als Teile der Gemeinde Dürrenbach; Erörterung des 1276/1278 genannten Ortes Swinshut des Klosters Langheim. Beginn von Grumbach, dem höchsten Dörflein des Landes (1800 Fuß), 1616 von Glasmeistern gegründet.",
  "Pröstrich and Schweinshüter as parts of the municipality of Dürrenbach; discussion of the place Swinshut of Langheim monastery named in 1276/1278. Start of Grumbach, the highest village of the country (1800 feet), founded in 1616 by glassmakers.",
  ["Pröstrich", "Schweinshüter", "Swinshut", "Kloster Langheim", "Grumbach", "Glashütte", "Glasmeister", "Frankenwald"],
  ["Pröstrich", "Schweinshüter", "Swinshut", "Langheim monastery", "Grumbach", "glassworks", "glassmakers", "Franconian Forest"],
  ["Dorf", "Urkunden", "Klöster", "Industrie"])

P("775",
  "Grumbach: Schule, Gemeinde (15 Bauern, 33 Häusler, 37 Schieferdecker), Flur von 1038 1/15 Morgen, J. Nic. Wildt; das Lustschloss Karolinengrün und die Mühlen. Beginn des Absatzes über Rodacherbrunn, Waldort auf 1800 Fuß an der Rodachquelle.",
  "Grumbach: school, municipality (15 farmers, 33 cottagers, 37 slaters), 1038 1/15 Morgen of land, J. Nic. Wildt; the pleasure palace Karolinengrün and the mills. Start of the passage on Rodacherbrunn, a forest hamlet at 1800 feet by the source of the Rodach.",
  ["Grumbach", "Karolinengrün", "Lustschloss", "Wildt", "Schieferdecker", "Rodacherbrunn", "Rodach", "Mühlen"],
  ["Grumbach", "Karolinengrün", "pleasure palace", "Wildt", "slaters", "Rodacherbrunn", "Rodach", "mills"],
  ["Dorf", "Burgen und Schlösser", "Berufe", "Gemeindefinanzen"])

P("776",
  "Rodacherbrunn (1866: 6 Häuser, 35 Einwohner; Wirtshaus an der alten Straße; wüstes Seligenstätt) und Heinrichshöhe (1801 gegründet, 98 Einwohner). Beginn von Titschendorf, dem südlichsten Dorf und einzigen Maingebiets-Ort des Fürstenthums.",
  "Rodacherbrunn (1866: 6 houses, 35 inhabitants; inn on the old road; deserted Seligenstätt) and Heinrichshöhe (founded 1801, 98 inhabitants). Start of Titschendorf, the southernmost village and the only place of the principality in the Main drainage area.",
  ["Rodacherbrunn", "Seligenstätt", "Heinrichshöhe", "Titschendorf", "Maingebiet", "Wüstung", "Wirtshaus", "Ortsname"],
  ["Rodacherbrunn", "Seligenstätt", "Heinrichshöhe", "Titschendorf", "Main basin", "deserted settlement", "inn", "place name"],
  ["Dorf", "Wüstung", "Ortsname", "Siedlungsform"])

P("777",
  "Titschendorf: 92 Privathäuser und 466 Einwohner mit Heinrichshöhe und Rodacherbrunn; Gründung durch Glaubensflüchtlinge aus Nordhalben, erstes Haus 1620, Kirche (1778 neu), Pfarrei seit 1661, Schule seit 1650 mit 76 Kindern, Mühlen im Rodachgrund.",
  "Titschendorf: 92 private houses and 466 inhabitants with Heinrichshöhe and Rodacherbrunn; founded by religious refugees from Nordhalben, first house 1620, church (rebuilt 1778), parish since 1661, school since 1650 with 76 children, mills in the Rodach valley.",
  ["Titschendorf", "Nordhalben", "Glaubensflüchtlinge", "Kirche", "Pfarrei", "Schule", "Rodachgrund", "Mühlen"],
  ["Titschendorf", "Nordhalben", "religious refugees", "church", "parish", "school", "Rodach valley", "mills"],
  ["Kirche", "Reformation", "Schule", "Pfarreien"])

P("778",
  "Titschendorf: Berufe (45 Bauern), Flur von 1800 5/8 Morgen, Jahrmärkte, fränkische Mundart und Sagen von Zwergen und Holzfräulein. Beginn von Neundorf, Schuldorf 1 Stunde SW. von Lobenstein mit 112 Privathäusern.",
  "Titschendorf: occupations (45 farmers), 1800 5/8 Morgen of land, fairs, Franconian dialect and legends of dwarfs and wood maidens. Start of Neundorf, a school village 1 hour SW of Lobenstein with 112 private houses.",
  ["Titschendorf", "Sagen", "Holzfräulein", "Zwerge", "Mundart", "Jahrmarkt", "Neundorf", "Lobenstein"],
  ["Titschendorf", "legends", "wood maidens", "dwarfs", "dialect", "fair", "Neundorf", "Lobenstein"],
  ["Sagen", "Mundart", "Landwirtschaft", "Dorf"])

P("779",
  "Neundorf: Schule (1771 neu, 128 Kinder), 670 Einwohner (716 mit den Bestandtheilen), Viehstand, Berufe, Gemeinde, Flur von 2754 1/3 Morgen, Sage von den neun Familien, Teilung zwischen Lobenstein und Ebersdorf, Brände zwischen 1806 und 1868.",
  "Neundorf: school (rebuilt 1771, 128 children), 670 inhabitants (716 with the dependencies), livestock, occupations, municipality, 2754 1/3 Morgen of land, legend of the nine families, division between Lobenstein and Ebersdorf, fires between 1806 and 1868.",
  ["Neundorf", "Schule", "Einwohner", "Viehstand", "Handwerker", "Gemeinde", "Neun-Familien-Sage", "Brand"],
  ["Neundorf", "school", "inhabitants", "livestock", "craftsmen", "municipality", "nine families legend", "fire"],
  ["Dorf", "Schule", "Berufe", "Brände"])

P("780",
  "Bestandtheile von Neundorf: das Kammergut Heinrichsgrün, der Gasthof Hornsgrün mit der Langwassermühle, das Jagdhaus Jägersruh; Hinweis auf die wüsten Orte am Stutenkamm und Langenstein. Beginn von Lichtenbrunn, Langdorf am Ostfuß des Sieglitzbergs.",
  "Dependencies of Neundorf: the Kammergut Heinrichsgrün, the inn Hornsgrün with the Langwassermühle, the hunting lodge Jägersruh; mention of the deserted places at the Stutenkamm and Langenstein. Start of Lichtenbrunn, a long village at the east foot of the Sieglitzberg.",
  ["Heinrichsgrün", "Hornsgrün", "Langwassermühle", "Jägersruh", "Langenstein", "Kammergut", "Jagdhaus", "Lichtenbrunn"],
  ["Heinrichsgrün", "Hornsgrün", "Langwassermühle", "Jägersruh", "Langenstein", "Kammergut", "hunting lodge", "Lichtenbrunn"],
  ["Kammergut", "Wüstung", "Gasthof", "Dorf"])

P("781",
  "Lichtenbrunn: 71 Privathäuser, 469 Einwohner, Schule mit 100 Kindern, Gemeindefinanzen, Berufe (20 Maurer, 18 Zimmerleute auswärts), Flur von 2152 1/2 Morgen, sorbischer Ursprung, früheres Rittergut und der von Superintendent Körber verfasste immerwährende Kalender.",
  "Lichtenbrunn: 71 private houses, 469 inhabitants, school with 100 children, municipal finances, occupations (20 masons, 18 carpenters working elsewhere), 2152 1/2 Morgen of land, Sorbian origin, former manor and the perpetual calendar written by Superintendent Körber.",
  ["Lichtenbrunn", "Schule", "Maurer", "Zimmerleute", "Flur", "Rittergut", "Körber", "Kalender"],
  ["Lichtenbrunn", "school", "masons", "carpenters", "land area", "manor", "Körber", "calendar"],
  ["Dorf", "Schule", "Berufe", "Ortsname"])

P("782",
  "Schluss von Lichtenbrunn (Gerichte, Lehen) und Schlegel: Grenzdorf am Kulm mit 50 Privathäusern und 335 Einwohnern, Schule seit 1856 (57 Kinder), Vorwerk, Gemeinde, Flur von 1496 5/6 Morgen, Brand von 1802 und Bemerkung zum Rennstieg.",
  "End of Lichtenbrunn (jurisdiction, fiefs) and Schlegel: a border village at the Kulm with 50 private houses and 335 inhabitants, school since 1856 (57 children), Vorwerk, municipality, 1496 5/6 Morgen of land, fire of 1802 and a remark on the Rennstieg.",
  ["Schlegel", "Kulm", "Grenzdorf", "Schule", "Vorwerk", "Brand 1802", "Rennstieg", "Lichtenbrunn"],
  ["Schlegel", "Kulm", "border village", "school", "Vorwerk", "fire of 1802", "Rennstieg", "Lichtenbrunn"],
  ["Dorf", "Schule", "Landwirtschaft", "Brände"])

P("783",
  "Seibis: kleines Grenzdorf mit 33 Privathäusern und 189 Einwohnern, Schule seit 1860 (37 Kinder), Berufe, Flur von 1243 5/6 Morgen, Maienfest, Mord an Wolf Heinrich v. Reitzenstein 1588, Bergwerk Marienzeche (1804). Beginn von Blankenstein.",
  "Seibis: small border village with 33 private houses and 189 inhabitants, school since 1860 (37 children), occupations, 1243 5/6 Morgen of land, May festival, murder of Wolf Heinrich v. Reitzenstein in 1588, Marienzeche mine (1804). Start of Blankenstein.",
  ["Seibis", "Maienfest", "Marienzeche", "Bergwerk", "Schule", "Reitzenstein", "Grenzdorf", "Blankenstein"],
  ["Seibis", "May festival", "Marienzeche", "mine", "school", "Reitzenstein", "border village", "Blankenstein"],
  ["Dorf", "Feste", "Bergbau", "Schule"])

P("784",
  "Blankenstein: 19 Privathäuser, 167 Einwohner, Rittergut mit Besitzerfolge, Hammerwerk (1606, 1801–1827), Baumwollspinnerei (1829, 1866 abgebrannt), Schule seit 1809 (29 Kinder), Berufe (10 Weber).",
  "Blankenstein: 19 private houses, 167 inhabitants, manor with its succession of owners, hammer works (1606, 1801–1827), cotton spinning mill (1829, burned in 1866), school since 1809 (29 children), occupations (10 weavers).",
  ["Blankenstein", "Rittergut", "Hammerwerk", "Baumwollspinnerei", "Selbitz", "Saale", "Weber", "Schule"],
  ["Blankenstein", "manor", "hammer works", "cotton spinning mill", "Selbitz", "Saale", "weavers", "school"],
  ["Rittergut", "Hüttenwesen und Hammerwerke", "Textilgewerbe", "Dorf"])

P("785",
  "Blankenstein: Flur von 186 1/9 Morgen, Selbitzbrücke, Eichenstein jetzt bayerisch. Kießling als politische Gemeinde mit Einzelgruppen (31 Häuser, 190 Einwohner, Flur von 1876 1/15 Morgen, 463 Schafe) und das Dörfchen Kießling selbst.",
  "Blankenstein: 186 1/9 Morgen of land, Selbitz bridge, Eichenstein now Bavarian. Kießling as a political municipality with scattered groups (31 houses, 190 inhabitants, 1876 1/15 Morgen of land, 463 sheep) and the hamlet of Kießling itself.",
  ["Blankenstein", "Selbitzbrücke", "Eichenstein", "Kießling", "Gemeinde", "Schafe", "Flur", "Tummelplatz"],
  ["Blankenstein", "Selbitz bridge", "Eichenstein", "Kießling", "municipality", "sheep", "land area", "Tummelplatz"],
  ["Dorf", "Gemeinden", "Rittergut", "Flurnamen"])

P("786",
  "Kießling: Dorf mit Forsthaus und Vorwerk, Einzelgruppen Absang, Bärwinkel, Wegnersbach, Knopfhütte, Buttermühle (Alaunwerk 1747–1769) und die Kupferhammer-Wüstung Platte. Beginn von Harra: Lage, 97 Privathäuser, 814 Einwohner, Viehstand, Kammergut.",
  "Kießling: village with forester's house and Vorwerk, outlying groups Absang, Bärwinkel, Wegnersbach, Knopfhütte, Buttermühle (alum works 1747–1769) and the deserted copper hammer Platte. Start of Harra: location, 97 private houses, 814 inhabitants, livestock, Kammergut.",
  ["Kießling", "Absang", "Buttermühle", "Knopfhütte", "Platte", "Kupferhammer", "Harra", "Kammergut"],
  ["Kießling", "Absang", "Buttermühle", "Knopfhütte", "Platte", "copper hammer", "Harra", "Kammergut"],
  ["Dorf", "Siedlungsform", "Mühlen", "Hüttenwesen und Hammerwerke"])

P("787",
  "Harra: Besitzgeschichte des Rittergutes (v. Harra, v. Blankenberg, v. Reitzenstein, v. Watzdorf, 1700 Eleonore Sophie, 1712 Gleichen und Hatzfeld) und Beschreibung der Kirche mit Altarschrein, Glocken und Denkmälern (Wolf Heinrich v. Reitzenstein, krügersches Denkmal von 1629).",
  "Harra: ownership history of the manor (v. Harra, v. Blankenberg, v. Reitzenstein, v. Watzdorf, 1700 Eleonore Sophie, 1712 Gleichen and Hatzfeld) and description of the church with altar shrine, bells and monuments (Wolf Heinrich v. Reitzenstein, the Krüger monument of 1629).",
  ["Harra", "Rittergut", "Blankenberg", "Reitzenstein", "Watzdorf", "Kammergut", "Kirche", "Denkmal"],
  ["Harra", "manor", "Blankenberg", "Reitzenstein", "Watzdorf", "Kammergut", "church", "monument"],
  ["Rittergut", "Kammergut", "Kirchengebäude", "Denkmal"])

P("788",
  "Harra: Kirchengemeinde mit rund 2300 Seelen, Pfarrer, Pfarrhaus, Schule (177 Kinder, zweiter Lehrer 1859), Gemeindefinanzen, Bauerngüter und Berufe (26 Weber, 19 Maurer), wirtschaftliche und sittliche Lage.",
  "Harra: parish with about 2300 souls, pastors, rectory, school (177 children, second teacher in 1859), municipal finances, farms and occupations (26 weavers, 19 masons), economic and moral conditions.",
  ["Harra", "Kirchengemeinde", "Pfarrer", "Schule", "Weber", "Maurer", "Gemeindefinanzen", "Gensd'arm"],
  ["Harra", "parish", "pastors", "school", "weavers", "masons", "municipal finances", "gendarme"],
  ["Kirche", "Pfarreien", "Schule", "Berufe"])

P("789",
  "Harra: Flur von 3708 1/2 Morgen, Lehen, Bauernaufruhr 1525, Pest, Dreißigjähriger Krieg, Brände 1643, 1808 und 1869, die „harraer Schlacht“ von 1826, Persönlichkeiten, sorbischer Anbau (Altenstadt) und Sagen (Todtenfels, Zwirbelfels).",
  "Harra: 3708 1/2 Morgen of land, fiefs, Peasants' War of 1525, plague, Thirty Years' War, fires of 1643, 1808 and 1869, the “Battle of Harra” of 1826, notable people, Sorbian settlement (Altenstadt) and legends (Todtenfels, Zwirbelfels).",
  ["Harra", "Bauernaufruhr 1525", "harraer Schlacht", "Pest", "Brand", "Altenstadt", "Todtenfels", "Sagen"],
  ["Harra", "Peasants' War 1525", "Battle of Harra", "plague", "fire", "Altenstadt", "Todtenfels", "legends"],
  ["Sagen", "Brände", "Sorben", "Seuchen"])

P("790",
  "Harra: Kupferplatte und Bestandtheile (Saalmühle, Geheeg, Staudenwiese, Sieglitzmühle, Lemnitzhammer mit Spinnerei und Weberei, Haus am Wald). Beginn von Langgrün: Kirch-, Schul- und Marktort mit 67 Privathäusern und 396 Einwohnern.",
  "Harra: Kupferplatte and dependencies (Saalmühle, Geheeg, Staudenwiese, Sieglitzmühle, Lemnitzhammer with spinning and weaving mill, Haus am Wald). Start of Langgrün: a church, school and market village with 67 private houses and 396 inhabitants.",
  ["Harra", "Lemnitzhammer", "Saalmühle", "Sieglitzmühle", "Staudenwiese", "Geheeg", "Spinnerei", "Langgrün"],
  ["Harra", "Lemnitzhammer", "Saalmühle", "Sieglitzmühle", "Staudenwiese", "Geheeg", "spinning mill", "Langgrün"],
  ["Mühlen", "Hüttenwesen und Hammerwerke", "Textilgewerbe", "Dorf"])

P("791",
  "Langgrün: Meierhof, Mooshäuser und Nackte Henne; neue Kirche von 1801 als Filial von Seubtendorf, Schule (91 Kinder), Gemeindebesitz, 30 Bauern, Brauerei und Jahrmarkt, Flur von 2653 5/9 Morgen mit 32 Teichen, Zusammenhang mit Niedergrün.",
  "Langgrün: Meierhof, Mooshäuser and Nackte Henne; new church of 1801 as a filial of Seubtendorf, school (91 children), municipal property, 30 farmers, brewery and fair, 2653 5/9 Morgen of land with 32 ponds, link with Niedergrün.",
  ["Langgrün", "Kirche", "Seubtendorf", "Schule", "Brauerei", "Jahrmarkt", "Teiche", "Niedergrün"],
  ["Langgrün", "church", "Seubtendorf", "school", "brewery", "fair", "ponds", "Niedergrün"],
  ["Kirche", "Schule", "Gemeinden", "Dorf"])

P("792",
  "Langgrün: Ortsname, Gerichts- und Lehensverhältnisse, Vorwerke, Brand von 1798 (30 Gehöfte). Das Vorwerk Niedergrün (zur Gemeinde Künsdorf). Beginn von Blintendorf, preußisch-reußischem Kirchdorf, Filial von Gefell.",
  "Langgrün: place name, jurisdiction and fiefs, Vorwerke, fire of 1798 (30 farmsteads). The Vorwerk Niedergrün (belonging to the municipality of Künsdorf). Start of Blintendorf, a village shared between Prussia and Reuss, a filial of Gefell.",
  ["Langgrün", "Niedergrün", "Vorwerk", "Brand 1798", "Kloster Saalburg", "Blintendorf", "Gefell", "Ortsname"],
  ["Langgrün", "Niedergrün", "Vorwerk", "fire of 1798", "Saalburg monastery", "Blintendorf", "Gefell", "place name"],
  ["Vorwerk", "Territorialgeschichte", "Urkunden", "Brände"])

P("793",
  "Blintendorf: reußischer Anteil mit 46 Häusern und 299 Einwohnern, gemeinsame Kirche (1696) und Schule auf preußischer Seite, Staatsvertrag vom 1. Dezember 1868 mit Preußen (Abfindung 2800 Thlr.), Schule mit 90 Kindern, Reichslehen Sparnberg.",
  "Blintendorf: the Reuss part with 46 houses and 299 inhabitants, common church (1696) and school on the Prussian side, state treaty with Prussia of 1 December 1868 (compensation 2800 Thlr.), school with 90 children, imperial fief of Sparnberg.",
  ["Blintendorf", "Preußen", "Staatsvertrag 1868", "Kirche", "Schule", "Sparnberg", "Gefell", "Frössen"],
  ["Blintendorf", "Prussia", "state treaty of 1868", "church", "school", "Sparnberg", "Gefell", "Frössen"],
  ["Kirche", "Territorialgeschichte", "Schule", "Dorf"])

P("794",
  "Blintendorf: Hoheitsverhältnisse (Böhmen, Sachsen, Hohenzollern, Hirschberg), Rittergut Funkenburg und seine Besitzer, Gemeinde, Berufe, Flur. Beginn von Göttengrün: Schuldörfchen mit 17 Privathäusern und 126 Einwohnern an der Straße Hirschberg–Schleiz.",
  "Blintendorf: sovereignty (Bohemia, Saxony, Hohenzollern, Hirschberg), the manor Funkenburg and its owners, municipality, occupations, land. Start of Göttengrün: a school village with 17 private houses and 126 inhabitants on the Hirschberg–Schleiz road.",
  ["Blintendorf", "Funkenburg", "Rittergut", "Sparnberg", "Göttengrün", "Straße Hirschberg-Schleiz", "Schieferbruch", "Torf"],
  ["Blintendorf", "Funkenburg", "manor", "Sparnberg", "Göttengrün", "Hirschberg–Schleiz road", "slate quarry", "peat"],
  ["Rittergut", "Dorf", "Berufe", "Gemeinden"])

P("795",
  "Göttengrün: Pfarrzugehörigkeit zu Gefell, Schulgeschichte (Schulhaus 1866, 30 Kinder), Gemeinde, Flur von 1024 Morgen mit 40 Teichen und Torfgruben, Sage vom Dörfchen Dockendorf, Urkunden 1295 und 1368. Beginn von Frössen, Kirch-, Pfarr- und Grenzdorf.",
  "Göttengrün: parish affiliation with Gefell, school history (school building 1866, 30 children), municipality, 1024 Morgen of land with 40 ponds and peat pits, legend of the hamlet Dockendorf, charters of 1295 and 1368. Start of Frössen, a parish and border village.",
  ["Göttengrün", "Gefell", "Schule", "Torf", "Teiche", "Dockendorf", "Frössen", "Kirchsteig"],
  ["Göttengrün", "Gefell", "school", "peat", "ponds", "Dockendorf", "Frössen", "church path"],
  ["Dorf", "Schule", "Sagen", "Wüstung"])

P("796",
  "Frössen: 60 Privathäuser und 422 Einwohner, Rittergut und seine Besitzer (v. Sparnberg, v. Dobeneck, Schönfels 1675, Reuß 1703/1704, Münch 1761), Auflösung des Gutes, Gründung und Neubau der Kirche (1701) mit 1600 Thlr. Schulden.",
  "Frössen: 60 private houses and 422 inhabitants, the manor and its owners (v. Sparnberg, v. Dobeneck, Schönfels 1675, Reuss 1703/1704, Münch 1761), dissolution of the estate, founding and rebuilding of the church (1701) with 1600 Thlr. of debt.",
  ["Frössen", "Rittergut", "Dobeneck", "Schönfels", "Hohenpreis", "Kirche", "Pfarrei", "Gutszerschlagung"],
  ["Frössen", "manor", "Dobeneck", "Schönfels", "Hohenpreis", "church", "parish", "estate break-up"],
  ["Rittergut", "Kirchengebäude", "Dorf", "Territorialgeschichte"])

P("797",
  "Frössen: Kirchweih, eingepfarrte Orte (Birk, Lerchenhügel, Pottiga, Lehesten, seit 1869 Göritz und Ullersreuth), Pfarrer, Schule (87 Kinder), Gemeindefinanzen, Berufe (12 Weber für ein Faktoreigeschäft, Weißnäherei).",
  "Frössen: church consecration festival, parish villages (Birk, Lerchenhügel, Pottiga, Lehesten, since 1869 Göritz and Ullersreuth), pastors, school (87 children), municipal finances, occupations (12 weavers for a trading firm, whitework sewing).",
  ["Frössen", "Kirchweih", "Pfarrer", "Schule", "Weber", "Weißnäherei", "Gottesacker", "Eingepfarrte"],
  ["Frössen", "church fair", "pastor", "school", "weavers", "whitework sewing", "cemetery", "parish villages"],
  ["Kirche", "Pfarreien", "Schule", "Berufe"])

P("798",
  "Frössen: Flur von 1852 1/7 Morgen und Zerstörung von 1634. Hohenpreis (Rittergut, früher Stöcketen, 8 Seelen). Beginn von Lerchenhügel: junges Forstdorf mit 27 Privathäusern, 211 Einwohnern, Sitz eines Försters und Lehrers.",
  "Frössen: 1852 1/7 Morgen of land and destruction of 1634. Hohenpreis (manor, formerly Stöcketen, 8 souls). Start of Lerchenhügel: a young forest village with 27 private houses and 211 inhabitants, seat of a forester and a teacher.",
  ["Frössen", "Flur", "Hohenpreis", "Stöcketen", "Rittergut", "Lerchenhügel", "Forsthaus", "Louisengrün"],
  ["Frössen", "land area", "Hohenpreis", "Stöcketen", "manor", "Lerchenhügel", "forester's house", "Louisengrün"],
  ["Rittergut", "Dorf", "Burgen und Schlösser", "Wald"])

P("799",
  "Lerchenhügel: Entstehung aus dem Waldwärterhaus Louisengrün, Schule (1866, 67 Kinder), Berufe, Flur von 82 1/2 Morgen, Volkswort über Lerch, Pirk, Pottge und Pfütz. Beginn von Pirk: Rittergutsort mit 207 Einwohnern und den Gütern Pirk und Sachsbühl.",
  "Lerchenhügel: origin from the forest warden's house Louisengrün, school (1866, 67 children), occupations, 82 1/2 Morgen of land, a saying about Lerch, Pirk, Pottge and Pfütz. Start of Pirk: a manor village with 207 inhabitants and the estates Pirk and Sachsbühl.",
  ["Lerchenhügel", "Louisengrün", "Schule", "Pirk", "Sachsbühl", "Rittergut", "Pfütz", "Besiedlung"],
  ["Lerchenhügel", "Louisengrün", "school", "Pirk", "Sachsbühl", "manor", "Pfütz", "settlement"],
  ["Dorf", "Rittergut", "Schule", "Siedlungsform"])

P("800",
  "Pirk: Besitz der Knoch (1810, 1818), Birkenhain, Pechmühle, Gemeinde und Berufe, Flur von 751 1/9 Morgen, Ortsname, „Raubstaaten“ Pirk, Pfütz und Lerchenhügel; Pfütz. Beginn von Pottiga, Schul- und Grenzdorf an der Saale.",
  "Pirk: ownership of the Knoch family (1810, 1818), Birkenhain, Pechmühle, municipality and occupations, 751 1/9 Morgen of land, place name, the “robber states” Pirk, Pfütz and Lerchenhügel; Pfütz. Start of Pottiga, a school and border village on the Saale.",
  ["Pirk", "Pfütz", "Pechmühle", "Birkenhain", "Raubstaaten", "Knoch", "Rittergut", "Pottiga"],
  ["Pirk", "Pfütz", "Pechmühle", "Birkenhain", "robber states", "Knoch", "manor", "Pottiga"],
  ["Dorf", "Rittergut", "Kriminalität", "Gemeinden"])

P("801",
  "Pottiga: Lage, 71 Privathäuser und 463 Einwohner mit Saalbach und Arlas, Besitzerfolge des Rittergutes, Klostergut des Stifts Saalburg, wechselnde Kirchenzugehörigkeit (Gefell, Berg, Sparnberg seit 1626) und Friedhof von 1824.",
  "Pottiga: location, 71 private houses and 463 inhabitants with Saalbach and Arlas, succession of owners of the manor, monastery estate of Saalburg, changing parish affiliation (Gefell, Berg, Sparnberg since 1626) and the cemetery of 1824.",
  ["Pottiga", "Rittergut", "Klostergut", "Saalburg", "Sparnberg", "Berg", "Kirchenzugehörigkeit", "Friedhof"],
  ["Pottiga", "manor", "monastery estate", "Saalburg", "Sparnberg", "Berg", "parish affiliation", "cemetery"],
  ["Rittergut", "Klöster", "Kirche", "Territorialgeschichte"])

P("802",
  "Pottiga: Umpfarrung nach Frössen, Pfaffenscheffel, Reformation 1529, Schule (95 Kinder), Braugemeinde aus 13 Häusern, Gemeindefinanzen, Berufe (15 Maurer), Volksfeste, Flur von 2122 1/13 Morgen mit Eisen- und Kupferkiesgruben, Beginn der Flurnamen.",
  "Pottiga: reassignment to the Frössen parish, Pfaffenscheffel, Reformation of 1529, school (95 children), brewing association of 13 houses, municipal finances, occupations (15 masons), folk festivals, 2122 1/13 Morgen of land with iron and copper pyrite mines, start of the field names.",
  ["Pottiga", "Pfaffenscheffel", "Reformation", "Schule", "Braugemeinde", "Bergbau", "Flur", "Frössen"],
  ["Pottiga", "Pfaffenscheffel", "Reformation", "school", "brewing association", "mining", "land area", "Frössen"],
  ["Kirche", "Schule", "Bergbau", "Gemeindefinanzen"])

P("803",
  "Pottiga: Flurnamen, Ortsgeschichte (1325, 1633, 1745 Gräfin Benigne Marie, Brand vom 6. Juli 1869) und Sagen; Aumühle; Saalbach mit Rittergut, Lederfabrik, Brauerei, Mühle, dem früheren Hammerwerk und dem Alaunwerk Johanneszeche.",
  "Pottiga: field names, local history (1325, 1633, 1745 Countess Benigne Marie, fire of 6 July 1869) and legends; Aumühle; Saalbach with manor, leather factory, brewery, mill, the former hammer works and the alum works Johanneszeche.",
  ["Pottiga", "Aumühle", "Saalbach", "Hammerwerk", "Lederfabrik", "Alaunwerk", "Benigne Marie", "Sagen"],
  ["Pottiga", "Aumühle", "Saalbach", "hammer works", "leather factory", "alum works", "Benigne Marie", "legends"],
  ["Mühlen", "Hüttenwesen und Hammerwerke", "Brauerei", "Sagen"])

P("804",
  "Arlas: vormaliger Wallfahrtsort mit Feldkirche (Bauten 1343, 1446, 1637), kirchliche Zugehörigkeit zu Gefell, Berg und Sparnberg, Kirchweih und Jahrmarkt (1856 nach Pottiga verlegt), Verfall der Kirche seit 1826, Kupferschmelzhütte um 1550, Sagen.",
  "Arlas: former pilgrimage site with a field church (buildings 1343, 1446, 1637), parish ties to Gefell, Berg and Sparnberg, church fair and annual market (moved to Pottiga in 1856), decay of the church since 1826, copper smelter around 1550, legends.",
  ["Arlas", "Wallfahrt", "Feldkirche", "Kirchweih", "Jahrmarkt", "Sparnberg", "Berg", "Kupferschmelzhütte"],
  ["Arlas", "pilgrimage", "field church", "church fair", "annual market", "Sparnberg", "Berg", "copper smelter"],
  ["Kirche", "Religion und Frömmigkeit", "Märkte", "Kirchengebäude"])

P("805",
  "Arlas: Deutung des Namens, Sage von den dreimal gestohlenen Glocken, Glockendiebstahl um 1750. Beginn von Göritz: Schul- und Grenzdorf, 72 Privathäuser und 527 Einwohner (607 mit Lehesten), Abpfarrung von Gefell 1869, Schule (100 Kinder), Rittergut.",
  "Arlas: interpretation of the name, legend of the bells stolen three times, bell theft around 1750. Start of Göritz: a school and border village, 72 private houses and 527 inhabitants (607 with Lehesten), parish change from Gefell in 1869, school (100 children), manor.",
  ["Arlas", "Ortsname", "Glocken", "Göritz", "Lehesten", "Abpfarrung 1869", "Rittergut", "Schule"],
  ["Arlas", "place name", "bells", "Göritz", "Lehesten", "parish change 1869", "manor", "school"],
  ["Ortsname", "Sagen", "Dorf", "Kirche"])

P("806",
  "Göritz: Rechte des Rittergutes (Frohndienste, Gerichte), Gemeindefinanzen, Berufe (40 Maurer, 38 Stickerinnen), Absatz von Stickereien, Strumpfwaren, Leder und Spiritus, Flur von 1361 1/8 Morgen, sorbischer Ursprung. Beginn von Lehesten (15 Häuser, 104 Einwohner).",
  "Göritz: rights of the manor (labour dues, courts), municipal finances, occupations (40 masons, 38 embroiderers), sale of embroidery, hosiery, leather and spirits, 1361 1/8 Morgen of land, Sorbian origin. Start of Lehesten (15 houses, 104 inhabitants).",
  ["Göritz", "Rittergut", "Frohndienst", "Maurer", "Stickerei", "Strumpfwaren", "Spiritus", "Lehesten"],
  ["Göritz", "manor", "labour dues", "masons", "embroidery", "hosiery", "spirits", "Lehesten"],
  ["Rittergut", "Berufe", "Handwerk", "Gemeinden"])

P("807",
  "Lehesten: Gemeindeverband mit Göritz, Mahlmühle, früheres Pochwerk, Hochfels. Ullersreuth: 42 Privathäuser und 277 Einwohner, Kirchen- und Pfarrverhältnis zu Gefell bis 1869, Kirche von 1761 mit Orgel, Schule (44 Kinder).",
  "Lehesten: municipal union with Göritz, grist mill, former stamping mill, Hochfels. Ullersreuth: 42 private houses and 277 inhabitants, church and parish ties with Gefell until 1869, church of 1761 with organ, school (44 children).",
  ["Lehesten", "Hochfels", "Pochwerk", "Ullersreuth", "Kirche", "Pfarrei Gefell", "Schule", "Orgel"],
  ["Lehesten", "Hochfels", "stamping mill", "Ullersreuth", "church", "Gefell parish", "school", "organ"],
  ["Dorf", "Kirche", "Pfarreien", "Schule"])

P("808",
  "Ullersreuth: Gemeindebesitz, wohlhäbiges Bauerndorf (27 Bauern), Flur von 2315,36 Morgen mit Flurnamen, Lehen und Gerichte, Ursprung, Leiden im Dreißigjährigen Krieg, Blitzschläge 1759 und 1861.",
  "Ullersreuth: municipal property, well-off farming village (27 farmers), 2315.36 Morgen of land with field names, fiefs and courts, origin, suffering in the Thirty Years' War, lightning strikes of 1759 and 1861.",
  ["Ullersreuth", "Gemeinde", "Bauerndorf", "Flur", "Flurnamen", "Dreißigjähriger Krieg", "Blitz", "Hohfels"],
  ["Ullersreuth", "municipality", "farming village", "land area", "field names", "Thirty Years' War", "lightning", "Hohfels"],
  ["Gemeinden", "Landwirtschaft", "Dreißigjähriger Krieg", "Flurnamen"])

P("809",
  "Vierzeiler über Felsenwand und Ährenfelder (Signatur B.). Das Bergschloss Hirschberg: Lage über der Saale, Reichsveste, Besitzer von den Voigten von Weida (1246) und Plauen (1296) über die thüringer Landgrafen und die Krone Böhmen bis zu den v. Zedtwitz (1476).",
  "Four-line verse on rock wall and cornfields (signed B.). The hill castle of Hirschberg: setting above the Saale, imperial fortress, owners from the bailiffs of Weida (1246) and Plauen (1296) via the Thuringian landgraves and the Crown of Bohemia to the v. Zedtwitz (1476).",
  ["Hirschberg", "Bergschloss", "Reichsveste", "Voigte von Weida", "Voigte von Plauen", "Zedtwitz", "Böhmen", "Saale"],
  ["Hirschberg", "hill castle", "imperial fortress", "bailiffs of Weida", "bailiffs of Plauen", "Zedtwitz", "Bohemia", "Saale"],
  ["Burgen und Schlösser", "Territorialgeschichte", "Vögte von Weida", "Mittelalter"])

P("810",
  "Schloss und Herrschaft Hirschberg: v. Beulwitz (1480), böhmische Lehnshoheit, Haus Reuß seit 1572, Heinrich VIII. als Residenzherr (1678–1711), Synode der Brüdergemeinde unter Zinzendorf 1743, Schlossbewohner, Sage. Beginn der kirchlichen Zugehörigkeit (Naumburg, Gefell).",
  "Castle and lordship of Hirschberg: the v. Beulwitz (1480), Bohemian feudal overlordship, House of Reuss from 1572, Heinrich VIII as resident ruler (1678–1711), synod of the Moravian Brethren under Zinzendorf in 1743, castle residents, legend. Start of the ecclesiastical affiliation (Naumburg, Gefell).",
  ["Hirschberg", "Beulwitz", "Heinrich VIII.", "Zinzendorf", "Brüdergemeinde", "Residenz", "Schloss", "Naumburg"],
  ["Hirschberg", "Beulwitz", "Heinrich VIII", "Zinzendorf", "Moravian Brethren", "residence", "castle", "Naumburg"],
  ["Burgen und Schlösser", "Fürstenhaus", "Territorialgeschichte", "Religion und Frömmigkeit"])

P("811",
  "Kirchlicher Hoheitsstreit um die „Streitkirchen“ Gefell, Hirschberg, Frössen und Arlas zwischen Naumburg, Bamberg, Reuß und Brandenburg-Baireuth bis zur Abtretung des Patronats 1804. Beginn von Hirschberg, dem Landstädtchen an der Saale, Name und Lage.",
  "Dispute over ecclesiastical sovereignty regarding the “contested churches” Gefell, Hirschberg, Frössen and Arlas among Naumburg, Bamberg, Reuss and Brandenburg-Bayreuth until the cession of the patronage in 1804. Start of Hirschberg, the small town on the Saale, name and location.",
  ["Hirschberg", "Streitkirchen", "Gefell", "Brandenburg-Baireuth", "Patronat", "Naumburg", "Bamberg", "Landstädtchen"],
  ["Hirschberg", "contested churches", "Gefell", "Brandenburg-Bayreuth", "patronage", "Naumburg", "Bamberg", "small town"],
  ["Kirche", "Territorialgeschichte", "Reformation", "Stadt"])

P("812",
  "Hirschberg (Stadt): Anlage mit Saalgasse und Marktgasse, 9 öffentliche Gebäude, 166 Privathäuser, 1828 Einwohner, Viehstand, Hausbau; die Kirche nach dem Brand von 1835 (eingeweiht 1842) mit Orgel und Glocken, Vorgängerkirchen und Nicolaikapelle.",
  "Hirschberg (town): layout with Saalgasse and Marktgasse, 9 public buildings, 166 private houses, 1828 inhabitants, livestock, house types; the church after the fire of 1835 (consecrated 1842) with organ and bells, earlier churches and the St Nicholas chapel.",
  ["Hirschberg", "Saalgasse", "Marktgasse", "Einwohner", "Kirche", "Brand 1835", "Orgel", "Nicolaikapelle"],
  ["Hirschberg", "Saalgasse", "Marktgasse", "inhabitants", "church", "fire of 1835", "organ", "St Nicholas chapel"],
  ["Stadt", "Kirchengebäude", "Siedlungsform", "Bevölkerung"])

P("813",
  "Hirschberg: Stadtkirche (Privileg 1479, Neubau 1774–1776 für 9000 Mk.), Gruft der Herrn v. Beulwitz und des Grafen Heinrich VIII., Friedhof von 1621, Pfarrer, Schulwesen mit 319 Kindern und fünf Lehrern, Patronatsrechte.",
  "Hirschberg: town church (privilege 1479, rebuilt 1774–1776 for 9000 Mk.), vault of the v. Beulwitz and Count Heinrich VIII, cemetery of 1621, pastors, schooling with 319 children and five teachers, patronage rights.",
  ["Hirschberg", "Stadtkirche", "Katharinenkapelle", "Friedhof", "Pfarrer", "Schule", "Lehrer", "Patronat"],
  ["Hirschberg", "town church", "St Catherine's chapel", "cemetery", "pastors", "school", "teachers", "patronage"],
  ["Kirche", "Pfarreien", "Schule", "Stadt"])

P("814",
  "Hirschberg: Schulhaus aus dem Koch-Vermächtnis (1860, 347 Kinder), Rathaus von 1836, Stadtsiegel, Gemeindebehörde, 58 Brauberechtigte, Gemeindefinanzen (10,000 Thlr. Schulden), Märkte, Behörden, Gasthöfe und vier Mühlen.",
  "Hirschberg: school building from the Koch bequest (1860, 347 children), town hall of 1836, town seal, municipal authorities, 58 brewing-right holders, municipal finances (10,000 Thlr. of debt), markets, offices, inns and four mills.",
  ["Hirschberg", "Rathaus", "Stadtsiegel", "Altbürger", "Braugerechtigkeit", "Gemeindefinanzen", "Mühlen", "Behörden"],
  ["Hirschberg", "town hall", "town seal", "old burghers", "brewing right", "municipal finances", "mills", "offices"],
  ["Stadt", "Verwaltung", "Gemeinden", "Mühlen"])

P("815",
  "Hirschberg: Gewerbe (Färbereien, Lohgerbereien, Lederfabrik, Baumwollfabriken, Weberei und Strumpfwirkerei), Handwerkerzahlen, 40 Taglöhner und 120 Dienstboten, Armenwesen mit der Kochischen Stiftung, Sinn der Bürger, Vereine, Sparkassen und Vergnügungsorte.",
  "Hirschberg: trades (dye works, tanneries, leather factory, cotton mills, weaving and hosiery), numbers of craftsmen, 40 day labourers and 120 servants, poor relief with the Koch foundation, civic spirit, societies, savings banks and recreation spots.",
  ["Hirschberg", "Gerberei", "Färberei", "Baumwollfabrik", "Strumpfwirkerei", "Armenwesen", "Stiftung", "Sparkasse"],
  ["Hirschberg", "tanning", "dyeing", "cotton mill", "hosiery weaving", "poor relief", "foundation", "savings bank"],
  ["Handwerk", "Industrie", "Armenwesen", "Stiftungen"])

P("816",
  "Hirschberg: Cholera 1866, Flur von 1341 Morgen mit nur 479 Obstbäumen, Ortsgeschichte (Stadt Ende 14. Jahrhundert, Privileg 1479, Wenzelshöhle, Streit mit den v. Beulwitz, Richter Kästner, Dreißigjähriger Krieg).",
  "Hirschberg: cholera of 1866, 1341 Morgen of land with only 479 fruit trees, local history (town at the end of the 14th century, privilege of 1479, Wenzel's cave, dispute with the v. Beulwitz, judge Kästner, Thirty Years' War).",
  ["Hirschberg", "Cholera 1866", "Flur", "Obstbäume", "Stadtprivileg", "Wenzelshöhle", "Beulwitz", "Kästner"],
  ["Hirschberg", "cholera of 1866", "land area", "fruit trees", "town privilege", "Wenzel's cave", "Beulwitz", "Kästner"],
  ["Stadt", "Territorialgeschichte", "Urkunden", "Seuchen"])

P("817",
  "Hirschberg: Brände 1750 und 1835, der Schriftsteller Heyne, Erbgerichte, Lehen, frühere Eisenhütten und Hammermühle am Aubach. Beginn von Venzka: Schul- und Grenzdorf mit 49 Privathäusern (mit Dornholz, Juchhöh, Quire, Kegelmühle), 311 Einwohnern, pfarrt nach Gefell.",
  "Hirschberg: fires of 1750 and 1835, the writer Heyne, hereditary jurisdiction, fiefs, former ironworks and the Hammermühle on the Aubach. Start of Venzka: a school and border village with 49 private houses (with Dornholz, Juchhöh, Quire, Kegelmühle), 311 inhabitants, in the Gefell parish.",
  ["Hirschberg", "Stadtbrand 1835", "Eisenhütten", "Hammermühle", "Venzka", "Gefell", "Schule", "Rittergut"],
  ["Hirschberg", "town fire of 1835", "ironworks", "Hammermühle", "Venzka", "Gefell", "school", "manor"],
  ["Brände", "Stadt", "Dorf", "Hüttenwesen und Hammerwerke"])

P("818",
  "Venzka: Rittergut (1755 Spangenberg, dann Fürst Heinrich LXXII.), Gemeinde mit 37 3/5 Morgen, 21 Bauerngüter, Berufe, Flur von 1683 1/12 Morgen, Geschichte. Die Kegelmühle und Beginn des Absatzes über Dornholz (10 Häuser).",
  "Venzka: manor (1755 Spangenberg, then Prince Heinrich LXXII), municipality with 37 3/5 Morgen, 21 farms, occupations, 1683 1/12 Morgen of land, history. The Kegelmühle and start of the passage on Dornholz (10 houses).",
  ["Venzka", "Rittergut", "Spangenberg", "Kegelmühle", "Dornholz", "Gemeinde", "Flur", "Heinrich LXXII."],
  ["Venzka", "manor", "Spangenberg", "Kegelmühle", "Dornholz", "municipality", "land area", "Heinrich LXXII"],
  ["Dorf", "Rittergut", "Gemeindefinanzen", "Mühlen"])

P("819",
  "Fundhäuser, Juchhöh (Straßenwirtshäuser an der Hofer Straße) und Quire. Mödlareuth: bayerisch-reußisches Grenzdorf, reußischer Teil mit 16 Häusern und 94 Einwohnern, Schule seit 1864 (33 Kinder), Mühlen, Gemeinde, Rittergut der v. Beulwitz.",
  "Fundhäuser, Juchhöh (roadside inns on the Hof road) and Quire. Mödlareuth: a village divided between Bavaria and Reuss, the Reuss part with 16 houses and 94 inhabitants, school since 1864 (33 children), mills, municipality, manor of the v. Beulwitz.",
  ["Fundhäuser", "Juchhöh", "Quire", "Mödlareuth", "Grenzdorf", "Tannenbach", "Rittergut", "Schule"],
  ["Fundhäuser", "Juchhöh", "Quire", "Mödlareuth", "border village", "Tannenbach", "manor", "school"],
  ["Dorf", "Gasthof", "Gemeinden", "Schule"])

P("820",
  "Mödlareuth: Berufe, Flur von 834 11/15 Morgen, Deutung des Namens, Geschichte, Poststraße Hof–Schleiz. Beginn von Gebersreuth: Grenzdorf mit Heidefeld und Straßenreuth, 70 Privathäuser, 444 Einwohner, Grenzlage an Bayern, Sachsen und Preußen.",
  "Mödlareuth: occupations, 834 11/15 Morgen of land, interpretation of the name, history, the Hof–Schleiz post road. Start of Gebersreuth: border village with Heidefeld and Straßenreuth, 70 private houses, 444 inhabitants, bordering Bavaria, Saxony and Prussia.",
  ["Mödlareuth", "Ortsname", "Poststraße", "Gebersreuth", "Heidefeld", "Straßenreuth", "Dreiländereck", "Grenzdorf"],
  ["Mödlareuth", "place name", "post road", "Gebersreuth", "Heidefeld", "Straßenreuth", "tripoint", "border village"],
  ["Dorf", "Lage und Grenzen", "Ortsname", "Gemeinden"])

P("821",
  "Gebersreuth: Berufe (10 Weber, 9 Maurer, 24 Weißnäherinnen), Flur von 2017 7/30 Morgen mit 12 Teichen und Torfgruben; Hauptort (38 Privathäuser, 255 Einwohner), Schule (93 Kinder), Mühlbergschiefer, Torfhandel (1 1/2 Million Ziegel) und Lehen der Dobareuther Rittergüter.",
  "Gebersreuth: occupations (10 weavers, 9 masons, 24 seamstresses), 2017 7/30 Morgen of land with 12 ponds and peat pits; main village (38 private houses, 255 inhabitants), school (93 children), Mühlberg slate, peat trade (1 1/2 million bricks) and fiefs of the Dobareuth manors.",
  ["Gebersreuth", "Torf", "Schieferbruch Mühlberg", "Weißnäherinnen", "Schule", "Flur", "Dobareuth", "Weber"],
  ["Gebersreuth", "peat", "Mühlberg slate quarry", "seamstresses", "school", "land area", "Dobareuth", "weavers"],
  ["Dorf", "Schule", "Bodenschätze", "Berufe"])

P("822",
  "Gebersreuth: Lehen und Gerichte; Straßenreuth (11 Häuser, 1783 Wirtshaus) und Heidefeld (21 Häuser, 1797 erstes Haus, Ruhr 1865). Beginn von Dobareuth: Schul- und Grenzdorf bei Gefell mit 56 Privathäusern, 387 Einwohnern und Kammergut.",
  "Gebersreuth: fiefs and courts; Straßenreuth (11 houses, inn of 1783) and Heidefeld (21 houses, first house 1797, dysentery in 1865). Start of Dobareuth: a school and border village near Gefell with 56 private houses, 387 inhabitants and a Kammergut.",
  ["Gebersreuth", "Straßenreuth", "Heidefeld", "Ruhr 1865", "Dobareuth", "Gefell", "Kammergut", "Wirtshaus"],
  ["Gebersreuth", "Straßenreuth", "Heidefeld", "dysentery 1865", "Dobareuth", "Gefell", "Kammergut", "inn"],
  ["Dorf", "Ortsname", "Krankheiten", "Siedlungsform"])

P("823",
  "Dobareuth: Kammergut aus drei Rittergütern, Pfarrei Gefell, Schule seit 1852 (65 Kinder), Gemeindebesitz, Berufe (18 Maurer, 7 Weber), Flur von 1426 13/20 Morgen mit 15 Teichen, Geschichte (1416, 1479, 1482), Brand 1866; Pfauenbach.",
  "Dobareuth: Kammergut formed from three manors, Gefell parish, school since 1852 (65 children), municipal property, occupations (18 masons, 7 weavers), 1426 13/20 Morgen of land with 15 ponds, history (1416, 1479, 1482), fire of 1866; Pfauenbach.",
  ["Dobareuth", "Kammergut", "Rittergüter", "Schule", "Maurer", "Teiche", "Pfauenbach", "Beulwitz"],
  ["Dobareuth", "Kammergut", "manors", "school", "masons", "ponds", "Pfauenbach", "Beulwitz"],
  ["Kammergut", "Schule", "Gemeinden", "Dorf"])

P("824",
  "Schluss von Pfauenbach. Rothenacker: abgelegenes Schul-, Grenz- und Bauerndorf mit 41 Privathäusern und 265 Einwohnern, Pfarrei Mißlareuth, Schule seit 1840 (40 Kinder), Berufe, Flur von 1543 3/5 Morgen mit 15 Teichen, Ortsname, Erbkretschmar.",
  "End of Pfauenbach. Rothenacker: a remote school, border and farming village with 41 private houses and 265 inhabitants, Mißlareuth parish, school since 1840 (40 children), occupations, 1543 3/5 Morgen of land with 15 ponds, place name, hereditary tavern.",
  ["Pfauenbach", "Rothenacker", "Bauerndorf", "Mißlareuth", "Schule", "Flur", "Ortsname", "Erbkretschmar"],
  ["Pfauenbach", "Rothenacker", "farming village", "Mißlareuth", "school", "land area", "place name", "hereditary tavern"],
  ["Dorf", "Schule", "Landwirtschaft", "Ortsname"])

P("825",
  "Schluss von Rothenacker und der Ortskunde: Lehen und Gerichte der Hirschberger Herrschaft, der „gelehrte Bauer“ Nicol Schmidt genannt Künzel (1606–1671) mit seinem Kalender und seiner Biographie in der Fußnote, Brand des Mühlhofs 1867.",
  "End of Rothenacker and of the topographical part: fiefs and courts of the Hirschberg lordship, the “learned peasant” Nicol Schmidt called Künzel (1606–1671) with his almanac and a biographical footnote, fire at the Mühlhof in 1867.",
  ["Rothenacker", "Nicol Schmidt", "Künzel", "gelehrter Bauer", "Kalender", "Lehen", "Brand 1867", "Mißlareuth"],
  ["Rothenacker", "Nicol Schmidt", "Künzel", "learned peasant", "almanac", "fiefs", "fire of 1867", "Mißlareuth"],
  ["Dorf", "Urkunden", "Brände"])
