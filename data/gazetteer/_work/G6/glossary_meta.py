# -*- coding: utf-8 -*-
"""G6 glossary: each entry has a regex; the page list is computed from the page texts (765-825)."""

GLOSS = []


def G(term, variants, kind, de, en, rx):
    GLOSS.append({"term": term, "variants": variants, "kind": kind, "de": de, "en": en, "_rx": rx})


# ---- units
G("Fuß", ["Fuss"], "unit",
  "Längenmaß; in den Ortsartikeln für Höhenlagen („1800 Fuß hoch“) und Bauhöhen. Brückners Umrechnungstabelle nennt den preußischen Fuß (139,13 Pariser Linien) mit 0,313853 m (S. 831); welcher Fuß den Höhenangaben zugrunde liegt, sagt der Text nicht.",
  "Unit of length; in the place articles used for elevations (“1800 Fuß hoch”) and building heights. Brückner's conversion table gives the Prussian foot (139.13 Paris lines) as 0.313853 m (p. 831); the text does not say which foot underlies the elevations.",
  r"\d\s?Fu(?:ß|ss)\b")
G("Morgen", ["Mrg."], "unit",
  "Flächenmaß für Fluren, Gemeindeland und Gutsflächen; 1 preußischer Morgen = 180 Quadratruthen = 0,255322 ha (S. 832). Bruchteile stehen im Druck als „2501 1/10 Morgen“ oder mit hochgestellten Ziffern.",
  "Unit of area for village lands, municipal land and estates; 1 Prussian Morgen = 180 square rods = 0.255322 ha (p. 832). Fractions are printed as “2501 1/10 Morgen” or with superscript digits.",
  r"\d\s?Morgen")
G("□Ruthe", ["Quadratruthe", "☐Ruthen", "□Ruthen"], "unit",
  "Quadratruthe, Flächenmaß hinter Morgenzahlen („23 Morgen 9 □Ruthen“); 1 preußische Quadratruthe = 14,184579 m² (S. 832), 180 Quadratruthen = 1 Morgen.",
  "Square rod, unit of area following Morgen figures (“23 Morgen 9 □Ruthen”); 1 Prussian square rod = 14.184579 m² (p. 832), 180 square rods = 1 Morgen.",
  r"[□☐]\s?Ruthen|\d\s?Ruthen")
G("Eimer", [], "unit",
  "Hohlmaß; Brückner nennt für Lobenstein 1 Eimer = 72 Kannen = 0,6435 hl, für Hirschberg 64 Kannen = 0,7328 hl (S. 832). Hier beim Spiritusabsatz von Göritz (über 600 Eimer).",
  "Liquid measure; Brückner gives 1 Eimer = 72 Kannen = 0.6435 hl for Lobenstein and 64 Kannen = 0.7328 hl for Hirschberg (p. 832). Here for the spirits trade of Göritz (over 600 Eimer).",
  r"Eimer")
G("Ctr.", ["Centner"], "unit",
  "Zentner, Gewichtsmaß (Göritz: Sohlleder gegen 160 Ctr.). Brückner gibt nur 1 Pfund (Zollpfund) = 0,5 kg an (S. 832); die Zentnergröße nennt er nicht.",
  "Hundredweight, unit of weight (Göritz: about 160 Ctr. of sole leather). Brückner only gives 1 pound (Zollpfund) = 0.5 kg (p. 832); he does not state the size of the hundredweight.",
  r"Ctr\.")
G("Fuder", [], "unit",
  "Fuhre, Wagenladung als Mengenangabe für Heu und Grummet (Heinrichsgrün 1647: Wieswachs zu 66 Fuder); eine Umrechnung gibt der Text nicht.",
  "Cartload, used as a quantity for hay and aftermath (Heinrichsgrün 1647: meadow yield of 66 Fuder); the text gives no conversion.",
  r"Fuder")
G("Scheffel", [], "unit",
  "Getreide- und Aussaatmaß (Heinrichsgrün: Feld zu 93 Scheffel Aussaat). Brückner gibt für Schleiz 1 Scheffel = 1,4237 hl an (S. 832), für Lobenstein nur Achtel-Maße.",
  "Grain and sowing measure (Heinrichsgrün: fields requiring 93 Scheffel of seed). Brückner gives 1 Scheffel = 1.4237 hl for Schleiz (p. 832), only eighth-measures for Lobenstein.",
  r"Scheffel")

# ---- currency
G("Thlr.", ["Thaler", "Thlr"], "currency",
  "Thaler, Rechnungs- und Umlaufmünze, in der Gemeindeschulden, Vermögen, Pachtsätze, Baukosten und Jahresausgaben der Orte angegeben werden.",
  "Thaler, the money of account and circulation in which municipal debts, assets, rents, building costs and annual expenditure of the places are stated.",
  r"Thlr\.")
G("Gulden", ["f."], "currency",
  "Gulden; in diesem Teil bei Stiftungen und Renten (Hirschberg: kochische Stiftung mit 3000 Gulden Kapital, Rente von 120 Gulden). Die Abkürzung „f.“ (Heinrichsgrün 1647: „58 f.“) ist wohl derselbe Gulden; der Text erklärt sie nicht.",
  "Guilder; in this part used for foundations and annuities (Hirschberg: the Koch foundation with a capital of 3000 guilders, an annuity of 120 guilders). The abbreviation “f.” (Heinrichsgrün 1647: “58 f.”) is probably the same guilder; the text does not explain it.",
  r"Gulden")
G("Mk.", ["Mark"], "currency",
  "Mark als Rechnungseinheit älterer Art: Anschläge von Rittergütern in den Landestheilungsacten von 1647 (z. B. 2000 Mk.), Kirchenvermögen (Weitisberga 40 Mk.) und Baukosten (Hirschberg 9000 Mk.; Blintendorf „594 Mk. 5 Gr.“ mit Groschen). Eine Umrechnung gibt Brückner nicht.",
  "Mark as an older unit of account: valuations of manors in the 1647 partition records (e.g. 2000 Mk.), church assets (Weitisberga 40 Mk.) and building costs (Hirschberg 9000 Mk.; Blintendorf “594 Mk. 5 Gr.” with groschen). Brückner gives no conversion.",
  r"\d\s?Mk\.")
G("Aßo", [], "currency",
  "Im Druck als „Aßo“ gesetzte Geldangabe bei Kirchen- und Pfarrbaukosten (S. 777: „1452²/₃ Aßo“; ebenso S. 764). Die Abkürzung wird nicht erklärt; die Lesung ist am Faksimile (S. 777) bestätigt.",
  "Monetary abbreviation printed as “Aßo” for church and rectory building costs (p. 777: “1452²/₃ Aßo”; also p. 764). The abbreviation is not explained; the reading was confirmed on the facsimile (p. 777).",
  r"Aßo")

# ---- land and tenure
G("Häusler", ["Kleinhäusler", "Hintersiedler", "Tropfhäusler"], "term",
  "Besitzstufen unterhalb des Bauern: Häusler bzw. Kleinhäusler besitzen ein Haus mit wenig oder keinem Feldbesitz, Hintersiedler sitzen auf abgetrennten Hofteilen; „Tropfhäusler (Taglöhner)“ nennt Brückner S. 765 als Gleichsetzung. Die Orte werden nach Bauern, Häuslern, Taglöhnern und Dienstboten gegliedert.",
  "Tenure classes below the farmer: Häusler or Kleinhäusler own a house with little or no farmland, Hintersiedler live on split-off parts of a farm; on p. 765 Brückner equates “Tropfhäusler” with day labourers. The places are broken down into farmers, cottagers, day labourers and servants.",
  r"Häusler|Hintersiedler|Tropfhäusler")
G("Fröhner", ["Frohnhäuser", "Frohndienste"], "term",
  "Frondienstpflichtige Hintersassen eines Gutsherrn, die für das Rittergut Hand- und Spanndienste leisten mussten (Göritz: drei Tage unentgeltlich, drei Tage für 16 Pfennige Taglohn wöchentlich). Als Erbfrohnbauern und Fröhner beschreibt Brückner die ältere Dorfbevölkerung vieler Rittergutsorte.",
  "Dependent tenants obliged to perform labour services for a lord of the manor (Göritz: three days a week unpaid, three days for a day wage of 16 pfennigs). Brückner describes the older village population of many manor villages as hereditary labour-due farmers and Fröhner.",
  r"Fröhner|Frohn")
G("Bauerngüter, Grundstücksverbände, ledige Grundstücke", ["Pertinenzen", "walzende Grundstücke"], "term",
  "Zählkategorien des bäuerlichen Grundbesitzes, die am Ende der Gemeindebeschreibung stehen (z. B. „29 Bauerngüter, 7 Grundstücksverbände und 62 ledige Grundstücke“). Bauerngüter sind geschlossene Höfe nach Größenklassen in Morgen (ganze, halbe, Viertel- und Achtelgüter); ledige Grundstücke sind nicht zu einem Gut gehörige Einzelflächen (Brückner S. 224: sechs auf ein geschlossenes Gut). „Walzende Grundstücke“ ist wohl dieselbe Kategorie in anderer Wortwahl; Grundstücksverband und Pertinenz werden nicht definiert.",
  "Counting categories of peasant landholding given at the end of the municipality descriptions (e.g. “29 farms, 7 land associations and 62 loose plots”). Bauerngüter are closed farms by size class in Morgen (whole, half, quarter and eighth farms); loose plots are single parcels not belonging to a farm (Brückner p. 224: six per closed farm). “Walzende Grundstücke” is probably the same category in other words; Grundstücksverband and Pertinenz are not defined.",
  r"Grundstücksverband|Grundstückverband|Pertinenz|ledige Grundst|walzende Grundst")
G("Rittergut", [], "term",
  "Adliges Gut mit besonderen Rechten (Ober- und Erbgerichte, Lehen, Kirchensatz); in vielen Orten dieses Teils der Ausgangspunkt der Besiedlung und später zerschlagen, an die Landesherrschaft gefallen oder zum Kammergut geworden.",
  "Noble estate with special rights (high and hereditary jurisdiction, fiefs, church patronage); in many places of this part the starting point of settlement, later broken up, reverted to the ruler or turned into a Kammergut.",
  r"Rittergut|Rittergüter")
G("Kammergut", [], "term",
  "Landesherrliches (fürstliches) Gut, das aus einem heimgefallenen oder angekauften Rittergut entstanden ist (Harra, Dobareuth, Heinrichsgrün, Hirschberg), oft mit Schäferei.",
  "Estate of the territorial ruler, formed from a reverted or purchased manor (Harra, Dobareuth, Heinrichsgrün, Hirschberg), often with a sheep farm.",
  r"Kammergut|Kammergüter")
G("Vorwerk", [], "term",
  "Zum Gut gehörender Wirtschaftshof außerhalb des Herrensitzes (Schlegel und Kießling zum Gut Harra; Niedergrün).",
  "Outlying farm belonging to an estate (Schlegel and Kießling for the Harra estate; Niedergrün).",
  r"Vorwerk")
G("Klostergut", ["Klosterhof"], "term",
  "Gut, das einem Kloster oder Stift zinste oder gehörte; in Pottiga das Gut des Stifts zum heil. Kreuz bei Saalburg, zuletzt in fünf Bauernhöfe geteilt, zusammen „Klosterhof“ genannt.",
  "Estate belonging or paying rent to a monastery or foundation; in Pottiga the estate of the Holy Cross foundation near Saalburg, finally divided into five farms, together called “Klosterhof”.",
  r"Klostergut|Klosterhof|Klosterbauern")
G("Ober- und Erbgerichte", ["Obergerichte", "Erbgerichte"], "term",
  "Rechte der Gerichtsbarkeit über einen Ort: die Obergerichte (höhere Gerichtsbarkeit) standen meist der Landesherrschaft oder dem Besitzer der Herrschaft zu, die Erbgerichte (niedere, erbliche Gerichtsbarkeit) dem Rittergut oder der Stadt. Brückner führt am Ende fast jedes Ortsartikels auf, wem sie zustanden.",
  "Rights of jurisdiction over a place: the high courts (higher jurisdiction) usually belonged to the territorial ruler or lord of the dominion, the hereditary courts (lower, hereditary jurisdiction) to the manor or the town. Brückner states at the end of almost every place article who held them.",
  r"Obergericht|Erbgericht|Ober- und Erbgericht")
G("Lehen", ["Lehn", "Afterlehn"], "term",
  "Lehen: an Vasallen verliehener Besitz oder verliehene Rechte (Schloss-, Pfarr-, Kirchen-, Rathslehen usw.); Afterlehn (dominium utile) bezeichnet das Untereigentum an einem Lehen (S. 810: die Lehngerechtigkeit/dominium directum lag bei Böhmen bzw. den Burggrafen, das Afterlehn bei den v. Beulwitz).",
  "Fief: property or rights granted to a vassal (castle, parish, church, council fiefs etc.); Afterlehn (dominium utile) is the sub-ownership of a fief (p. 810: the feudal overlordship/dominium directum lay with Bohemia and the burgraves, the sub-fief with the v. Beulwitz).",
  r"Lehen|Lehn|Afterlehn")
G("Kirchensatz", ["Patronat"], "term",
  "Patronatsrecht, also das Recht, die Pfarrstelle zu besetzen; mit Rittergütern verbunden (Weitisberga, Wurzbach, Oßla) oder landesherrlich; für Hirschberg, Frössen und Arlas lange zwischen Reuß und Brandenburg-Baireuth strittig (S. 811).",
  "Right of patronage, i.e. the right to appoint the pastor; attached to manors (Weitisberga, Wurzbach, Oßla) or held by the ruler; for Hirschberg, Frössen and Arlas long disputed between Reuss and Brandenburg-Bayreuth (p. 811).",
  r"Kirchensatz|Patronat|Besetzungsrecht")
G("Pflege", [], "term",
  "Verwaltungs- und Herrschaftsbezirk unter einem Pfleger; die „Herrschaft und Pflege Hirschberg“ (Reichsveste mit umliegenden Orten, später als Amt geführt, S. 809) ist der bekannteste Fall im Ortsteil.",
  "Administrative and lordship district under a Pfleger (steward); the “lordship and Pflege of Hirschberg” (imperial fortress with surrounding places, later run as an Amt, p. 809) is the best-known case in this part.",
  r"\bPflege\b")
G("Reichslehen", ["Reichsveste", "Reichsvoigt"], "term",
  "Unmittelbar vom Reich oder (später) von der Krone Böhmen zu Lehen gehende Herrschaft: Sparnberg mit Blintendorf und Ullersreuth, Hirschberg als Reichsveste unter Reichsvoigten.",
  "Dominion held directly from the Empire or (later) from the Crown of Bohemia: Sparnberg with Blintendorf and Ullersreuth, Hirschberg as an imperial fortress under imperial bailiffs.",
  r"Reichslehn|Reichslehen|Reichsveste|Reichsvoigt|Reichsgut|Reichsherrschaft|Reichsgebietlein")
G("zweiherrisch", ["Zweiherrische"], "term",
  "Von zwei Landesherrschaften beherrschter Ort: Weitisberga (Schwarzburg und Reuß), Blintendorf (Preußen und Reuß) u. ä.; dort liegen Kirche oder Schule oft jenseits der Grenze.",
  "Place ruled by two territorial lordships: Weitisberga (Schwarzburg and Reuss), Blintendorf (Prussia and Reuss) etc.; there church or school often lie on the other side of the border.",
  r"[Zz]weiherrisch")
G("Marktflecken", [], "term",
  "Ort mit Marktrecht unterhalb des Stadtrechts; Wurzbach wird so bezeichnet, Hirschberg galt nach den Landestheilungsacten von 1647 nur als Marktflecken (S. 816).",
  "Place with market rights but no town charter; Wurzbach is so called, Hirschberg counted only as a Marktflecken according to the 1647 partition records (p. 816).",
  r"Marktflecken")

# ---- church and school
G("Filial", ["Filialkirche"], "institution",
  "Kirche ohne eigene Pfarrei, die von einer Mutterkirche aus versorgt wird (Oßla von Wurzbach, Langgrün von Seubtendorf, Blintendorf von Gefell, Weitisberga von Heberndorf); „eingepfarrt“ heißen die Orte ohne eigene Kirche.",
  "Church without its own parish, served from a mother church (Oßla from Wurzbach, Langgrün from Seubtendorf, Blintendorf from Gefell, Weitisberga from Heberndorf); places without a church of their own are “eingepfarrt” (assigned to a parish).",
  r"Filial")
G("Vicarie", ["Vikarie"], "institution",
  "Geistlichenstelle unterhalb der Pfarrei; Oßla erhielt 1497 auf Betreiben der Einwohner eine eigene Vicarie, 1512 mit einem Pfarrgut ausgestattet (S. 771).",
  "Clerical post below the rank of a parish; Oßla received its own vicarage in 1497 at the request of its inhabitants, endowed with a glebe in 1512 (p. 771).",
  r"Vicarie")
G("Diaconat", ["Diaconus", "Diakonat"], "institution",
  "Zweite Geistlichenstelle (Diaconus) an einer Kirche, auch die dazugehörige Pfründe mit Lehen (Gefell: „Kirche, Pfarrei und Diaconat“; 1416 neu errichtetes Diaconat zu Gefell, S. 823).",
  "Second clerical post (deacon) at a church, also the associated benefice with fiefs (Gefell: “church, rectory and deaconry”; deaconry at Gefell newly established in 1416, p. 823).",
  r"Diacon")
G("Streitkirchen", [], "term",
  "Name für die Kirchen Gefell, Hirschberg, Frössen und Arlas, um deren kirchliche Hoheit sich Naumburg und Bamberg, später Reuß und Brandenburg-Baireuth stritten, bis Preußen 1804 das Patronat abtrat (S. 811).",
  "Name for the churches of Gefell, Hirschberg, Frössen and Arlas, whose ecclesiastical sovereignty was disputed between Naumburg and Bamberg and later between Reuss and Brandenburg-Bayreuth until Prussia ceded the patronage in 1804 (p. 811).",
  r"Streitkirch")
G("Kirchweih", ["Kirchweihe"], "term",
  "Jährliches Fest zum Weihetag der Kirche, meist mit Jahrmarkt verbunden (Oßla: Sonntag nach Kreuzeserhöhung; Frössen: früher letzter Trinitatissonntag; Arlas: Sonntag Exaudi).",
  "Annual festival on the dedication day of a church, usually combined with a fair (Oßla: Sunday after Holy Cross Day; Frössen: formerly the last Trinity Sunday; Arlas: Sunday Exaudi).",
  r"Kirchweih")
G("Maienfest", [], "term",
  "Frühsommerliches Dorffest mit Maienbaum: in Seibis zu Johanni, in Schlegel alle drei Jahre neben der Kirchweih (S. 782/783).",
  "Early-summer village festival with a maypole: at Seibis on St John's Day, at Schlegel every three years alongside the church fair (pp. 782/783).",
  r"Maienfest")
G("Pfaffenscheffel", [], "term",
  "Abgabe, die die Pottigaer an die Pfarrei Berg entrichteten und die auf den Pfiff der „heiligen Pfeife“ eingesammelt wurde; 1824 an die reußische Kammer übergegangen, 1867 abgelöst (S. 802).",
  "Levy paid by the people of Pottiga to the parish of Berg, collected at the blast of the “holy pipe”; passed to the Reuss treasury in 1824 and redeemed in 1867 (p. 802).",
  r"Pfaffenscheffel")
G("Wanderschule", [], "term",
  "Vorstufe fester Schulen: ein Lehrer (Katechet, Präceptor oder Handwerker) unterrichtete im Winter reihum in Wohnhäusern; in den Ortsartikeln beschreibt Brückner den Weg vom Reihe- und Wanderunterricht zum eigenen Schulhaus.",
  "Precursor of fixed schools: a teacher (catechist, preceptor or craftsman) taught in winter in rotation in private houses; in the place articles Brückner traces the path from rotating instruction to a school building of the village's own.",
  r"Wanderschule")
G("Reihetisch", [], "term",
  "Reihumverpflegung des Lehrers bei den Familien der Schulgemeinde als Teil der Besoldung; in Göritz 1843, in Gebersreuth 1852 abgelöst, in Pottiga bei der Wanderschule erwähnt (S. 802, 805, 821).",
  "Rotating board of the teacher with the families of the school district as part of his pay; redeemed in Göritz in 1843 and in Gebersreuth in 1852, mentioned with the itinerant school in Pottiga (pp. 802, 805, 821).",
  r"Reihetisch")
G("Katechet", ["Catechet", "Cantor"], "office",
  "Katechet: junger Theologe oder Lehrer, der Kinderlehre und Unterricht hielt (Wurzbach: bis 1815 unterrichteten nur Theologen als Catecheten); Cantor: Lehrer mit Kirchendienst, in Wurzbach seit 1815 so genannt, in Hirschberg zugleich Organist.",
  "Catechist: a young theologian or teacher giving religious instruction and teaching (Wurzbach: until 1815 only theologians taught as catechists); cantor: teacher with church duties, so called in Wurzbach since 1815 and at Hirschberg also the organist.",
  r"Katechet|Catechet|Cantor|Kantor")

# ---- local government, jurisdiction, trades
G("Landrathsbezirk", ["Landrathsamt"], "office",
  "Verwaltungsbezirk unter einem Landrath; die Orte dieses Teils liegen im Landrathsbezirk Ebersdorf (Wurzbach: zweitgrößter Ort, Hirschberg: dritter).",
  "Administrative district under a Landrath; the places of this part lie in the Landrathsbezirk Ebersdorf (Wurzbach: second largest place, Hirschberg: third).",
  r"Landrath\w{0,2}bezirk|Landrathsamt")
G("Friedensrichter", ["Friedensgericht"], "office",
  "Ehrenamtlicher Richter der seit dem Gesetz vom 28. April 1863 in allen Gemeinden eingerichteten Friedensgerichte zur gütlichen Beilegung von Streitsachen, auf drei Jahre gewählt (Brückner S. 282); Wurzbach hat einen für sich und Weitisberga, Harra einen eigenen.",
  "Lay judge of the conciliation courts set up in all municipalities under the law of 28 April 1863 to settle disputes amicably, elected for three years (Brückner p. 282); Wurzbach has one for itself and Weitisberga, Harra one of its own.",
  r"Friedensrichter")
G("Gensd'arm", ["Gendarm"], "office",
  "Landespolizist mit festem Dienstsitz am Ort (Wurzbach, Harra, Blintendorf, Hirschberg).",
  "Rural policeman with a fixed station in the place (Wurzbach, Harra, Blintendorf, Hirschberg).",
  r"Gensd'arm")
G("Braugemeinde", ["Reihenschank", "Altbürger", "Braugerechtigkeit"], "term",
  "Enge Gemeinde der brauberechtigten Hausbesitzer, die das Recht des Bierbrauens und -schenkens reihum ausüben (Pottiga: 13 Häuser, Reihenschank; Hirschberg: 58 Brauberechtigte, die Altbürger, gegenüber den Neubürgern, die das Bier fassweise von ihnen nehmen müssen, S. 814).",
  "Narrow association of house owners with brewing rights who brew and sell beer in rotation (Pottiga: 13 houses, rotating tap; Hirschberg: 58 brewing-right holders, the old burghers, as against the new burghers who must take their beer by the barrel from them, p. 814).",
  r"Braugemeinde|Reihenschank|Altbürger|Neubürger|Braugerechtigkeit|Brauberechtig")
G("Kriegshof", [], "term",
  "Name für eine Gemeinde, die die anfallenden Kriegslasten gemeinsam zu tragen hatte (Göritz ohne das Rittergut, S. 806).",
  "Name for a community that had to bear the war burdens falling on it jointly (Göritz without the manor, p. 806).",
  r"Kriegshof")
G("Erbkretschmar", [], "term",
  "Erbliche Dorfschenke (Kretscham) mit Schankrecht, oft ein Hinweis auf einen früheren Herrensitz (Rothenacker, S. 824/825; Langgrün, Gebersreuth).",
  "Hereditary village tavern (Kretscham) with the right to serve drink, often an indication of a former manor house (Rothenacker, pp. 824/825; Langgrün, Gebersreuth).",
  r"Erbkretsch")
G("wilde Ehe", ["wilden Ehen", "Concubinat"], "term",
  "Zeitgenössischer Ausdruck für eine nichteheliche Lebensgemeinschaft; Brückner zählt sie in jedem Ortsartikel mit den Angaben zur Sittlichkeit auf.",
  "Contemporary term for a cohabitation without marriage; Brückner counts them in every place article together with his remarks on morals.",
  r"wilde Ehe|wilden Ehen|Concubinat")
G("Almosenarme", ["Almosener", "Armenarme"], "term",
  "Empfänger von Armenunterstützung aus der Gemeinde; die Zahl wird in den Ortsartikeln neben der Zahl der Kapitalisten (Personen mit nennenswertem Kapitalvermögen) angegeben.",
  "Recipients of poor relief from the municipality; the number is given in the place articles next to the number of capitalists (people with notable capital assets).",
  r"Almosen|Armenarme")
G("Weißnäherei", ["Weißzeugstickerei"], "term",
  "Heimarbeit für Weißzeug (Leibwäsche, Stickerei), vor allem von Frauen und Mädchen; in Frössen, Pottiga, Göritz, Gebersreuth und Dobareuth als Nebenerwerb genannt.",
  "Home work on white goods (underwear, embroidery), mainly done by women and girls; mentioned as a side income in Frössen, Pottiga, Göritz, Gebersreuth and Dobareuth.",
  r"Weißnäh|Weißzeug")
G("Hochofen", ["Frischfeuer", "Cupolofen", "Blaufeuer"], "term",
  "Einrichtungen der Eisenwerke: Hochofen (Roheisenerzeugung), Frischfeuer (Herd zum Frischen des Roheisens zu Schmiedeeisen), Cupolofen (Kupolofen zum Umschmelzen für den Guss); genannt bei Heinrichshütte, Benignengrün und Lemnitzhammer.",
  "Installations of ironworks: blast furnace (pig iron production), finery fire (hearth for refining pig iron into wrought iron), cupola furnace (for remelting for casting); mentioned at Heinrichshütte, Benignengrün and Lemnitzhammer.",
  r"Hochofen|Hochöfen|Frischfeuer|Cupol|Blaufeuer")
G("Pochwerk", [], "term",
  "Stampfwerk zum Zerkleinern von Erz; in Lehesten früher vorhanden, Spuren noch zu sehen (S. 807).",
  "Stamp mill for crushing ore; formerly present at Lehesten, traces still visible (p. 807).",
  r"Pochwerk")
G("Alaun- und Vitriolwerk", [], "term",
  "Chemisches Bergwerk zur Gewinnung von Alaun und Vitriol aus Erzen; an der Buttermühle 1747—1769 ohne Ausbeute, bei Saalbach als Johanneszeche 1747 bis um 1802.",
  "Chemical mining works for obtaining alum and vitriol from ores; at the Buttermühle 1747—1769 without yield, near Saalbach as the Johanneszeche from 1747 to about 1802.",
  r"Alaun")
G("Torfziegel", [], "term",
  "Aus Torf gestochene Brennstoffziegel; Göttengrün gewinnt jährlich 200,000, Gebersreuth setzt rund 1 1/2 Millionen nach Gefell und Hirschberg ab.",
  "Fuel bricks cut from peat; Göttengrün produces 200,000 a year, Gebersreuth sells about 1 1/2 million to Gefell and Hirschberg.",
  r"Torfziegel")
G("Rennstieg", [], "term",
  "Alter Höhenweg auf dem Gebirgskamm; Brückner stellt fest, dass der Rennstieg vom Kulm nach Süden lief und nicht über Schlegel nach Blankenstein (S. 782).",
  "Old ridge path along the mountain crest; Brückner states that the Rennstieg ran south from the Kulm and not over Schlegel to Blankenstein (p. 782).",
  r"Rennstieg")
G("Kloster zum heil. Kreuz bei Saalburg", ["Kreuzkloster Saalburg", "Stift zum heil. Kreuze"], "institution",
  "Kloster bei Saalburg, das seit dem 14. Jahrhundert Zinsen, Höfe und Güter in Langgrün, Göttengrün, Frössen, Pottiga, Göritz, Gebersreuth und anderen Orten dieses Teils erwarb; das Stift besaß das Klostergut in Pottiga.",
  "Monastery near Saalburg which from the 14th century acquired rents, farms and estates in Langgrün, Göttengrün, Frössen, Pottiga, Göritz, Gebersreuth and other places of this part; the foundation owned the monastery estate at Pottiga.",
  r"Kloster.{0,60}Saalburg|Saalburg.{0,30}(?:Kloster|Stift)|Stifte? zum heil|Stiftsverwaltung|Kloster zum h")
G("Brüdergemeinde", [], "institution",
  "Herrnhuter Brüdergemeine unter Graf Zinzendorf, der 1722 Erdmuthe Dorothea Reuß-Ebersdorf heiratete; hielt vom 1. bis 12. Juli 1743 eine Synode auf Schloss Hirschberg (S. 810).",
  "Moravian Church under Count Zinzendorf, who married Erdmuthe Dorothea of Reuss-Ebersdorf in 1722; held a synod at Hirschberg castle from 1 to 12 July 1743 (p. 810).",
  r"Brüdergemeinde")

# ---- dialect
G("olzig", [], "dialect",
  "Lieblingswort der Oßlaer, „in allen möglichen Anwendungen gebraucht“ (S. 772); Brückner nennt Accentuation, Lautbrechung und besondere Wortformen als Eigenart der Mundart, eine Bedeutung gibt er nicht an.",
  "Favourite word of the people of Oßla, “used in all possible applications” (p. 772); Brückner cites accentuation, vowel breaking and special word forms as the peculiarity of the dialect but gives no meaning.",
  r"olzig")
G("horschig", ["horschiger"], "dialect",
  "Mundartwort für den Boden der Harraer Flur, die „meist steinig, trocken und ‚horschig‘“ sei (S. 789); die Bedeutung ist nicht erläutert (nach dem Zusammenhang ‚rauh, hart, trocken‘).",
  "Dialect word for the soil of the Harra fields, “mostly stony, dry and ‘horschig’” (p. 789); the meaning is not explained (from the context ‘rough, hard, dry’).",
  r"horschig")
