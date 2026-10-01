# -*- coding: utf-8 -*-
E = []
P = []
G = []

def pg(page, de, en, kde, ken, subj):
    P.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

E.append({
    "id": "waltersdorf",
    "name": "Waltersdorf",
    "start": {"page": "463", "block": "b2"},
    "end": {"page": "466", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Pfarr- und Kirchdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Waltersdorf", "year": 1288}],
    "dialect_form": "Waltersdorf",
    "first_mention_year": 1288,
    "location": {"verbatim": "2 1/2 Stunden WSW. von Gera", "relative_to": "Gera", "distance_hours": 2.5, "direction": "WSW"},
    "parish": {"status": "Pfarrdorf", "church_of": None, "verbatim": "Zu ihr gehört kein eingepfarrter Ort, dagegen als Filial das altenburgische Dorf St. Gangloff"},
    "school": {"exists": True, "pupils": 59},
    "houses": 50,
    "inhabitants": 345,
    "occupations": {"Bauern": 21, "Häusler": 31, "Taglöhner": 9, "Dienstboten": 26, "Kapitalisten": 4, "Holz-, Loh- und Kohlenhändler": 4, "Almosener": 7},
    "crafts": {"Maurer": 12, "Schneider": 3, "Fleischer": 2, "Zimmerleute": 2, "Böttcher": 1, "Schmied": 1, "Schuhmacher": 1, "Stellmacher": 1, "Wagner": 1, "Weber": 1},
    "flur_morgen": 1509.54,
    "flur_verbatim": "1509,54 Morgen",
    "soil": "circa 200 Morgen gut, 600 mittel, 700 gering",
    "livestock": {"Pferde": 42, "Rinder": 178, "Schafe": 242, "Schweine": 157, "Ziegen": 39, "Gänse": 400, "Bienenstöcke": 23},
    "municipal_finances": {"verbatim": "Die Gemeinde, deren Beamten 1 Bürgermeister mit Stellvertreter, 1 Schulvorstand und 1 Friedensrichter sind, hat als engere (Alt- oder Braugemeinde) ein Activvermögen von 550 Thlr. und 13 Morgen Grundbesitz, als weitere 70 Thlr. Schulden an das Kirchenärar, und circa 300 Thlr. als Jahresausgabe", "assets_thaler": 550, "debts_thaler": 70, "expenditure_thaler": 300},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Brauhaus", "Spritzenhaus", "Freigut", "Mühle", "Reihenschank", "Singverein"],
    "subplaces": [
        {"name": "Freigut Waltersdorf", "kind": "Rittergut", "page": "465"},
        {"name": "Gänsehals", "kind": "Sonstiges", "page": "463"},
        {"name": "Neustadt", "kind": "Sonstiges", "page": "463"}
    ],
    "events": [
        {"year": 1288, "event_de": "Ein nach dem Ort benanntes adliges Geschlecht kommt vor", "event_en": "A noble family named after the village is recorded"},
        {"year": 1328, "event_de": "Heinrich der Ritterhafte schenkt das Dorf (ohne Rittergut) dem Kloster Cronswitz (1315 die Güter seiner Schwester)", "event_en": "Heinrich the Knightly gives the village (excluding the manor) to Cronswitz convent (in 1315 his sister's estates)"},
        {"year": 1581, "event_de": "St. Gangloff wird von Laußnitz abgelöst und mit Waltersdorf verbunden", "event_en": "St. Gangloff is detached from Laußnitz and joined to Waltersdorf"},
        {"year": 1746, "event_de": "Vergleich zwischen Reuß und Altenburg über kirchliche Rechte (ratifiziert 18. August)", "event_en": "Settlement between Reuss and Altenburg on ecclesiastical rights (ratified 18 August)"},
        {"year": 1750, "event_de": "Brandstiftung am 27. Januar durch Daniel Poster: Kirche, Schule und 11 Bauernhöfe brennen ab", "event_en": "Arson on 27 January by Daniel Poster: church, school and 11 farms burn down"},
        {"year": 1756, "event_de": "Neubau der Kirche 1752-1756", "event_en": "New church built 1752-1756"},
        {"year": 1855, "event_de": "Schulhaus umgebaut und erweitert", "event_en": "School house rebuilt and enlarged"}
    ],
    "persons": ["Daniel Poster", "Jobst Görisch", "J. C. Giebner"],
    "notes": "Außer 1 Kirche, Pfarrei, Schule, Gemeindehaus, Brau- und Spritzenhaus 50 Privathäuser mit 27 Scheunen; 76 Familien; 1861: 334 Einwohner; 20 Güter (mit Freigut), 1 Grundstücksverband, 1 Pertinenz, 65 walzende Grundstücke; Kirchenbücher seit 1604, Kirchenvermögen 225 Thlr.; Pfarrbesoldung circa 900 Thlr.; Filial St. Gangloff (altenburgisch) mit 933 Einwohnern; Räuberbande aus St. Gangloff im 18. Jahrhundert; früher starkes Landfuhrwesen; deutscher Ursprung.",
    "summary_de": "Waltersdorf, Pfarr- und Kirchdorf an der Westgrenze des Landratsbezirks, 2 ½ Stunden westsüdwestlich von Gera: Kirche (1752–1756) mit Filial St. Gangloff (Altenburg), Streit um die kirchlichen Rechte bis 1746, Pfarrer, Schule (59 Kinder), Freigut, 345 Einwohner, Brände (1750), Flur 1509,54 Morgen.",
    "summary_en": "Waltersdorf, a parish village on the western border of the district, two and a half hours west-southwest of Gera: church (1752-1756) with the branch church of St. Gangloff (Altenburg), dispute over ecclesiastical rights until 1746, pastors, school (59 children), free estate, 345 inhabitants, fires (1750), field area 1509.54 Morgen."
})

E.append({
    "id": "kleinsaara",
    "name": "Kleinsaara",
    "start": {"page": "466", "block": "b2"},
    "end": {"page": "467", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Dörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Klein-Serichen", "year": None}, {"form": "Särl", "year": 1640}, {"form": "Kleinsara", "year": 1647}],
    "dialect_form": "Sär'l",
    "location": {"verbatim": "1 3/4 Stunde WSW. von Gera, an der Chaussee von da nach Jena", "relative_to": "Gera", "distance_hours": 1.75, "direction": "WSW"},
    "elevation": {"value": 680, "unit": "Fuß", "verbatim": "am Dorfteiche 680 Fuss hoch gelegen"},
    "parish": {"status": "eingepfarrt", "church_of": "Großsaara", "verbatim": "pfarrt, begräbt und schult von jeher nach Großsaara"},
    "school": {"exists": False, "note": "schult nach Großsaara"},
    "houses": 28,
    "inhabitants": 143,
    "occupations": {"Bauern": 17, "Häusler": 17, "Taglöhner": 7, "Dienstboten": 7, "Kapitalisten": 2},
    "crafts": {"Zimmerleute": 3, "Maurer": 2, "Schuhmacher": 1},
    "flur_morgen": 662.3,
    "flur_verbatim": "662 3/10 Morgen",
    "soil": "4/7 mittelgut, 2/7 gering, 1/7 gut",
    "livestock": {"Pferde": 3, "Rinder": 79, "Schafe": 200, "Schweine": 64, "Ziegen": 23, "Gänse": 30, "Bienenstöcke": 15},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Ortsbeamten besitzt als engere 2 Morgen (Dorfanger und Wiese) im Werthe von circa 200 Thlr., als weitere kein Vermögen, dagegen 600 Thlr. Schulden; ihre Jahresausgabe 112 bis 118 Thlr.", "assets_thaler": 200, "debts_thaler": 600, "expenditure_thaler_min": 112, "expenditure_thaler_max": 118},
    "facilities": ["Vorwerk", "Gemeinde-Armenhaus", "Privatgasthaus", "Mühle", "Schneidemühle", "Sandsteinbrüche"],
    "subplaces": [
        {"name": "Herrschaftliches Vorwerk Kleinsaara", "kind": "Vorwerk", "page": "467"},
        {"name": "Mühle Kleinsaara", "kind": "Mühle", "page": "467"}
    ],
    "events": [
        {"year": 1640, "event_de": "Junker Hans Heinrich Metsch am 27. Februar erschossen", "event_en": "Junker Hans Heinrich Metsch shot on 27 February"},
        {"year": 1650, "event_de": "Die v. Koppy gewinnen um 1650 das Gut und vereinigen es mit Großsaara", "event_en": "Around 1650 the von Koppy family acquires the estate and unites it with Großsaara"}
    ],
    "persons": ["Hans Heinrich Metsch"],
    "notes": "1 herrschaftliches Vorwerksgebäude, 1 Gemeinde-Armenhaus und 28 Privathäuser mit 23 Scheunen; 30 Familien; 1861: 152 Einwohner; 8 geschlossene Güter, 8 ledige Grundstücke neben dem Kammergutsboden; Vorwerk ursprünglich Pertinenzgut der Herrnburg Großsaara, bald nach 1750 durch Graf Heinrich XXX. an die Landesherrschaft und mit dem Kammergut Großsaara verbunden; Sandsteinverarbeitung; 2 Teiche, 4 Sandsteinbrüche.",
    "summary_de": "Kleinsaara, Dörfchen im Saarbachsgrund 1 ¾ Stunde westsüdwestlich von Gera an der Chaussee nach Jena, nach Großsaara gepfarrt und geschult; herrschaftliches Vorwerk (früher Rittergut), 143 Einwohner, Feldbau, Holzhandel und Sandsteinarbeit, Flur 662 3/10 Morgen.",
   "summary_en": "Kleinsaara, a small village in the Saarbach valley one and three quarter hours west-southwest of Gera on the Jena road, in the parish and school district of Großsaara; princely outlying farm (formerly a manor), 143 inhabitants, farming, timber trade and sandstone working, field area 662 3/10 Morgen."
})

E.append({
    "id": "grosssaara",
    "name": "Großsaara",
    "start": {"page": "467", "block": "b2"},
    "end": {"page": "469", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "freundliches Kirch- und Pfarrdorf, einst der weltliche Hauptpunkt der beiden Saara und von Geißen und Langengrobsdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Sara", "year": 1533}, {"form": "Großen Sara", "year": 1533}],
    "dialect_form": "Saare, Grußsaare",
    "first_mention_year": 1533,
    "location": {"verbatim": "1 1/2 Stunde SWS. von Gera, an der Chaussee von da nach Roda", "relative_to": "Gera", "distance_hours": 1.5, "direction": "SSW"},
    "parish": {"status": "Pfarrdorf", "church_of": None, "verbatim": "freundliches Kirch- und Pfarrdorf … Eingepfarrt ist Kleinsaara"},
    "school": {"exists": True, "pupils": 65},
    "houses": 39,
    "inhabitants": 296,
    "occupations": {"Bauern": 17, "Häusler": 26, "Taglöhner": 13, "Dienstboten": 43, "Kapitalisten": 5},
    "crafts": {"Maurer": 7, "Schuhmacher": 3, "Zimmerleute": 3, "Böttcher": 2, "Schmiede": 2, "Schneider": 2, "Tischler": 2, "Wagner": 1},
    "flur_morgen": 1253.4,
    "flur_verbatim": "1253 2/5 Morgen",
    "soil": "5/6 mittelgut, 1/6 gering",
    "livestock": {"Pferde": 31, "Rinder": 165, "Schafe": 350, "Schweine": 107, "Ziegen": 22, "Gänse": 100, "Bienenstöcke": 19},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 8 Ortsbeamten hat außer dem Besitze kleiner Parcellen vor den Häusern mit einem Jahreszinse von 7—8 Thlr. kein Vermögen, dagegen 1400 Thlr. Kirchbauschulden, wovon 600 Thlr. auf Kleinsaara fallen und außerdem noch 950 Thlr. Gemeindeschulden", "debts_thaler": 950, "church_debts_thaler": 1400, "expenditure_thaler": 200},
    "facilities": ["Kammergut", "Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Spritzenhaus", "Privatgasthaus", "Mühle", "Ziegelei", "Schullesebibliothek"],
    "subplaces": [
        {"name": "Kammergut Großsaara", "kind": "Kammergut", "page": "467"},
        {"name": "rother Löwe", "kind": "Sonstiges", "page": "467"},
        {"name": "Mühle Großsaara", "kind": "Mühle", "page": "468"}
    ],
    "events": [
        {"year": 1413, "event_de": "Mittlere Turmglocke mit Mönchsinschrift gegossen", "event_en": "Middle tower bell with monastic inscription cast"},
        {"year": 1633, "event_de": "Ort leidet im Dreißigjährigen Krieg bedeutend", "event_en": "Village suffers badly in the Thirty Years' War"},
        {"year": 1734, "event_de": "Kirche erweitert und fast ganz neu erbaut", "event_en": "Church enlarged and almost entirely rebuilt"},
        {"year": 1756, "event_de": "Tafeln 'Gräfl. Reuß. Plauisch. Territorium 1756' an zwei Häusern", "event_en": "Plaques 'Gräfl. Reuß. Plauisch. Territorium 1756' on two houses"},
        {"year": 1863, "event_de": "Restaurierung der Kirche, neuer Turm (3000 Thlr.)", "event_en": "Church restored, new tower (3,000 thalers)"},
        {"year": 1844, "event_de": "Neubau des Pfarrhauses (3400 Thlr.)", "event_en": "New parsonage built (3,400 thalers)"}
    ],
    "persons": ["Melchior Fehmel", "Kilian Bornig", "C. Bergner"],
    "notes": "1 Kammergut, 1 Kirche, Pfarrei, Schule, Gemeinde- und Spritzenhaus, außerdem 39 Privathäuser mit 24 Scheunen; 59 Familien; 1861: 292 Einwohner; 18 geschlossene Güter und 24 ledige Grundstücke neben dem Kammergut; Kirchenbücher seit 1608, Kirchenvermögen 1900 Thlr.; Pfarrer C. Bergner der 17.; Kammergut ehemals Burgbau und Herrnsitz mit Erbgericht über Groß- und Kleinsaara, Geißen und Langengrobsdorf, durch Heinrich XXX. an die Landesherrschaft; 13 Familien bauen ihr Jahresbrod; 1840 brannten 2 Häuser ab; Geißen und Langengrobsdorf schulten bis 1724 hierher.",
    "summary_de": "Großsaara, Kirch- und Pfarrdorf 1 ½ Stunden südsüdwestlich von Gera im Saarbachsgrund: ehemalige Herrnburg, jetzt Kammergut (mit Vorwerk Kleinsaara), Kirche mit Filialen Geißen und Kleinsaara, Schule (65 Kinder), 296 Einwohner, Bauern, Häusler und Handwerker, Flur 1253 2/5 Morgen, Schulden aus Kirchbau.",
    "summary_en": "Großsaara, a parish village one and a half hours south-southwest of Gera in the Saarbach valley: former castle seat, now a crown estate (with the Kleinsaara farm), church with branches at Geißen and Kleinsaara, school (65 children), 296 inhabitants, farmers, smallholders and craftsmen, field area 1253 2/5 Morgen, debts from the church building."
})

E.append({
    "id": "geissen",
    "name": "Geißen",
    "start": {"page": "469", "block": "b2"},
    "end": {"page": "470", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Kirchdörfchen, Filial von Großsaara",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Gizsan", "year": 1121}, {"form": "Geisingen", "year": 1533}, {"form": "Geussingen", "year": None}, {"form": "Geussen", "year": None}],
    "dialect_form": "Geißen",
    "first_mention_year": 1121,
    "location": {"verbatim": "1 1/4 Stunde WSW. von Gera, 1/4 Stunde unterhalb Großsaara", "relative_to": "Gera", "distance_hours": 1.25, "direction": "WSW"},
    "parish": {"status": "Filial", "church_of": "Großsaara", "verbatim": "Filial von Großsaara"},
    "school": {"exists": True, "pupils": 30},
    "houses": 16,
    "inhabitants": 116,
    "occupations": {"Bauern": 12, "Häusler": 7, "Taglöhner": 4, "Dienstboten": 29, "Kapitalisten": 4},
    "crafts": {"Müller": 2, "Maurer": 1, "Schmied": 1, "Schneider": 1, "Schuhmacher": 1, "Zimmermann": 1},
    "flur_morgen": 1424,
    "flur_verbatim": "1424 Morgen",
    "soil": "4/7 mittel, 1/7 gering, 2/7 gut",
    "livestock": {"Pferde": 16, "Rinder": 102, "Schafe": 260, "Schweine": 68, "Ziegen": 1, "Gänse": 165, "Bienenstöcke": 8},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt gegen 11 Morgen (meist Wiesen), im Werthe von 1200 Thlr., sonst weder Vermögen noch Schulden; ihre Jahresausgabe beträgt gegen 110-115 Thlr. 3 Communications- und Vicinalwege sind zu erhalten", "assets_thaler": 1200, "expenditure_thaler_min": 110, "expenditure_thaler_max": 115},
    "facilities": ["Kirche", "Schule", "Spritzenhaus", "Privatwirthshaus", "Feuerspritze", "Mühle"],
    "subplaces": [{"name": "Mühle (am oberen Ende von Windischenbernsdorf)", "kind": "Mühle", "page": "470"}],
    "events": [
        {"year": 1121, "event_de": "Gizsan in einer Urkunde des Klosters Bosau (Zuordnung unsicher)", "event_en": "Gizsan in a charter of Bosau convent (identification uncertain)"},
        {"year": 1488, "event_de": "Größte Glocke mit Mönchsinschrift gegossen", "event_en": "Largest bell with monastic inscription cast"},
        {"year": 1724, "event_de": "Eigene Schule (bis dahin nach Großsaara)", "event_en": "Own school (previously at Großsaara)"},
        {"year": 1756, "event_de": "Hauptreparatur der Kirche 1756-1757", "event_en": "Major church repair 1756-1757"},
        {"year": 1828, "event_de": "Schulhaus erbaut", "event_en": "School house built"},
        {"year": 1838, "event_de": "Orgel und Verschönerung der Kirche", "event_en": "Organ and church embellishment"}
    ],
    "notes": "1 Kirche, 1 Schule, 1 Spritzenhaus und 16 Privathäuser mit 16 Scheunen; 20 Familien; 1861: 131 Einwohner; 13 Bauerngüter, 2 Pertinenzstücke, 17 ledige Grundstücke; Kirchenbuch seit 1608, Kirchenvermögen 250 Thlr.; Langengrobsdorf ist eingekircht und eingeschult; alter sorbischer Anbau.",
    "summary_de": "Geißen, Kirchdörfchen, Filial von Großsaara, 1 ¼ Stunde westsüdwestlich von Gera im Saarbachtal; kleine Kirche mit Altarschnitzwerk und Glocke von 1488, eigene Schule seit 1724 (30 Kinder), 116 Einwohner, wohlhabende Bauern, Flur 1424 Morgen, erste Erwähnung wohl 1121.",
    "summary_en": "Geißen, a small church village and branch of Großsaara, one and a quarter hours west-southwest of Gera in the Saarbach valley; small church with carved altarpiece and a bell of 1488, own school since 1724 (30 children), 116 inhabitants, prosperous farmers, field area 1424 Morgen, probably first mentioned in 1121."
})

E.append({
    "id": "langengrobsdorf",
    "name": "Langengrobsdorf",
    "start": {"page": "470", "block": "b2"},
    "end": {"page": "471", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "tief eingebuchtetes, stilllebiges Dörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Grobstorf", "year": 1533}],
    "dialect_form": "Langengrußdorf, Langengroßdorf",
    "first_mention_year": 1533,
    "location": {"verbatim": "1 1/2 Stunde WSW. von Gera, 1/4 Stunde SOS. von Geißen", "relative_to": "Gera", "distance_hours": 1.5, "direction": "WSW"},
    "elevation": {"value": 670, "unit": "Fuß", "verbatim": "in der Mitte 670 Fuß hoch gelegen"},
    "parish": {"status": "eingepfarrt", "church_of": "Geißen", "verbatim": "Der Ort kircht, begräbt und schult nach Geißen"},
    "school": {"exists": False, "note": "schult seit 1724 nach Geißen, vorher Großsaara"},
    "houses": 11,
    "inhabitants": 77,
    "occupations": {"Bauern": 7, "Häusler": 3, "Taglöhner": 1, "Dienstboten": 11, "Kapitalisten": 2},
    "crafts": {"Maurer": 3, "Schneider": 1, "Uhrmacher": 1},
    "flur_morgen": 763.59,
    "flur_verbatim": "763,59 Morgen",
    "livestock": {"Pferde": 8, "Rinder": 51, "Schafe": 70, "Schweine": 40, "Ziegen": 10, "Gänse": 31, "Bienenstöcke": 2},
    "municipal_finances": {"verbatim": "Die kleine Gemeinde besitzt circa 6 Morgen (Communicationswege, Bach, Laubholz) mit 7 Steuereinheiten im Werthe von 70 Thlr., außerdem kein Vermögen, dagegen 682 Thlr. Schulden; die Jahresausgabe macht gegen 100 Thlr.", "assets_thaler": 70, "debts_thaler": 682, "expenditure_thaler": 100},
    "facilities": ["Gemeindehaus", "Privatschenke"],
    "events": [
        {"year": 1666, "event_de": "Kleines herrschaftliches Gut im Besitz derer v. Koppy", "event_en": "Small manorial estate held by the von Koppy family"},
        {"year": 1724, "event_de": "Schulverband mit Geißen", "event_en": "School district joined with Geißen"}
    ],
    "notes": "1 Gemeindehaus und 11 Privathäuser mit 9 Scheunen; 12 Familien; 1861: 72 Einwohner; Schafe (70) laut Fußnote nur 1864 (1867 keine angegeben); 7 geschlossene Güter, 1 Pertinenzstück, 11 ledige Grundstücke; 7 Familien bauen ihr Jahresbrod; 2 Almosenempfänger; sorbischer Ursprung vermutet (Dreiergruppe Pöppeln, Grobsdorf, Geißen).",
    "summary_de": "Langengrobsdorf, kleines tief eingebuchtetes Dorf im Langenthal 1 ½ Stunden westsüdwestlich von Gera, nach Geißen gepfarrt und geschult; 77 Einwohner, Feldwirtschaft und Holzhandel, wohlhabend, Flur 763,59 Morgen, Gemeindeschulden 682 Thlr.",
    "summary_en": "Langengrobsdorf, a small village tucked into the Langenthal one and a half hours west-southwest of Gera, assigned to the parish and school of Geißen; 77 inhabitants, farming and timber trade, prosperous, field area 763.59 Morgen, municipal debts of 682 thalers."
})

E.append({
    "id": "windischenbernsdorf",
    "name": "Windischenbernsdorf",
    "start": {"page": "471", "block": "b2"},
    "end": {"page": "472", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Langdörfchen in angenehmer Lage",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Börensdorf", "year": 1333}, {"form": "Winschenbernsdorf", "year": 1534}],
    "dialect_form": "Winschbernsdorf",
    "first_mention_year": 1333,
    "location": {"verbatim": "1 1/4 Stunde WSW. von Gera, an der Chaussee von da nach Roda", "relative_to": "Gera", "distance_hours": 1.25, "direction": "WSW"},
    "parish": {"status": "eingepfarrt", "church_of": "Frankenthal", "verbatim": "Der Ort pfarrt, begräbt und schult, dermalen mit 60 Kindern, nach Frankenthal"},
    "school": {"exists": False, "pupils": 60, "note": "schult nach Frankenthal"},
    "houses": 32,
    "inhabitants": 254,
    "occupations": {"Bauern": 10, "Kleinhäusler": 22, "Taglöhner": 25, "Dienstboten": 15},
    "crafts": {"Fleischer": 1, "Maurer": 4, "Zimmerleute": 5},
    "flur_morgen": 600.83,
    "flur_verbatim": "600 5/6 Morgen",
    "soil": "3/4 mittelgut, 1/4 gering",
    "livestock": {"Pferde": 14, "Rinder": 75, "Schweine": 45, "Ziegen": 6, "Gänse": 80, "Bienenstöcke": 1},
    "municipal_finances": {"verbatim": "Die Gemeinde unter 8 Ortsbeamten (incl. Gemeinderath) hat außer 1/2 Morgen Bachsand im Werthe von 25 Thlr. kein Vermögen, dagegen 75 Thlr. Schulden und einen Jahresetat von 100 Thlr.", "assets_thaler": 25, "debts_thaler": 75, "expenditure_thaler": 100},
    "facilities": ["Gemeinde-Armenhaus", "Privatgasthaus (Erbkretschmar)", "Mühle (zu Geißen gehörig)"],
    "subplaces": [{"name": "Mühl-, Oel- und Schneidemühle (gehört zu Geißen)", "kind": "Mühle", "page": "471"}],
    "events": [
        {"year": 1618, "event_de": "Ein Einwohner wegen fünfmaligen Meineids hingerichtet", "event_en": "An inhabitant executed for perjury committed five times"},
        {"year": 1666, "event_de": "Peter Fr. Pflug auf Scheubengrobsdorf besitzt auch Windischenbernsdorf", "event_en": "Peter Fr. Pflug of Scheubengrobsdorf also owns Windischenbernsdorf"}
    ],
    "persons": ["Peter Fr. Pflug"],
    "notes": "Außer 1 Gemeinde-Armenhaus 32 Privathäuser mit 15 Scheunen; 61 Familien; 1861: 266 Einwohner; 6 Bauerngüter, 4 Pertinenzstücke, 6 Grundstücksverbände, 33 ledige Grundstücke; ehemaliges Rittergut mit Scheubengrobsdorf verbunden (Besitz seit über 200 Jahren); 4 Almosenarme; Taglöhner meist in Färbereien und Fabriken von Gera; früher zur Pottendorfer, später zur Geraer Kirche; gehörte zur Pflege Langenberg; sorbischer Anbau.",
    "summary_de": "Windischenbernsdorf, Langdorf im Saartal 1 ¼ Stunde westsüdwestlich von Gera an der Chaussee nach Roda, nach Frankenthal gepfarrt und geschult (60 Kinder); 254 Einwohner, vorwiegend Taglöhner und Fabrikarbeiter in Gera, ehemaliges Rittergut, Flur 600 5/6 Morgen.",
    "summary_en": "Windischenbernsdorf, a long village in the Saar valley one and a quarter hours west-southwest of Gera on the Roda road, in the parish and school district of Frankenthal (60 children); 254 inhabitants, mostly day labourers and factory workers in Gera, a former manor, field area 600 5/6 Morgen."
})

E.append({
    "id": "scheubengrobsdorf",
    "name": "Scheubengrobsdorf",
    "start": {"page": "472", "block": "b2"},
    "end": {"page": "473", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "tief eingebuchtetes Dörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Scheiblingengrobsdorf", "year": None}, {"form": "Scheibengrobsdorf", "year": None}],
    "dialect_form": "Grusdorf, Scheimgrusdorf",
    "location": {"verbatim": "1 Stunde WSW. von Gera, seitwärts der gera-rodaer Hochstraße, im Saarthal", "relative_to": "Gera", "distance_hours": 1, "direction": "WSW"},
    "elevation": {"value": 590, "unit": "Fuß", "verbatim": "am untern Ende (W.) 590 Fuß hoch gelegen"},
    "parish": {"status": "eingepfarrt", "church_of": "Frankenthal", "verbatim": "Der Ort pfarrt, begräbt und schult, gegenwärtig mit 38 Kindern, nach dem 1/4 Stunde entfernten Frankenthal"},
    "school": {"exists": False, "pupils": 38, "note": "schult nach Frankenthal"},
    "houses": 32,
    "inhabitants": 221,
    "occupations": {"Bauern": 11, "Kleinhäusler": 21, "Taglöhner": 14, "Dienstboten": 20, "Handwerker": 15},
    "crafts": {"Branntweinbrenner": 1, "Gärtner": 1, "Holzhändler": 1},
    "flur_morgen": 936.5,
    "flur_verbatim": "936 1/2 Morgen",
    "soil": "1/7 gut, 4/7 mittelgut, 2/7 mager",
    "livestock": {"Pferde": 21, "Rinder": 91, "Schafe": 304, "Schweine": 54, "Ziegen": 10, "Gänse": 100, "Bienenstöcke": 15},
    "municipal_finances": {"verbatim": "Die Gemeinde unter 9 Ortsbeamten (incl. Gemeinderath) hat als engere gegen 6 Morgen Weideanger, zum Theil mit Pflaumenbäumen besetzt, über 600 Thlr. werth, als weitere blos Schulden und zwar 1300 Thlr.; ihr Jahresbedarf beträgt 350 Thlr.", "assets_thaler": 600, "debts_thaler": 1300, "expenditure_thaler": 350},
    "facilities": ["Rittergut", "Gemeindehaus", "Privatgasthaus", "Mühle (Oel-, Loh- und Schneidemühle)", "Fischteich"],
    "subplaces": [
        {"name": "Rittergut Scheubengrobsdorf", "kind": "Rittergut", "page": "472"},
        {"name": "Mühle Scheubengrobsdorf", "kind": "Mühle", "page": "473"}
    ],
    "events": [
        {"year": 1666, "event_de": "Peter Fr. Pflug besitzt Scheubengrobsdorf, Frankenthal und Windischenbernsdorf", "event_en": "Peter Fr. Pflug holds Scheubengrobsdorf, Frankenthal and Windischenbernsdorf"},
        {"year": 1683, "event_de": "Familie Dathe besitzt das Gut bis 1855", "event_en": "The Dathe family holds the estate until 1855"},
        {"year": 1867, "event_de": "Ludwig Jul. Preller aus Weimar kauft das Gut", "event_en": "Ludwig Jul. Preller of Weimar buys the estate"},
        {"year": 1771, "event_de": "Bergwand stürzt nach langem Regen ein (Erdfallsacker)", "event_en": "Hillside collapses after long rain (Erdfallsacker)"}
    ],
    "persons": ["Peter Fr. Pflug", "Ludwig Jul. Preller"],
    "notes": "1 Rittergut, 1 Gemeindehaus und 32 Privathäuser mit 30 Scheunen; 45 Familien; 1861: 221 Einwohner; Rittergut mit der Hälfte der Ortsflur; 11 geschlossene Güter, 1 Pertinenzstück, 38 ledige Grundstücke; 6 Bauernfamilien bauen ihr Jahresbrod; Rittergut wechselt mit Töppeln im Besetzungsrecht der Pfarr- und Schulstellen Frankenthal und Mühlsdorf; Flur enthält einen Teil der Wüstung Vollersdorf; wahrscheinlich sorbischer Ursprung.",
    "summary_de": "Scheubengrobsdorf, Dörfchen im Saartal 1 Stunde westsüdwestlich von Gera mit Rittergut (Besitzerfolge seit 1666), nach Frankenthal gepfarrt und geschult (38 Kinder); 221 Einwohner, Kleinhäusler und Taglöhner, Flur 936 1/2 Morgen, Gemeindeschulden 1300 Thlr., Rittergut mit Patronatsrecht.",
    "summary_en": "Scheubengrobsdorf, a small village in the Saar valley one hour west-southwest of Gera with a manor (owners since 1666), in the parish and school district of Frankenthal (38 children); 221 inhabitants, smallholders and day labourers, field area 936 1/2 Morgen, municipal debts of 1300 thalers, manor with patronage rights."
})

E.append({
    "id": "frankenthal",
    "name": "Frankenthal",
    "start": {"page": "473", "block": "b2"},
    "end": {"page": "476", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "zweizeiliges, tief eingebettetes, vom Straßenverkehr seitwärts gelegenes, volkreiches Langdorf mit Kirche, Pfarrei, Schule und Rittergut",
    "type": "Dorf",
    "wuestung": False,
    "location": {"verbatim": "1 Stunde westlich von der Stadt Gera", "relative_to": "Gera", "distance_hours": 1, "direction": "W"},
    "parish": {"status": "Pfarrdorf", "church_of": None, "verbatim": "Eingepfarrt sind Ernsee, Scheubengrobsdorf, Windischenbernsdorf und Töppeln und außerdem ist Mühlsdorf ihr Filial. Demnach umfaßt die Parochie 1720 Seelen"},
    "school": {"exists": True, "pupils": 307},
    "houses": 82,
    "inhabitants": 689,
    "occupations": {"Bauern": 9, "Häusler": 76, "Taglöhner": 120, "Dienstboten": 11, "Handeltreibende": 6, "Chirurg": 1, "Almosenempfänger": 15},
    "crafts": {"Zimmergesellen": 16, "Maurergesellen": 12, "Schneider": 4, "Schuhmacher": 4, "Gerber": 3, "Schmiede": 3, "Bäcker": 2, "Fleischer": 2, "Tischler": 2, "Wagner": 2, "Böttcher": 1, "Glaser": 1, "Ziegelbrenner": 1},
    "flur_morgen": 791.54,
    "flur_verbatim": "791,54 Morgen",
    "soil": "im Thale mittelgut, an den Bergwänden gering",
    "livestock": {"Pferde": 13, "Rinder": 81, "Schafe": 60, "Schweine": 78, "Ziegen": 39, "Gänse": 80, "Bienenstöcke": 7},
    "municipal_finances": {"verbatim": "Die Gemeinde unter 11 Ortsbeamten (incl. Gemeinderath) hat weder als engere (ihr Gemeindeanger wurde vor 15 Jahren mit 980 Thlr. einzeln verkauft und das Geld vertheilt) noch als weitere irgend Vermögen, dagegen 500 Thlr. Schulden und einen Jahresbedarf von 487 Thlr. für Communalbauten, 3 Communications- und 3 Vicinalwege", "debts_thaler": 500, "expenditure_thaler": 487},
    "facilities": ["Rittergut", "Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Privatgasthaus", "Privatschenke", "Mühle", "Schneidemühle", "Ziegelei", "Gendarm", "Steinbrüche"],
    "subplaces": [
        {"name": "Rittergut Frankenthal", "kind": "Rittergut", "page": "473"},
        {"name": "Sperlingsberg", "kind": "Sonstiges", "page": "473"}
    ],
    "events": [
        {"year": 1517, "event_de": "Neubau des alten Kirchleins (Platte mit dem Namen des Pfarrers Andres Franck)", "event_en": "New building of the old chapel (slab naming the priest Andres Franck)"},
        {"year": 1533, "event_de": "Kirchenvisitation: letzter katholischer Pfarrer Jacob Ziegler", "event_en": "Church visitation: last Catholic priest Jacob Ziegler"},
        {"year": 1715, "event_de": "Matrikel verzeichnet nur 20 Zinshäuser", "event_en": "Register lists only 20 tenant houses"},
        {"year": 1732, "event_de": "Kirche 1728-1732 neu erbaut", "event_en": "Church rebuilt 1728-1732"},
        {"year": 1772, "event_de": "Ruhrseuche nach großer Teuerung", "event_en": "Dysentery epidemic after great dearth"},
        {"year": 1819, "event_de": "Blitzschlag in Turm und Kirche, Brand rasch erstickt", "event_en": "Lightning strikes tower and church, fire quickly extinguished"},
        {"year": 1841, "event_de": "Neues Schulhaus am 14. October eingeweiht", "event_en": "New school house consecrated on 14 October"}
    ],
    "persons": ["Gottl. Heinr. Seiffarth", "Lor. Liebold", "J. Christoph Klaunig"],
    "notes": "86 Gebäude, darunter 4 Communalbauten (Kirche, Pfarrei, Schule, Gemeindehaus) und mit dem Gutsgebäude 82 Privathäuser mit 20 Scheunen; 176 Familien; 1861: 633 Einwohner; an Volkszahl der 6. Ort im Landrathsbezirk Gera; Rittergut (1/4 der Flur) gehörte früher mit Scheubengrobsdorf und Windischenbernsdorf zusammen, jetzt Kratzsch (Kaufpreis 19,050 Thlr.); 5 geschlossene Güter, 3 Pertinenzstücke, 1 Grundstücksverband, 56 ledige Grundstücke; Kirchenbücher seit 1645, Kirchenvermögen circa 500 Thlr.; Pfarrer Seiffarth (gest. 1869) der 25.; Kirche in der Nachfolge der Pottendorfer Marienkirche; Diebsbande 1816-1819; 3 wilde Ehen; Hammerwerk und Wollkämmerei eingegangen.",
    "summary_de": "Frankenthal, volkreiches Langdorf mit Kirche, Pfarrei, Schule und Rittergut, 1 Stunde westlich von Gera im Saartal: Mittelpunkt einer Parochie (1720 Seelen), 689 Einwohner, überwiegend Häusler und Taglöhner, Kirche (1728–1732), Schule (307 Kinder), Gemeindearmut, Flur 791,54 Morgen und Ortsgeschichte.",
    "summary_en": "Frankenthal, a populous long village with church, parsonage, school and manor, one hour west of Gera in the Saar valley: centre of a parish (1,720 souls), 689 inhabitants, mostly smallholders and day labourers, church (1728-1732), school (307 children), municipal poverty, field area 791.54 Morgen and local history."
})

E.append({
    "id": "thieschitz",
    "name": "Thieschitz",
    "start": {"page": "476", "block": "b2"},
    "end": {"page": "477", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "freundlich gelegenes Kirch- und Pfarrdörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Theschiß", "year": 1533}, {"form": "Tieschiß", "year": None}, {"form": "Thischitz", "year": None}, {"form": "Teschwitz", "year": None}],
    "dialect_form": "Thischitz",
    "first_mention_year": 1533,
    "location": {"verbatim": "1 1/8 Stunde NW. von Gera", "relative_to": "Gera", "distance_hours": 1.125, "direction": "NW"},
    "parish": {"status": "Pfarrdorf", "church_of": None, "verbatim": "eine auf der Kirchberghöhe erbaute Kirche, in die jetzt wie früher die zwei nahe gelegenen Dörfer Rubitz und Milbitz eingepfarrt sind"},
    "school": {"exists": True, "pupils": 66},
    "houses": 19,
    "inhabitants": 129,
    "occupations": {"Bauern": 7, "Häusler": 9, "Taglöhner": 5, "Dienstboten": 20, "Almosenarme": 3},
    "crafts": {"Maurer": 3, "Zimmerer": 3, "Schneider": 1, "Schuhmacher": 1, "Zeugmacher": 1, "Harmonikamacher": 1, "Gypsbrennerei": 1, "Ziegelbrennerei": 1},
    "flur_morgen": 665.25,
    "flur_verbatim": "665 1/4 Morgen",
    "soil": "größtentheils ergiebig",
    "livestock": {"Pferde": 13, "Rinder": 78, "Schafe": 127, "Schweine": 56, "Ziegen": 16, "Gänse": 115, "Bienenstöcke": 10},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere einige Grundstücke und darauf 1000 Thlr. Schulden, als weitere 150 Thlr. Passiva; ihre Jahresausgabe beträgt 150—170 Thlr. für öffentliche Bauten, 2 Communicationswege und 3 Vicinalwege", "debts_thaler": 1000, "expenditure_thaler_min": 150, "expenditure_thaler_max": 170},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Spritzenhaus", "Privatschenkwirthschaft", "Feuerspritze", "Ziegelei", "Gypsbrennerei", "Schullesebibliothek"],
    "events": [
        {"year": 1541, "event_de": "Sacristeistein mit Jahreszahl und Ort Robicz (Erbbegräbnis der Rubitzer Gutsbesitzer)", "event_en": "Sacristy stone with date and place Robicz (hereditary burial of the Rubitz estate owners)"},
        {"year": 1810, "event_de": "Kirche innen verschönert und mit Orgel versehen", "event_en": "Church interior embellished and equipped with an organ"},
        {"year": 1838, "event_de": "Neues massives Schulhaus", "event_en": "New solid school house"},
        {"year": 1857, "event_de": "Patronat geht vom Hauptpfarrer zu Gera an den Landesherrn über", "event_en": "Patronage passes from the principal pastor of Gera to the sovereign"},
        {"year": 1867, "event_de": "Schiff der Kirche neu gebaut, Turm ausgebessert", "event_en": "Nave of the church rebuilt, tower repaired"}
    ],
    "persons": ["Joh. Grau", "Heinr. Spengler", "Mackroth"],
    "notes": "5 Communalbauten (Kirche, Pfarrei, Schule, Gemeinde- und Spritzenhaus), außerdem 19 Privathäuser mit 7 Scheunen und 12 Höfen; 26 Familien; 1861: 115 Einwohner; Schüler: 14 aus Thieschitz, 43 aus Rubitz, 11 aus Milbitz; 7 Bauerngüter, 2 Grundstücksverbände, 6 Pertinenzstücke, 26 ledige Grundstücke; Flur 13/100 Wald, 20/100 Wiesen, 53/100 Feld; Kirchenvermögen 5500 Thlr.; Pfarrer H. Spengler der 27.; Pfarrer Mackroth (gest. 1866) Mineraloge mit Sammlung; Gips- und Kalkgewinnung; sorbischer Anbau; altheidnischer Kultpunkt vermutet.",
    "summary_de": "Thieschitz, Kirch- und Pfarrdörfchen 1 ⅛ Stunde nordwestlich von Gera am Ausgang des Erlbachs: Kirche mit eingepfarrten Dörfern Rubitz und Milbitz, Schule (66 Kinder), Pfarrer Mackroth als Mineraloge, 129 Einwohner, Gipsbrennerei und Ziegelei, geologisch interessante Flur (665 1/4 Morgen).",
    "summary_en": "Thieschitz, a small parish village one and an eighth hours northwest of Gera at the mouth of the Erlbach: church with the incorporated villages of Rubitz and Milbitz, school (66 children), pastor Mackroth as a mineralogist, 129 inhabitants, gypsum burning and brickworks, geologically interesting fields (665 1/4 Morgen)."
})

# ------------------------------------------------------------------ pages
pg("464", "Waltersdorf: Kirchengeschichte (Kirchenbücher seit 1604), Filial St. Gangloff (Altenburg), Streit zwischen Reuß und Altenburg um die kirchlichen Rechte bis zum Vergleich 1746, Patronat, Gottesacker, Pfarrhausbauten und Pfarreieinkünfte.",
   "Waltersdorf: church history (registers since 1604), branch church St. Gangloff (Altenburg), dispute between Reuss and Altenburg over ecclesiastical rights until the settlement of 1746, patronage, graveyard, parsonage buildings and parish revenues.",
   ["Waltersdorf", "Sankt Gangloff", "Kirche", "Pfarrei", "Altenburg", "Vergleich 1746", "Patronat", "Pfarrhaus", "Kirchenbücher"], ["Waltersdorf", "St. Gangloff", "church", "parish", "Altenburg", "settlement of 1746", "patronage", "parsonage", "church registers"], ["Dorf", "Pfarreien", "Kirche", "Territorialgeschichte"])
pg("465", "Waltersdorf: Pfarrer, Schule (59 Schüler), Freigut und seine Besitzer, Gemeindefinanzen, Berufe (Maurer, Händler), Armut und Landfuhrwesen, Flur 1509,54 Morgen mit Boden- und Obstbau.",
   "Waltersdorf: pastors, school (59 pupils), free estate and its owners, municipal finances, occupations (masons, dealers), poverty and overland carting, field area 1509.54 Morgen with soil and fruit growing.",
   ["Waltersdorf", "Schule", "Freigut", "Gemeindefinanzen", "Maurer", "Landfuhrwesen", "Flur", "Berufe", "Pfarrer"], ["Waltersdorf", "school", "free estate", "municipal finances", "masons", "carting trade", "field area", "occupations", "pastors"], ["Dorf", "Schule", "Gemeindefinanzen", "Berufe"])
pg("466", "Schluss von Waltersdorf (Flurnamen, Geschichte seit 1288, Cronswitz, Brand 1750 durch die St. Gangloffer Räuberbande, Kriegsleiden, Sagen); Kleinsaara, Dörfchen 1 ¾ Stunde westsüdwestlich von Gera: Lage, Häuser, 143 Einwohner, Vieh.",
   "End of Waltersdorf (field names, history since 1288, Cronswitz, fire of 1750 set by the St. Gangloff robber band, war hardships, legends); Kleinsaara, a small village one and three quarter hours west-southwest of Gera: location, houses, 143 inhabitants, livestock.",
   ["Waltersdorf", "Kleinsaara", "Räuberbande", "Brand 1750", "Cronswitz", "Flurnamen", "Dreißigjähriger Krieg", "Sagen", "Pest"], ["Waltersdorf", "Kleinsaara", "robber band", "fire of 1750", "Cronswitz", "field names", "Thirty Years' War", "legends", "plague"], ["Dorf", "Brände", "Kriminalität", "Sagen"])
pg("467", "Schluss von Kleinsaara (Vorwerk, Gemeindefinanzen, Berufe, Flur 662 3/10 Morgen, Erschießung 1640); Großsaara, Kirch- und Pfarrdorf 1 ½ Stunde südsüdwestlich von Gera: Lage, Häuser, 296 Einwohner, Vieh, ehemalige Herrnburg.",
   "End of Kleinsaara (outlying farm, municipal finances, occupations, field area 662 3/10 Morgen, shooting of 1640); Großsaara, a parish village one and a half hours south-southwest of Gera: location, houses, 296 inhabitants, livestock, former castle seat.",
   ["Kleinsaara", "Großsaara", "Vorwerk", "Herrnburg", "Gemeindefinanzen", "Sandstein", "Flur", "Saarbach", "Pfarrdorf"], ["Kleinsaara", "Großsaara", "outlying farm", "castle seat", "municipal finances", "sandstone", "field area", "Saar brook"], ["Dorf", "Rittergut", "Gemeindefinanzen"])
pg("468", "Großsaara: Kammergut als ehemalige Burg mit Besitzerfolge (v. Beulwitz, v. Wolframsdorf, v. Koppy, Heinrich XXX.), Kirche (15. Jahrhundert, 1734, 1863), Glocken, Pfarrer, Pfarrhaus 1844, Schule (65 Kinder), Gasthaus und Mühle, Gemeindeschulden.",
   "Großsaara: crown estate as former castle with succession of owners (von Beulwitz, von Wolframsdorf, von Koppy, Heinrich XXX), church (15th century, 1734, 1863), bells, pastors, parsonage of 1844, school (65 children), inn and mill, municipal debts.",
   ["Großsaara", "Kammergut", "Burg", "Kirche", "Glocken", "Pfarrer", "Schule", "Mühle", "Kirchbauschulden"], ["Großsaara", "crown estate", "castle", "church", "bells", "pastor", "school", "mill", "church-building debts"], ["Dorf", "Kammergut", "Kirchengebäude", "Schule"])
pg("469", "Schluss von Großsaara (Berufe, Flur 1253 2/5 Morgen, Geschichte, Brand 1840); Geißen, Kirchdörfchen und Filial von Großsaara: Namensformen, Lage, Häuser, 116 Einwohner, Vieh, Kirche mit Glocken und Altarschnitzwerk.",
   "End of Großsaara (occupations, field area 1253 2/5 Morgen, history, fire of 1840); Geißen, a small church village and branch of Großsaara: name forms, location, houses, 116 inhabitants, livestock, church with bells and carved altarpiece.",
   ["Großsaara", "Geißen", "Filialkirche", "Altarschnitzwerk", "Glocken", "Berufe", "Flur", "Einwohner", "Kirchdörfchen"], ["Großsaara", "Geißen", "branch church", "carved altarpiece", "bells", "occupations", "field area", "inhabitants"], ["Dorf", "Kirchengebäude", "Berufe"])
pg("470", "Schluss von Geißen (Schule, Mühlen, Gemeindefinanzen, Berufe, Flur 1424 Morgen, erste Erwähnung 1121); Langengrobsdorf, Dörfchen im Langenthal: Lage, 77 Einwohner, Vieh, Schule und Kirche in Geißen, Gemeindefinanzen.",
   "End of Geißen (school, mills, municipal finances, occupations, field area 1424 Morgen, first mention 1121); Langengrobsdorf, a small village in the Langenthal: location, 77 inhabitants, livestock, school and church at Geißen, municipal finances.",
   ["Geißen", "Langengrobsdorf", "Schule", "Mühlen", "Gemeindefinanzen", "Bosau", "Flur", "Berufe", "Ersterwähnung 1121"], ["Geißen", "Langengrobsdorf", "school", "mills", "municipal finances", "Bosau", "field area", "occupations"], ["Dorf", "Gemeindefinanzen", "Mühlen"])
pg("471", "Schluss von Langengrobsdorf (Berufe, Flur 763,59 Morgen, Namensdeutung); Windischenbernsdorf, Langdörfchen im Saartal: Lage, 254 Einwohner, Vieh, Pfarr- und Schulzugehörigkeit zu Frankenthal, Gemeindefinanzen, ehemaliges Rittergut.",
   "End of Langengrobsdorf (occupations, field area 763.59 Morgen, name etymology); Windischenbernsdorf, a long village in the Saar valley: location, 254 inhabitants, livestock, parish and school affiliation with Frankenthal, municipal finances, former manor.",
   ["Langengrobsdorf", "Windischenbernsdorf", "Frankenthal", "Rittergut", "Gemeindefinanzen", "Flur", "Namensdeutung", "Taglöhner", "Saartal"], ["Langengrobsdorf", "Windischenbernsdorf", "Frankenthal", "manor", "municipal finances", "field area", "name etymology", "day labourers"], ["Dorf", "Gemeindefinanzen", "Ortsname"])
pg("472", "Schluss von Windischenbernsdorf (Taglöhner in Gera, Flur 600 5/6 Morgen, Geschichte, Hinrichtung 1618); Scheubengrobsdorf, Dörfchen im Saartal mit Rittergut: Lage, 221 Einwohner, Vieh, Frankenthal als Pfarr- und Schulort, Besitzer des Guts.",
   "End of Windischenbernsdorf (day labourers in Gera, field area 600 5/6 Morgen, history, execution of 1618); Scheubengrobsdorf, a small village in the Saar valley with a manor: location, 221 inhabitants, livestock, Frankenthal as parish and school place, owners of the estate.",
   ["Windischenbernsdorf", "Scheubengrobsdorf", "Rittergut", "Taglöhner", "Flur", "Frankenthal", "Besitzer", "Hinrichtung 1618", "Saartal"], ["Windischenbernsdorf", "Scheubengrobsdorf", "manor", "day labourers", "field area", "Frankenthal", "owners", "execution 1618"], ["Dorf", "Rittergut", "Berufe"])
pg("473", "Schluss von Scheubengrobsdorf (Gutsbesitzer 1683–1867, Gemeindefinanzen, Berufe, Flur 936 1/2 Morgen, Bergsturz 1771); Beginn von Frankenthal, volkreiches Langdorf mit Rittergut: Lage, Häuser, 689 Einwohner, Vieh, Rittergut.",
   "End of Scheubengrobsdorf (estate owners 1683-1867, municipal finances, occupations, field area 936 1/2 Morgen, hillside collapse of 1771); start of Frankenthal, a populous long village with a manor: location, houses, 689 inhabitants, livestock, manor.",
   ["Scheubengrobsdorf", "Frankenthal", "Rittergut", "Gemeindefinanzen", "Flur", "Bergsturz", "Langdorf", "Einwohner", "Vieh"], ["Scheubengrobsdorf", "Frankenthal", "manor", "municipal finances", "field area", "landslide", "long village", "inhabitants"], ["Dorf", "Rittergut", "Gemeindefinanzen"])
pg("474", "Frankenthal: Rittergut und Besitzer, Kirche (1728–1732, Turm 1736, Orgel 1749), Kapellen der Gutsherren, Parochie mit eingepfarrten Orten (1720 Seelen), Visitation 1533, Pfarrer und Pfarreieinkommen, Pfarrwohnung.",
   "Frankenthal: manor and owners, church (1728-1732, tower 1736, organ 1749), chapels of the estate lords, parish with incorporated places (1,720 souls), visitation of 1533, pastors and parish income, parsonage.",
   ["Frankenthal", "Rittergut", "Kirche", "Parochie", "Pfarrer", "Pfarreieinkommen", "Visitation 1533", "Gutskapellen", "Pottendorf"], ["Frankenthal", "manor", "church", "parish", "pastor", "parish income", "visitation of 1533", "estate chapels", "Pottendorf"], ["Dorf", "Kirchengebäude", "Pfarreien", "Rittergut"])
pg("475", "Frankenthal: Schule (307 Kinder), Gemeindefinanzen, Berufe (Häusler, Taglöhner, Maurer- und Zimmergesellen), Armut, Diebsbande 1816–1819, Flur 791,54 Morgen, Ortsgeschichte (Verwüstung im 30jährigen Krieg, Ruhr 1772).",
   "Frankenthal: school (307 children), municipal finances, occupations (smallholders, day labourers, journeymen masons and carpenters), poverty, thieves' band 1816-1819, field area 791.54 Morgen, local history (devastation in the Thirty Years' War, dysentery 1772).",
   ["Frankenthal", "Schule", "Armut", "Taglöhner", "Diebsbande", "Gemeindefinanzen", "Flur", "Dreißigjähriger Krieg", "Ruhr"], ["Frankenthal", "school", "poverty", "day labourers", "thieves' band", "municipal finances", "field area", "Thirty Years' War", "dysentery"], ["Dorf", "Schule", "Kriminalität", "Gemeindefinanzen"])
pg("476", "Schluss von Frankenthal (Sage); Thieschitz, Kirch- und Pfarrdörfchen 1 ⅛ Stunde nordwestlich von Gera: Lage, Häuser, 129 Einwohner, Vieh, Kirche (Rubitz und Milbitz eingepfarrt), Pfarrer Mackroth als Mineraloge, Schule (66 Kinder).",
   "End of Frankenthal (legend); Thieschitz, a small parish village one and an eighth hours northwest of Gera: location, houses, 129 inhabitants, livestock, church (Rubitz and Milbitz incorporated), pastor Mackroth as mineralogist, school (66 children).",
   ["Frankenthal", "Thieschitz", "Kirche", "Pfarrer Mackroth", "Mineraliensammlung", "Rubitz", "Milbitz", "Schule", "Patronat"], ["Frankenthal", "Thieschitz", "church", "pastor Mackroth", "mineral collection", "Rubitz", "Milbitz", "school", "patronage"], ["Dorf", "Pfarreien", "Gesteine und Mineralien"])
pg("477", "Schluss von Thieschitz (Gemeindefinanzen, Gewerbe, Gips- und Kalkgewinnung, Flur 665 1/4 Morgen, Gerichtsverhältnisse); Beginn von Milbitz, Bauerndörfchen 1 Stunde nordwestlich von Gera in der Elsteraue: Lage, 81 Einwohner, Vieh, Gemeindefinanzen, Berufe.",
   "End of Thieschitz (municipal finances, trades, gypsum and lime extraction, field area 665 1/4 Morgen, jurisdiction); start of Milbitz, a small farming village one hour northwest of Gera in the Elster plain: location, 81 inhabitants, livestock, municipal finances, occupations.",
   ["Thieschitz", "Milbitz", "Gips", "Kalk", "Gemeindefinanzen", "Flur", "Erlbach", "Salzquellen", "Bauerndorf"], ["Thieschitz", "Milbitz", "gypsum", "lime", "municipal finances", "field area", "Erlbach", "salt springs", "farming village"], ["Dorf", "Gesteine und Mineralien", "Gemeindefinanzen"])

G.append({"term": "Kirchenspannhof", "variants": ["Kirchenspannhöfe", "Spannhof"], "kind": "term", "de": "Bauernhof mit Gespann, der zu Fuhren für Kirche und Pfarrei verpflichtet ist.", "en": "Farm with a draught team obliged to carry out carting services for the church and parsonage.", "pages": ["464"]})
G.append({"term": "Erbkretschmar", "variants": ["Erbkretscham", "Erbschenke"], "kind": "term", "de": "Erbliche Schankwirtschaft (Dorfgasthof) mit eigener Gerechtigkeit.", "en": "Hereditary tavern (village inn) with its own licence.", "pages": ["457", "468", "471", "475", "480"]})
G.append({"term": "Rittergut", "variants": ["Rittersitz"], "kind": "institution", "de": "Adliges Gut mit Gerichts- und Lehnsrechten über den Ort (Patrimonialgerichtsbarkeit, Kirchenpatronat), in den Ortsartikeln stets mit Besitzerfolge genannt.", "en": "Noble estate with jurisdiction and feudal rights over the village (patrimonial justice, church patronage), regularly described with its owners in the village articles.", "pages": ["424", "450", "452", "456", "473"]})
G.append({"term": "Ephorie", "variants": [], "kind": "institution", "de": "Kirchlicher Aufsichtsbezirk eines Superintendenten (Ephorus).", "en": "Ecclesiastical supervisory district of a superintendent (ephorus).", "pages": ["437", "445"]})
G.append({"term": "Gerichtsbarkeit", "variants": ["Obergerichte", "Niedergerichte", "Erbgerichte", "Lehn"], "kind": "term", "de": "In den Ortsartikeln unterschieden: Obergerichte (landesherrlich), Nieder- bzw. Erbgerichte und Lehn (beim Rittergut oder Amt).", "en": "Distinguished in the village articles: higher jurisdiction (held by the sovereign), lower or hereditary jurisdiction and fiefs (with the manor or the district office).", "pages": ["456", "459", "461", "465"]})
G.append({"term": "Pferdebauer", "variants": ["Pferdebauern", "Kühbauer"], "kind": "term", "de": "Bauer, der mit Pferden bzw. mit Kühen anspannt; Hinweis auf Größe des Hofs.", "en": "Farmer who ploughs with horses or with cows respectively; an indicator of farm size.", "pages": ["462", "463"]})
