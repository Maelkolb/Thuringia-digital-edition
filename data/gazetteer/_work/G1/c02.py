# -*- coding: utf-8 -*-
E = []
P = []
G = []

def pg(page, de, en, kde, ken, subj):
    P.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

# ------------------------------------------------------------------ entries
E.append({
    "id": "roschitz",
    "name": "Roschitz",
    "start": {"page": "423", "block": "b3"},
    "end": {"page": "425", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "zweiherrisches Pfarr- und Kirchdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Rodhacice", "year": 1146}, {"form": "Radeschitz", "year": 1401}, {"form": "Rodeschitz", "year": 1488}, {"form": "Ratschiz", "year": 1533}, {"form": "Rodenschütz", "year": None}],
    "dialect_form": "Ruschz und Ruschitz",
    "first_mention_year": 1146,
    "location": {"verbatim": "eine Stunde nördlich von Gera; 1/4 Stunde nordöstlich von Tinz", "relative_to": "Gera", "distance_hours": 1, "direction": "N"},
    "elevation": {"value": 525, "unit": "Fuß", "verbatim": "Die Mitte des Dorfes ist 525 Fuß hoch"},
    "parish": {"status": "Pfarr- und Kirchdorf (altenburgisch)", "church_of": None, "verbatim": "In kirchlicher und scholarer Beziehung gehört sie zu der dasigen herzoglich altenburgischen Kirche, Pfarrei und Schule"},
    "school": {"exists": True, "pupils": 5, "note": "fünf Kinder der reußischen Gemeinde in der altenburgischen Schule"},
    "houses": 5,
    "inhabitants": 32,
    "occupations": {"Dienstboten": 5},
    "flur_morgen": 109.4,
    "flur_verbatim": "109 2/5 Morgen",
    "soil": "fruchtbar",
    "livestock": {"Pferde": 5, "Rinder": 39, "Schafe": 74, "Schweine": 38, "Ziegen": 4, "Gänse": 35},
    "municipal_finances": {"verbatim": "Die Gemeinde hat außer zwei kleinen, beiden Gemeinden gemeinschaftlichen Dorfanger kein Vermögen und auch ihre Jahresbedürfnisse sind ohne Belang und werden, wenn sie nöthig sind, durch Umlagen aufgebracht"},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Rittergut", "Privatschenke", "Feuerspritze"],
    "subplaces": [{"name": "Rittergut Roschitz (reußischer Antheil)", "kind": "Rittergut", "page": "424"}],
    "events": [
        {"year": 1401, "event_de": "Kapelle zur selbstständigen Pfarrei erhoben (erster Pfarrer Nic. Blumenröder)", "event_en": "Chapel raised to an independent parish (first priest Nic. Blumenröder)"},
        {"year": 1533, "event_de": "Lehnbrief des Kurfürsten von Sachsen: Kemnate mit 4 Huben", "event_en": "Enfeoffment charter of the Elector of Saxony: Kemnate with 4 hides"},
        {"year": 1846, "event_de": "Neue Kirche erbaut und am 10. November eingeweiht", "event_en": "New church built and consecrated on 10 November"}
    ],
    "persons": ["Nic. Blumenröder", "Pastor Böhme"],
    "notes": "Zweiherriger Ort in der vom geraer Gebiet umschlossenen altenburgischen Exclave im Bramenthal; die größere altenburgische und die kleinere reußische Gemeinde haben die öffentlichen Hauptanstalten gemeinschaftlich; Angaben (5 Häuser, 32 Einwohner, 5 Familien, Vieh, Flur) betreffen die reußische Gemeinde; 1861: 35 Einwohner. Rittergut früher derer von Schauroth, jetzt von Brandenstein auf Hayn. In der Transkription steht die Überschrift als 'Roschütz' (423 b3), im Druck 'Roschitz'.",
    "summary_de": "Roschitz, zweiherriges Pfarr- und Kirchdorf im unteren Bramenthal, eine Stunde nördlich von Gera, in der altenburgischen Exclave; beschrieben wird vor allem der kleine reußische Teil mit 5 Häusern und 32 Einwohnern, die Kirche von 1846, das Rittergut (von Schauroth, später von Brandenstein) und die Grenzstreitigkeiten.",
    "summary_en": "Roschitz, a village shared between two sovereigns in the lower Brame valley, one hour north of Gera, inside the Altenburg exclave; the account concentrates on the small Reuss portion of 5 houses and 32 inhabitants, the church of 1846, the manor (von Schauroth, later von Brandenstein) and border disputes."
})

E.append({
    "id": "tinz",
    "name": "Tinz",
    "start": {"page": "425", "block": "b2"},
    "end": {"page": "427", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "kleines, anmuthig gelegenes Kirch- und Grenzdorf, früher Pfarr-, Wallfahrts- und Jahrmarktsort und öfters Wittwensitz reußischer Regentinnen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Tyncz", "year": 1290}, {"form": "Tinz", "year": 1323}, {"form": "Teintz", "year": 1496}, {"form": "Dintz", "year": 1533}, {"form": "Tyntz", "year": 1534}, {"form": "Thyntz", "year": 1540}, {"form": "Düntz", "year": 1639}],
    "dialect_form": "Tinz",
    "first_mention_year": 1290,
    "location": {"verbatim": "3/4 Stunde nördlich von Gera", "relative_to": "Gera", "distance_hours": 0.75, "direction": "N"},
    "parish": {"status": "Filial", "church_of": "Gera", "verbatim": "Die jetzige Kirche, Filial von Gera"},
    "school": {"exists": True, "pupils": 58},
    "houses": 27,
    "inhabitants": 315,
    "occupations": {"Bauern": 11, "Kleinhäusler": 22, "Taglöhner": 19, "Dienstboten": 24, "Kapitalisten": 2},
    "crafts": {"Harmonikatischler": 3, "Müller": 3, "Zimmerleute": 3, "Porzellandreher": 2, "Bäcker": 1, "Gärtner": 1, "Maurer": 1, "Porzellanmaler": 1, "Steindrucker": 1, "Schmied": 1, "Schneider": 1, "Schuhmacher": 1, "Ziegler": 1},
    "flur_morgen": 1003.5,
    "flur_verbatim": "1003 1/2 Morgen",
    "soil": "3/4 ergiebig, 1/4 gering",
    "livestock": {"Pferde": 24, "Rinder": 121, "Schafe": 300, "Schweine": 96, "Ziegen": 6, "Gänse": 240},
    "municipal_finances": {"verbatim": "Die Gemeinde hat kein Vermögen, dagegen 350 Thlr. Schulden und circa 200 Thlr. Jahresausgabe zur Erhaltung der Communalbauten, 2 Sturmfässer (statt Feuerspritze), 1 Dorfstraße, 2 Communications- und Vicinalwege", "debts_thaler": 350, "expenditure_thaler": 200},
    "facilities": ["Schloss", "Kammergut", "Park", "Kirche", "Schule", "Forsthaus", "Gemeindehaus", "Privatgasthof", "Restauration", "Mühle", "Ziegelei", "Lesebibliothek", "Sturmfässer"],
    "subplaces": [
        {"name": "Schloss Tinz", "kind": "Schloss", "page": "425"},
        {"name": "Kammergut Tinz", "kind": "Kammergut", "page": "425"},
        {"name": "Ziegelei Tinz", "kind": "Gewerbeanlage", "page": "426"}
    ],
    "events": [
        {"year": 1290, "event_de": "Markgraf Friedrich überlässt Tinz dem Voigt Heinrich von Plauen; Kammergut kommt an Plauen", "event_en": "Margrave Friedrich cedes Tinz to Voigt Heinrich of Plauen; the estate passes to Plauen"},
        {"year": 1319, "event_de": "Kammergut kommt von der Linie Weida für immer an das Haus Gera", "event_en": "Estate passes from the Weida line permanently to the house of Gera"},
        {"year": 1472, "event_de": "Haupterweiterung der Kirche 1470-1472, Neubau eingeweiht", "event_en": "Main enlargement of the church 1470-1472, new building consecrated"},
        {"year": 1539, "event_de": "Einkommen der Pfarrei Tinz dem Pfarrkasten zu Gera zugeschlagen", "event_en": "Income of the Tinz parish added to the parish fund of Gera"},
        {"year": 1540, "event_de": "Jahrmarkt von Tinz nach Gera verlegt", "event_en": "Annual fair moved from Tinz to Gera"},
        {"year": 1748, "event_de": "Heinrich XXV. errichtet das jetzige Schloss und beginnt den Park", "event_en": "Heinrich XXV builds the present castle and begins the park"},
        {"year": 1810, "event_de": "Brand von sieben Häusern und der Schule; 1811 zwei Häuser", "event_en": "Fire destroys seven houses and the school; two more houses in 1811"}
    ],
    "persons": ["Heinrich XXV.", "Heinrich XXX.", "Louise Christiane", "Blasius Gentschel"],
    "notes": "1 Schloss und Kammergut, 1 Kirche, 1 Schule, 1 Forsthaus, 1 Gemeindehaus und 27 Privathäuser mit 16 Scheunen; 67 Familien; 1861: 294 Einwohner; 6 Bauerngüter, 2 Pertinenzstücke, 68 ledige Grundstücke; Kirchenbücher seit 1637; Legat von 1500 Speciesthalern der Fürstin Wittwe L. Christiane; Lesebibliothek seit 1846; Sitz eines Försters; sorbischer Anbau.",
    "summary_de": "Tinz, kleines Kirch- und Grenzdorf ¾ Stunde nördlich von Gera an der gera-zeitzer Straße: Kammergut und Schloss (1748) mit Park, Kirche als Filial von Gera (13. Jahrhundert, Erweiterung 1470–1472), Schule, Gewerbe, Gemeindefinanzen und Flur von 1003 ½ Morgen; früher Wallfahrts- und Jahrmarktsort.",
    "summary_en": "Tinz, a small parish and border village three quarters of an hour north of Gera on the Gera-Zeitz road: crown estate and castle (1748) with park, church as a branch of Gera (13th century, enlarged 1470-1472), school, trades, municipal finances and a field area of 1003 1/2 Morgen; formerly a pilgrimage and fair site."
})

E.append({
    "id": "bieblach",
    "name": "Bieblach",
    "start": {"page": "427", "block": "b2"},
    "end": {"page": "427", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "kleines wasserarmes, baumloses Bauerndörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Weblok", "year": 1322}, {"form": "Wiblach", "year": 1533}, {"form": "Wiblick", "year": 1534}],
    "dialect_form": "Wieblich",
    "first_mention_year": 1322,
    "location": {"verbatim": "1/2 Stunde fast nördlich von Gera", "relative_to": "Gera", "distance_hours": 0.5, "direction": "N"},
    "parish": {"status": "eingepfarrt", "church_of": "Gera", "verbatim": "Der Ort pfarrt und begräbt von jeher nach Gera"},
    "school": {"exists": False, "note": "kann sich nach Tinz oder Gera zur Schule halten"},
    "houses": 14,
    "inhabitants": 109,
    "occupations": {"Bauern": 12, "Häusler": 1, "Dienstboten": 22},
    "flur_morgen": 661.89,
    "flur_verbatim": "661 8/9 Morgen",
    "soil": "meist trocken, halb gut, halb geringer",
    "livestock": {"Pferde": 31, "Rinder": 122, "Schafe": 654, "Schweine": 87, "Ziegen": 4, "Gänse": 250, "Bienenstöcke": 8},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 1 Ortsbeamten besitzt 30 Morgen Lehden, Anger und Obstplantagen im Werthe von 3000 Thlr. und außerdem 300 Thlr. Capital; ihre Jahresausgabe macht circa 110 Thlr.", "assets_thaler": 3000, "capital_thaler": 300, "expenditure_thaler": 110},
    "facilities": ["Gemeindehaus", "Schenke", "Schäferei"],
    "subplaces": [{"name": "Kammerschäferei Bieblach", "kind": "Gewerbeanlage", "page": "427"}],
    "events": [
        {"year": 1322, "event_de": "Die Voigte von Gera geben dem Kloster Cronswitz 32 Schilling Renten zu Bieblach", "event_en": "The advocates of Gera give 32 shillings of rent at Bieblach to Cronswitz convent"},
        {"year": 1757, "event_de": "11 Bauern festgenommen, weil sie in Dienst getretene Flüchtlinge aus Sachsen wegführen wollten", "event_en": "11 farmers arrested for trying to take away young refugees from Saxony who had entered service"},
        {"year": 1791, "event_de": "Brandstiftung: sechs Bauernhöfe brennen am 22. August nieder", "event_en": "Arson destroys six farms on 22 August"}
    ],
    "notes": "1 Gemeindehaus, 1 Kammerschäferei und 14 Privathäuser; 16 Familien; 1861: 102 Einwohner; 10 Güter, 40 ledige Grundstücke; kein Gewerbetreibender, kein Ortsarmer, 1 Gebrechlicher (Taubstummer); 11 Bauernhöfe sind der Kirche zu Gera decempflichtig; Flurstücke gehörten neun verschiedenen Lehen und Gerichtsbarkeiten; sorbischen Ursprungs.",
    "summary_de": "Bieblach, kleines Bauerndorf ½ Stunde nördlich von Gera auf einer Terrasse der Sterkenhöhe, nach Gera gepfarrt; 14 Häuser, 109 Einwohner, großer Schafbestand und herrschaftliche Schäferei, wohlhabende Bauern, Flur 661 8/9 Morgen mit zahlreichen Flurnamen und Lehensverhältnissen.",
    "summary_en": "Bieblach, a small farming village half an hour north of Gera on a terrace of the Sterkenhöhe, in the parish of Gera; 14 houses, 109 inhabitants, a large sheep stock and a princely sheep farm, prosperous farmers, and a field area of 661 8/9 Morgen with many field names and feudal tenures."
})

E.append({
    "id": "gera",
    "name": "Gera",
    "start": {"page": "428", "block": "b1"},
    "end": {"page": "448", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Hauptstadt des Fürstenthums",
    "type": "Stadt",
    "wuestung": False,
    "historic_forms": [{"form": "Geraha", "year": 1125}, {"form": "Gerawe", "year": None}, {"form": "Ghera", "year": 1145}, {"form": "Gerau", "year": None}, {"form": "Cheraw", "year": None}, {"form": "Jera", "year": None}],
    "dialect_form": "Gêre, Giere, Küre",
    "first_mention_year": 1125,
    "location": {"verbatim": "auf dem rechten Ufer dieses Flusses, im Angesichte des Residenzschlosses Osterstein, an der nürnberg-leipziger Straße"},
    "parish": {"status": "Hauptpfarrkirche (St. Salvator)", "church_of": None, "verbatim": "Die St. Salvatorkirche dient seitdem der Stadt als Hauptpfarrkirche … Zur Stadt gehören die Filiale Tinz, Lusan und Oberröppisch und als eingepfarrte Orte Pöppeln, Debschwitz, Pforten und Bieblach"},
    "school": {"exists": True, "pupils": 2700, "note": "städtischer Schulkörper mit 60 Lehrern und 13 Lehrerinnen; Gymnasium 1868: 190 Schüler"},
    "houses": 1087,
    "inhabitants": 16283,
    "census_year": 1867,
    "occupations": {"Handwerker": 1120, "Kunst- und Handelsgärtner": 32, "Aerzte": 13, "Advocaten und Notare": 10, "Arbeiter (mit Einschluß der Nachbardörfler)": 12000},
    "crafts": {"Zeug- und Leinweber": 409, "Schuhmacher": 170, "Schneider": 105, "Tuchmacher": 12, "Fleischer": 43, "Bäcker": 41, "Rothgerber": 58, "Sattler": 26, "Seiler": 25, "Drechsler": 22, "Seifensieder": 21, "Böttcher": 20, "Weißgerber": 17, "Nadler": 14, "Beutler": 15, "Stellmacher": 9, "Töpfer": 4, "Tischler": 44, "Schlosser": 26, "Lackirer": 21, "Glaser": 15, "Klempner": 15, "Zimmerleute": 13, "Maurer": 11, "Schmiede": 9, "Ziegel- und Schieferdecker": 9, "Oelmaler": 4, "Photographen": 5, "Bildhauer": 6, "Instrumentenmacher": 4, "Graveure": 2, "Optiker": 2, "Gold- und Silberarbeiter": 9, "Architecten und Ingenieurs": 11},
    "flur_morgen": 4720.78,
    "flur_verbatim": "4720 7/9 Morgen",
    "livestock": {"Pferde": 237, "Rinder": 50, "Schafe": 193, "Schweine": 369, "Ziegen": 55, "Esel": 1, "Bienenstöcke": 8},
    "municipal_finances": {"verbatim": "ein Vermögen von 540,600 Thlr., darunter 135,000 Thlr. (Versicherungswerth) an 22 Communalgebäuden, 208,500 Thlr. (Verkaufswerth) an Waldungen, 12000 Thlr. an Feldern, Wiesen und Gärten … 128180 Thlr. 12 Sgr. 4 Pf. 128071 Thlr. 13 Sgr. 9 Pf.", "assets_thaler": 540600, "income_thaler": 128180, "expenditure_thaler": 128071},
    "facilities": ["Rathhaus", "Gymnasium", "Realschule", "höhere Töchterschule", "Bürgerschule", "Webschule", "St. Salvatorkirche", "St. Trinitatiskirche", "Schauspielhaus", "fürstliches Palais", "Regierungsgebäude", "Landhaus", "Kaserne", "Bahnhof", "Postamt", "Telegraphenbureau", "Bank", "Sparkasse", "Gewerbebank", "Handelskammer", "Krankenhaus", "Waisenhaus", "Landarbeitshaus", "Hospital", "Gasanstalt", "Wasserleitung", "Gasthof", "Apotheke", "Bauverein", "Freimaurerloge", "Mühle"],
    "subplaces": [
        {"name": "Zschochern", "kind": "Vorstadt", "page": "429"},
        {"name": "Pöppeln", "kind": "Ortsteil", "page": "430"},
        {"name": "Innenstadt", "kind": "Ortsteil", "page": "429"},
        {"name": "Neubau", "kind": "Ortsteil", "page": "430"},
        {"name": "Klotzmühle", "kind": "Mühle", "page": "433"},
        {"name": "Angermühle", "kind": "Mühle", "page": "433"},
        {"name": "Walkmühle", "kind": "Mühle", "page": "434"},
        {"name": "altes Schloss", "kind": "Schloss", "page": "434"}
    ],
    "events": [
        {"year": 1237, "event_de": "Gerichtsbarkeit über Gera geht an den weidaer Reichsvoigt", "event_en": "Jurisdiction over Gera passes to the imperial advocate of Weida"},
        {"year": 1404, "event_de": "Stadtsiegel 'Sigillum borgensium in Gera'; Stadtrat aus 19 Personen", "event_en": "Town seal 'Sigillum borgensium in Gera'; town administration of 19 persons"},
        {"year": 1450, "event_de": "Erstürmung der Stadt (15. October) im Bruderkrieg durch die Zebracken; angeblich etwa 5000 Tote, ganze Stadt brennt", "event_en": "Storming of the town (15 October) in the Fraternal War; allegedly about 5,000 dead, the whole town burns"},
        {"year": 1479, "event_de": "Tuchmacherinnung gebildet", "event_en": "Cloth-makers' guild formed"},
        {"year": 1595, "event_de": "Nicolas de Smit lässt sich in Gera nieder und begründet die Wollenmanufactur", "event_en": "Nicolas de Smit settles in Gera and founds the woollen manufacture"},
        {"year": 1608, "event_de": "Heinrich Posthumus erhebt die Schule zum Landesgymnasium", "event_en": "Heinrich Posthumus raises the school to a state gymnasium"},
        {"year": 1639, "event_de": "Brand am Ostertag durch die Schweden: ein Drittel der Stadt mit St. Johanniskirche und Gymnasium", "event_en": "Fire on Easter Day set by the Swedes: one third of the town including St. John's church and the gymnasium"},
        {"year": 1686, "event_de": "Brand am 20. März: 258 Bürgerhäuser, über 50 Scheunen, 3 Thore", "event_en": "Fire on 20 March: 258 houses, over 50 barns, 3 gates"},
        {"year": 1780, "event_de": "Großer Stadtbrand am 18. September: 785 Bauten in 3 Stunden zerstört", "event_en": "Great town fire on 18 September: 785 buildings destroyed within 3 hours"},
        {"year": 1806, "event_de": "Im October zieht die französische Armee durch Gera, Napoleon und 150 Marschälle und Generäle einquartiert", "event_en": "In October the French army passes through Gera; Napoleon and 150 marshals and generals quartered"},
        {"year": 1813, "event_de": "Vor der Schlacht bei Leipzig 100,000 Mann im Biwak; Hauptquartier der Kaiser Alexander und Franz", "event_en": "Before the Battle of Leipzig 100,000 men bivouac; headquarters of Emperors Alexander and Francis"},
        {"year": 1848, "event_de": "Straßenkampf am 26. Juli: 1 Toter, 40-50 Verwundete", "event_en": "Street fighting on 26 July: 1 dead, 40-50 wounded"},
        {"year": 1852, "event_de": "Gasleitung eröffnet (Actienunternehmen)", "event_en": "Gas supply opened (joint-stock venture)"},
        {"year": 1859, "event_de": "Weißenfels-Geraer Eisenbahn eröffnet (19. März); Bahnhof erbaut", "event_en": "Weißenfels-Gera railway opened (19 March); station built"},
        {"year": 1865, "event_de": "Gößnitz-Geraer Eisenbahn in Betrieb (27. December)", "event_en": "Gößnitz-Gera railway in operation (27 December)"}
    ],
    "persons": ["Heinrich Posthumus", "Nicolas de Smit", "Heinrich XVIII.", "Heinrich XXX.", "Heinrich LXVII.", "Simon Musäus", "J. Zach. H. Hahn", "Wiprecht von Groitsch"],
    "notes": "Zahlen für Gera sammt Pöppeln (Zählung 1867): 1087 Häuser mit 43 öffentlichen Gebäuden, 117 Scheunen, 3470 Familien, 16283 Einwohner (1861: 14208); 78 Straßen, Gassen und Gäßchen; Stadtwaldung 1253 Morgen von 4720 7/9 Morgen Stadtflur; 89 Hauptfabriken (Kammwollenstoffe, Gerbereien, Harmonikas u. a.); 77 Dampfkessel; Vermögen der Stadt 540,600 Thlr.; Handwerkerangabe im Druck: 1120, die einzeln genannten Gewerbe summieren sich auf 1174 (Druckfehler oder Abweichung im Original, Transkription stimmt mit dem Druck überein). Einwohnerzahl 1647: 2372 (Tabelle S. 430), 1794: 6567.",
    "summary_de": "Gera, Hauptstadt des Fürstentums und größte Stadt des Landes (16283 Einwohner 1867): Lage und Straßenbild, Innenstadt, Vorstädte (Zschochern) und Neubau, Bauten und Kirchen, Behörden, Schulwesen mit Gymnasium, Industrie (Kammwollstoffe, Gerbereien, Harmonikas) und Handel, Vereinswesen, Stadtgeschichte mit den Bränden von 1450, 1639, 1686 und 1780, bedeutende Persönlichkeiten und Sagen.",
    "summary_en": "Gera, capital of the principality and its largest town (16,283 inhabitants in 1867): site and street plan, inner town, suburbs (Zschochern) and new development, buildings and churches, authorities, schools including the gymnasium, industry (worsted cloth, tanneries, harmonicas) and trade, associations, town history with the fires of 1450, 1639, 1686 and 1780, notable persons and legends."
})

E.append({
    "id": "poeppeln",
    "name": "Pöppeln",
    "start": {"page": "448", "block": "b2"},
    "end": {"page": "448", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "kleiner, am Fuße des Hainbergs eben und angenehm gelegener Vor- und Lustort von Gera",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Popelin", "year": None}, {"form": "Poppeln", "year": 1534}],
    "dialect_form": "Pöppeln oder Päppeln",
    "location": {"verbatim": "1/4 Stunde südwestlich davon entfernt, an der Straße von Gera nach Roda und Neustadt", "relative_to": "Gera", "distance_hours": 0.25, "direction": "SW"},
    "parish": {"status": "eingepfarrt", "church_of": "Gera", "verbatim": "Der Ort gehört zur Stadtgemeinde Gera, wohin er auch pfarrt, begräbt und schult"},
    "school": {"exists": False, "note": "schult nach Gera"},
    "houses": 24,
    "inhabitants": 280,
    "occupations": {"Bauern": 1, "Häusler": 17, "Dienstboten": 4},
    "livestock": {"Pferde": 7, "Rinder": 4, "Schafe": 3, "Schweine": 21, "Ziegen": 8, "Gänse": 2},
    "facilities": ["Ziegelfabrik", "Tabagie"],
    "subplaces": [
        {"name": "Martinsgrund", "kind": "Sonstiges", "page": "448"},
        {"name": "Steinstock", "kind": "Sonstiges", "page": "448"}
    ],
    "events": [
        {"year": 1539, "event_de": "Wolfgang v. Uttenhoven verkauft das Rittergut für 800 Gülden an die Stadt Gera", "event_en": "Wolfgang v. Uttenhoven sells the manor to the town of Gera for 800 guilders"},
        {"year": 1696, "event_de": "Plan der Vereinigung der Schule mit Untermhaus, Schulverband mit Gera bleibt", "event_en": "Planned merger of the school with Untermhaus; school affiliation with Gera retained"}
    ],
    "persons": ["Wolfgang v. Uttenhoven"],
    "notes": "Bestandtheil der Stadtgemeinde Gera (Zahlen sind in den Angaben zu Gera enthalten); 24 Privathäuser mit 3 Höfen, 74 Familien; ursprünglich ostersteinisches Burggut, Rittergut der Familie von Uttenhoven mit Vorwerk Bollersdorf [Vollersdorf].",
    "summary_de": "Pöppeln, Vor- und Lustort von Gera am Fuß des Hainbergs, ¼ Stunde südwestlich, Teil der Stadtgemeinde: 24 Häuser, 280 Einwohner, ehemaliges Rittergut (1539 an die Stadt Gera verkauft), Stadtwald, Burghügel und Martinsgrund.",
    "summary_en": "Pöppeln, a suburb and pleasure resort of Gera at the foot of the Hainberg, a quarter hour to the southwest and part of the town municipality: 24 houses, 280 inhabitants, former manor (sold to the town of Gera in 1539), town forest, castle mound and the Martinsgrund."
})

E.append({
    "id": "vollersdorf",
    "name": "Vollersdorf",
    "start": {"page": "448", "block": "b3"},
    "end": {"page": "449", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "ein ausgegangenes Dörfchen mit einem zu Pöppeln geschlagenen Vorwerke",
    "type": "Wüstung",
    "wuestung": True,
    "location": {"verbatim": "im jetzigen geraer Stadtwalde, nahe der Stelle, wo die Straßen von Roda und Neustadt zusammentreffen"},
    "parish": {"status": "eingepfarrt", "church_of": "Gera", "verbatim": "Der Ort war nach Gera gepfarrt und geschult"},
    "events": [
        {"year": 1632, "event_de": "Teilweise Verwüstung nach dem Bericht eines Augenzeugen", "event_en": "Partial devastation according to an eyewitness"},
        {"year": 1647, "event_de": "Landestheilungsacten verzeichnen den Ort noch als bestehend", "event_en": "Partition records of 1647 still list the place as existing"},
        {"year": 1806, "event_de": "Napoleon fragt beim Vorüberfahren nach der Stätte von Vollersdorf (Karte aus dem 18. Jahrhundert)", "event_en": "Napoleon, driving past, asks after the site of Vollersdorf (18th-century map)"}
    ],
    "persons": ["Napoleon"],
    "notes": "In der Transkription durchgehend 'Bollersdorf' (413, 418, 448), im Druck 'Vollersdorf' (448 und 449 sowie Register). Das Vorwerk gehörte zu den ostersteinischen Burggütern, später zum Rittergut Pöppeln.",
    "summary_de": "Wüstung Vollersdorf im heutigen geraer Stadtwald: ausgegangenes Dörfchen mit Vorwerk, Reste von Brunnen, Teichdamm und Grundmauern, Verwüstung 1632, noch im 18. Jahrhundert auf Karten verzeichnet; nach Gera gepfarrt.",
    "summary_en": "Deserted settlement of Vollersdorf in what is now Gera's town forest: a vanished hamlet with an outlying farm, remains of wells, a pond dam and foundations, devastated in 1632 and still shown on maps in the 18th century; part of the parish of Gera."
})

E.append({
    "id": "debschwitz",
    "name": "Debschwitz",
    "start": {"page": "449", "block": "b2"},
    "end": {"page": "450", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "mittelgroßes Dorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Debschitz", "year": None}, {"form": "Dobschwitz", "year": None}, {"form": "Deschitz", "year": 1533}, {"form": "Dobschitz", "year": 1534}],
    "dialect_form": "Dêschwitz",
    "location": {"verbatim": "1/2 Stunde SWS. von Gera, an der Chaussee von da nach Weida", "relative_to": "Gera", "distance_hours": 0.5, "direction": "SSW"},
    "parish": {"status": "eingepfarrt", "church_of": "Gera", "verbatim": "Der Ort pfarrt und begräbt seit alter Zeit nach Gera"},
    "school": {"exists": False, "note": "Kinder gehen seit 1696 nach Lusan"},
    "houses": 40,
    "inhabitants": 374,
    "occupations": {"Bauern": 14, "Häusler": 26, "Taglöhner": 36, "Dienstboten": 20, "Kapitalisten": 3, "Ortsarme": 12, "Familien in Fabrikarbeit (Gera)": 31},
    "crafts": {"Zimmerleute": 4, "Maurer": 3, "Wirthe": 2, "Fleischer": 1, "Instrumentenmacher": 1, "Schneider": 1, "Ziegelbrenner": 1},
    "flur_morgen": 751.89,
    "flur_verbatim": "751 8/9 Morgen",
    "soil": "3/5 mittelgut, 1/5 gut, 1/5 gering",
    "livestock": {"Pferde": 13, "Rinder": 100, "Schweine": 102, "Ziegen": 12, "Gänse": 120, "Bienenstöcke": 9},
    "municipal_finances": {"verbatim": "Die Gemeinde besaß als engere 70 Morgen Wiesen im Werthe von 1050 Thlr., als weitere ist sie ohne Vermögen und Schulden, bedarf aber jährlich circa 200 Thlr. zu ihrem Aufwande und hat 1 Dorfstraße und 2 Communications- und Vicinalwege zu erhalten", "assets_thaler": 1050, "expenditure_thaler": 200},
    "facilities": ["Gemeindehaus", "Privatschenke", "Gemeindeschenke", "Ziegelei", "Dorfstraße"],
    "subplaces": [{"name": "Kammergut Debschwitz (ehemalig)", "kind": "Kammergut", "page": "449"}],
    "events": [
        {"year": 1696, "event_de": "Plan der Einverleibung in die Schule Untermhaus; Schulbesuch in Lusan erlaubt", "event_en": "Planned incorporation into the Untermhaus school; attendance at Lusan allowed"},
        {"year": 1757, "event_de": "Lager von 6000 Mann von Debschwitz bis zum Hainberg (October)", "event_en": "Camp of 6,000 men from Debschwitz to the Hainberg (October)"},
        {"year": 1799, "event_de": "Eisgang der Elster beschädigt mehrere Häuser", "event_en": "Ice drift on the Elster damages several houses"},
        {"year": 1801, "event_de": "Sechs Bauernhöfe brennen durch Blitzschlag ab", "event_en": "Six farms burn down after a lightning strike"},
        {"year": 1823, "event_de": "Die Nachbarn kaufen Feld und Wiesen des Kammerguts; 1843 kauft die Stadt Gera dessen Waldung", "event_en": "The neighbours buy the fields and meadows of the crown estate; in 1843 the town of Gera buys its forest"},
        {"year": 1866, "event_de": "Gebäude des v. wiese'schen Guts durch Blitzschlag größtentheils abgebrannt", "event_en": "Buildings of the von Wiese estate largely burnt down by lightning"}
    ],
    "persons": ["G. W. B. v. Wiese"],
    "notes": "1 Gemeindehaus und 40 Privathäuser mit 17 Scheunen, 88 Haushaltungen; 1861: 274 Einwohner; 13 Bauerngüter, 2 Pertinenzen, 74 ledige Grundstücke; Gut des Kanzlers v. Wiese gehört dem v. wiese'schen Bürgerrettungs- und Industriebeförderungsinstitut; Todaustreiben als Brauch; Name sorbischen Ursprungs; Richtungsangabe im Druck 'SWS.'.",
    "summary_de": "Debschwitz, mittelgroßes Dorf an der Elster ½ Stunde südsüdwestlich von Gera an der Chaussee nach Weida, nach Gera gepfarrt und nach Lusan eingeschult; 40 Häuser, 374 Einwohner, Bauern und Fabrikarbeiter, Flur 751 8/9 Morgen, ehemaliges Kammergut, Todaustreiben und Brandfälle.",
    "summary_en": "Debschwitz, a medium-sized village on the Elster half an hour south-southwest of Gera on the Weida road, in the parish of Gera and school district of Lusan; 40 houses, 374 inhabitants, farmers and factory workers, field area 751 8/9 Morgen, a former crown estate, a 'Todaustreiben' custom and fires."
})

E.append({
    "id": "pforten",
    "name": "Pforten",
    "start": {"page": "450", "block": "b2"},
    "end": {"page": "451", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "langgezetteltes, freundliches Dorf, ein Lustort der Geraer",
    "type": "Dorf",
    "wuestung": False,
    "location": {"verbatim": "1/2 Stunde südlich von Gera", "relative_to": "Gera", "distance_hours": 0.5, "direction": "S"},
    "parish": {"status": "eingepfarrt", "church_of": "Gera", "verbatim": "Seit 1632 pfarrt und begräbt Pforten nach Gera"},
    "school": {"exists": True, "pupils": 104},
    "houses": 42,
    "inhabitants": 549,
    "occupations": {"Bauern": 3, "Häusler": 38, "Taglöhner": 12, "Dienstboten": 20},
    "crafts": {"Harmonikamacher": 3, "Zeugarbeiter": 3, "Zimmerleute": 3, "Bäcker": 2, "Korbmacher": 2, "Tischler": 2, "Bürstenbinder": 1, "Drechsler": 1, "Fleischer": 1, "Maurer": 1, "Schmied": 1, "Schlosser": 1, "Schneider": 1, "Schuhmacher": 1, "Ziegelbrenner": 1},
    "flur_morgen": 706.54,
    "flur_verbatim": "706 7/13 Morgen",
    "soil": "2/3 gering, 1/3 gut",
    "livestock": {"Pferde": 14, "Rinder": 69, "Schweine": 86, "Ziegen": 16, "Gänse": 25},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 9 Beamten (incl. Gemeinderath) hat als Grundbesitz 1 Morgen Wiesen im Werthe von 100 Thlr., außerdem 900 Thlr. Schulden und als Jahresausgabe circa 175 Thlr.", "assets_thaler": 100, "debts_thaler": 900, "expenditure_thaler": 175},
    "facilities": ["Rittergut", "Schule", "Gemeindehaus", "Brauerei", "Mühle", "Ziegelei", "Feuerspritze", "Gasthof", "Privatwirthschaft", "Steinbruch"],
    "subplaces": [
        {"name": "Rittergut Pforten", "kind": "Rittergut", "page": "450"},
        {"name": "Stärkehäuser", "kind": "Sonstiges", "page": "450"},
        {"name": "Gasthof zum Lindenthal", "kind": "Sonstiges", "page": "450"},
        {"name": "Brauerei Pforten", "kind": "Gewerbeanlage", "page": "450"}
    ],
    "events": [
        {"year": 1534, "event_de": "Kirchenvisitatoren befehlen die Rückgabe der der Kapelle entzogenen Felder", "event_en": "Church visitors order the return of the fields withdrawn from the chapel"},
        {"year": 1632, "event_de": "Kapelle wahrscheinlich durch Soldaten niedergebrannt", "event_en": "Chapel probably burnt down by soldiers"},
        {"year": 1760, "event_de": "Stärkefabrikation (1760-1793) errichtet", "event_en": "Starch manufacture established (1760-1793)"},
        {"year": 1799, "event_de": "Entdeckung eines altgermanischen Totenhofes (Heidengottesacker) mit Urnen und Bronzen", "event_en": "Discovery of an ancient Germanic burial ground ('Heidengottesacker') with urns and bronzes"},
        {"year": 1865, "event_de": "Schulhaus und eigener Lehrer", "event_en": "School building and own teacher"},
        {"year": 1866, "event_de": "Rittergut im März für circa 91,100 Thlr. an Chr. Aug. Keil verkauft", "event_en": "Manor sold in March to Chr. Aug. Keil for about 91,100 thalers"}
    ],
    "persons": ["Chr. Aug. Keil"],
    "notes": "1 Rittergut, 1 Schule, 1 Gemeindehaus und 42 Privathäuser mit 8 Höfen; 115 Familien; 1861: 423 Einwohner; Fußnote: nach der Zählung von 1867 nur 4 Schweine angegeben; 4 kleine Güter, 1 Pertinenzstück, 23 ledige Grundstücke; Besitzerreihe des Ritterguts seit 1488 (von Schauroth).",
    "summary_de": "Pforten, langgestrecktes Dorf und Ausflugsort der Geraer ½ Stunde südlich von Gera im Gössenthal, nach Gera gepfarrt; Rittergut mit Besitzerfolge seit 1488, Brauerei, 42 Häuser, 549 Einwohner, überwiegend Arbeiter in Gera, vorgeschichtliche Grabfunde (Heidengottesacker) und Sagen.",
    "summary_en": "Pforten, a long-drawn village and excursion spot of the people of Gera half an hour south of Gera in the Gössen valley, in the parish of Gera; manor with owners since 1488, brewery, 42 houses, 549 inhabitants, mostly workers in Gera, prehistoric burial finds ('Heidengottesacker') and legends."
})

E.append({
    "id": "zwoetzen",
    "name": "Zwötzen",
    "start": {"page": "451", "block": "b2"},
    "end": {"page": "453", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Kirch- und Grenzdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Zwecen", "year": None}, {"form": "Czwoczen", "year": 1358}, {"form": "Zwoizen", "year": 1410}, {"form": "Zweczen", "year": 1533}],
    "dialect_form": "Zwiezen",
    "first_mention_year": 1358,
    "location": {"verbatim": "3/4 Stunde südlich von Gera, Lusan gegenüber", "relative_to": "Gera", "distance_hours": 0.75, "direction": "S"},
    "parish": {"status": "Kirchdorf", "church_of": None, "verbatim": "Im Jahre 1604 erhob man den Ort zur Parochie und verband mit ihr Leumnitz als Filial … Zwötzen aber als Mutterkirche erhalten wurde"},
    "school": {"exists": True, "pupils": 112},
    "houses": 63,
    "inhabitants": 551,
    "occupations": {"Bauern": 12, "Häusler": 52, "Hand- oder Fabrikarbeiter": 84, "Dienstboten": 25},
    "crafts": {"Harmonikatischler": 7, "Schneider": 4, "Cigarrenfabrikanten": 2, "Händler": 2, "Hobelmacher": 2, "Schuhmacher": 2, "Bäcker": 1, "Korbmacher": 1, "Seiler": 1, "Stellmacher": 1, "Stubenmaler": 1, "Tischler": 1, "Wachstuchfabrikant": 1, "Wagner": 1, "Ziegler": 1, "Zimmermann": 1},
    "flur_morgen": 735.4,
    "flur_verbatim": "735,4 Morgen",
    "soil": "meist Mittelboden",
    "livestock": {"Pferde": 20, "Rinder": 92, "Schafe": 203, "Schweine": 127, "Ziegen": 42, "Gänse": 30, "Bienenstöcke": 14},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 11 Ortsbeamten (incl. Gemeinderath) hat statt Vermögen 1175 Thlr. Schulden und eine jährliche Ausgabe von 450 bis 500 Thlr. zur Erhaltung der Communalhäuser, der Dorfstraße und von 5 Communicationswegen", "debts_thaler": 1175, "expenditure_thaler_min": 450, "expenditure_thaler_max": 500},
    "facilities": ["Rittergut", "Kirche", "Schule", "Gemeindehaus", "Gasthaus", "Gemeindeschenke", "Ziegelei", "Friedhof"],
    "subplaces": [
        {"name": "Rittergut Zwötzen", "kind": "Rittergut", "page": "452"},
        {"name": "Aalicht (Schellsechse)", "kind": "Sonstiges", "page": "451"}
    ],
    "events": [
        {"year": 1358, "event_de": "Reinolt v. Zwötzen übergibt Güter in Zwötzen und Lusan dem Kloster Cronswitz", "event_en": "Reinolt v. Zwötzen gives estates in Zwötzen and Lusan to Cronswitz convent"},
        {"year": 1450, "event_de": "Zusammenkunft der feindlichen Brüder Kurfürst Friedrich und Herzog Wilhelm nach der Katastrophe von Gera", "event_en": "Meeting of the hostile brothers Elector Friedrich and Duke Wilhelm after the disaster of Gera"},
        {"year": 1598, "event_de": "Schule bereits vorhanden", "event_en": "School already in existence"},
        {"year": 1604, "event_de": "Zwötzen zur Parochie erhoben, Leumnitz als Filial", "event_en": "Zwötzen raised to a parish, Leumnitz as its branch"},
        {"year": 1711, "event_de": "Zwei Glocken gegossen", "event_en": "Two bells cast"},
        {"year": 1820, "event_de": "Herrnhaus des Ritterguts neu erbaut", "event_en": "Manor house newly built"},
        {"year": 1844, "event_de": "Pfarrei nach Leumnitz verlegt, Orgel in der Kirche", "event_en": "Parsonage moved to Leumnitz; organ installed in the church"},
        {"year": 1862, "event_de": "Überschwemmung des Friedhofs am 16. Mai durch den Schafgraben", "event_en": "Flooding of the cemetery on 16 May by the Schafgraben stream"}
    ],
    "persons": ["Reinolt v. Zwötzen", "Gottfr. v. Watzdorf"],
    "notes": "1 Rittergut, 1 Kirche, 1 Schule, 1 Gemeindehaus und 63 Privathäuser mit 17 Scheunen; 117 Familien; 1861: 464 Einwohner; 7 Güter, 3 Grundstücksverbände, 2 Pertinenzstücke, 43 ledige Grundstücke; 12 Familien bauen ihr Jahresbrod; Kirchenvermögen 561 5/6 Thlr.; Kirchenbücher seit 1648; Name sorbischen Ursprungs.",
    "summary_de": "Zwötzen, Kirch- und Grenzdorf ¾ Stunde südlich von Gera in der Elsteraue: Rittergut mit Besitzerfolge seit 1358, Kirche und Parochie (1604) mit Leumnitz, Schule (112 Kinder), 551 Einwohner, überwiegend Arbeiter und Handwerker (Harmonikatischler), Flur 735,4 Morgen, Ortsgeschichte und Sagen.",
    "summary_en": "Zwötzen, a parish and border village three quarters of an hour south of Gera in the Elster plain: manor with owners since 1358, church and parish (1604) with Leumnitz, school (112 children), 551 inhabitants, mostly workers and craftsmen (harmonica joiners), field area 735.4 Morgen, local history and legends."
})

# ------------------------------------------------------------------ pages
pg("425", "Schluss von Roschitz (Dienstboten, Flur 109 2/5 Morgen, Streit zwischen Reuß und Altenburg); Tinz, Kirch- und Grenzdorf ¾ Stunde nördlich von Gera: Namensformen, Häuser, 315 Einwohner, Vieh, Kammergut und Schloss (1748) mit Park, Kirche, Anfang der Kirchengeschichte.",
   "End of Roschitz (servants, field area 109 2/5 Morgen, dispute between Reuss and Altenburg); Tinz, a parish and border village three quarters of an hour north of Gera: name forms, houses, 315 inhabitants, livestock, crown estate and castle (1748) with park, church, start of the church history.",
   ["Roschitz", "Tinz", "Schloss Tinz", "Kammergut", "Park", "Heinrich XXV.", "Kirche", "Wallfahrt", "Witwensitz"], ["Roschitz", "Tinz", "Tinz castle", "crown estate", "park", "church", "pilgrimage", "dowager seat"], ["Dorf", "Burgen und Schlösser", "Kammergut"])
pg("426", "Tinz: Kirche (13. Jahrhundert, Erweiterung 1470–1472), Altarschnitzwerke, Glocken, Legat der Fürstin Louise Christiane, Zuordnung der Pfarrei zu Gera 1539, Schule, Gewerbe und Handwerker, Gemeindefinanzen, Flur 1003 ½ Morgen mit Flurnamen.",
   "Tinz: church (13th century, enlarged 1470-1472), carved altarpieces, bells, bequest of Princess Louise Christiane, assignment of the parish to Gera in 1539, school, trades and craftsmen, municipal finances, field area of 1003 1/2 Morgen with field names.",
   ["Tinz", "Kirche", "Schule", "Handwerker", "Gemeindefinanzen", "Flur", "Flurnamen", "Louise Christiane", "Pfarrei"], ["Tinz", "church", "school", "craftsmen", "municipal finances", "field area", "field names", "parish"], ["Dorf", "Kirchengebäude", "Gemeindefinanzen", "Flurnamen"])
pg("427", "Schluss von Tinz (sorbischer Ursprung, Kriegsleiden, Brände 1810/1811, Geistermaschine); Bieblach, Bauerndörfchen ½ Stunde nördlich von Gera: 109 Einwohner, Schafhaltung, Flur 661 8/9 Morgen, Flurnamen, Geschichte (Brandstiftung 1791).",
   "End of Tinz (Sorbian origin, war damage, fires 1810/1811, spirit machine); Bieblach, a small farming village half an hour north of Gera: 109 inhabitants, sheep farming, field area 661 8/9 Morgen, field names, history (arson 1791).",
   ["Tinz", "Bieblach", "Schafzucht", "Flurnamen", "Brandstiftung", "Sorben", "Bauerndorf", "Geistermaschine"], ["Tinz", "Bieblach", "sheep farming", "field names", "arson", "Sorbs", "farming village"], ["Dorf", "Viehzucht", "Brände"])
pg("428", "Beginn des Artikels Gera: Namensformen, Lage an der Elster und Eisenbahnen, Entfernungen zu anderen Städten, Straßennetz mit Haupt- und Querstraßen, freie Plätze, Pflasterung und Beleuchtung.",
   "Start of the article on Gera: name forms, location on the Elster and railways, distances to other towns, street network with main and cross streets, open squares, paving and lighting.",
   ["Gera", "Stadt", "Straßen", "Plätze", "Elster", "Eisenbahn", "Lage", "Namensformen", "Hauptstadt"], ["Gera", "town", "streets", "squares", "Elster", "railway", "location", "name forms", "capital"], ["Stadt", "Siedlungsform", "Straßen"])
pg("429", "Gera: Gasversorgung und Wasserleitung, Kanalisation, die drei Bestandteile der Stadt (Innenstadt mit Ringmauer und fünf Toren, ältere Vorstädte, Neubauten), Vorstadt Zschochern als ehemaliger sorbischer Ort mit Spottlied.",
   "Gera: gas supply and water mains, drainage, the three parts of the town (inner town with ring wall and five gates, older suburbs, new development), the suburb of Zschochern as a former Sorbian village with a mocking song.",
   ["Gera", "Gasversorgung", "Wasserleitung", "Innenstadt", "Stadtmauer", "Zschochern", "Vorstädte", "Brauberechtigung", "Stadtbefestigung"], ["Gera", "gas supply", "water supply", "inner town", "town wall", "Zschochern", "suburbs", "brewing right"], ["Stadt", "Siedlungsform", "Verkehr"])
pg("430", "Gera: Vorstädte und Neubau mit 22 neuen Straßen, Pöppeln als Stadtbezirk; Zählung 1867 mit 1087 Häusern, 3470 Familien, 16283 Einwohnern, Viehbestand, Stockwerke und Dachdeckung; Tabelle der Häuser- und Einwohnerzahlen 1647–1867.",
   "Gera: suburbs and new development with 22 new streets, Pöppeln as a town district; 1867 census with 1,087 houses, 3,470 families, 16,283 inhabitants, livestock, storeys and roofing; table of houses and inhabitants 1647-1867.",
   ["Gera", "Einwohnerzahl", "Häuser", "Volkszählung 1867", "Neubau", "Vorstädte", "Pöppeln", "Bevölkerungsentwicklung", "Tabelle"], ["Gera", "population", "houses", "census 1867", "new development", "suburbs", "Pöppeln", "population growth", "table"], ["Stadt", "Bevölkerung", "Volkszählung"])
pg("431", "Gera: Hauptgebäude (Palais, Schauspielhaus, Regierungsgebäude, Gymnasium, Kaserne, Bahnhof), Kirchen und Kapellen, Geschichte der St. Johanniskirche und ihrer Brände 1450, 1639 und 1780, sechs Kapellen der katholischen Zeit.",
   "Gera: main buildings (palace, theatre, government building, gymnasium, barracks, station), churches and chapels, history of St. John's church and its fires of 1450, 1639 and 1780, six chapels of the Catholic period.",
   ["Gera", "Johanniskirche", "Kapellen", "Schauspielhaus", "Regierungsgebäude", "Gymnasium", "Kirchenbrand", "Wolfgangskapelle", "Palais"], ["Gera", "St. John's church", "chapels", "theatre", "government building", "gymnasium", "church fire", "St. Wolfgang's chapel"], ["Stadt", "Kirchengebäude", "Brände"])
pg("432", "Gera: Reformation und Parochie (eingepfarrte Orte und Filiale), St. Salvatorkirche, St. Trinitatiskirche, Orgel, Glocken, Gruft Heinrichs XXX., Friedhof mit Denkmal Nicolaus de Smit, Gedächtnisfest der Toten.",
   "Gera: Reformation and parish (incorporated places and branch churches), St. Salvator church, St. Trinitatis church, organ, bells, tomb of Heinrich XXX, cemetery with the monument to Nicolaus de Smit, memorial festival of the dead.",
   ["Gera", "Salvatorkirche", "Trinitatiskirche", "Reformation", "Friedhof", "Parochie", "Heinrich XXX.", "Orgel", "Glocken"], ["Gera", "St. Salvator church", "Trinity church", "Reformation", "cemetery", "parish", "organ", "bells"], ["Stadt", "Kirchengebäude", "Reformation", "Pfarreien"])
pg("433", "Gera: Kommunalgebäude (Landarbeitshaus, Hospitäler, Superintendentur, Bürgerschule, Krankenhaus, Rathaus), Privathäuser wie das Fabrikgebäude Focke-Lubold (Bettelburg), Gasthöfe und Mühlen.",
   "Gera: municipal buildings (workhouse, hospitals, superintendency, burgher school, hospital, town hall), private houses such as the Focke-Lubold factory building ('Bettelburg'), inns and mills.",
   ["Gera", "Rathaus", "Krankenhaus", "Hospital", "Bürgerschule", "Focke Lubold", "Bettelburg", "Gasthöfe", "Mühlen"], ["Gera", "town hall", "hospital", "burgher school", "Focke Lubold", "inns", "mills"], ["Stadt", "Gasthof", "Mühlen"])
pg("434", "Gera: Angermühle, Walkmühle, abgetragenes altes Schloss; Behörden vor und nach 1848, Eisenbahnen (Eröffnung 1859 und 1865), Telegraph, Post, Gesundheitswesen und Rechtspflege; katholische Geistliche und erste lutherische Geistliche 1533.",
   "Gera: Anger mill, fulling mill, the demolished old castle; authorities before and after 1848, railways (opened 1859 and 1865), telegraph, post, health care and legal profession; Catholic clergy and the first Lutheran clergy in 1533.",
   ["Gera", "Behörden", "Eisenbahn", "Post", "Telegraph", "Ärzte", "altes Schloss", "Pfarrer", "Reformation"], ["Gera", "authorities", "railway", "post", "telegraph", "physicians", "old castle", "clergy", "Reformation"], ["Stadt", "Ämter und Behörden", "Eisenbahn", "Post und Telegraph"])
pg("435", "Gera: Zahl der Geistlichen und Besetzungsrecht der Pfarrstellen, Parochie mit 19,957 Seelen; Geschichte des Schulwesens von der Knabenschule über das Gymnasium illustre Rutheneum (1608) bis zur Trennung von Gymnasium und Bürgerschule.",
   "Gera: number of clergy and patronage of parish posts, parish of 19,957 souls; history of schooling from the boys' school to the Gymnasium illustre Rutheneum (1608) and the separation of gymnasium and burgher school.",
   ["Gera", "Geistliche", "Parochie", "Schulgeschichte", "Gymnasium", "Heinrich Posthumus", "Mädchenschule", "Seminar", "Superintendent"], ["Gera", "clergy", "parish", "school history", "gymnasium", "Heinrich Posthumus", "girls' school", "teacher seminary"], ["Stadt", "Schule", "Gymnasium", "Pfarreien"])
pg("436", "Gera: Gymnasium (190 Schüler 1868), städtisches Schulwesen mit Realschule (432 Zöglinge), höherer Töchterschule und drei Bürgerschulen, Schulgeldsätze, Sonntagszeichenschule, Fortbildungsschule und Webschule.",
   "Gera: gymnasium (190 pupils in 1868), municipal school system with a Realschule (432 pupils), a higher girls' school and three burgher schools, tuition rates, Sunday drawing school, continuation school and weaving school.",
   ["Gera", "Gymnasium", "Realschule", "Töchterschule", "Bürgerschule", "Schulgeld", "Webschule", "Schülerzahl", "Fortbildungsschule"], ["Gera", "gymnasium", "Realschule", "girls' school", "burgher school", "tuition", "weaving school", "pupil numbers"], ["Schule", "Gymnasium", "Stadt"])
pg("437", "Gera: Schulkörper mit 60 Lehrern und 2700 Zöglingen, Stiftungen des Gymnasiums, Verwaltungsbehörden in Kirchen- und Schulsachen, Privatschulen, Turnvereine, städtische Behörden, Feuerwehr und Vermögen der Stadt (540,600 Thlr.).",
   "Gera: school body with 60 teachers and 2,700 pupils, endowments of the gymnasium, administrative bodies for church and school matters, private schools, gymnastic clubs, municipal authorities, fire brigade and the town's assets (540,600 thalers).",
   ["Gera", "Schüler", "Lehrer", "Stiftungen", "Stadtrat", "Feuerwehr", "Stadtvermögen", "Turnverein", "Schulverwaltung"], ["Gera", "pupils", "teachers", "endowments", "town council", "fire brigade", "town assets", "gymnastics club"], ["Stadt", "Schule", "Stiftungen", "Feuerwehr und Brandschutz"])
pg("438", "Gera: Haushaltsplan der Stadt für 1869 (Tabelle der Kassen mit Einnahmen und Ausgaben in Thalern), Aufwendungen für Schulen, Wasserleitung und Eisenbahn, Armenfürsorge, Obergerichte seit 1237, Erbgerichte, Wappen und Wahrzeichen.",
   "Gera: the town's 1869 budget (table of funds with income and expenditure in thalers), spending on schools, water supply and railway, poor relief, higher jurisdiction since 1237, hereditary jurisdiction, coat of arms and emblems.",
   ["Gera", "Haushaltsplan 1869", "Stadtfinanzen", "Armenwesen", "Gerichtsbarkeit", "Wappen", "Wahrzeichen", "Kämmereikasse", "Thaler"], ["Gera", "budget 1869", "town finances", "poor relief", "jurisdiction", "coat of arms", "emblems", "treasury"], ["Stadt", "Gemeindefinanzen", "Armenwesen", "Rechtspflege"])
pg("439", "Gera: geringer Grundbesitz und Landwirtschaft, Gartenbau, Industrie (Kammwollstoffe, Gerberei, Harmonikas, Maschinenbau) mit Tabelle der Hauptfabriken nach Zahl, Arbeitern und Produktionswert; Dampfkessel und Kohlenverbrauch 1867.",
   "Gera: small landholding and farming, horticulture, industry (worsted cloth, tanning, harmonicas, machine building) with a table of the main factories by number, workers and value of production; steam boilers and coal consumption in 1867.",
   ["Gera", "Industrie", "Kammwollstoffe", "Gerbereien", "Harmonika", "Fabriken", "Dampfmaschinen", "Steinkohle", "Gartenbau"], ["Gera", "industry", "worsted cloth", "tanneries", "harmonicas", "factories", "steam engines", "coal", "horticulture"], ["Stadt", "Industrie", "Textilgewerbe", "Handel"])
pg("440", "Gera: Nebenindustrien, Handel (Umsatz 5–10 Millionen Thaler) und Handelskammer, Zahl der Handwerker nach Gewerben, Wochen- und Jahrmärkte, Gasthöfe und Schankwirtschaften, Arbeiterzahl und Kunstvereine.",
   "Gera: secondary industries, trade (turnover 5-10 million thalers) and chamber of commerce, number of craftsmen by trade, weekly and annual markets, inns and taverns, number of workers and art associations.",
   ["Gera", "Handwerker", "Handel", "Märkte", "Handelskammer", "Gasthöfe", "Gewerbefreiheit", "Wochenmärkte", "Kleinleipzig"], ["Gera", "craftsmen", "trade", "markets", "chamber of commerce", "inns", "freedom of trade", "weekly markets"], ["Stadt", "Handel", "Märkte", "Handwerk"])
pg("441", "Gera: Kunst und Wissenschaft (Künstler, Vereine, Zeitungen, Sammlungen), gemeinnütziger Bauverein 1864, Gesellschaften und Vogelschießen, Banken (Sparkasse, Geraer Bank 1856, Gewerbebank 1859) und Versicherungsvertretungen; Einfluss Geras auf das Umland.",
   "Gera: art and science (artists, societies, newspapers, collections), charitable building society of 1864, social clubs and the bird-shooting festival, banks (savings bank, Gera Bank 1856, trade bank 1859) and insurance agencies; Gera's influence on the surrounding region.",
   ["Gera", "Vereine", "Zeitungen", "Sparkasse", "Geraer Bank", "Vogelschießen", "Bauverein", "Versicherungen", "Sammlungen"], ["Gera", "societies", "newspapers", "savings bank", "Gera Bank", "bird shooting", "building society", "insurance", "collections"], ["Stadt", "Banken und Geld", "Sammlungen"])
pg("442", "Gera: Wirkungskreise der Stadt (Arbeiter-, Vergnügungs-, Produktenkreis), Stadtflur 4720 7/9 Morgen mit Stadtwald und Flurnamen; Sagen und Deutungen des Namens Gera und die frühe Stadtgeschichte (Sorben, 982, 1086).",
   "Gera: spheres of influence of the town (workers, leisure, produce supply), town land of 4720 7/9 Morgen with town forest and field names; legends and interpretations of the name Gera and early town history (Sorbs, 982, 1086).",
   ["Gera", "Stadtflur", "Stadtwald", "Flurnamen", "Namensdeutung", "Sagen", "Sorben", "Häselburg", "Einflussbereich"], ["Gera", "town land", "town forest", "field names", "name etymology", "legends", "Sorbs", "Häselburg"], ["Stadt", "Flurnamen", "Ortsname", "Sagen"])
pg("443", "Gera: Alter und Rechtsstellung des Orts (Gau, Stiftsgut Quedlinburg, Münzrecht, Adel von Gera), Stadterhebung und Gerichtsbarkeit seit 1237, Stadtverwaltung, Gesuch von 1419 um die pößnecker Stadtverfassung; Fußnoten zu Münze und Urkunden.",
   "Gera: age and legal status of the place (district, Quedlinburg convent estate, minting right, nobility of Gera), elevation to town and jurisdiction since 1237, town administration, the 1419 request for the Pößneck town constitution; footnotes on coinage and documents.",
   ["Gera", "Stadtrecht", "Stadterhebung", "Quedlinburg", "Münzrecht", "Stadtverfassung", "Pößneck", "Gerichtsbarkeit", "Mittelalter"], ["Gera", "town rights", "elevation to town", "Quedlinburg", "minting right", "town constitution", "Pößneck", "jurisdiction"], ["Stadt", "Mittelalter", "Rechtspflege", "Urkunden"])
pg("444", "Gera: Stadtgeschichte mit Erstürmung 1450, Bauernkrieg, Zerstörung 1639, Kriegsleiden bis 1813 und 1866, Revolte 1830 und Straßenkampf 1848, Stadtbrände 1686 und 1780 und Pestjahre seit 1348.",
   "Gera: town history with the storming of 1450, the Peasants' War, destruction in 1639, war hardships up to 1813 and 1866, the revolt of 1830 and street fighting in 1848, the town fires of 1686 and 1780 and plague years since 1348.",
   ["Gera", "Zerstörung 1450", "Dreißigjähriger Krieg", "Napoleonische Kriege", "Stadtbrand 1780", "Pest", "Revolution 1848", "Bauernkrieg", "Brände"], ["Gera", "destruction 1450", "Thirty Years' War", "Napoleonic Wars", "town fire 1780", "plague", "1848 revolution", "Peasants' War"], ["Stadt", "Brände", "Dreißigjähriger Krieg", "Napoleonische Kriege"])
pg("445", "Gera: Pestjahre, Wohltäter unter den Landesherren (Heinrich Posthumus, Heinrich XVIII., Heinrich XXX., Heinrich LXVII.), bedeutende Geraer und Superintendenten wie Simon Musäus.",
   "Gera: plague years, benefactors among the rulers (Heinrich Posthumus, Heinrich XVIII, Heinrich XXX, Heinrich LXVII), notable people from Gera and superintendents such as Simon Musäus.",
   ["Gera", "Pest", "Heinrich Posthumus", "Heinrich XXX.", "Heinrich XVIII.", "Simon Musäus", "Landesherren", "Persönlichkeiten", "Denkmal"], ["Gera", "plague", "Heinrich Posthumus", "Heinrich XXX", "Heinrich XVIII", "Simon Musäus", "rulers", "notable persons", "monument"], ["Stadt", "Fürstenhaus", "Seuchen", "Genealogie"])
pg("446", "Gera: Superintendenten und Gelehrte, Nicolas de Smit als Begründer der Wollenmanufactur (1595), Fabrik- und Handelsfirmen, Musiker, Orgelbauer, Maler und Bildhauer, Dichter und Schriftsteller aus Gera.",
   "Gera: superintendents and scholars, Nicolas de Smit as founder of the woollen manufacture (1595), manufacturing and trading firms, musicians, organ builders, painters and sculptors, poets and writers from Gera.",
   ["Gera", "Nicolas de Smit", "Wollmanufaktur", "Fabrikanten", "Musik", "Orgelbauer", "Maler", "Schriftsteller", "Superintendenten"], ["Gera", "Nicolas de Smit", "woollen manufacture", "manufacturers", "music", "organ builders", "painters", "writers", "superintendents"], ["Stadt", "Industrie", "Textilgewerbe", "Genealogie"])
pg("447", "Gera: Schriftsteller, Gelehrte und Juristen aus Gera sowie Gymnasiallehrer; Sagen und Spukgeschichten der Stadt (Gebind, Rathsteich, weiße Dame, Feuerdrache 1780, Bettelburg) und angebliche Klöster.",
   "Gera: writers, scholars and jurists from Gera and gymnasium teachers; legends and ghost stories of the town (Gebind, Rathsteich, White Lady, fire dragon of 1780, Bettelburg) and supposed monasteries.",
   ["Gera", "Sagen", "Spukgeschichten", "weiße Dame", "Gelehrte", "Schriftsteller", "Juristen", "Bettelburg", "Klöster"], ["Gera", "legends", "ghost stories", "White Lady", "scholars", "writers", "jurists", "Bettelburg", "monasteries"], ["Stadt", "Sagen", "Aberglaube"])
pg("448", "Schluss von Gera (angebliche Klöster, unterirdische Gänge); Pöppeln, Vor- und Lustort ¼ Stunde südwestlich von Gera (24 Häuser, 280 Einwohner, Rittergut 1539 an Gera verkauft); Wüstung Vollersdorf im geraer Stadtwald.",
   "End of Gera (supposed monasteries, underground passages); Pöppeln, a suburb and pleasure resort a quarter hour southwest of Gera (24 houses, 280 inhabitants, manor sold to Gera in 1539); the deserted settlement of Vollersdorf in Gera's town forest.",
   ["Gera", "Pöppeln", "Vollersdorf", "Wüstung", "Rittergut", "Martinsgrund", "unterirdische Gänge", "Stadtwald", "Hainberg"], ["Gera", "Pöppeln", "Vollersdorf", "deserted settlement", "manor", "Martinsgrund", "underground passages", "town forest"], ["Dorf", "Wüstung", "Rittergut", "Sagen"])
pg("449", "Schluss der Wüstung Vollersdorf; Debschwitz, mittelgroßes Dorf an der Elster ½ Stunde südsüdwestlich von Gera: Namensformen, 40 Häuser, 374 Einwohner, Vieh, Schule in Lusan, Kammergut, Gemeindefinanzen, Beschäftigung, Flur 751 8/9 Morgen.",
   "End of the deserted settlement of Vollersdorf; Debschwitz, a medium-sized village on the Elster half an hour south-southwest of Gera: name forms, 40 houses, 374 inhabitants, livestock, school at Lusan, crown estate, municipal finances, occupations, field area 751 8/9 Morgen.",
   ["Vollersdorf", "Debschwitz", "Gera", "Elster", "Gemeindefinanzen", "Flur", "Schule Lusan", "Kammergut", "Einwohner"], ["Vollersdorf", "Debschwitz", "Gera", "Elster", "municipal finances", "field area", "Lusan school", "crown estate"], ["Wüstung", "Dorf", "Gemeindefinanzen"])
pg("450", "Schluss von Debschwitz (Lehen, Todaustreiben, Kühtanz, Brände 1801, 1826, 1866); Pforten, langgestrecktes Dorf ½ Stunde südlich von Gera: 42 Häuser, 549 Einwohner, Rittergut mit Besitzerreihe seit 1488, Brauerei, Stärkehäuser, Kapelle.",
   "End of Debschwitz (feudal tenures, Todaustreiben custom, Kühtanz, fires of 1801, 1826 and 1866); Pforten, a long-drawn village half an hour south of Gera: 42 houses, 549 inhabitants, manor with owners since 1488, brewery, Starch Houses, chapel.",
   ["Debschwitz", "Pforten", "Todaustreiben", "Rittergut", "Brauerei", "Stärkehäuser", "Kapelle", "Brände", "Lindenthal"], ["Debschwitz", "Pforten", "Todaustreiben", "manor", "brewery", "Starch Houses", "chapel", "fires"], ["Dorf", "Rittergut", "Brauerei"])
pg("451", "Schluss von Pforten (Schule 104 Schüler, Finanzen, Berufe, Flur 706 7/13 Morgen, Flurnamen, Grabfunde auf dem Heidengottesacker 1799); Beginn von Zwötzen, Kirch- und Grenzdorf ¾ Stunde südlich von Gera, Namensformen, Lage und Ortsteile.",
   "End of Pforten (school with 104 pupils, finances, occupations, field area 706 7/13 Morgen, field names, grave finds at the 'Heidengottesacker' in 1799); start of Zwötzen, a parish and border village three quarters of an hour south of Gera, name forms, location and districts.",
   ["Pforten", "Zwötzen", "Heidengottesacker", "Grabfunde", "Flurnamen", "Schule", "Gemeindefinanzen", "Handwerker", "Brände"], ["Pforten", "Zwötzen", "Heidengottesacker", "grave finds", "field names", "school", "municipal finances", "craftsmen"], ["Dorf", "Vor- und Frühgeschichte", "Gemeindefinanzen", "Flurnamen"])
pg("452", "Zwötzen: Häuser, 551 Einwohner, Vieh, Rittergut mit Besitzerfolge seit 1358, Kirche, Parochie seit 1604 mit Leumnitz, Pfarrgut, Schule (112 Kinder), Gemeindefinanzen und Grundbesitz.",
   "Zwötzen: houses, 551 inhabitants, livestock, manor with owners since 1358, church, parish since 1604 with Leumnitz, parsonage land, school (112 children), municipal finances and landholdings.",
   ["Zwötzen", "Rittergut", "Kirche", "Parochie", "Pfarrei", "Schule", "Gemeindefinanzen", "Leumnitz", "Vieh"], ["Zwötzen", "manor", "church", "parish", "parsonage", "school", "municipal finances", "Leumnitz", "livestock"], ["Dorf", "Rittergut", "Pfarreien", "Schule"])
pg("453", "Schluss von Zwötzen (Berufe, Harmonikatischler, Flur 735,4 Morgen, Flurnamen, Geschichte und Sagen, Überschwemmung 1862); Beginn von Lusan, Kirch- und Schuldörfchen in der Elsteraue ¾ Stunde SWS. von Gera.",
   "End of Zwötzen (occupations, harmonica joiners, field area 735.4 Morgen, field names, history and legends, flood of 1862); start of Lusan, a small parish and school village in the Elster plain three quarters of an hour south-southwest of Gera.",
   ["Zwötzen", "Lusan", "Harmonika", "Flurnamen", "Überschwemmung 1862", "Sagen", "Geschichte", "Elsteraue", "Berufe"], ["Zwötzen", "Lusan", "harmonicas", "field names", "flood 1862", "legends", "history", "Elster plain", "occupations"], ["Dorf", "Berufe", "Sagen", "Naturkatastrophen"])

G.append({"term": "Decem", "variants": ["decempflichtig", "Zehnt"], "kind": "term", "de": "Zehnt: Naturalabgabe an Kirche oder Pfarrer; decempflichtige Höfe müssen sie leisten.", "en": "Tithe: payment in kind to a church or parish priest; farms liable to 'decem' had to render it.", "pages": ["426", "427", "449", "452"]})
G.append({"term": "Pertinenzstück", "variants": ["Pertinenz", "Grundstücksverband"], "kind": "term", "de": "Zu einem Gut oder einer Gerechtigkeit gehöriges Grundstück bzw. mehrere zusammen bewirtschaftete Grundstücke; in den Ortsartikeln neben Gütern und ledigen Grundstücken aufgezählt.", "en": "Parcel belonging to an estate or right; also groups of parcels held together; listed in the village articles next to farms and single parcels.", "pages": ["426", "449", "451", "452"]})
G.append({"term": "Häusler", "variants": ["Kleinhäusler"], "kind": "term", "de": "Dorfbewohner mit Haus und wenig oder keinem Feld, meist Handwerker oder Lohnarbeiter.", "en": "Villager with a house and little or no farmland, usually a craftsman or wage labourer.", "pages": ["419", "426", "449", "451"]})
G.append({"term": "Taglöhner", "variants": ["Taglohn"], "kind": "term", "de": "Tagelöhner, auf Tageslohn arbeitender Landarbeiter.", "en": "Day labourer paid by the day.", "pages": ["419", "426", "449", "451"]})
G.append({"term": "Theilungsacten", "variants": ["Landestheilungsacten"], "kind": "term", "de": "Akten der Landesteilung unter den reußischen Linien von 1647 mit Beschreibung der Orte, Rittergüter und Untertanen.", "en": "Records of the 1647 partition of the lands among the Reuss lines, describing places, manors and subjects.", "pages": ["413", "423", "449"]})
G.append({"term": "Zebracken", "variants": [], "kind": "term", "de": "Böhmische Söldner des Podiebrad, die 1450 Gera erstürmten.", "en": "Bohemian mercenaries of Podiebrad who stormed Gera in 1450.", "pages": ["444"]})
G.append({"term": "Sturmfass", "variants": ["Sturmfässer"], "kind": "term", "de": "Mit Wasser gefüllte Fässer als einfache Brandbekämpfungseinrichtung (hier statt einer Feuerspritze).", "en": "Water-filled barrels serving as simple fire-fighting equipment (here instead of a fire engine).", "pages": ["426"]})
G.append({"term": "Superintendent", "variants": ["Ephorus", "Ephorie"], "kind": "office", "de": "Leitender Geistlicher eines Kirchenbezirks (Ephorie), hier mit Sitz in Gera.", "en": "Senior clergyman of a church district (ephorate), here seated in Gera.", "pages": ["432", "435", "437"]})
G.append({"term": "Gymnasium illustre Rutheneum", "variants": ["Landesgymnasium"], "kind": "institution", "de": "1608 von Heinrich Posthumus als Landesgymnasium in Gera gegründete höhere Schule.", "en": "Higher school founded in Gera in 1608 by Heinrich Posthumus as the state gymnasium.", "pages": ["435", "436"]})
G.append({"term": "Todaustreiben", "variants": [], "kind": "term", "de": "Frühjahrsbrauch, bei dem eine Strohpuppe als Tod aus dem Ort getragen wird; hier in Debschwitz erhalten.", "en": "Spring custom of carrying a straw effigy of Death out of the village; preserved here at Debschwitz.", "pages": ["450"]})
