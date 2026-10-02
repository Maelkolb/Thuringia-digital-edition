"""Analysis: Medizinalwesen und Seuchen - Zeitleiste 1570-1866 (pp. 170, 171, 177)."""
from _common import *

LANES = {
    "arzt": bi("Ärzte vor Ort", "Physicians in place"),
    "pocken": bi("Blattern und Impfung", "Smallpox and vaccination"),
    "epi": bi("Weitere Epidemien", "Other epidemics"),
}
# (year, lane, place, event_de, event_en, value, unit_de, unit_en, page, phrase)
E = [
    (1570, "arzt", "Gera", "Erster Stadtarzt (um 1570)", "First town physician (about 1570)", None, None, None, "177", "kommt in Gera um 1570"),
    (1600, "arzt", "Schleiz", "Erster Stadtarzt (um 1600)", "First town physician (about 1600)", None, None, None, "177", "in Schleiz um 1600"),
    (1620, "arzt", "Lobenstein", "Erster Stadtarzt (um 1620)", "First town physician (about 1620)", None, None, None, "177", "in Lobenstein um 1620"),
    (1760, "arzt", "Hohenleuben", "Der erste Arzt sucht einen dauernden Sitz (um 1760)", "The first physician tries to settle permanently (about 1760)", None, None, None, "177", "In Hohenleuben suchte um 1760"),
    (1756, "pocken", "Gera", "208 Kinder sterben an den Blattern", "208 children die of smallpox", 208, "Kinder gestorben", "children died", "170", "1756 zu Gera 208 Kinder"),
    (1788, "pocken", "Ebersdorf", "150 Kinder liegen an den Blattern erkrankt", "150 children lie ill with smallpox", 150, "Kinder erkrankt", "children ill", "170", "1788 in dem Orte Ebersdorf"),
    (1790, "pocken", "Friesau und Remptendorf (Reuß ä. L.)", "Pfarrer Frotscher von Drognitz impft (Inoculation)", "Pastor Frotscher of Drognitz inoculates", None, None, None, "170", "1790 M. Frotscher"),
    (1791, "pocken", "Lobenstein-Ebersdorf", "Über 50 % der Gestorbenen sind Blatternopfer", "Over 50 % of the dead are smallpox victims", 50, "% der Gestorbenen", "% of the dead", "170", "1791 in dem Landestheile"),
    (1807, "pocken", "Fürstenthum", "75 Kinder erliegen den Blattern", "75 children succumb to smallpox", 75, "Kinder gestorben", "children died", "170", "1807 im Lande 75 Kinder"),
    (1820, "pocken", "Fürstenthum", "Die Impfung bricht sich mehr und mehr Bahn", "Vaccination increasingly gains ground", None, None, None, "170", "erst vom Jahre 1820"),
    (1826, "pocken", "Fürstenthum", "Mandat vom 31. Mai erhebt die Impfung zum allgemeinen Gesetz", "Decree of 31 May makes vaccination a general law", None, None, None, "170", "Mandat vom 31. Mai 1826"),
    (1844, "epi", "Schilbach", "Scharlachepidemie mit pestilentialischem Charakter, auch 50- bis 70-Jährige erkranken", "Scarlet fever epidemic of pestilential character, even 50- to 70-year-olds fall ill", None, None, None, "170", "1844 in Schilbach"),
    (1845, "epi", "Tanna", "Masern und Scharlach zugleich in und um Tanna", "Measles and scarlet fever together in and around Tanna", None, None, None, "170", "so 1845 in und um Tanna"),
    (1866, "epi", "Hirschberg und Untermhaus", "Cholera, einmalig durch Einschleppung", "Cholera, once only, brought in from outside", None, None, None, "171", "1866 durch Einschleppung"),
]


def locate(page_label, phrase):
    p = page(page_label)
    hits = []
    for b in p["blocks"] + p["footnotes"]:
        if phrase.replace("  ", " ") in text(page_label, b["id"]).replace("\n", " "):
            hits.append(b["id"])
    assert len(hits) >= 1, (page_label, phrase)
    return hits[0]


rows = []
for (yr, lane, place, ed, ee, val, ud, ue, pg, ph) in E:
    blk = locate(pg, ph)
    assert str(yr) in text(pg, blk), (yr, pg, blk)
    rows.append([yr, LANES[lane]["de"], LANES[lane]["en"], place, ed, ee, val, ud, ue, pg, blk])
rows.sort(key=lambda r: (r[0]))
print(len(rows))
ph = {r[3]: r[0] for r in rows if r[1] == LANES["arzt"]["de"]}
print(ph)
gap_gera_hoh = ph["Hohenleuben"] - ph["Gera"]
sp = [r for r in rows if r[1] == LANES["pocken"]["de"]]
span_pocken = (sp[-1][0] - sp[0][0])
first_death = next(r for r in rows if r[0] == 1756)
to_law = 1826 - 1756
print(gap_gera_hoh, span_pocken, to_law)
src = sorted({(r[9], r[10]) for r in rows}, key=lambda x: (int(x[0]), int(x[1][1:]) if x[1].startswith("b") else 100 + int(x[1][2:])))
src_refs = [{"page": p, "block": b} for p, b in src]
t177 = text("177", "b1")
assert "32 Aerzte und 10 Apotheken" in t177

ana = {
    "id": "gesundheit-medizinalwesen-und-seuchen-zeitleiste",
    "title": bi("Ärzte, Blatternimpfung und Epidemien: Zeitleiste 1570–1866", "Physicians, smallpox vaccination and epidemics: timeline 1570–1866"),
    "category": "health",
    "section": "t1-2-6",
    "sources": src_refs,
    "summary": bi(
        "Brückner nennt im Abschnitt »Volkskrankheit und Volksmedicin« eine Reihe datierter Ereignisse: das Auftreten der ersten Stadtärzte (Gera um 1570, Schleiz um 1600, Lobenstein um 1620, Hohenleuben um 1760), die Blatternepidemien des 18. Jahrhunderts mit der allmählichen Einführung der Impfung bis zum Mandat von 1826 und einzelne Epidemien von Masern, Scharlach und Cholera. Die Zeitleiste ordnet diese Angaben nach drei Themen.",
        "In the section “Volkskrankheit und Volksmedicin” Brückner names a series of dated events: the appearance of the first town physicians (Gera about 1570, Schleiz about 1600, Lobenstein about 1620, Hohenleuben about 1760), the smallpox epidemics of the 18th century with the gradual introduction of vaccination up to the decree of 1826, and individual epidemics of measles, scarlet fever and cholera. The timeline arranges these statements under three themes.",
    ),
    "method": bi(
        "Die Jahresangaben und Zahlen wurden aus dem Text S. 170, 171 und 177 und der Fußnote S. 170 zusammengestellt; jede Angabe ist über Seite und Block belegt (Zuordnung per Skript an Schlüsselwörtern geprüft). Aufgenommen sind nur Ereignisse mit Jahreszahl; die Gesamtzahlen für die Gegenwart (32 Ärzte und 10 Apotheken, vor 100 Jahren kaum ein Drittel) stehen ohne Jahr und sind nur im Text genannt. Die Zuordnung zu drei Themenzeilen ist redaktionell.",
        "The years and numbers were assembled from the text on pp. 170, 171 and 177 and the footnote on p. 170; each statement is documented by page and block (assignment checked by script against key phrases). Only events with a year are included; the present-day totals (32 physicians and 10 pharmacies, barely a third 100 years ago) have no year and appear only in the text. The assignment to three theme rows is editorial.",
    ),
    "findings": [
        bi(
            f"Die ersten Stadtärzte erscheinen in Gera um 1570, Schleiz um 1600 und Lobenstein um 1620; Hohenleuben folgt erst um 1760, also {gap_gera_hoh} Jahre nach Gera. Zur Zeit der Niederschrift zählt das Fürstenthum 32 Ärzte und 10 Apotheken, vor 100 Jahren kaum ein Drittel.",
            f"The first town physicians appear in Gera about 1570, Schleiz about 1600 and Lobenstein about 1620; Hohenleuben follows only about 1760, {gap_gera_hoh} years after Gera. At the time of writing the principality counts 32 physicians and 10 pharmacies, barely a third a hundred years earlier.",
        ),
        bi(
            f"Die belegten Blatternfälle reichen von 1756 (Gera: 208 gestorbene Kinder) über 1788 (Ebersdorf: 150 erkrankte Kinder), 1791 (Lobenstein-Ebersdorf: über 50 % der Gestorbenen) bis 1807 (75 gestorbene Kinder). Die Impfung setzt sich nach Brückner erst seit 1820 durch und wird 1826, {to_law} Jahre nach den 208 Todesfällen in Gera, durch Mandat allgemeines Gesetz.",
            f"The recorded smallpox cases run from 1756 (Gera: 208 children dead) through 1788 (Ebersdorf: 150 children ill) and 1791 (Lobenstein-Ebersdorf: over 50 % of the dead) to 1807 (75 children dead). According to Brückner vaccination gained ground only from 1820 and became general law by decree in 1826, {to_law} years after the 208 deaths at Gera.",
        ),
        bi(
            "Die Epidemien von 1844 (Scharlach in Schilbach), 1845 (Masern und Scharlach in Tanna) und 1866 (Cholera in Hirschberg und Untermhaus) sind örtlich begrenzt; die Cholera trat nach Brückner nur dieses eine Mal im Fürstenthum auf.",
            "The epidemics of 1844 (scarlet fever at Schilbach), 1845 (measles and scarlet fever at Tanna) and 1866 (cholera at Hirschberg and Untermhaus) were local; according to Brückner cholera occurred in the principality only this once.",
        ),
    ],
    "caveats": [
        bi(
            "Es handelt sich um Beispiele, die Brückner zur Illustration anführt, nicht um eine vollständige Chronik der Epidemien. Die Angaben haben verschiedene Maße (gestorbene Kinder, erkrankte Kinder, Anteil an allen Todesfällen) und sind nicht untereinander vergleichbar. Die Impfung von 1790 fand außerhalb des Fürstenthums (Reuß ä. L.) statt.",
            "These are examples that Brückner cites by way of illustration, not a complete chronicle of epidemics. The statements use different measures (children dead, children ill, share of all deaths) and are not comparable with one another. The vaccination of 1790 took place outside the principality (Reuss elder line).",
        ),
        bi(
            "Die Jahre »um 1570«, »um 1600«, »um 1620« und »um 1760« sind ungefähre Angaben Brückners.",
            "The years “about 1570”, “about 1600”, “about 1620” and “about 1760” are approximate statements by Brückner.",
        ),
    ],
    "datasets": [
        {
            "name": "events",
            "title": bi("Datierte Ereignisse des Gesundheitswesens", "Dated events of the health system"),
            "columns": [
                {"name": "year", "label": bi("Jahr", "Year"), "type": "integer", "unit": None},
                {"name": "lane_de", "label": bi("Thema (de)", "Theme (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "lane_en", "label": bi("Thema (en)", "Theme (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "event_de", "label": bi("Ereignis (de)", "Event (de)"), "type": "string", "unit": None},
                {"name": "event_en", "label": bi("Ereignis (en)", "Event (en)"), "type": "string", "unit": None},
                {"name": "value", "label": bi("Zahl", "Number"), "type": "integer", "unit": None},
                {"name": "value_unit_de", "label": bi("Einheit (de)", "Unit (de)"), "type": "string", "unit": None},
                {"name": "value_unit_en", "label": bi("Einheit (en)", "Unit (en)"), "type": "string", "unit": None},
                {"name": "page", "label": bi("Seite", "Page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Block", "Block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": src_refs,
        }
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "events",
            "title": bi("Zeitleiste von Ärzten, Blatternimpfung und Epidemien", "Timeline of physicians, smallpox vaccination and epidemics"),
            "caption": bi(
                "Jeder Punkt ist ein von Brückner datiertes Ereignis; die Zeilen trennen die Themen. Die Blatternzeile verdichtet sich im späten 18. Jahrhundert und endet mit dem Impfgesetz von 1826. Weitere Angaben stehen im Tooltip.",
                "Each dot is an event dated by Brückner; the rows separate the themes. The smallpox row becomes denser in the late 18th century and ends with the vaccination decree of 1826. Further details are in the tooltip.",
            ),
            "vegalite": {
                "height": 240,
                "mark": {"type": "point", "filled": True, "size": 110},
                "encoding": {
                    "y": {"field": {"de": "lane_de", "en": "lane_en"}, "type": "nominal", "sort": [LANES[k]["de"] for k in LANES], "title": None, "axis": {"labelLimit": 400}},
                    "x": {"field": "year", "type": "quantitative", "title": None, "scale": {"domain": [1550, 1880]}, "axis": {"format": "d", "values": [1550, 1600, 1650, 1700, 1750, 1800, 1850]}},
                    "color": {"field": {"de": "lane_de", "en": "lane_en"}, "type": "nominal", "legend": None, "scale": {"domain": [LANES[k] for k in LANES]}},
                    "tooltip": [
                        {"field": "year", "title": bi("Jahr", "Year")},
                        {"field": "place", "title": bi("Ort", "Place")},
                        {"field": {"de": "event_de", "en": "event_en"}, "title": bi("Ereignis", "Event")},
                        {"field": "page", "title": bi("Seite", "Page")},
                    ],
                },
            },
        }
    ],
    "transcription_issues": [],
    "keywords": {
        "de": ["Ärzte", "Apotheken", "Blattern", "Pocken", "Impfung", "Epidemien", "Scharlach", "Masern", "Cholera", "Medizinalwesen"],
        "en": ["physicians", "pharmacies", "smallpox", "vaccination", "epidemics", "scarlet fever", "measles", "cholera", "medical system"],
    },
    "related": ["gesundheit-krankheitsstatistik-lobenstein-gera-hohenleuben", "bevoelkerung-sterblichkeit-1858-1867"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
