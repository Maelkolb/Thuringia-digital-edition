import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")

# page: (summary_de, summary_en, keywords_de, keywords_en, subjects)
P = {}

def add(page, de, en, kde, ken, subj):
    assert page not in P
    P[page] = dict(page=page, summary_de=de, summary_en=en, keywords_de=kde, keywords_en=ken, subjects=subj)

add("487",
    "Schluss des Artikels Harpersdorf (Bohrversuche auf Steinsalz im Dessegrund 1822, Hausbrände 1856 und 1859) und Beginn des Artikels Kraftsdorf: zweiherriges Pfarr- und Grenzdorf drei Stunden westlich von Gera, Lage im Erlbachtal, Kirche, Pfarrei und Schule auf altenburgischem Grund, Pfarrer des 16. und 18. Jahrhunderts, Kirchenneubau 1844–1848; Zahlen zum reußischen Anteil.",
    "End of the Harpersdorf article (brine drilling in the Dessegrund in 1822, house fires in 1856 and 1859) and start of Kraftsdorf: a village divided between Reuss and Altenburg, three hours west of Gera in the Erlbach valley; church, rectory and school stand on Altenburg ground; pastors of the 16th and 18th centuries; church rebuilt 1844–1848.",
    ["Kraftsdorf", "Harpersdorf", "Steinsalz", "Bohrversuch", "Pfarrei", "Kirche", "Altenburg", "Erlbach"],
    ["Kraftsdorf", "Harpersdorf", "rock salt", "drilling", "parish", "church", "Altenburg", "Erlbach"],
    ["Dorf", "Pfarreien", "Kirchengebäude", "Bodenschätze"])

add("488",
    "Fortsetzung Kraftsdorf: Vieh, Schenken, Brauhäuser, vier Mühlen und Ziegelei, Gemeindevermögen und Ausgaben, Grundbesitz, Erwerb (Sandsteinarbeit, Maurer, Landfuhrwerk), Flur von 2386 Morgen, Geschichte des in vier Bauerngüter zerschlagenen Rittergutes, Brände 1842 und 1849.",
    "Kraftsdorf continued: livestock, taverns, brewhouses, four mills and a brickworks, municipal assets and expenses, landholdings, livelihoods (sandstone work, masons, carting), 2,386 Morgen of fields, history of the manor split into four farms, fires in 1842 and 1849.",
    ["Kraftsdorf", "Mühlen", "Ziegelei", "Sandstein", "Rittergut", "Gemeindevermögen", "Flur", "Brand"],
    ["Kraftsdorf", "mills", "brickworks", "sandstone", "manor", "municipal assets", "fields", "fire"],
    ["Dorf", "Gemeindefinanzen", "Mühlen", "Rittergut"])

add("489",
    "Wüstung Desse (1184 Deginstete, Kloster Lausnitz) und Beginn des Artikels Rüdersdorf: zweiherriges Kirch- und Pfarrdorf 2 1/2 Stunden WNW. von Gera mit historischen Namensformen, Lage und Ortsteilen; reußischer Anteil mit 77 Häusern, 512 Einwohnern, Vieh und Handwerkern (Steinhauer, Maurer, Zimmerer).",
    "Deserted village Desse (1184 Deginstete, Lausnitz monastery) and start of Rüdersdorf: a village shared between Reuss and Altenburg, 2 1/2 hours WNW of Gera, with historical name forms, setting and hamlets; the Reuss part has 77 houses, 512 inhabitants, livestock and craftsmen (stonecutters, masons, carpenters).",
    ["Desse", "Wüstung", "Rüdersdorf", "Kloster Lausnitz", "Steinhauer", "Altenburg", "Ortsname"],
    ["Desse", "deserted settlement", "Rüdersdorf", "Lausnitz monastery", "stonecutters", "Altenburg", "place name"],
    ["Wüstung", "Dorf", "Ortsname", "Berufe"])

add("490",
    "Schluss Rüdersdorf (Flur 1004 8/9 Morgen, Lehen und Frohntanz zu Langenberg, 1198 Schenkung an das Marienkloster Eisenberg, Sage von Burgen), Wüstung Schliffstein (1255 Kloster Lausnitz, 1364 Herren von Gera) und Beginn Stübnitz, kleines Plateaudorf mit 216 Einwohnern.",
    "End of Rüdersdorf (1,004 8/9 Morgen of fields, fiefs and the feudal dance at Langenberg, 1198 donation to the Marienkloster Eisenberg, legend of castles), deserted village Schliffstein (1255 Lausnitz monastery, 1364 lords of Gera) and start of Stübnitz, a small plateau village with 216 inhabitants.",
    ["Rüdersdorf", "Schliffstein", "Stübnitz", "Frohntanz", "Langenberg", "Marienkloster Eisenberg", "Steinbruch"],
    ["Rüdersdorf", "Schliffstein", "Stübnitz", "feudal dance", "Langenberg", "Marienkloster Eisenberg", "quarry"],
    ["Dorf", "Wüstung", "Territorialgeschichte", "Urkunden"])

add("491",
    "Schluss Stübnitz (kirchlich nach Rüdersdorf, Gemeindevermögen, Handwerker, Flur 527 5/18 Morgen, sorbischer Anbau, Flurnamen Hölle und Himmel) und Beginn Grüna, kleines Thal- und Grenzdorf im Schliffsteingrund mit 26 Häusern und 129 Einwohnern.",
    "End of Stübnitz (church ties to Rüdersdorf, municipal assets, craftsmen, 527 5/18 Morgen of fields, Sorbian settlement, field names Hölle and Himmel) and start of Grüna, a small valley village in the Schliffsteingrund with 26 houses and 129 inhabitants.",
    ["Stübnitz", "Grüna", "Rüdersdorf", "Schliffsteingrund", "Flurnamen", "sorbisch", "Handwerker"],
    ["Stübnitz", "Grüna", "Rüdersdorf", "Schliffsteingrund", "field names", "Sorbian", "craftsmen"],
    ["Dorf", "Flurnamen", "Sorben", "Gemeindefinanzen"])

add("492",
    "Schluss Grüna (Gemeindefinanzen, Maurer und Korbmacher, Flur 445,62 Morgen) und Beginn Hartmannsdorf, Kirchdorf im Schafgrund: Lage, Häuserzahl, 274 Einwohner, Rittergut (v. Ende, v. Wolframsdorf, später Paragiat Köstritz) und die wechselnde kirchliche Zugehörigkeit zu Köstritz und Rüdersdorf bis 1869.",
    "End of Grüna (municipal finances, masons and basket makers, 445.62 Morgen of fields) and start of Hartmannsdorf, a church village in the Schafgrund: setting, number of houses, 274 inhabitants, the manor (v. Ende, v. Wolframsdorf, later the Köstritz appanage) and its changing church affiliation with Köstritz and Rüdersdorf until 1869.",
    ["Grüna", "Hartmannsdorf", "Schafgrund", "Rittergut", "Köstritz", "Rüdersdorf", "Kirchenzugehörigkeit"],
    ["Grüna", "Hartmannsdorf", "Schafgrund", "manor", "Köstritz", "Rüdersdorf", "church affiliation"],
    ["Dorf", "Rittergut", "Pfarreien", "Gemeindefinanzen"])

add("493",
    "Schluss Hartmannsdorf (Kirche und Reparatur 1771, Schulhaus 1808 mit 47 Kindern, Mühlen, Gemeindefinanzen, Berufe, Kropfbildung, Flur 1401 1/2 Morgen, Volkssage) und Wüstung Oelsdorf, deren Stätte die gleichnamige Mühle bezeichnet.",
    "End of Hartmannsdorf (church and its repair in 1771, school building of 1808 with 47 pupils, mills, municipal finances, occupations, goitre, 1,401 1/2 Morgen of fields, folk legend) and the deserted village Oelsdorf, whose site is marked by the mill of the same name.",
    ["Hartmannsdorf", "Oelsdorf", "Wüstung", "Kirche", "Schule", "Mühlen", "Kropf", "Sage"],
    ["Hartmannsdorf", "Oelsdorf", "deserted settlement", "church", "school", "mills", "goitre", "legend"],
    ["Dorf", "Wüstung", "Kirchengebäude", "Sagen"])

add("494",
    "Dürrenberg (früheres Rittergut, jetzt Vorwerk von Köstritz, Familie v. Wolframsdorf) und Beginn Köstritz: Residenz der Paragiatlinie Reuß-Köstritz, Lage an der Elster, Ortsteile, Eisenbahnstation, 191 Gebäude und 1524 Einwohner, Schloss und die beiden alten Rittergüter.",
    "Dürrenberg (former manor, now a farm of Köstritz, family v. Wolframsdorf) and start of Köstritz: residence of the appanage line Reuss-Köstritz, setting on the Elster, hamlets, railway station, 191 buildings and 1,524 inhabitants, the palace and the two old manors.",
    ["Dürrenberg", "Köstritz", "Paragiat Reuß-Köstritz", "Schloss", "Elster", "Bahnhof", "Rittergut"],
    ["Dürrenberg", "Köstritz", "appanage Reuss-Köstritz", "palace", "Elster", "railway station", "manor"],
    ["Dorf", "Fürstenhaus", "Burgen und Schlösser", "Rittergut"])

add("495",
    "Köstritz: Rittergüter und Entstehung des Paragiums Reuß-Köstritz: Besitzer des 14. bis 17. Jahrhunderts, Graf Heinrich I. von Schleiz, 1690 anerkanntes Paragium unter Heinrich XXIV. (1704 Schloss), Heinrich VI. und Heinrich XLIII. (Fürstenwürde 1806).",
    "Köstritz: the manors and the origin of the appanage Reuss-Köstritz: owners from the 14th to 17th centuries, Count Heinrich I of Schleiz, the appanage recognised in 1690 under Heinrich XXIV (palace 1704), Heinrich VI and Heinrich XLIII (princely rank 1806).",
    ["Köstritz", "Paragium", "Heinrich XXIV.", "Heinrich XLIII.", "Wolframsdorf", "Schloss", "Genealogie"],
    ["Köstritz", "appanage", "Heinrich XXIV", "Heinrich XLIII", "Wolframsdorf", "palace", "genealogy"],
    ["Fürstenhaus", "Genealogie", "Territorialgeschichte", "Rittergut"])

add("496",
    "Köstritz: Konkurs nach dem Tod Heinrichs XLIII. (1814), Nachfolger Heinrich LXIV. und LXIX., Gerichtsverfassung, Kirche (1718 neu erbaut, Turm 1820), Kirchenvermögen, Kirchenbücher, eingepfarrte Orte und Filiale.",
    "Köstritz: bankruptcy after the death of Heinrich XLIII (1814), successors Heinrich LXIV and LXIX, judicial system, church (rebuilt 1718, tower 1820), church assets, parish registers, parish members and branch churches.",
    ["Köstritz", "Konkurs", "Heinrich XLIII.", "Heinrich LXIX.", "Kirche", "Kirchenvermögen", "Kirchenbücher"],
    ["Köstritz", "bankruptcy", "Heinrich XLIII", "Heinrich LXIX", "church", "church assets", "parish registers"],
    ["Fürstenhaus", "Genealogie", "Kirchengebäude", "Pfarreien"])

add("497",
    "Köstritz: Friedhöfe und Grabdenkmäler, Pfarrer und Collaboratoren, Schule mit 302 Kindern, Gemeindeverwaltung und Finanzen, Grundbesitz, Wandel des Erwerbs, fürstliche Brauerei (Köstritzer Schwarzbier) und Handelsgärtnereien.",
    "Köstritz: cemeteries and tombs, pastors and assistant ministers, school with 302 pupils, municipal administration and finances, landholdings, change of livelihoods, the princely brewery (Köstritzer black beer) and commercial nurseries.",
    ["Köstritz", "Brauerei", "Köstritzer Schwarzbier", "Handelsgärtnerei", "Schule", "Friedhof", "Gemeindefinanzen"],
    ["Köstritz", "brewery", "Köstritzer black beer", "commercial nursery", "school", "cemetery", "municipal finances"],
    ["Dorf", "Brauerei", "Schule", "Gemeindefinanzen"])

add("498",
    "Köstritz: Gärtnereien, 1864 gegründete Soolbadeanstalt, Gewerbe und Handwerk, Besitzgliederung der Einwohner, Armenstiftungen, Vereine, Flur von 2813 1/18 Morgen und deren Flurnamen, Ortsname, Komponist G. Benda und Heinrich Schütz.",
    "Köstritz: nurseries, the brine bath founded in 1864, trades and crafts, social structure of the inhabitants, charitable foundations, clubs, 2,813 1/18 Morgen of fields and their field names, place name, the composers G. Benda and Heinrich Schütz.",
    ["Köstritz", "Soolbad", "Gärtnerei", "Handwerk", "Armenstiftung", "Georg Benda", "Heinrich Schütz", "Flur"],
    ["Köstritz", "brine bath", "nursery", "crafts", "poor-relief foundation", "Georg Benda", "Heinrich Schütz", "fields"],
    ["Dorf", "Handwerk", "Stiftungen", "Armenwesen"])

add("499",
    "Schluss Köstritz (Persönlichkeiten, diluviale Tierreste 1862/63, Brände 1779 und 1829, Sagen), Wüstung Etzdorf mit Erwähnung von Eschewinsdorf, Eleonorenthal (Jägerhaus 1744) und Beginn Gleina mit Lage und Namensformen.",
    "End of Köstritz (notable people, Pleistocene animal remains 1862/63, fires of 1779 and 1829, legends), deserted village Etzdorf with a mention of Eschewinsdorf, Eleonorenthal (hunting lodge, 1744) and start of Gleina with its setting and name forms.",
    ["Köstritz", "Etzdorf", "Eschewinsdorf", "Eleonorenthal", "Gleina", "Diluvium", "Ausgrabung", "Brand"],
    ["Köstritz", "Etzdorf", "Eschewinsdorf", "Eleonorenthal", "Gleina", "Pleistocene", "excavation", "fire"],
    ["Wüstung", "Dorf", "Vor- und Frühgeschichte", "Brände"])

add("500",
    "Gleina: Lage in zwei Häusergruppen, Zusammenwachsen mit dem sorbischen Dorf Zwickau (Kirche 1151), Schloss auf dem Kolk, 147 Einwohner in 25 Privathäusern, Vieh, Kirche als Filial von Köstritz, Vikarei und Kirchenvermögen.",
    "Gleina: setting in two groups of houses, merger with the Sorbian village Zwickau (church in 1151), castle on the Kolk hill, 147 inhabitants in 25 private houses, livestock, church as a branch of Köstritz, vicarage and church assets.",
    ["Gleina", "Zwickau", "Kolk", "Kirche", "Vikarei", "Bosau", "sorbisch"],
    ["Gleina", "Zwickau", "Kolk", "church", "vicarage", "Bosau", "Sorbian"],
    ["Dorf", "Sorben", "Kirchengebäude", "Mittelalter"])

add("501",
    "Schluss Gleina (Schule 1839, Gemeindevermögen, Ackerbau, Flur 982 Morgen, Kupfererzgrube 1566, Brand 1709) und Beginn Seifartsdorf: zweiherriges Pfarrdorf 3 Stunden NW. von Gera mit Kirche, Glocken und Kirchenvermögen auf altenburgischem Grund.",
    "End of Gleina (school 1839, municipal assets, farming, 982 Morgen of fields, copper-ore mine 1566, fire of 1709) and start of Seifartsdorf: a parish village shared between Reuss and Altenburg, 3 hours NW of Gera, with church, bells and church assets on Altenburg ground.",
    ["Gleina", "Seifartsdorf", "Kupfererz", "Schule", "Ackerbau", "Kirche", "Glocken"],
    ["Gleina", "Seifartsdorf", "copper ore", "school", "farming", "church", "bells"],
    ["Dorf", "Landwirtschaft", "Bergbau", "Kirchengebäude"])

add("502",
    "Seifartsdorf: Pfarrer Hoffmann 1533, Pfarrhaus 1737–1739, Schule 1847, reußischer Anteil mit 27 Häusern und 148 Einwohnern, Gemeindefinanzen, Handwerker, Flur 551,95 Morgen, Geschichte seit 1260 (Lausnitz, Plauen, Gera), Pest 1633 und Brand 1725.",
    "Seifartsdorf: pastor Hoffmann in 1533, rectory 1737–1739, school 1847, the Reuss part with 27 houses and 148 inhabitants, municipal finances, craftsmen, 551.95 Morgen of fields, history since 1260 (Lausnitz, Plauen, Gera), plague 1633 and fire 1725.",
    ["Seifartsdorf", "Pfarrer", "Reformation", "Schule", "Stein", "Rittergut Caaschwitz", "Flur"],
    ["Seifartsdorf", "pastor", "Reformation", "school", "Stein", "Caaschwitz manor", "fields"],
    ["Dorf", "Pfarreien", "Reformation", "Gemeindefinanzen"])

add("503",
    "Schluss Seifartsdorf und Beginn Caaschwitz: Rittergutsort in der Elsteraue, 2 1/2 Stunden NNW. von Gera, 68 Privathäuser und 422 Einwohner; Geschichte des Ritterguts (1294 Felonie, 1386 Meerrettig, v. Schauroth, 1857 Kauf durch Nägler) und Kirche von 1751.",
    "End of Seifartsdorf and start of Caaschwitz: a manor village in the Elster meadows, 2 1/2 hours NNW of Gera, 68 private houses and 422 inhabitants; history of the manor (1294 felony, 1386 Meerrettig, v. Schauroth, purchase by Nägler in 1857) and the church of 1751.",
    ["Caaschwitz", "Seifartsdorf", "Rittergut", "Meerrettig", "Schauroth", "Nägler", "Kirche"],
    ["Caaschwitz", "Seifartsdorf", "manor", "Meerrettig", "Schauroth", "Nägler", "church"],
    ["Dorf", "Rittergut", "Genealogie", "Kirchengebäude"])

add("504",
    "Caaschwitz: Kirche und Vikarei (Filial von Langenberg, 1533 Absetzung des Vicars Fidler, um 1540 Seifartsdorf), Schule mit 67 Kindern, Gasthof, Gemeinde und Grundbesitz, Berufe, Flur 1627 1/3 Morgen, sorbischer Ortsname, Pest 1633 und 1637 und Niederbrennung 1637.",
    "Caaschwitz: church and vicarage (branch of Langenberg, vicar Fidler deposed in 1533, linked with Seifartsdorf about 1540), school with 67 pupils, inn, municipality and landholdings, occupations, 1,627 1/3 Morgen of fields, Sorbian place name, plague 1633 and 1637 and burning of the village in 1637.",
    ["Caaschwitz", "Vikarei", "Reformation", "Schule", "Pest", "Dreißigjähriger Krieg", "Ziegelei", "Flur"],
    ["Caaschwitz", "vicarage", "Reformation", "school", "plague", "Thirty Years' War", "brickworks", "fields"],
    ["Dorf", "Reformation", "Dreißigjähriger Krieg", "Seuchen"])

add("505",
    "Schluss Caaschwitz (Brände 1728, 1848, 1852 und 1860, Tanzwiese, weiße Dame) und Beginn Pohlitz: Kirch- und Grenzdorf an der Elster, Küchenort, durch den Meteoriten bekannt, 41 Privathäuser und 345 Einwohner, Kirche von 1723, Schule 56 Kinder, Rittergut.",
    "End of Caaschwitz (fires of 1728, 1848, 1852 and 1860, dance meadow, white lady) and start of Pohlitz: a church and border village on the Elster, a Küchenort, known for its meteorite, 41 private houses and 345 inhabitants, church of 1723, school with 56 pupils, manor.",
    ["Caaschwitz", "Pohlitz", "Meteorstein", "Brand 1728", "Kirche", "Küchenort", "Rittergut"],
    ["Caaschwitz", "Pohlitz", "meteorite", "fire of 1728", "church", "kitchen village", "manor"],
    ["Dorf", "Brände", "Kirchengebäude", "Rittergut"])

add("506",
    "Pohlitz: Rittergut (Wolframsdorf, Paragiat Köstritz), Gemeinde, Berufe, Flur 1490 1/15 Morgen, Frohnen und Gerichte, Pest 1566, Brände (Hauptbrand 22. März 1723), Pastoralkonferenz 1566 und Fall des Meteorsteins am 13. Oktober 1819.",
    "Pohlitz: manor (Wolframsdorf, Köstritz appanage), municipality, occupations, 1,490 1/15 Morgen of fields, feudal services and jurisdiction, plague 1566, fires (main fire on 22 March 1723), pastors' meeting of 1566 and the meteorite fall of 13 October 1819.",
    ["Pohlitz", "Meteorstein", "Pest 1566", "Brand 1723", "Frohnen", "Rittergut", "Musaeus"],
    ["Pohlitz", "meteorite", "plague of 1566", "fire of 1723", "feudal services", "manor", "Musaeus"],
    ["Dorf", "Naturkatastrophen", "Brände", "Seuchen"])

add("507",
    "Schluss Pohlitz (Sagen, Flur); Köstritzer Bahnhof (1858–1859), Saline Heinrichshall (1830 Steinsalzflöz, Oberbergrath Glenck) und chemische Fabrik (Soda, durchschnittlich 92 Arbeiter); Beginn Stublach, Dörfchen 10 Minuten westlich von Langenberg.",
    "End of Pohlitz (legends, fields); Köstritz railway station (1858–1859), the Heinrichshall saltworks (rock-salt seam in 1830, Oberbergrath Glenck) and chemical factory (soda, about 92 workers); start of Stublach, a small village 10 minutes west of Langenberg.",
    ["Pohlitz", "Köstritzer Bahnhof", "Heinrichshall", "Saline", "Soda", "chemische Fabrik", "Stublach"],
    ["Pohlitz", "Köstritz station", "Heinrichshall", "saltworks", "soda", "chemical factory", "Stublach"],
    ["Industrie", "Bergbau", "Eisenbahn", "Dorf"])

add("508",
    "Schluss Stublach (Gemeindefinanzen, Bauernhöfe, Flur 755 1/4 Morgen, Brand 1787, Sagen) und Beginn des Artikels über die Pflege Langenberg: Burgwartbezirke der Sorbenlande unter Heinrich I. und Otto I., Burg auf dem Hausberg, Besitz des Bistums Zeitz-Naumburg und der Markgrafen von Meißen.",
    "End of Stublach (municipal finances, farms, 755 1/4 Morgen of fields, fire of 1787, legends) and start of the article on the Pflege Langenberg: castle districts of the Sorbian lands under Henry I and Otto I, the castle on the Hausberg, holdings of the bishopric of Zeitz-Naumburg and the margraves of Meissen.",
    ["Stublach", "Pflege Langenberg", "Burgwart", "Hausberg", "Sorbenlande", "Heinrich I.", "Zeitz-Naumburg"],
    ["Stublach", "Pflege Langenberg", "castle district", "Hausberg", "Sorbian lands", "Henry I", "Zeitz-Naumburg"],
    ["Territorialgeschichte", "Sorben", "Burgen und Schlösser", "Mittelalter"])

add("509",
    "Pflege Langenberg: Besitzwechsel von den Markgrafen von Meißen über die Herren von Schönburg an Gera und Plauen (1333), Verkauf 1364 und 1502, Verlust der Pflegefunktion, Marktprivilegien 1505, Ruinen der Burg auf dem Hausberg; Fußnote mit den 55 Orten der Pflege.",
    "Pflege Langenberg: change of ownership from the margraves of Meissen via the lords of Schönburg to Gera and Plauen (1333), sales in 1364 and 1502, loss of its district function, market privileges in 1505, ruins of the castle on the Hausberg; footnote listing the 55 places of the Pflege.",
    ["Pflege Langenberg", "Schönburg", "Gera", "Plauen", "Burg Hausberg", "Marktprivileg", "Ortsliste"],
    ["Pflege Langenberg", "Schönburg", "Gera", "Plauen", "Hausberg castle", "market privilege", "list of places"],
    ["Territorialgeschichte", "Burgen und Schlösser", "Mittelalter", "Märkte"])

add("510",
    "Abbruch der Burg auf dem Hausberg (Steine für das Tinzer Schloss 1748) und Beginn Langenberg: Marktflecken 1 1/4 Stunde NNW. von Gera mit Lage, Straßen und Plätzen, 142 Privathäusern und 1453 Einwohnern, Bauweise, Gotteshaus als ehemalige Kapelle der 14 Nothelfer.",
    "Demolition of the castle on the Hausberg (stone used for Tinz palace in 1748) and start of Langenberg: a market town 1 1/4 hours NNW of Gera with its setting, streets and squares, 142 private houses and 1,453 inhabitants, building style, and the church as former chapel of the Fourteen Holy Helpers.",
    ["Langenberg", "Marktflecken", "Hausberg", "Kirche", "Nothelfer", "Einwohner", "Tinz"],
    ["Langenberg", "market town", "Hausberg", "church", "Holy Helpers", "inhabitants", "Tinz"],
    ["Dorf", "Kirchengebäude", "Siedlungsform", "Burgen und Schlösser"])

add("511",
    "Langenberg: Altar von 1486 und Kirchturm von 1502, Grabdenkmäler, die St. Jacobskirche beim Kammergut (Gutsmagazin, 1669–1817 wieder Kirche), Parochie mit Stublach und Pohlitz, Friedhof, vier Pfarrhäuser, Pfarrer von Sifridus 1323 bis Valentin Beutler.",
    "Langenberg: altar of 1486 and church tower of 1502, tombs, the St James church beside the Kammergut (granary, church again 1669–1817), parish with Stublach and Pohlitz, cemetery, four rectories, pastors from Sifridus in 1323 to Valentin Beutler.",
    ["Langenberg", "Jacobskirche", "Kirchturm", "Altar", "Pfarrer", "Friedhof", "Parochie"],
    ["Langenberg", "St James church", "church tower", "altar", "pastor", "cemetery", "parish"],
    ["Kirchengebäude", "Pfarreien", "Denkmal", "Mittelalter"])

add("512",
    "Langenberg: Pfarrer Beatus, Schule mit 281 Kindern, Hospital, Kirchen- und Schulvermögen, Rathaus, Kammergut (v. Eichicht, 1660 Gera), Gasthöfe, Schießhaus, Ziegeleien, Gemeinde der 66 Brauberechtigten mit Vermögen und Schulden.",
    "Langenberg: pastor Beatus, school with 281 pupils, hospital, church and school assets, town hall, Kammergut (v. Eichicht, Gera from 1660), inns, shooting house, brickworks, the commune of the 66 brewing-right holders with assets and debts.",
    ["Langenberg", "Schule", "Hospital", "Rathaus", "Kammergut", "Brauberechtigte", "Gemeindefinanzen"],
    ["Langenberg", "school", "hospital", "town hall", "Kammergut", "brewing-right holders", "municipal finances"],
    ["Schule", "Gemeinden", "Gemeindefinanzen", "Kammergut"])

add("513",
    "Langenberg: Tabelle der Einwohner nach Berufsgruppen 1864 (Industrie 931 Seelen), Weberei mit 112 Meistern, weitere Gewerbe, Märkte, Schießhaus, 1840 Kaltwasserheilanstalt, Flur 1564 2/3 Morgen, Weinbau, Ortsname und Zwergensage.",
    "Langenberg: table of inhabitants by occupational group in 1864 (industry 931 souls), weaving with 112 master weavers, other trades, markets, shooting house, the cold-water cure establishment of 1840, 1,564 2/3 Morgen of fields, viticulture, place name and dwarf legend.",
    ["Langenberg", "Berufsgruppen", "Weberei", "Kaltwasserheilanstalt", "Markt", "Weinbau", "Zwergensage"],
    ["Langenberg", "occupational groups", "weaving", "cold-water cure", "market", "viticulture", "dwarf legend"],
    ["Berufe", "Textilgewerbe", "Märkte", "Sagen"])

add("514",
    "Langenberg: Geschichte des Orts, Landgericht und Rügegericht, der bis 1804 gehaltene Herrn- oder Frohntanz unter der Linde, Marktprivilegien 1505, Verlegung der Regierung wegen der Pest 1610–1612, Kriegsleiden, Fußnoten zu Rolandssäule und Frohntanz.",
    "Langenberg: history of the place, regional court and court of presentment, the lord's or feudal dance held under the linden tree until 1804, market privileges of 1505, relocation of the government because of plague 1610–1612, war suffering, footnotes on the Roland column and the feudal dance.",
    ["Langenberg", "Frohntanz", "Rügegericht", "Landgericht", "Privilegien 1505", "Pest", "Linde"],
    ["Langenberg", "feudal dance", "court of presentment", "regional court", "privileges of 1505", "plague", "linden tree"],
    ["Rechtspflege", "Bräuche", "Territorialgeschichte", "Seuchen"])

add("515",
    "Schluss Langenberg (Pest 1633, Brände 1640, 1755, 1797 und 1838, Stipendien und Gelehrte, Volks-Zeitung 1795, Besuch Kaiser Franz 1813, Sagen) und Beginn Roben: Pfarr- und Kirchdorf 2 Stunden NNW. von Gera, 46 Häuser und 279 Einwohner, früheres Rittergut.",
    "End of Langenberg (plague 1633, fires of 1640, 1755, 1797 and 1838, scholarships and scholars, the Volks-Zeitung of 1795, visit of Emperor Franz in 1813, legends) and start of Roben: a parish village 2 hours NNW of Gera, 46 houses and 279 inhabitants, former manor.",
    ["Langenberg", "Roben", "Stipendium", "Volkszeitung", "Brand", "Pest 1633", "Kaiser Franz"],
    ["Langenberg", "Roben", "scholarship", "popular newspaper", "fire", "plague of 1633", "Emperor Franz"],
    ["Dorf", "Brände", "Stiftungen", "Sagen"])

add("516",
    "Roben: Rittergut (v. Eichicht, Caaschwitz, Steinbrücken), Kirche mit Neubau 1729–1731, Kirchenvermögen 12.670 Thlr., Pfarrer Georg Derre als erster lutherischer Pfarrer, Pfarrbesoldung, Pfarrwohnung 1693, Schule 1711, eingepfarrte Orte.",
    "Roben: manor (v. Eichicht, Caaschwitz, Steinbrücken), church rebuilt 1729–1731, church assets of 12,670 thalers, pastor Georg Derre as first Lutheran pastor, pastor's salary, rectory 1693, school 1711, parish members.",
    ["Roben", "Rittergut", "Kirche", "Georg Derre", "Pfarrei", "Kirchenvermögen", "Reformation"],
    ["Roben", "manor", "church", "Georg Derre", "parish", "church assets", "Reformation"],
    ["Dorf", "Kirchengebäude", "Pfarreien", "Reformation"])

add("517",
    "Schluss Roben (Schule 125 Kinder, Gemeinde, Erwerb in Braunkohlengruben und Saline, Flur 1403 3/10 Morgen, Geschichte seit 1209, Kriegsnöte, Gottfried Weiser) und Beginn Steinbrücken: hochgelegenes Grenzdorf, 42 Häuser, 314 Einwohner, Vieh.",
    "End of Roben (school with 125 pupils, municipality, work in lignite mines and the saltworks, 1,403 3/10 Morgen of fields, history from 1209, war hardships, Gottfried Weiser) and start of Steinbrücken: a high-lying border village, 42 houses, 314 inhabitants, livestock.",
    ["Roben", "Steinbrücken", "Braunkohle", "Schule", "Gemeinde", "Flur", "Siebenjähriger Krieg"],
    ["Roben", "Steinbrücken", "lignite", "school", "municipality", "fields", "Seven Years' War"],
    ["Dorf", "Schule", "Gemeindefinanzen", "Bergbau"])

add("518",
    "Steinbrücken: Rittergut mit Besitzern (v. Schauroth, Heinrich I. von Schleiz, 1719 Solms-Tecklenburg, 1812 v. Metsch, Majorat), Gemeinde ohne Vermögen, Erwerb, Vermögen der Einwohner, Flur 1960 1/2 Morgen, Name und Ansiedlung.",
    "Steinbrücken: manor and its owners (v. Schauroth, Heinrich I of Schleiz, Solms-Tecklenburg in 1719, v. Metsch in 1812, entailed estate), municipality without assets, livelihoods, wealth of the inhabitants, 1,960 1/2 Morgen of fields, name and settlement.",
    ["Steinbrücken", "Rittergut", "Majorat", "Metsch", "Schauroth", "Flur", "Armut"],
    ["Steinbrücken", "manor", "entailed estate", "Metsch", "Schauroth", "fields", "poverty"],
    ["Dorf", "Rittergut", "Genealogie", "Gemeinden"])

add("519",
    "Schluss Steinbrücken (Wüstungen Lichtenau und Rosenhof, Rosenhofsmarkung mit Schlösschen, Braupfannenteiche und Goldsage, ein Ort Hermannsdorf 1364) und Beginn Rusitz: kleines, reiches Bauerndorf 2 Stunden N. von Gera, 20 Häuser, 124 Einwohner, Rittergutsgeschichte.",
    "End of Steinbrücken (deserted villages Lichtenau and Rosenhof, the Rosenhof territory with its small castle mound, the Braupfannen ponds and gold legend, a place called Hermannsdorf in 1364) and start of Rusitz: a small, wealthy farming village 2 hours N of Gera, 20 houses, 124 inhabitants, manor history.",
    ["Lichtenau", "Rosenhof", "Hermannsdorf", "Wüstung", "Rusitz", "Braupfannenteiche", "Sage"],
    ["Lichtenau", "Rosenhof", "Hermannsdorf", "deserted settlement", "Rusitz", "Braupfannen ponds", "legend"],
    ["Wüstung", "Sagen", "Dorf", "Ortsname"])

add("520",
    "Schluss Rusitz (Erwerb, Wohlhabenheit, Flur 1287,87 Morgen, 1121 Kloster Bosau) und Beginn Lessen: Dörfchen am Lestenbächlein 1/2 Stunde SW. von Großaga, 23 Privathäuser, 163 Einwohner, Gemeindebrauhaus, Grundbesitzverhältnisse und Erwerb der Bauernschaft.",
    "End of Rusitz (livelihoods, prosperity, 1,287.87 Morgen of fields, 1121 Bosau monastery) and start of Lessen: a small village on the Lestenbächlein 1/2 hour SW of Großaga, 23 private houses, 163 inhabitants, communal brewhouse, landholdings and the peasants' livelihoods.",
    ["Rusitz", "Lessen", "Großaga", "Kloster Bosau", "Gemeindebrauhaus", "Bauernschaft", "Holzhandel"],
    ["Rusitz", "Lessen", "Großaga", "Bosau monastery", "communal brewhouse", "peasantry", "timber trade"],
    ["Dorf", "Landwirtschaft", "Gemeinden", "Holz"])

add("521",
    "Schluss Lessen (Flur 1401 1/9 Morgen, sorbischer Name, Brand 1843, Sage von der Braupfanne) und Beginn Großaga: ansehnlicher Pfarr-, Kirch- und Jahrmarktsort, fünftgrößter Ort des Bezirks, vier Hauptstraßen vom Markt, 723 Einwohner, Kirche des heiligen Bartholomäus.",
    "End of Lessen (1,401 1/9 Morgen of fields, Sorbian name, fire of 1843, legend of the brewing pan) and start of Großaga: a substantial parish and fair village, fifth-largest place of the district, four main roads radiating from the market, 723 inhabitants, church of St Bartholomew.",
    ["Lessen", "Großaga", "Jahrmarkt", "Bartholomäus", "Pfarrdorf", "Marktplatz", "Braupfanne"],
    ["Lessen", "Großaga", "annual fair", "St Bartholomew", "parish village", "market square", "brewing pan"],
    ["Dorf", "Märkte", "Kirchengebäude", "Sagen"])

add("522",
    "Großaga: Kirche (Kreuzgewölbe, Glocke von 1502, Grabdenksteine Metsch), eingepfarrte Orte, Frohnen und Decem, Kirchenvermögen, Haupt- und Nothgottesacker (Pest 1639–1641), katholische und erste lutherische Pfarrer, Widerstand gegen die Reformation.",
    "Großaga: church (groin vault, bell of 1502, Metsch grave slabs), parish members, feudal services and tithes, church assets, main and emergency cemeteries (plague 1639–1641), Catholic and first Lutheran pastors, resistance to the Reformation.",
    ["Großaga", "Kirche", "Glocke", "Pfarrer", "Reformation", "Friedhof", "Pest"],
    ["Großaga", "church", "bell", "pastor", "Reformation", "cemetery", "plague"],
    ["Kirchengebäude", "Pfarreien", "Reformation", "Seuchen"])

add("523",
    "Großaga: Pfarrwohnung 1745–1749, Pfarreieinkünfte, Schule mit 222 Kindern (1842 zweiter Lehrer), Rittergut (v. Etzdorf, Wolframsdorf, 1711 Kammergut) und die Belagerung eines Pächters, Gasthöfe, Gemeinde, Grundbesitz und Berufsgliederung.",
    "Großaga: rectory 1745–1749, parish revenues, school with 222 pupils (second teacher in 1842), manor (v. Etzdorf, Wolframsdorf, Kammergut from 1711) and the siege of a tenant, inns, municipality, landholdings and occupational structure.",
    ["Großaga", "Pfarrwohnung", "Schule", "Kammergut", "Etzdorf", "Wolframsdorf", "Gemeinde"],
    ["Großaga", "rectory", "school", "Kammergut", "Etzdorf", "Wolframsdorf", "municipality"],
    ["Schule", "Kammergut", "Gemeinden", "Pfarreien"])

add("524",
    "Großaga: Handwerker, Taglöhner, Vermögen und Sitten der Einwohner, der Appelsmarkt (Ablassmarkt am Bartholomäustag, 1678 erneuert), Lesebibliothek, Flur 1943 Morgen, Flurnamen, sorbischer Ursprung, Pest 1639–1641.",
    "Großaga: craftsmen, day labourers, wealth and morals of the inhabitants, the Appelsmarkt (indulgence fair on St Bartholomew's day, revived 1678), lending library, 1,943 Morgen of fields, field names, Sorbian origin, plague 1639–1641.",
    ["Großaga", "Appelsmarkt", "Ablassmarkt", "Handwerk", "Flurnamen", "Pest", "Lesebibliothek"],
    ["Großaga", "Appelsmarkt", "indulgence fair", "crafts", "field names", "plague", "lending library"],
    ["Märkte", "Handwerk", "Flurnamen", "Seuchen"])

add("525",
    "Schluss Großaga (Brände 1840–1865, Wachbusch, Cariuseiche, Sagen) und Beginn Kleinaga: Dorf 1/8 Stunde südlich von Großaga mit Unterdorf und Froschweide, 40 Privathäuser, 267 Einwohner, Kammergut und Forsthaus, Anfänge des Ritterguts.",
    "End of Großaga (fires 1840–1865, Wachbusch, Carius oak, legends) and start of Kleinaga: a village 1/8 hour south of Großaga with a lower village and Froschweide, 40 private houses, 267 inhabitants, Kammergut and forester's house, origins of the manor.",
    ["Großaga", "Kleinaga", "Froschweide", "Kammergut", "Forsthaus", "Sagen", "Cariuseiche"],
    ["Großaga", "Kleinaga", "Froschweide", "Kammergut", "forester's house", "legends", "Carius oak"],
    ["Dorf", "Sagen", "Kammergut", "Brände"])

add("526",
    "Kleinaga: Kammergut (v. Etzdorf, v. Metsch, 1697 an die Landesherrschaft), Privatkapelle und Erbbegräbnis, Gasthof, Gemeinden Kleinaga und Froschweide, Grundbesitz, Berufsgliederung, Vermögen und Sitten der Einwohner.",
    "Kleinaga: Kammergut (v. Etzdorf, v. Metsch, to the ruling house in 1697), private chapel and family burial place, inn, the communes of Kleinaga and Froschweide, landholdings, occupational structure, wealth and morals of the inhabitants.",
    ["Kleinaga", "Kammergut", "Froschweide", "Metsch", "Tümpling", "Kapelle", "Gemeinde"],
    ["Kleinaga", "Kammergut", "Froschweide", "Metsch", "Tümpling", "chapel", "municipality"],
    ["Dorf", "Kammergut", "Gemeinden", "Genealogie"])

add("527",
    "Schluss Kleinaga (Flur 1731 5/6 Morgen, Braunkohlenwerk 1821–1864, Nonnenklöster-Sage, Brände 1765 und 1811 in Froschweide), Wüstung Rödel (nur sechs Gehöfte, Bewohner siedelten nach Kleinaga) und Beginn Reichenbach: Dörfchen 3/4 Stunde südlich von Großaga mit 18 Privathäusern.",
    "End of Kleinaga (1,731 5/6 Morgen of fields, lignite mine 1821–1864, convent legend, fires of 1765 and 1811 at Froschweide), deserted village Rödel (only six farmsteads, inhabitants moved to Kleinaga) and start of Reichenbach: a small village 3/4 hour south of Großaga with 18 private houses.",
    ["Kleinaga", "Rödel", "Wüstung", "Braunkohlenwerk", "Froschweide", "Reichenbach", "Rügegericht"],
    ["Kleinaga", "Rödel", "deserted settlement", "lignite mine", "Froschweide", "Reichenbach", "court of presentment"],
    ["Dorf", "Wüstung", "Bergbau", "Brände"])

add("528",
    "Schluss Reichenbach (Statistik, Kirchenzugehörigkeit nach Großaga, Rittergut und Freigut bis zum 19. Jahrhundert, Braunkohlengrube seit 1851, Flur 747 1/2 Morgen, Brand des Gemeindehauses 1866) und Beginn des Straßenwirthshauses zum goldenen Kranich an der Gera-Leipziger Heerstraße.",
    "End of Reichenbach (statistics, church ties to Großaga, manor and free estate until the 19th century, lignite pit since 1851, 747 1/2 Morgen of fields, fire of the community house in 1866) and start of the wayside inn Zum goldenen Kranich on the Gera–Leipzig highway.",
    ["Reichenbach", "goldener Kranich", "Wirtshaus", "Braunkohle", "Heerstraße", "Gera-Leipzig", "Freigut"],
    ["Reichenbach", "Golden Crane", "inn", "lignite", "highway", "Gera–Leipzig", "free estate"],
    ["Dorf", "Gasthof", "Verkehr", "Bergbau"])

add("529",
    "Gasthof zum goldenen Kranich (Trotz, 1751) gegenüber dem altenburgischen Wachholderbusch und die Sage vom abgewiesenen Hausknecht; Beginn Seeligenstädt, Dörfchen 2 1/2 Stunden fast nördlich von Gera, 16 Häuser, 95 Einwohner, Kammergutsvorwerk (ehemaliges Rittergut).",
    "The inn Zum goldenen Kranich ('Trotz', 1751) opposite the Altenburg inn Wachholderbusch and the legend of the rejected servant; start of Seeligenstädt, a small village 2 1/2 hours almost due north of Gera, 16 houses, 95 inhabitants, Kammergut farm (former manor).",
    ["goldener Kranich", "Trotz", "Wachholderbusch", "Straßenwirtshaus", "Seeligenstädt", "Kammergutsvorwerk", "Sage"],
    ["Golden Crane", "Trotz", "Wachholderbusch", "wayside inn", "Seeligenstädt", "Kammergut farm", "legend"],
    ["Gasthof", "Sagen", "Dorf", "Kammergut"])

add("530",
    "Schluss Seeligenstädt (Gemeinde, Grundbesitz, Flur 524 1/2 Morgen, Name von der Hochebene Selig, Stadtsage) und Beginn Hermsdorf: hoch gelegenes Dorf an der preußischen Grenze, 3 Stunden NNO. von Gera, 26 Privathäuser, 199 Einwohner, kirchlich nach Heukewalde.",
    "End of Seeligenstädt (municipality, landholdings, 524 1/2 Morgen of fields, name derived from the Selig plateau, legend of a former town) and start of Hermsdorf: a high-lying village at the Prussian border, 3 hours NNE of Gera, 26 private houses, 199 inhabitants, church ties to Heukewalde.",
    ["Seeligenstädt", "Hermsdorf", "Heukewalde", "preußische Grenze", "Ortsname", "Flur", "Schule"],
    ["Seeligenstädt", "Hermsdorf", "Heukewalde", "Prussian border", "place name", "fields", "school"],
    ["Dorf", "Ortsname", "Gemeinden", "Lage und Grenzen"])

add("531",
    "Schluss Hermsdorf (aufgehobene Patrimonialgerichte, Gemeinde, Erwerb, Flur 1010,96 Morgen, Geschichte) und Beginn Wernsdorf: kleines hochgelegenes Kirch- und Bauerndorf 2 1/2 Stunden NNO. von Gera, Filial von Hirschfeld, 22 Privathäuser, 161 Einwohner.",
    "End of Hermsdorf (abolished patrimonial courts, municipality, livelihoods, 1,010.96 Morgen of fields, history) and start of Wernsdorf: a small high-lying church and farming village 2 1/2 hours NNE of Gera, branch of Hirschfeld, 22 private houses, 161 inhabitants.",
    ["Hermsdorf", "Wernsdorf", "Hirschfeld", "Patrimonialgericht", "Flur", "Kirche", "Bauerndorf"],
    ["Hermsdorf", "Wernsdorf", "Hirschfeld", "patrimonial court", "fields", "church", "farming village"],
    ["Dorf", "Rechtspflege", "Gemeindefinanzen", "Kirchengebäude"])

add("532",
    "Schluss Wernsdorf (Kirche mit Erneuerung 1859, Schule 1839 für drei Orte mit 91 Kindern, Gemeinde, Ackerbau, Flur 1185 1/3 Morgen, Brände 1774 und 1827) und Hinweis auf die wüste Markung Betzdorf.",
    "End of Wernsdorf (church renovated in 1859, school of 1839 for three villages with 91 pupils, municipality, farming, 1,185 1/3 Morgen of fields, fires of 1774 and 1827) with a reference to the deserted territory Betzdorf.",
    ["Wernsdorf", "Kirche", "Schule 1839", "Hirschfeld", "Söllmnitz", "Flur", "Blitzschlag"],
    ["Wernsdorf", "church", "school of 1839", "Hirschfeld", "Söllmnitz", "fields", "lightning"],
    ["Dorf", "Schule", "Kirchengebäude", "Brände"])

add("533",
    "Kretzschwitz: Dörfchen auf der Hochebene mit Rittergut, 18 Privathäuser, 123 Einwohner, kirchlich nach Dorna, Besitzer (v. Söllmnitz, v. Schauroth, Winkler, v. Ende, 1841 v. Brandenstein), Gemeinde, Ackerbau, Flur 1292,14 Morgen.",
    "Kretzschwitz: a small plateau village with a manor, 18 private houses, 123 inhabitants, belonging to Dorna for church affairs, owners (v. Söllmnitz, v. Schauroth, Winkler, v. Ende, v. Brandenstein from 1841), municipality, farming, 1,292.14 Morgen of fields.",
    ["Kretzschwitz", "Rittergut", "Winkler", "Dorna", "Söllmnitz", "Ackerbau", "Flur"],
    ["Kretzschwitz", "manor", "Winkler", "Dorna", "Söllmnitz", "farming", "fields"],
    ["Dorf", "Rittergut", "Landwirtschaft", "Genealogie"])

add("534",
    "Schluss Kretzschwitz (Zins an Großenstein 1381, Opferstätten-Sage), Wüstung Wolstieg (1364 noch Dörfchen) und Beginn Söllmnitz: Kirchdorf aus drei Häusergruppen (Groß- und Kleinsöllmnitz, Lauenhain), 342 Einwohner, Rittergut der v. Selmenitz, Luther-Brief an Felicitas v. Söllmnitz.",
    "End of Kretzschwitz (rent to Großenstein 1381, sacrificial-site legend), deserted village Wolstieg (still a small village in 1364) and start of Söllmnitz: a church village of three groups of houses (Groß- and Kleinsöllmnitz, Lauenhain), 342 inhabitants, manor of the v. Selmenitz, Luther's letter to Felicitas v. Söllmnitz.",
    ["Kretzschwitz", "Wolstieg", "Söllmnitz", "Selmenitz", "Rittergut", "Luther", "Lauenhain"],
    ["Kretzschwitz", "Wolstieg", "Söllmnitz", "Selmenitz", "manor", "Luther", "Lauenhain"],
    ["Wüstung", "Dorf", "Rittergut", "Reformation"])

add("535",
    "Söllmnitz: Besitzerfolge des Ritterguts, Gründung der Kirche Ende des 13. Jahrhunderts und Patronat, Pfarrei und Verbindung mit Hirschfeld, gotische Kirche, Glocken, Friedhof, Schule, Gemeindevermögen, Grundbesitz, Gewerbe und Brennerei und Brauerei des Guts.",
    "Söllmnitz: succession of owners of the manor, founding of the church in the late 13th century and its patronage, parish and link with Hirschfeld, Gothic church, bells, cemetery, school, municipal assets, landholdings, trades and the manor's distillery and brewery.",
    ["Söllmnitz", "Kirche", "Patronat", "Hirschfeld", "Selmenitz", "Brennerei", "Brauerei"],
    ["Söllmnitz", "church", "patronage", "Hirschfeld", "Selmenitz", "distillery", "brewery"],
    ["Kirchengebäude", "Pfarreien", "Rittergut", "Brauerei"])

add("536",
    "Schluss Söllmnitz (Einwohner, Flur 1161 7/10 Morgen, 1121 Bosau, Brand 1828), Lauenhain (fünf Bauernhöfe), Wüstung Betzdorf (Ludolph von Beitzdorf 1125) und Beginn Hirschfeld: Pfarr-, Kirch- und Grenzdorf 2 1/2 Stunden NNO. von Gera am Ursprung der Schnauder.",
    "End of Söllmnitz (inhabitants, 1,161 7/10 Morgen of fields, 1121 Bosau, fire of 1828), Lauenhain (five farms), deserted village Betzdorf (Ludolph of Beitzdorf in 1125) and start of Hirschfeld: a parish and border village 2 1/2 hours NNE of Gera at the source of the Schnauder.",
    ["Söllmnitz", "Lauenhain", "Betzdorf", "Wüstung", "Hirschfeld", "Schnauder", "Flurnamen"],
    ["Söllmnitz", "Lauenhain", "Betzdorf", "deserted settlement", "Hirschfeld", "Schnauder", "field names"],
    ["Dorf", "Wüstung", "Flurnamen", "Brände"])

add("537",
    "Hirschfeld: 228 Einwohner, gemischte Landeshoheit (Amt Ronneburg, altenburgische Grundstücke), Hoheitsausgleichungsvertrag vom 30. Mai 1868, Parochie mit drei Töchterkirchen (842 Seelen), Kirche, Taufstein 1663, Turm 1832, Grabstätten und Pfarrer Müller.",
    "Hirschfeld: 228 inhabitants, mixed sovereignty (Ronneburg district, Altenburg parcels), the sovereignty adjustment treaty of 30 May 1868, parish with three daughter churches (842 souls), church, font of 1663, tower of 1832, graves and pastor Müller.",
    ["Hirschfeld", "Landeshoheit", "Hoheitsausgleichungsvertrag", "Parochie", "Kirche", "Taufstein", "Ronneburg"],
    ["Hirschfeld", "sovereignty", "sovereignty adjustment treaty", "parish", "church", "baptismal font", "Ronneburg"],
    ["Verwaltung", "Kirchengebäude", "Pfarreien", "Territorialgeschichte"])

add("538",
    "Hirschfeld: erster lutherischer Pfarrer Fatsch, Pfarrhaus, Pfarrbesoldung, Schule 1838/39 mit 72 Kindern, Gemeinde, Grundbesitz, Ackerbau, Handwerker, wohlhabende Bauern, Flur 1417 2/15 Morgen.",
    "Hirschfeld: first Lutheran pastor Fatsch, rectory, pastor's income, school of 1838/39 with 72 pupils, municipality, landholdings, farming, craftsmen, prosperous farmers, 1,417 2/15 Morgen of fields.",
    ["Hirschfeld", "Pfarrer", "Pfarrhaus", "Schule", "Gemeinde", "Bauern", "Flur"],
    ["Hirschfeld", "pastor", "rectory", "school", "municipality", "farmers", "fields"],
    ["Pfarreien", "Schule", "Landwirtschaft", "Gemeindefinanzen"])

add("539",
    "Schluss Hirschfeld (Flurnamen, Pflege Langenberg, Streit um das Pfarrholz) und Beginn Bethenhausen: zweiherriges Kirch- und Grenzdörflein 2 1/4 Stunden NO. von Gera im Bramthal, altenburgischer und reußischer Teil, 111 Einwohner im reußischen Teil, Gasthof zum goldenen Hahn, Staatsverträge 1847 und 1868.",
    "End of Hirschfeld (field names, Pflege Langenberg, dispute over the parish woods) and start of Bethenhausen: a village shared between Reuss and Altenburg, 2 1/4 hours NE of Gera in the Bramthal, 111 inhabitants in the Reuss part, inn Zum goldenen Hahn, state treaties of 1847 and 1868.",
    ["Hirschfeld", "Bethenhausen", "zweiherrig", "Bramthal", "goldener Hahn", "Staatsvertrag 1868", "Landeshoheit"],
    ["Hirschfeld", "Bethenhausen", "shared lordship", "Bramthal", "Golden Cock", "state treaty of 1868", "sovereignty"],
    ["Dorf", "Territorialgeschichte", "Verwaltung", "Gasthof"])

add("540",
    "Schluss Bethenhausen (Kirche 1777, Glocke von 1483, Gemeinde, Ackerbau, altenburgische Tracht, Flur 540,95 Morgen) und Beginn Naundorf: ansehnliches Kirch- und Grenzdorf, Stammort der Familie v. Naundorf, 2 Stunden NO. von Gera, Lage an der Ronneburg-Zeitzer Straße.",
    "End of Bethenhausen (church of 1777, bell of 1483, municipality, farming, Altenburg costume, 540.95 Morgen of fields) and start of Naundorf: a substantial church and border village, ancestral seat of the v. Naundorf family, 2 hours NE of Gera on the Ronneburg–Zeitz road.",
    ["Bethenhausen", "Naundorf", "Tracht", "Kirche", "Glocke", "Familie v. Naundorf", "Flur"],
    ["Bethenhausen", "Naundorf", "costume", "church", "bell", "v. Naundorf family", "fields"],
    ["Dorf", "Kleidung und Tracht", "Kirchengebäude", "Rittergut"])

add("541",
    "Naundorf: Höhenlage, 62 Privathäuser und 366 Einwohner, Majoratsgut der v. Naundorf (Herrnhaus 1685), Kirche als Filial von Großenstein (Kapelle 1384, Neubau 1821 nach Brand 1810), Schule in Großenstein, Mühlen, Gemeinde und Grundbesitz.",
    "Naundorf: elevation, 62 private houses and 366 inhabitants, entailed manor of the v. Naundorf (manor house 1685), church as a branch of Großenstein (chapel 1384, new building 1821 after the 1810 fire), school at Großenstein, mills, municipality and landholdings.",
    ["Naundorf", "Majorat", "Familie v. Naundorf", "Kirche", "Großenstein", "Erlichsmühle", "Brand 1810"],
    ["Naundorf", "entailed estate", "v. Naundorf family", "church", "Großenstein", "Erlichsmühle", "fire of 1810"],
    ["Dorf", "Rittergut", "Kirchengebäude", "Mühlen"])

add("542",
    "Schluss Naundorf (Handwerker und Taglohn, Vermögenslage, Flur 932 1/5 Morgen im Steuerwert von 162.720 Thlr., Brand 10. August 1810) und Beginn Caasen: Plateaudörfchen 1/4 Stunde NO. von Groitschen, 18 Privathäuser, 108 Einwohner, Rittergut, Kirche und Schule in Groitschen.",
    "End of Naundorf (craftsmen and day labour, wealth situation, 932 1/5 Morgen of fields with a tax value of 162,720 thalers, fire of 10 August 1810) and start of Caasen: a small plateau village 1/4 hour NE of Groitschen, 18 private houses, 108 inhabitants, manor, church and school at Groitschen.",
    ["Naundorf", "Caasen", "Handwerk", "Steuerwert", "Brand 1810", "Rittergut", "Groitschen"],
    ["Naundorf", "Caasen", "crafts", "tax value", "fire of 1810", "manor", "Groitschen"],
    ["Dorf", "Handwerk", "Brände", "Rittergut"])

add("543",
    "Schluss Caasen (Besitzer des Ritterguts, Gemeinde, ärmliche Verhältnisse, Flur 347 8/15 Morgen, Erschießung 1806) und Beginn Groitschen: kleines Kirch- und Grenzdorf im oberen Bramthal, 94 Einwohner, mittelalterliche Pfarrei, Filial von Dorna, Streit um Pfarreinkünfte.",
    "End of Caasen (owners of the manor, municipality, poor conditions, 347 8/15 Morgen of fields, shooting in 1806) and start of Groitschen: a small church and border village in the upper Bramthal, 94 inhabitants, medieval parish, branch of Dorna, dispute over parish revenues.",
    ["Caasen", "Groitschen", "Rittergut", "Pfarrei", "Dorna", "Bramthal", "Pfarreinkünfte"],
    ["Caasen", "Groitschen", "manor", "parish", "Dorna", "Bramthal", "parish revenues"],
    ["Dorf", "Pfarreien", "Rittergut", "Napoleonische Kriege"])

add("544",
    "Schluss Groitschen (Kirche 1785/86, Schule 1842/43 für vier Orte mit 80 Kindern, Gemeindefinanzen, Bauerngüter, Flur 527 9/10 Morgen, Blitzschlag 1829) und Beginn Waaswitz, das kleinste Kirch- und Grenzdörfchen des Fürstentums.",
    "End of Groitschen (church 1785/86, school of 1842/43 for four villages with 80 pupils, municipal finances, farms, 527 9/10 Morgen of fields, lightning fire of 1829) and start of Waaswitz, the smallest church and border village of the principality.",
    ["Groitschen", "Waaswitz", "Kirche", "Schule", "Gemeindefinanzen", "Flur", "Dorna"],
    ["Groitschen", "Waaswitz", "church", "school", "municipal finances", "fields", "Dorna"],
    ["Dorf", "Kirchengebäude", "Schule", "Gemeindefinanzen"])

add("545",
    "Waaswitz: 47 Einwohner in fünf Bauernhöfen, Kirchlein von 1771 als Filial der altenburgischen Pfarrei Corbußen, Kirchen- und Schulverhältnisse, Gemeindevermögen, Freigut, Hoheitsausgleichungsvertrag von 1868 (Flur durchaus reußisch).",
    "Waaswitz: 47 inhabitants in five farms, small church of 1771 as a branch of the Altenburg parish of Corbußen, church and school arrangements, municipal assets, free estate, the 1868 sovereignty adjustment treaty (fields now wholly Reuss).",
    ["Waaswitz", "Corbußen", "Kirche", "Altenburg", "Hoheitsausgleichung", "Freigut", "Schulverhältnisse"],
    ["Waaswitz", "Corbußen", "church", "Altenburg", "sovereignty adjustment", "free estate", "school arrangements"],
    ["Dorf", "Kirchengebäude", "Pfarreien", "Territorialgeschichte"])

add("546",
    "Schluss Waaswitz (Flur 531 2/5 Morgen, sorbischer Ursprung) und Beginn Culm: geringes Dörfchen im Bramthal, 30 Privathäuser, 194 Einwohner, Rittergut mit Besitzerfolge 1534–1818 (Rossau, Oppel, Beust, Schmalz), Schule in Groitschen, Weinmühle.",
    "End of Waaswitz (531 2/5 Morgen of fields, Sorbian origin) and start of Culm: a modest village in the Bramthal, 30 private houses, 194 inhabitants, manor with owners 1534–1818 (Rossau, Oppel, Beust, Schmalz), school at Groitschen, Weinmühle.",
    ["Waaswitz", "Culm", "Rittergut", "Besitzer", "Weinmühle", "Branntweinbrennerei", "Groitschen"],
    ["Waaswitz", "Culm", "manor", "owners", "Weinmühle", "distillery", "Groitschen"],
    ["Dorf", "Rittergut", "Mühlen", "Genealogie"])

add("547",
    "Schluss Culm (Gemeindevermögen, Erwerb, Flur 691 9/10 Morgen, Menschenknochen auf dem Weinberg 1816, Tod von Wolf Adam Oppel 1643) und Beginn Zschippach: Kirch- und Grenzdörfchen 1/2 Stunde östlich von Dorna, 170 Einwohner, Rittergut (Söllmnitz, Schauroth, Ende, Koppy, Zehmen), Kirchlein.",
    "End of Culm (municipal assets, livelihoods, 691 9/10 Morgen of fields, human bones on the Weinberg in 1816, death of Wolf Adam Oppel in 1643) and start of Zschippach: a church and border village 1/2 hour east of Dorna, 170 inhabitants, manor (Söllmnitz, Schauroth, Ende, Koppy, Zehmen), small church.",
    ["Culm", "Zschippach", "Rittergut", "Zehmen", "Oppel", "Dreißigjähriger Krieg", "Weinberg"],
    ["Culm", "Zschippach", "manor", "Zehmen", "Oppel", "Thirty Years' War", "Weinberg hill"],
    ["Dorf", "Rittergut", "Dreißigjähriger Krieg", "Genealogie"])

add("548",
    "Zschippach: Ablösung der Frohnen und Lehen 1840, Kirche als Filial von Dorna (1645 niedergebrannt, Turm 1722), Schule in Dorna mit 25 Kindern, drei Mühlen (Knappen-, Zoitz-, Fuchsmühle), Gemeinde, Grundbesitz, Berufe, Flur 919,87 Morgen.",
    "Zschippach: buy-out of feudal dues and fiefs in 1840, church as a branch of Dorna (burned down in 1645, tower 1722), school at Dorna with 25 pupils, three mills (Knappen-, Zoitz-, Fuchsmühle), municipality, landholdings, occupations, 919.87 Morgen of fields.",
    ["Zschippach", "Frohnen", "Kirche", "Dorna", "Mühlen", "Knappenmühle", "Flur"],
    ["Zschippach", "feudal dues", "church", "Dorna", "mills", "Knappenmühle", "fields"],
    ["Dorf", "Mühlen", "Kirchengebäude", "Gemeindefinanzen"])

add("549",
    "Brände in Zschippach (1802, 1828, 1834, 1836) und Beginn Dorna: wichtiges Kirch- und Grenzdörfchen 1 1/4 Stunde NO. von Gera im Bramthal, 41 Privathäuser, 285 Einwohner, Rittergut mit Besitzerfolge (Schauroth, Naundorf, Weißenbach, Müller, Kahnt), Mutterkirche als frühe Missionsstätte, Petersberg.",
    "Fires at Zschippach (1802, 1828, 1834, 1836) and start of Dorna: an important church and border village 1 1/4 hours NE of Gera in the Bramthal, 41 private houses, 285 inhabitants, manor with succession of owners (Schauroth, Naundorf, Weißenbach, Müller, Kahnt), mother church as an early mission station, Petersberg.",
    ["Zschippach", "Dorna", "Rittergut", "Mutterkirche", "Petersberg", "Weißenbach", "Bramthal"],
    ["Zschippach", "Dorna", "manor", "mother church", "Petersberg", "Weißenbach", "Bramthal"],
    ["Dorf", "Rittergut", "Kirchengebäude", "Brände"])

add("550",
    "Dorna: Kirche mit Familienkapellen, Altarheiligenschrein vom Ende des 15. Jahrhunderts, Glocken, Kirchenvermögen, Parochie mit 1296 Seelen und Filialen, Pfarrer, Pfarrei von 1772/73, Schule (an 125 Kinder), Stiftung Leers.",
    "Dorna: church with family chapels, altarpiece shrine from the late 15th century, bells, church assets, parish of 1,296 souls with branch churches, pastors, rectory of 1772/73, school (about 125 pupils), the Leers foundation.",
    ["Dorna", "Kirche", "Altarschrein", "Parochie", "Pfarrer", "Schule", "Leers-Stiftung"],
    ["Dorna", "church", "altarpiece shrine", "parish", "pastor", "school", "Leers foundation"],
    ["Kirchengebäude", "Pfarreien", "Schule", "Stiftungen"])

add("551",
    "Dorna: Stiftungen für Schule und Kirche, Gasthäuser, Türkenmühle, Gemeinde, Grundbesitz, Erwerb (Maurer, Porzellanmaler), Vermögenslage, Flur 748 5/8 Morgen, Ortsname und Deutung des Petersbergs als Thorsberg, Obergerichte, Dreißigjähriger Krieg.",
    "Dorna: endowments for school and church, inns, Türkenmühle, municipality, landholdings, occupations (masons, porcelain painters), wealth situation, 748 5/8 Morgen of fields, place name and interpretation of the Petersberg as Thor's hill, jurisdiction, Thirty Years' War.",
    ["Dorna", "Petersberg", "Thorsberg", "Türkenmühle", "Porzellanmaler", "Ortsname", "Stiftung"],
    ["Dorna", "Petersberg", "Thor's hill", "Türkenmühle", "porcelain painters", "place name", "foundation"],
    ["Ortsname", "Mühlen", "Berufe", "Stiftungen"])

add("552",
    "Schluss Dorna (Brände 1707, 1848, Plünderung 1806, Kremel, Wüstenhain als Rest der Orte Negaz, Grenzvertrag 1807/1868) und Beginn Negis: kleines Bauern- und Grenzdorf 1/2 Stunde NNW. von Dorna, 13 Häuser, 93 Einwohner, Freigut, Gemeinde.",
    "End of Dorna (fires 1707 and 1848, plundering in 1806, Kremel hill, Wüstenhain as remnant of the places Negaz, boundary agreement of 1807/1868) and start of Negis: a small farming and border village 1/2 hour NNW of Dorna, 13 houses, 93 inhabitants, free estate, municipality.",
    ["Dorna", "Wüstenhain", "Kremel", "Negis", "Landesgrenze", "Grenzvertrag", "Freigut"],
    ["Dorna", "Wüstenhain", "Kremel", "Negis", "state border", "boundary treaty", "free estate"],
    ["Dorf", "Wüstung", "Lage und Grenzen", "Brände"])

add("553",
    "Schluss Negis (Dienstboten, Flur 920 3/10 Morgen, 1121 Nigaune und Kloster Bosau, Krieg 1631) und Beginn Schwaara: Pfarrkirchdorf 1 Stunde NO. von Gera im schwaarschen Grund, Ortsteile Schwaara und Bauschke, 185 Einwohner, Kirche mit Sakristei.",
    "End of Negis (servants, 920 3/10 Morgen of fields, 1121 Nigaune and Bosau monastery, war of 1631) and start of Schwaara: a parish village 1 hour NE of Gera in the Schwaara valley, hamlets Schwaara and Bauschke, 185 inhabitants, church with vestry.",
    ["Negis", "Schwaara", "Bauschke", "Kloster Bosau", "Pfarrkirchdorf", "Kirche", "Flur"],
    ["Negis", "Schwaara", "Bauschke", "Bosau monastery", "parish village", "church", "fields"],
    ["Dorf", "Kirchengebäude", "Pfarreien", "Urkunden"])

add("554",
    "Schwaara: Kollatur, Pfarrer Caspar Frank, Schwesterkirche Trebnitz, Schule in Trebnitz mit 29 Kindern, Gemeindefinanzen, Berufe, Flur 1385 Morgen, sorbischer Anbau, Vögte von Gera, Frohnen und Hundedecem.",
    "Schwaara: right of presentation, pastor Caspar Frank, sister church Trebnitz, school at Trebnitz with 29 pupils, municipal finances, occupations, 1,385 Morgen of fields, Sorbian settlement, Vögte of Gera, feudal services and Hundedecem.",
    ["Schwaara", "Pfarrer", "Trebnitz", "Hundedecem", "Frohnen", "Vögte von Gera", "Flur"],
    ["Schwaara", "pastor", "Trebnitz", "Hundedecem", "feudal services", "Vögte of Gera", "fields"],
    ["Pfarreien", "Gemeindefinanzen", "Vögte von Weida", "Landwirtschaft"])

add("555",
    "Schluss Schwaara (Streit um Zinsen 1486, Gefecht 1640, Brände, Kupferschächte, Sage von Großmutter Stehfest), Wüstung Werteln (1260, 1384, 1640 zerstört) und Beginn Trebnitz: Kirch- und Grenzdorf 3/4 Stunde NO. von Gera, 38 Privathäuser, 256 Einwohner.",
    "End of Schwaara (dispute over rents in 1486, skirmish of 1640, fires, copper shafts, legend of Grandmother Stehfest), deserted village Werteln (1260, 1384, destroyed 1640) and start of Trebnitz: a church and border village 3/4 hour NE of Gera, 38 private houses, 256 inhabitants.",
    ["Schwaara", "Werteln", "Bartholdisdorf", "Trebnitz", "Wüstung", "Kupfer", "Sage"],
    ["Schwaara", "Werteln", "Bartholdisdorf", "Trebnitz", "deserted settlement", "copper", "legend"],
    ["Wüstung", "Dorf", "Sagen", "Dreißigjähriger Krieg"])

add("556",
    "Trebnitz: Nikolauskirche und Ausbau 1672–1844, Schwesterkirche von Schwaara, Schule mit 70 Kindern (Trebnitz, Schwaara, Laasen), Gemeinde mit 24 Morgen Anger, Bauerngüter, Gewerbe, Flur 1720 3/5 Morgen, Wüstungen Zoche, Werteln und Speutewitz, Freigut.",
    "Trebnitz: St Nicholas church and its expansion 1672–1844, sister church of Schwaara, school with 70 pupils (Trebnitz, Schwaara, Laasen), commune with 24 Morgen of common green, farms, trades, 1,720 3/5 Morgen of fields, deserted villages Zoche, Werteln and Speutewitz, free estate.",
    ["Trebnitz", "Kirche", "Schule", "Laasen", "Schwaara", "Wüstungen", "Flur"],
    ["Trebnitz", "church", "school", "Laasen", "Schwaara", "deserted settlements", "fields"],
    ["Dorf", "Kirchengebäude", "Schule", "Gemeindefinanzen"])

add("557",
    "Schluss Trebnitz (Frohnen, Bergbau auf Kupfer und Silber um 1550, Brände 1633 und 1809), Wüstung Zoche (1534 nur noch Vorwerk) und Beginn der Wüstung Speutewitz mit Burg, Geschichte unter den v. Tegwitz (1385 an Gera) und Sagen.",
    "End of Trebnitz (feudal services, copper and silver mining around 1550, fires of 1633 and 1809), deserted village Zoche (only a Vorwerk by 1534) and start of the deserted village Speutewitz with its castle, history under the v. Tegwitz (to Gera in 1385) and legends.",
    ["Trebnitz", "Zoche", "Speutewitz", "Bergbau", "Burg", "Tegwitz", "Wüstung"],
    ["Trebnitz", "Zoche", "Speutewitz", "mining", "castle", "Tegwitz", "deserted settlement"],
    ["Wüstung", "Bergbau", "Burgen und Schlösser", "Sagen"])

add("558",
    "Schluss Speutewitz (Klostergüter, Hasensäule) und Laasen: Kammergut mit Zeile von 13 Kleinhäusern 3/4 Stunde NO. von Gera, 119 Einwohner, Herrnhaus mit alten Wehrresten, Taglöhner, Flur 610 7/9 Morgen, Besitzerfolge seit 1333 bis zum Kauf durch Landesherrin Dorothea 1574.",
    "End of Speutewitz (monastery estates, the Hasensäule sign) and Laasen: a Kammergut with a row of 13 cottages 3/4 hour NE of Gera, 119 inhabitants, manor house with old fortified remains, day labourers, 610 7/9 Morgen of fields, owners from 1333 until the purchase by the ruling consort Dorothea in 1574.",
    ["Speutewitz", "Laasen", "Kammergut", "Dorothea", "Taglöhner", "Wehrbau", "Cronswitz"],
    ["Speutewitz", "Laasen", "Kammergut", "Dorothea", "day labourers", "fortified building", "Cronswitz"],
    ["Wüstung", "Dorf", "Kammergut", "Burgen und Schlösser"])

add("559",
    "Schluss Laasen (Aufenthalte der Herrschaft, Betstube Heinrichs XXV., Steinertsbrunnen) und Beginn Leumnitz: freundliches Pfarr-, Kirch- und Grenzdorf 3/8 Stunde östlich von Gera, 45 Privathäuser, 387 Einwohner, Rittergut mit Besitzern, Kapelle und Kirche (1604 Filial von Zwötzen).",
    "End of Laasen (stays of the ruling family, prayer room of Heinrich XXV, Steinerts spring) and start of Leumnitz: a friendly parish and border village 3/8 hour east of Gera, 45 private houses, 387 inhabitants, manor and its owners, chapel and church (branch of Zwötzen from 1604).",
    ["Laasen", "Leumnitz", "Rittergut", "Kirche", "Zwötzen", "Heinrich XXV.", "Schellsechs"],
    ["Laasen", "Leumnitz", "manor", "church", "Zwötzen", "Heinrich XXV", "Schellsechs"],
    ["Dorf", "Rittergut", "Kirchengebäude", "Fürstenhaus"])

add("560",
    "Schluss Leumnitz (Pfarrsitz seit 1844, Schule 1865 mit 71 Kindern, Ziegeleien, Gemeindefinanzen, Fabrikarbeit in Gera, Flur 1056 5/6 Morgen, Brandstiftung 1852) und Zschippern, geringes Dörfchen 3/4 Stunde OSO. von Gera mit Vorwerk und Schäferei, 107 Einwohner.",
    "End of Leumnitz (parsonage since 1844, school of 1865 with 71 pupils, brickworks, municipal finances, factory work in Gera, 1,056 5/6 Morgen of fields, arson of 1852) and Zschippern, a modest village 3/4 hour ESE of Gera with a farm and sheepfold, 107 inhabitants.",
    ["Leumnitz", "Zschippern", "Pfarrsitz", "Schule", "Ziegelei", "Fabrikarbeit", "Brandstiftung"],
    ["Leumnitz", "Zschippern", "parsonage", "school", "brickworks", "factory work", "arson"],
    ["Dorf", "Schule", "Brände", "Industrie"])

add("561",
    "Schluss Zschippern (Vorwerk Pforten, Gemeindefinanzen, Fabrikarbeiter, Flur 308 3/5 Morgen) und Beginn Collis: kleines, reiches Bauerndorf 1 Stunde SO. von Gera im pfortner Grund, 76 Einwohner, kirchlich und schulisch nach Thränitz (Weimar), Viehzucht.",
    "End of Zschippern (Pforten farm, municipal finances, factory workers, 308 3/5 Morgen of fields) and start of Collis: a small, wealthy farming village 1 hour SE of Gera in the Pforten valley, 76 inhabitants, church and school at Thränitz (Weimar), cattle keeping.",
    ["Zschippern", "Collis", "Vorwerk", "Thränitz", "Viehzucht", "Eisenbahn Gößnitz", "Pforten"],
    ["Zschippern", "Collis", "farm", "Thränitz", "cattle keeping", "Gößnitz railway", "Pforten"],
    ["Dorf", "Viehzucht", "Gemeindefinanzen", "Eisenbahn"])

add("562",
    "Schluss Collis (Hunnenacker mit Urnenfund, Bevölkerung durch Eisenbahnarbeiter) und Beginn Kaimberg: Kirch-, Grenz- und Plateaudorf 1 1/4 Stunde SSO. von Gera, 44 Privathäuser, 319 Einwohner, Rittergut (Kaien, Koppy, Ende), Kirche als Filial von Thränitz, Weimar-Vertrag 1864.",
    "End of Collis (Hunnenacker with urn finds, population influenced by railway workers) and start of Kaimberg: a church, border and plateau village 1 1/4 hours SSE of Gera, 44 private houses, 319 inhabitants, manor (Kaien, Koppy, Ende), church as a branch of Thränitz, treaty with Weimar of 1864.",
    ["Collis", "Hunnenacker", "Urnen", "Kaimberg", "Rittergut", "Kirche", "Thränitz"],
    ["Collis", "Hunnenacker", "urns", "Kaimberg", "manor", "church", "Thränitz"],
    ["Dorf", "Vor- und Frühgeschichte", "Rittergut", "Kirchengebäude"])

add("563",
    "Schluss Kaimberg (Gasthaus, Collismühle, Gemeindefinanzen, Berufsgliederung, Flur 785 7/9 Morgen, sorbischer Name, Brand 1791) und Beginn Lichtenberg: kleines Grenz- und Plateaudorf 1 3/4 Stunde SO. von Gera, 19 Privathäuser, 125 Einwohner, Rittergut (Schäferei), kirchlich nach Niebra (Sachsen).",
    "End of Kaimberg (inn, Collis mill, municipal finances, occupational structure, 785 7/9 Morgen of fields, Sorbian name, fire of 1791) and start of Lichtenberg: a small border and plateau village 1 3/4 hours SE of Gera, 19 private houses, 125 inhabitants, manor (sheep farm), church ties to Niebra (Saxony).",
    ["Kaimberg", "Lichtenberg", "Collismühle", "Niebra", "Schäferei", "Rittergut", "Flur"],
    ["Kaimberg", "Lichtenberg", "Collis mill", "Niebra", "sheep farm", "manor", "fields"],
    ["Dorf", "Rittergut", "Schafe", "Gemeindefinanzen"])

add("564",
    "Schluss Lichtenberg (Bauerngüter, Berufe, Wohlstand, Flur 829 17/20 Morgen, v. Ende 1534) und Beginn Pohlen: kleines Kirch-, Grenz- und Plateaudorf, südlichster Punkt des reußischen Unterlandes, 3 Stunden SO. von Gera, 126 Einwohner, Filial von Wolfersdorf (Weimar), Kirche von 1665.",
    "End of Lichtenberg (farms, occupations, prosperity, 829 17/20 Morgen of fields, v. Ende in 1534) and start of Pohlen: a small church, border and plateau village, southernmost point of the Reuss lowlands, 3 hours SE of Gera, 126 inhabitants, branch of Wolfersdorf (Weimar), church of 1665.",
    ["Lichtenberg", "Pohlen", "Wolfersdorf", "Kirche", "Plateaudorf", "Gemeinde", "südlichster Punkt"],
    ["Lichtenberg", "Pohlen", "Wolfersdorf", "church", "plateau village", "municipality", "southernmost point"],
    ["Dorf", "Kirchengebäude", "Pfarreien", "Gemeinden"])

add("565",
    "Schluss Pohlen (Bauerngüter, Wohlstand, Flur 1250 4/5 Morgen, Rittersitz, v. Wolfersdorf und v. Raabe, Vereinigung mit Wüstfalke) und Beginn des Artikels über die Zwillingsdörfer Kleinfalke und Wüstfalke: Lage 2 Stunden SSO. von Gera, gleichartige Entstehung aus Rittergütern.",
    "End of Pohlen (farms, prosperity, 1,250 4/5 Morgen of fields, knight's seat, v. Wolfersdorf and v. Raabe, union with Wüstfalke) and start of the article on the twin villages Kleinfalke and Wüstfalke: location 2 hours SSE of Gera, parallel origin from manors.",
    ["Pohlen", "Kleinfalke", "Wüstfalke", "Zwillingsdörfer", "Raabe", "Wolfersdorf", "Rittergut"],
    ["Pohlen", "Kleinfalke", "Wüstfalke", "twin villages", "Raabe", "Wolfersdorf", "manor"],
    ["Dorf", "Rittergut", "Siedlungsform", "Genealogie"])

add("566",
    "Kleinfalke und Wüstfalke: Besitzer (v. Wolfersdorf, v. Raschau, v. Raabe, Leo, 1864 Bruhm), 1843 »vereinigte Rittergüter«, Gerichte, Kriegsschäden (1647 ohne Einwohner), kirchliche Zugehörigkeit zu Veitsberg (Weimar), Kirchenbuch und Friedhofsfrage.",
    "Kleinfalke and Wüstfalke: owners (v. Wolfersdorf, v. Raschau, v. Raabe, Leo, Bruhm in 1864), the 'united manors' of 1843, courts, war damage (no inhabitants in 1647), church ties to Veitsberg (Weimar), parish register and cemetery question.",
    ["Kleinfalke", "Wüstfalke", "vereinigte Rittergüter", "Veitsberg", "Raabe", "Leo", "Dreißigjähriger Krieg"],
    ["Kleinfalke", "Wüstfalke", "united manors", "Veitsberg", "Raabe", "Leo", "Thirty Years' War"],
    ["Rittergut", "Dreißigjähriger Krieg", "Pfarreien", "Dorf"])

add("567",
    "Schule für Kleinfalke und Wüstfalke (Beschluss 1809, seit 1810 Lehrer, 72 Kinder), Gemeindelasten; Kleinfalke mit 30 Privathäusern, 181 Einwohnern, Handwerkern, Flur 406 Morgen; Beginn Wüstfalke mit Rittergut, 26 Privathäusern und 176 Einwohnern.",
    "School for Kleinfalke and Wüstfalke (resolution of 1809, teacher since 1810, 72 pupils), municipal burdens; Kleinfalke with 30 private houses, 181 inhabitants, craftsmen, 406 Morgen of fields; start of Wüstfalke with manor, 26 private houses and 176 inhabitants.",
    ["Kleinfalke", "Wüstfalke", "Schule", "Gemeindelasten", "Weber", "Maurer", "Bockmühle"],
    ["Kleinfalke", "Wüstfalke", "school", "municipal burdens", "weavers", "masons", "post mill"],
    ["Schule", "Gemeinden", "Handwerk", "Dorf"])

add("568",
    "Schluss Wüstfalke (Gutsgebäude, Gemeinde, Berufe, Armut, Flur 271 1/2 Morgen, Verdienste des Gutsbesitzers Moritz Eduard Leo) und Beginn Otticha: kleines Bauern- und Plateaudörfchen 1 3/4 Stunde SSO. von Gera, Halbkreis um einen Teich, 85 Einwohner, Kirche und Schule in Niebra (Sachsen).",
    "End of Wüstfalke (manor buildings, municipality, occupations, poverty, 271 1/2 Morgen of fields, merits of the owner Moritz Eduard Leo) and start of Otticha: a small farming and plateau village 1 3/4 hours SSE of Gera, laid out in a semicircle around a pond, 85 inhabitants, church and school at Niebra (Saxony).",
    ["Wüstfalke", "Otticha", "Rittergut", "Leo", "Niebra", "Dorfanlage", "Gemeinde"],
    ["Wüstfalke", "Otticha", "manor", "Leo", "Niebra", "village layout", "municipality"],
    ["Dorf", "Rittergut", "Siedlungsform", "Gemeinden"])

add("569",
    "Schluss Otticha (Pferdebauern, Viehzucht, Wohlstand, Flur 799 1/30 Morgen, Flurnamen, sorbischer Ursprung, Zinsen an Kloster Cronswitz 1359 und 1361, Gerichtsstand) und damit Ende des Landestheils (Landrathsbezirks) Gera.",
    "End of Otticha (horse farmers, cattle keeping, prosperity, 799 1/30 Morgen of fields, field names, Sorbian origin, rents to Cronswitz convent in 1359 and 1361, jurisdiction) and with it the end of the Gera district.",
    ["Otticha", "Pferdebauern", "Viehzucht", "Flurnamen", "sorbisch", "Cronswitz", "Landrathsbezirk Gera"],
    ["Otticha", "horse farmers", "cattle keeping", "field names", "Sorbian", "Cronswitz", "Gera district"],
    ["Dorf", "Flurnamen", "Sorben", "Viehzucht"])

# ---------------------------------------------------------------- glossary
def pages_with(*pats):
    out = []
    for n in range(487, 570):
        t = (ROOT / "data" / "text" / "pages" / f"{n}.txt").read_text(encoding="utf-8")
        if any(re.search(p, t) for p in pats):
            out.append(str(n))
    return out

G = []
def gl(term, variants, kind, de, en, pats):
    pg = pages_with(*pats)
    assert pg, term
    G.append(dict(term=term, variants=variants, kind=kind, de=de, en=en, pages=pg))

gl("Morgen", ["Mrg."], "unit",
   "Flächenmaß der Flurangaben; 1 preuß. Morgen = 180 Quadratruthen = 0,2553 ha (S. 832).",
   "Unit of area used for the village fields; 1 Prussian Morgen = 180 square Ruthen = 0.2553 ha (p. 832).", [r"Morgen"])
gl("Ruthe", ["□R.", "Quadratruthe", "□Ruthe"], "unit",
   "Längen- bzw. Flächenmaß; 1 preuß. Ruthe = 12 Fuß = 3,766 m, 1 Quadratruthe = 14,18 m² (S. 831–832).",
   "Unit of length or area; 1 Prussian Ruthe = 12 feet = 3.766 m, 1 square Ruthe = 14.18 m² (pp. 831–832).", [r"Ruthe", r"□R"])
gl("Fuß", ["'"], "unit",
   "Längenmaß, in der Ortskunde für Höhenangaben der Orte; 1 preuß. Fuß = 0,3139 m (S. 831).",
   "Unit of length, used in the topography for the altitude of places; 1 Prussian foot = 0.3139 m (p. 831).", [r"\bFuß\b", r"\bFuss\b"])
gl("Stunde", [], "unit",
   "Wegstunde als Entfernungsangabe zwischen Orten (z. B. »3 Stunden W. von Gera«); Brückner gibt keinen Umrechnungswert an, die Tabelle S. 832 nennt als Entfernungsmaß die preuß. Meile zu 2000 Ruthen.",
   "Hour of walking used as a distance between places (e.g. '3 hours W of Gera'); Brückner gives no conversion, the table on p. 832 lists the Prussian mile of 2,000 Ruthen as the distance measure.", [r"Stunde"])
gl("Scheffel", [], "unit",
   "Getreide- und Hohlmaß; in Gera 1 dresdner Scheffel = 1,0383 hl (S. 832).",
   "Dry measure for grain; in Gera 1 Dresden Scheffel = 1.0383 hl (p. 832).", [r"Scheffel"])
gl("Pfund", ["Pfd."], "unit",
   "Gewichtsmaß; 1 Pfund (Zollpfund) = 0,5 kg (S. 832).",
   "Unit of weight; 1 pound (customs pound) = 0.5 kg (p. 832).", [r"Pfund"])
gl("Elle", [], "unit",
   "Längenmaß; in Gera 1 Elle = 0,5724 m (S. 831).",
   "Unit of length; in Gera 1 Elle = 0.5724 m (p. 831).", [r"\bElle\b"])
gl("Centner", ["Ctnr."], "unit",
   "Gewichtsmaß (Zentner), hier für die Sodaproduktion der chemischen Fabrik; zu 100 Pfund gerechnet.",
   "Unit of weight (hundredweight), here for the soda output of the chemical factory; counted as 100 pounds.", [r"Ctnr"])
gl("Thaler", ["Thlr."], "currency",
   "Hauptwährung der Vermögens-, Pacht- und Gemeindeangaben; 1 Thaler = 30 Silbergroschen (Sgr.).",
   "Main currency of the figures for assets, rents and municipal finances; 1 thaler = 30 silver groschen (Sgr.).", [r"Thlr"])
gl("Mark", ["Mk."], "currency",
   "Ältere Rechnungseinheit, hier vor allem für die Taxierung der Rittergüter in den Theilungsacten von 1647 (z. B. 2500 Mk.).",
   "Older unit of account, used here mainly for the valuation of manors in the partition records of 1647 (e.g. 2,500 Mk.).", [r"Mk\.", r"Mf\."])
gl("Schock Groschen", ["Schock"], "currency",
   "Mittelalterliche Rechnungsgröße; 1 Schock = 60 Groschen (z. B. 800 Schock Groschen für die Pflege Langenberg 1364).",
   "Medieval unit of account; 1 Schock = 60 groschen (e.g. 800 Schock Groschen for the Pflege Langenberg in 1364).", [r"Schock"])
gl("Gulden", [], "currency",
   "Silber- bzw. Goldwährung des Mittelalters und der Frühen Neuzeit (z. B. 40.000 Gulden für den Rückkauf der Pflege Langenberg 1502).",
   "Medieval and early modern silver or gold coin (e.g. 40,000 gulden for the buy-back of the Pflege Langenberg in 1502).", [r"Gulden"])
gl("Steuereinheit", [], "unit",
   "Maß des Steuerwerts von Grundstücken; 1 Steuereinheit = 10 Thlr. Steuerwerth (Berichtigung S. 831).",
   "Unit of the tax value of landholdings; 1 tax unit = 10 thalers of tax value (correction on p. 831).", [r"Steuereinheit"])
gl("Viehstatistik-Abkürzungen", ["Pf.", "R.", "Schf.", "Schw.", "Z.", "G.", "Bnst."], "term",
   "In der Ortskunde stehende Abkürzungen der Viehzählung: Pf. = Pferde, R. = Rinder, Schf. = Schafe, Schw. = Schweine, Z. = Ziegen, G. = Gänse, Bnst. = Bienenstöcke.",
   "Abbreviations used in the topography for the livestock count: Pf. = horses, R. = cattle, Schf. = sheep, Schw. = pigs, Z. = goats, G. = geese, Bnst. = beehives.", [r"Bnst\."])
gl("Pflege", ["Pflege Langenberg", "Burgwartbezirk"], "institution",
   "Mittelalterlicher Burgwartbezirk der Sorbenlande, als Reichslehen an adlige Geschlechter gegeben; die Pflege Langenberg umfasste über 60 Orte (S. 508–509).",
   "Medieval castle district in the Sorbian lands, granted as an imperial fief to noble families; the Pflege Langenberg originally comprised over 60 places (pp. 508–509).", [r"Pflege"])
gl("Küchendorf", ["Küchenort", "Amts- und Küchenort"], "term",
   "Dorf, das dem landesherrlichen Amt Gera oder dem Burgküchengut mit Spann- und Handfrohnen verpflichtet war.",
   "Village obliged to perform draught and manual labour services for the princely Gera district or castle kitchen estate.", [r"Küchen"])
gl("Rittergut", ["Rittersitz"], "term",
   "Adliges Gut mit Herrenhaus und Wirtschaftshof, früher mit Lehn-, Erb- oder Niedergerichtsrechten über den Ort verbunden.",
   "Noble estate with manor house and home farm, formerly linked with fiefs and lower or hereditary jurisdiction over the village.", [r"Rittergut"])
gl("Kammergut", ["Kammerguts"], "term",
   "Landesherrliches Gut, dessen Ertrag der fürstlichen Kammer zufloss; meist verpachtet (Pachtershaus).",
   "Estate of the ruling prince whose revenues went to the princely chamber; usually leased out (tenant's house).", [r"Kammergut"])
gl("Vorwerk", [], "term",
   "Zum Gut gehöriger Wirtschaftshof, häufig mit Schäferei und Drescherhaus.",
   "Outlying farm belonging to an estate, often with a sheepfold and threshers' house.", [r"Vorwerk"])
gl("Freigut", ["Handgut", "Anspanngut"], "term",
   "Von bäuerlichen Lasten freies bzw. gesondert verliehenes Gut; Brückner unterscheidet daneben Hand- und Anspanngüter (nach dem Zusammenhang: ohne bzw. mit Gespannhaltung).",
   "Estate free of peasant burdens or granted separately; Brückner also distinguishes Hand- and Anspanngüter (from context: without or with draught animals).", [r"Freigut", r"Anspanngut", r"Handgut"])
gl("Paragiat", ["Paragium", "Paragiatherrschaft"], "institution",
   "Apanage einer Nebenlinie: das 1690 anerkannte Paragium Reuß-Köstritz wurde für den jüngeren Sohn Heinrichs I. von Schleiz gebildet, ohne landesherrliche Hoheit (S. 495).",
   "Appanage of a cadet line: the Paragium Reuss-Köstritz, recognised in 1690, was formed for the younger son of Heinrich I of Schleiz, without sovereign authority (p. 495).", [r"Paragi"])
gl("Frohne", ["Frohnen", "Fröhner", "Frohndienst", "Frohnhäuser"], "term",
   "Fron: Pflichtarbeit (Spann- und Handfrohnen) der Untertanen für die Herrschaft; Fröhner sind die dazu Verpflichteten.",
   "Compulsory feudal labour (with draught animals or by hand) owed by subjects to their lord; Fröhner are those liable to it.", [r"[Ff]rohn", r"Fröhner"])
gl("Frohntanz", ["Herrntanz", "Rügegericht"], "term",
   "Alter Brauch beim langenberger Rügegericht: jährlicher Tanz der verpflichteten Personen unter der Linde auf dem Markt; 1804 aufgehoben (S. 514).",
   "Old custom attached to the Langenberg court of presentment: an annual dance of the liable persons under the linden tree on the market square; abolished in 1804 (p. 514).", [r"Frohntanz", r"Herrn- oder Frohntanz"])
gl("Obergerichte", ["Niedergerichte", "Erbgerichte", "Patrimonialgerichte"], "term",
   "Gerichtsrechte über den Ort: die Obergerichte waren meist landesherrlich, die Erb- und Niedergerichte standen Rittergütern zu; Patrimonialgerichte wurden im 19. Jh. aufgehoben.",
   "Jurisdictional rights over a village: high justice was mostly held by the ruling prince, hereditary and lower justice by manors; patrimonial courts were abolished in the 19th century.", [r"Obergericht", r"Erbgericht", r"Patrimonialgericht"])
gl("Lehn", ["Lehen", "Güterlehen", "Amtslehn"], "term",
   "Abhängigkeitsverhältnis eines Guts oder Hauses zu einem Lehnsherrn (Amt, Rittergut, Pfarrei), verbunden mit Zinsen und Diensten.",
   "Dependency of an estate or house on a feudal lord (district office, manor, parish), tied to rents and services.", [r"Lehn", r"Lehen"])
gl("Decem", ["Zehnt", "Pfarrdecem", "Rauchdecem", "Sackdecem", "Hundedecem"], "term",
   "Abgabe an Kirche oder Pfarrei, ursprünglich der Zehnte; Sonderformen: Rauchdecem (nach Feuerstellen), Sackdecem, Hundedecem (Brotgeld für die bischöflichen Jagdhunde, S. 554).",
   "Levy to church or parish, originally the tithe; special forms: Rauchdecem (per hearth), Sackdecem, Hundedecem (bread money for the bishop's hunting dogs, p. 554).", [r"[Dd]ecem", r"Zehnt"])
gl("Kollatur", ["Collatur", "Besetzungsrecht", "Patronat", "Kirchenlehn"], "term",
   "Recht, die Pfarrstelle zu besetzen (Patronat), meist beim Rittergutsbesitzer, Landesherrn oder Konsistorium.",
   "Right to appoint the parish priest (patronage), mostly held by the manor owner, the ruling prince or the consistory.", [r"Collatur", r"Besetzungsrecht", r"Patronat"])
gl("Filial", ["Filialkirche", "eingepfarrt", "Schwesterkirche", "Mutterkirche"], "term",
   "Kirchliche Zuordnung: Filial = abhängige Tochterkirche einer Mutterkirche; Schwesterkirche = gleichrangige Kirche derselben Pfarrei; eingepfarrt = zur fremden Pfarrei gehörig.",
   "Church affiliation: Filial = dependent branch church of a mother church; Schwesterkirche = sister church of equal rank in the same parish; eingepfarrt = belonging to another parish.", [r"Filial", r"eingepfarrt", r"Schwesterkirche"])
gl("Kirchenvisitation 1533", ["Visitationsacten"], "institution",
   "Erste lutherische Kirchen- und Schulvisitation im Gebiet; ihre Akten (Weimar) nennen Pfarrer, Lehnsherren und Einkünfte und sind Brückners Hauptquelle zur Reformationszeit.",
   "First Lutheran visitation of churches and schools in the area; its records (Weimar) name pastors, patrons and revenues and are Brückner's main source for the Reformation period.", [r"Visitation"])
gl("Häusler", ["Kleinhäusler", "Hausgenosse", "Hausgenossen"], "term",
   "Kleine Besitzer eines Hauses mit wenig oder ohne Land (Gegensatz Bauer); Hausgenossen wohnen zur Miete.",
   "Small owners of a house with little or no land (as opposed to farmers); Hausgenossen are tenants.", [r"Häusler", r"Hausgenosse"])
gl("Pferdebauer", ["Kühbauer", "Pferdebauern", "Kühbauern"], "term",
   "Bauer mit Pferdegespann (Vollbauer) bzw. nur mit Kühen als Zugtieren (kleinerer Bauer).",
   "Farmer with a team of horses (full farmer) or only with cows as draught animals (smaller farmer).", [r"Pferdebauer", r"Kühbauer"])
gl("Taglöhner", ["Taglohn"], "term",
   "Tagelöhner: Landarbeiter oder Gewerbearbeiter ohne eigenen Betrieb; in der Ortskunde eigene Gruppe neben Bauern, Häuslern und Dienstboten.",
   "Day labourer: agricultural or industrial worker without an enterprise of his own; a separate group in the topography next to farmers, cottagers and servants.", [r"Taglöhner", r"Taglohn"])
gl("Kapitalist", ["Kapitalisten"], "term",
   "Einwohner, der von Kapitalvermögen lebt; Brückner zählt ihre Zahl je Ort als Maß des Wohlstands.",
   "Inhabitant living from capital; Brückner counts them for each village as a measure of prosperity.", [r"Kapitalist"])
gl("Jahresbrod bauen", ["sein Jahresbrod bauen"], "term",
   "Redewendung der Ortskunde: so viel Getreide anbauen, dass der Jahresbedarf an Brot gedeckt ist; Indikator der Selbstversorgung (»bauen mehr als ihren Bedarf«).",
   "Phrase of the topography: to grow enough grain to cover the annual bread requirement; an indicator of self-sufficiency ('grow more than they need').", [r"Jahresbrod"])
gl("Pertinenzstück", ["Grundstücksverband", "ledige Grundstücke", "walzende Grundstücke"], "term",
   "Kategorien der Grundbesitzstatistik; Brückner erklärt sie hier nicht, nach dem Zusammenhang: Pertinenzstück = zu einem anderen Gut gehöriges Stück, Grundstücksverband = Gruppe zusammengehöriger Stücke, ledige/walzende Grundstücke = einzelne, frei veräußerliche Parzellen ohne Hofstelle.",
   "Categories of the landholding statistics; Brückner does not explain them here; from context: Pertinenzstück = parcel belonging to another estate, Grundstücksverband = group of related parcels, ledige/walzende Grundstücke = single freely transferable parcels without a farmstead.", [r"Pertinenz", r"Grundstücksverband", r"ledige", r"walzende"])
gl("engere und weitere Gemeinde", ["engere Gemeinde", "weitere Gemeinde"], "term",
   "Zweiteilung der Gemeindefinanzen: die engere Gemeinde (Berechtigte) besitzt Grundvermögen, die weitere (politische) Gemeinde trägt Aktiva, Schulden und Jahresausgaben (nach dem Zusammenhang).",
   "Two-part scheme of municipal finances: the narrower commune (those with rights) holds land assets, the wider (political) commune carries assets, debts and annual expenses (from context).", [r"als engere", r"als weitere"])
gl("Communications- und Vicinalwege", ["Communicationswege", "Vicinalwege"], "term",
   "Gemeindewege: Communicationswege verbinden Orte, Vicinalwege sind Nachbarschaftswege; deren Unterhalt zählt zu den Gemeindelasten.",
   "Local roads: Communicationswege link villages, Vicinalwege are neighbourhood roads; their upkeep counts among municipal burdens.", [r"Communications", r"Vicinal"])
gl("Brauberechtigte", ["Braugerechtigkeit", "Reihenschank", "Reihebierschank"], "term",
   "Besitzer des Rechts, Bier zu brauen und auszuschenken; Reihenschank = Schankrecht, das reihum unter den Berechtigten wechselt (nach dem Zusammenhang).",
   "Holders of the right to brew and sell beer; Reihenschank = tap right that rotates among the entitled (from context).", [r"Brauberechtigt", r"Braugerechtigkeit", r"Reihe[s]?schank", r"Reihebierschank"])
gl("Sturmfass", [], "term",
   "Wasserfass zur Brandbekämpfung, wo keine Feuerspritze vorhanden ist.",
   "Water barrel for fire fighting in places without a fire engine.", [r"Sturmfass", r"Sturmfässer"])
gl("Hoheitsausgleichungsvertrag", ["Staatsvertrag 1868"], "term",
   "Vertrag von 1868 (30. Mai, ratifiziert 5. August) mit S.-Altenburg zur Beseitigung gemischter Landeshoheit; betrifft u. a. Hirschfeld, Bethenhausen und Waaswitz.",
   "Treaty of 1868 (30 May, ratified 5 August) with Saxe-Altenburg abolishing mixed sovereignty; concerns Hirschfeld, Bethenhausen and Waaswitz among others.", [r"Hoheitsausgleichung"])
gl("Majorat", ["Majoratsgut"], "term",
   "Gut, das nach Erbfolge ungeteilt an den Ältesten der Familie übergeht (z. B. Rittergut Naundorf, Steinbrücken).",
   "Estate that passes undivided to the eldest of the family (e.g. the manors of Naundorf and Steinbrücken).", [r"Majorat"])
gl("Appelsmarkt", [], "term",
   "Jahrmarkt in Großaga (Ablassmarkt zum Bartholomäustag, 1678 erneuert), heute am Dienstag vor dem 1. Advent.",
   "Annual fair at Großaga (indulgence fair for St Bartholomew's day, revived in 1678), held on the Tuesday before the first Sunday of Advent.", [r"Appelsmarkt"])
gl("Wüstung", ["Wüste Markung", "wüst"], "term",
   "Untergegangene Siedlung; die Flur wurde meist Nachbarorten zugeschlagen, die Stätte lebt in Flurnamen fort.",
   "Abandoned settlement; its fields were usually added to neighbouring villages, and the site survives in field names.", [r"Wüstung", r"Wustung", r"wüste Markung"])
gl("Sorbischer Anbau", ["deutscher Anbau"], "term",
   "Brückners Herkunftsbestimmung der Dörfer nach Ortsnamen und Flurnamen: sorbische oder deutsche Gründung (Anbau = Siedlung).",
   "Brückner's classification of the origin of villages from place and field names: Sorbian or German foundation (Anbau = settlement).", [r"sorbisch", r"deutsche[rn]? Anbau"])
gl("Collaborator", ["Diaconus", "Präceptor"], "office",
   "Collaborator = studierter Hilfsgeistlicher und Lehrer, später Diaconus; Präceptor = Lehrer einer kleinen Schule vor der eigenen Schulgründung.",
   "Collaborator = academically trained assistant minister and teacher, later deacon; Präceptor = teacher of a small school before a proper school was founded.", [r"Collaborator", r"Diaconus", r"Präceptor"])
gl("Trauerfiscusverein", [], "institution",
   "Seit 1730 in Köstritz bestehender Verein zur Erleichterung der Beerdigungskosten (S. 497).",
   "Association in Köstritz since 1730 to ease burial costs (p. 497).", [r"Trauerfiscus"])
gl("Pascherwesen", [], "term",
   "Schmuggel (Paschen) über die Grenze; nach Brückner Ursache lockerer Sitten in Großaga (S. 524).",
   "Smuggling across the border; according to Brückner a cause of loose morals at Großaga (p. 524).", [r"Pascher"])
gl("Gensd'arm", ["Gensd'armerie"], "office",
   "Landgendarm als Polizeibeamter; Sitz in Köstritz, Langenberg und Leumnitz.",
   "Rural gendarme as police officer; stationed at Köstritz, Langenberg and Leumnitz.", [r"Gensd"])
gl("Zeugmacher", ["Muldenhauer"], "term",
   "Zeugmacher = Weber von Wollstoffen (»Zeug«); Muldenhauer = Hersteller hölzerner Mulden.",
   "Zeugmacher = weaver of woollen cloth ('Zeug'); Muldenhauer = maker of wooden troughs.", [r"Zeugmacher", r"Muldenhauer"])
gl("Erbkretscham", [], "term",
   "Erblich verliehene Dorfschenke, »Wiege« späterer Gasthöfe und Brauereien (S. 498, 542).",
   "Hereditarily granted village inn, the 'cradle' of later inns and breweries (pp. 498, 542).", [r"Erbkretscham", r"Erbkretschmar"])
gl("Leichenhof", ["Gottesacker", "Friedhof"], "term",
   "Friedhof; Leichenhof ist der Kirchhof, oft ummauert und um die Kirche gelegen.",
   "Cemetery; Leichenhof is the churchyard, often walled and lying around the church.", [r"Leichenhof"])

out = dict(package="G2", pages=[P[k] for k in sorted(P, key=int)], glossary=G)
(ROOT / "data" / "search" / "pages").mkdir(parents=True, exist_ok=True)
(ROOT / "data" / "search" / "pages" / "G2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(P), "pages;", len(G), "glossary terms")
missing = [str(n) for n in range(487, 570) if str(n) not in P]
print("missing", missing)
