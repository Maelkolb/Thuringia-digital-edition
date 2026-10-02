"""B01 analysis 2: the list of subscribers (pp. 835-840) - dataset and readership analysis."""
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
from common import write_analysis
from subs_classify import build, GROUP_LABELS, REGION_LABELS, FACSIMILE_FIXES

S = build()
N = len(S)
TOTAL_COPIES = sum(r["copies"] for r in S)
GROUP_ORDER = list(GROUP_LABELS)
REGION_ORDER = ["gera", "schleiz", "lobenstein", "outside"]

# ------------------------------------------------------------------ aggregates
def agg(keyf):
    e, c = Counter(), Counter()
    for r in S:
        k = keyf(r)
        e[k] += 1
        c[k] += r["copies"]
    return e, c

ge, gc = agg(lambda r: r["group"])
re_, rc = agg(lambda r: r["region"])
pe, pc = agg(lambda r: (r["place"], r["region"]))
grp_rank = {g: i + 1 for i, (g, _) in enumerate(sorted(ge.items(), key=lambda kv: (-kv[1], -gc[kv[0]])))}
gre, grc = agg(lambda r: (r["group"], r["region"]))

inside = [r for r in S if r["region"] != "outside"]
outside = [r for r in S if r["region"] == "outside"]
pct = lambda a, b: 100 * a / b
fmt1 = lambda x: f"{x:.1f}"
dec = lambda x: f"{x:.1f}".replace(".", ",")

# ------------------------------------------------------------------ dataset rows
sub_rows = []
for i, r in enumerate(S, start=1):
    sub_rows.append([i, r["page"], r["row"], r["copies"], r["title"], r["name"], r["occupation"], r["place_printed"], r["place"],
                     r["qualifier"], r["region"], r["entity"], r["group"], r["inst_kind"], r["noble"]])
sub_cols = [
    ("entry_no", "Nr.", "No.", "integer", None, True, "laufende Nummer der Listeneinträge (editorisch)"),
    ("page", "Seite", "Page", "string", None, False, None),
    ("row", "Zeile", "Row", "string", None, False, "Tabellenzeile des Blocks; r17+r18 = vom Transkript auf zwei Zeilen verteilter Eintrag"),
    ("copies", "Exemplare", "Copies", "integer", "Expl.", False, "Spalte Expl. wie gedruckt"),
    ("title", "Anrede", "Form of address", "string", None, False, "Herr/Frau; das gedruckte Wiederholungszeichen „ steht für Herr; bei den Fürstlichkeiten die gedruckte Anrede"),
    ("name_printed", "Name (gedruckt)", "Name (as printed)", "string", None, False, "bei Einrichtungen die Bezeichnung; sieben Namen nach dem Faksimile korrigiert (transcription_issues)"),
    ("occupation_printed", "Beruf/Stand (gedruckt)", "Occupation/rank (as printed)", "string", None, False, "bei Einrichtungen leer; Schlusspunkt weggelassen"),
    ("place_printed", "Ort (gedruckt)", "Place (as printed)", "string", None, False, None),
    ("place", "Ort (normalisiert)", "Place (normalised)", "string", None, True, "Schreibung des Ortsregisters (S. 826–829), ohne Zusätze wie bei Gera"),
    ("place_qualifier", "Ortszusatz", "Place qualifier", "string", None, True, None),
    ("region", "Lage", "Location", "string", None, True, "gera | schleiz | lobenstein (Landestheil nach den Seitenzahlen des Ortsregisters) | outside (außerhalb des Fürstenthums)"),
    ("entity_type", "Art des Eintrags", "Type of entry", "string", None, True, "person | firm (Buchhandlung ohne Anrede oder mit Firmenname) | institution"),
    ("group", "Gruppe", "Group", "string", None, True, "Berufsgruppe nach den Regeln in classification"),
    ("institution_kind", "Art der Einrichtung", "Kind of institution", "string", None, True, "authority | library | society | company"),
    ("noble_particle", "Name mit v.", "Name with v.", "integer", None, True, "1 = gedruckter Name beginnt mit v. (kein Adelsbeleg)"),
]

# place aggregate
place_rows = []
for (p, rg), e in sorted(pe.items(), key=lambda kv: (-kv[1], -pc[kv[0]], kv[0][0])):
    place_rows.append([p, rg, e, pc[(p, rg)]])
group_rows = [[g, grp_rank[g], ge[g], gc[g]] for g in sorted(ge, key=lambda g: grp_rank[g])]
region_rows = [[rg, i + 1, re_[rg], rc[rg]] for i, rg in enumerate(REGION_ORDER)]
gr_rows = [[g, grp_rank[g], rg, REGION_ORDER.index(rg) + 1, gre.get((g, rg), 0), grc.get((g, rg), 0)] for g in sorted(ge, key=lambda g: grp_rank[g]) for rg in REGION_ORDER]

# classification codebook
cb = defaultdict(lambda: [0, 0])
for r in S:
    key = (r["group"], r["occupation"] if r["entity"] != "institution" else f"(Einrichtung: {r['inst_kind']})")
    cb[key][0] += 1
    cb[key][1] += r["copies"]
cb_rows = [[g, o, v[0], v[1]] for (g, o), v in sorted(cb.items(), key=lambda kv: (grp_rank[kv[0][0]], -kv[1][0], kv[0][1]))]

# ------------------------------------------------------------------ numbers for the text
n_book_out = sum(1 for r in outside if r["group"] == "booksellers")
n_persons = sum(1 for r in S if r["entity"] == "person")
n_firms = sum(1 for r in S if r["entity"] == "firm")
n_inst = sum(1 for r in S if r["entity"] == "institution")
n_places = len({(r["place"], r["region"]) for r in S})
n_places_in = len({r["place"] for r in inside})
one_entry_places = sum(1 for k, v in pe.items() if v == 1)
gera, schleiz, loben = pe[("Gera", "gera")], pe[("Schleiz", "schleiz")], pe[("Lobenstein", "lobenstein")]
untermhaus = pe[("Untermhaus", "gera")]
three_towns = gera + schleiz + loben
three_towns_c = pc[("Gera", "gera")] + pc[("Schleiz", "schleiz")] + pc[("Lobenstein", "lobenstein")]
teich = next(r for r in S if r["copies"] == 50)
book_e, book_c = ge["booksellers"], gc["booksellers"]
book_c_ex = book_c - teich["copies"]
princes = [r for r in S if r["group"] == "court" and r["page"] == "835"]
prince_copies_jl = sum(r["copies"] for r in princes if "j. L." in r["occupation"])
court_c = gc["court"]
multi = [r for r in S if r["copies"] > 1]
cate = sum(1 for r in S if r["occupation"] == "Catechet")
serving = ge["officials"] + ge["teachers"] + ge["clergy"] + ge["forestry_mining"] + ge["court"]
land = ge["farmers"] + ge["craftsmen"]
noble = sum(r["noble"] for r in S)
women = [r for r in S if r["title"] == "Frau" or "Fürstin" in r["occupation"] or "Amtmännin" in r["occupation"]]
top_groups = sorted(ge, key=lambda g: -ge[g])
GL = GROUP_LABELS
print(N, TOTAL_COPIES, n_persons, n_firms, n_inst, n_places, one_entry_places)
print("regions", re_, rc, "inside", len(inside), sum(r["copies"] for r in inside), "outside", len(outside), sum(r["copies"] for r in outside))
print("top groups", [(g, ge[g], gc[g]) for g in top_groups])
print("three towns", three_towns, three_towns_c, "untermhaus", untermhaus, "serving", serving, "land", land, "catechets", cate, "noble", noble, "women", len(women))
print("multi", len(multi), [(r["name"], r["copies"]) for r in multi])
print("prince copies jl", prince_copies_jl, "court copies", court_c, "book", book_e, book_c, book_c_ex)

# ------------------------------------------------------------------ texts
title = {"de": "Die Subskribenten: Leserschaft des Buchs 1870", "en": "The subscribers: readership of the book in 1870"}
summary = {
    "de": (f"Die Subscriptionsliste am Ende des Buchs nennt {N} Subskribenten (Personen, Firmen und Einrichtungen) mit zusammen {TOTAL_COPIES} Exemplaren, "
           f"jeweils mit Beruf oder Stand und Wohnort. Ausgewertet werden die Herkunftsorte, die Berufsgruppen und der Anteil von Bestellern außerhalb des "
           f"Fürstenthums. Die Liste zeigt eine Leserschaft aus Beamten, Lehrern, Geistlichen, Kaufleuten und Buchhandlungen, die stark auf Gera, Schleiz und Lobenstein "
           f"konzentriert ist."),
    "en": (f"The list of subscribers at the end of the book names {N} subscribers (persons, firms and institutions) taking {TOTAL_COPIES} copies in all, each with "
           f"occupation or rank and place of residence. The analysis covers places of origin, occupational groups and the share of subscribers from outside the "
           f"principality. The list shows a readership of officials, teachers, clergy, merchants and booksellers, strongly concentrated in Gera, Schleiz and Lobenstein."),
}
method = {
    "de": (f"Quelle sind die Tabellen auf S. 835–840 (je ein Block; Spalten Expl. / Name / Beruf / Ort). Jeder Listeneintrag ist eine Zeile ({N} Zeilen); die Exemplarzahl, "
           f"der Name, der Beruf oder Stand und der Ort stehen wie gedruckt, das Wiederholungszeichen „ wurde als »Herr« aufgelöst; auf S. 835 stehen Name und Beruf in einer "
           f"Spalte und wurden am ersten Komma getrennt (Initialen gehören zum Namen); der vom Transkript auf zwei Zeilen verteilte Eintrag der Hof- und Staatsbibliothek München wurde "
           f"zusammengeführt. Alle sechs Seiten wurden am Faksimile geprüft. Abgeleitet (editorisch) sind: (1) der Ort in der Schreibung des Ortsregisters (S. 826–829; Zusätze wie »bei Gera« "
           f"abgetrennt); (2) die Lage: Landestheil Gera, Schleiz oder Lobenstein-Ebersdorf nach der Seitenzahl des Ortes im Ortsregister (Gera S. 407–569, Schleiz S. 570–705, Lobenstein-Ebersdorf S. 706–825), "
           f"sonst »außerhalb«; (3) die Berufsgruppe: zehn Gruppen für Personen und Firmen nach dem gedruckten Titel (Regeln im Datensatz »classification«, Reihenfolge der Prüfung: Hof, Buchhandel, "
           f"Lehrer, Geistliche, Forst/Berg, Beamte/Juristen, Kaufleute/Gewerbe, Handwerker, Landwirte, übrige), dazu die Gruppe »Behörden, Bibliotheken, Vereine« für Einrichtungen. "
           f"Bei Mehrfachtiteln gilt der erste passende Titel (»Catechet, Oberlehrer« = Lehrer). Aggregate (Einträge = Zeilen, Exemplare = Summe von Expl.) sind in eigenen Datensätzen ausgewiesen."),
    "en": (f"The source is the tables on pp. 835–840 (one block each; columns copies / name / occupation / place). Each list entry is one row ({N} rows); the number of copies, "
           f"the name, the occupation or rank and the place are given as printed, the ditto mark „ is resolved as “Herr”; on p. 835 name and occupation share one column and were "
           f"split at the first comma (initials belong to the name); the entry for the Hof- und Staatsbibliothek in Munich, which the transcript spreads over two rows, was merged. All six pages were "
           f"checked against the facsimile. Derived (editorial) are: (1) the place in the spelling of the Ortsregister (pp. 826–829; qualifiers such as “bei Gera” split off); (2) the location: district of Gera, Schleiz or "
           f"Lobenstein-Ebersdorf according to the page number of the place in the Ortsregister (Gera pp. 407–569, Schleiz pp. 570–705, Lobenstein-Ebersdorf pp. 706–825), otherwise “outside”; "
           f"(3) the occupational group: ten groups for persons and firms by the printed title (rules in the dataset “classification”; order of testing: court, book trade, teachers, clergy, "
           f"forestry/mining, officials/jurists, trade/industry, craftsmen, farmers, others), plus “authorities, libraries, societies” for institutions. Where a title is compound the first matching "
           f"title applies (“Catechet, Oberlehrer” = teacher). Aggregates (entries = rows, copies = sum of Expl.) are given in separate datasets."),
}
findings = [
    {"de": (f"Die Liste umfasst {N} Einträge mit {TOTAL_COPIES} Exemplaren: {n_persons} Personen, {n_firms} Firmen (Buchhandlungen) und {n_inst} Einrichtungen. "
            f"{len(S) - len(multi)} Einträge nehmen genau ein Exemplar ab; mehr als eines bestellen nur {len(multi)}, darunter die Buchhandlung Teich in Lobenstein mit {teich['copies']} "
            f"({dec(pct(teich['copies'], TOTAL_COPIES))} % aller Exemplare) und das Fürstenhaus Reuß j. L. mit {prince_copies_jl}."),
     "en": (f"The list has {N} entries taking {TOTAL_COPIES} copies: {n_persons} persons, {n_firms} firms (booksellers) and {n_inst} institutions. "
            f"{len(S) - len(multi)} entries take exactly one copy; only {len(multi)} order more, among them the bookshop of Teich in Lobenstein with {teich['copies']} "
            f"({fmt1(pct(teich['copies'], TOTAL_COPIES))} % of all copies) and the princely house of Reuss (younger line) with {prince_copies_jl}.")},
    {"de": (f"Die Bestellungen kommen überwiegend aus dem Fürstenthum: {len(inside)} Einträge ({dec(pct(len(inside), N))} %) und {sum(r['copies'] for r in inside)} Exemplare "
            f"({dec(pct(sum(r['copies'] for r in inside), TOTAL_COPIES))} %); {len(outside)} Einträge ({dec(pct(len(outside), N))} %) mit {sum(r['copies'] for r in outside)} Exemplaren "
            f"stammen von außerhalb, {n_book_out} davon von Buchhandlungen (u. a. in Berlin, Dresden, Leipzig, Rudolstadt)."),
     "en": (f"The orders come mostly from within the principality: {len(inside)} entries ({fmt1(pct(len(inside), N))} %) and {sum(r['copies'] for r in inside)} copies "
            f"({fmt1(pct(sum(r['copies'] for r in inside), TOTAL_COPIES))} %); {len(outside)} entries ({fmt1(pct(len(outside), N))} %) with {sum(r['copies'] for r in outside)} copies "
            f"come from outside, {n_book_out} of them from booksellers (in Berlin, Dresden, Leipzig, Rudolstadt, among others).")},
    {"de": (f"Die Besteller sind auf wenige Orte konzentriert: Gera allein {gera} Einträge ({dec(pct(gera, N))} %), mit Untermhaus {gera + untermhaus}; Schleiz {schleiz}, Lobenstein {loben}. "
            f"Zusammen stellen die drei Städte {three_towns} Einträge ({dec(pct(three_towns, N))} %) und {three_towns_c} Exemplare ({dec(pct(three_towns_c, TOTAL_COPIES))} %); {one_entry_places} der {n_places} Orte "
            f"erscheinen nur einmal. Nach Landestheilen: Gera {re_['gera']}, Schleiz {re_['schleiz']}, Lobenstein-Ebersdorf {re_['lobenstein']} Einträge."),
     "en": (f"The subscribers are concentrated in a few places: Gera alone {gera} entries ({fmt1(pct(gera, N))} %), {gera + untermhaus} with Untermhaus; Schleiz {schleiz}, Lobenstein {loben}. "
            f"Together the three towns account for {three_towns} entries ({fmt1(pct(three_towns, N))} %) and {three_towns_c} copies ({fmt1(pct(three_towns_c, TOTAL_COPIES))} %); {one_entry_places} of the {n_places} places "
            f"appear only once. By district: Gera {re_['gera']}, Schleiz {re_['schleiz']}, Lobenstein-Ebersdorf {re_['lobenstein']} entries.")},
    {"de": (f"Größte Gruppe sind die Beamten und Juristen ({ge['officials']} Einträge), vor den Lehrern ({ge['teachers']}), den Kaufleuten und Gewerbetreibenden ({ge['trade']}) und den Buchhandlungen ({ge['booksellers']} Einträge, "
            f"aber {book_c} Exemplare, davon {teich['copies']} von Teich). Geistliche ({ge['clergy']}), Forst- und Bergbeamte ({ge['forestry_mining']}) und Hof ({ge['court']}, {court_c} Exemplare) folgen; "
            f"Landwirte und Gutsverwalter ({ge['farmers']}) und Handwerker ({ge['craftsmen']}) sind zusammen nur {land} Einträge ({dec(pct(land, N))} %). Staats-, Schul- und Kirchendienst (Beamte, Lehrer, Geistliche, Forst/Berg, Hof) "
            f"machen {serving} Einträge ({dec(pct(serving, N))} %) aus."),
     "en": (f"The largest group are officials and jurists ({ge['officials']} entries), ahead of teachers ({ge['teachers']}), merchants and tradesmen ({ge['trade']}) and booksellers ({ge['booksellers']} entries "
            f"but {book_c} copies, {teich['copies']} of them Teich's). Clergy ({ge['clergy']}), forestry and mining staff ({ge['forestry_mining']}) and court ({ge['court']}, {court_c} copies) follow; "
            f"farmers and estate managers ({ge['farmers']}) and craftsmen ({ge['craftsmen']}) together make up only {land} entries ({fmt1(pct(land, N))} %). State, school and church service (officials, teachers, clergy, "
            f"forestry/mining, court) account for {serving} entries ({fmt1(pct(serving, N))} %).")},
]
caveats = [
    {"de": "Eine Subscriptionsliste verzeichnet Vorbestellungen, nicht Leser. Buchhandlungen (darunter die 50 Exemplare von Teich) bestellten vermutlich zum Weiterverkauf, Bibliotheken, Vereine und Behörden für mehrere Nutzer; die Liste sagt deshalb wenig über die Zahl der tatsächlichen Leser und gar nichts über Käufer nach Erscheinen. Ein »Köhler, Fr. Eug., Buchhändler« in Gera, so heißt auch der Verleger (Titelblatt), ist mit einem Exemplar verzeichnet.",
     "en": "A subscription list records advance orders, not readers. Booksellers (including Teich's 50 copies) presumably ordered for resale, libraries, societies and authorities for several users; the list therefore says little about the number of actual readers and nothing about buyers after publication. A “Köhler, Fr. Eug., Buchhändler” at Gera, the name of the publisher (title page), is entered with one copy."},
    {"de": f"Die Gruppenzuordnung folgt allein dem gedruckten Titel und ist eine Setzung: »Catechet« ({cate} Einträge) zählt zu den Geistlichen, »Cantor« zu den Lehrern, »Commerzienrath« zu den Kaufleuten, »Hof-« nur bei Hofdiensten (nicht Hofbuchhandlung, Hofapotheker). Unbestimmte Titel (Director, Dr.) stehen unter »übrige«. Die Rangfolge der drei größten Gruppen ändert sich nicht, wenn die Catecheten zu den Lehrern gezählt werden.",
     "en": f"The group assignment follows the printed title alone and is a convention: “Catechet” ({cate} entries) counts as clergy, “Cantor” as teacher, “Commerzienrath” as merchant, “Hof-” only for court service (not Hofbuchhandlung, Hofapotheker). Unspecific titles (Director, Dr.) go under “others”. The ranking of the three largest groups does not change if the catechists are counted as teachers."},
    {"de": "Orte: Untermhaus wird getrennt von Gera gezählt. »Neuhammer b. Saalburg« (so gedruckt) wurde wie »Neuhammer b. Lobenstein« mit dem einzigen Neuhammer des Ortsregisters (bei Saaldorf, S. 727) gleichgesetzt. Rückersdorf, Wohnort eines Pastors, fehlt im Ortsregister und wird als außerhalb gezählt; Greiz (Reuß ä. L.) und Schloß Greiz gelten als außerhalb des Fürstenthums.",
     "en": "Places: Untermhaus is counted separately from Gera. “Neuhammer b. Saalburg” (as printed) was equated, like “Neuhammer b. Lobenstein”, with the only Neuhammer in the Ortsregister (near Saaldorf, p. 727). Rückersdorf, residence of a pastor, is missing from the Ortsregister and is counted as outside; Greiz (Reuss, older line) and Schloß Greiz count as outside the principality."},
    {"de": f"Sieben Namen waren im Transkript verlesen (Maucke, Meißner, Sieckmann, Voß, Weißker ×3) und ein Ortsname (Weißendorf); sie sind nach dem Faksimile korrigiert. Frauen erscheinen nur als Fürstinnen und als »Amtmännin« ({len(women)} Einträge); {noble} Namen beginnen mit »v.«, ohne dass daraus Adel folgt.",
     "en": f"Seven names had been misread in the transcript (Maucke, Meißner, Sieckmann, Voß, Weißker ×3) and one place name (Weißendorf); they are corrected against the facsimile. Women appear only as princesses and as “Amtmännin” ({len(women)} entries); {noble} names begin with “v.”, which does not by itself imply nobility."},
]

# ------------------------------------------------------------------ charts
def lookup(mapping, idx):
    return "{" + ", ".join(f"'{k}': '{v[idx]}'" for k, v in mapping.items()) + "}"

GROUP_CALC = {"de": lookup(GROUP_LABELS, 0) + "[datum.group]", "en": lookup(GROUP_LABELS, 1) + "[datum.group]"}
REGION_CALC = {"de": lookup(REGION_LABELS, 0) + "[datum.region]", "en": lookup(REGION_LABELS, 1) + "[datum.region]"}
REGION_DOMAIN = [{"de": REGION_LABELS[k][0], "en": REGION_LABELS[k][1]} for k in REGION_ORDER]
MEASURE_CALC = {"de": "datum.measure == 'entries' ? 'Einträge' : 'Exemplare'", "en": "datum.measure == 'entries' ? 'Entries' : 'Copies'"}
MEASURE_DOMAIN = [{"de": "Einträge", "en": "Entries"}, {"de": "Exemplare", "en": "Copies"}]
T_REGION = {"de": "Lage", "en": "Location"}
T_GROUP = {"de": "Gruppe", "en": "Group"}
T_ENTRIES = {"de": "Einträge", "en": "Entries"}
T_COPIES = {"de": "Exemplare", "en": "Copies"}

c1 = {
    "height": 280,
    "transform": [{"filter": "datum.entries >= 4"}, {"calculate": REGION_CALC, "as": "region_label"}],
    "mark": "bar",
    "encoding": {
        "y": {"field": "place", "type": "nominal", "sort": "-x", "title": None},
        "x": {"field": "entries", "type": "quantitative", "title": {"de": "Einträge in der Liste", "en": "Entries in the list"}},
        "color": {"field": "region_label", "type": "nominal", "scale": {"domain": REGION_DOMAIN}, "title": T_REGION,
                  "legend": {"values": REGION_DOMAIN[:3], "labelLimit": 240, "titleLimit": 240}},
        "tooltip": [{"field": "place", "title": {"de": "Ort", "en": "Place"}}, {"field": "region_label", "title": T_REGION},
                    {"field": "entries", "title": T_ENTRIES}, {"field": "copies", "title": T_COPIES}],
    },
}


def grouped(cat_field, cat_calc_as, cat_title, calc, order_field, height, label_limit=None):
    axis = {"labelLimit": label_limit} if label_limit else {}
    return {
        "height": height,
        "transform": [{"calculate": calc, "as": cat_calc_as},
                      {"fold": ["entries", "copies"], "as": ["measure", "count"]},
                      {"calculate": MEASURE_CALC, "as": "measure_label"}],
        "mark": "bar",
        "encoding": {
            "y": {"field": cat_calc_as, "type": "nominal", "sort": {"field": order_field, "op": "min"}, "title": None, "axis": axis},
            "yOffset": {"field": "measure_label", "type": "nominal", "sort": MEASURE_DOMAIN},
            "x": {"field": "count", "type": "quantitative", "title": {"de": "Anzahl", "en": "Number"}},
            "color": {"field": "measure_label", "type": "nominal", "scale": {"domain": MEASURE_DOMAIN}, "title": {"de": "Maß", "en": "Measure"}},
            "tooltip": [{"field": cat_calc_as, "title": cat_title}, {"field": "measure_label", "title": {"de": "Maß", "en": "Measure"}},
                        {"field": "count", "title": {"de": "Anzahl", "en": "Number"}}],
        },
    }


c4 = {
    "height": 330,
    "transform": [{"calculate": GROUP_CALC, "as": "group_label"}, {"calculate": REGION_CALC, "as": "region_label"}],
    "mark": "rect",
    "encoding": {
        "x": {"field": "region_label", "type": "nominal", "sort": {"field": "region_order", "op": "min"}, "title": None,
              "axis": {"labelAngle": 0, "labelLimit": 300}},
        "y": {"field": "group_label", "type": "nominal", "sort": {"field": "group_order", "op": "min"}, "title": None, "axis": {"labelLimit": 400}},
        "color": {"field": "entries", "type": "quantitative", "title": T_ENTRIES},
        "tooltip": [{"field": "group_label", "title": T_GROUP}, {"field": "region_label", "title": T_REGION},
                    {"field": "entries", "title": T_ENTRIES}, {"field": "copies", "title": T_COPIES}],
    },
}

charts = [
    {"id": "c1", "dataset": "by_place",
     "title": {"de": "Orte mit mindestens vier Einträgen", "en": "Places with at least four entries"},
     "caption": {"de": f"Anzahl der Listeneinträge je Ort (ohne Exemplarzahl), nach Lage des Ortes gefärbt. Gera, Schleiz und Lobenstein stellen zusammen {three_towns} von {N} Einträgen; Osterstein ist das Schloß der Fürstenfamilie.",
                 "en": f"Number of list entries per place (not weighted by copies), coloured by location. Gera, Schleiz and Lobenstein together account for {three_towns} of {N} entries; Osterstein is the princely family's castle."},
     "vegalite": c1},
    {"id": "c2", "dataset": "by_group",
     "title": {"de": "Berufsgruppen der Subskribenten", "en": "Occupational groups of the subscribers"},
     "caption": {"de": f"Einträge und Exemplare je Gruppe, sortiert nach Einträgen. Bei den Buchhandlungen liegen die Exemplare weit über den Einträgen (Teich: {teich['copies']}), ebenso beim Hof.",
                 "en": f"Entries and copies per group, sorted by entries. For booksellers the copies far exceed the entries (Teich: {teich['copies']}), as for the court."},
     "vegalite": grouped("group", "group_label", T_GROUP, GROUP_CALC, "order", 400, 280)},
    {"id": "c3", "dataset": "by_region",
     "title": {"de": "Innerhalb und außerhalb des Fürstenthums", "en": "Inside and outside the principality"},
     "caption": {"de": f"Einträge und Exemplare nach Landestheil; außerhalb: {len(outside)} Einträge mit {sum(r['copies'] for r in outside)} Exemplaren.",
                 "en": f"Entries and copies by district; outside: {len(outside)} entries with {sum(r['copies'] for r in outside)} copies."},
     "vegalite": grouped("region", "region_label", T_REGION, REGION_CALC, "order", 260, 260)},
    {"id": "c4", "dataset": "group_region",
     "title": {"de": "Berufsgruppen nach Lage", "en": "Occupational groups by location"},
     "caption": {"de": "Anzahl der Einträge je Gruppe und Lage (Zahlenwerte im Tooltip und in der Datentabelle). Beamte, Lehrer und Kaufleute sind in allen drei Landestheilen vertreten; Buchhandlungen überwiegend außerhalb.",
                 "en": "Number of entries per group and location (values in the tooltip and the data table). Officials, teachers and merchants occur in all three districts; booksellers mostly outside."},
     "vegalite": c4},
]

# ------------------------------------------------------------------ datasets
def cols(spec):
    out = []
    for n, lde, len_, t, u, der, note in spec:
        c = {"name": n, "label": {"de": lde, "en": len_}, "type": t, "unit": u}
        if der:
            c["derived"] = True
        if note:
            c["note"] = note
        out.append(c)
    return out


blocks = [("835", "b3", "r2-r25"), ("836", "b1", "r2-r49"), ("837", "b1", "r2-r51"), ("838", "b1", "r2-r48"), ("839", "b1", "r2-r48"), ("840", "b1", "r2-r7")]
refs = [{"page": p, "block": b, "rows": r} for p, b, r in blocks]
datasets = [
    {"name": "subscribers", "title": {"de": "Subskribenten (ein Eintrag je Zeile)", "en": "Subscribers (one entry per row)"},
     "columns": cols(sub_cols), "rows": sub_rows, "source_refs": refs},
    {"name": "by_place", "title": {"de": "Einträge und Exemplare je Ort", "en": "Entries and copies per place"},
     "columns": cols([("place", "Ort", "Place", "string", None, True, None), ("region", "Lage", "Location", "string", None, True, None),
                      ("entries", "Einträge", "Entries", "integer", None, True, None), ("copies", "Exemplare", "Copies", "integer", None, True, None)]),
     "rows": place_rows, "source_refs": refs},
    {"name": "by_group", "title": {"de": "Einträge und Exemplare je Gruppe", "en": "Entries and copies per group"},
     "columns": cols([("group", "Gruppe", "Group", "string", None, True, None), ("order", "Rang", "Rank", "integer", None, True, "Rang nach Einträgen"),
                      ("entries", "Einträge", "Entries", "integer", None, True, None), ("copies", "Exemplare", "Copies", "integer", None, True, None)]),
     "rows": group_rows, "source_refs": refs},
    {"name": "by_region", "title": {"de": "Einträge und Exemplare je Lage", "en": "Entries and copies per location"},
     "columns": cols([("region", "Lage", "Location", "string", None, True, None), ("order", "Reihenfolge", "Order", "integer", None, True, None),
                      ("entries", "Einträge", "Entries", "integer", None, True, None), ("copies", "Exemplare", "Copies", "integer", None, True, None)]),
     "rows": region_rows, "source_refs": refs},
    {"name": "group_region", "title": {"de": "Gruppe × Lage", "en": "Group × location"},
     "columns": cols([("group", "Gruppe", "Group", "string", None, True, None), ("group_order", "Rang der Gruppe", "Group rank", "integer", None, True, None),
                      ("region", "Lage", "Location", "string", None, True, None), ("region_order", "Reihenfolge der Lage", "Location order", "integer", None, True, None),
                      ("entries", "Einträge", "Entries", "integer", None, True, None), ("copies", "Exemplare", "Copies", "integer", None, True, None)]),
     "rows": gr_rows, "source_refs": refs},
    {"name": "classification", "title": {"de": "Zuordnung der gedruckten Titel zu Gruppen", "en": "Assignment of printed titles to groups"},
     "columns": cols([("group", "Gruppe", "Group", "string", None, True, None), ("occupation_printed", "Beruf/Stand (gedruckt)", "Occupation/rank (as printed)", "string", None, False, None),
                      ("entries", "Einträge", "Entries", "integer", None, True, None), ("copies", "Exemplare", "Copies", "integer", None, True, None)]),
     "rows": cb_rows, "source_refs": refs},
]

# transcription issues (facsimile-confirmed name corrections)
issues = []
for (page, row), (field, was, now) in FACSIMILE_FIXES.items():
    issues.append({"page": page, "block": "b1", "cell": f"{row}c{3 if field == 'name' else 5}", "transcribed": was, "facsimile": now, "checked_facsimile": True,
                   "note": "Fraktur: " + {"Mauke, Rich.": "ck-Ligatur", "Meissner": "ß statt ss", "Weissendorf.": "ß statt ss", "Siekmann": "ck-Ligatur",
                                         "v. Boss": "Fraktur-V (wie in Volckmar, Vogel) als B gelesen", "Weissker": "ß statt ss"}[was]})

ana = {
    "id": "subskribenten-leserschaft-1870",
    "title": title, "category": "reception", "section": "subscribenten",
    "sources": [{"page": "835", "block": "b2"}] + refs,
    "summary": summary, "method": method, "findings": findings, "caveats": caveats,
    "datasets": datasets, "charts": charts, "transcription_issues": issues,
    "keywords": {"de": ["Subskribenten", "Subscriptionsliste", "Leserschaft", "Rezeption", "Buchhandlungen", "Lehrer", "Geistliche", "Beamte", "Gera", "Schleiz", "Lobenstein", "Exemplare"],
                 "en": ["subscribers", "subscription list", "readership", "reception", "booksellers", "teachers", "clergy", "officials", "Gera", "Schleiz", "Lobenstein", "copies"]},
    "generated_by": "Claude Sonnet 5.5 (subagent B01)", "date": "2026-10-01",
}
print(write_analysis(ana))
