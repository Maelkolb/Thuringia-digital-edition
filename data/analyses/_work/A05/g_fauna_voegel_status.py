"""Analysis: songbirds etc. by frequency in Unterland vs Oberland (p. 84) and raptors by frequency (p. 85), with the corrections of p. 831."""
from collections import Counter, defaultdict
from common import *

CAT = {  # key: (order, label_de, label_en, lean_de, lean_en, printed phrase)
    "D": (1, "Nur im Unterland (selten)", "Unterland only (rare)", "Unterland", "Unterland", "selten im Unterlande und nicht vorkömmlich im Oberlande"),
    "C": (2, "Unterland häufiger", "More common in Unterland", "Unterland", "Unterland", "nicht selten im Unterlande, selten oder weniger häufig im Oberlande"),
    "A": (3, "Beide Gebiete häufig", "Common in both", "beide Gebiete", "both areas", "häufig oder nicht selten im Unterlande und im Oberlande"),
    "B": (4, "Beide Gebiete selten", "Rare in both", "beide Gebiete", "both areas", "selten in beiden Gebieten"),
    "E": (5, "Oberland häufiger", "More common in Oberland", "Oberland", "Oberland", "häufiger im Oberlande als im Unterlande"),
}
# (category, name as printed/reconstructed, name after p.831, n_taxa, qualifier printed, p.831 note)
B = []


def add(cat, name, n=1, note=None, corr_name=None, corr_note=None):
    B.append((cat, name, corr_name or name, n, note, corr_note))


# A: häufig oder nicht selten in beiden
for nm, n, note in [
    ("Amseln", 1, None), ("Singdrosseln", 1, "(Zippen)"), ("Misteldrosseln", 1, None), ("Rothdrosseln", 1, "auf dem Zuge"),
    ("Krammetsvogel (Ziemer)", 1, "eigentlicher; colonienweise im pöllwitzer Walde und bei Niederdorf"), ("Rohrsperling", 1, None),
    ("Spottlaubvogel", 1, None), ("Weidenzeisig", 1, None), ("Rothschwänzchen (beide)", 2, "»beide Rothschwänzchen«"), ("Rothkehlchen", 1, None),
    ("graue Grasmücke", 1, None), ("fahle Grasmücke", 1, None), ("Klappergrasmücke", 1, None), ("Zaunkönig", 1, None),
    ("Goldhähnchen (beide)", 2, "»beide Goldhähnchen«"), ("gewöhnlicher Baumläufer", 1, None), ("Spechtmeise", 1, "im Druck »Specht-, Kohl-, Tannen- und Schwanzmeise«"),
    ("Kohlmeise", 1, None), ("Tannenmeise", 1, None), ("Schwanzmeise", 1, None), ("Bachstelze", 1, None), ("Baumpieper", 1, None),
    ("Heidelerche", 1, None), ("Feldlerche", 1, None), ("Haubenlerche", 1, "mehr und mehr zum Standvogel übergehend"),
    ("Goldammer", 1, None), ("Hänfling", 1, None), ("Stieglitz", 1, None), ("Zeisig", 1, "in beiden Gebieten brütend"),
    ("Leinfinke", 1, "strichweise"), ("Edelfinke", 1, None), ("Sperlinge", 1, "einige körnerarme Orte des Oberlandes meidend (Fußnote)"),
    ("Grünling (Zwuntsch, Zetscher)", 1, None), ("Gimpel", 1, "im Oberlande verhaßt"), ("Seidenschwanz", 1, None), ("Holzheher", 1, None),
    ("Dohlen", 1, "an einzelnen Punkten seßhaft"), ("Rauchschwalbe", 1, None), ("Segler", 1, None), ("Ziegenmelker (Nachtschatten)", 1, None),
    ("Grünspecht", 1, None), ("Eisvogel", 1, None),
]:
    add("A", nm, n, note)
for nm in ["Heuschreckensänger", "grauer Fliegenschnapper", "Kernbeißer", "Grauspecht"]:
    add("B", nm)
for nm in ["Rohrdrossel", "Rohrsänger", "schwirrender Laubvogel", "Rohrammer", "Hausschwalbe", "Pirol", "Kukuk"]:
    add("C", nm)
add("C", "die drei Grünspechte", 3, "der große Buntspecht nicht selten im Unterlande nistend", "die drei Buntspechte", "S. 831: »lies: Buntspechte statt Grünspechte«")
add("D", "Nachtigall", 1, None, None, "S. 831 (zu S. 85 Z. 7): Hauptschuld am Wegbleiben der Nachtigall im Unterland sei das Eingehen des Buschholzes in den Seitenthälern der Elster und der Mangel an Brutplätzen an den Ufern")
for nm in ["Sperbergrasmücke", "Uferschwalbe", "Krautvogel", "Wiedehopf", "Wendehals", "Nebelkrähe"]:
    add("D", nm)
add("D", "braunkehliger Steinschmetter", 1, None, "braunkehliger Steinschmätzer", "S. 831: »lies: Steinschmätzer statt Steinschmetter«")
add("E", "Wasserschwätzer", 1, "nur im Winter im Unterlande")
add("E", "Staar", 1)
add("E", "großer Steinschmetter", 1, None, "großer Steinschmätzer", "S. 831: »lies: Steinschmätzer statt Steinschmetter«")
add("E", "Kiefernkreuzschnabel", 1, "selten im Unterlande nistend, aber dann häufig")
add("E", "Fichtenkreuzschnabel", 1, "selten im Unterlande nistend, aber dann häufig")
add("E", "Würger", 1, "der große Würger (wälsche Elster) im Unterlande ausgerottet", None,
    "S. 831: der große Würger galt eine Zeit lang als ausgerottet, der Sommer 1869 hat ihn wieder als einheimisch nachgewiesen")

# verify a few of the entries against the block text (names as transcribed)
t84 = re.sub(r"\s+", " ", text("84", "b1"))
for key in ["Amseln", "Rothdrosseln", "Rohrsperling", "Spottlaubvogel", "Klappergrasmücke", "Zaunkönig", "Baumläufer", "Bachstelze", "Baumpieper", "Goldammer",
            "Hänfling", "Stieglitz", "Leinfinke", "Edelfinke", "Seidenschwanz", "Holzheher", "Rauchschwalbe", "Segler", "Ziegenmelker", "Eisvogel",
            "Heuschreckensänger", "Fliegenschnapper", "Kernbeißer", "Grauspecht", "Rohrdrossel", "Rohrsänger", "schwirrender Laubvogel", "Rohrammer",
            "Hausschwalbe", "Pirol", "Kukuk", "drei Grünspechte", "Nachtigall", "Sperbergrasmücke", "Uferschwalbe", "Krautvogel", "Wiedehopf", "Wendehals",
            "Nebelkrähe", "Wasserschwätzer", "Staar", "Kiefern- und Fichtenkreuzschnabel", "Würger", "Specht-, Kohl-, Tannen- und Schwanzmeise",
            "beide Rothschwänzchen", "beide Goldhähnchen", "graue und fahle Grasmücke", "Heidel-, Feld- und Haubenlerche", "Grünling oder Zwuntsch"]:
    assert key in t84, key

b_rows = []
for cat, name, cname, n, note, cnote in B:
    c = CAT[cat]
    b_rows.append([cat, c[0], c[1], c[2], c[3], c[4], name, cname, n, note, cnote, "84", "b1"])
tax = Counter()
ent = Counter()
for r in b_rows:
    tax[r[0]] += r[8]
    ent[r[0]] += 1
print("taxa", dict(tax), "entries", dict(ent), "total taxa", sum(tax.values()), "entries", sum(ent.values()))
n_tax = sum(tax.values())
ul_lean = tax["C"] + tax["D"]
print(ul_lean, tax["E"])
n_corr = sum(1 for r in b_rows if r[10] and ('lies' in r[10] or 'galt' in r[10]))
assert n_corr == 4

# ---------------------------------------------------------------- raptors (p. 85 b2)
RAP = [
    ("Sperber", "häufig", None), ("Mäusebussard", "häufig", None), ("Flußadler", "häufig", "schon im Juli vorkommend"), ("Thurmfalke", "häufig", None),
    ("Rauchbussard", "häufig", "schädlich; im Winter"), ("Hühnerhabicht", "nicht selten", None), ("Seeadler", "nicht selten", "des Winters im Unterlande"),
    ("Wespenbussard", "vereinzelt", None), ("Wanderfalke", "selten", None), ("Baumfalke", "selten", None), ("Milan", "noch seltener", None),
]
CLS = {"häufig": (1, "häufig", "common"), "nicht selten": (2, "nicht selten", "not rare"), "vereinzelt": (3, "vereinzelt", "scattered"),
       "selten": (4, "selten", "rare"), "noch seltener": (5, "noch seltener", "rarer still")}
t85 = re.sub(r"\s+", " ", text("85", "b2"))
assert "häufig der Sperber, Mäusebussard, Flußadler (schon im Juli vorkommend), der Thurmfalke und der schädliche Rauchbussard (im Winter)" in t85
assert "nicht selten der Hühnerhabicht und des Winters im Unterlande der Seeadler; vereinzelt der Wespenbussard; selten der Wanderfalke und Baumfalke und noch seltener der Milan" in t85
rap_rows = []
rank = Counter()
for nm, cl, note in RAP:
    rank[cl] += 1
    rap_rows.append([nm, CLS[cl][0], CLS[cl][1], CLS[cl][2], rank[cl], note, "85", "b2"])
n_rap_common = sum(1 for r in RAP if r[1] == "häufig")

REFS_B = [{"page": "84", "block": "b1"}]
ana = {
    "id": "fauna-voegel-unterland-oberland",
    "title": bi("Vogelarten nach Häufigkeit in Unterland und Oberland", "Bird species by frequency in the Unterland and the Oberland"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": [{"page": "84", "block": "b1"}, {"page": "85", "block": "b2"}, {"page": "84", "block": "fn1"}, {"page": "831", "block": "b1"}, {"page": "831", "block": "b2"}],
    "summary": bi(
        f"Brückner ordnet die häufigeren Vogelarten in fünf Gruppen, je nachdem, ob sie im Unterland (Gera) oder im Oberland (Schleiz, Lobenstein) häufiger oder seltener sind, und stuft die Raubvögel nach ihrer Häufigkeit ein. Ausgezählt ergeben sich {n_tax} Vogelnennungen; die Berichtigungen von S. 831 (Buntspechte, Steinschmätzer, großer Würger) sind eingearbeitet.",
        f"Brückner sorts the commoner bird species into five groups according to whether they are more or less frequent in the Unterland (Gera) or the Oberland (Schleiz, Lobenstein), and grades the birds of prey by frequency. Counted, this gives {n_tax} bird taxa; the corrections of p. 831 (woodpeckers, wheatears, great grey shrike) have been incorporated."),
    "method": bi(
        f"Die Aufzählung auf S. 84 wurde in Einzelnennungen aufgelöst: Reihungen wie »Specht-, Kohl-, Tannen- und Schwanzmeise« ergeben vier Nennungen, Zusammenfassungen mit Zahlwort (»beide Rothschwänzchen«, »die drei Grünspechte«) zählen als zwei bzw. drei Taxa, Pluralformen ohne Zahl (Sperlinge, Dohlen, Würger) als eines. Die fünf Gruppen sind Brückners Gliederung (Wortlaut in den Daten). Die Raubvögel (S. 85) sind nach seinen Häufigkeitswörtern geordnet: häufig, nicht selten, vereinzelt, selten, noch seltener. Die Berichtigungen von S. 831 sind in einer eigenen Spalte angegeben, die korrigierten Namen in einer zweiten. Vogelnamen sind die des Originals, nicht modernisiert.",
        f"The enumeration on p. 84 was resolved into single entries: sequences such as “Specht-, Kohl-, Tannen- und Schwanzmeise” give four entries, combined entries with a number word (“beide Rothschwänzchen”, “die drei Grünspechte”) count as two or three taxa, plural forms without a number (Sperlinge, Dohlen, Würger) as one. The five groups are Brückner's classification (wording in the data). The birds of prey (p. 85) are ordered by his frequency words: häufig, nicht selten, vereinzelt, selten, noch seltener. The corrections of p. 831 are given in a column of their own, the corrected names in a second. Bird names are those of the original, not modernised."),
    "findings": [
        bi(f"Der größte Teil der genannten Vögel ({tax['A']} von {n_tax} Taxa, {de(100 * tax['A'] / n_tax, 0)} %) ist in beiden Landesteilen häufig oder nicht selten. Zum Unterland neigen {ul_lean} Taxa ({tax['D']} davon kommen im Oberland nicht vor: Nachtigall, Sperbergrasmücke, Steinschmätzer, Uferschwalbe, Krautvogel, Wiedehopf, Wendehals, Nebelkrähe), zum Oberland {tax['E']} (Wasserschwätzer, Star, Steinschmätzer, Kreuzschnäbel, Würger).",
           f"Most of the birds named ({tax['A']} of {n_tax} taxa, {en(100 * tax['A'] / n_tax, 0)} %) are common or not rare in both parts of the territory. {ul_lean} taxa lean towards the Unterland ({tax['D']} of them do not occur in the Oberland: nightingale, barred warbler, “braunkehliger Steinschmätzer”, sand martin, Krautvogel, hoopoe, wryneck, hooded crow), {tax['E']} towards the Oberland (dipper, starling, “großer Steinschmätzer”, crossbills, shrikes)."),
        bi(f"Brückners Berichtigungen (S. 831) betreffen {n_corr} Einträge: Bei den »drei Grünspechten« lies Buntspechte, beim braunkehligen und beim großen »Steinschmetter« Steinschmätzer; der im Unterland für ausgerottet erklärte große Würger ist im Sommer 1869 wieder als einheimisch nachgewiesen worden. Zur Nachtigall, die im Unterland selten ist und im Oberland fehlt, ergänzt er als Hauptgrund das Eingehen des Buschholzes in den Seitentälern der Elster.",
           f"Brückner's corrections (p. 831) concern {n_corr} entries: for the “three Grünspechte” read Buntspechte (spotted woodpeckers), for the “braunkehliger” and the “große Steinschmetter” read Steinschmätzer; the great grey shrike declared exterminated in the Unterland was shown again to be native in the summer of 1869. For the nightingale, rare in the Unterland and absent from the Oberland, he adds as the main reason the loss of brushwood in the side valleys of the Elster."),
        bi(f"Unter den Raubvögeln nennt Brückner {n_rap_common} Arten als häufig (Sperber, Mäusebussard, Flußadler, Thurmfalke, Rauchbussard), zwei als nicht selten, eine als vereinzelt, zwei als selten (Wanderfalke, Baumfalke) und den Milan als noch seltener.",
           f"Among the birds of prey Brückner names {n_rap_common} species as common (sparrowhawk, common buzzard, Flußadler, kestrel, Rauchbussard), two as not rare, one as scattered, two as rare (peregrine, hobby) and the kite as rarer still."),
    ],
    "caveats": [
        bi("Die Gruppen sind qualitativ und beruhen auf Brückners Einschätzung; Zählungen liegen nicht zugrunde. Die Zahl der Taxa hängt von den Zählregeln ab (Sammelbezeichnungen, Pluralformen) und ist als Größenordnung zu lesen.",
           "The groups are qualitative and rest on Brückner's judgement; no counts underlie them. The number of taxa depends on the counting rules (collective designations, plural forms) and should be read as an order of magnitude."),
        bi("Im Faksimile steht an beiden Stellen »Steinschmetter«, die Transkription hat »Steinschmetzer«; Brückner berichtigt zu »Steinschmätzer« (S. 831). Seine Zeilenangaben (Z. 16, 19, 21, 23 v. o.) passen zu den Zeilen im Faksimile.",
           "The facsimile reads “Steinschmetter” in both places, the transcription has “Steinschmetzer”; Brückner corrects it to “Steinschmätzer” (p. 831). His line numbers (lines 16, 19, 21, 23 from the top) match the lines in the facsimile."),
        bi("Brückners Namen sind Volks- und Jägernamen des 19. Jahrhunderts; auf wissenschaftliche Namen wurde verzichtet, weil mehrere Bezeichnungen (Zwuntsch, Krautvogel, Holzheher, Flußadler) nicht eindeutig sind.",
           "Brückner's names are folk and hunters' names of the 19th century; scientific names were left out because several designations (Zwuntsch, Krautvogel, Holzheher, Flußadler) are not unambiguous."),
    ],
    "transcription_issues": [
        {"page": "84", "block": "b1", "transcribed": "Steinschmetzer (2 ×)", "facsimile": "Steinschmetter (2 ×; Z. 19 und 21 v. o.)", "checked_facsimile": True,
         "note": "Brückner berichtigt S. 831: »Steinschmätzer statt Steinschmetter«."},
    ],
    "datasets": [
        {"name": "birds_by_area",
         "title": bi("Vogelnennungen nach Häufigkeit in Unterland und Oberland (S. 84)", "Bird entries by frequency in the Unterland and the Oberland (p. 84)"),
         "columns": [
             col("cat_key", "Gruppe (Schlüssel)", "Group (key)", "string", None, True),
             col("cat_order", "Reihenfolge", "Order", "integer", None, True),
             col("cat_de", "Gruppe", "Group", "string", None, True),
             col("cat_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("lean_de", "Schwerpunkt", "Centre of gravity", "string", None, True),
             col("lean_en", "Schwerpunkt (EN)", "Centre of gravity (EN)", "string", None, True),
             col("bird", "Vogel (Druck, aufgelöst)", "Bird (print, resolved)", "string", None),
             col("bird_corrected", "Vogel (nach Berichtigung S. 831)", "Bird (after correction p. 831)", "string", None),
             col("n_taxa", "Zahl der Taxa", "Number of taxa", "integer", None, True),
             col("qualifier", "Zusatz im Druck", "Qualifier in print", "string", None),
             col("correction", "Berichtigung (S. 831)", "Correction (p. 831)", "string", None),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": b_rows, "source_refs": REFS_B},
        {"name": "raptors",
         "title": bi("Raubvögel nach Häufigkeit (S. 85)", "Birds of prey by frequency (p. 85)"),
         "columns": [
             col("bird", "Vogel", "Bird", "string", None),
             col("class_order", "Stufe (Reihenfolge)", "Level (order)", "integer", None, True),
             col("class_de", "Häufigkeit", "Frequency", "string", None),
             col("class_en", "Häufigkeit (EN)", "Frequency (EN)", "string", None, True),
             col("rank", "Platz in der Stufe", "Rank within level", "integer", None, True),
             col("qualifier", "Zusatz im Druck", "Qualifier in print", "string", None),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": rap_rows, "source_refs": [{"page": "85", "block": "b2"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "birds_by_area",
         "title": bi("Welche Vögel sind im Unterland, welche im Oberland häufiger?", "Which birds are more common in the Unterland, which in the Oberland?"),
         "caption": bi("Zahl der von Brückner genannten Vogeltaxa je Gruppe (S. 84, mit den Berichtigungen von S. 831). Die Balken sind von »nur im Unterland« bis »Oberland häufiger« geordnet.",
                       "Number of bird taxa named by Brückner per group (p. 84, with the corrections of p. 831). The bars are ordered from “Unterland only” to “more common in the Oberland”."),
         "vegalite": {"height": 240, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "cat_de", "en": "cat_en"}, "type": "nominal", "sort": {"field": "cat_order", "op": "min"}, "title": None, "axis": {"labelLimit": 240}},
                          "x": {"aggregate": "sum", "field": "n_taxa", "type": "quantitative", "title": bi("Vogeltaxa", "Bird taxa")},
                          "color": {"field": {"de": "lean_de", "en": "lean_en"}, "type": "nominal", "title": bi("Schwerpunkt", "Centre of gravity"),
                                    "scale": {"domain": [{"de": "Unterland", "en": "Unterland"}, {"de": "Oberland", "en": "Oberland"}, {"de": "beide Gebiete", "en": "both areas"}]}},
                          "tooltip": [{"field": {"de": "cat_de", "en": "cat_en"}, "title": bi("Gruppe", "Group")},
                                      {"aggregate": "sum", "field": "n_taxa", "title": bi("Taxa", "Taxa")}]}}},
        {"id": "c2", "dataset": "raptors",
         "title": bi("Raubvögel nach Häufigkeit (S. 85)", "Birds of prey by frequency (p. 85)"),
         "caption": bi("Brückners Häufigkeitsstufen für elf Raubvögel; Zusätze (»im Winter«, »schädlich«) stehen im Tooltip.",
                       "Brückner's frequency levels for eleven birds of prey; qualifiers (“in winter”, “harmful”) are in the tooltip."),
         "vegalite": {"height": 190,
                      "mark": {"type": "text", "fontSize": 12, "align": "center"},
                      "encoding": {
                          "x": {"field": {"de": "class_de", "en": "class_en"}, "type": "nominal", "title": None, "axis": {"labelAngle": 0, "orient": "top"},
                                "sort": {"field": "class_order", "op": "min"}},
                          "y": {"field": "rank", "type": "quantitative", "axis": None, "scale": {"reverse": True, "domain": [0.5, 5.5]}},
                          "text": {"field": "bird", "type": "nominal"},
                          "tooltip": [{"field": "bird", "title": bi("Vogel", "Bird")},
                                      {"field": {"de": "class_de", "en": "class_en"}, "title": bi("Häufigkeit", "Frequency")},
                                      {"field": "qualifier", "title": bi("Zusatz", "Qualifier")}]}}},
    ],
    "keywords": {"de": ["Vögel", "Vogelwelt", "Singvögel", "Raubvögel", "Nachtigall", "Unterland", "Oberland", "Häufigkeit", "Buntspecht", "Steinschmätzer"],
                 "en": ["birds", "avifauna", "songbirds", "birds of prey", "nightingale", "Unterland", "Oberland", "frequency", "woodpecker", "wheatear"]},
    "related": ["fauna-voegel-zugzeiten-und-seltene-gaeste", "fauna-aenderungen-seit-1647"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
