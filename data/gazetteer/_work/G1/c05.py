# -*- coding: utf-8 -*-
E = []
P = []
G = []

def pg(page, de, en, kde, ken, subj):
    P.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

E.append({
    "id": "milbitz",
    "name": "Milbitz",
    "start": {"page": "477", "block": "b2"},
    "end": {"page": "478", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Bauerndörfchen im Halbrund",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Mylwitz", "year": 1533}, {"form": "Mulbiß", "year": None}],
    "dialect_form": "Milbtz",
    "first_mention_year": 1533,
    "location": {"verbatim": "1 Stunde NW. von Gera, an der Straße von da nach Kraftsdorf, Tinz gegenüber, in der Thalsohle der Elster", "relative_to": "Gera", "distance_hours": 1, "direction": "NW"},
    "elevation": {"value": 500, "unit": "Fuß", "verbatim": "500 Fuß hoch, aber eben gelegen"},
    "parish": {"status": "eingepfarrt", "church_of": "Thieschitz", "verbatim": "Von jeher pfarrt, begräbt und schult der Ort (jetzt mit 11 Kindern) nach dem ganz nahen Thieschütz"},
    "school": {"exists": False, "pupils": 11, "note": "schult nach Thieschitz"},
    "houses": 10,
    "inhabitants": 81,
    "occupations": {"Bauern": 8, "Häusler": 1, "Dienstboten": 12, "Kapitalisten": 2},
    "crafts": {"Maurer": 1, "Tischler": 1},
    "flur_morgen": 496.18,
    "flur_verbatim": "496,18 Morgen",
    "soil": "an 3/4 guter Boden, fruchtbarer Wiesengrund",
    "livestock": {"Pferde": 17, "Rinder": 75, "Schafe": 258, "Schweine": 62, "Ziegen": 3, "Gänse": 60, "Bienenstöcke": 19},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 1 Ortsbeamten besitzt als engere einige Grundstücke im Werthe von 2000 Thlr., als weitere 400 Thlr. Schulden; ihre Jahresausgabe macht 130 Thlr. für Anstalten, 1 Communications- und 1 steinerne Brücke (seither Vicinal-Stegweg) über die Elster", "assets_thaler": 2000, "debts_thaler": 400, "expenditure_thaler": 130},
    "facilities": ["Gemeindehaus", "Privatgasthof", "Ziegelei", "steinerne Elsterbrücke", "Kalksteinbrüche"],
    "subplaces": [{"name": "Zwerghöhlen", "kind": "Sonstiges", "page": "478"}],
    "events": [
        {"year": 1799, "event_de": "Hochwasser der Elster im Februar beschädigt mehrere Gebäude", "event_en": "Flood of the Elster in February damages several buildings"}
    ],
    "notes": "1 Gemeindehaus und 10 Privathäuser mit 9 Scheunen; 13 Familien; 1861: 77 Einwohner; 9 Bauerngüter, 1 Grundstücksverband, 3 Pertinenzstücke, 24 ledige Grundstücke; 8 Bauern der Pfarrei Thieschitz decempflichtig; Feuerspritze in Thieschitz gemeinsam mit Rubitz; Amtslehn; 8 Kalksteinbrüche; sorbischen Ursprungs (nicht mit den zwei rudolstädter Dörfern Milbitz zu verwechseln); Sage von den Zwerghöhlen (Schaumkalk als Erstfundort).",
    "summary_de": "Milbitz, Bauerndörfchen im Halbrund in der Elsteraue 1 Stunde nordwestlich von Gera, nach Thieschitz gepfarrt und geschult (11 Kinder); 81 Einwohner, wohlhabende Bauern mit Viehzucht, Ziegelei, Flur 496,18 Morgen mit Wiesengrund und Kalksteinbrüchen, Sage vom Zwergvolk der Zwerghöhlen.",
    "summary_en": "Milbitz, a small farming village laid out in a half circle in the Elster plain one hour northwest of Gera, in the parish and school district of Thieschitz (11 children); 81 inhabitants, prosperous cattle farmers, brickworks, field area 496.18 Morgen with meadows and limestone quarries, the legend of the dwarf folk of the Zwerghöhlen."
})

E.append({
    "id": "rubitz",
    "name": "Rubitz",
    "start": {"page": "478", "block": "b2"},
    "end": {"page": "479", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "halbrundliches Dorf in freundlicher Lage",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Rupizan", "year": 1121}, {"form": "Ropizane", "year": 1146}, {"form": "Robicz", "year": None}, {"form": "Robitz", "year": 1488}, {"form": "Drobitz", "year": None}, {"form": "Drowitz", "year": None}],
    "dialect_form": "Rubz",
    "first_mention_year": 1121,
    "location": {"verbatim": "1/8 Stunde südwestlich von Thieschitz, von der Straße von Gera nach Kraftsdorf durchschnitten", "relative_to": "Thieschitz", "distance_hours": 0.125, "direction": "SW"},
    "parish": {"status": "eingepfarrt", "church_of": "Thieschitz", "verbatim": "Rubitz pfarrt, begräbt und schult von jeher, jetzt mit 43 Kindern, nach Thieschitz"},
    "school": {"exists": False, "pupils": 43, "note": "schult nach Thieschitz"},
    "houses": 28,
    "inhabitants": 225,
    "occupations": {"Bauern": 10, "Häusler": 13, "Taglöhner": 20, "Dienstboten": 13, "Kapitalisten": 2, "Almosenarme": 2},
    "crafts": {"Zimmerer": 3, "Maurer": 2, "Schuhmacher": 2, "Fleischer": 1, "Korbmacher": 1, "Müller": 1, "Schmied": 1, "Schneider": 1, "Wagner": 1, "Weber": 1},
    "flur_morgen": 1080.6,
    "flur_verbatim": "1080 3/5 Morgen",
    "soil": "Feld zu je 1/3 gut, mittel und gering",
    "livestock": {"Pferde": 12, "Rinder": 93, "Schafe": 272, "Schweine": 69, "Ziegen": 6, "Bienenstöcke": 6},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Ortsbeamten hat als engere einen Grundbesitz von circa 400 Thlr. Werth, als weitere 150 Thlr. Schulden und jährlich eine Ausgabe von 200 Thlr. für öffentliche Anstalten und 2 Vicinalwege", "assets_thaler": 400, "debts_thaler": 150, "expenditure_thaler": 200},
    "facilities": ["Rittergut", "Gemeindearmenhaus", "Gemeindebrauhaus", "Gemeindeschenke", "Mahlmühle", "Schneidemühle", "Lohmühle", "Gypsbruch", "Kalksteinbruch"],
    "subplaces": [
        {"name": "Rittergut Rubitz", "kind": "Rittergut", "page": "478"},
        {"name": "Cosse (nördliche Häuser)", "kind": "Sonstiges", "page": "478"},
        {"name": "Mühle Rubitz", "kind": "Mühle", "page": "478"}
    ],
    "events": [
        {"year": 1121, "event_de": "Naumburger Bischof Dietrich eignet dem Kloster Bosau 19 Scobronengrundstücke zu", "event_en": "Bishop Dietrich of Naumburg assigns 19 Scobron plots to Bosau convent"},
        {"year": 1620, "event_de": "Rittergut kommt um 1620 an die Familie v. Biesenroth", "event_en": "Manor passes to the von Biesenroth family around 1620"},
        {"year": 1817, "event_de": "Brand der Cossen-Häuser", "event_en": "Fire in the Cossen houses"},
        {"year": 1853, "event_de": "Drei Bauernhöfe brennen im August ab", "event_en": "Three farms burn down in August"},
        {"year": 1866, "event_de": "Das Rittergut wird Kammergut", "event_en": "The manor becomes a crown estate"}
    ],
    "persons": ["Familie v. Uttenhoven", "Familie v. Biesenroth"],
    "notes": "1 Gemeindearmenhaus, 1 Gemeindebrauhaus und mit dem Rittergute 28 Privathäuser mit 13 Scheunen und 25 Höfen; 47 Familien; 1861: 190 Einwohner; Gänse im Druck '30-40'; 12 kleine Bauerngüter (alle unter 40 Morgen), 2 Pertinenzstücke, 29 ledige Grundstücke neben dem Rittergutsareal; Flur 41/100 Wald, 40/100 Feld, 11/100 Wiesen, 8/100 Dorfraum, Gärten und Hut; 1/3 der Einwohner bemittelt; Zuständigkeit der Pfarrei Thieschitz für ein Haus und Gut (Lehn); Gewinnung von Düngergyps; sorbische Ansiedlung, ehemals Pflege Langenberg; Sage von zwei Rittern.",
    "summary_de": "Rubitz, halbrundes Dorf im unteren Erlbachsgrund, ⅛ Stunde südwestlich von Thieschitz, nach Thieschitz gepfarrt und geschult (43 Kinder); Rittergut (Besitzer v. Schauroth, v. Uttenhoven, v. Biesenroth; seit 1866 Kammergut), 225 Einwohner, Mühle, Gipsgewinnung, Flur 1080 3/5 Morgen mit viel Wald.",
    "summary_en": "Rubitz, a village laid out in a half circle in the lower Erlbach valley, an eighth hour southwest of Thieschitz, in the parish and school district of Thieschitz (43 children); manor (owners von Schauroth, von Uttenhoven, von Biesenroth; crown estate since 1866), 225 inhabitants, mill, gypsum extraction, field area 1080 3/5 Morgen with much forest."
})

E.append({
    "id": "texdorf",
    "name": "Texdorf",
    "start": {"page": "479", "block": "b2"},
    "end": {"page": "479", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "Die Wüstung Texdorf",
    "type": "Wüstung",
    "wuestung": True,
    "location": {"verbatim": "in der Flur von Rubitz auf der südöstlichen Berghöhe"},
    "facilities": ["herrschaftlicher Walddistrict"],
    "notes": "Im Ortsregister (S. 826-829) lautet der Name 'Terdorf'; im Druck der Artikelüberschrift 'Texdorf' (Fraktur x). Auch 418 und 419 ('Texdorf' als Flurstück in Ernsee) nennen den Namen.",
    "summary_de": "Wüstung Texdorf in der Flur von Rubitz, jetzt herrschaftlicher Walddistrict; angeblich gleichzeitig mit dem Kirchenort Pottendorf untergegangen, Ackerfurchen im Wald erkennbar.",
    "summary_en": "Deserted settlement of Texdorf in the field area of Rubitz, now a princely forest district; reportedly abandoned at the same time as the church site of Pottendorf, field furrows still visible in the forest."
})

E.append({
    "id": "toeppeln",
    "name": "Töppeln",
    "start": {"page": "479", "block": "b3"},
    "end": {"page": "480", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "eben, mild und angenehm gelegenes Thaldorf mit einem Rittergute",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Topelin", "year": 1333}, {"form": "Tepiln", "year": None}, {"form": "Doppiln", "year": 1533}],
    "dialect_form": "Teppeln",
    "first_mention_year": 1333,
    "location": {"verbatim": "1 1/2 Stunde WNW. von Gera, an der Straße von da nach Kraftsdorf", "relative_to": "Gera", "distance_hours": 1.5, "direction": "WNW"},
    "parish": {"status": "eingepfarrt", "church_of": "Frankenthal", "verbatim": "Der Ort pfarrt, begräbt und schult, jetzt mit 37 Kindern, nach Frankenthal, war aber in früherer Zeit mit der Kirche in Pottendorf in Verband"},
    "school": {"exists": False, "pupils": 37, "note": "schult nach Frankenthal"},
    "houses": 43,
    "inhabitants": 244,
    "occupations": {"Bauern": 5, "Häusler und Taglöhner": 35, "Dienstboten": 25, "Kapitalisten": 1, "Almosenarme": 2},
    "crafts": {"Maurergesellen": 9, "Zimmergesellen": 6, "Schuhmacher": 3, "Müller": 2, "Schneider": 2, "Bäcker": 1, "Fleischer": 1, "Schlosser": 1, "Weber": 1, "Ziegler": 1},
    "flur_morgen": 679.72,
    "flur_verbatim": "679 13/18 Morgen",
    "soil": "über die Hälfte ergiebig, für Weizen und Klee vorzüglich",
    "livestock": {"Pferde": 14, "Rinder": 75, "Schafe": 253, "Schweine": 60, "Ziegen": 15, "Gänse": 100, "Bienenstöcke": 20},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Ortsbeamten hat statt Vermögen 400 Thlr. Schulden und eine Jahresausgabe von 150 Thlr. zur Erhaltung der frankenthaler Cultgebäude, des Gemeindehauses, 1 Feuerspritze und 3 Communicationswege", "debts_thaler": 400, "expenditure_thaler": 150},
    "facilities": ["Rittergut", "Gemeindehaus", "Spritzenhaus", "Privatwirthshaus", "Obermühle", "Untermühle", "Ziegelei", "Feuerspritze"],
    "subplaces": [
        {"name": "Rittergut Töppeln", "kind": "Rittergut", "page": "480"},
        {"name": "Obermühle", "kind": "Mühle", "page": "480"},
        {"name": "Untermühle", "kind": "Mühle", "page": "480"},
        {"name": "Steinhaus (Kemnate)", "kind": "Sonstiges", "page": "480"}
    ],
    "events": [
        {"year": 1370, "event_de": "Aus dem Jahr 1370 stammt das alte Steinhaus (Kemnate) der Ritter- und Zwingburg", "event_en": "The old stone house (Kemnate) of the former castle dates from 1370"},
        {"year": 1518, "event_de": "Die v. Ende besitzen das Rittergut von 1518 bis um 1670", "event_en": "The von Ende family holds the manor from 1518 until about 1670"},
        {"year": 1564, "event_de": "Der Pfarrer von Frankenthal begleitet einen Delinquenten zum Hochgericht", "event_en": "The pastor of Frankenthal accompanies a delinquent to the gallows"},
        {"year": 1805, "event_de": "Familie Oberländer kauft das Rittergut für 45,000 Thlr.", "event_en": "The Oberländer family buys the manor for 45,000 thalers"},
        {"year": 1809, "event_de": "Seitengebäude des Ritterguts brennen ab", "event_en": "Outbuildings of the manor burn down"},
        {"year": 1862, "event_de": "Untermühle bis 1862 Papiermühle", "event_en": "The lower mill was a paper mill until 1862"}
    ],
    "persons": ["Familie v. Ende", "Familie Oberländer"],
    "notes": "1 Gemeinde- und 1 Spritzenhaus und mit Einschluß des Ritterguts 43 Privathäuser mit 18 Scheunen und 38 Höfen; 46 Familien; 1861: 217 Einwohner; im Druck 'K.' statt 'R.' bei den Rindern (75 K.); Rittergut mit fast 3/4 der Flur und Patronat über Kirche und Schule Frankenthal im Wechsel mit Scheubengrobsdorf; 5 geringe Güter und 13 ledige Grundstücke; Wollkämmerei und Handspinnerei durch Gera eingegangen; 8 Familien bauen ihr Jahresbrod; 1 geistesschwache Person; Flur: 2 Teiche, 2 Kalksteinbrüche, 1 Lehmgrube; sorbischer Anbau, früher zur Pflege Langenberg.",
    "summary_de": "Töppeln, Thaldorf mit Rittergut 1 ½ Stunden westnordwestlich von Gera an der Straße nach Kraftsdorf: Rittergut mit steinernem Kemnatenhaus von 1370 und Besitzerfolge, nach Frankenthal gepfarrt und geschult, 244 Einwohner, Handwerker und Taglöhner, Mühlen und Ziegelei, Flur 679 13/18 Morgen.",
    "summary_en": "Töppeln, a valley village with a manor one and a half hours west-northwest of Gera on the Kraftsdorf road: manor with a stone 'Kemnate' house of 1370 and its succession of owners, in the parish and school district of Frankenthal, 244 inhabitants, craftsmen and day labourers, mills and brickworks, field area 679 13/18 Morgen."
})

E.append({
    "id": "muehlsdorf",
    "name": "Mühlsdorf",
    "start": {"page": "481", "block": "b1"},
    "end": {"page": "482", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "hoch, frei und zugig gelegenes Kirchdörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Milensdorf", "year": 1330}, {"form": "Mülstorff", "year": 1533}],
    "dialect_form": "Mülsdorf",
    "first_mention_year": 1330,
    "location": {"verbatim": "1 1/2 Stunde WNW. von Gera, auf einem kahlen, waldentblößten Bergrücken", "relative_to": "Gera", "distance_hours": 1.5, "direction": "WNW"},
    "elevation": {"value": 775, "unit": "Fuß", "verbatim": "in der Dorfmitte 775 Fuß über dem Meere"},
    "parish": {"status": "Filial", "church_of": "Frankenthal", "verbatim": "sicher aber ist, daß die Reformation sie als Filial von Frankenthal vorfand, das sie seitdem geblieben ist"},
    "school": {"exists": True, "pupils": 31},
    "houses": 32,
    "inhabitants": 176,
    "occupations": {"Bauern": 17, "Häusler": 13, "Taglöhner": 6, "Dienstboten": 11},
    "crafts": {"Instrumentenmacher": 1, "Schmied": 1, "Wagner": 1, "Weber": 1},
    "flur_morgen": 741.5,
    "flur_verbatim": "741 1/2 Morgen",
    "soil": "5/6 mittelgut, 1/6 gering",
    "livestock": {"Pferde": 9, "Rinder": 101, "Schafe": 82, "Schweine": 81, "Ziegen": 12, "Gänse": 151, "Bienenstöcke": 10},
    "municipal_finances": {"verbatim": "Die Gemeinde hat als engere circa 13 Morgen Grundbesitz im Werthe von 1400 Thlr., als weitere 950 Thlr. Schulden und jährlich 150 bis 200 Thlr. Ausgaben für die Communalbauten, 1 Dorfstraße, 2 Communications- und 3 Vicinalwege", "assets_thaler": 1400, "debts_thaler": 950, "expenditure_thaler_min": 150, "expenditure_thaler_max": 200},
    "facilities": ["Rittergut", "Schäferei", "Kirche", "Schule", "Gemeindehaus", "Privatwirthshaus", "Friedhof"],
    "subplaces": [{"name": "Rittergut Mühlsdorf", "kind": "Rittergut", "page": "481"}],
    "events": [
        {"year": 1330, "event_de": "Heinrich v. Gera verkauft Zinsen im Ort dem Kloster Cronswitz", "event_en": "Heinrich of Gera sells dues in the village to Cronswitz convent"},
        {"year": 1708, "event_de": "Erster bekannter Lehrer Gundermann (ab 1701) geht weg, weil er mitfrohnen musste", "event_en": "The first known teacher Gundermann (from 1701) leaves because he had to share in compulsory labour"},
        {"year": 1736, "event_de": "Kirche auf der Stelle des früheren Kirchleins neu gebaut; Inneres 1785 ausgeschmückt", "event_en": "Church rebuilt on the site of the earlier chapel; interior decorated in 1785"},
        {"year": 1822, "event_de": "Schulhaus erbaut", "event_en": "School house built"},
        {"year": 1735, "event_de": "Geburt von J. Gottfried Fischer, später geadelter Leibarzt Kaiser Josephs II.", "event_en": "Birth of J. Gottfried Fischer, later ennobled personal physician of Emperor Joseph II"}
    ],
    "persons": ["J. Gottfried Fischer", "Gundermann"],
    "notes": "1 Kirche, Schule, Gemeindehaus und sammt dem Rittergute 32 Privathäuser mit 24 Höfen und Scheunen; 35 Familien; 1861: 192 Einwohner; 17 Güter, 2 Grundstücksverbände, 36 ledige Grundstücke neben dem Rittergutsareal; Rittergut: Familie von Ende auf Töppeln, jetzt Familie Kretzschmar; Kirchenvermögen 160 Thlr., Bücher seit 1650; zum Pfarrbau in Frankenthal trägt der Ort 1/4 bei; Bevölkerungsrückgang seit 1680 nur 3 Häuser Zuwachs; sorbischer Ursprung.",
    "summary_de": "Mühlsdorf, hoch gelegenes Kirchdörfchen 1 ½ Stunden westnordwestlich von Gera: Rittergut, Kirche (1736) als Filial von Frankenthal, Schule (31 Kinder), 176 Einwohner, überwiegend Bauern, Flur 741 1/2 Morgen, Geburtsort des Leibarztes Joseph Gottfried Fischer; Ersterwähnung 1330.",
    "summary_en": "Mühlsdorf, a church village in an exposed high position one and a half hours west-northwest of Gera: manor, church (1736) as a branch of Frankenthal, school (31 children), 176 inhabitants, mostly farmers, field area 741 1/2 Morgen, birthplace of the physician Joseph Gottfried Fischer; first mentioned in 1330."
})

E.append({
    "id": "cosse",
    "name": "Cosse",
    "start": {"page": "482", "block": "b2"},
    "end": {"page": "482", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "Die Wüstung Cosse",
    "type": "Wüstung",
    "wuestung": True,
    "location": {"verbatim": "ostnordöstlich von Mühlsdorf", "relative_to": "Mühlsdorf", "direction": "ONO"},
    "notes": "Bergdistrict, an dem Mühlsdorf, Thieschitz und Rubitz Anteil haben; jede Spur der Stätte verschwunden, die Geschichte nennt den Ort nicht. In der Transkription an Flurnamen-Stellen (476, 481) als 'Coffe' wiedergegeben.",
    "summary_de": "Wüstung Cosse, ein Bergdistrikt östlich-nordöstlich von Mühlsdorf zwischen Thieschitz und Hartmannsdorf, an dem Mühlsdorf, Thieschitz und Rubitz Anteil haben; der Ort muss früh wüst geworden sein, von ihm ist nichts überliefert.",
    "summary_en": "Deserted settlement of Cosse, a hill district east-northeast of Mühlsdorf between Thieschitz and Hartmannsdorf, shared by Mühlsdorf, Thieschitz and Rubitz; it must have been abandoned early, and nothing is recorded about it."
})

E.append({
    "id": "poersdorf",
    "name": "Pörsdorf",
    "start": {"page": "482", "block": "b3"},
    "end": {"page": "483", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "kleines Plateau-, Kirch- und Bauerndorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Porßdorf", "year": None}, {"form": "Bersdorf", "year": 1647}],
    "dialect_form": "Pörschdorf",
    "location": {"verbatim": "2 1/4 Stunde WNW. von Gera, außerhalb des Straßenverkehrs, auf der Höhenmulde eines Bergrückens", "relative_to": "Gera", "distance_hours": 2.25, "direction": "WNW"},
    "parish": {"status": "Filial", "church_of": "Rüdersdorf", "verbatim": "Die hiesige Kirche, ein Filial von Rüdersdorf"},
    "school": {"exists": False, "note": "Schule in Rüdersdorf"},
    "houses": 25,
    "inhabitants": 138,
    "occupations": {"Bauern": 23, "Häusler": 10, "Taglöhner": 2, "Dienstboten": 19, "Kapitalisten": 2},
    "crafts": {"Maurer": 2, "Schneider": 1, "Schuhmacher": 1, "Zimmermann": 1},
    "flur_morgen": 888.2,
    "flur_verbatim": "888 1/5 Morgen",
    "soil": "halb mittelgut, halb gering, doch gut gepflegt",
    "livestock": {"Pferde": 8, "Rinder": 114, "Schafe": 130, "Schweine": 68, "Ziegen": 8, "Gänse": 180, "Bienenstöcke": 20},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere 6 Acker Obstpflanzung und Hutung im Werthe von 600 Thlr., als weitere weder Activa noch Passiva", "assets_thaler": 600, "expenditure_thaler": 100},
    "facilities": ["Kirche", "Gemeindehaus", "Hirtenhaus", "Brauhaus", "Schenke", "Friedhof"],
    "subplaces": [
        {"name": "Vicarei", "kind": "Sonstiges", "page": "482"},
        {"name": "der Hof", "kind": "Sonstiges", "page": "483"}
    ],
    "events": [
        {"year": 1647, "event_de": "Theilungsacten: Bersdorf als Filial von Rüdersdorf", "event_en": "Partition records: Bersdorf as a branch of Rüdersdorf"},
        {"year": 1660, "event_de": "Nach dem 30jährigen Krieg nur 3 ganze und 2 halbe Pferdefrohngüter, 4 Handfrohngüter und 6 Kleinhäusler, circa 68 Seelen", "event_en": "After the Thirty Years' War only 3 full and 2 half horse-service farms, 4 hand-service farms and 6 smallholdings, about 68 souls"},
        {"year": 1746, "event_de": "Recess vom 18. August: Kirche und Kirchhof altenburgisch", "event_en": "Recess of 18 August: church and churchyard Altenburg"},
        {"year": 1835, "event_de": "Kirche auf einem Teil des alten Gemäuers neu erbaut (1400 Thlr.)", "event_en": "Church rebuilt on part of the old walls (1,400 thalers)"},
        {"year": 1859, "event_de": "Neuer Recess unterstellt Kirche und kirchliche Verhältnisse der reußischen Landesherrschaft", "event_en": "New recess places the church and ecclesiastical matters under the Reuss sovereign"}
    ],
    "notes": "1 Kirche, 1 Gemeinde-, 1 Hirten- und 1 Brauhaus und 25 Privathäuser mit 23 Scheunen und 20 Höfen; 26 Familien; 1861: 146 Einwohner; Schafe (130) laut Fußnote nur 1864 (1867 keine); 18 Bauerngüter, 1 Pertinenzstück, 29 walzende Grundstücke; Kirchenvermögen 970 Thlr. und Waldstück von 5 5/6 Morgen, Bücher seit 1653; 23 Familien bauen ihr Jahresbrod; Enclavenort (altenburgisch/reußisch gemischt, Kirche bis 1859 altenburgisch); wohl sorbischer Anbau.",
    "summary_de": "Pörsdorf, kleines Plateau-, Kirch- und Bauerndorf 2 ¼ Stunden westnordwestlich von Gera abseits der Straßen: Kirche (1835) als Filial von Rüdersdorf, bis 1859 unter altenburgischem Konsistorium, 138 Einwohner, wohlhabende Bauern, Schule in Rüdersdorf, Flur 888 1/5 Morgen.",
    "summary_en": "Pörsdorf, a small plateau village with church and farming community two and a quarter hours west-northwest of Gera, away from main roads: church (1835) as branch of Rüdersdorf, under the Altenburg consistory until 1859, 138 inhabitants, prosperous farmers, school at Rüdersdorf, field area 888 1/5 Morgen."
})

E.append({
    "id": "niederndorf",
    "name": "Niederndorf",
    "start": {"page": "483", "block": "b2"},
    "end": {"page": "484", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "freundliches Kirchdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Niderindorf", "year": 1184}, {"form": "Niderndorf", "year": 1533}],
    "dialect_form": "Nidendorf",
    "first_mention_year": 1184,
    "location": {"verbatim": "2 Stunden westlich von Gera", "relative_to": "Gera", "distance_hours": 2, "direction": "W"},
    "parish": {"status": "Filial", "church_of": "Kraftsdorf", "verbatim": "hat aber auf dem Kirchberg seine eigene Kirche, die seit dem Mittelalter ein Filial von Kraftsdorf ist"},
    "school": {"exists": False, "pupils": 41, "note": "schult nach Harpersdorf"},
    "houses": 50,
    "inhabitants": 269,
    "occupations": {"Bauern": 19, "Häusler": 39, "Taglöhner": 13, "Dienstboten": 22, "Waarenhändler": 2, "Ortsarme": 10},
    "crafts": {"Maurer": 7, "Tischler": 2, "Zimmerer": 2, "Böttcher": 1, "Fleischer": 1, "Müller": 1, "Schmied": 1, "Schneider": 1, "Schuhmacher": 1, "Wagner": 1},
    "flur_morgen": 1721.44,
    "flur_verbatim": "1721 11/25 Morgen",
    "soil": "2/5 gering, 3/5 mittelgut",
    "livestock": {"Pferde": 16, "Rinder": 109, "Schafe": 300, "Schweine": 88, "Ziegen": 39, "Gänse": 40, "Bienenstöcke": 7},
    "municipal_finances": {"verbatim": "Die Gemeinde hat als engere (aus 19 Bauern bestehend) an 3 Morgen (Gräserei, Obstpflanzung und Wege) im Werthe von 200 Thlr., als weitere 25 Thlr. Schulden und eine Jahresausgabe von 125 Thlr.", "assets_thaler": 200, "debts_thaler": 25, "expenditure_thaler": 125},
    "facilities": ["Kammergut", "Kirche", "Armenhaus", "Spritzenhaus", "Privatwirthshaus", "Mühle", "Schneidemühle", "Feuerspritze"],
    "subplaces": [
        {"name": "Kammergut Niederndorf", "kind": "Kammergut", "page": "484"},
        {"name": "Mühle Niederndorf", "kind": "Mühle", "page": "484"}
    ],
    "events": [
        {"year": 1184, "event_de": "Gerwich, ein orlamündaer Vasall, besitzt das Gut; das Kloster Lausnitz erhält hier Güter", "event_en": "Gerwich, a vassal of Orlamünde, holds the estate; Lausnitz convent receives estates here"},
        {"year": 1533, "event_de": "Visitation: Niederndorf, Harpersdorf und Kaltenborn als eingepfarrte Dörfer von Kraftsdorf", "event_en": "Visitation: Niederndorf, Harpersdorf and Kaltenborn listed as villages incorporated into Kraftsdorf"},
        {"year": 1668, "event_de": "Nacht des 28. Oktober: Kirche brennt bis aufs Gemäuer ab, 1690 vollends wiederhergestellt", "event_en": "Night of 28 October: church burns down to the walls, fully restored in 1690"},
        {"year": 1740, "event_de": "Heinrich XXX. übernimmt das Gut um 1740 mit 28,000 Mk.", "event_en": "Heinrich XXX takes over the estate around 1740 for 28,000 marks"}
    ],
    "persons": ["Gerwich", "J. Donat v. Vittinghof", "Heinrich XXX."],
    "notes": "Kammergut mit Försterwohnung, 1 Kirche, 1 Armen- und 1 Spritzenhaus und 47 Privathäuser, im Ganzen 50 bewohnte Häuser mit 38 Höfen und 25 Scheunen; 58 Familien; 1861: 248 Einwohner; Kammergut mit über 864 Morgen Wald (Hart und Huldigung), Wert über 200,000 Thlr.; 9 Bauerngüter, 2 Pertinenzstücke, 38 ledige Grundstücke; Kirche alt und morsch, Altarschrein aus katholischer Zeit, Glocken 1668 und 1669, Kirchenvermögen 1270 Thlr., Bücher seit 1761; 18 Ortshandwerker; unehelichen Geburten nehmen zu; sorbische Flurnamen.",
    "summary_de": "Niederndorf, Kirchdorf 2 Stunden westlich von Gera im Erlbachsgrund: Kammergut (ehemals Rittergut, Besitzerfolge seit 1184), Kirche als Filial von Kraftsdorf (Brand 1668), 269 Einwohner, Häusler und Bauern, Schule in Harpersdorf, Flur 1721 11/25 Morgen, Gegenstück zum altenburgischen Oberndorf.",
    "summary_en": "Niederndorf, a church village two hours west of Gera in the Erlbach valley: crown estate (formerly a manor, owners since 1184), church as a branch of Kraftsdorf (fire of 1668), 269 inhabitants, smallholders and farmers, school at Harpersdorf, field area 1721 11/25 Morgen, counterpart to the Altenburg village of Oberndorf."
})

E.append({
    "id": "kaltenborn",
    "name": "Kaltenborn",
    "start": {"page": "484", "block": "b2"},
    "end": {"page": "485", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "kleines, tief eingebuchtetes, vom Straßenverkehr unberührtes Langdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Kaltenborn", "year": 1333}],
    "dialect_form": "Kalnborn",
    "first_mention_year": 1333,
    "location": {"verbatim": "2 1/4 Stunde WWS. von Gera, inmitten zwischen Harpersdorf und Großsaara", "relative_to": "Gera", "distance_hours": 2.25, "direction": "WSW"},
    "parish": {"status": "eingepfarrt", "church_of": "Harpersdorf", "verbatim": "Später erhielt Kaltenborn wieder Kirche, Friedhof und Schule in Harpersdorf"},
    "school": {"exists": False, "note": "schult nach Harpersdorf"},
    "houses": 41,
    "inhabitants": 245,
    "occupations": {"Bauern": 25, "Häusler": 13, "Taglöhner": 10, "Dienstboten": 9},
    "crafts": {"Maurer": 8, "Steinmetzen": 7, "Zimmerleute": 6, "Fleischer": 1, "Schneider": 1, "Schuhmacher": 1, "Weber": 1},
    "flur_morgen": 1024.96,
    "flur_verbatim": "1024,96 Morgen",
    "soil": "zum größeren Theile mittelmäßig",
    "livestock": {"Pferde": 7, "Rinder": 101, "Schafe": 60, "Schweine": 53, "Ziegen": 3, "Gänse": 50, "Bienenstöcke": 7},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere 9 5/9 Morgen (Hutung, Wege und Bach) im Werthe von 200 Thlr., als weitere weder Vermögen noch Schulden; ihre Jahresausgabe beträgt gegen 150 Thlr.", "assets_thaler": 200, "expenditure_thaler": 150},
    "facilities": ["Armenhaus", "Brauhaus", "Spritzenhaus", "Schenke", "Feuerspritze"],
    "subplaces": [{"name": "Käseschenke (Gasthaus zum Fürstenkranz)", "kind": "Sonstiges", "page": "485"}],
    "events": [
        {"year": 1344, "event_de": "Herr v. Wolfersdorf gibt eine Mark Silber Ortszins an das Kloster Cronswitz; Freigut der Familie v. Wolfersdorf", "event_en": "Lord von Wolfersdorf gives one mark of silver in local dues to Cronswitz convent; free estate of the von Wolfersdorf family"},
        {"year": 1647, "event_de": "Theilungsacten: Kirche und Schule in Großsaara", "event_en": "Partition records: church and school at Großsaara"},
        {"year": 1861, "event_de": "Käseschenke brennt ab", "event_en": "The Käseschenke inn burns down"}
    ],
    "persons": ["Familie v. Wolfersdorf", "Familie v. Koppy"],
    "notes": "3 Communalhäuser (Armenhaus, Brauhaus, Spritzenhaus) und 41 Privathäuser mit 37 Höfen und 28 Scheunen; 49 Familien; 1861: 231 Einwohner; 18 Bauerngüter, 2 Grundstücksverbände, 1 Pertinenzstück, 37 ledige Grundstücke; Käseschenke isoliert im Südosten auf der Höhe des Käsebergs, rechter Name 'zum Fürstenkranz'; 15 Familien bauen ihr Jahresbrod; 1 wilde Ehe; deutscher Anbau, ursprünglich Bestandtheil der Pflege Langenberg; Richtung im Druck 'WWS.'. Das Ortsregister gibt für die Käseschenke S. 484 an (Text auf S. 485).",
    "summary_de": "Kaltenborn, kleines tief eingebuchtetes Langdorf im Käsethal 2 ¼ Stunden westsüdwestlich von Gera, nach Harpersdorf gepfarrt und geschult; 245 Einwohner, Landbau und Handarbeit (Maurer, Steinmetzen), Flur 1024,96 Morgen, Käseschenke (Gasthaus zum Fürstenkranz) auf dem Käseberg.",
    "summary_en": "Kaltenborn, a small long village tucked into the Käsethal two and a quarter hours west-southwest of Gera, in the parish and school district of Harpersdorf; 245 inhabitants, farming and manual trades (masons, stonecutters), field area 1024.96 Morgen, the Käseschenke inn ('Zum Fürstenkranz') on the Käseberg."
})

E.append({
    "id": "harpersdorf",
    "name": "Harpersdorf",
    "start": {"page": "485", "block": "b2"},
    "end": {"page": "487", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "zweizeilig langes Kirchdorf",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Harprechtsdorf", "year": 1333}],
    "dialect_form": "Harpersdorf",
    "first_mention_year": 1333,
    "location": {"verbatim": "2 1/2 Stunde westlich von Gera, an der Straße von da nach Kloster Lausnitz", "relative_to": "Gera", "distance_hours": 2.5, "direction": "W"},
    "elevation": {"value": 640, "unit": "Fuß", "verbatim": "in der Dorfmitte 640 Fuß hoch"},
    "parish": {"status": "Filial", "church_of": "Kraftsdorf", "verbatim": "Sie ist ein Filial von Kraftsdorf, steht aber unter der diesseitigen Landesherrschaft"},
    "school": {"exists": True, "pupils": 153},
    "houses": 77,
    "inhabitants": 412,
    "occupations": {"Oeconomen": 32, "Häusler": 49, "Taglöhner": 12, "Dienstboten": 27, "Kapitalisten": 1},
    "crafts": {"Steinhauer": 20, "Zimmerleute": 4, "Böttcher": 3, "Müller": 2, "Schuhmacher": 2, "Tischler": 2, "Wagner": 2, "Bäcker": 1, "Fleischer": 1, "Korbmacher": 1, "Schmied": 1, "Schneider": 1, "Bildhauer": 1, "Holzschneider": 1, "Uhrmacher": 1, "Victualienhändler": 1},
    "flur_morgen": 2287.3,
    "flur_verbatim": "2287 3/10 Morgen",
    "soil": "1/7 gut, 3/7 mittelgut, 3/7 gering",
    "livestock": {"Pferde": 14, "Rinder": 208, "Schweine": 145, "Ziegen": 37, "Gänse": 400, "Bienenstöcke": 16},
    "municipal_finances": {"verbatim": "Die Gemeinde Harpersdorf besitzt als engere nahe an 29 Morgen (Wiesen und Buschholz) im Werthe von 3500 Thlr., als weitere 80 Thlr. Kapital; ihre Jahresausgabe beträgt circa 300 Thlr.", "assets_thaler": 3500, "capital_thaler": 80, "expenditure_thaler": 300},
    "facilities": ["Kirche", "Schule", "Brauhaus", "Spritzenhaus", "Privatwirthshaus", "Gemeindeschenke", "Privatschnapsschank", "Mühle", "Feuerspritze", "Steinbrüche"],
    "subplaces": [
        {"name": "Oberoder Queckmühle", "kind": "Mühle", "page": "486"},
        {"name": "Schütz- oder Untermühle", "kind": "Mühle", "page": "486"},
        {"name": "Desse (Wüstung, ein Stück in der Flur)", "kind": "Wüstung", "page": "486"}
    ],
    "events": [
        {"year": 1524, "event_de": "Kirche bereits vorhanden (Notiz des Kraftsdorfer Pfarrarchivs)", "event_en": "Church already in existence (note in the Kraftsdorf parish archive)"},
        {"year": 1578, "event_de": "Ein Ortsnachbar wird wegen Totschlags mit dem Schwert hingerichtet", "event_en": "A villager is executed by the sword for killing another"},
        {"year": 1818, "event_de": "Kirche 1817 erbaut und 1818 eingeweiht", "event_en": "Church built in 1817 and consecrated in 1818"},
        {"year": 1822, "event_de": "Erfolglose Bohrversuche auf Steinsalz am Eingang des Dessegrundes", "event_en": "Unsuccessful drilling for rock salt at the entrance of the Dessegrund"},
        {"year": 1839, "event_de": "Schulhaus 1837-39 gebaut, am 5. November eingeweiht", "event_en": "School house built 1837-39, consecrated on 5 November"},
        {"year": 1856, "event_de": "Hausbrand am 23. Februar, ebenso im Februar 1859", "event_en": "House fire on 23 February, again in February 1859"}
    ],
    "persons": ["Ulz v. Schauroth"],
    "notes": "1 Kirche, 1 Schule, 1 Brau-, 1 Spritzenhaus und 77 Privathäuser mit 77 Höfen und 40 Scheunen; 77 Familien; 1861: 408 Einwohner; Steinhauer 'über 20'; 31 Bauerngüter, 1 Grundstücksverband, 2 Pertinenzstücke, 143 ledige Grundstücke; Güterlehen und Trift gehörten dem Kammergut Niederndorf; Kirchenvermögen 76 Thlr., Bücher seit 1761; Kaltenborn kircht, schult und begräbt hierher, Niederndorf ist eingeschult; Flur 5 Teiche, 8 Sandsteinbrüche, 1 Lehmgrube; Absatz der Werksteine nach Gera, Schleiz u. a.; früher zur Pflege Langenberg, ehemaliges Rittergut zerschlagen; deutscher Anbau.",
    "summary_de": "Harpersdorf, langgestrecktes Kirchdorf 2 ½ Stunden westlich von Gera: Kirche (1817/18) als Filial von Kraftsdorf, Schule (153 Kinder, auch Kaltenborn und Niederndorf), 412 Einwohner, über 20 Steinhauer mit Werksteinabsatz, Oeconomen und Häusler, Flur 2287 3/10 Morgen, Besitz früherer Rittergutsfamilien.",
    "summary_en": "Harpersdorf, a long-stretched church village two and a half hours west of Gera: church (1817/18) as a branch of Kraftsdorf, school (153 children, also Kaltenborn and Niederndorf), 412 inhabitants, over 20 stonecutters supplying dressed stone, farmers and smallholders, field area 2287 3/10 Morgen, former manorial owners."
})

# ------------------------------------------------------------------ pages
pg("478", "Schluss von Milbitz (Flur 496,18 Morgen, Kalksteinbrüche, Hochwasser 1799, Sage vom Zwergvolk der Zwerghöhlen); Rubitz, Dorf im Erlbachsgrund: Namensformen seit 1121, Lage, Häuser, 225 Einwohner, Vieh, Rittergut und Besitzer, Mühle.",
   "End of Milbitz (field area 496.18 Morgen, limestone quarries, flood of 1799, legend of the dwarf folk of the Zwerghöhlen); Rubitz, a village in the Erlbach valley: name forms since 1121, location, houses, 225 inhabitants, livestock, manor and owners, mill.",
   ["Milbitz", "Rubitz", "Zwerghöhlen", "Schaumkalk", "Rittergut", "Mühle", "Kalkstein", "Sagen", "Hochwasser 1799"], ["Milbitz", "Rubitz", "dwarf caves", "aphrite", "manor", "mill", "limestone", "legends", "flood 1799"], ["Dorf", "Sagen", "Gesteine und Mineralien", "Rittergut"])
pg("479", "Schluss von Rubitz (Gemeindefinanzen, Berufe, Flur 1080 3/5 Morgen, Brände, Gerichtsverhältnisse nach 1647); Wüstung Texdorf; Beginn von Töppeln, Thaldorf mit Rittergut 1 ½ Stunden westnordwestlich von Gera: Lage, Häuser, 244 Einwohner, Vieh.",
   "End of Rubitz (municipal finances, occupations, field area 1080 3/5 Morgen, fires, jurisdiction after 1647); the deserted settlement of Texdorf; start of Töppeln, a valley village with a manor one and a half hours west-northwest of Gera: location, houses, 244 inhabitants, livestock.",
   ["Rubitz", "Texdorf", "Wüstung", "Töppeln", "Gemeindefinanzen", "Flur", "Brände", "Rittergut", "Gypsbruch"], ["Rubitz", "Texdorf", "deserted settlement", "Töppeln", "municipal finances", "field area", "fires", "manor", "gypsum quarry"], ["Dorf", "Wüstung", "Gemeindefinanzen"])
pg("480", "Töppeln: Rittergut mit Kemnatenhaus von 1370 und Besitzerfolge bis 1805, Kirchen- und Schulzugehörigkeit zu Frankenthal, Mühlen, Gemeindefinanzen, Berufe und Rückgang der Wollkämmerei, Flur 679 13/18 Morgen, Namensdeutung.",
   "Töppeln: manor with 'Kemnate' house of 1370 and succession of owners to 1805, parish and school affiliation with Frankenthal, mills, municipal finances, occupations and the decline of wool combing, field area 679 13/18 Morgen, name etymology.",
   ["Töppeln", "Rittergut", "Kemnate", "Frankenthal", "Mühlen", "Wollkämmerei", "Gemeindefinanzen", "Flur", "Namensdeutung"], ["Töppeln", "manor", "Kemnate", "Frankenthal", "mills", "wool combing", "municipal finances", "field area", "name etymology"], ["Dorf", "Rittergut", "Mühlen", "Burgen und Schlösser"])
pg("481", "Mühlsdorf, hochgelegenes Kirchdörfchen 1 ½ Stunden westnordwestlich von Gera: Häuser, 176 Einwohner, Vieh, Rittergut, Kirche (1736) als Filial von Frankenthal, Schule (31 Kinder), Gemeindefinanzen, Berufe, Flur 741 1/2 Morgen.",
   "Mühlsdorf, an elevated church village one and a half hours west-northwest of Gera: houses, 176 inhabitants, livestock, manor, church (1736) as a branch of Frankenthal, school (31 children), municipal finances, occupations, field area 741 1/2 Morgen.",
   ["Mühlsdorf", "Kirche", "Rittergut", "Frankenthal", "Schule", "Gemeindefinanzen", "Flur", "Ackerbau", "Einwohner"], ["Mühlsdorf", "church", "manor", "Frankenthal", "school", "municipal finances", "field area", "farming", "inhabitants"], ["Dorf", "Kirchengebäude", "Gemeindefinanzen"])
pg("482", "Schluss von Mühlsdorf (Geschichte, Leibarzt Fischer); Wüstung Cosse; Pörsdorf, kleines Plateau- und Kirchdorf 2 ¼ Stunden westnordwestlich von Gera: Häuser, 138 Einwohner, Vieh, Kirche (1835) als Filial von Rüdersdorf mit altenburgischen Rechten, Gemeindebesitz.",
   "End of Mühlsdorf (history, physician Fischer); deserted settlement of Cosse; Pörsdorf, a small plateau and church village two and a quarter hours west-northwest of Gera: houses, 138 inhabitants, livestock, church (1835) as a branch of Rüdersdorf with Altenburg rights, municipal property.",
   ["Mühlsdorf", "Cosse", "Wüstung", "Pörsdorf", "Kirche", "Rüdersdorf", "Altenburger Konsistorium", "Recess 1746", "Joseph Gottfried Fischer"], ["Mühlsdorf", "Cosse", "deserted settlement", "Pörsdorf", "church", "Rüdersdorf", "Altenburg consistory", "recess 1746"], ["Dorf", "Wüstung", "Pfarreien", "Territorialgeschichte"])
pg("483", "Schluss von Pörsdorf (Güter, Berufe, Flur 888 1/5 Morgen, Bevölkerung 1660); Niederndorf, Kirchdorf 2 Stunden westlich von Gera: Namensformen seit 1184, Häuser, 269 Einwohner, Vieh, Schule in Harpersdorf, Kirche als Filial von Kraftsdorf, Brand 1668.",
   "End of Pörsdorf (farms, occupations, field area 888 1/5 Morgen, population in 1660); Niederndorf, a church village two hours west of Gera: name forms since 1184, houses, 269 inhabitants, livestock, school at Harpersdorf, church as a branch of Kraftsdorf, fire of 1668.",
   ["Pörsdorf", "Niederndorf", "Kirche", "Filial Kraftsdorf", "Brand 1668", "Flur", "Bevölkerung 1660", "Schule Harpersdorf", "Ortsnamen"], ["Pörsdorf", "Niederndorf", "church", "branch of Kraftsdorf", "fire of 1668", "field area", "population 1660", "Harpersdorf school"], ["Dorf", "Kirchengebäude", "Dreißigjähriger Krieg"])
pg("484", "Niederndorf: Kirche (Altarschrein, Glocken 1668/1669, Vermögen), Kammergut mit Besitzerfolge seit 1184 und Übernahme durch Heinrich XXX., Gemeindefinanzen, Berufe, Flur 1721 11/25 Morgen, Geschichte; Beginn von Kaltenborn, Langdorf im Käsethal.",
   "Niederndorf: church (altarpiece, bells of 1668/1669, assets), crown estate with succession of owners since 1184 and takeover by Heinrich XXX, municipal finances, occupations, field area 1721 11/25 Morgen, history; start of Kaltenborn, a long village in the Käsethal.",
   ["Niederndorf", "Kaltenborn", "Kammergut", "Besitzerfolge", "Kirche", "Altarschrein", "Gemeindefinanzen", "Flur", "Heinrich XXX."], ["Niederndorf", "Kaltenborn", "crown estate", "owners", "church", "altarpiece", "municipal finances", "field area", "Heinrich XXX"], ["Dorf", "Kammergut", "Kirchengebäude"])
pg("485", "Kaltenborn: Häuser, 245 Einwohner, Vieh, Kirchen- und Schulzugehörigkeit, Käseschenke (Gasthaus zum Fürstenkranz), Gemeindefinanzen, Berufe (Maurer, Steinmetzen), Flur 1024,96 Morgen, Geschichte; Beginn von Harpersdorf, Kirchdorf 2 ½ Stunden westlich von Gera.",
   "Kaltenborn: houses, 245 inhabitants, livestock, parish and school affiliation, Käseschenke inn ('Zum Fürstenkranz'), municipal finances, occupations (masons, stonecutters), field area 1024.96 Morgen, history; start of Harpersdorf, a church village two and a half hours west of Gera.",
   ["Kaltenborn", "Käseschenke", "Harpersdorf", "Steinmetzen", "Gemeindefinanzen", "Flur", "Pflege Langenberg", "Freigut", "Wolfersdorf"], ["Kaltenborn", "Käseschenke", "Harpersdorf", "stonecutters", "municipal finances", "field area", "Langenberg district", "free estate"], ["Dorf", "Gasthof", "Handwerk", "Gemeindefinanzen"])
pg("486", "Harpersdorf: Kirche (1817/18) als Filial von Kraftsdorf, Schule (153 Kinder), Wirtschaften und Mühlen, Gemeindefinanzen, Berufe (über 20 Steinhauer), Flur 2287 3/10 Morgen, Sandsteinbrüche, Geschichte (Pflege Langenberg, Hinrichtung 1578, Bohrversuche 1822).",
   "Harpersdorf: church (1817/18) as a branch of Kraftsdorf, school (153 children), inns and mills, municipal finances, occupations (over 20 stonecutters), field area 2287 3/10 Morgen, sandstone quarries, history (Langenberg district, execution of 1578, drilling attempts of 1822).",
   ["Harpersdorf", "Steinhauer", "Sandsteinbrüche", "Kirche", "Schule", "Mühlen", "Gemeindefinanzen", "Flur", "Steinsalz Bohrversuch"], ["Harpersdorf", "stonecutters", "sandstone quarries", "church", "school", "mills", "municipal finances", "field area", "rock salt drilling attempt"], ["Dorf", "Handwerk", "Gesteine und Mineralien", "Schule"])

G.append({"term": "Wüstung", "variants": ["wüst"], "kind": "term", "de": "Abgegangener, verlassener Ort; in Brückners Ortskunde mit eigenem Absatz behandelt (Pottendorf, Vollersdorf, Texdorf, Cosse).", "en": "Abandoned settlement; given a paragraph of its own in Brückner's topography (Pottendorf, Vollersdorf, Texdorf, Cosse).", "pages": ["419", "448", "479", "482"]})
G.append({"term": "Cronswitz", "variants": ["Kloster Cronswitz"], "kind": "institution", "de": "Kloster bei Gera, das im 13. und 14. Jahrhundert in vielen Dörfern des Unterlandes Güter und Zinsen erhielt.", "en": "Convent near Gera that received estates and dues in many villages of the Unterland in the 13th and 14th centuries.", "pages": ["427", "454", "466", "462"]})
G.append({"term": "Pflege Langenberg", "variants": ["Pflege"], "kind": "institution", "de": "Reichspflege Langenberg, alter Verwaltungsbezirk, zu dem zahlreiche Dörfer des Unterlandes ursprünglich gehörten.", "en": "Imperial district of Langenberg, an old administrative district to which many villages of the Unterland originally belonged.", "pages": ["413", "414", "480", "484"]})
G.append({"term": "Anspanngut", "variants": ["Anspanngüter", "Pferdefrohngut", "Handfrohngut"], "kind": "term", "de": "Bauerngut mit Gespann (Pferde- bzw. Ochsenfron) im Unterschied zum Handfrongut, dessen Besitzer nur mit der Hand fronten.", "en": "Farm with a draught team (horse or ox service) as opposed to a hand-service farm whose owner rendered labour by hand only.", "pages": ["482", "483"]})
G.append({"term": "Scheffel", "variants": ["Schffl."], "kind": "unit", "de": "Getreidemaß; nach Brückners Tabelle S. 832 gilt in Gera 1 dresdner Scheffel = 1,0383 Hektoliter.", "en": "Grain measure; according to Brückner's table on p. 832, 1 Dresden Scheffel = 1.0383 hectolitres in Gera.", "pages": ["474"]})
G.append({"term": "Morgen", "variants": ["Mrg.", "Acker"], "kind": "unit", "de": "Flächenmaß der Flurangaben in den Ortsartikeln; nach Brückners Tabelle S. 832 ist 1 preuß. Morgen (180 Quadratruthen) = 0,255322 Hektar.", "en": "Unit of area used in the field-area figures of the village articles; according to Brückner's table on p. 832, 1 Prussian Morgen (180 square rods) = 0.255322 hectares.", "pages": ["419", "426", "427", "452"]})
