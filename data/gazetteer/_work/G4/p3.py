from h import *

ENTRIES = []

# ---------------------------------------------------------------- Tanna
e = base("tanna", "Tanna", S(684, "b1"), S(689, "b1"), "Stadt", "kleine Stadt, die höchste und lustigste, an Volkszahl die fünfte des Landes")
e.update({
    "historic_forms": HF(("Tan", 1240), ("Tanna", 1310), "Tann", "Thanna", ("Markt zur Than", 1533)),
    "dialect_form": "die Tann",
    "first_mention_year": 1240,
    "location": LOC("zwischen Saalburg und Plauen, 3 Stunden W. von dieser, 2 Stunden O. von jener, gleichweit SSO. von Schleiz und NNO. von Hirschberg entfernt",
                    "Saalburg", 2, "O"),
    "parish": {"status": "Pfarrort", "verbatim": "Oberpfarrei und Diaconat; Parochie mit Frankendorf und den Filialen Schilbach und Zollgrün"},
    "school": {"exists": True, "pupils": 350},
    "houses": 216,
    "inhabitants": 1801,
    "occupations": {"Webermeister": 141, "Weber-Gesellen": 31, "Bürger (Oeconomie als Hauptgeschäft)": 50, "Taglöhner": 26, "Knechte": 17,
                    "Mägde": 26, "Kapitalisten": 21, "Ortsarme": 13, "Handelsconcessionisten": 10, "Kaufleute": 5, "Garnhändler": 3, "Fuhrwerker": 7},
    "crafts": {"Schuhmacher": 40, "Spinner": 24, "Fleischer": 16, "Gerber": 14, "Bäcker": 11, "Schneider": 11, "Schmiede": 8, "Strumpfwirker": 8,
               "Tischler": 6, "Wagner": 5, "Schlosser": 4, "Seiler": 4, "Böttcher": 3, "Kürschner": 3, "Putzmacherinnen": 3, "Drechsler": 2,
               "Färber": 2, "Glaser": 2, "Maurer": 2, "Nagelschmiede": 2, "Barbier": 1, "Klemptner": 1, "Sattler": 1, "Seifensieder": 1, "Töpfer": 1},
    "flur_morgen": 5439.33,
    "flur_verbatim": "5439 1/3 Morgen",
    "soil": "theilweise gut und ergiebig",
    "livestock": {"Pferde": 28, "Rinder": 386, "Schafe": 4, "Schweine": 191, "Ziegen": 103, "Esel": 1, "Bienenstöcke": 3, "Gänse": 228},
    "municipal_finances": {"verbatim": "Der Communalgrundbesitz umfasst außer den Gebäuden im Werthe von 58,250 Thlr. noch 42 Morgen Land ... gegen 10,000 Thlr. im Werthe. An Außenständen hat die Gemeinde 500 Thlr., an Schulden 8500 Thlr. Ihre Jahreseinnahme (1865) 3736 Thlr., ihre Ausgabe 3155 Thlr.",
                           "assets_thaler": 58250, "debts_thaler": 8500, "expenditure_thaler": 3155, "income_thaler": 3736, "year": 1865},
    "facilities": ["Kirche (St. Andreas)", "Oberpfarrei", "Diaconat", "Schule (vier Lehrer)", "Rathaus mit Rathskeller", "Armenhaus", "Brauhaus",
                   "Schützenhaus", "Spritzenhäuser (zwei)", "Gasthöfe (drei)", "Apotheke", "Wassermühle (Angermühle)", "Windmühle",
                   "städtische Ziegelei", "Brauverein", "Schützenverein", "Gesangverein", "Kram- und Viehmärkte (sieben)", "Arzt", "Thierarzt",
                   "Gensd'arm", "Revierförster", "Leichenfiscus"],
    "subplaces": [
        SP("Angermühle", "Mühle", 687, "Wassermühle der Stadt; die Mittelmühle in der tannaer Flur gehört politisch zu Frankendorf (Fußnote S. 687)"),
        SP("Anger", "Weiler", 684, "späterer Anbau, gilt als Vorstadt"),
        SP("Kapellenhöhe", "Sonstiges", 684, "Wallfahrtskapelle, erster Cultpunkt des Ortes und der Gegend"),
    ],
    "events": EV(
        (1232, "Pfarrer Berthold von Tanna urkundlich erwähnt", "parish priest Berthold of Tanna documented"),
        (1279, "Patronat der Kirche an den Deutschen Orden", "patronage of the church passes to the Teutonic Order"),
        (1494, "Stadt- und Marktgerechtigkeit durch Heinrich d. m. von Schleiz", "town and market rights granted by Heinrich the Middle of Schleiz"),
        (1545, "Stadt erwirbt von den v. Rußwurm deren Gerechtsame um 1150 Mk.", "the town acquires the rights of the v. Rußwurm for 1150 marks"),
        (1581, "Erwerb der Gerechtsame der v. Kospod um 60 Mk.", "acquisition of the rights of the v. Kospod for 60 marks"),
        (1626, "Pest tötet 195 Personen", "plague kills 195 people"),
        (1640, "Schweden zünden die Stadt an (16. Mai): alle Häuser bis auf drei", "Swedes set the town on fire (16 May): all houses but three"),
        (1713, "furchtbare Wasserfluth", "terrible flood"),
        (1783, "Erdbeben", "earthquake"),
        (1806, "Corps des Marschalls Ney haust hier (9.-11. Oktober); Brand von 8 Häusern und 7 Scheunen", "Marshal Ney's corps ravages the town (9–11 October); fire destroys 8 houses and 7 barns"),
        (1844, "Brand: 17 Häuser und das Rathaus (28. November)", "fire: 17 houses and the town hall (28 November)"),
        (1846, "Rathaus neu erbaut", "town hall rebuilt"),
        (1857, "Brand: 52 Häuser, darunter die Schule", "fire: 52 houses, including the school"),
        (1866, "Brand: 25 Häuser (30. Oktober)", "fire: 25 houses (30 October)"),
    ),
    "persons": ["Berthold", "Heinrich v. Tepen", "Balthasar v. Kospod", "Christoph Mülser", "Herm. Braun", "Clem. Pätz", "Joh. Georg Carl"],
    "summary_de": "Kleine Stadt, höchste und fünftgrößte des Landes (1801 Einwohner), in einem flachen Kessel der oberen Wettera, oft von Bränden heimgesucht. Der Artikel beschreibt Lage, Gassen und Gebäude, die Kirche und die ausgedehnte Parochie (Frankendorf, Filiale Schilbach und Zollgrün), Schule mit 350 Kindern, Rathaus, Gemeindefinanzen, Gewerbe (141 Webermeister, 40 Schuhmacher) und Viehhandel sowie die Geschichte seit der Stadtrechtsverleihung 1494, Kriegsschäden und Brände (1640, 1844, 1857, 1866).",
    "summary_en": "Small town, the highest and fifth largest of the principality (1801 inhabitants), in a flat basin of the upper Wettera and repeatedly ravaged by fires. The article covers location, streets and buildings, the church and its extensive parish (Frankendorf, filials Schilbach and Zollgrün), the school with 350 children, town hall, municipal finances, trades (141 master weavers, 40 shoemakers) and cattle trade, and the history since the grant of town rights in 1494, war damage and fires (1640, 1844, 1857, 1866).",
    "notes": "Familien 421; Privathäuser 216 (und mehrere Brandstätten), circa 145 Scheunen, 10 öffentliche Gebäude. Assets: 58,250 Thlr. Gebäude; dazu 42 Morgen Land im Wert von gegen 10,000 Thlr. Wüstungen Kämmera, Weidendorf und Dittersdorf haben eigene Absätze (eigene Einträge). Stadtwaldboden 18 1/2 Morgen (Fußnote).",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Kämmera
e = base("kaemmera", "Kämmera", S(689, "b2"), S(689, "b2"), "Wüstung", "Wüstung", True)
e.update({
    "location": LOC("im S. von Tanna, am Ursprunge der Wettera", "Tanna", None, "S"),
    "events": EV((1533, "bereits als wüster Ort bezeugt (Kirchenvisitationsacten)", "already documented as a deserted place (church visitation records)")),
    "summary_de": "Wüstung im Süden von Tanna am Ursprung der Wettera, schon 1533 ein wüster Ort; die Stätte vermutet Brückner in den großen Wiesen, wo man noch zu Beginn des Jahrhunderts Keller fand. Der Wüstungsbezirk war Besitz des Deutschen Ordens und kam an die Oberpfarrei Tanna, der die Wiesen noch gehören; die Sage kennt hier ein Schloss dreier Fräulein.",
    "summary_en": "Deserted settlement south of Tanna at the source of the Wettera, already deserted in 1533; Brückner places its site in the large meadows where cellars were still found early in the century. The whole district belonged to the Teutonic Order and passed to the chief parsonage of Tanna, which still owns the meadows; legend tells of a castle of three maidens here.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Weidendorf
e = base("weidendorf", "Weidendorf", S(689, "b3"), S(689, "b3"), "Wüstung", "Wüstung", True)
e.update({
    "location": LOC("dicht zur Seite der Kämmera, nach Willersdorf zu", "Kämmera"),
    "summary_de": "Wüstung dicht neben der Kämmera nach Willersdorf zu, an der Willersdorf Anteil hat; die Stelle heißt noch Weidendorf. Nach der Sage zogen die Einwohner im Dreißigjährigen Krieg nach Tanna, doch erwähnt keine Quelle den Ort. Die Reuthwiesen gehören zu ihm.",
    "summary_en": "Deserted settlement just beside the Kämmera towards Willersdorf, in which Willersdorf has a share; the spot is still called Weidendorf. Legend says the inhabitants moved to Tanna during the Thirty Years' War, but no historical source mentions the place. The Reuthwiesen meadows belong to it.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Dittersdorf (Wüstung bei Tanna)
e = base("dittersdorf-tanna", "Dittersdorf", S(689, "b4"), S(690, "b1"), "Wüstung", "Wüstung", True)
e.update({
    "historic_forms": HF(("Dytrichstorf", 1367), ("Dytrichsdorf", 1368)),
    "dialect_form": "Ditters, Dittersch",
    "first_mention_year": 1367,
    "location": LOC("zwischen Tanna, Willersdorf und der Kämmera", "Tanna"),
    "events": EV(
        (1367, "Heinrich von Gera übergibt Dytherichstorf bei der Tanna dem Kloster zum heil. Kreuz", "Heinrich of Gera gives Dytherichstorf near Tanna to the Holy Cross convent"),
        (1368, "Heinrich von Oschitz verkauft dem Kloster seine Güter in Dytrichsdorf", "Heinrich of Oschitz sells his estates at Dytrichsdorf to the convent"),
    ),
    "persons": ["Heinrich von Gera", "Heinrich von Oschitz"],
    "summary_de": "Wüstung zwischen Tanna, Willersdorf und der Kämmera, nicht zu verwechseln mit Wüst-Dittersdorf an der Wisentthal bei Schleiz. 1367 und 1368 noch bestehend (Übergabe und Verkauf von Gütern an das Kloster zum heil. Kreuz), vor der Reformation wüst geworden; die genaue Lage ist unbekannt, der Name lebt im Dittersweg bei Willersdorf fort.",
    "summary_en": "Deserted settlement between Tanna, Willersdorf and the Kämmera, not to be confused with Wüst-Dittersdorf on the Wisenthal near Schleiz. Still existing in 1367 and 1368 (gift and sale of estates to the Holy Cross convent), it was deserted before the Reformation; its exact site is unknown and the name survives in the Dittersweg near Willersdorf.",
    "notes": "Im Register unter Tanna (Parent) als Wüstung geführt; id mit Zusatz zur Unterscheidung vom Wüst-Dittersdorf bei Schleiz.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Frankendorf
e = base("frankendorf", "Frankendorf", S(690, "b2"), S(691, "b1"), "Dorf", "kleines Dorf")
e.update({
    "historic_forms": HF(("Brankendorf", 1350)),
    "dialect_form": "Frankendorf",
    "first_mention_year": 1350,
    "location": LOC("1/4 Stunde N. von Tanna, in demselben Landkessel, am Fuße der Ahornhöhe und an der Wettera", "Tanna", 0.25, "N"),
    "parish": {"status": "eingepfarrt", "church_of": "Tanna", "verbatim": "schult, pfarrt, begräbt, verkehrt und blickt nach Tanna, daher gleichsam dessen Vorstadt"},
    "school": {"exists": False},
    "houses": 39,
    "inhabitants": 245,
    "occupations": {"Taglöhner": 17, "Almosener": 2},
    "crafts": {"Maurer": 11, "Müller": 2, "Schmiede": 2, "Ziegelbrenner": 2},
    "flur_morgen": 1547.33,
    "flur_verbatim": "1547 1/3 Morgen (davon über 1000 Morgen Rittergut)",
    "livestock": {"Pferde": 13, "Rinder": 122, "Schafe": 290, "Schweine": 61, "Ziegen": 34, "Gänse": 90, "Bienenstöcke": 11},
    "municipal_finances": {"verbatim": "besitzt die Gemeinde, von einem Ortsbeamten verwaltet, nur einige Grundstücke im Werthe von 300 Thlr. Ihre Jahresausgabe macht circa 70 Thlr., davon 50 Thlr. für die Ortsarmen.",
                           "assets_thaler": 300, "expenditure_thaler": 70},
    "facilities": ["Rittergut mit Herrnhaus", "Gemeindehaus", "Armenhaus", "Privatschenke", "Mittelmühle", "Mahl- und Schneidemühle", "Ziegelei",
                   "Brennerei", "Knochenmühle", "Feuerspritze", "Schäferei auf der Sophienhöhe"],
    "subplaces": [
        SP("Mittelmühle", "Mühle", 690, "Mahl-, Oel- und Schneidemühle in der tannaer Flur, politisch zu Frankendorf gehörig"),
        SP("Angermühle", "Mühle", 690, "Register nennt Angermühle bei Frankendorf (S. 690); im Text beschreibt der Absatz die 'frankendorfer Mahl- und Schneidemühle'"),
        SP("Schäferei auf der Sophienhöhe", "Vorwerk", 690, "zum Rittergut gehörig"),
    ],
    "events": EV(
        (1350, "Reichsvoigt Heinrich zu Gera schenkt dem Kloster zum heil. Kreuz Geldzinsen zu Frankendorf", "Imperial Voigt Heinrich of Gera donates money rents at Frankendorf to the Holy Cross convent"),
        (1863, "drei Wohnhäuser brennen ab (18. Dezember)", "three dwelling houses burn down (18 December)"),
    ),
    "persons": ["v. Kospod", "Gottl. Knoch", "Kühn"],
    "summary_de": "Kleines Dorf eine Viertelstunde nördlich von Tanna im selben Landkessel, mit Tanna kirchlich, schulisch und wirtschaftlich verbunden (gleichsam dessen Vorstadt); 39 Privathäuser und 245 Seelen. Den Kern bildet das Rittergut der Familie v. Kospod (jetzt Lederfabrikant Knoch); die Flur umfasst 1547 1/3 Morgen, davon über 1000 Morgen des Gutes, mit Roggenbau und Torfstich. Brückner hält den Ort für deutschen Ursprungs.",
    "summary_en": "Small village a quarter hour north of Tanna in the same basin, tied to Tanna in church, school and daily life (almost its suburb); 39 private houses and 245 souls. Its core is the manor of the v. Kospod family (now owned by the leather manufacturer Knoch); the land measures 1547 1/3 Morgen, over 1000 of them belonging to the manor, with rye cultivation and peat cutting. Brückner considers the village of German origin.",
    "notes": "Einwohner 1864: 217. Nach dem Register ist die Angermühle Bestandtheil von Frankendorf (S. 690).",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Schilbach
e = base("schilbach", "Schilbach", S(691, "b2"), S(692, "b2"), "Dorf", "Kirchdorf")
e.update({
    "historic_forms": HF(("Schiltpach", 1325), "Schilbach", ("Schielbach", 1647), "Schildbach", "Schillbach"),
    "dialect_form": "Schilbich",
    "first_mention_year": 1325,
    "location": LOC("2 Stunden fast S. von Schleiz, 1 1/2 Stunden OSO. von Saalburg und 1/2 Stunde W. von Tanna, an der alten Straße von Tanna nach Saalburg",
                    "Schleiz", 2, "S"),
    "parish": {"status": "Kirchdorf", "church_of": "Tanna", "verbatim": "Die Kirche, ein Filial von Tanna; Ortspfarrer ist der tannaer Diaconus"},
    "school": {"exists": True, "pupils": 60},
    "houses": 56,
    "inhabitants": 336,
    "occupations": {"Bauern": 27, "Häusler": 13, "Taglöhner": 14, "Dienstboten": 35, "Kapitalisten": 1, "Almosener": 5},
    "crafts": {"Zimmerleute": 13, "Maurer": 5},
    "flur_morgen": 3084,
    "flur_verbatim": "3084 Morgen (darunter 1185 5/7 Morgen Feld, 846 5/7 Morgen Wald, 752 11/20 Morgen Wiesen)",
    "soil": "größtentheils von ergiebigem Boden",
    "livestock": {"Pferde": 11, "Rinder": 306, "Schafe": 563, "Schweine": 75, "Ziegen": 39, "Gänse": 322, "Bienenstöcke": 11},
    "municipal_finances": {"verbatim": "Die Gemeinde hat geringen Grundbesitz, dazu Schulden und 239 2/3 Thlr. Jahresausgabe.", "expenditure_thaler": 239.67},
    "facilities": ["Kirche", "Schule", "Armenhaus", "Spritzenhaus", "Rittergut", "Feuerspritze", "Gemeindeschenke", "Bier- und Branntweinschank", "Ziegelei",
                   "Schäferei (Kammergut Seubtendorf)", "Gasthof an der hofer Straße bei der Kapelle"],
    "subplaces": [
        SP("Kapelle, Straßenwirthshaus", "Gasthof", 692, "Gasthof die Kapelle (im Volke die Kappel) auf der Kappelhöhe an der hofer Straße; dabei stand vordem eine Kapelle"),
    ],
    "events": EV(
        (1325, "Kloster zum heil. Kreuz erhält einen Hof vom Landesherrn", "Holy Cross convent receives a farm from the territorial lord"),
        (1518, "Kloster erhält durch Tausch einen halben Hof von Jobst v. Kospod", "the convent obtains half a farm by exchange from Jobst v. Kospod"),
        (1608, "Alex. v. Kospod im Duell getötet (Grabdenkmal)", "Alex. v. Kospod killed in a duel (memorial)"),
        (1732, "Kirche neu erbaut", "church rebuilt"),
        (1741, "Schulhaus neu erbaut (1741/42)", "school building erected (1741/42)"),
        (1771, "Rittergut an Graf Heinrich XXX. verkauft", "manor sold to Count Heinrich XXX"),
        (1802, "Rittergut um circa 30,000 Thlr. an die Familie Knoch", "manor sold for about 30,000 thalers to the Knoch family"),
        (1804, "fünf Bauernhöfe brennen ab", "five farms burn down"),
        (1864, "Brand: 20 Häuser (8. Mai)", "fire: 20 houses (8 May)"),
        (1865, "zwei Bauernhöfe brennen ab (14. Juli)", "two farms burn down (14 July)"),
    ),
    "persons": ["J. Aug. v. Kospod", "Alex. v. Kospod", "Heinrich XXX.", "v. Flanz", "Knoch"],
    "summary_de": "Kirchdorf südlich von Schleiz an der alten Straße Tanna–Saalburg mit 56 Privathäusern, Rittergut und 336 Einwohnern; Filial von Tanna, Pfarrer ist der tannaer Diaconus. Das Rittergut war lange bei den v. Kospod, seit 1802 bei der Familie Knoch; die ausgedehnte Flur von 3084 Morgen trägt nach Brückner das beste Korn der Gegend. Erwähnt werden Schule (60 Kinder), mehrere Brände und das Straßenwirtshaus Kapelle auf der Kappelhöhe.",
    "summary_en": "Church village south of Schleiz on the old Tanna–Saalburg road with 56 private houses, a manor and 336 inhabitants; a filial of Tanna, whose deacon serves as its pastor. The manor was long held by the v. Kospod family and by the Knoch family from 1802; the extensive 3084 Morgen of land bear, according to Brückner, the best grain of the district. The article mentions the school (60 children), several fires and the roadside inn Kapelle on the Kappelhöhe.",
    "notes": "Einwohner 1861: 356. Livestock Schafe 563 (Rittergut/Kammergut mitgezählt). Der Gasthof 'die Kapelle' (S. 692 b2, eigener Absatz) ist als subplace geführt.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Mangelsdorf (Wüstung)
e = base("mangelsdorf", "Mangelsdorf", S(692, "b3"), S(693, "b1"), "Wüstung", "Wüstung", True)
e.update({
    "historic_forms": HF(("Mangolstorff", 1318), ("Manigoldisdorf", 1365), ("Mansdorf", 1533)),
    "dialect_form": "Mansdorf",
    "first_mention_year": 1318,
    "location": LOC("im SW. von Schilbach nach Wernsdorf hin", "Schilbach", None, "SW"),
    "events": EV(
        (1318, "Friedrich v. Mangolzstorf urkundlich genannt (Geschlecht lebt noch 1408)", "Friedrich v. Mangolzstorf documented (the family still lived in 1408)"),
        (1365, "Besitz von den v. Magwitz um 234 Pfund Heller an das Kloster zum heil. Kreuz", "estate passes from the v. Magwitz to the Holy Cross convent for 234 pounds of Heller"),
        (1533, "noch im Besitz des Klosters (Mansdorf)", "still owned by the convent (Mansdorf)"),
    ),
    "persons": ["Friedrich v. Mangolzstorf"],
    "summary_de": "Wüstung südwestlich von Schilbach nach Wernsdorf hin; ein Bezirk aus Holz- und Wiesenstücken (Petersbach, Pingera, Romlera) heißt noch Mangelsdorf oder Mansdorf, auch Mauerreste sind vorhanden. Der Ort wurde angeblich im arnshaugker Erbschaftskrieg zerstört; 1365 kam er von den v. Magwitz an das Kloster zum heil. Kreuz bei Saalburg. Mit ihm bringt man das Feldstück Backofenacker in Verbindung.",
    "summary_en": "Deserted settlement southwest of Schilbach towards Wernsdorf; a district of woods and meadows (Petersbach, Pingera, Romlera) is still called Mangelsdorf or Mansdorf, and remains of walls survive. The place was allegedly destroyed in the Arnshaugk succession war; in 1365 it passed from the v. Magwitz to the Holy Cross convent near Saalburg. The field Backofenacker is linked with it.",
    "notes": "Im Artikel Saalburg (S. 672) als Mansdorf (1533 Klosterbesitz, in der seubtendorfer Markung) genannt; Brückner verweist dort auf Seubtendorf.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Zollgrün
e = base("zollgruen", "Zollgrün", S(693, "b2"), S(695, "b1"), "Dorf", "langgestrecktes, waldumschlossenes Kirchdorf")
e.update({
    "historic_forms": HF("Grün", ("Gotschalgsgrün", 1350), ("Grün", 1404), ("Gottschalgsgrün", 1443), ("Grün", 1533), ("Gottschalksgrün", 1533),
                         ("Zollgrün", 1604), ("Gottschalksgrün oder Zollgrün", 1647)),
    "dialect_form": "Zollgrie und Zollgre",
    "first_mention_year": 1350,
    "location": LOC("an der hofer Straße, 1 1/2 Stunden SOS. von Schleiz, 3/4 Stunde NW. von Tanna", "Schleiz", 1.5, "SSO"),
    "parish": {"status": "Kirchdorf", "church_of": "Tanna", "verbatim": "Die Kirche, ein Filial von Tanna, ... hat den Diaconus zu Tanna zum Pfarrer"},
    "school": {"exists": True, "pupils": 88},
    "houses": 70,
    "inhabitants": 457,
    "occupations": {"Bauern": 24, "Kühbauern": 13, "Häusler": 29, "Hausgenossen": 19, "Taglöhner": 19, "Dienstboten": 31, "Kapitalisten": 2, "Almosener": 1},
    "crafts": {"Zimmerleute": 18, "Maurer": 12, "Spinner": 10, "Weber": 3, "Müller": 2, "Schmiede": 2, "Schuhmacher": 2, "Böttcher": 1,
               "Fleischer": 1, "Schneider": 1, "Wirth": 1},
    "flur_morgen": 3083.5,
    "flur_verbatim": "3083 1/2 Morgen",
    "soil": "zum guten Theile ergiebig",
    "livestock": {"Pferde": 6, "Rinder": 295, "Schafe": 96, "Schweine": 90, "Ziegen": 63, "Gänse": 369, "Bienenstöcke": 23},
    "municipal_finances": {"verbatim": "an Grundbesitz 20 13/14 Morgen im Werthe von 440 Thlr., freilich auch mit 680 Thlr. Schulden belastet. Ihre Jahresausgabe macht an 340 Thlr.",
                           "assets_thaler": 440, "debts_thaler": 680, "expenditure_thaler": 340},
    "facilities": ["Kirche", "Schule", "Armenhaus", "Spritzenhaus", "Rittergut", "Gasthof (privat)", "Feuerspritze", "Wassermühlen (zwei)"],
    "subplaces": [
        SP("Grünmühle", "Mühle", 694, "Wassermühle im Wetterathal, wo der mielesdorfer Bach einmündet"),
        SP("Hammermühle", "Mühle", 694, "Wassermühle an der Stelle einer 1766 erbauten, 1838 eingegangenen Eisenhütte"),
        SP("Röhnig", "Weiler", 693, "oberer Teil des Ortes"),
        SP("Burgstädtel", "Schloss", 694, "ehemaliges Schlösschen jenseits der Wetterabrücke, wahrscheinlich im arnshaugker Krieg zerstört"),
    ],
    "events": EV(
        (1407, "Nicol. Schildknecht verkauft seine Lehen zu Gottschalksgrün an Heinrich, Herrn von Gera", "Nicol. Schildknecht sells his fiefs at Gottschalksgrün to Heinrich, lord of Gera"),
        (1618, "Rittergut mit 2300 Mk. angeschlagen", "manor valued at 2300 marks"),
        (1623, "Kirche erneuert und erweitert", "church renovated and enlarged"),
        (1647, "bis 1666 zu Saalburg geschlagen", "attached to Saalburg until 1666"),
        (1713, "Verwüstung durch den angeschwollenen Dorfbach (5. Juli)", "devastation by the swollen village stream (5 July)"),
        (1766, "Eisenhütte erbaut (1838 eingegangen)", "iron works built (closed 1838)"),
        (1807, "Gasthof und Schule brennen ab (10. Dezember)", "inn and school burn down (10 December)"),
        (1808, "Schulhaus neu erbaut", "school building rebuilt"),
    ),
    "persons": ["Ernst Gottl. v. Kospod", "Nicol. Schildknecht"],
    "summary_de": "Langgestrecktes, waldumschlossenes Kirchdorf an der hofer Straße südöstlich von Schleiz mit 70 Privathäusern und 457 Einwohnern; Filial von Tanna, Pfarrer ist der tannaer Diaconus. Das Rittergut war lange bei den v. Kospod, später bei den Familien v. Wolfersdorf, v. Beulwitz und Knoch. Behandelt werden Kirche, Schule (88 Kinder), Landwirtschaft und Handwerk (24 Bauern, Flur 3083 1/2 Morgen), die Namensentwicklung von Grün zu Zollgrün sowie Grünmühle und Hammermühle.",
    "summary_en": "Elongated, forest-ringed church village on the road to Hof, southeast of Schleiz, with 70 private houses and 457 inhabitants; a filial of Tanna, with the Tanna deacon as pastor. The manor was long held by the v. Kospod family, later by the v. Wolfersdorf, v. Beulwitz and Knoch families. The article covers the church, the school (88 children), farming and crafts (24 farmers, 3083 1/2 Morgen), the development of the name from Grün to Zollgrün, and the Grünmühle and Hammermühle.",
    "notes": "Einwohner 1861: 451. Schulbau 1808: 1223 2/3 Aßo; Kirchenvermögen 242 Thlr. Aktiva, 680 Thlr. Passiva.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Hermannsdorf (Wüstung)
e = base("hermannsdorf", "Hermannsdorf", S(695, "b2"), S(695, "b2"), "Wüstung", "Wüstung", True)
e.update({
    "historic_forms": HF(("Hermannstorf", 1362)),
    "dialect_form": "Herrnsdorf",
    "first_mention_year": 1362,
    "location": LOC("im Westen von Zollgrün am Wege nach Wernsdorf im waldigen Districte Romlera", "Zollgrün", None, "W"),
    "events": EV((1362, "Nickel v. Kospod verkauft Güter zu Hermannsdorf an das Kloster zum heil. Kreuz", "Nickel v. Kospod sells estates at Hermannsdorf to the Holy Cross convent")),
    "persons": ["Nickel v. Kospod"],
    "summary_de": "Wüstung westlich von Zollgrün am Weg nach Wernsdorf im waldigen Distrikt Romlera, an dem auch Wernsdorf Anteil hat. Die Wiesenstelle heißt im Flurbuch noch Herrnsdorf; 1362 bestand der Ort noch, als Nickel v. Kospod Güter an das Kloster zum heil. Kreuz verkaufte. Brückner weist auf mehrfache irrtümliche Verwechslung mit Wernsdorf hin.",
    "summary_en": "Deserted settlement west of Zollgrün on the road to Wernsdorf, in the wooded Romlera district in which Wernsdorf also has a share. The meadow where it stood is still called Herrnsdorf in the field register; in 1362 the village still stood when Nickel v. Kospod sold estates to the Holy Cross convent. Brückner points out that the place has often been confused with Wernsdorf.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Mielesdorf
e = base("mielesdorf", "Mielesdorf", S(695, "b3"), S(697, "b2"), "Dorf", "Pfarr-, Kirch- und Grenzdorf an Sachsen")
e.update({
    "historic_forms": HF(("Millersdorf", 1533), "Milesdorf", "Mielesdorf", "Mühlesdorf"),
    "dialect_form": "Mielesdorf",
    "first_mention_year": 1533,
    "location": LOC("1 1/2 Stunde SO. von Schleiz, am Grünbächlein, auf einer sanften Hochmulde", "Schleiz", 1.5, "SO"),
    "elevation": {"value": 1400, "unit": "Fuß", "verbatim": "an der Schwelle der Kirche 1400 Fuß hoch"},
    "parish": {"status": "Pfarrort", "verbatim": "Pfarr-, Kirch- und Grenzdorf; Waldhaus eingepfarrt"},
    "school": {"exists": True, "pupils": 80},
    "houses": 62,
    "inhabitants": 426,
    "occupations": {"Bauern": 29, "Feldhäusler": 15, "Kleinhäusler": 18, "Taglöhner": 9, "Dienstboten": 21, "Kapitalisten": 2, "Ortsarme": 2},
    "crafts": {"Maurergesellen": 10, "Zimmerleute": 7, "Schneider": 3, "Weber": 2, "Böttcher": 1, "Drechsler": 1, "Fleischer": 1, "Schmied": 1,
               "Tischler": 1, "Holzhändler": 1},
    "flur_morgen": 2381.25,
    "flur_verbatim": "2381 1/4 Morgen",
    "soil": "1/5 gut, 2/5 mittel, 2/5 gering",
    "livestock": {"Pferde": 2, "Rinder": 272, "Schafe": 121, "Schweine": 105, "Ziegen": 52, "Gänse": 350, "Bienenstöcke": 6},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere, wozu 14 Bauern gehören, außer dem Brauhause circa 3 Morgen (Anger und zwei Dorfsteiche) im Werthe von 200 Thlr., aber dagegen 1000 Thlr. Schulden; die weitere hat 400 Thlr. Schulden.",
                           "assets_thaler": 200, "debts_thaler": 1000},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Armenhaus", "Brauhaus", "Spritzenhaus", "Chausseehaus (Waldhaus)", "Schenkwirthschaft im Brauhaus",
                   "Branntweinschank (concessionirt)", "Feuerspritze", "Windmühle"],
    "subplaces": [
        SP("Waldhaus", "Einzelhof", 697, "Chausseehaus 1/4 Stunde NWN. von Mielesdorf im schleizer Walde; zu Kirche und Schule Mielesdorf gehörig"),
    ],
    "events": EV(
        (1483, "Glocke (zersprungen 1856), angeblich von der Klause", "bell (cracked in 1856), reportedly from the Klause"),
        (1527, "Kloster bei Saalburg erwirbt einen Acker im Schwant", "the convent near Saalburg acquires a field in the Schwant"),
        (1533, "erster lutherischer Pfarrer Jodocus Eckner", "first Lutheran pastor Jodocus Eckner"),
        (1634, "13 Tote durch die Pest", "13 deaths from the plague"),
        (1710, "großer Teil des Ortes brennt ab (10. Februar)", "a large part of the village burns down (10 February)"),
        (1719, "Kirche von Graf Heinrich XI. neu erbaut", "church rebuilt by Count Heinrich XI"),
        (1863, "Schulhaus ganz neu erbaut", "school building rebuilt"),
        (1865, "Brand: 11 Bauernhöfe und 2 Kleinhäuser (27. April)", "fire: 11 farms and 2 cottages (27 April)"),
    ),
    "persons": ["Jodocus Eckner", "Heinrich XI.", "J. Christoph Hainisch", "Rob. Gustav Schubert"],
    "summary_de": "Pfarr-, Kirch- und Grenzdorf an Sachsen, 1400 Fuß hoch südöstlich von Schleiz, mit 62 Privathäusern und 426 Einwohnern. Die Kirche (Gründung durch den Deutschen Orden, Neubau 1719 durch Graf Heinrich XI.) hat keinen Filial, nur das Waldhaus ist eingepfarrt; Schule mit rund 80 Kindern. Feldbau und Kleingewerbe sind Hauptbeschäftigung (29 Bauern, Flur 2381 1/4 Morgen); Brückner nennt den Ort sorbisch-deutsch. Am Artikelende folgen das Waldhaus (Chausseehaus) und die alte Klause.",
    "summary_en": "Parish, church and border village on the Saxon frontier, 1400 feet high southeast of Schleiz, with 62 private houses and 426 inhabitants. The church (founded by the Teutonic Order, rebuilt in 1719 by Count Heinrich XI.) has no filial, only the Waldhaus is attached; the school has about 80 children. Farming and small trades are the main occupations (29 farmers, 2381 1/4 Morgen); Brückner calls the settlement Sorbian-German. The Waldhaus (toll house) and the old Klause follow at the end of the article.",
    "notes": "Einwohner 1864: 439. Kirchenvermögen 312 Thlr. eisernes Kapital, Pfarrholzkapital circa 700 Thlr. Freigut/Vorwerk (1647 'jenkisches Freigut') im Dreißigjährigen Krieg öde.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Alte Klause
e = base("alte-klause", "Alte Klause", S(697, "b3"), S(698, "b1"), "Wüstung", "anmuthige Stelle im schleizer Walde (ursprünglich Kapelle, dann Klause, dann Einsiedlerhütte)", True)
e.update({
    "location": LOC("im schleizer Walde, NON. von Mielesdorf, nahe der sächsischen Grenze", "Mielesdorf", None, "NNO"),
    "events": EV(
        (1399, "Kapelle von der Gräfin Elisabeth, Gemahlin des Voigts Heinrich von Gera und Schleiz, gestiftet (Johannes dem Täufer und Bartholomäus)", "chapel founded by Countess Elisabeth, wife of Voigt Heinrich of Gera and Schleiz (St John the Baptist and St Bartholomew)"),
    ),
    "persons": ["Elisabeth von Schwarzburg", "Heinrich von Gera und Schleiz", "Heinrich Scherenberg", "Heinrich XII."],
    "summary_de": "Anmutige Stelle im schleizer Wald nordnordöstlich von Mielesdorf nahe der sächsischen Grenze: ursprünglich eine 1399 gestiftete Kapelle mit Wohnung für einen Kaplan und sechs bis acht Priester und Laienbrüder, nach der Reformation eine Sommerklause Graf Heinrichs XII. mit Gottesdienst, später eine Einsiedlerhütte. Nur der Name Klause ist der Stelle geblieben.",
    "summary_en": "Pleasant spot in the Schleiz forest north-northeast of Mielesdorf near the Saxon border: originally a chapel founded in 1399 with housing for a chaplain and six to eight priests and lay brothers, after the Reformation a summer retreat of Count Heinrich XII. with services, later a hermit's hut. Only the name Klause remains.",
    "notes": "Im Register als Wüstung geführt ('Alte Klause'); der Text schreibt 'Die alte Klause oder Klause'.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Unterkoskau
e = base("unterkoskau", "Unterkoskau", S(698, "b2"), S(699, "b1"), "Dorf", "Kirch-, Pfarr- und Grenzdorf")
e.update({
    "historic_forms": HF(("Koskode", 1325), ("Koskode", 1350), "Kozzebode", ("Coßka", 1533), "Unterkoska", "Unterkoskau"),
    "dialect_form": "Uenterkoßka",
    "first_mention_year": 1325,
    "location": LOC("2 1/2 Stunden SO. von Schleiz, an der Wisentthal, an der Straße von da nach Reuth", "Schleiz", 2.5, "SO"),
    "parish": {"status": "Pfarrort", "verbatim": "Zu ihr gehört Willersdorf als Filial und Oberkoskau als eingepfarrter Ort"},
    "school": {"exists": True, "pupils": 106},
    "houses": 79,
    "inhabitants": 482,
    "occupations": {"Bauern": 33, "Kühbauern": 9, "Häusler": 24, "Hausgenossen": 8, "Taglöhner": 12, "Dienstboten": 58, "Kapitalisten": 8, "Ortsarme": 1},
    "crafts": {"Maurer": 16, "Weber": 7, "Handelsconcessionisten": 3, "Schuhmacher": 3, "Zimmerleute": 3, "Schmiede": 2, "Schneider": 2, "Wagner": 2,
               "Böttcher": 1, "Müller": 1, "Mühlenbauer": 1},
    "flur_morgen": 3308.75,
    "flur_verbatim": "3308 3/4 Morgen",
    "soil": "mehr magerer, auf kalter Unterlage ruhender, als ergiebiger Boden",
    "livestock": {"Pferde": 14, "Rinder": 392, "Schafe": 61, "Schweine": 120, "Ziegen": 51, "Bienenstöcke": 28, "Gänse": 750},
    "municipal_finances": {"verbatim": "Die Gemeinde hat außer ihren Communalgebäuden und 1 1/2 Morgen enthaltenden Wegräumen (drei Communicationswegen) keinen Grundbesitz und kein Vermögen, aber auch keine Schulden; ihre Jahresausgabe macht 150 Thlr.",
                           "expenditure_thaler": 150},
    "facilities": ["Kirche", "Pfarrei", "Schule", "Gemeindehaus", "Brauhaus", "Spritzenhaus", "Gasthaus (privat)", "Gemeindeschenke", "Feuerspritzen (zwei)",
                   "Wassermühle (Schlagmühle) mit Schneide-, Oel- und Graupenmühle", "Ziegeleien (vier)"],
    "subplaces": [
        SP("Schlagmühle", "Mühle", 698, "Wassermühle mit Schneide-, Oel- und Graupenmühle"),
    ],
    "events": EV(
        (1325, "Kloster zum heil. Kreuz erhält 11 1/2 Mark Zinsen", "Holy Cross convent receives 11 1/2 marks of rent"),
        (1534, "Egid. Handsogel erster lutherischer Pfarrer", "Egid. Handsogel first Lutheran pastor"),
        (1606, "Kirche und Pfarrei samt Kirchenbüchern brennen ab", "church and parsonage burn down with the parish registers"),
        (1761, "Blitzschlag: 5 Bauernhöfe brennen ab (17. Mai)", "lightning strike: 5 farms burn down (17 May)"),
        (1772, "G. G. Friedrich Mayer geboren (gest. 1818 zu Gera)", "G. G. Friedrich Mayer born (died 1818 in Gera)"),
        (1802, "Pfarrwohnhaus mit 2000 Thlr. Unkosten erbaut", "parsonage built at a cost of 2000 thalers"),
        (1864, "Brand: 11 Bauernhöfe (14. August)", "fire: 11 farms (14 August)"),
    ),
    "persons": ["Johannes Sorgel", "Egid. Handsogel", "Conr. Ad. Schnädelbach", "G. G. Friedrich Mayer"],
    "summary_de": "Kirch-, Pfarr- und Grenzdorf an der Wisentthal südöstlich von Schleiz mit 79 Privathäusern und 482 Einwohnern; zur Pfarrei gehören Willersdorf als Filial und Oberkoskau. Aus dem Mittelalter stammte eine Kapelle des Deutschen Ordens, die erste lutherische Pfarrstelle wurde 1534 besetzt. Schule mit 106 Kindern (27 aus Oberkoskau), Landwirtschaft mit Viehzucht und Handwerk (36 Bauerngüter, Flur 3308 3/4 Morgen); Geburtsort von G. G. Friedrich Mayer.",
    "summary_en": "Church, parish and border village on the Wisenthal southeast of Schleiz with 79 private houses and 482 inhabitants; Willersdorf is its filial and Oberkoskau is attached to the parish. A chapel of the Teutonic Order stood here in the Middle Ages and the first Lutheran pastor took office in 1534. School with 106 children (27 from Oberkoskau), farming with cattle breeding and crafts (36 farms, 3308 3/4 Morgen); birthplace of G. G. Friedrich Mayer.",
    "notes": "Einwohner 1861 nicht angegeben. Kirchenvermögen 4420 Thlr. Fußnote: Kirchengallerie irrt bei Hermannsgrün. Ein Stück der Wüstung Traundorf ist zur Flur geschlagen (S. 699).",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Oberkoskau
e = base("oberkoskau", "Oberkoskau", S(699, "b2"), S(700, "b1"), "Dorf", "kleines Dorf")
e.update({
    "historic_forms": HF(("Obirnkostode", 1350), "major Koskoth", ("Obirnkozzkode", 1368)),
    "dialect_form": "Oberkoskä",
    "first_mention_year": 1350,
    "location": LOC("1/4 Stunde fast südlich von Unterkoskau, 1 Stunde östlich von Tanna, an der Wisentthal", "Unterkoskau", 0.25, "S"),
    "parish": {"status": "eingepfarrt", "church_of": "Unterkoskau", "verbatim": "wohin es pfarrt, schult und begräbt"},
    "school": {"exists": False},
    "houses": 22,
    "inhabitants": 137,
    "occupations": {"Bauern": 13, "Feldhäusler": 7, "Häusler": 3, "Taglöhner": 2, "Dienstboten": 18},
    "crafts": {"Maurer": 4, "Müller": 2, "Tischler": 1, "Zimmermann": 1},
    "flur_morgen": 1562,
    "flur_verbatim": "1562 Morgen",
    "soil": "1/4 guter, 3/4 geringer Feldboden",
    "livestock": {"Pferde": 4, "Rinder": 142, "Schafe": 109, "Schweine": 39, "Ziegen": 21, "Bienenstöcke": 7, "Gänse": 300},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt neben ihren 3 Häusern 5 1/8 Morgen Dorfraum und außer den Communicationswegen 2 11/14 Morgen Grasboden, dabei einige geringe Schulden; ihre Jahresbedürfnisse sind 90 Thlr.",
                           "expenditure_thaler": 90},
    "facilities": ["Gemeindehaus", "Spritzenhaus", "Brauhaus", "Gemeindeschenke", "Feuerspritze", "Ziegelei", "Obermühle", "Mittelmühle"],
    "subplaces": [
        SP("Obermühle", "Mühle", 699, "Mahl-, Schneide- und Oelmühle an der Wisentthal"),
        SP("Mittelmühle", "Mühle", 699, "Mahl-, Schneide- und Oelmühle an der Wisentthal"),
    ],
    "events": EV(
        (1350, "Heinrich, Voigt zu Gera, überlässt dem Kloster zum heil. Kreuz Geldzinsen (auch 1 Mark von Elisabeth v. Kospod)", "Heinrich, Voigt of Gera, cedes money rents to the Holy Cross convent (also 1 mark from Elisabeth v. Kospod)"),
        (1368, "Heinrich v. Oschitz überlässt dem Kloster seine Güter zu Oberkoskau", "Heinrich v. Oschitz cedes his estates at Oberkoskau to the convent"),
        (1633, "sieben junge Oberkoskauer fallen im benachbarten Stelzen (Oktober)", "seven young men of Oberkoskau are killed in neighbouring Stelzen (October)"),
        (1860, "acht Häuser der Südzeile brennen ab", "eight houses of the south row burn down"),
    ),
    "summary_de": "Kleines Dorf, eine Viertelstunde südlich von Unterkoskau an der Wisentthal, mit 22 Privathäusern und 137 Einwohnern; pfarrt, schult und begräbt nach Unterkoskau. Ackerbau mit Viehzucht überwiegt (13 Bauern, Flur 1562 Morgen), zwei Mühlen (Ober- und Mittelmühle) liegen nahe. Brückner beschreibt den sorbischen Ort, Güter der v. Kospod, den Brand von 1860 und Sagen.",
    "summary_en": "Small village a quarter hour south of Unterkoskau on the Wisenthal with 22 private houses and 137 inhabitants; church, school and burial are at Unterkoskau. Arable farming with cattle breeding predominates (13 farmers, 1562 Morgen) and two mills (Obermühle and Mittelmühle) lie nearby. Brückner describes this Sorbian settlement, the estates of the v. Kospod, the fire of 1860 and local legends.",
    "notes": "Einwohner 1864: 150. Die Schüler gehen nach Unterkoskau (27 Kinder, S. 698).",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Willersdorf
e = base("willersdorf", "Willersdorf", S(700, "b2"), S(702, "b2"), "Dorf", "kleines, hoch und kühl gelegenes Kirchdorf")
e.update({
    "historic_forms": HF(("Willesdorf", 1533), "Wilmersdorf", ("Willersdorf und Willesdorf", 1647)),
    "dialect_form": "Willesdorf",
    "first_mention_year": 1533,
    "location": LOC("1/2 Stunde SWS. von Unterkoskau und 3/4 Stunde SO. von Tanna", "Unterkoskau", 0.5, "SSW"),
    "parish": {"status": "Kirchdorf", "church_of": "Unterkoskau", "verbatim": "kam als Filial nach Unterkoskau, wohin er noch gehört"},
    "school": {"exists": True},
    "houses": 36,
    "inhabitants": 212,
    "occupations": {"Bauern": 26, "Häusler": 8, "Taglöhner": 2, "Dienstboten": 21, "Kapitalisten": 7},
    "crafts": {"Maurer": 3, "Müller": 2, "Schieferdecker": 2, "Zimmerleute": 2, "Schmied": 1, "Schneider": 1, "Weber": 1, "Tischler": 1},
    "flur_morgen": 2400.75,
    "flur_verbatim": "2400 3/4 Morgen",
    "soil": "von mittler Ergiebigkeit",
    "livestock": {"Pferde": 5, "Rinder": 243, "Schafe": 29, "Schweine": 58, "Ziegen": 22, "Bienenstöcke": 18, "Gänse": 150},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt 63 Morgen theils Hutung, theils Holz im Werthe von 600 Thlr., hat sonst weder Kapitalien noch Schulden und bedarf jährlich 124 Thlr.",
                           "assets_thaler": 600, "expenditure_thaler": 124},
    "facilities": ["Kirche", "Schule", "Gemeindehaus", "Brauhaus", "Spritzenhaus", "Gemeindeschenke (in Pacht)", "Feuerspritze"],
    "subplaces": [
        SP("Bucklischmühle", "Mühle", 701, "Mahl- und Schneidemühle an der Wisentthal, südlich des Dorfes"),
        SP("Ottenmühle", "Mühle", 701, "Mahl- und Schneidemühle an der Wisentthal, südlich des Dorfes"),
        SP("Ebersberg", "Weiler", 702, "1647 mit fünf, jetzt mit drei Höfen besetzt; pfarrte und schulte früher nach Tanna; Glied der Gemeinde Willersdorf"),
    ],
    "events": EV(
        (1620, "Kirche (die jetzige) in den Jahren 1620 bis 1623 errichtet", "present church erected in 1620–1623"),
        (1766, "zwei Bauernhöfe brennen ab", "two farms burn down"),
        (1823, "Schulhaus in ziemlichen Stand gesetzt", "school building put in fair order"),
        (1832, "Blitzschlag: drei Häuser neben der Kirche brennen ab (12. Juni)", "lightning strike: three houses next to the church burn down (12 June)"),
        (1868, "Kirche repariert", "church repaired"),
    ),
    "persons": ["v. Rohrscheidt"],
    "summary_de": "Kleines, hoch gelegenes Kirchdorf am Ebersberg mit 36 Privathäusern und 212 Einwohnern; Filial der Pfarrei Unterkoskau, bis zur Reformation nach Tanna gepfarrt. Die Kirche entstand 1620 bis 1623, die Schule bestand schon im 17. Jahrhundert; zum Ort zählen die Bucklisch- und die Ottenmühle und der Ebersberg, die Flur umfasst 2400 3/4 Morgen. 1690 wohnte hier die adlige Familie v. Rohrscheidt (früheres Freigut); Sagen vom Spuk am Zeidelbrunnen schließen den Artikel.",
    "summary_en": "Small, high-lying church village at the Ebersberg with 36 private houses and 212 inhabitants; a filial of the parish of Unterkoskau, and before the Reformation part of the parish of Tanna. The church was built in 1620–1623 and the school existed by the 17th century; the Bucklischmühle, Ottenmühle and the Ebersberg belong to it, and the land measures 2400 3/4 Morgen. The noble family v. Rohrscheidt lived here in 1690 (former Freigut). Legends of haunting at the Zeidelbrunnen close the article.",
    "notes": "Schulkinder durchschnittlich 35-40 (Spanne, daher kein Einzelwert). Kirchenvermögen 500 Thlr. Zum Pfarrbau trägt Willersdorf 1/4 bei. Zum Ort gehört nach dem Register auch der Ebersberg, dessen Absatz S. 702 b2 hier eingeschlossen ist.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Traundorf (Wüstung)
e = base("traundorf", "Traundorf", S(702, "b3"), S(702, "b3"), "Wüstung", "ein alter wüster Ort, jetzt Wald und Hutung umfassend", True)
e.update({
    "historic_forms": HF("Trauendorf"),
    "dialect_form": "Traudorf",
    "location": LOC("in einem oberen Nebengründchen des Lohbachs, zwischen Unterkoskau und Tanna", "Tanna"),
    "summary_de": "Alter wüster Ort in einem oberen Nebengründchen des Lohbachs zwischen Unterkoskau und Tanna, jetzt Wald und Hutung. An der Markung haben beide Koskau und Willersdorf Anteil; der Zeitpunkt des Eingehens als Dorf ist unbekannt, noch vor etwa 80 Jahren war ein Garten zu sehen.",
    "summary_en": "Old deserted settlement in an upper side valley of the Lohbach between Unterkoskau and Tanna, now woodland and pasture. Both Koskau villages and Willersdorf share in its fields; when it ceased to be a village is unknown, and a garden could still be seen there about 80 years earlier.",
    "notes": "Ein Stück der Wüstung ist zur Flur von Unterkoskau geschlagen (S. 699).",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Stelzen
e = base("stelzen", "Stelzen", S(702, "b4"), S(704, "b1"), "Dorf", "zweiherrisches Kirch- und Grenzdorf, einer der höchsten Punkte des Landes")
e.update({
    "historic_forms": HF(("Stelcze", 1279), ("Stelcze", 1335)),
    "dialect_form": "Stelzen",
    "first_mention_year": 1279,
    "location": LOC("3 Stunden SO. von Schleiz, an der Straße von da nach Reuth (Bahnhof), auf dem zur Wisentthal geneigten Westrand einer hohen Bergwelle",
                    "Schleiz", 3, "SO"),
    "parish": {"status": "Kirchdorf", "church_of": "Reuth", "verbatim": "Filial von Reuth; eingepfarrt auch die Häuser von Spielmes rechts des Goldbaches"},
    "school": {"exists": True, "pupils": 71},
    "houses": 48,
    "inhabitants": 325,
    "occupations": {"Bauern": 22, "Häusler": 25, "Taglöhner": 2, "Dienstboten": 22},
    "crafts": {"Schuhmacher": 2, "Maurer": 1, "Tischler": 1, "Wirth": 1},
    "flur_morgen": 1826.5,
    "flur_verbatim": "1826 1/2 Morgen",
    "livestock": {"Pferde": 5, "Rinder": 265, "Schafe": 4, "Schweine": 64, "Ziegen": 35, "Gänse": 90, "Bienenstöcke": 10},
    "municipal_finances": {"verbatim": "Die Gemeinde hat als engere circa 200 Thlr. Vermögen, als weitere kein Kapital und keinen Besitz, dagegen eine Jahresausgabe von 50—60 Thlr.",
                           "assets_thaler": 200},
    "facilities": ["Kirche", "Schule", "Gemeindehaus", "Spritzenhaus", "Gasthöfe (zwei, ein sächsischer und ein reußischer)", "Feuerspritze", "Ziegeleien (drei)",
                   "sächsisch-hofer Eisenbahn durch die Flur"],
    "events": EV(
        (1279, "Heinrich, Herr von Gera, gibt Güter in Stelzen dem Deutschen Orden zu Schleiz", "Heinrich, lord of Gera, gives estates at Stelzen to the Teutonic Order of Schleiz"),
        (1333, "Kloster zum heil. Kreuz erhält 1 1/2 Mark Zinsen (seit 1333 und 1355)", "Holy Cross convent obtains 1 1/2 marks of rent (from 1333 and 1355)"),
        (1797, "Schulhaus erbaut (1796 oder 1797)", "school building erected (1796 or 1797)"),
        (1806, "Kirche neu erbaut", "church rebuilt"),
        (1822, "ganzer Ort Spielmes eingeschult", "the whole village of Spielmes is assigned to the school"),
        (1848, "Brand: 4 Bauerngüter und 1 Kleinhaus (26. Oktober)", "fire: 4 farms and 1 cottage (26 October)"),
        (1853, "Brände am 26. August und 5. Oktober", "fires on 26 August and 5 October"),
        (1864, "Kirche repariert", "church repaired"),
        (1867, "3 Höfe brennen ab (18. April)", "3 farms burn down (18 April)"),
        (1868, "4 Häuser brennen ab (21. Juni)", "4 houses burn down (21 June)"),
    ),
    "summary_de": "Zweiherrisches Kirch- und Grenzdorf an der Straße nach Reuth, einer der höchsten Punkte des Landes; 48 Privathäuser, 325 Einwohner. Kirche (1806 neu) und Schule (71 Kinder) liegen auf reußischem Boden, die Kirche ist Filial von Reuth; ein Teil der Flur und ein Gasthof stehen unter sächsischer Hoheit. Behandelt werden die Wallfahrtskapelle am Stelzenbaum (Aussicht, Sagen), die starke Vieh- und Gänsezucht, Brände seit 1848 und die Flur von 1826 1/2 Morgen.",
    "summary_en": "Village under two lords, a church and border village on the road to Reuth and one of the highest points of the principality; 48 private houses, 325 inhabitants. Church (rebuilt 1806) and school (71 children) lie on Reuss soil and the church is a filial of Reuth; part of the fields and one inn lie under Saxon sovereignty. The article covers the pilgrimage chapel at the Stelzenbaum (view, legends), heavy cattle and goose rearing, fires since 1848, and 1826 1/2 Morgen of land.",
    "notes": "Einwohner 1861: 283. Kirchenärar 4000 Thlr. Kirchenspannfrohnhöfe: Stelzen 24, Spielmes 13. Die Höhe der Kappel beim Stelzenbaum wird mit 1619 Fuß angegeben (die Kappel oberhalb Schilbach: 1610 Fuß); für das Dorf selbst gibt Brückner keine Höhe an.",
})
ENTRIES.append(e)

# ---------------------------------------------------------------- Spielmes
e = base("spielmes", "Spielmes", S(704, "b2"), S(705, "b2"), "Dorf", "kleines Grenzdorf")
e.update({
    "historic_forms": HF("Spilmeß", "Spilmes", "Spielmeß", "Spielmes"),
    "dialect_form": "Spielms und Spielmütz",
    "location": LOC("3 Stunden SOS. von Schleiz und 1/2 Stunde S. von Stelzen, im Hochthale des Goldbaches", "Schleiz", 3, "SSO"),
    "parish": {"status": "eingepfarrt", "church_of": "Stelzen", "verbatim": "pfarrt nur der größere rechts liegende Theil nach Stelzen, der links nach Mißlareuth"},
    "school": {"exists": False},
    "houses": 23,
    "inhabitants": 154,
    "occupations": {"Landwirthe": 19, "Häusler": 4, "Taglöhner": 4, "Dienstboten": 39},
    "crafts": {"Maurer": 1, "Weber": 1, "Zimmermann": 1},
    "flur_morgen": 1301.5,
    "flur_verbatim": "1301½ Morgen",
    "livestock": {"Pferde": 9, "Rinder": 199, "Schafe": 38, "Schweine": 37, "Ziegen": 14, "Gänse": 100, "Bienenstöcke": 13},
    "municipal_finances": {"verbatim": "Die Gemeinde besitzt als engere 1 Teich, als weitere weder Grund noch Kapital oder Schuld. Ihre Jahresausgabe durchschnittlich 40—50 Thlr."},
    "facilities": ["Spritzenhaus", "Gasthof (privat)", "Feuerspritze"],
    "subplaces": [
        SP("Reinhardswalde", "Einzelhof", 705, "einzelnes reußisches Haus auf der in Sachsen ausspringenden Landzunge der Flur, unweit des sächsischen Dorfes Reinhardswalde; gehört zur Gemeinde Spielmes, kircht nach Kennitz und schult nach Döles"),
    ],
    "events": EV(
        (1822, "Wanderschule aufgegeben; der ganze Ort schult nach Stelzen", "itinerant school ended; the whole village attends school at Stelzen"),
        (1860, "ein Bauernhof und ein Kleinhaus brennen ab (auch 1861)", "a farm and a cottage burn down (also 1861)"),
    ),
    "summary_de": "Kleines Grenzdorf im grasreichen Hochtal des Goldbachs, 23 Privathäuser und 154 Einwohner, hufeisenförmig um fette Wiesen angelegt und vom Goldbach in zwei Teile geteilt. Ein Teil pfarrt nach Stelzen, der andere nach Mißlareuth; die Schule ist in Stelzen. Ackerbau und Viehzucht sind die Erwerbsquellen (Flur 1301 1/2 Morgen, zungenförmig ins Sächsische greifend); zum Ort zählt das einzelne Haus bei Reinhardswalde.",
    "summary_en": "Small border village in the grassy high valley of the Goldbach with 23 private houses and 154 inhabitants, laid out in a horseshoe around rich meadows and divided in two by the Goldbach. One part belongs to the parish of Stelzen, the other to Mißlareuth; the school is at Stelzen. Livelihood is arable farming and cattle breeding (1301 1/2 Morgen, extending tongue-like into Saxony); a single house near Reinhardswalde belongs to the municipality.",
    "notes": "Einwohner 1864: 162. Der Artikel beginnt auf S. 704 b2 und endet mitten im Viehbestand der Seite; er setzt auf S. 705 b1 fort; 9 Pf. auf S. 704, 199 R. usw. auf S. 705. Das Register führt Reinhardswalde als Bestandtheil von Spielmes (S. 705).",
})
ENTRIES.append(e)
