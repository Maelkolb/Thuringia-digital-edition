PAGES = []

def P(page, de, en, kde, ken, subj):
    PAGES.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

P("570",
  "Einleitung zum Landestheil Schleiz (Wisentaland): größter der Landrathsbezirke mit 6,03 Quadratmeilen, bestehend aus einem größeren und einem kleineren, durch das greizer Zeulenroda getrennten Glied. Grenzen, weimarische und sächsische Exklaven, Höhenlage der Orte (800 bis 1560 Fuß), Hochflächen, Saale und Weida mit ihren Nebenbächen, Waldreichtum.",
  "Introduction to the Landestheil Schleiz (Wisentaland), the largest district division at 6.03 square miles, made up of a larger and a smaller part separated by the Greiz territory around Zeulenroda. Borders, Weimar and Saxon exclaves, elevation of the places (800 to 1,560 feet), plateaus, the Saale and Weida with their tributaries, forest wealth.",
  ["Landestheil Schleiz", "Wisentaland", "Landratsbezirk", "Fläche", "Grenzen", "Höhenlage", "Hochland", "Saale", "Weida", "Exklave"],
  ["district of Schleiz", "Wisentaland", "area", "borders", "elevation", "plateau", "Saale", "Weida", "exclave"],
  ["Lage und Grenzen", "Fläche", "Relief", "Flüsse und Bäche"])

P("571",
  "Wälder des Bezirks (1647 geschätzt: Pöllwitzer Wald 5828 3/4, Schleizer Wald 4487 1/4 Acker), Feld- und Wiesenboden, Viehzucht, ungenutzte Eisenvorkommen, Niedergang der Eisenhämmer, Weberei und Spinnerei und die Notlage der Weberbevölkerung. Der Bezirk hat drei Städte, einen Marktflecken, drei Jahrmarktsorte und 39 Dörfer; frühere Residenzen Reichenfels, Saalburg, Schleiz; über 30 mittelalterliche Rittergüter.",
  "Forests of the district (1647 estimate: Pöllwitz forest 5,828 3/4, Schleiz forest 4,487 1/4 Acker), farmland and meadows, cattle breeding, unused iron ore, decline of the ironworks, weaving and spinning and the distress of the weaver population. The district has three towns, one market town, three fair villages and 39 villages; former residences Reichenfels, Saalburg and Schleiz; over 30 medieval manors.",
  ["Wald", "Pöllwitzer Wald", "Viehzucht", "Eisen", "Eisenhämmer", "Weberei", "Spinnerei", "Weberbevölkerung", "Residenz", "Rittergut"],
  ["forest", "cattle breeding", "iron", "ironworks", "weaving", "spinning", "weavers", "residence", "manor"],
  ["Wald", "Viehzucht", "Textilgewerbe", "Burgen und Schlösser"])

P("572",
  "Schluss des Abschnitts über die Rittergüter (19 im Jahr 1647, jetzt 6: Hohenleuben und Triebes fürstlich, Frankendorf, Schilbach, Zollgrün bürgerlich, Weißendorf adlig). Tabelle der Bevölkerung des Landestheils Schleiz 1867 nach Orten: Glieder der Familien, Dienstboten, Gehilfen und Lehrlinge, Altersgruppen nach Geschlecht; Summe 27 368.",
  "End of the passage on the manors (19 in 1647, now 6: Hohenleuben and Triebes princely, Frankendorf, Schilbach, Zollgrün in bourgeois hands, Weißendorf noble). Table of the population of the Landestheil Schleiz in 1867 by place: family members, servants, assistants and apprentices, age groups by sex; total 27,368.",
  ["Rittergüter", "Bevölkerung 1867", "Volkszählung", "Dienstboten", "Altersverhältnisse", "Tabelle", "Schleiz", "Tanna", "Saalburg", "Hohenleuben"],
  ["manors", "population 1867", "census", "servants", "age structure", "table", "Schleiz", "Tanna", "Saalburg", "Hohenleuben"],
  ["Bevölkerung", "Volkszählung", "Rittergut"])

P("573",
  "Prozentverteilung der Bevölkerung (Familienglieder, Dienstboten, Gehilfen; Knaben, Mädchen, Männer, Frauen) und Tabelle zur Bewegung der Bevölkerung 1647 bis 1867 nach Orten (Familien und Einwohner 1647, Einwohner 1803 und 1833, Familien und Einwohner 1864 und 1867); 1867 insgesamt 6068 Familien und 27 368 Einwohner. Beginn der Auswertung des Wachstums in 220 Jahren.",
  "Percentage breakdown of the population (family members, servants, assistants; boys, girls, men, women) and a table of population change 1647 to 1867 by place (families and inhabitants 1647, inhabitants 1803 and 1833, families and inhabitants 1864 and 1867); in 1867 a total of 6,068 families and 27,368 inhabitants. Start of the discussion of growth over 220 years.",
  ["Bevölkerungsentwicklung", "Einwohnerzahl 1647", "Einwohnerzahl 1867", "Familien", "Prozent", "Tabelle", "Bevölkerungswachstum"],
  ["population change", "inhabitants 1647", "inhabitants 1867", "families", "percentages", "table", "population growth"],
  ["Bevölkerung", "Volkszählung"])

P("574",
  "Auswertung der Bevölkerungsentwicklung: Wachstum in Hohenleuben und Triebes um das Zehnfache, Weberdistrikt, Anteil von Stadt und Land (27,6 und 29,1 Prozent städtisch), Dichte je Quadratmeile, Seelen je Haus (4,53 in 1647, 7,21 jetzt). Historischer Überblick über die drei Reichspflegen Schleiz, Saalburg und Reichenfels und Beginn der Periode der Lobdaburger.",
  "Analysis of population change: tenfold growth in Hohenleuben and Triebes, the weaver district, urban and rural shares (27.6 and 29.1 percent urban), density per square mile, persons per house (4.53 in 1647, 7.21 now). Historical overview of the three imperial Pflegen Schleiz, Saalburg and Reichenfels, and the start of the Lobdaburg period.",
  ["Bevölkerungswachstum", "Weberdistrikt", "Stadt und Land", "Bevölkerungsdichte", "Reichspflege", "Pflege Schleiz", "Pflege Saalburg", "Pflege Reichenfels", "Lobdaburger", "Sorben"],
  ["population growth", "weaver district", "town and country", "population density", "imperial Pflege", "Lobdaburg", "Sorbs"],
  ["Bevölkerung", "Territorialgeschichte", "Sorben"])

P("575",
  "Herrschaftsgeschichte, Periode der Lobdaburger: sorbische Bezirke als Grundlage der drei Pflegen, Besitzer Weida (Reichenfels) und Lobdaburg (Schleiz, Saalburg), Mitbesitz der Voigte von Gera und der Landgräfin Elisabeth. Urkundenliste 1222 bis 1312 zu Schleiz, Saalburg, Tanna und Dittersdorf (Wüstung bei Schleiz) mit Bezug auf den Deutschen Orden.",
  "Rulers' history, the Lobdaburg period: Sorbian districts as the basis of the three Pflegen, owners Weida (Reichenfels) and Lobdaburg (Schleiz, Saalburg), co-ownership of the Voigts of Gera and Landgravine Elisabeth. A list of charters from 1222 to 1312 on Schleiz, Saalburg, Tanna and Dittersdorf (deserted village near Schleiz), relating to the Teutonic Order.",
  ["Lobdaburger", "Voigte von Gera", "Pflege", "Sorben", "Urkunden", "Deutscher Orden", "Saalburg", "Tanna", "Mittelalter"],
  ["Lobdaburg", "Voigts of Gera", "Pflege", "Sorbs", "charters", "Teutonic Order", "Middle Ages"],
  ["Territorialgeschichte", "Urkunden", "Mittelalter", "Vögte von Weida"])

P("576",
  "Periode des Hauses Gera: Heinrich der Mehrer und Gräfin Luckard, Besitznahme 1310 bis 1314, Erbstreit und Verträge von 1316 und 1320, Teilungen 1425, um 1439, 1481 und 1500, Aussterben 1550. Beginn der burggräflichen Periode (böhmische Lehen an das Haus Plauen 1547 und 1550) mit Liste der Regenten ab 1550.",
  "Period of the House of Gera: Heinrich the Elder and Countess Luckard, takeover 1310 to 1314, inheritance dispute and treaties of 1316 and 1320, partitions in 1425, around 1439, 1481 and 1500, extinction in 1550. Start of the burgrave period (Bohemian fiefs to the House of Plauen in 1547 and 1550) with a list of rulers from 1550.",
  ["Haus Gera", "Reußen", "Voigt von Gera", "Landesteilung", "Burggrafen von Plauen", "Heinrich der Beerber", "Heinrich der Unglückliche", "Erbstreit", "böhmische Lehen"],
  ["House of Gera", "Reuss", "Voigt of Gera", "partition", "burgraves of Plauen", "inheritance dispute", "Bohemian fiefs"],
  ["Territorialgeschichte", "Fürstenhaus", "Mittelalter"])

P("577",
  "Periode des Hauses Reuß: verzögerte Besitzergreifung bis 1590 wegen der Witwe Anna von Pommern, kaiserliches Endurteil 1589. Tabellen zur Aufeinanderfolge der Herrscher im Bezirk Schleiz 1572 bis 1647: gemeinschaftliche Regierung der drei Linien, Teilung 1596, Aussterben der mittleren Linie 1616 und gemeinsame Regierung der vier Söhne Heinrichs Posthumus 1635; Beginn der Teilung von 1647.",
  "Period of the House of Reuss: delayed takeover until 1590 because of the widow Anna of Pomerania, imperial ruling of 1589. Tables of the succession of rulers in the Schleiz district from 1572 to 1647: joint rule of the three lines, partition of 1596, extinction of the middle line in 1616 and joint rule of the four sons of Heinrich Posthumus in 1635; start of the partition of 1647.",
  ["Haus Reuß", "Anna von Pommern", "Landesteilung 1596", "Heinrich Posthumus", "mittlere Linie", "Herrscherfolge", "Pflege Schleiz", "Reuß-Plauen"],
  ["House of Reuss", "Anna of Pomerania", "partition 1596", "Heinrich Posthumus", "middle line", "succession of rulers", "Reuss-Plauen"],
  ["Territorialgeschichte", "Fürstenhaus", "Genealogie"])

P("578",
  "Landesteilung von 1647 mit Einnahmen der Anteile Heinrichs IX. (Schleiz mit Reichenfels) und Heinrichs I. (Pflege Saalburg, Teile von Schleiz und Lobenstein) in Mark, Groschen und Pfennig; Auflösung Saalburgs 1666 und Regentenfolge 1666 bis 1848. Ende der selbstständigen Herrschaft Schleiz 1848, Residenz Osterstein, Regenten bis Heinrich XIV. (seit 1867).",
  "Partition of 1647 with the revenues of the shares of Heinrich IX. (Schleiz with Reichenfels) and Heinrich I. (Pflege Saalburg, parts of Schleiz and Lobenstein) in marks, groschen and pfennigs; dissolution of Saalburg in 1666 and the succession of rulers from 1666 to 1848. End of the independent lordship of Schleiz in 1848, residence Osterstein, rulers up to Heinrich XIV. (since 1867).",
  ["Landesteilung 1647", "Heinrich IX.", "Heinrich I.", "Einnahmen", "Saalburg", "1666", "Reuß-Schleiz", "1848", "Osterstein", "Heinrich XIV."],
  ["partition 1647", "revenues", "Saalburg", "Reuss-Schleiz", "1848", "Osterstein", "rulers"],
  ["Territorialgeschichte", "Fürstenhaus", "Staatsfinanzen"])

P("579",
  "Beginn des Artikels Schleiz: urkundliche Namensformen seit 1232, Lage an der Wisentthal und dem Stelzenbächlein, Entfernungen, Brände von 1837 und 1856. Entstehung der Stadt aus Altstadt (sorbisch), Neustadt (Deutscher Orden) und Heinrichstadt (1706), Stadttore, getrennte Gemeinden mit eigener Verfassung.",
  "Start of the article on Schleiz: recorded name forms since 1232, location on the Wisentthal and the Stelzenbächlein, distances, fires of 1837 and 1856. Growth of the town from the Old Town (Sorbian), New Town (Teutonic Order) and Heinrichstadt (1706), town gates, separate municipalities with their own constitutions.",
  ["Schleiz", "Stadtgeschichte", "Altstadt", "Neustadt", "Heinrichstadt", "Stadttore", "Stadtbrand", "Ortsname", "Schlossberg", "Wisentthal"],
  ["Schleiz", "town history", "Old Town", "New Town", "Heinrichstadt", "town gates", "town fire", "place name"],
  ["Stadt", "Ortsname", "Siedlungsform"])

P("580",
  "Schleiz: Vereinigung der Gemeinden 1442, 1482 und 1851 (vier Viertel), Straßen und Plätze, 526 Gebäude im Jahr 1867 und ihre Bauweise nach den Bränden. Beschreibung des nach 1837 neu erbauten Schlosses auf dem Bergkegel mit Park, Kapelle und Türmen; frühere Burg.",
  "Schleiz: merger of the municipalities in 1442, 1482 and 1851 (four quarters), streets and squares, 526 buildings in 1867 and their construction after the fires. Description of the castle rebuilt after 1837 on its rocky hill with park, chapel and towers; the earlier fortress.",
  ["Schleiz", "Stadtverfassung", "Viertelsmeister", "Straßen", "Markt", "Gebäudezahl", "Schloss Schleiz", "Schlosspark", "Fürstenkapelle", "Stadtbrand 1837"],
  ["Schleiz", "town constitution", "streets", "market square", "number of buildings", "Schleiz castle", "palace chapel", "fire of 1837"],
  ["Stadt", "Burgen und Schlösser", "Hausbau", "Gemeinden"])

P("581",
  "Schleiz: Geschichte des Schlosses (Sitz der Reichsvoigte von Gera ab 1318, Burggraf Heinrich VII., Residenz Heinrichs IX., Brände 1476, 1689 und 1837), Schlosskapelle, Archive und Sammlungen, Louisenburg (1726) und Postgebäude, öffentliche Gebäude (Kreisgericht 1867, Armen- und Arbeitshaus, Krankenhaus). Beginn der Kirchenbeschreibung.",
  "Schleiz: history of the castle (seat of the Voigts of Gera from 1318, Burgrave Heinrich VII., residence of Heinrich IX., fires of 1476, 1689 and 1837), castle chapel, archives and collections, the Louisenburg (1726) and the post office building, public buildings (district court 1867, poorhouse and workhouse, hospital). Start of the description of the churches.",
  ["Schloss Schleiz", "Reichsvoigte", "Burggraf Heinrich VII.", "Schlossbrand", "Louisenburg", "Post", "Kreisgericht", "Krankenhaus", "Archive", "Kirchen"],
  ["Schleiz castle", "Voigts of Gera", "castle fire", "Louisenburg", "post office", "district court", "hospital", "archives", "churches"],
  ["Burgen und Schlösser", "Kirche", "Stadt"])

P("582",
  "Schleiz: Stadt- oder St. Georgenkirche (gegründet vor 1232, Brände 1417, 1637, 1689, 1837, Altar von 1723, vier neue Glocken) und die Bergkirche St. Marien (Todtenkirche, älteste Kirche der Gegend, Datierungen 1101, 1206, 1220, um 1400 und 1622 bis 1635, Familien v. Kospod und v. Tepen).",
  "Schleiz: the town church of St. George (founded before 1232, fires 1417, 1637, 1689, 1837, altar of 1723, four new bells) and the Bergkirche St. Marien (burial church, oldest church of the region, dates 1101, 1206, 1220, around 1400 and 1622 to 1635, families von Kospod and von Tepen).",
  ["Stadtkirche St. Georg", "Bergkirche St. Marien", "Kirchenbau", "Familie Kospod", "Kirchenbrand", "Altar", "Glocken", "Wisenter", "Deutscher Orden"],
  ["St. George's church", "Bergkirche St. Marien", "church building", "Kospod family", "church fire", "altar", "bells"],
  ["Kirchengebäude", "Kirche", "Urkunden"])

P("583",
  "Schleiz: Ausstattung der Bergkirche (Steinbild des Pestmannes Hans v. Kospod, Monument Heinrichs d. m., Erbbegräbnisse der Fürsten, Glocken von 1818), St. Wolfgangskapelle (Jahreszahl 1105, Wallfahrtsstation), St. Niclaskirche (1856 abgebrannt) und Kirche Allerheiligen auf dem Schloss (1387 erstmals genannt, Brand 1476).",
  "Schleiz: furnishings of the Bergkirche (stone figure of the plague man Hans von Kospod, monument of Heinrich d. m., princely burial vaults, bells of 1818), the St. Wolfgang chapel (date 1105, pilgrimage station), the St. Nicholas church (burnt down in 1856) and the All Saints church in the castle (first mentioned in 1387, fire of 1476).",
  ["Bergkirche", "Pestmann Kospod", "Fürstengruft", "St. Wolfgangskapelle", "Wallfahrt", "Niclaskirche", "Allerheiligenkirche", "Schlosskirche", "Stiftungen"],
  ["Bergkirche", "plague man Kospod", "princely crypt", "St. Wolfgang chapel", "pilgrimage", "Nicholas church", "All Saints church"],
  ["Kirchengebäude", "Sagen", "Kirche"])

P("584",
  "Schleiz: Ende der Allerheiligenkirche, Kirchfahrt (Görkwitz, Mönchgrün, Filial Oberböhmsdorf), Friedhof um die Bergkirche, Judenkirchhof und Vertreibung der Juden 1349, Kommende des Deutschen Ordens (seit 1217 bzw. 1240), Pfarrer von 1232 bis 1445, die sieben Geistlichen bei der Einführung der Reformation 1533; lateinische Distichen an der Friedhofsmauer.",
  "Schleiz: end of the All Saints church, church parish (Görkwitz, Mönchgrün, filial Oberböhmsdorf), cemetery around the Bergkirche, Jewish cemetery and expulsion of the Jews in 1349, commandery of the Teutonic Order (from 1217 and 1240 respectively), pastors from 1232 to 1445, the seven clergy at the introduction of the Reformation in 1533; Latin distichs on the cemetery wall.",
  ["Kirchspiel", "Friedhof", "Judenkirchhof", "Judenvertreibung 1349", "Deutscher Orden", "Kommende", "Pfarrer", "Reformation 1533", "Görkwitz", "Oberböhmsdorf"],
  ["parish", "cemetery", "Jewish cemetery", "expulsion of the Jews 1349", "Teutonic Order", "commandery", "pastors", "Reformation 1533"],
  ["Kirche", "Pfarreien", "Reformation"])

P("585",
  "Schleiz: Besoldung der Geistlichen und Kirchenvisitation 1533, erster Superintendent Thomas Spies, geistliches Stadtministerium, Lehnsrechte an den Kirchen, mittelalterliche Kalandbrüderschaft (seit 1387), Sagen von Klöstern bei Schleiz. Beginn der Geschichte des Schulwesens (Schulmeister seit 1374).",
  "Schleiz: salaries of the clergy and church visitation of 1533, first superintendent Thomas Spies, the town's clerical ministry, patronage rights over the churches, the medieval Kaland brotherhood (from 1387), legends of monasteries near Schleiz. Start of the history of the school system (schoolmaster since 1374).",
  ["Kirchenvisitation 1533", "Superintendent", "Thomas Spies", "Pfarrerbesoldung", "Kalandbrüderschaft", "Kloster", "Schulwesen", "Reformation"],
  ["church visitation 1533", "superintendent", "clergy salaries", "Kaland brotherhood", "monastery", "schools", "Reformation"],
  ["Reformation", "Pfarreien", "Klöster", "Schule"])

P("586",
  "Schleiz: Schulwesen von 1485 bis zur Gegenwart (Rector, Cantor, Baccalaureus), Rutheneum (Gymnasium, 114 Schüler), Bürgerknabenschule (394), Mädchenschule (349), Schullehrerseminar seit 1820 mit Taubstummenanstalt, Mädcheninstitut. Hospital, Waisenhaus, Krankenhaus; Beginn der Stiftungen.",
  "Schleiz: the school system from 1485 to the present (rector, cantor, baccalaureus), the Rutheneum (grammar school, 114 pupils), boys' burgher school (394), girls' school (349), teachers' seminary since 1820 with an institution for the deaf-mute, private girls' institute. Hospital, orphanage, infirmary; start of the foundations.",
  ["Rutheneum", "Gymnasium", "Bürgerschule", "Mädchenschule", "Lehrerseminar", "Taubstummenanstalt", "Hospital", "Waisenhaus", "Stiftungen", "Schleiz"],
  ["Rutheneum", "grammar school", "burgher school", "girls' school", "teachers' seminary", "deaf-mute institution", "orphanage", "foundations"],
  ["Schule", "Gymnasium", "Stiftungen"])

P("587",
  "Schleiz: Stiftungen, Vereine und Stipendien (weißkersches, engelschall-lauterbachsches, zödelsches Familienstipendium, Bürger- und Heinrichsstipendium), Volksleseanstalt. Rathaus (1597 erbaut, 1689 und 1837 abgebrannt, Ruine), Stadtbehörde, Vermögen der Commune 195 862 Thlr., Passiva 73 130 Thlr., Einnahme und Ausgabe 1868.",
  "Schleiz: foundations, associations and scholarships (the Weißker, Engelschall-Lauterbach and Zödel family scholarships, burgher and Heinrich scholarships), popular reading library. Town hall (built 1597, burnt in 1689 and 1837, now a ruin), municipal authority, municipal assets 195,862 thalers, liabilities 73,130 thalers, income and expenditure in 1868.",
  ["Stiftungen", "Stipendien", "Armenpflege", "Volksbibliothek", "Rathaus", "Gemeindevermögen", "Schulden", "Stadtfinanzen", "Weißker", "Thaler"],
  ["foundations", "scholarships", "poor relief", "library", "town hall", "municipal assets", "debts", "town finances"],
  ["Stiftungen", "Stipendien", "Gemeindefinanzen", "Armenwesen"])

P("588",
  "Schleiz: Ordensvermögen (circa 87 860 Thlr.), Ober- und Erbgerichte, Frohnen der Alt- und Neustadt, Stadterhebung vor 1342, Statuten von 1359 und 1419 (aus Pößneck), Stadtwappen mit Wisentkopf, Bracteaten, Münzhaus. Beginn der Aufzählung der in Schleiz ansässigen Behörden (Kammer, Kreisgericht, Landrathsamt u. a.).",
  "Schleiz: property of the Teutonic Order (about 87,860 thalers), high and hereditary jurisdiction, labour services of the Old and New Town, elevation to town status before 1342, statutes of 1359 and 1419 (from Pößneck), town arms with a bison head, bracteates, mint house. Start of the list of authorities seated in Schleiz (chamber, district court, district office and others).",
  ["Ordensvermögen", "Gerichtsbarkeit", "Frondienste", "Stadtrechte", "Stadtstatuten", "Pößneck", "Stadtwappen", "Wisent", "Bracteaten", "Behörden"],
  ["order property", "jurisdiction", "labour services", "town rights", "town statutes", "town arms", "bison", "bracteates", "authorities"],
  ["Verwaltung", "Rechtspflege", "Ämter und Behörden"])

P("589",
  "Schleiz: Behörden mit 18 Hofbediensteten und 46 Staatsbeamten; Stadtgemeinde mit 4953 Einwohnern in 1196 Familien (Viehstand, Bevölkerung seit 1647); Erwerbszweige Landwirtschaft und Brauerei, Handwerker nach Zahlen (131 Weber, 88 Schuhmacher, 67 Strumpfwirker), 61 Handlungen, Ursachen der schwachen Wirtschaft, frühere Tuchfabrikation und Bergbau, Märkte; Beginn der Gasthöfe.",
  "Schleiz: authorities with 18 court employees and 46 state officials; the town municipality with 4,953 inhabitants in 1,196 families (livestock, population since 1647); trades farming and brewing, craftsmen by numbers (131 weavers, 88 shoemakers, 67 stocking weavers), 61 shops, causes of the weak economy, earlier cloth production and mining, markets; start of the inns.",
  ["Einwohnerzahl", "Handwerker", "Weber", "Strumpfwirker", "Brauerei", "Handel", "Märkte", "Viehmärkte", "Gewerbe", "Tuchfabrikation"],
  ["inhabitants", "craftsmen", "weavers", "stocking weavers", "brewing", "trade", "markets", "cattle markets", "cloth production"],
  ["Handwerk", "Handel", "Märkte", "Berufe"])

P("590",
  "Schleiz: Gasthöfe (Sonne, Erbprinz, Schwan), Gesellschaften, Straßenlaternen 1787 und Gasbeleuchtung 1867, Vereine (naturhistorischer Verein, Liedertafeln, Schützengesellschaft). Flur von 3498 3/4 Morgen mit Aufzählung der Flurstücke; sorbischer Ursprung des Ortsnamens, Landtage und Zusammenkünfte; Beginn des Berichts über Luthers Aufenthalt.",
  "Schleiz: inns (Sonne, Erbprinz, Schwan), societies, street lamps in 1787 and gas lighting in 1867, associations (natural history society, glee clubs, shooting club). Town fields of 3,498 3/4 Morgen with a list of field names; Sorbian origin of the place name, diets and princes' meetings; start of the account of Luther's stay.",
  ["Gasthöfe", "Vereine", "Gasbeleuchtung", "Schützengesellschaft", "Flurnamen", "Flur", "Morgen", "Ortsname sorbisch", "Landtage", "Schleiz"],
  ["inns", "associations", "gas lighting", "shooting club", "field names", "town fields", "Sorbian place name", "diets"],
  ["Flurnamen", "Gasthof", "Ortsname"])

P("591",
  "Schleiz: Martin Luther in Schleiz am 9. und 10. Oktober 1529, Wohltäter der Stadt, berühmte Söhne (Behr, Böttcher, Kettner, Lenzer, die Reichards, v. Strauch). Liste der Stadtbrände von 1417 bis 1864 mit Zahl der Häuser (u. a. 1417, 1475, 1637, 1689, 1837).",
  "Schleiz: Martin Luther in Schleiz on 9 and 10 October 1529, benefactors of the town, famous natives (Behr, Böttcher, Kettner, Lenzer, the Reichards, von Strauch). List of the town fires from 1417 to 1864 with the number of houses (among them 1417, 1475, 1637, 1689, 1837).",
  ["Martin Luther", "Luther 1529", "Marburger Religionsgespräch", "berühmte Persönlichkeiten", "Johann Friedrich Böttcher", "Stadtbrände", "Brandchronik", "Schleiz"],
  ["Martin Luther", "Luther 1529", "famous natives", "Johann Friedrich Böttcher", "town fires", "fire chronicle"],
  ["Brände", "Reformation", "Stadt"])

P("592",
  "Schleiz: Brände 1869, Überschwemmungs-, Dürre-, Teuerungs- und Sterbejahre (Pest 1575 mit 656 Toten), Leiden im Dreißigjährigen Krieg (1640), Gefechte 1758 und am 9. Oktober 1806 (Napoleon im Schloss), Theatereinsturz 1842, Volksglaube und Sagen (Schweinsberg und Johannisnacht, Kirschgrund, Pestmann Kospod).",
  "Schleiz: fires of 1869, years of floods, drought, high prices and mortality (plague of 1575 with 656 dead), suffering in the Thirty Years' War (1640), engagements in 1758 and on 9 October 1806 (Napoleon in the castle), theatre collapse in 1842, folk beliefs and legends (Schweinsberg and St. John's night, Kirschgrund, plague man Kospod).",
  ["Überschwemmung", "Dürre", "Teuerung", "Pest 1575", "Dreißigjähriger Krieg", "Schlacht 1806", "Napoleon", "Theatereinsturz 1842", "Sagen", "Schweinsberg"],
  ["flood", "drought", "famine", "plague 1575", "Thirty Years' War", "1806 engagement", "Napoleon", "theatre collapse 1842", "legends"],
  ["Naturkatastrophen", "Seuchen", "Napoleonische Kriege", "Sagen"])

P("593",
  "Schleiz: Sagen (Pestmann Kospod, Drache 1637, Gespenst 1654, Hexenglaube, Medicinfrau Graf 1853 bis 1860), Mühlen der Stadtgemeinde (Windmühle, Burkhards- oder Billingsmühle, Herrnmühle, Helbigsmühle, Neumühle, Pfeffermühle). Beginn von Wüstendittersdorf (im Volke Trilloch) mit Höfen, Mühle, Försterei, Scharfrichterei und Ziegelei.",
  "Schleiz: legends (plague man Kospod, dragon of 1637, ghost of 1654, witch belief, the healer Graf 1853 to 1860), mills of the municipality (windmill, Burkhards or Billings mill, Herrnmühle, Helbigsmühle, Neumühle, Pfeffermühle). Start of Wüstendittersdorf (locally called Trilloch) with farms, mill, forester's house, knacker's yard and brickworks.",
  ["Sagen", "Aberglaube", "Hexen", "Heilerin", "Mühlen", "Burkhardsmühle", "Herrnmühle", "Helbigsmühle", "Wüstendittersdorf", "Trilloch"],
  ["legends", "superstition", "witches", "healer", "mills", "Wüstendittersdorf", "Trilloch"],
  ["Sagen", "Aberglaube", "Mühlen", "Wüstung"])

P("594",
  "Wüstendittersdorf: Deutungen des Namens Trillloch, Kapelle 1232, Schenkung 1302, Erlbrunnen, Teufelspredigtstuhl. Oberböhmsdorf: Namensformen seit 1362, Lage südöstlich von Schleiz, Aufbau aus Kerndorf, Anbau und drei Waldhöfen, Zahl der Häuser und der Familien (148, 682 Einwohner), Viehstand, Kirche als Filial von Schleiz.",
  "Wüstendittersdorf: interpretations of the name Trillloch, chapel in 1232, donation in 1302, the Erlbrunnen well, Teufelspredigtstuhl rock. Oberböhmsdorf: name forms since 1362, location south-east of Schleiz, structure of core village, new houses and three forest farms, number of houses and families (148, 682 inhabitants), livestock, church as a filial of Schleiz.",
  ["Wüstendittersdorf", "Trilloch", "Teufelspredigtstuhl", "Oberböhmsdorf", "Waldhäuser", "Dorfanlage", "Einwohnerzahl", "Kirche", "Filial", "Ortsname"],
  ["Wüstendittersdorf", "Trilloch", "Oberböhmsdorf", "forest farms", "village layout", "inhabitants", "church", "filial"],
  ["Wüstung", "Dorf", "Siedlungsform"])

P("595",
  "Oberböhmsdorf: Kirche (1665 erbaut, 1864 repariert und bereichert), Schule seit 1651 mit 122 Schülern, Kammergut seit 1819 und seine früheren Besitzer, Forstei, Gemeinde und Grundbesitz (28 Bauerngüter), Berufe (26 Maurer, 24 Zimmerleute), Wohlstand und Gesittung, Geburten und Sterbefälle; Beginn der Flurbeschreibung.",
  "Oberböhmsdorf: church (built 1665, repaired and enriched 1864), school since 1651 with 122 pupils, Kammergut since 1819 and its former owners, forestry office, municipality and landholding (28 farms), occupations (26 masons, 24 carpenters), prosperity and morals, births and deaths; start of the description of the parish land.",
  ["Oberböhmsdorf", "Kirche", "Schule", "Kammergut", "ehemaliges Rittergut", "Maurer", "Zimmerleute", "Bauerngüter", "Gemeinde", "Forstei"],
  ["Oberböhmsdorf", "church", "school", "Kammergut", "former manor", "masons", "carpenters", "farms", "municipality"],
  ["Kirchengebäude", "Kammergut", "Berufe", "Gemeindefinanzen"])

P("596",
  "Oberböhmsdorf: Flur von 2943 Morgen, Teiche, Eisengrube Louise, stillgelegte Antimongrube (Waldschlösschen), 1660 bis 1665 erbautes, kurzlebiges Alaun- und Vitriolwerk, Flurstücke, Name und Geschichte, Brand 1665, Lehen; die dürre Schäferei (Dürrhof, 1850 eingegangen). Beginn von Oschitz: Namensformen seit 1368, Lage südwestlich von Schleiz, Anlage des Dorfes.",
  "Oberböhmsdorf: parish land of 2,943 Morgen, ponds, the Louise iron mine, the closed antimony mine (Waldschlösschen), short-lived alum and vitriol works built 1660 to 1665, field names, name and history, fire of 1665, fiefs; the dry sheep farm (Dürrhof, given up in 1850). Start of Oschitz: name forms since 1368, location south-west of Schleiz, layout of the village.",
  ["Oberböhmsdorf", "Flur", "Eisengrube", "Antimon", "Alaunwerk", "Dürrhof", "Schäferei", "Oschitz", "Flurnamen", "Brand 1665"],
  ["Oberböhmsdorf", "parish land", "iron mine", "antimony", "alum works", "Dürrhof", "sheep farm", "Oschitz", "field names"],
  ["Bergbau", "Flurnamen", "Dorf"])

P("597",
  "Oschitz: Häuser (119 Privathäuser), 163 Familien mit 754 Einwohnern, Viehstand, Kirche von 1614 mit fürstlicher Kapelle und dem Grabdenkmal des Hans Casp. v. Kospod, Glocken, Kirchenvermögen, Friedhöfe, Kapelle von 1333, Pfarrverhältnisse zur Bergkirche Schleiz, Pfarrhaus, erster lutherischer Pfarrer Temler 1533.",
  "Oschitz: houses (119 private houses), 163 families with 754 inhabitants, livestock, church of 1614 with a princely chapel and the tomb monument of Hans Casp. von Kospod, bells, church assets, cemeteries, chapel of 1333, parish ties to the Bergkirche in Schleiz, parsonage, first Lutheran pastor Temler in 1533.",
  ["Oschitz", "Kirche 1614", "Kospod", "Grabdenkmal", "Kapelle 1333", "Pfarrei", "Friedhof", "Einwohnerzahl", "Häuser", "Viehstand"],
  ["Oschitz", "church 1614", "Kospod", "tomb monument", "chapel 1333", "parish", "cemetery", "inhabitants"],
  ["Kirchengebäude", "Pfarreien", "Dorf"])

P("598",
  "Oschitz: Pfarreieinkünfte, Schule (1766 erbaut, 139 Kinder), Kammergut aus drei Gütern (Edelhof, 1704), Gemeinde mit 500 Thlr. Vermögen und über 200 Thlr. Schulden, Privatgrundbesitz (41 Bauerngüter), Berufe (37 Zimmerleute, 33 Maurer), Armut und Gesittung; Flur von 4398 1/4 Morgen, Teiche und Gruben.",
  "Oschitz: parsonage income, school (built 1766, 139 children), Kammergut formed from three estates (Edelhof, 1704), municipality with 500 thalers of assets and over 200 thalers of debt, private landholding (41 farms), occupations (37 carpenters, 33 masons), poverty and morals; parish land of 4,398 1/4 Morgen, ponds and mines.",
  ["Oschitz", "Pfarrei", "Schule", "Kammergut", "Edelhof", "Kospod", "Gemeindefinanzen", "Zimmerleute", "Maurer", "Flur"],
  ["Oschitz", "parsonage", "school", "Kammergut", "manor house", "municipal finances", "carpenters", "masons", "parish land"],
  ["Schule", "Kammergut", "Berufe", "Gemeindefinanzen"])

P("599",
  "Oschitz: Flurstücke, Eisengruben am Lohmen, Eremitage Heinrichs XLII., Culm als vermutete Kultstätte, Sagen (Rittersbühl, Weihkessel, weiße Frau), Plünderung 1633 und Pest 1637, Lehen, Hammerwerk und Alaunwerk von 1695. Zur Gemeinde gehören Thomasmühle und Beyersmühle an der Wisentthal.",
  "Oschitz: field names, iron mines on the Lohmen, the Eremitage of Heinrich XLII., Culm as a presumed cult site, legends (Rittersbühl, holy-water stone, white lady), plunder in 1633 and plague in 1637, fiefs, ironworks and alum works of 1695. The Thomasmühle and Beyersmühle mills on the Wisentthal belong to the municipality.",
  ["Oschitz", "Flurnamen", "Eisengruben", "Eremitage", "Culm", "Kultstätte", "Sagen", "Dreißigjähriger Krieg", "Thomasmühle", "Beyersmühle"],
  ["Oschitz", "field names", "iron mines", "Eremitage", "cult site", "legends", "Thirty Years' War", "Thomasmühle", "Beyersmühle"],
  ["Flurnamen", "Sagen", "Dreißigjähriger Krieg", "Mühlen"])

P("600",
  "Oschitz: Kirche und Schule der Mühlen, Chausseehaus, kalte Schäferei (Kaltenhof), Oberschütz (Kolonie von 1712, 5 Häuser, 44 Einwohner) und der herrschaftliche Park Heinrichsruhe mit Gebäuden. Beginn von Görkwitz: Namensformen seit 1377, Lage nordwestlich von Schleiz, 44 Privathäuser, 58 Familien, 304 Einwohner.",
  "Oschitz: church and school ties of the mills, the toll house, the cold sheep farm (Kaltenhof), Oberschütz (colony of 1712, 5 houses, 44 inhabitants) and the princely park Heinrichsruhe with its buildings. Start of Görkwitz: name forms since 1377, location north-west of Schleiz, 44 private houses, 58 families, 304 inhabitants.",
  ["Oberschütz", "Heinrichsruhe", "Park", "Chausseehaus", "kalte Schäferei", "Kolonie", "Görkwitz", "Fürst Heinrich XLII.", "Landsitz", "Thomasmühle"],
  ["Oberschütz", "Heinrichsruhe", "park", "toll house", "sheep farm", "colony", "Görkwitz", "country seat"],
  ["Dorf", "Mühlen", "Fürstenhaus"])

P("601",
  "Görkwitz: Kirche in Schleiz, Schule seit 1825 mit 50 Kindern, Mühlen (Dorf-, Graupen-, Mittel- und Hohenofenmühle), Wollspinnerei, Gemeinde und Grundbesitz (18 Bauerngüter), Berufe (12 Maurer, 7 Zimmerleute, 4 Müller), Sage vom Speciesthaler; Flur von 1501 Morgen mit 55 Teichen, Kalkstein, Hammerwerk und Hütte Ernestine Augusta (1741 abgebrannt, bis 1836 in Betrieb), Flurstücke, Zerstörung 1640.",
  "Görkwitz: church in Schleiz, school since 1825 with 50 children, mills (village, pearl-barley, middle and Hohenofen mills), wool-spinning mill, municipality and landholding (18 farms), occupations (12 masons, 7 carpenters, 4 millers), legend of the specie thaler; parish land of 1,501 Morgen with 55 ponds, limestone, ironworks and the Ernestine Augusta furnace (burnt in 1741, in operation until 1836), field names, destruction in 1640.",
  ["Görkwitz", "Schule", "Mühlen", "Hohenofenmühle", "Wollspinnerei", "Hammerwerk", "Ernestine Augusta", "Kalkstein", "Flur", "Flurnamen"],
  ["Görkwitz", "school", "mills", "Hohenofenmühle", "wool spinning", "ironworks", "limestone", "parish land", "field names"],
  ["Berufe", "Hüttenwesen und Hammerwerke", "Mühlen", "Gemeindefinanzen"])

P("602",
  "Görkwitz: Gerichte und Lehen, Sagen (Feuersäule, zurückgerufene Tochter). Beginn von Oettersdorf: Namensformen seit 1320, Lage auf einer Hochebene nördlich von Schleiz (gegen 1250 Fuß), Ober- und Unterdorf, Häuser, Mühlen (Holzmühle), Kirche von 1302 und 1391, neue Kirche von 1843, Pörmitz als Filial.",
  "Görkwitz: jurisdiction and fiefs, legends (pillar of fire, daughter called back from the grave). Start of Oettersdorf: name forms since 1320, location on a plateau north of Schleiz (about 1,250 feet), upper and lower village, houses, mills (Holzmühle), church of 1302 and 1391, new church of 1843, Pörmitz as its filial.",
  ["Görkwitz", "Sagen", "Oettersdorf", "Namensformen", "Hochebene", "Holzmühle", "Lorenzkirche", "Kirche 1843", "Pörmitz", "Filial"],
  ["Görkwitz", "legends", "Oettersdorf", "name forms", "plateau", "Holzmühle", "St. Lawrence church", "church 1843", "Pörmitz"],
  ["Dorf", "Kirchengebäude", "Sagen"])

P("603",
  "Oettersdorf: Pfarrfrohnen und Decem, Pfarrer (letzte katholische, erster lutherischer Ulr. Stößel), Pfarrhaus 1866, Schule mit 133 Kindern, Taubstummenanstalt 1853 bis 1860, Friedhof mit Denkmal des 1806 gefallenen Obristen v. Hochheimer, Kammergut, Gemeinde (Schuld nach dem Brand), Privatgrundbesitz, 162 Familien mit 776 Einwohnern.",
  "Oettersdorf: parish labour services and tithe, pastors (last Catholic, first Lutheran Ulr. Stößel), parsonage 1866, school with 133 children, deaf-mute institution 1853 to 1860, cemetery with the monument to Colonel von Hochheimer, killed in 1806, Kammergut, municipality (debt after the fire), private landholding, 162 families with 776 inhabitants.",
  ["Oettersdorf", "Pfarrei", "Pfarrfrohnen", "Zehnt", "Schule", "Taubstummenanstalt", "Hochheimer", "Kammergut", "Gemeindeschulden", "Einwohnerzahl"],
  ["Oettersdorf", "parish", "labour services", "tithe", "school", "deaf-mute institution", "Hochheimer", "Kammergut", "municipal debt"],
  ["Pfarreien", "Schule", "Kammergut", "Gemeindefinanzen"])

P("604",
  "Oettersdorf: Viehstand, Flur von 4029 Morgen mit 77 Teichen, Flurstücke, sorbische Namen, Brände 1706, 1728, 1865 und 1869, Schlacht vom 9. Oktober 1806 (Ponte-Corvo gegen Tauenzien), russisches Lazarett und Typhus nach der Schlacht bei Leipzig, Gerichte. Beginn von Pörmitz (Namensformen seit 1445, Lage am Schlangenbächlein).",
  "Oettersdorf: livestock, parish land of 4,029 Morgen with 77 ponds, field names, Sorbian names, fires in 1706, 1728, 1865 and 1869, battle of 9 October 1806 (Ponte-Corvo against Tauenzien), Russian field hospital and typhus after the battle of Leipzig, jurisdiction. Start of Pörmitz (name forms since 1445, location on the Schlangenbächlein).",
  ["Oettersdorf", "Flur", "Teiche", "Flurnamen", "Dorfbrand 1865", "Schlacht 1806", "Ponte-Corvo", "Typhus", "Pörmitz", "Schlangenbächlein"],
  ["Oettersdorf", "parish land", "ponds", "field names", "village fire 1865", "battle of 1806", "typhus", "Pörmitz"],
  ["Brände", "Napoleonische Kriege", "Flurnamen", "Dorf"])

P("605",
  "Pörmitz: 47 Privathäuser, Kirche (Vorläufer, Neubau 1832 mit 830 Thlr. Zuschuss Heinrichs LXII.), Glocken von 1553 und 1732, Filial von Oettersdorf, Schule seit 1773 (37 Kinder), Gemeinde mit 800 Thlr. Vermögen und 2000 Thlr. Schulden, Grundbesitz, 52 Familien mit 252 Einwohnern.",
  "Pörmitz: 47 private houses, church (predecessor, rebuilt in 1832 with a subsidy of 830 thalers from Heinrich LXII.), bells of 1553 and 1732, filial of Oettersdorf, school since 1773 (37 children), municipality with 800 thalers of assets and 2,000 thalers of debt, landholding, 52 families with 252 inhabitants.",
  ["Pörmitz", "Kirche 1832", "Glocken", "Filial", "Schule 1773", "Gemeindefinanzen", "Bauerngüter", "Einwohnerzahl", "Hausbau", "Oettersdorf"],
  ["Pörmitz", "church 1832", "bells", "filial", "school 1773", "municipal finances", "farms", "inhabitants"],
  ["Kirchengebäude", "Schule", "Hausbau", "Gemeindefinanzen"])

P("606",
  "Pörmitz: Berufe, Viehstand, Flur von 2489 Morgen auf Grauwacke mit 107 Teichen (Pörmitzteich 93 Morgen), Teufelsberg, Flurstücke, Gerichte und Lehen. Triemsdorf (Wüstung zwischen Oettersdorf, Pörmitz, Löhma, Rödersdorf und Dittersdorf). Beginn von Löhma: Namensformen seit 1371, Lage nordöstlich von Schleiz, Ortsanlage.",
  "Pörmitz: occupations, livestock, parish land of 2,489 Morgen on greywacke with 107 ponds (Pörmitzteich 93 Morgen), Teufelsberg, field names, jurisdiction and fiefs. Triemsdorf (deserted village between Oettersdorf, Pörmitz, Löhma, Rödersdorf and Dittersdorf). Start of Löhma: name forms since 1371, location north-east of Schleiz, village layout.",
  ["Pörmitz", "Pörmitzteich", "Teiche", "Karpfen", "Grauwacke", "Triemsdorf", "Wüstung", "Löhma", "Flurnamen", "Teufelsberg"],
  ["Pörmitz", "Pörmitzteich", "ponds", "carp", "greywacke", "Triemsdorf", "deserted village", "Löhma", "field names"],
  ["Wüstung", "Flurnamen", "Dorf"])

P("607",
  "Löhma: 75 Privathäuser, 88 Familien mit 459 Einwohnern, Kapelle des Deutschen Ordens (h. Moritz) nach 1240, Kirche von 1709/10 unter Heinrich XI., Altartuch von 1626, Kirchenvermögen, Pfarrer von 1533 bis zum 17. Pfarrer, Schule (86 Kinder), Rittergut mit Schloss Heinrichs d. m. (um 1610), Geburtsort Heinrichs I. und Heinrichs XLII.",
  "Löhma: 75 private houses, 88 families with 459 inhabitants, chapel of the Teutonic Order (St. Maurice) after 1240, church of 1709/10 under Heinrich XI., altar cloth of 1626, church assets, pastors from 1533 to the 17th pastor, school (86 children), manor with the castle of Heinrich d. m. (around 1610), birthplace of Heinrich I. and Heinrich XLII.",
  ["Löhma", "Kirche 1709", "Deutscher Orden", "Pfarrer", "Schule", "Rittergut", "Schloss", "Heinrich XI.", "Heinrich XLII.", "Kapelle St. Moritz"],
  ["Löhma", "church 1709", "Teutonic Order", "pastors", "school", "manor", "castle", "Heinrich XI.", "Heinrich XLII."],
  ["Kirchengebäude", "Pfarreien", "Schule", "Rittergut"])

P("608",
  "Löhma: Stätte des Schlosses, Rittergut 1647 (Anschlag), Lehen, Mühlen an der Gülde (Roßmühle, Rählemühle) und Windmühle seit 1864, Gemeinde, Privatgrundbesitz (33 Bauerngüter), Berufe, Flur von 4065 1/3 Morgen mit 61 Teichen, Flurstücke, Pest 1640, Brände 1862 bis 1867, Sage vom silbernen Häuschen am Güldebrunnen.",
  "Löhma: site of the castle, manor as assessed in 1647, fiefs, mills on the Gülde (Roßmühle, Rählemühle) and a windmill since 1864, municipality, private landholding (33 farms), occupations, parish land of 4,065 1/3 Morgen with 61 ponds, field names, plague of 1640, fires 1862 to 1867, legend of the silver house at the Güldebrunnen.",
  ["Löhma", "Rittergut 1647", "Lehen", "Gülde", "Roßmühle", "Rählemühle", "Windmühle", "Flur", "Güldebrunnen", "Sagen"],
  ["Löhma", "manor 1647", "fiefs", "Gülde", "Roßmühle", "Rählemühle", "windmill", "parish land", "legends"],
  ["Rittergut", "Mühlen", "Sagen", "Gemeindefinanzen"])
