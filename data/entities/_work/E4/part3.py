# -*- coding: utf-8 -*-
"""Specific persons: Voigte of Weida, Plauen, Greiz and Gera, and the early Reuß (13th-16th century)."""
from part1 import P, M, R, AMB

# --- Weida ----------------------------------------------------------------------------------
P('Heinrich der Fromme', 'Heinrich der Fromme (von Weida)', 'Vogt (sagenhafter Stammvater)',
  'Heinrich von Weida, genannt der Fromme, nach den Chronisten Marschall Kaiser Heinrichs IV., Stammhaupt der Voigte von Weida und des Hauses Reuß; † c. 1100 (Tab. I); '
  'urkundlich nicht bezeugt, von Brückner aber als Persönlichkeit festgehalten (S. 323-324, 329).',
  'Heinrich of Weida, called the Pious, according to the chroniclers marshal of Emperor Heinrich IV., progenitor of the Voigte of Weida and of the house of Reuss; died c. 1100 (Tab. I); '
  'not attested in any charter, but retained by Brückner as a historical person (pp. 323-324, 329).')
M('Heinrich der Fromme von Weida', 'Heinrich der Fromme', 'variant with territory')
M('Heinrichs des Frommen', 'Heinrich der Fromme', 'genitive (his son of 1143, p. 329)')

P('Heinrich der Reiche', 'Heinrich der Reiche (von Weida)', 'Vogt',
  'Heinrich von Weida der Reiche, nach den Urkunden Sohn des 1143 beurkundeten Heinrich von Weida; 1188 bis † vor 1209; 1191 von Kaiser Heinrich VI. zum Ritter geschlagen; gründete 1193 das Prämonstratenserkloster Mildenfurt; '
  'verheiratet mit Berchta; Vater der drei ersten Voigte Heinrich d. ä., d. m. und d. j.; Urheber der Gleichnamigkeit des Hauses (S. 329, Tab. I).',
  'Heinrich of Weida the Rich, according to the charters son of the Heinrich of Weida attested in 1143; himself attested from 1188, died before 1209; knighted by Emperor Heinrich VI. in 1191; founded the Premonstratensian monastery of Mildenfurt in 1193; '
  'married to Berchta; father of the first three Voigte Heinrich d. ä., d. m. and d. j.; origin of the house\'s single name (p. 329, Tab. I).')
for k in ('Heinrich den Reichen', 'Heinrich dem Reichen', 'Heinrichs des Reichen', 'Heinrich von Weida der Reiche', 'Heinrich d. Reichen von Weida'):
    M(k, 'Heinrich der Reiche', 'inflection/word-order variant')

P('Heinrichs von Gottes Gnaden', 'Heinrich von Gottes Gnaden (Voigt von Weida)', 'Vogt',
  'Heinrich d. m., der sich seit 1224 d. ä. nannte, Voigt von Weida 1209-1249, urkundete „von Gottes Gnaden"; 1238 Deutschordensritter (Landmeister und Stellvertreter in Preußen); '
  'verheiratet 1) wohl mit einer Tochter von Colditz, 2) mit Jutta (stiftete Kloster Cronswitz); Vater der Voigte von Weida, Plauen und Gera.',
  'Heinrich d. m., who called himself d. ä. from 1224, Voigt of Weida 1209-1249, issued charters "by the grace of God"; Teutonic knight from 1238 (Landmeister and deputy in Prussia); '
  'married 1) probably a daughter of Colditz, 2) Jutta (founded Cronswitz convent); father of the Voigte of Weida, Plauen and Gera.',
  note='In Tab. I (p. 331) listed as "Heinrich d. m., von Gottes Gnaden"; corrigendum p. 833 on the style "von Gottes Gnaden".')

P('Heinrich von Elster-Weida', 'Heinrich von Weida (an der Elster), 1236-c. 1275', 'Vogt',
  'Heinrich, Voigt von Weida an der Elster, 1236-c. 1275, Gründer des Specialhauses Weida (Tab. II); 1270 Geber der Riethmühle an Kloster Volkenrode (nach A. Cohn); Sohn Heinrichs von Gottes Gnaden.',
  'Heinrich, Voigt of Weida on the Elster, 1236-c. 1275, founder of the special house of Weida (Tab. II); in 1270 donor of the Riethmühle to Volkenrode monastery (according to A. Cohn); son of Heinrich von Gottes Gnaden.',
  note='"Elster-Weida" is Cohn\'s term to distinguish the family from the Unstrut family of Weida; identified by date (1270, p. 325).')

P('Heinrich von Unstrut-Weida', 'Heinrich von Weida (an der Unstrut), 1143', 'Adliger',
  'Heinrich von Weida aus der Ritterfamilie von Weida an der Unstrut (Thüringen), 1143 im Gefolge Heinrichs des Löwen genannt; Gut bei Graba an Kloster Volkenrode; '
  'nach A. Cohn mit dem Weidaer Haus an der Elster verwandt, von Brückner (S. 324-328) bestritten.',
  'Heinrich of Weida of the knightly family of Weida on the Unstrut (Thuringia), named in 1143 in the retinue of Heinrich the Lion; estate near Graba given to Volkenrode monastery; '
  'according to A. Cohn related to the house of Weida on the Elster, which Brückner (pp. 324-328) disputes.')

P('Heinrich von Wida', 'Heinrich von Wida (Witha), 1170-1180', 'Adliger',
  'Heinrich von Wida (Witha), Vasall Heinrichs des Löwen aus der Unstruter Familie von Weida; 1170 im Gefolge des Herzogs, 1180 zum Kaiser übergetreten (Arnold von Lübeck); '
  'nach Cohn Stammvater der Voigte von Weida, nach Brückner nicht (S. 325-328).',
  'Heinrich of Wida (Witha), vassal of Heinrich the Lion from the Unstrut family of Weida; in the duke\'s retinue in 1170, went over to the emperor in 1180 (Arnold of Lübeck); '
  'according to Cohn ancestor of the Voigte of Weida, not so according to Brückner (pp. 325-328).')
M('Heinrich von Witha', 'Heinrich von Wida', 'spelling variant (quotation of Arnold of Lübeck, p. 328)')

P('Heinrich von Greiz', 'Heinrich von Greiz (Voigt, d. j. von Weida)', 'Vogt',
  'Heinrich d. j., jüngerer Bruder Heinrichs d. m. von Weida, 1209-nach 1240, von 1240 an Voigt von Greiz; starb kinderlos in den 1240er Jahren, sein Besitz kam an die Söhne Heinrichs d. m. (S. 330-332, 342).',
  'Heinrich d. j., younger brother of Heinrich d. m. of Weida, 1209-after 1240, Voigt of Greiz from 1240; died childless in the 1240s, his lands passed to the sons of Heinrich d. m. (pp. 330-332, 342).')

P('Heinrich d. ä. von Weida', 'Heinrich d. ä. von Weida (1295-c. 1364)', 'Vogt',
  'Heinrich d. ä., Voigt von Weida, 1295-c. 1364, seit 1323 Landvoigt zu Eger; verheiratet 1) mit einer Tochter von Plauen, 2) mit Katharina von Schönburg; Enkel des Gründers der Linie Weida; Vater u. a. Heinrichs des Ritter und Heinrichs des Rothen.',
  'Heinrich d. ä., Voigt of Weida, 1295-c. 1364, Landvoigt of Eger from 1323; married 1) a daughter of Plauen, 2) Katharina of Schönburg; grandson of the founder of the Weida line; father of Heinrich der Ritter and Heinrich der Rothe, among others.')

P('Heinrich der Graf', 'Heinrich der Graf (von Weida)', 'Vogt',
  'Heinrich von Weida, genannt der Graf, 1293-nach 1335; Vetter Heinrichs d. ä. und d. j. von Weida; verheiratet mit Hedwig (wohl von Lobdaburg-Arnshaugk); hinterließ einen Sohn, der 1332 der jüngste Voigt hieß (S. 335, 337, Tab. II).',
  'Heinrich of Weida, called the Count, 1293-after 1335; cousin of Heinrich d. ä. and d. j. of Weida; married Hedwig (probably of Lobdaburg-Arnshaugk); left a son, who was called the youngest Voigt in 1332 (pp. 335, 337, Tab. II).')

P('Heinrich der Ritter', 'Heinrich der Ritter (von Weida)', 'Vogt',
  'Heinrich der Ritter, Voigt von Weida, 1337-nach 1377; Sohn Heinrichs d. ä. aus zweiter Ehe; verkaufte 1366 seinen Anteil am Regnitzland an seinen Bruder Heinrich den Rothen, saß in Weida, ohne Leibeserben.',
  'Heinrich the Knight, Voigt of Weida, 1337-after 1377; son of Heinrich d. ä. by his second marriage; sold his share of the Regnitzland to his brother Heinrich the Red in 1366, lived at Weida, without heirs.')

P('Heinrich der Rothe', 'Heinrich der Rothe (von Weida)', 'Vogt',
  'Heinrich der Rothe, Voigt von Weida, 1377-c. 1388; Bruder Heinrichs des Ritter; 1367 mit dem ganzen Regnitzland belehnt, verkaufte es 1373 an den Burggrafen von Nürnberg; verheiratet mit Ilse von Gera.',
  'Heinrich the Red, Voigt of Weida, 1377-c. 1388; brother of Heinrich the Knight; enfeoffed with the whole Regnitzland in 1367, sold it in 1373 to the burgrave of Nuremberg; married Ilse of Gera.')
for k in ('Heinrich den Rothen', 'Heinrichs des Rothen'):
    M(k, 'Heinrich der Rothe', 'inflection variant')
M('Heinrich v. Rothe v. Weida', 'Heinrich der Rothe', 'Tab. III (p. 352): husband of Ilse von Gera (Tab. II: Heinrich der Rothe, ∞ Ilse von Gera)')

P('Heinrich von Weida zu Wildenfels', 'Heinrich von Weida zu Wildenfels († um 1535)', 'Herr',
  'Heinrich, Herr von Weida und Wildenfels, 1527 unter den Mitbelehnten der Herrschaft Greiz; † um 1535 als letzter männlicher Erbe des Hauses Weida; Vater der Margaretha, Erbin von Wildenfels (Tab. II).',
  'Heinrich, lord of Weida and Wildenfels, co-enfeoffed with the lordship of Greiz in 1527; died c. 1535 as last male heir of the house of Weida; father of Margaretha, heiress of Wildenfels (Tab. II).')

P('Heinrich von Wildenfels', 'Heinrich von Wildenfels (1315)', 'Adliger',
  'Heinrich von Wildenfels, 1315 unter den Helfern der Brüder von Gera in der Fehde gegen die Lobdaburger und den Landgrafen (S. 343).',
  'Heinrich of Wildenfels, in 1315 one of the allies of the brothers of Gera in the feud against the Lobdaburgs and the landgrave (p. 343).')

# --- Plauen and Reuß ------------------------------------------------------------------------
P('Heinrich der Ruthene', 'Heinrich der Ruthene (Ruzze, Reuß)', 'Vogt',
  'Heinrich der erste Ruthene (Ruzze, Reuß), Voigt von Plauen, mittlerer Sohn Heinrichs von Gottes Gnaden; 1244 bis † Ende 1303; Gründer der Linie Plauen; führt „von Gottes Vollmacht" und den Beinamen Reuß (urkundlich seit 1266); '
  'verheiratet mit Kunigunde von Eberstein; Vater Heinrichs des Böhmen und Heinrichs des Ruzze.',
  'Heinrich the first Ruthene (Ruzze, Reuss), Voigt of Plauen, middle son of Heinrich von Gottes Gnaden; attested from 1244, died end of 1303; founder of the Plauen line; styles himself "by the authority of God" and bears the epithet Reuss (in charters from 1266); '
  'married Kunigunde of Eberstein; father of Heinrich the Bohemian and Heinrich the Ruzze.')
for k, n in (('Heinrich der erste Ruthene', 'variant'), ('Heinrich der Ruthene (Ruzze, Reuß', 'table header (Tab. IV, p. 364); the key is truncated'),
             ('Heinrich von Plauen d. ä', 'p. 354 fn.: "Voigts Heinrich von Plauen d. ä.", husband of Kunigunde von Eberstein')):
    M(k, 'Heinrich der Ruthene', n)

P('Heinrich der Böhme', 'Heinrich der Böhme (Voigt von Plauen)', 'Vogt',
  'Heinrich der Böhme oder der Lange, älterer Sohn Heinrichs des Ruthenen; 1275-1302; verheiratet mit Katharina von Riesenburg; Vater der Voigte Heinrich d. ä. (der Lange) und Heinrich d. j. (Reuß); '
  'Wappen mit dem gekrönten Löwen.',
  'Heinrich the Bohemian or the Long, elder son of Heinrich the Ruthene; 1275-1302; married Katharina of Riesenburg; father of the Voigte Heinrich d. ä. (the Long) and Heinrich d. j. (Reuss); '
  'arms with the crowned lion.')

P('Heinrich der Ruzze', 'Heinrich der Ruzze (Reuß), 1276-1296', 'Vogt',
  'Heinrich Reuß oder Ruzze, jüngerer Sohn Heinrichs des Ruthenen; 1276 bis † vor 20. März 1296; Vater Heinrich Eriks, des Gründers des Hauses Reuß.',
  'Heinrich Reuss or Ruzze, younger son of Heinrich the Ruthene; attested from 1276, died before 20 March 1296; father of Heinrich Erik, the founder of the house of Reuss.')
M('Heinrichs Ruzze', 'Heinrich der Ruzze', 'genitive (p. 365: "der Erbsohn Heinrichs Ruzze")')

P('Heinrich Erik', 'Heinrich Erik (Reuß der Kleine)', 'Vogt',
  'Heinrich Reuß, genannt der Erik oder der Kleine, Voigt zu Greiz, Gründer des Hauses Reuß (jüngere Linie Plauen); 1290-1349; verheiratet 1) mit Salome, 2) mit Sophie; Landrichter im pleißener Land, 1324 Vormund des Landgrafen Friedrich des Ernsthaften; '
  'Urheber des ronneburger Bündnisses (1327); Vater Heinrichs des Strengen.',
  'Heinrich Reuss, called the Erik or the Little, Voigt at Greiz, founder of the house of Reuss (younger Plauen line); 1290-1349; married 1) Salome, 2) Sophie; Landrichter in the Pleißen territory, guardian of Landgrave Friedrich the Serious in 1324; '
  'originator of the Ronneburg alliance (1327); father of Heinrich the Strict.')
for k, n in (('Heinrich Reuß der Erik', 'variant'), ('Heinrich Reuß der Kleine', 'variant (epithet)'), ('Heinrichs des Kleinen', 'genitive (his son, p. 367)'),
             ('Heinrich Reuß von Plauen', 'p. 343: Voigt Heinrich Reuß von Plauen who stood with the landgrave in 1314/15 (cf. p. 365)')):
    M(k, 'Heinrich Erik', n)

P('Heinrich der Strenge', 'Heinrich der Strenge (Reuß von Greiz)', 'Vogt',
  'Heinrich Reuß der Strenge, Voigt von Greiz, Sohn Heinrich Eriks; 1327-1359; verheiratet mit Anna von Weida; im voigtländischen Krieg (1354) von den thüringer Landgrafen besiegt, verlor die Reichsfreiheit der Voigtei Greiz; Vater dreier Söhne (Heinrich d. ä., d. m., d. j.).',
  'Heinrich Reuss the Strict, Voigt of Greiz, son of Heinrich Erik; 1327-1359; married Anna of Weida; defeated by the Thuringian landgraves in the Voigtland war (1354), lost the imperial immediacy of the Greiz Voigtei; father of three sons (Heinrich d. ä., d. m., d. j.).')
for k in ('Heinrich Reuß den Strengen', 'Heinrich Reuß der Strenge'):
    M(k, 'Heinrich der Strenge', 'variant')

P('Heinrich dem Langen', 'Heinrich d. ä., der Lange (Voigt von Plauen, 1306-1373)', 'Vogt',
  'Heinrich d. ä., der Lange, Voigt (Herr) von Plauen, 1306-1373; verheiratet mit Sophie von Weida; unterstützte 1354 im voigtländischen Krieg Heinrich den Strengen von Greiz und verlor dabei Besitzungen; Vater Heinrichs d. ä. von Auerbach.',
  'Heinrich d. ä., the Long, Voigt (lord) of Plauen, 1306-1373; married Sophie of Weida; supported Heinrich the Strict of Greiz in the Voigtland war of 1354 and lost possessions; father of Heinrich d. ä. of Auerbach.',
  note='Identified from the context (p. 338: husband of Sophie von Weida; p. 367: 1354; cf. Tab. IV, p. 364). The bare epithet "der Lange" is ambiguous and listed separately.')
for k in ('Heinrichs des Langen', 'Heinrich des Langen'):
    M(k, 'Heinrich der Lange', 'genitive; denotes the Heinrich the Long of 1333 (Heinrich der Böhme, p. 354 fn.) and the father of Heinrich d. ä. of Auerbach (p. 356)')

P('Heinrich der Alte', 'Heinrich der Alte von Greiz (Reuß)', 'Vogt',
  'Heinrich d. j. Reuß, „der Alte von Greiz" (der „alte Russe"), 1413 bis nach 1449; Herr der halben Herrschaft Greiz, starb wohl unverheiratet und ohne Erben; sein Erbteil fiel an die Söhne seines Oheims Heinrichs d. j.',
  'Heinrich d. j. Reuss, "the Old One of Greiz" (the "old Reuss"), 1413 to after 1449; lord of half the lordship of Greiz, probably died unmarried and without heirs; his share passed to the sons of his uncle Heinrich d. j.')

P('Heinrich Reuß d. ä', 'Heinrich d. ä. Reuß zu Greiz (der Wallfahrer)', 'Herr',
  'Heinrich d. ä. Reuß, Herr zu Greiz und Oberkranichfeld, 1429-c. 1475, wegen einer Wallfahrt nach Palästina (1461) der Wallfahrer genannt; 1450 päpstliche Gunst (Beichtiger); verheiratet mit Magdalena von Schwarzenberg; Vater von sieben Söhnen und drei Töchtern.',
  'Heinrich d. ä. Reuss, lord of Greiz and Oberkranichfeld, 1429-c. 1475, called the Pilgrim after a pilgrimage to Palestine (1461); papal favor in 1450 (confessor); married Magdalena of Schwarzenberg; father of seven sons and three daughters.',
  note='Identified from the context (p. 369: papal letter of 3 April 1450 to "Heinrich Reuß d. ä."; p. 370).')

P('Heinrich der Friedsame', 'Heinrich der Friedsame (Reuß zu Greiz)', 'Landesherr',
  'Heinrich der Friedsame oder der Stille, Heinrich d. j. Reuß, Herr zu Greiz, seit 1529 auch zu Kranichfeld; 1476-1535; führte die Reformation ein; Vater der drei Brüder Heinrich d. ä., d. m., d. j., Ahnherr der Linien Reuß.',
  'Heinrich the Peaceable or the Quiet, Heinrich d. j. Reuss, lord of Greiz, also of Kranichfeld from 1529; 1476-1535; introduced the Reformation; father of the three brothers Heinrich d. ä., d. m., d. j., ancestor of the Reuss lines.')
for k, n in (('Heinrich den Friedsamen', 'inflection variant'), ('Heinrichs des Friedsamen', 'genitive')):
    M(k, 'Heinrich der Friedsame', n)

P('Heinrich Reuß von Untergreiz', 'Heinrich d. ä. Reuß (Herr zu Untergreiz, der Botschafter)', 'Landesherr',
  'Heinrich d. ä. Reuß, ältester Sohn Heinrichs des Friedsamen, Herr zu Untergreiz, genannt Botschafter (Gesandtschaften für den Kurfürsten von Sachsen); geb. 1506, † 1572; Stifter der älteren Linie Reuß; '
  'verheiratet 1) mit Agnes von Beichlingen, 2) mit Barbara von Metsch; 1547 mit seinen Brüdern geächtet.',
  'Heinrich d. ä. Reuss, eldest son of Heinrich the Peaceable, lord of Untergreiz, called the Ambassador (embassies for the elector of Saxony); born 1506, died 1572; founder of the elder line of Reuss; '
  'married 1) Agnes of Beichlingen, 2) Barbara of Metsch; outlawed with his brothers in 1547.')
M('Heinrich dem älteren', 'Heinrich Reuß von Untergreiz', 'p. 264: the three brothers Reuß-Plauen, coat of arms of 1561 (d. ä., d. m., d. j.)')

P('Heinrich der Mittlere', 'Heinrich d. m. Reuß (Herr zu Obergreiz)', 'Landesherr',
  'Heinrich d. m. Reuß, Herr zu Obergreiz, Stifter der mittleren Linie Reuß von Plauen; geb. 1525, † 1578; verheiratet mit Marie Salome von Oettingen; anfänglich eifrig lutherisch, flacianisch beeinflußt; herzoglich sächsischer Landeshauptmann von Weida.',
  'Heinrich d. m. Reuss, lord of Obergreiz, founder of the middle Reuss line of Plauen; born 1525, died 1578; married Marie Salome of Oettingen; at first zealously Lutheran, influenced by the Flacians; ducal Saxon captain of Weida.')
for k, n in (('Heinrich Reuß d. m', 'p. 375: letter of April 1565 to Duke Johann Friedrich the Younger of Gotha'),
             ('Heinrich dem mittleren', 'p. 264: the three brothers Reuß-Plauen, coat of arms of 1561 (d. ä., d. m., d. j.)')):
    M(k, 'Heinrich der Mittlere', n)

P('Heinrich dem jüngeren', 'Heinrich d. j. Reuß (Herr von Gera, 1530-1572)', 'Landesherr',
  'Heinrich d. j. Reuß, Herr von Gera, jüngster Sohn Heinrichs des Friedsamen, Gründer der jüngeren Linie Reuß (Reuß j. L.); geb. 1530, † 1572; verheiratet 1) mit Elisabeth von Schwarzburg-Leutenberg, 2) mit Dorothea von Solms-Sonnenwalde; Vater Heinrich Posthumus.',
  'Heinrich d. j. Reuss, lord of Gera, youngest son of Heinrich the Peaceable, founder of the younger line of Reuss (Reuss j. L.); born 1530, died 1572; married 1) Elisabeth of Schwarzburg-Leutenberg, 2) Dorothea of Solms-Sonnenwalde; father of Heinrich Posthumus.',
  note='Brückner names him "Heinrich von Gera" in Tab. VI (p. 394); the mention here is the coat of arms of 1561 (p. 264).')

P('Heinrich Rothbart', 'Heinrich Rothbart (Heinrich d. m. Reuß zu Schleiz)', 'Landesherr',
  'Heinrich d. m., genannt Rothbart, Herr zu Schleiz, jüngerer der beiden letzten Regenten der mittleren Linie (Obergreiz); geb. 1563, † 1616 erblos; verheiratet mit Agnes Marie von Erbach.',
  'Heinrich d. m., called Redbeard, lord of Schleiz, the younger of the last two rulers of the middle line (Obergreiz); born 1563, died 1616 without heirs; married Agnes Marie of Erbach.')

# --- Gera ------------------------------------------------------------------------------------
P('Heinrich d. Mehrer', 'Heinrich der Mehrer (d. ä., Voigt von Gera)', 'Vogt',
  'Heinrich d. ä., der Mehrer seines Landes, Voigt von Gera, jüngster Sohn Heinrichs von Gottes Gnaden und Gründer der Linie Gera; 1244 bis † vor Ende August 1279; verheiratet mit Luckard von Lobdaburg-Arnshaugk, durch die er Pausa, Lobenstein, Saalburg, Burgk und Schleiz gewann; '
  '1254 Teilnehmer des grimmaischen Vertrags.',
  'Heinrich d. ä., the Augmenter of his land, Voigt of Gera, youngest son of Heinrich von Gottes Gnaden and founder of the Gera line; attested from 1244, died before the end of August 1279; married Luckard of Lobdaburg-Arnshaugk, through whom he gained Pausa, Lobenstein, Saalburg, Burgk and Schleiz; '
  'party to the treaty of Grimma in 1254.')
for k, n in (('Heinrich des Mehrers', 'genitive'), ('Heinrich der Ältere', 'Tab. III header (p. 352): "Heinrich der Ältere, Voigt von Gera, 1244 - † vor Ende August 1279"'),
             ('Heinrich von Gera und Lobenstein', 'p. 774: Voigt who gave Swinshut to Langheim in 1278 (from Lobenstein, p. 342)')):
    M(k, 'Heinrich d. Mehrer', n)

P('Heinrich der Große', 'Heinrich der Große (d. ä., Voigt von Gera)', 'Vogt',
  'Heinrich d. ä., genannt der Große (von Kaiser Ludwig der Feste genannt), Voigt von Gera, Sitz Gera; 1307 bis c. 1345; verheiratet mit Sophie von Lobdaburg-Bergau; ohne Leibeserben; 1316 Reichslandrichter im pleißener Land.',
  'Heinrich d. ä., called the Great (called the Firm by Emperor Ludwig), Voigt of Gera, seat at Gera; 1307 to c. 1345; married Sophie of Lobdaburg-Bergau; without heirs; imperial Landrichter in the Pleißen territory in 1316.')
for k, n in (('Heinrich d. Große', 'abbreviated variant (p. 414)'), ('Heinrich den Großen', 'inflection variant (p. 576)'),
             ('Heinrich den Festen', 'epithet used by Emperor Ludwig (p. 343 fn.); p. 670 with his brother "den Freisinnigen"')):
    M(k, 'Heinrich der Große', n)

P('Heinrich der Worthalter', 'Heinrich der Worthalter (d. j., Voigt von Gera)', 'Vogt',
  'Heinrich d. j., der Worthalter (Minister der thüringer Landgrafen 1366; Tab. III: der Wohlbedachte), Voigt von Gera, Sitz Reichenfels; 1310 bis † 8. Dez. 1376; verheiratet mit Mechtild von Käfernburg; '
  'verpfändete in Geldnot Lobenstein, Burgk u. a. und trug seine Herrschaften zu Lehen auf; Vater Heinrichs des Dispensirten.',
  'Heinrich d. j., the Worthalter (minister of the Thuringian landgraves in 1366; Tab. III: the Prudent), Voigt of Gera, seat at Reichenfels; attested from 1310, died 8 Dec. 1376; married Mechtild of Käfernburg; '
  'pledged Lobenstein, Burgk etc. in financial need and made his lordships fiefs of others; father of Heinrich the Dispensed.')
for k, n in (('Heinrich d. Worthalter', 'abbreviated variant'), ('Heinrich dem Worthalter', 'inflection variant')):
    M(k, 'Heinrich der Worthalter', n)
for k in ('Heinrich den Freigesinnten', 'Heinrich der Freigesinnte', 'Heinrich den Freisinnigen'):
    M(k, 'Heinrich der Worthalter',
      'epithet "der Freigesinnte/Freisinnige", younger brother of Heinrich der Große (pp. 576, 670, 710: grandsons of Luckard; pledge of Lobenstein 1369); identified from the context')

P('Heinrich der Dispensirte', 'Heinrich der Dispensirte (Herr von Gera)', 'Vogt',
  'Heinrich der Dispensirte, Herr von Gera, Sohn Heinrichs des Worthalters; 1351 bis † Ende 1419/Anfang 1420; erhielt den Beinamen durch die Dispensation des Erzbischofs von Mainz für seine nahe verwandte zweite Frau Lutrada von Hohnstein; '
  'erste Frau Elisabeth von Schwarzburg; „Pfaffenbrief" 1405; Vater Heinrichs d. ä., d. m. (Beerber) und d. j.',
  'Heinrich the Dispensed, lord of Gera, son of Heinrich the Worthalter; attested from 1351, died end of 1419/early 1420; received the epithet through the dispensation of the archbishop of Mainz for his closely related second wife Lutrada of Hohnstein; '
  'first wife Elisabeth of Schwarzburg; "Pfaffenbrief" of 1405; father of Heinrich d. ä., d. m. (the Beerber) and d. j.')
for k in ('Heinrich den Dispensirten', 'Heinrich d. Dispensirte', 'Heinrich d. Dispenstirte'):
    M(k, 'Heinrich der Dispensirte', 'inflection/abbreviation/OCR variant')

P('Heinrich der Beerber', 'Heinrich der Beerber (d. m., Herr von Lobenstein)', 'Vogt',
  'Heinrich d. m. von Gera, genannt der Beerber, Herr von Lobenstein; geb. 1406, † c. 1481; 1426 Lobenstein mit Saalburg, Nordhalben und den hofer Lehen; nannte sich seit 1439 „der ältere"; nach dem Tod seines Bruders des Unglücklichen vereinigte er das geraer Land; '
  'verheiratet mit Mechtild von Schwarzburg-Wachsenburg; Vater von drei weltlichen Söhnen.',
  'Heinrich d. m. of Gera, called the Beerber, lord of Lobenstein; born 1406, died c. 1481; received Lobenstein with Saalburg, Nordhalben and the Hof fiefs in 1426; called himself "the elder" from 1439; after the death of his brother the Unfortunate he reunited the Gera lands; '
  'married Mechtild of Schwarzburg-Wachsenburg; father of three lay sons.',
  note='p. 630 credits "Heinrich den Beerber" with raising Zeulenroda to a town in 1438, which p. 347 attributes to his elder brother Heinrich d. ä.; the other mentions fit Heinrich d. m.')
for k, n in (('Heinrich den Beerber', 'inflection variant'),
             ('Heinrich b. m', 'OCR error for "d. m." (Tab. III, p. 352: "Heinrich b. m., geb. 1406, † c. 1481, Herr von Lobenstein 1426")'),
             ('Heinrich von Gera-Lobenstein', 'p. 348: the elder brother, Herr von Gera und Lobenstein, in the Bruderkrieg')):
    M(k, 'Heinrich der Beerber', n)

P('Heinrich der Unglückliche', 'Heinrich der Unglückliche (d. j., Herr von Gera und Schleiz)', 'Vogt',
  'Heinrich d. j. von Gera, Herr zu Gera und Schleiz, genannt der Unglückliche; geb. 1415, † zwischen 1452 und 1456; 1450 nach der Zerstörung Geras durch Herzog Wilhelm von Sachsen gefangen nach Böhmen geführt, 1451 freigelassen; '
  'verheiratet 1439 mit Anna von Henneberg-Römhild.',
  'Heinrich d. j. of Gera, lord of Gera and Schleiz, called the Unfortunate; born 1415, died between 1452 and 1456; taken prisoner to Bohemia in 1450 after Duke Wilhelm of Saxony destroyed Gera, released in 1451; '
  'married in 1439 Anna of Henneberg-Römhild.')
for k, n in (('Heinrichs des Unglücklichen', 'genitive'), ('Heinrich d. Unglückliche', 'abbreviated variant (p. 414)'),
             ('Heinrich von Gera und Schleiz', 'p. 348: captured in 1450'), ('Heinrich von Gera-Schleiz', 'p. 348: in the peace of 1451')):
    M(k, 'Heinrich der Unglückliche', n)

P('Heinrich der ä', 'Heinrich d. ä. (Herr zu Burgk, Linie Gera, 1404-1439)', 'Vogt',
  'Heinrich d. ä., ältester Sohn Heinrichs des Dispensirten aus zweiter Ehe; geb. 1404, 1426 Burgk mit Schleiz, Reichenfels, Langenberg und Tinz; erhob 1438 Zeulenroda zur Stadt; † Ende 1438/Anfang 1439 ohne Erben; verheiratet mit Wilburg von Schwarzburg-Leutenberg.',
  'Heinrich d. ä., eldest son of Heinrich the Dispensed by his second marriage; born 1404, received Burgk with Schleiz, Reichenfels, Langenberg and Tinz in 1426; raised Zeulenroda to a town in 1438; died end of 1438/early 1439 without heirs; married Wilburg of Schwarzburg-Leutenberg.',
  note='Identified from the context (p. 576: the three sons of 1425; his death c. 1439). The bare form "Heinrich d. ä." is ambiguous and listed separately.')
for k, n in (('Heinrichs des ä', 'genitive (p. 576: "nach dem Tode Heinrichs des ä." c. 1439)'),
             ('Heinrich b. ä', 'OCR error for "d. ä." (Tab. III, p. 352: "Heinrich b. ä., geb. 1404, † vor April 1439, Herr v. Burgk 1426")')):
    M(k, 'Heinrich der ä', n)

P('Heinrich d. m. von Schleiz', 'Heinrich d. m. (Herr zu Gera und Schleiz, 1478-1500)', 'Landesherr',
  'Heinrich d. m. von Gera, Herr zu Schleiz, 1478 bis † 1500; Gesamterbe der geraer Lande nach dem Tod seiner Brüder (1488, 1498); erhob 1494 Tanna zur Stadt; Geheimrat Kaiser Friedrichs III.; verheiratet mit Hedwig von Mansfeld-Heldrungen; Vater Heinrichs d. ä. (1502-1538) und Heinrichs d. j. (der Beharrliche).',
  'Heinrich d. m. of Gera, lord of Schleiz, attested from 1478, died 1500; sole heir of the Gera lands after the death of his brothers (1488, 1498); raised Tanna to a town in 1494; privy councillor of Emperor Friedrich III.; married Hedwig of Mansfeld-Heldrungen; father of Heinrich d. ä. (1502-1538) and Heinrich d. j. (the Persistent).',
  note='Identified from the context (p. 688 and p. 350: Tanna 1494). The bare form "Heinrich d. m." is ambiguous and listed separately.')

P('Heinrich den Beherrlichen', 'Heinrich d. j., der Beharrliche (Herr von Gera, † 1550)', 'Landesherr',
  'Heinrich d. j. von Gera, „der Beharrliche"; 1502 bis † 7. Aug. 1550 zu Burgk; geächtet nach der Schlacht bei Mühlberg (1547), verzichtete auf Gera; ohne Erben mit ihm erlosch das alte Haus Gera; verheiratet 1) mit Ludmilla von Lobkowitz und Hassenstein, 2) mit Margaretha von Schwarzburg-Leutenberg.',
  'Heinrich d. j. of Gera, "the Persistent"; attested from 1502, died 7 Aug. 1550 at Burgk; outlawed after the battle of Mühlberg (1547), renounced Gera; the old house of Gera became extinct with him, without heirs; married 1) Ludmilla of Lobkowitz and Hassenstein, 2) Margaretha of Schwarzburg-Leutenberg.',
  note='Brückner\'s p. 630 has "Beherrlichen" (also in the transcription); pp. 351/352 give "der Beharrliche"; the last ruler of Gera of 1550.')

P('Heinrich der Ritterhafte', 'Heinrich der Ritterhafte', 'Adliger',
  'Heinrich der Ritterhafte, 1315 und 1328 Stifter an Kloster Cronswitz (Güter zu Waltersdorf, die seiner Schwester Gertrude gehörten); Vorfahr Heinrichs, Herrn von Gera (1486).',
  'Heinrich the Chivalrous, donor to Cronswitz convent in 1315 and 1328 (goods at Waltersdorf that belonged to his sister Gertrude); ancestor of Heinrich, lord of Gera (1486).',
  note='Identity not established by Brückner (p. 466); possibly a member of the house of Gera (a sister Gertrud is given in Tab. III) - unverified.')
