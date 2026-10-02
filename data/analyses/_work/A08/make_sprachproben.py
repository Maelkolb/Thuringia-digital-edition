"""Analysis: Sprachproben der Mundart (pp. 145-151): places, districts, text kinds, length."""
import glob
import json
from collections import Counter, defaultdict
from _common import *

# Landestheil of each place from the gazetteer packages G1-G6 (Brückner Part II); fallback: none
LT = {}
for f in sorted(glob.glob(str(ROOT / "data" / "gazetteer" / "G*.json"))):
    d = json.loads(open(f, encoding="utf-8").read())
    for e in d["entries"]:
        LT.setdefault(e["name"], (e.get("landestheil"), e["start"]["page"]))

TYPES = {
    "gleichnis": bi("Gleichnis (Bibeltext)", "Parable (Gospel text)"),
    "gespraech": bi("Gespräch", "Conversation"),
    "erzaehlung": bi("Erzählung oder Fabel", "Story or fable"),
    "gedicht": bi("Gedicht", "Poem"),
}
UL, OL = "Unterland", "Oberland"
# (order, place, label_de, label_en, region, gazetteer name(s), type, title_de, title_en, [(page, block)...], contributor)
S = [
    (1, "Gera", "Umgegend von Gera", "Environs of Gera", UL, ["Gera"], "gespraech", "Zwei Jungen sprechen über die Schulstunde; Eduard gibt das Gleichnis vom Sämann wieder", "Two boys talk about the lesson; Eduard retells the parable of the sower", [("145", f"b{i}") for i in range(4, 14)], ""),
    (2, "Waltersdorf", "Waltersdorf (Gera)", "Waltersdorf (Gera)", UL, ["Waltersdorf"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("145", "b15")], "Giebner"),
    (2, "Waltersdorf", "Waltersdorf (Gera)", "Waltersdorf (Gera)", UL, ["Waltersdorf"], "erzaehlung", "Fabel vom zahmen Wolf", "Fable of the tame wolf", [("145", "b16"), ("146", "b1")], "Giebner"),
    (2, "Waltersdorf", "Waltersdorf (Gera)", "Waltersdorf (Gera)", UL, ["Waltersdorf"], "erzaehlung", "Erzählung vom heimgekehrten Sohn", "Story of the returned son", [("146", "b2")], "Giebner"),
    (3, "Kraftsdorf", "Kraftsdorf (Gera)", "Kraftsdorf (Gera)", UL, ["Kraftsdorf"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("146", "b5")], "Mad. Seydel"),
    (4, "Roben", "Roben (Gera)", "Roben (Gera)", UL, ["Roben"], "gleichnis", "Gleichnis vom Unkraut unter dem Weizen", "Parable of the tares", [("146", "b7")], "Buschendorf"),
    (5, "Leumnitz", "Leumnitz (Gera)", "Leumnitz (Gera)", UL, ["Leumnitz"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("147", "b2")], "Thrändorf"),
    (6, "Großaga", "Großaga (Gera)", "Großaga (Gera)", UL, ["Großaga"], "gedicht", "Gedicht in drei Strophen über das Küssen", "Poem in three stanzas about kissing", [("147", "b5"), ("147", "b6"), ("147", "b7")], ""),
    (7, "Triebes", "Triebes (Schleiz)", "Triebes (Schleiz)", OL, ["Triebes"], "gespraech", "Vater und Sohn über Frost im Korn und einen verunglückten Nachbarn", "Father and son on frost in the grain and an injured neighbour", [("147", f"b{i}") for i in range(10, 14)] + [("148", "b1")], ""),
    (8, "Leitlitz-Weckersdorf", "Leitlitz-Weckersdorf (Schleiz)", "Leitlitz-Weckersdorf (Schleiz)", OL, ["Leitlitz", "Weckersdorf"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("148", "b3")], "Schmidt"),
    (8, "Leitlitz-Weckersdorf", "Leitlitz-Weckersdorf (Schleiz)", "Leitlitz-Weckersdorf (Schleiz)", OL, ["Leitlitz", "Weckersdorf"], "gespraech", "Zwei Nachbarn über Wetter, Hagelversicherung und ein verunglücktes Mädchen", "Two neighbours on weather, hail insurance and an injured girl", [("148", "b4")], "Schmidt"),
    (9, "Oettersdorf", "Oettersdorf (Schleiz)", "Oettersdorf (Schleiz)", OL, ["Oettersdorf"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("149", "b2")], "Riedel"),
    (10, "Mielesdorf", "Mielesdorf (Schleiz)", "Mielesdorf (Schleiz)", OL, ["Mielesdorf"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("149", "b4")], "Meyer"),
    (11, "Tanna", "Tanna (Schleiz)", "Tanna (Schleiz)", OL, ["Tanna"], "gespraech", "Zwei Männer über Kaffee, Mittagessen und Wurst", "Two men on coffee, midday meal and sausage", [("149", "b6")] + [("150", f"b{i}") for i in range(1, 9)], ""),
    (12, "Oßla", "Oßla (Lobenstein-Ebersdorf)", "Oßla (Lobenstein-Ebersdorf)", OL, ["Oßla"], "gleichnis", "Gleichnis vom Sämann", "Parable of the sower", [("150", "b10")], "Hüttig"),
    (12, "Oßla", "Oßla (Lobenstein-Ebersdorf)", "Oßla (Lobenstein-Ebersdorf)", OL, ["Oßla"], "gespraech", "Zwei Alte vergleichen früher und jetzt (Wirtshäuser, Advokaten)", "Two old men compare past and present (inns, lawyers)", [("150", f"b{i}") for i in range(11, 19)], "Hüttig"),
    (13, "Altengesees", "Altengesees (Lobenstein-Ebersdorf)", "Altengesees (Lobenstein-Ebersdorf)", OL, ["Altengesees"], "gleichnis", "Gleichnis vom Unkraut unter dem Weizen", "Parable of the tares", [("151", "b2")], "D. Garthe"),
    (14, "Titschendorf", "Titschendorf (Lobenstein-Ebersdorf)", "Titschendorf (Lobenstein-Ebersdorf)", OL, ["Titschendorf"], "gleichnis", "Gleichnis vom Sämann mit Deutung", "Parable of the sower with interpretation", [("151", "b4")], "Fr. Harnisch"),
]

rows = []
used = []
for k, (order, place, lde, len_, region, gaz, typ, tde, ten, blocks, contrib) in enumerate(S, start=1):
    lts = {LT[g][0] for g in gaz if g in LT}
    assert len(lts) == 1, (place, lts)
    lt = lts.pop()
    t = " ".join(text(p, b) for p, b in blocks)
    n = len(t.split())
    if contrib:
        last = text(*blocks[-1]).rstrip()
        key = "Thründorf" if contrib == "Thrändorf" else contrib
        # signature may sit in a separate block (Giebner p. 146 b3, Thründorf p. 147 b3) or at the end of the last block
        if last.endswith(key + ".") or last.endswith(key):
            n -= len(key.split())
    pages = sorted({p for p, _ in blocks}, key=int)
    page_str = pages[0] if len(pages) == 1 else f"{pages[0]}–{pages[-1]}"
    blk = ", ".join(sorted({b for _, b in blocks}, key=lambda s: int(s[1:])))
    first = blocks[0]
    rows.append([k, order, place, lde, len_, region, lt, TYPES[typ]["de"], TYPES[typ]["en"], tde, ten, n, contrib, page_str, first[0], first[1]])
    used.extend(blocks)
# signatures in separate blocks
used += [("146", "b3"), ("147", "b3")]
assert "Giebner" in text("146", "b3")
print(text("147", "b3"))

tot_words = sum(r[11] for r in rows)
places = {r[2] for r in rows}
print(len(rows), "texts;", len(places), "places;", tot_words, "words")
by_region = Counter()
by_lt = Counter()
for place in places:
    r = next(r for r in rows if r[2] == place)
    by_region[r[5]] += 1
    by_lt[r[6]] += 1
print(by_region, by_lt)
typ_n = Counter(r[8] for r in rows)
print(typ_n)
words_place = defaultdict(int)
for r in rows:
    words_place[r[2]] += r[11]
print(sorted(words_place.items(), key=lambda kv: -kv[1]))
top = sorted(words_place.items(), key=lambda kv: -kv[1])[:3]
parables = [r for r in rows if r[8].startswith("Parable")]
sower = [r for r in parables if "sower" in r[10]]
tares = [r for r in parables if "tares" in r[10]]
print(len(parables), len(sower), len(tares))
assert len(sower) == 8 and len(tares) == 2
unsigned = sorted({r[2] for r in rows if not r[12]})
contributors = sorted({r[12] for r in rows if r[12]})
print(unsigned, contributors, len(contributors))
dialogues = [r for r in rows if r[8] == "Conversation"]
print(len(dialogues), [r[2] for r in dialogues])

# distinct block refs for sources
refs = sorted({(p, b) for p, b in used}, key=lambda x: (int(x[0]), int(x[1][1:])))
src_refs = [{"page": p, "block": b} for p, b in refs]
pw = [r[11] for r in parables]
w_wal = words_place["Waltersdorf"]
share_wal = round(100 * w_wal / tot_words)

TYPE_DOMAIN = [TYPES[k] for k in TYPES]
ana = {
    "id": "mundart-sprachproben-orte-und-textsorten",
    "title": bi("Mundartproben nach Orten und Textsorten (S. 145–151)", "Dialect samples by place and text kind (pp. 145–151)"),
    "category": "dialect",
    "section": "t1-2-3",
    "sources": src_refs,
    "summary": bi(
        f"Brückner belegt die Mundart des Fürstenthums mit Sprachproben aus {len(places)} Orten, geordnet nach Unterland ({by_region[UL]} Orte) und Oberland ({by_region[OL]} Orte). Zusammen sind es {len(rows)} Texte mit rund {tot_words} Wörtern: Gleichnisse aus dem Evangelium, Gespräche, eine Fabel, eine Erzählung und ein Gedicht. Die Übersicht zeigt, aus welchen Orten und in welchem Umfang die Mundart dokumentiert ist, und macht sichtbar, dass dieselbe Bibelstelle in zehn Orten zum Vergleich steht.",
        f"Brückner documents the dialect of the principality with samples from {len(places)} places, arranged by Unterland ({by_region[UL]} places) and Oberland ({by_region[OL]} places). In all there are {len(rows)} texts of about {tot_words} words: Gospel parables, conversations, a fable, a story and a poem. The overview shows from which places and to what extent the dialect is documented, and makes visible that the same Bible passage is available for comparison from ten places.",
    ),
    "method": bi(
        "Die Proben auf S. 145–151 wurden nach den Überschriften der Orte in Texte gegliedert (Textsorte und Titel vom Bearbeiter vergeben). Die Wortzahl ist die Zahl der durch Leerzeichen getrennten Wörter der Blöcke ohne Namenszeichen des Einsenders und nur ein Näherungswert für den Umfang. Der Landestheil jedes Ortes stammt aus dem Gazetteer der Ortskunde (Teil II); Brückners Gliederung in Unterland und Oberland steht daneben. Die Einsender sind die rechtsbündig gesetzten Namen am Ende der Proben.",
        "The samples on pp. 145–151 were divided into texts according to the place headings (text kind and title assigned by the analyst). The word count is the number of space-separated words in the blocks without the contributor’s signature and is only an approximate measure of length. The district (Landestheil) of each place comes from the gazetteer of the topography (Part II); Brückner’s division into Unterland and Oberland is given alongside. The contributors are the right-aligned names at the end of the samples.",
    ),
    "findings": [
        bi(
            f"Die {by_region[UL]} Proben des Unterlands stammen sämtlich aus dem Landestheil Gera; im Oberland liegen {by_lt['Schleiz']} Orte im Landestheil Schleiz (Triebes, Leitlitz-Weckersdorf, Oettersdorf, Mielesdorf, Tanna) und {by_lt['Lobenstein-Ebersdorf']} im Landestheil Lobenstein-Ebersdorf (Oßla, Altengesees, Titschendorf).",
            f"All {by_region[UL]} samples of the Unterland come from the district of Gera; in the Oberland {by_lt['Schleiz']} places lie in the district of Schleiz (Triebes, Leitlitz-Weckersdorf, Oettersdorf, Mielesdorf, Tanna) and {by_lt['Lobenstein-Ebersdorf']} in the district of Lobenstein-Ebersdorf (Oßla, Altengesees, Titschendorf).",
        ),
        bi(
            f"In {len(parables)} Orten wird ein Evangelium-Gleichnis in der Ortsmundart wiedergegeben (Sämann {len(sower)}-mal, Unkraut unter dem Weizen {len(tares)}-mal); der Sämann-Text wird außerdem im Geraer Gespräch zitiert. Damit lassen sich Lautformen desselben Textes von Ort zu Ort vergleichen.",
            f"In {len(parables)} places a Gospel parable is given in the local dialect (sower {len(sower)} times, tares {len(tares)} times); the sower text is also quoted in the Gera conversation. Sound forms of the same text can therefore be compared from place to place.",
        ),
        bi(
            f"Am ausführlichsten ist Waltersdorf dokumentiert (drei Texte, rund {w_wal} Wörter, etwa {share_wal} % des gesamten Umfangs), gefolgt von {top[1][0]} und {top[2][0]}.",
            f"Waltersdorf is documented at greatest length (three texts, about {w_wal} words, about {share_wal} % of the total), followed by {top[1][0]} and {top[2][0]}.",
        ),
        bi(
            f"Freie Texte außerhalb der Bibelstellen sind überwiegend Gespräche ({len(dialogues)}: Gera, Triebes, Leitlitz-Weckersdorf, Tanna, Oßla); Fabel, Erzählung und Gedicht kommen nur je einmal vor. Vier Proben (Gera, Großaga, Triebes, Tanna) sind ohne Namen des Einsenders; zehn Einsender sind genannt.",
            f"Free texts apart from the Bible passages are mostly conversations ({len(dialogues)}: Gera, Triebes, Leitlitz-Weckersdorf, Tanna, Oßla); fable, story and poem occur only once each. Four samples (Gera, Großaga, Triebes, Tanna) carry no contributor’s name; ten contributors are named.",
        ),
    ],
    "caveats": [
        bi(
            "Die Auswahl der Orte beruht auf den Einsendungen; sie ist weder gleichmäßig über das Land verteilt noch repräsentativ (aus dem Saalgebiet und dem Reichenfelser Webergebiet liegen kaum Proben vor). Orthographie und Lautzeichen (ê, ô, aï, ƒ) unterscheiden sich je nach Einsender und sind nicht ohne Weiteres vergleichbar.",
            "The choice of places depends on what was sent in; it is neither evenly spread over the country nor representative (hardly any samples exist from the Saale area and the Reichenfels weaving district). Orthography and sound symbols (ê, ô, aï, ƒ) differ by contributor and are not directly comparable.",
        ),
        bi(
            "Die Wortzahlen sind Näherungswerte (Leerzeichen-Zählung, mundartliche Zusammenziehungen zählen als ein Wort). Der Einsender der Leumnitzer Probe ist in der Transkription »Thründorf«; am Faksimile ist »Thrändorf« lesbar (Fraktur ä/ü). Die Zuordnung der Textsorten und der Titel stammt vom Bearbeiter.",
            "The word counts are approximations (space counting; dialect contractions count as one word). The contributor of the Leumnitz sample is “Thründorf” in the transcription; “Thrändorf” can be read on the facsimile (Fraktur ä/ü). The assignment of text kinds and titles is the analyst’s.",
        ),
    ],
    "datasets": [
        {
            "name": "samples",
            "title": bi("Mundartproben (Texte) mit Ort, Landestheil, Textsorte und Umfang", "Dialect samples (texts) with place, district, text kind and length"),
            "columns": [
                {"name": "no", "label": bi("Nr.", "No."), "type": "integer", "unit": None, "derived": True},
                {"name": "order", "label": bi("Reihenfolge der Orte bei Brückner", "Order of places in Brückner"), "type": "integer", "unit": None, "derived": True},
                {"name": "place", "label": bi("Ort", "Place"), "type": "string", "unit": None},
                {"name": "label_de", "label": bi("Ort (de, Anzeige)", "Place (de, display)"), "type": "string", "unit": None, "derived": True},
                {"name": "label_en", "label": bi("Ort (en, Anzeige)", "Place (en, display)"), "type": "string", "unit": None, "derived": True},
                {"name": "region", "label": bi("Gebiet nach Brückner", "Region according to Brückner"), "type": "string", "unit": None},
                {"name": "district", "label": bi("Landestheil (Gazetteer)", "District (gazetteer)"), "type": "string", "unit": None, "derived": True},
                {"name": "kind_de", "label": bi("Textsorte (de)", "Text kind (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "kind_en", "label": bi("Textsorte (en)", "Text kind (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "title_de", "label": bi("Inhalt (de)", "Content (de)"), "type": "string", "unit": None, "derived": True},
                {"name": "title_en", "label": bi("Inhalt (en)", "Content (en)"), "type": "string", "unit": None, "derived": True},
                {"name": "words", "label": bi("Umfang (Wörter)", "Length (words)"), "type": "integer", "unit": "Wörter", "derived": True},
                {"name": "contributor", "label": bi("Einsender", "Contributor"), "type": "string", "unit": None},
                {"name": "pages", "label": bi("Seiten", "Pages"), "type": "string", "unit": None},
                {"name": "page", "label": bi("Erste Seite", "First page"), "type": "string", "unit": None},
                {"name": "block", "label": bi("Erster Block", "First block"), "type": "string", "unit": None},
            ],
            "rows": rows,
            "source_refs": src_refs,
        }
    ],
    "charts": [
        {
            "id": "c1",
            "dataset": "samples",
            "title": bi("Umfang der Mundartproben nach Ort und Textsorte", "Length of the dialect samples by place and text kind"),
            "caption": bi(
                f"Wörter je Probe, in Brückners Reihenfolge (oben Unterland, unten Oberland; in Klammern der Landestheil). Am ausführlichsten belegt sind Waltersdorf, Leitlitz-Weckersdorf, Oßla und Tanna; die Gleichnisse umfassen {min(pw)} bis {max(pw)} Wörter.",
                f"Words per sample, in Brückner’s order (Unterland above, Oberland below; district in parentheses). Documented at greatest length are Waltersdorf, Leitlitz-Weckersdorf, Oßla and Tanna; the parables range from {min(pw)} to {max(pw)} words.",
            ),
            "vegalite": {
                "height": 380,
                "mark": "bar",
                "encoding": {
                    "y": {"field": {"de": "label_de", "en": "label_en"}, "type": "nominal", "sort": {"field": "order", "op": "min"}, "title": None, "axis": {"labelLimit": 420}},
                    "x": {"field": "words", "aggregate": "sum", "type": "quantitative", "title": bi("Wörter", "Words")},
                    "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": None, "scale": {"domain": TYPE_DOMAIN}, "legend": {"labelLimit": 400, "columns": 2}},
                    "tooltip": [
                        {"field": {"de": "label_de", "en": "label_en"}, "title": bi("Ort", "Place")},
                        {"field": {"de": "title_de", "en": "title_en"}, "title": bi("Text", "Text")},
                        {"field": "words", "title": bi("Wörter", "Words")},
                        {"field": "contributor", "title": bi("Einsender", "Contributor")},
                        {"field": "pages", "title": bi("Seiten", "Pages")},
                    ],
                },
            },
        },
        {
            "id": "c2",
            "dataset": "samples",
            "title": bi("Textsorten nach Landestheil", "Text kinds by district"),
            "caption": bi(
                "Zahl der Proben je Landestheil und Textsorte: Fabel, Erzählung und Gedicht sind nur aus dem Landestheil Gera belegt, Gespräche vor allem aus Schleiz.",
                "Number of samples per district and text kind: fable, story and poem are attested only from the district of Gera, conversations mainly from Schleiz.",
            ),
            "vegalite": {
                "height": 260,
                "mark": "bar",
                "encoding": {
                    "x": {"field": "district", "type": "nominal", "sort": ["Gera", "Schleiz", "Lobenstein-Ebersdorf"], "title": None, "axis": {"labelAngle": 0, "labelLimit": 400}},
                    "y": {"aggregate": "count", "type": "quantitative", "title": bi("Proben", "Samples"), "axis": {"tickMinStep": 1}},
                    "color": {"field": {"de": "kind_de", "en": "kind_en"}, "type": "nominal", "title": None, "scale": {"domain": TYPE_DOMAIN}, "legend": {"labelLimit": 400, "columns": 2}},
                    "tooltip": [
                        {"field": "district", "title": bi("Landestheil", "District")},
                        {"field": {"de": "kind_de", "en": "kind_en"}, "title": bi("Textsorte", "Text kind")},
                        {"aggregate": "count", "title": bi("Proben", "Samples")},
                    ],
                },
            },
        },
    ],
    "transcription_issues": [
        {"page": "147", "block": "b3", "transcribed": "Thründorf.", "facsimile": "Thrändorf.", "checked_facsimile": True, "note": "Name des Einsenders der Leumnitzer Probe; Fraktur ä/ü am Faksimile als »ä« gelesen."}
    ],
    "keywords": {
        "de": ["Mundart", "Sprachproben", "Dialekt", "Gleichnis vom Sämann", "Unterland", "Oberland", "Gera", "Tanna", "Titschendorf", "Waltersdorf"],
        "en": ["dialect", "dialect samples", "parable of the sower", "Unterland", "Oberland", "Gera", "Tanna", "Titschendorf", "Waltersdorf"],
    },
    "related": [],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
