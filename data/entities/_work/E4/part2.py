# -*- coding: utf-8 -*-
"""Specific persons of the houses Reuß j. L. / ä. L. (16th-19th century)."""
from part1 import P, M, R, AMB

# --- Heinrich Posthumus and the reigning princes -----------------------------------------
P('Heinrich Posthumus', 'Heinrich Posthumus', 'Landesherr',
  'Heinrich Posthumus Reuß (als Fürst Heinrich II. gezählt), Herr zu Gera, Stifter der jüngeren Linie Reuß (Reuß j. L.); '
  'geb. 10. Juni 1572, zwei Monate nach dem Tod des Vaters (daher Posthumus), † 3. Dez. 1635; eigene Regierung 1595-1635; '
  'Vater der Brüder Heinrich II., III., IX. und X.',
  'Heinrich Posthumus Reuss (counted as Heinrich II.), lord of Gera, founder of the younger line of Reuss (Reuss j. L.); '
  'born 10 June 1572, two months after his father\'s death (hence Posthumus), died 3 Dec. 1635; ruled in his own right 1595-1635; '
  'father of Heinrich II., III., IX. and X.',
  wd='Q97035',
  note='Brückner uses the epithet instead of a numeral (Tab. VI, p. 394; text pp. 375-376). Not to be confused with his son Heinrich II. von Gera (1602-1670).')
M('Heinrichs Posthumus', 'Heinrich Posthumus', 'genitive')

P('Fürst Heinrich XIV', 'Heinrich XIV. (Fürst Reuß j. L.)', 'Landesherr',
  'Heinrich XIV., regierender Fürst Reuß j. L. seit 11. Juli 1867; geb. 28. Mai 1832; verheiratet mit Pauline Louise Agnes von Württemberg; '
  'Urheber, Plangeber und Förderer des Buches (Vorwort, S. III).',
  'Heinrich XIV., reigning prince of Reuss (younger line) from 11 July 1867; born 28 May 1832; married to Pauline Louise Agnes of Württemberg; '
  'initiator, planner and promoter of the book (preface, p. III).',
  wd='Q553108',
  note='Brückner dedicates the work to him (p. III). The bare form "Heinrich XIV." is ambiguous (also Heinrich XIV. von Greiz, 1749-1799) and is listed separately.')
M('Heinrich Reuß XIV', 'Fürst Heinrich XIV', 'p. 499: the prince as Erbprinz (1862/63) and as ruler')

P('Heinrich LXII', 'Heinrich LXII. (Fürst Reuß j. L.)', 'Landesherr',
  'Heinrich LXII., Fürst von Reuß-Schleiz und seit 1848 des vereinigten Reuß j. L.; geb. 1785, regierte in Schleiz 1818-1848, im '
  'Gesamtland 1848-1854, † 19. Juni 1854 ohne Erben; Bruder und Vorgänger Heinrichs LXVII.',
  'Heinrich LXII., prince of Reuss-Schleiz and from 1848 of the united Reuss j. L.; born 1785, ruled in Schleiz 1818-1848 and in the '
  'whole principality 1848-1854, died 19 June 1854 without heirs; brother and predecessor of Heinrich LXVII.',
  wd='Q73528')
for k in ('Fürst Heinrich LXII', 'Fürsten Heinrich LXII', 'Heinrichs LXII'):
    M(k, 'Heinrich LXII', 'title/genitive variant')

P('Heinrich LXVII', 'Heinrich LXVII. (Fürst Reuß j. L.)', 'Landesherr',
  'Heinrich LXVII., Fürst Reuß j. L.; geb. 20. Okt. 1789, Nachfolger seines Bruders Heinrich LXII. am 19. Juni 1854, † 11. Juli 1867; '
  'verheiratet 1820 mit Sophie Adelheid von Reuß-Ebersdorf; Vater Heinrichs XIV.; Umbau des Schlosses Osterstein.',
  'Heinrich LXVII., prince of Reuss j. L.; born 20 Oct. 1789, succeeded his brother Heinrich LXII. on 19 June 1854, died 11 July 1867; '
  'married 1820 Sophie Adelheid of Reuss-Ebersdorf; father of Heinrich XIV.; rebuilt Osterstein castle.',
  wd='Q215064')
for k in ('Fürst Heinrich LXVII', 'Fürsten Heinrich LXVII', 'Heinrichs LXVII', 'Heinrich LXVII. Reuß j. L', 'Heinrich Reuß LXVII'):
    M(k, 'Heinrich LXVII', 'title/genitive variant')

P('Heinrich LXXII', 'Heinrich LXXII. (Fürst Reuß-Lobenstein-Ebersdorf)', 'Landesherr',
  'Heinrich LXXII., Fürst von Lobenstein-Ebersdorf, einziger Sohn Heinrichs LI.; geb. 1797, regierte 1822-1848 (Verzicht am 1. Okt. 1848), '
  '† Febr. 1853 in Dresden als letzter männlicher Sproß des Specialhauses Lobenstein; nannte die alte Landesvertretung „verrottet".',
  'Heinrich LXXII., prince of Lobenstein-Ebersdorf, only son of Heinrich LI.; born 1797, ruled 1822-1848 (abdicated 1 Oct. 1848), died Feb. 1853 '
  'in Dresden as the last male of the special house of Lobenstein; called the old estates "rotten".',
  note='The Marstall of the Osterstein is not his work (corrigendum, p. 833).')
for k in ('Fürst Heinrich LXXII', 'Fürst Heinrich Reuß LXXII'):
    M(k, 'Heinrich LXXII', 'title variant')

P('Heinrich XLII', 'Heinrich XLII. (Fürst Reuß zu Schleiz)', 'Landesherr',
  'Heinrich XLII., Graf, seit 1806 Fürst Reuß zu Schleiz; geb. 1752 zu Löhma, regierte 1784-1818 (Rheinbund 1807), † 1818; Sohn Heinrichs XII., Vater '
  'Heinrichs LXII. und LXVII.',
  'Heinrich XLII., count and from 1806 prince of Reuss-Schleiz; born 1752 at Löhma, ruled 1784-1818 (Confederation of the Rhine 1807), died 1818; son of '
  'Heinrich XII., father of Heinrich LXII. and LXVII.',
  note='One mention on p. 384 ("der ältere, Heinrich XLII.", his son and successor) is a misprint for LXII.; Brückner corrects it himself on p. 833 '
       '("S. 384, Z. 17 v. u. lies: LXII. statt XLII.").')
M('Fürst Heinrich XLII', 'Heinrich XLII', 'title variant')

P('Heinrich XXXV', 'Heinrich XXXV. (Fürst Reuß-Lobenstein)', 'Landesherr',
  'Heinrich XXXV., Graf, seit 1790 Reichsfürst von Reuß-Lobenstein; geb. 1738, 1802 Mitregent von Gera, † 1805 ohne Erben (Lobenstein fiel an Heinrich LIV.).',
  'Heinrich XXXV., count, from 1790 prince of the Empire of Reuss-Lobenstein; born 1738, co-regent of Gera from 1802, died 1805 without heirs '
  '(Lobenstein passed to Heinrich LIV.).',
  wd='Q119076424')
M('Fürsten Heinrich XXXV', 'Heinrich XXXV', 'title variant')

P('Heinrich XLIII', 'Heinrich XLIII. (Reuß-Köstritz)', 'Landesherr',
  'Heinrich XLIII., Graf Reuß zu Köstritz (von Brückner auch „Fürst" genannt); geb. 1752, übernahm 1783 das Paragiat, † 1814; Enkel Heinrichs XXIV.; Förderer von Kunst, Parkanlagen '
  'und der Köstritzer Brauerei, baute die Burg Reichenfels um (1806).',
  'Heinrich XLIII., count Reuss of Köstritz (also called "prince" by Brückner); born 1752, took over the Paragiat in 1783, died 1814; grandson of Heinrich XXIV.; patron of the arts, '
  'parks and the Köstritz brewery, rebuilt Reichenfels castle (1806).',
  wd='Q1486203')
for k in ('Fürst Heinrich XLIII', 'Heinrichs XLIII'):
    M(k, 'Heinrich XLIII', 'title/genitive variant')

P('Heinrich LIV', 'Heinrich LIV. (Fürst Reuß-Lobenstein-Selbitz)', 'Landesherr',
  'Heinrich LIV., Neffe Heinrichs XXI. aus der Nebenlinie Selbitz; geb. 1767, erbte 1805 Lobenstein, 1806 Reichsfürst, † 1824 ohne Nachkommen (Lobenstein fiel an Ebersdorf); '
  'verheiratet 1) Marie von Stolberg-Wernigerode, 2) Franziska Reuß-Köstritz.',
  'Heinrich LIV., nephew of Heinrich XXI. of the Selbitz branch; born 1767, inherited Lobenstein in 1805, prince of the Empire 1806, died 1824 without issue '
  '(Lobenstein passed to Ebersdorf); married 1) Marie of Stolberg-Wernigerode, 2) Franziska Reuss-Köstritz.',
  wd='Q55875295')

P('Heinrich LI', 'Heinrich LI. (Fürst Reuß-Ebersdorf)', 'Landesherr',
  'Heinrich LI., „der Gute", Graf, seit 1806 Fürst Reuß zu Ebersdorf; geb. 1761, regierte 1779-1822, 1802 Mitregent in Gera und Saalburg; verheiratet mit Louise von Hoym; '
  'Vater Heinrichs LXXII. und Schwiegervater Heinrichs LXVII.; bewirtete 1806 Napoleon in Ebersdorf.',
  'Heinrich LI., "the Good", count, from 1806 prince Reuss of Ebersdorf; born 1761, ruled 1779-1822, co-regent of Gera and Saalburg from 1802; married Louise of Hoym; '
  'father of Heinrich LXXII. and father-in-law of Heinrich LXVII.; entertained Napoleon at Ebersdorf in 1806.',
  wd='Q642401')
M('Heinrichs LI', 'Heinrich LI', 'genitive')

P('Heinrich LXIX', 'Heinrich LXIX. (Fürst Reuß-Köstritz)', 'Landesherr',
  'Heinrich LXIX., Fürst Reuß-Köstritz; geb. 19. Mai 1792, folgte 1856 seinem Vetter Heinrich LXIV. im Paragiat Köstritz; verheiratet 1834 mit Mathilde von Riese-Stallburg; '
  'ohne Erben (die Linie Heinrichs VI. endet mit ihm).',
  'Heinrich LXIX., prince Reuss-Köstritz; born 19 May 1792, succeeded his cousin Heinrich LXIV. in the Köstritz Paragiat in 1856; married 1834 Mathilde of Riese-Stallburg; '
  'without heirs (the line of Heinrich VI. ends with him).')
for k in ('Heinrich LXIX., Fürst Reuss-Köstritz', 'Heinrich LXIX., Fürst Reuss'):
    M(k, 'Heinrich LXIX', 'variant with title (list of manorial owners, p. 223)')

P('Heinrich XLIV', 'Heinrich XLIV. (Fürst Reuß-Köstritz, mittlerer Zweig)', 'Landesherr',
  'Heinrich XLIV., Graf, seit 1817 Fürst Reuß-Köstritz, mittlerer Zweig; geb. 1753, † 1832; Sohn Heinrichs IX.; Vater von sechs Söhnen (LX., LXIII., LXVI., LXX., LXXIV. und I.).',
  'Heinrich XLIV., count, from 1817 prince Reuss-Köstritz, middle branch; born 1753, died 1832; son of Heinrich IX.; father of six sons (LX, LXIII, LXVI, LXX, LXXIV and I).',
  wd='Q55875487')
M('Heinrich XXXXIV', 'Heinrich XLIV', 'old-style numeral XXXXIV = XLIV (p. 388)')

# --- 18th-century counts of Gera, Lobenstein, Ebersdorf, Köstritz, Schleiz ----------------------
P('Graf Heinrich XXX', 'Heinrich XXX. (Graf zu Gera)', 'Landesherr',
  'Heinrich XXX., Graf Reuß zu Gera, letzter Graf von Gera; geb. 1727, regierte 1748-1802 (54 Jahre), † 26./28. April 1802 kinderlos; verheiratet mit Louise Christiane, '
  'Pfalzgräfin von Zweibrücken-Birkenfeld-Gelnhausen; Sohn Heinrichs XXV.',
  'Heinrich XXX., count Reuss of Gera, last count of Gera; born 1727, ruled 1748-1802 (54 years), died 26/28 April 1802 childless; married Louise Christiane, '
  'Countess Palatine of Zweibrücken-Birkenfeld-Gelnhausen; son of Heinrich XXV.')
M('Heinrichs XXX', 'Graf Heinrich XXX', 'genitive (his widow, p. 422)')

P('Graf Heinrich XVIII', 'Heinrich XVIII. (Graf zu Gera, Fundator)', 'Landesherr',
  'Heinrich XVIII., Graf Reuß zu Gera, genannt Fundator (Bauherr); geb. 1677, zunächst unter Vormundschaft, seit 1698 selbständig, † 1735 unvermählt; '
  'Schöpfer der St.-Salvator-Kirche, des Zucht- und Waisenhauses und der Neustadt in Gera; ältester Sohn Heinrichs IV.',
  'Heinrich XVIII., count Reuss of Gera, called Fundator (founder/builder); born 1677, at first under guardianship, independent from 1698, died 1735 unmarried; '
  'creator of St. Salvator church, the workhouse/orphanage and the Neustadt in Gera; eldest son of Heinrich IV.')

P('Graf Heinrich XXV', 'Heinrich XXV. (Graf zu Gera)', 'Landesherr',
  'Heinrich XXV., Graf Reuß zu Gera, Bruder und Nachfolger Heinrichs XVIII.; regierte 1735-1748, † 1748; Vater Heinrichs XXX.; gründete eine Kolonie von Häuslern und Tagelöhnern.',
  'Heinrich XXV., count Reuss of Gera, brother and successor of Heinrich XVIII.; ruled 1735-1748, died 1748; father of Heinrich XXX.; founded a colony of cottagers and day laborers.',
  note='Identified from the context (Gera territory, 1730s-1740s); Heinrich XXV. von Lobenstein-Selbitz (1724-1801) is a different person.')

P('Graf Heinrich XV', 'Heinrich XV. (Graf Reuß zu Lobenstein)', 'Landesherr',
  'Heinrich XV., Graf Reuß zu Lobenstein, ältester Sohn Heinrichs III.; geb. 1674, übernahm 1710 die Herrschaft Lobenstein, † 1739; '
  'verheiratet mit Ernestine Eleonore von Schönburg-Waldenburg; Vater Heinrichs II.',
  'Heinrich XV., count Reuss of Lobenstein, eldest son of Heinrich III.; born 1674, took over the lordship of Lobenstein in 1710, died 1739; '
  'married Ernestine Eleonore of Schönburg-Waldenburg; father of Heinrich II.',
  note='Identified from the context (p. 798: residence 1706-1709 and after the fire of Lobenstein castle).')

P('Heinrich XXIV. von Köstritz', 'Heinrich XXIV. (Graf Reuß, Stifter der Linie Köstritz)', 'Landesherr',
  'Heinrich XXIV., jüngerer Sohn Heinrichs I. von Schleiz; geb. 1681, † 1748; erstes Haupt der Nebenlinie Köstritz (Paragiat); '
  'verheiratet mit Marie Eleonore Emilie von Promnitz-Dittersbach; Vater Heinrichs VI., IX. und XXIII.',
  'Heinrich XXIV., younger son of Heinrich I. of Schleiz; born 1681, died 1748; first head of the cadet line Köstritz (Paragiat); '
  'married Marie Eleonore Emilie of Promnitz-Dittersbach; father of Heinrich VI., IX. and XXIII.')

P('Heinrich XXIV. von Ebersdorf', 'Heinrich XXIV. (Graf Reuß-Ebersdorf)', 'Landesherr',
  'Heinrich XXIV., Graf Reuß zu Ebersdorf, ältester Sohn Heinrichs XXIX.; geb. 1724, regierte 1747-1779; verheiratet mit Caroline Ernestine von Erbach-Schönberg; Vater Heinrichs LI.',
  'Heinrich XXIV., count Reuss of Ebersdorf, eldest son of Heinrich XXIX.; born 1724, ruled 1747-1779; married Caroline Ernestine of Erbach-Schönberg; father of Heinrich LI.')

P('Heinrichs XXIX', 'Heinrich XXIX. (Graf Reuß-Ebersdorf)', 'Landesherr',
  'Heinrich XXIX., Graf Reuß zu Ebersdorf, einziger Sohn Heinrichs X.; geb. 1699, regierte bis 1747; Freund Zinzendorfs, gründete 1733 die Herrnhuter Kolonie Ebersdorf; '
  'verheiratet mit Sophie Theodore von Castell-Remlingen.',
  'Heinrich XXIX., count Reuss of Ebersdorf, only son of Heinrich X.; born 1699, ruled until 1747; friend of Zinzendorf, founded the Moravian colony at Ebersdorf in 1733; '
  'married Sophie Theodore of Castell-Remlingen.')

P('Heinrichs XXVI', 'Heinrich XXVI. (Reuß-Lobenstein-Selbitz)', 'Landesherr',
  'Heinrich XXVI., jüngerer Sohn Heinrichs III. von Lobenstein; geb. 1681, † 1730; verheiratet 1715 mit Juliane Rebecca von Tättenbach, Erbin von Selbitz; Stifter der Nebenlinie Reuß-Selbitz.',
  'Heinrich XXVI., younger son of Heinrich III. of Lobenstein; born 1681, died 1730; married 1715 Juliane Rebecca of Tättenbach, heiress of Selbitz; founder of the cadet line Reuss-Selbitz.')

P('Heinrich Reuß XXVI', 'Heinrich XXVI. (Graf Reuß-Ebersdorf, Historiker)', 'Landesherr, Gelehrter',
  'Heinrich XXVI., Graf Reuß zu Ebersdorf, Sohn Heinrichs XXIX.; geb. 1725, † 1796; Historiker des Hauses und Landes Reuß, Urkundensammler; Gewährsmann für Majers „Chronik der Reußen".',
  'Heinrich XXVI., count Reuss of Ebersdorf, son of Heinrich XXIX.; born 1725, died 1796; historian of the house and land of Reuss, collector of charters; inspirer of Majer\'s "Chronik der Reußen".',
  wd='Q55132822',
  note='Identified from the context (p. 324 fn.: Majer\'s Chronik der Reußen) and p. 738 (born 1725, died 1796 at Ebersdorf); the bare form "Heinrich XXVI." is ambiguous and listed separately.')

P('Graf Heinrich XII', 'Heinrich XII. (Graf Reuß zu Schleiz)', 'Landesherr',
  'Heinrich XII., Graf Reuß zu Schleiz, jüngerer Sohn Heinrichs XI.; geb. 1716, regierte 1744-1784, † 25. Juni 1784; verfaßte Andachtsschriften im Geiste der Herrnhuter; Stifter des Waisenhauses in Kirschkau und mehrerer Kirchen; '
  'Vater Heinrichs XLII.',
  'Heinrich XII., count Reuss of Schleiz, younger son of Heinrich XI.; born 1716, ruled 1744-1784, died 25 June 1784; wrote devotional works in the Moravian spirit; founder of the orphanage at Kirschkau and of several churches; '
  'father of Heinrich XLII.',
  wd='Q12363657')
for k in ('Grafen Heinrich XII', 'Heinrichs XII'):
    M(k, 'Graf Heinrich XII', 'title/genitive variant (all mentions concern the count of Schleiz)')

P('Heinrich Reuß XI', 'Heinrich XI. (Graf Reuß zu Schleiz)', 'Landesherr',
  'Heinrich XI., Graf Reuß zu Schleiz, älterer Sohn Heinrichs I.; geb. 1669, regierte 1692-1726, † 1726; legte die Heinrichstadt in Schleiz an (1706), baute das neue Residenzschloß und sechs Kirchen im Land; '
  'Vater Heinrichs I. und XII.',
  'Heinrich XI., count Reuss of Schleiz, elder son of Heinrich I.; born 1669, ruled 1692-1726, died 1726; laid out the Heinrichstadt at Schleiz (1706), built the new residential castle and six churches in the country; '
  'father of Heinrich I. and XII.',
  note='Identified from the context (Schleiz territory, 1690s-1720s); the bare form "Heinrich XI." is ambiguous (also Heinrich XI. von Obergreiz, 1722-1800).')
M('Heinrichs XI', 'Heinrich Reuß XI', 'genitive (legacy, portrait and church of Count Heinrich XI. of Schleiz)')

P('Heinrich I. von Schleiz', 'Heinrich I. (Graf Reuß zu Schleiz)', 'Landesherr',
  'Heinrich I., Enkel des Heinrich Posthumus, Sohn Heinrichs III.; geb. 1639, übernahm 1666 die Herrschaft Schleiz, Stammvater des jetzigen Fürstenhauses; residierte nach dem Brand von 1689 in Köstritz, wo er 1692 starb; '
  'dreimal verheiratet; Vater Heinrichs XI. und XXIV.',
  'Heinrich I., grandson of Heinrich Posthumus, son of Heinrich III.; born 1639, took over the lordship of Schleiz in 1666, ancestor of the present princely house; moved his residence to Köstritz after the fire of 1689 and died there in 1692; '
  'married three times; father of Heinrich XI. and XXIV.')
M('Graf Heinrich I', 'Heinrich I. von Schleiz', 'title variant (purchase of the manor of Köstritz, p. 495)')
M('Heinrich Reuß I', 'Heinrich I. von Schleiz', 'identified from the context (p. 651: purchase 1681 of the manor of Triebes for the Köstritz Paragiat)')

P('Heinrichs III', 'Heinrich III. (Reuß, Haupt der Linie Schleiz)', 'Landesherr',
  'Heinrich III., Sohn des Heinrich Posthumus, Haupt der schleizer Linie; geb. 1603, wohnte seit 1637 in Schleiz, † 1640 in Karlsbad; verheiratet mit Juliane Elise Rheingräfin zu Neufville, Witwe Heinrichs IV. von Obergreiz; Vater Heinrichs I.',
  'Heinrich III., son of Heinrich Posthumus, head of the Schleiz line; born 1603, lived at Schleiz from 1637, died 1640 at Carlsbad; married Juliane Elise, Rhinegravine of Neufville, widow of Heinrich IV. of Obergreiz; father of Heinrich I.')
M('Heinrich Reuß zu Schleiz', 'Heinrichs III', 'p. 401: husband of Juliane Elisabeth Rheingräfin v. Neufville (Tab. VII: Heinrich III., Haupt der schleizer Linie)')

P('Heinrich Reuß III', 'Heinrich III. (Graf Reuß zu Lobenstein)', 'Landesherr',
  'Heinrich III., Sohn Heinrichs X. von Lobenstein; geb. 1648, Reichsgraf seit 1673, Gründer der Specialline Lobenstein, † 1710; verheiratet mit Marie Christiane von Leiningen-Westerburg; Vater Heinrichs XV., XVII., XXVI.',
  'Heinrich III., son of Heinrich X. of Lobenstein; born 1648, count of the Empire from 1673, founder of the special line of Lobenstein, died 1710; married Marie Christiane of Leiningen-Westerburg; father of Heinrich XV., XVII., XXVI.',
  note='Identified from the context (p. 715: wife Marie Christiane, née Leiningen).')

P('Heinrichs IV', 'Heinrich IV. (Herr von Obergreiz)', 'Landesherr',
  'Heinrich IV., Gründer des Hauses Obergreiz (1625); geb. 1597, † 1629; verheiratet mit Juliane Elisabeth Rheingräfin zu Neufville (später Gattin Heinrichs III. von Schleiz); Vater Heinrichs I.',
  'Heinrich IV., founder of the house of Obergreiz (1625); born 1597, died 1629; married Juliane Elisabeth, Rhinegravine of Neufville (later wife of Heinrich III. of Schleiz); father of Heinrich I.')

P('Heinrichs VI', 'Heinrich VI. (Graf Reuß-Köstritz)', 'Landesherr',
  'Heinrich VI., älterer Sohn Heinrichs XXIV. von Köstritz, königlich dänischer Geheimrat; geb. 1707, † 1783; Haupt der älteren Köstritzer Linie, die mit Heinrich LXIX. endet.',
  'Heinrich VI., elder son of Heinrich XXIV. of Köstritz, Royal Danish privy councillor; born 1707, died 1783; head of the older Köstritz line, which ends with Heinrich LXIX.',
  note='Identified from the context (p. 388: "die Linie Heinrichs VI.").')

P('Heinrichs XV', 'Heinrich XV. (von Obergreiz)', 'Landesherr',
  'Heinrich XV., Sohn Heinrichs I. von Obergreiz; geb. 1676, † 1690; sein Tod vor 1694 führte zur Teilung zwischen Heinrich VI. und XVI.',
  'Heinrich XV., son of Heinrich I. of Obergreiz; born 1676, died 1690; his death before 1694 led to the partition between Heinrich VI. and XVI.')

P('Heinrichs XVII', 'Heinrich XVII. (Graf Reuß-Lobenstein)', 'Adliger, Offizier',
  'Heinrich XVII., Sohn Heinrichs III. von Lobenstein; Oberst in hessen-kasselischen Diensten; geb. 1676, † 1706; verheiratet mit Eleonore Sophie von Giech-Thurnau.',
  'Heinrich XVII., son of Heinrich III. of Lobenstein; colonel in Hessian (Kassel) service; born 1676, died 1706; married Eleonore Sophie of Giech-Thurnau.')

P('Heinrichs XIV', 'Heinrich XIV. (Graf Reuß zu Greiz, Feldmarschalleutnant)', 'Adliger, Offizier',
  'Heinrich XIV., Sohn Heinrichs XI. von Greiz; geb. 1749, † 1799; kaiserlicher Feldmarschalleutnant und Gesandter am preußischen Hof.',
  'Heinrich XIV., son of Heinrich XI. of Greiz; born 1749, died 1799; Imperial lieutenant field marshal and envoy at the Prussian court.',
  note='Not the reigning prince Heinrich XIV. (b. 1832), see "Fürst Heinrich XIV".')

# --- younger lines of the nineteenth century (Köstritz) ----------------------------------
P('Heinrich Reuß XII', 'Heinrich XII. (Prinz Reuß, Köstritz)', 'Prinz, Offizier',
  'Heinrich XII., Prinz Reuß (mittlere Linie Köstritz), preußischer Major; geb. 1829, 1866 im Feld gefallen; verheiratet 1858 mit Anna von Pleß-Hochberg-Fürstenstein; seine Witwe heiratete seinen Bruder Heinrich XIII. (S. 833).',
  'Heinrich XII., Prince Reuss (middle line Köstritz), Prussian major; born 1829, killed in action in 1866; married 1858 Anna of Pless-Hochberg-Fürstenstein; his widow married his brother Heinrich XIII. (p. 833).')

P('Heinrich Reuß VII', 'Heinrich VII. (Prinz Reuß, Köstritz)', 'Prinz, Diplomat',
  'Heinrich VII., Prinz Reuß (mittlere Linie Köstritz); geb. 1825; außerordentlicher Gesandter und bevollmächtigter Minister des Königs von Preußen und des Norddeutschen Bundes am russischen Hof.',
  'Heinrich VII., Prince Reuss (middle line Köstritz); born 1825; extraordinary envoy and minister plenipotentiary of the King of Prussia and the North German Confederation at the Russian court.')

P('Heinrich Reuß XIII', 'Heinrich XIII. (Prinz Reuß, Köstritz)', 'Prinz, Offizier',
  'Heinrich XIII., Prinz Reuß (mittlere Linie Köstritz), preußischer Major; geb. 1830; heiratete die Witwe seines Bruders Heinrich XII. (S. 833).',
  'Heinrich XIII., Prince Reuss (middle line Köstritz), Prussian major; born 1830; married the widow of his brother Heinrich XII. (p. 833).')

P('Heinrich XXVII', 'Heinrich XXVII. (Erbprinz Reuß j. L.)', 'Prinz',
  'Heinrich XXVII., Sohn Heinrichs XIV.; geb. 10. Nov. 1858, Erbprinz seit 11. Juli 1867.',
  'Heinrich XXVII., son of Heinrich XIV.; born 10 Nov. 1858, hereditary prince since 11 July 1867.')

P('Heinrich LXXIV', 'Heinrich LXXIV. (Fürst Reuß-Köstritz, mittlere Linie)', 'Prinz',
  'Heinrich LXXIV., Sohn Heinrichs XLIV.; geb. 1798, 1870 noch lebend; verheiratet 1) 1825 Clementine von Reichenbach-Goschütz, 2) 1855 Eleonore von Stolberg-Wernigerode; Vater Heinrichs IX., XXV. und XXXI.',
  'Heinrich LXXIV., son of Heinrich XLIV.; born 1798, still alive in 1870; married 1) 1825 Clementine of Reichenbach-Goschütz, 2) 1855 Eleonore of Stolberg-Wernigerode; father of Heinrich IX., XXV. and XXXI.',
  note='The cell on p. 398 ("Heinrich LXXIV., g. 1798, † 1855") appears to be a garbled duplicate of the cell "Heinrich LXXIII., g. 1798, † 1855" (younger line, same page); the text (p. 388) and Tab. XI (p. 399) show him alive.')

P('Heinrich LXIII', 'Heinrich LXIII. (Reuß-Köstritz, mittlere Linie)', 'Prinz',
  'Heinrich LXIII., Sohn Heinrichs XLIV.; geb. 1786, † 1841; verheiratet 1) Eleonore von Stolberg-Wernigerode, 2) deren Schwester Caroline; Vater von acht Söhnen, u. a. Heinrich IV., VII., XIII., XV., XVII.',
  'Heinrich LXIII., son of Heinrich XLIV.; born 1786, died 1841; married 1) Eleonore of Stolberg-Wernigerode, 2) her sister Caroline; father of eight sons, among them Heinrich IV., VII., XIII., XV., XVII.')

P('Heinrich LX', 'Heinrich LX. (Reuß-Köstritz, mittlere Linie)', 'Prinz',
  'Heinrich LX., Sohn Heinrichs XLIV.; geb. 1784, † 1833; verheiratet 1819 mit Dorothea Caroline von Carolath-Beuthen.',
  'Heinrich LX., son of Heinrich XLIV.; born 1784, died 1833; married 1819 Dorothea Caroline of Carolath-Beuthen.',
  note='The cell on p. 398 (Tab. X, "Heinrich LX., g. 1784, † 1813") is printed "H. LXI., g. 1784, † 1813" (a son of Heinrich XLIII.); the transcription reads LX.')

P('Heinrich LXIV', 'Heinrich LXIV. (Reuß-Köstritz)', 'Landesherr',
  'Heinrich LXIV., einziger nachgelassener Sohn Heinrichs XLIII., österreichischer Feldmarschalleutnant; geb. 1787, folgte 1814 im Paragiat Köstritz, † 15. Sept. 1856 bei Wien; mit ihm erlosch sein Zweig.',
  'Heinrich LXIV., only surviving son of Heinrich XLIII., Austrian lieutenant field marshal; born 1787, succeeded in the Köstritz Paragiat in 1814, died 15 Sept. 1856 near Vienna; his branch became extinct with him.')

P('Heinrich XLVIII', 'Heinrich XLVIII. (Reuß-Köstritz)', 'Prinz',
  'Heinrich XLVIII., jüngerer Sohn Heinrichs VI. von Köstritz; geb. 1759, † 1825; verheiratet mit Christiane Henriette von Schönburg-Wechselburg; Vater der Theresia (Theresienstiftung 1858).',
  'Heinrich XLVIII., younger son of Heinrich VI. of Köstritz; born 1759, died 1825; married Christiane Henriette of Schönburg-Wechselburg; father of Theresia (Theresia foundation of 1858).')
M('Heinrichs XLVIII', 'Heinrich XLVIII', 'genitive (his daughter Theresia, p. 498)')

P('Heinrich XXXVII', 'Heinrich XXXVII. (Reuß-Köstritz)', 'Prinz',
  'Heinrich XXXVII., ältester Sohn Heinrichs IX. von Köstritz (mittlere Linie); nach Tab. X geb. 1747, † 1774.',
  'Heinrich XXXVII., eldest son of Heinrich IX. of Köstritz (middle line); according to Tab. X born 1747, died 1774.')

P('Heinrich XXXIX', 'Heinrich XXXIX. (Reuß-Köstritz)', 'Prinz',
  'Heinrich XXXIX., Sohn Heinrichs IX. von Köstritz; geb. 1750, † 1815; verheiratet mit Henriette von Sinzendorf, Witwe Heinrich Augusts de la Motte Fouqué.',
  'Heinrich XXXIX., son of Heinrich IX. of Köstritz; born 1750, died 1815; married Henriette of Sinzendorf, widow of Heinrich August de la Motte Fouqué.')

P('Heinrich XXXXVII', 'Heinrich XLVII. (Reuß-Köstritz, jüngere Linie)', 'Prinz',
  'Heinrich XLVII. (gedruckt „XXXXVII."), Sohn Heinrichs XXIII. von Köstritz (jüngere Linie); nach Tab. X geb. 1756, † 1833.',
  'Heinrich XLVII. (printed "XXXXVII."), son of Heinrich XXIII. of Köstritz (younger line); according to Tab. X born 1756, died 1833.')

P('Heinrich LII', 'Heinrich LII. (Reuß-Köstritz, jüngere Linie)', 'Prinz',
  'Heinrich LII., Sohn Heinrichs XXIII. von Köstritz (jüngere Linie); geb. 1763, † 1851; Stifter der Heinrichsstiftung (1851) in Köstritz; verheiratet mit Justine von Watteville.',
  'Heinrich LII., son of Heinrich XXIII. of Köstritz (younger line); born 1763, died 1851; founder of the Heinrich foundation (1851) at Köstritz; married Justine of Watteville.')

P('Heinrich LV', 'Heinrich LV. (Reuß-Köstritz, Bischof der Herrnhuter)', 'Prinz, Geistlicher',
  'Heinrich LV., Sohn Heinrichs XXIII. aus dem Hause Köstritz; geb. 1768, † 1846 als Bischof der Herrnhuter (Brüdergemeine) zu London; verheiratet 1818 mit Marie von Reichenbach († 1840).',
  'Heinrich LV., son of Heinrich XXIII. of the house of Köstritz; born 1768, died 1846 as bishop of the Moravians (Herrnhuter) in London; married 1818 Marie of Reichenbach (d. 1840).')

P('Heinrich LIX', 'Heinrich LIX. (Reuß-Köstritz)', 'Prinz',
  'Heinrich LIX., Sohn Heinrichs XLIII. von Köstritz; geb. 1783, † 1784 (Tab. X).',
  'Heinrich LIX., son of Heinrich XLIII. of Köstritz; born 1783, died 1784 (Tab. X).')
P('Heinrich LXVI', 'Heinrich LXVI. (Reuß-Köstritz)', 'Prinz',
  'Heinrich LXVI., Sohn Heinrichs XLIV. von Köstritz; geboren und gestorben 1788 (Tab. XI).',
  'Heinrich LXVI., son of Heinrich XLIV. of Köstritz; born and died 1788 (Tab. XI).')
P('Heinrich LXX', 'Heinrich LXX. (Reuß-Köstritz)', 'Prinz',
  'Heinrich LXX., Sohn Heinrichs XLIV. von Köstritz; geb. 1793, † 1821 (Tab. XI).',
  'Heinrich LXX., son of Heinrich XLIV. of Köstritz; born 1793, died 1821 (Tab. XI).')
P('Heinrich LXXIII', 'Heinrich LXXIII. (Reuß-Köstritz, jüngere Linie)', 'Prinz',
  'Heinrich LXXIII., Enkel Heinrichs XXIII. von Köstritz (jüngere Linie); geb. 1798, † 1855.',
  'Heinrich LXXIII., grandson of Heinrich XXIII. of Köstritz (younger line); born 1798, died 1855.')
P('Heinrich LXXV', 'Heinrich LXXV. (Reuß-Köstritz, jüngere Linie)', 'Prinz',
  'Heinrich LXXV., Enkel Heinrichs XXIII. von Köstritz (jüngere Linie); geb. 3. Dez. 1800, † 24. Dez. 1800 (Tab. X).',
  'Heinrich LXXV., grandson of Heinrich XXIII. of Köstritz (younger line); born 3 Dec. 1800, died 24 Dec. 1800 (Tab. X).')
R('Heinrich LXV', 'transcription artefact: the table cell on p. 398 (Tab. X, row 9, col. 1) is printed "Franziska, g. 1788, † 1843. Gem. H. LIV. Reuß-Lobenstein, Wittwer Mariens v. Stolberg-Wernigerode"; there is no Heinrich LXV. in the print here')

P('Heinrich XXXI', 'Heinrich XXXI. (Prinz Reuß, Köstritz)', 'Prinz',
  'Heinrich XXXI., Sohn Heinrichs LXXIV. von Köstritz; geb. 1864 (Tab. XI).',
  'Heinrich XXXI., son of Heinrich LXXIV. of Köstritz; born 1864 (Tab. XI).')
P('Heinrich XXXII', 'Heinrich XXXII. (Prinz Reuß, Köstritz)', 'Prinz',
  'Heinrich XXXII., Prinz Reuß (Köstritz); geb. 1864 (Tab. XI, p. 399).',
  'Heinrich XXXII., Prince Reuss (Köstritz); born 1864 (Tab. XI, p. 399).')

# --- the Reuß branches of Greiz, Burgk, Untergreiz, Obergreiz (16th/17th c.) -------------------
P('Heinrich II. von Gera', 'Heinrich II. (Reuß zu Gera)', 'Landesherr',
  'Heinrich II., ältester überlebender Sohn des Heinrich Posthumus; geb. 1602, erhielt 1647 Gera (1666 Saalburg), Gründer des Specialhauses Gera, † 1670; verheiratet mit Katharina von Schwarzburg; Vater Heinrichs IV.',
  'Heinrich II., eldest surviving son of Heinrich Posthumus; born 1602, received Gera in 1647 (Saalburg in 1666), founder of the special house of Gera, died 1670; married Katharina of Schwarzburg; father of Heinrich IV.')

P('Heinrich II. v. Burgk', 'Heinrich II. (Herr von Burgk, Haus Untergreiz, 1634-1697)', 'Landesherr',
  'Heinrich II. von Burgk, Sohn Heinrichs V. von Untergreiz; geb. 1634, † 1697 ohne Erben; Sitz in Burgk; verheiratet mit Elise Sibille, Tochter Heinrichs II. von Burgk.',
  'Heinrich II. of Burgk, son of Heinrich V. of Untergreiz; born 1634, died 1697 without heirs; seat at Burgk; married Elise Sibille, daughter of Heinrich II. of Burgk.')
M('Heinrich Reuß II. zu Untergreiz und Burgk', 'Heinrich II. v. Burgk', 'p. 400: husband of Elisabeth Sibille (died 1697)')

P('Heinrichs II. Reuß zu Burgk', 'Heinrich II. (Herr von Burgk, 1575-1639)', 'Landesherr',
  'Heinrich II., Herr von Burgk, bayreuther Landeshauptmann; geb. 1575, † 1639; verheiratet mit Magdalene von Putbus; Vater Heinrichs III. († 1640) und der Elise Sibille.',
  'Heinrich II., lord of Burgk, captain of the Bayreuth territory; born 1575, died 1639; married Magdalene of Putbus; father of Heinrich III. (d. 1640) and of Elise Sibille.')

P('Heinrich VI. von Obergreiz', 'Heinrich VI. (Herr von Obergreiz und Dölau)', 'Landesherr, Feldmarschall',
  'Heinrich VI. von Obergreiz, Sohn Heinrichs I.; geb. 1649, sächsischer und kaiserlicher Feldmarschall, in der Schlacht bei Zenta 1697 tödlich verwundet; Vater Heinrichs I. und II.',
  'Heinrich VI. of Obergreiz, son of Heinrich I.; born 1649, Saxon and Imperial field marshal, mortally wounded at the battle of Zenta in 1697; father of Heinrich I. and II.')

P('Heinrich IV. von Untergreiz', 'Heinrich IV. (Herr von Untergreiz)', 'Landesherr',
  'Heinrich IV. von Untergreiz, Sohn Heinrichs V.; geb. 1638, † 1675; verheiratet mit Anna Dorothea von Ruppa; Vater Heinrichs XIII.',
  'Heinrich IV. of Untergreiz, son of Heinrich V.; born 1638, died 1675; married Anna Dorothea of Ruppa; father of Heinrich XIII.')

P('Heinrich V. von Untergreiz', 'Heinrich V. (Herr von Untergreiz)', 'Landesherr',
  'Heinrich V., Gründer des Hauses Untergreiz (1625); geb. 1602, erbte 1640 die Herrschaft Burgk, † 1667; verheiratet mit Anna Marie, Wild- und Rheingräfin von Neufville; Vater Heinrichs II., IV., V.',
  'Heinrich V., founder of the house of Untergreiz (1625); born 1602, inherited the lordship of Burgk in 1640, died 1667; married Anna Marie, Wild- and Rhinegravine of Neufville; father of Heinrich II., IV., V.')

P('Heinrich V. von Rothenthal', 'Heinrich V. (Herr von Rothenthal)', 'Landesherr',
  'Heinrich V. von Rothenthal, jüngster Sohn Heinrichs V. von Untergreiz; geb. 1645, † 1698 ohne Erben.',
  'Heinrich V. of Rothenthal, youngest son of Heinrich V. of Untergreiz; born 1645, died 1698 without heirs.')

P('Heinrich X. v. Lobenstein', 'Heinrich X. (Graf Reuß zu Lobenstein)', 'Landesherr',
  'Heinrich X., jüngster Sohn des Heinrich Posthumus, Gründer des Hauses Lobenstein; geb. 1621, † 1671; erkaufte 1664 die Herrschaft Hirschberg; verheiratet mit Marie Sibille Reuß-Obergreiz; Vater Heinrichs III., VIII. und X.',
  'Heinrich X., youngest son of Heinrich Posthumus, founder of the house of Lobenstein; born 1621, died 1671; bought the lordship of Hirschberg in 1664; married Marie Sibille Reuss-Obergreiz; father of Heinrich III., VIII. and X.',
  wd='Q97030')

P('Heinrich V. von Plauen', 'Heinrich V. von Plauen (Burggraf von Meißen)', 'Burggraf',
  'Burggraf Heinrich V. von Plauen (von Meißen), Graf von Hartenstein und Herr zu Plauen, oberster Kanzler von Böhmen; geb. 1508, † Mai 1554 vor der Plassenburg; erhielt nach der Reichsacht gegen Gera und Reuß 1547-1550 Gera, Schleiz, Lobenstein u. a. als böhmisches Lehen.',
  'Burgrave Heinrich V. of Plauen (of Meissen), count of Hartenstein and lord of Plauen, chief chancellor of Bohemia; born 1508, died May 1554 before the Plassenburg; after the outlawry of Gera and Reuss he received Gera, Schleiz, Lobenstein etc. as Bohemian fiefs in 1547-1550.',
  note='Brückner counts him as Heinrich V. and gives 1508 as year of birth (Tab. IV, p. 364); Wikidata and most literature count him as Heinrich IV. von Plauen and give 1510; death (May 1554) and offices agree. Heinrich V. in the Wikidata numbering is his son (1533-1568), who is Heinrich VI. in the numbering of Brückner.')
for k in ('Burggraf Heinrich V', 'Heinrich V. von Meißen'):
    M(k, 'Heinrich V. von Plauen', 'title variant')

P('Heinrich von Meißen', 'Heinrich II. von Plauen (Burggraf von Meißen)', 'Burggraf',
  'Burggraf Heinrich II. von Meißen, Herr zu Plauen (reg. 1429-1446); 1444 genannt bei der Belehnung der Brüder Reuß mit dem Weinberg Hainer am Gleißberg bei Jena.',
  'Burgrave Heinrich II. of Meissen, lord of Plauen (ruled 1429-1446); named in 1444 in the enfeoffment of the Reuss brothers with the Hainer vineyard below the Gleißberg near Jena.',
  note='Identified by date (1444, p. 369).')

P('Heinrich Herrn von Plauen', 'Heinrich I. von Plauen (Burggraf von Meißen)', 'Burggraf',
  'Heinrich I., Herr zu Plauen und Königswart, seit 1426 Burggraf von Meißen; 1389-1429; Reichs- und böhmischer Oberhofrichter; protestierte auf dem Konzil von Konstanz gegen die Verurteilung Hussens; verteidigte 1420 das Schloß zu Prag gegen die Hussiten; 1415 Vertrag mit dem Landgrafen von Leuchtenberg.',
  'Heinrich I., lord of Plauen and Königswart, burgrave of Meissen from 1426; 1389-1429; Imperial and Bohemian chief justice; protested at the Council of Constance against the condemnation of Hus; defended Prague castle against the Hussites in 1420; treaty with the landgrave of Leuchtenberg in 1415.',
  note='Identified by date and context (p. 368, treaty of 1415; cf. p. 357). Not the Teutonic Grand Master Heinrich von Plauen, his brother.')
