# -*- coding: utf-8 -*-
E = []
P = []
G = []

def pg(page, de, en, kde, ken, subj):
    P.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

E.append({
    "id": "lusan",
    "name": "Lusan",
    "start": {"page": "453", "block": "b2"},
    "end": {"page": "455", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Kirch- und Schuldörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Losa", "year": 1240}, {"form": "Losen", "year": None}, {"form": "Lossan", "year": 1348}, {"form": "Losa", "year": 1534}],
    "dialect_form": "Lus'n",
    "first_mention_year": 1240,
    "location": {"verbatim": "3/4 Stunde SWS. von Gera, an der Chaussee von da nach Weida, Zwötzen gegenüber", "relative_to": "Gera", "distance_hours": 0.75, "direction": "SSW"},
    "parish": {"status": "Filial", "church_of": "Gera", "verbatim": "Sie war von Anfang an ein Filial von Gera"},
    "school": {"exists": True, "pupils": 59},
    "houses": 16,
    "inhabitants": 140,
    "occupations": {"Bauern": 10, "Kleinhäusler": 8, "Dienstboten": 34, "Fabrikarbeiter": 3, "Handarbeiter": 3},
    "crafts": {"Tischler": 1, "Wirth": 1},
    "flur_morgen": 1083.1,
    "flur_verbatim": "1083 1/10 Morgen",
    "soil": "meist gut (5/10 gut, 3/10 mittel, 2/10 gering)",
    "livestock": {"Pferde": 27, "Rinder": 120, "Schafe": 218, "Schweine": 81, "Ziegen": 10, "Gänse": 282, "Bienenstöcke": 2},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 1 Ortsvorstande besitzt als engere ein Hirtenhaus, Wege, Hutungen, Obstanlagen und Teiche im Steuerwerthe von 557 9/10 Thlr. (früher war ihr Besitz größer, wurde aber vor Kurzem vertheilt), die weitere kein Vermögen und keine Schulden; die Jahresausgabe macht 48 1/6 Thlr.", "assets_thaler": 557.9, "expenditure_thaler": 48.17},
    "facilities": ["Kirche", "Schule", "Gemeindehaus", "Hirtenhaus", "Privatschenke", "Chausseehaus", "Feuerspritze", "Friedhof"],
    "subplaces": [{"name": "Türkenborn", "kind": "Sonstiges", "page": "455"}],
    "events": [
        {"year": 1333, "event_de": "Eine Kirche bereits vorhanden", "event_en": "A church already existed"},
        {"year": 1348, "event_de": "Heinrich von Gera verpfändet das Dörfchen 'Loßan' für 112 Mark Silber", "event_en": "Heinrich of Gera pledges the hamlet 'Loßan' for 112 marks of silver"},
        {"year": 1350, "event_de": "Der Ort kommt an das Kloster Cronswitz, das hier ein Klostervorwerk anlegt", "event_en": "The village passes to Cronswitz convent, which sets up a convent farm here"},
        {"year": 1358, "event_de": "Reinhold v. Zwötzen gibt seine Güter zu Lusan an Cronswitz", "event_en": "Reinhold v. Zwötzen gives his estates at Lusan to Cronswitz"},
        {"year": 1766, "event_de": "Schulhaus erbaut", "event_en": "School building erected"},
        {"year": 1817, "event_de": "Ein Bauernhof brennt ab", "event_en": "A farm burns down"}
    ],
    "persons": ["Heinrich von Gera", "Reinhold v. Zwötzen"],
    "notes": "In der Registerübersicht (S. 826-829) steht für Lusan die Seitenzahl 433; der Artikel steht auf S. 453. 1 Kirche, 1 Schule, 1 Gemeindehaus, 16 Privathäuser; 20 Familien; 1861: 118 Einwohner; 9 Bauerngüter, 1 Grundstücksverband, 7 Pertinenzen, 50 ledige Grundstücke; Kirche 1333 erwähnt, Glocken 1473 und 1837, Kirchenbücher seit 1640, Vermögen circa 900 Thlr.; Patronat der Stadt Gera; Oberröppisch und Debschwitz sind eingeschult; sorbischer Ort.",
    "summary_de": "Lusan, Kirch- und Schuldörfchen in der Elsteraue ¾ Stunde südsüdwestlich von Gera, Filial von Gera; wohlhabender Bauernort mit 140 Einwohnern, Schule für Oberröppisch und Debschwitz, Flur 1083 1/10 Morgen, im Mittelalter an das Kloster Cronswitz gekommen.",
    "summary_en": "Lusan, a small parish and school village in the Elster plain three quarters of an hour south-southwest of Gera, a branch of Gera's parish; a prosperous farming community of 140 inhabitants, school for Oberröppisch and Debschwitz, field area 1083 1/10 Morgen, passed to Cronswitz convent in the Middle Ages."
})

E.append({
    "id": "oberroeppisch",
    "name": "Oberröppisch",
    "start": {"page": "455", "block": "b2"},
    "end": {"page": "456", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Kirch- und Grenzdörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Robschiz", "year": 1239}, {"form": "Robschwiz", "year": None}, {"form": "Obernrepschiz", "year": 1533}, {"form": "Ropschiz", "year": 1534}, {"form": "Oberropschiz", "year": 1670}],
    "dialect_form": "Überröppsch",
    "first_mention_year": 1239,
    "location": {"verbatim": "an der Chaussee von Gera nach Weida, 1 1/4 Stunde fast südlich von jener und 1 1/4 Stunde nördlich von dieser Stadt", "relative_to": "Gera", "distance_hours": 1.25, "direction": "S"},
    "parish": {"status": "Filial", "church_of": "Gera", "verbatim": "Der Ort ist ein Filial von Gera, schult aber nach Lusan"},
    "school": {"exists": False, "note": "schult nach Lusan"},
    "houses": 17,
    "inhabitants": 128,
    "occupations": {"Bauern": 11, "Kleinhäusler": 5, "Taglöhner": 3, "Dienstboten": 16, "Kapitalisten": 3},
    "crafts": {"Brauer": 1, "Schmied": 1, "Schuhmacher": 1, "Zimmermann": 1, "Holzhändler": 1},
    "flur_morgen": 895.06,
    "flur_verbatim": "895 1/18 Morgen",
    "soil": "größtentheils ergiebig",
    "livestock": {"Pferde": 20, "Rinder": 110, "Schafe": 162, "Schweine": 84, "Ziegen": 4, "Bienenstöcke": 12},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 1 Ortsbeamten besitzt als engere ein Hirtenhaus und etwas Land (Hutung) im Steuerwerthe von 826 1/3 Thlr., als weitere weder Vermögen noch Schulden; dagegen circa 115 Thlr. Jahresausgabe und hat 3 Communicationswege zu erhalten", "assets_thaler": 826.33, "expenditure_thaler": 115},
    "facilities": ["Kirche", "Spritzenhaus", "Privatwirthshaus", "Hirtenhaus", "Feuerspritze", "Friedhof"],
    "subplaces": [{"name": "Hörsberg (Heerberg)", "kind": "Sonstiges", "page": "456"}],
    "events": [
        {"year": 1239, "event_de": "Jutta, Gemahlin Heinrichs, begnadigt das Kloster Cronswitz mit 6 Huben in Oberröppisch", "event_en": "Jutta, wife of Heinrich, grants Cronswitz convent 6 hides in Oberröppisch"},
        {"year": 1610, "event_de": "Ober- und Erbgerichte um 1610 an Rudolf v. Fuchs verpfändet und nicht eingelöst", "event_en": "Higher and hereditary jurisdiction pledged to Rudolf v. Fuchs around 1610 and never redeemed"},
        {"year": 1853, "event_de": "Sacristei an die Kirche angebaut", "event_en": "Sacristy added to the church"},
        {"year": 1860, "event_de": "Zwei Bauernhöfe brennen ab", "event_en": "Two farms burn down"}
    ],
    "persons": ["Jutta", "Rudolf v. Fuchs"],
    "notes": "1 Kirche, 1 Spritzenhaus, 17 Privathäuser mit 14 Scheunen; 21 Familien; 1861: 125 Einwohner; 11 Güter, 1 Verbandsstück, 9 ledige Grundstücke; Kirche aus dem 17. Jahrhundert, Bücher seit 1654, Vermögen über 300 Thlr.; 10 Bauernhöfe der St. Johanniskirche in Gera decempflichtig; Patronat der Stadt Gera; Flur im Süden an Weimar (Unterröppisch) grenzend; Hörsberg als Kult-, Wacht- und Lagerpunkt.",
    "summary_de": "Oberröppisch, Kirch- und Grenzdörfchen 1 ¼ Stunde südlich von Gera an der Chaussee nach Weida, Filial von Gera und eingeschult in Lusan; wohlhabende Bauern mit Viehzucht, Flur 895 1/18 Morgen, Hörsberg als Kult- und Kriegspunkt, Besitz des Klosters Cronswitz seit 1239.",
    "summary_en": "Oberröppisch, a small parish and border village one and a quarter hours south of Gera on the Weida road, a branch of Gera's parish with its school at Lusan; prosperous farmers with cattle breeding, field area 895 1/18 Morgen, the Hörsberg as cult and war site, Cronswitz convent holdings since 1239."
})

E.append({
    "id": "zeulsdorf",
    "name": "Zeulsdorf",
    "start": {"page": "456", "block": "b2"},
    "end": {"page": "457", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "kleines Dorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Zeulsdorf", "year": None}, {"form": "Zeilsdorf", "year": None}, {"form": "Seulsdorf", "year": 1533}],
    "dialect_form": "Zeilsdorf",
    "location": {"verbatim": "1 Stunde SWS. von Gera, am Nordfuße des Kirchbergs, im oberen Brietengraben", "relative_to": "Gera", "distance_hours": 1, "direction": "SSW"},
    "elevation": {"value": 650, "unit": "Fuß", "verbatim": "im Gutshofe 650 Fuß hoch"},
    "parish": {"status": "Filial und eingepfarrt", "church_of": "Dürrenebersdorf", "verbatim": "von dem deshalb Zeulsdorf theils Filial, theils ein eingepfarrter Ort ist"},
    "school": {"exists": False, "note": "Schule in Dürrenebersdorf"},
    "houses": 15,
    "inhabitants": 95,
    "occupations": {"Bauern": 12, "Häusler": 2, "Taglöhner": 3, "Dienstboten": 13},
    "flur_morgen": 675.17,
    "flur_verbatim": "675 1/6 Morgen",
    "soil": "3/7 gut, 2/7 mittel, 2/7 gering",
    "livestock": {"Pferde": 8, "Rinder": 69, "Schafe": 225, "Schweine": 45, "Ziegen": 4, "Gänse": 20, "Bienenstöcke": 19},
    "municipal_finances": {"verbatim": "Die Gemeinde unter 1 Ortsbeamten hat außer 10 2/3 ☐R. (und diese mit dem Rittergute gemeinschaftlich) und außer 1 Feuerspritze in Gemeinschaft mit Oberröppisch keinen Besitz und kein Vermögen, dagegen 80 Thlr. Schulden", "debts_thaler": 80, "expenditure_thaler": 80},
    "facilities": ["Rittergut", "Schlosskapelle", "Privatschenke", "Feuerspritze", "Teich"],
    "subplaces": [{"name": "Rittergut Zeulsdorf", "kind": "Rittergut", "page": "456"}],
    "events": [
        {"year": 1409, "event_de": "Das Gut ist im Besitz von Friedr. v. Groph", "event_en": "Estate held by Friedr. v. Groph"},
        {"year": 1648, "event_de": "Beide Gutsteile kommen als vereinigtes Gut durch Kauf an Kanzler Limmer", "event_en": "Both parts of the estate pass as one estate by purchase to Chancellor Limmer"},
        {"year": 1783, "event_de": "9 Morgen 47 ☐R. des Gutswaldes an die Stadt Gera verkauft", "event_en": "9 Morgen 47 square rods of the estate forest sold to the town of Gera"},
        {"year": 1815, "event_de": "Kammercommissionsrath Bartsch verkauft das Gut an Tobias Albert", "event_en": "Councillor Bartsch sells the estate to Tobias Albert"}
    ],
    "persons": ["Friedr. v. Groph", "Kanzler Limmer", "Tobias Albert"],
    "notes": "15 Privathäuser mit 12 Scheunen; 18 Familien; 1861: 90 Einwohner; Rittergut mit 9/11 der Flur, daneben 7 kleine Güter (unter 20 Morgen) und 7 walzende Grundstücke; Rittergut mit Patronat der Kirche in Dürrenebersdorf; in der Gutskapelle (Herrnhaus) Gottesdienst; keine Almosener, keine Gebrechlichen; sorbischer Ursprung; Richtung im Druck 'SWS.'.",
    "summary_de": "Zeulsdorf, kleines versteckt gelegenes Dorf 1 Stunde südsüdwestlich von Gera mit Rittergut (Besitzerfolge seit 1409), Gutskapelle im Herrnhaus, nach Dürrenebersdorf gepfarrt und geschult; 95 Einwohner, Flur 675 1/6 Morgen, Sagen von der Schlosskapelle.",
    "summary_en": "Zeulsdorf, a small, secluded village one hour south-southwest of Gera with a manor (owners since 1409), a chapel in the manor house, in the parish and school district of Dürrenebersdorf; 95 inhabitants, field area 675 1/6 Morgen, legends of the castle chapel."
})

E.append({
    "id": "weissig",
    "name": "Weißig",
    "start": {"page": "457", "block": "b2"},
    "end": {"page": "458", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "kleines Kirch- und Grenzdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Weissigk", "year": 1534}, {"form": "Weißka", "year": 1647}, {"form": "Weißke", "year": None}, {"form": "Weißig", "year": None}],
    "dialect_form": "Wêßg",
    "first_mention_year": 1534,
    "location": {"verbatim": "1/4 Stunde südlich von Dürrenebersdorf", "relative_to": "Dürrenebersdorf", "distance_hours": 0.25, "direction": "S"},
    "elevation": {"value": 860, "unit": "Fuß", "verbatim": "in der Ortsmitte 860 Fuß hoch"},
    "parish": {"status": "Filial", "church_of": "Dürrenebersdorf", "verbatim": "kam dieselbe als Filial zur nahgelegenen Pfarrei Dürrenebersdorf"},
    "school": {"exists": False, "pupils": 18, "note": "schult nach Dürrenebersdorf"},
    "houses": 20,
    "inhabitants": 130,
    "occupations": {"Bauern": 10, "Häusler": 12, "Taglöhner": 4, "Dienstboten": 16, "Kapitalisten": 2},
    "crafts": {"Zimmerleute": 3, "Schmied": 1, "Wagner": 1},
    "flur_morgen": 1015.83,
    "flur_verbatim": "1015⅚ Morgen",
    "soil": "1/5 gut, 2/5 mittel, 2/5 gering",
    "livestock": {"Pferde": 12, "Rinder": 100, "Schafe": 155, "Schweine": 75, "Ziegen": 4, "Gänse": 120, "Bienenstöcke": 7},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere (13 Bauern) circa 5 Morgen (Wiesen, Dorfteich, Dorfräume und Feld) im Werthe von 2000 Thlr., als weitere ist sie ohne Schulden und außer 9 Communicationswegen ohne Vermögen und Besitz; ihre Jahresausgabe beträgt 120—130 Thlr.", "assets_thaler": 2000, "expenditure_thaler_min": 120, "expenditure_thaler_max": 130},
    "facilities": ["Kirche", "Gemeindehaus", "Privatgasthof", "Erbschenke", "Friedhof"],
    "events": [
        {"year": 1732, "event_de": "Neubau der Kirche 1728-1732 an der Stelle der alten Bergkapelle", "event_en": "New church built 1728-1732 on the site of the old hill chapel"},
        {"year": 1731, "event_de": "Brand einiger Häuser", "event_en": "Fire destroys several houses"},
        {"year": 1796, "event_de": "Brandstiftung (9. Juli) durch eine Frau aus Langenberg: Ort bis auf Kirche und einige Häuser abgebrannt", "event_en": "Arson (9 July) by a woman from Langenberg: village burnt down except for the church and a few houses"},
        {"year": 1801, "event_de": "Orgel in der Kirche", "event_en": "Organ installed in the church"}
    ],
    "notes": "20 Privathäuser mit 15 Scheunen; 23 Familien; 1861: 128 Einwohner; 10 Bauerngüter, 1 Grundstücksverband, 8 Pertinenzen, 33 ledige Grundstücke; Kirche (Dachthurm mit 2 Glocken) ohne Vermögen; Gasthof gehörte zu den 7 Erbschenken der Landschaft Gera; deutscher Anbau aus einer Bergkapelle an der Hochstraße; Flur im Süden an Weimar grenzend; 18 Familien bauen ihr Jahresbrod.",
    "summary_de": "Weißig, kleines Kirch- und Grenzdorf auf dem Bergrücken ¼ Stunde südlich von Dürrenebersdorf an der Chaussee Gera–Neustadt; Filial von Dürrenebersdorf, 130 Einwohner, wohlhabende Bauern, Flur 1015⅚ Morgen, Entstehung aus einer Bergkapelle an der Hochstraße, Dorfbrand 1796.",
    "summary_en": "Weißig, a small parish and border village on the ridge a quarter hour south of Dürrenebersdorf on the Gera-Neustadt road; a branch of Dürrenebersdorf parish, 130 inhabitants, prosperous farmers, field area 1015 5/6 Morgen, origin in a hill chapel on the high road, village fire of 1796."
})

E.append({
    "id": "duerrenebersdorf",
    "name": "Dürrenebersdorf",
    "start": {"page": "458", "block": "b2"},
    "end": {"page": "460", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Pfarrkirchdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Dorren-Ebersdorf", "year": None}, {"form": "Durren-Ebersdorf", "year": None}, {"form": "Durnbergsdorf", "year": 1533}, {"form": "Dürren-Ebersdorf", "year": 1647}],
    "dialect_form": "Dörrnebersdorf",
    "location": {"verbatim": "1 Stunde südöstlich von Gera", "relative_to": "Gera", "distance_hours": 1, "direction": "SO"},
    "parish": {"status": "Pfarrkirchdorf", "church_of": None, "verbatim": "Weißig ist ihr Filial, dagegen Zeulsdorf beziehungsweise Filial und eingepfarrt"},
    "school": {"exists": True, "pupils": 100},
    "houses": 48,
    "inhabitants": 345,
    "occupations": {"Bauern": 14, "Kleinhäusler": 35},
    "crafts": {"Maurer": 5, "Schuhmacher": 3, "Korbmacher": 2, "Schneider": 2, "Zimmerleute": 2, "Brunnenmacher": 1, "Hufschmied": 1, "Müller": 1, "Tischler": 1},
    "flur_morgen": 676.95,
    "flur_verbatim": "676,95 Morgen",
    "soil": "circa 176 Morgen gut, 250 mittel, 250 gering",
    "livestock": {"Pferde": 6, "Rinder": 118, "Schweine": 92, "Ziegen": 20, "Gänse": 45, "Bienenstöcke": 15},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere circa 2 1/2 Morgen (Hut, Dorfteich und etwas Laubholz) in geringem Werthe, als weitere gegenwärtig (mit Zeulsdorf gemeinschaftlich) 400 Thlr. Schulden", "debts_thaler": 400},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Rittergut", "Gasthof", "Chausseehaus", "Windmühle", "Lesebibliothek"],
    "subplaces": [
        {"name": "Rittergut Dürrenebersdorf", "kind": "Rittergut", "page": "459"},
        {"name": "Windmühle", "kind": "Mühle", "page": "459"},
        {"name": "Chausseehaus", "kind": "Sonstiges", "page": "459"}
    ],
    "events": [
        {"year": 1533, "event_de": "Kirchenvisitation: letzter katholischer und erster lutherischer Pfarrer Joh. Elsner", "event_en": "Church visitation: last Catholic and first Lutheran priest Joh. Elsner"},
        {"year": 1684, "event_de": "Brand des Pfarrhofs und mehrerer Bauernhäuser im Juni, Pfarrbücher gehen unter", "event_en": "Fire destroys the parsonage and several farmhouses in June; parish registers lost"},
        {"year": 1723, "event_de": "Erweiterung der Kirche", "event_en": "Church enlarged"},
        {"year": 1747, "event_de": "Schulhaus bei der Kirche erbaut", "event_en": "School house built next to the church"},
        {"year": 1785, "event_de": "Kuppelförmiger Turm aufgebaut", "event_en": "Dome-shaped tower built"},
        {"year": 1815, "event_de": "Familie Heynisch kauft das Rittergut", "event_en": "The Heynisch family buys the manor"},
        {"year": 1865, "event_de": "Bedeutende Reparatur der Kirche und Orgel", "event_en": "Major church repair and organ acquisition"}
    ],
    "persons": ["Joh. Elsner", "Ernst Fichtner"],
    "notes": "4 Communalbauten (Kirche, Pfarrei, Schule, Gemeindehaus) und 48 Privathäuser mit 27 Höfen; 79 Familien; 1861: 289 Einwohner; 14 Bauerngüter und 24 ledige Grundstücke neben dem Rittergut; 15 Bauern und das Rittergut treiben Ackerbau als Hauptgeschäft; keine Almosenarmen; Kirchenbücher bis 1685; Pfarrer E. Fichtner der 26. evangelische; Collatur beim zeulsdorfer Rittergut; deutscher Anbau; Name zur Unterscheidung von anderen Ebersdorf (Flur trocken).",
    "summary_de": "Dürrenebersdorf, Pfarrkirchdorf in hoher Lage 1 Stunde südöstlich von Gera an der Chaussee nach Neustadt: Kirche mit Filialen Weißig und Zeulsdorf, Pfarrei und Schule (rund 100 Kinder), Rittergut, 345 Einwohner, Bauern, Kleinhäusler und Handwerker, Flur 676,95 Morgen, trockene Bergflur als Namensgrund.",
    "summary_en": "Dürrenebersdorf, a parish village in a high position one hour southeast of Gera on the Neustadt road: church with branches at Weißig and Zeulsdorf, parsonage and school (about 100 children), manor, 345 inhabitants, farmers, smallholders and craftsmen, field area 676.95 Morgen; the dry upland fields explain the name."
})

E.append({
    "id": "gorlitzsch",
    "name": "Gorlitzsch",
    "start": {"page": "460", "block": "b2"},
    "end": {"page": "461", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Grenzdörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Kurlitzsch", "year": None}, {"form": "Gurlitzsch", "year": None}, {"form": "Gorliz", "year": 1533}, {"form": "Gorlitzsch", "year": 1707}, {"form": "Gorlitz", "year": None}],
    "dialect_form": "Gorltzsch, Gorlsch",
    "location": {"verbatim": "1 1/2 Stunde SSW. von Gera, 1 Stunde NNW. von Sirbis (Weimar) und 1/2 Stunde W. von Unterröppisch (Weimar)", "relative_to": "Gera", "distance_hours": 1.5, "direction": "SSW"},
    "parish": {"status": "eingepfarrt", "church_of": "Unterröppisch", "verbatim": "Das Dörfchen war von jeher und ist noch nach Unterröppisch gepfarrt und nach Sirbis geschult"},
    "school": {"exists": False, "note": "geschult nach Sirbis (Weimar)"},
    "houses": 7,
    "inhabitants": 36,
    "occupations": {"Bauern": 5, "Häusler": 2, "Kapitalisten": 1},
    "crafts": {"Weber": 1},
    "flur_morgen": 427.07,
    "flur_verbatim": "427 7/100 Morgen",
    "soil": "mittelgut",
    "livestock": {"Pferde": 1, "Rinder": 26, "Schafe": 15, "Schweine": 14, "Ziegen": 4, "Gänse": 23, "Bienenstöcke": 7},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 1 Gemeindebeamten besitzt 1 4/15 Morgen Hutung und Obstpflanzung im Werthe von 60 Thlr., sonst kein Vermögen, hat dagegen 24 Thlr. Jahresausgabe, die Unterhaltung von 4 2/3 Morgen Communications- und Vicinalwegen und mit Zeulsdorf, Lusan und Oberröppisch eine gemeinschaftliche Spritze", "assets_thaler": 60, "expenditure_thaler": 24},
    "facilities": ["Spritze (gemeinschaftlich mit Zeulsdorf, Lusan und Oberröppisch)"],
    "events": [
        {"year": 1647, "event_de": "Theilungsacten: Nic. v. Ende zu Kaimberg und Pforten hat Ober- und Untergerichte, Lehn und Zinsen", "event_en": "Partition records: Nic. v. Ende of Kaimberg and Pforten holds the higher and lower jurisdiction, fiefs and dues"}
    ],
    "persons": ["Nic. v. Ende"],
    "notes": "7 zweistöckige Privat-Schieferhäuser mit 6 Scheunen; 7 Familien; 1861: 34 Einwohner; 5 kleine Güter, 2 Grundstücksverbände, 1 Pertinenzstück, 3 ledige Grundstücke; die 5 Gutsbesitzer bauen ihr Jahresbrod; Pfarrei und Schule weimarer Patronat; Flur im Süden und Osten an weimarisches Gebiet grenzend; alter Sorbenanbau, vermutlich Vorwerk eines Ritterguts (Pforten); Grundmauern des im 30jährigen Krieg zerstörten Vorwerks aufgefunden.",
    "summary_de": "Gorlitzsch, kleines Grenzdorf 1 ½ Stunden südsüdwestlich von Gera auf einem Bergsattel; 7 Häuser, 36 Einwohner, nach Unterröppisch gepfarrt und nach Sirbis (beide Weimar) geschult, Bauernort mit Flur von 427 7/100 Morgen, alter Sorbenanbau und wohl Vorwerk des Ritterguts Pforten.",
    "summary_en": "Gorlitzsch, a small border village one and a half hours south-southwest of Gera on a ridge saddle; 7 houses, 36 inhabitants, in the parish of Unterröppisch and the school district of Sirbis (both Weimar), a farming settlement with a field area of 427 7/100 Morgen, an old Sorbian settlement and probably an outlying farm of the Pforten manor."
})

E.append({
    "id": "hundhaupten",
    "name": "Hundhaupten",
    "start": {"page": "461", "block": "b2"},
    "end": {"page": "462", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "zweiherrisches Kirch-, Bauern- und Grenzdörfchen, Filial von Markersdorf (Weimar)",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Hunthewten", "year": None}, {"form": "Hundhoit", "year": None}, {"form": "Hundhäubt", "year": 1534}, {"form": "Hundhäubten", "year": 1660}],
    "dialect_form": "Hundhêden",
    "first_mention_year": 1262,
    "location": {"verbatim": "2 Stunden SW. von Gera", "relative_to": "Gera", "distance_hours": 2, "direction": "SW"},
    "elevation": {"value": 824, "unit": "Fuß", "verbatim": "824 Fuß hoch gelegenen Dorfteich"},
    "parish": {"status": "Filial", "church_of": "Markersdorf", "verbatim": "Filial von Markersdorf (Weimar)"},
    "school": {"exists": True, "pupils": 20, "note": "20 Schulkinder reußischer Seite; Schöna eingeschult"},
    "houses": 22,
    "inhabitants": 165,
    "occupations": {"Bauern": 17, "Häusler": 5, "Taglöhner": 6, "Dienstboten": 28},
    "crafts": {"Maurer": 2, "Zimmerer": 2, "Schneider": 1, "Schuhmacher": 1, "Wagner": 1},
    "flur_morgen": 1542.4,
    "flur_verbatim": "1542 2/5 Morgen",
    "soil": "meist mittelmäßig",
    "livestock": {"Pferde": 24, "Rinder": 141, "Schafe": 234, "Schweine": 77, "Ziegen": 19, "Gänse": 56, "Bienenstöcke": 8},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Ortsbeamten hat als engere einen Grundbesitz (1 Teich, 2 Wiesen, und 1 Trift) im Werthe von circa 1100 Thlr. und als weitere den Dorfraum und 4 Communicationswege, dabei 125 Thlr. Schulden", "assets_thaler": 1100, "debts_thaler": 125, "expenditure_thaler": 150},
    "facilities": ["Kirche (weimarisch)", "Schule (weimarisch)", "Gemeinde-Armenhaus", "Privatschenke", "Feuerspritze (in Großsaara)"],
    "subplaces": [{"name": "Zehntholz", "kind": "Sonstiges", "page": "462"}],
    "events": [
        {"year": 1262, "event_de": "Das Kloster Cronswitz besitzt hier seit 1262 und 1314 Güter, Zinsen und Lehen", "event_en": "Cronswitz convent holds estates, dues and fiefs here from 1262 and 1314"},
        {"year": 1722, "event_de": "Neubau der Kirche", "event_en": "New church built"},
        {"year": 1850, "event_de": "Ein Haus brennt ab", "event_en": "A house burns down"}
    ],
    "notes": "Zweiherriger Ort: reußischer Antheil 2/3, weimarischer 1/3 (weimarische Häusergruppe: 1 Kirche, 1 Schule, 1 Gemeindehaus, 8 Privathäuser); Angaben für den reußischen Teil: 1 Gemeinde-Armenhaus und 22 Privathäuser mit 21 Scheunen, 35 Familien; 1861: 155 Einwohner; 11 starke Güter, 1 Grundstücksverband, 5 ledige Grundstücke (alle Amtslehn); Flur auf drei Seiten von Weimar umschlossen, 16 Teiche und 3 Steinbrüche; Kirche mit Vermögen 550 Thlr., Bücher seit 1600; Parochie Markersdorf (Mutterkirche), Hundhaupten und Schöna Filiale; Zehntholz (circa 120 Morgen) im Besitz von 6 Familien.",
    "summary_de": "Hundhaupten, zweiherriges Kirch-, Bauern- und Grenzdorf 2 Stunden südwestlich von Gera in einer Hochmulde: reußischer Anteil (2/3) mit 22 Häusern und 165 Einwohnern, weimarischer Teil mit Kirche (1722) und Schule, wohlhabende Bauern, Flur 1542 2/5 Morgen, Besitz des Klosters Cronswitz seit 1262.",
    "summary_en": "Hundhaupten, a village shared between two sovereigns (parish, farming and border village) two hours southwest of Gera in an upland hollow: the Reuss part (two thirds) with 22 houses and 165 inhabitants, the Weimar part with the church (1722) and school, prosperous farmers, field area 1542 2/5 Morgen, Cronswitz convent holdings since 1262."
})

E.append({
    "id": "schoena",
    "name": "Schöna",
    "start": {"page": "462", "block": "b2"},
    "end": {"page": "463", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "eingebuchtetes, stillfriedliches, wohlhäbiges Kirch-, Bauern- und Grenzdörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Sconauwe", "year": None}, {"form": "Schenaw", "year": None}, {"form": "Schönau", "year": None}],
    "dialect_form": "Schêne",
    "location": {"verbatim": "1 3/4 Stunde SW. von Gera, inmitten zwischen Kleinsaara und Hundhaupten", "relative_to": "Gera", "distance_hours": 1.75, "direction": "SW"},
    "elevation": {"value": 735, "unit": "Fuß", "verbatim": "Die Kirche, auf dem Kirchberg … 735 Fuß hoch gelegen"},
    "parish": {"status": "Filial", "church_of": "Markersdorf", "verbatim": "Markersdorf wurde zur Mutterkirche, Schöna und Hundhaupten zu Filialen gemacht"},
    "school": {"exists": False, "pupils": 22, "note": "schult nach Hundhaupten"},
    "houses": 23,
    "inhabitants": 163,
    "occupations": {"Pferdebauern": 9, "Kühbauern": 5, "Häusler": 9, "Taglöhner": 9, "Dienstboten": 27, "Kapitalisten": 5},
    "crafts": {"Maurer": 2, "Schmied": 1, "Weber": 1, "Zimmerer": 1},
    "flur_morgen": 1476.8,
    "flur_verbatim": "1476 4/5 Morgen",
    "soil": "3/4 mittelgut, 1/4 gering",
    "livestock": {"Pferde": 24, "Rinder": 125, "Schafe": 159, "Schweine": 86, "Ziegen": 5, "Gänse": 183, "Bienenstöcke": 12},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Ortsbeamten besitzt 1 Gemeindehaus mit Umgebung (28 Ruthen), 9 1/2 Acker Wiesen im Werthe von 700 Thlr. und eine mit Großsaara und Hundhaupten gemeinschaftliche, zu Großsaara aufgestellte Feuerspritze; außerdem kein Vermögen und keine Schulden", "assets_thaler": 700, "expenditure_thaler": 200},
    "facilities": ["Kirche", "Gemeindehaus", "Privatwirthshaus", "Mühle", "Feuerspritze (in Großsaara)", "Friedhof"],
    "subplaces": [{"name": "Mühle Schöna", "kind": "Mühle", "page": "462"}],
    "events": [
        {"year": 1816, "event_de": "Landeshoheit der Kirche kommt von Sachsen an Weimar", "event_en": "Territorial sovereignty over the church passes from Saxony to Weimar"},
        {"year": 1850, "event_de": "Kircheninneres ganz umgestaltet", "event_en": "Church interior completely remodelled"},
        {"year": 1864, "event_de": "Landeshoheit über die Kirche an Reuß j. L. abgetreten; Kirchensatz bleibt bei Weimar", "event_en": "Sovereignty over the church ceded to Reuss j. L.; patronage remains with Weimar"}
    ],
    "notes": "1 Kirchlein, 1 Gemeindehaus und 23 Privathäuser mit 23 Höfen; 28 Familien; 1861: 141 Einwohner; 14 geschlossene Güter und 14 ledige Grundstücke; Kirchenvermögen 65 Thlr., Bücher seit 1600; 14 Familien bauen ihr Jahresbrod; 3 Almosener; Flur im Südwesten an Weimar grenzend (6 Teiche, 1 Steinbruch); deutscher Anbau (die Ableitung 'Schilfhain' wird abgelehnt); Besitz des Klosters Cronswitz seit 1262/1263; Amtsdorf.",
    "summary_de": "Schöna, stillfriedliches Kirch-, Bauern- und Grenzdorf 1 ¾ Stunden südwestlich von Gera im Görlitzbachtal: Kirche als Filial von Markersdorf (Weimar), 1864 an Reuß abgetreten, 163 Einwohner, Pferde- und Kühbauern, Schule in Hundhaupten, Flur 1476 4/5 Morgen, Besitz des Klosters Cronswitz seit 1262.",
    "summary_en": "Schöna, a quiet parish, farming and border village one and three quarter hours southwest of Gera in the Görlitzbach valley: church as branch of Markersdorf (Weimar), ceded to Reuss in 1864, 163 inhabitants, horse and cow farmers, school at Hundhaupten, field area 1476 4/5 Morgen, Cronswitz convent holdings since 1262."
})

# ------------------------------------------------------------------ pages
pg("454", "Lusan: Häuser, Einwohner, Vieh, Kirche (1333 erwähnt, Glocke 1473) als Filial von Gera, Schule für Oberröppisch und Debschwitz, Gemeindefinanzen, Berufe, Flur 1083 1/10 Morgen und Geschichte (1348 Verpfändung, 1350 Kloster Cronswitz).",
   "Lusan: houses, inhabitants, livestock, church (mentioned 1333, bell of 1473) as branch of Gera, school for Oberröppisch and Debschwitz, municipal finances, occupations, field area 1083 1/10 Morgen and history (pledged 1348, Cronswitz convent 1350).",
   ["Lusan", "Kirche", "Schule", "Cronswitz", "Gemeindefinanzen", "Flur", "Filial Gera", "Debschwitz", "Oberröppisch"], ["Lusan", "church", "school", "Cronswitz", "municipal finances", "field area", "branch of Gera", "Debschwitz", "Oberröppisch"], ["Dorf", "Kirchengebäude", "Klöster", "Gemeindefinanzen"])
pg("455", "Schluss von Lusan (Klostervorwerk, Sagen, Brand 1817, Türkenborn); Oberröppisch, Kirch- und Grenzdörfchen 1 ¼ Stunde südlich von Gera: Namensformen, Häuser, Einwohner, Vieh, Kirche als Filial von Gera, Gemeindefinanzen, Berufe, Flur 895 1/18 Morgen.",
   "End of Lusan (convent farm, legends, fire of 1817, Türkenborn spring); Oberröppisch, a small parish and border village one and a quarter hours south of Gera: name forms, houses, inhabitants, livestock, church as branch of Gera, municipal finances, occupations, field area 895 1/18 Morgen.",
   ["Lusan", "Oberröppisch", "Klostervorwerk", "Kirche", "Gemeindefinanzen", "Viehzucht", "Flur", "Filial Gera", "Türkenborn"], ["Lusan", "Oberröppisch", "convent farm", "church", "municipal finances", "cattle breeding", "field area", "branch of Gera"], ["Dorf", "Klöster", "Viehzucht"])
pg("456", "Schluss von Oberröppisch (Gerichtsstand, Kloster Cronswitz 1239, Hörsberg als Kult- und Kriegspunkt, Schwedenschanzen); Zeulsdorf, kleines Dorf mit Rittergut: Lage, Häuser, Einwohner, Vieh, Besitzerfolge des Guts seit 1409, Kapelle im Herrnhaus.",
   "End of Oberröppisch (jurisdiction, Cronswitz convent 1239, the Hörsberg as cult and war site, Swedish redoubts); Zeulsdorf, a small village with a manor: location, houses, inhabitants, livestock, succession of owners of the estate since 1409, chapel in the manor house.",
   ["Oberröppisch", "Zeulsdorf", "Hörsberg", "Rittergut", "Besitzerfolge", "Gutskapelle", "Schwedenschanzen", "Cronswitz", "Dürrenebersdorf"], ["Oberröppisch", "Zeulsdorf", "Hörsberg", "manor", "owners", "manor chapel", "Swedish redoubts", "Cronswitz"], ["Dorf", "Rittergut", "Dreißigjähriger Krieg"])
pg("457", "Schluss von Zeulsdorf (Gemeindefinanzen, Berufe, Flur 675 1/6 Morgen, Sagen); Weißig, kleines Kirch- und Grenzdorf ¼ Stunde südlich von Dürrenebersdorf: Lage, 130 Einwohner, Vieh, Bergkapelle an der Hochstraße, Kirche 1728–1732, Gasthof (Erbschenke), Beginn der Gemeindefinanzen.",
   "End of Zeulsdorf (municipal finances, occupations, field area 675 1/6 Morgen, legends); Weißig, a small parish and border village a quarter hour south of Dürrenebersdorf: location, 130 inhabitants, livestock, hill chapel on the high road, church of 1728-1732, inn (hereditary tavern), start of municipal finances.",
   ["Zeulsdorf", "Weißig", "Bergkapelle", "Hochstraße", "Kirche", "Gasthof", "Erbschenke", "Flur", "Dürrenebersdorf"], ["Zeulsdorf", "Weißig", "hill chapel", "high road", "church", "inn", "hereditary tavern", "field area"], ["Dorf", "Kirchengebäude", "Gasthof"])
pg("458", "Schluss von Weißig (Berufe, Flur 1015⅚ Morgen, Brände 1731 und 1796); Dürrenebersdorf, Pfarrkirchdorf 1 Stunde südöstlich von Gera: Lage, Häuser, Einwohner, Vieh, Reparaturen der Kirche 1723–1827.",
   "End of Weißig (occupations, field area 1015 5/6 Morgen, fires of 1731 and 1796); Dürrenebersdorf, a parish village one hour southeast of Gera: location, houses, inhabitants, livestock, repairs of the church 1723-1827.",
   ["Weißig", "Dürrenebersdorf", "Pfarrkirchdorf", "Kirche", "Brände", "Flur", "Einwohner", "Häuser", "Krebsgrund"], ["Weißig", "Dürrenebersdorf", "parish village", "church", "fires", "field area", "inhabitants", "houses"], ["Dorf", "Pfarreien", "Brände"])
pg("459", "Dürrenebersdorf: Kirche, Pfarrer (Joh. Elsner 1533), Pfarrhof nach Brand 1684, Schule (1747), Rittergut und seine Besitzer seit 1647, Gasthof und Windmühle, Gemeindefinanzen, Bauern und Kleinhäusler.",
   "Dürrenebersdorf: church, pastors (Joh. Elsner in 1533), parsonage after the fire of 1684, school (1747), manor and its owners since 1647, inn and windmill, municipal finances, farmers and smallholders.",
   ["Dürrenebersdorf", "Kirche", "Pfarrer", "Schule", "Rittergut", "Windmühle", "Gemeindefinanzen", "Pfarrhof", "Decem"], ["Dürrenebersdorf", "church", "pastor", "school", "manor", "windmill", "municipal finances", "parsonage", "tithe"], ["Dorf", "Pfarreien", "Rittergut", "Schule"])
pg("460", "Schluss von Dürrenebersdorf (Handwerker, Flur 676,95 Morgen, Namensgrund, Dreißigjähriger Krieg); Gorlitzsch, Grenzdörfchen 1 ½ Stunde südsüdwestlich von Gera: 36 Einwohner, nach Unterröppisch gepfarrt und nach Sirbis geschult (Weimar), Flur 427 7/100 Morgen.",
   "End of Dürrenebersdorf (craftsmen, field area 676.95 Morgen, origin of the name, Thirty Years' War); Gorlitzsch, a small border village one and a half hours south-southwest of Gera: 36 inhabitants, in the parish of Unterröppisch and school district of Sirbis (Weimar), field area 427 7/100 Morgen.",
   ["Dürrenebersdorf", "Gorlitzsch", "Dreißigjähriger Krieg", "Grenzdorf", "Weimar", "Flur", "Handwerker", "Namensherkunft", "Unterröppisch"], ["Dürrenebersdorf", "Gorlitzsch", "Thirty Years' War", "border village", "Weimar", "field area", "craftsmen", "name origin"], ["Dorf", "Dreißigjähriger Krieg", "Ortsname"])
pg("461", "Schluss von Gorlitzsch (Vorwerk, Funde); Hundhaupten, zweiherriges Kirch- und Grenzdorf 2 Stunden südwestlich von Gera: Namensformen, Teilung in reußischen und weimarischen Anteil, Kirche 1722, Schule, 165 Einwohner im reußischen Teil, Gemeindefinanzen, Berufe.",
   "End of Gorlitzsch (outlying farm, finds); Hundhaupten, a village shared between two sovereigns two hours southwest of Gera: name forms, division into Reuss and Weimar parts, church of 1722, school, 165 inhabitants in the Reuss part, municipal finances, occupations.",
   ["Gorlitzsch", "Hundhaupten", "zweiherriger Ort", "Weimar", "Kirche", "Schule", "Gemeindefinanzen", "Berufe", "Grenzdorf"], ["Gorlitzsch", "Hundhaupten", "village shared by two lords", "Weimar", "church", "school", "municipal finances", "occupations"], ["Dorf", "Gemeinden", "Pfarreien"])
pg("462", "Schluss von Hundhaupten (Flur 1542 2/5 Morgen, Flurnamen, Klosterbesitz Cronswitz); Schöna, Kirch-, Bauern- und Grenzdörfchen 1 ¾ Stunde südwestlich von Gera: Häuser, Einwohner, Vieh, Kirche und Zugehörigkeit zu Markersdorf, Landeshoheit 1816 und 1864, Schule in Hundhaupten, Gemeindefinanzen, Berufe.",
   "End of Hundhaupten (field area 1542 2/5 Morgen, field names, Cronswitz convent holdings); Schöna, a small parish, farming and border village one and three quarter hours southwest of Gera: houses, inhabitants, livestock, church and affiliation to Markersdorf, sovereignty in 1816 and 1864, school at Hundhaupten, municipal finances, occupations.",
   ["Hundhaupten", "Schöna", "Landeshoheit", "Markersdorf", "Kirche", "Flurnamen", "Cronswitz", "Gemeindefinanzen", "Bauern"], ["Hundhaupten", "Schöna", "sovereignty", "Markersdorf", "church", "field names", "Cronswitz", "municipal finances", "farmers"], ["Dorf", "Territorialgeschichte", "Pfarreien"])
pg("463", "Schluss von Schöna (Flur 1476 4/5 Morgen, Geschichte); Waltersdorf, Pfarr- und Kirchdorf 2 ½ Stunden westsüdwestlich von Gera: Lage, Häuser, 345 Einwohner, Vieh, Kirche (1752–1756, Brand 1750), Beginn der Geschichte der Pfarrei.",
   "End of Schöna (field area 1476 4/5 Morgen, history); Waltersdorf, a parish village two and a half hours west-southwest of Gera: location, houses, 345 inhabitants, livestock, church (1752-1756, fire of 1750), start of the parish history.",
   ["Schöna", "Waltersdorf", "Kirche", "Pfarrdorf", "Flur", "Brand 1750", "Saarbach", "Einwohner", "Häuser"], ["Schöna", "Waltersdorf", "church", "parish village", "field area", "fire of 1750", "Saar brook", "inhabitants"], ["Dorf", "Kirchengebäude", "Brände"])
