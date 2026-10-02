"""Analysis: arrival of migrant birds (p. 86) and rare migrants shot near Schleiz and Gera (pp. 85-86, with p. 831)."""
from collections import Counter
from common import *

t86 = re.sub(r"\s+", " ", text("86", "b2"))
t85 = re.sub(r"\s+", " ", text("85", "b3"))
t86b1 = re.sub(r"\s+", " ", text("86", "b1"))

# ------------------------------------------------------------------ arrival calendar (Gera area), p.86 b2
need("Feldlerchen, Staare, Singdrosseln, Kiebitze, Buchfinken und Heidelerchen", "86", "b2")
need("Rothkehlchen, weiße Bachstelzen, Waldschnepfen, Holztauben und Hausrothschwänzchen", "86", "b2")
need("Steinschmätzer, Hausschwalben, Fitislaubvogel, Gartenrothschwänzchen, Waldlaubvögel, Wiedehopfe, Wiesenpieper, Teich- und Wasserhuhne", "86", "b2")
need("Kukuk, Mauerschwalben, Gartengrasmücken, Pirol, Mehl- und Nachtschwalben, Fliegenschnapper, Wachteln und Wasserrallen", "86", "b2")
MONTHS = {2: ("Februar", "February"), 3: ("März", "March"), 4: ("April", "April"), 5: ("Mai", "May")}
# (month, name as printed (singular form where printed as plural), English where certain)
ARR = [
    (2, "Feldlerche", "Skylark"), (2, "Staar", "Starling"), (2, "Singdrossel", "Song thrush"), (2, "Kiebitz", "Lapwing"),
    (2, "Buchfink", "Chaffinch"), (2, "Heidelerche", "Woodlark"),
    (3, "Rothkehlchen", "Robin"), (3, "weiße Bachstelze", "White wagtail"), (3, "Waldschnepfe", "Woodcock"),
    (3, "Holztaube", None), (3, "Hausrothschwänzchen", "Black redstart"),
    (4, "Steinschmätzer", None), (4, "Hausschwalbe", None), (4, "Fitislaubvogel", "Willow warbler"),
    (4, "Gartenrothschwänzchen", "Common redstart"), (4, "Waldlaubvogel", "Wood warbler"), (4, "Wiedehopf", "Hoopoe"),
    (4, "Wiesenpieper", "Meadow pipit"), (4, "Teichhuhn", "Moorhen"), (4, "Wasserhuhn", None),
    (5, "Kukuk", "Cuckoo"), (5, "Mauerschwalbe", None), (5, "Gartengrasmücke", "Garden warbler"), (5, "Pirol", "Golden oriole"),
    (5, "Mehlschwalbe", None), (5, "Nachtschwalbe", None), (5, "Fliegenschnapper", None), (5, "Wachtel", "Quail"),
    (5, "Wasserralle", "Water rail"),
]
cnt = Counter(m for m, _, _ in ARR)
arr_rows = []
rank = Counter()
for m, nm, en_ in ARR:
    rank[m] += 1
    arr_rows.append([m, MONTHS[m][0], MONTHS[m][1], f"{MONTHS[m][0]} ({cnt[m]})", f"{MONTHS[m][1]} ({cnt[m]})", nm, en_, rank[m], "86", "b2"])
print("arrival counts", dict(cnt), len(ARR))
n_arr = len(ARR)
need("bis Mitte November", "86", "b2")
need("ein bis zwei Wochen später", "86", "b2")

# ------------------------------------------------------------------ rare migrants, pp.85-86 (+ p.831)
G = {"R": ("Raubvögel und Eulen", "Birds of prey and owls"), "S": ("Singvögel", "Songbirds"), "K": ("Krähenartige", "Crow family"),
     "H": ("Hühnerartige", "Gamebirds"), "P": ("Spechtartige", "Woodpeckers"), "W": ("Sumpf- und Wasservögel", "Marsh and water birds")}
ENUMS = [  # (printed enumeration, block, group, expanded names)
    ("Stein-, Schrei- und Flußadler", "85", "b3", "R", ["Steinadler", "Schreiadler", "Flußadler"]),
    ("der rothe Milan", "85", "b3", "R", ["rother Milan"]),
    ("Schilf-, Korn- und Rostweihe", "85", "b3", "R", ["Schilfweihe", "Kornweihe", "Rostweihe"]),
    ("schwarzbraune Rauchfußbussard", "85", "b3", "R", ["schwarzbrauner Rauchfußbussard"]),
    ("Wander-, Merlin-, Lerchen-, Würg- und rothfüßige Falke", "85", "b3", "R", ["Wanderfalke", "Merlinfalke", "Lerchenfalke", "Würgfalke", "rothfüßiger Falke"]),
    ("Sumpf-, Zwerg- und große Ohreule", "85", "b3", "R", ["Sumpfohreule", "Zwergohreule", "große Ohreule"]),
    ("Habichts-, Sperlings-, Zwerg- und Sperbereule", "85", "b3", "R", ["Habichtseule", "Sperlingseule", "Zwergeule", "Sperbereule"]),
    ("Citronenfink, Grau-, Schnee-, Zipp-, Rohr- und Zaunammer", "85", "b3", "S", ["Citronenfink", "Grauammer", "Schneeammer", "Zippammer", "Rohrammer", "Zaunammer"]),
    ("die Rothdrossel, der Seidenschwanz, Wasserschwätzer, Sprosser", "85", "b3", "S", ["Rothdrossel", "Seidenschwanz", "Wasserschwätzer", "Sprosser"]),
    ("Fitislaubvogel, Schilfrohrsänger, die Braunelle, Haubenmeise, Nachtschwalbe und das Schwarzkehlchen", "86", "b1", "S",
     ["Fitislaubvogel", "Schilfrohrsänger", "Braunelle", "Haubenmeise", "Nachtschwalbe", "Schwarzkehlchen"]),
    ("der Kolkrabe, der Tannenheher, der kleine graue Heher, der rothköpfige und rothrückige Würger", "86", "b1", "K",
     ["Kolkrabe", "Tannenheher", "kleiner grauer Heher", "rothköpfiger Würger", "rothrückiger Würger"]),
    ("der große Trappe", "86", "b1", "H", ["große Trappe"]),
    ("der Schwarz-, Grau- und Weißpecht", "86", "b1", "P", ["Schwarzspecht", "Grauspecht", "Weißspecht"]),
    ("der Fischreiher, die große und kleine Rohrdommel, der schwarze Storch", "86", "b1", "W", ["Fischreiher", "große Rohrdommel", "kleine Rohrdommel", "schwarzer Storch"]),
    ("die Moor- und kleine Pfulschnepfe, der vielfarbige Kampfläufer", "86", "b1", "W", ["Moorschnepfe", "kleine Pfulschnepfe", "vielfarbiger Kampfläufer"]),
    ("der Alpen-, Meer- und kleine Strandläufer, der Bruch- und Teichwasserläufer", "86", "b1", "W", ["Alpenstrandläufer", "Meerstrandläufer", "kleiner Strandläufer", "Bruchwasserläufer", "Teichwasserläufer"]),
    ("der Gold- und Küstenregenpfeifer, der kleine Strandpfeifer, graue Sonderling, europäische Austernfischer", "86", "b1", "W",
     ["Goldregenpfeifer", "Küstenregenpfeifer", "kleiner Strandpfeifer", "grauer Sonderling", "europäischer Austernfischer"]),
    ("Ohrentaucher, große und kleine Lappentaucher, Eis- und rothkehlige Taucher", "86", "b1", "W",
     ["Ohrentaucher", "große Lappentaucher", "kleine Lappentaucher", "Eistaucher", "rothkehliger Taucher"]),
    ("Gänsesäger, weiße und große Säger, die Saat- und Ackergans", "86", "b1", "W", ["Gänsesäger", "weißer Säger", "großer Säger", "Saatgans", "Ackergans"]),
    ("Eis-, Pfeif-, Tafel-, Knäck-, Berg-, Reiher-, Schall-, Spieß- und Sammtente", "86", "b1", "W",
     ["Eisente", "Pfeifente", "Tafelente", "Knäckente", "Bergente", "Reiherente", "Schallente", "Spießente", "Sammtente"]),
]
for enum, pg, bk, g, names in ENUMS:
    need(enum, pg, bk)
# p.831 (Brückner's corrections): five species are not rare; Schallente -> Schellente
FLAG = {"rothrückiger Würger": "sehr gemein", "Grauammer": "häufig", "kleiner Strandpfeifer": "häufig", "Nachtschwalbe": "häufig",
        "schwarzbrauner Rauchfußbussard": "nicht selten"}
for k in ("rothrückige Würger", "Grauammer", "kleine Strandpfeifer", "Nachtschwalbe", "schwarzbraune Rauchfußbussard"):
    pass
need("sehr gemein der rothrückige Würger, häufig die Grauammer, der kleine Strandpfeifer und die Nachtschwalbe und nicht selten der schwarzbraune Rauchfußbussard", "831", "b2")
need("lies: Schellente statt Schallente", "831", "b3")
# contradictions inside the book (editorial cross-check): same bird called common / regular elsewhere
CROSS = {
    "Flußadler": ("85", "b2", "häufig (Raubvögel: »Flußadler (schon im Juli vorkommend)«)", "Sperber, Mäusebussard, Flußadler"),
    "Rothdrossel": ("84", "b1", "häufig oder nicht selten (»Rothdrosseln (auf dem Zuge)«)", "Rothdrosseln (auf dem Zuge)"),
    "Seidenschwanz": ("84", "b1", "häufig oder nicht selten in beiden Gebieten", "Seidenschwanz,"),
    "Wasserschwätzer": ("84", "b1", "häufiger im Oberland als im Unterland", "Wasserschwätzer"),
    "Rohrammer": ("84", "b1", "nicht selten im Unterland; seit fünf Jahren in den Teichstrichen des Oberlandes eingezogen", "Rohrammer"),
    "Fitislaubvogel": ("86", "b2", "April-Ankömmling im Gebiet Gera (Zugvogel)", "Fitislaubvogel"),
}
for nm, (pg, bk, ph, probe) in CROSS.items():
    need(probe, pg, bk)
STATUS = {
    "none": (1, "als selten verzeichnet", "listed as rare"),
    "p831": (2, "nach S. 831 nicht selten", "not rare according to p. 831"),
    "cross": (3, "sonst im Text als häufig genannt", "elsewhere called common"),
}
rv_rows = []
for enum, pg, bk, g, names in ENUMS:
    for nm in names:
        corr = None
        stt = "none"
        cname = nm
        if nm in FLAG:
            stt = "p831"
            corr = f"S. 831: {FLAG[nm]}"
        elif nm in CROSS:
            stt = "cross"
            corr = None
        if nm == "Schallente":
            cname = "Schellente"
            corr = "S. 831: »lies: Schellente statt Schallente«"
        cr = CROSS.get(nm)
        rv_rows.append([G[g][0], G[g][1], nm, cname, STATUS[stt][0], STATUS[stt][1], STATUS[stt][2], corr,
                        f"S. {cr[0]}: {cr[2]}" if cr and stt == "cross" else None, pg, bk])
n_rv = len(rv_rows)
cg = Counter(r[0] for r in rv_rows)
print(n_rv, dict(cg))
n_flag = sum(1 for r in rv_rows if r[4] == 2)
n_cross = sum(1 for r in rv_rows if r[4] == 3)
n_water = cg[G["W"][0]]
n_rap = cg[G["R"][0]]
print(n_flag, n_cross)
pc = lambda a, b: 100 * a / b

ana = {
    "id": "fauna-voegel-zugzeiten-und-seltene-gaeste",
    "title": bi("Zugvögel: Ankunft im Frühjahr und seltene Gäste", "Migratory birds: spring arrival and rare visitors"),
    "category": "fauna",
    "section": "t1-1-9",
    "sources": [{"page": "86", "block": "b2"}, {"page": "85", "block": "b3"}, {"page": "86", "block": "b1"}, {"page": "831", "block": "b2"}, {"page": "831", "block": "b3"},
                {"page": "85", "block": "b2"}, {"page": "84", "block": "b1"}],
    "summary": bi(
        f"Brückner nennt für den Raum Gera die Ankunftsmonate von {n_arr} Zugvögeln im Frühjahr (Februar bis Mai) und zählt {n_rv} seltene Zug- und Strichvögel auf, die um Schleiz und Gera geschossen wurden. Die Diagramme zeigen den Frühjahrszug als Kalender und die seltenen Gäste nach Vogelgruppe; die Berichtigungen von S. 831 stellen fünf der »seltenen« Arten als häufig richtig.",
        f"For the Gera area Brückner names the arrival months of {n_arr} migratory birds in spring (February to May) and lists {n_rv} rare migrants and wanderers shot near Schleiz and Gera. The charts show the spring passage as a calendar and the rare visitors by bird group; the corrections of p. 831 set five of the “rare” species straight as common."),
    "method": bi(
        f"Die Reihungen auf S. 86 (Ankunft) und S. 85–86 (seltene Arten) wurden in Einzelnennungen aufgelöst (»Mehl- und Nachtschwalben« = zwei Nennungen); die Gruppen (Raubvögel und Eulen, Singvögel, Krähenartige, Hühnerartige, Spechtartige, Sumpf- und Wasservögel) folgen Brückners Überschriften. Als Quelle der Liste nennt S. 831 das Verzeichnis im 3. Jahresbericht der Gesellschaft von Freunden der Naturwissenschaften (Gera), S. 66. Die Berichtigungen von S. 831 (fünf als häufig oder nicht selten bezeichnete Arten, Schellente statt Schallente) sind eingetragen. Zusätzlich wurde die Liste mit den Häufigkeitsangaben von S. 84–86 verglichen (redaktioneller Abgleich, abgeleitet): {n_cross} Arten, die als selten aufgeführt sind, werden dort ausdrücklich als häufig oder als regelmäßige Zugvögel genannt. Die Monatszahl (2–5) ist eine redaktionelle Kodierung der Monatsnamen; englische Namen stehen nur, wo die Zuordnung sicher ist.",
        f"The sequences on p. 86 (arrival) and pp. 85–86 (rare species) were resolved into single entries (“Mehl- und Nachtschwalben” = two entries); the groups (birds of prey and owls, songbirds, crow family, gamebirds, woodpeckers, marsh and water birds) follow Brückner's headings. As the source of the list p. 831 names the list in the 3rd annual report of the Society of Friends of Natural Sciences (Gera), p. 66. The corrections of p. 831 (five species described as common or not rare, Schellente instead of Schallente) are entered. In addition the list was compared with the frequency statements on pp. 84–86 (editorial cross-check, derived): {n_cross} species listed as rare are explicitly called common or regular migrants there. The month number (2–5) is an editorial coding of the month names; English names are given only where the identification is certain."),
    "findings": [
        bi(f"Der Zug im Raum Gera beginnt im Februar mit {cnt[2]} Arten (Feldlerche, Star, Singdrossel, Kiebitz, Buchfink, Heidelerche); im März folgen {cnt[3]}, im April {cnt[4]} und im Mai {cnt[5]} Arten. Der Abzug fällt in die Zeit von Mitte August bis Mitte November; im höher gelegenen Oberland kehren die Vögel ein bis zwei Wochen später zurück.",
           f"In the Gera area the passage begins in February with {cnt[2]} species (skylark, starling, song thrush, lapwing, chaffinch, woodlark); {cnt[3]} follow in March, {cnt[4]} in April and {cnt[5]} in May. Departure falls between mid-August and mid-November; in the higher Oberland the birds return one to two weeks later."),
        bi(f"Von den {n_rv} seltenen Gästen sind {n_water} Sumpf- und Wasservögel ({de(pc(n_water, n_rv), 0)} %, darunter neun Entenarten) und {n_rap} Raubvögel und Eulen ({de(pc(n_rap, n_rv), 0)} %). Brückner bemerkt, dass Flüsse und Teiche zur Zugzeit von Wasservögeln aufgesucht, aber kaum als Brutplätze gewählt werden (S. 85).",
           f"Of the {n_rv} rare visitors {n_water} are marsh and water birds ({en(pc(n_water, n_rv), 0)} %, among them nine species of duck) and {n_rap} are birds of prey and owls ({en(pc(n_rap, n_rv), 0)} %). Brückner remarks that rivers and ponds are visited by water birds at passage time but hardly chosen as breeding places (p. 85)."),
        bi(f"Brückner selbst korrigiert auf S. 831 fünf Arten der Liste (rothrückiger Würger, Grauammer, kleiner Strandpfeifer, Nachtschwalbe, schwarzbrauner Rauchfußbussard) als häufig bis nicht selten. Weitere {n_cross} Arten (Flußadler, Rothdrossel, Seidenschwanz, Wasserschwätzer, Rohrammer, Fitislaubvogel) werden in seinem Text sonst als häufig oder regelmäßig bezeichnet; das deutet darauf hin, dass die Liste des Vereins geschossene Zugvögel und nicht nur tatsächlich seltene Arten umfasst.",
           f"On p. 831 Brückner himself corrects five species of the list (rothrückiger Würger, Grauammer, kleiner Strandpfeifer, Nachtschwalbe, schwarzbrauner Rauchfußbussard) as common to not rare. Another {n_cross} species (Flußadler, Rothdrossel, Seidenschwanz, Wasserschwätzer, Rohrammer, Fitislaubvogel) are elsewhere in his text called common or regular; this suggests that the society's list comprises migrants that were shot, not only species that are really rare."),
    ],
    "caveats": [
        bi("»Ankunft« gilt für den Landesteil Gera; Brückner gibt keine Jahre oder Tage an und weist darauf hin, dass der Eintritt von Jahr zu Jahr um wenige Tage bis zu einem Monat schwankt. Für Wasserhuhn, Holztaube, Mauerschwalbe und Hausschwalbe ist die moderne Zuordnung nicht sicher.",
           "“Arrival” applies to the Gera district; Brückner gives no years or days and notes that the arrival varies from year to year by a few days to a month. For Wasserhuhn, Holztaube, Mauerschwalbe and Hausschwalbe the modern identification is not certain."),
        bi("Der Abgleich der »seltenen« Arten mit den Häufigkeitsangaben auf S. 84–86 ist ein redaktioneller Vergleich gleichlautender Namen; er sagt nichts darüber, welche Angabe zutrifft. Mehrfachnennungen sind möglich, wenn Brückner mit einem Namen verschiedene Arten bezeichnet.",
           "The comparison of the “rare” species with the frequency statements on pp. 84–86 is an editorial comparison of identical names; it does not say which statement is correct. Double counting is possible where Brückner uses one name for different species."),
        bi("Die Namen sind Brückners Namen (nicht modernisiert); »Schallente« ist nach S. 831 als Schellente zu lesen. Die Liste folgt dem Verzeichnis eines Vereins (3. Jahresbericht) und gibt geschossene Vögel wieder, nicht Beobachtungen.",
           "The names are Brückner's (not modernised); “Schallente” is to be read as Schellente according to p. 831. The list follows a society's register (3rd annual report) and records shot birds, not observations."),
    ],
    "datasets": [
        {"name": "arrival",
         "title": bi("Ankunft der Zugvögel im Raum Gera (S. 86)", "Arrival of migratory birds in the Gera area (p. 86)"),
         "columns": [
             col("month", "Monat (Nummer)", "Month (number)", "integer", None, True, "redaktionelle Kodierung der Monatsnamen"),
             col("month_de", "Monat", "Month", "string", None),
             col("month_en", "Monat (EN)", "Month (EN)", "string", None, True),
             col("month_axis_de", "Monat mit Artenzahl", "Month with number of species", "string", None, True),
             col("month_axis_en", "Monat mit Artenzahl (EN)", "Month with number of species (EN)", "string", None, True),
             col("bird", "Vogel (Druck, Einzelform)", "Bird (print, singular)", "string", None),
             col("bird_en", "Englischer Name", "English name", "string", None, True),
             col("rank", "Reihenfolge im Monat", "Order within the month", "integer", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": arr_rows, "source_refs": [{"page": "86", "block": "b2"}]},
        {"name": "rare_visitors",
         "title": bi("Seltene Zug- und Strichvögel um Schleiz und Gera (S. 85–86, 831)", "Rare migrants and wanderers near Schleiz and Gera (pp. 85–86, 831)"),
         "columns": [
             col("group_de", "Gruppe", "Group", "string", None),
             col("group_en", "Gruppe (EN)", "Group (EN)", "string", None, True),
             col("bird", "Vogel (Druck, aufgelöst)", "Bird (print, resolved)", "string", None),
             col("bird_corrected", "Vogel (nach S. 831)", "Bird (after p. 831)", "string", None),
             col("status_order", "Stufe (Reihenfolge)", "Level (order)", "integer", None, True),
             col("status_de", "Einstufung", "Classification", "string", None, True),
             col("status_en", "Einstufung (EN)", "Classification (EN)", "string", None, True),
             col("correction", "Berichtigung (S. 831)", "Correction (p. 831)", "string", None),
             col("cross_check", "Abgleich mit S. 84–86", "Comparison with pp. 84–86", "string", None, True),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": rv_rows, "source_refs": [{"page": "85", "block": "b3"}, {"page": "86", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "arrival",
         "title": bi("Frühjahrszug: Ankunftsmonate im Raum Gera", "Spring passage: arrival months in the Gera area"),
         "caption": bi("Brückners Ankunftskalender der Zugvögel für den Landesteil Gera (S. 86), nach Monat geordnet. Im höher gelegenen Oberland kehren die Vögel ein bis zwei Wochen später zurück.",
                       "Brückner's arrival calendar of migratory birds for the Gera district (p. 86), ordered by month. In the higher Oberland the birds return one to two weeks later."),
         "vegalite": {"height": 230,
                      "mark": {"type": "text", "fontSize": 12},
                      "encoding": {
                          "x": {"field": {"de": "month_axis_de", "en": "month_axis_en"}, "type": "nominal", "title": None, "axis": {"labelAngle": 0, "orient": "top"},
                                "sort": {"field": "month", "op": "min"}},
                          "y": {"field": "rank", "type": "quantitative", "axis": None, "scale": {"reverse": True, "domain": [0.5, 9.5]}},
                          "text": {"field": "bird", "type": "nominal"},
                          "tooltip": [{"field": "bird", "title": bi("Vogel", "Bird")},
                                      {"field": "bird_en", "title": bi("Englischer Name", "English name")},
                                      {"field": {"de": "month_de", "en": "month_en"}, "title": bi("Ankunft", "Arrival")}]}}},
        {"id": "c2", "dataset": "rare_visitors",
         "title": bi("Seltene Zug- und Strichvögel um Schleiz und Gera", "Rare migrants and wanderers near Schleiz and Gera"),
         "caption": bi(f"{n_rv} namentlich aufgeführte Arten nach Vogelgruppe. Nach Brückners Berichtigung (S. 831) sind {n_flag} der Arten nicht selten; weitere {n_cross} sind in seinem Text an anderer Stelle als häufig oder regelmäßig bezeichnet.",
                       f"{n_rv} species named, by bird group. According to Brückner's correction (p. 831) {n_flag} of the species are not rare; another {n_cross} are called common or regular elsewhere in his text."),
         "vegalite": {"height": 260, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "group_de", "en": "group_en"}, "type": "nominal", "sort": "-x", "title": None, "axis": {"labelLimit": 220}},
                          "x": {"aggregate": "count", "type": "quantitative", "title": bi("Arten", "Species")},
                          "color": {"field": {"de": "status_de", "en": "status_en"}, "type": "nominal", "title": bi("Einstufung", "Classification"), "legend": {"columns": 1, "labelLimit": 360},
                                    "scale": {"domain": [{"de": STATUS[k][1], "en": STATUS[k][2]} for k in ("none", "p831", "cross")]}},
                          "order": {"field": "status_order", "type": "quantitative", "sort": "descending"},
                          "tooltip": [{"field": {"de": "group_de", "en": "group_en"}, "title": bi("Gruppe", "Group")},
                                      {"field": {"de": "status_de", "en": "status_en"}, "title": bi("Einstufung", "Classification")},
                                      {"aggregate": "count", "title": bi("Arten", "Species")}]}}},
    ],
    "transcription_issues": [],
    "keywords": {"de": ["Zugvögel", "Vogelzug", "Ankunft", "Frühjahr", "seltene Vögel", "Wasservögel", "Raubvögel", "Gera", "Schleiz", "Kuckuck", "Feldlerche"],
                 "en": ["migratory birds", "bird migration", "arrival", "spring", "rare birds", "water birds", "birds of prey", "Gera", "Schleiz", "cuckoo", "skylark"]},
    "related": ["fauna-voegel-unterland-oberland", "fauna-aenderungen-seit-1647"],
    "generated_by": GEN,
    "date": DATE,
}
del ana["transcription_issues"]
write(ana)
