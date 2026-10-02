"""Analysis: species found only in the Unterland / only in the Oberland (pp. 72-74), with Brückner's corrections (p. 830)."""
from collections import Counter
from common import *
from flora_lists import (unterland, oberland, FAMILY, MONOCOT_FAMILIES, DELETE_UL, ADD_UL, ADD_OL, SPELLING)

ul, ol = unterland(), oberland()
REG = {"UL": ("Nur im Unterland", "Unterland only"), "OL": ("Nur im Oberland", "Oberland only")}
ST = {"printed": ("im Druck, bleibt", "in print, stands"), "deleted": ("nach S. 830 gestrichen", "deleted according to p. 830"),
      "added": ("nach S. 830 ergänzt", "added according to p. 830"), "duplicate": ("Dublette (S. 73 und 74)", "duplicate (pp. 73 and 74)")}
n_ul_print, n_ol_print = len(ul), len(ol)
dist_ol_print = len({r["name"] for r in ol})
assert (n_ul_print, n_ol_print, dist_ol_print) == (95, 113, 112)
assert not ({r["name"] for r in ul} & {r["name"] for r in ol})

rows = []
seen_ol = set()
for r in ul + ol:
    fam = FAMILY[r["genus"]]
    mono = fam in MONOCOT_FAMILIES
    status, corr = "printed", None
    if r["region"] == "UL" and r["name"] in DELETE_UL:
        status = "deleted"
        corr = "S. 830: zu streichen, weil die Art auch im Oberland vorkommt" + (" (Z. 15 v. u.)" if r["name"] == "Laserpitium pruthenicum" else " (Z. 19/22 v. o.)")
    if r["region"] == "OL":
        if r["name"] in seen_ol:
            status = "duplicate"
        seen_ol.add(r["name"])
    note = r["note"]
    doubt = "ja" if r["doubtful"] else None
    if r["name"] == "Nuphar luteum":
        corr = "S. 830: der Stern fällt weg, da Nuphar luteum öfters im Oberland getroffen wird"
    if r["name"] == "Apocynum Venetum":
        corr = "S. 830 (zu S. 75): nach dem Hofgärtner Papst ist das Apocynum von Untermhaus Apocynum Venetum"
    if r["name"] == "Pulicaria dysenterica":
        corr = "Im Druck »Palicaria«; S. 830: lies Pulicaria"
    if r["name"] in SPELLING:
        corr = f"S. 830: lies {SPELLING[r['name']].split()[1]} statt {r['name'].split()[1]}"
    if r["doubtful"] and r["name"] != "Apocynum Venetum" and not note:
        note = "zweifelhaft, obschon als vorkömmlich angegeben (Fußnote)"
    if r["name"] == "Apocynum Venetum":
        note = "im Druck »(zweifelhaft)«"
    rows.append([REG[r["region"]][0], REG[r["region"]][1], r["name"], SPELLING.get(r["name"], r["name"]), r["genus"], fam,
                 "Einkeimblättrige" if mono else "Zweikeimblättrige", "Monocotyledons" if mono else "Dicotyledons",
                 status, ST[status][0], ST[status][1], doubt, note, corr, r["page"], r["block"]])
for nm, gen, pg, bk in ADD_UL + ADD_OL:
    reg = "UL" if (nm, gen, pg, bk) in ADD_UL else "OL"
    fam = FAMILY[gen]
    mono = fam in MONOCOT_FAMILIES
    rows.append([REG[reg][0], REG[reg][1], nm, nm, gen, fam, "Einkeimblättrige" if mono else "Zweikeimblättrige", "Monocotyledons" if mono else "Dicotyledons",
                 "added", ST["added"][0], ST["added"][1], None, None, "S. 830: als eigenthümlich einzutragen" + (" (im Druck »Phyteum«, in Brückners Berichtigung ohne Autor)" if gen == "Phyteum" else ""), pg, bk])

# the corrected lists = everything not deleted and not a duplicate
live = [r for r in rows if r[8] in ("printed", "added")]
ul_live = [r for r in live if r[0] == REG["UL"][0]]
ol_live = [r for r in live if r[0] == REG["OL"][0]]
n_ul, n_ol = len(ul_live), len(ol_live)
print("corrected:", n_ul, n_ol)
assert (n_ul, n_ol) == (93, 114)
fam_ul = Counter(r[5] for r in ul_live)
fam_ol = Counter(r[5] for r in ol_live)
fam_tot = fam_ul + fam_ol
top = [f for f, _ in fam_tot.most_common() if fam_ul[f] >= 4 or fam_ol[f] >= 4]
top.sort(key=lambda f: -(fam_ul[f] + fam_ol[f]))
print(top, len(top))
order = {f: i for i, f in enumerate(top, start=1)}
fam_rows = []
for reg, cnt, tot in (("UL", fam_ul, n_ul), ("OL", fam_ol, n_ol)):
    for f in top:
        fam_rows.append([REG[reg][0], REG[reg][1], f, f, order[f], cnt[f], round(100 * cnt[f] / tot, 1)])
fam_rows.sort(key=lambda r: (r[4], r[0]))
n_other_fams = len([f for f in fam_tot if f not in order])
oth_ul = sum(v for f, v in fam_ul.items() if f not in order)
oth_ol = sum(v for f, v in fam_ol.items() if f not in order)

ast_ul, orch_ul, orch_ol = fam_ul["Asteraceae"], fam_ul["Orchidaceae"], fam_ol["Orchidaceae"]
bras_ol, api_ol, cyp_ol, cyp_ul = fam_ol["Brassicaceae"], fam_ol["Apiaceae"], fam_ol["Cyperaceae"], fam_ul["Cyperaceae"]
mono_ul = sum(r[5] in MONOCOT_FAMILIES for r in ul_live)
mono_ol = sum(r[5] in MONOCOT_FAMILIES for r in ol_live)
mono_ul_p = sum(FAMILY[r["genus"]] in MONOCOT_FAMILIES for r in ul)
mono_ol_p = sum(FAMILY[r["genus"]] in MONOCOT_FAMILIES for r in ol)
doubt_print = [r for r in ul + ol if r["doubtful"]]
doubt_left = [r for r in doubt_print if r["name"] not in ("Apocynum Venetum", "Nuphar luteum")]
print(ast_ul, orch_ul, orch_ol, bras_ol, api_ol, cyp_ol, cyp_ul, len(doubt_print), len(doubt_left), mono_ul, mono_ol, mono_ul_p, mono_ol_p)
p = lambda a, b: 100 * a / b

REFS = [{"page": "72", "block": "b5"}, {"page": "73", "block": "b1", "rows": "r1-r35"},
        {"page": "73", "block": "b3", "rows": "r1-r12"}, {"page": "74", "block": "b1", "rows": "r1-r45"},
        {"page": "830", "block": "b7"}, {"page": "830", "block": "b8"}, {"page": "830", "block": "b9"}, {"page": "830", "block": "b10"}]
ana = {
    "id": "flora-exklusivarten-unterland-oberland",
    "title": bi("Pflanzen, die nur im Unterland oder nur im Oberland wachsen", "Plants found only in the Unterland or only in the Oberland"),
    "category": "flora",
    "section": "t1-1-8",
    "sources": REFS + [{"page": "72", "block": "fn5"}, {"page": "72", "block": "fn6"}, {"page": "73", "block": "fn1"}, {"page": "74", "block": "fn1"},
                       {"page": "75", "block": "b2"}, {"page": "830", "block": "b11"}],
    "summary": bi(
        "Brückner druckt die Verzeichnisse der Blütenpflanzen, die ausschließlich im Unterland (Gera) beziehungsweise ausschließlich im Oberland (Schleiz, Lobenstein) vorkommen, und berichtigt sie auf S. 830 (drei Streichungen, drei Ergänzungen). Die Listen wurden Art für Art erfasst und nach Pflanzenfamilien ausgezählt: Die Unterländer Besonderheiten sind vor allem Korbblütler und Orchideen, die oberländischen Kreuzblütler, Doldenblütler und Sauergräser.",
        "Brückner prints the lists of flowering plants that occur exclusively in the Unterland (Gera) or exclusively in the Oberland (Schleiz, Lobenstein) and corrects them on p. 830 (three deletions, three additions). The lists were captured species by species and counted by plant family: the Unterland specialities are mostly composites and orchids, those of the Oberland crucifers, umbellifers and sedges."),
    "method": bi(
        f"Die vier Listen (S. 72 Fließtext in zwei Spalten, S. 73–74 Tabellen mit zwei Spalten) wurden Zeile für Zeile erfasst; Gedankenstriche (»- pumila«) wurden zur Gattung der Zeile darüber in derselben Spalte aufgelöst, Autorenkürzel und Fußnotenzeichen weggelassen. Brückners eigene Berichtigungen auf S. 830 (Zusätze und Berichtigungen) sind eingearbeitet: Laserpitium pruthenicum, Neottia Nidus avis und Gentiana ciliata sind aus der Unterlandliste zu streichen (sie kommen auch im Oberland vor), Salvia verticillata ist im Unterland, Libanotis montana und Phyteum orbiculare sind im Oberland einzutragen, bei Nuphar luteum fällt der Stern weg, »vilosum« ist »villosum«, »Palicaria« ist Pulicaria. Der Datensatz enthält die gedruckten Zeilen mit Statusangabe (bleibt, gestrichen, Dublette) und die ergänzten Arten; gezählt wurden die Arten nach Berichtigung ({n_ul} im Unterland, {n_ol} im Oberland, die zweite Nennung von Subularia aquatica ausgenommen). Die Familienzuordnung (heutige Systematik, APG IV) und die Einteilung in Zwei- und Einkeimblättrige sind eine redaktionelle Zutat (abgeleitet), keine Angabe Brückners; sie beruht allein auf der Gattung. Brückners Namen sind Linnésche Namen des 19. Jahrhunderts und wurden nicht modernisiert. Ausgezählt wurden {len(top)} Familien mit mindestens vier Arten in einem der beiden Verzeichnisse; die übrigen {n_other_fams} Familien sind zusammengefasst (im Diagramm nicht gezeigt).",
        f"The four lists (p. 72 running text in two columns, pp. 73–74 two-column tables) were captured line by line; dashes (“- pumila”) were resolved to the genus of the line above in the same column, authority abbreviations and footnote marks were dropped. Brückner's own corrections on p. 830 (Zusätze und Berichtigungen) have been incorporated: Laserpitium pruthenicum, Neottia Nidus avis and Gentiana ciliata are to be deleted from the Unterland list (they also occur in the Oberland), Salvia verticillata is to be entered for the Unterland, Libanotis montana and Phyteum orbiculare for the Oberland, the asterisk at Nuphar luteum falls away, “vilosum” is “villosum”, “Palicaria” is Pulicaria. The dataset contains the printed lines with a status (stands, deleted, duplicate) and the added species; the species after correction were counted ({n_ul} in the Unterland, {n_ol} in the Oberland, the second mention of Subularia aquatica excluded). The family assignment (current systematics, APG IV) and the split into dicotyledons and monocotyledons are an editorial addition (derived), not a statement by Brückner; they rest on the genus alone. Brückner's names are 19th-century Linnaean names and were not modernised. {len(top)} families with at least four species in either list were counted separately; the remaining {n_other_fams} families are pooled (not shown in the chart)."),
    "findings": [
        bi(f"Gedruckt sind {n_ul_print} Arten für das Unterland und {n_ol_print} Zeilen (davon {dist_ol_print} verschiedene Namen) für das Oberland; Brückners Tabelle auf S. 72 nennt 96 und 113. Nach seinen Berichtigungen (S. 830) umfassen die Listen {n_ul} Arten im Unterland und {n_ol} im Oberland. Die Tabellenzahlen hat Brückner nicht berichtigt. Keine Art steht in beiden Listen.",
           f"Printed are {n_ul_print} species for the Unterland and {n_ol_print} lines (of them {dist_ol_print} distinct names) for the Oberland; Brückner's table on p. 72 gives 96 and 113. After his corrections (p. 830) the lists comprise {n_ul} species in the Unterland and {n_ol} in the Oberland. Brückner did not correct the table figures. No species appears in both lists."),
        bi(f"Im Unterland stellen Korbblütler ({ast_ul} Arten, {de(p(ast_ul, n_ul), 1)} %) und Orchideen ({orch_ul}, {de(p(orch_ul, n_ul), 1)} %) zusammen {de(p(ast_ul + orch_ul, n_ul), 1)} % der Besonderheiten. Im Oberland sind es nur {fam_ol['Asteraceae']} Korbblütler und {orch_ol} Orchideen.",
           f"In the Unterland composites ({ast_ul} species, {en(p(ast_ul, n_ul), 1)} %) and orchids ({orch_ul}, {en(p(orch_ul, n_ul), 1)} %) together make up {en(p(ast_ul + orch_ul, n_ul), 1)} % of the specialities. In the Oberland there are only {fam_ol['Asteraceae']} composites and {orch_ol} orchids."),
        bi(f"Im Oberland führen Kreuzblütler ({bras_ol}) und Doldenblütler ({api_ol}); zusammen sind das {de(p(bras_ol + api_ol, n_ol), 1)} % der oberländischen Arten. Sauergräser sind mit {cyp_ol} gegenüber {cyp_ul} Arten im Oberland dreieinhalbmal so häufig vertreten.",
           f"In the Oberland crucifers ({bras_ol}) and umbellifers ({api_ol}) lead; together they make up {en(p(bras_ol + api_ol, n_ol), 1)} % of the Oberland species. Sedges are represented by {cyp_ol} species in the Oberland against {cyp_ul} in the Unterland, 3.5 times as many."),
        bi("Das Muster passt zu Brückners Beschreibung des Unterlandes als luftmilder, mit Buntsandstein- und Zechsteinböden, und des Oberlandes als teich-, quell- und moorreich (S. 75, 78); es deutet darauf hin, dass die Verzeichnisse vor allem Standortunterschiede widerspiegeln. Ein Beleg dafür sind die Listen selbst nicht, da Brückner keine Standorte angibt.",
           "The pattern fits Brückner's description of the Unterland as milder in climate with Bunter sandstone and Zechstein soils, and of the Oberland as rich in ponds, springs and bogs (pp. 75, 78); it suggests that the lists mainly reflect differences in habitat. The lists themselves do not prove this, as Brückner gives no habitats."),
    ],
    "caveats": [
        bi(f"Brückner kennzeichnet {len(doubt_print)} Arten als zweifelhaft (Apocynum Venetum im Unterland; im Oberland Ranunculus Philonotis, Nuphar luteum, Saxifraga tridactylites, Rhynchospora alba und Orlaya grandiflora: »Zweifelhaft, obschon als vorkömmlich angegeben«). Zwei davon klärt er auf S. 830: Der Stern bei Nuphar luteum fällt weg, und das Apocynum von Untermhaus ist nach dem Hofgärtner Papst Apocynum Venetum. Alle sechs sind in den Daten markiert und mitgezählt.",
           f"Brückner marks {len(doubt_print)} species as doubtful (Apocynum Venetum in the Unterland; in the Oberland Ranunculus Philonotis, Nuphar luteum, Saxifraga tridactylites, Rhynchospora alba and Orlaya grandiflora: “doubtful, although given as occurring”). He settles two of them on p. 830: the asterisk at Nuphar luteum falls away, and the Apocynum of Untermhaus is, according to the court gardener Papst, Apocynum Venetum. All six are flagged in the data and counted."),
        bi(f"Die Einteilung der Namen in Ein- und Zweikeimblättrige ergibt nach den Berichtigungen im Unterland {mono_ul} Einkeimblättrige und {n_ul - mono_ul} Zweikeimblättrige (Tabelle S. 72: 25 und 71), im Oberland {mono_ol} und {n_ol - mono_ol} (Tabelle: 19 und 94); vor den Berichtigungen waren es im Unterland {mono_ul_p} und {n_ul_print - mono_ul_p}. Die Abweichungen ließen sich nicht aufklären.",
           f"Sorting the names into monocotyledons and dicotyledons gives, after the corrections, {mono_ul} monocotyledons and {n_ul - mono_ul} dicotyledons in the Unterland (table p. 72: 25 and 71), and {mono_ol} and {n_ol - mono_ol} in the Oberland (table: 19 and 94); before the corrections the Unterland had {mono_ul_p} and {n_ul_print - mono_ul_p}. The deviations could not be resolved."),
        bi("Einzelne Fundmeldungen in Brückners Text widersprechen den Listen: Geranium sylvaticum steht unter den nur im Oberland vorkommenden Arten, wird aber auf S. 76 »bei Tinz« genannt, wo der Zusammenhang das Unterland meint (vgl. die Analyse der Fundorte).",
           "A few records in Brückner's text contradict the lists: Geranium sylvaticum is listed among the species found only in the Oberland, yet p. 76 mentions it “near Tinz”, where the context means the Unterland (see the analysis of the find-spots)."),
        bi("Die Familienzuordnung folgt der heutigen Systematik; einzelne Gattungen (Cineraria, Lepigonum, Pulegium, Sarothamnus) tragen bei Brückner Namen, die heute als Synonyme gelten und hier nach der Gattung eingeordnet wurden.",
           "The family assignment follows current systematics; a few genera (Cineraria, Lepigonum, Pulegium, Sarothamnus) carry names in Brückner that are now synonyms and were placed by genus."),
    ],
    "transcription_issues": [
        {"page": "72", "block": "b5", "transcribed": "Pulicaria dysenterica, Grtn.", "facsimile": "Palicaria dysenterica, Grtn.", "checked_facsimile": True,
         "note": "Das Faksimile hat »Palicaria«; Brückner berichtigt auf S. 830: »lies: Pulicaria statt Palicaria« (Z. 11 v. u.). Die Transkription hat die Berichtigung stillschweigend vorweggenommen."},
    ],
    "datasets": [
        {"name": "species",
         "title": bi("Nur im Unterland bzw. nur im Oberland vorkommende Phanerogamen (S. 72–74, mit Berichtigungen S. 830)", "Phanerogams found only in the Unterland or only in the Oberland (pp. 72–74, with corrections p. 830)"),
         "columns": [
             col("region_de", "Vorkommen", "Occurrence", "string", None, True, "nach der Überschrift der Liste"),
             col("region_en", "Vorkommen (EN)", "Occurrence (EN)", "string", None, True),
             col("name", "Name bei Brückner", "Name in Brückner", "string", None, False, "Gattung + Art, Gedankenstriche aufgelöst"),
             col("name_corrected", "Name nach Berichtigung", "Name after correction", "string", None),
             col("genus", "Gattung", "Genus", "string", None),
             col("family", "Familie (heutige Systematik)", "Family (current systematics)", "string", None, True, "redaktionelle Zuordnung nach der Gattung"),
             col("class_de", "Klasse", "Class", "string", None, True),
             col("class_en", "Klasse (EN)", "Class (EN)", "string", None, True),
             col("status_key", "Status (Schlüssel)", "Status (key)", "string", None, True),
             col("status_de", "Status", "Status", "string", None, True),
             col("status_en", "Status (EN)", "Status (EN)", "string", None, True),
             col("doubtful", "Im Druck als zweifelhaft bezeichnet", "Marked as doubtful in print", "string", None),
             col("note", "Anmerkung", "Note", "string", None),
             col("correction", "Berichtigung (S. 830)", "Correction (p. 830)", "string", None),
             col("page", "Seite", "Page", "string", None),
             col("block", "Block", "Block", "string", None),
         ],
         "rows": rows, "source_refs": REFS},
        {"name": "family_counts",
         "title": bi("Exklusivarten nach Familie (nach Berichtigung)", "Exclusive species by family (after correction)"),
         "columns": [
             col("region_de", "Vorkommen", "Occurrence", "string", None, True),
             col("region_en", "Vorkommen (EN)", "Occurrence (EN)", "string", None, True),
             col("family_de", "Familie", "Family", "string", None, True),
             col("family_en", "Familie (EN)", "Family (EN)", "string", None, True),
             col("family_order", "Reihenfolge", "Order", "integer", None, True),
             col("species", "Arten", "Species", "integer", "Arten", True),
             col("share_pct", "Anteil an der Liste", "Share of the list", "number", "%", True),
         ],
         "rows": fam_rows, "source_refs": REFS},
    ],
    "charts": [
        {"id": "c1", "dataset": "family_counts",
         "title": bi("Welche Pflanzenfamilien sind nur im Unter- oder nur im Oberland vertreten?", "Which plant families occur only in the Unterland or only in the Oberland?"),
         "caption": bi(f"Zahl der Arten je Familie in den beiden Exklusivlisten nach Brückners Berichtigungen (Familien mit mindestens vier Arten in einer Liste; Familienzuordnung redaktionell). Nicht dargestellt sind {n_other_fams} weitere Familien mit zusammen {oth_ul} (Unterland) und {oth_ol} (Oberland) Arten.",
                       f"Number of species per family in the two exclusive lists after Brückner's corrections (families with at least four species in one list; family assignment editorial). Not shown are {n_other_fams} further families with {oth_ul} (Unterland) and {oth_ol} (Oberland) species in total."),
         "vegalite": {"height": 380, "mark": "bar",
                      "encoding": {
                          "y": {"field": {"de": "family_de", "en": "family_en"}, "type": "nominal", "sort": {"field": "family_order", "op": "min"}, "title": None},
                          "yOffset": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal",
                                      "sort": [{"de": "Nur im Unterland", "en": "Unterland only"}, {"de": "Nur im Oberland", "en": "Oberland only"}]},
                          "x": {"field": "species", "type": "quantitative", "title": bi("Arten", "Species")},
                          "color": {"field": {"de": "region_de", "en": "region_en"}, "type": "nominal", "title": bi("Vorkommen", "Occurrence"),
                                    "scale": {"domain": [{"de": "Nur im Unterland", "en": "Unterland only"}, {"de": "Nur im Oberland", "en": "Oberland only"}]}},
                          "tooltip": [{"field": {"de": "family_de", "en": "family_en"}, "title": bi("Familie", "Family")},
                                      {"field": {"de": "region_de", "en": "region_en"}, "title": bi("Vorkommen", "Occurrence")},
                                      {"field": "species", "title": bi("Arten", "Species")},
                                      {"field": "share_pct", "title": bi("% der Liste", "% of the list")}]}}},
    ],
    "keywords": {"de": ["Flora", "Unterland", "Oberland", "Pflanzenfamilien", "Orchideen", "Korbblütler", "Kreuzblütler", "Seltenheiten", "Phanerogamen", "Berichtigungen"],
                 "en": ["flora", "Unterland", "Oberland", "plant families", "orchids", "composites", "crucifers", "rarities", "phanerogams", "corrigenda"]},
    "related": ["flora-artenzahlen-phanerogamen-kryptogamen", "flora-seltene-pflanzen-fundorte"],
    "generated_by": GEN,
    "date": DATE,
}
write(ana)
