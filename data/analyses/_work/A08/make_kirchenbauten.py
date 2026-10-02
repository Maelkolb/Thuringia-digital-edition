"""Analysis: Neubauten von Kirchen 1611-1782 (pp. 133-134, 'Das Gotteshaus')."""
import re
from _common import *

t133 = text("133", "b1")
t134 = text("134", "b1")

entries = []  # place_label, place, church, year_start, year_end, kind


def add(place, year0, year1=None, church=None):
    label = f"{place} ({church})" if church else place
    entries.append([label, place, church or "", year0, year1 or year0])


# --- 17th century (end of p. 133 + beginning of p. 134)
m = re.search(r"die (\d{4}) bis (\d{4}) aufgeführte,.*?Trinitatiskirche zu Gera eröffnet, an die sich (\d{4}) (\w+), (\d{4})—(\d{4}) (\w+),$", t133)
assert m, "17th century part 1"
add("Gera", int(m.group(1)), int(m.group(2)), "Trinitatiskirche")
add(m.group(4), int(m.group(3)))
add(m.group(7), int(m.group(5)), int(m.group(6)))
m = re.match(r"(\d{4}) (\w+), (\d{4}) (\w+) und (\d{4}) (\w+) mit der (St\. Georgenkirche) anschließt", t134)
assert m, "17th century part 2"
add(m.group(2), int(m.group(1)))
add(m.group(4), int(m.group(3)))
add(m.group(6), int(m.group(5)), None, "St. Georgenkirche")

# --- 18th century list
m = re.search(r"Kirchen des 18\. Jahrhunderts (.*?)\. Zugleich", t134)
assert m
seq = re.split(r", | und ", m.group(1))
pending = []
for piece in seq:
    mm = re.match(r"^(.*?) (\d{4})$", piece)
    if not mm:
        pending.append(piece)
        continue
    names, year = pending + [mm.group(1)], int(mm.group(2))
    pending = []
    for n in names:
        if " mit der " in n:
            place, church = n.split(" mit der ")
            add(place, year, None, church)
        else:
            add(n, year)
assert not pending

# --- 19th century example
m = re.search(r"die (\d{4}) erbaute Kirche zu (\w+)", t133)
assert m
add(m.group(2), int(m.group(1)))

entries.sort(key=lambda r: (r[3], r[1]))
for e in entries:
    e.append("17. Jh." if e[3] < 1700 else ("18. Jh." if e[3] < 1800 else "19. Jh."))
    e.append("17th c." if e[3] < 1700 else ("18th c." if e[3] < 1800 else "19th c."))
print(len(entries))
for e in entries:
    print(e)
c17 = [e for e in entries if e[3] < 1700]
c18 = [e for e in entries if 1700 <= e[3] < 1800]
c19 = [e for e in entries if e[3] >= 1800]
print(len(c17), len(c18), len(c19))
assert len(c17) == 6 and len(c18) == 23 and len(c19) == 1

# decade counts
from collections import Counter
dec = Counter((e[3] // 10) * 10 for e in entries)
print(sorted(dec.items()))
peak = sum(dec[d] for d in (1710, 1720, 1730))
share_peak = round(100 * peak / len(c18), 0)
print("1710-1739:", peak, "of", len(c18), share_peak)
years = sorted(e[3] for e in entries)
gaps = [(b - a, a, b) for a, b in zip(years, years[1:])]
gaps.sort(reverse=True)
y18 = sorted(e[3] for e in c18)
gap18 = max((y - x, x, y) for x, y in zip(y18, y18[1:]))
assert gap18[1:] == (1733, 1753)
print(gaps[:5])
# older parts
assert "Baujahr 1101" in t133 and "Jahre 1193 erbaut" in t133 and "Zeit von 1450" in t133
older = [
    ["Schleiz, Bergkirche", "Schlussstein der Sakristei nennt das Baujahr", "Schleiz, Bergkirche (Sakristei)", 1101],
    ["Untermhaus", "Kapelle, nach der Überlieferung erbaut (nach Brückner erst Anfang des 13. Jh.)", "Untermhaus (Kapelle)", 1193],
    ["Untermhaus", "Bau des Schiffs", "Untermhaus (Schiff)", 1450],
]
en_old = {
    1101: "keystone of the sacristy bears the year of construction",
    1193: "chapel, said to have been built (according to Brückner only in the early 13th century)",
    1450: "construction of the nave",
}

rows_new = [[e[0], e[1], e[2], e[3], e[4], e[5], e[6]] for e in entries]

ana = {
    "id": "wohnen-kirchenneubauten-1611-1842",
    "title": bi("Kirchenneubauten 1611–1842", "New church buildings, 1611–1842"),
    "category": "housing",
    "section": "t1-2-2",
    "sources": [
        {"page": "133", "block": "b1"},
        {"page": "134", "block": "b1"},
        {"page": "131", "block": "b3"},
    ],
    "summary": bi(
        f"Im Abschnitt »Das Gotteshaus« zählt Brückner die Kirchen auf, die in der Neuzeit neu errichtet wurden: sechs im 17. und {len(c18)} im 18. Jahrhundert, dazu als jüngstes Beispiel Hirschberg 1842 (zusammen {len(entries)} Bauten). Die Grafiken stellen die Bauten nach Jahrzehnten und als Zeitleiste dar: Der Schwerpunkt liegt in den Jahrzehnten 1710–1739, kein erhaltener Bau reicht vollständig vor 1200 zurück.",
        f"In the section “Das Gotteshaus” Brückner lists the churches newly built in the modern period: six in the 17th and {len(c18)} in the 18th century, plus Hirschberg in 1842 as the most recent example ({len(entries)} buildings in all). The charts show the buildings by decade and as a timeline: the emphasis lies on the decades 1710–1739, and no surviving building dates entirely from before 1200.",
    ),
    "method": bi(
        "Die Orts- und Jahresangaben wurden aus dem Fließtext S. 133 f. maschinell ausgelesen (Jahr 1611–1613 für Gera, 1640–1642 für Tanna als Spannen; bei den Spannen zählt das Anfangsjahr), Paare wie »Mielesdorf und Künsdorf 1719« als zwei Bauten mit gleichem Jahr. Die Jahreszahlen wurden am Faksimile (S. 133 unten, S. 134 oben) kontrolliert. Das 19. Jahrhundert ist nur durch das von Brückner genannte Beispiel Hirschberg (1842) vertreten. Die älteren Bauteile (Sakristei der Bergkirche 1101, Kapelle Untermhaus 1193, Schiff Untermhaus 1450) stehen in einer eigenen Tabelle.",
        "Place and year data were read out of the running text on pp. 133 f. by script (1611–1613 for Gera and 1640–1642 for Tanna are spans; the starting year counts); pairs such as “Mielesdorf und Künsdorf 1719” count as two buildings with the same year. The years were checked against the facsimile (p. 133 bottom, p. 134 top). The 19th century is represented only by Brückner’s example Hirschberg (1842). The older building parts (sacristy of the Bergkirche 1101, chapel at Untermhaus 1193, nave at Untermhaus 1450) are given in a separate table.",
    ),
    "findings": [
        bi(
            f"Brückner führt {len(c17)} Neubauten des 17. Jahrhunderts (1611–1694) und {len(c18)} des 18. Jahrhunderts (1702–1782) an; die Mehrzahl der noch bestehenden Kirchen stammt, wie er schreibt, aus dem 18. Jahrhundert.",
            f"Brückner names {len(c17)} new buildings of the 17th century (1611–1694) and {len(c18)} of the 18th century (1702–1782); the majority of the churches still standing date, as he writes, from the 18th century.",
        ),
        bi(
            f"{peak} der {len(c18)} Bauten des 18. Jahrhunderts ({dz(share_peak, 0)} %) entstanden in den drei Jahrzehnten 1710–1739; allein 1710–1719 sind es {dec[1710]} (Löhma, Dittersdorf, Triebes, Köstritz, Mielesdorf, Künsdorf).",
            f"{peak} of the {len(c18)} buildings of the 18th century ({ez(share_peak, 0)} %) were put up in the three decades 1710–1739; 1710–1719 alone accounts for {dec[1710]} (Löhma, Dittersdorf, Triebes, Köstritz, Mielesdorf, Künsdorf).",
        ),
        bi(
            f"Innerhalb des 18. Jahrhunderts liegt die größte Lücke zwischen 1733 (Lobenstein) und 1753 (Kirschkau): {gap18[0]} Jahre ohne genannten Neubau; die Reihe endet 1782 mit der Salvatorkirche in Gera. Im 17. Jahrhundert verteilen sich sechs Bauten auf {c17[-1][3] - c17[0][3]} Jahre (1611–1694).",
            f"Within the 18th century the longest gap lies between 1733 (Lobenstein) and 1753 (Kirschkau): {gap18[0]} years without a named new building; the series ends in 1782 with the Salvatorkirche at Gera. In the 17th century six buildings are spread over {c17[-1][3] - c17[0][3]} years (1611–1694).",
        ),
        bi(
            "Die Städte sind früh vertreten (Gera 1611–1613, Tanna 1640–1642, Saalburg 1642, Schleiz 1694); ab 1702 überwiegen Dörfer. Älter als diese Neubauten sind nur Teile: die Sakristei der Schleizer Bergkirche (Baujahr 1101), die Kapelle von Untermhaus (1193) und deren Schiff (1450). Kein vollständig erhaltener Kirchenbau reicht über 1200 zurück.",
            "The towns appear early (Gera 1611–1613, Tanna 1640–1642, Saalburg 1642, Schleiz 1694); from 1702 villages predominate. Older than these new buildings are only parts: the sacristy of the Bergkirche at Schleiz (year of construction 1101), the chapel at Untermhaus (1193) and its nave (1450). No completely preserved church building dates from before 1200.",
        ),
    ],
    "caveats": [
        bi(
            "Die Liste gibt, was Brückner als »neue Kirchen« hervorhebt; sie ist keine vollständige Zählung aller Kirchenbauten des Landes, und Umbauten, Erweiterungen und Reparaturen (im 18. Jahrhundert »viele ältere Kirchen«) sind nicht erfasst.",
            "The list gives what Brückner highlights as “new churches”; it is not a complete count of all church buildings in the country, and rebuilding, extensions and repairs (in the 18th century “many older churches”) are not covered.",
        ),
        bi(
            "Die Datierung der älteren Bauteile ist bei Brückner unsicher (Kapelle Untermhaus »soll« 1193 erbaut sein, entstand »offenbar aber erst im Anfange des 13. Jahrhunderts«). Mehrere Orte nennt er zugleich als Träger romanischer oder gotischer Reste ohne Jahr; diese fehlen in der Zeitleiste.",
            "The dating of the older building parts is uncertain in Brückner (the chapel at Untermhaus “is said to” have been built in 1193, “evidently only at the beginning of the 13th century”). He also names several places as having Romanesque or Gothic remains without a year; these are missing from the timeline.",
        ),
    ],
    "datasets": [
        {
            "name": "new_churches",
            "title": bi("Neu errichtete Kirchen nach Brückner", "Newly built churches according to Brückner"),
            "columns": [
                {"name": "place_label", "label": bi("Ort (Kirche)", "Place (church)"), "type": "string", "unit": None},
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "church", "label": bi("Kirche", "Church"), "type": "string", "unit": None},
                {"name": "year_start", "label": bi("Baubeginn bzw. Baujahr", "Start / year of construction"), "type": "integer", "unit": None},
                {"name": "year_end", "label": bi("Bauende (bei Spannen)", "End (for spans)"), "type": "integer", "unit": None},
                {"name": "century_de", "label": bi("Jahrhundert (de)", "Century (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "century_en", "label": bi("Jahrhundert (en)", "Century (en)"), "type": "string", "unit": None, "derived": True},
            ],
            "rows": rows_new,
            "source_refs": [{"page": "133", "block": "b1"}, {"page": "134", "block": "b1"}],
        },
        {
            "name": "older_parts",
            "title": bi("Ältere Bauteile (Beispiele Brückners)", "Older building parts (Brückner’s examples)"),
            "columns": [
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "note_de", "label": bi("Bauteil (de)", "Building part (de)"), "type": "string", "unit": None},
                {"name": "note_en", "label": bi("Bauteil (en)", "Building part (en)"), "type": "string", "unit": None},
                {"name": "year", "label": bi("Jahr", "Year"), "type": "integer", "unit": None},
            ],
            "rows": [[o[0], o[1], en_old[o[3]], o[3]] for o in older],
            "source_refs": [{"page": "133", "block": "b1"}],
        },
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "new_churches",
            "title": bi("Kirchenneubauten je Jahrzehnt", "New church buildings per decade"),
            "caption": bi(
                "Zahl der von Brückner genannten Neubauten je Jahrzehnt (bei Spannen das Anfangsjahr). Die Hauptmasse entsteht 1710–1739; 1842 (Hirschberg) steht für die neueste Zeit.",
                "Number of the new buildings named by Brückner per decade (for spans the starting year). The bulk is built in 1710–1739; 1842 (Hirschberg) stands for the most recent period.",
            ),
            "vegalite": {
                "height": 240,
                "mark": "bar",
                "encoding": {
                    "x": {"field": "year_start", "bin": {"step": 10}, "type": "quantitative", "title": bi("Jahrzehnt", "Decade"), "axis": {"format": "d", "values": [1600, 1650, 1700, 1750, 1800, 1850]}, "scale": {"domain": [1600, 1850]}},
                    "y": {"aggregate": "count", "type": "quantitative", "title": bi("Neubauten", "New buildings"), "axis": {"tickMinStep": 1}},
                    "tooltip": [
                        {"field": "year_start", "bin": {"step": 10}, "title": bi("Jahrzehnt", "Decade")},
                        {"aggregate": "count", "title": bi("Neubauten", "New buildings")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "new_churches",
            "title": bi("Zeitleiste der Neubauten 1611–1782", "Timeline of new buildings, 1611–1782"),
            "caption": bi(
                "Jeder Punkt ist eine von Brückner genannte Kirche, geordnet nach dem Baujahr (bei Gera, Trinitatiskirche, und Tanna Baubeginn: 1611–1613 bzw. 1640–1642). Je steiler die Reihe, desto dichter die Bautätigkeit; die Farben trennen das 17. vom 18. Jahrhundert.",
                "Each dot is a church named by Brückner, ordered by year of construction (for Gera, Trinitatiskirche, and Tanna the start: 1611–1613 and 1640–1642). The steeper the series, the denser the building activity; colours separate the 17th from the 18th century.",
            ),
            "vegalite": {
                "height": 420,
                "transform": [{"filter": "datum.year_start < 1800"}],
                "encoding": {
                    "y": {"field": "place_label", "type": "nominal", "sort": {"field": "year_start", "op": "min"}, "title": None, "axis": {"labelLimit": 400, "labelFontSize": 10}},
                },
                "layer": [
                    {
                        "mark": {"type": "point", "filled": True, "size": 50},
                        "encoding": {
                            "x": {"field": "year_start", "type": "quantitative", "title": None, "scale": {"domain": [1600, 1800]}, "axis": {"format": "d"}},
                            "color": {"field": {"de": "century_de", "en": "century_en"}, "type": "nominal", "title": None, "scale": {"domain": [bi("17. Jh.", "17th c."), bi("18. Jh.", "18th c.")]}},
                            "tooltip": [
                                {"field": "place_label", "title": bi("Kirche", "Church")},
                                {"field": "year_start", "title": bi("Baujahr / Baubeginn", "Year / start")},
                                {"field": "year_end", "title": bi("Bauende", "End")},
                            ],
                        },
                    },
                ],
            },
        },
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Kirchen", "Kirchenbau", "Gotteshaus", "Barock", "18. Jahrhundert", "Trinitatiskirche Gera", "Bergkirche Schleiz", "Baugeschichte"],
        "en": ["churches", "church building", "baroque", "18th century", "Trinitatiskirche Gera", "Bergkirche Schleiz", "architectural history"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
