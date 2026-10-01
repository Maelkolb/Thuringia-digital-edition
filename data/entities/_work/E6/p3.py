from lib import *

# =====================================================================
# 5. Schulen und Bildungseinrichtungen
# =====================================================================
acc("Gymnasium zu Gera", "Gymnasium Rutheneum zu Gera", kind="Schule",
    gloss="Gymnasium illustre Rutheneum at Gera (state grammar school)",
    merges=["Gymnasium", "Gymnasiums", "Gymnasium illustre (Rutheneum", "Gymnasium illustre Rutheneum",
            "fürstlichen Landesschule zu Gera"],
    note="Founded 1608 by Heinrich Posthumus as Gymnasium illustre (Rutheneum), a Landesgymnasium (pp. 375, 435). Bare 'Gymnasium' "
         "(pp. 431-437, 444) is this school; 'fürstliche Landesschule zu Gera' (p. 305) is taken as the same school.")
acc("Rutheneum", "Rutheneum zu Schleiz", kind="Schule", gloss="Rutheneum at Schleiz (grammar school)",
    merges=["Lyceum Rutheneum"], register_page="579",
    note="Not the Gera school of the same name: the Schleiz Rutheneum, municipal and reorganised 1869 on Prussian lines (p. 586).")
acc("Realschule", "Realschule zu Gera", kind="Schule", gloss="Realschule at Gera (secondary school)",
    merges=["Realschule zu Gera"])
acc("höheren Töchterschule", "Höhere Töchterschule zu Gera", kind="Schule", gloss="higher girls' school at Gera",
    merges=["höhere Töchterschule"])
acc("erste Bürgerschule der Knaben", "Erste Bürgerschule der Knaben (Gera)", kind="Schule", gloss="first municipal school for boys, Gera")
acc("zweite Bürgerschule", "Zweite Bürgerschule (Gera)", kind="Schule", gloss="second municipal school, Gera")
acc("dritte Bürgerschule", "Dritte Bürgerschule (Gera)", kind="Schule", gloss="third municipal school, Gera")
acc("Rathskreischule", "Rathskreischule (Gera)", kind="Schule", gloss="council district school (school for the poor), Gera")
acc("Gesammtstadtschule", "Gesammtstadtschule (Gera)", kind="Schule", gloss="united municipal school, Gera",
    merges=["Gesammststadtschule"], note="'Gesammststadtschule' (p. 833, corrigenda) is a spelling variant.")
concept("Bürgerschulen", "Bürgerschule", "Schulform", "municipal school (Bürgerschule)")
acc("Sonntagszeichenschule", "Sonntagszeichenschule (Gera)", kind="Schule", gloss="Sunday drawing school, Gera")
acc("Fortbildungsschule", "Fortbildungsschule (Gera)", kind="Schule", gloss="continuation school, Gera")
acc("Webschule", "Webschule (Gera)", kind="Schule", gloss="weaving school, Gera")
acc("Taubstummenanstalt", "Taubstummenanstalt (Gera)", kind="Schule", gloss="institution for the deaf-mute, Gera")
acc("Agnesschule", "Agnesschule (Untermhaus)", kind="Schule", gloss="Agnesschule (infant school and training for maids), Untermhaus",
    note="Founded 10 Nov. 1869 by the reigning prince and princess as a Kleinkinderbewahranstalt, linked with a training school for female servants (p. 422).")
acc("Handelsschule des Dr. Amthor", "Handelsschule des Dr. Amthor (Gera)", kind="Schule", gloss="commercial school of Dr. Amthor, Gera")
acc("Bergbauschule", "Bergbauschule (Lobenstein)", kind="Schule", gloss="mining school, Lobenstein")
acc("Näh- und Strickschule", "Näh- und Strickschule (Hohenleuben)", kind="Schule", gloss="sewing and knitting school, Hohenleuben")
acc("Michaelisschule", "Michaelisschule zu Lüneburg", kind="Schule", gloss="Michaelisschule at Lüneburg")
acc("Landesseminars", "Landesseminar zu Schleiz", kind="Schule", gloss="teachers' seminary of the state at Schleiz",
    merges=["schleizer Seminar"])
acc("Heinrichstiftung", "Heinrichstiftung (Schleiz)", kind="Stiftung", gloss="Heinrich foundation, Schleiz")
concept("Schule", "Schule", "Einrichtung", "school",
        merges=["Schulen", "städtischen Schulanstalten", "lateinischen Schulen"],
        note="Generic word; the specific schools are separate entries.")
concept("Wanderschulen", "Wanderschule", "Schulform", "itinerant school", merges=["Wanderschule"],
        note="The 'sog. Wanderschulen' of the 17th century (p. 296); 'eigene Wanderschule' (p. 677).")
concept("Akademien", "Akademie", "Einrichtung", "academy (university-level school)")
acc("Schule zu Untermhaus", "Schule zu Untermhaus", kind="Schule", gloss="school of Untermhaus", register_page="420")
acc("Schule von Kulm", "Schule zu Kulm", kind="Schule", gloss="school of Kulm", register_page="675")
acc("Convictorium", "Convictorium zu Leipzig", kind="Stiftung", gloss="Convictorium at Leipzig (free-board foundation)")
acc("v. wiese’schen Bürgerrettungs- und Industriebeförderungsinstitut",
    "v. Wiese’sches Bürgerrettungs- und Industriebeförderungsinstitut (Gera)", kind="Stiftung",
    gloss="v. Wiese foundation for the rescue of citizens and the promotion of industry, Gera")
acc("Volksleseanstalt für das reußische Oberland", "Volksleseanstalt für das reußische Oberland", kind="Bibliothek",
    gloss="public reading institution for the Reuss Upland (Schleiz)")
concept("Lesebibliothek", "Lesebibliothek", "Einrichtung", "lending library", note="Untermhaus, since 1846 (p. 426).")
concept("Volksbibliothek", "Volksbibliothek", "Einrichtung", "people's library", note="Ebersdorf, founded 1866 by the princess (p. 736).")
acc("Gymnasialbibliothek", "Gymnasialbibliothek (Gera)", kind="Bibliothek", gloss="grammar school library, Gera")
acc("Bibliothek, großherzogl", "Großherzogliche Bibliothek (Weimar)", kind="Bibliothek", gloss="Grand-Ducal Library, Weimar",
    note="Subscriber, p. 836.")

# =====================================================================
# 6. Vereine, Gesellschaften, Stiftungen
# =====================================================================
acc("Gesellschaft von Freunden der Naturwissenschaften", "Gesellschaft von Freunden der Naturwissenschaften in Gera",
    kind="Verein", gloss="Society of Friends of the Natural Sciences, Gera",
    merges=["Gesellschaft von Freunden der Naturwissenschaft in Gera und Schleiz", "Gesellschaft von Freunden der Naturwissenschaft",
            "Gesellschaft von Naturfreunden", "naturwissenschaftlicher Verein"],
    note="Publisher of Jahresberichte since 1858. The variants name the same society; 'naturwissenschaftlicher Verein' (p. 441, in the Gera "
         "town description) is taken as this society. The Schleiz society is a separate entry.")
acc("naturwissenschaftlichen Verein in Schleiz", "Naturwissenschaftlicher Verein in Schleiz", kind="Verein",
    gloss="Natural Science Society, Schleiz", merges=["naturhistorischer Verein", "Verein, naturwissenschaftl"],
    note="'Verein, naturwissenschaftl.' = subscriber at Schleiz (p. 839).")
acc("land- und forstwirthschaftlicher Verein", "Land- und forstwirthschaftlicher Verein (Gera)", kind="Verein",
    gloss="agricultural and forestry society, Gera", merges=["Verein, landwirthschaftl"])
acc("voigtländische alterthumsforschende Verein", "Voigtländischer alterthumsforschender Verein zu Hohenleuben", kind="Verein",
    gloss="Voigtland Antiquarian Society, Hohenleuben", register_page="633",
    merges=["voigtländischen alterthumsforschenden Vereins", "alterthumsforschenden Vereins zu Hohenleuben",
            "historischen Vereins zu Hohenleuben", "Verein zu Hohenleuben", "alterthumsforschenden Vereins",
            "voigtländischen Verein", "voigtländischen alterthumsforschenden Vereine", "Verein, alterthumsforschender"],
    note="Runs the museum/collections in Schloss Hohenleuben; Brückner also says 'historischer Verein'.")
acc("Gustav-Adolf-Stiftung", "Gustav-Adolf-Stiftung", kind="Verein", gloss="Gustavus Adolphus Foundation (Protestant aid society)",
    merges=["Gustav-Adolfs-Verein"], note="'Gustav-Adolfs-Verein' (p. 639) is the local branch founded 1845 at Hohenleuben.")
acc("Pestalozziverein", "Pestalozziverein", kind="Verein", gloss="Pestalozzi Society (teachers' relief), founded 1866")
acc("thüringer Brandversicherungsvereins", "Thüringer Brandversicherungsverein", kind="Verein",
    gloss="Thuringian fire insurance society", note="A branch among clergy and teachers (p. 304).")
acc("magdeburger Landfeuersocietät", "Magdeburger Landfeuersocietät", kind="Versicherung",
    gloss="Magdeburg rural fire insurance society",
    merges=["Magdeburger Landfeuer-Societät", "magdeburger Feuerversicherungsanstalt"],
    note="'magdeburger Feuerversicherungsanstalt' (p. 379) is taken as the same institution. Subscriber: its general direction at Altenhausen (p. 836).")
acc("Küchengarten-Gesellschaft", "Küchengarten-Gesellschaft (Gera)", kind="Verein", gloss="Küchengarten society, Gera")
acc("Stenographenverein", "Stenographenverein (Gera)", kind="Verein", gloss="shorthand society, Gera")
acc("Fortbildungsverein für Gewerbtreibende", "Fortbildungsverein für Gewerbtreibende (Gera)", kind="Verein", gloss="continuing-education society for tradesmen, Gera")
acc("Bauverein", "Bauverein (Gera)", kind="Verein", gloss="public-benefit building society, Gera (1864)")
acc("Gärtnerverein unter dem Namen Flora", "Gärtnerverein Flora (Gera)", kind="Verein", gloss="gardeners' society 'Flora', Gera")
acc("thüringer Kunstverein", "Thüringer Kunstverein", kind="Verein", gloss="Thuringian art society")
acc("astronomischen Vereins", "Astronomischer Verein (Gera)", kind="Verein", gloss="astronomical society, Gera")
acc("Gallerie Späthe", "Gallerie Späthe (Gera)", kind="Galerie", gloss="Gallerie Späthe (art and trade exhibition), Gera")
acc("Liedertafel", "Liedertafel", kind="Verein", gloss="Liedertafel (male choral society)", merges=["Liedertafeln"],
    note="Generic type; 'die Liedertafel' (p. 440) is the chief choral society of Gera, '2 Liedertafeln' (p. 590) those of Schleiz.")
acc("Luther-Liedertafel", "Luther-Liedertafel (Hohenleuben)", kind="Verein", gloss="Luther Liedertafel (choral society), Hohenleuben, founded 1846")
acc("Gesangverein", "Gesangverein", kind="Verein", gloss="choral society", merges=["Singverein"],
    note="Generic: choral societies of various places (e.g. Hohenleuben p. 639, p. 687).")
acc("Sängerchor", "Sängerchor (Hohenleuben)", kind="Verein", gloss="singers' choir, Hohenleuben (1857)")
acc("Schützengesellschaft", "Schützengesellschaft (Gera)", kind="Verein", gloss="rifle society, Gera")
acc("Schützenvereine", "Schützenverein", kind="Verein", gloss="rifle society",
    note="Generic: rifle societies of various small towns (pp. 687, 736).")
acc("Schützencompagnie", "Schützencompagnie (Hohenleuben)", kind="Verein", gloss="rifle company, Hohenleuben (1860)")
acc("Bürgererholung", "Bürgererholung (Hohenleuben)", kind="Verein", gloss="citizens' recreation society, Hohenleuben (1860)")
acc("Erholungsgesellschaft", "Erholungsgesellschaft (Hohenleuben)", kind="Verein", gloss="recreation society, Hohenleuben (since 1830)")
acc("Lesezirkel", "Lesezirkel (Hohenleuben)", kind="Verein", gloss="reading circle, Hohenleuben (since 1842)")
acc("Bürgerwehr", "Bürgerwehr (Hohenleuben)", kind="Verein", gloss="citizens' militia, Hohenleuben (1848)")
acc("Kalandbrüder", "Kalandbrüder (Schleiz)", kind="Bruderschaft", gloss="Kaland brotherhood, Schleiz",
    note="Met monthly in the Allerheiligenkirche until the Reformation (p. 584).")
acc("Kalandsbrüdergesellschaft", "Kalandsbrüdergesellschaft (Pahren)", kind="Bruderschaft", gloss="Kaland brotherhood, Pahren (1350)")
acc("geraer Zeugmacherinnung", "Geraer Zeugmacherinnung", kind="Zunft", gloss="Gera weavers' guild (Zeugmacher)")
acc("magdeburger Schöppenstuhls", "Magdeburger Schöppenstuhl", kind="Gericht", gloss="Magdeburg court of aldermen (Schöppenstuhl)")
acc("königsberger Liederbundes", "Königsberger Liederbund", kind="Verein", gloss="Königsberg song circle (of Simon Dach)")

# --- Kapitalien, Banken, Kassen
acc("geraer Bank", "Geraer Bank", kind="Bank", gloss="Gera bank (joint-stock, 4 million Thaler capital)", merges=["Bank"],
    note="'Bank' (p. 431) in the list of Gera buildings is this bank.")
acc("Gewerbebank in Gera", "Gewerbebank in Gera", kind="Bank", gloss="trades bank (Schulze-Delitzsch cooperative), Gera",
    merges=["Gewerbebank"])
acc("Sparkasse", "Sparkasse zu Gera", kind="Bank", gloss="savings bank, Gera (state institution since 1843)")
acc("schleizer Sparkasse", "Sparkasse zu Schleiz", kind="Bank", gloss="savings bank, Schleiz",
    merges=["Sparkassenverwaltung"], note="'Sparkassenverwaltung' (p. 639) is the Hohenleuben branch of the Schleiz savings bank.")
acc("lobensteiner Sparkasse", "Sparkasse zu Lobenstein", kind="Bank", gloss="savings bank, Lobenstein")
acc("Vorschussverein in Schleiz", "Vorschussverein in Schleiz", kind="Bank", gloss="credit cooperative (Vorschussverein), Schleiz")
acc("Landrentenbank", "Landrentenbank", kind="Bank", gloss="state land-annuity bank (planned)",
    note="Proposed institution for redeeming land burdens (p. 229).")
acc("Ed. Glaßchen Bankgeschäfts", "Ed. Glaßchen Bankgeschäft (Gera)", kind="Bank", gloss="Ed. Glaß banking house, Gera (bankrupt 1866)")
acc("Kämmeraholzgelderkasse", "Kämmeraholzgelderkasse", kind="Kasse", gloss="municipal fund for wood money (Kämmerei)")

# --- Firmen, Fabriken, Werke
acc("Kanitz'sche Buchhandlung", "Kanitz'sche Buchhandlung", kind="Firma", gloss="Kanitz bookshop")
acc("Mitscher & Röstell", "Mitscher & Röstell (Berlin)", kind="Firma", gloss="Mitscher & Röstell, bookseller, Berlin", note="Subscriber, p. 838.")
acc("v. Puttkammer & Mühlbrecht", "v. Puttkammer & Mühlbrecht (Berlin)", kind="Firma", gloss="v. Puttkammer & Mühlbrecht, bookseller, Berlin", note="Subscriber, p. 838.")
acc("chemischen Fabrik", "Chemische Fabrik (Heinrichshall)", kind="Fabrik", gloss="chemical factory at Heinrichshall",
    merges=["chemische Fabrik", "Chem. Fabrik", "chemischen Fabrik Heinrichshall"],
    note="Next to the Saline Heinrichshall in the parish of Pohlitz (pp. 38, 505, 507); Brückner's index: 'Chemische Fabrik (Pohlitz) 507'.",
    register_page="507")
place("Saline Heinrichshall", "Saline Heinrichshall", "Saline", "Heinrichshall saltworks", register_page="507", in_principality=True,
      note="Brückner's index: 'Heinrichshall (Pohlitz) 507'.")
acc("Königin-Marienhütte", "Königin-Marienhütte (Cainsdorf bei Zwickau)", kind="Fabrik", gloss="Königin-Marienhütte ironworks near Zwickau",
    merges=["Marienhütte"])
acc("Actien-Stahlgussfabrik", "Actien-Stahlgussfabrik (Saale)", kind="Fabrik", gloss="joint-stock cast-steel factory on the Saale (projected 1867)")
acc("Eisenwerksgesellschaft zu Hüttensteinach", "Eisenwerksgesellschaft zu Hüttensteinach", kind="Firma", gloss="ironworks company of Hüttensteinach")
acc("Fiedlers Baumwollenspinnfabrik", "Fiedlers Baumwollenspinnfabrik", kind="Fabrik", gloss="Fiedler's cotton spinning mill",
    note="Founded 1829, first as Heynisch's mill (p. 784).")
acc("Silberbergwerk Fortuna", "Silberbergwerk Fortuna", kind="Bergwerk", gloss="silver mine Fortuna")
acc("Johanneszeche", "Johanneszeche", kind="Bergwerk", gloss="Johanneszeche alum and vitriol works (1747-c. 1802)")
acc("güldenen Hirsch", "Alaun- und Vitriolwerk „güldener Hirsch“", kind="Bergwerk", gloss="alum and vitriol works 'güldener Hirsch'",
    merges=["Hoff auf Gott"], note="Worked 1683-1716 and (as 'Hoff auf Gott') 1779-1804 (p. 245).")
place("Christiansglück", "Christiansglück", "Werk", "Christiansglück (alum and vitriol works / ironworks)",
      register_page="727", in_principality=True,
      note="Brückner's index: 'Christiansglück (Saaldorf) 727'; locally 'Silberknie' or 'Vitriolwerk'.")
place("Spaniershammer", "Spaniershammer", "Hammerwerk", "Spaniershammer (hammer works)", register_page="728", in_principality=True,
      note="Index: 'Spaniershammer (Saaldorf) 728'.")
place("polnische Hammer", "Polnischer Hammer", "Hammerwerk", "Polish hammer (hammer works)", in_principality=True)
place("Neuhammer", "Neuhammer", "Hammerwerk", "Neuhammer (hammer works)", register_page="727", in_principality=True,
      note="Index: 'Neuhammer (Saaldorf) 727'; at the Saale below the Muckenberg. A second Neuhammer lies near Lobenstein.")
place("Heinrichshütte", "Heinrichshütte", "Eisenhütte", "Heinrichshütte (ironworks/foundry)", register_page="770", in_principality=True,
      note="Index: 'Heinrichshütte (Wurzbach) 770'.")
place("Rosenthal", "Rosenthal", "Fabrik", "Rosenthal (spinning mill at Blankenstein)", register_page="834", in_principality=True,
      note="'Die Spinnfabrik zu Blankenstein führt den Namen Rosenthal' (p. 834, corrigenda).")
acc("pfortner Brauerei", "Brauerei Pforten", kind="Betrieb", gloss="brewery at Pforten", register_page="450")
acc("Gemeindebrauhause", "Gemeindebrauhaus", kind="Betrieb", gloss="communal brewhouse")
concept("Brauerei", "Brauerei", "Betrieb", "brewery", merges=["Bierbrauerei"])
concept("Ziegelei", "Ziegelei", "Betrieb", "brickworks")
concept("Tuchfabrik", "Tuchfabrik", "Betrieb", "cloth factory")
concept("Spinnfabrik", "Spinnfabrik", "Betrieb", "spinning mill")
concept("Porzellanfabrik", "Porzellanfabrik", "Betrieb", "porcelain factory")
concept("Lederfabrik", "Lederfabrik", "Betrieb", "leather factory")
concept("Wollengarnspinnerei", "Wollgarnspinnerei", "Betrieb", "woollen yarn spinning mill", merges=["Wollgarnspinnerei"])
concept("Harmonikafabrikation", "Harmonikafabrik", "Betrieb", "accordion factory")
concept("Stärkefabrikation", "Stärkefabrik", "Betrieb", "starch factory")
concept("Salpeter- und Pottaschensiedereien", "Salpeter- und Pottaschensiederei", "Betrieb", "saltpetre and potash boileries")

# --- Gasthoefe
acc("Sonne", "Gasthof Sonne (Schleiz)", kind="Gasthof", gloss="inn 'Sonne', Schleiz", note="'der einzige Gasthof ersten Ranges' (p. 589).")
acc("Erbprinz", "Gasthof Erbprinz (Schleiz)", kind="Gasthof", gloss="inn 'Erbprinz', Schleiz", merges=["blaue Engel"],
    note="Formerly 'der berühmte blaue Engel' (p. 589).")
acc("drei Schwanen", "Gasthof zu den drei Schwanen (Schleiz)", kind="Gasthof", gloss="inn 'Three Swans', Schleiz")
acc("baierische Hof", "Baierischer Hof (Schleiz)", kind="Gasthof", gloss="inn 'Baierischer Hof', Schleiz", merges=["goldener Wolf"],
    note="Formerly 'goldener Wolf' (p. 589).")
acc("Privatgasthof zum Mohren", "Gasthof zum Mohren (Untermhaus)", kind="Gasthof", gloss="inn 'zum Mohren', Untermhaus", register_page="420")
acc("Fürstenkeller", "Fürstenkeller (Untermhaus)", kind="Gasthof", gloss="Fürstenkeller (tavern at the brewery), Untermhaus", register_page="420")
acc("Gasthof zum Lindenthal", "Gasthof zum Lindenthal (Pforten)", kind="Gasthof", gloss="inn 'zum Lindenthal', Pforten",
    merges=["Lindenthalgasthof"], register_page="450")
acc("Gasthof „die Kapelle", "Gasthof „die Kapelle“", kind="Gasthof", gloss="inn 'die Kapelle'", note="Locally 'die Kappel' (p. 692).")

# =====================================================================
# 7. Kirchen, Hospitaeler und andere Bauten
# =====================================================================
concept("Trinitatiskirche zu Gera", "Trinitatiskirche zu Gera", "Bauwerk", "Trinity Church, Gera",
        merges=["Trinitatiskirche", "St. Trinitatiskirche", "St. Trinitatis"],
        note="Also called Friedhofskirche, built 1613 at the Gottesacker (p. 432).")
concept("St. Johanniskirche", "St. Johanniskirche zu Gera", "Bauwerk", "St John's Church, Gera",
        merges=["Johanniskirche", "St. Johannis-"])
concept("St. Salvatorkirche", "St. Salvatorkirche zu Gera", "Bauwerk", "St Saviour's Church, Gera", merges=["St. Salvator"])
concept("Waisenhauskirche", "Waisenhauskirche zu Gera", "Bauwerk", "orphanage church, Gera")
concept("Bergkirche", "Bergkirche zu Schleiz", "Bauwerk", "Bergkirche (Church of St Mary on the hill), Schleiz", merges=["St. Marien"],
        register_page="579", note="Officially 'St. Marien' (p. 582: 'Kirche zu St. Marien, gewöhnlich die Bergkirche genannt').")
concept("St. Wolfgangskapelle", "St. Wolfgangskapelle zu Schleiz", "Bauwerk", "St Wolfgang's chapel, Schleiz", register_page="579")
concept("Georgenkirche zu Schleiz", "Georgenkirche zu Schleiz", "Bauwerk", "St George's Church, Schleiz", merges=["Georgenkirche"], register_page="579")
concept("Kirche zu Schleiz", "Kirche zu Schleiz", "Bauwerk", "church of Schleiz", merges=["schleizer Kirche"], register_page="579")
concept("Peterskirche in Weida", "Peterskirche in Weida", "Bauwerk", "St Peter's Church, Weida")
concept("Petrikirche", "Petrikirche (Erfurt)", "Bauwerk", "Petrikirche, Erfurt", note="Only as a comparison for the tower of the Bergkirche (p. 133).")
concept("Marienkirche", "Marienkirche", "Bauwerk", "Church of St Mary",
        note="Homonyms: the Marienkirche at Nordhausen (p. 133, architectural comparison) and the Marienkirche of Schleiz, i.e. the Bergkirche (p. 582).")
concept("Marienkirche zu Pottendorf", "Marienkirche zu Pottendorf", "Bauwerk", "St Mary's Church, Pottendorf (destroyed)")
concept("Kirche zu Untermhaus", "Kirche zu Untermhaus", "Bauwerk", "church of Untermhaus", register_page="420")
concept("Kirche in Langenberg", "Kirche in Langenberg", "Bauwerk", "church of Langenberg", register_page="508")
concept("Kirche zu Hirschberg", "Kirche zu Hirschberg", "Bauwerk", "church of Hirschberg", register_page="809")
concept("Kirche zu Roben", "Kirche zu Roben", "Bauwerk", "church of Roben", register_page="515")
concept("Kirche zu Köstritz", "Kirche zu Köstritz", "Bauwerk", "church of Köstritz", register_page="494")
concept("Kirche zu Großenstein", "Kirche zu Großenstein", "Bauwerk", "church of Großenstein")
concept("Kirche zu Schmirchau", "Kirche zu Schmirchau", "Bauwerk", "church of Schmirchau")
concept("Kirche zu Rödersdorf", "Kirche zu Rödersdorf", "Bauwerk", "church of Rödersdorf", register_page="611")
concept("thieschützer Kirche", "Kirche zu Thieschütz", "Bauwerk", "church of Thieschütz")
concept("Kirche zu Gesell", "Kirche zu Gesell", "Bauwerk", "church of Gesell", merges=["geseller Kirche"])
concept("Kirche von Gera", "Kirche von Gera", "Bauwerk", "church of Gera", note="p. 421: 'Anfänglich wurde die Kirche von Gera aus besorgt' (a chapel served from Gera).")
concept("Stadtkirche", "Stadtkirche", "Bauwerk", "town church", note="Generic; the town church of Schleiz, Saalburg or Hirschberg, depending on the passage.")
concept("Ortskirche", "Ortskirche", "Bauwerk", "village church", note="Generic: the church of the village being described.")
concept("Kirche", "Kirche", "Einrichtung", "church", merges=["Kirchen"],
        note="Generic word (the church as institution or building).")
concept("Kloster", "Kloster", "Einrichtung", "monastery", merges=["Klöster", "Klöstern"],
        note="Generic word. Often 'das Kloster (bei Saalburg)' = Kloster zum heil. Kreuz; also legendary 'versunkene Klöster' near Schleiz and Arlas.")
concept("Pfarrei", "Pfarrei", "Einrichtung", "parish", merges=["Pfarramte"])
concept("Superintendentur", "Superintendentur", "Einrichtung", "superintendency (church district and its seat)")
concept("Diaconat", "Diaconat", "Einrichtung", "deaconate (second clergy post and its house)")
concept("Waisenhaus", "Waisenhaus", "Einrichtung", "orphanage")
concept("Apotheke", "Apotheke", "Einrichtung", "pharmacy", merges=["Apotheken"])
concept("Krankenhausstation", "Krankenhausstation", "Einrichtung", "hospital ward", note="Hohenleuben (p. 169).")
acc("Krankenhaus", "Städtisches Krankenhaus (Gera)", kind="Anstalt", gloss="municipal hospital, Gera (founded 1850)",
    merges=["städtischen Krankenhauses"])
acc("Kaltwasserheilanstalt", "Kaltwasserheilanstalt (Langenberg)", kind="Anstalt", gloss="cold-water cure establishment, Langenberg",
    merges=["Wasserheilanstalt"], register_page="508",
    note="Founded by Dr. Blau at Langenberg (p. 43); 'Wasserheilanstalt' (p. 510) is the same.")
acc("Heilbadeanstalt", "Heilbadeanstalt (Lobenstein)", kind="Anstalt", gloss="spa bath establishment, Lobenstein (1869)")
acc("St. Wolfgang", "Hospital St. Wolfgang (Gera)", kind="Hospital", gloss="St Wolfgang hospital, Gera ('der arme Spittel')",
    merges=["Hospitäler St. Wolfgang", "Hospitäler"],
    note="'Hospitäler' (p. 833, corrigenda) = the two hospitals united in 1868.")
acc("beatae virginis Mariae", "Hospital beatae virginis Mariae (Gera)", kind="Hospital",
    gloss="hospital of the Blessed Virgin Mary, Gera ('der reiche Spittel')",
    merges=["Hospitäler beatae virginis Mariae", "Marienhospitals"],
    note="'Marienhospital' (p. 433) is taken as this hospital; the new church of 1782 was built on its former site.")
acc("Hospital zu Wunsiedel", "Hospital zu Wunsiedel", kind="Hospital", gloss="hospital at Wunsiedel")
acc("Langenberger Spital", "Langenberger Spital", kind="Hospital", gloss="hospital of Langenberg", register_page="508")
acc("weidaischen Terminei", "Weidaische Terminei (Gera)", kind="Kloster", gloss="collecting house (Terminei) of the Weida friars, Gera",
    note="Site of the Diaconat at Gera (p. 433).")
concept("Hauptsteueramtsgebäude", "Hauptsteueramtsgebäude (Gera)", "Bauwerk", "main tax office building, Gera (1867)")
concept("Staat", "Staat", "Staatswesen", "state", note="Generic: 'der Staat' (p. 177).")

# =====================================================================
# 8. Gemeinden, Rittergueter, Kammergueter
# =====================================================================
acc("Köstritzer Gemeinde", "Gemeinde Köstritz", kind="Gemeinde", gloss="municipality of Köstritz", register_page="494")
acc("Gemeinde Kaimberg", "Gemeinde Kaimberg", kind="Gemeinde", gloss="municipality of Kaimberg", register_page="562")
acc("Commune Hohenleuben", "Gemeinde Hohenleuben", kind="Gemeinde", gloss="municipality of Hohenleuben", register_page="633")
concept("Rittergut", "Rittergut", "Gutsform", "manor (Rittergut)", note="Generic: the manor of the village being described (p. 480).")
concept("Kammergut", "Kammergut", "Gutsform", "domain estate (Kammergut)", merges=["Kammergute", "Kammergutes", "fürstliches Kammergut"],
        note="Generic: estates managed by the princely chamber; named ones are separate place entries.")
place("Ritterguts Großsaara", "Rittergut Großsaara", "Rittergut", "manor of Großsaara", register_page="467", in_principality=True)
place("Rittergute zu Scheubengrobsdorf", "Rittergut Scheubengrobsdorf", "Rittergut", "manor of Scheubengrobsdorf", register_page="472", in_principality=True)
place("Rittergut zu Frankenthal", "Rittergut Frankenthal", "Rittergut", "manor of Frankenthal", register_page="473", in_principality=True)
place("rubitzer Rittergut", "Rittergut Rubitz", "Rittergut", "manor of Rubitz", register_page="478", in_principality=True)
place("Rittergute Dürrenberg", "Rittergut Dürrenberg", "Rittergut", "manor of Dürrenberg", register_page="494", in_principality=True,
      note="Index: 'Dürrenberg (Hartmannsdorf) 494'.")
place("Rittergute Steinbrücken", "Rittergut Steinbrücken", "Rittergut", "manor of Steinbrücken", register_page="517", in_principality=True)
place("Rittergutes Zschippach", "Rittergut Zschippach", "Rittergut", "manor of Zschippach", register_page="547", in_principality=True)
place("Rittergute Pforten", "Rittergut Pforten", "Rittergut", "manor of Pforten", merges=["pfortner Rittergute"], register_page="450", in_principality=True)
place("Rittergut Kaimberg", "Rittergut Kaimberg", "Rittergut", "manor of Kaimberg", register_page="562", in_principality=True)
place("Rittergute zu Lichtenberg", "Rittergut Lichtenberg", "Rittergut", "manor of Lichtenberg", register_page="563", in_principality=True)
place("Rittergut Reichenfels", "Rittergut Reichenfels", "Rittergut", "manor of Reichenfels", register_page="630", in_principality=True)
place("Rittergut zu Blankenberg", "Rittergut Blankenberg", "Rittergut", "manor of Blankenberg",
      note="Patron of the church at Blankenberg (p. 804).")
place("Rittergute Blintendorf", "Rittergut Blintendorf", "Rittergut", "manor of Blintendorf", register_page="792", in_principality=True)
place("Rittergute Frössen", "Rittergut Frössen", "Rittergut", "manor of Frössen", register_page="795", in_principality=True)
place("harraer Rittergute", "Rittergut Harra", "Rittergut", "manor of Harra", register_page="786", in_principality=True)
place("Waldrittergute Arlas", "Waldrittergut Arlas", "Rittergut", "forest manor of Arlas", merges=["Waldrittergut"],
      register_page="804", in_principality=True, note="Consolidated with Blankenstein (p. 804).")
place("Rittergut Zollgrün", "Rittergut Zollgrün", "Rittergut", "manor of Zollgrün", register_page="693", in_principality=True)
place("Rittergüter Frankendorf", "Rittergut Frankendorf", "Rittergut", "manor of Frankendorf", register_page="690", in_principality=True,
      note="Named together with Seubtendorf (p. 700).")
place("Rittergütern Schilbach", "Rittergut Schilbach", "Rittergut", "manor of Schilbach", register_page="691", in_principality=True)
place("Kammergute Galenberg", "Kammergut Galenberg", "Kammergut", "domain estate of Galenberg", register_page="723", in_principality=True)
place("Kammergute Pöritzsch", "Kammergut Pöritzsch", "Kammergut", "domain estate of Pöritzsch", register_page="730", in_principality=True)
place("Kammerguts Kleinaga", "Kammergut Kleinaga", "Kammergut", "domain estate of Kleinaga", register_page="525", in_principality=True)
place("Kammergut Seubtendorf", "Kammergut Seubtendorf", "Kammergut", "domain estate of Seubtendorf", register_page="681", in_principality=True)
place("Kammergute Hirschberg", "Kammergut Hirschberg", "Kammergut", "domain estate of Hirschberg", register_page="809", in_principality=True)

# =====================================================================
# 9. Rejects, fragments, noise
# =====================================================================
rej("Landbaumeister", "title of an official (person), not an institution")
rej("Reichspostmeister", "title of an official (person), not an institution")
rej("Braunkohlenwerksbesitzer", "occupation (lignite-mine owner), not an institution")
rej("Saalburger", "demonym (inhabitants of Saalburg), not an institution")
rej("Hirschberger", "demonym (inhabitants of Hirschberg), not an institution")
rej("hirschberger Schloßherrn", "title of a person (lord of Hirschberg castle), not an institution")
rej("v. watzdorfische", "adjective from a noble family name, no entity")
rej("v. beulwitz-rettenbachsche", "adjective from a noble family name, no entity")
rej("geraer Raths- und oberröppischer Lehn", "descriptive phrase for fiefs, no single entity")
rej("Kirchen-", "fragment of 'Kirchen- und Schulbesuch' (church attendance)")
rej("Schulbesuch", "school attendance, not an institution")
rej("Hag’lvorsicherg’n", "dialect text (spoken line), not an institution")
mrg("Stift", "Kloster Cronswitz")  # p. 454: 'das genannte Stift' = Stift Cronswitz
mrg("Klosters", "Kloster zum heil. Kreuz")
mrg("deutschen Ordensbrüder", "deutschen Orden")
