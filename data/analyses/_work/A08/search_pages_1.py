# -*- coding: utf-8 -*-
"""Search metadata A08, part 1: pages 119-154 (Wohnliche Einrichtung, Mundart)."""

P = []


def add(page, sde, sen, kde, ken, subj):
    P.append({"page": page, "summary_de": sde, "summary_en": sen, "keywords_de": kde, "keywords_en": ken, "subjects": subj})


add("119",
    "Orts- und Flurnamen als Geschichtsquelle; phantastische Ableitungen (Katten, Chämen) werden zurückgewiesen. Etwa die Hälfte der Ortsnamen und ein Sechzigstel der Flurnamen sind sorbisch, im Unterland dichter als im Oberland; Beispiele sorbischer Namen und ihrer Gruppen. Fußnoten deuten Ernsee, Langenberg, Dragensdorf, Lobenstein.",
    "Place and field names as a historical source; fanciful derivations (Katten, Chämen) are rejected. About half the place names and one sixtieth of the field names are Sorbian, denser in the Unterland than in the Oberland; examples of Sorbian names and their groups. Footnotes interpret Ernsee, Langenberg, Dragensdorf, Lobenstein.",
    ["Ortsnamen", "Flurnamen", "Sorben", "Namensdeutung", "Unterland", "Oberland", "Besiedlung", "Kulm", "Wernsdorf"],
    ["place names", "field names", "Sorbs", "name etymology", "colonisation", "Unterland", "Oberland"],
    ["Ortsname", "Flurnamen", "Sorben"])
add("120",
    "Die Sorben mieden Wald und schweren Boden, deutsche Kolonisten rodeten; daher haben Berge, Bäche und Flurstücke meist deutsche Namen. Sorbische Namen beschreiben Naturformen oder erinnern an die alte Heimat; Zitat des Jenaer Slawisten Schleicher zu 90 sorbischen Ortsnamen (polabischer Stamm); Überleitung zur Namentabelle.",
    "The Sorbs avoided forest and heavy soil, German settlers cleared land; hence most mountains, streams and fields have German names. Sorbian names describe natural forms or recall the old homeland; quotation from the Jena Slavist Schleicher on 90 Sorbian place names (Polabian tribe); introduction to the name table.",
    ["Sorben", "Ortsnamen", "Schleicher", "Polaben", "Rodung", "Kolonisation", "Namensdeutung", "Jena"],
    ["Sorbs", "place names", "Schleicher", "Polabians", "land clearance", "colonisation"],
    ["Ortsname", "Sorben", "Flurnamen"])
add("121",
    "Tabelle der sorbischen Wurzeln mit Bedeutung und davon abgeleiteten Ortsnamen (29 Wurzeln: gora Berg, las waldig, lus Sumpf, kostriza Kirche u. a.), danach Hinweise auf Schleiz, Schwarm, Sormitz und Böhmsdorf. Deutsche Ortsnamen: 40 Orte enden auf -dorf; Fußnoten zu Gleina, Schwarm (Theilungsakten 1647).",
    "Table of Sorbian roots with meaning and the place names derived from them (29 roots: gora mountain, las wooded, lus swamp, kostriza church, etc.), followed by notes on Schleiz, Schwarm, Sormitz and Böhmsdorf. German place names: 40 places end in -dorf; footnotes on Gleina and Schwarm (partition records of 1647).",
    ["sorbische Wurzeln", "Ortsnamen", "Gera", "Köstritz", "Plauen", "Schleiz", "Namenstabelle", "Dorf-Namen", "Etymologie"],
    ["Sorbian roots", "place names", "Gera", "Köstritz", "Plauen", "Schleiz", "etymology", "-dorf names"],
    ["Ortsname", "Sorben"])
add("122",
    "Deutsche Ortsnamen: vorsorbische (Hundhaupten, Steinbrücken, Elster), Rodungsnamen des 10./11. Jahrhunderts im Oberland (Reuth, Grün, Gehau) und Orte nach dem Dreißigjährigen Krieg (Neuärgerniß, Titschendorf). Flurnamen mit Hain, Teufel, Galgen, Heide, Schwedenschanze; keltische Deutungsversuche. Beginn der Dorf- und Städtebetrachtung.",
    "German place names: pre-Sorbian ones (Hundhaupten, Steinbrücken, Elster), clearing names of the 10th/11th century in the Oberland (Reuth, Grün, Gehau) and places founded after the Thirty Years’ War (Neuärgerniß, Titschendorf). Field names with Hain, Teufel, Galgen, Heide, Schwedenschanze; Celtic etymologies. Start of the discussion of villages and towns.",
    ["Ortsnamen", "Flurnamen", "Rodung", "Teufelsberg", "Galgenberg", "Schwedenschanze", "Hain", "Kelten", "Dreißigjähriger Krieg"],
    ["place names", "field names", "clearing", "Devil’s hill", "gallows hill", "Swedish redoubt", "Celts", "Thirty Years’ War"],
    ["Ortsname", "Flurnamen"])
add("123",
    "Anlage der Dörfer: Lage in Mulden und Talrinnen; sorbische Rundlinge (Hufeisenform um einen Anger mit Teich, Sackgasse, Gärten und Hutrain außen; Otticha, Niederböhmsdorf) gegenüber langzeiligen deutschen Dörfern. Gründung durch Sorben auch bei deutschen Ortsnamen erkennbar.",
    "Layout of villages: situation in hollows and valley troughs; Sorbian round villages (horseshoe around a green with pond, dead-end lane, gardens and pasture strip outside; Otticha, Niederböhmsdorf) versus the long-row German villages. Sorbian foundation recognisable even where the place name is German.",
    ["Dorfanlage", "Rundling", "Anger", "Sackgasse", "Sorben", "Otticha", "Niederböhmsdorf", "Siedlungsform"],
    ["village layout", "round village", "village green", "dead-end lane", "Sorbs", "Otticha", "Niederböhmsdorf"],
    ["Siedlungsform", "Sorben"])
add("124",
    "Deutsche Dörfer in Zeilen und Gruppen; Pflege der Gassen, Dorflinden, Brunnen (zu Pfingsten geschmückt). Ortswappen: Stadtwappen von Gera, Schleiz, Lobenstein, Tanna, Saalburg, Hirschberg; 22 Dörfer führen einen Baum im Siegel, dazu Siegel mit Bäumen und Tieren, Tieren allein und landwirtschaftlichen Bildern.",
    "German villages in rows and groups; care of lanes, village limes, wells (decorated at Whitsun). Local coats of arms: town arms of Gera, Schleiz, Lobenstein, Tanna, Saalburg, Hirschberg; 22 villages bear a tree in their seal, further seals with trees and animals, animals alone and agricultural images.",
    ["Wappen", "Ortssiegel", "Dorflinde", "Brunnen", "Gera", "Schleiz", "Lobenstein", "Tanna", "Saalburg", "Hirschberg"],
    ["coats of arms", "village seals", "village linden", "wells", "Gera", "Schleiz", "Lobenstein", "Tanna", "Saalburg", "Hirschberg"],
    ["+Wappen und Siegel", "Dorf", "Siedlungsform"])
add("125",
    "Weitere Siegelmotive (Kirchen, Brücken, Pyramide, tanzender Jüngling in Dettersdorf). Neckende Ortsnamen und Wahrzeichen (Bier-Gera, Striezel-Hohenleuben, Schmalburg, Hirschbacher Gemeinschaftsuhr, Gassennamen wie Klatschgasse); das Lobensteiner Bittlied um Regen.",
    "Further seal motifs (churches, bridges, pyramid, dancing youth at Dettersdorf). Teasing place names and landmarks (Bier-Gera, Striezel-Hohenleuben, Schmalburg, the communal clock of Hirschbach, street names such as Klatschgasse); the Lobenstein rain-prayer rhyme.",
    ["Ortssiegel", "Spitznamen", "Neckname", "Wahrzeichen", "Hirschbach", "Hohenleuben", "Saalburg", "Lobenstein", "Volkshumor"],
    ["village seals", "nicknames", "landmarks", "Hirschbach", "Hohenleuben", "Saalburg", "Lobenstein", "folk humour"],
    ["+Wappen und Siegel", "Ortsname", "Bräuche"])
add("126",
    "Gemeindewesen: sorbische Familiensitze, deutsche Dorfgemeinde, Stammgemeinde (Brau- oder alte Gemeinde) und weitere Gemeinde; vier Glieder des Gemeindevermögens (Grundbesitz, Gerechtsame, Gebäude, Kapitalien). Patrimonialgerichts- und Amtsorte, Gutsgerichtsbarkeit, Hundeloch und Galgen; Beginn der städtischen und dörflichen Behörden.",
    "Municipal organisation: Sorbian family seats, German village commune, core commune (brewing or old commune) and wider commune; four components of communal property (land, rights, buildings, capital). Patrimonial-court and district villages, manorial jurisdiction, dungeon and gallows; start of the urban and village authorities.",
    ["Gemeinde", "Stammgemeinde", "Gemeindevermögen", "Patrimonialgericht", "Rittergut", "Amtsorte", "Gerichtsbarkeit", "Hundeloch"],
    ["commune", "core commune", "communal property", "patrimonial court", "manor", "district villages", "jurisdiction"],
    ["Gemeinden", "Rechtspflege", "Rittergut"])
add("127",
    "Städtische und dörfliche Ortsbehörden (Schulze, Älteste, Vierleute, Stadtverordnete) und ihre heutigen Nachfolger; Gemeindeumlagen, Hand- und Spanndienste; Abschaffung der Reihekost für Lehrer und Arme. Beginn des Abschnitts »Das Haus«: Bauernhaus, sorbische Hofraithe als Viereck mit Hof.",
    "Urban and village authorities (Schulze, elders, Vierleute, town councillors) and their present successors; communal levies, hand and team labour; abolition of the rota meals for teachers and the poor. Start of the section “The house”: the farmhouse, Sorbian farmstead as a quadrangle with yard.",
    ["Gemeindeverwaltung", "Schulze", "Vierleute", "Bürgermeister", "Umlagen", "Hand- und Spanndienste", "Bauernhaus", "Hofraithe"],
    ["municipal administration", "village mayor", "Vierleute", "mayor", "levies", "corvée", "farmhouse", "farmstead"],
    ["Gemeinden", "Hausbau", "Ämter und Behörden"])
add("128",
    "Das alte Bauernhaus: Aufbau des Gehöfts, vier Veränderungen im Baumaterial; ursprünglich einstöckiger Schrotbau (Blockbau) mit Strohdach, kleinen Fenstern und der zentralen Wohnstube mit »höllischem« Ofen; Stubeneinrichtung und Beleuchtung mit Spänen; Pfarrhaus Dürrenebersdorf bis 1819 Blockbau. Zweite Periode mit Kleinhäuslern.",
    "The old farmhouse: layout of the farmstead, four changes of building material; originally a single-storey log house (Schrotbau) with thatched roof, small windows and the central living room with a “hellish” stove; furnishing and lighting with wood splints; Dürrenebersdorf parsonage a log house until 1819. Second period with cottagers.",
    ["Bauernhaus", "Schrotbau", "Blockhaus", "Strohdach", "Wohnstube", "Ofen", "Dürrenebersdorf", "Hausbau", "Kienspan"],
    ["farmhouse", "log construction", "log house", "thatched roof", "living room", "stove", "Dürrenebersdorf", "house building", "pine splint"],
    ["Hausbau", "Wohnen"])
add("129",
    "Weitere Wandlungen des Bauernhauses: Fachbau statt Schrotbau, dann Massivbau und dreistöckige städtische Bauweise (Einfluss von Gera und Schleiz); Dachdeckung von Stroh über Schindeln zu Ziegeln und Schiefer; verschwundene Dachzeichen und Hausinschriften (Spruchbeispiele in Fußnote); schmuckloses Hausgerät, Tisch mit eingetieften Tellern.",
    "Further changes of the farmhouse: half-timbering instead of log construction, then masonry and three-storey urban style (influence of Gera and Schleiz); roofing from straw via shingles to tiles and slate; vanished roof signs and house inscriptions (examples in a footnote); plain furniture, table with hollowed plates.",
    ["Fachwerk", "Massivbau", "Dachdeckung", "Schiefer", "Hausinschriften", "Hausgerät", "Gera", "Schleiz", "Bauernhaus"],
    ["half-timbering", "masonry", "roofing", "slate", "house inscriptions", "furniture", "Gera", "Schleiz", "farmhouse"],
    ["Hausbau", "Wohnen"])
add("130",
    "Die eine Stube des Bauernhauses als Mittelpunkt allen Lebens; Hausnamen. Das Bürgerhaus: alle alten Bürgerhäuser sind abgebrannt, die Ringmauerstädte Gera, Schleiz, Saalburg und Lobenstein hatten Gotik und Renaissance; Tanna und Hirschberg dörflicher; Einfluss von Dynasten, Ritterorden und Stift Quedlinburg.",
    "The single living room of the farmhouse as the centre of all life; house names. The burgher house: all old burgher houses have burnt down, the walled towns of Gera, Schleiz, Saalburg and Lobenstein had Gothic and Renaissance periods; Tanna and Hirschberg more village-like; influence of the dynasts, the Teutonic Order and Quedlinburg abbey.",
    ["Bürgerhaus", "Stadtbrände", "Gera", "Schleiz", "Saalburg", "Lobenstein", "Tanna", "Hirschberg", "Hausname", "Quedlinburg"],
    ["burgher house", "town fires", "Gera", "Schleiz", "Saalburg", "Lobenstein", "Tanna", "Hirschberg", "house name"],
    ["Hausbau", "Wohnen", "Stadt"])
add("131",
    "Städtische Bauweise der Gegenwart: Gera als modernste Stadt, schlichtere Bauformen in Schleiz, Lobenstein, Hirschberg, Tanna, einförmig Saalburg; Rathaus Gera mit altertümlichen Grundmauern und Turm, Eingang aus dem 13. Jahrhundert. Beginn des Abschnitts »Das Gotteshaus«: kein Kirchenbau reicht vollständig über 1200 zurück.",
    "Present-day urban building: Gera as the most modern town, plainer building forms at Schleiz, Lobenstein, Hirschberg and Tanna, monotonous Saalburg; Gera town hall with ancient foundations and tower, entrance dating from the 13th century. Start of the section “The house of God”: no church building reaches back completely beyond 1200.",
    ["Städtebau", "Rathaus Gera", "Gera", "Schleiz", "Saalburg", "Lobenstein", "Kirchenbau", "Rathäuser"],
    ["urban architecture", "Gera town hall", "Gera", "Schleiz", "Saalburg", "Lobenstein", "church building"],
    ["Hausbau", "Kirchengebäude", "Stadt"])
add("132",
    "Älteste Kirchen: wenige romanische Reste (Portal und Steinmedaillon der Bergkirche Schleiz, Altarnischen im Unterland), abgegangene Wallfahrtskapellen (Pottendorf, Seligenstädt, Tanna, Stelzen), Marienbild Holla poppa; Gotik an Bergkirche und Untermhaus; Beschreibung der Bergkirche nach Puttrich.",
    "Oldest churches: few Romanesque remains (portal and stone medallion of the Bergkirche at Schleiz, altar niches in the Unterland), vanished pilgrimage chapels (Pottendorf, Seligenstädt, Tanna, Stelzen), Marian image Holla poppa; Gothic at the Bergkirche and Untermhaus; description of the Bergkirche after Puttrich.",
    ["Bergkirche Schleiz", "Romanik", "Gotik", "Untermhaus", "Wallfahrtskapelle", "Pottendorf", "Puttrich", "Kirchenbau", "Marienbild"],
    ["Bergkirche Schleiz", "Romanesque", "Gothic", "Untermhaus", "pilgrimage chapel", "Pottendorf", "Puttrich", "church building"],
    ["Kirchengebäude", "Religion und Frömmigkeit"])
add("133",
    "Portal und Baujahr (Sakristei 1101) der Bergkirche, Kapelle Untermhaus (1193, Schiff um 1450); gotische Kirchenteile in vielen Orten, Renaissance- und Rokokomischbauten; die meisten Kirchen stammen aus dem 17. und 18. Jahrhundert, Hirschberg 1842. Beginn der Liste der Neubauten mit Trinitatiskirche Gera 1611–1613.",
    "Portal and year of construction (sacristy 1101) of the Bergkirche, chapel at Untermhaus (1193, nave about 1450); Gothic church parts in many places, Renaissance and Rococo mixed buildings; most churches date from the 17th and 18th centuries, Hirschberg 1842. Start of the list of new buildings with the Trinitatiskirche at Gera 1611–1613.",
    ["Kirchenbau", "Bergkirche Schleiz", "Untermhaus", "Trinitatiskirche Gera", "Renaissance", "Rokoko", "Hirschberg", "Gotik", "Baujahre"],
    ["church building", "Bergkirche Schleiz", "Untermhaus", "Trinitatiskirche Gera", "Renaissance", "Rococo", "Hirschberg", "Gothic", "years of construction"],
    ["Kirchengebäude"])
add("134",
    "Liste der Kirchenneubauten von 1614 bis 1782 (Oschitz, Tanna, Saalburg, Schleiz St. Georg, Gräfenwarth, Lobenstein 1733, Kirschkau, Lössau, Gera Salvatorkirche u. a.); Kirschkau und Lössau als freundliche Landkirchen; Turmformen. Beginn der Glockenkunde: Alter, Namen, Inschriften (Bethenhausen, Lusan, Gera).",
    "List of new church buildings from 1614 to 1782 (Oschitz, Tanna, Saalburg, Schleiz St. Georg, Gräfenwarth, Lobenstein 1733, Kirschkau, Lössau, Gera Salvatorkirche and others); Kirschkau and Lössau as pleasant country churches; tower forms. Start of the account of bells: age, names, inscriptions (Bethenhausen, Lusan, Gera).",
    ["Kirchenneubauten", "Barock", "Kirschkau", "Lössau", "Salvatorkirche Gera", "Kirchtürme", "Glocken", "Glockeninschriften", "18. Jahrhundert"],
    ["new churches", "baroque", "Kirschkau", "Lössau", "Salvatorkirche Gera", "church towers", "bells", "bell inscriptions", "18th century"],
    ["Kirchengebäude", "+Glockenkunde"])
add("135",
    "Glockeninschriften und -namen vor und nach der Reformation (Michael, Vox mea vox vite; Glockengießer 1451 Osterstein, Gutsherr 1502 Großaga; Pertsch in Gera). Altarschreine der Saalfelder Werkstatt (ca. 1445–1505; Friesau 1447, Langenberg 1486); Fußnoten mit Inschriftenbeispielen.",
    "Bell inscriptions and names before and after the Reformation (Michael, Vox mea vox vite; bell founder 1451 Osterstein, lord of the manor 1502 Großaga; Pertsch of Gera). Altar shrines of the Saalfeld workshop (c. 1445–1505; Friesau 1447, Langenberg 1486); footnotes with inscription examples.",
    ["Glocken", "Glockeninschriften", "Glockengießer", "Altarschrein", "Saalfeld", "Langenberg", "Marienaltar", "Reformation"],
    ["bells", "bell inscriptions", "bell founder", "altar shrine", "Saalfeld", "Langenberg", "Marian altar", "Reformation"],
    ["Kirchengebäude", "+Glockenkunde", "Religion und Frömmigkeit"])
add("136",
    "Marienaltarschreine mit Heiligen und ihren Attributen (Petrus, Georg, Barbara, Katharina u. a.); Rokokomalerei, Grabdenkmäler des 16.–18. Jahrhunderts, Steinkanzel Bergkirche Schleiz, Taufstein Tanna; Reste der Holzschnitzerei aus katholischer Zeit (14 Nothelfer in Langenberg).",
    "Marian altar shrines with saints and their attributes (Peter, George, Barbara, Catherine and others); Rococo painting, tomb monuments of the 16th–18th centuries, stone pulpit of the Bergkirche at Schleiz, font at Tanna; remains of Catholic-period wood carving (14 Holy Helpers at Langenberg).",
    ["Altarschrein", "Heilige", "Grabdenkmäler", "Holzschnitzerei", "Nothelfer", "Bergkirche Schleiz", "Kanzel", "Taufstein", "Langenberg"],
    ["altar shrine", "saints", "tomb monuments", "wood carving", "Holy Helpers", "Bergkirche Schleiz", "pulpit", "font", "Langenberg"],
    ["Kirchengebäude", "Religion und Frömmigkeit"])
add("137",
    "Taufbecken Mühlsdorf, Kelch Schwaara (14. Jahrhundert), Kirchenbibliotheken (Kirschkau, Schleiz); einziges Kloster Stift zum Heiligen Kreuz bei Saalburg (letzter Rest 1868 abgebrochen). »Das weltliche Herrnhaus«: Burgruinen (Osterstein-Rundturm), neun fürstliche Schlösser, Bauzeiten Osterstein 1470, 1666, 1702–1706.",
    "Baptismal basin at Mühlsdorf, chalice at Schwaara (14th century), church libraries (Kirschkau, Schleiz); the only monastery, the Stift zum Heiligen Kreuz near Saalburg (last remnant demolished 1868). “The secular manor house”: castle ruins (round tower of Osterstein), nine princely palaces, building periods of Osterstein 1470, 1666, 1702–1706.",
    ["Taufbecken", "Kelch", "Kirchenbibliothek", "Kloster Saalburg", "Osterstein", "Burgen", "Schlösser", "Heinrich LXVII.", "Gera"],
    ["baptismal basin", "chalice", "church library", "Saalburg monastery", "Osterstein", "castles", "palaces", "Heinrich LXVII", "Gera"],
    ["Burgen und Schlösser", "Klöster", "Kirchengebäude"])
add("138",
    "Schluss des Abschnitts Wohnen (Rittergutsgebäude ohne Gericht und Galgen). »Die Mundart«: Mundart als gewachsene, Schriftsprache als gemachte Sprache; die voigtländische Mundart als mitteldeutsche Form; sorbische Familiennamen (1566 in Großaga nur sechs von 72 Familien); Abstufungen nach Lage und Verkehr.",
    "End of the section on dwellings (manor-house buildings without court and gallows). “The dialect”: dialect as grown, written language as made language; the Voigtland dialect as a Central German form; Sorbian family names (in 1566 only six of 72 families at Großaga); gradations by location and traffic.",
    ["Mundart", "voigtländisch", "Schriftsprache", "sorbische Familiennamen", "Großaga", "Rittergut", "Dialekt", "Sprachgeschichte"],
    ["dialect", "Voigtland dialect", "standard language", "Sorbian surnames", "Großaga", "manor", "language history"],
    ["Mundart", "Rittergut", "Sorben"])
add("139",
    "Vier Mundartströmungen im Voigtland (thüringisch, sächsisch, fränkisch, ostbayerisch) und ihre Verbreitung (Unterland thüringisch, Saale und Frankenwald fränkisch, Titschendorf rein fränkisch); Tabelle von 20 Wörtern der Schriftsprache mit ihren dialektischen Formen; Lobensteiner Satzbeispiele.",
    "Four dialect currents in the Voigtland (Thuringian, Saxon, Franconian, East Bavarian) and their distribution (Unterland Thuringian, Saale and Frankenwald Franconian, Titschendorf purely Franconian); table of 20 standard words with their dialect forms; sample sentences from Lobenstein.",
    ["Mundart", "Dialektgebiete", "thüringisch", "fränkisch", "sächsisch", "ostbayerisch", "Titschendorf", "Wortformen", "Frankenwald"],
    ["dialect", "dialect areas", "Thuringian", "Franconian", "Saxon", "East Bavarian", "Titschendorf", "word forms", "Franconian Forest"],
    ["Mundart"])
add("140",
    "Lautlehre der Vokale: a, ä, au und e in allgemeiner und örtlicher Aussprache, jeweils mit Wortbeispielen (a zu o: Hose, Stodt; a zu au; e zu a; Nebel/Nabel in Tanna und Kayla).",
    "Phonology of vowels: a, ä, au and e in general and local pronunciation, each with word examples (a to o: Hose, Stodt; a to au; e to a; Nebel/Nabel at Tanna and Kayla).",
    ["Vokale", "Lautwandel", "Aussprache", "Lautlehre", "Mundart", "a zu o", "Tanna"],
    ["vowels", "sound change", "pronunciation", "phonology", "dialect", "a to o", "Tanna"],
    ["Mundart"])
add("141",
    "Lautwandel der Vokale i, ei, ie, eu, o, ö und u, allgemein und örtlich (ei zu ê, i zu e, o zu u u. a.) mit Beispielwörtern, darunter der Spruch über Eberlenner und Ongerlenner.",
    "Sound change of the vowels i, ei, ie, eu, o, ö and u, general and local (ei to ê, i to e, o to u and others) with example words, among them the saying on Eberlenner and Ongerlenner.",
    ["Vokale", "Lautwandel", "Diphthonge", "Aussprache", "Mundart", "Beispielwörter"],
    ["vowels", "sound change", "diphthongs", "pronunciation", "dialect", "example words"],
    ["Mundart"])
add("142",
    "Schluss der Vokale (u, ü) und Konsonanten: b und p, d und t werden nicht unterschieden; Verhalten von b, d, t, ch, f, g, h, j in Aus-, In- und Anlaut mit Beispielen (obber/adder, nischt/nix, ga/cha).",
    "End of the vowels (u, ü) and the consonants: b and p, d and t are not distinguished; behaviour of b, d, t, ch, f, g, h, j in final, medial and initial position with examples (obber/adder, nischt/nix, ga/cha).",
    ["Konsonanten", "Lautwandel", "Aussprache", "Mundart", "nischt", "nix", "Oberland", "Unterland"],
    ["consonants", "sound change", "pronunciation", "dialect", "nischt", "nix", "Oberland", "Unterland"],
    ["Mundart"])
add("143",
    "Konsonanten l, m, n, s, r mit Ausfall- und Angleichungsregeln; Wortbiegung: Tabelle der Formen von Artikel (bestimmt, unbestimmt) und Fürwörtern (1. und 3. Person) in Singular und Plural nach Fällen.",
    "The consonants l, m, n, s, r with rules of omission and assimilation; inflection: table of the forms of the article (definite, indefinite) and pronouns (1st and 3rd person) in singular and plural by case.",
    ["Konsonanten", "Wortbiegung", "Artikel", "Fürwörter", "Pronomen", "Deklination", "Mundart", "Tabelle"],
    ["consonants", "inflection", "article", "pronouns", "declension", "dialect", "table"],
    ["Mundart"])
add("144",
    "Grammatik der Mundart: Kürzung von Artikel und Fürwörtern, zertrümmerter Genitiv, Familiennamen mit -é (de Kelleré), Hausbesitzer-Beinamen (Mielesdorf, Kraftsdorf), Pluralbildung und abweichendes Geschlecht; Imperfekt und Perfekt, drei Infinitivformen, ostbayerische Satzformen.",
    "Dialect grammar: shortening of article and pronouns, shattered genitive, family names with -é (de Kelleré), nicknames by house owners (Mielesdorf, Kraftsdorf), plural formation and divergent gender; imperfect and perfect, three infinitive forms, East Bavarian sentence patterns.",
    ["Grammatik", "Genitiv", "Plural", "Familiennamen", "Beinamen", "Infinitiv", "Mundart", "Mielesdorf", "Kraftsdorf"],
    ["grammar", "genitive", "plural", "family names", "by-names", "infinitive", "dialect", "Mielesdorf", "Kraftsdorf"],
    ["Mundart", "Sprachproben"])
add("145",
    "Sprachproben im Unterland: Umgegend von Gera (Gespräch zweier Jungen, Eduard erzählt das Gleichnis vom Sämann) und Waltersdorf (Gleichnis vom Sämann; Beginn der Fabel vom zahmen Wolf).",
    "Dialect samples from the Unterland: environs of Gera (conversation of two boys, Eduard tells the parable of the sower) and Waltersdorf (parable of the sower; start of the fable of the tame wolf).",
    ["Sprachproben", "Gleichnis vom Sämann", "Gera", "Waltersdorf", "Mundart", "Unterland", "Gespräch", "Fabel"],
    ["dialect samples", "parable of the sower", "Gera", "Waltersdorf", "dialect", "Unterland", "dialogue", "fable"],
    ["Sprachproben", "Mundart"])
add("146",
    "Fortsetzung der Waltersdorfer Proben (Fabel vom zahmen Wolf; Erzählung vom heimkehrenden Sohn, den die Eltern erschlagen); Gleichnis vom Sämann aus Kraftsdorf und vom Unkraut unter dem Weizen aus Roben mit den Namen der Einsender (Giebner, Mad. Seydel, Buschendorf).",
    "Continuation of the Waltersdorf samples (fable of the tame wolf; story of the returning son slain by his parents); parable of the sower from Kraftsdorf and of the tares from Roben with the names of the contributors (Giebner, Mad. Seydel, Buschendorf).",
    ["Sprachproben", "Waltersdorf", "Kraftsdorf", "Roben", "Gleichnis vom Sämann", "Unkraut unter dem Weizen", "Fabel", "Erzählung", "Mundart"],
    ["dialect samples", "Waltersdorf", "Kraftsdorf", "Roben", "parable of the sower", "parable of the tares", "fable", "story", "dialect"],
    ["Sprachproben", "Mundart"])
add("147",
    "Sprachproben: Leumnitz (Gleichnis vom Sämann) und Großaga (dreistrophiges Gedicht über Küssen und Werben); Beginn des Oberlands mit Triebes (Gespräch von Vater und Sohn über den Frost im Korn und einen verunglückten Nachbarn aus Neuärgerniß).",
    "Dialect samples: Leumnitz (parable of the sower) and Großaga (three-stanza poem about kissing and wooing); start of the Oberland samples with Triebes (conversation of father and son about frost in the grain and an injured neighbour from Neuärgerniß).",
    ["Sprachproben", "Leumnitz", "Großaga", "Triebes", "Oberland", "Gedicht", "Gespräch", "Neuärgerniß", "Mundart"],
    ["dialect samples", "Leumnitz", "Großaga", "Triebes", "Oberland", "poem", "dialogue", "Neuärgerniß", "dialect"],
    ["Sprachproben", "Mundart"])
add("148",
    "Schluss des Triebeser Gesprächs; Leitlitz-Weckersdorf: Gleichnis vom Sämann und ein Gespräch zweier Nachbarn über Wetter, Hagelversicherung und ein verunglücktes Mädchen; Fußnoten zu Dialektwörtern (zum Abend, hört, im Frühjahr).",
    "End of the Triebes conversation; Leitlitz-Weckersdorf: parable of the sower and a conversation of two neighbours about weather, hail insurance and an injured girl; footnotes on dialect words (zum Abend, hört, im Frühjahr).",
    ["Sprachproben", "Triebes", "Leitlitz", "Weckersdorf", "Wetter", "Hagelversicherung", "Gespräch", "Mundart", "Oberland"],
    ["dialect samples", "Triebes", "Leitlitz", "Weckersdorf", "weather", "hail insurance", "dialogue", "dialect", "Oberland"],
    ["Sprachproben", "Mundart"])
add("149",
    "Sprachproben aus dem Oberland: Oettersdorf und Mielesdorf (Gleichnis vom Sämann) und Tanna (Gespräch zweier Männer beim Aufbruch zur Arbeit über Kaffee, Mittagessen und Wurst); Fußnoten zu Kaffee und Schnaps.",
    "Dialect samples from the Oberland: Oettersdorf and Mielesdorf (parable of the sower) and Tanna (conversation of two men setting out for work about coffee, midday meal and sausage); footnotes on coffee and schnapps.",
    ["Sprachproben", "Oettersdorf", "Mielesdorf", "Tanna", "Gleichnis vom Sämann", "Kaffee", "Gespräch", "Mundart", "Oberland"],
    ["dialect samples", "Oettersdorf", "Mielesdorf", "Tanna", "parable of the sower", "coffee", "dialogue", "dialect", "Oberland"],
    ["Sprachproben", "Mundart"])
add("150",
    "Schluss des Tannaer Gesprächs; Oßla (Gleichnis vom Sämann; Gespräch zweier alter Männer, die die gute alte Zeit mit abendlichem Zusammensitzen der Nachbarn und einem einzigen Wirtshaus der heutigen Prozess- und Wirtshausfreude gegenüberstellen; Einsender Hüttig).",
    "End of the Tanna conversation; Oßla (parable of the sower; conversation of two old men contrasting the good old days, with neighbours sitting together in the evening and a single inn, with today’s love of lawsuits and taverns; contributor Hüttig).",
    ["Sprachproben", "Tanna", "Oßla", "Gleichnis vom Sämann", "Wirtshaus", "Advokaten", "gute alte Zeit", "Mundart", "Oberland"],
    ["dialect samples", "Tanna", "Oßla", "parable of the sower", "inn", "lawyers", "good old days", "dialect", "Oberland"],
    ["Sprachproben", "Mundart"])
add("151",
    "Sprachproben Altengesees (Gleichnis vom Unkraut unter dem Weizen) und Titschendorf (Gleichnis vom Sämann mit Deutung, fränkische Lautung; Fußnote zu Sonderformen der Titschendorfer); Beginn der Wortliste »Idiotismen« (A bis Arzen).",
    "Dialect samples from Altengesees (parable of the tares) and Titschendorf (parable of the sower with interpretation, Franconian pronunciation; footnote on peculiar Titschendorf forms); start of the word list “Idiotismen” (A to Arzen).",
    ["Sprachproben", "Altengesees", "Titschendorf", "Gleichnis", "Idiotismen", "Wortliste", "fränkisch", "Mundart", "Dialektwörter"],
    ["dialect samples", "Altengesees", "Titschendorf", "parable", "idioms", "word list", "Franconian", "dialect", "dialect words"],
    ["Sprachproben", "Mundart"])
add("152",
    "Wortliste der Mundart (Idiotismen) von Ast bis Hingerwerklich: knappe Erklärungen mundartlicher Wörter, darunter Druid (Alp), Büßen (Übel durch Zauber entfernen), Eignen sich (Todesvorzeichen), Gutermuth (Kindtaufe), Hebeschmaus, Pampus, Bröckelpols.",
    "Word list of the dialect (Idiotismen) from Ast to Hingerwerklich: brief explanations of dialect words, among them Druid (nightmare spirit), Büßen (removing ills by magic), Eignen sich (omen of death), Gutermuth (christening), Hebeschmaus, Pampus, Bröckelpols.",
    ["Wortliste", "Idiotismen", "Dialektwörter", "Druid", "Hebeschmaus", "Gutermuth", "Aberglaube", "Kartoffelgerichte", "Mundart"],
    ["word list", "idioms", "dialect words", "Druid", "Hebeschmaus", "Gutermuth", "superstition", "potato dishes", "dialect"],
    ["Mundart"])
add("153",
    "Wortliste der Mundart von Hingerärschlich bis Schälle: u. a. Höhlerbier (Lagerbier), Käsehitsche (Kinderschlitten), Leichenessen, Lih (Kienlichtpfanne), Pimpelmutter (Hebamme), Papperei, Pfannenpolse, Präßläber, ze Rocken gehn, Huzen gehn.",
    "Word list of the dialect from Hingerärschlich to Schälle: among others Höhlerbier (lager beer), Käsehitsche (children’s sledge), Leichenessen (funeral meal), Lih (pine-light pan), Pimpelmutter (midwife), Papperei, Pfannenpolse, Präßläber, ze Rocken gehn, Huzen gehn.",
    ["Wortliste", "Idiotismen", "Dialektwörter", "Hebamme", "Leichenessen", "Lagerbier", "Rockenstube", "Hutzenstube", "Mundart"],
    ["word list", "idioms", "dialect words", "midwife", "funeral meal", "lager beer", "spinning room", "dialect"],
    ["Mundart"])
add("154",
    "Schluss der Wortliste (Schändiren bis Zwieslich: Schotten Molken, Trauerbrod, Unkraut Epilepsie, Unternächte die zwölf Nächte, Zitz). Beginn von »Kleid und Kost«: städtische Mode gegenüber bäuerlicher Tracht, Gera durchweg modisch.",
    "End of the word list (Schändiren to Zwieslich: Schotten whey, Trauerbrod, Unkraut epilepsy, Unternächte the twelve nights, Zitz). Start of “Dress and food”: urban fashion versus peasant costume, Gera fashionable throughout.",
    ["Wortliste", "Idiotismen", "Dialektwörter", "Unternächte", "Trauerbrod", "Kleidung", "Mode", "Tracht", "Gera"],
    ["word list", "idioms", "dialect words", "twelve nights", "funeral bread", "clothing", "fashion", "costume", "Gera"],
    ["Mundart", "Kleidung und Tracht"])
