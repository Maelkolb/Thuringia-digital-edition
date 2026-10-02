"""Analysis geologie-fossilfunde-zechstein-clymenienkalk: fossil finds listed by Brückner/Liebe (pp. 35, 38)."""
import re
from common import *

M = lambda de_, en_: {"de": de_, "en": en_}

# ---- Zechstein of Gera (p. 38 b1) -----------------------------------------------------------------
t38 = text("38", "b1")
seg = t38[t38.index("Es wurden bis jetzt daselbst gesammelt:") + len("Es wurden bis jetzt daselbst gesammelt:"):]
seg = seg[: seg.index("andere Pflanzen") + len("andere Pflanzen")]
items = [x.strip() for x in seg.split("—")]
zech = []
for it in items:
    m = re.match(r"^(über\s+)?(\d+)\s+(?:Arten\s+)?(.*?)(?:,\s*worunter.*|\s+2c\.|\s+und noch.*)?$", it)
    if not m:
        print("NO MATCH", it)
        continue
    zech.append([m.group(1) is not None, int(m.group(2)), m.group(3).strip()])
for z in zech:
    print(z)
assert len(zech) == 14, len(zech)

ZINFO = {
    # German name as printed -> (English, group)
    "Fische": ("fishes", "vertebrate"),
    "Schwimmkrebse": ("ostracods (“swimming crustaceans”)", "arthropod"),
    "Röhrenwürmer": ("tube worms", "other"),
    "Kammschnecke": ("chambered snail (nautiloid)", "mollusc"),
    "Seeschnecken": ("sea snails", "mollusc"),
    "ächte Muscheln": ("true bivalves", "mollusc"),
    "Armfußmuscheln": ("brachiopods (lamp shells)", "brachiopod"),
    "Strahlthiere": ("echinoderms (“radiates”)", "other"),
    "Corallen": ("corals", "other"),
    "Wurzelfüßer": ("foraminifera (rhizopods)", "other"),
    "Seeschwämme": ("sponges", "other"),
    "Seetange": ("seaweeds", "plant"),
    "Farne": ("ferns", "plant"),
    "Nadelhölzer": ("conifers", "plant"),
}
zrows = []
for i, (over, n, name) in enumerate(zech, 1):
    # transcription reads "Kammschnecke"; the print has "Kammerschnecke" (checked at the facsimile)
    key = name
    en_, grp = ZINFO[key]
    printed = "Kammerschnecke" if key == "Kammschnecke" else name
    zrows.append([i, printed, en_, grp, "über" if over else "", n])
zsum = sum(r[5] for r in zrows)
print("Zechstein total", zsum)

# ---- Clymenienkalk (p. 35 b1) ---------------------------------------------------------------------
t35 = text("35", "b1")
start = t35.index("Es sind bis jetzt in diesen drei Etagen innerhalb des Gebietes gefunden worden:")
seg2 = t35[start:]
seg2 = seg2[seg2.index(":") + 1: seg2.index("Korallen und Seeschwämme") + len("Korallen und Seeschwämme")]
print(seg2)
WORD = {"ein": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8}
pat = re.compile(r"\b(zwei|drei|vier|fünf|sechs|acht|sieben)\s+(?:Arten\s+(?:von\s+)?)?([A-ZÄÖÜ][\wäöüß]+)")
found = [(WORD[a], b) for a, b in pat.findall(seg2) if b != 'Tantaculiten']  # 'worunter drei Tantaculiten' is a subset of the five Schwimmschnecken
print(found)
CINFO = {
    "Schwimmkrebsen": ("Schwimmkrebse", "ostracods (“swimming crustaceans”)", "arthropod"),
    "Ruderkrebse": ("Ruderkrebse", "trilobites (“oar crustaceans”)", "arthropod"),
    "Gradhorn": ("Gradhorn", "straight-horn cephalopods (Orthoceras)", "mollusc"),
    "Keulenhorn": ("Keulenhorn", "club-horn cephalopods", "mollusc"),
    "Clymenien": ("Clymenien", "clymenias (coiled cephalopods)", "mollusc"),
    "Goniatiten": ("Goniatiten", "goniatites (coiled cephalopods)", "mollusc"),
    "Schwimmschnecken": ("Schwimmschnecken", "swimming snails (incl. 3 tentaculites)", "mollusc"),
    "Seeschnecken": ("Seeschnecken", "sea snails", "mollusc"),
    "Muscheln": ("Muscheln", "bivalves", "mollusc"),
}
crows = []
for i, (n, name) in enumerate(found, 1):
    de_, en_, grp = CINFO[name]
    crows.append([i, de_, en_, grp, n])
assert len(crows) == 9, crows
csum = sum(r[4] for r in crows)
print("Clymenien total", csum)

# ---- derived shares -------------------------------------------------------------------------------
z_by_grp = {}
for r in zrows:
    z_by_grp[r[3]] = z_by_grp.get(r[3], 0) + r[5]
c_by_grp = {}
for r in crows:
    c_by_grp[r[3]] = c_by_grp.get(r[3], 0) + r[4]
print(z_by_grp, c_by_grp)
z_inv_marine = zsum - z_by_grp["plant"] - z_by_grp["vertebrate"]
ceph_c = sum(r[4] for r in crows if r[1] in ("Gradhorn", "Keulenhorn", "Clymenien", "Goniatiten"))
mol_z = z_by_grp["mollusc"]
brach_z = z_by_grp["brachiopod"]
pc = lambda a, b: a / b * 100
top_z = sorted(zrows, key=lambda r: -r[5])[:3]
top_c = sorted(crows, key=lambda r: -r[4])[:3]

findings = [
    M(f"Für den Zechstein von Gera nennt Liebe {zsum} Arten in {len(zrows)} Gruppen (»über 7 Arten Schwimmkrebse« als 7 gezählt; dazu »noch eine Anzahl andere Pflanzen«). Am artenreichsten sind {top_z[0][1]} ({top_z[0][5]}), {top_z[1][1]} ({top_z[1][5]}) und {top_z[2][1]} ({top_z[2][5]}).",
      f"For the Zechstein of Gera Liebe names {zsum} species in {len(zrows)} groups (“over 7 species of Schwimmkrebse” counted as 7; plus “a number of other plants”). The groups richest in species are {top_z[0][2]} ({top_z[0][5]}), {top_z[1][2]} ({top_z[1][5]}) and {top_z[2][2]} ({top_z[2][5]})."),
    M(f"Weichtiere ({mol_z} Arten) und Armfüßer ({brach_z}) stellen zusammen {de(pc(mol_z+brach_z,zsum),0)} % der gezählten Zechstein-Arten; Pflanzen kommen auf {z_by_grp['plant']} Arten ({de(pc(z_by_grp['plant'],zsum),0)} %).",
      f"Molluscs ({mol_z} species) and brachiopods ({brach_z}) together make up {en(pc(mol_z+brach_z,zsum),0)} % of the counted Zechstein species; plants account for {z_by_grp['plant']} species ({en(pc(z_by_grp['plant'],zsum),0)} %)."),
    M(f"Im Clymenienkalk zählt Liebe {csum} Arten; die Hälfte davon ({ceph_c} Arten, {de(pc(ceph_c,csum),0)} %) sind Kopffüßer (von Liebe als »Kammerschnecken« zusammengefasst: Gradhorn, Keulenhorn, Clymenien, Goniatiten), allen voran die {top_c[0][1]} mit {top_c[0][4]} Arten. Korallen und Seeschwämme werden ohne Zahl erwähnt.",
      f"For the Clymenia limestone Liebe counts {csum} species; half of them ({ceph_c} species, {en(pc(ceph_c,csum),0)} %) are cephalopods (grouped by Liebe as “Kammerschnecken”: Gradhorn, Keulenhorn, Clymenien, Goniatiten), led by the {top_c[0][2]} with {top_c[0][4]} species. Corals and sponges are mentioned without a number."),
    M("Beide Listen sind Zwischenstände (»bis jetzt gesammelt«, »bis jetzt gefunden«); Brückner bzw. sein Gewährsmann Liebe weist selbst darauf hin, dass weitere Funde zu erwarten sind (S. 41: Knochenlehme »werden noch an vielen anderen Punkten nachgewiesen werden«).",
      "Both lists are interim tallies (“so far collected”, “so far found”); the author of the section, Liebe, himself expects further finds (p. 41 on bone-bearing loams: “will still be found at many other places”)."),
]
# the last finding refers to p. 40 (13 b); fix the page reference by checking the text
assert "werden noch an vielen anderen Punkten nachgewiesen werden" in text("40", "b5")
findings[3] = M("Beide Listen sind Zwischenstände (»bis jetzt gesammelt«, »bis jetzt gefunden«); der Verfasser des Abschnitts, Prof. Liebe, rechnet selbst mit weiteren Funden (S. 40 zu den knochenführenden Lehmlagern: »werden noch an vielen anderen Punkten nachgewiesen werden«).",
                "Both lists are interim tallies (“so far collected”, “so far found”); the author of the section, Prof. Liebe, himself expects further finds (p. 40 on the bone-bearing loam deposits: “will still be found at many other places”).")
for f in findings:
    print(f["de"])

ZCOLS = [
    {"name": "order", "label": M("Reihenfolge im Text", "Order in the text"), "type": "integer", "unit": None, "derived": True},
    {"name": "taxon", "label": M("Gruppe (wie gedruckt)", "Group (as printed)"), "type": "string", "unit": None, "note": "»Kammerschnecke« im Druck; die Textübertragung liest »Kammschnecke« (Faksimile S. 38 geprüft)."},
    {"name": "taxon_en", "label": M("Gruppe (englisch, modern)", "Group (English, modern)"), "type": "string", "unit": None, "derived": True},
    {"name": "taxon_group", "label": M("Großgruppe", "Major group"), "type": "string", "unit": None, "derived": True, "note": "editorische Einteilung"},
    {"name": "qualifier", "label": M("Zusatz", "Qualifier"), "type": "string", "unit": None, "note": "»über« = Mindestzahl"},
    {"name": "species", "label": M("Zahl der Arten", "Number of species"), "type": "integer", "unit": "Arten", "note": "Bei »3 Röhrenwürmer« u. ä. nennt der Text keine Einheit; gemeint sind vermutlich Arten."},
]
CCOLS = [
    {"name": "order", "label": M("Reihenfolge im Text", "Order in the text"), "type": "integer", "unit": None, "derived": True},
    {"name": "taxon", "label": M("Gruppe (wie gedruckt)", "Group (as printed)"), "type": "string", "unit": None},
    {"name": "taxon_en", "label": M("Gruppe (englisch, modern)", "Group (English, modern)"), "type": "string", "unit": None, "derived": True},
    {"name": "taxon_group", "label": M("Großgruppe", "Major group"), "type": "string", "unit": None, "derived": True, "note": "editorische Einteilung"},
    {"name": "species", "label": M("Zahl der Arten", "Number of species"), "type": "integer", "unit": "Arten", "derived": True, "note": "Im Druck als Zahlwörter (vier, zwei, …) geschrieben und hier in Ziffern übertragen."},
]

TT = lambda f, d, e: {"field": f, "title": M(d, e)}
GL = {"calculate": {"de": "datum.taxon_group == 'vertebrate' ? 'Wirbeltiere' : datum.taxon_group == 'arthropod' ? 'Krebstiere' : datum.taxon_group == 'mollusc' ? 'Weichtiere' : datum.taxon_group == 'brachiopod' ? 'Armfüßer' : datum.taxon_group == 'other' ? 'übrige Wirbellose' : 'Pflanzen'",
                    "en": "datum.taxon_group == 'vertebrate' ? 'Vertebrates' : datum.taxon_group == 'arthropod' ? 'Crustaceans' : datum.taxon_group == 'mollusc' ? 'Molluscs' : datum.taxon_group == 'brachiopod' ? 'Brachiopods' : datum.taxon_group == 'other' ? 'Other invertebrates' : 'Plants'"},
      "as": "group_l"}
TL = {"calculate": {"de": "datum.taxon", "en": "datum.taxon_en"}, "as": "taxon_l"}
ALL_GROUPS = ["mollusc", "brachiopod", "arthropod", "other", "vertebrate", "plant"]
LEGEND_EXPR = {"de": "datum.value == 'vertebrate' ? 'Wirbeltiere' : datum.value == 'arthropod' ? 'Krebstiere' : datum.value == 'mollusc' ? 'Weichtiere' : datum.value == 'brachiopod' ? 'Armfüßer' : datum.value == 'other' ? 'übrige Wirbellose' : 'Pflanzen'",
               "en": "datum.value == 'vertebrate' ? 'Vertebrates' : datum.value == 'arthropod' ? 'Crustaceans' : datum.value == 'mollusc' ? 'Molluscs' : datum.value == 'brachiopod' ? 'Brachiopods' : datum.value == 'other' ? 'Other invertebrates' : 'Plants'"}


def chart(h, present):
    return {
        "height": h,
        "transform": [GL, TL],
        "mark": "bar",
        "encoding": {
            "y": {"field": "taxon_l", "type": "nominal", "title": None, "sort": {"field": "species", "op": "max", "order": "descending"}, "axis": {"labelLimit": 260}},
            "x": {"field": "species", "type": "quantitative", "title": M("Zahl der Arten", "Number of species"), "axis": {"tickMinStep": 1}},
            "color": {"field": "taxon_group", "type": "nominal", "title": None, "scale": {"domain": ALL_GROUPS},
                      "legend": {"values": [g for g in ALL_GROUPS if g in present], "labelExpr": LEGEND_EXPR, "columns": 3}},
            "tooltip": [TT("taxon", "Gruppe (gedruckt)", "Group (as printed)"), TT("taxon_en", "Modern", "Modern"), TT("group_l", "Großgruppe", "Major group"), TT("species", "Arten", "Species")],
        },
    }


SRC = [{"page": "35", "block": "b1"}, {"page": "38", "block": "b1"}]
ana = {
    "id": "geologie-fossilfunde-zechstein-clymenienkalk",
    "title": M("Versteinerungen im Zechstein von Gera und im Clymenienkalk", "Fossils of the Zechstein at Gera and of the Clymenia limestone"),
    "category": "geology",
    "section": "t1-1-5",
    "sources": SRC,
    "summary": M(
        f"In der geognostischen Übersicht von Prof. Liebe stehen für zwei Formationen Zählungen der bisher im Land gefundenen Versteinerungen: der Zechstein von Gera (»bei den Geognosten berühmt«) mit {len(zrows)} Gruppen und der devonische Clymenienkalk mit {len(crows)} Gruppen. Die Auswertung ordnet die Gruppen modernen Großgruppen zu und zeigt, welche Tierklassen jeweils überwiegen.",
        f"In the geological overview by Prof. Liebe two formations come with tallies of the fossils found so far in the country: the Zechstein of Gera (“famous among geognosts”) with {len(zrows)} groups and the Devonian Clymenia limestone with {len(crows)} groups. The analysis assigns the groups to modern major groups and shows which classes of animals predominate in each."),
    "method": M(
        "Die Artenzahlen wurden aus den Aufzählungen S. 38 (Zechstein) und S. 35 (Clymenienkalk) per Textmuster übernommen; Zahlwörter (»vier«, »sechs« …) sind in Ziffern gesetzt. »Über 7 Arten« ist als 7 gezählt. Die modernen Großgruppen (Weichtiere, Armfüßer, Krebstiere usw.) und die englischen Namen sind editorisch; die Gruppen sind so benannt, wie Liebe sie nennt (z. B. Schwimmkrebse = Ostrakoden, Ruderkrebse = Trilobiten, Gradhorn = Orthoceras; vgl. S. 30 und 34). Bei den Pflanzen des Zechsteins nennt der Text zusätzlich »noch eine Anzahl andere Pflanzen« ohne Zahl; bei den Korallen und Seeschwämmen des Clymenienkalks fehlt die Zahl ebenfalls. Beides ist nicht in den Summen enthalten.",
        "Species counts were taken from the lists on p. 38 (Zechstein) and p. 35 (Clymenia limestone) by text pattern; number words (“vier”, “sechs” …) were set in digits. “Over 7 species” is counted as 7. The modern major groups (molluscs, brachiopods, crustaceans etc.) and the English names are editorial; the groups are named as Liebe names them (e.g. Schwimmkrebse = ostracods, Ruderkrebse = trilobites, Gradhorn = Orthoceras; cf. pp. 30 and 34). For the Zechstein plants the text adds “a number of other plants” without a figure; for the corals and sponges of the Clymenia limestone the figure is also missing. Neither is included in the totals."),
    "findings": findings,
    "caveats": [
        M("Die Einteilung nach modernen Großgruppen ist eine Deutung; Begriffe wie »Strahlthiere« oder »Wurzelfüßer« hatten 1870 teils andere Umfänge als heute.",
          "The division into modern major groups is an interpretation; terms such as “Strahlthiere” or “Wurzelfüßer” partly had a different scope in 1870 than today."),
        M("Die Zahlen stammen aus Liebes Wissensstand von 1870; sie sind Mindestzahlen, vor allem bei den mit »über« oder ohne Zahl genannten Gruppen.",
          "The figures reflect Liebe's knowledge of 1870; they are minimum counts, above all for groups given with “over” or without a number."),
        M("Zechstein und Clymenienkalk werden in unterschiedlicher Gruppengliederung aufgezählt; die Gesamtzahlen (Zechstein vs. Clymenienkalk) sind daher nur eingeschränkt vergleichbar.",
          "Zechstein and Clymenia limestone are listed with different group divisions; their totals are therefore only partly comparable."),
    ],
    "datasets": [
        {"name": "zechstein", "title": M("Funde im Zechstein von Gera", "Finds in the Zechstein of Gera"), "columns": ZCOLS, "rows": zrows, "source_refs": [{"page": "38", "block": "b1"}]},
        {"name": "clymenien", "title": M("Funde im Clymenienkalk", "Finds in the Clymenia limestone"), "columns": CCOLS, "rows": crows, "source_refs": [{"page": "35", "block": "b1"}]},
    ],
    "charts": [
        {"id": "c1", "dataset": "zechstein",
         "title": M("Zechstein von Gera: gefundene Arten nach Gruppe", "Zechstein of Gera: species found by group"),
         "caption": M(f"Zahl der von Liebe genannten Arten je Gruppe (insgesamt {zsum}); »Schwimmkrebse« mindestens 7. Pflanzen ohne Zahl (»eine Anzahl andere«) sind nicht enthalten.",
                      f"Number of species named by Liebe per group ({zsum} in total); Schwimmkrebse at least 7. Plants without a figure (“a number of others”) are not included."),
         "vegalite": chart(380, {r[3] for r in zrows})},
        {"id": "c2", "dataset": "clymenien",
         "title": M("Clymenienkalk: gefundene Arten nach Gruppe", "Clymenia limestone: species found by group"),
         "caption": M(f"Zahl der Arten je Gruppe (insgesamt {csum}); Korallen und Seeschwämme sind ohne Zahl genannt und fehlen. Die »Schwimmschnecken« schließen drei Tentaculiten ein.",
                      f"Number of species per group ({csum} in total); corals and sponges are named without a figure and are missing. The “Schwimmschnecken” include three tentaculites."),
         "vegalite": chart(300, {r[3] for r in crows})},
    ],
    "transcription_issues": [
        {"page": "38", "block": "b1", "transcribed": "1 Kammschnecke", "facsimile": "1 Kammerschnecke", "checked_facsimile": True,
         "note": "Wortlaut in der Aufzählung der Gera-Zechstein-Fossilien; die Zahlen (7, 7, 3, 1, 9, 25, 20, 2, 8, 2, 2, 3, 2, 4) wurden am Faksimile bestätigt."},
    ],
    "keywords": {"de": ["Versteinerungen", "Fossilien", "Zechstein", "Gera", "Clymenienkalk", "Devon", "Liebe", "Geologie", "Muscheln", "Goniatiten"],
                 "en": ["fossils", "petrifactions", "Zechstein", "Gera", "Clymenia limestone", "Devonian", "Liebe", "geology", "bivalves", "goniatites"]},
    "generated_by": "Claude Sonnet 5.5 (subagent A02)",
    "date": "2026-10-01",
}
write_analysis(ana)
