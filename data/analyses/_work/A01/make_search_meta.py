"""Writes data/search/pages/A01.json (search metadata for pages 1-24)."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\totom\Projects\reuss-edition")

P = []


def page(label, de, en, kde, ken, subjects):
    P.append(dict(page=label, summary_de=de, summary_en=en, keywords_de=kde, keywords_en=ken, subjects=subjects))


for lab in ("1", "2"):
    page(lab, "Leerseite", "Blank page", [], [], [])

page("3",
     "Beginn des Kapitels »Die Natur des Landes«, Abschnitt 1 »Überblick und Bild des Ganzen«: das reußische Land als Mittelstück des alten Voigtlandes (Sorbenmark, Osterland, Voigtland); frühere Ausdehnung unter den Voigten (über 80 Quadratmeilen), Herkunft der Namen Voigtland und Reuß, drei Viertel des Erblandes beim Fürstentum Reuß jüngere Linie. Fußnote zum Spottnamen »Raubstaaten« für Greiz, Schleiz und Lobenstein.",
     "Start of the chapter “Die Natur des Landes”, section 1 “Overview and picture of the whole”: the land of Reuss as the central part of the old Voigtland (Sorbenmark, Osterland, Voigtland); its former extent under the Voigts (over 80 square miles), the origin of the names Voigtland and Reuss, three quarters of the inherited land belonging to the younger line. Footnote on the nickname “Raubstaaten” for Greiz, Schleiz and Lobenstein.",
     ["Vogtland", "Voigtland", "Reuß", "Sorbenmark", "Osterland", "Vögte", "Greiz", "Schleiz", "Lobenstein", "Raubstaaten"],
     ["Vogtland", "Voigtland", "Reuss", "Sorbenmark", "Osterland", "bailiffs", "Greiz", "Schleiz", "Lobenstein"],
     ["Territorialgeschichte", "Vögte von Weida", "Ortsname", "Lage und Grenzen"])

page("4",
     "Bodengestalt des Reußenlandes zwischen Fichtelgebirge und Frankenwald, Saale und Elster (Elbegebiet). Gliederung des Fürstentums in Oberland (11,03 Quadratmeilen, im Mittel 1360′ hoch) und Unterland (4,03 Quadratmeilen, 730′), durch den weimarischen Neustädter Kreis getrennt. Das Oberland auf Grauwacke und Tonschiefer: höchster Punkt Fichteberg 1925′, tiefstes Niveau an der Leube 800′; Beginn der Angabe seiner geographischen Ausdehnung.",
     "Landform of the land of Reuss between the Fichtelgebirge and the Frankenwald, Saale and Elster (Elbe catchment). Division of the principality into the Oberland (11.03 square miles, mean altitude 1360′) and the Unterland (4.03 square miles, 730′), separated by the Weimar district of Neustadt. The Oberland on greywacke and clay slate: highest point Fichteberg 1925′, lowest level at the Leube 800′; start of the statement of its geographical extent.",
     ["Oberland", "Unterland", "Fichtelgebirge", "Frankenwald", "Saale", "Elster", "Fichteberg", "Grauwacke", "Tonschiefer", "Terrasse"],
     ["Oberland", "Unterland", "Fichtelgebirge", "Frankenwald", "Saale", "Elster", "Fichteberg", "greywacke", "clay slate"],
     ["Relief", "Lage und Grenzen", "Flüsse und Bäche", "Geologie"])

page("5",
     "Lage und Gestalt von Ober- und Unterland: Länge der Grenzen in Stunden (Oberland 48, davon 22 an Reuß ä. L.; Unterland 18, davon 9 an Altenburg), Elster-Saale- und Elster-Pleiße-Platte des Unterlandes (tiefster Punkt 459′, höchster Scheidberg 989′), Unterschiede der beiden Landesteile in Klima, Sprache und Gewerbe. Gliederung in die Bezirke Gera, Schleiz und Lobenstein-Ebersdorf, 6 Städte und 167 Landorte.",
     "Position and shape of the Oberland and Unterland: length of the boundaries in hours (Oberland 48, of which 22 with Reuss elder line; Unterland 18, of which 9 with Altenburg), the Elster–Saale and Elster–Pleiße plates of the Unterland (lowest point 459′, highest Scheidberg 989′), differences between the two parts in climate, speech and trades. Division into the districts of Gera, Schleiz and Lobenstein-Ebersdorf, 6 towns and 167 rural places.",
     ["Grenzen", "Umfang", "Nachbarstaaten", "Tanna", "Unterland", "Scheidberg", "Elster", "Bezirke", "Städte", "Marktflecken"],
     ["boundaries", "perimeter", "neighbouring states", "Tanna", "Unterland", "Scheidberg", "Elster", "districts", "towns"],
     ["Lage und Grenzen", "Relief", "Bodenschätze", "Gemeinden"])

page("6",
     "Abschnitt 2 »Mathematische Lage«: geographische Ausdehnung von Unter- und Oberland und Tabelle von 37 trigonometrisch bestimmten Punkten (Röttersdorf bis Kraftsdorf) mit Länge (von Ferro) und Breite in Grad, Minuten und Sekunden sowie dem gemessenen Gegenstand (Kirche, Turmknopf, Signal). Fußnote zu den preußischen Generalstabskarten und der Triangulation von Thüringen 1851–1855.",
     "Section 2 “Mathematical position”: geographical extent of the Unterland and Oberland and a table of 37 points fixed by triangulation (Röttersdorf to Kraftsdorf) with longitude (from Ferro) and latitude in degrees, minutes and seconds and the object measured (church, tower finial, signal). Footnote on the Prussian General Staff maps and the triangulation of Thuringia 1851–1855.",
     ["geographische Länge", "geographische Breite", "Koordinaten", "Triangulation", "Ferro", "Generalstab", "Turmknopf", "Röttersdorf", "Lobenstein", "Schleiz"],
     ["longitude", "latitude", "coordinates", "triangulation", "Ferro meridian", "General Staff", "tower finial", "Röttersdorf", "Lobenstein", "Schleiz"],
     ["Lage und Grenzen"])

page("7",
     "Fortsetzung der Koordinatentabelle (20 Punkte, Stelzenbaum bis Bethenhausen, darunter Gera, Köstritz, Hohenleuben); westlichster Punkt Röttersdorf, östlichster Bethenhausen, südlichster Titschendorf, nördlichster Großaga; Orte gleicher Länge und Breite. Abschnitt 3 »Größe oder Umfang der Bodenfläche«: ältere Flächenangabe bis 1840 (21,1 Quadratmeilen nach Hassel und Stein) und Beginn der Landesvermessung seit 1840.",
     "Continuation of the coordinate table (20 points, Stelzenbaum to Bethenhausen, including Gera, Köstritz, Hohenleuben); westernmost point Röttersdorf, easternmost Bethenhausen, southernmost Titschendorf, northernmost Großaga; places of equal longitude and latitude. Section 3 “Size or extent of the land area”: the older area figure until 1840 (21.1 square miles after Hassel and Stein) and the start of the land survey from 1840.",
     ["Koordinaten", "Gera", "Köstritz", "Hohenleuben", "Bethenhausen", "Titschendorf", "Großaga", "Fläche", "Quadratmeilen", "Landesvermessung"],
     ["coordinates", "Gera", "Köstritz", "Hohenleuben", "Bethenhausen", "Titschendorf", "area", "square miles", "land survey"],
     ["Lage und Grenzen", "Fläche"])

page("8",
     "Landesvermessung mit dem Messtisch (Gera seit 1840, Schleiz seit 1843, Lobenstein-Ebersdorf nur Croquirung), Kartenmaßstäbe und preußische Generalstabsaufnahme 1851–1857. Tabelle der Flächenberechnungen (Engelhardt, Nowack, Landesvermessung; zusammen 15,06 Quadratmeilen, 316 738 preußische Morgen) und Größenvergleich mit Reuß ä. L., Sachsen-Koburg, Schwarzburg-Sondershausen, Sachsen-Altenburg, Sachsen-Meiningen und Sachsen-Weimar.",
     "Land survey with the plane table (Gera from 1840, Schleiz from 1843, Lobenstein-Ebersdorf only sketched), map scales and the Prussian General Staff survey of 1851–1857. Table of the area calculations (Engelhardt, Nowack, land survey; 15.06 square miles in total, 316,738 Prussian Morgen) and size comparison with Reuss elder line, Saxe-Coburg, Schwarzburg-Sondershausen, Saxe-Altenburg, Saxe-Meiningen and Saxe-Weimar.",
     ["Fläche", "Landesvermessung", "Messtisch", "Kataster", "Morgen", "Quadratmeilen", "Nachbarstaaten", "Nowack", "Engelhardt", "Grundsteuer"],
     ["area", "land survey", "plane table", "cadastre", "Morgen", "square miles", "neighbouring states", "Nowack", "Engelhardt", "land tax"],
     ["Fläche", "Lage und Grenzen", "Steuern", "Maße und Gewichte"])

page("9",
     "Beginn von Abschnitt 4 »Plastik des Landes oder dessen senkrechte Gliederung«: Unterland und Oberland als zwei Stufenlandschaften des oberen Saal-Elstergebiets mit tief eingeschnittenem Haupttal (Elster, Saale) und zwei Seitenlandschaften; Unterschiede in Gestein, Höhe und Luft; der Bau des Unterlandes aus Elstertal, Ost- und Westlandschaft.",
     "Start of section 4 “Relief of the land or its vertical articulation”: the Unterland and Oberland as two stepped landscapes of the upper Saale–Elster region with a deeply cut main valley (Elster, Saale) and two side landscapes; differences in rock, altitude and air; the structure of the Unterland from Elster valley, east and west landscape.",
     ["Plastik", "Relief", "Stufenlandschaft", "Elstertal", "Saaltal", "Unterland", "Oberland", "Terrasse", "Plateau", "Hochfläche"],
     ["relief", "stepped landscape", "Elster valley", "Saale valley", "Unterland", "Oberland", "terrace", "plateau"],
     ["Relief", "Flüsse und Bäche", "Geologie"])

page("10",
     "Elstertal im Unterland (mittlere Betthöhe 500′, 394′ unter den Uferlandschaften); Tabelle der höchsten Punkte der West- und Ostlandschaft (800′–989′ und 780′–912′) mit Senkung nach Norden und Nordosten; Landschaftsnamen (Bramthal, Eleonorenthal, Holzland) und Bergnamen am rechten Elsterufer von der Lichtenau bis zum Zoitsberg.",
     "Elster valley in the Unterland (mean bed altitude 500′, 394′ below the bank landscapes); table of the highest points of the west and east landscape (800′–989′ and 780′–912′) with a descent towards the north and north-east; landscape names (Bramthal, Eleonorenthal, Holzland) and mountain names on the right bank of the Elster from the Lichtenau to the Zoitsberg.",
     ["Elstertal", "Westlandschaft", "Ostlandschaft", "Höhen", "Bergnamen", "Bramthal", "Eleonorenthal", "Holzland", "Zoitsberg", "Gera"],
     ["Elster valley", "west landscape", "east landscape", "altitudes", "mountain names", "Bramthal", "Eleonorenthal", "Holzland", "Gera"],
     ["Relief", "Höhenmessung", "Flurnamen", "Flüsse und Bäche"])

page("11",
     "Bergnamen am rechten (Bramthal, kleine Schnauder, Aga) und linken Elsterufer (fünf Abschnitte); Höhenlage der bewohnten Orte im Unterland (Caaschwitz tiefster, Käseschenke höchster Ort, Unterschied 493′; Verteilung auf Höhenklassen) und Beginn der Höhenliste für das rechte Elsterufer. Fußnote: alle Höhen in preußischen Dezimalfuß, auf den Pegel bei Swinemünde bezogen.",
     "Mountain names on the right (Bramthal, little Schnauder, Aga) and left bank of the Elster (five sections); altitude of the inhabited places in the Unterland (Caaschwitz lowest, Käseschenke highest, difference 493′; distribution over altitude classes) and start of the altitude list for the right bank of the Elster. Footnote: all altitudes in Prussian decimal feet, referred to the Swinemünde gauge.",
     ["Bergnamen", "Elsterufer", "Höhenlage", "bewohnte Orte", "Caaschwitz", "Käseschenke", "Dezimalfuß", "Pegel Swinemünde", "Köstritz", "Tinz"],
     ["mountain names", "Elster bank", "altitude", "inhabited places", "Caaschwitz", "Käseschenke", "decimal foot", "Swinemünde gauge", "Köstritz"],
     ["Höhenmessung", "Flurnamen", "Relief", "Maße und Gewichte"])

page("12",
     "Höhen der bewohnten Orte des Unterlandes: rechtes Elsterufer (Gera 505–600′ bis Pohlen 860–880′, mit Zwischenpunkten wie Kirche, Mühle, Ziegelei) und Beginn des linken Elsterufers (Caaschwitz, Köstritz, Milbitz, Untermhaus). Fußnote zu den Bahnhöfen Köstritz und Gera aus dem Nivellement der Thüringer Eisenbahn (577 und 607,53 rheinische Fuß).",
     "Altitudes of the inhabited places of the Unterland: right bank of the Elster (Gera 505–600′ to Pohlen 860–880′, with intermediate points such as church, mill, brickworks) and start of the left bank (Caaschwitz, Köstritz, Milbitz, Untermhaus). Footnote on the railway stations of Köstritz and Gera from the levelling of the Thuringian railway (577 and 607.53 Rhenish feet).",
     ["Höhenlage", "Gera", "Zwötzen", "Langenberg", "Zschippern", "Köstritz", "Caaschwitz", "Nivellement", "Bahnhof", "Eisenbahn"],
     ["altitude", "Gera", "Zwötzen", "Langenberg", "Zschippern", "Köstritz", "Caaschwitz", "levelling", "railway station"],
     ["Höhenmessung", "Dorf", "Eisenbahn"])

page("13",
     "Höhenliste des linken Elsterufers im Unterland (Töppeln bis Käseschenke 953′, Schornsteinrand 973,4′) und Beginn der »Höhenpunkte des Unterlandes« (Gypsbrüche unterhalb Gleina 500′ bis 763′): benannte Berge wie Geiersberg und Galgenberg bei Gera sowie Himmelsrichtungs-Höhen.",
     "Altitude list of the left bank of the Elster in the Unterland (Töppeln to Käseschenke 953′, chimney rim 973.4′) and start of the “height points of the Unterland” (gypsum quarries below Gleina 500′ to 763′): named mountains such as Geiersberg and Galgenberg near Gera as well as compass-direction heights.",
     ["Höhenlage", "Käseschenke", "Frankenthal", "Kraftsdorf", "Hundhaupten", "Höhenpunkte", "Geiersberg", "Galgenberg", "Gera", "Toisen"],
     ["altitude", "Käseschenke", "Frankenthal", "Kraftsdorf", "Hundhaupten", "height points", "Geiersberg", "Gera"],
     ["Höhenmessung", "Relief", "Dorf"])

page("14",
     "Fortsetzung der Höhenpunkte des Unterlandes von 768′ bis 939′, nach der Höhe geordnet: Himmelsrichtungs-Höhen wie »Nordhöhe von Schöna«, Berge und Signalpunkte (Thümmelsberg, Zippenbusch, Hart bei Hundhaupten, Mittelberg bei Waltersdorf), Windmühlen und Chausseepunkte.",
     "Continuation of the height points of the Unterland from 768′ to 939′, ordered by altitude: compass-direction heights such as “Nordhöhe von Schöna”, mountains and signal points (Thümmelsberg, Zippenbusch, Hart near Hundhaupten, Mittelberg near Waltersdorf), windmills and road points.",
     ["Höhenpunkte", "Berghöhen", "Thümmelsberg", "Zippenbusch", "Dürrenebersdorf", "Kaltenborn", "Schöna", "Rüdersdorf", "Signal", "Windmühle"],
     ["height points", "mountain heights", "Thümmelsberg", "Zippenbusch", "Dürrenebersdorf", "Kaltenborn", "signal", "windmill"],
     ["Höhenmessung", "Relief"])

page("15",
     "Letzte Höhenpunkte des Unterlandes (955′ bis Scheidberg bei Hundhaupten 989′). Beginn der Schilderung des Oberlandes: Saaltal als Felsspalte zwischen zwei Hochflächen, »erstarrtes Meer« der Landwellen, Mulden und Wasserläufe; Namenwörter für Hochflächen (Mark, Brand, Heide), Höhen (Bühl, Hügel, Kulm, Delsch) und Täler (Senk, Kerbe, Graben).",
     "Last height points of the Unterland (955′ to Scheidberg near Hundhaupten 989′). Start of the description of the Oberland: the Saale valley as a rock cleft between two plateaus, the “frozen sea” of land waves, hollows and watercourses; name words for plateaus (Mark, Brand, Heide), heights (Bühl, Hügel, Kulm, Delsch) and valleys (Senk, Kerbe, Graben).",
     ["Scheidberg", "Oberland", "Hochplateau", "Saaltal", "Mulden", "Flurnamen", "Bühl", "Kulm", "Höhenpunkte", "Landwellen"],
     ["Scheidberg", "Oberland", "plateau", "Saale valley", "hollows", "field names", "Bühl", "Kulm", "height points"],
     ["Relief", "Höhenmessung", "Flurnamen"])

page("16",
     "Einteilung des Oberlandes nach Höhe und Lage (oben und unten, Oberland, Mittelland, Unterland je nach Standort); höchster Randwulst im Süden und Südosten (Frankenwald, Diebsweg 1685′), Durchbruch der Saale beim Harraer Tor; das linke Saaleplateau mit Frankenwald und eliasbrunner Hochbuckel; Beginn der Beschreibung des Frankenwalds.",
     "Division of the Oberland by altitude and position (above and below, Oberland, Mittelland, Unterland depending on the viewpoint); highest rim ridge in the south and south-east (Frankenwald, Diebsweg 1685′), the Saale breaking through at the Harra gate; the left Saale plateau with Frankenwald and the Eliasbrunn upland; start of the description of the Frankenwald.",
     ["Oberland", "Frankenwald", "Diebsweg", "Saale", "Harra", "Eliasbrunn", "Rennsteig", "Schleiz", "Tanna", "Gliederung"],
     ["Oberland", "Frankenwald", "Diebsweg", "Saale", "Harra", "Eliasbrunn", "Rennsteig", "Schleiz", "Tanna"],
     ["Relief", "Flurnamen", "Lage und Grenzen", "Flüsse und Bäche"])

page("17",
     "Der Frankenwald als einziges Gebirgsstück des Fürstentums (Wasserscheide Saale–Main, Rennsteig, höchster Randstrich, Rodung durch das Bamberger Michaelskloster im 12. Jahrhundert, Waldfläche 1647) mit den Hauptbergen nach Ost-, Süd-, Nord- und Westseite (Kulm, Hohe Tanne, Fichteberg). Beginn des eliasbrunner Hochbuckels (Spitze bei Eliasbrunn, 213′ unter dem höchsten Frankenwaldberg).",
     "The Frankenwald as the principality's only mountain section (Saale–Main watershed, Rennsteig, highest rim, clearing by the Bamberg Michaelskloster in the 12th century, forest area in 1647) with the main mountains by east, south, north and west side (Kulm, Hohe Tanne, Fichteberg). Start of the Eliasbrunn upland (summit near Eliasbrunn, 213′ lower than the highest Frankenwald mountain).",
     ["Frankenwald", "Fichteberg", "Kulm", "Hohe Tanne", "Rennsteig", "Bamberg", "Michaelskloster", "Eliasbrunn", "Bergnamen", "Waldfläche"],
     ["Frankenwald", "Fichteberg", "Kulm", "Hohe Tanne", "Rennsteig", "Bamberg", "Michaelskloster", "Eliasbrunn", "mountain names"],
     ["Relief", "Wald", "Klöster", "Flurnamen"])

page("18",
     "Berge des eliasbrunner Hochbuckels nach Flussgebieten (Otter, Ilm, Törpig, Lemnitz, Friesa); rechte Saaluferlandschaft mit der Hirschberger Saalwand (Landschwelle am Diebsweg 230′ unter dem Kulm, Zugehörigkeit zu Bamberg oder Naumburg) und Berglisten; Beginn des Wiesenthal-Wetteraplateaus (Dreistädtehochland, vier Täler, Schleizer Wald 1647).",
     "Mountains of the Eliasbrunn upland by river basin (Otter, Ilm, Törpig, Lemnitz, Friesa); right Saale bank landscape with the Hirschberg Saale wall (land ridge at the Diebsweg 230′ below the Kulm, allegiance to Bamberg or Naumburg) and mountain lists; start of the Wiesenthal–Wettera plateau (three-towns upland, four valleys, Schleiz forest in 1647).",
     ["Eliasbrunn", "Hirschberg", "Saalwand", "Diebsweg", "Wiesenthal", "Wettera", "Bergnamen", "Bistum Naumburg", "Schleizer Wald", "Lemnitz"],
     ["Eliasbrunn", "Hirschberg", "Saale wall", "Diebsweg", "Wiesenthal", "Wettera", "mountain names", "diocese of Naumburg", "Schleiz forest"],
     ["Relief", "Flurnamen", "Wald", "Kirche"])

page("19",
     "Wiesenthal-Wetteraplateau mit Teichlagern und Wäldern, den Städten Tanna, Schleiz und Saalburg und der Christianisierung durch Bistum Naumburg, Grafen von Eberstein und Lobdaburg, Weidaer Herren und Deutschen Orden, mit Berglisten nach Tälern; Modelitzmulde (»schleizer Italien«) mit Berglisten nach Himmelsrichtungen; Beginn des ziegenrücker und hohenleubener Plateaus.",
     "Wiesenthal–Wettera plateau with ponds and forests, the towns of Tanna, Schleiz and Saalburg and the Christianisation by the diocese of Naumburg, the Counts of Eberstein and Lobdaburg, the lords of Weida and the Teutonic Order, with mountain lists by valley; the Modelitz basin (“Schleiz Italy”) with mountain lists by compass direction; start of the Ziegenrück and Hohenleuben plateau.",
     ["Wiesenthal", "Wettera", "Modelitzmulde", "Tanna", "Schleiz", "Saalburg", "Teiche", "Bergnamen", "Deutscher Orden", "Christianisierung"],
     ["Wiesenthal", "Wettera", "Modelitz basin", "Tanna", "Schleiz", "Saalburg", "ponds", "mountain names", "Teutonic Order"],
     ["Relief", "Flurnamen", "Teiche und Seen", "Wald"])

page("20",
     "Ziegenrücker und hohenleubener Plateau als nördlichste, niedrigste Terrassen des Oberlandes mit Berglisten. Beginn der Liste »Die Höhe der bewohnten Punkte des Oberlandes« (Schloßmühle bei Reichenfels 800′ bis Schleiz, Schloss 1169,5′): Orte wie Langenwetzendorf, Triebes, Hohenleuben, Saalburg, Harra, Blankenstein, Mühlen und Hämmer an Saale und Sormitz.",
     "The Ziegenrück and Hohenleuben plateaus as the northernmost, lowest terraces of the Oberland, with mountain lists. Start of the list “The altitude of the inhabited points of the Oberland” (Schloßmühle near Reichenfels 800′ to Schleiz, castle 1169.5′): places such as Langenwetzendorf, Triebes, Hohenleuben, Saalburg, Harra, Blankenstein, mills and hammers on the Saale and Sormitz.",
     ["Höhenlage", "bewohnte Orte", "Oberland", "Hohenleuben", "Triebes", "Saalburg", "Harra", "Langenwetzendorf", "Hammerwerke", "Plateau"],
     ["altitude", "inhabited places", "Oberland", "Hohenleuben", "Triebes", "Saalburg", "Harra", "hammer mills", "plateau"],
     ["Höhenmessung", "Relief", "Dorf", "Hüttenwesen und Hammerwerke"])

page("21",
     "Fortsetzung der Höhen der bewohnten Punkte des Oberlandes (1150′–1475′): Schleiz (Schloss-Westturmspitze 1340,6′), Hirschberg, Lehesten, Lobenstein, Ebersdorf, Oberböhmsdorf, Wurzbach, Blintendorf, Heinrichsruh (Wetterfahne 289,628 Toisen), Kulm und Mödlareuth, mit Zwischenpunkten wie Kirchen, Mühlen und Schäfereien.",
     "Continuation of the altitudes of the inhabited points of the Oberland (1150′–1475′): Schleiz (castle west tower tip 1340.6′), Hirschberg, Lehesten, Lobenstein, Ebersdorf, Oberböhmsdorf, Wurzbach, Blintendorf, Heinrichsruh (weather vane 289.628 toises), Kulm and Mödlareuth, with intermediate points such as churches, mills and sheep farms.",
     ["Höhenlage", "bewohnte Orte", "Schleiz", "Lobenstein", "Ebersdorf", "Wurzbach", "Hirschberg", "Heinrichsruh", "Lehesten", "Kulm"],
     ["altitude", "inhabited places", "Schleiz", "Lobenstein", "Ebersdorf", "Wurzbach", "Hirschberg", "Heinrichsruh"],
     ["Höhenmessung", "Dorf", "Mühlen", "Relief"])

page("22",
     "Schluss der Höhen der bewohnten Punkte des Oberlandes (1420′–1874,6′): Tanna, Eliasbrunn, Heinersdorf, Röttersdorf, Grumbach, Kohlhäuser, Karolinensfeld; Zusammenfassung (tiefster Punkt Schloßmühle Reichenfels oder Neue Mühle Hohenleuben, höchster Karolinensfeld, Unterschied 874′, Durchschnitt 1340′, 63 Wohnpunkte höher, 74 tiefer). Beginn der »Berghöhen des Oberlandes« (992′–1183′).",
     "End of the altitudes of the inhabited points of the Oberland (1420′–1874.6′): Tanna, Eliasbrunn, Heinersdorf, Röttersdorf, Grumbach, Kohlhäuser, Karolinensfeld; summary (lowest point Schloßmühle Reichenfels or Neue Mühle Hohenleuben, highest Karolinensfeld, difference 874′, average 1340′, 63 inhabited points higher, 74 lower). Start of the “mountain heights of the Oberland” (992′–1183′).",
     ["Höhenlage", "bewohnte Orte", "Tanna", "Eliasbrunn", "Karolinensfeld", "Röttersdorf", "Titschendorf", "Berghöhen", "Oberland", "höchster Wohnort"],
     ["altitude", "inhabited places", "Tanna", "Eliasbrunn", "Karolinensfeld", "Röttersdorf", "mountain heights", "Oberland", "highest village"],
     ["Höhenmessung", "Relief", "Dorf"])

page("23",
     "Berghöhen des Oberlandes von 1183′ bis 1598′, nach der Höhe geordnet: benannte Berge (Heinrichsstein, Hartebruch, Königsberg, Muckenberg, Moosflocke, Kulm bei Kulm, Großer Silberberg, Geheeg), Himmelsrichtungs-Höhen, Signalpunkte und die Wetterfahne in Heinrichsruh.",
     "Mountain heights of the Oberland from 1183′ to 1598′, ordered by altitude: named mountains (Heinrichsstein, Hartebruch, Königsberg, Muckenberg, Moosflocke, Kulm bei Kulm, Großer Silberberg, Geheeg), compass-direction heights, signal points and the weather vane in Heinrichsruh.",
     ["Berghöhen", "Oberland", "Heinrichsstein", "Hartebruch", "Muckenberg", "Silberberg", "Moosflocke", "Kulm", "Höhenpunkte", "Signal"],
     ["mountain heights", "Oberland", "Heinrichsstein", "Hartebruch", "Muckenberg", "Silberberg", "Kulm", "height points"],
     ["Höhenmessung", "Relief"])

page("24",
     "Berghöhen des Oberlandes von 1600′ bis Fichteberg 1925′ (u. a. Rosenbühl, Mittelberg im Frankenwald, Oßlahügel, Finkenberg, Sieglitzberg, Hohe Tanne, Kulm). Beginn von Abschnitt 5 »Geognostische Übersicht« von Prof. Liebe: das Oberland als erstarrtes Meer, Anordnung der Berge in Reihen von Nordost nach Südwest.",
     "Mountain heights of the Oberland from 1600′ to Fichteberg 1925′ (among others Rosenbühl, Mittelberg in the Frankenwald, Oßlahügel, Finkenberg, Sieglitzberg, Hohe Tanne, Kulm). Start of section 5 “Geognostic overview” by Prof. Liebe: the Oberland as a frozen sea, mountains arranged in rows from north-east to south-west.",
     ["Berghöhen", "Fichteberg", "Kulm", "Sieglitzberg", "Hohe Tanne", "Finkenberg", "Oßlahügel", "Frankenwald", "Geologie", "Liebe"],
     ["mountain heights", "Fichteberg", "Kulm", "Sieglitzberg", "Hohe Tanne", "Finkenberg", "Frankenwald", "geology", "Liebe"],
     ["Höhenmessung", "Relief", "Geologie"])

G = [
    dict(term="Voigtland", variants=["Vogtland", "terra advocatorum"], kind="term",
         de="Altes Herrschaftsgebiet der Vögte von Weida, Gera und Plauen im Raum zwischen Saale, Elster und Erzgebirge; Brückner führt den Namen und »Reuß« auf dasselbe Herrscherhaus zurück (S. 3).",
         en="Old territory of the bailiffs (Vögte) of Weida, Gera and Plauen between the Saale, Elster and the Ore Mountains; Brückner traces both the name and “Reuß” back to the same ruling house (p. 3).",
         pages=["3", "5"]),
    dict(term="Hercynischer Gebirgszug", variants=["hercynisch"], kind="term",
         de="Von Südosten nach Nordwesten streichende Gebirgsrichtung der deutschen Mittelgebirge (Böhmerwald bis Harz); Brückner stellt das Reußenland auf ein nördliches Seitenglied dieses Zuges (S. 3).",
         en="North-west to south-east trending mountain direction of the German uplands (Bohemian Forest to the Harz); Brückner places the Reuss land on a northern side member of this chain (p. 3).",
         pages=["3"]),
    dict(term="Oberland", variants=["Unterland"], kind="term",
         de="Brückners Zweiteilung des Fürstentums: das größere, südliche Oberland (Saal-Elster-Terrasse, 11,03 Quadratmeilen, im Mittel 1360′) und das kleinere, nördliche Unterland (mittlere Elster, 4,03 Quadratmeilen, 730′); beide sind getrennt (S. 4).",
         en="Brückner's twofold division of the principality: the larger, southern Oberland (Saale–Elster terrace, 11.03 square miles, mean 1360′) and the smaller, northern Unterland (middle Elster, 4.03 square miles, 730′); the two are separated (p. 4).",
         pages=["4", "5", "9", "10", "15", "16", "20"]),
    dict(term="Dezimalfuß", variants=["Decimalfuß", "preuß. Decimalfuß", "′"], kind="unit",
         de="Preußischer Dezimalfuß, die Einheit aller Höhenangaben der Landeskunde (S. 11 Anm.): 1/10 preußische Ruthe, also 0,3766 m (Ruthe = 3,766242 m, S. 831); bezogen auf den Pegel bei Swinemünde. Nicht zu verwechseln mit dem Pariser Fuß (0,3248 m). Das Zeichen ′ hinter Zahlen bedeutet bei Höhen »Fuß«.",
         en="Prussian decimal foot, the unit of all altitude figures in the Landeskunde (p. 11 note): 1/10 of a Prussian Ruthe, i.e. 0.3766 m (Ruthe = 3.766242 m, p. 831); referred to the Swinemünde gauge. Not to be confused with the Paris foot (0.3248 m). The sign ′ after numbers means “foot” for altitudes.",
         pages=["4", "5", "10", "11", "12", "13", "14", "15", "16", "17", "18", "20", "21", "22", "23", "24"]),
    dict(term="Pegel bei Swinemünde", variants=["amsterdamer Pegel"], kind="term",
         de="Höhenbezugsfläche der Höhenangaben: der Wasserstandsmesser bei Swinemünde (Ostsee); die Bahnhöfe Köstritz und Gera waren zuvor auf den Amsterdamer Pegel bezogen (S. 11–12 Anm.).",
         en="Datum of the altitude figures: the water-level gauge at Swinemünde (Baltic Sea); the stations of Köstritz and Gera were previously referred to the Amsterdam gauge (pp. 11–12 notes).",
         pages=["11", "12"]),
    dict(term="Toise", variants=["Toisen"], kind="unit",
         de="Altes französisches Längenmaß zu 6 Pariser Fuß (≈ 1,949 m); für die Turmhöhen von Dürrenebersdorf und Heinrichsruh gibt Brückner Toisen an (S. 13, 21).",
         en="Old French length unit of 6 Paris feet (≈ 1.949 m); for the tower heights of Dürrenebersdorf and Heinrichsruh Brückner gives toises (pp. 13, 21).",
         pages=["13", "21"]),
    dict(term="Quadratmeile", variants=["□Meile", "□M."], kind="unit",
         de="Flächenmaß der Staatsstatistik; Brückner nennt es ohne Erklärung. Nach seinen Zahlen (316 738 Morgen = 14,965 □M.) etwa 54 km², also nahe der geographischen Quadratmeile (55,06 km²).",
         en="Area unit of state statistics; Brückner gives it without explanation. By his figures (316,738 Morgen = 14.965 □M.) about 54 km², i.e. close to the geographical square mile (55.06 km²).",
         pages=["3", "4", "7", "8"]),
    dict(term="Morgen", variants=["preußischer Morgen", "pr. Morgen"], kind="unit",
         de="Preußischer Morgen zu 180 Quadratruthen; nach Brückners Tabelle S. 832 = 0,255322 ha. Die Landesvermessung rechnet die Fläche des Fürstentums mit 316 738 Morgen (S. 8).",
         en="Prussian Morgen of 180 square Ruthen; according to Brückner's table on p. 832 = 0.255322 ha. The land survey gives the area of the principality as 316,738 Morgen (p. 8).",
         pages=["8"]),
    dict(term="Stunde", variants=["Stunden"], kind="unit",
         de="Wegstunde als Längenmaß, hier für die Länge des Landes und seiner Grenzen (Oberland 11 Stunden lang, Umfang 48 Stunden); Brückners Umrechnungstabelle (S. 831–832) enthält keinen Wert dafür.",
         en="Walking hour used as a length measure, here for the length of the land and its boundaries (Oberland 11 hours long, perimeter 48 hours); Brückner's conversion table (pp. 831–832) gives no value for it.",
         pages=["4", "5"]),
    dict(term="Nürnberger Acker", variants=["nürnberger Acker"], kind="unit",
         de="Ältere Flächeneinheit, mit der 1647 die Waldflächen des Frankenwalds und des Schleizer Waldes angegeben wurden (S. 17–18); Brückner nennt keine Umrechnung.",
         en="Older area unit in which the forest areas of the Frankenwald and the Schleiz forest were stated in 1647 (pp. 17–18); Brückner gives no conversion.",
         pages=["17", "18"]),
    dict(term="Ferro", variants=["Ostlänge von Ferro", "L."], kind="term",
         de="Insel Ferro (El Hierro), deren Meridian bis ins 19. Jahrhundert als Nullmeridian diente; die Längen auf S. 4–7 sind östlich von Ferro gezählt (»L.«). Greenwich-Länge = Ferro-Länge − 17° 40′.",
         en="Island of Ferro (El Hierro), whose meridian served as prime meridian until the 19th century; the longitudes on pp. 4–7 are counted east of Ferro (“L.”). Greenwich longitude = Ferro longitude − 17° 40′.",
         pages=["4", "5", "6", "7"]),
    dict(term="Turmknopf", variants=["Thurmknopf", "Thkn."], kind="term",
         de="Kugel oder Knauf auf der Turmspitze; häufigster Messpunkt der Triangulation und der Höhenangaben (»Kirche, Thkn.« = Kirchturmknopf).",
         en="Ball or finial on top of a tower; the most frequent measuring point of the triangulation and altitude figures (“Kirche, Thkn.” = church tower finial).",
         pages=["6", "7", "13", "20", "21", "22"]),
    dict(term="Triangulation", variants=["Generalstabskarten", "Generalstab"], kind="term",
         de="Dreiecksmessung als Grundlage der Landesaufnahme; die Ortsbestimmungen beruhen auf den preußischen Generalstabskarten und der Triangulation von Thüringen (1851–1855, Berlin 1859; S. 6 Anm.).",
         en="Triangulation as the basis of the land survey; the position fixes rest on the Prussian General Staff maps and the triangulation of Thuringia (1851–1855, Berlin 1859; p. 6 note).",
         pages=["6", "8"]),
    dict(term="Messtisch", variants=["Meßtisch"], kind="term",
         de="Zeichentisch der Feldmesser (Messtischaufnahme) für die Kartierung der Fluren; so wurden Gera (ab 1840) und Schleiz (ab 1843) aufgenommen.",
         en="Plane table of the surveyors (plane-table survey) for mapping the fields; Gera (from 1840) and Schleiz (from 1843) were surveyed this way.",
         pages=["7", "8"]),
    dict(term="Triftablösung", variants=["Trift"], kind="term",
         de="Ablösung der Triftrechte, also der Rechte, Vieh über fremden Grund zu treiben und zu weiden; Anlass der Vermessungen von Gera und Schleiz (S. 7–8).",
         en="Redemption of drift rights, i.e. the rights to drive and graze livestock across other people's land; the occasion for the surveys of Gera and Schleiz (pp. 7–8).",
         pages=["7", "8"]),
    dict(term="Enclave", variants=["Exclave", "Ex- und Enclaven"], kind="term",
         de="Fremdes Gebiet innerhalb des eigenen (Enclave) bzw. eigenes Gebiet außerhalb des Landes (Exclave); Brückner rechnet sie in den Umfang ein (S. 5); das Unterland hat die Exclave Otticha, Falke, Pohlen und Lichtenberg (S. 9).",
         en="Foreign territory inside one's own (enclave) or one's own territory outside the country (exclave); Brückner includes them in the perimeter (p. 5); the Unterland has the exclave of Otticha, Falke, Pohlen and Lichtenberg (p. 9).",
         pages=["5", "9"]),
    dict(term="Marktflecken", variants=["Marktdorf", "Marktdörfer"], kind="term",
         de="Größerer Ort mit Marktrecht ohne Stadtrechte; das Fürstentum hat nach Brückner 4 Marktflecken und 11 Marktdörfer unter den 167 Landorten (S. 5).",
         en="Larger place with market rights but without town rights; according to Brückner the principality has 4 market boroughs and 11 market villages among its 167 rural places (p. 5).",
         pages=["5"]),
    dict(term="Grauwacke", variants=["Thonschiefer", "Tonschiefer"], kind="term",
         de="Dunkler, feinkörniger Sandstein und tonige Schiefer der älteren Erdzeitalter; der Untergrund des Oberlandes (S. 4).",
         en="Dark, fine-grained sandstone and clayey slate of the older geological periods; the bedrock of the Oberland (p. 4).",
         pages=["4"]),
    dict(term="Rennstieg", variants=["Rennsteig"], kind="term",
         de="Alter Höhenweg auf dem Kamm von Frankenwald und Thüringer Wald; nach Brückner Wasserscheide zwischen Saale und Main (»alter Kehr-, Wende- oder Rennstiegboden«, S. 16–17).",
         en="Old ridge path on the crest of the Frankenwald and the Thuringian Forest; according to Brückner the watershed between Saale and Main (“old Kehr-, Wende- or Rennstiegboden”, pp. 16–17).",
         pages=["16", "17"]),
    dict(term="Nivellement", variants=[], kind="term",
         de="Höhenmessung durch Visieren (Nivellieren); die Bahnhöfe Köstritz und Gera entstammen dem Nivellement der Thüringer Eisenbahn (S. 12 Anm.).",
         en="Height measurement by levelling; the stations of Köstritz and Gera come from the levelling of the Thuringian railway (p. 12 note).",
         pages=["12"]),
    dict(term="Bühl", variants=["Bühel", "Hübel", "Hügel"], kind="dialect",
         de="Hügel, Anhöhe; Grundwort zahlreicher oberländischer Bergnamen (Steinbühl, Rittersbühl); Brückner nennt es unter den Wörtern für Höhen und Buckel (S. 15).",
         en="Hill, rise; generic element of many Oberland mountain names (Steinbühl, Rittersbühl); Brückner lists it among the words for heights and humps (p. 15).",
         pages=["15", "17", "18", "19"]),
    dict(term="Leite", variants=["Leithe"], kind="dialect",
         de="Berghang, Abhang (mundartlich); Grundwort von Bergnamen wie Siegelleite, Pechleite, Wetteraleite (S. 17–19).",
         en="Mountain slope, hillside (dialect); generic element of mountain names such as Siegelleite, Pechleite, Wetteraleite (pp. 17–19).",
         pages=["17", "18", "19"]),
    dict(term="Hart", variants=["Hartebruch"], kind="dialect",
         de="Wald auf einer Anhöhe (Hardt); als Bergname in Unter- und Oberland vielfach genannt (z. B. Hart bei Hundhaupten, obere und untere Hart bei Niederböhmsdorf).",
         en="Wooded height (Hardt); frequent as a mountain name in the Unterland and Oberland (e.g. Hart near Hundhaupten, upper and lower Hart near Niederböhmsdorf).",
         pages=["11", "14", "20"]),
    dict(term="Tännig", variants=["Tännicht", "Erlich", "Birkicht"], kind="dialect",
         de="Mundartliche Sammelbildung auf -ig/-icht für Gehölz: Tännig = Tannenwald, Erlich = Erlengehölz, Birkicht = Birkengehölz; häufige Bergnamen im Oberland (S. 17–20).",
         en="Dialect collective formation in -ig/-icht for woodland: Tännig = fir wood, Erlich = alder grove, Birkicht = birch grove; frequent mountain names in the Oberland (pp. 17–20).",
         pages=["17", "18", "19", "20"]),
    dict(term="Kulm", variants=["Culm"], kind="dialect",
         de="Bergkuppe (Kulm als Bergname); zweithöchste benannte Erhebung des Oberlandes nach dem Fichteberg (Kulm im Frankenwald, 1913′) und zugleich Ortsname im Oberland; nicht zu verwechseln mit dem geologischen Kulm (Karbon).",
         en="Summit, rounded hill (Kulm as a mountain name); second-highest named elevation of the Oberland after the Fichteberg (Kulm in the Frankenwald, 1913′) and also a place name in the Oberland; not to be confused with the geological Kulm (Carboniferous).",
         pages=["15", "17", "18", "19", "21", "23", "24"]),
    dict(term="Delsch", variants=["Oelsch", "Lohmen"], kind="dialect",
         de="Oberländische Wörter für Höhen und Buckel (Delsch, Lohmen), die Brückner S. 15 neben Bühl, Hügel, Kopf, Stein, Fels, Berg und Kulm aufführt; als Bergnamen Oelsch und Lohmen häufig.",
         en="Oberland words for heights and humps (Delsch, Lohmen) that Brückner lists on p. 15 beside Bühl, Hügel, Kopf, Stein, Fels, Berg and Kulm; frequent as mountain names Oelsch and Lohmen.",
         pages=["15", "19", "20", "23"]),
]

out = dict(package="A01", pages=P, glossary=G)
path = ROOT / "data" / "search" / "pages" / "A01.json"
path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", path, len(P), "pages", len(G), "glossary entries")
