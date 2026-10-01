# -*- coding: utf-8 -*-
"""Persons named Heinrich outside the princely houses: rulers, nobility, clergy, scholars, owners."""
from part1 import P, M, R, AMB

# --- kings, emperors, princes outside Reuß -----------------------------------------------------
P('Heinrichs des Löwen', 'Heinrich der Löwe', 'Herzog',
  'Heinrich der Löwe, Herzog von Sachsen und Bayern; 1180 geächtet; Brückner erörtert Vasallen aus seinem Gefolge (Familie von Witha/Weida an der Unstrut) im Streit um die Abstammung des Hauses Reuß (S. 324-329).',
  'Heinrich the Lion, duke of Saxony and Bavaria; outlawed in 1180; Brückner discusses vassals in his retinue (the family of Witha/Weida on the Unstrut) in the dispute over the origin of the house of Reuss (pp. 324-329).')

P('Heinrich der Vogler', 'Heinrich I. der Vogler', 'König',
  'Heinrich I., der Vogler, Sachse, deutscher König (bei Brückner auch „Kaiser Heinrich"); ordnete die Sorbenmark, Gaueinteilung und Ortsanlagen; nach der Sage zerstörte er in Langenberg ein heidnisches Götzenbild (S. 198, 319-320, 514).',
  'Heinrich I. the Fowler, Saxon, German king (also called "Emperor Heinrich" by Brückner); organized the Sorbian March, the division into Gaue and settlements; according to legend he destroyed a heathen idol at Langenberg (pp. 198, 319-320, 514).')
for k in ('König Heinrich I', 'Königs Heinrich', 'Kaiser Heinrich I'):
    M(k, 'Heinrich der Vogler', 'title/inflection variant')

P('König Heinrich II', 'Heinrich II. (deutscher König und Kaiser)', 'König',
  'Heinrich II., deutscher König (später Kaiser); schenkte 1011 einen beträchtlichen Teil des orla-saalfelder Gebietes dem Pfalzgrafen Ehrenfried (S. 320).',
  'Heinrich II., German king (later emperor); in 1011 gave a considerable part of the Orla-Saalfeld region to Count Palatine Ehrenfried (p. 320).')

P('Kaiser Heinrich IV', 'Heinrich IV. (Kaiser)', 'Kaiser',
  'Heinrich IV., Kaiser; übergab 1060 die Burgwarte Langenberg dem Hochstift Naumburg; nach der Überlieferung machte er Heinrich den Frommen zu seinem Marschall (S. 320, 323).',
  'Heinrich IV., emperor; gave the Burgwart of Langenberg to the bishopric of Naumburg in 1060; according to tradition he made Heinrich the Pious his marshal (pp. 320, 323).')

P('Heinrich der Erlauchte', 'Heinrich der Erlauchte (Markgraf von Meißen)', 'Markgraf',
  'Heinrich der Erlauchte, Markgraf von Meißen und Landgraf von Thüringen (Wettiner); schloß 1254 den grimmaischen Vertrag mit den Voigten von Weida, Plauen und Gera; Lehnsherr von Gebieten der Voigte (S. 334, 354, 490).',
  'Heinrich the Illustrious, margrave of Meissen and landgrave of Thuringia (Wettin); concluded the treaty of Grimma with the Voigte of Weida, Plauen and Gera in 1254; feudal lord of territories of the Voigte (pp. 334, 354, 490).')
for k in ('Heinrich dem Erlauchten von Meissen', 'Heinrich dem Erlauchten'):
    M(k, 'Heinrich der Erlauchte', 'inflection variant')

# --- counts, princes and nobles linked to the house -----------------------------------------------
P('Heinrich von Schwarzburg', 'Heinrich von Schwarzburg (Graf, 1450/51)', 'Graf',
  'Graf Heinrich von Schwarzburg, im thüringischen Bruderkrieg Gegner der Brüder Heinrich von Gera-Schleiz und Heinrich von Gera-Lobenstein; Friede am 27. Jan. 1451 (S. 348).',
  'Count Heinrich of Schwarzburg, opponent of the brothers Heinrich of Gera-Schleiz and Heinrich of Gera-Lobenstein in the Thuringian fratricidal war; peace on 27 Jan. 1451 (p. 348).')
P('Heinrich v. Schwarzburg-Leutenberg', 'Heinrich von Schwarzburg-Leutenberg (Graf)', 'Graf',
  'Graf Heinrich von Schwarzburg-Leutenberg, in zweiter Ehe verheiratet mit einer Tochter (Brigitta) des Hauses Gera, Witwe eines von Schönburg (Tab. III, S. 352).',
  'Count Heinrich of Schwarzburg-Leutenberg, married as her second husband to a daughter (Brigitta) of the house of Gera, widow of a lord of Schönburg (Tab. III, p. 352).')
P('Johann Heinrich von Schwarzburg-Leutenberg', 'Johann Heinrich von Schwarzburg-Leutenberg (Graf)', 'Graf',
  'Graf Johann Heinrich von Schwarzburg-Leutenberg, 1527 verheiratet mit Margaretha von Weida, der Erbin von Wildenfels († nach 1562); verkaufte Wildenfels (S. 340, Tab. II).',
  'Count Johann Heinrich of Schwarzburg-Leutenberg, married in 1527 to Margaretha of Weida, heiress of Wildenfels (d. after 1562); sold Wildenfels (p. 340, Tab. II).')
M('Joh. Heinrich', 'Johann Heinrich von Schwarzburg-Leutenberg', 'abbreviated form (Tab. II, p. 341)')
P('Heinrich von Truhendingen', 'Heinrich von Truhendingen (Graf)', 'Graf',
  'Graf Heinrich von Truhendingen, erster Gatte der Dorothea von Gera; Vater des Oswald von Truhendingen, der Anna, die Tochter Heinrichs d. ä. von Greiz, heiratete (S. 352, 368).',
  'Count Heinrich of Truhendingen, first husband of Dorothea of Gera; father of Oswald of Truhendingen, who married Anna, daughter of Heinrich d. ä. of Greiz (pp. 352, 368).')
M('Heinrich von Trübenbingen', 'Heinrich von Truhendingen', 'OCR variant of Truhendingen (Tab. III, p. 352)')
P('Heinrich v. Beichlingen', 'Heinrich von Beichlingen (zu Rothenburg)', 'Adliger',
  'Heinrich von Beichlingen zu Rothenburg, † 1366; verheiratet mit Sophie von Gera (Tab. III, S. 352).',
  'Heinrich of Beichlingen at Rothenburg, died 1366; married Sophie of Gera (Tab. III, p. 352).')
P('Heinrich v. Schwanberg', 'Heinrich von Schwanberg', 'Adliger',
  'Heinrich von Schwanberg, Gatte der Margaretha von Plauen († nach 1465), Tochter des Burggrafen Heinrich II. (Tab. IV, S. 364).',
  'Heinrich of Schwanberg, husband of Margaretha of Plauen (d. after 1465), daughter of Burgrave Heinrich II. (Tab. IV, p. 364).')
P('Heinrich v. Anhalt-Köthen', 'Heinrich von Anhalt-Köthen', 'Fürst',
  'Heinrich von Anhalt-Köthen, † 1847; 1819 verheiratet mit Auguste Reuß-Köstritz (1794-1855) (Tab. XI, S. 399).',
  'Heinrich of Anhalt-Köthen, died 1847; married in 1819 Auguste Reuss-Köstritz (1794-1855) (Tab. XI, p. 399).')
P('Heinrich Graf v. Reichenbach-Goschütz', 'Heinrich Graf von Reichenbach-Goschütz', 'Graf',
  'Heinrich Graf von Reichenbach-Goschütz, † 1855; verheiratet mit Emilie Reuß-Köstritz (1787-1854) (Tab. X, S. 398).',
  'Count Heinrich of Reichenbach-Goschütz, died 1855; married Emilie Reuss-Köstritz (1787-1854) (Tab. X, p. 398).')
P('Heinrich August von Stolberg', 'Heinrich August von Stolberg (zu Schwarzau)', 'Graf',
  'Heinrich August von Stolberg zu Schwarzau, † 1748; verheiratet mit Ernestine Emilie Reuß (1705-1728), später mit Friederike Charlotte von Hohenlohe (Tab. XIV, S. 402).',
  'Heinrich August of Stolberg at Schwarzau, died 1748; married Ernestine Emilie Reuss (1705-1728), later Friederike Charlotte of Hohenlohe (Tab. XIV, p. 402).')
P('Friedrich Heinrich von Stein', 'Friedrich Heinrich von Stein (in Lausnitz)', 'Adliger',
  'Friedrich Heinrich von Stein in Lausnitz; verheiratet mit Eva Emilie Reuß (1667-1716) (Tab. XIV, S. 402).',
  'Friedrich Heinrich of Stein at Lausnitz; married Eva Emilie Reuss (1667-1716) (Tab. XIV, p. 402).')
P('Wolfgang Heinrich v. Schönburg-Penig', 'Wolfgang Heinrich von Schönburg-Penig', 'Graf',
  'Wolfgang Heinrich von Schönburg-Penig, † 1657; verheiratet mit Judith Eva Reuß (1614-1666) (Tab. XII, S. 400).',
  'Wolfgang Heinrich of Schönburg-Penig, died 1657; married Judith Eva Reuss (1614-1666) (Tab. XII, p. 400).')
P('Chriſtian Heinrich v. Reitzenſtein', 'Christian Heinrich von Reitzenstein', 'Adliger',
  'Christian Heinrich von Reitzenstein, † 1762; verheiratet mit Christiane Marie Eleonore Reuß-Lobenstein (1722-1764) (Tab. VIII, S. 396).',
  'Christian Heinrich of Reitzenstein, died 1762; married Christiane Marie Eleonore Reuss-Lobenstein (1722-1764) (Tab. VIII, p. 396).',
  note='The key spells "Chriſtian" and "Reitzenſtein" with long s (transcription).')
P('Heinrich Augusts de la Motte Fouqué', 'Heinrich August de la Motte Fouqué', 'Adliger',
  'Heinrich August de la Motte Fouqué, erster Gatte der Henriette von Sinzendorf († 1826), die danach Heinrich XXXIX. Reuß-Köstritz heiratete (Tab. X, S. 398); von Brückner nicht näher bezeichnet.',
  'Heinrich August de la Motte Fouqué, first husband of Henriette of Sinzendorf (d. 1826), who afterwards married Heinrich XXXIX. Reuss-Köstritz (Tab. X, p. 398); not further identified by Brückner.',
  note='The key has the genitive ending ("Heinrich Augusts"); not linked to the Prussian general of the same name, as the generation cannot be established from Brückner.')
P('Heinrich Wilhelm zu Solms-Tecklenburg', 'Heinrich Wilhelm zu Solms-Tecklenburg', 'Graf',
  'Graf Heinrich Wilhelm zu Solms-Tecklenburg; erkaufte 1719 für 40 000 Thlr. das steinbrücken-robensche Gesamtgut, das zuvor zum Köstritzer Paragiat gehört hatte (S. 518).',
  'Count Heinrich Wilhelm of Solms-Tecklenburg; bought in 1719 for 40,000 thalers the combined Steinbrücken-Roben estate, which had previously belonged to the Köstritz Paragiat (p. 518).')

# --- landowners and local nobility ------------------------------------------------------------
P('Heinrich Bernhard', 'Heinrich Bernhard (v. Metsch)', 'Gutsbesitzer',
  'Heinrich Bernhard von Metsch, Besitzer von Kleinaga bald nach 1610, Vorgänger Adam Heinrichs von Metsch (S. 526).',
  'Heinrich Bernhard of Metsch, owner of Kleinaga soon after 1610, predecessor of Adam Heinrich of Metsch (p. 526).')
P('Adam Heinrich v. Metsch', 'Adam Heinrich von Metsch', 'Gutsbesitzer',
  'Adam Heinrich von Metsch, Besitzer von Kleinaga bis 1683, dann Verkauf an Veit Ludwig von Tümpling (S. 526).',
  'Adam Heinrich of Metsch, owner of Kleinaga until 1683, then sold to Veit Ludwig of Tümpling (p. 526).')
P('Hans Heinrich Metsch', 'Hans Heinrich Metsch', 'Adliger',
  'Junker Hans Heinrich Metsch, am 27. Febr. 1640 im Dreißigjährigen Krieg erschossen und am 3. März in Großsaara begraben (S. 467).',
  'Junker Hans Heinrich Metsch, shot on 27 Feb. 1640 in the Thirty Years\' War and buried at Großsaara on 3 March (p. 467).')
P('Christoph Heinrich v. Beust', 'Christoph Heinrich von Beust', 'Gutsbesitzer',
  'Christoph Heinrich von Beust, 1649 Gutsherr (S. 546).',
  'Christoph Heinrich of Beust, lord of the manor in 1649 (p. 546).')
P('Heinrich v. Ende', 'Heinrich von Ende', 'Gutsbesitzer',
  'Heinrich von Ende, gelangte 1667 durch Ankauf beider Hälften in den Besitz eines ganzen Gutes (S. 547).',
  'Heinrich of Ende, acquired both halves of an estate by purchase in 1667 (p. 547).')
P('Heinrich Nicol. v. Ende', 'Heinrich Nicolaus von Ende (zu Kaimberg)', 'Gutsbesitzer',
  'Heinrich Nicolaus von Ende zu Kaimberg, 1647 mit Erb- und Obergerichten, Lehn und Zinsen in einem Ort (S. 569).',
  'Heinrich Nicolaus of Ende at Kaimberg, in 1647 holder of the hereditary and high jurisdiction, fief and dues in one village (p. 569).')
P('Jobst Heinrich v. Watzdorf', 'Jobst Heinrich von Watzdorf (auf Köstritz)', 'Gutsbesitzer',
  'Jobst Heinrich von Watzdorf auf Köstritz, unterzeichnete 1581 eine Urkunde (S. 495).',
  'Jobst Heinrich of Watzdorf at Köstritz, signed a charter in 1581 (p. 495).')
P('Georg Heinrich v. Kospod', 'Georg Heinrich von Kospod', 'Adliger',
  'Georg Heinrich von Kospod, am 13. Mai 1702 von Adam Römer auf Langenwolschendorf im Rohgrund erschossen (S. 625).',
  'Georg Heinrich of Kospod, shot on 13 May 1702 by Adam Römer of Langenwolschendorf in the Rohgrund (p. 625).')
P('Heinrich v. Eichicht', 'Heinrich von Eichicht', 'Gutsbesitzer',
  'Heinrich von Eichicht auf Langenberg, 1533 Besitzer eines Gutes (S. 515).',
  'Heinrich of Eichicht at Langenberg, owner of an estate in 1533 (p. 515).')
P('Heinrich v. Langenberg', 'Heinrich von Langenberg', 'Adliger',
  'Heinrich von Langenberg, 1240 genannt, Angehöriger des nach Langenberg benannten Adelsgeschlechts (S. 513).',
  'Heinrich of Langenberg, named in 1240, member of the noble family named after Langenberg (p. 513).')
P('Heinrich v. Privel', 'Heinrich von Privel', 'Adliger',
  'Heinrich von Privel, Afterlehnsträger eines Gebietes, das die Reichsvoigte von Gera, Plauen und Weida von Markgraf Heinrich dem Erlauchten zu Lehen hatten; 1255 (S. 490).',
  'Heinrich of Privel, sub-vassal of a territory held by the imperial Voigte of Gera, Plauen and Weida from Margrave Heinrich the Illustrious; 1255 (p. 490).')
P('Heinrich v. Sloven', 'Heinrich von Sloven', 'Adliger',
  'Heinrich von Sloven, Afterlehnsträger (mit Heinrich von Privel) eines Gebietes der Reichsvoigte; 1255 (S. 490).',
  'Heinrich of Sloven, sub-vassal (with Heinrich of Privel) of a territory of the imperial Voigte; 1255 (p. 490).')
P('Heinrich v. Saalburg', 'Heinrich von Saalburg', 'Adliger',
  'Heinrich von Saalburg, genannt 1225-1310 in der Reihe der Burgmannen (Familie von Saalburg) (S. 664).',
  'Heinrich of Saalburg, named between 1225 and 1310 in the series of burgmen (family of Saalburg) (p. 664).')
P('Heinrich v. Brandenstein', 'Heinrich von Brandenstein', 'Adliger',
  'Heinrich von Brandenstein schenkte 1302 mit Albert zwei Güter in Dittersdorf dem Deutschen Orden zu Schleiz (S. 594).',
  'Heinrich of Brandenstein donated two estates at Dittersdorf to the Teutonic Order at Schleiz in 1302 together with Albert (p. 594).')
P('Heinrich von Oschitz', 'Heinrich von Oschitz', 'Geistlicher',
  'Heinrich von Oschitz, Glied der Familie von Kospod, Pfarrer zu Münchberg; übergab 1368 dem Kloster zum Heiligen Kreuz bei Saalburg Güter zu Oberkoskau (S. 689, 700).',
  'Heinrich of Oschitz, member of the family of Kospod, parish priest at Münchberg; gave estates at Oberkoskau to the Holy Cross convent near Saalburg in 1368 (pp. 689, 700).')
M('Heinrich v. Oschitz', 'Heinrich von Oschitz', 'abbreviated variant (p. 700)')
P('Wolf Heinrich von Reitzenstein', 'Wolf Heinrich von Reitzenstein (auf Kischling)', 'Adliger',
  'Wolf Heinrich von Reitzenstein auf Kischling, † 6. Dez. 1587 (Grabinschrift), nach S. 783 von seinem Knecht zu Seibis erschlagen (1588).',
  'Wolf Heinrich of Reitzenstein at Kischling, died 6 Dec. 1587 (epitaph); according to p. 783 killed by his servant at Seibis (1588).',
  note='Brückner gives 1587 (epitaph, p. 787) and 1588 (p. 783).')
M('Wolf Heinrich v. Reitzenstein', 'Wolf Heinrich von Reitzenstein', 'abbreviated variant (p. 783)')
P('Heinrich v. Reitzenstein', 'Heinrich von Reitzenstein', 'Gutsbesitzer',
  'Heinrich von Reitzenstein, 1647 noch im Besitz des unteren Ritterguts (S. 787).',
  'Heinrich of Reitzenstein, still owner of the lower manor in 1647 (p. 787).')
P('Heinrich v. Merenbach', 'Heinrich von Merenbach', 'Gutsbesitzer',
  'Heinrich von Merenbach; von ihm kaufte 1678 das Herrscherhaus zu Schleiz ein Gut, das 1692 an das Paragiat Köstritz überging (S. 634).',
  'Heinrich of Merenbach; the ruling house of Schleiz bought an estate from him in 1678 that passed to the Köstritz Paragiat in 1692 (p. 634).')
P('Heinrich v. Müffling gen. Weiß', 'Heinrich von Müffling genannt Weiß', 'Gutsbesitzer',
  'Heinrich von Müffling genannt Weiß, Besitzer von Reichenfels; kaufte 1601 die Hälfte von seinem Schwiegervater, 1602 die andere Hälfte (S. 632, 636).',
  'Heinrich of Müffling called Weiß, owner of Reichenfels; bought half in 1601 from his father-in-law and the other half in 1602 (pp. 632, 636).')
M('Heinrich v. Müffling, gen. Weiß', 'Heinrich v. Müffling gen. Weiß', 'punctuation variant (p. 636)')
P('Heinrich Michel', 'Heinrich Michel', 'Gutsbesitzer',
  'Heinrich Michel, kaufte ein Freigut um 2550 Mk. (S. 643); das Gut ging später an die Gemeinde.',
  'Heinrich Michel, bought a free estate for 2,550 marks (p. 643); the estate later passed to the parish.')
P('J. Heinrich Münch', 'Johann Heinrich Münch', 'Gutsbesitzer',
  'J. Heinrich Münch, kaufte 1761 Güter (Frössen) von der Herrschaft Lobenstein (S. 796).',
  'J. Heinrich Münch, bought estates (Frössen) from the lordship of Lobenstein in 1761 (p. 796).')
P('Karl Heinrich Spangenberg', 'Karl Heinrich Spangenberg', 'Gutsbesitzer',
  'Karl Heinrich Spangenberg, Rittergutsbesitzer (Liste der Rittergüter S. 223; Kauf eines Gutes S. 456).',
  'Karl Heinrich Spangenberg, manor owner (list of manors p. 223; purchase of an estate p. 456).')
P('Heinrich Ferd. Bruhm', 'Heinrich Ferdinand Bruhm', 'Gutsbesitzer',
  'Heinrich Ferd. Bruhm, Rittergutsbesitzer (Liste der Rittergüter, S. 223).',
  'Heinrich Ferd. Bruhm, manor owner (list of manors, p. 223).',
  note='Possibly identical with the Gera merchant Heinrich Bruhm (p. 833); not stated by Brückner.')
P('Heinrich Bruhm', 'Heinrich Bruhm (Kaufmann in Gera)', 'Stifter',
  'Heinrich Bruhm, Kaufmann zu Gera; stiftete für die Stadt Gera 1000 Thlr. für die städtische Armenkasse, 500 Thlr. für die Gesamtstadtschule und 500 Thlr. für die Schulbibliothek (S. 833).',
  'Heinrich Bruhm, merchant at Gera; donated to the town of Gera 1,000 thalers for the municipal poor fund, 500 thalers for the combined town school and 500 thalers for the school library (p. 833).',
  note='Possibly identical with the manor owner Heinrich Ferd. Bruhm (p. 223); not stated by Brückner.')

# --- clergy and officials ---------------------------------------------------------------------------
P('Heinrich v. Brunswick', 'Heinrich von Brunswick', 'Geistlicher',
  'Heinrich von Brunswick, 1297 und 1302 Pfarrer (Deutschordenscomthur) zu Schleiz (S. 584).',
  'Heinrich of Brunswick, parish priest (Teutonic commander) at Schleiz in 1297 and 1302 (p. 584).')
P('Heinrich Schwarz', 'Heinrich Schwarz', 'Geistlicher',
  'Heinrich Schwarz, 1341 Pfarrer zu Schleiz (S. 584).',
  'Heinrich Schwarz, parish priest at Schleiz in 1341 (p. 584).')
P('Heinrich v. Hopfgarten', 'Heinrich von Hopfgarten', 'Geistlicher',
  'Heinrich von Hopfgarten, 1399 Pfarrer zu Schleiz (S. 584).',
  'Heinrich of Hopfgarten, parish priest at Schleiz in 1399 (p. 584).')
P('Heinrich v. Tepen', 'Heinrich von Tepen', 'Geistlicher',
  'Heinrich von Tepen, 1332 Pfarrer zu Hohenleuben, später in Tanna, kam 1348 als Pfarrer nach Hof (S. 638, 685).',
  'Heinrich of Tepen, parish priest at Hohenleuben in 1332, later at Tanna, went to Hof as parish priest in 1348 (pp. 638, 685).')
P('Heinrich Tenner', 'Heinrich Tenner', 'Geistlicher',
  'Heinrich Tenner, 1407 und 1415 katholischer Pfarrer zu Gera (S. 434).',
  'Heinrich Tenner, Catholic parish priest at Gera in 1407 and 1415 (p. 434).')
P('Heinrich Smer', 'Heinrich Smer', 'Geistlicher',
  'Heinrich Smer, 1415 Pfarrer zu Göschitz (S. 610).',
  'Heinrich Smer, parish priest at Göschitz in 1415 (p. 610).')
P('Heinrich Scherenberg', 'Heinrich Scherenberg', 'Geistlicher',
  'Heinrich Scherenberg, erster Kaplan der Waldkapelle, vom Bischof von Naumburg bestätigt (S. 697).',
  'Heinrich Scherenberg, first chaplain of the forest chapel, confirmed by the bishop of Naumburg (p. 697).')
P('Heinrich Dopplick', 'Heinrich Dopplick', 'Geistlicher',
  'Heinrich Dopplick, 1494 neuer Priester einer Kapelle (S. 664).',
  'Heinrich Dopplick, new priest of a chapel in 1494 (p. 664).')
P('Heinrich Beyrer', 'Heinrich Beyrer', 'Geistlicher',
  'Heinrich Beyrer, Kaplan zur Reformationszeit, wegen papistischer Gesinnung von den Visitatoren abgesetzt (S. 652).',
  'Heinrich Beyrer, chaplain at the time of the Reformation, removed by the visitors for his papist views (p. 652).')
P('Heinrich Siber', 'Heinrich Siber', 'Geistlicher',
  'Heinrich Siber, erster lutherischer Pfarrer (S. 648).',
  'Heinrich Siber, first Lutheran parish priest (p. 648).')
P('Heinrich Klinger', 'Heinrich Klinger', 'Geistlicher',
  'Heinrich Klinger, erster lutherischer Pfarrer (S. 813).',
  'Heinrich Klinger, first Lutheran parish priest (p. 813).')
P('Heinrich Poßner', 'Heinrich Poßner', 'Geistlicher',
  'Heinrich Poßner, Pfarrer; sein Bildnis hängt in der herrschaftlichen Kapelle (S. 516).',
  'Heinrich Poßner, parish priest; his portrait hangs in the manorial chapel (p. 516).')
P('Heinrich Beck', 'Heinrich Beck', 'Geistlicher',
  'Heinrich Beck, bei der Einführung der Reformation zum Pfarrer ernannt, Diaconus war Georg Amandus (S. 665).',
  'Heinrich Beck, appointed parish priest when the Reformation was introduced; the deacon was Georg Amandus (p. 665).')
P('Heinrich Spörel', 'Heinrich Spörel', 'Bürgermeister',
  'Heinrich Spörel, Bürgermeister; Vermächtnis für arme Schulkinder (S. 667).',
  'Heinrich Spörel, mayor; bequest for poor schoolchildren (p. 667).')
P('Heinrich Schreiber', 'Heinrich Schreiber', 'Siedler',
  'Heinrich Schreiber, erbaute 1801 auf einer Höhe das erste Haus der nach ihm benannten Siedlung (S. 776).',
  'Heinrich Schreiber, built in 1801 the first house on a hill of the settlement named after him (p. 776).')
P('J. Heinrich Born', 'Johann Heinrich Born', 'Geistlicher',
  'Mag. J. Heinrich Born, Pastor zu Dohna; Stifter eines Legats (S. 308).',
  'Mag. J. Heinrich Born, pastor at Dohna; founder of a bequest (p. 308).')
P('J. Heinrich Scherber', 'Johann Heinrich Scherber', 'Geistlicher',
  'J. Heinrich Scherber, Pfarrer zu Berg; beschrieb das Leben des gelehrten Bauern Künzel in Rothenacker (S. 825).',
  'J. Heinrich Scherber, parish priest at Berg; wrote a biography of the learned peasant Künzel at Rothenacker (p. 825).')

# --- scholars, artists, writers ------------------------------------------------------------------------
P('Heinrich Schütz', 'Heinrich Schütz', 'Komponist',
  'Heinrich Schütz (Sagittarius), 1585-1672, Dresdner Oberkapellmeister, „wahrer Begründer der neueren deutschen Musik"; Geburtsort Köstritz (S. 498).',
  'Heinrich Schütz (Sagittarius), 1585-1672, chapel master at Dresden, "true founder of modern German music"; born at Köstritz (p. 498).')
P('Heinrich Albert', 'Heinrich Albert (Alberti)', 'Komponist, Liederdichter',
  'Heinrich Albert (Alberti), geb. 28. Juni 1604, berühmter Liederdichter und Komponist, Freund Simon Dachs, musikalische Seele des Königsberger Dichterkreises; nach Brückner † 1668 in Königsberg; aus Lobenstein (S. 722).',
  'Heinrich Albert (Alberti), born 28 June 1604, famous hymn poet and composer, friend of Simon Dach, musical soul of the Königsberg poets\' circle; according to Brückner died 1668 at Königsberg; native of Lobenstein (p. 722).',
  note='Brückner gives 1668 for his death.')
P('Heinrich Gottfr. Reichard', 'Heinrich Gottfried Reichard', 'Gelehrter',
  'Heinrich Gottfr. Reichard, geb. 1742, † 1801 in Grimma, Philologe; aus Schleiz (S. 591).',
  'Heinrich Gottfr. Reichard, born 1742, died 1801 at Grimma, philologist; native of Schleiz (p. 591).')
P('Heinrich Gottlieb Reichard', 'Heinrich Gottlieb Reichard', 'Beamter',
  'Dr. Heinrich Gottlieb Reichard, zweiter Sohn des Geographen Chr. Gottl. Reichard; geb. 1789, Geh. Justizrat in Gera, † 1852 in Interlaken; aus Lobenstein (S. 723).',
  'Dr. Heinrich Gottlieb Reichard, second son of the geographer Chr. Gottl. Reichard; born 1789, privy justice councillor at Gera, died 1852 at Interlaken; native of Lobenstein (p. 723).')
P('J. Heinrich Behr', 'Johann Heinrich Behr', 'Gelehrter, Baumeister',
  'J. Heinrich Behr, geb. 1647, † 1717, Mathematiker, Ingenieur und Baumeister in Berlin; aus Schleiz (S. 591).',
  'J. Heinrich Behr, born 1647, died 1717, mathematician, engineer and master builder in Berlin; native of Schleiz (p. 591).')
P('Heinrich Balth. Roth', 'Heinrich Balthasar Roth', 'Gelehrter',
  'Heinrich Balth. Roth, geb. 1639, † 1689, Professor der Rechte zu Jena; aus Gera (S. 833).',
  'Heinrich Balth. Roth, born 1639, died 1689, professor of law at Jena; native of Gera (p. 833).')
