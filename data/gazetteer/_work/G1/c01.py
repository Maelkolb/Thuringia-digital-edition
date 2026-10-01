# -*- coding: utf-8 -*-
E = []
P = []
G = []

# ------------------------------------------------------------------ entries
E.append({
    "id": "landestheil-gera",
    "name": "Landestheil Gera",
    "start": {"page": "407", "block": "b1"},
    "end": {"page": "415", "block": "b5"},
    "landestheil": "Gera",
    "type_verbatim": "Der Landestheil oder Landrathsbezirk Gera",
    "type": "Landestheil",
    "wuestung": False,
    "elevation": {"value": 730, "unit": "Fuß", "verbatim": "von 460 bis 989 Fuß ansteigend … circa 730 Fuß hohen mittleren Durchschnittsfläche"},
    "houses": 4023,
    "inhabitants": 38147,
    "census_year": 1867,
    "facilities": ["Residenzschloss Osterstein", "Stadt Gera", "Elsterthal", "Eisenbahn"],
    "events": [
        {"year": 999, "event_de": "Kaiser und Reich eignen die Vogtei Gera dem Kloster Quedlinburg zu", "event_en": "Emperor and Empire grant the advocacy of Gera to Quedlinburg convent"},
        {"year": 1237, "event_de": "Die Vögte von Weida erlangen die Gerichtsbarkeit über Stadt und Pflege Gera", "event_en": "The advocates of Weida obtain jurisdiction over town and district of Gera"},
        {"year": 1306, "event_de": "Die Vögte sichern sich die Pflege Gera durch Ankauf", "event_en": "The advocates secure the district of Gera by purchase"},
        {"year": 1364, "event_de": "Die Vögte von Gera erwerben die zweite Hälfte der Pflege Langenberg (erste Hälfte um 1328)", "event_en": "The advocates of Gera acquire the second half of the Langenberg district (first half about 1328)"},
        {"year": 1547, "event_de": "Die Lehnsherrlichkeit geht durch Burggraf Heinrich V. an die Krone Böhmen über", "event_en": "Feudal overlordship passes to the Crown of Bohemia through Burgrave Heinrich V"},
        {"year": 1647, "event_de": "Theilungsacten: Zählung von 1 Stadt, 14 Amtsdörfern, 9 Mischdörfern und 57 adligen Orten", "event_en": "Partition records: 1 town, 14 official villages, 9 mixed villages and 57 noble villages"},
        {"year": 1848, "event_de": "Vereinigung aller reußischen Landesteile unter Fürst Heinrich LXII. (1. October)", "event_en": "Unification of all Reuss territories under Prince Heinrich LXII (1 October)"}
    ],
    "persons": ["Heinrich LXII.", "Heinrich LXVII.", "Heinrich XIV.", "Heinrich V. (Burggraf)", "Heinrich Posthumus"],
    "notes": "Fläche 4,03 ☐M. in Hauptkörper und Exclave (Lichtenberg, Otticha, Pohlen, Wüst- und Kleinfalke); 5 Stunden breit, 4 Stunden lang; 16 Orte im Elsterthal, 35 auf der Ostseite, 30 auf der Westseite; Bevölkerung 1647: 8392, 1794: 19523, 1867: 38147 (Tabellen S. 409-413); 8096 Familien 1867.",
    "summary_de": "Einleitende Übersicht über das reußische Unterland: Grenzen, Gliederung in Elsterthal, Ost- und Westbuckel, Bevölkerungsentwicklung 1647–1867 nach Orten, Industrie- und Agrarorte, Besitzverhältnisse und die Herrschaftsgeschichte von den Vögten von Weida bis zur Vereinigung 1848.",
    "summary_en": "Introductory overview of the Reuss lowland (Unterland): boundaries, division into Elster valley and eastern and western upland, population development 1647-1867 by place, industrial and agrarian places, tenure structure, and the history of rule from the advocates of Weida to the unification of 1848."
})

E.append({
    "id": "osterstein",
    "name": "Osterstein",
    "start": {"page": "415", "block": "b6"},
    "end": {"page": "418", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "Residenzschloß des Fürstenthums",
    "type": "Schloss",
    "wuestung": False,
    "first_mention_year": 1234,
    "location": {"verbatim": "1/4 Stunde nordwestlich von Gera", "relative_to": "Gera", "distance_hours": 0.25, "direction": "NW"},
    "elevation": {"value": 60, "unit": "Fuß über der Elster", "verbatim": "auf einem 60 Fuß über der Elster hohen Nordostcap des waldreichen Hainbergs"},
    "parish": {"status": "Schlosskirche", "church_of": "Untermhaus", "verbatim": "von 1852 an begann wieder der Gottesdienst in der Schlosskirche, deren Pastorat seit 1854 der erste Diacon zu Gera als Hofprediger und als Pfarrer zu Untermhaus verwaltet"},
    "facilities": ["Schlosskirche", "Marstall", "Marmorsaal", "Ahnensaal", "Waffensaal", "Bibliothek", "Archiv", "Schlossgarten", "Reithaus"],
    "subplaces": [
        {"name": "Wolfsbrücke", "kind": "Sonstiges", "page": "417"},
        {"name": "Preußenwiese", "kind": "Sonstiges", "page": "418"},
        {"name": "Torstensohnseiche", "kind": "Sonstiges", "page": "418"},
        {"name": "Siebeneichen", "kind": "Sonstiges", "page": "418"}
    ],
    "events": [
        {"year": 1234, "event_de": "Erste urkundliche Erwähnung; der weidaische Reichsvoigt Heinrich residiert hier", "event_en": "First documentary mention; the imperial advocate Heinrich of Weida resides here"},
        {"year": 1450, "event_de": "Nach der Verwüstung Geras wird Osterstein bleibende Residenz", "event_en": "After the devastation of Gera, Osterstein becomes the permanent residence"},
        {"year": 1470, "event_de": "Nordflügel durch Heinrich von Gera erbaut (1468-1470)", "event_en": "North wing built by Heinrich of Gera (1468-1470)"},
        {"year": 1665, "event_de": "Neubau des Ostflügels unter Heinrich II.", "event_en": "New east wing under Heinrich II"},
        {"year": 1702, "event_de": "Erneuerung des Nordflügels, Ahnensaal und Schlossgarten unter Heinrich XVIII.", "event_en": "Renewal of the north wing; ancestral hall and palace garden under Heinrich XVIII"},
        {"year": 1852, "event_de": "Einweihung der restaurierten Schlosskirche am 30. Mai", "event_en": "Restored palace church consecrated on 30 May"},
        {"year": 1863, "event_de": "Südlicher Prachtbau mit Brücke und Thorgebäude 1859-1863 durch Heinrich LXVII.", "event_en": "Southern state building with bridge and gatehouse, 1859-1863, under Heinrich LXVII"}
    ],
    "persons": ["Heinrich LXVII.", "Heinrich XVIII.", "Heinrich II.", "Heinrich LXII.", "Heinrich LXXII.", "Heinrich XIV."],
    "summary_de": "Osterstein, Residenzschloss des Fürstentums, ¼ Stunde nordwestlich von Gera auf dem Hainberg: ehemalige Reichsburg, urkundlich 1234, Bauperioden vom 15. bis 19. Jahrhundert, Schlosskirche, Sagen, Umgebung und der ursprüngliche Rentendistrict.",
    "summary_en": "Osterstein, residence castle of the principality, a quarter hour northwest of Gera on the Hainberg: former imperial castle, documented in 1234, building phases from the 15th to the 19th century, castle church, legends, surroundings and the original rent district."
})

E.append({
    "id": "ernsee",
    "name": "Ernsee",
    "start": {"page": "418", "block": "b3"},
    "end": {"page": "419", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "hoch, frisch und zugig gelegenes Dörfchen",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [
        {"form": "Ernse", "year": 1397}, {"form": "Ernsehe", "year": 1533},
        {"form": "Irrensehe", "year": None}, {"form": "Irrenshöhe", "year": None},
        {"form": "Errensehe", "year": None}, {"form": "Ehrensee", "year": None}
    ],
    "dialect_form": "Ernsee",
    "first_mention_year": 1397,
    "location": {"verbatim": "zwischen Osterstein und Frankenthal, 3/4 Stunde westlich von Gera", "relative_to": "Gera", "distance_hours": 0.75, "direction": "W"},
    "parish": {"status": "eingepfarrt", "church_of": "Frankenthal", "verbatim": "pfarrt, begräbt und schult … nach Frankenthal"},
    "school": {"exists": False, "pupils": 23, "note": "schult nach Frankenthal"},
    "houses": 17,
    "inhabitants": 136,
    "occupations": {"Bauern": 13, "Häusler": 3, "Taglöhner": 12, "Dienstboten": 28},
    "crafts": {"Maurer": 4, "Zimmerer": 2, "Dachdecker": 1, "Schneider": 1},
    "flur_morgen": 677.73,
    "flur_verbatim": "677 11/15 Morgen",
    "livestock": {"Pferde": 13, "Rinder": 84, "Schafe": 413, "Schweine": 81, "Ziegen": 7, "Gänse": 103, "Bienenstöcke": 9},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt kein Vermögen, wohl aber 300 Thlr. Schulden und bedarf jährlich 127 Thlr. für Kirche, Pfarrei und Schule in Frankenthal, für ihr Gemeindehaus und zur Erhaltung der Dorfstraße und zweier Communicationswege, die ihr durch ein Abkommen vom 21", "debts_thaler": 300, "expenditure_thaler": 127},
    "facilities": ["Kammergut", "Forstei", "Gemeindehaus", "Privatwirthshaus", "Feuerspritze", "Dorfteiche"],
    "subplaces": [
        {"name": "Kammergut Ernsee", "kind": "Kammergut", "page": "418"},
        {"name": "Waldschlösschen", "kind": "Sonstiges", "page": "418"}
    ],
    "events": [
        {"year": 1397, "event_de": "Erste Erwähnung; Pezold von Ernse", "event_en": "First mention; Pezold von Ernse"},
        {"year": 1616, "event_de": "Eine ernseer Kindesmörderin wird gegäckt", "event_en": "An infanticide from Ernsee is executed"},
        {"year": 1856, "event_de": "Abkommen mit der fürstlichen Kammer über die Gemeindelasten (21. Januar)", "event_en": "Agreement with the princely chamber on municipal burdens (21 January)"}
    ],
    "notes": "1 Kammergutsgebäude, 1 Gemeindehaus, 17 Privathäuser mit 11 Scheunen; 29 Familien; 1861: 128 Einwohner; 7 bäuerliche Güter; Flur 74 % Feld, 2 % Wiesen, Steuerwerth 71,460 Thlr.; sorbischen Ursprungs; früher zur Kirche des wüsten Pottendorf.",
    "summary_de": "Ernsee, kleines Höhendorf ¾ Stunde westlich von Gera, nach Frankenthal gepfarrt und eingeschult; Kammergut als ehemaliges Burg- und Küchengut von Osterstein, Forstei, Gemeindefinanzen, Namensdeutungen und sorbischer Ursprung.",
    "summary_en": "Ernsee, a small upland village three quarters of an hour west of Gera, assigned to the parish and school of Frankenthal; its crown estate, formerly a castle and kitchen estate of Osterstein, forester's lodge, municipal finances, name etymologies and Sorbian origin."
})

E.append({
    "id": "pottendorf",
    "name": "Pottendorf",
    "start": {"page": "419", "block": "b2"},
    "end": {"page": "420", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "Die Wüstung Pottendorf",
    "type": "Wüstung",
    "wuestung": True,
    "location": {"verbatim": "3/8 Stunde nördlich von Ernsee", "relative_to": "Ernsee", "distance_hours": 0.375, "direction": "N"},
    "facilities": ["Marienkirchlein (Wallfahrtsort)", "Teich"],
    "events": [
        {"year": 1800, "event_de": "Noch vollständige Mauern, Scheunenlager und Miststätten angetroffen", "event_en": "Complete walls, barn sites and dung heaps still found"},
        {"year": 1853, "event_de": "Wald-Saugarten angelegt, später wieder aufgegeben", "event_en": "Game park for wild boar laid out, later abandoned"}
    ],
    "summary_de": "Wüstung Pottendorf, nördlich von Ernsee, jetzt herrschaftlicher Walddistrict: ehemaliger Kultort mit Marienkirche und Wallfahrt (Marienpuppe), Zerstörung im 15. Jahrhundert, Sagen und Verbleib des Marienbildes in Untermhaus.",
    "summary_en": "Deserted settlement of Pottendorf north of Ernsee, now a princely forest district: a former cult site with a Marian church and pilgrimage (the 'Marienpuppe'), destroyed in the 15th century, with legends and the later fate of the Marian image in Untermhaus."
})

E.append({
    "id": "untermhaus",
    "name": "Untermhaus",
    "start": {"page": "420", "block": "b2"},
    "end": {"page": "423", "block": "b1"},
    "landestheil": "Gera",
    "type_verbatim": "großes Kirch- und Pfarrdorf, höfischer Vorort von Osterstein, Verkehrsvorstadt von Gera",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Unterhaus", "year": 1191}, {"form": "Underhaus", "year": 1534}, {"form": "Unterheuser", "year": 1534}],
    "dialect_form": "Unterhaus",
    "first_mention_year": 1191,
    "location": {"verbatim": "1/8 Stunde nordwestlich von Gera", "relative_to": "Gera", "distance_hours": 0.125, "direction": "NW"},
    "parish": {"status": "Pfarrdorf", "church_of": None, "verbatim": "großes Kirch- und Pfarrdorf … 1736 wurden unter Heinrich XXV. die vorher nach Gera in die Hauptkirche gepfarrten Gemeinden Untermhaus, Gries und Cuba von der Stadt getrennt, zu einer eigenen Parochie vereinigt"},
    "school": {"exists": True, "pupils": 320},
    "houses": 101,
    "inhabitants": 1731,
    "occupations": {"Bauern": 2, "Kapitalisten": 10, "Handeltreibende": 8, "Hauderer": 3, "selbstständige Gewerbtreibende": 153, "unselbstständige Gewerbtreibende und Fabrikarbeiter": 311},
    "crafts": {"Maurer": 16, "Schneider": 7, "Bäcker": 6, "Schuhmacher": 6, "Zimmerleute": 6, "Fleischer": 5, "Weber": 4, "Korbmacher": 3, "Sattler": 3, "Fischer": 2, "Tischler": 2, "Gärtner": 1, "Gerber": 1, "Glaser": 1, "Goldarbeiter": 1, "Klempner": 1, "Schlosser": 1, "Seiler": 1, "Zinngießer": 1},
    "livestock": {"Pferde": 54, "Rinder": 33, "Schweine": 109, "Esel": 1, "Ziegen": 16, "Gänse": 30, "Bienenstöcke": 16},
    "municipal_finances": {"verbatim": "Ihr Grundeigenthum, 3 5/6 Morgen groß und 7500 Thlr. werth, besteht in Communalgebäuden, freien Plätzen, Ortsstraßen und 3 Communicationswegen. An Kapital hat sie circa 1000 Thlr., an Schulden circa 6000 Thlr., wovon ein Theil auf Cuba kommt; ihre Jahresausgabe beträgt 600 bis 700 Thlr.", "assets_thaler": 7500, "capital_thaler": 1000, "debts_thaler": 6000, "expenditure_thaler_min": 600, "expenditure_thaler_max": 700},
    "facilities": ["Kirche", "Schule", "Agnesschule", "Armenhaus", "Rentamt", "Gasthof", "Brauerei", "Mühle", "Dampfmühle", "Porzellanfabrik", "Harmonikafabrik", "Feuerspritze", "Gemeindebibliothek", "Militärschießplatz"],
    "subplaces": [
        {"name": "Gries", "kind": "Sonstiges", "page": "420"},
        {"name": "Aue", "kind": "Sonstiges", "page": "420"},
        {"name": "neue Straße", "kind": "Sonstiges", "page": "420"},
        {"name": "Reitsteg", "kind": "Sonstiges", "page": "420"},
        {"name": "Bach", "kind": "Sonstiges", "page": "420"},
        {"name": "Kammergut Untermhaus", "kind": "Kammergut", "page": "420"},
        {"name": "Küchengarten", "kind": "Sonstiges", "page": "422"},
        {"name": "Fasanerie", "kind": "Sonstiges", "page": "421"},
        {"name": "Hausmühle", "kind": "Mühle", "page": "422"}
    ],
    "events": [
        {"year": 1191, "event_de": "Erste urkundliche Erwähnung (Unterhaus)", "event_en": "First documentary mention (Unterhaus)"},
        {"year": 1709, "event_de": "Hochwasser reißt einige Häuser weg", "event_en": "Flood sweeps away several houses"},
        {"year": 1729, "event_de": "Kammergut nach dem Brand um 1729 von Heinrich XVIII. neu erbaut; Küchengarten angelegt", "event_en": "Crown estate rebuilt by Heinrich XVIII after a fire around 1729; kitchen garden laid out"},
        {"year": 1736, "event_de": "Untermhaus, Gries und Cuba werden von Gera getrennt und zu einer eigenen Parochie vereinigt", "event_en": "Untermhaus, Gries and Cuba separated from Gera and united as their own parish"},
        {"year": 1851, "event_de": "Gries mit Nebentheilen mit Untermhaus zu einer Gemeinde vereinigt", "event_en": "Gries and its parts merged with Untermhaus into one municipality"},
        {"year": 1864, "event_de": "Bau eines Schulhauses", "event_en": "New school building"},
        {"year": 1866, "event_de": "Cholera im Herbst", "event_en": "Cholera in autumn"},
        {"year": 1869, "event_de": "Gründung der Agnesschule (Kleinkinderbewahranstalt) am 10. November", "event_en": "Agnesschule (infant care institution) founded on 10 November"}
    ],
    "persons": ["Heinrich d. Reichen von Weida", "Heinrich XVIII.", "Heinrich XXV.", "Heinrich LXVII."],
    "notes": "395 Familien; 1861: 1257 Einwohner; 1 Kammergutsgebäude, 3 Beamtenbauten, 2 Gemeinde-Armenhäuser, 101 Privathäuser; besitzt keine Flurmarkung (Grundeigenthum 3 5/6 Morgen); 41 ledige Grundstücke; die Toten werden in Gera begraben; Schule mit drei Lehrern seit 1865; Kirchenvermögen circa 2212 Thlr.; Kirchenbücher seit 1736.",
    "summary_de": "Untermhaus, großes Kirch- und Pfarrdorf am Fuß des Osterstein, ⅛ Stunde nordwestlich von Gera: städtischer Charakter mit Hof- und Staatsbeamten, Gewerbetreibenden und Fabrikarbeitern; Entstehung als Vorburg, Kirche mit Marienbild (\"Puppe\"), Parochie seit 1736, Schule, Gemeindefinanzen, Gewerbe und Küchengarten.",
    "summary_en": "Untermhaus, a large church and parish village at the foot of Osterstein, an eighth of an hour northwest of Gera: urban in character with court and state officials, tradesmen and factory workers; origins as outer bailey, church with Marian image ('Puppe'), parish since 1736, school, municipal finances, trades and the kitchen garden."
})

E.append({
    "id": "cuba",
    "name": "Cuba",
    "start": {"page": "423", "block": "b2"},
    "end": {"page": "423", "block": "b2"},
    "landestheil": "Gera",
    "type_verbatim": "Dörfchen in der niederen Thalsohle der Elster",
    "type": "Dorf",
    "wuestung": False,
    "historic_forms": [{"form": "Kuba", "year": 1534}],
    "dialect_form": "Kube",
    "first_mention_year": 1534,
    "location": {"verbatim": "1/3 Stunde nordwestlich von Gera", "relative_to": "Gera", "distance_hours": 0.33, "direction": "NW"},
    "parish": {"status": "eingepfarrt", "church_of": "Untermhaus", "verbatim": "pfarrt seit 1736 … nach Untermhaus, vorher nach Gera"},
    "school": {"exists": False, "note": "schult seit 1696 nach Untermhaus, vorher nach Gera"},
    "houses": 24,
    "inhabitants": 328,
    "occupations": {"Feldbautreibende": 6, "Kapitalisten": 4},
    "crafts": {"Maurer": 3, "Bäcker": 1, "Fleischer": 1, "Gärtner": 1, "Gerber": 1, "Korbmacher": 1, "Schneider": 1, "Schuhmacher": 1, "Zimmermann": 1},
    "livestock": {"Pferde": 18, "Rinder": 19, "Schafe": 12, "Schweine": 38, "Ziegen": 4, "Bienenstöcke": 8},
    "municipal_finances": {"verbatim": "Die Gemeinde mit 2 Beamten besitzt außer dem Armenhause (200 Thlr. werth) und einem Antheile an der Feuerspritze in Untermhaus 150 Thlr. Schulden", "assets_thaler": 200, "debts_thaler": 150, "expenditure_thaler": 160},
    "facilities": ["Gemeindearmenhaus", "Privatwirthshaus", "Mühle", "Fournirschneidemühle", "Brettschneiderei", "Militärbadeplatz"],
    "subplaces": [
        {"name": "Mühle Cuba", "kind": "Mühle", "page": "423"},
        {"name": "Fournirschneidemühle", "kind": "Gewerbeanlage", "page": "423"},
        {"name": "Militärbadeplatz", "kind": "Sonstiges", "page": "423"}
    ],
    "events": [
        {"year": 1590, "event_de": "Kupferhammer kurz nach 1590 unterhalb der Mühle errichtet", "event_en": "Copper hammer built shortly after 1590 below the mill"},
        {"year": 1772, "event_de": "Brand", "event_en": "Fire"},
        {"year": 1780, "event_de": "Buchdruckerei 1780-1783", "event_en": "Printing works, 1780-1783"},
        {"year": 1799, "event_de": "Hochwasser; Ort drei Tage lang unnahbare Insel", "event_en": "Flood; village an inaccessible island for three days"},
        {"year": 1808, "event_de": "Steingutfabrik begründet, später Wollenwaarendruckerei", "event_en": "Earthenware factory founded, later a woollen-goods printing works"},
        {"year": 1864, "event_de": "Fournirschneidemaschine und Brettschneiderei angelegt", "event_en": "Veneer-cutting machine and sawmill set up"}
    ],
    "persons": ["J. Gottlieb Nündel"],
    "notes": "1 Gemeindearmenhaus, 24 Privathäuser mit 7 Scheunen; 76 Familien; 1861: 296 Einwohner; keine Feldmarkung (1 kleines Gut unter 20 Morgen, 9 ledige Grundstücke); 8 Ortsarme; Ursprung in der Mühle am Nordende (Kemnate eines ostersteiner Burgmannes, Familie von Schauroth).",
    "summary_de": "Cuba, kleines Dorf in der Elsteraue ⅓ Stunde nordwestlich von Gera, nach Untermhaus gepfarrt und eingeschult; ohne eigene Feldmarkung, Bewohner meist Fabrik- und Handarbeiter; Mühle als Ursprung des Orts, Kupferhammer, Steingutfabrik, Naturdichter Nündel.",
    "summary_en": "Cuba, a small village in the Elster floodplain a third of an hour northwest of Gera, assigned to the parish and school of Untermhaus; without its own field area, inhabitants mostly factory and manual workers; the mill as origin of the settlement, a copper hammer, an earthenware factory, and the nature poet Nündel."
})

# ------------------------------------------------------------------ pages
def pg(page, de, en, kde, ken, subj):
    P.append({"page": page, "summary_de": de, "summary_en": en, "keywords_de": kde, "keywords_en": ken, "subjects": subj})

pg("405", "Titelblatt des II. Theils: Ortskunde des Fürstenthums Reuß j. L.", "Part title of Part II: topography (Ortskunde) of the Principality of Reuss j. L.",
   ["Ortskunde", "Titel", "II. Teil", "Fürstentum Reuß jüngere Linie"], ["topography", "part title", "Part II", "principality of Reuss"], ["Titelei"])
P.append({"page": "406", "summary_de": "Leerseite", "summary_en": "Blank page", "keywords_de": [], "keywords_en": [], "subjects": []})
pg("407", "Beginn der Ortskunde mit dem Landestheil Gera (reußisches Unterland): Namensherkunft, Hauptkörper und Exclave, Grenzen zu Preußen, Sachsen und Sachsen-Altenburg, Enclavenorte, Fläche 4,03 Quadratmeilen und Höhenlage 460 bis 989 Fuß, Gliederung in Elsterthal und zwei Landbuckel.",
   "Start of the topography with the Landestheil Gera (Reuss lowland): origin of the name, main body and exclave, borders with Prussia, Saxony and Saxe-Altenburg, enclave villages, area of 4.03 square miles, elevation 460 to 989 feet, division into the Elster valley and two upland ridges.",
   ["Landestheil Gera", "Unterland", "Exklave", "Grenzen", "Weiße Elster", "Elstertal", "Fläche", "Höhenlage"], ["Gera district", "lowland", "exclave", "boundaries", "White Elster", "Elster valley", "area", "elevation"], ["Lage und Grenzen", "Fläche", "Relief"])
pg("408", "Entwässerung der beiden Landbuckel zur Elster und Vorrang des Elsterthals mit Gera, Köstritz, Untermhaus und Langenberg; Anteil der drei Landglieder an der Bevölkerung 1647, 1864 und 1867 sowie Verteilung der Orte nach Größenklassen (Tabellen).",
   "Drainage of the two upland ridges into the Elster and the predominance of the Elster valley with Gera, Köstritz, Untermhaus and Langenberg; population shares of the three sub-regions in 1647, 1864 and 1867 and distribution of places by size class (tables).",
   ["Elstertal", "Bevölkerungsverteilung", "Gera", "Köstritz", "Langenberg", "Untermhaus", "Ortsgrößen", "Ostseite", "Westseite"], ["Elster valley", "population distribution", "village sizes", "Gera", "Köstritz"], ["Bevölkerung", "Flüsse und Bäche", "Siedlungsform"])
pg("409", "Einfluss Geras auf die Nachbarlandschaften und Bevölkerung 1867 nach Familiengliedern, Dienstboten, Gehilfen und Altersgruppen für die Orte Gera bis Pörsdorf (Tabelle, Beginn); Gera mit Pöppeln 16283 Einwohner.",
   "Influence of Gera on neighbouring areas and the 1867 population by family members, servants, assistants and age groups for places from Gera to Pörsdorf (table, first part); Gera with Pöppeln 16,283 inhabitants.",
   ["Volkszählung 1867", "Bevölkerung", "Altersgruppen", "Dienstboten", "Gera", "Köstritz", "Langenberg", "Tabelle"], ["census 1867", "population", "age groups", "servants", "Gera", "table"], ["Bevölkerung", "Volkszählung", "Berufe"])
pg("410", "Bevölkerung 1867 nach Familiengliedern, Dienstboten und Altersgruppen für die Orte Pohlen bis Zwötzen (Tabelle, Fortsetzung); Gesamtsumme 38147 Einwohner im Landestheil mit Prozentanteilen; Überleitung zur Volkszunahme 1647–1867.",
   "Population in 1867 by family members, servants and age groups for places from Pohlen to Zwötzen (table, continued); district total 38,147 inhabitants with percentage shares; introduction to population growth 1647-1867.",
   ["Volkszählung 1867", "Bevölkerung", "Altersverteilung", "Dienstboten", "Gesamtsumme", "Tabelle", "Zwötzen"], ["census 1867", "population", "age distribution", "servants", "total", "table"], ["Bevölkerung", "Volkszählung"])
pg("411", "Tabelle der Volkszunahme 1647, 1794 und 1867 mit Einwohnern, Familien und Häusern der Orte des Landestheils Gera von Gera bis Rüdersdorf.",
   "Table of population growth in 1647, 1794 and 1867 with inhabitants, families and houses for the places of the Gera district from Gera to Rüdersdorf.",
   ["Bevölkerungsentwicklung", "1647", "1794", "1867", "Einwohner", "Familien", "Häuser", "Tabelle"], ["population growth", "inhabitants", "families", "houses", "table"], ["Bevölkerung", "Volkszählung"])
pg("412", "Fortsetzung der Tabelle der Volkszunahme (Scheubengrobsdorf bis Zwötzen) mit Summen: 8392 Einwohner 1647, 19523 1794, 38147 1867; Zunahme der Bevölkerung um 354 Prozent; Verhältnis von Stadt zu Land 1647–1867; Beginn des Vergleichs von Industrie- und Agrarorten.",
   "Continuation of the population growth table (Scheubengrobsdorf to Zwötzen) with totals of 8,392 inhabitants in 1647, 19,523 in 1794 and 38,147 in 1867; population growth of 354 percent; urban versus rural share 1647-1867; start of the comparison of industrial and agrarian places.",
   ["Bevölkerungszunahme", "Stadt und Land", "Einwohnerzahl", "Quadratmeile", "Industrieorte", "Agrarorte", "Tabelle"], ["population increase", "urban and rural", "inhabitants", "square mile", "industrial places", "agrarian places"], ["Bevölkerung", "Volkszählung"])
pg("413", "Einwohner der vier Industrieorte (Gera, Köstritz, Langenberg, Untermhaus) und der Agrarorte 1647, 1794, 1867; Häuserzuwachs; Gliederung der Orte 1647 in Stadt, Amtsdörfer, Mischdörfer und adlige Orte; Rittergüter; Gebiete der Herrschaft Gera (Osterstein, Stiftsvoigtei, Pflege Langenberg, Caaschwitz).",
   "Inhabitants of the four industrial places (Gera, Köstritz, Langenberg, Untermhaus) and of the agrarian places in 1647, 1794 and 1867; growth in houses; classification of places in 1647 into town, official villages, mixed villages and noble villages; manorial estates; territories of the lordship of Gera.",
   ["Industrieorte", "Agrarorte", "Rittergüter", "Amtsdörfer", "Herrschaft Gera", "Osterstein", "Langenberg", "Caaschwitz", "Teilungsakten 1647"], ["industrial places", "agrarian places", "manors", "official villages", "lordship of Gera", "partition records 1647"], ["Bevölkerung", "Rittergut", "Territorialgeschichte"])
pg("414", "Herrschaftsgeschichte des Gebiets Gera: Erwerbungen der Vögte von Weida und Gera (Gerichtsbarkeit 1237, Caaschwitz 1295, Langenberg 1328 und 1364), Lehnsherrlichkeit der Wettiner und der Krone Böhmen bis 1807; Liste der Regenten der geraischen Linie; Fußnote zu Quedlinburger Einkünften.",
   "History of rule over the Gera territory: acquisitions by the advocates of Weida and Gera (jurisdiction 1237, Caaschwitz 1295, Langenberg 1328 and 1364), feudal overlordship of the Wettins and the Crown of Bohemia until 1807; list of rulers of the Gera line; footnote on Quedlinburg revenues.",
   ["Vögte von Weida", "Vögte von Gera", "Quedlinburg", "Langenberg", "Wettiner", "Böhmen", "Regenten", "Heinrich", "Lehnsherrlichkeit"], ["advocates of Weida", "advocates of Gera", "Quedlinburg", "Wettin", "Bohemia", "rulers", "feudal overlordship"], ["Vögte von Weida", "Territorialgeschichte", "Genealogie"])
pg("415", "Fortsetzung der Regentenfolge der geraischen Linie bis zur Vereinigung unter Fürstenhaus Schleiz 1848 (Heinrich LXII., LXVII., XIV.); Beginn des Artikels Osterstein, Residenzschloss ¼ Stunde nordwestlich von Gera, mit Lage und Fußnote zu den elf Schlössern des Fürstentums.",
   "Continuation of the succession of rulers of the Gera line to the unification under the house of Schleiz in 1848 (Heinrich LXII, LXVII, XIV); start of the article on Osterstein, residence castle a quarter hour northwest of Gera, with its location and a footnote on the eleven castles of the principality.",
   ["Osterstein", "Residenzschloss", "Regenten", "Heinrich LXVII.", "Fürstenhaus Schleiz", "Gera", "Schlösser", "1848"], ["Osterstein", "residence castle", "rulers", "house of Schleiz", "castles", "1848"], ["Burgen und Schlösser", "Fürstenhaus", "Genealogie"])
pg("416", "Osterstein: Baugeschichte der ehemaligen Reichsburg, Wehrturm aus dem 11./12. Jahrhundert, Sagen vom kopflosen Reiter und Otternkönig, Namensdeutung (Hainberg), erste Erwähnung 1234, Residenz seit 1450; Nordflügel 1468–1470.",
   "Osterstein: building history of the former imperial castle, defensive tower from the 11th/12th century, legends of the headless rider and the otter king, name etymology (Hainberg), first mention 1234, residence from 1450; north wing 1468-1470.",
   ["Osterstein", "Reichsburg", "Wehrturm", "Sagen", "Otternkönig", "Hainberg", "Sorben", "Geschichte"], ["Osterstein", "imperial castle", "keep", "legends", "otter king", "Hainberg"], ["Burgen und Schlösser", "Sagen", "Mittelalter"])
pg("417", "Osterstein: Um- und Neubauten 1526 bis 1864 unter Heinrich II., XVIII., LXII., LXXII. und LXVII., Ahnensaal, Sammlungen, Auffahrt von Untermhaus, Schlosskapelle des heiligen Georg und Restaurierung 1852, Glocken 1451 und 1454, Hofprediger und Garnisonprediger.",
   "Osterstein: alterations and new building from 1526 to 1864 under Heinrich II, XVIII, LXII, LXXII and LXVII, ancestral hall, collections, the approach road from Untermhaus, the castle chapel of St George and its restoration in 1852, bells of 1451 and 1454, court and garrison preachers.",
   ["Osterstein", "Schlosskirche", "Ahnensaal", "Hofprediger", "Georgskapelle", "Heinrich XVIII.", "Heinrich LXVII.", "Glocken", "Marstall"], ["Osterstein", "castle church", "ancestral hall", "court preacher", "bells", "stables"], ["Burgen und Schlösser", "Kirchengebäude", "Fürstenhaus"])
pg("418", "Schluss des Artikels Osterstein (Umgebung, Sagen, Rentendistrict mit Waldungen und Vorwerken); Beginn von Ernsee, Dörfchen 3/4 Stunde westlich von Gera: historische Namensformen, Häuser, Einwohner, Vieh, Pfarr- und Schulzugehörigkeit zu Frankenthal, Kammergut.",
   "End of the article on Osterstein (surroundings, legends, rent district with woods and outlying farms); start of Ernsee, a small village three quarters of an hour west of Gera: historical name forms, houses, inhabitants, livestock, parish and school affiliation with Frankenthal, crown estate.",
   ["Osterstein", "Rentendistrict", "Ernsee", "Kammergut", "Frankenthal", "Viehbestand", "Wolfsbrücke", "Torstensohn"], ["Osterstein", "rent district", "Ernsee", "crown estate", "Frankenthal", "livestock"], ["Burgen und Schlösser", "Dorf", "Kammergut"])
pg("419", "Schluss von Ernsee (Gemeindefinanzen, Berufe, Flur 677 11/15 Morgen, Flurnamen, Namensdeutungen, sorbischer Ursprung) und Wüstung Pottendorf nördlich von Ernsee als alter Kultort mit Marienkirchlein und Wallfahrt.",
   "End of Ernsee (municipal finances, occupations, field area of 677 11/15 Morgen, field names, name etymologies, Sorbian origin) and the deserted settlement of Pottendorf north of Ernsee as an old cult site with a small Marian church and pilgrimage.",
   ["Ernsee", "Pottendorf", "Wüstung", "Wallfahrt", "Marienbild", "Flur", "Gemeindefinanzen", "Namensdeutung", "Hollapuppe"], ["Ernsee", "Pottendorf", "deserted settlement", "pilgrimage", "Marian image", "field area"], ["Dorf", "Wüstung", "Gemeindefinanzen", "Ortsname"])
pg("420", "Schluss von Pottendorf (Zerstörung, Steine für Kirchenbauten); Beginn von Untermhaus, Kirch- und Pfarrdorf am Fuß des Osterstein: Lage, Einwohner 1731, Häuser, Vieh, Straßen, Bestandteile (Gries), Vorburg und Kammergut, Justizamt.",
   "End of Pottendorf (destruction, stones reused for church buildings); start of Untermhaus, a church and parish village at the foot of Osterstein: location, 1,731 inhabitants, houses, livestock, streets, constituent parts (Gries), outer bailey and crown estate, justice office.",
   ["Untermhaus", "Pottendorf", "Gries", "Osterstein", "Kammergut", "Vorburg", "Justizamt", "Einwohner", "Häuser"], ["Untermhaus", "Pottendorf", "Gries", "outer bailey", "crown estate", "justice office"], ["Dorf", "Wüstung", "Gemeinden"])
pg("421", "Untermhaus: Kammergut und Amthaus, Kirche (15. Jahrhundert) mit Marienbild \"Puppe\" und Altarschrein, Puppenzins, Parochie seit 1736, Garnisonkirche, Orgel 1738, Kirchenvermögen, Beginn der Schulgeschichte.",
   "Untermhaus: crown estate and former office building, church (15th century) with the Marian image 'Puppe' and altar shrine, 'Puppenzins' dues, parish since 1736, garrison church, organ of 1738, church assets, start of the school history.",
   ["Untermhaus", "Kirche", "Marienbild", "Puppe", "Parochie 1736", "Garnisonkirche", "Orgel", "Hofprediger", "Kirchenbücher"], ["Untermhaus", "church", "Marian image", "parish 1736", "garrison church", "organ"], ["Kirchengebäude", "Pfarreien", "Dorf"])
pg("422", "Untermhaus: Schule (320 Schüler), Agnesschule 1869, Gasthof, Mühlen, Gemeindefinanzen, Berufe (Maurer, Schneider usw.), Armenzahl, Pest und Cholera, Hochwasser 1709, Küchengarten von 1729.",
   "Untermhaus: school (320 pupils), Agnesschule of 1869, inn, mills, municipal finances, occupations (masons, tailors etc.), number of poor, plague and cholera, flood of 1709, kitchen garden of 1729.",
   ["Untermhaus", "Schule", "Agnesschule", "Gemeindefinanzen", "Handwerker", "Porzellanfabrik", "Cholera", "Küchengarten", "Armenhaus"], ["Untermhaus", "school", "municipal finances", "craftsmen", "porcelain factory", "cholera", "kitchen garden"], ["Schule", "Gemeindefinanzen", "Berufe", "Dorf"])
pg("423", "Schluss von Untermhaus (Küchengarten); Cuba, Dörfchen ⅓ Stunde nordwestlich von Gera (328 Einwohner, Häuser, Vieh, Gewerbe, Mühle, Kupferhammer 1590, Steingutfabrik, Dichter Nündel); Beginn von Roschitz, Dorf der altenburgischen Exclave im Bramenthal.",
   "End of Untermhaus (kitchen garden); Cuba, a small village a third of an hour northwest of Gera (328 inhabitants, houses, livestock, trades, mill, copper hammer 1590, earthenware factory, poet Nündel); start of Roschitz, a village in the Altenburg exclave in the Brame valley.",
   ["Untermhaus", "Cuba", "Mühle", "Kupferhammer", "Steingutfabrik", "Roschitz", "Altenburger Exklave", "Bramenthal"], ["Untermhaus", "Cuba", "mill", "copper hammer", "earthenware factory", "Roschitz", "Altenburg exclave"], ["Dorf", "Mühlen", "Industrie"])
pg("424", "Roschitz: gemischte Landeshoheit der altenburgischen und reußischen Gemeinde, Lage im Bramenthal, reußischer Teil mit 5 Häusern und 32 Einwohnern, Kirche (1846), Pfarrei, Schule, Patronat, Rittergut der Familie von Schauroth.",
   "Roschitz: mixed territorial sovereignty of the Altenburg and Reuss municipalities, location in the Brame valley, Reuss portion with 5 houses and 32 inhabitants, church (1846), parish, school, patronage, manor of the von Schauroth family.",
   ["Roschitz", "Bramenthal", "Altenburger Exklave", "Gemischte Landeshoheit", "Kirche", "Patronat", "Rittergut", "Schauroth"], ["Roschitz", "Brame valley", "Altenburg exclave", "mixed sovereignty", "church", "patronage", "manor"], ["Dorf", "Rittergut", "Pfarreien"])

# ------------------------------------------------------------------ glossary
G.append({"term": "Kammergut", "variants": ["Kammergutsgebäude"], "kind": "institution", "de": "Landesherrliches Gut, das von der fürstlichen Kammer (Domänenverwaltung) bewirtschaftet bzw. verpachtet wird.", "en": "Estate of the prince administered or leased by the princely chamber (domain administration).", "pages": ["418", "420"]})
G.append({"term": "Amtsdorf", "variants": ["Küchendorf", "Amts- und Küchendörfer", "Mischdorf"], "kind": "term", "de": "Nach den Teilungsakten von 1647: Dorf, das dem landesherrlichen Amt unterstand (Amts- bzw. Küchendorf); Mischdörfer waren herrschaftlich-adlig geteilte Orte.", "en": "In the 1647 partition records: a village subject to the princely office (official or kitchen village); mixed villages were divided between ruler and nobility.", "pages": ["413"]})
G.append({"term": "Ortskunde", "variants": [], "kind": "term", "de": "Brückners Bezeichnung für die ortsweise Landesbeschreibung des II. Teils.", "en": "Brückner's term for the place-by-place description of Part II.", "pages": ["405"]})
G.append({"term": "Thlr.", "variants": ["Thaler", "Sgr.", "Pf."], "kind": "currency", "de": "Thaler (Thlr.), die Währungseinheit der Gemeindefinanzen in den Ortsartikeln; Unterteilung in Silbergroschen (Sgr.) und Pfennige (Pf.), wie im Haushaltsplan der Stadt Gera (S. 438).", "en": "Thaler (Thlr.), the currency unit of the municipal finances in the place articles; subdivided into silver groschen (Sgr.) and pfennigs (Pf.), as in the budget of the town of Gera (p. 438).", "pages": ["419", "422", "438"]})
G.append({"term": "Poppenzins", "variants": ["Puppenzins"], "kind": "term", "de": "Abgabe (Geld, Brot, eine Henne) an die Marienkirche, die vom ursprünglichen Pottendorf nach Untermhaus übertragen wurde.", "en": "Dues (money, bread, a hen) owed to the Marian church that passed from Pottendorf to Untermhaus.", "pages": ["419", "421"]})
G.append({"term": "Fröhner", "variants": ["frohnen"], "kind": "term", "de": "Dienstpflichtige, die Frondienste für eine Herrschaft zu leisten hatten.", "en": "Subjects owing corvée labour to a lord.", "pages": ["418", "423"]})
G.append({"term": "Kemnate", "variants": [], "kind": "term", "de": "Burgmannensitz, festes Steinhaus (wörtlich beheizbares Haus), hier Sitz eines ostersteiner Burgmannes.", "en": "Seat of a castle-man, fortified stone house; here the seat of a burgman of Osterstein.", "pages": ["423", "424"]})
G.append({"term": "Hauderer", "variants": [], "kind": "term", "de": "Lohnkutscher, Fuhrmann, der Fahrten gegen Bezahlung anbietet.", "en": "Hired coachman or carter offering transport for payment.", "pages": ["422"]})
