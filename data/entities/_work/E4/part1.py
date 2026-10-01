# -*- coding: utf-8 -*-
"""Build data/entities/decisions/E4.json (persons named Heinrich).

Conventions
 - AMB: accept as ambiguous name form (label as printed, note 'ambiguous; refers to different persons ...')
 - P:   accept as one identified person (label, kind, description_de/en, optional wikidata)
 - M:   merge (spelling/inflection variant, or title/territory variant of the same person/form)
 - R:   reject (transcription artefact)
"""
import json, sys
from pathlib import Path

ROOT = Path(r'C:\Users\totom\Projects\reuss-edition')
KEYS = json.load(open(ROOT / 'data/entities/slices.json', encoding='utf-8'))['E4']['keys']
KS = set(KEYS)
D = {}
WD = json.load(open(ROOT / 'data/entities/_work/E4/wd_verified.json', encoding='utf-8')) if (ROOT / 'data/entities/_work/E4/wd_verified.json').exists() else {}


def _put(d):
    k = d['key']
    assert k in KS, 'unknown key ' + repr(k)
    assert k not in D, 'duplicate ' + repr(k)
    D[k] = d


GENERIC = ('ambiguous; refers to different persons. ')


def AMB(key, label, note='', kind='Landesherr (mehrdeutig)'):
    d = {'key': key, 'action': 'accept', 'label': label, 'class': 'person', 'kind': kind,
         'note': GENERIC + note.strip()}
    d['note'] = d['note'].strip()
    _put(d)


def P(key, label, kind, de, en, wd=None, note=None):
    d = {'key': key, 'action': 'accept', 'label': label, 'class': 'person', 'kind': kind,
         'description_de': de, 'description_en': en}
    q = wd if wd else WD.get(key)
    if q:
        d['wikidata'] = q
    if note:
        d['note'] = note
    _put(d)


def M(key, into, note=None):
    d = {'key': key, 'action': 'merge', 'into': into}
    if note:
        d['note'] = note
    _put(d)


def R(key, reason):
    _put({'key': key, 'action': 'reject', 'reason': reason})


# ---------------------------------------------------------------------------
# 1. ambiguous name forms (bare epithets, bare numerals, territorial forms)
# ---------------------------------------------------------------------------
NUM = ('The numeral is counted afresh in every century and separately for the elder and younger line of Reuss '
       '(Brückner p. 376), so the same form denotes different princes; see the genealogical tables pp. 341-402. ')

AMB('Heinrich', 'Heinrich',
    'Members of the houses of Weida, Gera, Plauen and Reuß (Voigte, Herren, Grafen, Fürsten) as well as '
    'kings/emperors (Heinrich I., Heinrich IV., Heinrich VI.), Landgraf Heinrich of Thuringia and clergy; '
    'also the table cells of the genealogies (pp. 325-364) that give only the first name.')
AMB('Heinrich d. ä', 'Heinrich d. ä.',
    'Several Voigte of Weida, Gera, Plauen and Greiz and later Herren/Grafen Reuß who were called "der Ältere" '
    '(13th-16th c.), e.g. Heinrich d. ä. von Weida (1276-c. 1316; 1295-c. 1364), von Gera (1307-c. 1345; 1404-1439; '
    '1502-1538), Reuß zu Greiz (1429-c. 1475), Reuß zu Untergreiz (1506-1572).')
AMB('Heinrich d. j', 'Heinrich d. j.',
    'Several Voigte of Weida, Gera, Plauen and Greiz and later Herren Reuß who were called "der Jüngere" '
    '(13th-16th c.), e.g. Heinrich d. j. von Weida, von Gera (the Worthalter, the Unglückliche, the Beharrliche), '
    'Reuß von Greiz/Ronneburg, Reuß zu Gera (1530-1572).')
AMB('Heinrich d. m', 'Heinrich d. m.',
    'Several Voigte of Weida, Gera and Greiz and Herren Reuß called "der Mittlere" (13th-17th c.), e.g. Heinrich d. m. '
    'von Weida (1209-1249), von Gera (the Beerber, 1406-c. 1481; the Fintende, 1478-1500), Reuß zu Obergreiz '
    '(1525-1578), Reuß zu Schleiz (Rothbart, 1563-1616).')
AMB('Heinrich I', 'Heinrich I.',
    NUM + 'Includes King/Emperor Heinrich I. (the Fowler), Burggraf Heinrich I. von Plauen (1389-1429), Heinrich I. '
    'von Schleiz (1639-1692; 1695-1744), Heinrich I. von Obergreiz (1627-1681; 1693-1714) and a prince born 1803 '
    '(printed "I.", transcribed "L." on p. 399).')
AMB('Heinrich II', 'Heinrich II.',
    NUM + 'Includes Burggraf Heinrich II. von Plauen (1429-1446), Heinrich II. von Gera (1602-1670), Heinrich II. von Burgk '
    '(two persons), Heinrich II. von Köstritz (1803-1852), Heinrich II. von Lobenstein (d. 1782) and Heinrich II. von Obergreiz (1696-1722).')
AMB('Heinrich III', 'Heinrich III.',
    NUM + 'Includes Burggraf Heinrich III. von Plauen (1446-1482), Heinrich III. von Schleiz (1603-1640), Heinrich III. '
    'von Lobenstein (1648-1710), Heinrich III. von Untergreiz (1701-1768) and Heinrich III. von Burgk (d. 1640).')
AMB('Heinrich IV', 'Heinrich IV.',
    NUM + 'Includes Burggraf Heinrich IV. von Plauen (1482-1520), Heinrich IV. von Gera (1650-1686), Heinrich IV. von Obergreiz '
    '(1597-1629), Heinrich IV. von Untergreiz (1638-1675), Prince Heinrich IV. (b. 1821, Köstritz).')
AMB('Heinrich V', 'Heinrich V.',
    NUM + 'Mostly Burggraf Heinrich V. von Plauen (1508-1554; see the separate entry "Heinrich V. von Plauen"), but also '
    'Heinrich V. Reuß zu Greiz (1549-1604), Heinrich V. von Untergreiz (1602-1667), Heinrich V. von Rothenthal (1645-1698) and others.')
AMB('Heinrich VI', 'Heinrich VI.',
    NUM + 'Includes Emperor Heinrich VI. (Staufer), Burggraf Heinrich VI. von Plauen (1533-1568), Heinrich VI. von Köstritz '
    '(1707-1783), Heinrich VI. von Obergreiz (1649-1697) and others.')
AMB('Heinrich VII', 'Heinrich VII.',
    NUM + 'Mostly Burggraf Heinrich VII. von Plauen (1536-1572), but also Prince Heinrich VII. Reuß (b. 1825, Prussian envoy; '
    'see the separate entry "Heinrich Reuß VII") and others.')
AMB('Heinrich VIII', 'Heinrich VIII.',
    NUM + 'Includes Heinrich VIII. Herr von Hirschberg (1652-1711) and several short-lived princes in the tables.')
AMB('Heinrich IX', 'Heinrich IX.',
    NUM + 'Includes Heinrich IX. von Schleiz (1616-1666), Heinrich IX. von Köstritz (1711-1780, Prussian minister of state) '
    'and Prince Heinrich IX. (b. 1827).')
AMB('Heinrich X', 'Heinrich X.',
    NUM + 'Includes Heinrich X. von Lobenstein (1621-1671; see the separate entry "Heinrich X. v. Lobenstein"), Heinrich X. '
    'von Ebersdorf (1662-1711) and Prince Heinrich X. (1827-1847, Köstritz).')
AMB('Heinrich XI', 'Heinrich XI.',
    NUM + 'Includes Heinrich XI. von Schleiz (1669-1726; see "Heinrich Reuß XI"), Heinrich XI. von Obergreiz/Greiz (1722-1800, '
    'first prince of Greiz) and others.')
AMB('Heinrich XII', 'Heinrich XII.',
    NUM + 'Mostly Graf Heinrich XII. von Schleiz (1716-1784; see "Graf Heinrich XII"), but also Prince Heinrich XII. (1829-1866) '
    'and short-lived princes in the tables.')
AMB('Heinrich XIII', 'Heinrich XIII.',
    NUM + 'Includes Heinrich XIII. von Obergreiz (1672-1733), Heinrich XIII. von Greiz (1747-1817), Prince Heinrich XIII. (b. 1830) and others.')
AMB('Heinrich XIV', 'Heinrich XIV.',
    NUM + 'Nine of the eleven mentions denote the reigning prince Heinrich XIV. Reuß j. L. (b. 1832; see the separate entry '
    '"Fürst Heinrich XIV"); the others are table cells for Heinrich XIV. of Greiz (1749-1799, p. 401) and a child of Obergreiz (1674-1682, p. 402).')
AMB('Heinrich XV', 'Heinrich XV.',
    NUM + 'Includes Heinrich XV. von Lobenstein (1674-1739), Heinrich XV. von Obergreiz (1676-1690), Heinrich XV. von Greiz '
    '(1751-1825, Imperial general), Prince Heinrich XV. (b. 1834).')
AMB('Heinrich XVI', 'Heinrich XVI.',
    NUM + 'Includes Heinrich XVI. von Obergreiz (1678-1698) and Heinrich XVI. of Greiz (1759-1763).')
AMB('Heinrich XVII', 'Heinrich XVII.',
    NUM + 'Includes Heinrich XVII. von Lobenstein (1676-1706), Heinrich XVII. von Greiz (1761-1807, Prussian colonel) and Prince Heinrich XVII. (b. 1839).')
AMB('Heinrich XVIII', 'Heinrich XVIII.',
    NUM + 'Mostly Heinrich XVIII. von Gera, called Fundator (1677-1735; see "Graf Heinrich XVIII"), but also Prince Heinrich XVIII. (b. 1847) '
    'and an infant of Greiz (1787).')
AMB('Heinrich XIX', 'Heinrich XIX.',
    NUM + 'Heinrich XIX. von Greiz (1790-1836) and Prince Heinrich XIX. (b. 1848).')
AMB('Heinrich XX', 'Heinrich XX.',
    NUM + 'Heinrich XX. von Greiz (1794-1859, prince) and Prince Heinrich XX. (b. 1852).')
AMB('Heinrich XXI', 'Heinrich XXI.',
    NUM + 'Heinrich XXI. von Lobenstein-Selbitz (1721-1807) and a prince born 1853.')
AMB('Heinrich XXII', 'Heinrich XXII.',
    NUM + 'Includes Graf Heinrich XXII. von Gera (1680-1731), the reigning prince Heinrich XXII. Reuß ä. L. (b. 1846) and a prince born 1854.')
AMB('Heinrich XXIII', 'Heinrich XXIII.',
    NUM + 'Includes Heinrich XXIII. von Lobenstein (1680-1723), Heinrich XXIII. von Köstritz (1722-1787), a prince of Greiz (1844) and a prince born 1855.')
AMB('Heinrich XXIV', 'Heinrich XXIV.',
    NUM + 'Heinrich XXIV. von Köstritz (1681-1748), Heinrich XXIV. von Ebersdorf (1724-1779) and a prince born 1855 (Köstritz).')
AMB('Heinrich XXV', 'Heinrich XXV.',
    NUM + 'Heinrich XXV. von Gera (d. 1748), Heinrich XXV. von Lobenstein-Selbitz (1724-1801) and others.')
AMB('Heinrich XXVI', 'Heinrich XXVI.',
    NUM + 'Heinrich XXVI. von Lobenstein-Selbitz (1681-1730), Heinrich XXVI. von Ebersdorf (1725-1796, historian of the house; '
    'most mentions) and a prince born 1857.')
AMB('Heinrich XXVIII', 'Heinrich XXVIII.',
    NUM + 'Heinrich XXVIII. von Ebersdorf (1726-1797, Herrnhut) and a prince born 1859.')
AMB('Heinrich XXIX', 'Heinrich XXIX.',
    NUM + 'Mostly Heinrich XXIX. von Ebersdorf (1699-1747), but also a prince born 1860 (Köstritz).')
AMB('Heinrich XXX', 'Heinrich XXX.',
    NUM + 'Twelve of the thirteen mentions denote Graf Heinrich XXX. von Gera (1727-1802; see "Graf Heinrich XXX"); one table cell '
    '(p. 399) is a prince born 1862 (Köstritz).')

# name forms with territorial / epithet qualification that stay ambiguous
AMB('Heinrich von Gera', 'Heinrich von Gera',
    'Voigte and Herren of Gera of different generations (13th-16th c.), e.g. Heinrich der Mehrer, der Große, der Worthalter, der Dispensirte; '
    'also the table header of Heinrich von Gera (1530-1572, founder of the younger line, p. 394), burgmen and the Cologne canon Heinrich von Gera (1451).',
    'Voigt/Herr von Gera (mehrdeutig)')
AMB('Heinrich von Weida', 'Heinrich von Weida',
    'Voigte of Weida of different generations: the progenitor (1143), Heinrich der Reiche, Heinrich von Weida (1236-1275), '
    'Heinrich d. ä. (1295-c. 1364) and others (p. 323-340).',
    'Voigt von Weida (mehrdeutig)')
AMB('Heinrich von Plauen', 'Heinrich von Plauen',
    'Voigte/Burggrafen von Plauen of different generations: Heinrich der Ruthene, der Böhme, der Lange, the Burggrafen Heinrich I.-VII. '
    'and the Teutonic Grand Master Heinrich von Plauen (d. 1429).',
    'Voigt von Plauen (mehrdeutig)')
AMB('Heinrich Reuß', 'Heinrich Reuß',
    'Voigte/Herren Reuß of Plauen, Greiz, Ronneburg and Obergreiz of different generations (mostly Heinrich Reuß der Erik, 1290-1349, '
    'but also Heinrich Reuß zu Ronneburg, zu Greiz 1496, d. m. zu Gesell/Burgk 1616).',
    'Voigt/Herr Reuß (mehrdeutig)')
AMB('Heinrich d. ä. von Gera', 'Heinrich d. ä. von Gera',
    'Heinrich d. ä. von Gera of different generations: the Voigt of 1316 (der Große), the Herr of 1486 (1482-1488) and the Herr of 1501 (1502-1538).',
    'Voigt/Herr von Gera (mehrdeutig)')
AMB('Heinrich der ältere', 'Heinrich der ältere',
    'Heinrich d. ä. Reuß zu Untergreiz (1506-1572, called Botschafter) and Heinrich d. ä. Herr von Gera (1502-1538, mentioned 1505).',
    'Herr (mehrdeutig)')
AMB('Heinrich Reuß d. j', 'Heinrich Reuß d. j.',
    'Heinrich d. j. Reuß von Greiz/Ronneburg (1384-1429, war against King Wenzel 1399) and Heinrich d. j. Reuß zu Greiz/Kranichfeld (1429-1462).',
    'Herr Reuß (mehrdeutig)')
AMB('Heinrich Reuss d. j', 'Heinrich Reuss d. j.',
    'Heinrich d. j. Reuß (Voigt, 1323) and Landesherr of 1614 and 1627 (several rulers of the elder and younger line).',
    'Voigt/Landesherr Reuß (mehrdeutig)')
AMB('Heinrich der Lange', 'Heinrich der Lange',
    'Voigte of Plauen of the older line with the epithet "der Lange" (the Böhme, c. 1275-1302; d. ä. 1306-1373; d. j. 1306-1352; also the '
    'son of 1333) and a knight Heinrich der Lange at Langgrün (1345).',
    'Voigt von Plauen (mehrdeutig)')

# ---------------------------------------------------------------------------
# 2. merges of variants into ambiguous base forms
# ---------------------------------------------------------------------------
M('Heinrichs', 'Heinrich', 'genitive; refers to different persons, as the base form')
M('Heinrichs d. m', 'Heinrich d. m', 'genitive; refers to different persons, as the base form')
M('Heinrichs d. ä', 'Heinrich d. ä', 'genitive; refers to different persons, as the base form')
M('Heinrichs d. j', 'Heinrich d. j', 'genitive; refers to different persons, as the base form')
M('Heinrich der m', 'Heinrich d. m', 'abbreviation variant')
M('Heinrich der mittlere', 'Heinrich d. m', 'epithet written out; context (Gera, Zwickau) does not identify the person beyond "d. m. of Gera"')
M('Heinrichs II', 'Heinrich II', 'genitive; refers to different persons, as the base form')
M('Heinrichs I', 'Heinrich I', 'genitive; denotes King Heinrich I. (p. 667) as well as Heinrich I. von Schleiz (p. 634)')
M('Heinrichs IX', 'Heinrich IX', 'genitive; denotes Heinrich IX. von Schleiz (1616-1666) and Heinrich IX. von Köstritz (1711-1780, p. 496)')
M('Heinrichs X', 'Heinrich X', 'genitive; denotes Heinrich X. von Lobenstein (p. 577) and probably Heinrich X. (p. 716)')
M('Heinrichs XXIV', 'Heinrich XXIV', 'genitive; denotes Heinrich XXIV. von Köstritz (pp. 496, 631) and von Ebersdorf (p. 737)')
M('Heinrich L', 'Heinrich I',
  'transcription error: the table cell on p. 399 (Tab. XI, "Heinrich I., geb. 1803, + 1805", youngest son of Heinrich XLIV. von Köstritz) is printed "I.", '
  'the transcription reads "L."')
M('Heinrich Reuss', 'Heinrich Reuß', 'spelling variant; the two mentions denote different Voigte Reuß (pp. 336, 354)')
M('Heinrich Reuß von Greiz', 'Heinrich Reuß', 'denotes Heinrich der Strenge (1355, p. 356) and Heinrich d. ä. (1496, p. 350)')
M('Heinrich Reuss von Plauen', 'Heinrich Reuß', 'p. 555: Graf Heinrich Reuß (1384, Ronneburg), not identified further')
M('Heinrich Reuß v. Plauen', 'Heinrich Reuß', 'p. 341: husband of Anna von Weida; not identified further')
M('Heinrichs von Plauen', 'Heinrich von Plauen', 'p. 337: Schwager of the Weida brothers (1319); not identified further')
M('Heinrich v. Plauen', 'Heinrich von Plauen', 'p. 335 fn.: Voigt of Plauen in 1276 (Ruthene or his son); abbreviated form')
M('Heinrich Herr von Plauen', 'Heinrich von Plauen', 'p. 795: "Herr von Plauen", 1295')
M('Heinrich v. Weida', 'Heinrich von Weida', 'abbreviation variant')
M('Heinrichs von Gera', 'Heinrich von Gera', 'genitive')
M('Heinrich v. Gera', 'Heinrich von Gera', 'abbreviation variant')
M('Heinrich zu Gera', 'Heinrich von Gera', 'variant: Dynast/Reichsvoigt of Gera')
M('Heinrich, Herr von Gera', 'Heinrich von Gera', 'variant with title; refers to different Herren von Gera (1460, 1486)')
M('Heinrich Herr von Gera', 'Heinrich von Gera', 'variant with title; refers to different Herren von Gera (1374, 1513)')
M('Heinrich, Herrn von Gera', 'Heinrich von Gera', 'variant with title (p. 694)')
M('Heinrich Herrn zu Gera', 'Heinrich von Gera', 'variant with title; p. 416 fn.: the builder of the north wing of the Osterstein (1468-1470), same person as the text on p. 416')
M('Heinrich der ältere von Gera', 'Heinrich d. ä. von Gera', 'variant; denotes Heinrich d. ä. of 1425 (p. 732) and of 1502 (p. 509)')
