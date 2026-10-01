# -*- coding: utf-8 -*-
"""Build data/search/pages/G5.json (pages 706-764)."""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")

P = []  # (page, de, en, kw_de, kw_en, subjects)


def add(page, de, en, kde, ken, subj):
    P.append((page, de, en, kde, ken, subj))


add("706",
    "Einleitung zum Landestheil Lobenstein-Ebersdorf: südlichstes und höchstes Gebiet des Fürstentums, Grenzen zu Bayern, Sachsen, Schleiz, Greiz, Ziegenrück, Schwarzburg und Meiningen; äußerste Punkte Lothra, Titschendorf, Röttersdorf und Gebersreuth, tiefste Stelle im Saaltal bei Pöritzsch (1000 Fuß), höchste der Fichteberg (1925 Fuß). Vier Landschaftsformen; Fußnote zum Namen Ruthenenland (terra ruthenica, 1276).",
    "Introduction to the Lobenstein-Ebersdorf district: the principality's southernmost and highest area, bordering Bavaria, Saxony, Schleiz, Greiz, Ziegenrück, Schwarzburg and Meiningen; extreme points at Lothra, Titschendorf, Röttersdorf and Gebersreuth, lowest point in the Saale valley near Pöritzsch (1,000 feet), highest the Fichteberg (1,925 feet). Four landscape types; a footnote on the name Ruthenenland (terra ruthenica, 1276).",
    ["Landestheil Lobenstein-Ebersdorf", "Grenzen", "Frankenwald", "Saaletal", "Fichteberg", "Höhenlage", "Ruthenenland", "Sorben", "Heinrich von Gera"],
    ["Lobenstein-Ebersdorf district", "borders", "Franconian Forest", "Saale valley", "elevation", "Ruthenenland", "Sorbs"],
    ["Lage und Grenzen", "Relief", "Sorben"])

add("707",
    "Entwässerung des Landestheils (Saale; nur Titschendorf zum Main) und Bevölkerung 1867: Tabelle nach 45 Orten mit Familiengliedern, Dienstboten, Gehilfen und Altersgruppen; Summe 22.359 Einwohner (Lobenstein 2833, Wurzbach 1861, Hirschberg 1828, Ebersdorf 1008).",
    "Drainage of the district (Saale; only Titschendorf drains to the Main) and the 1867 population: a table of 45 places with family members, servants, assistants and age groups; total 22,359 inhabitants (Lobenstein 2,833, Wurzbach 1,861, Hirschberg 1,828, Ebersdorf 1,008).",
    ["Bevölkerung 1867", "Einwohnerzahlen", "Altersverhältnisse", "Dienstboten", "Saale", "Main", "Lobenstein", "Wurzbach", "Hirschberg"],
    ["population 1867", "inhabitants", "age structure", "servants", "Saale", "Main watershed", "table"],
    ["Bevölkerung", "Volkszählung", "Flüsse und Bäche"])

add("708",
    "Prozentanteile der Bevölkerung (Familienglieder 90,8 %, Dienstboten 5,6 %, Gehilfen 3,6 %; Männer 31,1 %, Frauen 35,1 %) und Tabelle der Bevölkerungsbewegung 1647, 1784, 1833 und 1867 nach Orten; 1647: 1433 Familien mit 6453 Einwohnern, 1867: 4792 Familien mit 22.359 Einwohnern.",
    "Population shares in percent (family members 90.8, servants 5.6, assistants 3.6; men 31.1, women 35.1) and a table of population change in 1647, 1784, 1833 and 1867 by place; 1647: 1,433 families with 6,453 inhabitants, 1867: 4,792 families with 22,359 inhabitants.",
    ["Bevölkerungsentwicklung", "Einwohnerzahlen 1647", "1784", "1833", "1867", "Familien", "Prozentanteile", "Tabelle"],
    ["population growth", "inhabitants 1647", "1784", "1833", "1867", "families", "percentages"],
    ["Bevölkerung", "Volkszählung"])

add("709",
    "Städtische und ländliche Bevölkerung 1647 und 1867, Bevölkerungsdichte (4470,8 Köpfe je Quadratmeile), Berufsverteilung in Prozent, Viehstand je Familie und Grundbesitz (14 Kammer- und 7 Rittergüter, 962 Bauerngüter, 1644 Kleinhäusler); Beginn der Herrschaftsgeschichte: Lobdaburg-Arnshaugk, Otto von Lobenstein 1250, Voigte von Gera 1276/1278.",
    "Urban and rural population in 1647 and 1867, population density (4,470.8 persons per square mile), occupational shares in percent, livestock per family and landholding (14 crown and 7 knightly estates, 962 farms, 1,644 cottagers); start of the lordship's history: Lobdaburg-Arnshaugk, Otto of Lobenstein 1250, advocates of Gera 1276/1278.",
    ["Bevölkerungsdichte", "Berufe", "Viehstand", "Grundbesitz", "Bauerngüter", "Kleinhäusler", "Lobdaburg-Arnshaugk", "Voigte von Gera", "Kloster Langheim"],
    ["population density", "occupations", "livestock", "landholding", "farms", "cottagers", "Lobdaburg-Arnshaugk", "advocates of Gera"],
    ["Bevölkerung", "Berufe", "Territorialgeschichte"])

add("710",
    "Herrschaftsgeschichte Lobensteins: Verpfändung 1369 und böhmische Lehnsauftragung 1371, Erbportionen der Heinriche von Gera bis 1509, Heinrich der Beharrliche (+1550) und die Reformation 1543, Übergang an Burggraf Heinrich V. von Plauen 1547, Verpfändungen 1567–1570 an Schwarzburg und die Vizthum von Eckstädt (60.000 Gülden).",
    "History of the Lobenstein lordship: pledge in 1369 and enfeoffment to Bohemia in 1371, inheritance portions of the Heinrichs of Gera until 1509, Heinrich the Persistent (d. 1550) and the Reformation in 1543, transfer to Burgrave Heinrich V of Plauen in 1547, pledges of 1567–1570 to Schwarzburg and the Vizthum von Eckstädt (60,000 gulden).",
    ["Herrschaft Lobenstein", "Heinrich von Gera", "Burggrafen von Plauen", "Verpfändung", "Vizthum von Eckstädt", "Reformation 1543", "Schlacht bei Mühlberg", "Böhmen"],
    ["lordship of Lobenstein", "Heinrich of Gera", "burgraves of Plauen", "pledge", "Vizthum von Eckstädt", "Reformation 1543", "Bohemia"],
    ["Territorialgeschichte", "Reformation", "Fürstenhaus"])

add("711",
    "Vertrag von 1576 mit den Vizthum; Ankauf der Anteile der älteren (1585) und mittleren Linie (1588) durch die jüngere Linie Reuß; Heinrich Posthumus (Münze 1620), Erbteilung 1647 und Specialhaus Lobenstein bis 1848; Regentenfolge und die 1678 gebildeten Portionen Lobenstein, Hirschberg und Ebersdorf mit ihren Dörfern und Rittergütern; Fußnoten zu Pfandschaft, Rittermannlehen und Lehenstücken.",
    "Settlement of 1576 with the Vizthum; purchase of the shares of the elder (1585) and middle line (1588) by the younger Reuss line; Heinrich Posthumus (mint 1620), partition of 1647 and the special house of Lobenstein until 1848; succession of rulers and the portions of Lobenstein, Hirschberg and Ebersdorf formed in 1678 with their villages and manors; footnotes on the pledge, knight fiefs and single fiefs.",
    ["Specialhaus Lobenstein", "Heinrich Posthumus", "Erbteilung 1647", "Teilung 1678", "Hirschberg", "Ebersdorf", "Rittergüter", "Reuß jüngere Linie", "Lehen"],
    ["special house of Lobenstein", "Heinrich Posthumus", "partition 1647", "partition 1678", "Hirschberg", "Ebersdorf", "manors", "fiefs"],
    ["Territorialgeschichte", "Fürstenhaus", "Genealogie"])

add("712",
    "Stammtafel der drei Linien des Specialhauses (Lobenstein, Hirschberg, Ebersdorf) von Heinrich III. bis Heinrich LXXII. († 1853) mit Todesjahren; Ende der Linie Lobenstein-Ebersdorf 1848. Aufteilung der Orte der Herrschaften Lobenstein und Ebersdorf nach der Teilung von 1711 mit ihren Pfarrverbänden (Beginn).",
    "Genealogical table of the three lines of the special house (Lobenstein, Hirschberg, Ebersdorf) from Heinrich III to Heinrich LXXII (d. 1853) with death years; end of the Lobenstein-Ebersdorf line in 1848. Allocation of places to the lordships of Lobenstein and Ebersdorf after the partition of 1711 with their parish groups (beginning).",
    ["Stammtafel", "Heinrich XXXV.", "Heinrich LXXII.", "Linie Ebersdorf", "Linie Hirschberg", "Teilung 1711", "Herrschaft Ebersdorf", "Pfarrverbände"],
    ["genealogical table", "Heinrich XXXV", "Heinrich LXXII", "Ebersdorf line", "Hirschberg line", "partition 1711", "parish groups"],
    ["Genealogie", "Fürstenhaus", "Territorialgeschichte"])

add("713",
    "Fortsetzung der Ortsverzeichnisse von 1711; sächsisches Recht und naumburger Kirchenaufsicht, Reformation 1543, Konsistorium Gera 1604–1863, Superintendentur 1844–1867 in Ebersdorf. Beginn des Artikels Lobenstein: Namensformen, Lage am Schlossberg, Plätze und Gassen, öffentliche Gebäude.",
    "Continuation of the 1711 place lists; Saxon law and the supervision of the Naumburg see, Reformation in 1543, consistory at Gera 1604–1863, superintendency at Ebersdorf 1844–1867. Start of the Lobenstein article: name forms, location below the Schlossberg, squares and streets, public buildings.",
    ["Lobenstein", "Kirchenaufsicht", "Konsistorium Gera", "Superintendentur", "Sächsisches Recht", "Namensformen", "Schlossberg", "Gassen", "Lemnitz"],
    ["Lobenstein", "church supervision", "consistory at Gera", "superintendency", "Saxon law", "name forms", "streets"],
    ["Stadt", "Kirche", "Ämter und Behörden", "Lage und Grenzen"])

add("714",
    "Lobenstein: Gebäudebestand (19 öffentliche, 388 Privathäuser, 1509 nur 130 Häuser), Gassen, Burg auf dem Schlossberg (Georgskapelle, Warte 96 Fuß hoch, Schweden 1632, Verfall nach dem Dreißigjährigen Krieg) und Beginn des Neubaus des Schlosses 1601.",
    "Lobenstein: building stock (19 public buildings, 388 private houses, only 130 houses in 1509), streets, the castle on the Schlossberg (chapel of St George, 96-foot watchtower, Swedes in 1632, decay after the Thirty Years' War) and the start of the new castle in 1601.",
    ["Lobenstein", "Burg Lobenstein", "Schlossberg", "Wartturm", "Georgskapelle", "Schweden 1632", "Heinrich Posthumus", "Schloss"],
    ["Lobenstein", "Lobenstein castle", "Schlossberg", "watchtower", "St George's chapel", "Swedes 1632", "Heinrich Posthumus"],
    ["Stadt", "Burgen und Schlösser", "Dreißigjähriger Krieg"])

add("715",
    "Lobenstein: Unterschloss (1610), das nach dem Brand von 1714 im Tal erbaute Schloss (Residenz bis 1824, dann Wittumssitz, Amts- und Gerichtsgebäude), Marstall als Badehaus, Palais Christianenzell; mittelalterliche Kapellen und die Stadtkirche (h. Michael) mit vier Altären, Erweiterung 1587–1612.",
    "Lobenstein: lower castle (1610), the castle in the valley built after the fire of 1714 (residence until 1824, then dower seat, later court and office building), stables as bathhouse, Palais Christianenzell; medieval chapels and the town church (St Michael) with four altars, enlarged 1587–1612.",
    ["Schloss Lobenstein", "Unterschloss", "Residenz", "Marstall", "Palais Christianenzell", "Stadtkirche", "Michaeliskirche", "Kapellen", "Brand 1714"],
    ["Lobenstein castle", "lower castle", "residence", "stables", "Palais Christianenzell", "town church", "chapels", "fire 1714"],
    ["Burgen und Schlösser", "Kirchengebäude", "Stadt"])

add("716",
    "Lobenstein: herrschaftliche Gruft, Kirchenbrände 1714, 1732 und 1862, Kirchenbibliothek (gestiftet 1632), Neubau und Weihe 1863, Orgel 1866; eingepfarrte Orte, Filiale Schönbrunn und Unterlemnitz, Kirchenvermögen und Schulden, Geistliche, Patronat; Vikare vor der Reformation.",
    "Lobenstein: princely vault, church fires of 1714, 1732 and 1862, church library (founded 1632), new church consecrated in 1863, organ of 1866; parish members, daughter churches Schönbrunn and Unterlemnitz, church assets and debts, clergy, patronage; vicars before the Reformation.",
    ["Stadtkirche Lobenstein", "Kirchenbrand 1862", "Kirchenbibliothek", "Gruft", "Orgel", "Parochie", "Filiale", "Oberpfarrer", "Pfarrer"],
    ["town church", "church fire 1862", "church library", "burial vault", "organ", "parish", "daughter churches", "pastors"],
    ["Kirchengebäude", "Pfarreien", "Brände", "Reformation"])

add("717",
    "Lobenstein: Pfarrer und Superintendenten seit der Reformation (erster lutherischer Pfarrer Gallus Ellenius), Oberpfarrei und Diaconat, Knaben- und Mädchenschule mit 509 Kindern, Fortbildungsschule 1865, Schulgeschichte bis 1733.",
    "Lobenstein: pastors and superintendents since the Reformation (first Lutheran pastor Gallus Ellenius), rectory and deacon's house, boys' and girls' schools with 509 children, continuation school 1865, school history to 1733.",
    ["Pfarrer", "Superintendent", "Gallus Ellenius", "Knabenschule", "Mädchenschule", "Fortbildungsschule", "Schulgeschichte", "Lehrer", "Reformation"],
    ["pastors", "superintendent", "Gallus Ellenius", "boys' school", "girls' school", "continuation school", "school history", "teachers"],
    ["Schule", "Pfarreien", "Reformation"])

add("718",
    "Lobenstein: Geschichte der Mädchenschule (öffentlich seit 1683), acht Schul- und Kirchenstiftungen (Albert, Werner, Schulze, Gebhardt, Maaß, Süßenguth, Rau, Gehring), Rathaus 1864/65, Hospital (Legat 1634), Armenhaus; Beginn der Übersicht der Staatsbehörden.",
    "Lobenstein: history of the girls' school (public since 1683), eight school and church endowments (Albert, Werner, Schulze, Gebhardt, Maaß, Süßenguth, Rau, Gehring), town hall 1864/65, hospital (bequest 1634), poorhouse; start of the overview of state authorities.",
    ["Mädchenschule", "Stiftungen", "Rathaus", "Hospital", "Armenhaus", "Legate", "Süßenguth", "Gehring", "Behörden"],
    ["girls' school", "endowments", "town hall", "hospital", "poorhouse", "bequests", "authorities"],
    ["Stiftungen", "Schule", "Armenwesen", "Stadt"])

add("719",
    "Lobenstein: Behörden und Gemeindeverwaltung, Gemeindevermögen (Activa 44.845, Passiva 22.000 Thlr.), Wasserleitung, Feuerlöschwesen (Feuerwehr 70 Mann), sechs Jahr- und sechs Viehmärkte, Gasthäuser, Mühlen und Tuchfabriken, Bevölkerung 1509–1867, Viehstand.",
    "Lobenstein: authorities and municipal administration, municipal assets (44,845 thalers; liabilities 22,000), water supply, fire fighting (fire brigade of 70 men), six annual fairs and six cattle markets, inns, mills and cloth factories, population 1509–1867, livestock.",
    ["Gemeindefinanzen", "Behörden", "Feuerwehr", "Jahrmärkte", "Viehmärkte", "Gasthäuser", "Mühlen", "Tuchfabriken", "Einwohnerzahl 1867"],
    ["municipal finances", "authorities", "fire brigade", "annual fairs", "cattle markets", "inns", "mills", "cloth factories"],
    ["Gemeindefinanzen", "Märkte", "Feuerwehr und Brandschutz", "Bevölkerung"])

add("720",
    "Lobenstein: Rückgang von Tuchmacherei, Wollkämmerei und Bergbau, Auswanderung; Gewerbetreibende nach Zahl (121 Tuchmacher), Sparkasse und Vorschusskasse (1864), Vereine, Schützengesellschaft (1772), Ausflugsorte; Anfang der Beschreibung des 1868 errichteten Heilbades.",
    "Lobenstein: decline of cloth-making, wool combing and mining, emigration; tradespeople by number (121 cloth makers), savings bank and loan society (1864), associations, shooting society (1772), excursion spots; start of the description of the spa founded in 1868.",
    ["Tuchmacher", "Wollkämmerei", "Auswanderung", "Gewerbe", "Sparkasse", "Vorschusskasse", "Schützengesellschaft", "Armut", "Heilbad"],
    ["cloth makers", "wool combing", "emigration", "trades", "savings bank", "loan society", "shooting society", "poverty"],
    ["Textilgewerbe", "Handwerk", "Auswanderung", "Berufe"])

add("721",
    "Lobenstein: Heilbad (Moor-, Molken-, Fichtennadel- und Dampfbäder); Stadtflur 3591 19/25 Morgen mit Flurnamen, Teichen und Eisensteingruben; Ortsname und Sagen, Stadterhebung 1371, Tore und Vorstädte, Statuten, Wappen, Gerichtsbarkeit.",
    "Lobenstein: spa (peat, whey, pine-needle and steam baths); town land of 3,591 19/25 Morgen with field names, ponds and iron-ore pits; place name and legends, town status 1371, gates and suburbs, statutes, coat of arms, jurisdiction.",
    ["Heilbad", "Kurort", "Stadtflur", "Flurnamen", "Ortsname", "Wappen", "Stadtrecht", "Statuten", "Ludwig der Bayer"],
    ["spa", "health resort", "town land", "field names", "place name", "coat of arms", "town rights", "statutes"],
    ["Mineralquellen", "Gesundheit", "Flurnamen", "Ortsname", "Stadt"])

add("722",
    "Lobenstein: Lehen und Häuserzahl 1783, Frondienste, Pfarrgericht, städtische Rechte und Wallfahrtspflicht der Amtsdörfer, Kriegsschäden, Brände 1714, 1732, 1800 und 1862; Beginn der Reihe berühmter Söhne der Stadt (Lobeck, Volkmar, Alberti, Zopf u. a.).",
    "Lobenstein: fiefs and number of houses in 1783, labour services, parish court, town rights and the pilgrimage duty of the district villages, war damage, fires of 1714, 1732, 1800 and 1862; start of the list of the town's famous sons (Lobeck, Volkmar, Alberti, Zopf and others).",
    ["Brände 1714", "1732", "1862", "Frondienste", "Wallfahrt", "Berühmte Persönlichkeiten", "Heinrich Albert", "Johann Lobeck", "Zopf"],
    ["fires 1714", "1732", "1862", "labour services", "pilgrimage", "famous natives", "Heinrich Albert", "Johann Lobeck"],
    ["Brände", "Stadt", "Rechtspflege", "Genealogie"])

add("723",
    "Lobenstein: weitere berühmte Söhne (Reichard, Hohl, Körber, Sorge), Intelligenzblatt 1784–1805, Mordfall 1869, Bracteatenfund und die Einzelhäuser der Stadtflur (Schießhaus, Galgenvorwerk/Galenberg, Herrnmühle, Kleinfriesa, Hämmerleinsmühle). Beginn des Artikels Saaldorf, eines Gemeinde- und Schulverbandes im Saaltal.",
    "Lobenstein: more famous sons (Reichard, Hohl, Körber, Sorge), the Intelligenzblatt 1784–1805, a murder case in 1869, a find of bracteates and the outlying houses of the town land (shooting lodge, Galgenvorwerk/Galenberg, Herrnmühle, Kleinfriesa, Hämmerleinsmühle). Start of the Saaldorf article, a municipal and school district in the Saale valley.",
    ["Lobenstein", "Einzelhäuser", "Galenberg", "Herrnmühle", "Kleinfriesa", "Hämmerleinsmühle", "Intelligenzblatt", "Saaldorf", "Saaltal"],
    ["Lobenstein", "outlying houses", "Galenberg", "Herrnmühle", "Kleinfriesa", "newspaper", "Saaldorf", "Saale valley"],
    ["Stadt", "Mühlen", "Kammergut", "Siedlungsform"])

add("724",
    "Saaldorf: Eisen- und Bergbauindustrie im Saaltal und ihr Niedergang ohne Eisenbahnanschluss (Spaniershammer, polnischer Hammer, Christiansglück; Gussstahlplan 1868); Gemeindebezirk mit 83 Privathäusern, 831 Einwohnern, Viehstand, Gewerben (39 Bergleute), Armut; Kirch- und Schulzugehörigkeit, Gemeindeschulden.",
    "Saaldorf: iron and mining industry in the Saale valley and its decline without a railway connection (Spaniershammer, Polish hammer, Christiansglück; cast-steel plan 1868); municipal district with 83 private houses, 831 inhabitants, livestock, trades (39 miners), poverty; church and school affiliation, municipal debts.",
    ["Saaldorf", "Eisenindustrie", "Hammerwerke", "Bergleute", "Niedergang", "Eisenbahn", "Gussstahl", "Gemeindeschulden", "Armut"],
    ["Saaldorf", "iron industry", "hammer works", "miners", "decline", "railway", "cast steel", "municipal debt"],
    ["Hüttenwesen und Hammerwerke", "Bergbau", "Gemeinden", "Gemeindefinanzen"])

add("725",
    "Saaldorf: Flur 971 17/18 Morgen und Gerichtsbarkeit; die Bestandtheile Magwitzhaus, Saalhof, Hennemannsreuth, Mühlberg, Saalgrün und Saaldorf im engeren Sinn (Köhler, Schulgeschichte, 152 Schulkinder 1866); Beginn von Haueisen (Kammergut).",
    "Saaldorf: parish land of 971 17/18 Morgen and jurisdiction; the components Magwitzhaus, Saalhof, Hennemannsreuth, Mühlberg, Saalgrün and Saaldorf proper (charcoal burners, school history, 152 pupils in 1866); start of Haueisen (crown estate).",
    ["Saaldorf", "Magwitzhaus", "Mühlberg", "Saalgrün", "Köhler", "Schulhaus", "Haueisen", "Flur", "Hennemannsreuth"],
    ["Saaldorf", "Magwitzhaus", "Mühlberg", "Saalgrün", "charcoal burners", "school building", "Haueisen", "parish land"],
    ["Gemeinden", "Schulgebäude", "Siedlungsform", "Kammergut"])

add("726",
    "Saaldorf: Kammergut Haueisen mit Besitzergeschichte (1829/1830 an den Fürsten), früheres Eisenhüttenwerk (Volkmars-Hammer) sowie Alaun- und Vitriolwerk („güldener Hirsch“, „Hoff auf Gott“, 1603 mit 40 Arbeitern); Rödelsgrün; Jagdschlösschen Weidmannsheil (1837) mit Aussichtspunkten.",
    "Saaldorf: crown estate Haueisen with its owners (taken over by the prince in 1829/1830), former ironworks (Volkmars-Hammer) and alum and vitriol works ('güldener Hirsch', 'Hoff auf Gott', 40 workers in 1603); Rödelsgrün; hunting lodge Weidmannsheil (1837) with viewpoints.",
    ["Haueisen", "Kammergut", "Alaunwerk", "Vitriolwerk", "Hammerwerk", "Weidmannsheil", "Jagdschloss", "Rödelsgrün", "Heinrich LXXII."],
    ["Haueisen", "crown estate", "alum works", "vitriol works", "hammer works", "Weidmannsheil", "hunting lodge", "Rödelsgrün"],
    ["Kammergut", "Hüttenwesen und Hammerwerke", "Bergbau", "Burgen und Schlösser"])

add("727",
    "Saaldorf: oberes und unteres Schlösschen, Rödelshammer (polnischer Hammer, 1795, seit 1846 eingegangen), Christiansglück (Alaun- und Vitriolwerk), Naturpunkt Heinrichstein, Neuhammer (Eisenwerk, 1869 von der fürstlichen Kammer übernommen), Neuhaus und Beginn von Gottliebsthal (Gasthof, Wollspinnerei).",
    "Saaldorf: upper and lower Schlösschen, Rödelshammer (Polish hammer, built 1795, closed 1846), Christiansglück (alum and vitriol works), the scenic spot Heinrichstein, Neuhammer (ironworks, taken over by the prince's chamber in 1869), Neuhaus and the beginning of Gottliebsthal (inn, wool spinning).",
    ["Schlösschen", "Rödelshammer", "Christiansglück", "Heinrichstein", "Neuhammer", "Neuhaus", "Gottliebsthal", "Eisenwerk", "Alaun"],
    ["Schlösschen", "Rödelshammer", "Christiansglück", "Heinrichstein", "Neuhammer", "Neuhaus", "Gottliebsthal", "ironworks"],
    ["Hüttenwesen und Hammerwerke", "Bergbau", "Siedlungsform"])

add("728",
    "Saaldorf: Gottliebsthal (Spinnerei und Tuchfabrik seit 1849, Felsenhöhlen und Lochhansen), Neuwerk (Waffenhammer 1803–1823), Spaniershammer (Stahlhütte, Hammerwerk bis 1852, seit 1863 Ziegelfabrik und Schneidemühle) und Motschenmühle.",
    "Saaldorf: Gottliebsthal (spinning mill and cloth factory since 1849, rock caves and 'Lochhansen'), Neuwerk (weapons hammer 1803–1823), Spaniershammer (steelworks, hammer works until 1852, brickworks and sawmill since 1863) and Motschenmühle.",
    ["Gottliebsthal", "Lochhansen", "Neuwerk", "Spaniershammer", "Motschenmühle", "Tuchfabrik", "Ziegelfabrik", "Stahlhütte", "Saale"],
    ["Gottliebsthal", "cave dwellers", "Neuwerk", "Spaniershammer", "Motschenmühle", "cloth factory", "brickworks", "steelworks"],
    ["Hüttenwesen und Hammerwerke", "Mühlen", "Textilgewerbe", "Ziegelei"])

add("729",
    "Schematischer Plan des Saaldorfer Gemeinde- und Schulbezirks (Saalpolynesien genannt) mit den Orten von Heinrichsstein und Silberknie bis Magwitzhaus sowie den Seitenbächen (Rattenbach, Ziezelbach).",
    "Schematic plan of the Saaldorf municipal and school district (called 'Saalpolynesien') showing the places from Heinrichsstein and Silberknie to Magwitzhaus and the side streams (Rattenbach, Ziezelbach).",
    ["Plan", "Saaldorf", "Saalpolynesien", "Gemeindebezirk", "Schulbezirk", "Ortsplan", "Heinrichsstein", "Gottliebsthal"],
    ["plan", "Saaldorf", "Saalpolynesien", "municipal district", "school district", "place map", "Heinrichsstein"],
    ["Gemeinden", "Siedlungsform", "Lage und Grenzen"])

add("730",
    "Pöritzsch: Grenzdörfchen zwischen Saalburg und Ebersdorf mit Kammergut; Lage, Häuser, 163 Einwohner, Viehstand; Pfarr- und Schulzugehörigkeit zu Zoppothen (Greiz), Geschichte der 1505 gegründeten Annenkapelle und des Streits um ihr Kapital, Besitzer des Ritterguts (v. Draxdorf), Gemeindeverhältnisse.",
    "Pöritzsch: border hamlet between Saalburg and Ebersdorf with a crown estate; location, houses, 163 inhabitants, livestock; parish and school at Zoppothen (Greiz), history of the chapel of St Anne founded in 1505 and the dispute over its capital, owners of the manor (von Draxdorf), municipal conditions.",
    ["Pöritzsch", "Grenzdorf", "Kammergut", "Zoppothen", "Annenkapelle", "Draxdorf", "Saalburg", "Einwohner 163"],
    ["Pöritzsch", "border village", "crown estate", "Zoppothen", "chapel of St Anne", "Draxdorf", "Saalburg"],
    ["Dorf", "Kammergut", "Pfarreien", "Gemeinden"])

add("731",
    "Pöritzsch (Schluss): Bauerngüter, Berufe, Flur 1578 1/3 Morgen mit Flurnamen, Geschichte, Schanze 1806; Wüstung Hohendorf mit wüstem Schloss und Schatzsage. Beginn Ebersdorf (Marktflecken, Sommerresidenz, herrnhuter Kolonie): Namensformen, Lage, Gedicht von Uhl.",
    "Pöritzsch (end): farms, occupations, parish land of 1,578 1/3 Morgen with field names, history, redoubt of 1806; the deserted settlement Hohendorf with a ruined castle and a treasure legend. Start of Ebersdorf (market town, summer residence, Moravian colony): name forms, location, a poem by Uhl.",
    ["Pöritzsch", "Hohendorf", "Wüstung", "Flurnamen", "Sorben", "Schatzsage", "Ebersdorf", "Marktflecken", "Herrnhuter"],
    ["Pöritzsch", "Hohendorf", "deserted settlement", "field names", "Sorbs", "treasure legend", "Ebersdorf", "market town"],
    ["Wüstung", "Flurnamen", "Sagen", "Dorf"])

add("732",
    "Ebersdorf: Lage in einer Hochmulde und Aufbau (Schloss, Ortsgemeinde, herrnhuter Anbau), öffentliche Gebäude und Privathäuser; Schloss mit Park und Orangerie; Geschichte des Rittergutes von 1402 bis zu den v. Magwitz (1580); Fußnote zum Besitz der Familie v. Draxdorf.",
    "Ebersdorf: location in an upland hollow and layout (castle, village congregation, Moravian extension), public buildings and private houses; castle with park and orangery; history of the manor from 1402 to the von Magwitz (1580); footnote on the possessions of the von Draxdorf family.",
    ["Ebersdorf", "Schloss Ebersdorf", "Park", "Orangerie", "Rittergut", "Draxdorf", "Magwitz", "Herrnhuter Anbau", "Sommerresidenz"],
    ["Ebersdorf", "Ebersdorf castle", "park", "orangery", "manor", "Draxdorf", "Magwitz", "Moravian quarter"],
    ["Burgen und Schlösser", "Rittergut", "Siedlungsform", "Dorf"])

add("733",
    "Ebersdorf: Kauf des Gutes 1682 für Heinrich X., Schlossbau 1690–1693, Residenzzeit, Gebietserweiterungen 1711, 1802 und 1824; Bevölkerungstabelle 1528–1867 (1008 Einwohner, davon Ortsgemeinde 707, Brüdergemeinde 301); Behörden vor und nach 1848, Kammergut.",
    "Ebersdorf: purchase of the estate in 1682 for Heinrich X, castle built 1690–1693, residence period, territorial gains in 1711, 1802 and 1824; population table 1528–1867 (1,008 inhabitants, 707 in the village congregation, 301 in the Moravian congregation); authorities before and after 1848, crown estate.",
    ["Ebersdorf", "Residenz", "Heinrich X.", "Heinrich XXIX.", "Bevölkerungsentwicklung", "Behörden", "Kammergut", "Revolution 1848", "Schlossbau"],
    ["Ebersdorf", "residence", "Heinrich X", "Heinrich XXIX", "population growth", "authorities", "crown estate", "1848"],
    ["Fürstenhaus", "Bevölkerung", "Ämter und Behörden", "Revolution 1848"])

add("734",
    "Ebersdorf: Kirche (Neubau 1622), Turm, Glocken, Orgel, Gruft des Regentenhauses (18 Särge), Friedhöfe; Filialverhältnis zu Friesau und Streit um den Kirchbau.",
    "Ebersdorf: church (rebuilt 1622), tower, bells, organ, vault of the ruling house (18 members), cemeteries; relationship as daughter church of Friesau and the dispute over the church building.",
    ["Kirche Ebersdorf", "Kirchenbau 1622", "Fürstengruft", "Glocken", "Orgel", "Friedhof", "Friesau", "Magwitz"],
    ["Ebersdorf church", "church building 1622", "princely vault", "bells", "organ", "cemetery", "Friesau"],
    ["Kirchengebäude", "Pfarreien", "Fürstenhaus"])

add("735",
    "Ebersdorf: Hofgemeinde und Hofkirche, selbstständige Pfarrei 1745, Ephorie 1844–1868; Pfarrhaus und Schulgeschichte (Schule seit 1718, 140 Schüler), Stiftungen, zwei Gasthöfe, Spritzen.",
    "Ebersdorf: court congregation and court church, independent parish in 1745, superintendency 1844–1868; parsonage and school history (school since 1718, 140 pupils), endowments, two inns, fire pumps.",
    ["Pfarrei Ebersdorf", "Hofprediger", "Hofgemeinde", "Schule", "Pfarrhaus", "Stiftungen", "Gasthöfe", "Ephorie", "Friesau"],
    ["Ebersdorf parish", "court preacher", "court congregation", "school", "parsonage", "endowments", "inns"],
    ["Pfarreien", "Schule", "Stiftungen"])

add("736",
    "Ebersdorf: Gemeindeverwaltung und -finanzen, Einwohner nach Ständen, Viehstand, Bauerngüter, Gewerbe (110 Gewerbe und Handwerke), Armenfürsorge, Bibliothek, Schützenverein, Flur 1065 Morgen mit Flurnamen; Anfang der Geschichte der herrnhutischen Brüdergemeinde (1733 unter Heinrich XXIX.).",
    "Ebersdorf: municipal administration and finances, residents by status, livestock, farms, trades (110 trades and crafts), poor relief, library, shooting club, parish land of 1,065 Morgen with field names; start of the history of the Moravian congregation (1733 under Heinrich XXIX).",
    ["Gemeindefinanzen", "Gewerbe", "Handwerker", "Armenfürsorge", "Flur", "Brüdergemeinde", "Herrnhuter", "Zinzendorf", "Schützenverein"],
    ["municipal finances", "trades", "craftsmen", "poor relief", "parish land", "Moravian congregation", "Zinzendorf", "shooting club"],
    ["Gemeindefinanzen", "Berufe", "Religion und Frömmigkeit", "Handwerk"])

add("737",
    "Ebersdorf: Ansiedlung der Brüdergemeinde und ihre Bauten (Chorhäuser, Gemeinhaus, Wohnhäuser 1742–1748), Gottesacker 1740, Befreiung von der Landesinspektion 1751, Gerichtsstand, Leitung durch die Unitätsdirektion in Berthelsdorf, Ausgaben und Schulden (23.400 Thlr.).",
    "Ebersdorf: settlement of the Moravian congregation and its buildings (choir houses, community house, dwellings 1742–1748), burial ground 1740, exemption from the state's church inspection in 1751, jurisdiction, direction by the Unity board in Berthelsdorf, expenses and debts (23,400 thalers).",
    ["Brüdergemeinde", "Herrnhuter", "Zinzendorf", "Chorhaus", "Gemeinhaus", "Unitätsdirektion", "Berthelsdorf", "Gerichtsstand", "Schulden"],
    ["Moravian congregation", "Herrnhut", "Zinzendorf", "choir house", "community house", "Unity board", "Berthelsdorf", "jurisdiction"],
    ["Religion und Frömmigkeit", "Kirche", "Rechtspflege"])

add("738",
    "Ebersdorf: Mitgliederzahlen und Gewerbe der Brüdergemeinde (Verluste der Tuch- und Weberei), Viehstand; Ortsname und frühe Geschichte, Wüstung Altenebersdorf; Erdmuth Dorothea von Zinzendorf (1700–1756) und Heinrich XXVI. (1725–1796); Fußnote zu J. J. Moser (1739–1749 in Ebersdorf).",
    "Ebersdorf: membership and trades of the Moravian congregation (losses in cloth and weaving works), livestock; place name and early history, deserted Altenebersdorf; Erdmuth Dorothea von Zinzendorf (1700–1756) and Heinrich XXVI (1725–1796); footnote on J. J. Moser (in Ebersdorf 1739–1749).",
    ["Brüdergemeinde", "Erdmuth Dorothea", "Heinrich XXVI.", "Zinzendorf", "Johann Jacob Moser", "Altenebersdorf", "Ortsname", "Wüstung", "Tuchfabrik"],
    ["Moravian congregation", "Erdmuth Dorothea", "Heinrich XXVI", "Zinzendorf", "Johann Jacob Moser", "Altenebersdorf", "place name", "deserted settlement"],
    ["Religion und Frömmigkeit", "Genealogie", "Wüstung", "Ortsname"])

add("739",
    "Ebersdorf (Schluss, nach dem Faksimile): Armen- und Waisenhaus 1732 (Pflege eines Zuges von 1000 Salzburger Emigranten), Napoleons Quartier im Schloss am 9. Oktober 1806 und Schutz für das Reußenland, Besuch der „schönen Spanierin Lola“ (wohl Lola Montez) bei Heinrich LXXII., Verkauf einer orientalischen Münzsammlung nach Jena, Hagelschläge und Brände; Fußnote zu Napoleons Zug 8.–13. Oktober 1806.",
    "Ebersdorf (end, from the facsimile): poor-house and orphanage 1732 (care for a column of 1,000 Salzburg emigrants), Napoleon's quarters in the castle on 9 October 1806 and his protection for Reuss, a visit by 'the beautiful Spanish woman Lola' (probably Lola Montez) to Heinrich LXXII, sale of an oriental coin collection to Jena, hailstorms and fires; footnote on Napoleon's march of 8–13 October 1806.",
    ["Napoleon 1806", "Salzburger Emigranten", "Waisenhaus", "Lola Montez", "Münzsammlung", "Hagelschlag", "Heinrich LXXII.", "Ebersdorf"],
    ["Napoleon 1806", "Salzburg emigrants", "orphanage", "Lola Montez", "coin collection", "hailstorm", "Heinrich LXXII", "Ebersdorf"],
    ["Napoleonische Kriege", "Armenwesen", "Brände", "Fürstenhaus"])

add("740",
    "Ebersdorf (Schluss): Spukgeschichten in Remptendorf, Zoppothen und Bellevue. Schönbrunn: Lage, Dorfbild, Kirche (Marienkapelle, Bau Ende 17. Jh.) mit Orgel und Glocken, Filial von Lobenstein, Schule (92 Kinder), Gasthof, Ziegelhütten.",
    "Ebersdorf (end): ghost stories from Remptendorf, Zoppothen and Bellevue. Schönbrunn: location, village layout, church (Marian chapel, built end of the 17th century) with organ and bells, daughter church of Lobenstein, school (92 children), inn, brickworks.",
    ["Schönbrunn", "Kirchdorf", "Marienkapelle", "Schönbrunnen", "Spukgeschichten", "Schule", "Filial Lobenstein", "Ziegelhütten", "Glocken"],
    ["Schönbrunn", "church village", "Marian chapel", "spring fountain", "ghost stories", "school", "daughter church of Lobenstein", "brickworks"],
    ["Dorf", "Kirchengebäude", "Sagen", "Schule"])

add("741",
    "Schönbrunn: Gemeindefinanzen und Grundbesitz, Einzelhäuser Bellevue (1783), Pohligshaus, weißer Trutz und grüner Affe; 561 Einwohner, Viehstand, Gewerbe, Bauerngüter, Flur 2562½ Morgen mit Flurnamen, Ortsname; Beginn der Geschichte (Schäferei, Rittergut Altenebersdorf).",
    "Schönbrunn: municipal finances and landholding, outlying houses Bellevue (1783), Pohligshaus, the 'white Trutz' and 'green ape' inns; 561 inhabitants, livestock, trades, farms, parish land of 2,562½ Morgen with field names, place name; start of the history (sheep farm, manor of Altenebersdorf).",
    ["Schönbrunn", "Bellevue", "Pohligshaus", "Trutz", "Gemeindefinanzen", "Flurnamen", "Bauerngüter", "Ortsname", "Altenebersdorf"],
    ["Schönbrunn", "Bellevue", "Pohligshaus", "Trutz inn", "municipal finances", "field names", "farms", "place name"],
    ["Dorf", "Gemeindefinanzen", "Flurnamen", "Ortsname"])

add("742",
    "Schönbrunn (Schluss): Wüstung Altenebersdorf, Wirtshaus Trutz, Zins an das Kloster Saalburg 1325, Lindenallee 1782. Unterlemnitz: Namensformen, Lage im Lemnitztal, Häuser, Kammergut (altes landesherrliches Vorwerk), Kirche (Petrus und Paulus) und Schule.",
    "Schönbrunn (end): deserted Altenebersdorf, the Trutz inn, rent to Saalburg monastery in 1325, lime avenue of 1782. Unterlemnitz: name forms, location in the Lemnitz valley, houses, crown estate (an old seigniorial outlying farm), church (Peter and Paul) and school.",
    ["Altenebersdorf", "Wüstung", "Lindenallee", "Unterlemnitz", "Kammergut", "Vorwerk", "Kirche", "Lemnitz", "Namensformen"],
    ["Altenebersdorf", "deserted settlement", "lime avenue", "Unterlemnitz", "crown estate", "outlying farm", "church", "name forms"],
    ["Wüstung", "Dorf", "Kammergut", "Kirchengebäude"])

add("743",
    "Unterlemnitz (Schluss): Schule (66 Kinder), Einwohner 372, Viehstand, Gemeinde, Berufe, Flur 2609 7/9 Morgen mit Flurnamen, sorbische Anlage, Brände 1845 und 1857. Beginn von Helmsgrün (Schuldorf): Namensformen und Lage.",
    "Unterlemnitz (end): school (66 children), 372 inhabitants, livestock, municipality, occupations, parish land of 2,609 7/9 Morgen with field names, Sorbian foundation, fires of 1845 and 1857. Start of Helmsgrün (school village): name forms and location.",
    ["Unterlemnitz", "Schule", "Gemeindefinanzen", "Berufe", "Flurnamen", "Brände", "Sorben", "Helmsgrün", "Einwohner 372"],
    ["Unterlemnitz", "school", "municipal finances", "occupations", "field names", "fires", "Sorbs", "Helmsgrün"],
    ["Dorf", "Gemeinden", "Brände", "Sorben"])

add("744",
    "Helmsgrün (Schluss): Häuser, 456 Einwohner, Pfarrzugehörigkeit zu Heinersdorf, Schule 1740, Gemeinde, Berufe, Flur 2177 1/11 Morgen mit Flurnamen, Eibig und Sage vom wilden Jäger. Beginn von Heinersdorf (Kirch- und Pfarrdorf): Namensformen.",
    "Helmsgrün (end): houses, 456 inhabitants, parish affiliation to Heinersdorf, school of 1740, municipality, occupations, parish land of 2,177 1/11 Morgen with field names, the Eibig and a legend of the wild huntsman. Start of Heinersdorf (church and parish village): name forms.",
    ["Helmsgrün", "Schuldorf", "Heinersdorf", "Schulgründung 1740", "Flurnamen", "Wilder Jäger", "Berufe", "Gemeindefinanzen", "Einwohner 456"],
    ["Helmsgrün", "school village", "Heinersdorf", "school founded 1740", "field names", "wild huntsman", "occupations", "municipal finances"],
    ["Dorf", "Schule", "Flurnamen", "Sagen"])

add("745",
    "Heinersdorf: hohe Lage an der Straße Lobenstein–Wurzbach, Dorfbild, 605 Einwohner in 130 Familien, Vorwerk und Rittergut mit Besitzerfolge und Zerschlagung 1758/1830; Marienkapelle (vor 1411), Parochialkirche seit 1546 und ihre Baugeschichte.",
    "Heinersdorf: high location on the Lobenstein-Wurzbach road, village layout, 605 inhabitants in 130 families, outlying farm and manor with owners and break-up in 1758/1830; Marian chapel (before 1411), parish church since 1546 and its building history.",
    ["Heinersdorf", "Rittergut", "Vorwerk", "Marienkapelle", "Parochialkirche", "Kirchenbau", "Besitzergeschichte", "Zerschlagung", "Einwohner 605"],
    ["Heinersdorf", "manor", "outlying farm", "Marian chapel", "parish church", "church building", "ownership history", "break-up of estate"],
    ["Dorf", "Rittergut", "Kirchengebäude", "Pfarreien"])

add("746",
    "Heinersdorf: Kirche (Glocken 1509 und 1537, Gruft), Pfarrhof, Pfarrer (Barthol. Groh, 19 Pfarrer), Schule (100 Kinder); Gewerbe, Bauerngüter, Sitten (uneheliche Kinder), Gesundheit, Flur 2923 4/9 Morgen mit Flurnamen.",
    "Heinersdorf: church (bells of 1509 and 1537, vault), parsonage, pastors (Barthol. Groh; 19 pastors), school (100 children); trades, farms, morals (illegitimate children), health, parish land of 2,923 4/9 Morgen with field names.",
    ["Heinersdorf", "Kirche", "Glocken", "Pfarrer Groh", "Pfarrhof", "Schule", "uneheliche Kinder", "Flurnamen", "Bauerngüter"],
    ["Heinersdorf", "church", "bells", "Pastor Groh", "parsonage", "school", "illegitimate children", "field names"],
    ["Pfarreien", "Schule", "Bräuche", "Flurnamen"])

add("747",
    "Heinersdorf (Schluss): Gemeindefinanzen, Geschichte (1347, Bauernaufstand 1573, Plünderung 1806, Brand 1853), Bärenmühle und Klettigsgrund (Hammermühle, Klettigshammer), Wüstenheinersdorf. Beginn von Oberlemnitz (kleines Kirchdorf): Namensformen, Lage, Dorfbild.",
    "Heinersdorf (end): municipal finances, history (1347, peasant revolt of 1573, plundering of 1806, fire of 1853), Bärenmühle and Klettigsgrund (hammer mill, Klettigshammer), deserted Wüstenheinersdorf. Start of Oberlemnitz (small church village): name forms, location, village layout.",
    ["Heinersdorf", "Bärenmühle", "Klettigsgrund", "Wüstenheinersdorf", "Bauernaufstand 1573", "Groh Chronik", "Hammerwerk", "Oberlemnitz", "Gemeindefinanzen"],
    ["Heinersdorf", "Bärenmühle", "Klettigsgrund", "Wüstenheinersdorf", "peasant revolt 1573", "Groh chronicle", "hammer works", "Oberlemnitz"],
    ["Dorf", "Wüstung", "Mühlen", "Gemeindefinanzen"])

add("748",
    "Oberlemnitz: Häuser, Kapelle der h. Margaretha und Kirche von 1738, Schule (42 Kinder), 238 Einwohner, Landwirtschaft, Bauerngüter, Gemeinde, Flur 1950 7/18 Morgen mit Flurnamen, Ereignis von 1550 (Hans Eisenbeiß), Brand 1838.",
    "Oberlemnitz: houses, chapel of St Margaret and church of 1738, school (42 children), 238 inhabitants, farming, farms, municipality, parish land of 1,950 7/18 Morgen with field names, an event of 1550 (Hans Eisenbeiß), fire in 1838.",
    ["Oberlemnitz", "Margarethenkapelle", "Kirche 1738", "Schule", "Landwirtschaft", "Flurnamen", "Hans Eisenbeiß", "Gemeindefinanzen", "Brand 1838"],
    ["Oberlemnitz", "chapel of St Margaret", "church 1738", "school", "farming", "field names", "Hans Eisenbeiß", "municipal finances"],
    ["Dorf", "Kirchengebäude", "Landwirtschaft", "Schule"])

add("749",
    "Eliasbrunn: hohe Lage, Dorfbild, 267 Einwohner in 53 Familien, Kapelle des h. Burkhard (Wallfahrtskapelle) und Kirche von 1703, Quelle Eliasbrunn und Sage, Orgel und Glocken, Schule 1733, Gemeinde und Bauerngüter.",
    "Eliasbrunn: high location, village layout, 267 inhabitants in 53 families, chapel of St Burchard (pilgrimage chapel) and church of 1703, the spring Eliasbrunn and its legend, organ and bells, school 1733, municipality and farms.",
    ["Eliasbrunn", "Elias-Quelle", "Wallfahrtskapelle", "Kirche 1703", "Schule 1733", "Sage", "Bauerngüter", "Gemeinde", "Burkhard"],
    ["Eliasbrunn", "Elias spring", "pilgrimage chapel", "church 1703", "school 1733", "legend", "farms", "municipality"],
    ["Dorf", "Kirchengebäude", "Quellen", "Sagen"])

add("750",
    "Eliasbrunn (Schluss): Berufe, Flur 2319 1/3 Morgen mit Flurnamen, Ortsname und Wallfahrt, Mord des Bauern Eisenbeis 1606, Gerichtsherren. Beginn von Ruppersdorf: Namensformen, Lage, 426 Einwohner, Häuser, Rupertuskapelle.",
    "Eliasbrunn (end): occupations, parish land of 2,319 1/3 Morgen with field names, place name and pilgrimage, the killing by the farmer Eisenbeis in 1606, judicial lords. Start of Ruppersdorf: name forms, location, 426 inhabitants, houses, chapel of St Rupert.",
    ["Eliasbrunn", "Eisenbeis", "Mord 1606", "Wallfahrt", "Flurnamen", "Ruppersdorf", "Rupertuskapelle", "Ortsname", "Henkersfleck"],
    ["Eliasbrunn", "Eisenbeis", "murder 1606", "pilgrimage", "field names", "Ruppersdorf", "chapel of St Rupert", "place name"],
    ["Dorf", "Ortsname", "Kriminalität", "Flurnamen"])

add("751",
    "Ruppersdorf: Kirchenbau 1853 (12.000 Thlr.), alte Glocken (Laurentiusglocke 1514), Pfarrhaus, Pfarrer, Schule (75 Schüler), Gemeindefinanzen, Bauerngüter, Berufe, Flur 2204 2/3 Morgen.",
    "Ruppersdorf: church building of 1853 (12,000 thalers), old bells (Lawrence bell of 1514), parsonage, pastors, school (75 pupils), municipal finances, farms, occupations, parish land of 2,204 2/3 Morgen.",
    ["Ruppersdorf", "Kirche 1853", "Glocken", "Laurentiusglocke", "Pfarrhaus", "Schule", "Gemeindefinanzen", "Bauerngüter", "Flur"],
    ["Ruppersdorf", "church 1853", "bells", "Lawrence bell", "parsonage", "school", "municipal finances", "farms"],
    ["Kirchengebäude", "Pfarreien", "Schule", "Gemeindefinanzen"])

add("752",
    "Ruppersdorf (Schluss): Namensherkunft, Geschichte (Blitzbrand 1707, Wolfgang Krüger 1566, Pfarrer Danz 1703, Gerichtsherren bis 1439). Thierbach: Namensformen, Lage, Kammergut, 179 Einwohner, Schule seit 1841, Gemeinde, Bauerngüter.",
    "Ruppersdorf (end): origin of the name, history (lightning fire of 1707, Wolfgang Krüger 1566, Pastor Danz 1703, judicial lords until 1439). Thierbach: name forms, location, crown estate, 179 inhabitants, school since 1841, municipality, farms.",
    ["Ruppersdorf", "Wolfgang Krüger", "Blitzschlag 1707", "Gerichtsherrschaft", "Thierbach", "Kammergut", "Schule 1841", "Bauerngüter", "Ortsname"],
    ["Ruppersdorf", "Wolfgang Krüger", "lightning 1707", "jurisdiction", "Thierbach", "crown estate", "school 1841", "farms"],
    ["Dorf", "Ortsname", "Brände", "Kammergut"])

add("753",
    "Thierbach (Schluss): Berufe, Flur 1382 7/9 Morgen, Namensform Dürrbach, Brand 1865. Gemeinde Lückenmühle (1848 gegründet): Zusammensetzung aus Lückenmühle, Rödern, Siehdichfür, Joachimsmühle und Weißbach, 124 Einwohner, Kirch- und Schulverband, Schule 1866/67, Landwirtschaft.",
    "Thierbach (end): occupations, parish land of 1,382 7/9 Morgen, the form Dürrbach, fire of 1865. Municipality of Lückenmühle (founded 1848): composition from Lückenmühle, Rödern, Siehdichfür, Joachimsmühle and Weißbach, 124 inhabitants, church and school ties, school 1866/67, farming.",
    ["Thierbach", "Lückenmühle", "Gemeinde Lückenmühle", "Siehdichfür", "Rödern", "Joachimsmühle", "Weißbach", "Schule 1867", "Brand 1865"],
    ["Thierbach", "Lückenmühle", "municipality of Lückenmühle", "Siehdichfür", "Rödern", "Joachimsmühle", "Weißbach", "school 1867"],
    ["Gemeinden", "Dorf", "Schulgebäude", "Landwirtschaft"])

add("754",
    "Lückenmühle (Schluss): Flur 1270 Morgen mit 22 Teichen; Bestandtheile Rödern (früheres Rittergut, 1782 an vier Bauern aufgeteilt), Lückenmühle (Forsthaus, Mühle), Siehdichfür (Forsthaus; Namenssage), Joachimsmühle und reußische Häuser in Weißbach (Freigut; Beginn der Besitzgeschichte).",
    "Lückenmühle (end): parish land of 1,270 Morgen with 22 ponds; components Rödern (former manor, divided among four farmers in 1782), Lückenmühle (forester's house, mill), Siehdichfür (forester's house; name legend), Joachimsmühle and Reuss houses in Weißbach (freehold estate; start of its ownership history).",
    ["Lückenmühle", "Rödern", "Siehdichfür", "Joachimsmühle", "Weißbach", "Forsthaus", "Rittergut", "Namenssage", "Teiche"],
    ["Lückenmühle", "Rödern", "Siehdichfür", "Joachimsmühle", "Weißbach", "forester's house", "manor", "name legend"],
    ["Mühlen", "Rittergut", "Forstwirtschaft", "Teiche und Seen"])

add("755",
    "Weißbach (Schluss: Familie v. Poseck, Kloster Saalburg). Karolinenfield: waldeinsames Kammergut im Schwalbengrund (früher Waldhaus, Widerwillen), 64 Einwohner, Pfarr- und Schulzugehörigkeit zu Remptendorf; Forsthaus am Streitwald. Beginn von Thimmendorf: Namensformen und Lage.",
    "Weißbach (end: von Poseck family, Saalburg monastery). Karolinenfield: secluded crown estate in the Schwalbengrund (earlier Waldhaus, Widerwillen), 64 inhabitants, parish and school at Remptendorf; forester's house at the Streitwald. Start of Thimmendorf: name forms and location.",
    ["Karolinenfield", "Widerwillen", "Waldhaus", "Streitwald", "Forsthaus", "Kammergut", "Weißbach", "Poseck", "Thimmendorf"],
    ["Karolinenfield", "Widerwillen", "Waldhaus", "Streitwald", "forester's house", "crown estate", "Weißbach", "Poseck"],
    ["Kammergut", "Forstwirtschaft", "Ortsname", "Dorf"])

add("756",
    "Thimmendorf: Häuser, 358 Einwohner, Ortsteil Trotzdorf (Burg), Rittergut der v. Watzdorf, Kirche (Brände 1559 und 1676, Neubau 1677) und die puhlsche Stiftung von 1402 (Pfarrholz, wöchentliche Messe).",
    "Thimmendorf: houses, 358 inhabitants, the quarter Trotzdorf (Burg), manor of the von Watzdorf, church (fires of 1559 and 1676, rebuilt 1677) and the Puhle endowment of 1402 (parish wood, weekly mass).",
    ["Thimmendorf", "Trotzdorf", "Rittergut Watzdorf", "Kirche 1677", "Puhlsche Stiftung", "Pfarrholz", "Brand 1676", "Burg", "Messstiftung"],
    ["Thimmendorf", "Trotzdorf", "Watzdorf manor", "church 1677", "Puhle endowment", "parish wood", "fire 1676", "mass endowment"],
    ["Dorf", "Stiftungen", "Kirchengebäude", "Rittergut"])

add("757",
    "Thimmendorf (Schluss): Verwendung der puhlschen Stiftung und Holzverkauf 1866, Schule (57 Kinder), Gemeinde, Berufe, drei Jahrmärkte, Flur 2908 1/4 Morgen mit Flurnamen, Geschichte (Poppo 1310, Brände 1559, 1676, 1857), Gerichtsherren.",
    "Thimmendorf (end): use of the Puhle endowment and timber sale of 1866, school (57 children), municipality, occupations, three annual fairs, parish land of 2,908 1/4 Morgen with field names, history (Poppo 1310, fires of 1559, 1676, 1857), judicial lords.",
    ["Thimmendorf", "Puhlsche Stiftung", "Holzverkauf 1866", "Schule", "Märkte", "Flurnamen", "Brände", "Conrad Poppo", "Gemeindefinanzen"],
    ["Thimmendorf", "Puhle endowment", "timber sale 1866", "school", "fairs", "field names", "fires", "Conrad Poppo"],
    ["Stiftungen", "Märkte", "Brände", "Gemeindefinanzen"])

add("758",
    "Lothra: Lage im Landratsbezirk, Häuser, 273 Einwohner, Rittergüter der v. Watzdorf und v. Poseck, Teilungen 1628 und 1664, Zerschlagung 1783 und 1813, unteres Herrenhaus (Gasthof und Brauhaus), Pfaffengut.",
    "Lothra: location in the district, houses, 273 inhabitants, manors of the von Watzdorf and von Poseck, partitions of 1628 and 1664, break-up in 1783 and 1813, lower manor house (inn and brewery), parson's estate.",
    ["Lothra", "Rittergüter", "Watzdorf", "Poseck", "Zerschlagung", "Herrenhaus", "Pfaffengut", "Namensformen", "Einwohner 273"],
    ["Lothra", "manors", "Watzdorf", "Poseck", "break-up of estates", "manor house", "parson's estate", "name forms"],
    ["Dorf", "Rittergut", "Gasthof"])

add("759",
    "Lothra: Kirche (Martin; Glocke 1500; Restaurierung 1834), Filial von Altengesees, Friedhof, Schule (45 Kinder, Neubau 1864), Gasthöfe, Lothramühle, Gemeinde und Bauerngüter, Berufe.",
    "Lothra: church (St Martin; bell of 1500; restoration 1834), daughter church of Altengesees, cemetery, school (45 children, new building 1864), inns, Lothramühle, municipality and farms, occupations.",
    ["Lothra", "Kirche", "Martinskirche", "Glocke 1500", "Filial Altengesees", "Schule 1864", "Gasthöfe", "Lothramühle", "Bauerngüter"],
    ["Lothra", "church", "St Martin's church", "bell 1500", "daughter church of Altengesees", "school 1864", "inns", "Lothramühle"],
    ["Kirchengebäude", "Schule", "Pfarreien", "Gasthof"])

add("760",
    "Lothra: Berufe, Flur 1769 2/5 Morgen mit Flurnamen, Namens- und Besitzgeschichte (Poppo 1310), Brände 1721 und 1865; zahlreiche Sagen von Edelmann, Kobolden (Holzmännle), Futtermännchen, Schatz im Brunnen und Gespenstern an der Brandkiefer.",
    "Lothra: occupations, parish land of 1,769 2/5 Morgen with field names, name and ownership history (Poppo 1310), fires of 1721 and 1865; many legends of a nobleman, kobolds (Holzmännle), a feed sprite, a treasure in a well and ghosts at the Brandkiefer.",
    ["Lothra", "Sagen", "Kobolde", "Holzmännle", "Brandkiefer", "Flurnamen", "Brand 1721", "Gespenster", "Aberglaube"],
    ["Lothra", "legends", "kobolds", "wood sprites", "Brandkiefer", "field names", "fire 1721", "ghosts"],
    ["Sagen", "Aberglaube", "Flurnamen", "Brände"])

add("761",
    "Lothra (Schluss der Sagen: Kreuzweg, Mönchspfütze, Hechel). Altengesees: Lage im Waldkessel, Häuser, 245 Einwohner, Rittergut der v. Watzdorf (1763 zerschlagen), Kapelle um 1300, Kirche 1517, Erneuerungen.",
    "Lothra (end of the legends: crossroads, Mönchspfütze, Hechel). Altengesees: location in a wooded basin, houses, 245 inhabitants, manor of the von Watzdorf (broken up in 1763), chapel around 1300, church of 1517, renovations.",
    ["Lothra", "Sagen", "Altengesees", "Rittergut Watzdorf", "Kirche 1517", "Kapelle", "Zerschlagung 1763", "Namensformen", "Einwohner 245"],
    ["Lothra", "legends", "Altengesees", "Watzdorf manor", "church 1517", "chapel", "break-up 1763", "name forms"],
    ["Sagen", "Dorf", "Rittergut", "Kirchengebäude"])

add("762",
    "Altengesees: Friedhof, Pfarrhaus (nach Brand 1806 neu erbaut), Pfarrer, Schule (44 Kinder), Gemeinde und Schulden, Berufe, Armut, Sitten (gemeinsames Singen, Spinnstuben, Heischereime bei Festen); Fußnote zum Patronatsstreit Christoph v. Watzdorfs 1594–1606.",
    "Altengesees: cemetery, parsonage (rebuilt after the fire of 1806), pastors, school (44 children), municipality and debts, occupations, poverty, customs (communal singing, spinning bees, rhymed begging at feasts); footnote on Christoph von Watzdorf's patronage dispute of 1594–1606.",
    ["Altengesees", "Pfarrhaus", "Pfarrer", "Schule", "Sitten und Bräuche", "Spinnstube", "Singen", "Patronatsstreit", "Gemeindeschulden"],
    ["Altengesees", "parsonage", "pastors", "school", "customs", "spinning bee", "singing", "patronage dispute"],
    ["Pfarreien", "Bräuche", "Gemeindefinanzen", "Schule"])

add("763",
    "Altengesees (Schluss): Flur 1551 Morgen mit Flurnamen, Ortsname, Brände (1680, 1806), Klimavergleich mit Leutenberg. Beginn Gahma: Lage an der Chaussee Lobenstein–Leutenberg, Dorfbild, 294 Einwohner, Rittergut, Kirche (Bartholomäus) und ursprünglicher Kirchensprengel.",
    "Altengesees (end): parish land of 1,551 Morgen with field names, place name, fires (1680, 1806), climate comparison with Leutenberg. Start of Gahma: location on the Lobenstein-Leutenberg highway, village layout, 294 inhabitants, manor, church (St Bartholomew) and its original parish area.",
    ["Altengesees", "Flurnamen", "Ortsname", "Klima", "Gahma", "Kirchensprengel", "Bartholomäuskirche", "Hufeisenform", "Einwohner 294"],
    ["Altengesees", "field names", "place name", "climate", "Gahma", "parish area", "St Bartholomew's church", "horseshoe layout"],
    ["Dorf", "Ortsname", "Klima", "Pfarreien"])

add("764",
    "Gahma: Kirche (Orgel 1732, Glocken 1834), Pfarrer, Pfarrholz (Puhle 1402), Schule (77 Kinder), Mühlen im Sormitzgrund (Zschachen-, Neu-/Ponzels- und Grubersmühle), Schmelzhütte 1699–1732, Silberbergwerk Fortuna, Gemeinde, Berufe, Bauerngüter.",
    "Gahma: church (organ of 1732, bells of 1834), pastors, parish wood (Puhle 1402), school (77 children), mills in the Sormitz valley (Zschachen-, Neu-/Ponzels- and Grubersmühle), smelter 1699–1732, silver mine Fortuna, municipality, occupations, farms.",
    ["Gahma", "Kirche", "Pfarrholz", "Schule", "Zschachenmühle", "Silberbergwerk Fortuna", "Schmelzhütte", "Sormitz", "Mühlen"],
    ["Gahma", "church", "parish wood", "school", "Zschachenmühle", "silver mine Fortuna", "smelter", "Sormitz"],
    ["Mühlen", "Bergbau", "Kirchengebäude", "Schule"])

# ----------------------------------------------------------------- glossary
GL = []  # term, variants, kind, de, en, regex, extra_pages


def g(term, variants, kind, de, en, rx, extra=None):
    GL.append((term, variants, kind, de, en, rx, extra or []))


g("Morgen", ["Mrg."], "unit", "Flächenmaß; 1 preuß. Morgen = 180 Quadratruthen = 0,255322 ha (S. 832). Flurgrößen werden mit Bruchteilen angegeben (z. B. 2562½ Morgen).",
  "Unit of area; 1 Prussian Morgen = 180 square rods = 0.255322 ha (p. 832). Parish-land areas are given with fractions (e.g. 2,562½ Morgen).", r"Morgen")
g("□Ruthe", ["Quadratruthe"], "unit", "Flächenmaß; 1 preuß. Quadratruthe = 14,184579 m² (S. 832); 180 Quadratruthen = 1 Morgen.",
  "Unit of area; 1 Prussian square rod = 14.184579 m² (p. 832); 180 square rods = 1 Morgen.", r"[□☐] ?Ruthen")
g("Fuß", [], "unit", "Längenmaß; 1 preuß. Fuß = 0,313853 m, 12 Fuß = 1 preuß. Ruthe (S. 831). In den Ortsartikeln für Höhenangaben der Orte und Berge; den Bezugspunkt nennt Brückner an diesen Stellen nicht.",
  "Unit of length; 1 Prussian foot = 0.313853 m, 12 feet = 1 Prussian rod (p. 831). In the place articles used for the heights of places and hills; Brückner does not name the datum here.", r"\bFuß\b|Fuss")
g("Stunde", ["Stunden"], "unit", "Wegmaß: Entfernungen und Lagen werden in Stunden (Gehstunden) angegeben, z. B. „1/2 Stunde SW. von Saalburg“. Brückner definiert den Wert nicht; gemeint ist üblicherweise die in einer Stunde zu Fuß zurückgelegte Strecke.",
  "Distance measure: distances and locations are given in hours (walking hours), e.g. '1/2 hour SW of Saalburg'. Brückner does not define the value; normally the distance covered on foot in one hour.", r"Stunden?\b")
g("□Meile", ["Quadratmeile"], "unit", "Flächenmaß für Landesgebiete; die preuß. Meile = 2000 preuß. Ruthen (S. 832), nach den dortigen Angaben rund 7,53 km (1,0043 × 7500 m). Der Landestheil umfasst etwa 5 □Meilen.",
  "Unit of area for territories; the Prussian mile = 2,000 Prussian rods (p. 832), about 7.53 km by the figures given there (1.0043 × 7,500 m). The district measures about 5 square miles.", r"[□☐] ?Meile")
g("Thlr.", ["Thaler"], "currency", "Thaler, die Hauptrechnungsmünze zur Zeit Brückners; in den Ortsartikeln für Pacht, Gemeindevermögen, Schulden, Baukosten und Stiftungen.",
  "Thaler, the main currency of account in Brückner's time; used in the place articles for rents, municipal assets, debts, building costs and endowments.", r"Thlr", ["739"])
g("Gülden", ["Gulden"], "currency", "Ältere Rechnungsmünze, in den Ortsartikeln vor allem für Preise und Pfandsummen des 15.–18. Jahrhunderts (z. B. 17.000 Gülden 1497, 60.000 Gülden 1569). Brückner nennt hier keinen Umrechnungswert.",
  "Older currency of account, in the place articles mainly for prices and pledge sums of the 15th–18th centuries (e.g. 17,000 gulden in 1497, 60,000 gulden in 1569). Brückner gives no conversion value here.", r"Gülden")
g("Mark (Mk.)", ["Mk."], "currency", "Ältere Rechnungsmünze bzw. Gewichtsmark für Zinsen und Preise (z. B. 11.500 Mk. für das Gut Ebersdorf 1580, 8 Mark Geldzinsen). Ein Wert wird nicht angegeben.",
  "Older currency or weight mark for rents and prices (e.g. 11,500 marks for the Ebersdorf estate in 1580, 8 marks of rent). No value is given.", r"\bMk\.|\d\s?Mark\b|3/4 Mark|zwei Mark|1 1/2 Schock")
g("Groschen", ["Gr."], "currency", "Unterteilung des Thalers bzw. Guldens in kleinen Beträgen (z. B. 1 Gülden 8 Groschen Steuer).",
  "Subdivision of the thaler or gulden for small sums (e.g. 1 gulden 8 groschen of tax).", r"Groschen|\d Gr\.")
g("Aßo", ["Aßv"], "currency", "Im Druck stehende, von Brückner nicht erklärte Abkürzung für eine Geldsumme bei Kirchenbaukosten (z. B. Oberlemnitz 1738: 433 Aßo 1 Gr.; in der Transkription auch „Aßv“). Bedeutung ungeklärt.",
  "Abbreviation printed for a sum of money in church building costs and not explained by Brückner (e.g. Oberlemnitz 1738: 433 Aßo 1 Gr.; also transcribed 'Aßv'). Meaning unclear.", r"Aß[ov]")
g("Kammergut", ["Kammergüter"], "term", "Landesherrliches (fürstliches) Gut, dessen Erträge der fürstlichen Kammer zufließen und das in der Regel verpachtet wird; oft aus einem Rittergut oder Vorwerk hervorgegangen.",
  "Estate of the prince, whose revenue goes to the princely chamber and which is usually leased; often derived from a manor or outlying farm.", r"Kammergut|Kammergüter")
g("Rittergut", ["Rittersitz"], "term", "Adeliges Gut mit Herrenhaus, Gerichtsbarkeit, Lehen und Gerechtsamen über Dorfbewohner (Erbgerichte, Fronen); viele wurden im 18./19. Jahrhundert zerschlagen oder an die Landesherrschaft verkauft.",
  "Noble estate with a manor house, jurisdiction, fiefs and rights over villagers (hereditary courts, labour services); many were broken up or sold to the territorial lord in the 18th/19th centuries.", r"Rittergut|Rittergüter|Rittersitz|Rittermannlehn")
g("Vorwerk", [], "term", "Außen- bzw. Nebenhof eines Rittergutes oder Herrenhofes (Hof, Feld, Wald, Erbgerichte, Hintersättler); kann zum Kern eines Dorfes werden.",
  "Outlying farm of a manor or lord's court (farmyard, field, wood, hereditary jurisdiction, subtenants); can become the core of a village.", r"Vorwerk")
g("Freigut", ["Freigüter"], "term", "Bäuerliches oder adeliges Gut mit besonderen Freiheiten (z. B. von bestimmten Abgaben und Diensten); in Lothra und Heinersdorf genannt.",
  "Farm or noble estate with special exemptions (e.g. from certain dues and services); mentioned at Lothra and Heinersdorf.", r"Freigut|Freigüter")
g("Mannlehn", ["Rittermannlehn", "Mannlehen"], "term", "Lehen, das auch in männlicher Linie weitergegeben wird bzw. an den Lehnsmann (Vasallen) vergeben ist; „mannlehnbares Rittergut“ (Heinersdorf).",
  "Fief held by a vassal and passed on in the male line; 'mannlehnbares Rittergut' (Heinersdorf).", r"(?i)mannlehn|mannlehen")
g("Amtslehen", ["Pfarrlehen", "Klosterlehen"], "term", "Lehen, die dem Amt (der Landesherrschaft), der Pfarrei oder einem Kloster zustanden; Brückner führt bei jedem Ort an, wem Ober- und Erbgerichte und Lehen gehörten.",
  "Fiefs belonging to the office (the territorial lord), the parish or a monastery; for each place Brückner states who held the high and hereditary courts and fiefs.", r"Amtslehen|Pfarrlehen|Klosterlehen|Pfarreilehen|Gerichtslehen")
g("Obergerichte / Erbgerichte", ["Erbgericht", "Niedergerichte"], "term", "Obergerichte (hohe Gerichtsbarkeit) standen meist dem Landesherrn zu; Erbgerichte (niedere Gerichtsbarkeit) gehörten oft den Rittergutsbesitzern oder Pfarreien.",
  "High jurisdiction (Obergerichte) usually belonged to the territorial lord; hereditary courts (low jurisdiction) often belonged to manor owners or parishes.", r"Obergericht|Erbgericht|Niedergericht|Untergericht|Patrimonialgericht")
g("Grundstücksverbände", ["Pertinenzen", "ledige Grundstücke", "walzende Grundstücke"], "term", "Kategorien des bäuerlichen Grundbesitzes in Brückners Statistik neben den Bauerngütern (nach Morgen gestaffelt): zusammenhängende Grundstücksverbände, Pertinenzen und ledige (walzende) Grundstücke ohne Gutsverband (S. 709). Genaue Abgrenzung nicht erklärt.",
  "Categories of peasant land in Brückner's statistics besides the farms (graded by Morgen): land groups, appurtenances and single (freely tradable) plots without farm affiliation (p. 709). Exact delimitation not explained.", r"Grundstücksverb|Pertinenz|ledige.{0,20}Grundst|walzende")
g("Kleinhäusler", ["Häusler"], "term", "Besitzer eines kleinen Hauses ohne oder nur mit wenig Land; nach S. 709 gelten 1644 Kleinhäusler als „ohne weiteren Grundbesitz“.",
  "Owner of a small house with little or no land; according to p. 709, 1,644 cottagers have 'no further landholding'.", r"Kleinhäusler|Häusler")
g("Hintersattler", ["Hintersiedler", "Hintersättler"], "term", "Bewohner ohne vollen Besitz in der Gemeinde, der auf dem Grund eines anderen (z. B. eines Bauern) siedelt; in Vorwerksbeschreibungen genannt.",
  "Resident without full property rights in the municipality who lives on another's land (e.g. a farmer's); named in descriptions of outlying farms.", r"Hintersattler|Hintersiedler|Hintersättler")
g("Tropfhäusler", ["Fröhner", "Frohnbauer", "Fröner"], "term", "Kleine Leute mit Haus (Tropf), zu Frondiensten für das Rittergut verpflichtet; Brückner setzt Tropfhäusler mit Taglöhnern und Fröhnern gleich (S. 764, 759).",
  "Small people with a cottage, obliged to labour services for the manor; Brückner equates cottagers (Tropfhäusler) with day labourers and Fröhner (pp. 764, 759).", r"Tropfhäusler|Fröhner|Frohnbauern|Frohnbauer|Frohnhäuser|Frohnen")
g("Taglöhner", ["Taglohn"], "term", "Tagelöhner, im Taglohn arbeitende Einwohner ohne eigenen Hof.", "Day labourer working for daily wages without a farm of their own.", r"Taglöhner|Taglohn")
g("Hufe", ["Hufen", "Hufner"], "unit", "Bäuerliche Besitzgröße (ganze, halbe Hufe usw.); Brückner nennt für Lothra 10 Hufen und kleinere Anteile, aber keine Flächenangabe.",
  "Traditional size of a peasant holding (whole, half hide etc.); Brückner gives 10 hides and smaller shares for Lothra but no area.", r"Hufe\b|Hufen\b|Hufner")
g("Wüstung", ["wüster Ort"], "term", "Abgegangene, verlassene Siedlung; nur Flur- oder Burgreste und Namen bleiben (z. B. Hohendorf, Wüstenheinersdorf, Altenebersdorf).",
  "Deserted settlement; only field remains, castle remains and names survive (e.g. Hohendorf, Wüstenheinersdorf, Altenebersdorf).", r"Wüstung|wüster Ort|wüstes? Schloss|wüst gelegen|wüst\b")
g("Filial", ["Filialkirche", "Tochterkirche"], "term", "Kirche ohne eigenen Pfarrer, die von einer Mutterkirche (Parochie) mitversorgt wird; Gegenstück: „eingepfarrt“ (Ort gehört zum Pfarrbezirk).",
  "Church without its own pastor served by a mother church (parish); the counterpart is 'eingepfarrt' (a place belonging to the parish district).", r"Filial|eingepfarrt|pfarrt")
g("Superintendent", ["Superintendentur", "Ephorie"], "office", "Evangelischer Geistlicher mit Aufsicht über mehrere Pfarreien (Diözese); die Superintendentur des Landestheils war in Lobenstein, 1844–1867/68 in Ebersdorf (Ephorie).",
  "Protestant clergyman supervising several parishes (diocese); the district's superintendency was at Lobenstein, at Ebersdorf in 1844–1867/68 (Ephorie).", r"Superintendent|Ephorie")
g("Archidiaconus", ["Diaconus", "Compastor"], "office", "Zweit- bzw. Drittgeistlicher an einer Stadtkirche (Archidiaconus = erster, Diaconus = zweiter Helfer des Oberpfarrers); der Compastor ist der mitbetreuende Pfarrer von Filialen.",
  "Second or third clergyman at a town church (archdeacon = first, deacon = second assistant to the senior pastor); the compastor is the co-pastor serving daughter churches.", r"Archidiacon|Diacon|Compastor")
g("Consistorium", [], "institution", "Kirchenbehörde, die über Pfarrer, Kirchen und Schulen aufsichtsführend ist; für Lobenstein 1604–1863 das Consistorium zu Gera, seit 1863 Abteilung des Ministeriums für Kirchen- und Schulangelegenheiten (S. 713).",
  "Church authority supervising pastors, churches and schools; for Lobenstein it was the consistory at Gera in 1604–1863, since 1863 a department of the ministry of church and school affairs (p. 713).", r"Consistorium")
g("Kirchensatz", ["Patronat", "Besetzungsrecht"], "term", "Recht, Pfarrstellen zu besetzen (Patronat); bei Brückner „Besetzungsrecht“, meist landesherrlich, früher z. T. beim Abt von Saalfeld oder bei Rittergutsbesitzern.",
  "Right to appoint to parish posts (patronage); in Brückner 'Besetzungsrecht', mostly held by the territorial lord, formerly partly by the abbot of Saalfeld or manor owners.", r"Kirchensatz|Patronat|Besetzungsrecht")
g("Hofprediger", [], "office", "Prediger am fürstlichen Hof, in Ebersdorf zugleich Ortspfarrer (seit 1745); in Lobenstein 1725–1742 eine eigene Stelle.",
  "Preacher at the princely court, at Ebersdorf also the local pastor (since 1745); at Lobenstein a separate post in 1725–1742.", r"Hofprediger")
g("Brüdergemeinde", ["Herrnhuter", "Brüdergemeine", "Unität"], "institution", "Herrnhuter Brüdergemeine (Zinzendorf); in Ebersdorf seit 1733, mit Chorhäusern der ledigen Brüder und Schwestern, eigener Gerichts- und Verwaltungsordnung und Leitung durch die Unitätsdirektion in Berthelsdorf (S. 736–738).",
  "Moravian Church congregation (Zinzendorf); at Ebersdorf since 1733, with choir houses of the single brothers and sisters, its own jurisdiction and administration and direction by the Unity board in Berthelsdorf (pp. 736–738).", r"Brüdergemeinde|Herrnhut|herrnhut", ["739"])
g("Chorhaus", [], "term", "Gemeinschaftshaus der ledigen Brüder bzw. Schwestern in der Herrnhuter Gemeine (Chorhaus der ledigen Brüder, der ledigen Schwestern); in Ebersdorf später Pfarr- und Schulhaus.",
  "Communal house of the single brothers or sisters in the Moravian congregation; at Ebersdorf later used as parsonage and school.", r"Chorhaus")
g("Sorben", ["Slaven", "Ruthenen", "sorbisch"], "term", "Slawische Bevölkerung des Mittelalters; nach der Fußnote S. 706 abwechselnd Sorben, Slaven und Ruthenen genannt; Brückner sieht in Orts- und Flurnamen Hinweise auf sorbische Anlagen.",
  "Slavic population of the Middle Ages; according to the footnote on p. 706 called alternately Sorbs, Slavs and Ruthenians; Brückner reads place and field names as evidence of Sorbian settlements.", r"Sorben|sorbisch|Slaven")
g("Ruthenenland", ["terra ruthenica"], "term", "Name des Frankenwaldgebiets um Lobenstein; 1276 urkundlich terra ruthenica (S. 706, Fußnote).",
  "Name of the Franconian Forest area around Lobenstein; documented in 1276 as terra ruthenica (p. 706, footnote).", r"Ruthenen")
g("Specialhaus", ["Speciallinie"], "term", "Nebenlinie des Hauses Reuß mit eigenem Landesteil (hier das Specialhaus Lobenstein 1647–1848 mit den Linien Lobenstein, Hirschberg und Ebersdorf).",
  "Cadet branch of the house of Reuss with its own territory (here the special house of Lobenstein 1647–1848 with the lines of Lobenstein, Hirschberg and Ebersdorf).", r"Specialhaus|Speciallinie|Spezialhaus")
g("Landrathsbezirk", ["Landrathsamt"], "office", "Verwaltungsbezirk bzw. Behörde eines Landraths; der Landestheil Lobenstein-Ebersdorf bildet einen Landrathsbezirk mit Sitz des Landrathsamts in Ebersdorf.",
  "Administrative district or office of a Landrat; the Lobenstein-Ebersdorf district forms one with its Landrat office seated at Ebersdorf.", r"Landrath")
g("Rentamt", ["Rentei"], "office", "Fürstliche Finanzbehörde für Einkünfte aus Kammergütern und Abgaben; in Ebersdorf im Schloss.",
  "Princely finance office for income from crown estates and dues; at Ebersdorf in the castle.", r"Rentamt|Rentei")
g("Bergamt", [], "office", "Bergbehörde, die Bergbau, Gruben und Hüttenwerke beaufsichtigt; in Lobenstein.",
  "Mining authority supervising mines, pits and ironworks; at Lobenstein.", r"Bergamt")
g("Physicat", [], "office", "Amtsarztstelle (Physikus), staatlicher Arzt eines Bezirks; in Lobenstein.",
  "Post of district physician (Physikus), the state doctor of a district; at Lobenstein.", r"Physicat")
g("Friedensrichter", [], "office", "Unterster Richter für kleine Streitigkeiten in einer Gemeinde; in Lobenstein und Ebersdorf genannt.",
  "Lowest judge for petty disputes in a municipality; named at Lobenstein and Ebersdorf.", r"Friedensrichter")
g("Chaussee", ["Kunststraße"], "term", "Befestigte, gut ausgebaute Landstraße; Kunststraße ist Brückners gleichbedeutender Ausdruck.",
  "Paved, well-built highway; 'Kunststraße' is Brückner's synonymous expression.", r"Chaussee|Kunststraße")
g("Vicinalweg", ["Vicinalwege"], "term", "Gemeindeverbindungsweg zwischen Nachbarorten, von den Gemeinden zu unterhalten (Gemeindelasten).",
  "Local road between neighbouring places maintained by the municipalities (municipal burden).", r"Vicinal")
g("Schrotbau", ["Schrotbauten"], "term", "Blockbau aus waagerecht aufeinander gefügten Balken (Bauweise alter Bauernhäuser, meist einstöckig mit Spitzdach).",
  "Log construction of horizontally stacked beams (building method of old farmhouses, mostly one-storey with a pointed roof).", r"Schrotbau|Schrotbauten")
g("hartweich", [], "term", "In Brückners Dachstatistik neben Schiefer, Schindeln und Ziegeln verwendete Angabe; Bedeutung nicht erklärt, wohl eine gemischte (hart und weich) gedeckte Bauweise (Deutung).",
  "Term used in Brückner's roof statistics beside slate, shingles and tiles; meaning not explained, probably a mixed (hard and soft) roofing (interpretation).", r"hartweich")
g("Schindel", ["Schindeln"], "term", "Dachdeckung mit dünnen Holzplättchen; in der Dachstatistik der Ortsartikel neben Schiefer und Ziegeln angegeben.",
  "Roofing with thin wooden tiles; listed in the roof statistics of the place articles beside slate and tiles.", r"Schindel")
g("Hammerwerk", ["Hammer", "Stabhammer", "Hochofen", "Frischfeuer"], "term", "Wasserkraftbetriebenes Eisenwerk mit Hammer, ursprünglich Hammerwerk zur Eisen- und Stahlverarbeitung; Saaldorf ist im Saaltal ein Schwerpunkt (z. B. Neuhammer, Spaniershammer, Rödelshammer).",
  "Water-powered ironworks with a hammer for forging iron and steel; Saaldorf in the Saale valley is a centre (e.g. Neuhammer, Spaniershammer, Rödelshammer).", r"Hammerwerk|Stabhamm|Hochofen|Frischfeuer|Blaufeuer|Stahlfeuer|Zainhammer|Schmelzofen|Eisenhütte")
g("Alaun- und Vitriolwerk", ["Alaunwerk"], "term", "Chemisches Werk, das aus Alaunschiefer Alaun und Vitriol (Eisen- und Kupfersulfate) gewinnt; in Haueisen und Christiansglück.",
  "Chemical works extracting alum and vitriol (iron and copper sulphates) from alum shale; at Haueisen and Christiansglück.", r"Alaun")
g("Schneidemühle", [], "term", "Sägemühle; oft mit einer Mahlmühle verbunden.", "Sawmill; often combined with a grist mill.", r"Schneidemühle")
g("Walkmühle", ["Walkerei"], "term", "Mühle zum Walken (Verdichten) von Tuch in der Tuchmacherei.", "Mill for fulling cloth in cloth making.", r"Walkmühle|Walkerei")
g("Lohmühle", [], "term", "Mühle, die Eichenrinde (Lohe) für die Gerberei zerkleinert.", "Mill grinding oak bark (tan) for tanning.", r"Lohmühle")
g("Bracteat", ["Bracteaten"], "term", "Einseitig geprägte mittelalterliche Silbermünze (Hohlpfennig); Funde auf dem Gehege bei Lobenstein und in Ebersdorf.",
  "Medieval silver coin struck on one side (hollow penny); found on the Gehege near Lobenstein and at Ebersdorf.", r"Bracteat")
g("Intelligenzblatt", [], "term", "Anzeigen- und Nachrichtenblatt; das „Lobensteiner Intelligenzblatt“ erschien 1784–1805.",
  "Advertising and news sheet; the 'Lobensteiner Intelligenzblatt' appeared in 1784–1805.", r"Intelligenzbl")
g("Wollkämmerei", ["Wollkammarbeiter"], "term", "Vorbereitung der Wolle durch Kämmen vor dem Spinnen; in Lobenstein ein im 19. Jahrhundert erloschener Gewerbezweig.",
  "Preparation of wool by combing before spinning; in Lobenstein a trade that died out in the 19th century.", r"Wollkamm|Wollkämm")
g("Köhler", ["Köhlerei"], "term", "Holzkohlenbrenner; sächsische Köhler siedelten nach einem Raupenfraß in den Saalwäldern (Saaldorf, S. 725).",
  "Charcoal burner; Saxon charcoal burners settled in the Saale forests after a caterpillar plague (Saaldorf, p. 725).", r"Köhler")
g("Stern- und Scheibenschießen", [], "term", "Von Zeit zu Zeit in Orten wie Eliasbrunn, Gottliebsthal und Haueisen veranstaltete Schützenbelustigung (Schießen auf Stern und Scheibe).",
  "Shooting entertainment held from time to time in places such as Eliasbrunn, Gottliebsthal and Haueisen (shooting at a star and a target).", r"Stern- und Scheibenschießen")
g("Reihetisch", ["Wandelkost", "Wandelschule", "Reihesschank"], "dialect", "Dorfbräuche der Schul- und Schankversorgung: Reihetisch/Wandelkost = Lehrer wird reihum bei den Familien verköstigt, Wandelschule = Unterricht wechselnd in Häusern, Reihesschank = reihum ausgeübtes Schankrecht (aus dem Zusammenhang erschlossen).",
  "Village customs of school and tavern provision: Reihetisch/Wandelkost = the teacher is fed in turn by the families, Wandelschule = lessons held in rotating houses, Reihesschank = tavern right exercised in rotation (inferred from context).", r"Reihetisch|Wandelkost|Wandelschule|Reihesschank")
g("Gastgerechtigkeit", [], "term", "Recht, eine Gastwirtschaft zu betreiben; haftet an einem Haus oder Gut (z. B. in Heinersdorf auf dem Freigut).",
  "Right to run an inn; attached to a house or estate (e.g. at Heinersdorf on the freehold farm).", r"Gastgerechtigkeit")
g("Fortbildungsschule", [], "institution", "Weiterführende Gewerbeschule für Jugendliche nach der Volksschule; in Lobenstein 1865 gegründet, mit Unterricht Freitags und Sonntags (S. 717).",
  "Continuing trade school for young people after elementary school; founded at Lobenstein in 1865 with lessons on Fridays and Sundays (p. 717).", r"Fortbildungsschule")
g("Schulvorstand", [], "institution", "Örtliches Aufsichtsgremium der Schule aus Pfarrer, Lehrer, Bürgermeister und Ortsnachbarn (z. B. Unterlemnitz seit 1842).",
  "Local school board of pastor, teacher, mayor and local residents (e.g. Unterlemnitz since 1842).", r"Schulvorstand")
g("engere Gemeinde", ["weitere Gemeinde"], "term", "Die „engere“ Gemeinde ist die Gemeinschaft der Berechtigten (z. B. 37 Gerechtigkeiten in Gahma) mit eigenem Gemeindegut, im Unterschied zur „weiteren“ politischen Gemeinde (aus dem Zusammenhang erschlossen).",
  "The 'narrower' municipality is the community of those entitled (e.g. 37 rights at Gahma) with its own common property, as opposed to the 'wider' political municipality (inferred from context).", r"engere|weitere Gemeinde|weitere politische|weitere\b.{0,20}Vermögen")
g("Kapitalisten", ["Almosenarme"], "term", "Brückner nennt bei jedem Ort die Zahl der „Kapitalisten“ (von Kapitalerträgen lebende Einwohner) und der „Almosenarmen“ (Empfänger von Armenunterstützung) als Wohlstandsmaß.",
  "For each place Brückner gives the number of 'capitalists' (residents living on investment income) and 'almoners' (recipients of poor relief) as a measure of wealth.", r"Kapitalist|Almosenarme|Almosenempf")
g("wilde Ehe", [], "term", "Nichteheliche Lebensgemeinschaft ohne Trauung; Brückner zählt sie als Maß des sittlichen Zustands.",
  "Cohabitation without marriage; Brückner counts them as a measure of moral condition.", r"wilde Ehe|wilden Ehen")
g("Jahresbrod bauen", [], "term", "Wendung für Bauern, deren eigene Ernte für das ganze Jahr reicht („ihr Jahresbrod bauen“).",
  "Idiom for farmers whose own harvest suffices for the whole year ('ihr Jahresbrod bauen').", r"Jahresbrod")
g("Vicar", ["Vikar", "Caplan"], "office", "Hilfsgeistlicher einer vorreformatorischen Pfarrei, der Kapellen und Altäre bedient; in Lobenstein drei Vicare vor 1543 (S. 716).",
  "Assistant clergyman of a pre-Reformation parish serving chapels and altars; Lobenstein had three vicars before 1543 (p. 716).", r"Vicar|Caplan")
g("Cantor", ["Catechet", "Rector"], "office", "Lehrerstellen an Stadtschulen: Rector (Leiter der Knabenschule), Cantor (Gesangs- und Musiklehrer, Kirchendienst), Catechet (Leiter der Mädchenschule, Theologe).",
  "Teaching posts at town schools: rector (head of the boys' school), cantor (singing and music teacher with church duties), catechist (head of the girls' school, a theologian).", r"Cantor|Catechet|Rector")
g("Weichbild", [], "term", "Stadtgebiet bzw. Gemarkung einer Stadt; „im Weichbilde der Stadt“ = innerhalb der städtischen Gemarkung.",
  "Urban territory of a town; 'im Weichbilde der Stadt' = within the town's boundaries.", r"Weichbild")
g("Pf., R., Schf., Schw., Z., G., Bnst.", ["Bnst."], "term", "Abkürzungen im Viehstand der Ortsartikel: Pf. = Pferde, R. = Rinder, Schf. = Schafe, Schw. = Schweine, Z. = Ziegen, G. = Gänse, Bnst. = Bienenstöcke (Auflösung nach der Reihenfolge der Viehstandsangabe S. 709).",
  "Abbreviations in the livestock figures of the place articles: Pf. = horses, R. = cattle, Schf. = sheep, Schw. = pigs, Z. = goats, G. = geese, Bnst. = beehives (resolved from the order of the livestock figures on p. 709).", r"Schf\.")

# ---------------------------------------------------------------- assemble
pages = {}
for f in sorted((ROOT / "data" / "text" / "pages").glob("*.txt")):
    pages[f.stem] = f.read_text(encoding="utf-8")

labels = [str(x) for x in range(706, 765)]
assert [p[0] for p in P] == labels, ([p[0] for p in P], labels)

glossary = []
for term, variants, kind, de, en, rx, extra in GL:
    pg = [l for l in labels if re.search(rx, pages[l])]
    for e in extra:
        if e not in pg:
            pg.append(e)
    pg = sorted(set(pg), key=int)
    if not pg:
        print("NO PAGES for glossary term", term)
        continue
    glossary.append({"term": term, "variants": variants, "kind": kind, "de": de, "en": en, "pages": pg})

out = {
    "package": "G5",
    "pages": [{"page": p, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj}
              for p, de, en, kde, ken, subj in P],
    "glossary": glossary,
}
dst = ROOT / "data" / "search" / "pages" / "G5.json"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(P), "pages;", len(glossary), "glossary terms")
